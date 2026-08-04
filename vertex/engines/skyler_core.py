"""vertex/engines/skyler_core.py — SKYLER CORE (SKYLER LOT 5).

Pipeline canonique (SKYLER_ARCHITECTURE.md) :

  contextes déjà calculés (technique, marché, catalyseurs, anomalies)
    → SkylerPacket typé (contradictions, inconnues, freshness floor, audit trail)
    → hard gates (PRIORITAIRES — le score ne les contourne jamais)
    → score /40 depuis les blocs de la Constitution V2
    → scénarios (niveaux RÉELS du plan moteur ; probabilité None tant qu'aucun
      modèle calibré — jamais un chiffre arbitraire)
    → SkylerDecision déterministe (vocabulaire canonique, sans Claude).

Règles d'honnêteté :
  - un contexte non branché est INSUFFISANT (0 point, listé), jamais rempli ;
  - Skyler CONSOMME le verdict canonique existant (decision_stack) et ne le
    contredit jamais vers le haut — désaccord = contradiction tracée + prudence ;
  - chaque point de score porte sa justification (`basis`) ;
  - fonctions PURES, déterministes, JSON-sérialisables. Aucun ordre.
"""
from __future__ import annotations

SCHEMA_VERSION = 1
ENGINE_VERSION = '0.1.0'

_BULLISH = ('ACHETER', 'RENFORCER', 'BUY')


def _profile():
    from vertex.strategy.constitution import load_profile
    return load_profile()


# ─── SkylerPacket ───────────────────────────────────────────────────────────────

def build_packet(sym, detail, market=None, events=None, anomaly=None,
                 as_of=None, demo=False, options_ctx=None):
    """Agrège les sorties moteurs existantes en un packet typé — sans muter les
    sources, sans recalculer, sans inventer."""
    detail = detail or {}
    audit = [{'step': 'inputs', 'result': {
        'detail': bool(detail), 'market': market is not None,
        'events': events is not None, 'anomaly': anomaly is not None}}]
    prof = _profile()

    plan = detail.get('plan') or {}
    technical = ({'available': True, 'score': detail.get('score'),
                  'verdict': detail.get('verdict'), 'trend': detail.get('trend'),
                  'rsi': detail.get('rsi'), 'regime': detail.get('regime'),
                  'setup_quality': detail.get('setup_quality'),
                  'confidence': detail.get('confidence'),
                  'atr_pct': detail.get('atr_pct'), 'plan': plan or None}
                 if detail.get('score') is not None else
                 {'available': False, 'reason': 'aucun détail technique du scan pour ce titre'})

    contexts = {
        'market': market if market is not None else {'available': False,
                                                     'reason': 'MarketContext non fourni'},
        'technical': technical,
        'catalysts': events if events is not None else {'available': False,
                                                        'reason': 'timeline non fournie'},
        'anomalies': anomaly if anomaly is not None else {'available': False,
                                                          'reason': 'scan anomalies non fourni'},
        'fundamentals': {'available': False,
                         'reason': 'contexte fondamental non branché (lot ultérieur)'},
        'options': (options_ctx if options_ctx is not None else
                    {'available': False, 'reason': 'OptionsContext non fourni'}),
        'portfolio': {'available': False,
                      'reason': 'PortfolioContext non branché (lot 7)'},
    }
    audit.append({'step': 'contexts', 'result': {
        k: bool(v.get('available', True)) for k, v in contexts.items()}})

    # Détecteur de contradictions (déterministe, jamais résolu en douce).
    contradictions = []
    verdict = (detail.get('verdict') or '').upper()
    reg = ((market or {}).get('regime') or {})
    adj = reg.get('adjustments') or {}
    if verdict in _BULLISH and adj.get('new_risk_allowed') is False:
        contradictions.append({'kind': 'verdict_vs_regime',
                               'detail': 'Verdict haussier (%s) alors que le régime %s bloque le risque neuf.'
                                         % (verdict, reg.get('label'))})
    if verdict in _BULLISH and (anomaly or {}).get('extreme') == 'low':
        contradictions.append({'kind': 'verdict_vs_extreme',
                               'detail': 'Verdict haussier alors que le titre clôture au plus BAS de sa fenêtre.'})
    for c in ((market or {}).get('conflicts') or []):
        contradictions.append({'kind': 'sources_conflict',
                               'detail': 'Sources en conflit sur %s (non résolu).' % c.get('dimension')})
    audit.append({'step': 'contradictions', 'result': len(contradictions)})

    unknowns = sorted(k for k, v in contexts.items() if v.get('available') is False)

    return {
        'schema_version': SCHEMA_VERSION, 'engine_version': ENGINE_VERSION,
        'profile_version': getattr(prof, 'version', None),
        'symbol': sym, 'generated_as_of': as_of, 'freshness_floor': as_of,
        'demo': bool(demo), 'contexts': contexts,
        'contradictions': contradictions, 'unknowns': unknowns,
        'audit_trail': audit,
    }


# ─── Score /40 (blocs de la Constitution V2) ────────────────────────────────────

def score40(packet):
    """Score par blocs du profil actif. Chaque point est justifié ; un bloc sans
    contexte branché vaut 0 et est listé INSUFFICIENT — jamais estimé."""
    prof = _profile()
    cfg = (prof.raw.get('skyler_score') or {}).get('blocks') or {}
    ctx = packet['contexts']
    tech = ctx['technical'] if ctx['technical'].get('available') else {}
    plan = tech.get('plan') or {}
    ev = ctx['catalysts'] if ctx['catalysts'].get('available', True) and ctx['catalysts'].get('events') is not None else None
    ano = ctx['anomalies'] if ctx['anomalies'].get('available', True) and 'events' in (ctx['anomalies'] or {}) else None
    reg = (ctx['market'] or {}).get('regime') or {}

    blocks = {}

    def block(name, points, status, basis):
        mx = cfg.get(name, 0)
        blocks[name] = {'points': max(0, min(int(points), mx)), 'max': mx,
                        'status': status, 'basis': basis}

    block('fundamentals_quality', 0, 'INSUFFICIENT',
          'contexte fondamental non branché — 0 point, jamais estimé')

    if ev is None:
        block('catalysts', 0, 'INSUFFICIENT', 'timeline d’événements non fournie')
    else:
        dated = [e for e in ev.get('events', []) if e.get('dte') is not None]
        near = [e for e in dated if e['dte'] <= 90]
        if near:
            block('catalysts', 2, 'PARTIAL',
                  '%d événement(s) daté(s) ≤ 90 j — présence datée seulement, '
                  'nouveauté/pricing non évalués (plafonné 2/%d)' % (len(near), cfg.get('catalysts', 5)))
        else:
            block('catalysts', 0, 'AVAILABLE', 'aucun catalyseur daté ≤ 90 j')

    score = tech.get('score')
    if score is None:
        block('technical_timing', 0, 'INSUFFICIENT', 'score technique absent')
    else:
        pts = round(score * cfg.get('technical_timing', 6) / 100.0)
        block('technical_timing', pts, 'AVAILABLE',
              'score technique moteur %s/100 → %d/%d' % (score, pts, cfg.get('technical_timing', 6)))

    if ano is None:
        block('institutions_flow_anomalies', 0, 'INSUFFICIENT',
              'flux institutionnels non branchés et anomalies non fournies')
    else:
        block('institutions_flow_anomalies', 1, 'PARTIAL',
              'anomalies statistiques seules (%d évènement(s)) — flux institutionnels '
              'non branchés (plafonné 1/%d)' % (len(ano.get('events', [])),
                                                cfg.get('institutions_flow_anomalies', 4)))

    label, conf = reg.get('label'), reg.get('confidence') or 0.0
    if not label or label == 'UNKNOWN':
        block('market_regime_sector', 0, 'INSUFFICIENT', 'régime inconnu (dimensions insuffisantes)')
    else:
        pts = {'TREND_UP': 4, 'RISK_ON': 4, 'VOLATILITY_COMPRESSION': 3,
               'CHOP': 2, 'TRANSITION': 2, 'MEAN_REVERSION': 2,
               'RISK_OFF': 1, 'TREND_DOWN': 1, 'VOLATILITY_EXPANSION': 1,
               'EUPHORIA': 1, 'PANIC': 0}.get(label, 0)
        if conf < 0.5 and pts > 0:
            pts -= 1
        block('market_regime_sector', pts, 'AVAILABLE',
              'régime %s (confiance %.2f) → %d/%d' % (label, conf, pts,
                                                      cfg.get('market_regime_sector', 4)))

    rr = plan.get('rr_res')
    if rr is None:
        block('asymmetry_scenarios', 0, 'INSUFFICIENT', 'plan moteur absent — R:R structurel inconnu')
    else:
        pts = 6 if rr >= 3 else 4 if rr >= 2 else 2 if rr >= 1 else 0
        block('asymmetry_scenarios', pts, 'AVAILABLE',
              'R:R structurel vers la résistance = %.1f → %d/%d' % (rr, pts,
                                                                    cfg.get('asymmetry_scenarios', 6)))

    octx = ctx['options']
    if not octx.get('available'):
        block('options_quality', 0, 'INSUFFICIENT',
              octx.get('reason') or 'OptionsContext indisponible')
    else:
        best = octx.get('best') or {}
        q = best.get('quality')
        if q is None:
            block('options_quality', 1, 'PARTIAL',
                  'candidat %s sans note de qualité — 1/%d' % (octx.get('universe'),
                                                               cfg.get('options_quality', 6)))
        else:
            pts = round(q * cfg.get('options_quality', 6) / 100.0)
            status = 'AVAILABLE'
            basis = 'meilleur candidat %s qualité %s/100 → %d/%d' % (
                octx.get('universe'), q, pts, cfg.get('options_quality', 6))
            if not octx.get('best_in_mandate', True):
                pts = min(pts, cfg.get('options_quality', 6) // 2)
                status = 'PARTIAL'
                basis += ' — plafonné : meilleur candidat HORS MANDAT'
            block('options_quality', pts, status, basis)

    avail = sum(1 for name in ('technical', 'market', 'catalysts', 'anomalies')
                if packet['contexts'][name].get('available', True) is not False)
    block('data_quality', avail, 'AVAILABLE' if avail >= 2 else 'INSUFFICIENT',
          '%d/4 contextes branchés disponibles → %d/%d' % (avail, avail, cfg.get('data_quality', 4)))

    total = sum(b['points'] for b in blocks.values())
    insufficient = sorted(n for n, b in blocks.items() if b['status'] == 'INSUFFICIENT')

    lv = (prof.raw.get('conviction_levels') or {})
    if total >= (lv.get('S_PLUS') or {}).get('score_min', 36):
        level = 'S_PLUS'
    elif total >= (lv.get('S') or {}).get('score_min', 32):
        level = 'S'
    elif total >= (lv.get('A') or {}).get('score_min', 28):
        level = 'A'
    elif total >= (lv.get('B') or {}).get('score_min', 24):
        level = 'B'
    else:
        level = 'REFUS_WATCH'
    # Constitution : S+ impossible si des blocs critiques manquent.
    if insufficient and level in ('S_PLUS', 'S'):
        level = 'A'

    return {'total': total, 'max': 40, 'blocks': blocks, 'level': level,
            'insufficient_blocks': insufficient,
            'note': 'Le score ne contourne jamais les hard gates ; blocs non branchés = 0, jamais estimés.'}


# ─── Hard gates (prioritaires) ──────────────────────────────────────────────────

def hard_gates(packet, score):
    """Évalue les portes de la Constitution V2. Non évaluable ≠ non déclenché :
    triggered=None + raison (contexte non branché)."""
    prof = _profile()
    ids = prof.raw.get('hard_gates') or []
    tech = packet['contexts']['technical']
    plan = (tech.get('plan') or {}) if tech.get('available') else {}
    out = []

    def gate(gid, triggered, reason):
        out.append({'id': gid, 'triggered': triggered, 'reason': reason})

    for gid in ids:
        if gid == 'RR_BELOW_2':
            rr = plan.get('rr_res')
            if rr is None:
                gate(gid, None, 'R:R structurel inconnu (plan absent)')
            else:
                gate(gid, bool(rr < 2.0), 'R:R structurel = %.1f (minimum 2.0)' % rr)
        elif gid == 'NO_INVALIDATION':
            gate(gid, plan.get('stop') is None, 'stop technique %s' %
                 ('présent (%.2f)' % plan['stop'] if plan.get('stop') is not None else 'ABSENT'))
        elif gid == 'DATA_QUALITY_CRITICAL':
            trig = (not tech.get('available')) or \
                   (score['blocks'].get('data_quality', {}).get('points', 0) < 2) or \
                   (len(score['insufficient_blocks']) >= 4)
            gate(gid, bool(trig), '%d bloc(s) insuffisant(s) ; qualité données %s/4'
                 % (len(score['insufficient_blocks']),
                    score['blocks'].get('data_quality', {}).get('points', 0)))
        elif gid == 'SOURCES_CONFLICT':
            confl = [c for c in packet['contradictions'] if c['kind'] == 'sources_conflict']
            gate(gid, bool(confl), '%d conflit(s) de sources' % len(confl))
        elif gid == 'THESIS_BROKEN':
            ext = (packet['contexts']['anomalies'] or {}).get('extreme') \
                if packet['contexts']['anomalies'].get('available', True) else None
            v = (tech.get('verdict') or '').upper()
            gate(gid, bool(v in _BULLISH and ext == 'low'),
                 'verdict %s vs extrême de fenêtre %s' % (v or 'n/d', ext or 'aucun'))
        else:
            gate(gid, None, 'contexte requis non branché (lots 6-7) — porte non évaluable, jamais supposée fermée')
    return out


# ─── Scénarios (niveaux réels, probabilités jamais inventées) ───────────────────

def scenarios(detail):
    plan = (detail or {}).get('plan') or {}
    entry, stop = plan.get('entry'), plan.get('stop')
    tp2, tp3 = plan.get('tp2'), plan.get('tp3')
    if entry is None or stop is None or tp2 is None:
        return {'available': False,
                'reason': 'plan moteur incomplet — aucun scénario inventé'}

    note = 'modèle de probabilité non calibré — aucune probabilité affichée (lot 9 : calibration)'

    def sc(name, target, trigger):
        return {'name': name, 'target': target,
                'return_pct': round((target / entry - 1) * 100, 2),
                'trigger': trigger, 'invalidation': stop,
                'probability': None, 'probability_note': note,
                'horizon_days': None,
                'assumptions': ['niveaux réels du plan moteur (ATR/structure)'],
                'unknowns': ['probabilités non calibrées', 'horizon non modélisé']}

    return {'available': True,
            'bear': sc('pessimiste', stop, 'cassure du stop technique'),
            'base': sc('probable', tp2, 'poursuite de la tendance vers TP2'),
            'bull': sc('exceptionnel', tp3 if tp3 is not None else tp2,
                       'extension au-delà de la résistance'),
            'model': {'type': 'plan_levels_deterministic', 'calibrated': False}}


# ─── SkylerDecision (déterministe, sans Claude) ─────────────────────────────────

def decide(sym, detail, market=None, events=None, anomaly=None, as_of=None,
           demo=False, options_ctx=None):
    packet = build_packet(sym, detail, market=market, events=events,
                          anomaly=anomaly, as_of=as_of, demo=demo,
                          options_ctx=options_ctx)
    score = score40(packet)
    gates = hard_gates(packet, score)
    scen = scenarios(detail)
    audit = list(packet['audit_trail'])
    audit.append({'step': 'score40', 'result': score['total']})
    triggered = [g for g in gates if g['triggered'] is True]
    audit.append({'step': 'hard_gates', 'result': [g['id'] for g in triggered]})

    verdict = ((detail or {}).get('verdict') or '').upper()
    if triggered:
        decision = 'REFUSER' if score['total'] < 24 else 'ATTENDRE'
        capped_by = triggered[0]['id']
        main_reason = 'Hard gate %s : %s' % (capped_by, triggered[0]['reason'])
    else:
        capped_by = None
        if score['total'] >= 28:
            decision = 'ACHETER'
        elif score['total'] >= 24:
            decision = 'ATTENDRE'
        else:
            decision = 'REFUSER'
        main_reason = 'Score Skyler %d/40 (niveau %s)' % (score['total'], score['level'])
        # Jamais plus agressif que le verdict canonique existant.
        if decision == 'ACHETER' and verdict and verdict not in _BULLISH:
            decision = 'ATTENDRE'
            main_reason += ' — plafonné : le verdict canonique (%s) est prudent' % verdict
            packet['contradictions'].append({'kind': 'skyler_vs_canonical',
                                             'detail': 'Skyler favorable mais verdict canonique %s — décision plafonnée.' % verdict})
    audit.append({'step': 'decision', 'result': decision})

    plan = (detail or {}).get('plan') or {}
    entry, stop = plan.get('entry'), plan.get('stop')
    max_risk_pct = (round((entry - stop) / entry * 100, 2)
                    if entry and stop is not None and entry > 0 else None)

    dated = sorted([e for e in ((events or {}).get('events') or [])
                    if e.get('dte') is not None], key=lambda e: e['dte'])
    catalyst = ('%s (J-%d)' % (dated[0]['label'], dated[0]['dte'])) if dated else None

    if packet['contradictions']:
        objection = packet['contradictions'][0]['detail']
    elif triggered:
        objection = triggered[0]['reason']
    elif score['insufficient_blocks']:
        objection = 'Blocs non branchés (%s) — la note est incomplète par construction.' \
                    % ', '.join(score['insufficient_blocks'])
    else:
        objection = 'Probabilités des scénarios non calibrées (lot 9).'

    unknown_gates = sorted(g['id'] for g in gates if g['triggered'] is None)

    return {
        'symbol': sym, 'generator': 'deterministic', 'as_of': as_of,
        'decision': decision, 'capped_by_gate': capped_by,
        'score': score, 'level': score['level'],
        'gates': gates, 'scenarios': scen,
        'invalidation': stop, 'max_risk_pct': max_risk_pct,
        'catalyst': catalyst,
        'main_reason': main_reason, 'strongest_objection': objection,
        'unknowns': sorted(set(packet['unknowns'] + unknown_gates)),
        'contradictions': packet['contradictions'],
        'audit_trail': audit,
        'note': 'Décision analytique READONLY — jamais un ordre ; Claude peut rédiger, jamais modifier ces chiffres.',
    }


__all__ = ['build_packet', 'score40', 'hard_gates', 'scenarios', 'decide',
           'SCHEMA_VERSION', 'ENGINE_VERSION']
