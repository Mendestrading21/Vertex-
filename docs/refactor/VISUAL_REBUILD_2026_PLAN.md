# Vertex — Refonte visuelle totale 2026

## Mandat

Recomposer l’ensemble de l’interface Vertex à partir du corpus utilisateur du
12 août 2026. La refonte est présentationnelle et interactionnelle : aucune
formule, aucun moteur financier, aucune source réelle et aucun invariant
READONLY/ANALYSIS_ONLY ne changent.

## Résultat cible

- une seule grammaire visuelle Obsidian Copper sur les huit espaces ;
- une réponse décisionnelle immédiate par vue ;
- quatre KPI, un graphique hero, un rail de contexte et un tableau principal au
  maximum dans le parcours visible ;
- quatre tailles de graphiques cohérentes et identifiables ;
- source, période, unité, fraîcheur, limites et états dégradés partout ;
- tableaux de 48 px, lisibles, accessibles, sans débordement ;
- détail dans un drawer desktop / plein écran mobile ;
- zéro glow permanent, zéro donnée inventée, zéro ambiguïté d’exécution.

## Lots d’exécution

| Lot | Périmètre | Critère de sortie |
|---|---|---|
| 620 | références + shell + grilles + cartes + charts + tables + drawer | primitives communes testées, API existante préservée |
| 621 | Aujourd’hui + Marchés | répétitions retirées/repliées, une preuve principale par vue |
| 622 | Opportunités + Portefeuille | shortlist/tableaux/risk hiérarchisés, données manquantes honnêtes |
| 623 | Options | contexte ticker unique, payoff/IV/GEX priorisés, legacy rattaché |
| 624 | Journal + Système | méthode et santé d’abord, ledger/diagnostics en avancé |
| 625 | harmonisation Analyse + QA globale | responsive 6 largeurs, données réelles/démo/erreurs, a11y, SW |

Chaque lot suit : audit ciblé → modification bornée → tests → navigateur →
revue du diff → commit local. Les lots ne sont pas fusionnés ni publiés sans
preuve de leur compatibilité.

## Matrice de validation globale

- Largeurs : 390, 768, 1024, 1366, 1440 et 1920 px.
- Routes : `/`, `/markets`, `/opportunities`, `/analysis/AAPL`, `/portfolio`,
  `/options`, `/journal`, `/system` et toutes leurs sous-vues visibles.
- États : réel, `DEMO=1`, `NO_IBKR=1`, données insuffisantes, périmé, erreur et
  hors-ligne lorsque simulable sans modifier la logique métier.
- Sécurité : aucune action exécutable, pas d’ordre IBKR, libellés READONLY
  explicites, provenance et limites conservées.
- Qualité : suite Pytest complète, `node --check`, `py_compile`, `git diff
  --check`, absence d’erreur console, focus clavier, reduced motion, contraste
  et absence de débordement horizontal.

## Arbitrages visuels

La structure vient principalement de `9D8A`, `E165` et `9604`. Le drawer vient
de `E95`, les tailles de graphiques de `8CB`. Grafana et les dashboards serveurs
ne sont utilisés que pour la précision des unités et de la fraîcheur. Leurs murs
de données, tuiles saturées et palettes multicolores sont explicitement rejetés.

La carte détaillée des références et interdits se trouve dans
`docs/refactor/VISUAL_REFERENCE_MAP.md`.
