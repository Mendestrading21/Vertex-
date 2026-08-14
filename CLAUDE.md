# Vertex — instructions projet pour Claude Code

## Mission
Vertex est un terminal d’aide à la décision d’investissement. Il doit rester **READONLY** : analyser, hiérarchiser, expliquer, comparer et suivre. Il ne doit jamais créer, modifier, transmettre ou exécuter un ordre financier.

## Règle obligatoire pour tout travail UI / UX / design / graphique
Avant de modifier une page, un composant, une couleur, un texte, une icône, une grille, un tableau, un graphique ou le shell, lire et appliquer :

`.claude/skills/rebuilding-vertex-visual-system/SKILL.md`

Ce skill est la source de vérité opérationnelle de la refonte Vertex Signal OS. Il contient les règles visuelles, la méthode page-par-page, la grammaire TradingView, la micro-copy, les composants, la validation et les critères de sortie.

Ne pas improviser une nouvelle direction esthétique en dehors de ce système.

## Sources de vérité existantes à préserver
- `vertex/strategy/` : moteurs de décision et Constitution.
- `vertex/visualization/palette.py` : registre couleur Python.
- `vertex/static/vertex/js/charts/chart-theme-obsidian-copper.js` : miroir du thème graphique navigateur.
- `vertex/static/vertex/js/charts/chart-core.js` : moteur graphique canonique.
- `vertex/ui/shell/` : shell et navigation canoniques.
- `docs/design/VERTEX_SIGNAL_OS.md` : contrat de design engagé.
- `tests/` : gardiens produit, sécurité, accessibilité, cache et cohérence visuelle.

## Invariants non négociables
1. Aucun chemin d’exécution d’ordre.
2. Aucune donnée inventée pour remplir un widget.
3. Les états `loading`, `empty`, `stale`, `error`, `demo`, `offline` restent explicites.
4. Une couleur = une signification.
5. Une donnée importante = un traitement visuel dominant, pas dix accents concurrents.
6. Toute modification de `/static` impose la mise à jour cohérente du cache/service worker et de ses tests gardiens.
7. Toute refonte doit conserver ou améliorer accessibilité, responsive, handlers et routes.
8. Ne jamais déclarer une page terminée sans exécuter sa checklist de validation du skill.

## Méthode de travail
- Travailler **une page canonique à la fois**.
- Auditer d’abord, proposer la hiérarchie, puis reconstruire.
- Réutiliser des primitives communes avant de créer un composant local.
- Après chaque page : tests ciblés + contrôle visuel desktop/tablette/mobile + zéro bouton mort + zéro erreur console.
- Seulement après validation, passer à la page suivante.

## Ordre recommandé
1. Shell global
2. Aujourd’hui
3. Marchés
4. Opportunités
5. Analyse
6. Portefeuille
7. Options
8. Journal
9. Système
10. Passe finale responsive/accessibilité/performance/cohérence
