"""
vertex/data_sources/fundamentals.py — Fondamentaux par titre (yfinance tk.info) + médianes par secteur.

Permet de juger la VALORISATION d'un titre vs ses pairs : P/E du titre comparé au
P/E médian de son secteur (cher / dans la moyenne / décoté), marges, croissance, beta.

⚠️ tk.info est LENT et parfois incomplet (champs None) → tourné dans un thread dédié,
rafraîchi toutes les ~6 h. Étiqueter : fondamentaux yfinance, peuvent dater.
"""
import statistics
from concurrent.futures import ThreadPoolExecutor

import yfinance as yf

from vertex.market import sectors
from vertex.data_sources.models import utc_now_iso


def _f(v):
    try:
        return float(v) if v is not None else None
    except Exception:
        return None


def _one(s):
    """Fondamentaux d'UN titre via tk.info, AVEC sa provenance.

    ## Ce que cette source sait, et ce qu'elle ignore

    `yfinance.info` rend des valeurs COURANTES. Il ne dit ni quand la donnée a
    été observée, ni quand elle est devenue publique. Vertex enregistre donc :

    - `recu_a` : l'instant de RECEPTION, mesuré, par titre ;
    - `observe_a` : **inconnu** ;
    - `available_at` : **inconnu**.

    Les deux derniers restent `None` parce qu'on ne les connaît pas. Les
    remplir avec `recu_a` — l'erreur naturelle, et celle que le lot-level
    `as_of` commettait de fait — ferait croire qu'un P/E lu aujourd'hui était
    connaissable aujourd'hui, alors qu'il reflète un dépôt dont la date de
    publication n'est pas dans la charge. `exiger_disponibilite()` refuse donc
    ces valeurs comme preuve historique (`AUDIT-TOTAL-2026-08-25` P0.2).

    ## Un dossier vide n'est pas un dossier absent

    Mesuré le 25 août 2026 : `ZZZZ_INEXISTANT` — 404 chez Yahoo — ressortait
    avec les QUATORZE champs à `null` et **aucun marqueur d'erreur**,
    strictement indiscernable d'un titre réel dont les fondamentaux manquent.
    `QUALITY_STANDARD` §1 exige « erreur ou raison de l'absence » ; `erreur`
    la porte désormais.
    """
    recu_a = utc_now_iso()
    try:
        info = yf.Ticker(s).info or {}
    except Exception as exc:                                  # noqa: BLE001
        return s, {'source': 'yfinance.info', 'recu_a': recu_a,
                   'observe_a': None, 'available_at': None,
                   'erreur': ('%s: %s' % (type(exc).__name__, exc))[:160]}
    sec = sectors.SECTOR_MAP.get(s) or info.get('sector')
    return s, {
        'source': 'yfinance.info',
        'recu_a': recu_a,
        #  Inconnus, et laisses inconnus. Voir le docstring.
        'observe_a': None,
        'available_at': None,
        'pe': _f(info.get('trailingPE')),
        'fwd_pe': _f(info.get('forwardPE')),
        'pb': _f(info.get('priceToBook')),
        'peg': _f(info.get('pegRatio') or info.get('trailingPegRatio')),
        'margin': _f(info.get('profitMargins')),
        'growth': _f(info.get('revenueGrowth')),
        'beta': _f(info.get('beta')),
        'mcap': _f(info.get('marketCap')),
        'div': _f(info.get('dividendYield')),
        'roe': _f(info.get('returnOnEquity')),
        'debt_eq': _f(info.get('debtToEquity')),
        'sector': sec,
        'industry': info.get('industry'),
        'name': info.get('shortName') or info.get('longName'),
        #  Rempli plus bas : un dossier ENTIEREMENT vide vient d'un symbole que
        #  la source ne connait pas, pas d'un titre sans fondamentaux.
        'erreur': None,
    }


def build(symbols):
    """tk.info pour CHAQUE titre (parallélisé) → {by_sym:{sym:{...}}, by_sector:{sec:{median_pe,...}}}.
    Couvre TOUT l'univers passé (plus seulement la watchlist cœur)."""
    by_sym = {}
    try:
        with ThreadPoolExecutor(max_workers=8) as ex:        # 176× tk.info en série = trop lent
            for s, v in ex.map(_one, list(symbols)):
                if v is not None:
                    by_sym[s] = v
    except Exception:
        for s in symbols:                                     # repli séquentiel si l'executor casse
            _s, v = _one(s)
            if v is not None:
                by_sym[_s] = v

    #  Un dossier dont AUCUN champ financier n'est rempli ne vient pas d'un
    #  titre sans fondamentaux : la source ne connait pas le symbole. Mesure du
    #  25 aout 2026 : `ZZZZ_INEXISTANT` ressortait avec quatorze `null` et
    #  aucun marqueur, indiscernable d'un titre reel incomplet.
    _CHAMPS = ('pe', 'fwd_pe', 'pb', 'peg', 'margin', 'growth', 'beta',
               'mcap', 'div', 'roe', 'debt_eq', 'sector', 'industry', 'name')
    for _s, v in by_sym.items():
        if v.get('erreur'):
            continue
        if all(v.get(c) is None for c in _CHAMPS):
            v['erreur'] = 'symbole inconnu de la source (aucun champ rendu)'

    by_sector = {}
    allsecs = set(v.get('sector') for v in by_sym.values() if v.get('sector'))
    for sec in allsecs:
        members = [v for k, v in by_sym.items() if v.get('sector') == sec]
        pes = [v['pe'] for v in members if v.get('pe') and 0 < v['pe'] < 250]
        fwd = [v['fwd_pe'] for v in members if v.get('fwd_pe') and 0 < v['fwd_pe'] < 250]
        mg = [v['margin'] for v in members if v.get('margin') is not None]
        gr = [v['growth'] for v in members if v.get('growth') is not None]
        if pes or fwd:
            by_sector[sec] = {
                'median_pe': round(statistics.median(pes), 1) if pes else None,
                'median_fwd_pe': round(statistics.median(fwd), 1) if fwd else None,
                'median_margin': round(statistics.median(mg) * 100, 1) if mg else None,
                'median_growth': round(statistics.median(gr) * 100, 1) if gr else None,
                'n': len(members),
                #  Une mediane calculee sur trois titres d'un secteur qui en
                #  compte quarante n'est pas la mediane du secteur. Sans ces
                #  comptes, un lot a moitie muet produit un repere qui a l'air
                #  aussi solide qu'un lot complet.
                'n_pe': len(pes),
                'n_ecartes': sum(1 for v in members if v.get('erreur')),
            }
    return {'by_sym': by_sym, 'by_sector': by_sector,
            'provenance': {'source': 'yfinance.info',
                           #  `as_of` est l'instant de RECEPTION du lot, pas la
                           #  date a laquelle l'information est devenue publique.
                           #  Chaque titre porte desormais son propre `recu_a`.
                           'as_of': utc_now_iso(),
                           'observe_a': None, 'available_at': None,
                           'preuve_historique': False,
                           'refresh_policy_hours': 6, 'read_only': True,
                           'note': 'lot fondamental susceptible de champs partiels ; aucune valeur absente n’est imputée'}}


def valuation(pe, sector_median_pe):
    """Étiquette de valorisation d'un P/E vs la médiane de son secteur."""
    if not pe or not sector_median_pe or sector_median_pe <= 0:
        return None
    r = pe / sector_median_pe
    if r >= 1.3:
        return {'label': 'cher (premium)', 'ratio': round(r, 2), 'tone': 'warn'}
    if r <= 0.75:
        return {'label': 'décoté', 'ratio': round(r, 2), 'tone': 'good'}
    return {'label': 'dans la moyenne', 'ratio': round(r, 2), 'tone': 'neutral'}
