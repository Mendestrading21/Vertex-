"""vertex.ai.gateway — porte partagée des appels IA sortants (lot 11).

Constat mesuré : `investment_agent` passait par RateLimiter + AIAudit +
fallback, mais copilote, briefs et enrichissement appelaient Anthropic en
DIRECT. Cette porte réunit les deux gardes manquantes en un seul point :

- **budget de débit par famille d'appel** (fenêtre glissante 60 s, par
  processus) — un clic copilote effréné n'affame pas les briefs, et
  inversement ; un run d'enrichissement complet (24 titres × 2 recherches)
  tient dans son budget ;
- **journal d'audit partagé** (`vertex.ai.audit.AUDIT`) — chaque appel,
  refus de budget compris, laisse une trace bornée en mémoire, sans secret.

La porte n'est consultée QUE lorsque la couche IA est disponible : sans clé,
les chemins de repli existants restent intacts et ne consomment rien.
Le refus n'est JAMAIS une exception : l'appelant garde son repli
déterministe honnête.
"""
from __future__ import annotations

from .audit import AUDIT
from .rate_limits import RateLimiter

#  Budgets par famille (appels / 60 s). Le copilote est piloté au clic →
#  serré ; les briefs sont appelés par fiche → moyen ; l'enrichissement est
#  un lot borné (MAX_SYMBOLS=24 × 2 surfaces = 48 appels) → il doit tenir
#  ENTIER dans une fenêtre, sinon la porte casserait un run légitime.
_BUDGETS = {'copilot': 10, 'briefs': 30, 'enrichment': 60}
_DEFAULT_BUDGET = 20
_WINDOW_S = 60.0

_limiters: dict[str, RateLimiter] = {}


def _limiter(source: str) -> RateLimiter:
    lim = _limiters.get(source)
    if lim is None:
        lim = RateLimiter(max_calls=_BUDGETS.get(source, _DEFAULT_BUDGET),
                          window_s=_WINDOW_S)
        _limiters[source] = lim
    return lim


def allow(source: str, symbol: str = '') -> bool:
    """Vrai si l'appel peut partir. Un refus est journalisé, jamais levé."""
    if _limiter(source).allow():
        return True
    AUDIT.record(symbol=symbol or '', source=source, ok=False,
                 errors=['rate_limited'])
    return False


def record(*, source: str, symbol: str = '', ok: bool, errors=None,
           duration_ms=None, model: str = '') -> None:
    """Trace d'audit d'un appel effectué (succès ou panne provider)."""
    AUDIT.record(symbol=symbol or '', source=source, ok=ok,
                 errors=list(errors or []), duration_ms=duration_ms,
                 model=model)


def status() -> dict:
    """Consommation courante par famille (lecture seule, pour /system)."""
    out = {}
    for source in sorted(set(_BUDGETS) | set(_limiters)):
        out[source] = _limiter(source).status()
    return out


def reset_for_test() -> None:
    _limiters.clear()


__all__ = ['allow', 'record', 'status', 'reset_for_test']
