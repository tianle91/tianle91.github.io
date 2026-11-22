"""Check provider definitions, reporting completeness and atomic refresh failures."""
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from distress_data import parse_homeleader, parse_teranet
import fetch_data

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / 'fixtures'


def test_homeleader_uses_gta_new_homes_not_listed_or_subtotals():
    group = parse_homeleader((FIXTURES / 'homeleader-pos.csv').read_text())
    points = group['series'][0]['points']
    assert group['unit'] == 'homes'
    assert len(points) == 23
    assert points[0] == {'period': '2025-01', 'value': 33, 'status': 'observed'}
    assert points[-2] == {'period': '2026-10', 'value': 46, 'status': 'observed'}
    assert points[-1] == {'period': '2026-11', 'value': 38, 'status': 'observed', 'partial': True}
    assert '60 days' in group['note']
    # Regional rows are overlapping breakdowns, not extra GTA homes.
    lines = (FIXTURES / 'homeleader-pos.csv').read_text().splitlines()
    shuffled = '\n'.join(lines[:2] + list(reversed(lines[2:])))
    assert parse_homeleader(shuffled) == group


@pytest.mark.parametrize('damage', ['timestamp', 'columns', 'decimal', 'negative', 'duplicate',
                                    'gap', 'terminal', 'partial', 'subtotal', 'excess'])
def test_homeleader_rejects_malformed_or_incomplete_feed(damage):
    raw = (FIXTURES / 'homeleader-pos.csv').read_text()
    if damage == 'timestamp': raw = raw.replace('Data as of', 'Updated')
    elif damage == 'columns': raw = raw.replace('new_listings,', 'new_count,')
    elif damage == 'decimal': raw = raw.replace('53,37,33,', '53,37,33.5,')
    elif damage == 'negative': raw = raw.replace('53,37,33,', '53,37,-33,')
    elif damage == 'duplicate': raw += '\n' + next(line for line in raw.splitlines() if line.startswith('2025-01,gta,'))
    elif damage == 'gap': raw = '\n'.join(line for line in raw.splitlines() if not line.startswith('2025-02,gta,'))
    elif damage == 'terminal': raw = '\n'.join(line for line in raw.splitlines() if not line.startswith('"2026-11 (to date)",gta,'))
    elif damage == 'partial': raw = raw.replace('2026-11 (to date)', '2026-11')
    elif damage == 'subtotal': raw = raw.replace('2025-01,gta,,,,', '2025-01,gta,Toronto,,,')
    else: raw = raw.replace('53,37,33,', '53,37,38,')
    with pytest.raises(ValueError): parse_homeleader(raw)


def test_teranet_uses_embedded_numeric_data_without_executing_scripts():
    group = parse_teranet((FIXTURES / 'teranet-power-sale.html').read_text())
    points = group['series'][0]['points']
    assert group['unit'] == 'transfers'
    assert [p['value'] for p in points] == [4410, 3712, 2596, 2096, 1977, 1472, 942, 578, 1104, 2123, 2979]
    assert [p['period'] for p in points] == [str(year) for year in range(2015, 2026)]
    assert 'Annual completed transfers' in group['note']


@pytest.mark.parametrize('damage', ['edition', 'chart', 'truncated', 'negative', 'totals'])
def test_teranet_rejects_changed_or_incomplete_report(damage):
    raw = (FIXTURES / 'teranet-power-sale.html').read_text()
    if damage == 'edition': raw = raw.replace('2015 to 2025', '2016 to 2026')
    elif damage == 'chart': raw = raw.replace('Power of Sale Trends - Years', 'Other chart')
    elif damage == 'truncated': raw = raw.replace('2123,2979', '2123')
    elif damage == 'negative': raw = raw.replace('4410,3712', '-4410,3712')
    else: raw = raw.replace('2123,2979', '2123,2980')
    with pytest.raises(ValueError): parse_teranet(raw)


@pytest.mark.parametrize('failed_source', [fetch_data.HOMELEADER_CSV, fetch_data.TERANET])
def test_required_new_source_failure_preserves_published_data(tmp_path, monkeypatch, failed_source):
    data = json.loads((ROOT / 'data/series.json').read_text())
    old_groups = [g for g in data['groups'] if g['id'] in {'provinces', 'lenders', 'private', 'consumer', 'outlook'}]
    monkeypatch.setattr(fetch_data, 'parse_cmhc', lambda _: deepcopy(old_groups))
    annual = next(g for g in data['groups'] if g['id'] == 'annual')['series'][0]['points']
    monkeypatch.setattr(fetch_data, 'parse_annual', lambda _: annual)

    def monthly(_, source):
        vintage = {'mw2112.pdf':'2021', 'mw2312.pdf':'2023', 'mw2512.pdf':'2025', 'mw2609.pdf':'latest'}[source.rsplit('/',1)[-1]]
        return fetch_data.parse_monthly_text((FIXTURES / f'trreb-{vintage}.txt').read_text(), source)
    monkeypatch.setattr(fetch_data, 'parse_monthly', monthly)

    def get(url):
        if url == failed_source: raise RuntimeError('Required provider unavailable')
        if url == fetch_data.HOMELEADER_CSV:
            return SimpleNamespace(text=(FIXTURES / 'homeleader-pos.csv').read_text())
        return SimpleNamespace(content=b'', text='<a href="/mw2609.pdf">Latest</a>')

    target = tmp_path / 'series.json'
    target.write_text(json.dumps(data))
    before, mtime = target.read_bytes(), target.stat().st_mtime_ns
    with pytest.raises(RuntimeError, match='Required provider'):
        fetch_data.publish(fetch_data.collect(get), target)
    assert target.read_bytes() == before
    assert target.stat().st_mtime_ns == mtime
