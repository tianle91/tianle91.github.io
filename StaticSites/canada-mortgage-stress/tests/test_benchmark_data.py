"""Official source selection, vintage completeness and safe refresh checks."""
from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

from openpyxl import load_workbook
import pytest

from benchmark_data import (CREA, RATE_API, RATE_LATEST, WORKBOOK, collect_benchmark,
                            discover_workbook, parse_benchmark, parse_rates)
from fetch_data import publish, validate_dataset

FIXTURES = Path(__file__).parent / 'fixtures'
ROOT = Path(__file__).resolve().parent.parent
URL = 'https://www.crea.ca/files/mls-hpi-data/MLS_HPI-Nov-2026.zip'


def test_exact_benchmark_dollars_from_current_toronto_vintage():
    result = parse_benchmark((FIXTURES/'crea-toronto-nov2026.zip').read_bytes(), URL)
    points = result['series'][0]['points']
    assert result['unit'] == 'CAD'
    assert result['vintage'] == 'MLS_HPI-Nov-2026.zip'
    assert len(points) == 262
    assert points[0]['value'] == 315300  # Benchmark dollars, not index=100.
    assert points[-2] == {'period':'2026-09','value':917600,'status':'observed'}
    assert points[-1] == {'period':'2026-10','value':916400,'status':'observed'}


@pytest.mark.parametrize('damage', ['sheet','column','gap','terminal','duplicate','index_instead_of_price'])
def test_bad_workbook_cannot_shorten_or_change_the_series(damage):
    with ZipFile(FIXTURES/'crea-toronto-nov2026.zip') as archive:
        book = load_workbook(BytesIO(archive.read(WORKBOOK)))
    sheet = book['GREATER_TORONTO']
    if damage == 'sheet': sheet.title = 'AGGREGATE'
    elif damage == 'column': sheet['H1'] = 'Composite_HPI'
    elif damage == 'gap': sheet.delete_rows(20)
    elif damage == 'terminal': sheet.delete_rows(sheet.max_row)
    elif damage == 'duplicate': sheet.cell(3,1).value = sheet.cell(2,1).value
    else: sheet.cell(2,8).value = 100
    output = BytesIO();book.save(output)
    packed = BytesIO()
    with ZipFile(packed,'w') as archive: archive.writestr(WORKBOOK,output.getvalue())
    with pytest.raises(ValueError): parse_benchmark(packed.getvalue(),URL)


def test_download_discovery_requires_official_unambiguous_link():
    assert discover_workbook(f'<a href="{URL}">Accept and download data</a>') == URL
    for html in ['<a href="https://example.com/fake.zip">Download</a>',
                 f'<a href="{URL}">One</a><a href="{URL.replace("Nov","Oct")}">Two</a>']:
        with pytest.raises(ValueError): discover_workbook(html)


def rate_fixture():
    data = json.loads((FIXTURES/'boc-mortgage-fixed.json').read_text())
    return data, {'observations':[data['observations'][-1]]}


def test_actual_uninsured_funds_advanced_rates_not_policy_or_posted_rates():
    data, latest = rate_fixture()
    result = parse_rates(data,latest)
    points = result['series'][0]['points']
    assert points[0] == {'period':'2013-01','value':3.18,'status':'observed'}
    assert points[-1] == {'period':'2026-09','value':4.66,'status':'observed'}
    assert len(points) == 165
    assert 'renewals and refinancing' in result['note']
    assert result['geography'] == 'Canada, chartered banks'


@pytest.mark.parametrize('damage', ['definition','gap','terminal','missing_value','nan','negative','duplicate'])
def test_bad_rates_fail_instead_of_interpolating_or_extending(damage):
    data, latest = rate_fixture()
    if damage == 'definition': data['seriesDetail']['V122667786']['description'] = 'Outstanding balances'
    elif damage == 'gap': data['observations'].pop(10)
    elif damage == 'terminal': data['observations'].pop()
    elif damage == 'missing_value': data['observations'][10].pop('V122667786')
    elif damage == 'nan': data['observations'][10]['V122667786']['v'] = 'nan'
    elif damage == 'negative': data['observations'][10]['V122667786']['v'] = '-1'
    else: data['observations'].insert(10,deepcopy(data['observations'][10]))
    with pytest.raises(ValueError): parse_rates(data,latest)


@pytest.mark.parametrize('failed', [CREA, URL, RATE_API, RATE_LATEST])
def test_required_comparison_source_failure_keeps_prior_dataset(tmp_path, failed):
    target = tmp_path/'series.json'
    data = json.loads((ROOT/'data/series.json').read_text())
    target.write_text(json.dumps(data))
    before, mtime = target.read_bytes(),target.stat().st_mtime_ns
    rates,latest = rate_fixture()
    def get(url):
        if url == failed: raise RuntimeError('Required source failed')
        if url == CREA: return SimpleNamespace(text=f'<a href="{URL}">Download</a>')
        if url == URL: return SimpleNamespace(content=(FIXTURES/'crea-toronto-nov2026.zip').read_bytes())
        return SimpleNamespace(json=lambda: latest if url == RATE_LATEST else rates)
    with pytest.raises(RuntimeError):
        comparison = collect_benchmark(get)
        data['groups'] = [g for g in data['groups'] if g['id'] not in {'benchmark','mortgage_rates'}]+comparison
        data.pop('retrieved_at')
        publish(data,target)
    assert target.read_bytes() == before
    assert target.stat().st_mtime_ns == mtime


def test_dataset_rejects_benchmark_index_as_dollars_or_forecast_rate():
    data = json.loads((ROOT/'data/series.json').read_text())
    price = next(g for g in data['groups'] if g['id'] == 'benchmark')
    price['series'][0]['points'][0]['value'] = 100
    with pytest.raises(ValueError,match='benchmark/rate'): validate_dataset(data)
    price['series'][0]['points'][0]['value'] = 315300
    rate = next(g for g in data['groups'] if g['id'] == 'mortgage_rates')
    rate['series'][0]['points'][-1]['status'] = 'forecast'
    with pytest.raises(ValueError,match='benchmark/rate'): validate_dataset(data)
