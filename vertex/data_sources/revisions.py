"""vertex/data_sources/revisions.py — CE QUI A CHANGÉ ENTRE DEUX OBSERVATIONS.

`VERTEX-INTELLIGENCE-2.0` Phase 4, dernier critère d'acceptation :

> historique des révisions

## Le défaut, mesuré le 26 août 2026

`analyst_deep.get()` écrit `cache[sym] = pack` : chaque rafraîchissement — TTL
12 heures — **écrase** l'instantané précédent. Quand un consensus BPA, une
tendance de révision ou une croissance attendue change entre deux passages,
Vertex n'en garde **aucune trace**.

Le seul « historique » disponible venait de Yahoo lui-même : `surprises.history`
(les surprises de résultats passées) et `eps_trend.d90` (un unique point à
90 jours). Ce sont les observations de Yahoo, pas celles de Vertex.

Or pour une thèse, **le changement est souvent l'information** : un consensus
qui glisse de 5,32 à 5,31 ne dit rien ; trois révisions à la baisse en trente
jours disent quelque chose. Sans mémoire, la seconde lecture est impossible.

## Ce qu'on sait, et ce qu'on ne sait pas

On sait **quand Vertex a vu** le changement. On ne sait pas **quand il a eu
lieu** : entre deux passages espacés de douze heures, la révision a pu tomber
à n'importe quel moment. C'est la distinction de D-076, et elle est portée par
le nom du champ — `vu_a`, jamais `date_revision`.

Renseigner une date de révision qu'on ignore ferait passer une observation pour
un fait daté, et rendrait ces entrées utilisables comme preuve historique — ce
qu'elles ne sont pas.

## Ce que ce module ne fait pas

Il ne détecte pas les révisions **entre** deux passages : deux mouvements qui
s'annulent dans l'intervalle sont invisibles, et le disent. Une couverture
réelle exigerait un flux d'événements, pas une comparaison d'instantanés.
"""
from __future__ import annotations

#: Les champs SCALAIRES dont un changement est decisionnel. Le chemin est
#: pointe : `eps_trend.current` designe `pack['eps_trend']['current']`.
#:
#: On ne suit PAS les blocs entiers : `surprises.history` change de forme a
#: chaque publication de resultats sans qu'une revision ait eu lieu, et
#: l'historique se remplirait de bruit — un journal illisible est un journal
#: qu'on cesse de lire.
CHAMPS_SUIVIS = (
    'eps_trend.current',
    'eps_trend.revision_pct_90d',
    'eps_revisions.net30',
    'eps_revisions.trend',
    'growth_fwd',
)

#: Bornage. Un cache de revisions qui grossit sans fin finit par etre supprime
#: en entier, et l'historique avec.
MAX_PAR_TITRE = 20

#: En deca, un ecart est du bruit d'arrondi de la source, pas une revision.
SEUIL_RELATIF = 0.001


def _lire(pack, chemin: str):
    """La valeur au bout d'un chemin pointé, ou `None`."""
    cur = pack
    for cle in chemin.split('.'):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(cle)
    return cur


def _a_change(avant, apres) -> bool:
    """Le changement est-il réel, ou du bruit d'arrondi ?"""
    if avant is None or apres is None:
        return avant is not apres
    if isinstance(avant, bool) or isinstance(apres, bool):
        return avant != apres
    if isinstance(avant, (int, float)) and isinstance(apres, (int, float)):
        if avant == apres:
            return False
        base = max(abs(avant), abs(apres), 1e-9)
        return abs(apres - avant) / base > SEUIL_RELATIF
    return avant != apres


def diff(avant, apres, vu_a) -> list:
    """Les changements observés entre deux instantanés du même titre.

    Chaque entrée porte `champ`, `avant`, `apres` et `vu_a` — l'instant où
    **Vertex a vu** le changement, jamais celui où il a eu lieu.
    """
    if not isinstance(avant, dict) or not isinstance(apres, dict):
        return []
    #  Un instantane VIDE est un PREMIER PASSAGE, pas un etat ou tout valait
    #  `None`. Le traiter comme un etat ferait apparaitre cinq « revisions » a
    #  la premiere observation — ou juste apres un echec total de la source,
    #  qui rend precisement un dossier vide. On ne fabrique pas un mouvement a
    #  partir d'une absence de reference.
    if not avant:
        return []
    out = []
    for chemin in CHAMPS_SUIVIS:
        a, b = _lire(avant, chemin), _lire(apres, chemin)
        if _a_change(a, b):
            out.append({'champ': chemin, 'avant': a, 'apres': b, 'vu_a': vu_a})
    return out


def accumuler(historique, nouveaux, maximum: int = MAX_PAR_TITRE) -> list:
    """L'historique borné, du plus récent au plus ancien.

    Les nouveaux passent devant : un lecteur qui tronque lit ce qui vient
    d'arriver, pas ce qui a été oublié.
    """
    ancien = list(historique or [])
    return (list(nouveaux or []) + ancien)[:max(0, int(maximum))]


def couverture(historique) -> dict:
    """Ce que cet historique couvre, et ce qu'il ne peut pas voir.

    Sans ce bloc, une liste vide se lit « aucune révision » alors qu'elle peut
    signifier « premier passage » ou « rien qui dépasse le seuil de bruit ».
    """
    h = list(historique or [])
    return {
        'entrees': len(h),
        'plafond': MAX_PAR_TITRE,
        'sature': len(h) >= MAX_PAR_TITRE,
        'champs_suivis': list(CHAMPS_SUIVIS),
        'vu_a_le_plus_ancien': (h[-1].get('vu_a') if h else None),
        'vu_a_le_plus_recent': (h[0].get('vu_a') if h else None),
        'date_de_revision': None,
        'note': ("`vu_a` est l'instant ou Vertex a OBSERVE le changement, pas "
                 "celui ou la revision a eu lieu : entre deux passages, elle a "
                 "pu tomber a n'importe quel moment. Deux mouvements qui "
                 "s'annulent dans l'intervalle sont invisibles."),
        'read_only': True,
    }
