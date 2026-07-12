"""vertex.scheduler.registry — registre des jobs de fond (§24).

Les boucles historiques de terminal.py restent les exécutants (aucun
re-threading risqué) : elles se DÉCLARENT ici et émettent un battement
(`beat`) à chaque exécution. Le registre expose statut, dernière exécution,
prochaine exécution estimée, durée et dernier résultat — pour la vue
Système/Automatisations et le rapport de démarrage. Priorité produit :
positions ouvertes > stops > options > risques > décisions > opportunités >
univers (l'ordre d'affichage reflète cette priorité).
"""
from __future__ import annotations

import time
import threading

_LOCK = threading.Lock()

# Jobs canoniques (nom → métadonnées). interval_s = cadence NOMINALE de la
# boucle historique ; les jobs « événement » ont interval_s None.
_JOBS: dict[str, dict] = {}

_CANONICAL = (
    ('STARTUP_HEALTH_CHECK', 'Vérification des connexions au démarrage', None),
    ('POSITION_REFRESH', 'Cotation des positions déclarées (pos-quotes)', 45),
    ('OPTION_POSITION_REFRESH', 'Chaînes options IBKR (lecture seule)', 300),
    ('MARKET_DATA_REFRESH', 'Scan univers + indices + contexte marché', 360),
    ('PORTFOLIO_RECALCULATION', 'Risque portefeuille sur positions réelles', None),
    ('DECISION_RECALCULATION', 'Décisions exécutives (par requête/à la demande)', None),
    ('CATALYST_REFRESH', 'Calendrier earnings + macro', 3600),
    ('NEWS_REFRESH', 'Fil de nouvelles assaini', 900),
    ('PREMARKET_BRIEF', 'Brief pré-marché', None),
    ('INTRADAY_BRIEF', 'Brief intraday', None),
    ('CLOSE_BRIEF', 'Brief de clôture', None),
    ('EOD_SNAPSHOT', 'Instantané de fin de journée (track record)', 86400),
    ('WEEKLY_REVIEW', 'Sélection & revue hebdomadaire', 604800),
    ('SYSTEM_AUDIT', 'Diagnostics système', None),
    ('DATA_BACKUP', 'Backup quotidien du desk (rotation 7)', 86400),
    ('TRACK_RECORD_UPDATE', 'Mise à jour de la fiabilité mesurée', 86400),
    ('ALERTS_EVALUATION', 'Évaluation serveur des alertes utilisateur', 60),
    # Position Intelligence (§39) — cycle de vie analytique des positions.
    ('STARTUP_POSITION_SYNC', 'Détection & réconciliation des positions au démarrage', None),
    ('OPEN_POSITION_REFRESH', 'Cotation des positions actions ouvertes', 45),
    ('OPEN_OPTION_REFRESH', 'Cotation des positions options ouvertes', 60),
    ('MATERIAL_POSITION_RECALCULATION', 'Recalcul après changement matériel', None),
    ('THESIS_HEALTH_REVIEW', 'Réévaluation de la santé des thèses', None),
    ('EOD_POSITION_SNAPSHOT', 'Instantané de fin de journée des positions', 86400),
    ('POSITION_INTEGRITY_AUDIT', 'Audit d’intégrité des positions', None),
)

for name, desc, interval in _CANONICAL:
    _JOBS[name] = {'name': name, 'description': desc, 'interval_s': interval,
                   'last_run': None, 'last_ok': None, 'last_error': None,
                   'runs': 0, 'last_duration_ms': None}


def beat(name: str, ok: bool = True, error: str | None = None,
         duration_ms: float | None = None) -> None:
    """Battement émis par une boucle historique après une exécution."""
    with _LOCK:
        j = _JOBS.setdefault(name, {'name': name, 'description': '', 'interval_s': None,
                                    'last_run': None, 'last_ok': None, 'last_error': None,
                                    'runs': 0, 'last_duration_ms': None})
        j['last_run'] = time.time()
        j['last_ok'] = bool(ok)
        j['last_error'] = (str(error)[:200] if error else None)
        j['runs'] += 1
        if duration_ms is not None:
            j['last_duration_ms'] = round(duration_ms)


def jobs() -> list[dict]:
    """Snapshot trié par priorité produit (ordre canonique)."""
    now = time.time()
    out = []
    with _LOCK:
        for name, _, _ in _CANONICAL:
            j = dict(_JOBS[name])
            if j['last_run'] and j['interval_s']:
                j['next_run_eta_s'] = max(0, round(j['last_run'] + j['interval_s'] - now))
            else:
                j['next_run_eta_s'] = None
            j['age_s'] = round(now - j['last_run']) if j['last_run'] else None
            out.append(j)
    return out


class _Registry:
    beat = staticmethod(beat)
    jobs = staticmethod(jobs)


registry = _Registry()

__all__ = ['registry', 'jobs', 'beat']
