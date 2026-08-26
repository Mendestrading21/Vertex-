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


#: Marqueur d'un evenement que la cle ne sait pas rapprocher. Il n'est PAS
#: deduplique — mais il est SERVI.
CLE_ABSENTE = 'CLE_ABSENTE'


def deduplicate(events: list[dict]) -> list[dict]:
    """Fusionne les doublons. **Une cle absente n'est pas un evenement absent.**

    ## Le defaut, mesure le 26 aout 2026

    Un titre dont aucun token ne fait trois caracteres hors mots vides
    produisait une cle vide — et l'evenement etait **jete en silence**, apres
    avoir pourtant passe la validation du pipeline. Personne ne le comptait :
    ni `rejected`, qui ne couvre que la validation, ni rien d'autre.

    Ce ne sont pas des cas theoriques ; ce sont des manchettes financieres
    ordinaires, ou les tickers font deux lettres :

    ```text
    'AI up 5%'      -> cle ''  -> JETE
    'BP up'         -> cle ''  -> JETE
    'GM & F up 3%'  -> cle ''  -> JETE
    ```

    Sur neuf titres realistes, **quatre perdus sans trace**.

    Desormais un evenement sans cle est **conserve**, marque `CLE_ABSENTE` et
    jamais fusionne : deux titres qu'on ne sait pas rapprocher restent deux
    evenements. C'est moins commode qu'un doublon supprime, et infiniment
    preferable a une manchette disparue.
    """
    by_key: dict[str, dict] = {}
    sans_cle: list[dict] = []
    for ev in events:
        k = _key(ev.get('title', ''))
        if not k:
            sans_cle.append(dict(ev, corroborations=1, dedup=CLE_ABSENTE))
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
    return list(by_key.values()) + sans_cle


__all__ = ['deduplicate', 'CLE_ABSENTE']
