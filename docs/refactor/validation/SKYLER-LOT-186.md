# SKYLER V2 — LOT 186 : gardien des JS statiques et des liens d'assets

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-186`
(base : `integration/vertex-skyler-v2` @ `5fba96d`, lot 185 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Extension du lot 182 : le sweep validait les blocs <script> INLINE
des pages servies — les 31 fichiers JS chargés par `src=`
(chart-core, regime-aura, catalyst-runway, vx-shell, vx-core…)
n'étaient PAS couverts par node --check, et rien ne vérifiait que
les liens d'assets des pages résolvent.

## 2. Ce qui est figé (`tests/test_static_js_assets_lot186.py`, 5 tests)

```text
Syntaxe — les 31 fichiers JS du produit (hors vendor) parsent TOUS
  (node --check, 0 erreur, anti-vide ≥ 30) ; seul exclu documenté :
  la bibliothèque tierce minifiée lightweight-charts (vendor)
Liens — les ≥ 40 assets (<script src=> + <link css>) référencés par
  les 13 routes servies résolvent TOUS en 200 (aucun lien mort) ;
  AUCUN asset http(s) externe (autonomie hors-ligne — acquis polices
  auto-hébergées des lots 81-85, désormais gardé en continu)
Espaces de noms — chaque builder charts/*.js s'enregistre sur
  VXCharts ; seule exception documentée : le thème
  (chart-theme-obsidian-copper.js) chargé AVANT chart-core, qui
  expose VXChartTheme (miroir de palette.py, déjà gardé par
  test_js_theme_matches_python_palette)
Constat : tout l'état présent est sain (0 invalide, 0 lien mort,
  0 externe) — les gardiens empêchent la régression
```

## 3. Preuves

```text
python -m pytest tests/test_static_js_assets_lot186.py -q → 5 passed
python -m pytest tests/ -q → 2450 passed, 2 skipped (2445 + 5)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 187 : candidats — pages vivantes de la refonte les moins gardées
(survey a), tools/ d'audit, ou nouvelle direction. MINI-BILAN au
lot 190.
