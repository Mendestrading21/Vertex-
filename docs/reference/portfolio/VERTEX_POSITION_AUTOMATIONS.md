# Vertex — Automatisations positions (§39)

Jobs enregistrés au scheduler central (`vertex/scheduler/registry.py`),
visibles dans Système → Automatisations :
STARTUP_POSITION_SYNC · OPEN_POSITION_REFRESH · OPEN_OPTION_REFRESH ·
MATERIAL_POSITION_RECALCULATION · THESIS_HEALTH_REVIEW ·
EOD_POSITION_SNAPSHOT · POSITION_INTEGRITY_AUDIT.

Fréquences adaptatives (§24) : positions proches du stop en priorité,
positions stables au ralenti, ne pas surcharger IBKR. Recalcul déclenché
sur changement matériel (§25-26), jamais sur microvariation.
