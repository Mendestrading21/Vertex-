"""
vertex/data/company.py — COUCHE ENTREPRISE (profil « lent », rafraîchi ~1×/semaine).

VERTEX sépare deux natures de données :
  • les VALEURS DE MARCHÉ (cours, technique, Grecs options) — EN DIRECT (IBKR/yfinance) ;
  • le PROFIL D'ENTREPRISE (activité, CEO, employés, segments de revenus, fondamentaux) —
    qui ne bouge pas d'un jour à l'autre → mis en cache sur disque et rafraîchi au plus
    UNE FOIS PAR SEMAINE.

Ce module ne fournit QUE le profil lent. Il se rafraîchit tout seul : si l'entrée en
cache a plus de 7 jours, on retente un fetch yfinance (sur la machine de l'utilisateur) ;
sinon on sert le cache. Sans réseau (cloud/démo), on retombe sur une couche curée pour
les grands noms — jamais de page vide, et l'état « rassis » est signalé à l'UI.

Segments de revenus et année de fondation sont CURÉS (les feeds gratuits ne les donnent
pas de façon fiable). Les concurrents sont dérivés automatiquement des pairs de la même
industrie dans l'univers scanné → couverture de TOUTES les entreprises.
"""

import json
import os
import time

try:
    from vertex.data.universe import _INDUSTRY, _GICS_SECTOR, _GICS, UNIVERSE
except Exception:  # pragma: no cover
    _INDUSTRY, _GICS_SECTOR, _GICS, UNIVERSE = {}, {}, {}, []

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_CACHE = os.path.join(_ROOT, 'company_cache.json')
_WEEK = 7 * 24 * 3600

# ─── Segments de revenus (curés — % approximatifs du CA, ordre décroissant) ───
REVENUE_SEGMENTS = {
    'NVDA': [('Data Center', 78), ('Gaming', 12), ('Prof. Visualization', 3), ('Automobile', 2), ('Autres', 5)],
    'AAPL': [('iPhone', 52), ('Services', 22), ('Mac', 10), ('Wearables', 9), ('iPad', 7)],
    'MSFT': [('Intelligent Cloud', 43), ('Productivity', 32), ('Personal Computing', 25)],
    'GOOGL': [('Search', 57), ('YouTube', 11), ('Google Cloud', 12), ('Réseau', 9), ('Autres', 11)],
    'AMZN': [('Online Stores', 40), ('Third-party', 24), ('AWS', 17), ('Publicité', 9), ('Abonnements', 7), ('Autres', 3)],
    'META': [('Publicité', 96), ('Reality Labs', 2), ('Autres', 2)],
    'TSLA': [('Automobile', 79), ('Énergie & Stockage', 9), ('Services', 8), ('Autres', 4)],
    'AVGO': [('Semi-conducteurs', 58), ('Logiciels d\'infra', 42)],
    'AMD': [('Data Center', 50), ('Client', 30), ('Gaming', 12), ('Embedded', 8)],
    'NFLX': [('Streaming', 99), ('Autres', 1)],
    'CRM': [('Subscription & Support', 94), ('Services pro', 6)],
    'META': [('Publicité', 96), ('Reality Labs', 2), ('Autres', 2)],
    'JPM': [('Consumer Banking', 42), ('Corporate & Invest.', 34), ('Asset Mgmt', 13), ('Commercial', 11)],
    'V': [('Services', 34), ('Data Processing', 33), ('International', 27), ('Autres', 6)],
    'MA': [('Payment Network', 62), ('Value-added Services', 38)],
    'LLY': [('Diabète & Obésité', 55), ('Oncologie', 18), ('Immunologie', 14), ('Neuroscience', 13)],
    'COST': [('Alimentaire', 54), ('Non-alimentaire', 30), ('Services', 12), ('Abonnements', 4)],
    'HD': [('Bricolage / Maison', 100)],
    'UNH': [('UnitedHealthcare', 63), ('Optum', 37)],
    'XOM': [('Upstream', 38), ('Raffinage', 42), ('Chimie', 20)],
    'WMT': [('Walmart US', 68), ('International', 18), ('Sam\'s Club', 14)],
}

# ─── Année de fondation (curée — yfinance ne la donne pas de façon fiable) ───
FOUNDED = {
    'NVDA': 1993, 'AAPL': 1976, 'MSFT': 1975, 'GOOGL': 1998, 'AMZN': 1994, 'META': 2004,
    'TSLA': 2003, 'AVGO': 1991, 'AMD': 1969, 'NFLX': 1997, 'CRM': 1999, 'JPM': 1799,
    'V': 1958, 'MA': 1966, 'LLY': 1876, 'COST': 1983, 'HD': 1978, 'UNH': 1977,
    'XOM': 1870, 'WMT': 1962,
}

# ─── Profil curé (secours hors-ligne / démo — grands noms). Le fetch live yfinance
#     enrichit/rafraîchit ces valeurs sur la machine de l'utilisateur. ───
PROFILE_CURATED = {
    'NVDA': dict(activity='GPU & puces d\'accélération IA', model='Fabless · design de puces',
                 position='Dominante (~90% du marché IA)', ceo='Jensen Huang', employees=29600,
                 country='États-Unis', clients='Hyperscalers, cloud, OEM, gaming', moat='~90% du marché IA'),
    'AAPL': dict(activity='Électronique grand public & services', model='Matériel + écosystème de services',
                 position='Leader premium', ceo='Tim Cook', employees=161000, country='États-Unis',
                 clients='Grand public mondial', moat='Écosystème verrouillé, marque'),
    'MSFT': dict(activity='Logiciels, cloud (Azure) & IA', model='Licences + cloud par abonnement',
                 position='Leader cloud & productivité', ceo='Satya Nadella', employees=228000,
                 country='États-Unis', clients='Entreprises & grand public', moat='Coûts de migration élevés'),
    'GOOGL': dict(activity='Recherche, publicité, cloud, IA', model='Publicité ciblée + cloud',
                  position='Quasi-monopole de la recherche', ceo='Sundar Pichai', employees=182000,
                  country='États-Unis', clients='Annonceurs, entreprises', moat='Données & échelle'),
    'AMZN': dict(activity='E-commerce & cloud (AWS)', model='Marketplace + cloud + pub',
                 position='Leader e-commerce & cloud', ceo='Andy Jassy', employees=1500000,
                 country='États-Unis', clients='Grand public & entreprises', moat='Logistique & AWS'),
    'META': dict(activity='Réseaux sociaux & publicité', model='Publicité ciblée',
                 position='Leader social mondial', ceo='Mark Zuckerberg', employees=67000,
                 country='États-Unis', clients='Annonceurs', moat='Effets de réseau (milliards d\'utilisateurs)'),
    'TSLA': dict(activity='Véhicules électriques & énergie', model='Intégration verticale',
                 position='Leader VE premium', ceo='Elon Musk', employees=125000, country='États-Unis',
                 clients='Grand public', moat='Marque, batteries, logiciel'),
    'AVGO': dict(activity='Semi-conducteurs & logiciels d\'infra', model='Puces + logiciels par acquisitions',
                 position='Leader connectivité', ceo='Hock Tan', employees=37000, country='États-Unis',
                 clients='Data centers, télécoms, OEM', moat='Portefeuille de brevets'),
}

_LABELS = {'États-Unis': '🇺🇸 États-Unis'}


def _load():
    try:
        with open(_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _save(cache):
    try:
        with open(_CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
    except Exception:
        pass


def peers(sym, n=4):
    """Concurrents = pairs de la MÊME INDUSTRIE dans l'univers (sinon même secteur GICS)."""
    ind = _INDUSTRY_OF().get(sym)
    pool = []
    if ind:
        pool = [s for s, i in _INDUSTRY_OF().items() if i == ind and s != sym]
    if len(pool) < 2:
        sec = _GICS_SECTOR.get(sym)
        pool = [s for s in _GICS.get(sec, []) if s != sym]
    return pool[:n]


_IND_CACHE = {}


def _INDUSTRY_OF():
    """ticker → industrie (aplati depuis _INDUSTRY = {industrie: [tickers]})."""
    if not _IND_CACHE:
        for indus, syms in (_INDUSTRY or {}).items():
            for s in syms:
                _IND_CACHE[s] = indus
    return _IND_CACHE


def _fetch_profile(sym):
    """Profil via yfinance .info (lent/flaky — tourne sur la machine de l'utilisateur)."""
    import yfinance as yf
    info = yf.Ticker(sym).info or {}
    officers = info.get('companyOfficers') or []
    ceo = None
    for o in officers:
        t = (o.get('title') or '').lower()
        if 'ceo' in t or 'chief executive' in t:
            ceo = o.get('name')
            break
    if not ceo and officers:
        ceo = officers[0].get('name')
    return {
        'name': info.get('shortName') or info.get('longName'),
        'activity': info.get('industry'),
        'sector': info.get('sector'),
        'ceo': ceo,
        'employees': info.get('fullTimeEmployees'),
        'country': info.get('country'),
        'summary': info.get('longBusinessSummary'),
        'website': info.get('website'),
        # fondamentaux « lents » (cadence hebdo suffit)
        'pe': info.get('trailingPE'), 'forward_pe': info.get('forwardPE'),
        'peg': info.get('pegRatio'), 'margin': info.get('profitMargins'),
        'roe': info.get('returnOnEquity'), 'rev_growth': info.get('revenueGrowth'),
        'eps_growth': info.get('earningsGrowth'), 'fcf': info.get('freeCashflow'),
        'debt_to_ebitda': None, 'cash': info.get('totalCash'), 'debt': info.get('totalDebt'),
        'dividend': info.get('dividendYield'), 'mcap': info.get('marketCap'),
    }


def get(sym, demo=False, allow_fetch=True):
    """Profil d'entreprise (cache hebdo). Retourne un dict enrichi + méta de fraîcheur.

    - `demo=True`  : jamais de réseau, on sert la couche curée (cloud/démo).
    - rafraîchit en tâche de fond si l'entrée a > 7 jours et `allow_fetch`.
    """
    sym = (sym or '').upper()
    cache = _load()
    e = cache.get(sym)
    fresh = bool(e) and (time.time() - (e.get('ts') or 0) < _WEEK)

    if not fresh and allow_fetch and not demo:
        try:
            prof = _fetch_profile(sym)
            if prof.get('name') or prof.get('employees'):
                e = {'ts': time.time(), **{k: v for k, v in prof.items() if v is not None}}
                cache[sym] = e
                _save(cache)
                fresh = True
        except Exception:
            pass

    # secours curé (jamais de vide)
    cur = PROFILE_CURATED.get(sym, {})
    base = dict(cur)
    if e:
        base.update({k: v for k, v in e.items() if v is not None})

    country = base.get('country') or (cur.get('country'))
    out = {
        'symbol': sym,
        'name': base.get('name'),
        'activity': base.get('activity') or cur.get('activity') or _INDUSTRY_OF().get(sym),
        'model': base.get('model') or cur.get('model'),
        'position': base.get('position') or cur.get('position'),
        'ceo': base.get('ceo') or cur.get('ceo'),
        'employees': base.get('employees') or cur.get('employees'),
        'country': _LABELS.get(country, country),
        'clients': cur.get('clients'),
        'moat': cur.get('moat') or base.get('position'),
        'summary': base.get('summary'),
        'sector': base.get('sector') or _GICS_SECTOR.get(sym),
        'industry': _INDUSTRY_OF().get(sym),
        'founded': FOUNDED.get(sym),
        'segments': REVENUE_SEGMENTS.get(sym),
        'peers': peers(sym),
        # fondamentaux lents (None si non fetché — l'UI affiche « — »)
        'fundamentals': {k: base.get(k) for k in
                         ('pe', 'forward_pe', 'peg', 'margin', 'roe', 'rev_growth',
                          'eps_growth', 'fcf', 'cash', 'debt', 'dividend', 'mcap')},
        'stale': not fresh,          # True → couche curée / cache > 7j (UI le signale)
        'updated': (e or {}).get('ts'),
    }
    return out


__all__ = ['get', 'peers', 'REVENUE_SEGMENTS', 'FOUNDED', 'PROFILE_CURATED']
