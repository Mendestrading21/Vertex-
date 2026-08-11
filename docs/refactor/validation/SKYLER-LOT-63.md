# SKYLER V2 — LOT 63 : mini-aires de Marchés lissées monotone (signature 2026)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-63-inspection`
(base : `integration/vertex-skyler-v2` @ `85595e4`, fraîchement fetchée) ·
Mode : travail continu.

## 1. Justification du choix de lot

Écart de cohérence RÉEL constaté en capture (lot 56) : sur Marchés, les
mini-aires des cartes d'indices (`sparkArea`, SVG local de
markets_page.py) étaient des POLYLIGNES anguleuses rendues juste
au-dessus du grand graphique `C.area` lissé monotone — deux langages
visuels sur la même page.

## 2. Livré

- `monotonePath(xs, ys)` : lissage **monotone Fritsch-Carlson** — même
  principe que le `cubicInterpolationMode 'monotone'` de Chart.js
  (lot 51) : la courbe ne dépasse JAMAIS les données réelles, les points
  restent exacts, le calcul est déterministe (aucun aléatoire) ;
- `sparkArea` trace désormais ligne ET aire sur ce chemin lissé — le
  dégradé de remplissage et le point actif final sont conservés tels
  quels ; couleurs inchangées (tokens sémantiques) ;
- `sparkSvg` (ancien mini-trait) : AUCUN consommateur dans tout le dépôt
  (vérifié par grep) — code mort SUPPRIMÉ.

## 3. Tests (rouges d'abord — 5 nouveaux)

`tests/test_polish_lot63.py` (rouge confirmé sur les comportements
nouveaux) : chemin lissé monotone présent, plus de polyline/polygon dans
la section · dégradé + point final conservés · aucun aléatoire ·
sparkSvg absent · SW ≥ v119.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1684 passed, 2 skipped   (1679 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v119 servi,
  cycle souverain inclus)
Preuve navigateur /markets : les 4 mini-aires des cartes d'indices
  rendent un <path> avec courbes cubiques (« C ») — 4/4, zéro polyline
  restante — 0 erreur console. Capture carte S&P 500 conservée.
```

SW `td-shell-v118` → `td-shell-v119` + 4 gardiens.

## 5. Invariants

READONLY intact · aucun moteur touché · données réelles uniquement (le
lissage n'invente jamais d'extrême — Fritsch-Carlson est monotone par
construction) · zéro littéral couleur nouveau · `main` intacte ·
fichiers runtime non commités.

## 6. Suite

Boucle continue ré-armée (un seul send_later). Le langage visuel 2026
est maintenant uniforme sur les graphiques du produit (Chart.js + SVG
locaux). Prochain réveil : nouveau tour d'inspection honnête — si plus
rien de prouvable, RC périodique et bascule en surveillance espacée.

**Arrêt après ce lot — validation humaine requise.**
