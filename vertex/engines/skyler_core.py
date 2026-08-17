"""vertex/engines/skyler_core.py — SKYLER CORE (LOT 5, étendu 0.2.0 → 0.7.0).

Pipeline canonique (SKYLER_ARCHITECTURE.md + DECISION_ENGINE.md) :

  contextes déjà calculés (technique, marché, catalyseurs, anomalies, options,
  portefeuille) + revue red-team produite (red_team.review)
    → SkylerPacket typé (contradictions, inconnues, freshness floor, audit trail)
    → hard gates (PRIORITAIRES — le score ne les contourne jamais)
    → score /40 (Constitution V2) plafonné par blocs insuffisants ET par
      l'absence de red-team pour S/S+ (apply_red_team_rule)
    → scénarios (niveaux RÉELS du plan moteur ; probabilité None tant qu'aucun
      modèle calibré — jamais un chiffre arbitraire)
    → SkylerDecision déterministe (vocabulaire canonique, sans Claude) +
      état opérationnel dérivé (operational_state) +
      confiance factorisée (confidence : data_quality × agreement ×
      robustness mesurée par perturbation × calibration réelle par contexte).

Règles d'honnêteté :
  - un contexte non branché est INSUFFISANT (0 point, listé), jamais rempli ;
  - Skyler CONSOMME le verdict canonique existant (decision_stack) et ne le
    contredit jamais vers le haut — désaccord = contradiction tracée + prudence ;
  - chaque point de score et chaque facteur de confiance portent leur `basis` ;
  - tout changement de règle bumpe ENGINE_VERSION (historique des décisions
    figé PAR version dans la mémoire — jamais recalculé) ;
  - fonctions PURES, déterministes, JSON-sérialisables. Aucun ordre.
"""
from __future__ import annotations

SCHEMA_VERSION = 1
# 0.2.0 : règle red-team S/S+ · 0.3.0 : état opérationnel + confiance factorisée
# 0.4.0 : la revue red-team PRODUITE (red_team.review) entre dans la décision
# 0.5.0 : robustness MESURÉE par analyse de perturbation (liste fixe, déterministe)
# 0.6.0 : calibration RÉELLE (scenario hit rate de la mémoire, par version, bornée)
# 0.7.0 : calibration PAR CONTEXTE consommée (cellule du niveau courant si mesurée)
# 0.8.0 : priorité étendue niveau → RÉGIME → global (régime figé dans la mémoire)
# 0.9.0 : catalyst_kind émis (kind EXPLICITE du même événement daté le plus
#         proche que `catalyst` — fait du moteur events, jamais re-parsé)
# 1.0.0 : les gates DTE / liquidité du mandat options sont évaluées depuis le
#         meilleur candidat réellement transmis au SkylerPacket.
# 1.1.0 : qualité et réconciliation deviennent des contextes explicites ; le
#         nombre de modules branchés ne peut plus simuler une donnée fiable.
ENGINE_VERSION = '1.1.0'

PERTURBATIONS = ('score_technique_-10', 'score_technique_+10', 'rr_-0.5', 'rr_+0.5',
                 'regime_confidence_-0.2', 'regime_confidence_+0.2',
                 'sans_market', 'sans_events', 'sans_anomaly', 'sans_options',
                 'sans_portfolio')

_BULLISH = ('ACHETER', 'RENFORCER', 'BUY')

OPERATIONAL_STATES = ('SURVEILLER', 'PREPARER', 'DECLENCHEMENT_CONDITIONNEL',
                      'CONFIRMATION_REQUISE', 'SECURISATION_PARTIELLE', 'RUNNER',
                      'THESE_A_REEVALUER', 'DONNEES_INSUFFISANTES')


def operational_state(decision, gates, plan):
    """DECISION_ENGINE §2.2 : état opérationnel analytique dérivé
    DÉTERMINISTIQUEMENT — précise le contexte, ne devient jamais une décision
    finale. Ordre des règles : données d'abord, thèse ensuite, puis le plan."""
    trig = {g['id'] for g in (gates or []) if g.get('triggered') is True}
    if 'DATA_QUALITY_CRITICAL' in trig:
        return 'DONNEES_INSUFFISANTES', 'gate DATA_QUALITY_CRITICAL active — données critiques insuffisantes'
    if 'THESIS_BROKEN' in trig:
        return 'THESE_A_REEVALUER', 'gate THESIS_BROKEN active — la thèse doit être réévaluée'
    if decision in ('ACHETER', 'RENFORCER'):
        return 'PREPARER', 'décision %s — préparation analytique de l’entrée (jamais un ordre)' % decision
    if decision == 'ATTENDRE':
        if trig:
            return 'CONFIRMATION_REQUISE', ('attente plafonnée par gate(s) %s — confirmation requise'
                                            % ', '.join(sorted(trig)))
        if plan and plan.get('entry') is not None and plan.get('tp2') is not None:
            return 'DECLENCHEMENT_CONDITIONNEL', ('plan moteur présent (entrée %.2f) — déclenchement conditionnel'
                                                  % plan['entry'])
        return 'SURVEILLER', 'attente sans plan complet — simple surveillance'
    return 'SURVEILLER', 'décision %s — surveillance par défaut' % (decision or 'n/d')


def confidence(packet, score, robustness=None, calibration=None):
    """DECISION_ENGINE §7 : confidence = data_quality × agreement × robustness ×
    calibration. Chaque facteur borné [0,1] avec base explicite ; plafonds
    obligatoires (régime UNKNOWN ≤ 0,55 ; conflit de sources ≤ 0,50 ;
    contradiction ≤ 0,60) ; calibration plafonnée à 0,50 tant qu'aucun
    historique n'existe. `robustness` MESURÉE par analyse de perturbation
    (0.5.0) quand fournie — proxy blocs insuffisants en secours, dit.
    ESTIMATION (F3) à méthode documentée — jamais 100 %."""
    dq_pts = (score['blocks'].get('data_quality') or {}).get('points', 0)
    n_contra = len(packet['contradictions'])
    n_insuf = len(score['insufficient_blocks'])
    if robustness is not None and robustness.get('value') is not None:
        rob = {'value': robustness['value'],
               'basis': 'analyse de perturbation : %d/%d perturbation(s) laissent la '
                        'décision inchangée%s' % (robustness.get('stable', 0),
                                                  robustness.get('n_applicable', 0),
                        ' — bascule sous : ' + ', '.join(f['perturbation']
                                                         for f in robustness.get('flipped', []))
                        if robustness.get('flipped') else '')}
    else:
        rob = {'value': round(max(0.0, 1.0 - n_insuf / 8.0), 3),
               'basis': '%d bloc(s) insuffisant(s) sur 8 — proxy de robustesse '
                        '(analyse de perturbation non applicable)' % n_insuf}
    factors = {
        'data_quality': {'value': round(dq_pts / 4.0, 3),
                         'basis': 'bloc data_quality %d/4 du score' % dq_pts},
        'agreement': {'value': round(max(0.0, 1.0 - 0.2 * n_contra), 3),
                      'basis': '%d contradiction(s) tracée(s) — −0,20 chacune' % n_contra},
        'robustness': rob,
        'calibration': ({'value': calibration['value'], 'basis': calibration['basis']}
                        if calibration is not None and calibration.get('value') is not None else
                        {'value': 0.5,
                         'basis': 'aucun historique de calibration — facteur plafonné à 0,50, '
                                  'jamais supposé calibré'}),
    }
    value = 1.0
    for f in factors.values():
        value *= f['value']
    caps = []
    reg = ((packet['contexts'].get('market') or {}).get('regime') or {})
    if (reg.get('label') or 'UNKNOWN') == 'UNKNOWN':
        value = min(value, 0.55)
        caps.append('régime UNKNOWN — confiance plafonnée à 0,55')
    if any(c['kind'] == 'sources_conflict' for c in packet['contradictions']):
        value = min(value, 0.50)
        caps.append('conflit de sources non résolu — confiance plafonnée à 0,50')
    elif n_contra:
        value = min(value, 0.60)
        caps.append('contradiction non résolue — confiance plafonnée à 0,60')
    return {'value': round(value, 3), 'factors': factors, 'caps_applied': caps,
            'estimated': True,
            'method': 'produit de facteurs déterministes documentés (F3), borné par '
                      'les plafonds de DECISION_ENGINE §7 — pas une probabilité calibrée'}


def apply_red_team_rule(level, red_team):
    """ADVERSARIAL_COMMITTEE §8 : une note S ou S+ sans red-team COMPLÉTÉE est
    invalide — plafonnée à A avec raison explicite. Les autres niveaux passent
    inchangés. Règle pure, déterministe."""
    if level in ('S_PLUS', 'S') and not (red_team or {}).get('complete'):
        return 'A', ('niveau %s plafonné à A : red-team absente ou incomplète '
                     '(obligatoire pour S/S+)' % level)
    return level, None


def _profile():
    from vertex.strategy.constitution import load_profile
    return load_profile()


# ─── SkylerPacket ───────────────────────────────────────────────────────────────

def build_packet(sym, detail, market=None, events=None, anomaly=None,
                 as_of=None, demo=False, options_ctx=None, portfolio_ctx=None,
                 red_team=None, data_quality_ctx=None, reconciliation_ctx=None, fundamental_ctx=None):
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
        'fundamentals': (fundamental_ctx if fundamental_ctx is not None else
                         {'available': False, 'reason': 'contexte fondamental non fourni'}),
        'options': (options_ctx if options_ctx is not None else
                    {'available': False, 'reason': 'OptionsContext non fourni'}),
        'portfolio': (portfolio_ctx if portfolio_ctx is not None else
                      {'available': False, 'reason': 'PortfolioContext non fourni'}),
        'data_quality': (data_quality_ctx if data_quality_ctx is not None else
                         {'available': False, 'reason': 'preuve de qualité des données non fournie'}),
        'reconciliation': (reconciliation_ctx if reconciliation_ctx is not None else
                           {'available': False, 'reason': 'preuve de réconciliation non fournie'}),
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
    reconciliation = contexts['reconciliation'] or {}
    if reconciliation.get('available') and reconciliation.get('actionable_allowed') is False:
        contradictions.append({'kind': 'sources_conflict',
                               'detail': 'Réconciliation non actionnable : %s' %
                                         (reconciliation.get('reason') or 'conflit ou désalignement déclaré')})
    audit.append({'step': 'contradictions', 'result': len(contradictions)})

    unknowns = sorted(k for k, v in contexts.items() if v.get('available') is False)
    context_coverage = {
        'known_contexts': len(contexts) - len(unknowns),
        'total_contexts': len(contexts),
        'coverage_pct': round(100 * (len(contexts) - len(unknowns)) / len(contexts), 1) if contexts else 0.0,
        'unknown_contexts': unknowns,
        'read_only': True,
        'note': 'contextes manquants restent visibles et ne sont jamais considérés favorables',
    }

    return {
        'schema_version': SCHEMA_VERSION, 'engine_version': ENGINE_VERSION,
        'profile_version': getattr(prof, 'version', None),
        'symbol': sym, 'generated_as_of': as_of, 'freshness_floor': as_of,
        'demo': bool(demo), 'contexts': contexts,
        'red_team': (red_team if red_team is not None else
                     {'complete': False, 'basis': 'aucune red-team exécutée'}),
        'contradictions': contradictions, 'unknowns': unknowns,
        'context_coverage': context_coverage,
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

    dq = ctx['data_quality'] or {}
    rec = ctx['reconciliation'] or {}
    quality = dq.get('overall')
    if not dq.get('available'):
        block('data_quality', 0, 'INSUFFICIENT',
              dq.get('reason') or 'preuve de qualité des données non fournie')
    elif dq.get('actionable_allowed') is not True:
        block('data_quality', 0, 'INSUFFICIENT',
              'qualité %s non actionnable : %s' % (quality or 'inconnue',
                                                    '; '.join(dq.get('warnings') or [])))
    elif not rec.get('available') or rec.get('actionable_allowed') is not True:
        block('data_quality', 0, 'INSUFFICIENT',
              (rec.get('reason') or 'réconciliation non fournie ou non actionnable'))
    else:
        points = {'FRESH': 4, 'RECENT': 3}.get(quality, 0)
        status = 'AVAILABLE' if points else 'INSUFFICIENT'
        block('data_quality', points, status,
              'qualité critique %s et réconciliation actionnable → %d/%d' %
              (quality or 'inconnue', points, cfg.get('data_quality', 4)))

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
    # ADVERSARIAL_COMMITTEE §8 : S/S+ sans red-team complétée = invalide.
    level, rt_cap = apply_red_team_rule(level, packet.get('red_team'))

    return {'total': total, 'max': 40, 'blocks': blocks, 'level': level,
            'insufficient_blocks': insufficient,
            'red_team_cap': rt_cap,
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
            dq = packet['contexts'].get('data_quality') or {}
            rec = packet['contexts'].get('reconciliation') or {}
            trig = (not tech.get('available')) or (dq.get('actionable_allowed') is not True) or \
                   (rec.get('actionable_allowed') is not True) or \
                   (score['blocks'].get('data_quality', {}).get('points', 0) < 2) or \
                   (len(score['insufficient_blocks']) >= 4)
            gate(gid, bool(trig), '%d bloc(s) insuffisant(s) ; qualité %s ; réconciliation %s'
                 % (len(score['insufficient_blocks']), dq.get('overall') or 'non prouvée',
                    'actionnable' if rec.get('actionable_allowed') is True else 'non prouvée/non actionnable'))
        elif gid == 'SOURCES_CONFLICT':
            confl = [c for c in packet['contradictions'] if c['kind'] == 'sources_conflict']
            gate(gid, bool(confl), '%d conflit(s) de sources' % len(confl))
        elif gid == 'THESIS_BROKEN':
            ext = (packet['contexts']['anomalies'] or {}).get('extreme') \
                if packet['contexts']['anomalies'].get('available', True) else None
            v = (tech.get('verdict') or '').upper()
            gate(gid, bool(v in _BULLISH and ext == 'low'),
                 'verdict %s vs extrême de fenêtre %s' % (v or 'n/d', ext or 'aucun'))
        elif gid == 'LOSER_REINFORCEMENT':
            pctx = packet['contexts']['portfolio']
            cand = (pctx or {}).get('candidate') if pctx.get('available') else None
            v = (tech.get('verdict') or '').upper()
            if cand is None:
                gate(gid, None, 'portefeuille non fourni — renforcement perdant non évaluable')
            elif not cand.get('held'):
                gate(gid, False, 'aucune position existante sur ce titre')
            elif cand.get('is_loser') is None:
                gate(gid, None, 'P&L inconnu (cote absente) — jamais supposé gagnant')
            else:
                gate(gid, bool(cand['is_loser'] and v in _BULLISH),
                     'position %s (%+.1f %%) et verdict %s'
                     % ('PERDANTE' if cand['is_loser'] else 'gagnante',
                        cand.get('pnl_pct') or 0.0, v or 'n/d'))
        elif gid == 'CONCENTRATION_EXCESSIVE':
            pctx = packet['contexts']['portfolio']
            cand = (pctx or {}).get('candidate') if pctx.get('available') else None
            if cand is None:
                gate(gid, None, 'portefeuille non fourni — concentration non évaluable')
            else:
                try:
                    max_w = _profile().max_stock_weight_pct
                except Exception:
                    max_w = 15.0
                gate(gid, bool((cand.get('weight_pct') or 0.0) >= max_w),
                     'poids actuel %.1f %% (plafond %.0f %% par titre)'
                     % (cand.get('weight_pct') or 0.0, max_w))
        elif gid in ('SPREAD_EXCESSIVE', 'OI_INSUFFICIENT', 'DTE_OUT_OF_MANDATE'):
            octx = packet['contexts']['options'] or {}
            best = octx.get('best') or {}
            mandate = best.get('mandate') or {}
            if not octx.get('available') or not best:
                gate(gid, None, 'candidat options non fourni — gate non évaluable')
                continue
            if gid == 'SPREAD_EXCESSIVE':
                ok = mandate.get('spread_ok')
                gate(gid, None if ok is None else not bool(ok),
                     ('spread non fourni — jamais supposé conforme' if ok is None else
                      'spread %.2f %% %s le mandat' % (best.get('spread_pct') or 0,
                                                         'respecte' if ok else 'dépasse')))
            elif gid == 'OI_INSUFFICIENT':
                ok = mandate.get('oi_ok')
                gate(gid, None if ok is None else not bool(ok),
                     ('open interest non fourni — jamais supposé conforme' if ok is None else
                      'open interest %s %s le mandat' % (best.get('oi'),
                                                          'respecte' if ok else 'ne respecte pas')))
            else:
                dte = best.get('dte')
                window = octx.get('window') or []
                if not isinstance(dte, (int, float)) or len(window) != 2:
                    gate(gid, None, 'DTE ou fenêtre d’univers absent(e) — jamais supposé(e) conforme')
                else:
                    low, high = window
                    inclusive_high = octx.get('universe') == 'LEAPS'
                    in_window = low <= dte <= high if inclusive_high else low <= dte < high
                    gate(gid, not in_window,
                         'DTE %s %s la fenêtre %s de %s' %
                         (dte, 'respecte' if in_window else 'sort de', window,
                          octx.get('universe') or 'l’univers'))
        else:
            gate(gid, None, 'contexte requis non branché — porte non évaluable, jamais supposée fermée')
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

def _decision_label(packet, score, gates, detail):
    """Cœur du verdict (sans effet de bord) — PARTAGÉ entre decide() et
    l'analyse de perturbation pour interdire toute divergence de règles.
    Renvoie (décision, gate déclenchée ou None, plafonné par verdict canonique)."""
    triggered = [g for g in gates if g['triggered'] is True]
    verdict = ((detail or {}).get('verdict') or '').upper()
    if triggered:
        return ('REFUSER' if score['total'] < 24 else 'ATTENDRE'), triggered[0], False
    if score['total'] >= 28:
        decision = 'ACHETER'
    elif score['total'] >= 24:
        decision = 'ATTENDRE'
    else:
        decision = 'REFUSER'
    capped_canonical = bool(decision == 'ACHETER' and verdict and verdict not in _BULLISH)
    return ('ATTENDRE' if capped_canonical else decision), None, capped_canonical


def perturbation_analysis(base_decision, sym, detail, market=None, events=None,
                          anomaly=None, as_of=None, demo=False, options_ctx=None,
                          portfolio_ctx=None, red_team=None, data_quality_ctx=None,
                          reconciliation_ctx=None):
    """Robustesse MESURÉE (0.5.0) : re-décide sous une liste FIXE de variations
    documentées des entrées et mesure la part des perturbations applicables qui
    laissent la décision inchangée. Déterministe — aucun aléatoire ; une
    perturbation sans donnée d'entrée est NON APPLICABLE, listée, exclue de la
    fraction (jamais comptée stable par défaut)."""
    def _label_for(d2, m2, e2, a2, o2, p2):
        pk = build_packet(sym, d2, market=m2, events=e2, anomaly=a2, as_of=as_of,
                          demo=demo, options_ctx=o2, portfolio_ctx=p2,
                          red_team=red_team, data_quality_ctx=data_quality_ctx,
                          reconciliation_ctx=reconciliation_ctx)
        sc = score40(pk)
        return _decision_label(pk, sc, hard_gates(pk, sc), d2)[0]

    detail = detail or {}
    plan = detail.get('plan') or {}
    results, not_applicable = [], []
    for name in PERTURBATIONS:
        d2, m2, e2, a2 = detail, market, events, anomaly
        o2, p2 = options_ctx, portfolio_ctx
        if name.startswith('score_technique'):
            if detail.get('score') is None:
                not_applicable.append(name)
                continue
            delta = 10 if name.endswith('+10') else -10
            d2 = dict(detail)
            d2['score'] = max(0, min(100, detail['score'] + delta))
        elif name.startswith('rr'):
            if plan.get('rr_res') is None:
                not_applicable.append(name)
                continue
            delta = 0.5 if name.endswith('+0.5') else -0.5
            d2 = dict(detail)
            d2['plan'] = dict(plan)
            d2['plan']['rr_res'] = plan['rr_res'] + delta
        elif name.startswith('regime_confidence'):
            reg = (market or {}).get('regime') or {}
            if reg.get('confidence') is None:
                not_applicable.append(name)
                continue
            delta = 0.2 if name.endswith('+0.2') else -0.2
            m2 = dict(market)
            m2['regime'] = dict(reg)
            m2['regime']['confidence'] = max(0.0, min(1.0, reg['confidence'] + delta))
        elif name == 'sans_market':
            if market is None:
                not_applicable.append(name)
                continue
            m2 = None
        elif name == 'sans_events':
            if events is None:
                not_applicable.append(name)
                continue
            e2 = None
        elif name == 'sans_anomaly':
            if anomaly is None:
                not_applicable.append(name)
                continue
            a2 = None
        elif name == 'sans_options':
            if options_ctx is None:
                not_applicable.append(name)
                continue
            o2 = None
        elif name == 'sans_portfolio':
            if portfolio_ctx is None:
                not_applicable.append(name)
                continue
            p2 = None
        results.append((name, _label_for(d2, m2, e2, a2, o2, p2)))

    flipped = [{'perturbation': n, 'decision': l} for n, l in results
               if l != base_decision]
    n_app = len(results)
    stable = n_app - len(flipped)
    return {'value': (round(stable / n_app, 3) if n_app else None),
            'n_applicable': n_app, 'stable': stable,
            'flipped': flipped, 'not_applicable': not_applicable,
            'basis': ('%d/%d perturbation(s) applicables laissent la décision inchangée '
                      '— liste fixe déterministe' % (stable, n_app)) if n_app else
                     'aucune perturbation applicable (entrées minimales) — robustesse non mesurable'}


def decide(sym, detail, market=None, events=None, anomaly=None, as_of=None,
           demo=False, options_ctx=None, portfolio_ctx=None, red_team=None,
           calibration=None, data_quality_ctx=None, reconciliation_ctx=None, fundamental_ctx=None):
    packet = build_packet(sym, detail, market=market, events=events,
                          anomaly=anomaly, as_of=as_of, demo=demo,
                          options_ctx=options_ctx, portfolio_ctx=portfolio_ctx,
                          red_team=red_team, data_quality_ctx=data_quality_ctx,
                          reconciliation_ctx=reconciliation_ctx, fundamental_ctx=fundamental_ctx)
    score = score40(packet)
    gates = hard_gates(packet, score)
    scen = scenarios(detail)
    audit = list(packet['audit_trail'])
    audit.append({'step': 'score40', 'result': score['total']})
    triggered = [g for g in gates if g['triggered'] is True]
    audit.append({'step': 'hard_gates', 'result': [g['id'] for g in triggered]})

    verdict = ((detail or {}).get('verdict') or '').upper()
    decision, gate_hit, capped_canonical = _decision_label(packet, score, gates, detail)
    if gate_hit is not None:
        capped_by = gate_hit['id']
        main_reason = 'Hard gate %s : %s' % (capped_by, gate_hit['reason'])
    else:
        capped_by = None
        main_reason = 'Score Skyler %d/40 (niveau %s)' % (score['total'], score['level'])
        if capped_canonical:
            # Jamais plus agressif que le verdict canonique existant.
            main_reason += ' — plafonné : le verdict canonique (%s) est prudent' % verdict
            packet['contradictions'].append({'kind': 'skyler_vs_canonical',
                                             'detail': 'Skyler favorable mais verdict canonique %s — décision plafonnée.' % verdict})
    audit.append({'step': 'decision', 'result': decision})

    plan = (detail or {}).get('plan') or {}
    op_state, op_basis = operational_state(decision, gates, plan)
    pert = perturbation_analysis(decision, sym, detail, market=market, events=events,
                                 anomaly=anomaly, as_of=as_of, demo=demo,
                                 options_ctx=options_ctx, portfolio_ctx=portfolio_ctx,
                                 red_team=red_team, data_quality_ctx=data_quality_ctx,
                                 reconciliation_ctx=reconciliation_ctx)
    conf = confidence(packet, score, robustness=pert, calibration=calibration)
    audit.append({'step': 'operational_state', 'result': op_state})
    audit.append({'step': 'perturbation', 'result': pert['value']})
    entry, stop = plan.get('entry'), plan.get('stop')
    max_risk_pct = (round((entry - stop) / entry * 100, 2)
                    if entry and stop is not None and entry > 0 else None)

    dated = sorted([e for e in ((events or {}).get('events') or [])
                    if e.get('dte') is not None], key=lambda e: e['dte'])
    catalyst = ('%s (J-%d)' % (dated[0]['label'], dated[0]['dte'])) if dated else None
    # kind du MÊME événement — source unique, jamais re-parsé depuis le label
    catalyst_kind = (dated[0].get('kind') or None) if dated else None

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

    pctx = packet['contexts']['portfolio']
    sizing = pctx.get('sizing') if pctx.get('available') else None

    return {
        'symbol': sym, 'generator': 'deterministic', 'as_of': as_of,
        'decision': decision, 'capped_by_gate': capped_by,
        'operational_state': op_state, 'operational_state_basis': op_basis,
        'confidence': conf, 'perturbation': pert,
        'red_team': {'complete': bool((packet.get('red_team') or {}).get('complete')),
                     'required': score['level'] in ('S_PLUS', 'S'),
                     'basis': (packet.get('red_team') or {}).get('basis')
                              or 'aucune red-team exécutée — S/S+ impossible sans elle'},
        'sizing': sizing,
        'score': score, 'level': score['level'],
        'gates': gates, 'scenarios': scen,
        'invalidation': stop, 'max_risk_pct': max_risk_pct,
        'catalyst': catalyst, 'catalyst_kind': catalyst_kind,
        'main_reason': main_reason, 'strongest_objection': objection,
        'unknowns': sorted(set(packet['unknowns'] + unknown_gates)),
        'contradictions': packet['contradictions'],
        'audit_trail': audit,
        'note': 'Décision analytique READONLY — jamais un ordre ; Claude peut rédiger, jamais modifier ces chiffres.',
    }


__all__ = ['build_packet', 'score40', 'hard_gates', 'scenarios', 'decide',
           'apply_red_team_rule', 'operational_state', 'confidence',
           'perturbation_analysis', 'PERTURBATIONS',
           'OPERATIONAL_STATES', 'SCHEMA_VERSION', 'ENGINE_VERSION']
