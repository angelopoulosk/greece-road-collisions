# Τροχαίες συγκρούσεις στην Ελλάδα

> «Το “ατύχημα” υπονοεί ότι δεν φταίει κανείς.» — Hot Fuzz (2007)

Road collisions (συγκρούσεις) and ambulance transports (διακομιδές) in Greece, extracted from the
government map at [accidents.maps.gov.gr](https://accidents.maps.gov.gr/geo-analytics/), plus a simple
interactive map.

**Map:** https://angelopoulosk.github.io/greece-road-collisions/

## Data

| File | Records | Period |
|---|---|---|
| `data/collisions.csv` / `.xlsx` | 84,331 | 01/10/2020 – 19/05/2025 |
| `data/transports.csv` / `.xlsx` | 119,897 | 01/10/2020 – 31/12/2024 |

Columns: `id`, `datetime_athens`, `timestamp_utc`, `longitude`, `latitude`, `municipality`,
`description` (recorded cause, collisions only), `color` (marker colour used by the source map).

`data/collisions.json` and `data/transports.json` are compact column files used by the map.

## How it was collected

The source only returns results within 10 km of a point and for at most 6 months at a time.
On 13/11/2026 the whole country was covered with 1,264 overlapping 10 km circles on a hexagonal grid,
each queried in 6-month windows from 01/10/2020 for both types. Records returned by more than one
circle were de-duplicated by record id. Circles with no events in a full test year
(04/2022 – 04/2023) and no neighbouring circle with events were not queried further. The source
had no records after the end dates above.

`scripts/build.py` turns the raw dump into the files under `data/`.

## Source and licence

Data: Hellenic Ministry of Digital Governance, Ministry of Citizen Protection and Ministry of
Infrastructure and Transport, via accidents.maps.gov.gr. This repository is an unofficial copy.
