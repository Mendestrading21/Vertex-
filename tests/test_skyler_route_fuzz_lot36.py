"""tests/test_skyler_route_fuzz_lot36.py — SKYLER LOT 36 : fuzz du cœur HTTP.

Batterie à LISTE FIXE (zéro aléatoire) sur `/api/skyler/<sym>` — la route la
plus riche du programme (packet + red-team + calibration + décision + hooks
journal/mémoire/séances). Contrat : JAMAIS de 500 ; symbole inconnu ou
dégénéré → décision honnête (blocs INSUFFISANTS, jamais inventés) ; magasins
runtime corrompus → les hooks fail-safe ne cassent JAMAIS la décision ;
déterminisme à état constant ; clamp du symbole (upper, ≤ 12) respecté.
"""
import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Client avec magasins runtime isolés (jamais les vrais fichiers)."""
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    return terminal.app.test_client()


DEGENERATE_SYMS = ('ZZZINCONNU', 'aapl', 'A' * 500, 'AA PL', "l'sym",
                   '<script>alert(1)</script>', 'sym%00', 'éàç漢字',
                   '..', '-', '_', '0', 'NULL', 'undefined')


def test_degenerate_symbols_never_500_always_structured(client):
    for s in DEGENERATE_SYMS:
        r = client.get('/api/skyler/' + s)
        assert r.status_code != 500, 'sym=%r → HTTP 500' % s
        if r.status_code == 200:
            d = r.get_json()
            dec = d['decision']
            assert dec['generator'] == 'deterministic'
            assert 'score' in dec and 'gates' in dec
            assert len(str(d.get('symbol') or '')) <= 12    # clamp respecté


def test_unknown_symbol_honest_insufficient_never_invented(client):
    dec = client.get('/api/skyler/ZZZINCONNU').get_json()['decision']
    # titre hors scan : aucune donnée technique → la note est incomplète PAR
    # CONSTRUCTION et la décision ne peut pas être un achat
    assert dec['score']['insufficient_blocks']
    assert dec['decision'] in ('ATTENDRE', 'REFUSER')
    assert 'jamais un ordre' in dec['note']


def test_readonly_note_always_served(client):
    for s in ('ZZZINCONNU', 'AAPL'):
        dec = client.get('/api/skyler/' + s).get_json()['decision']
        assert 'READONLY' in dec['note'] or 'jamais un ordre' in dec['note']


def test_deterministic_at_constant_state(client):
    a = client.get('/api/skyler/ZZZINCONNU').get_json()['decision']
    b = client.get('/api/skyler/ZZZINCONNU').get_json()['decision']
    assert a['decision'] == b['decision']
    assert a['score']['total'] == b['score']['total']
    assert a['level'] == b['level']
    assert a['confidence'] == b['confidence']


CORRUPTED_STORES = (
    ('skyler_memory.json', '"corrompu"'),
    ('skyler_memory.json', '{"decisions": "x", "outcomes": 42}'),
    ('skyler_memory.json', '{"decisions": [1, "a", null], "outcomes": ["b"]}'),
    ('skyler_journal.json', '{"pas": "une liste"}'),
    ('skyler_sessions.json', '[1, 2, 3]'),
    ('desk_data.json', '"corrompu"'),
)


def test_corrupted_runtime_stores_never_break_decision(client, tmp_path):
    """Chaque magasin corrompu, un par un : les hooks fail-safe (journal,
    mémoire, séances, portefeuille, calibration) ne cassent JAMAIS la
    décision servie — et un second appel (chemin dédupliqué) tient aussi."""
    for name, raw in CORRUPTED_STORES:
        (tmp_path / name).write_text(raw, encoding='utf-8')
        for _ in range(2):
            r = client.get('/api/skyler/ZZZINCONNU')
            assert r.status_code == 200, '%s corrompu → HTTP %d' % (name, r.status_code)
            assert r.get_json()['decision']['generator'] == 'deterministic'
        (tmp_path / name).unlink()


def test_all_stores_corrupted_at_once_still_served(client, tmp_path):
    for name, raw in CORRUPTED_STORES[:1] + CORRUPTED_STORES[3:]:
        (tmp_path / name).write_text(raw, encoding='utf-8')
    r = client.get('/api/skyler/ZZZINCONNU')
    assert r.status_code == 200
    d = r.get_json()
    assert d['decision']['generator'] == 'deterministic'


def test_calibration_scope_survives_corrupted_memory(client, tmp_path):
    """Mémoire corrompue → la calibration retombe fail-safe (facteur absent ou
    global 0,50) — jamais une cellule inventée, jamais un crash."""
    (tmp_path / 'skyler_memory.json').write_text(
        '{"decisions": [7, null, "x"], "outcomes": "y"}', encoding='utf-8')
    d = client.get('/api/skyler/ZZZINCONNU').get_json()['decision']
    conf = d.get('confidence') or {}
    factors = conf.get('factors') or {}
    calib = factors.get('calibration')
    if isinstance(calib, dict) and 'value' in calib:
        assert calib['value'] == 0.5
