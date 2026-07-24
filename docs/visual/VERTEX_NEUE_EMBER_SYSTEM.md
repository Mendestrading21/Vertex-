# VERTEX NEUE EMBER — Système visuel (Neon Glass Orange)

> Source unique d'identité de Vertex. Remplace **Signal Green** (vert de marque
> `#84aa31`) et l'ancienne palette locale *Neon Glass* (`#ff7a1e`) par une seule
> identité **Orange Ember `#FF6D29`** fixée **à la racine** (`tokens.css` + les 3
> miroirs graphiques). Aucune 4ᵉ surcouche : la couleur est corrigée à la source.
>
> Branche : `agent/vertex-neon-glass-graphs` · issue #14. **ANALYSIS ONLY — aucun
> ordre, aucun moteur financier modifié, IBKR reste READONLY.**

## 1. Principe fondateur — une couleur = une signification

| Couleur | Hex | Rôle **exclusif** |
|---|---|---|
| **Orange Ember** | `#FF6D29` | Identité / marque / action principale / sélection / navigation / focus / point actif. **Ne signifie JAMAIS « hausse ».** |
| Émeraude | `#2ED6A1` | Gain / hausse / confirmation réelle / état sain. |
| Corail | `#FF5F69` | Perte / risque / invalidation / erreur. |
| Ambre | `#FFC857` | Attente / seuil / prudence / alerte. |
| Violet | `#9B7BFF` | Options / volatilité (uniquement pertinent). |
| Cyan | `#45D6E8` | Comparaison technique (série de contraste — jamais l'identité). |
| Gris chaud | `#BABABA` | Neutre / benchmark / indisponible. |

**Aucun vert de marque. Aucun bleu identitaire.** Le canvas global est `#05070C`
(très sombre, légèrement froid) ; les surfaces sont chaudes (`#161316` →
`#1D1819` → `#251D1B`), profondeur cuivre `#453027`.

## 2. Où vit la couleur (la seule source, puis ses miroirs)

1. **`vertex/static/vertex/css/tokens.css`** — SOURCE unique de tous les tokens
   `--vx-*`. Le shell entier (sidebar, topbar, nav mobile, overlays — **hors**
   `.vx-content`) en hérite : tuer le vert ici le tue partout.
2. **`vertex/visualization/palette.py`** — source Python des couleurs de séries
   graphiques (`BRAND=#FF6D29`, `SERIES=(BRAND, BEIGE, NEUTRAL, OPTION, AMBER,
   COPPER)`).
3. **`vertex/static/vertex/js/charts/chart-theme-obsidian-copper.js`** — miroir JS
   **strict** de `palette.py` (test `test_js_theme_matches_python_palette`).
4. **`vertex/static/vertex/js/charts/chart-core.js`** — repli codé en dur, 3ᵉ copie,
   identique à `palette.SERIES` (test `test_chart_core_fallback_series_matches_palette`).

> Les 3 miroirs graphiques (2·3·4) sont synchronisés **en lockstep** : toute
> dérive casse un test. `neon-glass.css` ne contient **plus aucun littéral
> orange** — il source `--ng-neon: var(--vx-ember-500)`.

## 3. Tokens clés (extrait)

```
--vx-canvas:#05070C  --vx-shell:#100E0F  --vx-surface:#161316
--vx-surface-elevated:#1D1819  --vx-surface-hover:#251D1B  --vx-warm-depth:#453027
--vx-ember-500:#FF6D29 (marque)  --vx-ember-400:#FF824B (hover)  --vx-ember-600:#e85a19 (pressé)
--vx-ember-ink:#161316 (texte sur bouton orange — JAMAIS blanc)
--vx-positive:#2ED6A1  --vx-negative:#FF5F69  --vx-warning:#FFC857
--vx-option/--vx-violet:#9B7BFF  --vx-technical/--vx-cyan:#45D6E8
--vx-text-primary:#F8F5F3  --vx-text-secondary:#BABABA  --vx-text-muted:#8A8284
--vx-brand:var(--vx-ember-500)  --vx-brand-gradient / --vx-glow-brand
```

**Compat sans casse** : `--vx-signal-*`, `--vx-orange-*`, `--vx-copper-*` sont
*repointés* sur la rampe Ember (toute référence résiduelle devient orange, rien
ne casse). Ils sont **dépréciés** et à retirer progressivement.

## 4. Cartes glass & profondeur

- Carte = verre local : `backdrop-filter: blur(14px)`, bordure fine chaude,
  ombre discrète, filet cuivre décoratif en tête (`::before`, `pointer-events:none`).
- **`overflow: visible` par défaut** sur les cartes glass — correction d'un bug où
  `overflow:hidden` rognait tooltips et menus.
- 3 niveaux de profondeur : surface `#161316` → élevée `#1D1819` → survol `#251D1B`.
- Glow **réservé** au live / point actif / sélection / alerte — jamais permanent.

## 5. Typographie

- Direction : **Neue Montreal**. **Aucun fichier licencié n'est embarqué** dans le
  dépôt → fallback robuste **Inter** (déjà chargé), en conservant la hiérarchie et
  le rythme Neue Montreal. **Aucun téléchargement supplémentaire** : le rendu reste
  correct sans dépendance réseau nouvelle.
- Nombres : `tabular-nums`, JetBrains Mono.
- Échelle : display 40 · page 32 · section 22 · carte 15 · corps 14 · meta 12 · KPI 30.

## 6. Motion

Reveal court, skeleton→contenu, changement de période, point actif, hover léger,
pulse live bref, drawer/modal. Durées 120–240 ms. `prefers-reduced-motion` **strict**.

## 7. Interdits

Pas de vert de marque · pas de bleu identitaire · pas de littéral orange hors
`tokens.css` · pas de glow permanent · pas de gradient décoratif sans fonction ·
pas de donnée inventée (absence → `—`/état honnête) · pas de modification moteur/
données/route pour l'esthétique · READONLY intact.

## 8. Gardiens (tests)

`test_visual_intelligence.py` (parité 3 miroirs + zéro-bleu) · `test_obsidian_theme.py`
(zéro-bleu tokens/pages) · `test_ui_v3.py::test_v3_tokens_are_canonical` (tokens Ember
canoniques, plus de `#84aa31`) · `test_design_system_v1.py` (typo Inter fallback) ·
`test_neon_glass_01.py` (identité sourcée tokens, overflow visible, `::before` non
cliquable, classes `vx-mk-*` stables, zéro-bleu, glow live-only, reduced-motion,
scope briefing+markets, READONLY).
