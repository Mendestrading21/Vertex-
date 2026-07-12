"""vertex.market.news_impact — classification & importance (§15).

Classement par mots-clés déterministes (macro / politique / résultats /
guidance / secteur / entreprise) et score d'importance : corroborations,
entités du portefeuille concernées, catégorie. La direction d'impact reste
« potentielle » — jamais une causalité affirmée.
"""
from __future__ import annotations

_CATEGORIES = (
    ('MACRO', ('fed', 'fomc', 'cpi', 'inflation', 'rate', 'rates', 'yield',
               'treasury', 'jobs', 'payroll', 'gdp', 'pib', 'taux', 'bce', 'ecb')),
    ('POLITIQUE', ('trump', 'white house', 'congress', 'tariff', 'tarif',
                   'election', 'senate', 'regulation', 'antitrust', 'ban',
                   'sanction', 'gouvernement')),
    ('RESULTATS', ('earnings', 'résultats', 'revenue', 'profit', 'quarter',
                   'q1', 'q2', 'q3', 'q4', 'beats', 'misses', 'eps')),
    ('GUIDANCE', ('guidance', 'outlook', 'forecast', 'prévisions', 'raises',
                  'cuts', 'warns')),
    ('SECTEUR', ('semiconductor', 'chips', 'ai', 'artificial intelligence',
                 'cloud', 'energy', 'oil', 'banks', 'retail', 'pharma')),
)


def classify(title: str) -> str:
    t = (title or '').lower()
    for cat, words in _CATEGORIES:
        if any(w in t for w in words):
            return cat
    return 'ENTREPRISE'


def score_importance(event: dict, portfolio_syms: list[str]) -> int:
    """0-100 — déterministe : corroborations + portefeuille + catégorie."""
    score = 30
    score += min(30, 10 * (event.get('corroborations', 1) - 1))
    if any(s in portfolio_syms for s in event.get('entities', [])):
        score += 25
    if event.get('category') in ('MACRO', 'POLITIQUE'):
        score += 10
    if event.get('category') in ('RESULTATS', 'GUIDANCE'):
        score += 15
    senti = event.get('sentiment')
    if isinstance(senti, (int, float)) and abs(senti) >= 0.5:
        score += 5
    return min(100, score)


def potential_impact(event: dict) -> dict:
    """Direction POTENTIELLE (jamais « causera ») dérivée du sentiment fourni."""
    senti = event.get('sentiment')
    if not isinstance(senti, (int, float)):
        return {'direction': 'INCONNUE', 'confidence': 0.0}
    if senti > 0.15:
        return {'direction': 'POSITIF_POTENTIEL', 'confidence': min(0.7, abs(senti))}
    if senti < -0.15:
        return {'direction': 'NEGATIF_POTENTIEL', 'confidence': min(0.7, abs(senti))}
    return {'direction': 'NEUTRE', 'confidence': 0.3}


__all__ = ['classify', 'score_importance', 'potential_impact']
