"""vertex/options/dealer_synthesis.py — SYNTHÈSE « POSITIONNEMENT DEALER » (thèse).

Assemble une lecture lisible du positionnement d'options d'un sous-jacent à partir
du profil GEX (gex.compute) et du flux notable (flow.analyze), plus le contexte
d'événement (résultats). Produit la « thèse » façon desk : biais directionnel,
régime de volatilité, zone d'aimant gamma (mur call / mur put), horizon, risque
événementiel — et un récit en français.

HONNÊTETÉ (invariant produit) :
- la « zone-cible » est le MUR GAMMA (concentration d'exposition), présenté comme un
  AIMANT de positionnement, JAMAIS comme une prévision de prix ;
- déterministe (aucun modèle génératif ici), fondé uniquement sur les nombres réels ;
- donnée absente → champ None + récit qui le dit ; jamais de certitude inventée ;
- lecture seule, aucun ordre.
"""
from __future__ import annotations


def _pct_above(gex):
    """Part (0-100) du |net GEX| situé au-dessus du spot — mesure de concentration."""
    a = abs(gex.get('gex_above_spot') or 0.0)
    b = abs(gex.get('gex_below_spot') or 0.0)
    tot = a + b
    return round(100 * a / tot) if tot else None


def build(gex, flow=None, *, earnings_in_days=None, symbol=None):
    """Thèse de positionnement dealer. `gex` = sortie de gex.compute ; `flow` = flow.analyze."""
    gex = gex or {}
    flow = flow or {}
    sym = symbol or gex.get('symbol')
    spot = gex.get('spot')

    if gex.get('empty') or spot is None:
        return {
            'symbol': sym, 'empty': True, 'bias': None, 'regime': None,
            'magnet': None, 'support': None, 'horizon_dte': None,
            'earnings_risk': None, 'headline': None, 'narrative': None,
            'evidence': [], 'generator': 'deterministic',
            'reason': gex.get('reason') or 'profil GEX indisponible (données réelles absentes)',
        }

    net = gex.get('net_gex_total')
    regime = gex.get('regime')            # 'stabilisant' | 'accelerateur' | 'neutre'
    bias = gex.get('bias')                # 'haussier' | 'baissier' | 'neutre'
    call_wall = gex.get('call_wall')
    put_wall = gex.get('put_wall')
    flip = gex.get('zero_gamma')
    conc = _pct_above(gex)

    # Aimant = mur du côté du biais (haussier → mur call au-dessus ; baissier → mur put).
    magnet = call_wall if bias == 'haussier' else put_wall if bias == 'baissier' else None
    support = put_wall

    evidence = []
    if net is not None:
        sign = 'positif' if net > 0 else 'négatif' if net < 0 else 'neutre'
        evidence.append('Net GEX %s (%s)' % (sign,
                        'dealers longs gamma → volatilité amortie' if net > 0 else
                        'dealers courts gamma → mouvements amplifiés' if net < 0 else 'équilibré'))
    if conc is not None:
        evidence.append('%d %% du GEX concentré au-dessus du spot' % conc)
    if call_wall is not None:
        evidence.append('Mur call (aimant haussier) à %s' % _f(call_wall))
    if put_wall is not None:
        evidence.append('Mur put (support) à %s' % _f(put_wall))
    if flip is not None:
        evidence.append('Bascule zero-gamma ≈ %s' % _f(flip))
    if not flow.get('empty'):
        sk = flow.get('skew')
        if sk:
            evidence.append('Flux notable orienté %s (%s %% du premium)' % (
                sk, flow.get('call_pct')))

    # Horizon : DTE du plus gros flux, sinon None.
    horizon = None
    fc = (flow.get('contracts') or [])
    if fc and fc[0].get('dte') is not None:
        horizon = fc[0]['dte']

    # Risque événementiel (résultats) — réel si fourni.
    earnings_risk = None
    if isinstance(earnings_in_days, (int, float)) and not isinstance(earnings_in_days, bool):
        if earnings_in_days >= 0:
            earnings_risk = ('imminent (résultats J-%d)' % int(earnings_in_days)
                             if earnings_in_days <= 10 else 'résultats dans %d j' % int(earnings_in_days))

    headline = _headline(bias, regime, sym)
    narrative = _narrative(sym, spot, bias, regime, net, conc, magnet, support,
                           flip, flow, earnings_risk)

    return {
        'symbol': sym, 'empty': False, 'spot': spot,
        'bias': bias, 'regime': regime,
        'magnet': magnet, 'support': support, 'zero_gamma': flip,
        'horizon_dte': horizon, 'earnings_risk': earnings_risk,
        'headline': headline, 'narrative': narrative,
        'evidence': evidence, 'generator': 'deterministic',
    }


def _f(x):
    try:
        return ('%.2f' % float(x)).rstrip('0').rstrip('.')
    except (TypeError, ValueError):
        return str(x)


def _headline(bias, regime, sym):
    b = {'haussier': 'Biais haussier', 'baissier': 'Biais baissier'}.get(bias, 'Biais neutre')
    r = {'stabilisant': 'régime stabilisant (pinning)',
         'accelerateur': 'régime accélérateur (cassures amplifiées)',
         'neutre': 'régime neutre'}.get(regime, '')
    return '%s%s — %s' % (b, ' ' + sym if sym else '', r) if r else b


def _narrative(sym, spot, bias, regime, net, conc, magnet, support, flip, flow, earnings_risk):
    """Récit en français, fondé uniquement sur les nombres réels ci-dessus."""
    s = sym or 'le sous-jacent'
    parts = []
    if net is not None and net > 0:
        parts.append("Le gamma dealer net est positif : les teneurs de marché sont "
                     "longs gamma et tendent à amortir la volatilité (effet d'aimant / pinning).")
    elif net is not None and net < 0:
        parts.append("Le gamma dealer net est négatif : les teneurs de marché sont courts "
                     "gamma et tendent à amplifier les mouvements (risque de cassure).")
    if conc is not None:
        side = 'au-dessus' if conc >= 50 else 'sous'
        parts.append("L'exposition est concentrée %s du cours (%d %%), ce qui oriente le "
                     "biais court terme %s." % (side, conc if conc >= 50 else 100 - conc,
                                                'à la hausse' if conc >= 50 else 'à la baisse'))
    if magnet is not None:
        parts.append("Zone d'aimant gamma : %s (concentration d'exposition — un niveau "
                     "que le positionnement tend à attirer, PAS une prévision de prix)." % _f(magnet))
    if support is not None:
        parts.append("Support de positionnement (mur put) : %s." % _f(support))
    if flip is not None:
        parts.append("Bascule zero-gamma ≈ %s : au-dessus le régime est stabilisant, "
                     "en dessous il devient accélérateur." % _f(flip))
    if flow and not flow.get('empty') and flow.get('skew'):
        parts.append("Le flux notable du cycle penche %s (%d %% du premium négocié)."
                     % (flow.get('skew'), flow.get('call_pct') or 0))
    if earnings_risk:
        parts.append("Risque événementiel %s : les résultats ajoutent de l'incertitude, "
                     "à intégrer dans le dimensionnement." % earnings_risk)
    parts.append("Positionnement d'options — lecture seule, aucune recommandation d'ordre ; "
                 "à confirmer par le sous-jacent et la discipline de risque.")
    return ' '.join(parts)


__all__ = ['build']
