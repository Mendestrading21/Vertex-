"""vertex.research.factory — Research Factory : cycle de vie et walk-forward (§29).

Cycle : IDEA → DEFINED → BACKTESTED → WALK_FORWARD → PAPER_VALIDATED →
APPROVED / REJECTED → RETIRED. Aucun signal ne devient actif uniquement parce
que son backtest historique est beau : APPROVED exige walk-forward + contrôles
de biais documentés.
"""
from __future__ import annotations

from dataclasses import dataclass, field

STATES = ('IDEA', 'DEFINED', 'BACKTESTED', 'WALK_FORWARD', 'PAPER_VALIDATED',
          'APPROVED', 'REJECTED', 'RETIRED')

_TRANSITIONS = {
    'IDEA': {'DEFINED', 'REJECTED', 'RETIRED'},
    'DEFINED': {'BACKTESTED', 'REJECTED', 'RETIRED'},
    'BACKTESTED': {'WALK_FORWARD', 'REJECTED', 'RETIRED'},
    'WALK_FORWARD': {'PAPER_VALIDATED', 'REJECTED', 'RETIRED'},
    'PAPER_VALIDATED': {'APPROVED', 'REJECTED', 'RETIRED'},
    'APPROVED': {'RETIRED'},
    'REJECTED': {'IDEA', 'RETIRED'},
    'RETIRED': set(),
}

REQUIRED_DEFINITION = ('hypothesis', 'universe', 'horizon', 'signal', 'entry',
                       'invalidation', 'exit', 'costs', 'benchmark', 'metrics',
                       'rejection_criteria')

BIAS_CONTROLS = ('look_ahead', 'survivorship', 'data_leakage', 'multiple_testing',
                 'overfitting', 'selection_bias', 'slippage', 'spread', 'latency',
                 'delisted_securities', 'corporate_actions', 'parameter_instability')


class LifecycleError(ValueError):
    pass


@dataclass
class Experiment:
    name: str
    definition: dict = field(default_factory=dict)
    state: str = 'IDEA'
    history: list = field(default_factory=list)
    bias_controls: dict = field(default_factory=dict)
    results: dict = field(default_factory=dict)

    def advance(self, new_state: str, evidence: dict | None = None) -> None:
        if new_state not in STATES:
            raise LifecycleError(f'état inconnu: {new_state}')
        if new_state not in _TRANSITIONS[self.state]:
            raise LifecycleError(f'transition interdite: {self.state} → {new_state}')
        if new_state == 'DEFINED':
            missing = [k for k in REQUIRED_DEFINITION if not self.definition.get(k)]
            if missing:
                raise LifecycleError(f'définition incomplète: {missing}')
        if new_state == 'APPROVED':
            missing = [k for k in BIAS_CONTROLS if k not in self.bias_controls]
            if missing:
                raise LifecycleError(f'contrôles de biais non documentés: {missing}')
            if not self.results.get('walk_forward'):
                raise LifecycleError('APPROVED exige un walk-forward — un beau backtest '
                                     'historique ne suffit jamais')
        self.history.append({'from': self.state, 'to': new_state,
                             'evidence': evidence or {}})
        self.state = new_state


def walk_forward_splits(n_samples: int, n_folds: int = 5, embargo: int = 5) -> list[dict]:
    """Découpage walk-forward SANS look-ahead : chaque fold s'entraîne sur le
    passé strict et teste sur le futur, séparés par un embargo."""
    if n_samples < (n_folds + 1) * 20:
        raise ValueError('échantillon trop court pour un walk-forward sérieux')
    fold_size = n_samples // (n_folds + 1)
    splits = []
    for k in range(1, n_folds + 1):
        train_end = k * fold_size
        test_start = train_end + embargo
        test_end = min(test_start + fold_size, n_samples)
        if test_start >= test_end:
            break
        splits.append({'train': (0, train_end), 'test': (test_start, test_end),
                       'embargo': embargo})
    return splits


def run_walk_forward(returns: list[float], signal_fn, n_folds: int = 5,
                     embargo: int = 5) -> dict:
    """signal_fn(train_returns) -> callable(window) -> position (0/1) pour le test.

    Le signal est CALIBRÉ sur le train uniquement, appliqué au test — le test
    ne voit jamais ses propres données à la calibration (anti look-ahead).
    """
    splits = walk_forward_splits(len(returns), n_folds, embargo)
    fold_results = []
    for sp in splits:
        tr_lo, tr_hi = sp['train']
        te_lo, te_hi = sp['test']
        strategy = signal_fn(returns[tr_lo:tr_hi])
        pnl = []
        for i in range(te_lo, te_hi):
            # la stratégie ne voit que les données STRICTEMENT antérieures à i
            position = strategy(returns[:i])
            pnl.append(position * returns[i])
        avg = sum(pnl) / len(pnl) if pnl else 0.0
        fold_results.append({'train': sp['train'], 'test': sp['test'],
                             'mean_return': round(avg, 6), 'n': len(pnl)})
    oos = [f['mean_return'] for f in fold_results]
    positive_folds = sum(1 for x in oos if x > 0)
    return {'folds': fold_results, 'oos_mean': round(sum(oos) / len(oos), 6) if oos else None,
            'positive_folds': positive_folds, 'total_folds': len(oos),
            'passed': bool(oos) and positive_folds >= max(2, len(oos) - 1)}


def apply_costs(gross_returns: list[float], spread_pct: float = 0.05,
                slippage_pct: float = 0.05, turnover: float = 1.0) -> list[float]:
    """Retourne les rendements nets d'un coût par transaction documenté."""
    cost = (spread_pct + slippage_pct) / 100 * turnover
    return [r - cost for r in gross_returns]
