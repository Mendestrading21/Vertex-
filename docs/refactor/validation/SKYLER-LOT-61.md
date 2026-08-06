# SKYLER V2 — LOT 61 : runway anti-collision + fallbacks des charts JS purgés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-61-runway-labels`
(base : `integration/vertex-skyler-v2` @ `ddb2f78`, fraîchement fetchée) ·
Mode : reprise du travail continu (« continue » utilisateur après l'arrêt
du lot 60).

## 1. Justification du choix de lot

Défaut visuel RÉEL repéré sur la capture du lot 56 et volontairement
laissé de côté alors : les étiquettes du Catalyst Runway (briefing) se
chevauchaient quand plusieurs catalyseurs tombent sur des DTE proches
(ALB J-7 / ARE J-7 / Inflation J-8 illisibles). En inspectant le fichier,
seconde trouvaille : le gardien anti-palette-périmée du lot 59 couvrait
les pages Python mais PAS les JS de charts — 25 fallbacks d'anciennes
palettes y restaient.

## 2. Runway : anti-collision déterministe

L'alternance haut/bas par PARITÉ d'index posait parfois deux étiquettes
proches du même côté, et le bornage au bord droit pouvait les rapprocher
encore (défaut résiduel attrapé par le harnais de preuve au premier
essai — corrigé avant livraison, dit). Solution finale : **deux rangées
d'étiquettes par côté**, chaque étiquette prenant la première rangée où
il reste ≥ MIN_GAP de place, calculée sur la position BORNÉE au viewBox.
Déterministe (même calendrier → même dessin, aucun aléatoire) ;
l'étiquette ne sort jamais de la piste ; viewBox 84 → 120 de haut.

## 3. Charts JS : 25 fallbacks périmés purgés

`chart-core.js` (12), `catalyst-runway.js` (3), `anomaly-scan.js` (4 —
dont le token INEXISTANT `--vx-text-dim` ACTIF), `regime-aura.js` (2) +
3e token fantôme découvert : `--vx-bg-app` → remappé sur `--vx-bg-0`
(réel). Gardiens PROSPECTIFS étendus au répertoire charts : fallback ∈
valeurs actuelles + token référencé existant. Inventaires hex des
gardiens 51-53 mis à jour en conséquence (+#121214, +#F8F5F3 canoniques).

## 4. Tests (rouges d'abord — 5 nouveaux)

`tests/test_charts_2026_lot61.py` (rouge 5/5 confirmé) : plus de parité
(`i % 2` absent) + `MIN_GAP`/rangées présents · étiquettes bornées ·
fallbacks charts ∈ palette actuelle · tokens référencés existants ·
SW ≥ v117.

## 5. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1675 passed, 2 skipped   (1670 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v117 servi,
  cycle souverain inclus)
Preuve navigateur par HARNAIS (calendrier DENSE de la capture lot 56 :
  J-2/J-3/J-5/J-7/J-7/J-8) : chevauchements MESURÉS entre les 12 textes
  (bounding boxes) = 0 ; hors-limites = 0 ; 0 erreur console. Le premier
  essai (1 chevauchement résiduel dû au bornage) a été attrapé par ce
  même harnais et corrigé — la preuve a fait son travail. Capture :
  lot61_runway.png.
```

SW `td-shell-v116` → `td-shell-v117` + 4 gardiens.

## 6. Invariants

READONLY intact · aucun moteur touché · aucun aléatoire (placement
déterministe) · zéro littéral couleur nouveau (25 périmés remplacés) ·
`main` intacte · fichiers runtime non commités.

## 7. Suite

Boucle continue ré-armée (un seul send_later). Candidats lot 62 :
balayage des fallbacks restants hors charts (vx-shell/vx-core/vx-entities
JS), ou harmonisation des mini-charts SVG de markets_page (sparkArea
locale vs signature 2026).

**Arrêt après ce lot — validation humaine requise.**
