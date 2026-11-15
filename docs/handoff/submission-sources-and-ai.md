# André — fontes e declaração de IA para a submissão

## Mensagem sobre as fontes

Sim, devemos citar FIRMS, IBGE e MapBiomas, indicando o papel de cada um. Também
usamos NASA GIBS para imagens de contexto e OpenStreetMap como mapa-base.

1. NASA FIRMS: observações de focos ativos e FRP de MODIS (Terra/Aqua) e VIIRS
   (Suomi-NPP), via arquivos/API Standard Processing. É a fonte das detecções;
   não apresentamos esses registros como incêndios individuais ou área queimada.
   https://firms.modaps.eosdis.nasa.gov/
2. IBGE, edição 2025: limite oficial do bioma Pantanal, escala 1:250.000, usado
   para a referência geográfica e recorte pelos centros das detecções.
   https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/biomas/vetores/2025_Biomas-e-Sistema-Costeiro-Marinho-do-Brasil-1-250000_shp.zip
3. Projeto MapBiomas: uso e cobertura da terra, Coleção 11, ano 2020, resolução
   30 m, asset de cobertura v3. É uma camada opcional de contexto no mapa:
   não gera os focos, não mede área queimada e não comprova cobertura do sensor.
   https://brasil.mapbiomas.org/
   https://plataforma.mapbiomas.org/
4. NASA GIBS: imagem opcional de contexto MODIS Terra em cor verdadeira, camada
   `MODIS_Terra_CorrectedReflectance_TrueColor`. Não extraímos as métricas dessa imagem.
   https://nasa-gibs.github.io/gibs-api-docs/access-basics/
5. OpenStreetMap contributors: mapa-base. Manter os créditos visíveis no mapa.
   https://www.openstreetmap.org/copyright

Não listar o polígono antigo gerado no Gemini como fonte oficial: ele foi
substituído e não é a geometria ativa. Os arquivos IBGE de uso da terra de 2018
e os recursos do MMA enviados anteriormente não alimentam a camada ativa atual.
Também não atribuir o mapa-base à CARTO: o código atual usa tiles OpenStreetMap.

## Texto em inglês para aproveitar na submissão

ChronoFlare uses NASA FIRMS Standard Processing active-fire observations from
MODIS aboard Terra and Aqua and VIIRS aboard Suomi-NPP. The official IBGE 2025
Pantanal biome boundary provides the fixed spatial reference. Optional MapBiomas
Collection 11 land-cover data for 2020 (30 m, coverage asset v3) provide landscape
context. NASA GIBS supplies optional MODIS Terra true-color context imagery, and
OpenStreetMap contributors provide the basemap. Context imagery and land cover
are not the source of the fire detections, burned-area estimates or observation
coverage. Thermal detections are not confirmed individual fires. Data-processing
provenance and limitations are documented in the repository.

## IA: declaração conhecida, a completar com os outros integrantes

OpenAI Codex assisted with code generation, debugging, tests and documentation.
NASA FIRMS observations were obtained from NASA and were not synthesized by a
generative AI model. Native summaries and calibration/validation outputs were
computed by versioned scripts; those scripts were developed with AI assistance.
The separate demonstration fixtures are synthetic values produced by deterministic
scripts implemented with AI assistance and are labeled as synthetic. Statistical
calibration candidates are not accepted scientific truth: the frozen candidate
failed the registered forward checks and harmonization remains unapproved.
The team is responsible for reviewing AI-assisted outputs and documenting the
remaining limitations.

Confirmar com a equipe quais outras ferramentas foram usadas e em quê. Não afirmar
que a lista está completa ou que houve revisão humana integral sem essa confirmação.
O uso de IA no texto científico, vídeo, voz e artes também precisa entrar no inventário.

A orientação pública do GO Team permite IA e exige identificar onde e como ela
foi usada. Código/dados e áudio precisam de reconhecimento em texto descritivo e
metadados; imagens/vídeos gerados por IA precisam de marca visível. Não usar ou
modificar elementos de identidade visual da NASA em material gerado por IA.
Referência: https://github.com/nasa/spaceapps/discussions/1849
O guia completo de submissão não estava acessível na consulta; conferir no seu
acesso qualquer exigência adicional do formulário final.

No vídeo, diferenciar gravação real do app de imagens/vídeos gerados por IA.
Informar se a voz é sintética; nesses casos, incluir a declaração na descrição
e nos metadados e aplicar a marca visível quando for mídia visual gerada por IA.

O link FortiGuard é para pedir classificação/revisão de sites no filtro web, não
para declarar IA no Space Apps. Se houve bloqueio, identificar a URL e a categoria
antes de solicitar revisão; essa solicitação é separada da submissão do projeto.

Atualização do inventário informado por Jorge: Cursor foi usado no frontend da
Anastasia. Claude e Claude Code estão previstos para investigação da harmonização
e revisão final; confirmar o uso efetivo antes de descrever essas etapas como
concluídas. O inventário de voz, imagem e vídeo ainda depende de confirmação.
