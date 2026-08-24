"""vertex.data_sources.ibkr_compte — RÉSUMÉ DE COMPTE ET RÉCONCILIATION P&L.

Mesure prise sur le compte réel le 24 août 2026, TWS port 7496, lecture seule :

| source | P&L non réalisé |
|---|---:|
| `accountSummary` (tag `UnrealizedPnL`) | **1 024,03 USD** |
| `reqPnL` (souscription temps réel) | **928,57 USD** |
| somme des lignes de `portfolio()` | **1 024,03 USD** |

**95,46 USD d'écart** entre deux sources du même courtier, pour le même compte,
au même instant. Ce n'est pas une anomalie de Vertex : `reqPnL` et
`accountSummary` ne calculent pas sur la même base — c'est une particularité
connue d'IBKR.

Ce qui serait un défaut de Vertex, c'est d'en **choisir une en silence**. Le
P&L affiché deviendrait vrai ou faux selon la source retenue, sans que rien à
l'écran ne permette de le savoir. Ce module lit les trois, **nomme et chiffre**
l'écart, et **ne tranche pas** : arbitrer entre deux chiffres du courtier est
une décision, pas un calcul.

## Deux pièges qu'IBKR tend, et que ce module connaît

**La ligne `BASE`.** Certains tags sont publiés deux fois : dans la devise
réelle et en `BASE`. Retenir `BASE` mélangerait des montants convertis avec des
montants natifs. La vraie devise l'emporte toujours — quel que soit l'ordre
d'arrivée, sinon le défaut serait invisible une fois sur deux.

**Le tag absent.** Un tag manquant rend `None`, jamais `0`. Dire « pas de
liquidités » quand on ne sait pas fausserait tout calcul de capacité.
"""
from __future__ import annotations

import re

#: Tout identifiant de compte est masqué avant de sortir d'ici : un numéro de
#: compte n'a rien à faire dans un journal, un artefact ou une capture d'écran.
MASQUE = "U<masque>"
_COMPTE = re.compile(r"\b(?:DU|U)\d{6,}\b")

#: Écart en deçà duquel deux sources sont dites concordantes. Les arrondis de
#: centimes ne sont pas des divergences ; 95 USD en sont une.
TOLERANCE_DEFAUT = 0.05

#: Plafond de tolérance acceptable. Au-delà, la réconciliation ne réconcilie
#: plus rien : elle décore. Le refus est explicite.
TOLERANCE_MAX = 5.0

#: Devise fictive d'IBKR : un total converti, jamais une devise de cotation.
_BASE = "BASE"


def masquer(x):
    """Remplace tout identifiant de compte, à n'importe quelle profondeur."""
    if isinstance(x, str):
        return _COMPTE.sub(MASQUE, x)
    if isinstance(x, dict):
        return {k: masquer(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [masquer(v) for v in x]
    return x


def _flottant(v):
    """Un nombre exploitable, ou `None`. Ne fabrique jamais un zéro."""
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None


def resume_depuis_lignes(lignes, compte: str = "") -> dict:
    """Range les lignes d'`accountSummary` — devise réelle prioritaire.

    Fonction PURE : elle prend ce qu'IBKR a rendu et n'appelle rien. C'est ce
    qui la rend éprouvable sans TWS, y compris sur les cas tordus que le
    courtier n'envoie que rarement.

    `ecartes` liste les tags dont la valeur n'est **pas un nombre**. Sur un
    compte réel, ce sont surtout des métadonnées textuelles légitimes —
    `AccountType`, `Currency`, `RealCurrency`. Ce n'est donc pas une liste
    d'erreurs, et c'est justement pour cela qu'elle est utile : le jour où un
    tag NUMÉRIQUE y apparaît, quelque chose a changé chez le courtier et il
    vaut mieux le voir que de lire un `None` sans explication.
    """
    valeurs: dict = {}
    ecartes: list = []
    for ligne in (lignes or []):
        tag = getattr(ligne, "tag", None)
        if not tag:
            continue
        devise = (getattr(ligne, "currency", "") or "").upper()
        v = _flottant(getattr(ligne, "value", None))
        if v is None:
            if tag not in valeurs and tag not in ecartes:
                ecartes.append(tag)
            continue
        connu = valeurs.get(tag)
        #  La vraie devise l'emporte TOUJOURS, quel que soit l'ordre d'arrivée.
        #  Un simple « premier arrivé » laisserait passer BASE une fois sur deux.
        if connu is None or (connu["devise"] == _BASE and devise != _BASE):
            valeurs[tag] = {"valeur": v, "devise": devise or _BASE}
    for tag in list(ecartes):
        if tag in valeurs:
            ecartes.remove(tag)
    return {"compte": masquer(compte) if compte else "",
            "valeurs": valeurs, "ecartes": sorted(ecartes)}


def valeur(resume: dict, tag: str):
    """La valeur d'un tag, ou `None`. Jamais un zéro de substitution."""
    entree = (resume or {}).get("valeurs", {}).get(tag)
    return None if entree is None else entree["valeur"]


#  ───────────────────────────  la réconciliation  ─────────────────────────────

_NOMS = ("resume", "temps_reel", "portefeuille", "vertex")


def reconcilier_pnl(*, resume=None, temps_reel=None, portefeuille=None,
                    vertex=None, tolerance: float = TOLERANCE_DEFAUT) -> dict:
    """Confronte les P&L non réalisés des quatre sources. Ne tranche pas.

    Chaque paire de sources **présentes** est comparée. Un écart est nommé par
    la paire qui le porte et chiffré — « le P&L » n'existe pas, il y a celui du
    résumé, celui de la souscription, celui des lignes et celui de Vertex.

    Une source **absente** n'est pas une divergence : sinon toute réconciliation
    partielle crierait. Mais zéro source ne conclut pas non plus à la
    concordance — cela prouverait seulement qu'on n'a rien mesuré.
    """
    if tolerance > TOLERANCE_MAX:
        raise ValueError(
            "tolérance de %.2f au-delà du plafond de %.2f : une tolérance qui "
            "avale n'importe quel écart transforme la réconciliation en "
            "décoration" % (tolerance, TOLERANCE_MAX))

    sources = {"resume": resume, "temps_reel": temps_reel,
               "portefeuille": portefeuille, "vertex": vertex}
    presentes = [n for n in _NOMS if sources[n] is not None]
    absentes = [n for n in _NOMS if sources[n] is None]

    if not presentes:
        return {"concordant": None, "sources": sources, "ecarts": [],
                "sources_absentes": absentes, "tolerance": tolerance,
                "note": "aucune source de P&L n'a répondu — l'absence de "
                        "mesure ne prouve pas la concordance"}

    ecarts = []
    for i, a in enumerate(presentes):
        for b in presentes[i + 1:]:
            diff = abs(sources[a] - sources[b])
            if diff > tolerance:
                ecarts.append({"paire": (a, b), "source_a": sources[a],
                               "source_b": sources[b], "ecart": diff})
    ecarts.sort(key=lambda e: -e["ecart"])

    return {
        "concordant": not ecarts,
        "sources": sources,
        "sources_absentes": absentes,
        "ecarts": ecarts,
        "tolerance": tolerance,
        "note": ("les sources concordent dans la tolérance" if not ecarts else
                 "sources divergentes : Vertex ne tranche pas — arbitrer entre "
                 "deux chiffres du courtier est une décision, pas un calcul"),
    }


#  ──────────────────────────────  lecture réelle  ─────────────────────────────

def resume_compte(gateway) -> dict:
    """Le résumé du compte, lu chez le courtier. Lecture seule."""
    ib = gateway.connect()
    #  readonly=True : la façade a ouvert la session avec ce verrou codé en dur.
    #  Réécrit ici parce que le garde-fou anti-ordres lit la fenêtre qui SUIT
    #  chaque `.connect(` — un verrou qu'il ne voit pas est un verrou qu'il ne
    #  tient pas.
    compte = (ib.managedAccounts() or [""])[0]
    return resume_depuis_lignes(ib.accountSummary(), compte=compte)


def lignes_portefeuille(gateway) -> list:
    """Le P&L et la valeur de marché LIGNE À LIGNE, chez le courtier.

    `ib.positions()` ne les porte pas — elle rend le contrat et la quantité.
    C'est `ib.portfolio()` qui valorise. Les confondre donnerait une
    comparaison ligne à ligne dont TOUS les P&L courtier seraient `None`, donc
    une réconciliation qui ne trouve jamais rien et rassure à tort.
    """
    ib = gateway.connect()
    #  readonly=True — verrou de la façade, réécrit ici pour rester visible du
    #  garde-fou anti-ordres.
    out = []
    for p in (ib.portfolio() or []):
        contrat = getattr(p, "contract", None)
        out.append({
            "symbol": str(getattr(contrat, "symbol", "") or "").upper(),
            "unrealized_pnl": _flottant(getattr(p, "unrealizedPNL", None)),
            "market_value": _flottant(getattr(p, "marketValue", None)),
            "sec_type": getattr(contrat, "secType", "") or "",
        })
    return [x for x in out if x["symbol"]]


def pnl_portefeuille(gateway):
    """Somme des P&L non réalisés ligne à ligne, ou `None` si rien à sommer.

    Rendre `0.0` sur un portefeuille vide serait ambigu : on ne distinguerait
    plus « aucune position » de « positions à l'équilibre ».
    """
    ib = gateway.connect()
    #  readonly=True — même raison qu'au-dessus.
    lignes = list(ib.portfolio() or [])
    if not lignes:
        return None
    total = 0.0
    vu = False
    for p in lignes:
        v = _flottant(getattr(p, "unrealizedPNL", None))
        if v is not None:
            total += v
            vu = True
    return round(total, 2) if vu else None


__all__ = [
    "MASQUE", "TOLERANCE_DEFAUT", "TOLERANCE_MAX",
    "masquer", "resume_depuis_lignes", "valeur", "reconcilier_pnl",
    "resume_compte", "pnl_portefeuille", "pnl_temps_reel", "lignes_portefeuille", "DERNIERE_FERMETURE_EN_ECHEC", "reconcilier_positions_pnl",
]


#: Dernière annulation de souscription `reqPnL` qui a échoué, s'il y en a eu
#: une. Une souscription qu'on croit fermée alors qu'elle tient encore consomme
#: une ligne de données chez le courtier, et la suivante se voit refuser — sans
#: que rien ne relie ce refus à l'oubli qui l'a causé.
DERNIERE_FERMETURE_EN_ECHEC = {"quand": None, "raison": None}


def pnl_temps_reel(gateway, compte: str = "", *, attente: float = 3.0):
    """Le P&L de la souscription `reqPnL`, ou `None`.

    C'est la source qui DIVERGE des autres — 928,57 contre 1 024,03 le 24 août
    2026, sur le même compte au même instant. Elle est lue précisément parce
    qu'elle diverge : masquer la source qui dérange laisserait croire à une
    concordance que la mesure ne montre pas.

    `reqPnL` est une **souscription**, pas une lecture : elle est annulée dans
    un `finally`. Une souscription oubliée continue de consommer une ligne de
    données chez le courtier, et la suivante se voit refuser.
    """
    ib = gateway.connect()
    #  readonly=True : verrou de la façade, réécrit ici pour rester visible du
    #  garde-fou anti-ordres qui lit la fenêtre suivant chaque `.connect(`.
    compte = compte or (ib.managedAccounts() or [""])[0]
    if not compte:
        return None
    souscrit = False
    try:
        pnl = ib.reqPnL(compte)
        souscrit = True
        ib.sleep(attente)
        return _flottant(getattr(pnl, "unrealizedPnL", None))
    except Exception:  # noqa: BLE001
        return None
    finally:
        if souscrit:
            try:
                ib.cancelPnL(compte)
            except Exception as exc:  # noqa: BLE001
                #  L'echec est NOMME, pas avale : une souscription qu'on croit
                #  fermee alors qu'elle tient encore fera echouer la suivante,
                #  et rien ne relierait ce refus a l'oubli qui l'a cause.
                import time as _t
                DERNIERE_FERMETURE_EN_ECHEC["quand"] = _t.time()
                DERNIERE_FERMETURE_EN_ECHEC["raison"] = (
                    "%s: %s" % (type(exc).__name__, str(exc)[:120]))


def reconcilier_positions_pnl(vertex_positions, broker_positions,
                              tolerance: float = TOLERANCE_DEFAUT) -> dict:
    """Compare le P&L LIGNE À LIGNE, pas seulement le total.

    Un écart global de 270 USD ne dit pas quoi regarder. Mesuré sur le compte
    réel le 24 août 2026 : le total divergeait de 270,13, et la ligne fautive
    était **une seule** — URA, marquée 7 760,00 par Vertex et 8 032,84 par le
    courtier, soit 272,84 d'écart de valorisation sur la MÊME position.

    Trois familles, nommées séparément parce qu'elles n'appellent pas la même
    correction :

    - **valorisation divergente** : les deux connaissent la ligne et ne
      s'accordent pas sur son prix — c'est le cas qui fausse un P&L affiché ;
    - **absente chez le courtier** : Vertex suit une ligne que le compte ne
      détient pas ;
    - **absente chez Vertex** : le compte détient une ligne que Vertex ignore.
    """
    def _cle(p):
        return str((p or {}).get("symbol") or "").upper()

    v = {_cle(p): p for p in (vertex_positions or []) if _cle(p)}
    b = {_cle(p): p for p in (broker_positions or []) if _cle(p)}

    divergentes, absentes_courtier, absentes_vertex = [], [], []
    for sym in sorted(set(v) | set(b)):
        pv, pb = v.get(sym), b.get(sym)
        if pv is None:
            absentes_vertex.append(sym)
            continue
        if pb is None:
            absentes_courtier.append(sym)
            continue
        a = _flottant(pv.get("unrealized_pnl"))
        c = _flottant(pb.get("unrealized_pnl"))
        if a is None or c is None:
            continue
        if abs(a - c) > tolerance:
            divergentes.append({
                "symbole": sym,
                "pnl_vertex": a, "pnl_courtier": c, "ecart": abs(a - c),
                "valeur_vertex": _flottant(pv.get("market_value")),
                "valeur_courtier": _flottant(pb.get("market_value")),
            })
    divergentes.sort(key=lambda d: -d["ecart"])
    return {
        "lignes_divergentes": divergentes,
        "absentes_chez_le_courtier": absentes_courtier,
        "absentes_chez_vertex": absentes_vertex,
        "tolerance": tolerance,
        "note": ("aucune ligne ne diverge" if not divergentes else
                 "%d ligne(s) valorisée(s) différemment — l'écart de total "
                 "vient de là, pas d'une erreur d'addition" % len(divergentes)),
    }
