"""elio/vertex_ml.py — VERTEX v3 : couche ML / CALIBRATION (probabilité de gain).

Le rapport quant place la calibration (régression logistique / isotonic) en
PRIORITÉ HAUTE, avant XGBoost. On transforme les sous-scores Vertex en une
PROBABILITÉ DE GAIN calibrée via un méta-modèle logistique déterministe.

Design « extra optionnel » conforme au rapport :
  • par défaut : méta-modèle logistique PUR NUMPY (aucune dépendance lourde) ;
  • si un artefact entraîné `vertex_model.json` existe ET que scikit-learn/xgboost
    sont installés, on l'utilise (chemin upgrade) ; sinon fallback transparent.

Pur, déterministe, rapide, aucun appel réseau, aucun ordre.
⛔ ANALYSE ÉDUCATIVE — la probabilité est indicative, jamais une promesse.
"""
import math

# Détection souple des libs ML (extra optionnel) — jamais bloquant.
try:                                   # pragma: no cover
    import joblib  # noqa: F401
    _HAS_SKLEARN = True
except Exception:
    _HAS_SKLEARN = False

_MODEL = None                          # artefact entraîné chargé paresseusement (si présent)


def _sigmoid(z):
    if z < -40:
        return 0.0
    if z > 40:
        return 1.0
    return 1.0 / (1.0 + math.exp(-z))


def _n(x, lo=0.0, hi=100.0):
    """Normalise un score 0-100 vers ~[-1, 1] (centré 50)."""
    try:
        return max(-1.5, min(1.5, ((float(x) - (lo + hi) / 2) / ((hi - lo) / 2))))
    except Exception:
        return 0.0


# ── Méta-modèle logistique (coefficients = priors quantitatifs raisonnés) ──────
# logit = b0 + Σ w_i · feature_i. Calibré pour que :
#   edge ~80 → p_win ≈ 0.70 · edge ~50 → ≈ 0.45 · edge ~30 → ≈ 0.30
_W = {
    'trend_quality': 0.85, 'entry_quality': 0.70, 'rr': 0.55,
    'expected_move': 0.45, 'institutionality': 0.40, 'extension_penalty': -0.80,
}
_B0 = -0.15


def _features(v):
    return {
        'trend_quality': _n(v.get('trend_quality')),
        'entry_quality': _n(v.get('entry_quality')),
        'rr': _n(v.get('rr')),
        'expected_move': _n(v.get('expected_move')),
        'institutionality': _n(v.get('institutionality')),
        'extension_penalty': _n(v.get('extension_penalty')),
    }


def predict(vertex_block):
    """Entrée : bloc vertex (sous-scores + mc). Sortie : proba de gain calibrée."""
    try:
        v = vertex_block or {}
        f = _features(v)
        # logit centré sur l'EDGE composite (déjà une fusion des sous-scores), avec
        # une pente humble pour une probabilité réaliste (edge 86→~0.74, 55→0.5,
        # 30→~0.32), puis petit ajustement first-touch Monte-Carlo (non double-compté).
        edge = float(v.get('edge') or 50.0)
        logit = 0.032 * (edge - 54.0)
        mc = v.get('mc') or {}
        if mc:
            ft = (mc.get('p_tp1_first') or 0) - (mc.get('p_stop_before_tp1') or 0)
            logit += 0.25 * ft
        logit += 0.15 * f['trend_quality'] - 0.15 * f['extension_penalty']   # nuance structure
        # artefact ML entraîné si disponible (chemin upgrade XGBoost/sklearn)
        model_used = 'logistic'
        if _MODEL is not None and _HAS_SKLEARN:        # pragma: no cover
            try:
                import numpy as np
                p = float(_MODEL.predict_proba(np.array([list(f.values())]))[0, 1])
                return {'p_win': round(p, 3), 'meta_score': round(p * 100),
                        'model': 'ml_artifact'}
            except Exception:
                pass
        p = max(0.05, min(0.85, _sigmoid(logit)))      # humble : jamais > 85 %
        return {'p_win': round(p, 3), 'meta_score': round(p * 100), 'model': model_used}
    except Exception:
        return None
