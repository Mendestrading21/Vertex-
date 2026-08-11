# SKYLER V2 — LOT 72 : PROGRAMME 100 % — audit PERFORMANCE

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-72-performance`
(base : `integration/vertex-skyler-v2` @ `f13109e`, fraîchement fetchée).

## 1. Mesures réelles (Playwright, cache froid par page, serveur démo)

```text
page            DCLms  totalKB  res   js(kB)    css(kB)   doublons/erreurs
/                1021      689   47   10(345)   16(118)   -
/markets          297     1097   39   13(340)   16(118)   -
/opportunities    224     1116   44   15(342)   16(118)   -
/analysis         274      535   33    8(336)   16(118)   -
/portfolio        244      559   45   16(341)   16(118)   -
/options          299      619   43   17(435)   16(118)   -
/journal          244      515   35    9(336)   16(118)   -
/system           239      536   40   10(336)   16(118)   -
```

(Le 1021 ms de `/` = démarrage à froid du navigateur, pas la page — les
7 suivantes mesurent 224-299 ms.)

## 2. Verdict : SAIN

- **0 doublon** de chargement, **0 ressource en erreur** (≥400) ;
- vendor `lightweight-charts` (160 kB, le plus gros fichier du dépôt)
  chargé UNIQUEMENT par `/analysis` — lazy loading correct, vérifié ;
- plus gros fichiers première partie : chart-core.js 39 kB,
  options-intel.js 39 kB, neon-glass.css 46 kB — raisonnables ;
- poids total par page 515-1116 kB (le haut = données JSON de scan,
  pas des assets) ; DCL < 300 ms partout en régime établi.

**Aucun défaut réel — lot documentaire avec mesures publiées.**

## 3. Gardiens prospectifs (nés verts, dits)

`tests/test_perf_lot72.py` (3 tests) : vendor jamais dans le shell +
budget 64 kB par fichier JS première partie + budget 64 kB par CSS —
toute dérive future de poids cassera la suite.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1699 passed, 2 skipped   (1696 + 3)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v123)
Responsive 8 × 3 → 0 débordement, 0 erreur
```

Pas de bump SW : aucun changement de shell visible.

## 5. Suite

Lot 73 : accessibilité — angles restants (navigation clavier complète,
aria des contrôles dynamiques, contrastes).
