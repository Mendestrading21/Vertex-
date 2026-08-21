"""vertex/market/wmb.py — ADAPTER WMB BRIEF VERSIONNÉ (#780).

WMB (*Wall Street Market Brief*) est le contexte macro quotidien de Vertex :
régime, politique monétaire, inflation, géopolitique, secteurs, catalyseurs.

`PRODUCT_CONTRACT.md` lui fixe trois bornes, et la troisième est la raison
d'être de ce module :

1. date, source et provenance **obligatoires** ;
2. il ne fournit **jamais** un prix canonique ;
3. il ne contourne **jamais** un hard gate.

## La décision de conception : rendre l'interdit exécutable

Un commentaire qui dit « WMB ne fournit pas de prix » n'empêche rien. Six mois
plus tard, un champ `spx_close` apparaît dans une charge, quelqu'un le lit « en
attendant », et la règle est morte sans que rien n'ait échoué.

L'ingestion **met donc en quarantaine** tout champ qui ressemble à une donnée de
marché canonique (prix, prime, Greek, IV, strike…). Ces champs ne sont pas
silencieusement jetés — les jeter serait une autre forme de mensonge : ils sont
déplacés dans `quarantaine`, comptés, et le brief porte la trace de ce qui a été
écarté. La règle devient une **propriété du code**, vérifiable par un test, et
la tentative reste visible.

## Statut de vérification — une affirmation sans source reste UNVERIFIED

`PRODUCT_CONTRACT.md` : *« une affirmation non reliée à une source reste
`UNVERIFIED` »*. Ce n'est pas un détail d'affichage : c'est ce qui empêche un
brief bien écrit de peser autant qu'un fait sourcé. Chaque énoncé porte donc son
propre statut, et `confiance` est calculée depuis la proportion de vérifiés —
jamais saisie à la main.

## Hash et historique des corrections

Le hash porte sur le **contenu normalisé**, pas sur la charge brute : deux
ingestions du même brief avec un espace en plus donnent le même hash, et donc
pas de fausse « correction ». Quand le hash change pour une même date, l'entrée
précédente est conservée dans `corrections` — un brief qui se corrige est une
information, pas un accident à effacer.

## Ce que ce module ne fait pas

Il n'appelle aucun réseau et ne décide de rien. Il **normalise et étiquette**.
La récupération du brief (fichier, API, saisie) appartient à son appelant, et la
décision appartient aux moteurs déterministes.
"""
from __future__ import annotations

import hashlib
import json
import re
import datetime as _dt
from typing import Any, Dict, List, Optional

from vertex.market.news_dedup import _key as _cle_dedup

#: Version du schéma. Tout brief ingéré la porte : un packet décisionnel qui
#: cite un brief doit pouvoir dire *quelle forme* de brief il a lu.
SCHEMA_VERSION = 1

#: Vocabulaire de fraîcheur commun au produit (`QUALITY_STANDARD.md` §1).
FRESHNESS = ('LIVE', 'DELAYED', 'STALE', 'DEMO', 'OFFLINE', 'MISSING')

#: Au-delà, le contexte macro du jour n'est plus le contexte du jour.
_FRAIS_HEURES = 24
_RASSIS_HEURES = 72

#: LES CHAMPS QUE WMB N'A PAS LE DROIT DE FOURNIR. La liste vise des NOMS de
#: données de marché canoniques — pas des mots du langage courant : « price »
#: dans une phrase d'analyse est légitime, un CHAMP `price` ne l'est pas.
_CHAMPS_INTERDITS = re.compile(
    r'^(price|last|bid|ask|mid|close|open|high|low|premium|mark|nav|'
    r'delta|gamma|theta|vega|rho|iv|implied_vol\w*|strike|dte|oi|'
    r'open_interest|greeks?)$',
    re.IGNORECASE,
)


def _maintenant() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _iso(d: _dt.datetime) -> str:
    return d.astimezone(_dt.timezone.utc).isoformat(timespec='seconds')


def _horodatage(valeur: Any) -> Optional[_dt.datetime]:
    """Lit un horodatage sans jamais en inventer un.

    Une date absente ou illisible rend `None`, ce qui fera classer le brief en
    `MISSING`. Substituer « maintenant » serait exactement le zéro silencieux
    que `QUALITY_STANDARD.md` interdit."""
    if isinstance(valeur, _dt.datetime):
        return valeur if valeur.tzinfo else valeur.replace(tzinfo=_dt.timezone.utc)
    if isinstance(valeur, str) and valeur.strip():
        brut = valeur.strip().replace('Z', '+00:00')
        try:
            d = _dt.datetime.fromisoformat(brut)
        except ValueError:
            return None
        return d if d.tzinfo else d.replace(tzinfo=_dt.timezone.utc)
    return None


def _fraicheur(publie: Optional[_dt.datetime], maintenant: _dt.datetime,
               demo: bool = False) -> str:
    if demo:
        return 'DEMO'
    if publie is None:
        return 'MISSING'
    heures = (maintenant - publie).total_seconds() / 3600.0
    if heures < 0:
        #  Un brief daté du futur n'est pas « très frais » : il est douteux.
        return 'MISSING'
    if heures <= _FRAIS_HEURES:
        return 'LIVE'
    if heures <= _RASSIS_HEURES:
        return 'DELAYED'
    return 'STALE'


def _quarantaine(obj: Any, chemin: str = '') -> tuple:
    """Sépare le contenu admissible des champs de marché interdits.

    Rend `(propre, ecartes)`. Les écartés sont **conservés** avec leur chemin :
    un champ jeté en silence empêcherait de comprendre pourquoi un brief semble
    incomplet, et masquerait une source qui essaie de fournir des prix."""
    ecartes: List[Dict[str, Any]] = []
    if isinstance(obj, dict):
        propre = {}
        for cle, val in obj.items():
            sous = '%s.%s' % (chemin, cle) if chemin else str(cle)
            if _CHAMPS_INTERDITS.match(str(cle)):
                ecartes.append({'champ': sous, 'raison': 'donnee de marche canonique'})
                continue
            v, e = _quarantaine(val, sous)
            propre[cle] = v
            ecartes.extend(e)
        return propre, ecartes
    if isinstance(obj, list):
        propre_l, i = [], 0
        for v in obj:
            pv, e = _quarantaine(v, '%s[%d]' % (chemin, i))
            propre_l.append(pv)
            ecartes.extend(e)
            i += 1
        return propre_l, ecartes
    return obj, ecartes


def _enonces(brut: Any) -> List[Dict[str, Any]]:
    """Normalise les énoncés et leur attribue leur statut de vérification.

    Un énoncé relié à au moins une source devient `VERIFIED` ; sinon il reste
    `UNVERIFIED`. Aucun autre statut n'est inventé ici."""
    out = []
    for e in (brut or []):
        if isinstance(e, str):
            e = {'texte': e}
        if not isinstance(e, dict):
            continue
        texte = str(e.get('texte') or e.get('text') or '').strip()
        if not texte:
            continue
        sources = [s for s in (e.get('sources') or []) if str(s).strip()]
        out.append({
            'texte': texte,
            'sources': sources,
            'statut': 'VERIFIED' if sources else 'UNVERIFIED',
            'secteurs': list(e.get('secteurs') or e.get('sectors') or []),
            'actifs': list(e.get('actifs') or e.get('assets') or []),
        })
    return out


def _dedupliquer(enonces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Fusionne les énoncés qui racontent la même chose.

    On réutilise la clé de `vertex.market.news_dedup` plutôt que d'écrire une
    seconde déduplication : deux algorithmes de dédup divergent au premier
    ajustement, et le prompt maître demande de chercher les doublons avant
    d'ajouter du code. Le mieux sourcé gagne ; ses sources sont réunies."""
    par_cle: Dict[str, Dict[str, Any]] = {}
    ordre: List[str] = []
    for e in enonces:
        k = _cle_dedup(e['texte']) or e['texte'].lower()
        if k not in par_cle:
            par_cle[k] = dict(e)
            ordre.append(k)
            continue
        garde = par_cle[k]
        fusion = sorted(set(garde['sources']) | set(e['sources']))
        gagnant = e if len(e['sources']) > len(garde['sources']) else garde
        par_cle[k] = {**gagnant, 'sources': fusion,
                      'statut': 'VERIFIED' if fusion else 'UNVERIFIED'}
    return [par_cle[k] for k in ordre]


def _hash(contenu: Dict[str, Any]) -> str:
    """Empreinte du CONTENU NORMALISÉ, pas de la charge brute.

    Deux ingestions du même brief à un espace près doivent donner le même hash,
    sinon chaque relecture serait signalée comme une « correction »."""
    forme = json.dumps(contenu, sort_keys=True, ensure_ascii=False,
                       separators=(',', ':'))
    return hashlib.sha256(forme.encode('utf-8')).hexdigest()[:16]


def ingest(charge: Optional[Dict[str, Any]], *, demo: bool = False,
           precedent: Optional[Dict[str, Any]] = None,
           maintenant: Optional[_dt.datetime] = None) -> Dict[str, Any]:
    """Normalise un brief WMB et rend un objet versionné, daté et traçable.

    `precedent` permet de tenir l'historique des corrections : si le hash change
    pour la même date de publication, l'ancien contenu est conservé.

    `maintenant` est injectable — sans quoi la fraîcheur ne serait pas testable
    de façon déterministe.
    """
    maintenant = maintenant or _maintenant()
    charge = charge if isinstance(charge, dict) else {}

    publie = _horodatage(charge.get('publie') or charge.get('published_at')
                         or charge.get('date'))
    sources = sorted({str(s).strip() for s in (charge.get('sources') or [])
                      if str(s).strip()})

    corps, ecartes = _quarantaine({
        'enonces': charge.get('enonces') or charge.get('statements') or [],
        'evenements': charge.get('evenements') or charge.get('events') or [],
        'secteurs': charge.get('secteurs') or charge.get('sectors') or {},
        'regime': charge.get('regime'),
    })

    enonces = _dedupliquer(_enonces(corps.get('enonces')))
    verifies = sum(1 for e in enonces if e['statut'] == 'VERIFIED')

    contenu = {
        'enonces': enonces,
        'evenements': corps.get('evenements') or [],
        'secteurs': corps.get('secteurs') or {},
        'regime': corps.get('regime'),
    }
    empreinte = _hash(contenu)

    #  CONFIANCE CALCULÉE, JAMAIS SAISIE. Elle ne mesure qu'une chose : la part
    #  d'énoncés reliés à une source. Ce n'est pas une conviction de marché, et
    #  la nommer ainsi éviterait qu'on la lise comme telle.
    confiance = round(verifies / len(enonces), 3) if enonces else 0.0

    corrections = list((precedent or {}).get('corrections') or [])
    if precedent and precedent.get('hash') and precedent['hash'] != empreinte:
        if precedent.get('publie') == (_iso(publie) if publie else None):
            corrections.append({
                'hash': precedent['hash'],
                'remplace_le': _iso(maintenant),
                'enonces': len((precedent.get('contenu') or {}).get('enonces') or []),
            })

    return {
        'schema_version': SCHEMA_VERSION,
        'source_name': 'WMB Brief',
        'publie': _iso(publie) if publie else None,
        'ingere': _iso(maintenant),
        'fraicheur': _fraicheur(publie, maintenant, demo=demo),
        'sources': sources,
        'contenu': contenu,
        'verification': {
            'enonces': len(enonces),
            'verifies': verifies,
            'non_verifies': len(enonces) - verifies,
        },
        'confiance_sourcage': confiance,
        'hash': empreinte,
        'corrections': corrections,
        'quarantaine': ecartes,
        #  RAPPEL EXÉCUTABLE DES BORNES DU MANDAT. Un consommateur peut les
        #  lire ; un test peut les vérifier.
        'mandat': {
            'fournit_prix_canonique': False,
            'peut_contourner_hard_gate': False,
            'role': 'macro_context',
        },
    }


def est_exploitable(brief: Optional[Dict[str, Any]]) -> bool:
    """Un brief est exploitable comme contexte s'il est daté et pas rassis.

    `STALE`, `MISSING` et `OFFLINE` restent AFFICHABLES — l'honnêteté ne diminue
    pas — mais ils ne doivent pas nourrir un contexte présenté comme celui du
    jour."""
    if not isinstance(brief, dict):
        return False
    return brief.get('fraicheur') in ('LIVE', 'DELAYED', 'DEMO')


__all__ = ['SCHEMA_VERSION', 'FRESHNESS', 'ingest', 'est_exploitable']
