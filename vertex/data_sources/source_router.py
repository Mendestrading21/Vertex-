"""vertex.data_sources.source_router — priorité des sources, sans mélange silencieux.

Priorité (§12) :
  1. IBKR live
  2. IBKR delayed / frozen — clairement indiqué
  3. fournisseur secondaire validé
  4. fallback EOD
  5. indisponible (honnête : None, jamais un chiffre inventé)
"""
from __future__ import annotations

import time
from typing import Callable

from .models import (
    ProvenancedValue, SOURCE_IBKR, SOURCE_SECONDARY, SOURCE_FALLBACK_EOD,
    MODE_LIVE, MODE_DELAYED, MODE_FROZEN, MODE_EOD, missing,
)
from . import provenance

# (source, mode) ordonnés par préférence décroissante.
PRIORITY: tuple[tuple[str, str], ...] = (
    (SOURCE_IBKR, MODE_LIVE),
    (SOURCE_IBKR, MODE_DELAYED),
    (SOURCE_IBKR, MODE_FROZEN),
    (SOURCE_SECONDARY, MODE_DELAYED),
    (SOURCE_SECONDARY, MODE_EOD),
    (SOURCE_FALLBACK_EOD, MODE_EOD),
)


def rank(source: str, mode: str) -> int:
    try:
        return PRIORITY.index((source, mode))
    except ValueError:
        return len(PRIORITY)


class SourceRouter:
    """Route une demande vers la meilleure source disponible.

    Les providers sont des callables ``() -> ProvenancedValue | None`` déclarés
    avec leur (source, mode). Le routeur essaie dans l'ordre de priorité et
    marque ``fallback_used`` dès qu'on n'est plus sur la source de tête.
    """

    def __init__(self, failure_threshold: int = 2, cooldown_seconds: float = 30.0,
                 slow_provider_ms: float = 2500.0, clock: Callable[[], float] | None = None) -> None:
        self._providers: list[tuple[int, str, str, Callable[[], ProvenancedValue | None]]] = []
        self._failure_threshold = max(1, int(failure_threshold))
        self._cooldown_seconds = max(1.0, float(cooldown_seconds))
        self._slow_provider_ms = max(1.0, float(slow_provider_ms))
        self._clock = clock or time.monotonic
        self._state: dict[tuple[str, str], dict] = {}

    def register(self, source: str, mode: str,
                 provider: Callable[[], ProvenancedValue | None]) -> None:
        self._providers.append((rank(source, mode), source, mode, provider))
        self._providers.sort(key=lambda item: item[0])
        self._state.setdefault((source, mode), {
            'failures': 0, 'open_until': 0.0, 'last_latency_ms': None,
            'slow_calls': 0, 'calls': 0,
        })

    def health(self) -> dict:
        """État agrégé des fournisseurs, sans URL, erreur ni donnée de marché."""
        now = self._clock()
        providers = []
        for _, source, mode, _ in self._providers:
            state = self._state[(source, mode)]
            open_for = max(0.0, state['open_until'] - now)
            providers.append({
                'source': source, 'mode': mode,
                'status': 'OPEN' if open_for else 'CLOSED',
                'failures': state['failures'],
                'open_for_seconds': round(open_for, 3),
                'calls': state['calls'],
                'last_latency_ms': state['last_latency_ms'],
                'slow_calls': state['slow_calls'],
            })
        return {'read_only': True, 'failure_threshold': self._failure_threshold,
                'cooldown_seconds': self._cooldown_seconds, 'providers': providers}

    def fetch(self) -> ProvenancedValue:
        errors: list[str] = []
        for idx, (_, source, mode, provider) in enumerate(self._providers):
            state = self._state[(source, mode)]
            now = self._clock()
            if state['open_until'] > now:
                errors.append(f'{source}/{mode}: circuit_ouvert')
                continue
            started = self._clock()
            try:
                pv = provider()
            except Exception:  # une source qui casse ne casse pas l'app
                state['calls'] += 1
                state['failures'] += 1
                if state['failures'] >= self._failure_threshold:
                    state['open_until'] = self._clock() + self._cooldown_seconds
                errors.append(f'{source}/{mode}: indisponible')
                continue
            elapsed_ms = (self._clock() - started) * 1000
            state['calls'] += 1
            state['last_latency_ms'] = round(max(0.0, elapsed_ms), 3)
            if pv is None or pv.value is None:
                state['failures'] += 1
                if state['failures'] >= self._failure_threshold:
                    state['open_until'] = self._clock() + self._cooldown_seconds
                errors.append(f'{source}/{mode}: indisponible')
                continue
            state['failures'] = 0
            state['open_until'] = 0.0
            pv.source, pv.source_mode = source, mode
            pv.fallback_used = idx > 0
            if elapsed_ms > self._slow_provider_ms:
                state['slow_calls'] += 1
                pv.warnings.append(f'latence_source_elevee {source}/{mode}')
            if idx > 0:
                pv.warnings.append(
                    f'source de repli {source}/{mode} (sources devant indisponibles)')
            provenance.refresh_quality(pv)
            return pv
        pv = missing('aucune source disponible')
        pv.warnings.extend(errors)
        return pv
