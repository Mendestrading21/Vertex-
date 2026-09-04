# Vertex — Renforcement de l’intelligence 1.1

## Finalité

Cette évolution renforce l’intelligence **en lecture seule** de Vertex. Elle n’ajoute aucune exécution d’ordres, aucun formulaire de transaction et aucun mécanisme de transmission à un courtier.

## Qualité et réconciliation désormais obligatoires

Skyler ne mesure plus la qualité des données au nombre de modules visibles. Une décision doit recevoir une preuve explicite de qualité (`AnalyticsPacket` ou détail enrichi) et un rapport de réconciliation actionnable. Si la qualité, la fraîcheur ou la réconciliation est absente ou dégradée, le bloc `data_quality` est insuffisant et la gate `DATA_QUALITY_CRITICAL` plafonne la décision.

> Une source globale, un scan présent ou une valeur affichée ne constituent pas une preuve instrumentale de qualité.

## Gates options actives

Les gates déjà déclarées par le profil ne sont plus seulement documentaires. Le meilleur candidat transmis dans le contexte options est maintenant évalué pour `SPREAD_EXCESSIVE`, `OI_INSUFFICIENT` et `DTE_OUT_OF_MANDATE`. Une valeur non fournie reste non évaluable ; elle n’est jamais implicitement conforme.

## Anomalies de signal

Le nouveau contexte d’anomalies utilise l’analyse OHLCV enrichie lorsque open, high, low, close et volume sont réellement présents. Sans OHLCV complet, Vertex retourne un contexte `CLOSE_ONLY` assorti de sa limite. Il ne reconstruit ni volume, ni chandeliers, ni benchmark. L’analyse peut donc exploiter retours extrêmes, gaps, volume relatif, divergences, changement de volatilité et signaux relatifs uniquement lorsque les entrées le permettent.

## Mémoire et calibration options

La mémoire conserve le contexte options par univers, bucket DTE et plan de détention. Le résumé de calibration affiche la maturité des cellules `SWING_3_6M` et DTE, mais porte explicitement le scope `DIRECTIONAL_PROXY_ONLY`. Il ne s’agit pas d’une probabilité de P&L de contrat : bid/ask de sortie, slippage et quote de sortie doivent être enregistrés avant toute calibration contractuelle.

## Validation

La suite complète a été exécutée après cette évolution : **3 029 tests réussis**. Les tests ajoutés vérifient les gates options, les preuves de qualité/réconciliation, les voies OHLCV et close-only, ainsi que le résumé de calibration options.
