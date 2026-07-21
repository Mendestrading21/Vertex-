# Vertex — Design tokens (Black Glass Institutional)

> **Vérité runtime = `vertex/static/vertex/css/glass.css`** (chargé en
> dernier, il fait autorité), dérivé de `vertex/static/vertex/css/tokens.css`.
> Ce document RÉSUME ces deux fichiers ; en cas de doute, le CSS gagne.
> _(Correctif DES-01 : les valeurs orange/bleu « Dark Financial Luxury »
> décrites ici auparavant sont ABANDONNÉES — voir `.claude/rules/vertex-design-rules.md`.)_

Direction visuelle canonique : **Black Glass Institutional** — fond
noir/graphite neutre, cartes en verre gris translucide, blanc/gris/argent
en couleur structurelle. **UNE COULEUR = UNE SIGNIFICATION.** Zéro bleu ;
violet réservé aux options. Aucune couleur arbitraire dans les pages —
uniquement des tokens `--vx-*` (gardien `test_v3_tokens_are_canonical`).

## Couleurs (canoniques `tokens.css` / `glass.css`)

| Rôle | Token | Valeur |
|---|---|---|
| Fonds (obsidian → graphite) | `--vx-obsidian-900…`, `--vx-graphite-*` | `#08090b` → `#262a30` |
| Surfaces | `--vx-surface-0…elevated`, `-hover` | `#0b0c0f` `#101216` `#15171c` `#1b1e23` `#232830` |
| Verre (carte / élevée / critique) | `--vx-glass-1/2/3` | `rgba(24,26,31,.62)` / `rgba(32,35,41,.62)` / `rgba(46,50,58,.66)` |
| Bordures | `--vx-border-faint/soft/default/strong` | blanc α .05 / .09 / .14 / .22 |
| Texte | `--vx-text-primary/secondary/muted/faint` | `#f3f5f8` `#b7bcc4` `#828892` `#5c626b` |
| **Marque / structure / neutre** | `--vx-brand` = `--vx-silver` | `#c9cdd4` (argent) |
| Positif (gain / validation) | `--vx-positive(-strong/-soft)` | `#36c889` / `#22a970` |
| Négatif (perte / risque / alerte) | `--vx-negative(-strong/-soft)` | `#ed655c` / `#ce4d46` |
| Attention (incertitude / retardé) | `--vx-warning(-soft)` | `#dda23b` |
| **Options / IV / Greeks** | `--vx-option` = `--vx-violet` | `#9c79d0` |
| Benchmark / neutre / indispo. | `--vx-steel`, `--vx-neutral-chart` | `#909b94` |
| Macro / cross-asset (graphes) | `teal` (chart-theme) | `#53b9ad` |

**Zéro bleu.** Les alias legacy `--vx-info` / `--vx-blue` / `--vx-cyan` sont
remappés sur l'acier/le sable neutres (`--vx-steel-2` / `--vx-sand`) — jamais
de teinte bleue ni cyan. Les rampes « signal / orange / copper » de l'ancienne
identité verte sont remappées argent/graphite par `glass.css`. Alias legacy
conservés le temps de la migration, à ne pas utiliser dans du code neuf.

## Typographie

- `--vx-font` : Inter, Geist, system-ui… · `--vx-font-mono` : SFMono/Roboto
  Mono/JetBrains (chiffres financiers, `font-variant-numeric: tabular-nums`
  systématique via `.vx-mono`, `.vx-num`, `td.vx-num`).
- Échelle `--vx-fs-*` (hero / table / kpi-lg inclus) ; chiffres tabulaires
  alignés à droite ; formats via `VX.fmt.*`.

## Espacements, rayons, élévation

- Échelle 4/8/12/16/20/24/32/40/48/64 (`--vx-s1…s16`).
- Rayons : 8 (contrôles) · 12 (cartes) · 14 (héro) · 16 (modales).
- Verre : `--vx-glass-sheen` (liseré interne) + `--vx-blur-sm/md` ; ombres
  `--shadow-card` / `--shadow-float`. Halo/glow d'accent réservé aux éléments
  actifs importants — jamais généralisé.
- Transitions courtes — coupées par `prefers-reduced-motion`.

## Layout

Grille 12 colonnes explicite (`.vx-grid-N` + `.vx-span-*`), contenu borné,
sidebar + topbar + barre mobile issues du shell unique (`vertex/ui/shell/`).

## Ambiance de fond

Fond noir/graphite **neutre** (aucun halo orange/cuivre) : vignettage discret
+ verre translucide gris, fixes, non animés, jamais derrière le texte principal.
Le grain visuel vient du verre (`--vx-glass-*`) et des bordures argentées, pas
d'une teinte de marque.
