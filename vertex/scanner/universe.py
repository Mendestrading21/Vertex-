"""vertex.scanner.universe — univers principal du scanner institutionnel (§22).

S&P 100-like (grosses capitalisations de l'union S&P500/Nasdaq100/Dow30 déjà
chargée), Nasdaq 100, leaders sectoriels, watchlist, positions détenues,
favoris et candidats manuels. Chaque symbole porte son ORIGINE (membership).
"""
from __future__ import annotations

from vertex.data.universe import INDEX_MEMBERS, WATCHLIST

ORIGIN_INDEX = 'INDEX'
ORIGIN_WATCHLIST = 'WATCHLIST'
ORIGIN_POSITION = 'POSITION'
ORIGIN_FAVORITE = 'FAVORITE'
ORIGIN_MANUAL = 'MANUAL'

# Priorité de scan par origine (une position détenue passe toujours d'abord).
ORIGIN_PRIORITY = {ORIGIN_POSITION: 0, ORIGIN_FAVORITE: 1, ORIGIN_MANUAL: 2,
                   ORIGIN_WATCHLIST: 3, ORIGIN_INDEX: 4}


def build_universe(positions: list[str] | None = None,
                   favorites: list[str] | None = None,
                   manual: list[str] | None = None,
                   max_symbols: int | None = None) -> list[dict]:
    """Univers dédupliqué, trié par priorité d'origine."""
    members: dict[str, dict] = {}

    def add(sym: str, origin: str):
        sym = (sym or '').strip().upper()
        if not sym:
            return
        cur = members.get(sym)
        if cur is None or ORIGIN_PRIORITY[origin] < ORIGIN_PRIORITY[cur['origin']]:
            members[sym] = {'symbol': sym, 'origin': origin}

    for s in INDEX_MEMBERS.get('union') or []:
        add(s, ORIGIN_INDEX)
    for s in INDEX_MEMBERS.get('ndx100') or []:
        add(s, ORIGIN_INDEX)
    for s in WATCHLIST:
        add(s, ORIGIN_WATCHLIST)
    for s in favorites or []:
        add(s, ORIGIN_FAVORITE)
    for s in manual or []:
        add(s, ORIGIN_MANUAL)
    for s in positions or []:
        add(s, ORIGIN_POSITION)

    out = sorted(members.values(),
                 key=lambda m: (ORIGIN_PRIORITY[m['origin']], m['symbol']))
    return out[:max_symbols] if max_symbols else out
