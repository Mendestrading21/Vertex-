"""vertex/data_sources/fred.py — LA DATE À LAQUELLE UN CHIFFRE EXISTAIT VRAIMENT.

`SOURCES-APIS-OPEN-SOURCE` : « FRED — clé gratuite — taux, courbe, liquidité,
crédit, macro — **adopter** ». Et : « FRED fournit la profondeur historique et
les **vintages** ».

## Ce qui a été vérifié le 26 août 2026, avec une vraie clé

Emplois non agricoles (`PAYEMS`), mois de **mai 2026**, toutes ses versions
successives :

```text
connue du 2026-06-05 au 2026-07-01 : 159 001
connue du 2026-07-02 au 2026-08-06 : 158 927
connue du 2026-08-07 a aujourd'hui : 158 861
```

**Le même mois, trois chiffres.** Révisé deux fois, de 140 000 emplois au
total. Un rétrotest qui daterait `158 861` à mai emploierait un nombre qui
**n'existait pas avant le 7 août** — le look-ahead à l'état pur, sur la
statistique la plus regardée du calendrier américain.

## Ce que FRED apporte et que BLS v1 n'a pas

Chaque observation porte `realtime_start` et `realtime_end` : l'intervalle
pendant lequel **cette valeur-là** était celle publiée. `realtime_start` est
donc exactement l'`available_at` que D-132 laissait vide faute de source.

Ces observations peuvent, elles, **fonder une preuve historique** — et
`exiger_disponibilite` les accepte, contrairement à celles de BLS v1. C'est la
différence entre une source datée et une source qui décrit seulement le présent.

## Interroger le passé sans le réécrire

`observations(..., as_of='2026-07-05')` rend la série **telle qu'elle était
connue ce jour-là**. C'est le socle d'un rétrotest sans look-ahead : on ne
demande pas « quelle est la valeur de mai », mais « que savait-on de mai le
5 juillet ».

## Ce que ce module ne fait pas

Il n'appelle **jamais** le réseau dans un chemin de page (D-072, P0.1), et il
ne devine aucune unité : chaque série déclare la sienne, vérifiée.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from .macro_observation import MacroObservation

BASE = 'https://api.stlouisfed.org/fred/series/observations'

DRAPEAU = 'VERTEX_ENABLE_FRED'
VAR_CLE = 'FRED_API_KEY'

#: FRED annonce 120 requetes par minute. On reste tres en deca : ces series
#: sont quotidiennes ou mensuelles, et un scan n'a aucune raison de les
#: marteler.
MAX_APPELS_MINUTE = 30

DELAI_S = 20.0
TTL_S = 6 * 3600

#: FRED ecrit `.` pour une periode SANS valeur publiee — un jour ferie sur une
#: serie quotidienne, par exemple. Ce n'est pas zero, et ce n'est pas une
#: erreur : c'est une absence, et elle se nomme.
MARQUEUR_ABSENT = '.'

#: Quand on interroge SANS `as_of`, FRED rend la fenetre temps-reel COURANTE :
#: `realtime_start` vaut alors la date d'interrogation, pas la date de premiere
#: publication. C'est une BORNE SUPERIEURE — elle dit « au plus tard ce
#: jour-la », jamais « exactement ce jour-la ».
#:
#: L'erreur va donc dans le sens SUR : un retrotest qui s'y fie ignore une
#: donnee qu'il aurait pu employer, il n'en emploie jamais une qu'il ne pouvait
#: pas connaitre. Mais la presenter comme exacte serait une fausse precision,
#: et c'est le defaut que ce programme corrige depuis D-084.
#:
#: `vintages()` donne, lui, la VRAIE premiere publication : c'est ce que la
#: requete de vintage demande explicitement.
QUALITE_BORNE = 'BORNE_SUPERIEURE'
NOTE_BORNE = ("`available_at` est la fenetre temps-reel interrogee, donc une "
              "BORNE SUPERIEURE de la date de publication ; `vintages()` donne "
              "la premiere publication exacte")

#: Series suivies, avec leur unite REELLE. Une unite devinee vaut une valeur
#: devinee : `DGS10` est un POURCENTAGE annuel, `PAYEMS` un nombre en MILLIERS.
SERIES = {
    'DGS10': {'libelle': 'Taux Treasury 10 ans', 'unite': '%', 'frequence': 'D'},
    'DGS2': {'libelle': 'Taux Treasury 2 ans', 'unite': '%', 'frequence': 'D'},
    'DGS3MO': {'libelle': 'Taux Treasury 3 mois', 'unite': '%', 'frequence': 'D'},
    'T10Y2Y': {'libelle': 'Pente 10 ans - 2 ans', 'unite': '%', 'frequence': 'D'},
    'PAYEMS': {'libelle': 'Emplois non agricoles', 'unite': 'milliers',
               'frequence': 'M'},
    'UNRATE': {'libelle': 'Taux de chômage', 'unite': '%', 'frequence': 'M'},
    'CPIAUCSL': {'libelle': 'CPI-U désaisonnalisé (indice)',
                 'unite': 'indice 1982-84=100', 'frequence': 'M'},
    'BAMLH0A0HYM2': {'libelle': 'Spread high yield US', 'unite': '%',
                     'frequence': 'D'},
    'DTWEXBGS': {'libelle': 'Dollar pondéré (large)', 'unite': 'indice',
                 'frequence': 'D'},
    'VIXCLS': {'libelle': 'VIX (clôture)', 'unite': 'points', 'frequence': 'D'},
}

_VERROU = threading.Lock()
_CACHE: dict = {}
_APPELS: list = []


def _cle() -> str:
    return str(os.environ.get(VAR_CLE, '')).strip()


def active() -> bool:
    """Drapeau posé **et** clé présente. Le drapeau seul ne suffit pas : une
    source activée sans clé échouerait à chaque appel, et l'échec passerait
    pour une panne de FRED."""
    drapeau = str(os.environ.get(DRAPEAU, '')).strip() in ('1', 'true', 'TRUE', 'yes')
    return drapeau and bool(_cle())


def _quota_restant() -> int:
    limite = time.time() - 60.0
    while _APPELS and _APPELS[0] < limite:
        _APPELS.pop(0)
    return max(0, MAX_APPELS_MINUTE - len(_APPELS))


def etat() -> dict:
    """Ce que cette source peut faire, et pourquoi elle ne peut pas."""
    return {
        'active': active(),
        'drapeau': DRAPEAU,
        'cle_requise': True,
        'cle_presente': bool(_cle()),
        'appels_restants_minute': _quota_restant(),
        'plafond_minute': MAX_APPELS_MINUTE,
        'series_connues': sorted(SERIES),
        'date_de_publication_fournie': True,
        'vintages': True,
        'available_at_par_defaut': QUALITE_BORNE,
        'note': ("`realtime_start` donne la date a laquelle cette valeur-la "
                 "etait publiee : ces observations PEUVENT fonder une preuve "
                 "historique, contrairement a celles de BLS v1 (D-132)"),
        'read_only': True,
    }


def _appeler(params: dict) -> dict:
    p = {'api_key': _cle(), 'file_type': 'json'}
    p.update(params)
    url = BASE + '?' + urllib.parse.urlencode(p)
    req = urllib.request.Request(
        url, headers={'User-Agent': os.environ.get('SEC_USER_AGENT', 'Vertex/1.0')})
    with urllib.request.urlopen(req, timeout=DELAI_S) as r:
        return json.loads(r.read().decode('utf-8'))


def _nombre(v):
    if v is None or str(v).strip() == MARQUEUR_ABSENT:
        return None
    try:
        f = float(str(v).replace(',', ''))
    except (TypeError, ValueError):
        return None
    return f if f == f else None


def observations(series_id: str, *, debut=None, fin=None, as_of=None,
                 limite=None, force=False) -> dict:
    """Les observations d'une série, **datées de leur disponibilité réelle**.

    `as_of` rend la série **telle qu'elle était connue ce jour-là** : on ne
    demande pas « quelle est la valeur de mai », mais « que savait-on de mai le
    5 juillet ». C'est le socle d'un rétrotest sans look-ahead.

    Rend toujours `{'observations', 'manquantes', 'etat', 'erreur'}`.
    """
    sid = str(series_id or '').strip().upper()
    base = {'observations': [], 'manquantes': [], 'etat': etat(), 'erreur': None}
    if sid not in SERIES:
        base['erreur'] = 'serie inconnue de ce module : %s' % (sid or '(vide)')
        return base
    if not active():
        base['erreur'] = ('source desactivee (%s) ' % DRAPEAU if not
                          str(os.environ.get(DRAPEAU, '')).strip()
                          else 'cle %s absente' % VAR_CLE)
        return base

    params = {'series_id': sid, 'sort_order': 'desc'}
    if debut:
        params['observation_start'] = str(debut)
    if fin:
        params['observation_end'] = str(fin)
    if as_of:
        #  La serie TELLE QU'ELLE ETAIT CONNUE ce jour-la.
        params['realtime_start'] = str(as_of)
        params['realtime_end'] = str(as_of)
    if limite:
        params['limit'] = int(limite)
    clef = tuple(sorted(params.items()))

    with _VERROU:
        entree = _CACHE.get(clef)
        if entree and not force and (time.time() - entree['ts']) < TTL_S:
            return {'observations': list(entree['obs']),
                    'manquantes': list(entree['manq']), 'etat': etat(),
                    'erreur': None, 'depuis_cache': True}
        if _quota_restant() <= 0:
            base['erreur'] = ('quota %d appels/minute atteint — aucune donnee '
                              'inventee' % MAX_APPELS_MINUTE)
            return base
        _APPELS.append(time.time())

    try:
        brut = _appeler(params)
    except (urllib.error.URLError, OSError, ValueError) as exc:   # noqa: BLE001
        base['erreur'] = '%s: %s' % (type(exc).__name__, exc)
        return base

    meta = SERIES[sid]
    out, manquantes = [], []
    for o in (brut.get('observations') or []):
        valeur = _nombre(o.get('value'))
        if valeur is None:
            #  `.` = absence PUBLIEE par FRED (jour ferie, serie interrompue).
            #  L'ecarter en silence ferait croire a une serie continue.
            manquantes.append({'observed_at': o.get('date'),
                               'marqueur_source': o.get('value'),
                               'motif': 'valeur non publiee par la source'})
            continue
        out.append(MacroObservation(
            series_id=sid, valeur=valeur, unite=meta['unite'],
            frequence=meta['frequence'],
            observed_at=str(o.get('date') or ''),
            #  LE POINT : la date a laquelle cette valeur-la etait publiee.
            available_at=str(o.get('realtime_start') or ''),
            provider='FRED',
            provider_record_id='%s:%s@%s' % (sid, o.get('date'),
                                             o.get('realtime_start')),
            libelle=meta['libelle'],
            #  BORNE SUPERIEURE, pas la premiere publication — voir plus bas.
            quality=QUALITE_BORNE,
            notes=(NOTE_BORNE,),
        ))
    with _VERROU:
        _CACHE[clef] = {'ts': time.time(), 'obs': list(out),
                        'manq': list(manquantes)}
    return {'observations': out, 'manquantes': manquantes, 'etat': etat(),
            'erreur': None, 'depuis_cache': False}


def vintages(series_id: str, observed_at: str, *, force=False) -> dict:
    """Toutes les versions successives d'UNE observation, de la plus ancienne
    à la plus récente.

    C'est ce qui rend une révision visible. Mesuré le 26 août 2026 sur les
    emplois de mai : `159 001` → `158 927` → `158 861`. Le même mois, trois
    chiffres, et seul le premier existait en juin.

    Chaque version porte `revision` (son rang, 0 pour la première) et
    `precedente` (la valeur qu'elle remplace) — jamais devinée : `None` pour la
    toute première.
    """
    sid = str(series_id or '').strip().upper()
    base = {'versions': [], 'etat': etat(), 'erreur': None}
    if sid not in SERIES:
        base['erreur'] = 'serie inconnue de ce module : %s' % (sid or '(vide)')
        return base
    if not active():
        base['erreur'] = 'source desactivee ou cle absente'
        return base

    params = {'series_id': sid, 'observation_start': str(observed_at),
              'observation_end': str(observed_at),
              #  Tout l'historique de revision que FRED connait.
              'realtime_start': '1776-07-04', 'realtime_end': '9999-12-31',
              'sort_order': 'asc'}
    clef = tuple(sorted(params.items()))
    with _VERROU:
        entree = _CACHE.get(clef)
        if entree and not force and (time.time() - entree['ts']) < TTL_S:
            return {'versions': list(entree['obs']), 'etat': etat(),
                    'erreur': None, 'depuis_cache': True}
        if _quota_restant() <= 0:
            base['erreur'] = 'quota atteint'
            return base
        _APPELS.append(time.time())

    try:
        brut = _appeler(params)
    except (urllib.error.URLError, OSError, ValueError) as exc:   # noqa: BLE001
        base['erreur'] = '%s: %s' % (type(exc).__name__, exc)
        return base

    meta = SERIES[sid]
    versions, precedente = [], None
    for rang, o in enumerate(brut.get('observations') or []):
        valeur = _nombre(o.get('value'))
        if valeur is None:
            continue
        versions.append(MacroObservation(
            series_id=sid, valeur=valeur, unite=meta['unite'],
            frequence=meta['frequence'],
            observed_at=str(o.get('date') or ''),
            available_at=str(o.get('realtime_start') or ''),
            provider='FRED',
            provider_record_id='%s:%s@%s' % (sid, o.get('date'),
                                             o.get('realtime_start')),
            libelle=meta['libelle'],
            revision=len(versions),
            precedente=precedente,
            #  Ici `realtime_start` EST la premiere publication de cette
            #  version-la : c'est ce que la requete de vintage demande.
            quality='MEASURED',
        ))
        precedente = valeur
    with _VERROU:
        _CACHE[clef] = {'ts': time.time(), 'obs': list(versions), 'manq': []}
    return {'versions': versions, 'etat': etat(), 'erreur': None,
            'depuis_cache': False, 'revisions': max(0, len(versions) - 1)}


def vider_cache() -> None:
    """Pour les bancs : sans cela, un test contaminerait le suivant."""
    with _VERROU:
        _CACHE.clear()
        _APPELS.clear()
