# SKYLER V2 — LOT 52 : crosshair app au survol + harmonisation multiLine

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-52-crosshair`
(base : `integration/vertex-skyler-v2` @ `aada9d3`, fraîchement fetchée) ·
Mode : développement, axe VISUEL (direction utilisateur « plus plus plus 2026 »).

## 1. Justification du choix de lot

Suite directe du lot 51 sur l'axe visuel demandé. Ce qui manquait encore
pour le ressenti « app de courtage » : la **ligne de visée au survol**
(crosshair) — présente dans toutes les apps de courtage modernes — et la
cohérence de `C.multiLine` (comparaisons multi-séries), resté sur l'ancien
rendu (1,5 px, tension .25 non monotone). Même stratégie que le lot 51 :
livraison **centrale** dans `chart-core.js`, zéro fork.

## 2. Livré (fichier unique `vertex/static/vertex/js/charts/chart-core.js`)

- **`C.crosshairPlugin(color)`** (id `vxCrosshair`) : ligne de visée
  VERTICALE pointillée (`setLineDash [3,3]`, `color+'59'`) du haut en bas
  de la zone de tracé, **suivant le point ACTIF du tooltip** (mode index —
  `getActiveElements`, jamais dessinée hors survol, `tt.opacity === 0`
  respecté) + point actif surligné (r=3, couleur pleine) ;
- **câblé par défaut dans `C.area`** (`{crosshair:true}` désactivable) —
  s'empile avec `vxGlow` et `vxLastDot` du lot 51 ;
- **`C.multiLine` harmonisé sur la signature 2026** : lissage
  `cubicInterpolationMode 'monotone'` (jamais de faux extrêmes entre les
  points réels), ligne 2 px, tension .35, crosshair (couleur `C.colors.brand`)
  — mêmes principes que `C.area`, désactivable `{crosshair:false}`.

Palette : **aucun littéral couleur nouveau** — gardien à inventaire exact
identique au lot 51 (le lot n'a le droit d'en ajouter aucun).

## 3. Tests (rouges d'abord — 5 nouveaux)

`tests/test_charts_2026_lot52.py` (rouge confirmé avant l'édition — 4/5,
le gardien anti-littéral étant une non-régression déjà verte, attendu) :
`vxCrosshair` + `setLineDash` + `getActiveElements` dans la section du
plugin · `C.area` câble `C.crosshairPlugin` (opt `crosshair`) ·
`C.multiLine` monotone + 2 px + crosshair · aucun hex nouveau · SW ≥ v109
et v108 absent.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_charts_2026_lot52.py -q → 5 passed
python -m pytest tests/ -q → 1638 passed, 2 skipped   (1633 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut
  (8 pages 0 erreur console · client-log 0 · SW v109 servi · parcours
   mémoire · cycle souverain : altération refusée + restauration bouton)
Preuve navigateur visuelle (Chromium, survol réel au 2/3 du graphique
/markets) : ligne de visée verticale pointillée rendue à la position du
curseur, point actif surligné, tooltip affiché, pastille de dernier prix
« 413,00 » du lot 51 toujours rendue — 0 erreur console.
```

SW `td-shell-v108` → `td-shell-v109` (`vertex/app/routes/system.py`) + les
4 gardiens mis à jour (y compris les assertions « vN-1 absent »).

## 5. Invariants

READONLY intact · données réelles uniquement — le crosshair ne fait que
POINTER un point réel existant (aucune valeur inventée), le lissage
monotone de `multiLine` ne dépasse jamais les données · moteur 0.9.0
inchangé (zéro ligne moteur) · `main` intacte · fichiers runtime non
commités.

## 6. Suite (axe visuel — « plus plus plus »)

Candidats lot 53 : polish des chandeliers (`C.candles` s'il existe — mèches
fines, corps arrondis), profondeur des cartes (élévation/glass), donut/bars
harmonisés (coins arrondis déjà partiels). La validation humaine physique
reste l'étape décisive.

**Arrêt après ce lot — validation humaine requise.**
