"""vertex/engines/events.py — TIMELINE D'ÉVÉNEMENTS NORMALISÉE (SKYLER LOT 4).

Agrège en UNE forme canonique les événements réels d'un titre déjà produits
ailleurs (news assainies, earnings du calendrier, macro datée, anomalies
statistiques). Chaque événement porte :

  {kind, label, date, dte, category: 'fact'|'interpretation', source,
   impact_hint, impact_derivation, importance, confidence}

Règles d'honnêteté :
  - la PUBLICATION d'une news est un fait ; son IMPACT ne l'est pas — il n'est
    suggéré (`impact_hint`) que par des mots-clés DÉTERMINISTES et transparents
    (`impact_derivation: 'keywords'`), sinon None ;
  - une anomalie statistique est une INTERPRÉTATION (confiance EXACT_STATISTICAL :
    z-scores exacts) ; une date de calendrier est un fait DÉCLARÉ ;
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


def _ev(kind, label, category, source, date=None, dte=None, impact_hint=None,
        impact_derivation=None, importance=None, confidence=None):
    return {'kind': kind, 'label': label, 'category': category, 'source': source,
            'date': date, 'dte': dte, 'impact_hint': impact_hint,
            'impact_derivation': impact_derivation, 'importance': importance,
            'confidence': confidence}


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
        events.append(_ev('macro', m['label'], 'fact', 'calendar.macro',
                          date=m.get('date'), dte=m.get('dte'),
                          impact_hint=(m.get('kind') or None),
                          impact_derivation=('calendar' if m.get('kind') else None),
                          importance=m.get('importance'), confidence='DECLARED'))

    revision_mentions = []
    for n in dedupe_news(news or []):
        title = n.get('title')
        if not title:
            continue
        hint, deriv = _impact_from_title(title)
        if hint == 'RATING':
            revision_mentions.append({'title': title, 'source': 'news.%s' % (n.get('publisher') or 'externe'),
                                      'date': n.get('time'), 'derivation': 'title_keywords'})
        events.append(_ev('news', title, 'fact',
                          'news.%s' % (n.get('publisher') or 'externe'),
                          date=n.get('time'), dte=None,
                          impact_hint=hint, impact_derivation=deriv,
                          confidence=None))

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


__all__ = ['build']
