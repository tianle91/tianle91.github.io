# Toronto infrastructure tracker

A major-project watchlist centred on all six Gardiner rehabilitation sections,
plus the Don River / Central Waterfront water program and a searchable City
project register. Shared Leaflet controls provide asset layers, search, results,
location, fit and mobile details. The Gardiner shortcut shows all six sections,
including completed ones. Project links such as `?project=gardiner-3` reopen a
specific record. Sources and schedules are visible in every record.

The default view combines the City register and major-project watchlist, excluding
completed and post-construction work. Tap the map to search nearby mapped geometry
within 250 m, 500 m or 1 km. The location button uses browser geolocation to do the
same, on request only. Clear the nearby search to return to citywide results.
Search matches street and project text; it is not an address geocoder.
Missing geometry remains searchable citywide but cannot match a nearby search.
No nearby record is evidence only of this snapshot’s coverage, not that work is
unplanned. Results link to City 311 for verification or reporting repair needs.
It includes Transportation Services, Toronto Water, Parks, City Planning,
Economic Development and City-owned TTC, Toronto Hydro and Toronto Community
Housing records. Provincial and private projects, moratoria, lane-restriction
records and study-only programs are excluded. This is not an exhaustive inventory
of municipal capital assets or an inventory of live road closures.

## Usage

- `make` builds offline from `data/projects.json`.
- `make test` runs offline coverage, normalization, safety and publication checks.
- `make data` refreshes all three official register layers and checks watchlist
  source pages, then builds. Internet is required only for explicit refresh.
- `make snapshots` captures desktop/mobile review images after explicit browser setup.

The shared `../.venv`, locked dependencies and Make environment are used. See
[repository instructions](../AGENTS.md). No credentials or new dependencies are needed.
The output embeds data, application code and shared theme. Leaflet 1.9.4 from
unpkg and OpenStreetMap tiles need internet at viewing time.

## Data sources and interpretation

- [T.O.INview](https://map.toronto.ca/toinview/) official web map
  `bd89470eca2c44158383266ec2226005`. Its ArcGIS services are
  `COTGEO_TOINVIEW_PROGRAM_POINT`, `..._LINE`, `..._POLYGON`, under
  `https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/`.
- [Gardiner strategic plan](https://www.toronto.ca/services-payments/streets-parking-transportation/road-maintenance/bridges-and-expressways/expressways/gardiner-expressway/gardiner-expressway-rehabilitation-strategy/)
  and its Section 3 early-works page.
- [Don River / Central Waterfront project list](https://www.toronto.ca/services-payments/water-environment/managing-rain-melted-snow/what-the-city-is-doing-stormwater-management-projects/lower-don-river-taylor-massey-creek-and-inner-harbour-program/projects-of-the-lower-don-river-taylor-massey-creek-and-inner-harbour-program/).
- [Ontario ownership transfer announcement](https://news.ontario.ca/en/release/1007548/ontario-to-take-ownership-of-gardiner-expressway-and-don-valley-parkway-in-fall-2027)
  schedules the Gardiner/DVP transfer for fall 2027. Ownership is City at review.
- Contains information licensed under the
  [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).
  Basemap © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).

`make data` first requests every object ID per layer, fetches bounded batches,
then verifies exact ID coverage. It normalizes HTML into plain text, checks links,
retains missing geometry and publishes only after every required request succeeds.
Identical normalized content preserves the snapshot timestamp, bytes and mtime.
Counts represent location records, not unique contracts. Different layers can
represent parts of the same project, and the watchlist overlaps the register.
No costs or percent-complete estimates are inferred.

The register's Active status includes procurement, design and old records. Only
an explicit Construction contract state becomes Construction. Other records
remain Active — schedule unconfirmed, or are assigned explicit design/planning
contract stages. Warranty/post-construction and completed contracts are separate
stages and hidden by the default Open filter. Published years are displayed without inferring on-site work.
Records still Active beyond their end year carry a warning in details.

## Editorial review and tracking

`data/major-projects.json` is a reviewed editorial input. Its review dates and
source-text hashes establish a baseline. `make data` checks those pages and flags
changed sources in `projects.json`; it never silently advances a review date or
invents a new summary. To update: read the changed official source, revise the
record and schedule, update its reviewed date and hash using `evidence(url)`,
then refresh. Script/style changes are excluded from the text hash. Other page
text can trigger a conservative review flag.

This is a committed snapshot with explicit operator refresh, not an automated
monitor or a subscription. Unchanged page hashes do not establish that a project's
status is unchanged in reality. Always follow the official source for current work.
Gardiner corridors use City road centrelines clipped at approximate section limits.
The Section 5 line depicts the existing road, not the future realignment.
Other watchlist points are illustrative; register geometry is City-published.
Centrelines are committed in the reviewed watchlist input; explicit review updates
those corridors when section limits change.
They do not establish construction footprints, exact tunnel alignments or closures.
