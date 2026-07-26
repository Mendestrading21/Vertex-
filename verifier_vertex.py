#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERTEX — Vérification de mise en route ("demain, tout marche à 100 %").

Contrôle complet en UNE commande, sans navigateur et sans réseau (in-process) :

    python verifier_vertex.py

Étapes : suite de tests (pytest) → contrôles directs sur l'application Flask
(8 espaces en document complet + fragment, endpoints de session, santé, badges de
fraîcheur, invariant LECTURE SEULE, Service Worker). Verdict final GO / NO-GO.

Mode analyse uniquement : n'exécute jamais d'ordre (READONLY). Rapide, robuste,
portable (aucun port ouvert, aucun processus lancé).
"""
import os
import re
import sys

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

ROOT = os.path.dirname(os.path.abspath(__file__))
OK, KO = ' \033[92m✓\033[0m', ' \033[91m✗\033[0m'
results = []


def check(label, cond, detail=''):
    ok = bool(cond)
    results.append(ok)
    line = (OK if ok else KO) + ' ' + label
    if detail and not ok:
        line += '  — ' + str(detail)
    print(line)
    return ok


def section(t):
    print('\n\033[1m' + t + '\033[0m')


def _read(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


def main():
    print('\n============================================================')
    print(' VERTEX — Vérification de mise en route (analyse, lecture seule)')
    print('============================================================')

    # ── 1. Suite de tests ──
    section('1. Suite de tests (pytest)')
    try:
        import pytest
        rc = pytest.main(['tests/', '-q', '--no-header', '-p', 'no:cacheprovider'])
        check('pytest 100 % vert', rc == 0, 'code=%s' % rc)
    except Exception as e:
        check('pytest exécutable', False, e)

    # ── 2. Application Flask (in-process) ──
    section('2. Application (santé & routes)')
    try:
        import terminal
        terminal.app.config['TESTING'] = True
        cli = terminal.app.test_client()
    except Exception as e:
        check("Chargement de l'application", False, e)
        return _verdict()
    check("Chargement de l'application", True)
    check('/healthz → 200', cli.get('/healthz').status_code == 200)
    try:
        check('/readyz : LECTURE SEULE', cli.get('/readyz').get_json().get('readonly') is True)
    except Exception as e:
        check('/readyz : LECTURE SEULE', False, e)

    # ── 3. Les 8 espaces (document complet) ──
    section('3. Les 8 espaces (document complet)')
    spaces = {'/': 'briefing', '/markets': 'markets', '/opportunities': 'opportunities',
              '/analysis': 'analysis', '/portfolio': 'portfolio', '/options': 'options',
              '/journal': 'journal', '/system': 'system'}
    for url, active in spaces.items():
        try:
            html = cli.get(url).get_data(as_text=True)
            good = html.lstrip().lower().startswith('<!doctype') and ('data-space="%s"' % active) in html
        except Exception as e:
            good = False
        check('%-14s → 200 + contenu' % url, good)

    # ── 4. Navigation continue (fragment = shell persistant) ──
    section('4. Shell persistant (rendu de fragment)')
    ok_frag = True
    for url, active in spaces.items():
        try:
            frag = cli.get(url, headers={'X-Vertex-Fragment': '1'}).get_data(as_text=True)
            if '<!doctype' in frag.lower() or 'class="vx-fragment"' not in frag or ('data-active="%s"' % active) not in frag:
                ok_frag = False
        except Exception:
            ok_frag = False
    check('Fragment servi pour les 8 espaces (sans reconstruire le shell)', ok_frag)

    # ── 5. Session d'analyse ──
    section("5. Session d'analyse")
    try:
        dg = cli.get('/api/session/digest').get_json()
        check('Digest (state=%s)' % dg.get('state'), 'state' in dg)
    except Exception as e:
        check('Digest de session', False, e)
    try:
        mf = cli.get('/api/session/manifest').get_json()
        check('Manifest (session_id=%s, qualité=%s%%)' % (mf.get('session_id'), mf.get('quality_pct')),
              all(k in mf for k in ('session_id', 'status', 'quality_pct')))
    except Exception as e:
        check('Manifest de session', False, e)

    # ── 6. Mécaniques de continuité livrées ──
    section('6. Mécaniques de continuité (assets)')
    core = _read('vertex', 'static', 'vertex', 'js', 'vx-core.js')
    check('Core : store/SWR/cache/fraîcheur/prix',
          all(f in core for f in ('VX.store', 'VX.swr', 'VX.fetch.peek', 'VX.freshness', 'VX.prices')))
    router = _read('vertex', 'static', 'vertex', 'js', 'vx-router.js')
    check('Routeur : SPA + préchargement + repli dur',
          all(f in router for f in ('X-Vertex-Fragment', 'pushState', 'function prefetch', 'hard(href)')))
    shell = _read('vertex', 'static', 'vertex', 'js', 'vx-shell.js')
    check('Shell : offline + surveillance de session',
          all(f in shell for f in ('setNet', 'watchSession', 'Hors ligne', 'Reconnecté')))
    pages = os.path.join('vertex', 'ui', 'pages')
    check('Badges de fraîcheur (Analyse/Marchés/Portefeuille/Opportunités)',
          'an-fresh' in _read(pages, 'analysis_page.py') and 'vx-mk-fresh' in _read(pages, 'markets_page.py')
          and 'pf-fresh' in _read(pages, 'portfolio_page.py') and 'op-fresh' in _read(pages, 'opportunities_page.py'))
    check('Prix central alimenté (Analyse)', 'VX.prices.setLive' in _read(pages, 'analysis_page.py'))

    # ── 7. Invariant LECTURE SEULE ──
    section('7. Invariant LECTURE SEULE (aucun ordre)')
    try:
        from vertex.app.config import READONLY
        check('READONLY = True', READONLY is True)
    except Exception as e:
        check('READONLY', False, e)
    rules = ' '.join(str(r) for r in terminal.app.url_map.iter_rules()).lower()
    check('Aucune route de passage d\'ordre',
          not any(w in rules for w in ('place_order', 'placeorder', 'submitorder', 'transmit_order')))

    # ── 8. Service Worker ──
    section('8. Service Worker (version)')
    try:
        sw = cli.get('/sw.js').get_data(as_text=True)
        m = re.search(r'td-shell-v(\d+)', sw)
        check('Version SW ≥ v70 (CONTINUITY) : v%s' % (m.group(1) if m else '?'),
              bool(m) and int(m.group(1)) >= 70)
    except Exception as e:
        check('Service Worker', False, e)

    return _verdict()


def _verdict():
    total, passed = len(results), sum(results)
    print('\n============================================================')
    if passed == total and total > 0:
        print(' \033[92mVERDICT : GO — %d/%d contrôles OK. Vertex est prêt à 100 %%.\033[0m' % (passed, total))
        print(' Lancement : python terminal.py  →  http://localhost:5002')
        print('============================================================\n')
        return 0
    print(' \033[91mVERDICT : NO-GO — %d/%d OK (%d échec[s]).\033[0m' % (passed, total, total - passed))
    print(' Corrige les lignes ✗ ci-dessus avant de lancer.')
    print('============================================================\n')
    return 1


if __name__ == '__main__':
    sys.exit(main())
