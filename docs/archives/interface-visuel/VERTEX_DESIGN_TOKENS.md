# Vertex — Design tokens V3 (Dark Financial Luxury)

Source unique : `vertex/static/vertex/css/tokens.css`. Aucune couleur
arbitraire dans les pages — gardien `test_v3_tokens_are_canonical`.
Règle : **UNE COULEUR = UNE SIGNIFICATION**.

## Couleurs

| Rôle | Token | Valeur |
|---|---|---|
| Fonds (profond → proche) | `--vx-bg-0…3` | `#050608` `#080b10` `#0b0f16` `#10151e` |
| Surfaces | `--vx-surface-1…3`, `-hover` | `#111720` `#151c27` `#1a2230` `#202a38` |
| Bordures | `--vx-border-soft/default/strong` | blanc α .055 / .085 / .14 |
| Texte | `--vx-text-primary/secondary/muted/faint` | `#f7f8fa` `#b3bdca` `#7f8b9d` `#596577` |
| **Marque** (action, actif, focus) | `--vx-brand`, `-strong`, `-soft` | `#f68a3c` `#ff9a4d` α .14 |
| Ambre / cuivre | `--vx-amber`, `--vx-copper` | `#f5b942` `#d9773f` |
| Positif | `--vx-positive(-soft)` | `#2acb7f` |
| Négatif (rouge corail) | `--vx-negative(-soft)` | `#f05d55` |
| Attention | `--vx-warning(-soft)` | `#f3a93b` |
| Information | `--vx-info(-soft)` | `#4ca6ff` |
| Données/live | `--vx-cyan(-soft)` | `#2cc9d8` |
| Options & IA | `--vx-violet(-soft)` | `#8b6df6` |
| Benchmark/neutre | `--vx-neutral-chart` | `#738096` |
| Dégradé marque | `--vx-brand-gradient` | 135° `#f68a3c→#d9773f` |
| Halo héro | `--vx-hero-halo` | radial orange α .075 |

Alias legacy (`--vx-bg`, `--vx-blue`, `--vx-*-dim`…) conservés le temps de
la migration — mappés sur les tokens V3, à ne pas utiliser dans du code neuf.

## Typographie

- `--vx-font` : Inter, Geist, system-ui… · `--vx-font-mono` : SFMono/Roboto
  Mono/JetBrains (chiffres financiers, `font-variant-numeric: tabular-nums`
  systématique via `.vx-mono`, `.vx-num`, `td.vx-num`).
- Échelle : page 32 · sous-titre 14 · section 19 · widget 13 · KPI 28/20 ·
  corps 13 · méta 11.

## Espacements, rayons, élévation

- Échelle 4/8/12/16/20/24/32/40/48/64 (`--vx-s1…s16`).
- Rayons : 8 (contrôles) · 12 (cartes) · 14 (héro) · 16 (modales).
- Ombres : `--vx-shadow-1/2/modal` + `--vx-glow-brand` (réservé aux
  éléments actifs importants — jamais généralisé).
- Transitions : 140/200/240 ms — coupées par `prefers-reduced-motion`.

## Layout

Grille 12 colonnes (`.vx-grid` + `.vx-col-2…12`), contenu max 1600 px,
sidebar 240/72 px, topbar 62 px, barre mobile 56 px.

## Ambiance de fond

`body::before` : deux halos radiaux orange/cuivre (α ≤ .05) + vignettage
α .28 — fixes, non animés, jamais derrière le texte principal.
