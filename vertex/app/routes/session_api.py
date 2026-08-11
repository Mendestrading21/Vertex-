"""
vertex/app/routes/session_api.py — SESSION D'ANALYSE (Blueprint).

Expose la « session d'analyse toujours ouverte » : un digest de commandement
assemblé depuis l'état DÉJÀ calculé (`scan_state` + `cal_state`) par
`vertex.engines.session_digest`. Aucun nouveau calcul, aucun ordre.

Vitesse / disponibilité instantanée :
- Le dernier digest « ready » est mémorisé (mémoire + disque `session_digest.json`).
- Au démarrage à froid (scan pas encore publié), on ressert l'instantané disque
  marqué `state='restored'` → l'écran est peuplé immédiatement, honnêtement daté.
- Écriture disque throttlée (best-effort) pour ne pas marteler le FS.

GET /api/session/digest — le digest courant (ou l'instantané restauré).
"""
from __future__ import annotations

import time

from flask import Blueprint, jsonify

from vertex.app.state import scan_state, cal_state
from vertex.app.config import DEMO_MODE
from vertex.engines import session_digest, session_snapshot
from vertex.services import persist

bp = Blueprint('session_api', __name__)

_SNAPSHOT_FILE = 'session_digest_cache.json'      # *_cache.json → gitignoré (runtime)
_WRITE_EVERY_S = 30

# Instantané le plus récent (restauré du disque au chargement du module → prêt tout de suite).
_last = {'digest': persist.load_json(_SNAPSHOT_FILE, None), 'written': 0.0}


@bp.route('/api/session/digest')
def api_session_digest():
    """Digest de la session d'analyse. Lecture seule ; jamais de donnée inventée."""
    d = session_digest.build(scan_state, cal_state, demo=DEMO_MODE)

    if d.get('state') == 'ready':
        _last['digest'] = d
        now = time.time()
        if now - _last['written'] > _WRITE_EVERY_S:      # persistance best-effort throttlée
            persist.save_json(_SNAPSHOT_FILE, d)
            _last['written'] = now
        return jsonify(d)

    # Scan pas encore publié : ressert le dernier instantané connu, marqué honnêtement.
    snap = _last.get('digest')
    if snap:
        restored = dict(snap)
        restored['state'] = 'restored'
        # HONNÊTETÉ : l'âge figé au build sous-estimerait la vraie ancienneté d'un
        # instantané restauré (potentiellement d'une exécution précédente). On l'efface
        # → le client n'affiche que l'horodatage absolu `as_of`, jamais un âge faussement frais.
        restored['age_s'] = None
        return jsonify(restored)

    return jsonify(d)      # première session à froid, rien à restaurer → 'analyzing'


@bp.route('/api/session/manifest')
def api_session_manifest():
    """Manifest de la session d'analyse : session_id + intégrité (couverture, qualité,
    statut, fraîcheur). Le client s'en sert pour détecter une NOUVELLE session et
    basculer atomiquement. Lecture seule ; jamais de donnée inventée."""
    return jsonify(session_snapshot.build(scan_state))


__all__ = ['bp']
