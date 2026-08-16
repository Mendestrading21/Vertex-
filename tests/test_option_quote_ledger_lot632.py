from vertex.services import persist
from vertex.tracking import repository as repo


def _contract(**overrides):
    out = {'sym': 'ABC', 'type': 'CALL', 'exp': '2026-12-18', 'strike': 125.0,
           'bid': 3.8, 'ask': 4.2, 'mid': 4.0, 'oi': 900}
    out.update(overrides)
    return out


def _create_option():
    return repo.create(tracking_id='opt-ledger-1', entity_type='OPTION', symbol='ABC',
                       contract_id='ABC|2026-12-18|125|C', started_at='2026-08-16T10:00:00Z',
                       quote={'bid': 3.0, 'ask': 3.4, 'source': 'initial_board'})


def test_option_board_ledger_records_observed_mid_with_evidence(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    _create_option()
    stats = repo.record_option_board([_contract()], at='2026-08-16T10:05:00Z', source='ibkr')
    tracked = repo.get('opt-ledger-1')
    assert stats['snapshots_added'] == 1
    assert tracked['snapshots'][-1]['price'] == 4.0
    assert tracked['snapshots'][-1]['evidence']['price_kind'] == 'BID_ASK_MID'
    assert tracked['data_quality']['last_option_quote_resolution']['available'] is True


def test_option_board_ledger_normalizes_strike_and_deduplicates_same_as_of(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    _create_option()
    repo.record_option_board([_contract(strike=125.0)], at='2026-08-16T10:05:00Z')
    stats = repo.record_option_board([_contract(strike=125)], at='2026-08-16T10:05:00Z')
    assert stats['skipped_same_as_of'] == 1
    assert len(repo.get('opt-ledger-1')['snapshots']) == 1


def test_option_board_ledger_keeps_missing_contract_explicit(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    _create_option()
    stats = repo.record_option_board([], at='2026-08-16T10:05:00Z')
    tracked = repo.get('opt-ledger-1')
    assert stats['unresolved'] == 1
    assert tracked['snapshots'] == []
    assert 'absent' in tracked['data_quality']['last_option_quote_resolution']['reason']
