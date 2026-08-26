# Design system Vertex (réalité : CSS + classes, pas React)

Le design system n'est PAS une bibliothèque de composants React : c'est un ensemble de **variables CSS**
(`--vx-*`), de **classes partagées** (`vx-card`, `vx-kpi`, `vx-badge`…), de **primitives graphiques**
(`VXCharts`) et de **formats** (`VX.fmt.*`). Source de vérité CSS = `vertex/static/vertex/css/glass.css`
(chargé en DERNIER). Cross-ref : `docs/VERTEX_DESIGN_TOKENS.md`, `docs/claude/VERTEX_GLASS_VISUAL_CONTRACT.md`.

## Direction artistique — « Black Glass Institutional »
Sombre, institutionnelle, haut de gamme, précise, orientée trading. Glassmorphism maîtrisé. Sans néons, sans
gadget, sans surcharge, sans multiplication de couleurs.

## Palette sémantique (STRICTE — jamais coder une couleur en dur dans une page)
| Rôle | Usage | Règle |
|---|---|---|
| fond canvas | noir/graphite quasi noir | neutre |
| surface / surface élevée | verre gris translucide | bordures fines discrètes |
| texte primaire / secondaire / muted | lisibilité forte → atténuée | contraste AA |
| **vert** | positif, validation, gain | sémantique stricte |
| **rouge** | négatif, perte, alerte critique | sémantique stricte |
| **orange** | incertitude, prudence, intermédiaire | sémantique stricte |
| **bleu/gris bleuté** | information/action neutre | **jamais** décoratif ; « zéro bleu » ailleurs |
| **violet** | **réservé aux options** | fonction sémantique uniquement |

Une même sémantique = une même couleur sur TOUTES les pages et TOUS les graphiques. Utiliser les tokens, jamais
des hex bruts. ⚠️ Piège connu : les moteurs renvoient parfois un `state_col` hex (dont du bleu) — toujours
**mapper `state` → `C.colors`**, jamais l'hex moteur.

## Tokens (groupes) — voir `--vx-*` dans glass.css
`background.canvas/surface/surfaceElevated/overlay` · `border.subtle/default/strong` ·
`text.primary/secondary/muted/disabled` · `status.positive/negative/warning/info/neutral` · `brand` ·
`chart.series.N/grid/axis/reference` · spacing · radius · typographie. (Enumération réelle : `docs/vertex-audit/04-design-audit.md`.)

## Système de cartes — variantes cibles à mapper sur `vx-card`
Toutes les cartes dérivent d'UN système commun (`vx-card` + modificateurs). Ne pas créer une carte ad hoc si une
variante existante peut être étendue. Variantes cibles (mission §6.2) : `MetricCard` (KPI), `StatusCard`,
`InsightCard` (`vx-insight`), `AlertCard`, `ChartCard` (`vx-chart-card`), `PositionCard`, `OpportunityCard`,
`DecisionCard`, `DataQualityCard`. Invariants : même rayon, bordure, ombre, espacements, hiérarchie typo, header,
actions, états **loading/error/empty**, responsive. (Inventaire réel : `docs/vertex-audit/05-component-inventory.md`.)

## Densité
Trois niveaux : confortable (cartes de décision) · standard · compact (tableaux de trading). Ne pas tout remplacer
par du texte : badges, jauges, barres, sparklines, heatmaps, mini-graphes, tooltips, drawers, popovers.

## Typographie
Échelle centralisée : titre de page · titre de section · titre de carte · valeur financière principale ·
secondaire · label · aide · métadonnée · texte de tableau · annotation graphique. **Chiffres tabulaires** pour les
valeurs financières (police mono JetBrains) ; nombres alignés à droite en colonne.

## Formats financiers (`VX.fmt.*` — `vertex/static/vertex/js/vx-core.js`)
Centraliser TOUT formatage : devise, %, quantité, prix, P&L, market cap, volatilité, greeks, date, heure, durée,
grand nombre, **valeur absente**. Ne jamais dupliquer la logique de format dans une page.

### États d'une valeur — ne JAMAIS confondre (règle 4 / data-integrity)
`0` (vrai zéro) · `—` (donnée absente/non applicable) · `N/A` · `Indisponible` · `Estimation` (modèle) ·
`Retardée` · `Périmée`. Chaque état a une signification EXACTE et un rendu distinct. Une absence n'est jamais
masquée par `0`.
