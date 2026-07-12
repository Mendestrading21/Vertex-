"""vertex.visualization.chart_spec — objet canonique de graphique (§5).

Un graphique majeur n'est pas qu'une série de points : c'est un objet complet
qui porte sa question, ses données, sa provenance, sa qualité et son
interprétation. Ce module construit et valide cet objet — surcouche du contrat
d'interprétation (`schemas.py`). Donnée absente → statut INCONNU, jamais un
chiffre inventé. Lecture seule.
"""
from __future__ import annotations

from .schemas import STATUSES, ST_INCONNU, _clean_list, _clamp_conf

# Types de graphiques reconnus (grammaire visuelle §4).
CHART_TYPES = (
    'line', 'area', 'candlestick', 'bar', 'diverging_bar', 'stacked_bar',
    'heatmap', 'scatter', 'bubble', 'radar', 'gauge', 'sankey', 'waterfall',
    'treemap', 'fan', 'cone', 'donut', 'sparkline',
)

# Niveaux de fraîcheur / qualité de donnée (§30).
FRESHNESS = ('LIVE', 'DELAYED', 'STALE', 'FALLBACK', 'DEMO', 'MISSING', 'UNKNOWN')
QUALITY = ('HIGH', 'MEDIUM', 'LOW', 'DEGRADED', 'UNKNOWN')

_REQUIRED = ('id', 'title', 'question', 'chart_type', 'series', 'source',
             'as_of', 'freshness', 'quality', 'dominant_reading',
             'strategy_impact', 'confirmation', 'invalidation',
             'uncertainties', 'status', 'confidence')


def chart_spec(chart_id, title, question, chart_type, *, series=None,
               source=None, as_of=None, freshness='UNKNOWN', quality='UNKNOWN',
               dominant_reading='', strategy_impact='', confirmation=None,
               invalidation=None, uncertainties=None, status=ST_INCONNU,
               confidence=None) -> dict:
    """Construit un objet graphique canonique validé et normalisé.

    `series` : liste de séries (chaque item libre, mais idéalement
    {name,color,role,points}). Lecture vide ou aucune série exploitable ⇒
    statut forcé INCONNU (règle de vérité)."""
    ct = chart_type if chart_type in CHART_TYPES else 'line'
    fr = freshness if freshness in FRESHNESS else 'UNKNOWN'
    ql = quality if quality in QUALITY else 'UNKNOWN'
    st = status if status in STATUSES else ST_INCONNU
    series = list(series) if series else []
    if not str(dominant_reading or '').strip() or not series:
        st = ST_INCONNU
    return {
        'id': str(chart_id),
        'title': str(title),
        'question': str(question),
        'chart_type': ct,
        'series': series,
        'source': _clean_list(source),
        'as_of': as_of,
        'freshness': fr,
        'quality': ql,
        'dominant_reading': str(dominant_reading or ''),
        'strategy_impact': str(strategy_impact or ''),
        'confirmation': _clean_list(confirmation),
        'invalidation': _clean_list(invalidation),
        'uncertainties': _clean_list(uncertainties),
        'status': st,
        'confidence': _clamp_conf(confidence),
    }


def empty_spec(chart_id, title, question, chart_type, *,
               reason='données indisponibles', source=None,
               freshness='MISSING') -> dict:
    """Graphique canonique en état vide honnête (aucune donnée exploitable)."""
    return chart_spec(chart_id, title, question, chart_type, series=[],
                      source=source, freshness=freshness, quality='UNKNOWN',
                      dominant_reading='', status=ST_INCONNU,
                      uncertainties=[reason],
                      strategy_impact='Aucun impact : donnée insuffisante.')


def is_valid_chart_spec(d) -> bool:
    if not isinstance(d, dict):
        return False
    for k in _REQUIRED:
        if k not in d:
            return False
    if d['chart_type'] not in CHART_TYPES:
        return False
    if d['status'] not in STATUSES:
        return False
    if d['freshness'] not in FRESHNESS or d['quality'] not in QUALITY:
        return False
    for k in ('series', 'source', 'confirmation', 'invalidation', 'uncertainties'):
        if not isinstance(d[k], list):
            return False
    return True


__all__ = ['chart_spec', 'empty_spec', 'is_valid_chart_spec',
           'CHART_TYPES', 'FRESHNESS', 'QUALITY']
