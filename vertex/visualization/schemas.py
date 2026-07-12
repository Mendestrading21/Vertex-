"""vertex.visualization.schemas — contrat canonique d'interprétation (§6).

Un « graphique » Vertex n'est pas qu'un dessin : c'est une paire
(données, interprétation). L'interprétation est un dictionnaire au format
STRICT ci-dessous, produit côté serveur, jamais inventé côté client.

Champs :
  chart_id          identifiant stable du graphique (ex. 'options.iv_term')
  question          LA question à laquelle le graphique répond (une phrase)
  dominant_reading  lecture dominante en une phrase claire
  status            FAVORABLE | NEUTRE | DEFAVORABLE | BLOQUANT | INCONNU
  confidence        0..1 (None si non mesurable) — jamais gonflé
  positive_evidence liste de faits qui soutiennent une lecture favorable
  negative_evidence liste de faits qui pèsent contre
  uncertainties     liste des zones d'ombre / données manquantes
  strategy_impact   ce que ça change concrètement pour la décision
  source            provenance des données (IBKR, MODEL_ESTIMATE, DESK…)
  as_of             horodatage ISO de la donnée (None si inconnu)
  limitations       limites méthodologiques honnêtes (§6.8)
"""
from __future__ import annotations

ST_FAVORABLE = 'FAVORABLE'
ST_NEUTRE = 'NEUTRE'
ST_DEFAVORABLE = 'DEFAVORABLE'
ST_BLOQUANT = 'BLOQUANT'
ST_INCONNU = 'INCONNU'

STATUSES = (ST_FAVORABLE, ST_NEUTRE, ST_DEFAVORABLE, ST_BLOQUANT, ST_INCONNU)

_REQUIRED = ('chart_id', 'question', 'dominant_reading', 'status',
             'positive_evidence', 'negative_evidence', 'uncertainties',
             'strategy_impact', 'source', 'as_of', 'limitations')


def _clean_list(x) -> list:
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return [str(i) for i in x if i not in (None, '')]
    return [str(x)]


def _clamp_conf(c):
    if c is None:
        return None
    try:
        c = float(c)
    except (TypeError, ValueError):
        return None
    return round(max(0.0, min(1.0, c)), 3)


def interpretation(chart_id: str, question: str, dominant_reading: str,
                   status: str, *, confidence=None, positive_evidence=None,
                   negative_evidence=None, uncertainties=None,
                   strategy_impact='', source='', as_of=None,
                   limitations=None) -> dict:
    """Construit une interprétation canonique validée et normalisée.

    Statut inconnu forcé si la lecture dominante est vide (règle de vérité :
    on ne rend pas un verdict sans matière)."""
    status = status if status in STATUSES else ST_INCONNU
    if not str(dominant_reading or '').strip():
        status = ST_INCONNU
    return {
        'chart_id': str(chart_id),
        'question': str(question),
        'dominant_reading': str(dominant_reading or ''),
        'status': status,
        'confidence': _clamp_conf(confidence),
        'positive_evidence': _clean_list(positive_evidence),
        'negative_evidence': _clean_list(negative_evidence),
        'uncertainties': _clean_list(uncertainties),
        'strategy_impact': str(strategy_impact or ''),
        'source': str(source or ''),
        'as_of': as_of,
        'limitations': _clean_list(limitations),
    }


def unknown(chart_id: str, question: str, *, reason='données indisponibles',
            source='', limitations=None) -> dict:
    """Interprétation INCONNU honnête — la donnée manque, on ne devine pas."""
    return interpretation(
        chart_id, question,
        dominant_reading='',
        status=ST_INCONNU,
        uncertainties=[reason],
        strategy_impact='Aucun impact décisionnel : donnée insuffisante.',
        source=source, as_of=None, limitations=limitations)


def is_valid_interpretation(d) -> bool:
    """Vrai si d respecte le contrat canonique (clés + types de base)."""
    if not isinstance(d, dict):
        return False
    for k in _REQUIRED:
        if k not in d:
            return False
    if d['status'] not in STATUSES:
        return False
    for k in ('positive_evidence', 'negative_evidence', 'uncertainties',
              'limitations'):
        if not isinstance(d[k], list):
            return False
    c = d.get('confidence')
    if c is not None and not isinstance(c, (int, float)):
        return False
    return True


__all__ = [
    'STATUSES', 'ST_FAVORABLE', 'ST_NEUTRE', 'ST_DEFAVORABLE', 'ST_BLOQUANT',
    'ST_INCONNU', 'interpretation', 'unknown', 'is_valid_interpretation',
]
