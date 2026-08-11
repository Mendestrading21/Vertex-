# SKYLER LOT 203 — Tournée TV : cône σ hachuré + murs GEX en dominantes

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-203` (base : lot 202 fusionné)

## Livré

### 1. Cône de mouvement attendu (Options / Volatilité) — bandes hachurées

`pages/options-intel.js` (chartCone) : les bandes 1σ (brand) et 2σ
(copper) sont une **estimation lognormale** (σ = spot · IV_ATM ·
√(DTE/365)) — leurs remplissages passent des aplats translucides aux
**motifs hachurés** (`C.hatchPattern`, lot 197), la texture commune à
tout ce qui est projeté (cône de projection, payoff, théta). Repli
translucide propre si le helper est absent. Médiane, tooltips et
légende inchangés.

### 2. GEX par strike (Options / Positionnement) — les MURS en dominantes

`pages/options-gex.js` (renderBars) : les deux niveaux que le trader
cherche — le **mur call** (plus gros call GEX) et le **mur put** (plus
gros |put GEX|), calculés seulement s'il y a ≥ 2 strikes — deviennent
les dominantes du graphique : barre en pleine intensité (1 vs .55 pour
les autres) et **valeur RÉELLE en chip pleine couleur** (texte sombre,
borné au viewBox) au bout de la barre. Axe, strikes, ligne de spot
pointillée et pied honnête inchangés.

## Accros

Aucun.

## Preuves

- `node --check` OK (options-intel.js, options-gex.js).
- Serveur DEMO port 5002 : `lot203-cone-card.png` (bandes σ hachurées,
  médiane blanche, spot 180), `lot203-gex-card.png` (mur call chip
  « 15.59 M$ » pleine intensité, mur put chip « −6.24 M$ », autres
  adoucies, spot pointillé) — envoyées, **0 erreur console**.
- SW `td-shell-v166` → `v167` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 204 : derniers ☐ de TV-CHARTS-INVENTORY.md — double probabilité,
sparklines KPI (constat données), barres S+/S/A/B (héritage à
constater), puis polish transverse. MINI-BILAN 201-205 au lot 205.
