"""vertex.market.news_pipeline — ingestion & validation des actualités (§15).

Source : le fil réel déjà collecté et assaini (news_state, boucle
d'actualités multi-sources). Ce module NORMALISE et VALIDE — il n'invente
jamais un événement : titre + source + heure requis, sinon rejeté
(le rejet est compté, pas masqué).
"""
from __future__ import annotations

from vertex.market.news_dedup import deduplicate
from vertex.market.news_impact import classify, score_importance


def _valid(item: dict) -> bool:
    return bool(item.get('title')) \
        and bool(item.get('publisher') or item.get('source')) \
        and bool(item.get('time') or item.get('date'))


def collect(news_state: dict, portfolio_syms: list[str] | None = None) -> dict:
    """items bruts → événements validés/dédupliqués/classés + stats de rejet."""
    raw = list(news_state.get('items') or [])
    rejected = 0
    events = []
    for it in raw:
        if not isinstance(it, dict) or not _valid(it):
            rejected += 1
            continue
        title = str(it.get('title') or '').strip()
        ev = {
            'title': title,
            'title_fr': str(it.get('fr') or '').strip() or None,
            'source': str(it.get('publisher') or it.get('source') or '').strip(),
            'time': str(it.get('time') or it.get('date') or ''),
            'link': it.get('link') or None,
            'sentiment': it.get('senti'),
            'entities': [str(it['sym']).upper()] if it.get('sym') else [],
        }
        ev['category'] = classify(title)
        events.append(ev)
    events = deduplicate(events)
    for ev in events:
        ev['importance'] = score_importance(ev, portfolio_syms or [])
        ev['positions_concerned'] = [s for s in ev.get('entities', [])
                                     if s in (portfolio_syms or [])]
    events.sort(key=lambda e: (e['importance'], e.get('time') or ''), reverse=True)
    return {'events': events, 'rejected': rejected,
            'raw_count': len(raw), 'updated': news_state.get('updated')}


__all__ = ['collect']
