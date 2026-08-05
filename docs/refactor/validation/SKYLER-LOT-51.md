# SKYLER V2 — LOT 51 : graphiques niveau app 2026 (signature visuelle centrale)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-51-charts-2026`
(base : `integration/vertex-skyler-v2` @ `960857b`, fraîchement fetchée) ·
Mode : développement, axe VISUEL (direction utilisateur explicite).

## 1. Justification du choix de lot

Direction utilisateur active : « Continue et continue encore à plus de le
voiler les graphique le visuel un peux comme ibtk mais la vertion app ce
genre de nouveau visuelle plus plus plus 2026 » — pousser le visuel des
graphiques vers un rendu d'app de courtage moderne (esprit app IBKR).
Le lot 50 avait conclu NO-GO sur l'axe optimisation ; l'axe visuel devient
donc l'axe de travail. Choix d'implémentation : livrer la signature
**CENTRALEMENT dans `chart-core.js`** (le renderer commun `C.area`) — toutes
les cartes `areaCard` du produit en bénéficient d'un coup, **zéro fork** de
renderer, zéro divergence future.

## 2. Livré (fichier unique `vertex/static/vertex/js/charts/chart-core.js`)

La signature visuelle 2026, appliquée à `C.area` :

- **Courbe lisse monotone** : `cubicInterpolationMode: 'monotone'`
  (+ tension .35) — le lissage ne dépasse **jamais** les données réelles
  (pas de faux extrêmes inventés par l'interpolation : invariant « données
  réelles uniquement » respecté jusque dans le rendu), les points restent
  exacts ;
- **Dégradé d'aire riche 3 arrêts** : `color+'4D'` → (0.45) `color+'17'` →
  `color+'00'` — profondeur de fondu façon app moderne (avant : 2 arrêts) ;
- **Glow subtil de la ligne** : plugin `C.glowPlugin` (id `vxGlow`) —
  `shadowColor color+'59'`, `shadowBlur 7`, dataset principal seulement ;
- **Pastille de dernier prix** : plugin `C.lastDotPlugin` (id `vxLastDot`) —
  halo (r=7, `color+'22'`) + point (r=3) sur le **dernier point réel**
  (les null de fin de série sont sautés — jamais un point interpolé) +
  pilule de prix (`ctx.roundRect`) au bord droit, texte via `yFmt` ou
  `VX.fmt.price`, contraste texte = fond tooltip du thème (`#151719`
  secours déjà présent dans le fichier) ;
- **Ligne** : `borderWidth 2` (avant 1.6) + `interaction {mode:'index',
  intersect:false}` (survol type app de courtage) ;
- **Opts nouveaux** `C.area(..., {last:true, glow:true})` — désactivables
  par appelant, activés par défaut (toutes les cartes upgradées).

Palette : **aucun littéral couleur nouveau** — uniquement `C.colors` + les
suffixes alpha sur la couleur reçue (idiome déjà en place). `C.mount`
transmet la config telle quelle à `new Chart(...)` — le tableau `plugins`
top-level est du Chart.js natif, aucun changement de `C.mount`.

## 3. Tests (rouges d'abord — 6 nouveaux)

`tests/test_charts_2026_lot51.py` (rouge 6/6 confirmé avant l'édition) :
monotone présent · ≥3 `addColorStop` dans la section `C.area` · `vxGlow` +
`shadowBlur` · `vxLastDot` + pilule · **gardien anti-littéral** (inventaire
exact des hex existants du fichier — le lot n'a le droit d'en ajouter
AUCUN) · SW ≥ v108 et v107 absent.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_charts_2026_lot51.py -q → 6 passed
python -m pytest tests/ -q → 1633 passed, 2 skipped   (1627 + 6)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut
  (8 pages 0 erreur console · client-log 0 · SW v108 servi · parcours
   mémoire · cycle souverain : altération refusée 400 empreinte_invalide
   + restauration par le vrai bouton Importer)
Preuve navigateur visuelle (Chromium, 1280×900) :
  /, /markets, /portfolio → 0 erreur console ;
  CanvasRenderingContext2D.roundRect supporté (true) ;
  capture du canvas /markets : courbe lisse + glow + dégradé profond +
  pastille « 413,00 » au bord droit — signature app 2026 rendue.
```

SW `td-shell-v107` → `td-shell-v108` (`vertex/app/routes/system.py`) + les
4 gardiens mis à jour (production_guards_canonical, reconstruction_today,
redesign_ui, ui_v3 — y compris les assertions « vN-1 absent »).

## 5. Invariants

READONLY intact (aucun ordre) · données réelles uniquement — le lissage
monotone est choisi précisément parce qu'il n'invente jamais d'extrême, et
la pastille affiche la vraie dernière valeur (jamais interpolée) · moteur
0.9.0 inchangé (zéro ligne moteur touchée) · `main` intacte · fichiers
runtime non commités.

## 6. Suite (axe visuel — « plus plus plus »)

Candidats lot 52 sur le même axe : crosshair/tooltips raffinés (ligne de
visée verticale type app), harmonisation `C.multiLine`/sparklines sur la
même signature, polish chandeliers, profondeur des cartes. La validation
humaine physique reste l'étape décisive.

**Arrêt après ce lot — validation humaine requise.**
