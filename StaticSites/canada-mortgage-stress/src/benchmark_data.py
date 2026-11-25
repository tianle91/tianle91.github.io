"""Direct CREA benchmark workbook and Bank of Canada funds-advanced rate data."""
import calendar
from datetime import datetime
from io import BytesIO
import math
import re
from urllib.parse import urlparse
from zipfile import ZipFile

from bs4 import BeautifulSoup
from openpyxl import load_workbook

CREA = 'https://www.crea.ca/housing-market-stats/mls-home-price-index/hpi-tool/'
BOC = 'https://www.bankofcanada.ca/rates/banking-and-financial-statistics/interest-rates-for-new-and-existing-lending-by-chartered-banks/'
RATE_ID = 'V122667786'
RATE_API = f'https://www.bankofcanada.ca/valet/observations/{RATE_ID}/json?start_date=2013-01-01'
RATE_LATEST = f'https://www.bankofcanada.ca/valet/observations/{RATE_ID}/json?recent=1'
WORKBOOK = 'Not Seasonally Adjusted (M).xlsx'


def months(start, end):
    first = int(start[:4]) * 12 + int(start[5:]) - 1
    last = int(end[:4]) * 12 + int(end[5:]) - 1
    return [f'{value // 12}-{value % 12 + 1:02}' for value in range(first, last + 1)]


def discover_workbook(html):
    links = {a['href'] for a in BeautifulSoup(html, 'html.parser').select('a[href]')
             if urlparse(a['href']).hostname == 'www.crea.ca' and
             re.search(r'/MLS_HPI-[A-Za-z]+-\d{4}(?:_EN)?\.zip$', a['href'])}
    if len(links) != 1:
        raise ValueError('Expected one current CREA monthly HPI download')
    return links.pop()


def parse_benchmark(content, url):
    match = re.search(r'/MLS_HPI-([A-Za-z]+)-(\d{4})(?:_EN)?\.zip$', url)
    if not match or match[1][:3] not in list(calendar.month_abbr):
        raise ValueError('Unrecognized CREA release vintage')
    release_month = list(calendar.month_abbr).index(match[1][:3])
    # Monthly releases contain observations through the preceding month.
    ordinal = int(match[2]) * 12 + release_month - 2
    terminal = f'{ordinal // 12}-{ordinal % 12 + 1:02}'
    with ZipFile(BytesIO(content)) as archive:
        if archive.namelist().count(WORKBOOK) != 1:
            raise ValueError('CREA non-seasonally-adjusted monthly workbook missing')
        book = load_workbook(BytesIO(archive.read(WORKBOOK)), read_only=True, data_only=True)
        try:
            if 'GREATER_TORONTO' not in book.sheetnames:
                raise ValueError('CREA Greater Toronto sheet missing')
            rows = iter(book['GREATER_TORONTO'].values)
            header = list(next(rows))
            if header.count('Date') != 1 or header.count('Composite_Benchmark') != 1:
                raise ValueError('CREA benchmark columns changed')
            date_col, price_col = header.index('Date'), header.index('Composite_Benchmark')
            points = []
            for row in rows:
                date, value = row[date_col], row[price_col]
                if date is None and all(cell is None for cell in row):
                    continue
                if not isinstance(date, datetime) or date.day != 1:
                    raise ValueError('Invalid CREA observation month')
                if not isinstance(value, (float, int)) or isinstance(value, bool) or not math.isfinite(value) or not 100_000 < value < 5_000_000:
                    raise ValueError('Invalid CREA benchmark dollar price')
                points.append({'period': date.strftime('%Y-%m'), 'value': value, 'status': 'observed'})
        finally:
            book.close()
    if [p['period'] for p in points] != months('2005-01', terminal):
        raise ValueError(f'CREA benchmark must cover January 2005 through {terminal}')
    return {'id': 'benchmark', 'title': 'Greater Toronto composite benchmark price',
            'unit': 'CAD', 'frequency': 'Monthly', 'geography': 'Greater Toronto (TRREB), not City of Toronto alone',
            'source': 'CREA MLS® HPI, GREATER_TORONTO, Composite_Benchmark, not seasonally adjusted',
            'source_url': CREA, 'download_url': url, 'vintage': url.rsplit('/', 1)[-1],
            'note': 'Quality-adjusted composite benchmark from a single current CREA workbook vintage; historical values may be revised. Nominal Canadian dollars, not an average sale price. Greater Toronto / TRREB coverage, not City of Toronto alone.',
            'series': [{'name': 'Composite benchmark price', 'points': points}]}


def parse_rates(payload, latest):
    detail = payload.get('seriesDetail', {}).get(RATE_ID, {})
    if detail.get('label') != 'Fixed rate, 5 years and over' or 'Funds advanced' not in detail.get('description', '') or 'uninsured' not in detail.get('description', ''):
        raise ValueError('Bank of Canada mortgage rate definition changed')
    points = []
    for row in payload.get('observations', []):
        date = row.get('d', '')
        if not re.fullmatch(r'\d{4}-(?:0[1-9]|1[0-2])-01', date):
            raise ValueError('Invalid Bank of Canada monthly date')
        value = float(row.get(RATE_ID, {}).get('v', 'nan'))
        if not math.isfinite(value) or not 0 <= value <= 25:
            raise ValueError('Missing or invalid Bank of Canada mortgage rate')
        points.append({'period': date[:7], 'value': value, 'status': 'observed'})
    last = latest.get('observations', [])
    if len(last) != 1 or len(points) < 120:
        raise ValueError('Incomplete Bank of Canada rate history or latest observation')
    if [p['period'] for p in points] != months('2013-01', last[0]['d'][:7]) or points[-1]['value'] != float(last[0][RATE_ID]['v']):
        raise ValueError('Rate history must reach the independently fetched latest observation')
    return {'id': 'mortgage_rates', 'title': 'Uninsured fixed mortgage rate, 5 years and over',
            'unit': '%', 'frequency': 'Monthly', 'geography': 'Canada, chartered banks',
            'source': f'Bank of Canada, {RATE_ID}, funds advanced', 'source_url': BOC, 'download_url': RATE_API,
            'note': 'Canada-wide average rate on uninsured residential mortgage funds advanced by chartered banks, fixed terms of five years and over. Includes new credit, renewals and refinancing; not a Toronto-specific quote, posted rate, policy rate or rate on outstanding balances.',
            'series': [{'name': 'Fixed mortgage rate (5+ years, uninsured)', 'points': points}]}


def collect_benchmark(get):
    url = discover_workbook(get(CREA).text)
    benchmark = parse_benchmark(get(url).content, url)
    rates = parse_rates(get(RATE_API).json(), get(RATE_LATEST).json())
    return [benchmark, rates]


def validate_comparison_group(group):
    if group['frequency'] != 'Monthly' or len(group['series']) != 1:
        raise ValueError('Expected one monthly benchmark/rate series')
    points = group['series'][0]['points']
    price = group['id'] == 'benchmark'
    expected_unit, first = ('CAD', '2005-01') if price else ('%', '2013-01')
    if group['unit'] != expected_unit or not points or points[0]['period'] != first:
        raise ValueError('Benchmark/rate units or starting month changed')
    for point in points:
        value = point['value']
        if point['status'] != 'observed' or not math.isfinite(value) or not (
                100_000 < value < 5_000_000 if price else 0 <= value <= 25):
            raise ValueError('Invalid benchmark/rate observation')
