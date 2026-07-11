"""vertex.research.institutional.quality_growth — filtre qualité-croissance (§23)."""
from __future__ import annotations


def quality_growth_profile(f: dict) -> dict:
    """f : {'revenue_growth','margin','roe','fcf_margin','debt_to_equity',
    'dilution_pct','revenue_growth_prev'} → profil + drapeaux."""
    flags, strengths = [], []
    g = f.get('revenue_growth')
    if g is not None:
        if g >= 0.20:
            strengths.append(f'hypercroissance ({g:.0%})')
        elif g >= 0.10:
            strengths.append(f'croissance solide ({g:.0%})')
        elif g < 0:
            flags.append('chiffre d’affaires en contraction')
        gp = f.get('revenue_growth_prev')
        if gp is not None and g < gp - 0.08:
            flags.append('décélération marquée de la croissance')
    m = f.get('margin')
    if m is not None:
        (strengths if m >= 0.20 else flags).append(
            f'marge {"élevée" if m >= 0.20 else "faible"} ({m:.0%})' if m >= 0.20 or m < 0.08
            else f'marge correcte ({m:.0%})')
    roe = f.get('roe')
    if roe is not None and roe >= 0.20:
        strengths.append(f'ROE {roe:.0%}')
    fcf = f.get('fcf_margin')
    if fcf is not None and fcf < 0:
        flags.append('cash-flow libre négatif')
    de = f.get('debt_to_equity')
    if de is not None and de > 2.0:
        flags.append(f'levier élevé (D/E {de:.1f})')
    dil = f.get('dilution_pct')
    if dil is not None and dil > 4:
        flags.append(f'dilution {dil:.1f}%/an')
    strengths = [s for s in strengths if 'correcte' not in s]
    profile = 'QUALITY_GROWTH' if len(strengths) >= 2 and not flags else \
              'GROWTH_WITH_RISKS' if strengths and flags else \
              'QUALITY_ISSUES' if flags else 'NEUTRAL'
    return {'profile': profile, 'strengths': strengths, 'flags': flags}
