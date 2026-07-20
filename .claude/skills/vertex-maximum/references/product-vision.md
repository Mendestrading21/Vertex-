# Vision produit & vocabulaire canonique

## La boucle de décision
`OBSERVER → COMPRENDRE → DÉTECTER → ÉVALUER → DÉCIDER → EXÉCUTER(=préparer) → SURVEILLER → MESURER → APPRENDRE`

Chaque page se rattache à une ou plusieurs étapes. Chaque bloc d'information répond à UNE question :

| Question | Où elle vit |
|---|---|
| Que se passe-t-il ? | Dashboard, Events |
| Pourquoi ? | Analyse, Intelligence |
| Quelle est mon exposition ? | Portefeuille, Dashboard |
| Quel est le risque ? | Portefeuille (risque), Intelligence |
| Quelle opportunité ? | Opportunités |
| Quelle décision proposée ? confiance ? | Intelligence (analyste + comité) |
| Quel scénario défavorable ? | Analyse, Opportunités, Intelligence |
| Quel ordre envisager ? quelle taille ? quand sortir ? | Desk (prep/sim), fiche position |
| Qu'est-ce qui invalide la thèse ? | Analyse, Journal |
| Quel résultat ? qu'apprend Vertex ? | Performance, Journal |

## Le contrat de réponse de Vertex
Vertex doit pouvoir dérouler, preuves à l'appui :
> Voici ce qui se passe · pourquoi · ce que ça implique pour ton portefeuille · les risques · les meilleures
> opportunités · la décision recommandée · la taille adaptée · l'ordre proposé (à coller dans TWS) · les contrôles
> effectués · ce qui s'est réellement passé · le résultat · ce que Vertex en apprend.

## Vocabulaire canonique (§27) — un concept = un mot, partout (code, UI, docs)
| Terme | Définition stricte | À NE PAS confondre |
|---|---|---|
| **signal** | une OBSERVATION unitaire (moteur) | ≠ recommandation |
| **score** | mesure normalisée 0-100 d'une dimension | ≠ décision |
| **recommandation** | combinaison de signaux + contraintes + risque | ≠ ordre |
| **décision** | recommandation validée / appliquée par l'humain | ≠ recommandation |
| **ordre** | instruction d'exécution — **JAMAIS transmise par Vertex** (prep/sim only) | ≠ décision |
| **exécution** | ce qui s'est réellement passé côté IBKR (observé) | ≠ ordre préparé |
| **opportunité** | candidat à l'entrée, scoré et expliqué | ≠ position |
| **position** | exposition réelle détenue (IBKR) | ≠ opportunité |
| **stratégie** | structure (actions / options multi-jambes) | — |
| **scénario** | trajectoire conditionnelle (central/haussier/baissier) | — |
| **confiance** | niveau de fiabilité de la recommandation | ≠ probabilité de gain |
| **statut** | état de cycle de vie (proposée/en attente/expirée…) | — |

## Séparation des couches (§9) — ne jamais mélanger
`Raw Data → Normalized → Derived Metrics → Signals → Scores → Scenarios → Recommendations → Decisions → (Orders préparés) → Executions observées → Outcomes → Learnings`

Un signal n'est pas une décision. Une recommandation n'est pas un ordre. Vertex s'arrête à **préparer** l'ordre.

## Explicabilité obligatoire de toute recommandation
Pourquoi cette action ? Quels facteurs la soutiennent / la contredisent ? Quelle donnée la changerait ? Quelles
limites (sizing/risque) appliquées ? Quel scénario défavorable ? Toute recommandation porte : création,
**expiration**, statut, version. Une recommandation ne reste jamais active indéfiniment.
