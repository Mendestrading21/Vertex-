# 05 — Inventaire des composants (design system)

Design system = **variables CSS `--vx-*`** + variantes de carte `vx-card` + primitives `VXCharts` + formats
`VX.fmt.*`. **19 feuilles CSS** (`vertex/static/vertex/css/`) chargées en cascade, `glass.css` **en dernier**
(fait autorité) :
`animations · base · buttons · charts · cockpit · components · control-surface · fonts · forms · glass · layout ·
polish · premium · responsive · states · tables · tokens · utilities`.

## Findings
- **CMP-01 (P1) — `.vx-card` fragmenté.** Défini/redéfini dans **6 feuilles** : `base.css`, `cockpit.css`,
  `components.css`, `glass.css`, `polish.css`, `premium.css` (4 avec un reset `.vx-card { … }`). Empilement
  d'overrides difficile à raisonner. **Action** : une définition canonique dans `components.css` + modificateurs
  (`.vx-card--metric`, `--decision`, `--chart`, `--compact`) ; `glass.css` ne porte que le vernis « verre ».
- **CMP-02 (P1) — 4 systèmes de tuiles KPI concurrents** : `vx-kpi` (36 occ.), `vx-metric` (50), `vx-stat` (52),
  `vx-stat-xl` (6). Quatre grammaires pour le même besoin « chiffre + label + delta ». **Action** : fusionner en
  un **MetricCard** unique (une classe + variantes de taille/état) ; migrer les pages progressivement ; garder un
  alias temporaire pour ne rien casser.
- **DES-01 (P1) — Docs de design périmés.** `docs/claude/VERTEX_DESIGN_TOKENS.md` et `VERTEX_CHART_LIBRARY.md`
  décrivent une palette **orange/bleu** abandonnée, contredisant `glass.css` (Black Glass, zéro bleu). Risque :
  induire un futur contributeur en erreur. **Action** : marquer ces docs « PÉRIMÉ — voir glass.css / references/
  design-system.md » ou les régénérer.
- **DES-02 (P2) — Palette « zéro bleu » : bien tenue à la source.** `tokens.css:120-122,174-176` remappe
  `--vx-info`/`--vx-blue`/`--vx-information` → argent/acier. Vérifier qu'aucune page n'injecte un hex bleu en dur
  ni ne rend un `state_col` moteur brut (mapper `state` → `C.colors`).
- **CMP-03 (P1) — Sidebar legacy orange injectée en dur, 4× dans `terminal.py`.** Un bloc `<style>#vside…`
  identique est réinjecté aux lignes **2874, 4515, 4862, 5319** avec l'**ancienne palette orange** hardcodée
  (`#FF7A18`, `#FF9A3D`, `rgba(255,122,24,…)`) et **14 items** de nav (`nth-of-type(1..14)`). C'est le shell
  legacy du monolithe, contraire à Black Glass (zéro orange structurel) et à `PRIMARY_NAV` (8 items). Hex orange
  aussi en fallback `--vc` sur `.necard`/`.ccard` (`terminal.py:2774,5709`). **Action (Phase 3)** : supprimer ces
  injections une fois les pages entièrement servies par le shell canonique ; factoriser tout style commun dans le
  CSS tokenisé. Ne retirer qu'après avoir confirmé qu'aucune vue legacy n'en dépend (bump SW requis).

## Palette sémantique (source `tokens.css:3-8`)
vert `#36c889`=positif · corail `#ed655c`=négatif/risque · ambre `#dda23b`=incertitude · argent `#c9cdd4`=
structure/marque · violet `#9c79d0`=**options uniquement** · **zéro bleu**. Une sémantique = une couleur partout.

## Cible (Phase 2 fondations)
Un MetricCard, une `.vx-card` + modificateurs, tokens comme seule source de couleur/rayon/espacement, formats via
`VX.fmt.*`, docs de design réalignés sur `glass.css`. Détail : `references/design-system.md`.
