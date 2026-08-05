# SKYLER V2 — LOT 48 : cycle souverain complet dans la RC outillée

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-48-rc-sovereign-cycle`
(base : `integration/vertex-skyler-v2` @ `5cb5eff`, fraîchement fetchée) ·
Mode : développement continu.

## 1. Choix du lot — justification

Backlog proposé : (a) cycle souverain dans la RC outillée, (b) bilan
consolidé n°3, (c) autre. Choix : **(a)** — les lots 45/46/47 ont
construit la chaîne export → vérification → restauration, mais seule la
livraison du lot 47 l'a prouvée en navigateur, une fois. Le mécanisme le
plus critique du desk (la survie de l'historique décisionnel) mérite
d'être re-prouvé À CHAQUE RC, pas seulement le jour de sa livraison —
d'autant que DEUX défauts réels n'ont été visibles qu'en navigateur
(J-1 lot 37, empreinte JS lot 47).

## 2. Livré — `tools/rc_short_audit.js` étendu (CYCLE SOUVERAIN)

Après le parcours mémoire, chaque RC exécute désormais :

1. **export** : bundle téléchargé, présence de `content_sha256` exigée ;
2. **altération refusée** : une copie du bundle avec la note modifiée
   est POSTée — le serveur doit répondre **400 `empreinte_invalide`**
   (tout autre statut/erreur = défaut) ;
3. **restauration par le VRAI bouton** : le bundle INTACT est écrit dans
   un fichier temporaire puis uploadé via `setInputFiles` sur
   `#vx-mem-import-file` (le vrai chemin utilisateur, pas un fetch) —
   le message affiché doit dire la restauration et un ledger **SAIN** ;
4. tout écart alimente la liste de défauts (code retour 1) ; fichier
   temporaire nettoyé.

## 3. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1627 passed, 2 skipped (inchangé — outil
                                                     d'audit seulement)

tools/rc_short_audit.js (serveur DEMO=1 NO_IBKR=1) :
  8 pages HTTP 200 · console_err=0 · pageerror=0 · client-log n=0
  sw.js td-shell-v107 · /memory/<id> 200 · cellule 404 lisible dit
  import bundle altéré   HTTP 400  (empreinte_invalide)      ← refus prouvé
  import via bouton      « Restauration terminée — … »       ← bouton prouvé
  RC COURTE : GO — 0 défaut.
```

Aucun code produit touché → moteur 0.9.0 et **SW v107 inchangés**.

## 4. Invariants tenus

- l'altération est refusée et DITE ; la restauration passe par le vrai
  chemin utilisateur (bouton), pas un raccourci d'API ;
- données réelles uniquement (bundle réellement exporté, vraiment
  altéré, vraiment restauré — rien de simulé) ;
- READONLY absolu ; `domcontentloaded` ; fichiers runtime jamais
  commités ; `main` intacte.

## 5. Backlog (candidats lot 49)

1. Bilan consolidé n°3 (lots 44-48 : restauration souveraine complète,
   2 défauts réels attrapés en preuve navigateur, RC auto-prouvante) ;
2. Retour aux RC périodiques espacées si le backlog code s'épuise —
   chaque RC prouvant désormais AUSSI le cycle souverain.

**Arrêt après ce lot — validation humaine requise.**
