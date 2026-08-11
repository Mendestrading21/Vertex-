"""vertex/engines/postmortem.py — POST-MORTEM DU JOURNAL (discipline & biais).

Analyse les trades CLÔTURÉS déclarés dans le desk (myTradesClosed) + les entrées
de journal (vxJournal) pour répondre : « qu'est-ce que mes sorties disent de ma
discipline ? ». Statistiques réelles (win rate, profit factor, espérance, meilleurs/
pires), instruments (actions vs options), récidives par titre, et DRAPEAUX
comportementaux dérivés des chiffres — jamais des jugements inventés.

Invariants : fonction PURE (aucune I/O) ; lecture seule, aucun ordre ; donnée absente
→ None / listes vides honnêtes ; aucun trade ignoré silencieusement sans raison.
"""
from __future__ import annotations


def _num(x):
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v or v in (float('inf'), float('-inf')):
        return None
    return v


def _days_between(a, b):
    """Jours entre deux dates ISO (YYYY-MM-DD...). None si non parsables."""
    try:
        from datetime import date
        pa = date.fromisoformat(str(a)[:10])
        pb = date.fromisoformat(str(b)[:10])
        return abs((pb - pa).days)
    except (TypeError, ValueError):
        return None


def build(closed, journal=None):
    """Post-mortem depuis les trades clôturés (+ champs comportementaux du journal)."""
    rows = []
    for t in (closed or []):
        if not isinstance(t, dict):
            continue
        cost, exit_ = _num(t.get('cost')), _num(t.get('exit'))
        if cost is None or exit_ is None or cost <= 0:
            continue                          # sans coût/sortie réels → inexploitable
        pnl = exit_ - cost
        rows.append({
            'sym': str(t.get('sym') or '?').upper(),
            'type': str(t.get('type') or 'STK').upper(),
            'pnl': round(pnl, 2),
            'pnl_pct': round(100 * pnl / cost, 1),
            'hold_days': _days_between(t.get('added'), t.get('closed')),
            'note': (t.get('note') or '')[:120],
        })

    if not rows:
        return {
            'empty': True, 'trades_n': 0, 'wins': 0, 'losses': 0, 'win_rate': None,
            'total_pnl': None, 'avg_win': None, 'avg_loss': None, 'profit_factor': None,
            'expectancy': None, 'best': None, 'worst': None, 'by_type': {},
            'repeat_losers': [], 'hold_days_avg': None, 'flags': [],
            'mistakes': [], 'narrative': None, 'generator': 'deterministic',
            'reason': 'aucun trade clôturé exploitable (coût + sortie réels requis)',
        }

    wins = [r for r in rows if r['pnl'] > 0]
    losses = [r for r in rows if r['pnl'] <= 0]
    tot = sum(r['pnl'] for r in rows)
    gw = sum(r['pnl'] for r in wins)
    gl = abs(sum(r['pnl'] for r in losses))
    avg_win = round(gw / len(wins), 2) if wins else None
    avg_loss = round(-gl / len(losses), 2) if losses else None
    win_rate = round(100 * len(wins) / len(rows))
    pf = round(gw / gl, 2) if gl > 0 else None            # profit factor (None si aucune perte)
    expectancy = round(tot / len(rows), 2)
    best = max(rows, key=lambda r: r['pnl'])
    worst = min(rows, key=lambda r: r['pnl'])
    holds = [r['hold_days'] for r in rows if r['hold_days'] is not None]
    hold_avg = round(sum(holds) / len(holds), 1) if holds else None

    by_type = {}
    for r in rows:
        b = by_type.setdefault(r['type'], {'n': 0, 'pnl': 0.0})
        b['n'] += 1
        b['pnl'] = round(b['pnl'] + r['pnl'], 2)

    loss_by_sym = {}
    for r in losses:
        loss_by_sym[r['sym']] = loss_by_sym.get(r['sym'], 0) + 1
    repeat_losers = sorted([s for s, n in loss_by_sym.items() if n >= 2],
                           key=lambda s: -loss_by_sym[s])

    # Drapeaux comportementaux — DÉRIVÉS des chiffres, jamais psychologisés à vide.
    flags = []
    if avg_win is not None and avg_loss is not None and abs(avg_loss) > avg_win:
        flags.append('Perte moyenne (%.0f) supérieure au gain moyen (%.0f) — les stops '
                     'sont-ils respectés aussi vite que les prises de profit ?' % (avg_loss, avg_win))
    if repeat_losers:
        flags.append('Récidive de pertes sur : %s — même thèse rejouée sans nouvelle preuve ?'
                     % ', '.join(repeat_losers[:4]))
    if pf is not None and pf < 1:
        flags.append('Profit factor %.2f < 1 : le système perd de l\'argent en l\'état.' % pf)
    if win_rate >= 60 and tot < 0:
        flags.append('Win rate élevé (%d %%) mais P&L total négatif — les pertes sont '
                     'trop grosses par rapport aux gains.' % win_rate)
    opt_pnl = sum(v['pnl'] for k, v in by_type.items() if k != 'STK')
    stk_pnl = (by_type.get('STK') or {}).get('pnl', 0.0)
    if opt_pnl < 0 and stk_pnl > 0:
        flags.append('Les options détruisent ce que les actions construisent '
                     '(options %.0f vs actions %.0f).' % (opt_pnl, stk_pnl))

    # Erreurs/leçons explicitement notées dans le journal (texte de l'utilisateur, réel).
    mistakes = []
    for e in (journal or []):
        if isinstance(e, dict) and (e.get('mistake') or '').strip():
            mistakes.append({'ticker': e.get('ticker'), 'mistake': str(e['mistake'])[:140],
                             'date': e.get('date')})
    mistakes = mistakes[-8:]

    narrative = _narrative(len(rows), win_rate, tot, pf, expectancy, best, worst, flags)

    return {
        'empty': False, 'trades_n': len(rows), 'wins': len(wins), 'losses': len(losses),
        'win_rate': win_rate, 'total_pnl': round(tot, 2),
        'avg_win': avg_win, 'avg_loss': avg_loss, 'profit_factor': pf,
        'expectancy': expectancy,
        'best': {'sym': best['sym'], 'pnl': best['pnl'], 'pnl_pct': best['pnl_pct']},
        'worst': {'sym': worst['sym'], 'pnl': worst['pnl'], 'pnl_pct': worst['pnl_pct']},
        'by_type': by_type, 'repeat_losers': repeat_losers, 'hold_days_avg': hold_avg,
        'flags': flags, 'mistakes': mistakes, 'narrative': narrative,
        'generator': 'deterministic',
    }


def _narrative(n, wr, tot, pf, exp, best, worst, flags):
    parts = ['%d trade(s) clôturé(s) : %d %% de réussite, P&L cumulé %.0f.' % (n, wr, tot)]
    if pf is not None:
        parts.append('Profit factor %.2f, espérance %.0f par trade.' % (pf, exp))
    parts.append('Meilleur : %s (%+.0f) · pire : %s (%+.0f).'
                 % (best['sym'], best['pnl'], worst['sym'], worst['pnl']))
    if flags:
        parts.append('Point de discipline prioritaire : %s' % flags[0])
    else:
        parts.append('Aucun drapeau de discipline détecté sur cet échantillon.')
    parts.append('Post-mortem descriptif — pas un conseil ; la discipline (stops, '
                 'dimensionnement) reste la règle.')
    return ' '.join(parts)


__all__ = ['build']
