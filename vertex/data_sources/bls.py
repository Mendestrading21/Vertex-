"""vertex/data_sources/bls.py — LES SÉRIES OFFICIELLES DE L'EMPLOI ET DES PRIX.

`SOURCES-APIS-OPEN-SOURCE` : « BLS API — v1 sans clé, v2 clé gratuite — CPI,
emploi, salaires et séries officielles — **adopter** ».

## Ce qui a été vérifié le 26 août 2026, en appelant vraiment

```text
POST https://api.bls.gov/publicAPI/v1/timeseries/data/
     {"seriesid": ["CUUR0000SA0"], "startyear": "2025", "endyear": "2026"}

status : REQUEST_SUCCEEDED     observations : 19
{'year': '2026', 'period': 'M07', 'periodName': 'July',
 'value': '333.918', 'latest': 'true'}
```

**Sans clé**, comme annoncé. La v1 est plafonnée à 25 requêtes par jour et par
adresse : c'est peu, et c'est la raison d'être du cache et de la limite de
débit ci-dessous.

## Le piège, visible dans la réponse elle-même

Les seules clés d'une observation sont `footnotes`, `latest`, `period`,
`periodName`, `value`, `year`. **Aucune date de publication.**

Or une série macro en a deux : la période qu'elle **décrit** et l'instant où
elle devient **connaissable**. Le CPI de juillet est publié à la mi-août ;
l'employer en juillet donnerait à un rétrotest une information que le marché
n'avait pas.

`available_at` reste donc **vide** — inconnu, jamais « immédiatement
disponible » — et `exiger_disponibilite` refuse ces valeurs comme preuve
historique. Elles restent parfaitement utilisables pour décrire le présent,
qui est leur usage ici.

La v2, avec clé, expose `calculations` et `catalog` ; **je n'ai pas pu le
vérifier** faute de clé, et je ne l'affirme donc pas.

## Ce module ne collecte jamais dans un chemin de page

Une requête d'utilisateur ne déclenche pas un appel réseau (D-072, P0.1) :
`observations()` est fait pour un job de fond, et le cache sert tout le reste.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request

from .macro_observation import (MacroObservation, fin_de_periode, frequence_de)

BASE_V1 = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'

#: Feature flag. `SOURCES-APIS-OPEN-SOURCE` l'exige **même sans clé** : « les
#: sources officielles activables sans clé doivent quand même avoir un feature
#: flag, une politique de cache, un timeout et une limite de débit ».
DRAPEAU = 'VERTEX_ENABLE_BLS'

#: Plafond documenté de la v1 : 25 requêtes par jour et par adresse. On s'arrête
#: nettement en deçà — dépasser ferait bannir l'adresse, et le repli serait
#: alors une absence totale, pas une dégradation.
MAX_APPELS_JOUR = 20

DELAI_S = 20.0

#: Un lot est réutilisé douze heures : ces séries sont mensuelles, les
#: rafraîchir plus souvent consommerait le quota sans rien apprendre.
TTL_S = 12 * 3600

#: Séries suivies, avec leur unité RÉELLE. Une unité devinée vaut une valeur
#: devinée : `CUUR0000SA0` est un **indice**, pas un pourcentage, et l'afficher
#: avec un `%` inventerait une inflation de 333 %.
SERIES = {
    'CUUR0000SA0': {'libelle': 'CPI-U, tous articles (indice)',
                    'unite': 'indice 1982-84=100'},
    'LNS14000000': {'libelle': 'Taux de chômage U-3', 'unite': '%'},
    'CES0000000001': {'libelle': 'Emplois non agricoles (milliers)',
                      'unite': 'milliers'},
}

_VERROU = threading.Lock()
_CACHE: dict = {}
_APPELS: list = []


def active() -> bool:
    """Le drapeau est-il posé ? Par défaut **non** : une source officielle
    n'entre pas en service par surprise."""
    return str(os.environ.get(DRAPEAU, '')).strip() in ('1', 'true', 'TRUE', 'yes')


def _quota_restant() -> int:
    limite = time.time() - 24 * 3600
    while _APPELS and _APPELS[0] < limite:
        _APPELS.pop(0)
    return max(0, MAX_APPELS_JOUR - len(_APPELS))


def etat() -> dict:
    """Ce que cette source peut faire maintenant, et ce qu'elle ne sait pas.

    Servi aux surfaces : une source désactivée ou à court de quota doit se
    distinguer d'une source qui n'a rien trouvé.
    """
    return {
        'active': active(),
        'drapeau': DRAPEAU,
        'cle_requise': False,
        'appels_restants_24h': _quota_restant(),
        'plafond_24h': MAX_APPELS_JOUR,
        'series_connues': sorted(SERIES),
        'date_de_publication_fournie': False,
        'note': ("l'API v1 ne fournit PAS la date de publication : "
                 "`available_at` reste vide et ces valeurs ne peuvent pas "
                 "fonder une preuve historique"),
        'read_only': True,
    }


def _appeler(series_ids, debut, fin):
    charge = json.dumps({'seriesid': list(series_ids),
                         'startyear': str(debut), 'endyear': str(fin)}).encode()
    req = urllib.request.Request(
        BASE_V1, data=charge,
        headers={'Content-Type': 'application/json',
                 'User-Agent': os.environ.get('SEC_USER_AGENT', 'Vertex/1.0')})
    with urllib.request.urlopen(req, timeout=DELAI_S) as r:
        return json.loads(r.read().decode('utf-8'))


def observations(series_id: str, *, debut=None, fin=None, force=False) -> dict:
    """Les observations d'une série, avec leur provenance.

    Rend toujours `{'observations': [...], 'etat': {...}, 'erreur': str|None}`.
    Une absence reste une absence : jamais de valeur inventée, jamais une
    liste vide présentée comme « aucune donnée » quand c'est le quota ou le
    drapeau qui a parlé.
    """
    sid = str(series_id or '').strip().upper()
    base = {'observations': [], 'etat': etat(), 'erreur': None,
            'manquantes': []}
    if sid not in SERIES:
        base['erreur'] = 'serie inconnue de ce module : %s' % (sid or '(vide)')
        return base
    if not active():
        base['erreur'] = 'source desactivee (%s absent)' % DRAPEAU
        return base

    annee = time.gmtime().tm_year
    debut = int(debut or annee - 1)
    fin = int(fin or annee)
    clef = (sid, debut, fin)

    with _VERROU:
        entree = _CACHE.get(clef)
        if entree and not force and (time.time() - entree['ts']) < TTL_S:
            return {'observations': list(entree['obs']), 'etat': etat(),
                    'erreur': None,
                    'manquantes': list(entree.get('manquantes') or []),
                    'depuis_cache': True}
        if _quota_restant() <= 0:
            base['erreur'] = ('quota v1 epuise (%d appels/24 h) — '
                              'aucune donnee inventee' % MAX_APPELS_JOUR)
            if entree:
                base['observations'] = list(entree['obs'])
                base['depuis_cache'] = True
                base['erreur'] += ' ; cache perime servi et signale'
                base['perime'] = True
            return base
        _APPELS.append(time.time())

    try:
        brut = _appeler([sid], debut, fin)
    except (urllib.error.URLError, OSError, ValueError) as exc:   # noqa: BLE001
        base['erreur'] = '%s: %s' % (type(exc).__name__, exc)
        return base

    if str(brut.get('status')) != 'REQUEST_SUCCEEDED':
        base['erreur'] = 'BLS: %s %s' % (brut.get('status'),
                                         '; '.join(brut.get('message') or []))
        return base

    meta = SERIES[sid]
    out = []
    manquantes = []
    for serie in (brut.get('Results') or {}).get('series') or []:
        for ligne in (serie.get('data') or []):
            valeur = _nombre(ligne.get('value'))
            date_obs = fin_de_periode(ligne.get('year'), ligne.get('period'))
            if valeur is None or not date_obs:
                #  BLS ecrit `-` pour une periode SANS valeur publiee. Mesure du
                #  26 aout 2026 : octobre 2025 du CPI-U est dans ce cas. Un mois
                #  sans donnee n'est pas un mois qu'on n'a pas demande — l'ecarter
                #  en silence ferait croire a une serie continue.
                manquantes.append({
                    'periode': '%s%s' % (ligne.get('year'), ligne.get('period')),
                    'observed_at': date_obs or None,
                    'marqueur_source': ligne.get('value'),
                    'motif': ('valeur non publiee par la source'
                              if valeur is None else 'periode illisible'),
                })
                continue
            out.append(MacroObservation(
                series_id=sid, valeur=valeur, unite=meta['unite'],
                frequence=frequence_de(ligne.get('period')),
                observed_at=date_obs,
                #  INCONNU. L'API v1 ne le donne pas — voir le docstring.
                available_at='',
                provider='BLS_v1',
                provider_record_id='%s:%s%s' % (sid, ligne.get('year'),
                                                ligne.get('period')),
                libelle=meta['libelle'],
                notes=tuple(f.get('text') for f in (ligne.get('footnotes') or [])
                            if isinstance(f, dict) and f.get('text')),
            ))
    out.sort(key=lambda o: o.observed_at, reverse=True)
    with _VERROU:
        _CACHE[clef] = {'ts': time.time(), 'obs': list(out),
                        'manquantes': list(manquantes)}
    return {'observations': out, 'etat': etat(), 'erreur': None,
            'manquantes': manquantes, 'depuis_cache': False}


def _nombre(v):
    try:
        f = float(str(v).replace(',', ''))
    except (TypeError, ValueError):
        return None
    return f if f == f else None            # ecarte les NaN


def vider_cache() -> None:
    """Pour les bancs : sans cela, un test contaminerait le suivant."""
    with _VERROU:
        _CACHE.clear()
        _APPELS.clear()
