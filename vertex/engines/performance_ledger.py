"""vertex.engines.performance_ledger — track record complet (§34, corrige §6.10).

Sépare STRICTEMENT :
  SIGNAL (généré) → ALERT (présentée) → RECOMMENDATION → USER_DECISION →
  SIMULATED_POSITION → REAL_POSITION (ouverte/clôturée).
La performance théorique des signaux n'est JAMAIS confondue avec la
performance réelle d'un portefeuille : les métriques sont calculées PAR type.
"""
from __future__ import annotations

import math
from collections import defaultdict

RECORD_TYPES = ('SIGNAL', 'ALERT', 'RECOMMENDATION', 'USER_DECISION',
                'SIMULATED_POSITION', 'REAL_POSITION')


class PerformanceLedger:
    def __init__(self) -> None:
        self._records: list[dict] = []
        self._seq = 0

    def record(self, record_type: str, symbol: str, payload: dict | None = None,
               parent_id: str | None = None) -> dict:
        if record_type not in RECORD_TYPES:
            raise ValueError(f'type de trace inconnu: {record_type}')
        self._seq += 1
        entry = {'id': f'{record_type.lower()}-{self._seq}', 'type': record_type,
                 'symbol': symbol.upper(), 'parent_id': parent_id,
                 'payload': dict(payload or {}), 'closed': False, 'result': None}
        self._records.append(entry)
        return entry

    def close(self, entry_id: str, result: dict) -> dict:
        """result : {'return_pct','underlying_return_pct','spy_return_pct','mae_pct',
        'mfe_pct','days_held','stop_hit','tp_hit','days_to_25','days_to_50',
        'days_to_100','setup','regime','delta','dte','iv','data_quality','anomaly'}"""
        for e in self._records:
            if e['id'] == entry_id:
                e['closed'] = True
                e['result'] = dict(result)
                return e
        raise KeyError(entry_id)

    def records(self, record_type: str | None = None, closed: bool | None = None) -> list[dict]:
        out = self._records
        if record_type:
            out = [e for e in out if e['type'] == record_type]
        if closed is not None:
            out = [e for e in out if e['closed'] == closed]
        return list(out)

    # ── métriques ─────────────────────────────────────────────────────
    def metrics(self, record_type: str) -> dict:
        """Métriques calculées UNIQUEMENT sur ce type de trace — jamais mélangées."""
        closed = self.records(record_type, closed=True)
        rets = [e['result'].get('return_pct') for e in closed
                if e['result'].get('return_pct') is not None]
        out = {'type': record_type, 'n_total': len(self.records(record_type)),
               'n_closed': len(closed), 'metrics_scope':
               'théorique (signal)' if record_type in ('SIGNAL', 'ALERT', 'RECOMMENDATION')
               else 'réel/simulé (position)'}
        if len(rets) < 5:
            out['note'] = 'moins de 5 résultats clôturés — métriques non affichées (honnêteté)'
            return out
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        gross_win = sum(wins)
        gross_loss = abs(sum(losses)) or 1e-9
        mean = sum(rets) / len(rets)
        sd = math.sqrt(sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)) if len(rets) > 1 else 0
        downside = [r for r in rets if r < 0]
        dsd = math.sqrt(sum(r ** 2 for r in downside) / len(downside)) if downside else 0
        equity, peak, max_dd = 1.0, 1.0, 0.0
        for r in rets:
            equity *= (1 + r / 100)
            peak = max(peak, equity)
            max_dd = min(max_dd, (equity / peak - 1) * 100)
        spy = [e['result'].get('spy_return_pct') for e in closed
               if e['result'].get('spy_return_pct') is not None]
        alpha = (mean - sum(spy) / len(spy)) if spy else None
        out.update({
            'win_rate': round(len(wins) / len(rets), 3),
            'expectancy_pct': round(mean, 2),
            'profit_factor': round(gross_win / gross_loss, 2),
            'sharpe_like': round(mean / sd, 2) if sd else None,
            'sortino_like': round(mean / dsd, 2) if dsd else None,
            'max_drawdown_pct': round(max_dd, 2),
            'calmar_like': round((equity - 1) * 100 / abs(max_dd), 2) if max_dd else None,
            'alpha_vs_spy_pct': round(alpha, 2) if alpha is not None else None,
            'mae_avg': _avg(closed, 'mae_pct'), 'mfe_avg': _avg(closed, 'mfe_pct'),
            'stop_hit_rate': _rate(closed, 'stop_hit'), 'tp_hit_rate': _rate(closed, 'tp_hit'),
            'days_to_25_avg': _avg(closed, 'days_to_25'),
            'days_to_50_avg': _avg(closed, 'days_to_50'),
            'days_to_100_avg': _avg(closed, 'days_to_100'),
        })
        return out

    def breakdown(self, record_type: str, by: str) -> dict:
        """Résultats par setup/régime/delta/DTE/IV/qualité de données/anomalie."""
        closed = self.records(record_type, closed=True)
        groups: dict[str, list] = defaultdict(list)
        for e in closed:
            key = e['result'].get(by)
            r = e['result'].get('return_pct')
            if key is not None and r is not None:
                groups[str(key)].append(r)
        return {k: {'n': len(v), 'mean_pct': round(sum(v) / len(v), 2),
                    'win_rate': round(sum(1 for x in v if x > 0) / len(v), 2)}
                for k, v in groups.items() if len(v) >= 3}

    def funnel(self) -> dict:
        """Entonnoir signal → position réelle : où les idées se perdent."""
        return {t: len(self.records(t)) for t in RECORD_TYPES}


def _avg(closed, key):
    vals = [e['result'].get(key) for e in closed if e['result'].get(key) is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def _rate(closed, key):
    vals = [bool(e['result'].get(key)) for e in closed if key in e['result']]
    return round(sum(vals) / len(vals), 3) if vals else None
