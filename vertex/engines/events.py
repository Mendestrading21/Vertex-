"""vertex/engines/events.py — TIMELINE D'ÉVÉNEMENTS NORMALISÉE (SKYLER LOT 4).

Agrège en UNE forme canonique les événements réels d'un titre déjà produits
ailleurs (news assainies, earnings du calendrier, macro datée, anomalies
statistiques). Chaque événement porte :

  {kind, label, date, dte, category: 'fact'|'estimate'|'interpretation',
   source, impact_hint, impact_derivation, importance, confidence,
   date_fiabilite: 'PUBLIEE'|'INDICATIVE'}

Règles d'honnêteté :
  - la PUBLICATION d'une news est un fait ; son IMPACT ne l'est pas — il n'est
    suggéré (`impact_hint`) que par des mots-clés DÉTERMINISTES et transparents
    (`impact_derivation: 'keywords'`), sinon None ;
  - une anomalie statistique est une INTERPRÉTATION (confiance EXACT_STATISTICAL :
    z-scores exacts) ; une date de calendrier PUBLIÉE est un fait DÉCLARÉ ;
  - une date de calendrier INDICATIVE n'est pas un fait. Le calendrier macro
    place le CPI « au 13 » par convention et déduit le NFP du premier vendredi ;
    seules les dates FOMC sont publiées par la Fed. Le drapeau `approx` était
    perdu ici : le CPI du 13 septembre sortait `fact`/`DECLARED`, identique à la
    décision FOMC du 16. `date_fiabilite` le porte désormais, et le doute est le
    DÉFAUT — une source qui ne dit pas si sa date est publiée n'est pas crue sur
    parole ;
  - `peut_fonder_un_gate()` est la garde posée pour l'avenir. Aucun des treize
    hard gates V4 ne consomme les événements AUJOURD'HUI — c'est mesuré, et le
    dire évite de prétendre fermer une brèche ouverte. Le jour où un gate de
    fenêtre d'événement s'écrira, il ne pourra pas accepter en silence une date
    que personne n'a publiée ;
  - un événement daté n'est jamais noté « catalyseur » par sa seule existence ;
  - révisions d'analystes : AUCUNE source branchée → `available: False` honnête,
    jamais estimé ;
  - fonction PURE, déterministe, JSON-sérialisable. Lecture seule, aucun ordre.
"""
from __future__ import annotations

import re

from vertex.services.news_plus import dedupe_news

# Mots-clés déterministes → suggestion d'impact (transparent, jamais une certitude).
_KEYWORDS = (
    ('EARNINGS', ('earnings', 'résultats', 'resultats', 'beats', 'misses', 'guidance', 'revenue')),
    ('RATING', ('upgrade', 'downgrade', 'initiates', 'price target', 'objectif de cours')),
    ('REGULATORY', ('fda', 'sec ', 'lawsuit', 'antitrust', 'probe', 'enquête', 'amende')),
    ('MA', ('acquisition', 'merger', 'rachat', 'buyout', 'takeover')),
)


def _impact_from_title(title):
    t = ' %s ' % re.sub(r'\s+', ' ', str(title or '').lower())
    for tag, words in _KEYWORDS:
        if any(w in t for w in words):
            return tag, 'keywords'
    return None, None


#: Fiabilité de la DATE d'un événement — distincte de la confiance dans son
#: impact. Une date publiée par l'émetteur ou l'institution est un fait ; une
#: date posée par convention ne l'est pas, même si elle tombe juste.
DATE_PUBLIEE = 'PUBLIEE'
DATE_INDICATIVE = 'INDICATIVE'


def fiabilite_de_date(source_dict, defaut=DATE_INDICATIVE):
    """Lit le drapeau `approx` d'une entrée de calendrier.

    Le défaut est INDICATIVE, et c'est le sens du doute : une source qui ne dit
    pas si sa date est publiée ne doit pas être crue sur parole. Supposer
    « publiée » ferait entrer n'importe quelle estimation comme un fait.
    """
    if not isinstance(source_dict, dict) or 'approx' not in source_dict:
        return defaut
    return DATE_INDICATIVE if source_dict.get('approx') else DATE_PUBLIEE


def peut_fonder_un_gate(event) -> bool:
    """Cet événement peut-il déclencher ou lever un hard gate ?

    Deux refus, et aucun n'est cosmétique :

    - une date **indicative** n'a été publiée par personne. La laisser fonder
      un gate reviendrait à bloquer — ou débloquer — une décision sur une
      convention interne ;
    - un événement **sans date** n'ouvre aucune fenêtre temporelle : il n'y a
      rien à comparer.

    La garde n'est pas un refus généralisé : une date publiée passe. Une garde
    qui refuse tout serait contournée au premier besoin réel.
    """
    if not isinstance(event, dict) or not event.get('date'):
        return False
    return event.get('date_fiabilite') == DATE_PUBLIEE


def _ev(kind, label, category, source, date=None, dte=None, impact_hint=None,
        impact_derivation=None, importance=None, confidence=None,
        date_fiabilite=DATE_PUBLIEE, sources=None):
    ev = {'kind': kind, 'label': label, 'category': category, 'source': source,
          'date': date, 'dte': dte, 'impact_hint': impact_hint,
          'impact_derivation': impact_derivation, 'importance': importance,
          'confidence': confidence, 'date_fiabilite': date_fiabilite}
    if sources:
        #  Toutes les sources qui ont rapporte CE fait. `source` reste la
        #  premiere, pour les consommateurs existants ; `sources` les porte
        #  toutes, parce qu'un fait rapporte par trois agences n'est pas la
        #  meme preuve qu'un fait rapporte par une.
        ev['sources'] = sources
        ev['n_sources'] = len(sources)
    return ev


def _nom_source(n):
    """Le nom du publieur, quelle que soit la cle du producteur.

    Mesure du 26 aout 2026 : `ibkr_news` et le fil yfinance emettent `pub`,
    `news_plus.rss_news` emet `publisher`, et ce moteur ne lisait que
    `publisher`. **Toute depeche IBKR et tout article yfinance ressortait donc
    `news.externe`** — la source effacee a l'endroit meme ou le packet doit la
    porter.

    `dedupe_news` normalise desormais tout dans `sources[].pub` : on le lit en
    premier, et les cles historiques restent en repli.
    """
    origines = n.get('sources')
    if isinstance(origines, list) and origines:
        premier = origines[0].get('pub') if isinstance(origines[0], dict) else None
        if premier:
            return premier
    return n.get('publisher') or n.get('pub') or 'externe'


def build(sym, news=None, earnings=None, macro=None, anomaly=None, as_of=None):
    """Timeline normalisée d'un titre. Toutes les entrées sont OPTIONNELLES —
    absent = simplement omis (jamais inventé). `news` doit arriver déjà assainie
    (sanitize_news) ; la déduplication est appliquée ici."""
    events = []

    for e in (earnings or []):
        if not isinstance(e, dict) or not (e.get('date') or e.get('dte') is not None):
            continue
        events.append(_ev('earnings', 'Résultats %s' % (e.get('sym') or sym),
                          'fact', 'calendar.earnings', date=e.get('date'),
                          dte=e.get('dte'), impact_hint='EARNINGS',
                          impact_derivation='calendar', confidence='DECLARED'))

    for m in (macro or []):
        if not isinstance(m, dict) or not m.get('label'):
            continue
        #  Le drapeau `approx` du calendrier décide de la NATURE de l'entrée :
        #  une date publiée est un fait déclaré, une date de convention est une
        #  estimation. Les confondre — ce que faisait ce code — rendait le CPI
        #  du 13 septembre indiscernable de la décision FOMC du 16.
        fiab = fiabilite_de_date(m)
        publiee = fiab == DATE_PUBLIEE
        events.append(_ev('macro', m['label'],
                          'fact' if publiee else 'estimate', 'calendar.macro',
                          date=m.get('date'), dte=m.get('dte'),
                          impact_hint=(m.get('kind') or None),
                          impact_derivation=('calendar' if m.get('kind') else None),
                          importance=m.get('importance'),
                          confidence='DECLARED' if publiee else 'INDICATIVE',
                          date_fiabilite=fiab))

    revision_mentions = []
    for n in dedupe_news(news or []):
        title = n.get('title')
        if not title:
            continue
        hint, deriv = _impact_from_title(title)
        nom = _nom_source(n)
        origines = n.get('sources') if isinstance(n.get('sources'), list) else None
        if hint == 'RATING':
            revision_mentions.append({'title': title, 'source': 'news.%s' % nom,
                                      'date': n.get('time'), 'derivation': 'title_keywords',
                                      'sources': origines, 'n_sources': len(origines or [])})
        events.append(_ev('news', title, 'fact', 'news.%s' % nom,
                          date=n.get('time'), dte=None,
                          impact_hint=hint, impact_derivation=deriv,
                          confidence=None, sources=origines))

    for a in ((anomaly or {}).get('events') or []):
        if not isinstance(a, dict) or not a.get('label'):
            continue
        events.append(_ev('anomaly', a['label'], 'interpretation',
                          'engine.anomaly', date=None, dte=None,
                          impact_hint=None, confidence='EXACT_STATISTICAL'))

    # Datés d'abord (DTE croissant — le plus proche est le plus actionnable),
    # non datés ensuite dans leur ordre d'arrivée. Tri stable = déterministe.
    events.sort(key=lambda e: (e['dte'] is None, e['dte'] if e['dte'] is not None else 0))
    source_counts = {}
    category_counts = {}
    for event in events:
        source_counts[event['source']] = source_counts.get(event['source'], 0) + 1
        category_counts[event['category']] = category_counts.get(event['category'], 0) + 1
    dated_events = sum(1 for event in events if event.get('date') is not None or event.get('dte') is not None)
    news_events = [event for event in events if event.get('kind') == 'news']
    news_timestamped = sum(1 for event in news_events if event.get('date') is not None)
    keyword_impacts = sum(1 for event in news_events if event.get('impact_derivation') == 'keywords')

    return {
        'symbol': sym, 'as_of': as_of, 'n': len(events), 'events': events,
        'coverage': {
            'input_channels': {'news_provided': news is not None,
                               'earnings_provided': earnings is not None,
                               'macro_provided': macro is not None,
                               'anomaly_provided': anomaly is not None},
            'source_counts': source_counts, 'category_counts': category_counts,
            'dated_events': dated_events, 'undated_events': len(events) - dated_events,
            'news_timestamp_coverage': {'timestamped_news': news_timestamped,
                                        'total_news': len(news_events),
                                        'untimestamped_news': len(news_events) - news_timestamped,
                                        'coverage_pct': round(100 * news_timestamped / len(news_events), 1)
                                        if news_events else 0.0,
                                        'status': 'TIMESTAMP_COVERAGE_ONLY',
                                        'note': 'format d’horodatage non normalisé : aucun âge ou impact n’est déduit'},
            'news_impact_coverage': {'keyword_classified_news': keyword_impacts,
                                     'unclassified_news': len(news_events) - keyword_impacts,
                                     'total_news': len(news_events),
                                     'coverage_pct': round(100 * keyword_impacts / len(news_events), 1)
                                     if news_events else 0.0,
                                     'status': 'KEYWORD_DERIVATION_ONLY',
                                     'note': 'titre non classé = aucune interprétation d’impact créée'},
            'all_events_have_source': all(event.get('source') for event in events),
            'read_only': True,
            'note': 'canal absent, événement non daté ou sans mention de révision reste explicitement qualifié',
        },
        'revisions': ({'available': True, 'status': 'NEWS_MENTIONS_ONLY',
                       'mentions': revision_mentions,
                       'note': 'mentions de titres détectées ; pas de consensus ni révision confirmée'}
                      if revision_mentions else
                      {'available': False,
                       'reason': 'aucune mention de révision ni source de consensus branchée — jamais estimé'}),
        'generator': 'deterministic',
        'note': 'Timeline descriptive — un événement daté n’est pas un catalyseur par défaut ; '
                'impact suggéré uniquement par mots-clés transparents.',
    }


__all__ = ['build', 'DATE_PUBLIEE', 'DATE_INDICATIVE', 'fiabilite_de_date', 'peut_fonder_un_gate']
