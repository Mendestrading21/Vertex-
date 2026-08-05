"""vertex/engines/red_team.py — PRODUCTEUR RED-TEAM DÉTERMINISTE (LOT 14).

ADVERSARIAL_COMMITTEE §8 : tout dossier S ou S+ doit subir une passe red-team
répondant à 10 questions minimum — « une note S+ sans red-team complétée est
invalide ». Ce module PRODUIT cette passe depuis les données réelles du
SkylerPacket :

  - chaque question reçoit une réponse FONDÉE (citant les données, avec niveau
    de preuve F1/F2) ou reste UNANSWERED avec la raison exacte — jamais une
    réponse inventée pour compléter la revue ;
  - `complete=True` UNIQUEMENT si les 10 questions ont une réponse fondée ;
  - la revue est déterministe (même packet → même revue) et versionnée.

La règle de plafonnement (skyler_core.apply_red_team_rule) reste inchangée :
elle consomme `complete`. Lecture seule, aucun ordre.
"""
from __future__ import annotations

import math

# 1.1.0 : Q05/Q08 chiffrées par repricing Black-Scholes canonique quand le
# candidat est complet (F3, modèle et hypothèses étiquetés) — fallback
# qualitatif F2 sinon, UNANSWERED sans IV (inchangé).
RED_TEAM_VERSION = '1.1.0'

_REPRICE_RATE = 0.045    # taux fixe documenté de la revue (hypothèse listée)


def _fin(x):
    return (isinstance(x, (int, float)) and not isinstance(x, bool)
            and math.isfinite(x))


def _reprice_inputs(best):
    """Entrées de repricing VALIDES ou None — NaN/négatifs/DTE nul refusés,
    jamais chiffré sur une entrée douteuse."""
    b = best or {}
    spot, strike, dte, iv = b.get('spot'), b.get('strike'), b.get('dte'), b.get('iv')
    right = 'C' if str(b.get('type') or 'CALL').upper().startswith('C') else 'P'
    if not (_fin(spot) and spot > 0 and _fin(strike) and strike > 0
            and _fin(dte) and dte > 0 and _fin(iv) and 0 < iv < 4):
        return None
    return {'spot': float(spot), 'strike': float(strike),
            't_years': float(dte) / 365.0, 'iv': float(iv), 'right': right}

_QUESTIONS = (
    ('Q01', 'Qu’est-ce qui est déjà dans le prix ?'),
    ('Q02', 'Quel chiffre peut être trompeur ?'),
    ('Q03', 'Quelle hypothèse unique porte trop de poids ?'),
    ('Q04', 'Que se passe-t-il si le catalyseur est retardé de 90 jours ?'),
    ('Q05', 'Que se passe-t-il si l’IV baisse de 10 points ?'),
    ('Q06', 'Que se passe-t-il si le marché passe risk-off ?'),
    ('Q07', 'Le portefeuille possède-t-il déjà la même exposition cachée ?'),
    ('Q08', 'Pourquoi l’option est-elle meilleure que l’action ?'),
    ('Q09', 'Quel est le chemin plausible vers la perte maximale ?'),
    ('Q10', 'Quelle preuve invalide immédiatement la note S/S+ ?'),
)


def _q(qid, question, status, answer=None, evidence_level=None, reason=None):
    out = {'id': qid, 'question': question, 'status': status}
    if status == 'ANSWERED':
        out['answer'] = answer
        out['evidence_level'] = evidence_level
    else:
        out['reason'] = reason
    return out


def review(packet, score):
    """Passe red-team déterministe sur un packet + score. Répond seulement avec
    les données présentes — l'absence est dite, jamais comblée."""
    ctx = (packet or {}).get('contexts') or {}
    tech = ctx.get('technical') or {}
    tech = tech if tech.get('available') else {}
    plan = tech.get('plan') or {}
    market = ctx.get('market') or {}
    reg = market.get('regime') or {}
    cat = ctx.get('catalysts') or {}
    ano = ctx.get('anomalies') or {}
    ano = ano if ano.get('available', True) and 'events' in ano else {}
    octx = ctx.get('options') or {}
    octx = octx if octx.get('available') else {}
    pctx = ctx.get('portfolio') or {}
    pctx = pctx if pctx.get('available') else {}
    sc = score or {}
    blocks = sc.get('blocks') or {}
    qs = []
    q = dict(_QUESTIONS)

    # Q01 — déjà dans le prix : position technique réelle (RSI, extrême de fenêtre).
    rsi = tech.get('rsi')
    extreme = ano.get('extreme')
    if rsi is not None or extreme:
        parts = []
        if rsi is not None:
            parts.append('RSI %.0f' % rsi)
        if extreme:
            parts.append('clôture au plus %s de sa fenêtre' % ('HAUT' if extreme == 'high' else 'BAS'))
        qs.append(_q('Q01', q['Q01'], 'ANSWERED',
                     'Le prix intègre déjà : %s — plus la lecture est tendue, plus '
                     'l’avantage restant est faible.' % ' ; '.join(parts), 'F2'))
    else:
        qs.append(_q('Q01', q['Q01'], 'UNANSWERED',
                     reason='ni RSI ni position dans la fenêtre disponibles — non évaluable'))

    # Q02 — chiffre trompeur : état réel des données (blocs insuffisants, mode).
    insuf = sc.get('insufficient_blocks') or []
    demo = bool((packet or {}).get('demo'))
    qs.append(_q('Q02', q['Q02'], 'ANSWERED',
                 ('Blocs insuffisants : %s%s — tout chiffre issu de ces blocs vaut 0, '
                  'jamais une estimation.' % (', '.join(insuf) if insuf else 'aucun',
                                              ' ; MODE DÉMO étiqueté' if demo else '')),
                 'F1'))

    # Q03 — hypothèse dominante : répartition réelle des points de score.
    scored = {n: b for n, b in blocks.items() if (b.get('points') or 0) > 0}
    if not blocks:
        qs.append(_q('Q03', q['Q03'], 'UNANSWERED', reason='aucun bloc de score fourni'))
    elif not scored:
        qs.append(_q('Q03', q['Q03'], 'ANSWERED',
                     'Aucun bloc ne porte de point — pas d’hypothèse dominante, le dossier est vide.', 'F2'))
    else:
        total = sum(b.get('points') or 0 for b in scored.values())
        top = max(scored, key=lambda n: scored[n].get('points') or 0)
        share = (scored[top].get('points') or 0) / total * 100 if total else 0
        qs.append(_q('Q03', q['Q03'], 'ANSWERED',
                     'Le bloc %s porte %d/%d points (%.0f %%)%s.' %
                     (top, scored[top].get('points') or 0, total, share,
                      ' — DÉPENDANCE À UNE HYPOTHÈSE UNIQUE' if len(scored) == 1 else ''),
                     'F2'))

    # Q04 — catalyseur retardé : événements datés réels.
    dated = sorted([e for e in (cat.get('events') or []) if e.get('dte') is not None],
                   key=lambda e: e['dte'])
    if cat.get('available') is False:
        qs.append(_q('Q04', q['Q04'], 'UNANSWERED', reason='timeline d’événements non fournie'))
    elif dated:
        e = dated[0]
        qs.append(_q('Q04', q['Q04'], 'ANSWERED',
                     'Catalyseur le plus proche : « %s » (J-%d). Retardé de 90 j, il sort '
                     'de la fenêtre des 90 jours — la thèse perd son déclencheur daté et '
                     'le theta travaille contre toute option courte.' % (e.get('label'), e['dte']),
                     'F1'))
    else:
        qs.append(_q('Q04', q['Q04'], 'ANSWERED',
                     'Aucun catalyseur daté connu — la thèse ne dépend d’aucune date ; '
                     'un retard ne change rien, mais rien ne force non plus le mouvement.', 'F1'))

    # Q05 — IV −10 pts : CHIFFRÉ par repricing BS canonique quand le candidat
    # est complet (F3, modèle + hypothèses) ; qualitatif F2 sinon ; sans IV,
    # UNANSWERED — jamais chiffré sur une entrée douteuse.
    best_c = octx.get('best') or {}
    iv = best_c.get('iv')
    rp = _reprice_inputs(best_c)
    if iv is None or not _fin(iv):
        qs.append(_q('Q05', q['Q05'], 'UNANSWERED',
                     reason='aucune IV réelle disponible (OptionsContext absent ou sans IV) — impact non calculable'))
    elif rp is not None:
        from vertex.options.scenario_pricer import bs_price
        v_now = bs_price(rp['spot'], rp['strike'], rp['t_years'], rp['iv'],
                         _REPRICE_RATE, rp['right'])
        v_down = bs_price(rp['spot'], rp['strike'], rp['t_years'],
                          max(0.01, rp['iv'] - 0.10), _REPRICE_RATE, rp['right'])
        if v_now > 0 and math.isfinite(v_now) and math.isfinite(v_down):
            impact = (v_down / v_now - 1) * 100
            item = _q('Q05', q['Q05'], 'ANSWERED',
                      'IV %.0f %% → %.0f %% : valeur théorique du candidat %+.1f %% '
                      '(spot et échéance inchangés). Black-Scholes européen, taux fixe '
                      '%.1f %%, dividende non modélisé — ESTIMATION, jamais un prix broker.'
                      % (rp['iv'] * 100, max(0.01, rp['iv'] - 0.10) * 100, impact,
                         _REPRICE_RATE * 100), 'F3')
            item['model'] = 'black_scholes_european'
            qs.append(item)
        else:
            qs.append(_q('Q05', q['Q05'], 'ANSWERED',
                         'IV du meilleur candidat : %.0f %% — une contraction de 10 points '
                         'réduit la valeur extrinsèque (vega) ; le contrat doit survivre à ce '
                         'scénario sans que la thèse sous-jacente change.' % (iv * 100 if iv < 3 else iv),
                         'F2'))
    else:
        qs.append(_q('Q05', q['Q05'], 'ANSWERED',
                     'IV du meilleur candidat : %.0f %% — une contraction de 10 points '
                     'réduit la valeur extrinsèque (vega) ; le contrat doit survivre à ce '
                     'scénario sans que la thèse sous-jacente change.' % (iv * 100 if iv < 3 else iv),
                     'F2'))

    # Q06 — marché risk-off : exige un régime connu.
    label = reg.get('label')
    if not label or label == 'UNKNOWN':
        qs.append(_q('Q06', q['Q06'], 'UNANSWERED',
                     reason='régime de marché inconnu — comportement en risk-off non évaluable'))
    else:
        allowed = (reg.get('adjustments') or {}).get('new_risk_allowed')
        qs.append(_q('Q06', q['Q06'], 'ANSWERED',
                     'Régime actuel %s (risque neuf %s). En passage risk-off, le régime '
                     'bloque le risque neuf et la position existante doit tenir son '
                     'invalidation — aucune moyenne à la baisse n’est autorisée.' %
                     (label, 'autorisé' if allowed else 'déjà bloqué'), 'F2'))

    # Q07 — exposition cachée : exige le portefeuille réel.
    if not pctx:
        qs.append(_q('Q07', q['Q07'], 'UNANSWERED',
                     reason='portefeuille non fourni — exposition cachée non évaluable'))
    else:
        qs.append(_q('Q07', q['Q07'], 'ANSWERED',
                     '%d position(s), poids max %s %.1f %%, HHI %.2f — toute nouvelle ligne '
                     'corrélée au titre dominant concentre davantage.' %
                     (pctx.get('n_positions') or 0, pctx.get('top_symbol') or 'n/d',
                      pctx.get('top_weight_pct') or 0.0, pctx.get('hhi') or 0.0), 'F1'))

    # Q08 — option vs action : GRILLE spot pessimiste/probable/exceptionnel ×
    # IV −10/0/+10 depuis les niveaux RÉELS du plan quand tout est disponible
    # (F3) ; qualitatif F2 sinon ; sans candidat noté, UNANSWERED.
    best = octx.get('best') or {}
    targets = {'stop': plan.get('stop'), 'TP2': plan.get('tp2'), 'TP3': plan.get('tp3')}
    grid_ok = (rp is not None and all(_fin(v) and v > 0 for v in targets.values()))
    if best.get('quality') is None:
        qs.append(_q('Q08', q['Q08'], 'UNANSWERED',
                     reason='aucun candidat option noté — la comparaison action/option n’a pas de base'))
    elif grid_ok:
        from vertex.options.scenario_pricer import bs_price
        v_now = bs_price(rp['spot'], rp['strike'], rp['t_years'], rp['iv'],
                         _REPRICE_RATE, rp['right'])
        if v_now > 0 and math.isfinite(v_now):
            cells = []
            for name, tgt in targets.items():
                for div_lbl, div in (('IV−10', -0.10), ('IV0', 0.0), ('IV+10', 0.10)):
                    v = bs_price(float(tgt), rp['strike'], rp['t_years'],
                                 max(0.01, rp['iv'] + div), _REPRICE_RATE, rp['right'])
                    cells.append('%s/%s %+.0f %%' % (name, div_lbl,
                                                     (v / v_now - 1) * 100)
                                 if math.isfinite(v) else '%s/%s n/d' % (name, div_lbl))
            stock_tp2 = (targets['TP2'] / rp['spot'] - 1) * 100
            opt_tp2 = (bs_price(targets['TP2'], rp['strike'], rp['t_years'],
                                rp['iv'], _REPRICE_RATE, rp['right']) / v_now - 1) * 100
            item = _q('Q08', q['Q08'], 'ANSWERED',
                      'Grille spot × IV (temps inchangé, theta non consommé) : %s. '
                      'Au TP2, option %+.0f %% vs action %+.0f %% — la convexité %s '
                      'l’action sur le scénario probable. Black-Scholes européen, taux '
                      'fixe %.1f %% — ESTIMATION.'
                      % (' · '.join(cells), opt_tp2, stock_tp2,
                         'bat' if opt_tp2 > stock_tp2 else 'ne bat pas',
                         _REPRICE_RATE * 100), 'F3')
            item['model'] = 'black_scholes_european'
            qs.append(item)
        else:
            qs.append(_q('Q08', q['Q08'], 'ANSWERED',
                         'Meilleur candidat %s qualité %s/100 — l’option ne bat l’action que si '
                         'la convexité paie son theta et son spread ; sinon l’action reste le '
                         'véhicule par défaut.' % (octx.get('universe') or 'n/d', best.get('quality')),
                         'F2'))
    else:
        qs.append(_q('Q08', q['Q08'], 'ANSWERED',
                     'Meilleur candidat %s qualité %s/100 — l’option ne bat l’action que si '
                     'la convexité paie son theta et son spread ; sinon l’action reste le '
                     'véhicule par défaut.' % (octx.get('universe') or 'n/d', best.get('quality')),
                     'F2'))

    # Q09 — chemin vers la perte maximale : exige une invalidation réelle.
    entry, stop = plan.get('entry'), plan.get('stop')
    if entry is None or stop is None:
        qs.append(_q('Q09', q['Q09'], 'UNANSWERED',
                     reason='plan sans stop technique — le chemin de perte n’est pas borné'))
    else:
        loss = (entry - stop) / entry * 100 if entry else 0.0
        qs.append(_q('Q09', q['Q09'], 'ANSWERED',
                     'Cassure du stop %.2f depuis l’entrée %.2f = perte action %.1f %% ; '
                     'gap au travers du stop = perte supérieure possible — dit, pas masqué.' %
                     (stop, entry, loss), 'F2'))

    # Q10 — preuve d'invalidation immédiate : exige le stop + gates.
    if stop is None:
        qs.append(_q('Q10', q['Q10'], 'UNANSWERED',
                     reason='aucune invalidation définie — rien ne peut invalider proprement la note'))
    else:
        qs.append(_q('Q10', q['Q10'], 'ANSWERED',
                     'Clôture sous %.2f (invalidation technique) ou activation d’une hard '
                     'gate données/thèse invalide immédiatement la note — la décision '
                     'repasse en réévaluation.' % stop, 'F1'))

    answered = sum(1 for x in qs if x['status'] == 'ANSWERED')
    return {'version': RED_TEAM_VERSION, 'generator': 'deterministic',
            'questions': qs, 'answered': answered, 'complete': answered == 10,
            'basis': ('revue red-team %d/10 questions fondées sur les données réelles — '
                      '%s' % (answered, 'COMPLÈTE' if answered == 10 else
                              'incomplète : les questions sans données restent ouvertes, jamais comblées'))}


__all__ = ['review', 'RED_TEAM_VERSION']
