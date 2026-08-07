# SKYLER V2 — LOT 187 : design system honnête (défaut réel corrigé)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-187`
(base : `integration/vertex-skyler-v2` @ `fe1fe54`, lot 186 fusionné).
Lot correctif MINIMAL + tests — moteurs intacts, READONLY intact.

## 1. DÉFAUT RÉEL trouvé au survey

`vertex/ui/pages/design_system_page.py` (254 l, servie sur
/design-system et /system/design-system, ZÉRO test dédié) — la page
de RÉFÉRENCE (« source unique de vérité de l'identité ») affichait
des hex PÉRIMÉS recopiés à la main : 10+ étiquettes divergeaient de
tokens.css (ex. `--vx-black` affiché #020202, réel #060405 ;
`--vx-obsidian-950` devenu alias var(--vx-canvas) montrait l'ancien
hex). Les pastilles étaient justes (elles rendent var(--…)), mais
les ÉTIQUETTES mentaient — exactement le genre de dérive qu'une page
de référence doit interdire.

## 2. Correctif (structurel, minimal)

```text
vertex/ui/pages/design_system_page.py — les hex ne sont PLUS
  recopiés : _load_tokens() lit tokens.css à l'import et résout les
  alias var() un niveau ; les groupes (_BG/_COPPER/_SEM/_TEXT) ne
  listent plus que les NOMS de variables. La double source a
  disparu : la page LIT la vérité, elle ne peut plus mentir.
vertex/app/routes/system.py — SW td-shell-v151 → v152 (changement
  visible utilisateur) + les 4 gardiens de version mis à jour
  (production_guards_canonical, reconstruction_today, redesign_ui,
  ui_v3).
```

## 3. Ce qui est figé (`tests/test_design_system_page_lot187.py`, 6 tests)

```text
Preuve rouge/vert — chaque hex affiché == la valeur RÉELLE de
  tokens.css (≥ 30 swatches, 0 divergence — avant correctif : 10+) ;
  chaque variable exposée EXISTE dans tokens.css (un renommage CSS
  fait échouer la référence, jamais un silence) ; les alias var()
  sont montrés résolus en hex final
Invariants de page (jamais gardés) — ids uniques, #8f8a83 absent,
  aucun verbe d'ordre, ≥ 20 échantillons copiables data-ds-copy,
  état vide de référence au libellé produit exact
SW — v152 servi (gardien)
```

## 4. Preuves

```text
python -m compileall → 0 erreur
python -m pytest tests/test_design_system_page_lot187.py -q → 6 passed
python -m pytest tests/ -q → 2456 passed, 2 skipped (2450 + 6)
SW v151 → v152 + 4 gardiens verts
```

## 5. Suite

LOT 188 : survey — pages vivantes restantes (intelligence_page 662 l
/ 2 mentions), tools/, ou nouvelle direction. MINI-BILAN au lot 190.
