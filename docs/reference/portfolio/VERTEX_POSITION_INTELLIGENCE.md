# Vertex — Position Intelligence

Moteur central du cycle de vie analytique des positions (`vertex/positions`).
Chaîne : Détection → Validation → Réconciliation → Enrichissement → Calcul →
Analyse → Contrôle stratégique → Risque → Verdict → Explication → Alerte →
Snapshot → Historique → Interface.

⛔ **LECTURE SEULE ABSOLUE.** Aucun module ne contient de méthode d'exécution
(`place_order`, `close_position`, `auto_close`, `auto_reduce`…) — gardien
`test_no_order_path_in_positions_package`. Un verdict RÉDUIRE ou
SORTIE_ANALYTIQUE_PROPOSÉE est une recommandation ; aucune position réelle
n'est jamais clôturée automatiquement.

## Modules
`models` (canoniques), `repository` (sources), `reconciler` (§7),
`calculator` (§10-12), `lifecycle` (§14-15, matérialité, priorité, action),
`thesis_health` (§16), `detector` (Startup Report §6), `change_detector`
(§27), `alerts` (§29), `audit` (§41), `recalculator` (orchestrateur + verdict
ExecutiveEngine unique).

## API (lecture seule)
`/api/positions/state` · `/report` · `/audit` · `/reconcile` · `/alerts` ·
`/<id>/changes`.

## Invariant de vérité
Donnée absente → `None` (jamais 0). Cotation manquante → statut
`AWAITING_DATA` / `AWAITING_CONTRACT_DATA`, affiché honnêtement. IBKR hors
ligne → positions locales CONSERVÉES (jamais clôturées) et
`missing_positions = 0`.
