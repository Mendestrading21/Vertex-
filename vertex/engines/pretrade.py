"""vertex/engines/pretrade.py — TICKET PRÉ-TRADE (le « ticket d'ordre », version analyse).

Chez un broker, on saisit un ordre. Chez VERTEX (lecture seule absolue), on saisit
une INTENTION — titre + montant envisagé — et l'assistant vérifie tout ce qu'un
desk vérifierait AVANT d'agir, depuis les données déjà calculées :

  1. Verdict du comité (ACHETER/RENFORCER/ATTENDRE/ÉVITER) pour le titre.
  2. Régime de marché (RISK-ON / NEUTRE / RISK-OFF).
  3. Positionnement dealer (biais + régime GEX) si disponible.
  4. Proximité des résultats (risque événementiel).
  5. CONCENTRATION RÉSULTANTE : le poids du titre dans le book APRÈS l'ajout
     (positions actions valorisées aux prix réels + montant envisagé).
  6. Plan de niveaux : invalidation (stop) définie ? R:R calculable ?
  7. Garde-fou perdants (Constitution §18) : ajouter à une position PERDANTE
     sans confirmation = signalé DÉFAVORABLE.

Verdict global : FAVORABLE / MITIGÉ / DÉFAVORABLE — DESCRIPTIF, jamais un ordre,
jamais un conseil d'exécution. Donnée absente → contrôle « inconnu » honnête.
Fonction pure (aucune I/O).
"""
from __future__ import annotations

OK, WARN, KO, UNKNOWN = 'ok', 'attention', 'defavorable', 'inconnu'


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


def _chk(key, label, status, detail):
    return {'key': key, 'label': label, 'status': status, 'detail': detail}


def build(symbol, amount, *, verdict=None, roro=None, gex_bias=None, gex_regime=None,
          earnings_in_days=None, positions=None, prices_by_sym=None, plan=None):
    """Ticket pré-trade pour `symbol` avec `amount` (montant envisagé, monnaie du compte)."""
    sym = str(symbol or '').upper()
    amt = _num(amount)
    prices_by_sym = prices_by_sym or {}
    checks = []

    # 1. Verdict comité (vérité des verdicts — jamais recalculé ici).
    v = (verdict or '').upper() or None
    if v in ('ACHETER', 'RENFORCER'):
        checks.append(_chk('verdict', 'Verdict du comité', OK, '%s — le comité valide le dossier.' % v))
    elif v == 'ATTENDRE':
        checks.append(_chk('verdict', 'Verdict du comité', WARN, 'ATTENDRE — le comité ne valide pas (encore) ce dossier.'))
    elif v in ('EVITER', 'ÉVITER', 'ALLEGER', 'ALLÉGER', 'VENDRE'):
        checks.append(_chk('verdict', 'Verdict du comité', KO, '%s — le comité est contre.' % v))
    else:
        checks.append(_chk('verdict', 'Verdict du comité', UNKNOWN, 'Titre hors du scan courant — aucun verdict.'))

    # 2. Régime de marché.
    r = (roro or '').upper() or None
    if r == 'RISK-ON':
        checks.append(_chk('regime', 'Régime de marché', OK, 'RISK-ON — environnement porteur.'))
    elif r == 'RISK-OFF':
        checks.append(_chk('regime', 'Régime de marché', KO, 'RISK-OFF — risque neuf déconseillé par le régime.'))
    elif r:
        checks.append(_chk('regime', 'Régime de marché', WARN, '%s — environnement sans conviction.' % r))
    else:
        checks.append(_chk('regime', 'Régime de marché', UNKNOWN, 'Régime indisponible.'))

    # 3. Positionnement dealer (GEX) — optionnel, réel seulement.
    if gex_bias:
        st = OK if gex_bias == 'haussier' else KO if gex_bias == 'baissier' else WARN
        extra = ' Régime accélérateur : mouvements amplifiés.' if gex_regime == 'accelerateur' else ''
        if gex_regime == 'accelerateur' and st == OK:
            st = WARN
        checks.append(_chk('gex', 'Positionnement dealer', st,
                           'Biais %s.%s' % (gex_bias, extra)))
    else:
        checks.append(_chk('gex', 'Positionnement dealer', UNKNOWN,
                           'Profil GEX indisponible pour ce titre.'))

    # 4. Résultats imminents.
    e = earnings_in_days if isinstance(earnings_in_days, (int, float)) and not isinstance(earnings_in_days, bool) else None
    if e is not None and 0 <= e <= 7:
        checks.append(_chk('earnings', 'Résultats', KO if e <= 2 else WARN,
                           'Résultats J-%d — gap possible, dimensionner en conséquence.' % int(e)))
    elif e is not None:
        checks.append(_chk('earnings', 'Résultats', OK, 'Prochains résultats dans %d j.' % int(e)))
    else:
        checks.append(_chk('earnings', 'Résultats', UNKNOWN, 'Date de résultats inconnue.'))

    # 5. Concentration résultante (positions actions aux prix réels + montant envisagé).
    existing_sym = 0.0
    book = 0.0
    losing_existing = None
    for t in (positions or []):
        if not isinstance(t, dict) or str(t.get('type') or 'STK').upper() != 'STK':
            continue
        qty, cost = _num(t.get('qty')), _num(t.get('cost'))
        px = _num(prices_by_sym.get(str(t.get('sym') or '').upper()))
        val = (qty * px) if (qty and px) else (cost or 0.0)     # repli honnête : coût déclaré
        book += val
        if str(t.get('sym') or '').upper() == sym:
            existing_sym += val
            # 7. garde-fou perdants : position existante en perte (prix réel < prix de revient)
            if qty and px and cost and qty > 0:
                losing_existing = (px < cost / qty)
    if amt is not None and amt > 0:
        total_after = book + amt
        weight = 100 * (existing_sym + amt) / total_after if total_after > 0 else None
        if weight is not None:
            st = KO if weight > 25 else WARN if weight > 15 else OK
            checks.append(_chk('concentration', 'Concentration résultante', st,
                               '%s pèserait %.0f %% du book après l\'ajout (%s).'
                               % (sym, weight,
                                  'trop concentré' if st == KO else 'surveiller' if st == WARN else 'raisonnable')))
        else:
            checks.append(_chk('concentration', 'Concentration résultante', UNKNOWN, 'Book vide — poids non calculable.'))
    else:
        checks.append(_chk('concentration', 'Concentration résultante', UNKNOWN, 'Montant envisagé manquant.'))

    # 6. Plan de niveaux (invalidation + R:R) — depuis le plan moteur réel.
    p = plan or {}
    stop, tp1 = _num(p.get('stop')), _num(p.get('tp1'))
    px_now = _num(prices_by_sym.get(sym))
    if stop and px_now and px_now > stop:
        if tp1 and tp1 > px_now:
            rr = (tp1 - px_now) / (px_now - stop)
            st = OK if rr >= 2 else WARN
            checks.append(_chk('plan', 'Plan de niveaux', st,
                               'Invalidation %.2f · TP1 %.2f · R:R %.1f:1%s.'
                               % (stop, tp1, rr, '' if rr >= 2 else ' (< 2:1 — Constitution)')))
        else:
            checks.append(_chk('plan', 'Plan de niveaux', WARN,
                               'Invalidation %.2f définie, objectif manquant — R:R non calculable.' % stop))
    else:
        checks.append(_chk('plan', 'Plan de niveaux', WARN,
                           'Aucune invalidation définie — un trade sans stop n\'a pas de plan.'))

    # 7. Garde-fou perdants (Constitution §18).
    if losing_existing is True:
        checks.append(_chk('losers', 'Garde-fou perdants (§18)', KO,
                           'Position existante EN PERTE sur %s — renforcer un perdant exige une '
                           'confirmation positive explicite du marché.' % sym))
    elif losing_existing is False:
        checks.append(_chk('losers', 'Garde-fou perdants (§18)', OK,
                           'La position existante sur %s est gagnante.' % sym))

    # Verdict global.
    statuses = [c['status'] for c in checks]
    if KO in statuses:
        overall, tone = 'DÉFAVORABLE', 'ko'
    elif WARN in statuses:
        overall, tone = 'MITIGÉ', 'warn'
    elif all(s == UNKNOWN for s in statuses):
        overall, tone = 'INCONNU', 'unknown'
    else:
        overall, tone = 'FAVORABLE', 'ok'
    n_ko = statuses.count(KO)
    n_warn = statuses.count(WARN)
    narrative = ('Vérification pré-trade %s : %d contrôle(s) défavorable(s), %d à surveiller, '
                 'sur %d. Rapport DESCRIPTIF — Vertex ne passe jamais d\'ordre et ceci '
                 'n\'est pas un conseil d\'exécution ; la décision et la discipline restent les tiennes.'
                 % (sym, n_ko, n_warn, len(checks)))

    return {
        'symbol': sym, 'amount': amt,
        'overall': overall, 'tone': tone,
        'checks': checks, 'narrative': narrative,
        'generator': 'deterministic',
    }


__all__ = ['build']
