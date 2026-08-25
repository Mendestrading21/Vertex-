"""Vertex 1.0 — LE GRAPHE DE CONNAISSANCE NE SE RECONSTRUIT PAS A CHAQUE VUE.

Mesure d'origine : `/api/skyler/graph` rendait 200 en **26 s**, et
`/api/skyler/graph/<sym>` reconstruisait tout le graphe avant de propager —
26 s de plus. Le balayage des 92 surfaces les comptait « en erreur » alors
qu'elles repondaient : elles etaient seulement trop lentes pour etre vues.
Un widget qui met 26 s ne s'affiche pas, il tourne puis le navigateur
abandonne.

Ce fichier garde les deux moities du correctif :

- le graphe est memoise pour un etat de scan donne ;
- la CLE nomme tout ce dont il depend. Un cache dont la cle oublie une entree
  sert une reponse perimee en la presentant comme fraiche — ce qui est pire
  que la lenteur qu'il corrige.
"""
from __future__ import annotations

import time

from vertex.app.routes import analysis_api as api


def _vider():
    api._KG_MEMO.update({'clef': None, 'valeur': None, 'construit_a': None})
    #  Le lot « graphe chaud » a ajoute une reconstruction de FOND : sans la
    #  remettre a zero, un chantier laisse par un banc precedent bloquerait le
    #  suivant, qui echouerait pour une raison sans rapport avec ce qu'il teste.
    api._KG_CHANTIER.update({'actif': False, 'echec_a': None, 'erreur': None})


def _attendre_chantier(secondes=10.0):
    """La reconstruction est asynchrone : l'attendre EXPLICITEMENT vaut mieux
    qu'esperer que l'ordonnanceur l'ait faite avant l'assertion suivante."""
    fin = time.monotonic() + secondes
    while api._KG_CHANTIER['actif'] and time.monotonic() < fin:
        time.sleep(0.02)


#  ------------------------------------------------------- la memoisation agit

def test_le_graphe_n_est_construit_qu_une_fois_par_etat_de_scan(monkeypatch):
    """Deux vues du meme scan doivent couter UNE construction. C'est tout
    l'ecart entre 26 s et l'instantane."""
    _vider()
    appels = []
    monkeypatch.setattr(api, '_kg_construire', lambda: appels.append(1) or {'g': 1})
    monkeypatch.setattr(api, '_kg_clef', lambda: ('scan-1', 5, 0, None))
    #  L'egalite EXACTE etait accessoire : depuis le lot « graphe chaud », la
    #  charge porte aussi sa fraicheur. Ce qui est garde ici, c'est le nombre
    #  de constructions — l'ecart entre 26 s et l'instantane.
    for _ in range(3):
        g = api._kg_build()
        assert g['g'] == 1
        assert g['fraicheur'] == api.FRAICHEUR_LIVE
    assert len(appels) == 1, 'le graphe a ete reconstruit alors que rien ne bougeait'


def test_un_nouveau_scan_invalide_le_graphe(monkeypatch):
    """Sinon l'ecran montrerait le graphe de l'avant-dernier scan en le datant
    du dernier — un mensonge de fraicheur, pas une optimisation."""
    _vider()
    appels = []
    monkeypatch.setattr(api, '_kg_construire', lambda: appels.append(1) or {'n': len(appels)})
    clef = {'v': ('scan-1', 5, 0, None)}
    monkeypatch.setattr(api, '_kg_clef', lambda: clef['v'])
    api._kg_build()
    clef['v'] = ('scan-2', 5, 0, None)          # le scan a tourne
    #  Depuis le lot « graphe chaud », le visiteur recoit l'ancien graphe
    #  MARQUE date pendant que le neuf se construit en fond. La reconstruction
    #  a bien lieu — elle ne se paie simplement plus dans la requete.
    servi = api._kg_build()
    assert servi['fraicheur'] == api.FRAICHEUR_STALE
    _attendre_chantier()
    assert len(appels) == 2, 'un nouveau scan doit reconstruire'
    assert api._kg_build()['fraicheur'] == api.FRAICHEUR_LIVE


#  ------------------------------------------- la cle nomme TOUTES ses entrees

def test_la_cle_couvre_le_scan_l_univers_le_calendrier_et_le_desk():
    """Les positions vivent dans `desk_data.json`, HORS du scan. Une cle qui
    les oublie figerait le graphe sur un portefeuille perime."""
    src = open(api.__file__, encoding='utf-8').read()
    deb = src.index('def _kg_clef')
    corps = src[deb:src.index('def _kg_build', deb)]
    assert "scan_state.get('scan_ts')" in corps, 'la cle doit suivre le scan'
    assert 'len(detail)' in corps, "la cle doit suivre la taille de l'univers"
    assert 'cal_state' in corps, 'la cle doit suivre le calendrier'
    assert 'desk_data.json' in corps and 'getmtime' in corps, (
        'la cle doit suivre le desk — les positions changent hors du scan')


def test_le_desk_modifie_invalide_le_graphe(monkeypatch):
    """Une position ajoutee doit se voir dans le graphe sans attendre le scan
    suivant."""
    _vider()
    appels = []
    monkeypatch.setattr(api, '_kg_construire', lambda: appels.append(1) or {'n': len(appels)})
    clef = {'v': ('scan-1', 5, 0, 1000.0)}
    monkeypatch.setattr(api, '_kg_clef', lambda: clef['v'])
    api._kg_build()
    clef['v'] = ('scan-1', 5, 0, 2000.0)        # desk_data.json reecrit
    api._kg_build()
    assert len(appels) == 2, 'un desk modifie doit reconstruire le graphe'


def test_la_propagation_par_symbole_passe_par_le_meme_cache():
    """`/api/skyler/graph/<sym>` appelait `_kg_build()` en plein : sans cache
    partage, la fiche d'un titre payait la construction complete."""
    src = open(api.__file__, encoding='utf-8').read()
    deb = src.index('def api_skyler_graph_sym')
    corps = src[deb:deb + 900]
    assert '_kg_build()' in corps, (
        'la route par symbole doit passer par le graphe memoise, pas '
        'reconstruire pour son compte')
