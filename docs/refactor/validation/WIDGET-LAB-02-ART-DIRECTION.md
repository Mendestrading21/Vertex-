# WIDGET LAB — ART DIRECTION PASS 02

> `/widget-lab` validé dans son principe. Cette passe élève le **niveau de
> sophistication visuelle** : matières travaillées, palettes par famille (l'orange
> n'est plus la couleur de tous les widgets), variantes réellement distinctes
> (concepts, pas couleurs), nouvelles formes signature, micro-interactions, vraie
> version mobile, et les **5 familles manquantes**. **Aucune page produit touchée.**
> Route autonome, aucune donnée réelle, aucun moteur, READONLY.

## 1. Objectif atteint — reconnaissable sans titre/logo/orange

Chaque widget se reconnaît désormais par sa **forme**, sa **profondeur** et sa
**matière** — pas par l'orange. L'orange Ember reste réservé à : sélection,
interaction, ligne de décision, focus, **point actif**, identité. Preuve : le
bench Regime Aura présente 6 concepts distincts (halo / horizon de phase / brume /
capsule à tension / champ de pression / tuile météo), chacun sur une matière
différente, l'orange n'apparaissant que sur l'anneau de confiance.

## 2. Matières (6 tiers)

Système `.wl-surf--*` : **matte · smoked · polished · deepblack · metal · frosted**.
Chaque matière = fond travaillé + **bord intérieur clair** (`inset 0 1px`) + **bord
extérieur sombre** + ombre diffuse + **micro-texture CSS** (feTurbulence en data-URI,
opacité ~3,5 %, `mix-blend:overlay`). `polished` ajoute un reflet supérieur ; `metal`
un balayage diagonal chaud ; `deepblack` une vignette chaude ; `frosted` un blur
fort translucide. Une **étiquette de matière** est affichée sur chaque tuile, et
**les variantes d'un même widget portent des matières différentes** (cyclage
automatique, ou matière explicite par variante). `data-live` déclenche un léger
**balayage de matière** (sheen) réservé au direct.

## 3. Palettes par famille (orange non décoratif)

Accent chromatique propre par famille, cohérent avec la sémantique :

| Famille | Accent | Logique |
|---|---|---|
| Régime | émeraude | atmosphérique par état |
| Momentum | **vert citron** `#B6F04A` | force |
| Volatilité / Options | **violet électrique** | vol/convexité |
| Analyse / Journal | ambre doré | verdict / attente / discipline |
| Portefeuille | **blanc cassé** `#E7E2DA` | constellation |
| Marchés / Système | cyan contrôlé | comparaison / information neutre |
| Opportunité / Breadth | émeraude | confirmation / participation |

Rose/magenta réservé aux divergences (dans la grammaire). **Aucune couleur
décorative ; aucun bleu identitaire** (gardien vérifié).

## 4. Variantes réellement distinctes (concepts, pas couleurs)

**Regime Aura** V1→V6 : halo atmosphérique · **horizon de phase** (Horizon Band) ·
**brume indéterminée** · **capsule à tension** latérale · **champ de pression**
(Pressure Field, iso-barres) · **tuile météo** (Market Weather Tile). Chacune change
forme + composition + lecture + hiérarchie + matière. Idem Conviction (Spine plein
vs **Pillar segmenté**), Momentum (Comb vs **Ribs** en cage thoracique), Thesis
Pulse (intacte/surveiller/**invalidée plate**).

## 5. Nouvelles formes signature implémentées (SVG/CSS réels)

Horizon Band · Pressure Field · Regime Capsule · **Signal Bloom / Opportunity
Beacon** · **Risk Crater** · **Momentum Ribs** · **Conviction Pillar** ·
**Volatility Rift** · **Catalyst Countdown Ring** · **Drawdown Canyon** ·
**Portfolio Constellation** · **Greek Vector Field** · **Payoff Terrain** ·
**Thesis Pulse** (ECG) · **Confidence Lens** (diaphragme) · **Market Weather Tile** ·
Scenario Triad · Score Decomposition · Committee Consensus · Concentration Tower ·
Bias Heatmap · Progress Ladder · Source Freshness Matrix · Engine Status Spine ·
**READONLY Seal** · Data Integrity Reactor. (≈ 25 formes nouvelles, toutes rendues).

## 6. Familles ajoutées

- **Analyse** : Verdict Slab · Scenario Triad · Thesis Pulse · Score Decomposition ·
  Committee Consensus · Confidence Lens.
- **Portefeuille** : Allocation Constellation · Concentration Tower · Drawdown
  Canyon · Winner/Loser Guardrails.
- **Options** : Payoff Terrain · Greek Vector Field · Liquidity Lens · Theta Burn.
- **Journal** : Discipline Ring · Bias Heatmap · Progress Ladder.
- **Système** : Data Integrity Reactor · Source Freshness Matrix · Engine Status
  Spine · READONLY Seal.

## 7. Micro-interactions

Hover **révèle une donnée secondaire** (`.wl-more`), **lift** −2 px + matière
renforcée ; **tooltip verre** (`.wl-tip`) sur les cellules ; **glow local**
uniquement autour de la donnée active ; **profondeur au focus** (`focus-within`) ;
**balayage de matière au LIVE**. Durées 120–240 ms, easing `cubic-bezier(.23,1,.32,1)`,
`prefers-reduced-motion` → tout `animation:none`.

## 8. Mobile

Toggle **« Aperçu mobile »** dans l'en-tête (rend une colonne à 390 px inline) +
vraie mise en page mobile : header/nav qui **wrap**, benches empilés, widgets
pleine largeur, tables/graphes larges en **défilement contrôlé** (jamais de
débordement de page), zones tactiles ≥ 44 px sur les contrôles. Mesuré à **390 px :
0 débordement**.

## 9. Typographie

Valeurs principales très nettes (tabular-nums, poids 800–850), labels fins,
sous-labels discrets, meilleure séparation chiffre/unité/variation, moins de gris
uniforme. Lecture < 2 s préservée.

## 10. Chiffres & tests

- **44 widgets** (benches), **80 tuiles de variantes**, **14 familles** (≥ 40 exigé).
- `python -m compileall -q terminal.py vertex` → exit 0.
- `python -m pytest tests/ -q` → **971 passed, 2 skipped** (+ gardiens AD-02 :
  familles, matières, ≥ 40 widgets, zéro-bleu, échantillons étiquetés, READONLY).
- Navigateur **1440 & 390** : **0 débordement, 0 erreur console**.
- Interaction verdict + toggle mobile vérifiés.

## 11. Captures (évidence de session)

`lab2-regime.png` (6 concepts × 6 matières), `lab2-analyse.png` (Verdict/Scenario/
Thesis), `lab2-options.png`, `lab2-full.png` (page complète), `lab2-390.png` (mobile),
`lab2-mobilepreview.png` (toggle).

## 12. Limites restantes / différé

- Certaines formes de la liste (Capital Flow Stream, Institutional Footprint,
  Volatility Term Rift 3D, LEAPS Compatibility, Structure Comparison) sont
  **spécifiées mais pas encore rendues** — prochaine itération.
- La « vraie version mobile par widget » est aujourd'hui surtout un **reflow +
  défilement contrôlé** ; les versions mobiles *dédiées* (détail secondaire replié
  par widget via container queries) restent à approfondir sur les widgets complexes.
- Micro-texture : coût GPU négligeable mesuré ; à re-vérifier sur très bas de gamme.
- Le lab reste un **catalogue** : la sélection Officiel/Référence/Rejeté + export
  permet de graver les choix avant reconstruction des pages.

## Verdict

Le laboratoire passe du « propre » au **premium** : matières distinctes, palettes
par famille (orange réservé à l'identité/interaction), variantes = concepts,
≈ 25 formes signature nouvelles réellement implémentées, 5 familles ajoutées,
micro-interactions et mobile. **44 widgets · 971 tests verts · 0 débordement · 0
erreur console · READONLY · aucune donnée inventée.** **Arrêt pour validation
humaine.** Dis-moi tes choix (Officiel/Référence/Rejeté, via Exporter) et les
formes à pousser ou retirer.
