"""Vertex 1.0 — LA CAPACITÉ DE `vertex-live`, LA GARANTIE DE `main`.

## Deux branches, deux moitiés du même problème

Le board d'options couvre l'univers par **rotation** IBKR. Entre deux passages,
un titre qu'on consulte peut n'y être pour rien, et **toutes ses cartes options
restent vides** — sans qu'on sache si le titre n'a pas d'options ou si le board
ne l'a pas encore vu.

`vertex-live` a écrit `options/on_demand.py` pour combler ce trou. C'est la
bonne idée, et `main` ne l'a jamais eue.

Mais `live` l'appelle **en synchrone dans quatre routes** — `_od.warm_chain(sym)`
dans `options_intel_api`, `decision_api`, `desk`. Une requête d'utilisateur
déclenche donc une collecte réseau : c'est exactement le défaut **P0.1** que
`main` a fermé, mesuré à **28–48 secondes** sur `/api/ticker/<sym>`, jusqu'à
136,9 s.

`main`, lui, a le magasin d'instantanés : valeur datée servie **immédiatement**,
rafraîchissement en fond, demandes concurrentes coalescées, états `LIVE` /
`DELAYED` / `STALE` / `MISSING` distincts. Mais rien pour combler un trou.

**Ce lot marie les deux.** Greffer `on_demand` tel quel aurait rétabli le défaut
de 40 secondes ; l'ignorer aurait laissé les cartes vides. Ni l'un ni l'autre
n'était acceptable.

## Mesuré

```text
titre dans le board : 1 contrat,  etat=LIVE,    0,0000 s
titre absent        : 0 contrat,  etat=MISSING, 0,0007 s  (chargement en fond)
```

## Ce que ça change pour le lecteur

« Aucun contrat » cessait de vouloir dire deux choses. Il signifie désormais
« pas encore » quand `chargement_en_cours` est vrai, et « ce titre n'a pas
d'options » sinon.
"""
from __future__ import annotations

import time

import pytest

from vertex.app import snapshot as _instantane
from vertex.options import chaine_a_la_demande as C

BOARD = [{'sym': 'AAPL', 'strike': 300.0, 'type': 'CALL'},
         {'sym': 'AAPL', 'strike': 310.0, 'type': 'CALL'},
         {'sym': 'KO', 'strike': 95.0, 'type': 'CALL'}]


#  ═══════════  1. le cas nominal est GRATUIT  ═════════════════════════════════

def test_un_titre_DEJA_dans_le_board_ne_declenche_rien():
    """La chaîne à la demande ne se réveille que sur un trou réel : un titre
    couvert n'a aucune raison de déclencher une collecte."""
    liste, meta = C.contrats('AAPL', BOARD)
    assert len(liste) == 2
    assert meta.etat == _instantane.LIVE
    assert meta.source == 'options_board'


def test_le_board_est_filtre_sur_LE_titre_demande():
    """Rendre le board entier ferait passer les options de KO pour celles
    d'AAPL — la confusion la plus facile à commettre."""
    liste, _ = C.contrats('KO', BOARD)
    assert {c['sym'] for c in liste} == {'KO'}


def test_la_casse_du_symbole_ne_change_rien():
    assert len(C.contrats('aapl', BOARD)[0]) == 2


#  ═══════════  2. le trou réel ne BLOQUE PAS la page  ═════════════════════════

def test_un_titre_ABSENT_rend_la_main_immediatement():
    """Le cœur du lot. `live` appelait `warm_chain` en synchrone dans quatre
    routes ; c'est le défaut P0.1, mesuré à 28–48 s."""
    debut = time.perf_counter()
    liste, meta = C.contrats('ZZQQXX', BOARD)
    duree = time.perf_counter() - debut
    assert duree < 0.5, 'la route a bloque %.2f s' % duree
    assert liste == []
    assert meta.etat == _instantane.MISSING


def test_l_absence_est_NOMMEE_et_non_seulement_vide():
    """« Aucun contrat » voulait dire deux choses : « pas encore » et « ce titre
    n'a pas d'options ». Un lecteur ne pouvait pas les distinguer."""
    e = C.etat('ZZQQXX2', BOARD)
    assert e['contrats'] == 0
    assert e['chargement_en_cours'] is True
    assert 'pas encore' in e['note']


def test_un_symbole_VIDE_ne_declenche_aucun_chargement():
    liste, meta = C.contrats('', BOARD)
    assert liste == [] and meta.etat == _instantane.MISSING
    assert meta.erreur


def test_la_liste_rendue_est_TOUJOURS_iterable():
    """Jamais `None` : un appelant qui itère ne doit pas avoir à s'en soucier —
    c'est ainsi qu'une carte options tombe en erreur au lieu de rester vide."""
    for sym in ('AAPL', 'ZZQQXX3', '', None):
        liste, _ = C.contrats(sym, BOARD)
        assert isinstance(liste, list)


def test_un_board_ABSENT_ne_fait_pas_tomber_l_appel():
    for board in (None, [], [{}], ['pas un dict']):
        liste, meta = C.contrats('AAPL', board)
        assert isinstance(liste, list) and meta is not None


#  ═══════════  3. la collecte passe bien par le magasin  ══════════════════════

def test_le_chargement_est_confie_au_MAGASIN_et_non_appele_en_ligne():
    """Un appel direct à `on_demand` depuis une route rétablirait exactement le
    défaut que P0.1 a fermé. Le magasin garantit le non-blocage, la coalescence
    des demandes concurrentes et l'état honnête."""
    import inspect
    src = inspect.getsource(C)
    assert '_MAGASIN.servir' in src
    assert 'attendre' in src
    #  L'import de `on_demand` est PARESSEUX, a l'interieur du constructeur :
    #  au niveau du module, il s'executerait a l'import de la route.
    i = src.index('def _charger')
    assert 'from vertex.options import on_demand' in src[i:i + 400]


def test_le_magasin_borne_la_fraicheur_ET_l_age_maximal():
    """Une chaîne d'une heure ne décrit plus le marché : l'afficher comme
    `STALE` serait pire qu'un vide honnête."""
    assert C.FRAICHEUR_S == 300.0
    assert C.PLAFOND_S == 3600.0
    assert C.PLAFOND_S > C.FRAICHEUR_S


def test_deux_demandes_CONCURRENTES_ne_declenchent_pas_deux_collectes():
    """La fiche tire grille, surface et max-pain en même temps : sans
    coalescence, trois collectes identiques partiraient. C'est le `singleflight`
    du magasin — et c'est la raison pour laquelle il fallait passer par lui."""
    import threading
    appels = {'n': 0}
    vrai = C._MAGASIN.servir

    def _compter(clef, constructeur, **kw):
        def _tracee():
            appels['n'] += 1
            time.sleep(0.05)
            return [], {}
        return vrai(clef, _tracee, **kw)

    C._MAGASIN.servir = _compter
    try:
        fils = [threading.Thread(target=C.contrats, args=('CONCUR', BOARD))
                for _ in range(3)]
        for f in fils:
            f.start()
        for f in fils:
            f.join(timeout=3)
        time.sleep(0.3)
        assert appels['n'] <= 1, 'le magasin n a pas coalesce : %d collectes' % appels['n']
    finally:
        C._MAGASIN.servir = vrai


#  ═══════════  4. aucune route ne collecte en synchrone  ══════════════════════

def test_AUCUNE_route_n_appelle_warm_chain_en_synchrone():
    """Le recensement qui empêche le défaut de revenir. `vertex-live` avait
    quatre appels de ce genre ; les reprendre aurait rétabli les 40 secondes."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    coupables = []
    for f in sorted((racine / 'vertex' / 'app' / 'routes').glob('*.py')):
        src = f.read_text(encoding='utf-8', errors='replace')
        for n, ligne in enumerate(src.splitlines(), 1):
            if 'warm_chain(' in ligne and not ligne.strip().startswith('#'):
                coupables.append('%s:%d' % (f.name, n))
    assert coupables == [], (
        'collecte synchrone dans une route (defaut P0.1) : %s' % coupables)


def test_le_recensement_LIT_vraiment_les_routes():
    """Sans ce contrôle, « aucun coupable » voudrait dire « je n'ai rien lu »."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    routes = list((racine / 'vertex' / 'app' / 'routes').glob('*.py'))
    assert len(routes) >= 10, 'arbre de routes suspect : %d' % len(routes)


def test_on_demand_est_bien_PRESENT_et_utilisable():
    """Contre-épreuve : interdire l'appel synchrone ne doit pas revenir à
    supprimer la capacité — c'était tout l'intérêt de `vertex-live`."""
    from vertex.options import on_demand
    for nom in ('fetch', 'warm_chain', 'board_with', 'contract_mark'):
        assert hasattr(on_demand, nom), nom
