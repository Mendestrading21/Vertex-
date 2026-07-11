"""vertex.portfolio.replacement_engine — remplacements dans l'équipe (§25)."""
from __future__ import annotations

from .team_engine import candidate_fit


def propose_replacement(snapshot, profile, candidate: dict,
                        scores_by_symbol: dict | None = None) -> dict:
    """Si le portefeuille est plein, propose la position la plus faible du même
    rôle comme remplacement candidat — PROPOSITION seulement, jamais exécutée."""
    fit = candidate_fit(snapshot, profile, candidate)
    out = {'fit': fit, 'replacement_candidate': None, 'notes': []}
    if not fit['blocked']:
        out['notes'].append('place disponible — pas de remplacement nécessaire')
        return out
    scores = scores_by_symbol or {}
    role = candidate.get('role')
    same_role = [p for p in snapshot.positions if p.role == role]
    pool = same_role or list(snapshot.positions)
    if not pool:
        out['notes'].append('aucune position à remplacer')
        return out
    weakest = min(pool, key=lambda p: scores.get(p.symbol, 50))
    cand_score = scores.get(candidate.get('symbol'), None)
    weakest_score = scores.get(weakest.symbol, None)
    out['replacement_candidate'] = {'symbol': weakest.symbol, 'role': weakest.role,
                                    'score': weakest_score}
    if cand_score is not None and weakest_score is not None \
            and cand_score <= weakest_score:
        out['notes'].append(f'le candidat ({cand_score}) n’améliore pas la plus faible '
                            f'position du rôle ({weakest.symbol}: {weakest_score}) — '
                            'remplacement déconseillé')
    else:
        out['notes'].append(f'remplacement proposé: {weakest.symbol} → '
                            f"{candidate.get('symbol')} (décision humaine requise)")
    return out
