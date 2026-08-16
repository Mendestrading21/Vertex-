# Contrat d’intégration Claude ↔ Vertex Intelligence

## But

Claude peut modifier la présentation, mais ne doit jamais recalculer le score, modifier une gate ou reconstruire un verdict. Les données d’intelligence sont fournies par les routes Python existantes et restent exclusivement en lecture seule.

## Route de référence

`GET /api/skyler/<SYMBOL>` retourne le packet, la décision, la revue red-team et les diagnostics de calibration. Depuis cette itération, `decision.readiness` constitue le contrat de présentation stable pour l’état de préparation analytique.

| Champ | Type | Règle d’affichage |
|---|---|---|
| `decision.decision` | chaîne | Afficher tel quel : ne pas le traduire en instruction d’ordre. |
| `decision.capped_by_gate` | chaîne ou `null` | Si renseigné, le présenter avant le score. |
| `decision.gates` | liste | Conserver les trois états `true`, `false`, `null`. `null` signifie « non évaluable », pas « conforme ». |
| `decision.readiness.status` | chaîne | Utiliser pour le résumé : `BLOCKED_BY_GATE`, `EVIDENCE_REQUIRED`, `SCORE_INCOMPLETE` ou `ANALYTICAL_REVIEW_READY`. |
| `decision.readiness.actions` | liste | Afficher les actions de collecte/résolution comme diagnostics, jamais comme actions de trading. |
| `decision.option_calibration` | objet | Toujours conserver le label `DIRECTIONAL_PROXY_ONLY` tant que le P&L de contrat n’est pas mesuré. |
| `decision.opportunity_attribution` | objet | Présenter drivers, faiblesses, gates et preuves manquantes sans transformer ce diagnostic en ordre. |
| `decision.performance_monitor` | objet | Afficher comme surveillance descriptive ; ne jamais le représenter comme une recalibration automatique. |
| `decision.opportunity_reliability` | objet | Expliquer la qualité des preuves et de la cohorte, sans remplacer le verdict ni appeler à l’exécution. |
| `decision.instrument_profile` | objet | Afficher la classe et la source de classification ; `UNKNOWN` ne doit jamais être remplacé par une classe présumée. |
| `decision.sector_coherence` | objet | Afficher comme comparaison descriptive du scan sectoriel ; ne pas l’interpréter comme une instruction d’allocation. |
| `decision.portfolio.asset_mix` | objet | Afficher les poids des types d’actifs déclarés ; conserver `UNCLASSIFIED` lorsque le type n’est pas prouvé. |
| `decision.multi_asset_guard` | objet | Présenter les preuves multi-actifs manquantes comme une revue requise ; ce bloc ne remplace ni les gates ni le verdict. |
| `GET /api/skyler/health` | objet | Afficher seulement comme état technique non sensible ; ne jamais afficher ou déduire les contenus de cache. |
| `decision.multi_asset_guard.issues` | liste | Afficher `OPTION_BOARD_TRUNCATED` comme couverture options partielle ; ne pas la masquer ni la convertir en conformité. |

## Invariants à ne pas casser

1. Une gate `triggered=None` doit rester visuellement distincte d’une gate `False`.
2. Les données `PARTIAL_MANDATE` et `OUT_OF_MANDATE` ne doivent pas être masquées par un score de qualité.
3. La bannière « analyse lecture seule » doit rester visible ; aucune UI ne doit ajouter un bouton d’ordre, de broker ou d’exécution.
4. Le contrat de quote options résout le contrat par `SYM|EXP|STRIKE|C/P`, jamais par symbole seul. Une quote absente devient `DATA_REQUIRED`.
5. Le champ `cost` historique n’est jamais présenté comme une quote de marché actuelle sans source explicite.
6. `GET /api/skyler/monitor?horizon=H5|H10|H15|H20|H60` reste indisponible sous son seuil d’échantillon ; `INSUFFICIENT_SAMPLE` n’est jamais traduit par « performance stable ».
7. `GET /api/tracking/options/cohort` ne présente les métriques d’une cohorte ou d’un segment que lorsque son champ `available` vaut `true` ; le périmètre affiché reste hypothétique.

## Séparation des responsabilités

| Domaine | Responsable | Fichiers de référence |
|---|---|---|
| Décision, score, gates et calibration | Vertex Intelligence | `vertex/engines/`, `vertex/options/` |
| API analytique et contrats JSON | Vertex Intelligence | `vertex/app/routes/analysis_api.py`, `tracking_api.py` |
| Design, libellés et composants | Claude / branche design | `vertex/ui/`, `vertex/static/` |

Cette séparation minimise les conflits Git : les composants de design consomment les structures JSON sans modifier les moteurs de décision.
