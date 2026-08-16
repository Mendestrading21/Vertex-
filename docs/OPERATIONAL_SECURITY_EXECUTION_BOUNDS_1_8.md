# Vertex — sécurité opérationnelle et bornes d’exécution 1.8

## Validation d’identifiants

Les routes analytiques prioritaires `vertex`, `anomalies`, `evidence` et `skyler` valident désormais les symboles avant tout accès au scan ou calcul. Un symbole est normalisé en majuscules seulement s’il respecte la forme bornée `[A-Z0-9][A-Z0-9.-]{0,11}`. Les caractères ambigus, les séparateurs de chemin et les identifiants excédant douze caractères sont rejetés avec `400 symbole_invalide`; ils ne sont jamais tronqués.

## Borne de board options

Le scanner d’horizon traite au plus 5 000 contrats par appel. Cette limite protège les routes analytiques contre un board anormalement grand. Lorsque la limite est atteinte, la sortie contient `input_truncated`, `input_limit`, `input_contracts_inspected` et, quand disponible, `input_contracts_total`.

> Une troncature de board ne devient jamais une couverture supposée complète. Le garde-fou multi-actifs ajoute `OPTION_BOARD_TRUNCATED` et demande une revue, sans modifier le verdict Skyler.

## Intégrité de lecture

Ces protections bornent les entrées et le travail de calcul, mais ne transforment pas Vertex en système transactionnel. Les routes restent analytiques, les warnings restent descriptifs et aucun ordre ne peut être créé.
