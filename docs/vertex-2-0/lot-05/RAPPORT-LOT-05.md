# Rapport — Lot 5 · Contrats instrument, source et unité

## Livré

L'enveloppe `ProvenancedValue` est portée au contrat canonique du skill
(`connection-and-resilience-matrix.md`) :

- **historiques, intouchés** : value · source · source_mode · timestamp ·
  age_seconds · quality · fallback_used · warnings ;
- **ajoutés (lot 5)** : `unit` · `currency` · `instrument_id` ·
  `observed_at`/`received_at` (séparer l'observation de la réception : leur
  écart est la latence, la confondre avec l'âge rend une donnée lente
  « fraîche ») · `entitlement` · `schema_version` (1.1) · `lineage` (chaque
  étape s'ajoute, aucune ne s'efface) · `error` (la panne est une donnée).

**Aucun défaut n'invente une valeur** : tous les nouveaux champs valent
None/''/[] à l'absence — une unité ou une devise par défaut serait une
invention. Gardé par le banc.

Le producteur central (`cotation_unifiee.resoudre_cotation`) pose désormais
`instrument_id`, `currency` (seulement si l'appelant la CONNAÎT — jamais un
USD supposé), `unit='prix'` et son `lineage`.

## Compatibilité prouvée

- le gardien historique `test_to_dict_contract_is_complete` épinglait le set
  EXACT des clés : étendu au nouveau contrat (pas affaibli — le set reste
  exact, une clé qui apparaît sans passer par ce banc est une dérive de
  schéma) ;
- `missing()` rend toujours None/MISSING — jamais un zéro ;
- toutes les fixtures passent sans modification.

## Hors lot, et dit

La migration des autres producteurs (fallback EOD, chaînes, historiques) se
fait route par route dans les lots de domaine ; la quarantaine et le snapshot
atomique appartiennent au lot 6.

## Preuves

Rouge d'abord (4 échecs mesurés), puis suite complète : voir commit.
