"""vertex/options/chaine_a_la_demande.py — LA CAPACITÉ DE `live`, LA GARANTIE DE `main`.

## Deux branches, deux moitiés du même problème

Le board d'options couvre l'univers par rotation IBKR : entre deux passages, un
titre qu'on consulte peut n'y être pour rien, et **toutes ses cartes options
restent vides**. `vertex-live` a écrit `options/on_demand.py` pour combler ce
trou — et c'est la bonne idée.

Mais `live` l'appelle **en synchrone dans quatre routes** (`_od.warm_chain(sym)`
dans `options_intel_api`, `decision_api`, `desk`) : une requête d'utilisateur
déclenche une collecte réseau. C'est exactement le défaut P0.1 que `main` a
fermé — `/api/ticker/<sym>` mesuré à **28–48 secondes**, jusqu'à 136,9 s.

`main`, de son côté, a le magasin d'instantanés (`app/snapshot.py`) : il sert
une valeur datée **immédiatement**, rafraîchit en fond, coalesce les demandes
concurrentes, et distingue `LIVE` / `DELAYED` / `STALE` / `MISSING`. Mais il n'a
jamais eu de quoi combler un titre absent du board.

Ce module marie les deux. La chaîne est chargée **en fond**, la route rend tout
de suite ce qu'elle a, et l'état dit la vérité.

## Pourquoi `attendre=False`

Parce qu'une chaîne d'options se paie en secondes, pas en millisecondes. Bloquer
une page pour l'attendre, c'est le défaut d'origine ; rendre `MISSING` en
disant qu'un chargement est en cours, c'est une absence **nommée**, et
l'utilisateur peut recharger dix secondes plus tard.

## Ce que ce module ne fait pas

Il ne remplace pas le board : quand le board a des contrats pour ce titre, on
les sert directement, sans rien déclencher. La chaîne à la demande ne se réveille
que sur un **trou réel**.
"""
from __future__ import annotations

from vertex.app import snapshot as _instantane

#: Une chaine d'options bouge lentement au regard d'une page consultee : cinq
#: minutes evitent de marteler le courtier sans jamais servir un prix d'hier.
FRAICHEUR_S = 300.0

#: Au-dela, la valeur cesse d'etre servie meme comme `STALE` : une chaine d'une
#: heure ne decrit plus le marche, et l'afficher serait pire qu'un vide.
PLAFOND_S = 3600.0

_MAGASIN = _instantane.Magasin('chaine-options')


def contrats(sym: str, board=None, *, attendre: bool = False):
    """Les contrats connus pour ce titre, et l'état de cette connaissance.

    Rend `(contrats, Meta)`. `contrats` est une liste — vide quand rien n'est
    encore chargé, jamais `None` : un appelant qui itère ne doit pas avoir à
    s'en soucier.

    **La route ne bloque pas.** Si le board couvre déjà le titre, on le sert
    sans rien déclencher. Sinon la chaîne est chargée **en fond** et l'appel
    rend `MISSING` avec `rafraichissement_en_cours` — une absence nommée, pas
    une page figée.
    """
    sym = str(sym or '').upper().strip()
    if not sym:
        return [], _instantane.Meta(etat=_instantane.MISSING,
                                    erreur='symbole vide')

    #  1. Le board d'abord. Un titre deja couvert n'a aucune raison de
    #     declencher une collecte : c'est le cas NOMINAL, et il est gratuit.
    if board:
        #  `isinstance` et pas `c or {}` : une entree qui n'est pas un dict —
        #  un board partiellement corrompu, une liste de chaines — faisait
        #  tomber l'appel. Une route ne doit pas mourir sur une donnee sale.
        deja = [c for c in board
                if isinstance(c, dict)
                and str(c.get('sym') or '').upper() == sym]
        if deja:
            return deja, _instantane.Meta(etat=_instantane.LIVE,
                                          source='options_board')

    #  2. Le trou reel : chargement EN FOND, reponse immediate.
    def _charger():
        from vertex.options import on_demand as _od
        recus = _od.fetch(sym) or []
        return recus, {'source': 'chaine_a_la_demande',
                       'qualite': 'MEASURED' if recus else 'ABSENTE'}

    valeur, meta = _MAGASIN.servir(
        sym, _charger, fraicheur_s=FRAICHEUR_S, plafond_s=PLAFOND_S,
        attendre=attendre)
    return (valeur or []), meta


def etat(sym: str, board=None) -> dict:
    """Ce que la surface doit pouvoir dire de cette chaîne.

    Sans ce bloc, « aucun contrat » se lit comme « ce titre n'a pas d'options »
    alors qu'il peut signifier « la chaîne arrive ».
    """
    liste, meta = contrats(sym, board)
    return {
        'symbole': str(sym or '').upper(),
        'contrats': len(liste),
        'etat': meta.etat,
        'source': meta.source,
        'chargement_en_cours': bool(getattr(meta, 'rafraichissement_en_cours', False)),
        'age_s': meta.age_s,
        'erreur': meta.erreur,
        'note': ("un titre absent du board est charge EN FOND : la page ne "
                 "bloque pas, et « aucun contrat » signifie ici « pas encore », "
                 "pas « ce titre n'a pas d'options »"),
        'read_only': True,
    }
