"""vertex/app/routes/company_api.py — API ENTREPRISE (profil, analystes, noms).

Extrait de `terminal.py` au titre de #779. Ces trois routes y étaient décorées
directement sur `app`, ce qui en faisait la seule surface du produit dont le
propriétaire était le monolithe et non un blueprint.

## Pourquoi ces trois-là en premier

Les dépendances des quatorze routes LEGACY ont été mesurées à l'AST. Celles-ci
sont les seules — avec `/api/track-record` — à ne dépendre de **rien d'autre que
`app`** : pas d'état local, pas de verrou, pas de fonction privée du monolithe.
Elles se déplacent donc **sans injection**, ce qui est la plus petite
convergence prouvable au sens du prompt maître.

`/api/track-record` reste pour l'instant dans `terminal.py` : elle appelle
l'auto-évaluation du moteur, qui relève de la mémoire et de la calibration
(#783). La ranger ici, ou dans `tracking_api` qui gère des suivis
*hypothétiques*, serait un mensonge de nommage.

## Contrat conservé à l'identique

Les trois vues gardent leur corps, leurs messages d'erreur et leur forme de
réponse. L'extraction déplace la propriété, **pas le comportement** — c'est ce
que `tests/test_vertex_1_0_routes_company_parity.py` garde.

⛔ Lecture seule : aucune de ces routes ne prépare ni ne transmet d'ordre.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app.config import DEMO_MODE
from vertex.data import company as _company
from vertex.data_sources import analyst_deep

bp = Blueprint('company_api', __name__)


@bp.route('/api/company/<sym>')
def api_company(sym):
    """Profil d'entreprise seul (cache hebdomadaire — activité, CEO, segments, pairs)."""
    try:
        return jsonify(_company.get(sym.upper(), demo=DEMO_MODE, brief=True))
    except Exception as e:
        return jsonify({'error': f'{type(e).__name__}: {e}'})


@bp.route('/api/analyst/<sym>')
def api_analyst(sym):
    """Données analystes PROFONDES à la demande (révisions BPA, surprises, notes,
    détention, initiés) — yfinance caché 12 h. En démo : rien (pas de réseau)."""
    if DEMO_MODE:
        return jsonify({'demo': True})
    try:
        return jsonify(analyst_deep.get(sym.upper()) or {})
    except Exception as e:
        return jsonify({'error': f'{type(e).__name__}: {e}'})


@bp.route('/api/names')
def api_names():
    """{ticker: nom d'entreprise} depuis le cache — pour afficher les noms dans Stock info
    (lecture seule, instantané, aucun fetch réseau)."""
    try:
        cache = _company._load()
        return jsonify({k: v.get('name') for k, v in cache.items()
                        if isinstance(v, dict) and v.get('name')})
    except Exception:
        return jsonify({})


__all__ = ['bp']
