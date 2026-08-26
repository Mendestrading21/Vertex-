"""Vertex 1.0 · G2 — le balayage des surfaces creuses, et ses propres pièges.

Trois défauts de suite ont eu la même forme — **une donnée existait et l'écran
restait vide** — et les trois ont été trouvés *un par un, après signalement*.
L'instrument `mesurer_surfaces_vides` existe pour que le quatrième se voie
avant d'être vécu.

Ce fichier garde surtout **l'instrument contre lui-même**, parce qu'il s'est
trompé trois fois en une heure :

1. il appelait des routes **à effet** (rescan, refresh) : il n'aurait pas
   mesuré, il aurait *agi* — et le premier essai a expiré pour cette raison ;
2. il attendait la fin d'un **flux SSE** qui, par nature, ne finit jamais, et
   classait « en erreur » un endpoint qui fonctionne exactement comme prévu ;
3. il comptait comme pannes ses propres **échantillons inexistants** — un 404
   sur `decision_id=inexistant` est la bonne réponse, pas un défaut.

Un instrument qui fabrique son propre bruit noie les vraies anomalies dedans.
"""
from __future__ import annotations

import pytest

from tools.vertex_1_0.mesurer_surfaces_vides import (
    FLUX_PERMANENTS, ROUTES_A_EFFET, classer, compter_donnees, temoins,
)


def test_les_temoins_de_l_outil_passent():
    assert temoins() == []


# ── Ce qui compte comme une donnée ────────────────────────────────────────

@pytest.mark.parametrize('charge', [
    {}, {'results': {}}, {'items': []}, {'a': None}, {'ok': True},
    {'etat': 'n/d'}, {'source': 'demo'}, {'x': ''}, [],
])
def test_une_charge_sans_donnee_exploitable_compte_zero(charge):
    """La panne silencieuse : HTTP 200, carte propre, et rien dedans."""
    assert compter_donnees(charge) == 0


@pytest.mark.parametrize('charge,attendu', [
    ({'quotes': {'ACN': {'last': 198.0}}}, 1),
    ({'n': 0}, 1),
    ({'lignes': [{'a': 1}, {'b': 2}]}, 2),
    ({'nom': 'Nestlé'}, 1),
])
def test_une_vraie_valeur_est_comptee(charge, attendu):
    assert compter_donnees(charge) == attendu


def test_un_zero_MESURE_n_est_pas_une_absence():
    """« Zéro opportunité aujourd'hui » est une réponse. La confondre avec un
    silence ferait crier l'outil sur une journée calme."""
    assert compter_donnees({'opportunites': 0}) == 1


def test_un_statut_n_est_pas_un_contenu():
    """Sans cette règle, `{'status': 'ok'}` passerait pour une surface pleine —
    et l'outil ne verrait plus JAMAIS un écran creux."""
    assert compter_donnees({'status': 'ok', 'error': 'none'}) == 0


def test_une_structure_cyclique_ou_profonde_ne_fait_pas_boucler():
    profond = {'a': {}}
    n = profond
    for _ in range(30):
        n['a'] = {'a': {}}
        n = n['a']
    assert compter_donnees(profond) == 0


# ── Le classement ─────────────────────────────────────────────────────────

def test_une_surface_marche_vide_est_signalee():
    """C'est précisément là que les trois défauts ont vécu."""
    assert classer('/api/market/summary', 200, {}) == 'VIDE_A_EXAMINER'


def test_un_vide_qui_vient_du_bureau_n_est_pas_une_panne():
    """Pas de trade déclaré, pas d'alerte armée : le vide est une vérité sur
    l'utilisateur. Crier dessus rendrait l'outil inutilisable."""
    assert classer('/api/desk', 200, {}) == 'VIDE_ATTENDU'


def test_un_cache_reseau_vide_n_accuse_pas_le_produit():
    """Dans un environnement sans réseau, ces caches NE PEUVENT PAS être
    remplis. Les confondre ferait accuser le produit d'une contrainte
    d'environnement."""
    assert classer('/api/names', 200, {}) == 'VIDE_CACHE_RESEAU'


def test_un_404_sur_un_echantillon_inexistant_est_la_bonne_reponse():
    assert classer('/api/skyler/memory/inexistant', 404, None) == 'ATTENDU_404'


def test_un_VRAI_404_reste_une_erreur():
    """L'indulgence accordée aux échantillons ne doit pas s'étendre à tout —
    sinon l'outil excuserait une route réellement cassée."""
    assert classer('/api/decision/reelle', 404, None) == 'ERREUR'
    assert classer('/api/market/summary', 500, None) == 'ERREUR'


def test_une_surface_pleine_est_pleine():
    assert classer('/api/market/summary', 200, {'vix': 14.2}) == 'PLEINE'


# ── L'instrument ne doit pas agir, ni attendre l'impossible ───────────────

def test_le_corpus_exclut_les_routes_a_effet():
    """Un instrument qui appelle `/api/rescan` ne mesure plus : il relance un
    scan, consomme du quota, et fausse la mesure suivante."""
    assert '/api/rescan' in ROUTES_A_EFFET
    assert '/api/live/refresh' in ROUTES_A_EFFET


def test_le_corpus_exclut_les_flux_permanents():
    """Un flux SSE ne répond jamais « fini » : c'est sa nature. L'attendre
    faisait expirer l'outil et accusait un endpoint qui fonctionne."""
    assert '/api/live/events' in FLUX_PERMANENTS


def test_le_corpus_vient_de_la_table_de_routage():
    """Une liste écrite à la main diverge au premier ajout de route, et la
    mesure porte alors sur un produit qui n'existe plus."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1]
           / 'tools/vertex_1_0/mesurer_surfaces_vides.py').read_text(encoding='utf-8')
    assert 'url_map.iter_rules()' in src, (
        'le corpus n\'est plus dérivé du routage : il mesurera un produit '
        'périmé sans le dire.')
