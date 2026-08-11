"""tests/test_anomaly_engine.py — détection d'anomalies de cours : exactitude + honnêteté."""
from vertex.engines import anomaly


def _flat(n, base=100.0, step=0.05):
    """Série calme : alternance ±step % — σ non nulle, aucun |z|≥2 attendu du bruit."""
    cl = [base]
    for i in range(n - 1):
        cl.append(round(cl[-1] * (1 + (step if i % 2 == 0 else -step) / 100), 6))
    return cl


def test_spike_detected_with_exact_index():
    cl = _flat(30)
    cl.append(round(cl[-1] * 1.08, 6))          # +8 % : spike évident
    d = anomaly.scan(cl)
    assert d['empty'] is False
    spikes = [e for e in d['events'] if e['kind'] == 'spike']
    assert len(spikes) == 1
    assert spikes[0]['i'] == len(cl) - 1        # index exact de la clôture anormale
    assert spikes[0]['ret_pct'] == 8.0
    assert spikes[0]['z'] > 2
    assert d['n_spikes'] == 1


def test_calm_series_has_no_spikes():
    d = anomaly.scan(_flat(40))
    assert d['n_spikes'] == 0
    assert 'Aucun mouvement statistiquement anormal' in d['narrative']


def test_streak_detected():
    cl = _flat(30)
    for _ in range(6):                          # 6 hausses consécutives
        cl.append(round(cl[-1] * 1.001, 6))
    d = anomaly.scan(cl)
    st = [e for e in d['events'] if e['kind'] == 'streak']
    assert st and st[0]['days'] >= 6 and st[0]['up'] is True
    assert d['streak'] >= 6


def test_vol_shift_detected():
    cl = _flat(40, step=0.05)                   # calme
    for i in range(5):                          # 5 jours agités (±1 %)
        cl.append(round(cl[-1] * (1 + (0.01 if i % 2 == 0 else -0.01)), 6))
    d = anomaly.scan(cl)
    vs = [e for e in d['events'] if e['kind'] == 'vol_shift']
    assert vs and vs[0]['ratio'] >= 1.8
    assert d['vol_ratio'] >= 1.8


def test_extreme_high_detected():
    cl = _flat(30)
    cl.append(round(max(cl) * 1.001, 6))        # nouveau plus haut
    d = anomaly.scan(cl)
    assert d['extreme'] == 'high'
    assert any(e['kind'] == 'extreme' and e['side'] == 'high' for e in d['events'])


def test_short_series_is_honest():
    d = anomaly.scan([100, 101, 102])
    assert d['empty'] is True
    assert d['events'] == []
    assert 'pas de statistique inventée' in d['reason']


def test_bad_values_filtered_not_invented():
    cl = _flat(30) + [None, 'x', -5]            # points invalides ignorés
    d = anomaly.scan(cl)
    assert d['points'] == 30


def test_narrative_is_descriptive_not_forecast():
    d = anomaly.scan(_flat(30))
    assert 'pas une prévision' in d['narrative']


def test_anomalies_route_reads_real_series():
    import terminal
    from vertex.app.state import scan_state
    cl = [100.0]
    for i in range(30):
        cl.append(round(cl[-1] * (1 + (0.0005 if i % 2 == 0 else -0.0005)), 6))
    cl.append(round(cl[-1] * 1.07, 6))          # spike réel
    scan_state.setdefault('detail', {})['TESTX'] = {'series': {'close': cl}}
    try:
        d = terminal.app.test_client().get('/api/anomalies/TESTX').get_json()
        assert d['symbol'] == 'TESTX'
        assert d['empty'] is False
        assert d['n_spikes'] >= 1
    finally:
        scan_state['detail'].pop('TESTX', None)


def test_analysis_page_has_anomaly_card():
    import terminal
    body = terminal.app.test_client().get('/analysis/AAPL').get_data(as_text=True)
    assert 'an-anomaly' in body
    assert 'anomaly-scan.js' in body
    assert 'Scanner d' in body                   # titre de la carte
