"""tests/test_flux_contrat_simulateur_lot32.py — LOT 32 : le parcours du blueprint.

Le blueprint exige : action primaire d'Options = « Simuler le contrat »,
et « le contexte instrument… suit le parcours Opportunités → Analyse →
Options → Simulateur ». Mesuré : le simulateur ne lisait AUCUN paramètre
d'URL et aucune vue Options n'offrait le lien — le parcours n'existait
pas. Et le refus Options rendait le message brut de l'API. Nés ROUGES.
"""


def _sim():
    return open('vertex/static/vertex/js/pages/simulator.js', encoding='utf-8').read()


def _scan():
    return open('vertex/static/vertex/js/pages/options-scanner.js', encoding='utf-8').read()


def test_le_simulateur_lit_le_contexte_d_url():
    js = _sim()
    assert 'URLSearchParams(location.search)' in js.replace('window.', '')
    for champ in ('sim-sym', 'sim-strike', 'sim-dte', 'sim-mid'):
        assert champ in js
    #  arrivée par clic explicite → le calcul part tout seul
    assert 'prefillDepuisContexte' in js


def test_le_tiroir_du_scanner_offre_simuler_le_contrat():
    js = _scan()
    assert 'Simuler ce contrat' in js
    assert '/simulator?' in js
    #  le lien porte les paramètres RÉELS du candidat (cost/100 = prime mid)
    for p in ('sym:', 'strike:', 'dte:', "q.set('mid'"):
        assert p in js, p
    assert 'c.cost' in js and '/ 100' in js, 'prime mid = coût par contrat / 100'


def test_le_refus_options_parle_les_champs_de_l_interface():
    js = _sim()
    assert 'paramètres invalides' not in js, 'plus de message brut d\'API'
    assert 'Strike, Horizon' in js, (
        'le refus nomme les champs de l\'interface, en français')
