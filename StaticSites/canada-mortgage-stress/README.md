# Ontario arrears & house prices

An indexed comparison of **Ontario bank mortgage arrears** and **Toronto-area
house prices**. Both series share one calendar axis and one index axis. Each
starts at 100 in the first shared month, so 120 means 20% above that series’
starting value. The tooltip shows the index alongside the original share of
mortgages 90+ days overdue or the average sale price in Canadian dollars.

## Interface

The fixed series are **monthly Ontario bank arrears including the CMHC
forecast** and **monthly Toronto-area average sale prices**. There are no series
selectors or date controls. The plot always shows their full shared history,
with the bounds calculated from the committed observations.

The current shared period is **January 2021–September 2026**. The plot and cursor
clip to those exact month boundaries. Bank observations run through
June 2026, so the displayed dashed forecast covers July–September 2026. Later
forecast months are excluded because corresponding price data are unavailable.

Hover or tap to inspect, or focus the chart and use Left/Right to step through
months (Home/End jump to the window edges). The tooltip labels the exact period of each
nearest published observation, within half the reporting interval. It never
interpolates values or carries a stale series beyond its published coverage.
Definitions and linked sources are in one collapsed section beneath the charts.
The page embeds all data, scripts and styles and works offline.

## Data and limits

- **Ontario monthly bank arrears:** observed January 2021–June 2026; CMHC Fall
  2026 forecast July 2026–June 2027, clipped to shared price coverage. Share of
  CBA-member bank mortgage accounts 90+ days overdue. Arrears and delinquency
  mean the same 90+ day measure here.
- **Toronto-area monthly prices:** January 2020–September 2026 in the source,
  clipped to the shared window. TRREB average sale prices, **not Ontario-wide
  prices** and **not a quality-adjusted HPI**. Sales mix affects price averages.

Monthly prices retain two report vintages: legacy coverage through 2023 and
expanded member-board coverage from the 2024 records used here. Separate paths
in the same price color preserve the break; a vertical dashed line marks it.
The boundary is a source-vintage break, not the exact date membership changed.
Newer overlapping report revisions take precedence. Each monthly record retains
its source URL. Annual history also has changing market coverage and conceals
monthly turning points. These data do not establish an arrears-to-price-bottom
lag or prove that prices have not bottomed.

The source JSON retains the original broader CMHC tables for provenance and
refresh validation. Quarterly bank history, annual prices, GTHA private-lender rates, other
provinces and national consumer-credit series are excluded from the indexed plot.
Inventory history is not presented.

The **GTA power-of-sale listings** panel has two separate source choices:

- **Homeleader (default):** residential homes in Toronto, Peel, York, Durham
  and Halton, January 2025 onward. Downloaded directly from the publisher's
  aggregate CSV. Use `new_listings`, not `listed` (which includes relistings).
  Concurrent listings for a property count once; a return within 60 days is
  treated as the same listing period. Detection uses public listing remarks
  and can miss undisclosed lender sales. This remains publisher-derived MLS
  analysis, not direct access to the MLS feed.
- **Valery:** the original screenshot's 24 monthly listing-event counts,
  October 2024–September 2026. New MLS numbers count again, so these counts
  cannot be combined with Homeleader's history. This fixed October 28, 2026
  report edition is preserved in `data/valery-gta-power-of-sale-2026-10.csv`,
  a reviewed transcription of the numerical table, verified November 21, 2026.
  The site blocks automated HTTP downloads; newer editions require review.

Homeleader's current month is hatched and explicitly labelled **to date** in
inspection and the table. The summary compares the latest complete month with
that month a year earlier, when available; it never compares a partial month
against a full month. The feed's timestamp anchors required terminal coverage.
The downloaded November 22 UTC snapshot covers January 2025–November 2026,
with November incomplete. Counts and past months may be revised by the provider.

The separate **Ontario power-of-sale transfers** panel uses Teranet's Q1 2026
Market Insights, Figure 4A. Its 11 annual observations cover 2015–2025. These
are registered completed transfers, not new MLS listings or active inventory.
The parser reads the original report's embedded numerical chart JSON, without
executing scripts or estimating image heights. It fetches that fixed report
edition directly during refresh; discovering newer report editions is manual.
No monthly or 2026 transfer history is inferred.

All count plots use their own zero-based axes and published reporting windows;
none extends or rebases the arrears/price plot. Hover/tap or keyboard arrows
inspect counts; Home/End jump to the edges. Expandable tables expose every
observation. Source, geography, counting method and reporting window remain
visible beside each chart.

Both public CSV alternatives were tested successfully over HTTP on November
21, 2026 local time. Homeleader was selected for its longer history (January
2025 versus PropertyMesh's October 2025). Only Homeleader is integrated;
PropertyMesh is not silently substituted if the source fails. Neither source
is a direct MLS connection. New-source failures abort refresh before publishing.
The original CMHC/TRREB data were preserved while adding these new sources.

## Toronto benchmark prices and borrowing costs

Two additional sections compare the **Greater Toronto (TRREB) composite MLS®
HPI benchmark** with **Canada-wide uninsured fixed mortgage rates, terms of five
years and over**. Greater Toronto is not City of Toronto alone. The original
average-sale-price/arrears plot is retained; benchmark prices are a separate,
quality-adjusted measure and are never spliced into that average-price history.

- **Raw comparison:** benchmark dollars and mortgage percentages in vertically
  aligned plots with the same monthly time axis and inspection cursor. Each has
  its own labelled original-unit axis; dollar prices and rates are not rebased
  onto an arbitrary common scale.
- **Borrowing-cost comparison:** benchmark price and estimated mortgage-payment
  burden, both indexed to 100 in the first shared month. Every month's payment
  uses that month's observed mortgage rate, not one fixed reference rate. The
  readout shows the original benchmark price, applicable mortgage rate, monthly
  principal-and-interest payment, and both indexes. The down payment is held at
  20% and amortization at 25 years throughout.

For example, a payment index of 200 means twice the first month's estimated
payment. If payments rise faster than benchmark prices, the change in borrowing
costs has added to the modelled payment burden. This is a derived payment
comparison, not a market valuation, inflation adjustment, total cost of ownership
or income-based affordability index. It excludes taxes, maintenance, condo fees,
insurance and transaction costs. Each month models a fresh loan at that month's
rate; it does not track an existing loan or predict rates at renewal.

For a nominal annual mortgage rate `r` (as a fraction), the equivalent monthly
rate is `i = (1 + r/2)^(1/6) - 1`, using Canadian fixed-rate semi-annual
compounding. With `n = 300` monthly payments, the payment factor is
`a(r) = i / (1 - (1+i)^(-n))`; at zero interest it is `1/n`. Monthly payment is
`benchmark × 0.8 × a(r)`. The price index is `benchmark / first benchmark × 100`;
the payment index is `payment / first payment × 100`. The calculation is checked
against FCAC's published example: a $300,000 loan, 25 years, 5% produces
$1,744.81/month. Additional tests hold price constant to isolate the effect of
historical rates and hold rates constant to confirm the two indexes coincide.

The November 2026 CREA download supplies a single revised vintage of monthly
non-seasonally-adjusted `GREATER_TORONTO / Composite_Benchmark` observations,
January 2005–October 2026. Historical revisions are preserved as one consistent
vintage; separate past reports are not joined. The Bank of Canada series
`V122667786` supplies January 2013–September 2026. It measures rates on funds
advanced by chartered banks, including renewals/refinancing; it is not a posted
rate, policy rate, Toronto-specific quote or outstanding-balance rate.

Both new charts use their exact common window, **January 2013–September 2026**.
October's benchmark is retained in the source JSON but has no matching rate and
is not plotted or used for a payment estimate. There is no interpolation,
carry-forward, forecast or rate substitution. Hover/tap and keyboard arrows
inspect both charts together; Home/End jump to the first/last common month.

Explicit `make data` discovers the current official CREA ZIP link and parses
`Not Seasonally Adjusted (M).xlsx` with the already-declared `openpyxl` dependency.
Only the Toronto composite benchmark column is selected, not the national
aggregate, an HPI index level or average sale prices. Coverage must reach the
month preceding the release vintage. The Bank of Canada Valet history is
checked against an independently requested latest observation. Missing data,
changed definitions or failure of either source aborts publication of the whole
combined dataset. Offline builds/tests use the committed observations. Fixtures
retain the exact Toronto worksheet values (other boards omitted) and the rate
API response. Existing arrears, average-price and power-of-sale observations
were preserved when these two new series were acquired on November 25, 2026.

## Visual snapshots

[Desktop (1440 × 900)](tests/snapshots/desktop.jpg) ·
[Mobile (390 × 844)](tests/snapshots/mobile.jpg) ·
[Power-of-sale desktop](tests/snapshots/power-sale-desktop.jpg) ·
[Power-of-sale mobile](tests/snapshots/power-sale-mobile.jpg) ·
[Transfers desktop](tests/snapshots/transfers-desktop.jpg) ·
[Transfers mobile](tests/snapshots/transfers-mobile.jpg) ·
[Benchmark desktop](tests/snapshots/benchmark-desktop.jpg) ·
[Benchmark mobile](tests/snapshots/benchmark-mobile.jpg) ·
[Borrowing-cost desktop](tests/snapshots/borrowing-cost-desktop.jpg) ·
[Borrowing-cost mobile](tests/snapshots/borrowing-cost-mobile.jpg)

Generate review images of the actual HTML page:

```sh
make snapshot-browser  # explicit headless Chromium setup; repeat after Playwright upgrades
make snapshots         # rebuild from committed data, then capture all five sections at both sizes
```

Capture uses a temporary loopback server and fresh light-mode contexts. Mobile
uses touch emulation. All plots, the inspection readout, fonts and responsive
geometry must finish rendering before capture; page errors, external requests
and horizontal overflow fail the command. All ten captures must succeed before
existing review images are replaced. These JPEGs show the initial viewport;
longer pages continue below the image. They are visual review references, not
automated pixel comparisons.

The chart pages are self-contained, so capture works offline once the locked
Python dependencies and browser are installed. Browser downloads happen only
through `make snapshot-browser`. Ordinary builds, tests and data refreshes do
not install browsers or capture images. Recapture after visual changes and
commit the reviewed images. On Linux, install Chromium's
[manual system prerequisites](https://playwright.dev/python/docs/browsers#install-system-dependencies)
if needed; the targets do not install OS packages.

Optional browser fixtures check incomplete rendering, moving paths, page errors,
overflow and blocked external resources without live data or network assets:

```sh
make browser-test # shared offline browser fixtures; browser setup is explicit
```

## Build, test and refresh

```sh
make system-deps # explicit macOS/Homebrew installation of uv
make deps        # install complete locked environment when missing/stale
make             # offline build from committed data
make test        # offline Python tests
make open        # open the generated HTML
make data        # explicit network refresh, then rebuild
make clean       # remove generated HTML
make clean-deps  # remove environment/stamp; clean-venv is an alias
node tests/test_timeline.cjs # optional checks, Node 18+, no npm dependencies
node tests/test_mortgage_costs.cjs # mortgage math and exact-month coverage checks
```

Build within this checkout: the Makefile includes `../python-project.mk`.
Homebrew must already be installed for `system-deps`; other platforms need uv
installed manually. uv manages Python >=3.11. No credentials are needed.
Environments are reused without repair. Use `make clean-deps && make deps` for
an incomplete environment. Missing/stale locks fail without being rewritten.

Fetching uses requests, BeautifulSoup for CMHC accessible chart tables, and
pypdf layout extraction for TRREB PDFs, the Homeleader aggregate CSV, and
Teranet’s embedded annual chart JSON, the CREA benchmark workbook and Bank of
Canada Valet mortgage-rate data. Valery remains a fixed reviewed CSV snapshot. All required inputs must validate before
one `data/series.json` is replaced atomically. Missing periods, duplicates,
implausible values, truncated tables and missing report links fail the refresh.
Homeleader must contain consecutive GTA-only totals from January 2025 through
its source timestamp month, with only that last month marked incomplete. Teranet
must retain Figure 4A’s 2015–2025 count series and the report’s stated totals.
The latest monthly price table must cover the full previous year and January
through the report month discovered from its PDF filename. Combined history
must also reach that month; surviving extracted rows cannot shorten the endpoint.
Unchanged normalized records preserve bytes, timestamps and mtime. Raw PDFs are
not retained. Network access is confined to `make data` and dependency setup;
installed builds/tests stay offline. Failed refreshes retain previous data/output.

The rolling CMHC URL must still contain the **Fall 2026** edition; a new edition
requires reviewing definitions and forecast vintage before updating the parser.
TRREB archive reports may need extending when a new year creates a history gap.

Sources live in `src/`; `timeline.js` holds the date/selection model and `app.js`
renders the indexed SVG plot; `power-sale.js` renders the listing and transfer
count panels. `distress_data.py` parses the listing/transfer sources.
`benchmark_data.py` parses the benchmark/rate sources; `mortgage-costs.js` holds
the payment model and exact-month join, and `benchmark.js` renders the two new
comparison sections. `tests/` contains parser fixtures and model checks.
The committed artifact is `output/canada-mortgage-stress.html`.

## Data sources

- [CREA MLS® HPI Tool](https://www.crea.ca/housing-market-stats/mls-home-price-index/hpi-tool/):
  official monthly ZIP discovery; [November 2026 workbook bundle](https://www.crea.ca/files/mls-hpi-data/MLS_HPI-Nov-2026.zip),
  not seasonally adjusted, `GREATER_TORONTO / Composite_Benchmark` in dollars.
- [Bank of Canada mortgage rates](https://www.bankofcanada.ca/rates/banking-and-financial-statistics/interest-rates-for-new-and-existing-lending-by-chartered-banks/):
  [Valet series V122667786](https://www.bankofcanada.ca/valet/observations/V122667786/json?start_date=2013-01-01),
  uninsured fixed rates of five years and over, funds advanced.
  [Funds-advanced definition](https://www.bankofcanada.ca/rates/banking-and-financial-statistics/funds-advanced-and-outstanding-balances-for-new-and-existing-lending-by-chartered-banks/).
- [FCAC mortgage-interest examples](https://www.canada.ca/en/financial-consumer-agency/services/mortgages/interest-on-mortgages.html):
  independent reference payment used by the calculation test.

- [Homeleader GTA Power of Sale Tracker](https://homeleaderrealty.com/power-of-sale-tracker/):
  methodology and [monthly aggregate CSV](https://homeleaderrealty.com/api/hlr/v1/pos/csv).
  Downloaded from the publisher during explicit refreshes; source timestamp is
  preserved as a date. The offline parser fixture retains the downloaded aggregate
  CSV, including overlapping regional/type breakdowns that are not summed.
- [Teranet Q1 2026 Market Insights](https://teraintelligence.teranet.ca/market_insights/market-insights-q1-2026/):
  Figure 4A, Ontario registered power-of-sale transfer counts, 2015–2025.
  The offline fixture retains only the relevant heading and embedded chart script.

- [Valery Power of Sale Report, October 2026](https://valery.ca/research/power-of-sale/):
  GTA new monthly listings, October 2024–September 2026; published October 28,
  2026. Valery analysis of TRREB MLS® data. The reviewed CSV preserves this edition.

- [CMHC Residential Mortgage Industry Report, Fall 2026](https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-research/research-reports/housing-finance/residential-mortgage-industry-report):
  accessible tables, Ontario observations from Figures 1 and 13. Underlying
  sources include the Canadian Bankers Association and Statistics Canada.
- [TRREB Historic Statistics](https://public.trreb.ca/wp-content/files/market-stats/market-watch/historic.pdf):
  annual sale prices and the changing-market-area caveat.
- [TRREB Market Watch](https://public.trreb.ca/market-data/market-watch/): latest
  report discovery and the notice about expanded coverage and revised history.
- [December 2021](https://public.trreb.ca/wp-content/files/market-stats/market-watch/mw2112.pdf),
  [December 2023](https://public.trreb.ca/wp-content/files/market-stats/market-watch/mw2312.pdf),
  [December 2025](https://public.trreb.ca/wp-content/files/market-stats/market-watch/mw2512.pdf),
  and [September 2026](https://public.trreb.ca/wp-content/files/market-stats/market-watch/mw2609.pdf)
  Market Watch reports: monthly sale-price tables. Copyright Toronto Regional
  Real Estate Board. Exact report URLs are also in the HTML and JSON.

Shared build-time components and the single Python environment are documented
in the [repo README](../README.md). Project `make clean-deps` removes that shared
environment, not a private environment. Add dependencies at the repository root;
`site.toml` holds listing metadata and `pytest.ini` configures this project’s tests.
The generated HTML remains standalone and embeds its application assets/data.
