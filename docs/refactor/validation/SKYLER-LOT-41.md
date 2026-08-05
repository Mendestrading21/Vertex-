# SKYLER V2 — LOT 41 : RC courte étendue au parcours mémoire

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-41-rc-memory-journey`
(base : `integration/vertex-skyler-v2` @ `ba91859`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) RC courte étendue au parcours mémoire,
(b) fuzz dédié des routes cellule, (c) autre. Choix : **(a)**.

- Les lots 20/23/39/40 ont construit la chaîne mémoire complète
  (décision → record figé → post-mortem → cellule) mais l'audit
  périodique outillé (lot 32) ne parcourait que les 8 pages : les vues
  mémoire n'étaient vérifiées en navigateur qu'à la main, lot par lot.
  Désormais chaque RC courte prouve AUSSI la chaîne mémoire.
- (b) reste au backlog — les patrons voisins sont déjà couverts (lot 34).

## 2. Livré — `tools/rc_short_audit.js` étendu

Après le parcours des 8 pages, l'audit :

1. **fige une décision démo** (`/api/skyler/AAPL`) puis lit le dernier
   record de `/api/skyler/memory` ;
2. **vérifie `/memory/<id>` en vrai navigateur** : HTTP 200, texte
   « Décision figée » présent, 0 erreur console ;
3. **vérifie la vue cellule** : si le magasin publie une cellule,
   `/memory/cell/<group>/<key>` doit rendre 200 ; sinon (démo : aucune
   cellule mesurée — honnête) le **404 LISIBLE est vérifié et DIT**
   (« Cellule inconnue » présent) — jamais un état inventé ;
4. tout écart alimente la liste de défauts (code retour 1).

## 3. Défaut d'OUTIL trouvé et corrigé pendant le lot

Premier passage : faux défaut « Décision figée absent » alors que la vue
servait bien le texte — `document.body.innerText` reflète la casse
AFFICHÉE (`text-transform: uppercase` CSS → « DÉCISION FIGÉE — AAPL »).
Correctif : comparaison insensible à la casse, documentée dans l'outil.
C'est un défaut de l'outil d'audit, pas du produit — dit comme tel.

## 4. Preuves

```text
NODE_PATH=… node tools/rc_short_audit.js (serveur DEMO=1 NO_IBKR=1) :
  8 pages HTTP 200 · console_err=0 · pageerror=0
  /healthz 200 · /api/client-log n=0 · sw.js td-shell-v106
  /memory/c860630af7b04767              HTTP 200  console_err=0
  /memory/cell/by_level/AUCUNE_CELLULE  HTTP 404  console_err=0
  (aucune cellule mesurée publiée — 404 lisible vérifié à la place)
  RC COURTE : GO — 0 défaut.

python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1593 passed, 2 skipped (inchangé — outil
                                                     d'audit seulement)
```

Aucun code produit touché → moteur 0.9.0 et **SW v106 inchangés** (pas de
bump : l'outil n'est pas du shell servi).

## 5. Invariants tenus

- données réelles uniquement : l'absence de cellule mesurée en démo est
  DITE et le 404 lisible vérifié à la place — jamais un état simulé ;
- READONLY absolu (l'audit lit ; la décision démo figée est le
  comportement produit normal de la route d'analyse) ;
- `domcontentloaded` (jamais networkidle) ; fichiers runtime jamais
  commités ; `main` intacte.

## 6. Backlog restant (candidats lot 42)

1. Fuzz dédié `/memory/cell` (clés encodées dégénérées) si un doute
   apparaît — patrons voisins déjà couverts lot 34 ;
2. Bilan périodique suivant (lots 38+) quand le volume le justifiera ;
3. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
