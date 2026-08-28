"""vertex.research.multiplicity — correction de la multiplication des essais.

Pipeline anti-illusion (point 10) : tester 50 stratégies à α = 5 % produit
~2,5 « découvertes » par pur hasard. Le registre conserve TOUS les essais
(rejetés compris) précisément pour que ce nombre soit connu ; ce module en
tire le seuil corrigé (Bonferroni — conservateur, simple, sans hypothèse
de dépendance) et un jugement honnête qui nomme la correction appliquée.

Aucun classement, aucune promesse : une p-value « significative » sous
correction reste une PREUVE PARTIELLE, jamais un verdict financier.
"""
from __future__ import annotations


def seuil_corrige(alpha: float, n_essais: int) -> float:
    """Seuil de Bonferroni : α / n. `n_essais` = essais TENTÉS (rejetés compris)."""
    if not isinstance(n_essais, int) or n_essais < 1:
        raise ValueError('n_essais doit être un entier ≥ 1 — le nombre '
                         'd\'essais TENTÉS, jamais 0')
    if not (0 < alpha < 1):
        raise ValueError('alpha doit être dans (0, 1)')
    return alpha / n_essais


def jugement(*, p_value: float, alpha: float = 0.05, n_essais: int = 1) -> dict:
    """Jugement honnête d'une p-value sous multiplicité."""
    seuil = seuil_corrige(alpha, n_essais)
    ok = p_value < seuil
    return {
        'significatif': bool(ok),
        'p_value': p_value,
        'alpha': alpha,
        'n_essais': n_essais,
        'seuil_corrige': seuil,
        'methode': 'bonferroni',
        'note': ('p=%.4g comparée au seuil %.4g (α=%.2g corrigé pour %d essais '
                 'tentés, rejetés compris). %s' % (
                     p_value, seuil, alpha, n_essais,
                     'Sous le seuil corrigé — preuve partielle, pas un verdict.'
                     if ok else
                     'Au-dessus du seuil corrigé — indiscernable du hasard '
                     'après multiplicité.')),
    }


__all__ = ['seuil_corrige', 'jugement']
