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
que `tests/test_routes_company_parity.py` garde.

⛔ Lecture seule : aucune de ces routes ne prépare ni ne transmet d'ordre.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app.config import DEMO_MODE
from vertex.data import company as _company
from vertex.app import snapshot as _instantane
from vertex.data_sources import analyst_deep
from vertex.data_sources import sec_fondamentaux as _sec_f

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


#  ── SEC EDGAR : la seule source fondamentale DATEE du produit ───────────────
#
#  Elle etait ecrite, testee, et branchee NULLE PART. Les fondamentaux Reuters
#  sont refuses par le compte IBKR (10358) et `yfinance` n'expose aucune date
#  de publication : sans cette route, aucun fait fondamental du produit ne
#  peut dire ce qui etait connaissable a une date donnee.
#
#  Servie par le magasin d'instantanes, jamais en synchrone : un
#  `companyfacts` fait plusieurs mega-octets et se paie en secondes. La route
#  rend tout de suite ce qu'elle a et charge le reste EN FOND — c'est le
#  defaut P0.1, et on ne le rouvre pas pour une source de plus.
FRAICHEUR_SEC_S = 6 * 3600.0
PLAFOND_SEC_S = 48 * 3600.0
_MAGASIN_SEC = _instantane.Magasin('sec-fondamentaux')


@bp.route('/api/sec/fondamentaux/<sym>')
def api_sec_fondamentaux(sym):
    """Faits deposes a la SEC pour ce titre, chacun date de sa publication.

    Chaque fait porte DEUX dates : `observed_at` (la periode decrite) et
    `available_at` (le depot). Les confondre est exactement ce que la doctrine
    interdit — un retrotest qui daterait un resultat de sa periode emploierait
    un chiffre publie des semaines plus tard.
    """
    symbole = str(sym or '').upper()[:12]

    def _charger():
        r = _sec_f.fondamentaux(symbole)
        return r, {'source': 'SEC_EDGAR',
                   'qualite': 'MEASURED' if r.get('faits') else 'ABSENTE'}

    valeur, meta = _MAGASIN_SEC.servir(
        symbole, _charger, fraicheur_s=FRAICHEUR_SEC_S,
        plafond_s=PLAFOND_SEC_S, attendre=False)
    corps = dict(valeur or {'symbole': symbole, 'faits': []})
    corps['etat_fraicheur'] = {
        'etat': meta.etat,
        'age_s': meta.age_s,
        'chargement_en_cours': bool(getattr(meta, 'rafraichissement_en_cours', False)),
        'erreur': meta.erreur,
        'note': ('un premier appel sur un titre froid rend MISSING et charge en '
                 'fond : « aucun fait » signifie ici « pas encore », pas '
                 '« cette entreprise n a rien depose »'),
    }
    corps['read_only'] = True
    return jsonify(corps)


@bp.route('/api/sec/etat')
def api_sec_etat():
    """L'etat de la source — dont le drapeau et le contact, separement.

    `VERTEX_ENABLE_SEC` a longtemps figure dans un `.env` sans que RIEN ne le
    lise. Cette route rend la question verifiable depuis la page Systeme.
    """
    return jsonify(_sec_f.etat())


__all__ = ['bp']
