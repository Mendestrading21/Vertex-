"""vertex.market.news_dedup — déduplication d'actualités (§15).

Deux titres qui racontent le même événement (mêmes tokens significatifs)
sont fusionnés — la version la plus récente et la mieux sourcée gagne.
Purement déterministe, aucune invention.
"""
from __future__ import annotations

import re

_STOP = {'the', 'a', 'an', 'of', 'to', 'in', 'on', 'for', 'and', 'or', 'as',
         'is', 'are', 'at', 'by', 'with', 'after', 'before', 'le', 'la',
         'les', 'des', 'de', 'du', 'un', 'une', 'et', 'en', 'sur', 'pour'}


def _key(title: str) -> str:
    toks = [t for t in re.findall(r'[a-z0-9]{3,}', (title or '').lower())
            if t not in _STOP]
    return '|'.join(sorted(set(toks))[:8])


def deduplicate(events: list[dict]) -> list[dict]:
    by_key: dict[str, dict] = {}
    for ev in events:
        k = _key(ev.get('title', ''))
        if not k:
            continue
        cur = by_key.get(k)
        if cur is None:
            by_key[k] = dict(ev, corroborations=1)
        else:
            cur['corroborations'] = cur.get('corroborations', 1) + 1
            cur.setdefault('also_from', [])
            src = ev.get('source')
            if src and src != cur.get('source') and src not in cur['also_from']:
                cur['also_from'].append(src)
            if (ev.get('time') or '') > (cur.get('time') or ''):
                cur.update({k2: v for k2, v in ev.items() if v})
    return list(by_key.values())


__all__ = ['deduplicate']
