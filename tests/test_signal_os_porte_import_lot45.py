"""SIGNAL OS · LOT 45 — LA PORTE PAR LAQUELLE DU TEXTE ARBITRAIRE ENTRE.

Réserve nommée deux fois — `SIGNAL-OS-40` §5 et `SIGNAL-OS-42` §4.3 :
`POST /api/skyler/memory/import` est le seul chemin par lequel un texte que le
produit n'a pas calculé entre dans la mémoire décisionnelle. Le balayage des
sorties est **GET seul** (l'invariant READONLY interdit de tirer des POST à
l'aveugle), donc cette porte n'était pas mesurée.

## Ce que l'empreinte protège, et ce qu'elle ne protège pas

Le gestionnaire vérifie un `content_sha256` **avant** toute écriture : une
archive altérée est refusée et rien n'est touché. C'est de l'**intégrité**, pas
de la **provenance** — qui fabrique le bundle calcule aussi son empreinte. Le
contenu reste donc arbitraire par construction, et c'est normal : un import est
une restauration, pas un canal de confiance.

La question n'est donc pas « peut-on stocker du balisage ? » — on le peut. Elle
est : **que font les sorties de ce qui a été stocké ?**

## Comment ce gardien entre, sans tirer un POST

Par la porte du moteur, `decision_memory.merge_memory` — l'appel exact que le
gestionnaire fait après avoir validé l'empreinte. Même discipline qu'au lot 40 :
on emprunte la porte du produit, on n'écrit pas un magasin à la main avec une
forme devinée, et on ne frôle pas l'invariant READONLY.

## Ce qui est verrouillé

1. Le rendu HTML (`/memory/<decision_id>`) **échappe** — c'est le seul endroit
   où un humain lit ce contenu.
2. L'API JSON (`/api/skyler/memory/<decision_id>`) rend le champ **tel quel**,
   et c'est **acceptable aujourd'hui parce qu'aucun consommateur ne le peint** —
   mesuré, pas supposé. Le test l'ancre pour que le jour où un rendu apparaît,
   on choisisse un domicile au lieu d'en découvrir deux (même raisonnement
   qu'au lot 33 pour le double échappement).
"""
import pytest

CHARGE = '<script>alert(1)</script>Thèse "importée"'


@pytest.fixture
def memoire_importee(tmp_path, monkeypatch):
    """Un record entré par la porte de l'import, avec un champ libre piégé."""
    from vertex.engines import decision_memory as dm
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    rec = {
        'memory_schema': dm.MEMORY_SCHEMA_VERSION,
        'decision_id': 'imp45deadbeef00',
        'engine_version': 'importe-0.0.0',
        'symbol': 'IMP45', 'as_of': '2026-08-17', 'recorded_at': '2026-08-17',
        'decision': 'SURVEILLER', 'level': 'B',
        'thesis': CHARGE,                     # champ libre → le vecteur
        'catalyst': None, 'trigger': None, 'invalidation': None,
        'strongest_objection': None, 'minority_opinion': None,
        'operational_state': None, 'confidence': None,
        'score_total': 12, 'score_max': 40, 'demo': True,
    }
    #  LA PORTE DU MOTEUR, pas un POST : `merge_memory` est l'appel que le
    #  gestionnaire fait une fois l'empreinte validée.
    fusion, _ = dm.merge_memory(dm.empty_memory(), {'decisions': [rec],
                                                    'outcomes': []})
    persist.save_json(dm.MEMORY_FILE, fusion)
    import terminal
    return terminal.app.test_client(), rec['decision_id']


def test_la_these_importee_est_bien_stockee(memoire_importee):
    """Sans ce point d'ancrage, les deux tests suivants pourraient passer parce
    que rien n'est entré — un vert qui ne prouve rien."""
    from vertex.engines import decision_memory as dm
    from vertex.services import persist
    mem = persist.load_json(dm.MEMORY_FILE, None) or {}
    rec = dm.find_decision(mem, 'imp45deadbeef00')
    assert rec is not None, 'l\'import n\'a rien stocke — test sans objet'
    assert rec['thesis'] == CHARGE, 'le moteur a transforme le champ libre'


def test_le_rendu_html_echappe_le_texte_importe(memoire_importee):
    """LA propriété. C'est le seul endroit où un humain lit ce contenu."""
    client, did = memoire_importee
    corps = client.get('/memory/%s' % did).get_data(as_text=True)
    assert 'IMP45' in corps, 'la vue ne rend pas le record — test sans objet'
    assert '<script>alert(1)' not in corps, (
        'la vue post-mortem peint du balisage importe VIVANT — '
        'l\'echappement au rendu a saute')
    assert '&lt;script&gt;' in corps, (
        'le texte importe ne ressort pas sous forme echappee : verifier que la '
        'these est bien affichee, sinon ce test ne garde plus rien')


def test_l_api_json_rend_le_champ_tel_quel_et_personne_ne_le_peint(memoire_importee):
    """ANCRE D'UN FAIT MESURÉ, pas un jugement.

    L'API rend le champ brut. Ce n'est pas une fuite aujourd'hui : aucun
    consommateur ne le peint — vérifié en cherchant l'appel dans tout le code
    d'interface. Le jour où un rendu apparaîtra, ce test tombera avec le
    deuxième et il faudra choisir UN domicile pour l'échappement."""
    import pathlib
    client, did = memoire_importee
    blob = client.get('/api/skyler/memory/%s' % did).get_data(as_text=True)
    assert '<script>alert(1)' in blob or '\\u003cscript\\u003ealert(1)' in blob, (
        'l\'API n\'expose plus le champ tel quel — le domicile de '
        'l\'echappement a change, mettre a jour SIGNAL-OS-40 §5')
    consommateurs = [p for p in pathlib.Path('vertex/ui').rglob('*.py')
                     if '/api/skyler/memory/' in p.read_text(encoding='utf-8')
                     and 'memory/export' not in p.read_text(encoding='utf-8')]
    assert not consommateurs, (
        'un consommateur d\'interface lit desormais /api/skyler/memory/<id> '
        '(%s) : il faut decider ou le texte est echappe, une seule fois'
        % ', '.join(str(p) for p in consommateurs))
