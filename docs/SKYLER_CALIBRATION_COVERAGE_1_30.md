# Vertex — couverture de calibration Skyler

Le journal de décisions expose `outcomes.coverage_pct`, qui mesure la part des décisions disposant à la fois d’un prix enregistré et d’une cote actuelle.

Le bloc `outcomes.by_decision` segmente cette couverture par décision canonique. Il sert uniquement à qualifier l’observation disponible ; il ne classe ni la qualité d’une décision ni sa performance.

Les décisions non mesurées restent comptées séparément. Le score de Brier demeure indisponible tant qu’aucune probabilité calibrée n’a été émise ; Vertex ne déduit aucune probabilité depuis un verdict.
