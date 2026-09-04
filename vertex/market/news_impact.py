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
    """0-100 — déterministe : corroborations + portefeuille + catégorie.

    LOT 609 — CE QUE LE SEUIL DE SENTIMENT DISCRIMINE VRAIMENT. Le seul
    producteur de `sentiment` (`news_plus.sentiment`) rend EXACTEMENT -1, 0 ou
    +1. Sur ce domaine, `abs(senti) >= 0.5` ne sépare PAS le fort du faible :
    il sépare seulement le SIGNÉ du NEUTRE — vérifié par énumération exhaustive
    du domaine. Le seuil est conservé tel quel (il resterait correct si une
    source continue apparaissait) mais il ne mesure aucune intensité aujourd'hui.
    """
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
    """Direction POTENTIELLE (jamais « causera ») dérivée du sentiment fourni.

    LOT 609 — `confidence` N'EST PAS UNE MESURE AUJOURD'HUI. `min(0.7, abs(senti))`
    a l'air calculé ; sur le domaine réel du producteur ({-1, 0, +1}) il ne prend
    QU'UNE valeur par direction : 0.7 pour un signe, 0.3 pour le neutre. C'est un
    littéral déguisé en calcul.

    Rien n'est changé au comportement — cette valeur n'est affichée nulle part
    (seule `direction` l'est, dans l'« Actualité dominante » de `/`), et lui
    inventer une amplitude serait ajouter de la fausse précision. Ce qui est
    corrigé, c'est le SILENCE : quiconque rendra `sentiment` continu doit savoir
    que ces seuils et cette confiance ont été écrits pour un continuum qu'ils
    n'ont jamais reçu. Gardien : `tests/test_sentiment_contrat.py`.
    """
    senti = event.get('sentiment')
    if not isinstance(senti, (int, float)):
        return {'direction': 'INCONNUE', 'confidence': 0.0}
    if senti > 0.15:
        return {'direction': 'POSITIF_POTENTIEL', 'confidence': min(0.7, abs(senti))}
    if senti < -0.15:
        return {'direction': 'NEGATIF_POTENTIEL', 'confidence': min(0.7, abs(senti))}
    return {'direction': 'NEUTRE', 'confidence': 0.3}


__all__ = ['classify', 'score_importance', 'potential_impact']
