"""vertex.options.strike_memory — NE PAS REDEMANDER CE QUE LE COURTIER A REFUSÉ.

## Le défaut, mesuré le 25 août 2026 sur le compte réel

`reqSecDefOptParams` rend les strikes **toutes échéances confondues**. Le
produit en fait l'union, puis applique cette même liste à **chaque** échéance —
alors que le pas d'IBKR change avec l'échéance : 1 $ sur les hebdomadaires
proches, 5 $ ou 10 $ sur les lointaines.

Relevé dans le journal du serveur (échantillon de 250 lignes) :

| titre | échéance | refus | strikes refusés |
|---|---|---:|---|
| MRNA | 2026-10-16 | 12 | 136, 137, 138, 139, 141, 142, 143, 144, 146, 147… |
| MRNA | 2026-11-20 | 12 | *les mêmes* |
| MRNA | 2027-03-19 | 12 | *les mêmes* |
| ORCL | 2026-11-20 | 11 | 138, 139, 141…147, 148, 149 |
| NRG  | 2026-12-18 | 11 | 104, 106…109, 111…114, 116 |

Le motif est net : **tout sauf les multiples de 5**. Et les mêmes strikes sont
refusés pour *chaque* échéance du même titre, à chaque cycle de rotation.

**214 refus sur 250 lignes.** La rotation demande 14 strikes par échéance : il
en revient donc trois ou quatre. Environ **quatre cinquièmes du travail demandé
au courtier sont jetés**, indéfiniment, et cette file est la même que celle des
requêtes interactives — d'où les fiches à 30-45 s mesurées le même jour.

## Ce que ce module fait, et ce qu'il ne fait pas

Il **retient ce que le courtier a refusé**, par (titre, échéance), et retire
ces strikes de la demande suivante.

Il n'**invente** jamais un strike : il ne sait que filtrer une liste proposée
ailleurs. Un module qui déduirait « le pas est de 5, donc 155 doit exister »
fabriquerait un contrat que personne n'a listé — exactement ce que le produit
s'interdit.

Il n'aveugle pas non plus le produit : un refus **expire**, parce qu'une
échéance gagne de nouveaux strikes quand le sous-jacent bouge. Et si tout ce
qui est proposé est connu comme refusé, on **redemande quand même** — une
mémoire périmée qui viderait la chaîne en silence serait pire que le
gaspillage qu'elle corrige.
"""
from __future__ import annotations

import threading
import time

#: Durée de vie d'un refus. Une échéance gagne de nouveaux strikes quand le
#: sous-jacent s'éloigne : retenir un refus pour toujours finirait par cacher
#: des contrats réellement listés. Six heures couvrent largement un cycle de
#: rotation sans traverser une séance entière.
DUREE_REFUS_S = 6 * 3600

#: Plafond de mémoire. Sans lui, un produit qui tourne des semaines garderait
#: une entrée par (titre, échéance) visité — la fuite lente que personne ne
#: voit avant qu'elle ne compte.
MAX_ENTREES = 4000

_VERROU = threading.Lock()
_REFUS: dict[tuple[str, str], dict[float, float]] = {}

#: Ce que la memoire a REELLEMENT evite, depuis le demarrage. Un correctif
#: dont on ne peut pas mesurer l'effet est une intention : sans ces compteurs,
#: le seul moyen d'observer le gain serait de comparer deux journaux du
#: courtier a la main.
#:
#: `redemandes_faute_de_mieux` compte les fois ou TOUT etait connu comme
#: refuse et ou l'on a redemande quand meme. Ce n'est pas un echec — c'est la
#: garde anti-aveuglement qui joue — mais un chiffre qui grimpe sans cesse
#: dirait que la memoire ne sert plus a rien, et il vaut mieux le voir.
_COMPTEURS = {'strikes_proposes': 0, 'strikes_evites': 0,
              'redemandes_faute_de_mieux': 0}


def _cle(symbole: str, echeance: str) -> tuple[str, str]:
    """`2027-03-19` et `20270319` désignent la même échéance.

    Les deux orthographes circulent dans le produit ; les traiter comme deux
    clés distinctes ferait retenir un refus qu'on ne relirait jamais — une
    mémoire qui n'oublie pas mais ne se souvient pas non plus.
    """
    return (str(symbole or '').upper(), str(echeance or '').replace('-', ''))


def noter_refus(symbole: str, echeance: str, strikes) -> int:
    """Le courtier n'a pas trouvé ces contrats. Rend le nombre retenu."""
    if not strikes:
        return 0
    cle, maintenant = _cle(symbole, echeance), time.time()
    with _VERROU:
        connus = _REFUS.setdefault(cle, {})
        for k in strikes:
            try:
                connus[float(k)] = maintenant
            except (TypeError, ValueError):
                #  Un strike illisible n'est pas un refus : le noter ferait
                #  entrer une clé qu'aucune demande ne pourra jamais égaler.
                continue
        _elaguer()
        return len(connus)


def noter_acceptes(symbole: str, echeance: str, strikes) -> None:
    """Ces contrats existent : tout refus antérieur les concernant est FAUX.

    Sans cet oubli, une mémoire prise pendant une coupure du courtier — où
    tout échoue — resterait vraie pour six heures et viderait la chaîne.
    """
    if not strikes:
        return
    cle = _cle(symbole, echeance)
    with _VERROU:
        connus = _REFUS.get(cle)
        if not connus:
            return
        for k in strikes:
            try:
                connus.pop(float(k), None)
            except (TypeError, ValueError):
                continue
        if not connus:
            _REFUS.pop(cle, None)


def filtrer(symbole: str, echeance: str, strikes) -> list[float]:
    """Les strikes à demander, refus connus retirés.

    **Ne rend jamais une liste vide alors qu'on lui en a donné une.** Si tout
    est connu comme refusé, on redemande tout : une mémoire périmée qui
    viderait la chaîne en silence serait pire que le gaspillage.
    """
    proposes = []
    for k in (strikes or []):
        try:
            proposes.append(float(k))
        except (TypeError, ValueError):
            continue
    if not proposes:
        return []
    cle, maintenant = _cle(symbole, echeance), time.time()
    with _VERROU:
        connus = _REFUS.get(cle) or {}
        gardes = [k for k in proposes
                  if maintenant - connus.get(k, 0.0) > DUREE_REFUS_S]
        _COMPTEURS['strikes_proposes'] += len(proposes)
        if gardes:
            _COMPTEURS['strikes_evites'] += len(proposes) - len(gardes)
        else:
            #  Tout etait connu refuse : on redemande. Aucun aller-retour
            #  n'est evite ici, et le compter comme tel gonflerait le gain
            #  d'un travail qu'on refait entierement.
            _COMPTEURS['redemandes_faute_de_mieux'] += 1
    return gardes or proposes


def statistiques() -> dict:
    """De quoi mesurer l'effet, plutot que de l'affirmer.

    `part_evitee_pct` vaut `None` tant qu'aucun strike n'a ete propose :
    rendre 0 % ferait passer « je n'ai rien mesure » pour « je n'evite rien ».
    """
    with _VERROU:
        proposes = _COMPTEURS['strikes_proposes']
        evites = _COMPTEURS['strikes_evites']
        return {'couples': len(_REFUS),
                'refus_retenus': sum(len(v) for v in _REFUS.values()),
                'strikes_proposes': proposes,
                'strikes_evites': evites,
                'redemandes_faute_de_mieux':
                    _COMPTEURS['redemandes_faute_de_mieux'],
                'part_evitee_pct': (round(evites / proposes * 100, 1)
                                    if proposes else None)}


def oublier_tout() -> None:
    with _VERROU:
        _REFUS.clear()
        for k in _COMPTEURS:
            _COMPTEURS[k] = 0


def _elaguer() -> None:
    """Appelé sous verrou. Retire les couples les plus anciens au plafond."""
    if len(_REFUS) <= MAX_ENTREES:
        return
    par_age = sorted(_REFUS.items(), key=lambda kv: max(kv[1].values() or [0]))
    for cle, _ in par_age[:len(_REFUS) - MAX_ENTREES]:
        _REFUS.pop(cle, None)
