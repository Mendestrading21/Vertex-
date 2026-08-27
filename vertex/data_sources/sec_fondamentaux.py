"""vertex/data_sources/sec_fondamentaux.py — SEC EDGAR, ENFIN BRANCHÉ.

## Ce qui manquait

`sec_edgar.py` était **écrit et testé**, et consommé par *aucune* page ni
route. Mesuré le 27 août 2026 : zéro import hors de ses propres bancs. Et
`VERTEX_ENABLE_SEC=1` figurait dans le `.env` de l'utilisateur alors que
**rien ne lisait ce drapeau** — une source déclarée active que personne
n'interroge est pire qu'une source absente : elle donne l'illusion de la
couverture.

Ce module est le pont qui manquait : du **ticker** aux faits XBRL datés.

## Pourquoi cette source compte particulièrement ici

Les fondamentaux Reuters sont **refusés** par le compte IBKR (erreur 10358,
abonnement absent). `yfinance.Ticker.info` en donne, mais **sans date de
publication** — c'est le défaut P0 du domaine fondamental : impossible de dire
ce qui était connaissable à une date donnée.

La SEC publie les deux : la période décrite (`end`) et la date de dépôt
(`filed`). C'est la seule source du produit qui permette un rétrotest
fondamental honnête.

## Ce que ce module ne fait pas

Il n'invente pas de CIK. La correspondance ticker → CIK vient du fichier
officiel de la SEC ; un ticker absent de ce fichier rend une **absence
nommée**, jamais un identifiant deviné. Un mauvais CIK servirait les comptes
d'une autre entreprise sous le nom de la tienne — la pire erreur possible pour
cette source.

Il ne recalcule aucun ratio. Il sert des faits déposés, avec leur date.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.request

from vertex.data_sources import sec_edgar as _sec
from vertex.domain.instruments import Instrument, normaliser_cik

#: Le drapeau que l'utilisateur avait déjà posé et que personne ne lisait.
DRAPEAU = 'VERTEX_ENABLE_SEC'

#: La SEC impose un `User-Agent` nommant un contact réel. `sec_edgar.user_agent`
#: refuse d'appeler sans lui ; on ne contourne pas ce refus.
VAR_CONTACT = 'SEC_USER_AGENT'

#: Fair-access SEC : dix requêtes par seconde maximum. On reste très en
#: dessous — un desk consulte des fiches, il ne moissonne pas l'EDGAR.
MAX_APPELS_MINUTE = 30

#: Un dépôt trimestriel ne bouge pas dans la journée. Six heures suffisent, et
#: le premier appel d'une session sert le cache du précédent.
TTL_S = 6 * 3600.0

#: La table ticker → CIK change de quelques lignes par semaine.
TTL_TABLE_S = 24 * 3600.0

URL_TABLE = 'https://www.sec.gov/files/company_tickers.json'

#: Les faits qu'une fiche affiche. Restreint VOLONTAIREMENT : `companyfacts`
#: rend des milliers de tags, et tout servir noierait la page. Chaque entrée
#: nomme le tag XBRL exact — jamais une approximation.
FAITS = {
    'Revenues': 'Chiffre d affaires',
    'RevenueFromContractWithCustomerExcludingAssessedTax': 'Chiffre d affaires',
    'NetIncomeLoss': 'Resultat net',
    'Assets': 'Total actif',
    'Liabilities': 'Total passif',
    'StockholdersEquity': 'Capitaux propres',
    'EarningsPerShareDiluted': 'BPA dilue',
    'CommonStockSharesOutstanding': 'Actions en circulation',
    'CashAndCashEquivalentsAtCarryingValue': 'Tresorerie',
    'OperatingIncomeLoss': 'Resultat operationnel',
}

_VERROU = threading.Lock()
_APPELS: list = []
_CACHE: dict = {}
_TABLE: dict = {'ts': 0.0, 'par_ticker': {}}


def active() -> bool:
    """La source ne s'active QUE si le drapeau ET le contact sont posés.

    Un drapeau sans contact produirait un refus à chaque appel, et ce refus
    passerait pour une panne de la SEC.
    """
    if os.environ.get(DRAPEAU, '') in ('', '0', 'false', 'no'):
        return False
    return bool((os.environ.get(VAR_CONTACT) or '').strip())


def etat() -> dict:
    """Ce qu'une surface doit pouvoir dire de cette source."""
    return {
        'source': 'SEC_EDGAR',
        'active': active(),
        'drapeau': DRAPEAU,
        'drapeau_pose': os.environ.get(DRAPEAU, '') not in ('', '0', 'false', 'no'),
        'contact_pose': bool((os.environ.get(VAR_CONTACT) or '').strip()),
        'appels_restants_minute': max(0, MAX_APPELS_MINUTE - _appels_recents()),
        'ttl_s': TTL_S,
        'date_de_publication_fournie': True,
        'note': ('la SEC publie la periode decrite ET la date de depot : '
                 'c est la seule source du produit qui permette un retrotest '
                 'fondamental honnete'),
        'read_only': True,
    }


def _appels_recents() -> int:
    limite = time.time() - 60.0
    return sum(1 for t in _APPELS if t > limite)


def _lire(url: str, timeout: float = 20.0):
    entete = {'User-Agent': _sec.user_agent(),
              'Accept-Encoding': 'gzip, deflate'}
    req = urllib.request.Request(url, headers=entete)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        brut = r.read()
        if (r.headers.get('Content-Encoding') or '') == 'gzip':
            import gzip as _gz
            brut = _gz.decompress(brut)
    return json.loads(brut.decode('utf-8', 'replace'))


def cik_de(ticker: str, *, lecteur=None) -> str:
    """Le CIK d'un ticker, d'après le fichier OFFICIEL de la SEC.

    Rend `''` quand le ticker n'y figure pas. **Ne devine jamais** : servir les
    comptes d'une autre entreprise sous le nom de celle-ci serait la pire
    erreur possible de cette source.
    """
    t = str(ticker or '').strip().upper()
    if not t:
        return ''
    with _VERROU:
        frais = (time.time() - _TABLE['ts']) < TTL_TABLE_S and _TABLE['par_ticker']
    if not frais:
        table = (lecteur or _lire)(URL_TABLE)
        par = {}
        for ligne in (table or {}).values():
            if isinstance(ligne, dict) and ligne.get('ticker'):
                par[str(ligne['ticker']).upper()] = normaliser_cik(ligne.get('cik_str'))
        with _VERROU:
            _TABLE['par_ticker'] = par
            _TABLE['ts'] = time.time()
    return _TABLE['par_ticker'].get(t, '')


def fondamentaux(ticker: str, *, lecteur=None, force: bool = False) -> dict:
    """Les faits déposés d'un émetteur, chacun daté de sa publication.

    Rend toujours la même forme : `{'faits': [...], 'etat': …, 'erreur': …}`.
    Une absence reste une absence — jamais un zéro, jamais une valeur d'une
    autre entreprise.
    """
    t = str(ticker or '').strip().upper()
    base = {'symbole': t, 'cik': '', 'faits': [], 'etat': etat(),
            'erreur': None, 'rapport': {}}

    if not t:
        base['erreur'] = 'symbole vide'
        return base
    if not active():
        base['erreur'] = ('source desactivee : %s et %s doivent etre poses'
                          % (DRAPEAU, VAR_CONTACT))
        return base

    with _VERROU:
        entree = _CACHE.get(t)
        if entree and not force and (time.time() - entree['ts']) < TTL_S:
            return {**base, 'cik': entree['cik'], 'faits': list(entree['faits']),
                    'rapport': dict(entree['rapport']), 'depuis_cache': True}
        if _appels_recents() >= MAX_APPELS_MINUTE:
            base['erreur'] = ('cadence SEC atteinte (%d/min) — aucune donnee '
                              'inventee' % MAX_APPELS_MINUTE)
            if entree:
                base.update({'cik': entree['cik'], 'faits': list(entree['faits']),
                             'depuis_cache': True, 'perime': True})
                base['erreur'] += ' ; cache perime servi et signale'
            return base
        _APPELS.append(time.time())

    try:
        cik = cik_de(t, lecteur=lecteur)
    except Exception as e:
        base['erreur'] = 'table ticker->CIK illisible : %s: %s' % (type(e).__name__, e)
        return base
    if not cik:
        base['erreur'] = ('%s absent du fichier officiel de la SEC — aucun CIK '
                          'devine' % t)
        return base
    base['cik'] = cik

    try:
        brut = _sec.charger_companyfacts(cik, lecteur=(
            (lambda url, entete: lecteur(url)) if lecteur else None))
    except _sec.EntitlementManquant as e:
        base['erreur'] = 'contact SEC absent : %s' % e
        return base
    except Exception as e:
        base['erreur'] = '%s: %s' % (type(e).__name__, str(e)[:140])
        return base

    inst = Instrument(cik=cik, ticker=t)
    try:
        obs, rapport = _sec.faits_vers_observations(brut, inst, avec_rapport=True)
    except Exception as e:
        base['erreur'] = 'conversion impossible : %s: %s' % (type(e).__name__, e)
        return base

    #  On ne garde que les faits qu'une fiche affiche, et la version la PLUS
    #  RECEMMENT DEPOSEE de chaque (tag, periode) — les retraitements sont
    #  ordonnes par `revision` dans la conversion.
    retenus = {}
    for o in obs:
        tag = str(o.champ or '').split(':')[-1]
        if tag not in FAITS:
            continue
        clef = (tag, o.observed_at)
        ancien = retenus.get(clef)
        if ancien is None or (o.revision or 0) >= (ancien.revision or 0):
            retenus[clef] = o

    faits = [{
        'tag': str(o.champ or '').split(':')[-1],
        'libelle': FAITS.get(str(o.champ or '').split(':')[-1], ''),
        'valeur': o.valeur,
        'unite': o.unite,
        'devise': o.devise,
        'observed_at': o.observed_at,       # la periode DECRITE
        'available_at': o.available_at,     # la date de DEPOT
        'revision': o.revision,
        'quality': o.quality,
        'provider': o.provider,
    } for o in retenus.values()]
    faits.sort(key=lambda f: (f['tag'], f['observed_at']), reverse=True)

    with _VERROU:
        _CACHE[t] = {'ts': time.time(), 'cik': cik, 'faits': faits,
                     'rapport': rapport}
    return {**base, 'faits': faits, 'rapport': rapport}


def vider_cache():
    with _VERROU:
        _CACHE.clear()
        _TABLE['ts'] = 0.0
        _TABLE['par_ticker'] = {}
        del _APPELS[:]
