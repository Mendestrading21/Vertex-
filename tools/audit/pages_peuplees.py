"""Charge chaque page AVEC DES DONNÉES et relève ce qui casse.

## Pourquoi cet outil existe

En mode démo, Vertex sert des collections vides : zéro ligne de scan, zéro
position, zéro clôture. Des pans entiers de code ne s'exécutent donc **jamais**.
Une page peut afficher zéro erreur console, zéro bloc vide et passer toute la
suite, tout en étant **inutilisable dès qu'une donnée arrive**.

Mesuré : `opportunities_page.py` appelait six fonctions introuvables dans tout
le dépôt. Avec un scan réel, la vue Radar tombait dès la première carte. Rien ne
le montrait.

## Ce que l'outil fait

Il injecte un scan et un desk fictifs — assez riches pour réveiller les chemins
endormis — puis charge chaque page et compte les erreurs. Les données sont
CLAIREMENT synthétiques : l'outil sert à faire tomber du code, pas à produire
une capture de démonstration.
"""
from __future__ import annotations

import argparse
import json
import sys

SYMBOLES = ('SPY', 'QQQ', 'XLK', 'MSFT', 'AAPL', 'XOM', 'NVDA', 'ZZZZ')

SCAN = {
    'rows': [{
        'symbol': s, 'score': 60 + i * 3, 'change': (i - 3) * 0.8, 'price': 100 + i * 7,
        'sector': 'Big Tech' if i % 2 else 'Energie', 'verdict': 'ATTENDRE' if i % 2 else 'BUY',
        'decision': 'ATTENDRE' if i % 2 else 'ACHETER', 'grade': 'B', 'rs': 70, 'rsi': 50,
        'pos52': 60, 'regime': 'TREND', 'rr': 2.1, 'vx_pwin': 0.55, 'vx_ev': 1.2,
        'anomaly_score': 30 + i * 5, 'anomaly_lvl': 'ACTIF', 'anomalies': ['gap'],
        'st_conf': 60, 'vx_edge': 61, 'ext_atr': 0.5,
        'playbook': {'ic': '🎯', 'name': 'Repli sur tendance', 'col': '#38BDF8',
                     'desc': 'Entrer sur un creux dans une tendance saine.'},
    } for i, s in enumerate(SYMBOLES)],
    'detail': {s: {'price': 100 + i * 7,
                   'series': {'close': [90 + j for j in range(40)]},
                   'mtf': {'state': 'HAUSSIER'}}
               for i, s in enumerate(SYMBOLES)},
    'indices': [{'name': 'S&P 500', 'change': 0.4, 'spark': [1, 2, 3, 4, 5]},
                {'name': 'VIX', 'change': -1.1, 'spark': [5, 4, 3, 2, 1]}],
    'sectors': [{'sector': 'Big Tech', 'avg_score': 71, 'avg_change': 0.9, 'n': 4,
                 'avg_rvol': 1.2},
                {'sector': 'Energie', 'avg_score': 58, 'avg_change': -0.4, 'n': 4,
                 'avg_rvol': 0.9}],
    'internals': {'health': 62, 'pct_a50': 58, 'pct_a200': 51,
                  'history': [{'d': '2026-08-%02d' % d, 'a50': 50 + d, 'a200': 45 + d,
                               'health': 55 + d} for d in range(20, 28)]},
    'market_ctx': {'roro': 'RISK-ON', 'vix': 16.2, 'breadth': {'above50': 58},
                   'spy_regime': 'TREND', 'best_sector': {'sector': 'Big Tech'}},
    'committee': {'decisions': [{'symbol': 'MSFT', 'verdict': 'ACHETER'}],
                  'counts': {'ACHETER': 1, 'ATTENDRE': 6, 'ÉVITER': 1}},
    'updated': '2026-08-27T19:00:00Z', 'scan_ts': '2026-08-27T19:00:00Z',
    'scan_age': 420, 'data_source': 'demo', 'source': 'scan',
}

TRADES = [
    {'id': 1, 'sym': 'MSFT', 'type': 'STK', 'qty': 40, 'cost': 14800, 'added': '2026-05-12',
     'entrySnap': {'stop': 330.0, 'tgt': 440.0, 'thesis': 'Thèse déclarée.'}},
    {'id': 2, 'sym': 'AAPL', 'type': 'STK', 'qty': 60, 'cost': 12900, 'added': '2026-03-04',
     'entrySnap': {'stop': 185.0, 'tgt': 255.0}},
    {'id': 5, 'sym': 'NVDA', 'type': 'CALL', 'right': 'C', 'qty': 2, 'cost': 2400,
     'strike': 150, 'exp': '2027-01-15', 'added': '2026-07-02', 'entrySnap': {'stop': 6.0}},
]
JOURNAL = [{'id': i, 'date': d, 'ticker': s, 'result': r, 'pnl': p, 'reason': 'raison',
            'lesson': 'leçon', 'stop': 10, 'exit': 11}
           for i, (d, s, r, p) in enumerate(
               [('2026-02-10', 'MSFT', 'WIN', 820), ('2026-03-19', 'TSLA', 'LOSS', -540),
                ('2026-05-08', 'GOOG', 'WIN', 910), ('2026-06-30', 'BA', 'LOSS', -390),
                ('2026-07-15', 'META', 'WIN', 1180), ('2026-08-05', 'CRM', 'WIN', 350)], 1)]
CLOTURES = [{'id': i, 'sym': e['ticker'], 'type': 'STK', 'qty': 10, 'cost': 5000,
             'exit': 5000 + e['pnl'], 'closed': e['date'], 'added': e['date'],
             'pnl_pct': round(e['pnl'] / 50.0, 1)} for i, e in enumerate(JOURNAL, 1)]

ROUTES = [
    '/', '/calendar', '/calendar?view=options', '/markets', '/markets?view=indices',
    '/markets?view=sectors', '/markets?view=breadth', '/markets?view=volatility',
    '/opportunities', '/opportunities?view=stocks', '/opportunities?view=etf',
    '/opportunities?view=options', '/opportunities?view=anomalies',
    '/opportunities?view=calendar', '/opportunities?view=portfolio',
    '/analysis', '/options', '/options?view=positions', '/simulator',
    '/portfolio', '/portfolio?view=positions', '/portfolio?view=allocation',
    '/portfolio?view=risk', '/portfolio?view=theses', '/portfolio?view=options',
    '/follow-up', '/performance', '/performance?view=journal',
    '/performance?view=progression', '/performance?view=track-record',
    '/intelligence', '/system', '/system?view=alerts', '/system?view=security',
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=3000)
    ap.add_argument('--routes', nargs='*')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    routes = args.routes or ROUTES
    total = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 1000})
        ctx.add_init_script(
            "localStorage.setItem('myTrades', %s);"
            "localStorage.setItem('vxJournal', %s);"
            "localStorage.setItem('myTradesClosed', %s);"
            "localStorage.setItem('myCapital','50000');"
            % (json.dumps(json.dumps(TRADES)), json.dumps(json.dumps(JOURNAL)),
               json.dumps(json.dumps(CLOTURES))))
        ctx.route('**/scan**', lambda r: r.fulfill(
            status=200, content_type='application/json', body=json.dumps(SCAN)))
        page = ctx.new_page()
        for route in routes:
            fautes: list[str] = []
            page.on('pageerror', lambda e: fautes.append('levée : %s' % e))
            page.on('console', lambda m: fautes.append('console : %s' % m.text)
                    if m.type == 'error' else None)
            try:
                page.goto(args.base + route, wait_until='domcontentloaded')
                page.wait_for_timeout(args.wait)
                casse = page.evaluate(
                    "() => { const e = document.querySelector('.vx-error-banner,"
                    "[data-kind=\"error\"]'); return e ? e.innerText.replace(/\\s+/g,' ')"
                    ".slice(0,110) : ''; }")
            except Exception as exc:  # noqa: BLE001
                casse = 'navigation impossible : %s' % exc
            page.remove_listener('pageerror', lambda e: None) if False else None
            n = len(fautes) + (1 if casse else 0)
            total += n
            etat = 'OK' if not n else '%d faute(s)' % n
            print('%-40s %s' % (route, etat))
            for f in fautes[:3]:
                print('     %s' % f[:160])
            if casse:
                print('     bandeau : %s' % casse)
            page.remove_listener  # no-op lisible
            page = ctx.new_page() if fautes else page
        nav.close()
    print('\nTOTAL : %d faute(s) sur %d route(s) PEUPLÉE(S)' % (total, len(routes)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
