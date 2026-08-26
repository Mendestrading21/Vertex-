"""vertex.market.news_pipeline — ingestion & validation des actualités (§15).

Source : le fil réel déjà collecté et assaini (news_state, boucle
d'actualités multi-sources). Ce module NORMALISE et VALIDE — il n'invente
jamais un événement : titre + source + heure requis, sinon rejeté
(le rejet est compté, pas masqué).
"""
from __future__ import annotations

from vertex.market.news_dedup import deduplicate
from vertex.market.news_impact import classify, score_importance
from vertex.services.news_plus import nom_publieur


def _valid(item: dict) -> bool:
    """Titre + publieur + heure. Sans quoi l'événement n'est ni datable ni
    attribuable, et le rejet est COMPTÉ, pas masqué.

    `nom_publieur` remplace `publisher or source` : ces deux clés seules
    rejetaient **toutes les dépêches IBKR et tout le fil yfinance** — qui
    émettent `pub` — en les comptant comme MALFORMÉS. Mesure du 26 août 2026 :
    deux articles sur trois perdus.
    """
    return not raisons_rejet(item)


#: Les causes de rejet, nommées. `rejected` disait COMBIEN, jamais POURQUOI —
#: et un compte sans cause est une forme de masquage. C'est précisément ce qui
#: a envoyé chercher le défaut de D-122 du mauvais côté : deux dépêches IBKR
#: sur trois étaient comptées comme MALFORMÉES alors que le consommateur lisait
#: la mauvaise clé.
CAUSES_REJET = ('non_dict', 'titre_absent', 'publieur_absent', 'date_absente')


def raisons_rejet(item) -> list:
    """Toutes les raisons pour lesquelles cet item ne peut pas devenir un
    événement. Liste vide = item valide.

    Un item peut échouer sur **plusieurs** conditions ; elles sont toutes
    rendues. Ne garder que la première ferait apparaître la seconde seulement
    une fois la première corrigée, et le diagnostic se ferait en deux passes
    au lieu d'une.

    `_valid` en dérive : deux implantations de la même règle divergeraient, et
    c'est exactement le défaut que ce programme paie depuis D-117.
    """
    if not isinstance(item, dict):
        return ['non_dict']
    manque = []
    if not str(item.get('title') or '').strip():
        manque.append('titre_absent')
    if not nom_publieur(item):
        manque.append('publieur_absent')
    if not (item.get('time') or item.get('date')):
        manque.append('date_absente')
    return manque


def collect(news_state: dict, portfolio_syms: list[str] | None = None) -> dict:
    """items bruts → événements validés/dédupliqués/classés + stats de rejet."""
    raw = list(news_state.get('items') or [])
    rejected = 0
    par_cause = {c: 0 for c in CAUSES_REJET}
    events = []
    for it in raw:
        manque = raisons_rejet(it)
        if manque:
            rejected += 1
            for cause in manque:
                par_cause[cause] += 1
            continue
        title = str(it.get('title') or '').strip()
        ev = {
            'title': title,
            'title_fr': str(it.get('fr') or '').strip() or None,
            'source': nom_publieur(it),
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
            #  `rejected` compte les ITEMS ; `rejets_par_cause` compte les
            #  CONDITIONS, et un item peut en manquer plusieurs. Leur somme
            #  n'a donc pas a etre egale — `rejets_note` le dit, plutot que de
            #  laisser un lecteur conclure a une incoherence.
            'rejets_par_cause': par_cause,
            'rejets_note': ('un item peut manquer plusieurs conditions : la somme '
                            'par cause peut depasser le nombre d items rejetes'),
            'raw_count': len(raw), 'updated': news_state.get('updated')}


__all__ = ['collect', 'raisons_rejet', 'CAUSES_REJET']
