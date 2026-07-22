# Vertex V4 — Design System Obsidian Prism

> **Status: ACTIVE**
> Owner: Vertex V4
> Last verified against: `integration/vertex-v4-clean`
> Supersedes: Black Glass, Signal Green, Obsidian Copper

Ce fichier est la source de vérité courte du design. La spécification complète est
`docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md` et les décisions figées sont dans
`docs/vertex-v4/DECISIONS.md`.

## Direction

Terminal d'analyse institutionnel sombre, précis et dense sans être étouffant.
L'interface doit paraître premium, calme et construite comme un seul produit —
jamais gaming, jamais néon, jamais multicolore sans raison.

Référence maître :
`docs/vertex-v4/reference/00-master-obsidian-prism.jpg`.

## Palette

- Canvas : `#030509`, `#050810`, `#070B12`.
- Surfaces : graphite froid translucide, hiérarchisé sur trois niveaux.
- Texte : `#F5F7FB`, `#BEC5D2`, `#858E9F`, `#596273`.
- Marque : violet `#6D4AFF`, prism `#9A5CFF`, magenta `#D86CB7`, corail `#F08A62`.
- Positif : `#35D28B` uniquement.
- Négatif / risque : `#FF625F` uniquement.
- Attente / incertitude : `#E6A846` uniquement.
- Bleu : série de comparaison rare, jamais identité dominante.

Tous les usages passent par des tokens `--vx-*`. Aucun hex local dans une page.
Une couleur conserve la même signification sur chaque page et graphique.

## Typographie

- Interface : General Sans auto-hébergée.
- Données : JetBrains Mono auto-hébergée.
- Nombres : chiffres tabulaires, unités visibles, alignement à droite en tableau.
- Titres éditoriaux naturels ; uppercase réservé aux micro-labels courts.

## Profondeur

Une seule stratégie : surfaces obsidienne + bordures fines + verre localisé.
Le glass est réservé à la topbar, aux panneaux hero, aux overlays et aux éléments
sélectionnés. Pas de blur sur chaque carte et aucun glow permanent.

## Composants

Quatre niveaux seulement :

1. Hero panel — message ou graphique majeur, maximum deux par écran.
2. Analytical panel — graphique, analyse ou table principale.
3. Metric tile — KPI compact, delta et sparkline.
4. Inspector panel — verdict, risques, niveaux et détails contextuels.

Les composants dérivent des primitives partagées `vx-*`. Chaque état loading,
empty, partial, stale et error doit être explicite et utile.

## Graphiques

- Utiliser `window.VXCharts` et le contrat `docs/canonical/CHART_CONTRACT.md`.
- Montrer question, source, période, unité, fraîcheur et conclusion.
- Série principale prism ; benchmark neutre ; couleurs financières strictement sémantiques.
- Aucun graphique décoratif ou donnée fabriquée pour remplir un panneau.
- Tooltips lisibles, grilles discrètes, réduction du mouvement respectée.

## Layout

- Grille 12 colonnes, contenu max 1680 px.
- Espacement de base 4 px ; rythme principal 12–16 px.
- Sidebar 164–184 px ouverte, 64–72 px repliée.
- Topbar 54–60 px.
- Rayons 7–10 px sur contrôles, 10–14 px sur cartes.
- Cibles tactiles mobiles de 44 px quand l'espace le permet.

## Navigation cible

Briefing · Marchés · Opportunités · Portefeuille · Analyse · Options ·
Performance · Intelligence · Système.

## Motion et accessibilité

- Transitions 120–220 ms, ease-out, transform/opacity en priorité.
- Press feedback discret ; aucune animation continue.
- `prefers-reduced-motion` respecté.
- Contraste AA, focus visible, clavier complet.
- Le risque ne dépend jamais uniquement du rouge ou du vert.

## Garde-fous

- READONLY intact ; aucun CTA ne suggère l'envoi d'un ordre.
- Aucune valeur fictive présentée comme réelle.
- Aucun style Black Glass, Signal Green ou Obsidian Copper ajouté.
- Les fichiers legacy encore chargés ne sont supprimés qu'après migration, preuve
  visuelle, tests verts et mise à jour de `MIGRATION_MAP.md`.
