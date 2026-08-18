"""SIGNAL OS · LOT 40 — LES NEUF ROUTES À IDENTIFIANT, MESURÉES.

Réserve n°2 de `SIGNAL-OS-38` §4 : neuf règles GET portent un identifiant
(suivi, décision figée, cellule de calibration, position, graphique) et
sortaient du balayage des sorties de news, faute d'id valide dans le jeu de
démonstration. `tools/mesurer_sorties_identites.py` fabrique ces identités par
les portes du produit puis balaie les neuf routes — 9/9 couvertes, aucune ne
sert la charge, témoin vivant.

Ce fichier ne rejoue pas le balayage (vingt-cinq passages du moteur Skyler :
plusieurs minutes, hors de propos dans une suite de 40 s). Il verrouille les
**deux barrières** que la mesure a mises au jour, et qui sont la vraie raison du
zéro — sans elles, un titre d'actualité finirait gelé dans la mémoire
décisionnelle, donc servi par `/api/skyler/memory/<decision_id>`.

1. La route assainit les actualités AVANT de les donner au moteur.
2. Le catalyseur n'est choisi que parmi les événements **datés**, et un
   événement d'actualité n'est jamais daté.

L'une ou l'autre suffirait. Les deux peuvent s'éroder séparément, donc les deux
sont gardées séparément.
"""
import pytest


@pytest.fixture
def persistance(tmp_path, monkeypatch):
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    return persist


TITRE_PIEGE = '<script>alert(1)</script>Résultats "record"'


def test_un_evenement_d_actualite_n_est_jamais_date():
    """PREMIÈRE MOITIÉ de la barrière n°2 — la timeline elle-même.

    `events.build` date les résultats et la macro, jamais une actualité : une
    news n'a pas de date d'échéance, seulement une heure de publication."""
    from vertex.engines import events as E
    out = E.build('TSTQ',
                  news=[{'title': TITRE_PIEGE, 'publisher': 'X', 'time': '2026-01-02'}],
                  earnings=[{'sym': 'TSTQ', 'date': '2026-09-01', 'dte': 15}],
                  macro=[], anomaly=None, as_of='2026-08-17')
    news = [e for e in out['events'] if e['kind'] == 'news']
    assert news, 'la news n\'est pas entree dans la timeline — test sans objet'
    assert all(e['dte'] is None for e in news), (
        'une actualite est desormais DATEE : elle peut devenir le catalyseur, '
        'donc entrer dans la memoire figee et sortir par /api/skyler/memory/<id>')


def test_le_catalyseur_fige_ne_retient_qu_un_evenement_date():
    """SECONDE MOITIÉ — le moteur, mesuré de bout en bout.

    Le catalyseur est gelé tel quel dans le record immuable de la mémoire. S'il
    pouvait porter un titre externe, la mémoire deviendrait une sortie de texte
    externe — et son unique rendu HTML échappe, mais son API JSON, non."""
    from vertex.engines import events as E, skyler_core as sk
    ev = E.build('TSTQ',
                 news=[{'title': TITRE_PIEGE, 'publisher': 'X', 'time': '2026-01-02'}],
                 earnings=[{'sym': 'TSTQ', 'date': '2026-09-01', 'dte': 15}],
                 macro=[], anomaly=None, as_of='2026-08-17')
    d = sk.decide('TSTQ', {'price': 100.0, 'closes': [90.0 + i for i in range(60)]},
                  market=None, events=ev, anomaly=None, as_of='2026-08-17', demo=True)
    assert d['catalyst'] == 'Résultats TSTQ (J-15)', (
        'le catalyseur choisi a change : %r' % d['catalyst'])
    assert '<script>' not in (d['catalyst'] or ''), 'balisage externe dans le catalyseur'


def test_la_route_skyler_assainit_les_actualites_avant_le_moteur(persistance):
    """BARRIÈRE n°1, prise par la route et non par la lecture du code.

    On dépose le titre BRUT dans le magasin du scan — un état que la production
    n'atteint pas (son écrivain unique assainit), mais dont on veut savoir que
    la route survivrait s'il arrivait."""
    import terminal
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    sauve = detail.get('SKY40')
    detail['SKY40'] = {'price': 100.0, 'closes': [90.0 + i for i in range(60)],
                       'news': [{'title': TITRE_PIEGE, 'publisher': 'X',
                                 'time': '2026-01-02', 'link': 'javascript:alert(3)'}]}
    try:
        corps = terminal.app.test_client().get('/api/skyler/SKY40').get_data(as_text=True)
    finally:
        if sauve is None:
            detail.pop('SKY40', None)
        else:
            detail['SKY40'] = sauve
    assert corps, 'la route n\'a rien servi — test sans objet'
    for marqueur in ('<script>alert(1)', 'javascript:alert(3)'):
        assert marqueur not in corps, (
            'la route sert du balisage externe vivant (%s) : l\'assainissement '
            'avant `events.build` a saute' % marqueur)


def test_la_liste_des_routes_a_identifiant_ne_diverge_pas():
    """ANTI-DIVERGENCE. La même liste vit à deux endroits — la réserve du lot 39
    et l'outil du lot 40. Deux copies qui se contredisent valent moins qu'une."""
    from tests.test_signal_os_enumeration_sorties_lot33 import RESERVE_IDENTIFIANTS
    from tools import mesurer_sorties_identites as outil
    assert set(outil.REGLES) == RESERVE_IDENTIFIANTS, (
        'la liste de l\'outil et celle de la reserve ont diverge :\n'
        '  outil seul : %s\n  reserve seule : %s'
        % (sorted(set(outil.REGLES) - RESERVE_IDENTIFIANTS),
           sorted(RESERVE_IDENTIFIANTS - set(outil.REGLES))))


def test_l_outil_ne_touche_pas_l_environnement_a_l_import():
    """Un outil qu'on IMPORTE ne doit pas changer l'environnement du processus.

    `sans_courtier()` pose `NO_IBKR=1` — indispensable au balayage, désastreux
    si le seul fait d'importer le module l'imposait à la suite de tests."""
    import ast
    import pathlib
    src = pathlib.Path('tools/mesurer_sorties_identites.py').read_text(encoding='utf-8')
    for noeud in ast.parse(src).body:
        for sous in ast.walk(noeud):
            if (isinstance(sous, ast.Attribute) and sous.attr in ('environ',)
                    and not isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef))):
                pytest.fail('`os.environ` touche au niveau du module — '
                            'l\'import du module changerait l\'environnement')
