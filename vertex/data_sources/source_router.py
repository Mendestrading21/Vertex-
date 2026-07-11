"""vertex.data_sources.source_router — priorité des sources, sans mélange silencieux.

Priorité (§12) :
  1. IBKR live
  2. IBKR delayed / frozen — clairement indiqué
  3. fournisseur secondaire validé
  4. fallback EOD
  5. indisponible (honnête : None, jamais un chiffre inventé)
"""
from __future__ import annotations

from typing import Callable, Iterable

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

    def __init__(self) -> None:
        self._providers: list[tuple[int, str, str, Callable[[], ProvenancedValue | None]]] = []

    def register(self, source: str, mode: str,
                 provider: Callable[[], ProvenancedValue | None]) -> None:
        self._providers.append((rank(source, mode), source, mode, provider))
        self._providers.sort(key=lambda item: item[0])

    def fetch(self) -> ProvenancedValue:
        errors: list[str] = []
        for idx, (_, source, mode, provider) in enumerate(self._providers):
            try:
                pv = provider()
            except Exception as exc:  # une source qui casse ne casse pas l'app
                errors.append(f'{source}/{mode}: {exc.__class__.__name__}: {exc}')
                continue
            if pv is None or pv.value is None:
                errors.append(f'{source}/{mode}: indisponible')
                continue
            pv.source, pv.source_mode = source, mode
            pv.fallback_used = idx > 0
            if idx > 0:
                pv.warnings.append(
                    f'source de repli {source}/{mode} (sources devant indisponibles)')
            provenance.refresh_quality(pv)
            return pv
        pv = missing('aucune source disponible')
        pv.warnings.extend(errors)
        return pv
