# ChronoFlare

**Understanding fire activity through time.**

Explore satellite-detected fire activity through time with MODIS and VIIRS, making sensor provenance, coverage, and uncertainty visible. An independent NASA Space Apps project; not an official NASA product.

## Current status

The default calendar and annual comparisons use **synthetic fire-activity data**. A separate **experimental real-detection solar calendar** covers August 1–15, 2020, with Terra, Aqua and S-NPP kept separate and observation coverage unknown. The Map has a **separate unreviewed detection batch for August 1–15, 2020**, supplied by the team from FIRMS. The map offers the full Brazil download and an optional point-centre subset using the verified IBGE 2025 Pantanal boundary; coverage assessment and scientific validation are still pending. Harmonization is disabled until approval.

Available now:

- An [experimental solar calendar](docs/experimental-solar-calendar.md), selected through **Calendar dataset**, with real API detections, complete input time windows, an explicitly unapproved quality-filter option and traceable CSV hashes. Its [source inspector](docs/solar-detection-inspector.md) maps and lists the exact records behind each selected cell.
- Daily year-by-month/day calendar, original MODIS/VIIRS bases, date selection, details, and same-day comparisons across years.
- Calendar, Map, and Methodology views with validated date/base/comparison links, availability-aware defaults, and browser Back/Forward support. See [selection and navigation](docs/selection-navigation.md).
- An interactive [detection explorer](docs/detection-explorer.md): Brazil/Pantanal geographic views, separate MODIS/VIIRS layers, UTC date/platform filters, display grouping, point details and an accessible record table. A dark OpenStreetMap background, optional NASA GIBS imagery and [MapBiomas 2020 land-cover context](docs/mapbiomas-context.md) provide geographic context. Detections remain unreviewed and independent of the synthetic calendar.
- An **offline NASA FIRMS SP download client**, preserving original CSVs and SHA-256 provenance. A MAP_KEY is required; an authenticated historical MODIS request has passed. The [historical pilot](docs/firms-pilot-ingestion.md) reconciles API records against the existing regional reference.
- An offline CSV normalizer that preserves raw fields and provenance, validates technical fields, and produces unreviewed raw-detection JSONL without applying pending scientific rules. See [raw-ingestion setup](docs/raw-ingestion.md).
- A tested [annual-comparison adapter and chart](docs/annual-comparison.md), two-year/source controls, keyboard day inspection and offline `npm run data:compare` command, preserving gaps and leap days.
- Runtime dataset validation, automated tests, CI, and Vercel configuration.

Seasonal references, anomalies, uncertainty intervals, H3 fire layers, calibration, and scientific diagnostics must come from reviewed offline outputs. They are not inferred from context imagery.

## Quick start

Use Node.js 22.12+ or 24. Python 3.12+ is needed for offline processing/tests. Offline geospatial processing requires Shapely, pyshp and pyproj from `science/requirements.txt`; the downloader and normalizer use the standard library.

```sh
npm ci
npm run dev
```

Open the Vite URL printed in the terminal. To verify the application:

```sh
npm test
python3 -m pip install -r science/requirements.txt
npm run test:science
npm run data:validate
npm run build
```

Optional live connectivity check (Node.js 24.5+, not run in CI; honors proxy environment variables):

```sh
npm run sources:check
```

This checks a public GIBS JPEG, not fire coverage or scientific validity. The map loads detection assets on demand and handles imagery failures independently of its records and the calendar.

## External sources

**NASA GIBS:** connected directly from the browser for visual context, without credentials. The imagery date is the review window's last UTC date; the regional aggregation helper separately uses the fixed −56.65° mean solar reference. Missing imagery does not mean zero fire. See [GIBS API documentation](https://nasa-gibs.github.io/gibs-api-docs/access-basics/).

**NASA FIRMS:** the download client makes one explicit, bounded SP request (1–5 days), using `FIRMS_MAP_KEY` from the local environment. Raw downloads stay outside the frontend. See [external-source setup](docs/external-sources.md) for key setup, an example command, provenance, and current limits. No backend, database, or authenticated browser API is required.

## Scientific handoff

Read the [current map delivery update](docs/project-status/2026-11-14/regional-delivery-update.md), [coverage proposal review](docs/coverage-delivery-review.md), [delivery contract](docs/data-handoff.md), [blueprint v1.2](docs/blueprint-v1.2.md), and [validation status](docs/validation-report.md). Executable schemas live in `app/src/data/schema.ts`.

The frontend serves derived static artifacts from `app/public/data/v1/`. Replace the complete fixture package with consistent reviewed outputs and run:

```sh
npm run data:validate -- --real
```

This is a structural check, not scientific approval. The offline FIRMS downloader does not produce frontend aggregates, establish coverage, select platforms, calibrate sensors, or authorize `data_status=real`.

`npm run fixtures` regenerates deterministic synthetic artifacts. **Do not run it after integrating real data:** it replaces the fixture paths under `app/public/data/v1/`. The build never runs it automatically.

## Deploy to Vercel

Import this repository with the repository root as the Root Directory. `vercel.json` sets `npm run build` and the `dist/` output. Views use query parameters, so no SPA rewrite is needed. This change does not create or verify a deployment. Never add the FIRMS key to frontend environment variables; GIBS needs no key.

## Repository

```text
app/src/                 React UI, source adapters, schemas, tests
app/public/data/v1/      Static derived artifacts (currently synthetic)
app/public/data/detection-review/v1/  Separate unreviewed regional detections
science/scripts/        Offline FIRMS download and raw CSV normalization
science/tests/          Offline acquisition/intake tests; no live credentials
science/configs/        Registered protocols, thresholds and scientific decisions
scripts/                Fixture generation, data validation, source smoke check
docs/                   Blueprint, scientific handoff, external-source setup
```

## Next milestones

- Science pipeline: complete the fixed multi-year source acquisition, audit real support, fit independent training-only models and evaluate the registered Plan A/B criteria.
- André: review the source-bound scientific evidence and any future publication candidate; deliveries 3 and 4 are already registered.
- Application: integrate reviewed H3/GeoJSON fire layers, scientific charts, and full-year comparisons.
- Team: browser/device QA, scientific and code review, Vercel deployment, and presentation materials.

## Interpretation and AI disclosure

FRP is radiative power, not total energy or burned area. Thermal detections are not confirmed individual fires. Original sensor scales are not directly comparable; missing observations are not zeros. Estimates before 2012 are extrapolations without direct VIIRS validation. This is not a forecasting or emergency-response service.

Built with React, TypeScript, Vite, Zod, Leaflet, Python and Shapely for offline geometry checks. Codex assisted with implementation and documentation. Human review of code, interface, and scientific claims is required before submission; empirical results come from the source-bound offline pipeline and frozen validation reports, separate from synthetic application fixtures. Project license remains to be selected by the team.

## Project language

English is the working language for the interface, accessibility labels, CLI output, tests, documentation, commit messages, and pull requests. Run `npm run language:check` before submitting changes; CI checks common Portuguese regressions. Documents specifically addressed to André under `docs/handoff/` may remain in Portuguese; proper names such as André and Pantanal retain their spelling. The Portuguese README has been retired under the current English-only requirement.

The Calendar dataset selector also offers a separate
[experimental real-detection solar calendar](docs/experimental-solar-calendar.md)
for August 1–15, 2020. Platforms stay separate, quality filtering is proposed
and unapproved, and observation coverage remains unknown. See the
[verified v1.2 operational-evidence review](docs/coverage-v1.2-review.md).

The [indicator delivery review](docs/indicator-delivery-review.md) records the
new SP quality audit, supplied calibration protocol and remaining aggregation
clarifications. It does not approve harmonization or relabel frozen preview data.

A [bounded 2019 training-period pilot](docs/training-period-pilot.md) now has
verified acquisition and a same-rule offline 2020 audit. These are separate
pre-deduplication research inputs, not new approved calendar metrics or a fitted
harmonization model.

The [indicator v1.1 preparation](docs/observed-indicator-pipeline.md) now produces
source-bound observed day/night aggregates with deterministic deduplication.
Real frozen-model experiments have now been executed; the combined forward
candidate failed the registered bias and naive-improvement checks. Harmonization
remains unapproved and application fixtures stay separate. See the
[actual experiment report](docs/multiyear-evidence/experiment-summary.json). Delivery-4
[thresholds are registered](docs/scientific-thresholds.md). The
[multi-year pipeline](docs/multiyear-pipeline.md) now provides fixed acquisition,
verified resume, actual sample audits and frozen-model experiments; it does not
publish harmonized application data.

See the [AI assistance and content provenance disclosure](docs/ai-disclosure.md)
and machine-readable [`ai-disclosure.json`](app/public/ai-disclosure.json). The
team inventory and final submission media must be confirmed before calling the
disclosure complete. Raw NASA observations are distinct from AI-assisted code,
derived statistics and explicitly synthetic demonstration fixtures.
