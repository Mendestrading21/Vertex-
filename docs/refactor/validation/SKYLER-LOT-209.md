# SKYLER LOT 209 — A11y : drawer/modal fermés aria-hidden + inert

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-209` (base : lot 208 fusionné)

## Livré

### Correctif d'accessibilité (observation du lot 206)

Les panneaux hors-canvas FERMÉS (drawer d'entité, modal) restaient
exposés aux lecteurs d'écran et au focus clavier :

1. **Shell (`vertex/ui/shell/__init__.py`)** : `aria-hidden="true"` +
   `inert` posés sur `#vx-drawer` et `#vx-modal` dans le markup servi
   (état initial fermé).
2. **`vx-shell.js`** : helpers `panelOpen/panelClose` — l'ouverture
   RETIRE les deux attributs, la fermeture les REPOSE ; drawer et
   modal passent par le même chemin. Retour de focus (`lastFocus`)
   préservé.
3. Sidebar mobile : non touchée — elle est VISIBLE sur desktop et son
   repli est piloté par media query CSS ; un aria-hidden JS
   introduirait un risque de régression desktop pour un gain nul
   (constat rapporté, hors périmètre du correctif sûr).

### Gardien `tests/test_a11y_drawer_lot209.py` (5 tests)

Drawer fermé aria-hidden + inert dans le HTML SERVI ; modal idem ;
identité dialogue conservée (role/aria-modal/aria-label) ; la source
JS bascule bien les deux attributs dans les deux sens via
panelOpen/panelClose ; le retour de focus n'a pas été cassé.

### Preuve navigateur (cycle complet)

FERMÉ `{aria-hidden:'true', inert:true}` → OUVERT (openDrawer)
`{aria-hidden:null, inert:false}` → REFERMÉ `{aria-hidden:'true',
inert:true}` — 0 erreur console.

## Décision SW

Bump `td-shell-v167` → `v168` + 5 gardiens : le HTML du shell change —
sans bump, les clients au SW en cache ne recevraient jamais le
correctif (le bump est ici le VECTEUR de déploiement, pas un
changement cosmétique).

## Preuves

- `node --check` OK (vx-shell.js) ; import shell OK.
- Suite complète : **2466 passed / 2 skipped** (2461 + 5 nouveaux).
- Capture drawer ouvert envoyée.

## Suite

LOT 210 : MINI-BILAN 206-210 + prochain entretien ou directive.
