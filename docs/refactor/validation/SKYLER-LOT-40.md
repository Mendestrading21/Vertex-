# SKYLER V2 — LOT 40 : vue HTML lisible de la cellule de calibration

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-40-cell-view`
(base : `integration/vertex-skyler-v2` @ `57efe44`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) vue HTML lisible de la cellule, (b) RC
courte étendue, (c) fuzz de la route cell. Choix : **(a)** — le
complément direct du lot 39 : les badges pointaient vers du JSON brut,
utilisable pour l'audit mais pas pour la lecture. La vue lisible ferme
la boucle trader : badge → cellule → record → post-mortem, tout en HTML.

## 2. Périmètre livré

### 2.1 Route — `GET /memory/cell/<group>/<key>` (HTML)

Même mécanique que la vue post-mortem du lot 23 (`render_shell` +
markupsafe partout) :

- résumé de cellule : facteur, hit rate, n mesures (ou « INSUFFISANT —
  n mesure(s), facteur non calculé »), basis moteur ;
- table des décisions MESURÉES : titre, séance, décision, niveau,
  régime, catalyseur (avec type), résultat honnête — badge vert
  « contenu (hit) » / rouge « hors scénarios (miss) » — et lien
  « détail → » vers le post-mortem `/memory/<id>` de chaque record ;
- retour vers Performance ; 404 LISIBLES (groupe inconnu avec la liste
  des groupes valides, cellule inconnue) ;
- source de données : `cell_decisions` du lot 39 (source unique
  d'appartenance) — la vue lit, ne recalcule rien.

### 2.2 Badges — vers la vue lisible

Les badges de la carte Mémoire visent désormais `/memory/cell/…`
(l'API JSON `/api/skyler/memory/cell/…` reste servie pour l'audit,
couverte par ses tests de route du lot 39 — gardien lot 39 mis à jour
en conséquence, commentaire daté). Shell visible → **SW v105 → v106**
+ 4 gardiens.

## 3. Méthode — rouge d'abord

`tests/test_cell_view_lot40.py` (7 tests) écrit AVANT ; premier passage
6 failed / 1 passed (le test badges durci après avoir constaté qu'il
passait trivialement par sous-chaîne — rouge réel confirmé ensuite).
Après : **7 passed**.

Couverture : résumé + table + liens post-mortem sur magasin construit
(25 records mesurés) ; hit/miss dits honnêtement ; **XSS : symbole
hostile figé AFFICHÉ ÉCHAPPÉ** (`&lt;script&gt;` visible, jamais exécuté,
jamais caché) ; 404 lisibles × 2 ; magasin corrompu sans 500 ; badges →
vue lisible (et plus l'API) ; SW ≥ v106.

## 4. Preuves

```text
python -m pytest tests/test_cell_view_lot40.py -q → 7 passed
python -m compileall -q terminal.py vertex        → exit 0
python -m pytest tests/ -q → 1593 passed, 2 skipped (baseline 1586 → +7)

tools/rc_short_audit.js : 8 pages HTTP 200 · console_err=0 · pageerror=0
  /api/client-log n=0 · sw.js td-shell-v106 · RC COURTE : GO — 0 défaut.

Live : GET /memory/cell/by_level/INEXISTANT → 404 (lisible)
       GET /memory/cell/by_magie/A          → 404 (lisible)
```

Moteur 0.9.0 inchangé — la vue lit `cell_decisions`, ne recalcule rien.

## 5. Invariants tenus

- XSS : markupsafe sur TOUT contenu mémoire (prouvé sur symbole
  hostile — affiché échappé, pas caché : la donnée réelle reste dite) ;
- données réelles uniquement : hit/miss réels par record, n/d honnête,
  404 dits ; la vue ne recalcule ni n'invente ;
- source unique (lot 39) consommée telle quelle ; lecture seule ;
- SW bump v106 + 4 gardiens ; RC courte GO ; `main` intacte ;
- fichiers runtime jamais commités.

## 6. Backlog restant (candidats lot 41)

1. RC courte étendue (`/memory/<id>` + `/memory/cell/…` d'un record réel
   dans le parcours de `tools/rc_short_audit.js`) ;
2. Fuzz dédié de la route cell (clés encodées dégénérées — la batterie
   lot 34 couvre déjà les patrons voisins) ;
3. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
