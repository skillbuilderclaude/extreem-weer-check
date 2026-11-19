# Extreem weer check (Hanab Pipelines & Utilities)

Webapp bij OP-WI | Extreem weer: hitte en kou en MP-BD | Extreem weer: hitte en kou.
De app toont per locatie de fase voor hitte of kou, de KNMI-waarschuwing en de maatregelen.

## Bestanden
- `index.html`: de app (één bestand, geen installatie).
- `warnings.json`: KNMI-waarschuwingen via MeteoAlarm. Een geplande taak ververst het bestand elk kwartier.
- `knmi.py`: haalt de waarschuwingen op en schrijft `warnings.json`.
- `.github/workflows/knmi-waarschuwingen.yml`: de geplande taak (GitHub Actions).

## Online zetten (GitHub Pages)
1. Maak een openbare opslagplaats `extreem-weer-check` en zet deze bestanden in de hoofdmap. De taak staat in `.github/workflows/`.
2. Settings > Pages: bron "Deploy from a branch", branch `main`, map `/ (root)`.
3. Settings > Actions > General > Workflow permissions: "Read and write permissions".
4. Actions > "KNMI-waarschuwingen ophalen" > Run workflow, om de taak een eerste keer te starten.
Het adres wordt https://skillbuilderclaude.github.io/extreem-weer-check/

## Werking van de waarschuwingen
De app leest `warnings.json`. Is het bestand ouder dan 6 uur of niet bereikbaar, dan vraagt de app de KNMI-code handmatig.
Code oranje of rood voor gladheid, sneeuw of kou geeft minimaal fase Oranje of Rood. Code geel of oranje voor hitte geeft minimaal fase Geel of Oranje.

## Versie
v0.7, 19-11-2026, concept HSE.
