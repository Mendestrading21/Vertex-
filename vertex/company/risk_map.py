"""vertex.company.risk_map — carte des risques d'entreprise (§24).

Classe les risques d'un dossier (valorisation, financier, croissance,
concurrence, exécution, événementiel, concentration) en niveau × probabilité ×
impact, à partir de données RÉELLES (fundamentals + médianes sectorielles).
Donnée absente → niveau INCONNU (jamais fabriqué). Pur et testable.
"""
from __future__ import annotations

LOW, MED, HIGH = 'FAIBLE', 'MODÉRÉ', 'ÉLEVÉ'
UNKNOWN = 'INCONNU'
_ORDER = {LOW: 1, MED: 2, HIGH: 3, UNKNOWN: 0}


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _risk(category, level, *, prob, impact, note, source='fundamentals'):
    return {'category': category, 'level': level, 'probability': prob,
            'impact': impact, 'note': note, 'source': source,
            'known': level != UNKNOWN}


def _valuation(fu, med):
    pe = _num(fu.get('pe'))
    mpe = _num((med or {}).get('median_pe'))
    if pe is None or mpe is None or mpe <= 0:
        return _risk('Valorisation', UNKNOWN, prob=None, impact=HIGH,
                     note='P/E ou médiane sectorielle indisponible.')
    ratio = pe / mpe
    if ratio >= 1.6:
        return _risk('Valorisation', HIGH, prob='HIGH', impact=HIGH,
                     note='P/E %.0f vs médiane %.0f (×%.1f) — prime de valorisation élevée.' % (pe, mpe, ratio))
    if ratio >= 1.2:
        return _risk('Valorisation', MED, prob='MED', impact=MED,
                     note='P/E %.0f légèrement au-dessus de la médiane (×%.1f).' % (pe, ratio))
    return _risk('Valorisation', LOW, prob='LOW', impact=MED,
                 note='P/E %.0f en ligne/décoté vs médiane %.0f.' % (pe, mpe))


def _financial(fu):
    dte = _num(fu.get('debt_to_ebitda'))
    if dte is None:
        return _risk('Financier / dette', UNKNOWN, prob=None, impact=HIGH,
                     note='Dette/EBITDA indisponible.')
    if dte >= 3.5:
        return _risk('Financier / dette', HIGH, prob='HIGH', impact=HIGH,
                     note='Dette/EBITDA %.1f× — levier élevé, sensibilité aux taux.' % dte)
    if dte >= 2:
        return _risk('Financier / dette', MED, prob='MED', impact=MED,
                     note='Dette/EBITDA %.1f× — levier modéré.' % dte)
    return _risk('Financier / dette', LOW, prob='LOW', impact=MED,
                 note='Bilan sain (Dette/EBITDA %.1f×).' % dte)


def _growth(fu):
    rg = _num(fu.get('rev_growth'))
    if rg is None:
        return _risk('Croissance', UNKNOWN, prob=None, impact=MED,
                     note='Croissance du chiffre d\'affaires indisponible.')
    if rg < 0:
        return _risk('Croissance', HIGH, prob='HIGH', impact=HIGH,
                     note='Chiffre d\'affaires en contraction (%.0f %%).' % rg)
    if rg < 8:
        return _risk('Croissance', MED, prob='MED', impact=MED,
                     note='Croissance molle (%.0f %%) — thèse growth fragile.' % rg)
    return _risk('Croissance', LOW, prob='LOW', impact=MED,
                 note='Croissance soutenue (%.0f %%).' % rg)


def _execution(fu):
    margin = _num(fu.get('margin'))
    eps = _num(fu.get('eps_growth'))
    if margin is None and eps is None:
        return _risk('Exécution', UNKNOWN, prob=None, impact=MED,
                     note='Marge et croissance BPA indisponibles.')
    if (margin is not None and margin < 5) or (eps is not None and eps < 0):
        return _risk('Exécution', HIGH, prob='MED', impact=HIGH,
                     note='Rentabilité sous pression (marge %s, BPA %s).'
                     % (('%.0f %%' % margin) if margin is not None else 'n/d',
                        ('%.0f %%' % eps) if eps is not None else 'n/d'))
    return _risk('Exécution', LOW, prob='LOW', impact=MED,
                 note='Exécution opérationnelle correcte.')


def _competition(comp):
    moat = str((comp or {}).get('moat') or '').lower()
    if not moat:
        return _risk('Concurrence', UNKNOWN, prob=None, impact=MED,
                     note='Avantage concurrentiel (moat) non renseigné.', source='profil')
    weak = any(w in moat for w in ('faible', 'aucun', 'limité', 'narrow', 'none', 'low'))
    if weak:
        return _risk('Concurrence', HIGH, prob='MED', impact=HIGH,
                     note='Barrières à l\'entrée jugées faibles.', source='profil')
    return _risk('Concurrence', LOW, prob='LOW', impact=MED,
                 note='Avantage concurrentiel jugé solide.', source='profil')


def _event(fu):
    ed = _num(fu.get('earnings_in_days'))
    if ed is None:
        ed_raw = fu.get('earnings_date')
        return _risk('Événementiel (earnings)', UNKNOWN if ed_raw is None else MED,
                     prob=None if ed_raw is None else 'MED', impact=HIGH,
                     note=('Date de résultats : %s.' % ed_raw) if ed_raw
                     else 'Date de résultats inconnue.', source='calendrier')
    if 0 <= ed <= 7:
        return _risk('Événementiel (earnings)', HIGH, prob='HIGH', impact=HIGH,
                     note='Résultats dans %d j — risque de gap/IV crush.' % int(ed), source='calendrier')
    if 0 <= ed <= 21:
        return _risk('Événementiel (earnings)', MED, prob='MED', impact=HIGH,
                     note='Résultats dans %d j — à intégrer au timing.' % int(ed), source='calendrier')
    return _risk('Événementiel (earnings)', LOW, prob='LOW', impact=MED,
                 note='Résultats éloignés (%d j).' % int(ed), source='calendrier')


def build(company, *, sector_median=None, earnings_in_days=None):
    """Rend la carte des risques d'un dossier. `company` : payload company (avec
    'fundamentals'). `earnings_in_days` optionnel (sinon lu du calendrier)."""
    comp = company or {}
    fu = dict(comp.get('fundamentals') or {})
    if earnings_in_days is not None:
        fu['earnings_in_days'] = earnings_in_days
    risks = [
        _valuation(fu, sector_median), _financial(fu), _growth(fu),
        _execution(fu), _competition(comp), _event(fu),
    ]
    known = [r for r in risks if r['known']]
    highest = max((r['level'] for r in known), key=lambda l: _ORDER[l]) if known else UNKNOWN
    return {
        'symbol': comp.get('symbol'),
        'risks': risks,
        'known_count': len(known),
        'total_count': len(risks),
        'highest_level': highest,
        'high_risks': [r['category'] for r in risks if r['level'] == HIGH],
        'limitations': ['Carte heuristique fondée sur les fondamentaux et les '
                        'médianes sectorielles — indicateur de vigilance, pas une prévision.'],
    }


__all__ = ['build', 'LOW', 'MED', 'HIGH', 'UNKNOWN']
