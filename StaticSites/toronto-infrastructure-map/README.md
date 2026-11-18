# Toronto infrastructure tracker

A major-project watchlist centred on all six Gardiner rehabilitation sections,
plus the Don River / Central Waterfront water program and a searchable City
project register. Shared Leaflet controls provide asset layers, search, results,
location, fit and mobile details. The Gardiner shortcut shows all six sections,
including completed ones. Project links such as `?project=gardiner-3` reopen a
specific record. Sources and schedules are visible in every record.

The street basemap is muted by default so project colours stand out. The Street
map contrast selector restores the full basemap when street context is needed.
Major projects draw above register records. Selecting a map feature or result
adds a white outline and a persistent highlighted-project key; clear it from the
key or change filters. Project lines and pins enlarge at neighbourhood zoom.

## Share a view

Pan/zoom and choose filters, then use **Copy link to this view**, or copy the
browser address. The URL updates with `replaceState` rather than adding a browser
history entry for every pan or keystroke. Opening a link restores its centre and
zoom, search, collection, stage, owner, category layers (including none selected),
basemap contrast, radius preference and highlighted project. Browser Back/Forward
also reapplies incoming URL state. Existing project-only links remain supported.

Parameters are `lat`, `lng`, `z`, `q`, `scope`, `stage`, `owner`, `layers`,
`basemap`, `radius` and `project`, with `v=1` identifying serialized views. Default
filters are omitted; unknown unrelated query parameters/fragments are preserved.
Invalid values fall back to defaults and category/owner values are validated
against the available options. Centres are stored to six decimal places; rendered
position can vary within a pixel with viewport layout and Leaflet rounding.

The live location circle, location permission and tracking state are excluded.
A recipient starts without that local distance filter; they can choose ◎ to show
projects near their own location using the shared radius preference. The copy
confirmation makes this limitation explicit. Clipboard failures leave the full
shareable link in the address bar and show a manual-copy message.

`make share-test` explicitly runs desktop/mobile URL and clipboard regressions
with the same optional `BROWSER_EXECUTABLE` selection as `make click-test`.

The default view combines the City register and major-project watchlist, excluding
completed and post-construction work. Use ◎ and allow browser location access to show a nearby-project circle.
It stays centred on the browser’s reported position and follows location updates
while visible. Drag anywhere on its circumference to resize from 100 m to 5 km;
there is no resize icon. Preset radii remain available in the filters. The
circumference is keyboard focusable and supports arrow keys (25 m; Shift for
100 m), Home and End. Project clicks open details;
empty-map clicks never create or move the circle. The × button on the south
(bottom) edge is the only user control that dismisses the circle. It removes
the circle and location pin, stops location updates, resets ◎, and restores
citywide results. Filters and the Gardiner shortcut preserve the circle and
respect its active radius. While active, ◎ fits the circle back into view without
restarting location access; this also brings × into view after panning or resizing. Clicking ◎ again requests a fresh position using the browser’s
existing permission state. The page cannot revoke browser-level permission.
Search matches street and project text; it is not an address geocoder.
Missing geometry remains searchable citywide but cannot match a nearby search.
No nearby record is evidence only of this snapshot’s coverage, not that work is
unplanned. The prominent Report a problem to 311 link stays beside search/counts
across all tabs, including the compact mobile panel, and opens City 311 in a new
tab for verification or reporting repair needs without losing the map state.
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
- `make click-test` runs explicit real-mouse/touch regressions after browser setup.
  An existing browser can be selected with `BROWSER_EXECUTABLE=/absolute/path`.

The click regression serves a small fixture through the production renderer and
application. It checks register lines, pins, repeated selection through the
highlight overlay, major corridors, permission-gated circle creation, real
mouse/touch circumference resizing, location tracking, dismissal and restart,
permission denial, and ensuring filters, the Gardiner shortcut and active ◎ do
not dismiss the circle. Empty-map clicks leave
the location circle unchanged. In particular, offscreen major geometry must not intercept clicks on
register records. Major and highlight layers use SVG so their blank surfaces
allow clicks through; the larger register retains its shared Canvas renderer.

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
