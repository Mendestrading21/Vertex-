"""vertex/ai/copilot.py — COPILOTE D'ANALYSE (assistant intellectuel de trading).

Répond en français à une question de trading en s'ANCRANT exclusivement dans les
nombres réels déjà calculés par Vertex : session d'analyse (digest), positionnement
dealer (GEX/flux/thèse) du titre, positions déclarées du desk. Deux modes :

- Claude (ANTHROPIC_API_KEY présente) : rédige une synthèse d'analyste à partir du
  contexte JSON fourni — étiquetée « via Claude », JAMAIS présentée comme donnée broker.
- Repli déterministe (pas de clé) : assemble honnêtement les récits moteurs existants.

INVARIANTS ABSOLUS :
- lecture seule — le copilote ne passe, ne modifie, ne suggère d'exécuter AUCUN ordre ;
- aucune donnée inventée : le contexte transmis à Claude est le JSON réel, et le prompt
  interdit d'affirmer un chiffre absent du contexte ;
- aucune clé/secret écrit ou renvoyé ; questions bornées ; réponses bornées.
"""
from __future__ import annotations

import json

from vertex.ai import briefs
from vertex.services import persist

MAX_QUESTION = 500
MODEL = briefs.MODEL                      # même modèle que la couche IA existante

_SYSTEM = (
    "Tu es le copilote d'analyse du terminal Vertex (lecture seule). Tu réponds en "
    "français, en analyste de marché discipliné. RÈGLES STRICTES : "
    "1) Fonde CHAQUE affirmation chiffrée sur le CONTEXTE JSON fourni — si une donnée "
    "n'y est pas, dis « donnée indisponible », n'invente jamais. "
    "2) Tu ne recommandes JAMAIS de passer, modifier ou clôturer un ordre ; tu analyses. "
    "3) Distingue toujours faits (chiffres du contexte) et interprétation. "
    "4) Termine par une ligne « Risques / à surveiller ». Réponse ≤ 220 mots."
)


def _positions_for(symbol=None):
    """Positions déclarées du desk (myTrades du blob serveur) — jamais inventées."""
    try:
        blob = persist.load_json('desk_data.json', {}) or {}
        raw = (blob.get('data') or {}).get('myTrades')
        trades = json.loads(raw) if isinstance(raw, str) else (raw or [])
    except Exception:
        return []
    out = []
    for t in trades if isinstance(trades, list) else []:
        if not isinstance(t, dict):
            continue
        if symbol and str(t.get('sym', '')).upper() != symbol:
            continue
        out.append({'sym': t.get('sym'), 'type': t.get('type'), 'qty': t.get('qty'),
                    'cost': t.get('cost'), 'strike': t.get('strike'), 'exp': t.get('exp'),
                    'stop': (t.get('entrySnap') or {}).get('stop')})
    return out[:20]


def build_context(scan_state, symbol=None):
    """Contexte RÉEL du copilote : digest de session + positionnement du titre + desk."""
    from vertex.engines import session_digest
    from vertex.options import gex as _gex, flow as _flow, dealer_synthesis as _ds
    scan_state = scan_state or {}
    ctx = {'digest': session_digest.build(scan_state, None)}
    sym = str(symbol or '').upper() or None
    if sym:
        board = scan_state.get('options_board') or []
        contracts = [c for c in board if str(c.get('sym', '')).upper() == sym]
        detail = (scan_state.get('detail') or {}).get(sym) or {}
        profile = _gex.compute(contracts, spot=detail.get('price'), symbol=sym)
        # le récit complet est volumineux : on transmet l'essentiel chiffré
        ctx['positioning'] = {k: profile.get(k) for k in (
            'symbol', 'spot', 'empty', 'net_gex_total', 'net_vanna_total', 'regime',
            'bias', 'zero_gamma', 'call_wall', 'put_wall', 'contracts_used')}
        ctx['flow'] = _flow.analyze(contracts, symbol=sym, top=4)
        ctx['synthesis'] = _ds.build(profile, ctx['flow'],
                                     earnings_in_days=detail.get('earnings_in_days'),
                                     symbol=sym)
        ctx['detail'] = {'price': detail.get('price'), 'score': detail.get('score'),
                         'earnings_in_days': detail.get('earnings_in_days')}
    ctx['positions'] = _positions_for(sym)
    # Post-mortem du journal (résumé chiffré) : ancre les questions de discipline
    # (« quelles sont mes erreurs récurrentes ? ») dans les trades RÉELS clôturés.
    try:
        blob = persist.load_json('desk_data.json', {}) or {}
        data = blob.get('data') or {}

        def _parse(key):
            raw = data.get(key)
            v = json.loads(raw) if isinstance(raw, str) else (raw or [])
            return v if isinstance(v, list) else []
        from vertex.engines import postmortem as _pm
        pm = _pm.build(_parse('myTradesClosed'), _parse('vxJournal'))
        if not pm.get('empty'):
            ctx['postmortem'] = {k: pm.get(k) for k in (
                'trades_n', 'win_rate', 'total_pnl', 'profit_factor', 'expectancy',
                'repeat_losers', 'flags', 'best', 'worst')}
    except Exception:
        pass
    return ctx


def _fallback(ctx, symbol, conseil_cle=True):
    """Repli déterministe honnête : récits moteurs existants. `conseil_cle`
    est faux quand la clé EXISTE mais que le budget d'appels est atteint —
    conseiller de configurer la clé serait alors un mensonge."""
    parts = []
    syn = ctx.get('synthesis') or {}
    if syn.get('narrative'):
        parts.append(syn['narrative'])
    dg = ctx.get('digest') or {}
    reg = (dg.get('regime') or {})
    if reg.get('label'):
        parts.append('Climat de marché : %s.' % reg['label'])
    pos = ctx.get('positions') or []
    if pos:
        parts.append('%d position(s) déclarée(s)%s dans le desk.' % (
            len(pos), (' sur ' + symbol) if symbol else ''))
    if not parts:
        parts.append('Pas assez de données réelles pour répondre — lance une analyse '
                     'ou attends la fin du scan.')
    if conseil_cle:
        parts.append('(Réponse assemblée par les moteurs déterministes — configure '
                     'ANTHROPIC_API_KEY pour la synthèse rédigée par Claude.)')
    else:
        parts.append('(Réponse assemblée par les moteurs déterministes — limite '
                     'd\'appels IA atteinte, réessaie dans une minute.)')
    return ' '.join(parts)


def answer(question, scan_state, symbol=None):
    """Réponse du copilote. Retourne un dict JSON-sérialisable, jamais d'exception."""
    q = str(question or '').strip()[:MAX_QUESTION]
    sym = (str(symbol or '').upper()[:12] or None)
    if not q:
        return {'ok': False, 'error': 'question vide', 'source': None, 'answer': None}
    try:
        ctx = build_context(scan_state, sym)
    except Exception as e:
        return {'ok': False, 'error': 'contexte indisponible: %s' % e,
                'source': None, 'answer': None}

    #  Lot 11 : l'appel Claude passe par la porte partagée (budget + audit).
    #  Un refus de budget n'est PAS une panne : repli déterministe, libellé
    #  qui dit la VRAIE raison. La porte n'est consultée que si la couche IA
    #  est disponible — sans clé, rien n'est consommé.
    label_repli = 'Moteurs déterministes (Claude non configuré ou indisponible)'
    conseil_cle = True
    if briefs.available():
        from vertex.ai import gateway as _gw
        if not _gw.allow('copilot', sym or ''):
            label_repli = ('Moteurs déterministes (limite d\'appels IA atteinte '
                           '— réessaie dans une minute)')
            conseil_cle = False
        else:
            import time as _time
            t0 = _time.monotonic()
            try:
                from anthropic import Anthropic
                client = Anthropic()
                payload = json.dumps(ctx, ensure_ascii=False, default=str)[:14000]
                msg = client.messages.create(
                    model=MODEL, max_tokens=600, system=_SYSTEM,
                    messages=[{'role': 'user', 'content':
                               'CONTEXTE JSON (données réelles Vertex) :\n%s\n\nQUESTION : %s'
                               % (payload, q)}])
                txt = (msg.content[0].text or '').strip()
                if txt:
                    _gw.record(source='copilot', symbol=sym or '', ok=True,
                               duration_ms=round((_time.monotonic() - t0) * 1000, 1),
                               model=MODEL)
                    return {'ok': True, 'answer': txt, 'source': 'claude', 'model': MODEL,
                            'symbol': sym, 'label': 'Analyse via Claude — estimation, pas une donnée broker',
                            'readonly': True}
                _gw.record(source='copilot', symbol=sym or '', ok=False,
                           errors=['empty_response'],
                           duration_ms=round((_time.monotonic() - t0) * 1000, 1),
                           model=MODEL)
            except Exception as exc:                # repli déterministe ci-dessous
                _gw.record(source='copilot', symbol=sym or '', ok=False,
                           errors=[exc.__class__.__name__],
                           duration_ms=round((_time.monotonic() - t0) * 1000, 1),
                           model=MODEL)
    return {'ok': True, 'answer': _fallback(ctx, sym, conseil_cle),
            'source': 'deterministic',
            'model': None, 'symbol': sym, 'label': label_repli,
            'readonly': True}


__all__ = ['answer', 'build_context']
