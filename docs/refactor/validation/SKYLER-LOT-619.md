# SKYLER — LOT 619 · ANALYSE, DÉCISION D’ABORD

Ce lot applique les fondations Obsidian Copper du lot 618 à la fiche Analyse.
La page répond désormais dans cet ordre : **identité et prix → verdict →
scénarios → graphique principal → thèse et risques → preuves détaillées**.
Les calculs financiers, moteurs, données et routes métier restent inchangés.

## Résultat visuel

- Une seule carte porte la décision principale ; les sorties Skyler et
  ExecutiveEngine deviennent des preuves secondaires.
- Le chandelier devient la preuve visuelle dominante, immédiatement sous le
  verdict. La thèse, le comité, les quatre dimensions et le plan conservent une
  hiérarchie sobre, sans halo ni mouvement décoratif.
- Le rail ne contient plus que le plan et les risques. Il est sticky uniquement
  au-dessus de 1024 px ; tablette et mobile retrouvent un flux naturel.
- Scores, anomalies, évidence, signaux et outils sont conservés sous deux
  disclosures accessibles : **Analyse approfondie** et **Outils d’analyse**.
- Les actions ambiguës ont été renommées : **Calculer le dimensionnement**,
  **Copier l’analyse**, avec la mention persistante **aucune exécution**.

## Graphiques honnêtes

Trois ambiguïtés visuelles ont été retirées sans modifier les données :

1. Un axe radar absent n’est plus transformé en zéro. Le polygone n’est pas
   tracé et les axes `n/d` sont nommés. Le vrai zéro reste une valeur valide.
2. Un résultat futur n’est plus épinglé sur la dernière bougie historique. Il
   apparaît dans un bandeau daté, explicitement **hors série historique**.
3. Le scanner d’anomalies garde une ligne cuivre neutre et des repères
   statiques. Il affiche minimum, maximum, dernière valeur et source ; il ne
   prétend plus que toute série est constituée de « clôtures réelles ».

Le cône du plan a été retiré de cette fiche : il reliait des niveaux fixes sans
distribution probabiliste et doublait entrée, stop et objectifs. Le chandelier
et un rail risque/rendement compact portent désormais ces niveaux une seule
fois.

## Défauts trouvés pendant la validation

La validation navigateur a trouvé deux défauts que les gardiens statiques ne
voyaient pas :

- Lightweight Charts héritait parfois de `en-US@posix`, rejeté par `Intl` et
  capable d’interrompre le chandelier. La locale est désormais fixée à
  `fr-FR`.
- Le verdict pouvait afficher `n/d` si la décision arrivait avant le dossier
  ticker. Le prix est maintenant remis à jour lorsque ce second résultat
  arrive.

Des gardiens couvrent ces deux chemins ainsi que l’ordre DOM, les identifiants
historiques, la divulgation progressive, le radar incomplet, la fraîcheur issue
du scan, le catalyseur futur, l’absence d’animation permanente, `aria-live` et
le comportement responsive du rail.

## Validation réelle du rendu

Chromium headless a chargé `/analysis/AAPL` avec un jeu de données QA
déterministe, non persisté et jamais présenté comme donnée produit :

| largeur | HTTP | débordement X | graphique | rail | console / requêtes |
| ---: | ---: | ---: | --- | --- | --- |
| 1440 px | 200 | 0 px | présent | sticky | 0 / 0 |
| 1024 px | 200 | 0 px | présent | statique | 0 / 0 |
| 390 px | 200 | 0 px | présent | statique | 0 / 0 |

À chaque largeur : une seule décision visible, aucune copie interne visible,
et les deux zones avancées sont fermées par défaut. Les captures QA restent
temporaires (`/tmp`) et ne sont pas des actifs produit.

## Cycle et garde-fous

- Baseline : **2934 tests**.
- Nouveau gardien : `tests/test_analysis_visual_lot619.py`, **13 tests**.
- Suite finale : **2947 passed**, aucun échec.
- `compileall`, trois `node --check` et `git diff --check` : verts.
- Les 8 routes canoniques, `/analysis/AAPL` et `/healthz` répondent **200**.
- `/api/system/status` confirme `readonly: true`, `analysis_only: true` et
  `order_execution: disabled-by-design`.
- Service worker : **v200 → v201** ; empreinte statique
  `29d408427b6fde1f2dc8f06b9189d3701df2676eb066644e0de19357ab68ec95`.
- Production : **6 fichiers** ; aucun moteur, calcul financier, schéma de
  données ou route métier modifié.

## Portée

Ce lot modernise la fiche ticker Analyse, pas l’index de comparaison legacy ni
les autres espaces. Il est construit sur les fondations globales du lot 618.
La branche reste locale, sans push ni PR, en attente d’une validation humaine
avant le prochain espace.

## Verdict

**GO technique et visuel.** La fiche est plus courte à lire, plus calme et plus
honnête sur ses données, tout en conservant chaque preuve sous détail.
