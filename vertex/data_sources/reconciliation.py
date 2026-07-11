"""vertex.data_sources.reconciliation — comparaison entre sources (§13).

Quand deux sources décrivent la même réalité, elles doivent être d'accord.
Sinon : incohérence documentée, et au-delà d'un seuil → ACTIONABLE interdit,
décision maximale ATTENDRE.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

from .provenance import parse_iso

# Seuils par défaut
PRICE_DISAGREEMENT_WARN_PCT = 0.5    # écart de prix suspect
PRICE_DISAGREEMENT_BLOCK_PCT = 2.0   # écart de prix bloquant (split raté, mauvais mapping…)
TIMESTAMP_MISMATCH_BLOCK_S = 6 * 3600  # spot et options de séances différentes
SPLIT_RATIOS = (2.0, 3.0, 4.0, 5.0, 10.0, 20.0, 0.5, 1 / 3, 0.25, 0.2, 0.1)


@dataclass
class Inconsistency:
    code: str
    severity: int            # 1 info · 2 avertissement · 3 bloquant
    detail: str
    observed: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReconciliationReport:
    symbol: str
    inconsistencies: list = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return any(i.severity >= 3 for i in self.inconsistencies)

    @property
    def actionable_allowed(self) -> bool:
        return not self.blocking

    @property
    def max_decision(self) -> str | None:
        """Décision maximale imposée (None = pas de plafond)."""
        return 'ATTENDRE' if self.blocking else None

    def add(self, code: str, severity: int, detail: str, **observed) -> None:
        self.inconsistencies.append(Inconsistency(code, severity, detail, observed))

    def to_dict(self) -> dict:
        return {'symbol': self.symbol, 'blocking': self.blocking,
                'actionable_allowed': self.actionable_allowed,
                'max_decision': self.max_decision,
                'inconsistencies': [i.to_dict() for i in self.inconsistencies]}


def _pct_gap(a: float, b: float) -> float:
    ref = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / ref * 100.0


def _looks_like_split(a: float, b: float) -> bool:
    if not a or not b:
        return False
    ratio = a / b
    return any(abs(ratio - r) / r < 0.03 for r in SPLIT_RATIOS)


def reconcile_spot(symbol: str, quotes: list[dict],
                   report: ReconciliationReport | None = None) -> ReconciliationReport:
    """Compare des cotations {'source','price','timestamp','currency'} entre elles."""
    report = report or ReconciliationReport(symbol)
    priced = [q for q in quotes if q.get('price') not in (None, 0)]
    if len(priced) >= 2:
        base = priced[0]
        for other in priced[1:]:
            gap = _pct_gap(float(base['price']), float(other['price']))
            if _looks_like_split(float(base['price']), float(other['price'])):
                report.add('SPLIT_MISMATCH', 3,
                           f"ratio de prix {base['source']}/{other['source']} compatible avec un split non appliqué",
                           prices={base['source']: base['price'], other['source']: other['price']})
            elif gap >= PRICE_DISAGREEMENT_BLOCK_PCT:
                report.add('SOURCE_DISAGREEMENT', 3,
                           f"écart de prix {gap:.2f}% entre {base['source']} et {other['source']}",
                           gap_pct=round(gap, 3))
            elif gap >= PRICE_DISAGREEMENT_WARN_PCT:
                report.add('SOURCE_DISAGREEMENT', 2,
                           f"écart de prix {gap:.2f}% entre {base['source']} et {other['source']}",
                           gap_pct=round(gap, 3))
        currencies = {q.get('currency') for q in priced if q.get('currency')}
        if len(currencies) > 1:
            report.add('CURRENCY_MISMATCH', 3,
                       f'devises incompatibles entre sources: {sorted(currencies)}',
                       currencies=sorted(currencies))
    return report


def reconcile_spot_vs_options(symbol: str, spot_ts: str, chain_ts: str,
                              report: ReconciliationReport | None = None) -> ReconciliationReport:
    """Le spot et la chaîne d'options doivent venir de la même séance."""
    report = report or ReconciliationReport(symbol)
    s, c = parse_iso(spot_ts), parse_iso(chain_ts)
    if s is None or c is None:
        report.add('TIMESTAMP_MISMATCH', 2, 'timestamp spot ou chaîne manquant',
                   spot_ts=spot_ts, chain_ts=chain_ts)
        return report
    gap = abs((s - c).total_seconds())
    if gap > TIMESTAMP_MISMATCH_BLOCK_S:
        report.add('TIMESTAMP_MISMATCH', 3,
                   f'spot et chaîne d’options séparés de {gap / 3600:.1f}h — séances différentes',
                   gap_seconds=int(gap))
    return report


def reconcile_earnings_dates(symbol: str, dates: dict,
                             report: ReconciliationReport | None = None) -> ReconciliationReport:
    """dates = {'IBKR': '2026-07-28', 'SECONDARY': '2026-07-29', ...}"""
    report = report or ReconciliationReport(symbol)
    distinct = {d for d in dates.values() if d}
    if len(distinct) > 1:
        report.add('EARNINGS_DATE_DIVERGENCE', 3,
                   f'dates de résultats divergentes: {dates} — tenir la position à travers '
                   'les résultats est interdit tant que la date n’est pas confirmée',
                   dates=dict(dates))
    return report


def reconcile_contract(symbol: str, contract: dict,
                       report: ReconciliationReport | None = None) -> ReconciliationReport:
    """Vérifie multiplicateur / devise / mapping d'un contrat d'option."""
    report = report or ReconciliationReport(symbol)
    mult = contract.get('multiplier')
    if mult not in (None, '', 100, '100'):
        report.add('MULTIPLIER_MISMATCH', 3,
                   f'multiplicateur inattendu: {mult!r} (attendu 100)', multiplier=mult)
    cur = contract.get('currency')
    if cur not in (None, '', 'USD'):
        report.add('CURRENCY_MISMATCH', 3, f'devise de contrat inattendue: {cur!r}', currency=cur)
    und = (contract.get('underlying') or '').upper()
    if und and und != symbol.upper():
        report.add('CONTRACT_MAPPING_ERROR', 3,
                   f'sous-jacent du contrat {und!r} ≠ symbole demandé {symbol!r}', underlying=und)
    bid, ask = contract.get('bid'), contract.get('ask')
    if bid is not None and ask is not None and float(bid) > float(ask) > 0:
        report.add('BID_ABOVE_ASK', 3, f'marché croisé: bid {bid} > ask {ask}', bid=bid, ask=ask)
    return report
