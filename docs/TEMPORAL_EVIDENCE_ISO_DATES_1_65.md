# Vertex — Dates ISO canoniques pour les preuves temporelles

Le moteur d’analyse conserve désormais les dates de la série OHLC dans `series.dates` au format **ISO `YYYY-MM-DD`**. Cette forme est exploitable par les contrôles de continuité chronologique, de stress historique et de rupture de régime.

Les libellés courts destinés à l’affichage sont séparés dans `series.date_labels` au format `MM-JJ`. Cette séparation évite qu’un libellé visuel incomplet soit interprété comme une preuve de date.

> Les prix et volumes observés ne sont ni interpolés ni recalculés. La correction ne modifie aucun score, gate, verdict ou mécanisme d’exécution : Vertex demeure un outil d’analyse en lecture seule.
