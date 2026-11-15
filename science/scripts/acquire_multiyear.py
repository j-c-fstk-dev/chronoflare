"""Resume a frozen FIRMS acquisition with verified cache entries and bounded retries."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import time

from acquisition_plan import fingerprint, load_plan
from firms_download import ENDPOINT, DownloadError, download_area, validate_csv, validate_request
from normalize_detections import file_hash

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = PROJECT / "science/configs/acquisition_plan.json"


def write_json(path, value):
    temporary = path.with_suffix(".partial")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def verify_entry(root, request):
    directory = root / "raw" / request["id"]
    if directory.is_symlink() or any((directory / name).is_symlink() for name in ("detections.csv", "provenance.json")):
        raise ValueError("Cache symlinks are not supported")
    metadata = json.loads((directory / "provenance.json").read_text())
    bounds, start, end = validate_request(request["source"], request["bbox"], request["start"], request["days"])
    path = directory / "detections.csv"
    if (metadata.get("source") != request["source"] or metadata.get("bbox") != list(bounds)
        or metadata.get("requested_start_utc") != start.isoformat() or metadata.get("requested_end_utc_inclusive") != end.isoformat()
        or metadata.get("endpoint") != ENDPOINT or metadata.get("processing_level") != "SP"
        or metadata.get("sha256") != file_hash(path) or metadata.get("bytes") != path.stat().st_size
        or metadata.get("row_count") != validate_csv(path.read_bytes(), bounds, start, end)):
        raise ValueError("Cache entry failed source, bounds, date, size, count or hash validation")
    return {"id": request["id"], "block_id": request["block_id"], "source": request["source"],
            "start": request["start"], "days": request["days"],
            **{key: metadata[key] for key in ("sha256", "bytes", "row_count", "retrieved_at_utc")}}


@contextmanager
def acquisition_lock(root):
    with (root / ".acquisition.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another acquisition owns this cache") from None
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def acquire(*, root, plan_path=DEFAULT_PLAN, map_key=None, max_new_requests=416, downloader=download_area, sleep=time.sleep, delay=1.):
    plan = load_plan(plan_path)
    root = root.resolve()
    if any(root.is_relative_to(PROJECT / name) for name in ("app", "dist")):
        raise ValueError("Use an offline cache outside application assets")
    if type(max_new_requests) is not int or not 0 <= max_new_requests <= plan["request_count"]:
        raise ValueError("Request budget is outside the frozen plan")
    root.mkdir(parents=True, exist_ok=True)
    if (root / "raw").is_symlink(): raise ValueError("Cache symlinks are not supported")
    (root / "raw").mkdir(exist_ok=True)
    with acquisition_lock(root):
        plan_file = root / "plan.json"
        if plan_file.exists():
            if json.loads(plan_file.read_text()) != plan: raise ValueError("Existing cache belongs to another plan")
        else:
            write_json(plan_file, plan)
        entries, attempts, failures = [], 0, []
        def snapshot():
            result = {"schema_version": "multiyear-acquisition-evidence/1.0.0", "plan_fingerprint": fingerprint(plan),
                      "completed_requests": len(entries), "planned_requests": plan["request_count"],
                      "new_request_attempts": attempts, "complete": len(entries) == plan["request_count"],
                      "requests": entries, "failures": failures, "coverage_status": "unknown", "harmonization_approved": False}
            write_json(root / "manifest.json", result)
            return result
        # Validate every existing entry before spending the next request budget.
        existing = set()
        for request in plan["requests"]:
            if (root / "raw" / request["id"]).exists():
                entries.append(verify_entry(root, request)); existing.add(request["id"])
        snapshot()
        for request in plan["requests"]:
            if request["id"] in existing: continue
            if attempts >= max_new_requests: break
            success = False
            for retry in range(3):
                if attempts >= max_new_requests: break
                attempts += 1
                sleep(delay if retry == 0 else 15 * retry)
                try:
                    downloader(source=request["source"], bbox=request["bbox"], start=request["start"], days=request["days"],
                               output=root / "raw" / request["id"], map_key=map_key)
                    entries.append(verify_entry(root, request))
                    success = True
                    print(f"Verified {len(entries)}/{plan['request_count']} requests", flush=True)
                    snapshot()
                    break
                except DownloadError as error:
                    message = str(error)
                    category = ("rate_limit" if "rate limit" in message else "response_schema" if "schema" in message else "request_or_provider" if "HTTP" in message else "transport_or_validation")
                    print(f"Request attempt failed: {category}; retry budget remains bounded", flush=True)
                    # Do not print upstream responses, exceptions or credential-bearing URLs.
                    if (root / "raw" / request["id"]).exists(): raise ValueError("Partial cache entry needs offline investigation") from None
            if not success:
                failures.append({"id": request["id"], "reason": "provider_or_transport_failed_or_budget_exhausted"})
                break
        return snapshot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", dest="root", type=Path, required=True)
    parser.add_argument("--max-new-requests", type=int, default=416)
    args = parser.parse_args()
    try:
        report = acquire(**vars(args), map_key=os.environ.get("FIRMS_MAP_KEY"))
    except (ValueError, OSError, KeyError, DownloadError):
        parser.exit(1, "Error: acquisition failed; preserved cache requires review.\n")
    print(json.dumps({key: report[key] for key in ("completed_requests", "planned_requests", "new_request_attempts", "complete")}))
    if report["failures"]: raise SystemExit(1)
