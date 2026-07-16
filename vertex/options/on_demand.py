"""vertex/options/on_demand.py — chaîne d'options À LA DEMANDE.

Le board (rotation IBKR + focus) couvre l'univers en quelques heures ; entre-temps,
un titre consulté (/options/<sym>, carte options de la fiche) peut ne pas y être →
toutes ses cartes restaient « Aucune donnée ». Ce module comble le trou : si le
board n'a AUCUN contrat pour le symbole demandé, on va chercher sa chaîne tout de
suite via le même moteur (legacy_engine.best_for_symbol — IBKR si TWS est ouvert,
repli yfinance sinon), avec un cache TTL pour ne pas marteler la source.

Honnêteté des données (règle produit) : si le fetch échoue ou si le titre n'a pas
de spot dans le scan, on renvoie [] — l'UI garde son état vide honnête, jamais un
chiffre inventé. ⛔ LECTURE SEULE.
"""
from __future__ import annotations

import time

from vertex.app.state import scan_state
from vertex.options import legacy_engine

# TTL du cache à la demande : 15 min — assez frais pour l'analyse, assez long pour
# ne pas refaire 3 appels de chaîne à chaque rafraîchissement de page.
TTL_S = 900
# Résultat VIDE (scan pas prêt, chaîne injoignable) : réessai rapide — sinon un
# fetch raté au démarrage laisserait le dossier vide 15 minutes.
EMPTY_TTL_S = 120


def _has_sym(board, sym):
    return any(str(c.get('sym', '')).upper() == sym for c in board)


def fetch(sym):
    """Contrats à la demande pour `sym` (cache TTL). [] honnête si impossible."""
    sym = (sym or '').upper()
    if not sym:
        return []
    cache = scan_state.setdefault('options_ondemand', {})
    ent = cache.get(sym)
    now = time.time()
    if ent and now - (ent.get('ts') or 0) < TTL_S:
        return ent.get('contracts') or []
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    spot = detail.get('price')
    contracts = []
    if isinstance(spot, (int, float)) and spot > 0:
        plan = detail.get('plan') or {}
        tgt = plan.get('tp2') or round(spot * 1.12, 2)
        try:
            contracts = legacy_engine.best_for_symbol(
                sym, spot, tgt, 'call', max_n=4,
                buckets=('court', 'moyen', 'long'),
                earnings_dte=detail.get('earnings_dte'))
        except Exception:
            contracts = []
        # Verdict baissier → aussi des puts (protection / thèse courte).
        if (detail.get('verdict') or '').upper() in ('SELL', 'STRONG_SELL', 'AVOID'):
            stop = plan.get('stop') or round(spot * 0.90, 2)
            try:
                contracts = contracts + legacy_engine.best_for_symbol(
                    sym, spot, stop, 'put', max_n=2,
                    buckets=('moyen', 'long'),
                    earnings_dte=detail.get('earnings_dte'))
            except Exception:
                pass
        # `best_for_symbol` ne pose pas le champ spot ; vol_charts (structure par
        # terme, cône, smile) et les scénarios en dépendent — on l'injecte ici.
        for c in contracts:
            c.setdefault('spot', spot)
    # vide → n'empoisonne le cache que EMPTY_TTL_S (réessai rapide après le scan)
    ts = now if contracts else (now - TTL_S + EMPTY_TTL_S)
    cache[sym] = {'ts': ts, 'contracts': contracts}
    return contracts


def contract_mark(sym, exp_prefix, strike, right):
    """Mid RÉEL d'un contrat PRÉCIS via la chaîne (IBKR si TWS ouvert via le
    monkeypatch de legacy_engine.yf, sinon yfinance). Utilisé pour marquer les
    positions options du desk quand IBKR ne cote pas — le board ne contient que
    les « meilleurs » strikes, pas forcément celui détenu. None honnête si le
    contrat n'est pas coté ; cache TTL partagé (pas de martelage)."""
    sym = (sym or '').upper()
    right = (right or 'C').upper()
    try:
        strike = float(strike)
    except (TypeError, ValueError):
        return None
    key = '%s|%s|%s|%s' % (sym, exp_prefix or '', strike, right[:1])
    cache = scan_state.setdefault('options_mark_cache', {})
    ent = cache.get(key)
    now = time.time()
    if ent and now - (ent.get('ts') or 0) < TTL_S:
        return ent.get('mark')
    mark = None
    try:
        tk = legacy_engine.yf.Ticker(sym)
        exps = list(tk.options or [])
        exp = next((e for e in exps if str(e).startswith(str(exp_prefix or ''))), None)
        if exp:
            ch = tk.option_chain(exp)
            df = ch.puts if right.startswith('P') else ch.calls
            rows = df[abs(df['strike'] - strike) < 0.01]
            if len(rows):
                r0 = rows.iloc[0]
                bid = float(r0['bid'] or 0)
                ask = float(r0['ask'] or 0)
                last = float(r0['lastPrice'] or 0)
                if bid > 0 and ask > 0:
                    mark = round((bid + ask) / 2.0, 2)
                elif last > 0:
                    mark = round(last, 2)
    except Exception:
        mark = None
    cache[key] = {'ts': now, 'mark': mark}
    return mark


def board_with(sym):
    """Board global ∪ contrats à la demande pour `sym` s'il en est absent.

    Ne mute PAS scan_state['options_board'] (la boucle _opt_loop le republie et
    écraserait l'ajout) — la fusion se fait à la lecture, le cache TTL absorbe
    le coût.
    """
    board = scan_state.get('options_board') or []
    sym = (sym or '').upper()
    if not sym or _has_sym(board, sym):
        return board
    extra = fetch(sym)
    return list(board) + extra if extra else board


__all__ = ['fetch', 'board_with', 'contract_mark', 'TTL_S']
