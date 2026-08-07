# SKYLER LOT 226 — Budgets JS/CSS statiques : mesure de dérive (gardien vert, marge fondue documentée)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-226` (base : lot 225 fusionné)

## Objet

Piste proposée trois fois, enfin prise : mesurer les tailles réelles
de `vertex/static/**` contre les gardiens de budget du lot 72
(`test_perf_lot72.py` — 64 kB par fichier première partie, vendor
isolé sur /analysis).

## Mesure

### JS première partie (top 6, hors vendor)

| Fichier | Taille | vs budget 64 kB |
|---|---:|---:|
| charts/chart-core.js | **57,2 kB** | **89 %** |
| pages/options-intel.js | 39,1 kB | 61 % |
| pages/options-structure.js | 36,8 kB | 58 % |
| vx-entities.js | 31,7 kB | 50 % |
| vx-core.js | 27,0 kB | 42 % |
| vx-shell.js | 21,4 kB | 33 % |

### CSS (top 2) et vendor

- neon-glass.css : **47,0 kB** (73 %) ; components.css 17,0 kB ;
- vendor lightweight-charts : 159,8 kB — gardien d'isolement vert
  (absent du shell, chargé par /analysis seule).

## Verdict

- **Gardien VERT, aucune violation** : tout fichier première partie
  est sous 64 kB.
- **Dérive réelle documentée** : chart-core.js est passé de ~39 kB
  (calibration lot 72) à **57,2 kB** — les +18 kB sont le coût
  LÉGITIME de la tournée graphique TV (lots 189-213 : jauge TV,
  hachures, chips, extrêmes, radar dominant, levelLines, dominantes) —
  mais la marge restante n'est plus que de **6,8 kB**.
- **Contre-vérité corrigée** : le commentaire de calibration du
  gardien disait encore « chart-core/options-intel 39 kB » — recalibré
  aux valeurs mesurées, avec la consigne explicite : au prochain
  palier, **discuter le budget AVANT de le crever** (pas de hausse en
  douce du budget — c'est exactement la dérive que le gardien ferme).

Aucun code produit touché — recalibration de commentaire dans le test
+ constat chiffré.

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : tests/docs seulement.

## Preuves

- `test_perf_lot72.py` : 3/3 verts après recalibration.
- Suite complète : **2482 passed / 2 skipped** (référence maintenue).

## Suite

LOT 227 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
