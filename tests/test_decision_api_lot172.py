"""
LOT 172 — Caractérisation HTTP des deux endpoints de gestion de position
(`vertex/app/routes/decision_api.py` — /api/position-decision/<sym> et
/api/options-for/<sym>, à ZÉRO test alors que les moteurs servis
(`recommendation.position_decision` / `options_for_position`) sont
couverts par le lot 87). Ces tests figent le CÂBLAGE HTTP : parsing des
paramètres (corrompu → None, jamais un crash), normalisation du type
détenu, sous-jacent honnête, board vide → note explicite.
"""
import pytest

import terminal
from vertex.app.state import scan_state


@pytest.fixture()
def client():
    saved = scan_state.get('options_board')
    yield terminal.app.test_client()
    scan_state['options_board'] = saved


def _board():
    return [
        {'sym': 'TSTQ', 'type': 'CALL', 'strike': 105, 'exp': '2026-12-18',
         'dte': 45, 'quality': 80, 'grade': 'A', 'delta': 0.30, 'mid': 3.5, 'pop': 55},
        {'sym': 'TSTQ', 'type': 'CALL', 'strike': 100, 'exp': '2027-12-17',
         'dte': 365, 'quality': 70, 'grade': 'B', 'delta': 0.75, 'mid': 15.0, 'pop': 60},
        {'sym': 'TSTQ', 'type': 'PUT', 'strike': 95, 'exp': '2026-11-20',
         'dte': 60, 'quality': 65, 'grade': 'B', 'delta': -0.30, 'mid': 2.5, 'pop': 50},
        {'sym': 'OTHR', 'type': 'CALL', 'strike': 50, 'exp': '2026-12-18',
         'dte': 45, 'quality': 90, 'grade': 'S', 'delta': 0.5, 'mid': 5, 'pop': 60},
    ]


# ── /api/position-decision/<sym> : la gestion de position par HTTP ───────────

def test_symbole_inconnu_hold_et_sous_jacent_honnete(client):
    # Titre absent du scan : la gestion répond quand même (HOLD par défaut)
    # et le sous-jacent est étiqueté DATA_INSUFFICIENT — jamais inventé.
    r = client.get('/api/position-decision/tstq').get_json()
    assert r['symbol'] == 'TSTQ'                    # symbole normalisé majuscules
    assert r['verdict'] == 'HOLD' and r['confidence'] == 60
    assert r['underlying'] == {'decision': 'DATA_INSUFFICIENT',
                               'label': 'Données insuffisantes', 'tone': 'gray'}
    assert r['underlying_availability']['available'] is True
    assert r['underlying_availability']['status'] == 'UNDERLYING_ANALYSIS_AVAILABLE'


def test_repli_sous_jacent_expose_sans_modifier_recommandation(client, monkeypatch):
    from vertex.app.routes import decision_api

    def _unavailable(*args, **kwargs):
        raise RuntimeError('interne')

    monkeypatch.setattr(decision_api._decision, 'evaluate', _unavailable)
    r = client.get('/api/position-decision/TSTQ').get_json()
    assert r['verdict'] == 'HOLD'
    assert r['underlying'] is None
    assert r['underlying_availability'] == {
        'available': False,
        'status': 'UNDERLYING_ANALYSIS_UNAVAILABLE',
        'reason': 'analyse sous-jacente indisponible ; décision de position calculée sans ce contexte',
        'read_only': True,
        'does_not_change_recommendation': True,
    }


def test_stop_touche_via_query_params(client):
    r = client.get('/api/position-decision/TSTQ'
                   '?type=STK&entry=100&stop=95&current=94').get_json()
    assert r['verdict'] == 'EXIT'
    assert r['risk'] == 'perte au stop' and r['confidence'] == 78


def test_params_corrompus_ignores_jamais_de_crash(client):
    # entry=abc, pl_pct=xyz, dte= → tous None (le _f avale l'illisible) :
    # la décision retombe sur HOLD au lieu de casser la requête.
    r = client.get('/api/position-decision/TSTQ?entry=abc&pl_pct=xyz&dte=')
    assert r.status_code == 200
    assert r.get_json()['verdict'] == 'HOLD'


def test_seuils_de_discipline_stock_20_option_25_par_http(client):
    # La distinction action/option traverse la couche HTTP intacte.
    g = lambda q: client.get('/api/position-decision/TSTQ?' + q).get_json()['verdict']
    assert g('type=STK&pl_pct=-20') == 'EXIT'       # action : -20 % suffit
    assert g('type=CALL&pl_pct=-20') == 'HOLD'      # option : la convexité tolère plus
    assert g('type=CALL&pl_pct=-25') == 'EXIT'      # option : -25 % coupe


def test_theta_commande_pres_de_l_expiration(client):
    r = client.get('/api/position-decision/TSTQ?type=CALL&dte=10&pl_pct=15').get_json()
    assert r['verdict'] == 'TAKE_PROFIT'
    assert r['risk'] == 'thêta / expiration'


# ── /api/options-for/<sym> : les véhicules autour d'une position ─────────────

def test_board_vide_note_explicite_jamais_un_contrat_invente(client):
    scan_state['options_board'] = []
    r = client.get('/api/options-for/tstq').get_json()
    assert r['sym'] == 'TSTQ' and r['held_type'] == 'STK'
    assert r['suggestions'] == []
    assert 'Aucun contrat chargé pour TSTQ' in r['note']


def test_position_action_5_roles_dont_revenu_et_protection(client):
    scan_state['options_board'] = _board()
    r = client.get('/api/options-for/TSTQ').get_json()
    roles = [s['role'] for s in r['suggestions']]
    assert roles == ['CALL', 'PUT', 'LEAPS', 'COVERED_CALL', 'PROTECTIVE_PUT']
    by = {s['role']: s for s in r['suggestions']}
    assert by['CALL']['strike'] == 105              # meilleure qualité (80)
    assert by['LEAPS']['strike'] == 100 and by['LEAPS']['dte'] == 365   # ≥ 300 j
    assert by['COVERED_CALL']['delta'] == 0.30      # fenêtre delta 0.15-0.40
    assert by['PROTECTIVE_PUT']['delta'] == -0.30
    assert r['note'] is None
    # Le titre voisin du board (OTHR, qualité 90) n'est JAMAIS mélangé.
    assert all(s['sym'] == 'TSTQ' for s in r['suggestions'])


def test_position_option_detenue_pas_de_covered_call(client):
    # type ≠ STK → normalisé 'OPT' : revenu/protection (réservés aux actions
    # détenues) disparaissent — on ne vend pas un call couvert sans actions.
    scan_state['options_board'] = _board()
    r = client.get('/api/options-for/TSTQ?type=CALL').get_json()
    assert r['held_type'] == 'OPT'
    assert [s['role'] for s in r['suggestions']] == ['CALL', 'PUT', 'LEAPS']


# ── Invariant produit : la couche HTTP est bien LECTURE SEULE ────────────────

def test_module_decision_api_sans_verbe_d_ordre():
    import inspect
    from vertex.app.routes import decision_api
    src = inspect.getsource(decision_api).lower()
    for verb in ('placeorder', 'place_order', 'submit_order', 'transmit'):
        assert verb not in src
