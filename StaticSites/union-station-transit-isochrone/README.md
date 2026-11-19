# Union Station Transit Isochrone Map

An interactive Leaflet map of the **morning commute-shed of Toronto's Union
Station**: where you can live and still **reach Union by public transit** in
**15, 30, 45, 60, 75, 90 and 120 minutes**, arriving during the weekday morning peak — subway,
streetcar, bus, GO rail and UP Express, plus the walk at each end. The result is a
self-contained `output/union-station-transit-isochrone.html` with toggleable layers, a legend, geolocation, and a
click-anywhere "which band is this in?" readout. Search station names, lines or
transport modes. Stations toggle independently by mode alongside the seven
travel-time bands. The matching count refers to station points; the band count
is separate. Search filters stations while bands remain available as context.
Clicking the map or using location keeps the nearest-station itinerary readout.

GO rail, TTC subway, and streetcar/light-rail routes have separate line toggles. The lines follow
official GTFS shapes, use the published route colors, and show route names on
hover or tap. Both directions, short turns, and branches are merged into each
route. The Data sources panel records the line snapshot date separately from
the commute-shed routing date.

This is a **reverse isochrone** (travel time *to* Union, arriving by ~9 am), so it
respects peak-direction service. Routing direction is the one knob with real cost:
each map point is a separate r5py search. The default grid uses 500 m spacing,
and routing is the expensive step. Change resolution via the env vars below.

## Share a view

Use the share glyph beside search (**Copy link to this view**) or copy the address bar to share the current map
centre, zoom, search and selected layers/filters. Links restore that combination
on a fresh page; invalid values use defaults. URLs update without adding a history
entry for each interaction. Browser Back/Forward restores incoming URL state.
Location access, permission and live proximity calculations are not restored
from a link. The shared map UI and URL helpers are embedded into
the standalone output at build time.

## Visual snapshots

[Desktop (1440 × 900)](tests/snapshots/desktop.jpg) ·
[Mobile (390 × 844)](tests/snapshots/mobile.jpg)

Regenerate both review images explicitly:

```sh
make snapshot-browser  # one-time headless Chromium download; repeat after Playwright upgrades
make snapshots         # rebuild from committed inputs, then capture both views
```

Run `make lines` to refresh only the route shapes and rebuild the map. This uses
the GO/TTC feeds without running Java, downloading OSM, or recomputing polygons.
`make data` also refreshes the line snapshot as part of the full routing update.

The shared capture helper serves this project on a temporary loopback port and uses fresh,
light-mode Chromium contexts with no search or user location. Mobile uses touch
emulation and the compact panel; browser chrome and the on-screen keyboard are
excluded. It waits for initialization, fonts, loaded tiles and settled map motion.
Both captures must succeed before existing images are replaced. Images are visual
review references, not automated pixel comparisons; upstream map tiles can change.

Snapshot capture needs network access to the page's map scripts and tiles. It
never refreshes committed data or installs browsers automatically. Ordinary
`make`, `make test` and `make data` do not capture snapshots. Python dependencies
remain locked in the repository-root environment. On Linux, install Chromium's
[manual system prerequisites](https://playwright.dev/python/docs/browsers#install-system-dependencies)
if required; these targets do not install OS packages. Recapture after visual
changes and commit the reviewed images with them.

## Map controls

The desktop sidebar puts search and the matching count above **Layers**,
**Results**, and **Data sources** tabs. On phones, the same controls live in an
expandable bottom panel. Search and selected layers determine both the count
and results; layer badges show matches available before layer selection. Results
list up to 50 matches; narrow the search to find a specific feature.

On phones, the compact panel keeps search and counts visible. **Show results & filters**
expands it; **Show more map** folds it down. Focusing search also expands the
panel. It follows the visible viewport when the keyboard opens, and Search/Enter
dismisses the keyboard. Source links remain available under **Data sources**.
Long location details open in a scrollable mobile dialog with a persistent close
button; short map labels remain anchored popups. Desktop keeps its sidebar and popups.

Use **Center on my location** (◎) to request browser location and show its
accuracy circle, or **Fit matching features** (⛶) to frame the current selection.
Location is requested only after a click and stays in browser memory. HTTPS or
localhost is needed for location in most browsers. Denied, unavailable and timed
out requests show a message and can be retried. The **Provenance** footer opens
source links, snapshot information and accuracy caveats.


## Quick start

The build computes real, full-network transit reach with
[r5py](https://r5py.readthedocs.io/) — multimodal RAPTOR routing over GTFS +
OpenStreetMap, including the street-network walk at each end. One-time setup,
then `make data`:

```bash
# 1. Install uv, Java 21, and osmium on macOS with Homebrew already installed.
make system-deps

# 2. Obtain/refresh all inputs, route, and rebuild the map.
make data    # downloads OSM + TTC/GO/UP feeds, clips, routes, and rebuilds
make open    # opens output/union-station-transit-isochrone.html in your default browser
```

`make data` uses the repository-root `.venv`, installed by `make deps` (see
the [repo README](../README.md)). It downloads and conditionally refreshes OSM and the separate TTC, GO, and UP
Express feeds, validates active service, and auto-clips the OSM extract to the GTHA bbox (R5 caps the geographic
extent), then writes `data/reachability.json` (a grid→Union travel-time grid), contours
it into `output/isochrones.geojson`, and renders `output/union-station-transit-isochrone.html`. It routes for the next
non-holiday weekday (Wednesday).

The committed `output/union-station-transit-isochrone.html` is already built this way, so you can also just open
it directly — the internet is only needed for map tiles and the Leaflet library.

### Installing Java 21

r5py needs a **Java 21 JDK** on PATH. On macOS with Homebrew:

```bash
brew install --cask temurin@21   # prompts for your password to install the JDK
/usr/libexec/java_home -v 21     # verify: prints the JDK path
java -version                    # verify: shows 21.x
```

Temurin registers with macOS's `java_home`, so `java` is usually on PATH
automatically. If `java -version` still reports "Unable to locate a Java
Runtime", add to your `~/.zshrc` and re-open the shell:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
```

Not using Homebrew? Grab the Temurin 21 `.pkg` from
[adoptium.net](https://adoptium.net/temurin/releases/?version=21).

## What's on the map

* **Four time bands** (toggle on/off): ≤30 min, ≤1 h, ≤1.5 h, ≤2 h. Each band is
  the area from which you can *reach* Union within that time by transit + walking.
  They form the characteristic "octopus" shape — reach stretches along the subway
  and GO rail lines and pools around stations.
* **Station markers** (toggleable): every modelled subway / GO / UP station,
  colour-coded by mode. Click one for its line, routed time to Union, and the
  step-by-step trip (which line, where you board, departure time).
* **Click anywhere** → it tells you which time band the point falls in and shows
  the **suggested trip via the nearest station** — walk to the station, then the
  exact transit legs to Union. Great for "could I live here and still get to Union
  in under an hour, and how?"
* **Locate-me** → shows a "you are here" pin (automatically on load if the
  browser grants location, or via the ◎ button) and reports your own band.

## How the isochrones are built

`make data` routes a grid of points over the GTHA *to* Union with r5py (arriving
during the morning peak), where each trip already includes the door-to-door walk.
`src/build_isochrones.py` buffers each point within time `T` by its remaining walk
budget and unions the circles with shapely, then simplifies the result. Bands are
nested by construction (30 ⊂ 60 ⊂ 90 ⊂ 120). It also runs
a second, heavier pass (`r5py.DetailedItineraries`) for the reachable stations to
record each one's step-by-step trip to Union, which the map shows on click.

### Why it's still an "isochrone"

An isochrone is any set of equal-travel-time contours anchored on a point. This map
measures time *to* Union rather than *from* it, which makes it a **reverse
isochrone** — also called a **catchment area** or **commute-shed**. The term still
fits: the bands are equal-travel-time contours, just inbound. The UI copy says
"commute-shed" because it reads more clearly; the code keeps `isochrone` in
filenames since both names describe the same thing.

### Travel-time model: best-timed vs typical

For each point, r5py samples a departure every minute across the window — the
`MAX_MINUTES` before arrival (07:00–09:00 by default, so even a 2-hour trip can
still arrive by 9) — and records each trip's travel time, a *distribution*, not one
number. `PERCENTILE` selects which point of it to report (lower = faster): `1` ≈
the best-timed trip, `50` the median. The choice only matters for infrequent
service (illustrative, sampled over an 8–9am window):

| station | p1 | p25 | p50 (median) |
|---|---|---|---|
| Richmond Hill GO (sparse peak rail) | **52** | 109 | unreachable |
| Downtown (frequent subway) | 24 | 27 | 27 |

Frequent subway is flat — whenever you leave, the trip is about the same, so the
percentile barely matters. Sparse peak-direction rail is a cliff: catch the one
useful inbound train and it's 52 min; miss it and you fall back to a ~109-min
bus+subway trip, and most departure-minutes can't make it at all (so the median
reads as *unreachable*).

The default `PERCENTILE=1` models a **planned commute** — you check the schedule and
leave to catch your train — which is the honest choice for an arrive-by-9am map; the
median would erase viable-but-infrequent GO lines. The trade-off: it assumes good
timing (Richmond Hill's 52 min is real, but only via that one train). Raise
`PERCENTILE` toward `50` for a conservative "turn up and go" reading.

### Tunables (env vars)

* `ARRIVE_HHMM` (default `09:00`) — arrival time at Union.
* `PERCENTILE` (default `1`) — travel-time percentile over the departure window;
  `1` ≈ the best-timed trip, `50` the median.
* `GRID_SPACING_M` (default `500`) — grid resolution. **Reverse routing is one
  r5py search per point**, so finer grids are much slower (≈4× per halving).
* `MAX_MINUTES` (default `120`) — time budget *and* the departure-window length
  (window = `[ARRIVE_HHMM − MAX_MINUTES, ARRIVE_HHMM]`); `BBOX_S/N/W/E` — extent.

## Files

| File | Purpose |
|------|---------|
| `src/fetch_data.py` | Complete preparation, downloads, validation, and routing cache |
| `src/fetch_isochrones.py` | `make data`: real transit routing with r5py (OSM + GTFS) → `data/reachability.json` |
| `src/build_isochrones.py` | Unions reachable walk-circles (shapely) into `output/isochrones.geojson` |
| `src/build_map.py` | Renders `output/union-station-transit-isochrone.html` from the geojson + model |
| `data/transit_model.json` | Origin, bands, params + station list (used for markers and as the offline fallback) |
| `data/transit_lines.geojson` | Committed GO rail, TTC subway, and streetcar/light-rail route shapes and line snapshot date |
| `src/transit_lines.py` | Offline GTFS rail/subway/streetcar shape extraction and deterministic snapshot publication |
| `data/routing_grid.json` | Committed routed points and model settings for reproducible offline contours |
| `data/reachability.json` | r5py travel-time grid (each point → Union) + per-station step-by-step itineraries (generated by `make data`) |
| `output/isochrones.geojson` | Generated band polygons (committed so the map works without a build) |
| `output/union-station-transit-isochrone.html` | Generated map (committed) |
| `data/README.md` | Managed downloads, cache behavior, and custom input overrides |
| `tests/` | pytest suite (dates/holidays, station snapping, itinerary parsing, builder smoke test) |
| `Makefile` | `make` builds the map from the committed model, `make data` re-routes it, `make osm` clips the OSM extract, `make open` opens it, `make clean` removes output |

## Tests

```bash
make test    # runs pytest in the shared root .venv
```

The suite uses pytest and Shapely from the shared environment, with synthetic
GTFS fixtures for line extraction. It runs without r5py, Java, or downloaded feeds.
It covers Easter/holiday service dates, station snapping, itinerary leg parsing,
route filtering, branch geometry, repeatable snapshots, and a smoke test that runs the
builders end-to-end in a temp dir (falling back to the curated model). The r5py
routing itself isn't unit-tested (it needs Java + feeds); its helpers are.
Root `make test` runs this suite and the offline build alongside every other project.

## Caveats

* **Bands are for arriving at Union ~9 am on a weekday (morning peak).** Transit
  reach is highly time-dependent: **GO and UP run far less often off-peak** and
  several GO lines are peak-direction only, so the off-peak/return commute-shed is
  smaller. Tune with `ARRIVE_HHMM`.
* **Times assume a well-timed departure** (you leave home to catch the train) —
  the bands use the best trip in the window (`PERCENTILE=1`), not the median. See
  [Travel-time model](#travel-time-model-best-timed-vs-typical) for why, and raise
  `PERCENTILE` for a more conservative "turn up and go" reading.
* **The grid samples every 500 m by default.** Contouring buffers each reachable
  point by 375 m, so boundaries remain approximate. Lower `GRID_SPACING_M` for
  finer sampling at the cost of additional routing work.
* **Use current GTFS feeds.** `make data` routes for the next non-holiday
  Wednesday, so each feed's `calendar` must cover that date or you'll get empty
  isochrones.
* Stations with routed itineraries use their GTFS-snapped coordinates and routed
  travel times. Stations without routed details use the curated coordinates and
  approximate all-day typical times.

## Refresh and dependencies

This project includes the repository's [shared Python/uv Make template](../python-project.mk).
Its own Makefile defines artifact inputs, rendering rules, and any configuration
overrides. Build inside the repository checkout so the shared template is available.

`make system-deps` installs [uv](https://formulae.brew.sh/formula/uv),
[osmium-tool](https://formulae.brew.sh/formula/osmium-tool), and
[Temurin Java 21](https://formulae.brew.sh/cask/temurin@21)
on macOS using [Homebrew](https://brew.sh), which must already be installed.
On other platforms, install those tools manually before `make deps` / `make data`.
System installation runs only when explicitly requested; other targets never
invoke it. Credentials must be supplied separately.

`make deps` installs the repository's complete locked Python environment, including
test dependencies, when it is new or the dependency manifests change. `make data`
uses the same setup before fetching all required upstream inputs. Repeated commands
reuse the environment; they do not attempt repairs. To reinstall from scratch, run
`make clean-deps && make deps` (`clean-venv` remains an alias). Missing or stale
locks fail without being rewritten.
Dependency setup may require network access; installed builds/tests are offline.
`make data` obtains every required input and rebuilds outputs automatically.
Unchanged upstream content preserves data timestamps; missing generated files are
restored. Required-source failures retain previous datasets and return an error.

Shared build-time components and the single Python environment are documented
in the [repo README](../README.md). Project `make clean-deps` removes that shared
environment, not a private environment. Add dependencies at the repository root;
`site.toml` holds listing metadata and `pytest.ini` configures this project’s tests.
The generated HTML remains standalone and embeds its application assets/data.

A small committed `data/station_itineraries.json` preserves the published routed
station details and their original date when the ignored routing grid is absent.
It is used only with routed GeoJSON, never with the curated fallback geometry.
`make data` updates it from validated routing results and restores it on cache reuse.

The committed `data/routing_grid.json` retains the points, 500 m grid spacing,
arrival window and routing provenance needed to reproduce the seven contours.
Offline builds use it when the larger local `reachability.json` cache is absent.
`make data` updates both the contour grid and station itinerary snapshot.
