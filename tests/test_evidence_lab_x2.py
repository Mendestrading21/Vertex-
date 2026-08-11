"""tests/test_evidence_lab_x2.py — SKYLER X2 : laboratoire d'évidence.

Statistiques EX POST sur les événements passés de la série RÉELLE : rendements
avant (forward) à 1/5/10 barres après chaque spike |z|≥2 historique, MFE/MAE
exacts sur 10 barres. IN-SAMPLE et DESCRIPTIF — jamais présenté comme un
backtest de stratégie ; événements non mesurables (trop récents) comptés et
dits ; série trop courte → indisponible honnête.
"""
import pytest

from vertex.engines import evidence_lab as EV


def _series_with_spike():
    """45 clôtures : plat à 100 (bruit ±0.05 %), spike +8 % à l'index 30, puis
    +1 %/barre pendant 10 barres — tout est calculable à la main."""
    cl = [100.0]
    for i in range(29):
        cl.append(round(cl[-1] * (1 + (0.0005 if i % 2 == 0 else -0.0005)), 6))
    cl.append(round(cl[-1] * 1.08, 6))          # index 30 : spike
    for _ in range(10):
        cl.append(round(cl[-1] * 1.01, 6))      # suites contrôlées
    for _ in range(4):
        cl.append(cl[-1])
    return cl


def test_forward_returns_and_mfe_hand_computed():
    cl = _series_with_spike()
    d = EV.study(cl)
    assert d['available'] is True
    assert d['n_events'] >= 1
    up = d['up']
    assert up['n_measured'] >= 1
    # à la main : après le spike (index 30), +1 %/barre → fwd_5 = 1.01^5 - 1 ≈ +5.10 %
    assert up['median_fwd_5_pct'] == pytest.approx(5.10, abs=0.05)
    assert up['median_fwd_1_pct'] == pytest.approx(1.0, abs=0.02)
    assert up['median_fwd_10_pct'] == pytest.approx((1.01 ** 10 - 1) * 100, abs=0.1)
    # MFE sur 10 barres = +10.46 % ; MAE = +1 % (jamais sous l'entrée) → MAE ≥ 0
    assert up['median_mfe_pct'] == pytest.approx((1.01 ** 10 - 1) * 100, abs=0.1)
    assert up['median_mae_pct'] >= 0.9


def test_down_spikes_bucketed_separately():
    cl = [100.0]
    for i in range(29):
        cl.append(round(cl[-1] * (1 + (0.0005 if i % 2 == 0 else -0.0005)), 6))
    cl.append(round(cl[-1] * 0.92, 6))          # spike -8 %
    for _ in range(12):
        cl.append(round(cl[-1] * 0.995, 6))     # dérive -0.5 %/barre
    d = EV.study(cl)
    assert d['down']['n_measured'] >= 1
    assert d['down']['median_fwd_5_pct'] == pytest.approx((0.995 ** 5 - 1) * 100, abs=0.1)
    assert d['up']['n_measured'] == 0           # aucun spike haussier inventé


def test_unmeasurable_recent_events_counted_not_invented():
    """Un spike dans les 10 dernières barres n'a pas d'avenir mesurable → compté
    non mesurable, jamais extrapolé."""
    cl = _series_with_spike()
    cl.append(round(cl[-1] * 1.08, 6))          # spike tout en fin de série
    d = EV.study(cl)
    assert d['n_unmeasurable'] >= 1


def test_short_series_honest():
    d = EV.study([100.0, 101.0, 102.0])
    assert d['available'] is False and 'reason' in d


def test_no_events_honest():
    cl = [100.0]
    for i in range(59):
        cl.append(round(cl[-1] * (1 + (0.0005 if i % 2 == 0 else -0.0005)), 6))
    d = EV.study(cl)
    assert d['available'] is True and d['n_events'] == 0
    assert d['up']['n_measured'] == 0 and d['up']['median_fwd_5_pct'] is None


def test_labels_in_sample_not_backtest():
    d = EV.study(_series_with_spike())
    assert 'in-sample' in d['note'].lower() or 'échantillon' in d['note'].lower()
    assert 'backtest' in d['note'].lower()      # la mise en garde est explicite
    assert d['generator'] == 'deterministic'


def test_evidence_route():
    import terminal
    from vertex.app.state import scan_state
    scan_state.setdefault('detail', {})['EVLX'] = {'series': {'close': _series_with_spike()}}
    try:
        d = terminal.app.test_client().get('/api/evidence/EVLX').get_json()
        assert d['symbol'] == 'EVLX'
        assert d['available'] is True and d['n_events'] >= 1
        assert d['series_source'] == 'scan.series.close'
    finally:
        scan_state['detail'].pop('EVLX', None)


def test_analysis_page_has_evidence_card():
    """Gardien X2 : la fiche Analyse expose le laboratoire d'évidence."""
    import terminal
    body = terminal.app.test_client().get('/analysis/AAPL').get_data(as_text=True)
    assert 'an-evidence' in body
    assert 'loadEvidence' in body
