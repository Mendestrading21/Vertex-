"""
LOT 175 — Caractérisation HTTP de la SESSION D'ANALYSE
(`vertex/app/routes/session_api.py`). Le moteur du digest (lot 150) et
le manifest (continuity lot 5) sont couverts ; la lacune était la
LOGIQUE DE RESTAURATION de la route /api/session/digest : mémorisation
du dernier digest prêt, écriture disque throttlée, instantané resservi
marqué « restored » avec l'ÂGE EFFACÉ (honnêteté), démarrage à froid
« analyzing ». Plus deux trous du manifest (bool rejeté, plafond 100 %).
"""
import pytest

import terminal
from vertex.app.routes import session_api as SA
from vertex.services import persist


_READY = {'state': 'ready', 'as_of': '09:00', 'age_s': 5, 'regime': {},
          'opportunities': [], 'catalysts': [], 'market': {},
          'confidence': None, 'generator': 'deterministic'}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    saved = dict(SA._last)
    SA._last.update({'digest': None, 'written': 0.0})
    yield terminal.app.test_client()
    SA._last.update(saved)


def _force(monkeypatch, digest):
    monkeypatch.setattr(SA.session_digest, 'build', lambda *a, **k: dict(digest))


# ── /api/session/digest : mémorisation, restauration, honnêteté de l'âge ─────

def test_premiere_session_a_froid_analyzing(client, monkeypatch):
    # Aucun instantané mémorisé ni sur disque : l'état 'analyzing' est servi
    # tel quel — jamais un digest inventé.
    _force(monkeypatch, {'state': 'analyzing', 'as_of': None})
    d = client.get('/api/session/digest').get_json()
    assert d['state'] == 'analyzing'


def test_digest_pret_servi_memorise_et_ecrit_sur_disque(client, monkeypatch, tmp_path):
    _force(monkeypatch, _READY)
    d = client.get('/api/session/digest').get_json()
    assert d['state'] == 'ready' and d['age_s'] == 5
    assert SA._last['digest']['as_of'] == '09:00'   # mémorisé pour la restauration
    assert (tmp_path / 'session_digest_cache.json').exists()   # persisté


def test_ecriture_disque_throttlee_une_seule_fois(client, monkeypatch):
    writes = []
    real = persist.save_json
    monkeypatch.setattr(persist, 'save_json',
                        lambda name, data: writes.append(name) or real(name, data))
    _force(monkeypatch, _READY)
    client.get('/api/session/digest')
    client.get('/api/session/digest')               # < 30 s après la première
    assert writes.count('session_digest_cache.json') == 1


def test_instantane_restaure_age_efface_honnete(client, monkeypatch):
    # Un scan qui retombe « pas prêt » ressert le dernier instantané, marqué
    # 'restored', l'as_of absolu conservé mais l'ÂGE EFFACÉ : l'âge figé au
    # build sous-estimerait la vraie ancienneté — le client n'affiche que
    # l'horodatage absolu, jamais un âge faussement frais.
    _force(monkeypatch, _READY)
    client.get('/api/session/digest')               # mémorise le digest prêt
    _force(monkeypatch, {'state': 'analyzing', 'as_of': None})
    d = client.get('/api/session/digest').get_json()
    assert d['state'] == 'restored'
    assert d['as_of'] == '09:00'                    # horodatage absolu conservé
    assert d['age_s'] is None                       # jamais un âge faussement frais


def test_restauration_ne_mute_pas_l_instantane_memorise(client, monkeypatch):
    # La restauration sert une COPIE : l'instantané mémorisé reste 'ready'
    # (sinon une seconde restauration servirait un état déjà dégradé).
    _force(monkeypatch, _READY)
    client.get('/api/session/digest')
    _force(monkeypatch, {'state': 'analyzing', 'as_of': None})
    client.get('/api/session/digest')
    assert SA._last['digest']['state'] == 'ready'
    assert SA._last['digest']['age_s'] == 5


# ── Manifest : deux trous du moteur pur ──────────────────────────────────────

def test_session_id_refuse_le_booleen():
    from vertex.engines import session_snapshot as SS
    assert SS.session_id_for(True) is None          # bool est un int en Python
    assert SS.session_id_for('173000') is None      # chaîne refusée aussi


def test_couverture_plafonnee_a_100_univers_perime():
    # scanned 600 > universe 517 (univers périmé) → 100 %, jamais 116 %.
    from vertex.engines import session_snapshot as SS
    m = SS.build({'rows': [{'symbol': 'A'}], 'detail': {},
                  'scan_ts': 1.0, 'scanned_n': 600, 'universe_n': 517})
    assert m['coverage_pct'] == 100
    assert m['quality_pct'] == 0                    # 0/1 couvert par le détail


# ── Invariant produit : la couche HTTP est bien LECTURE SEULE ────────────────

def test_module_session_api_sans_verbe_d_ordre():
    import inspect
    src = inspect.getsource(SA).lower()
    for verb in ('placeorder', 'place_order', 'submit_order', 'transmit'):
        assert verb not in src
