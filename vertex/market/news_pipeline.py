"""vertex.market.news_pipeline — ingestion & validation des actualités (§15).

Source : le fil réel collecté par la boucle d'actualités multi-sources
(`news_state`). Ce module NORMALISE et VALIDE — il n'invente jamais un
événement : titre + source + heure requis, sinon rejeté (le rejet est compté,
pas masqué).

⚠ LOT 32 — `news_state['items']` est BRUT : la boucle y dépose les titres
yfinance/RSS tels quels, et c'est chaque sortie qui assainit. Ce module est une
sortie comme une autre : ses titres partent dans le brief éditorial
(`/api/briefing/editorial`), qui n'appelle pas `sanitize_news`. Mesuré :
`<img src=x onerror=…>` sortait vivant dans `daily.what_changed`. On retire ici
le BALISAGE (pas les méta-caractères — le client échappe déjà au rendu).
"""
from __future__ import annotations

from vertex.market.news_dedup import deduplicate
from vertex.market.news_impact import classify, score_importance
from vertex.services.news_plus import safe_link, strip_markup


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
        title = strip_markup(str(it.get('title') or '')).strip()
        if not title:                     # titre entièrement fait de balisage
            rejected += 1
            continue
        ev = {
            'title': title,
            'title_fr': strip_markup(str(it.get('fr') or '')).strip() or None,
            'source': strip_markup(str(it.get('publisher') or it.get('source') or '')).strip(),
            'time': strip_markup(str(it.get('time') or it.get('date') or '')),
            'link': safe_link(it.get('link')),
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
