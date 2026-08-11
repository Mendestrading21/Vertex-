# SKYLER LOT 286 — Verdict de version « à jour / mise à jour disponible »

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-286` (base : lot 284 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Le « Go » utilisateur (lot 285) a lancé la purge Étape 1. La moitié
1/2 (adaptation des tests, catégories B/C de l'annexe) est FAITE et
poussée (`agent/skyler-v2-lot-285`, commit b8d3842). La moitié 2/2
(retrait des 82 défs / 5 236 lignes dans terminal.py, table des spans
prête) est **bloquée par le classifieur de permissions du mode auto**
(3 approches raisonnables refusées) — en attente d'un déblocage
utilisateur (règle Bash, mode interactif, ou « réessaie »). Aucune PR
É1 tant que l'étape n'est pas complète. **Le GO reste acquis.**

## Livré ce lot (développement, carte Application)

`renderAppInfo` compare désormais DEUX versions réelles :

- **Version locale (cache de cet appareil)** : `caches.keys()`.
- **Version publiée (serveur)** : lue de `/sw.js` servi à l'instant
  (`fetch {cache:'no-store'}` → `td-shell-vN`) — donnée réelle déjà
  servie, aucun endpoint nouveau.
- **Badge verdict** : « à jour » si égales, « mise à jour disponible »
  si le serveur est plus récent — l'utilisateur sait si le bouton de
  mise à jour (lot 284) vaut le clic. Une version manquante → « n/d »
  honnête, jamais un verdict inventé.

## Gardien neuf — `tests/test_app_version_check_lot286.py` (2 tests)

Version serveur lue de /sw.js sans cache ; verdict = comparaison
réelle `server>local` + états n/d honnêtes. (Le gardien du lot 284
continue d'interdire tout numéro de version codé en dur.)

## Preuves (navigateur réel, DEMO)

- Affiché : **« locale td-shell-v176 · publiée td-shell-v176 · badge
  “à jour” »** — deux lectures indépendantes qui concordent.
- 0 erreur console ; pas de débordement (1416/1440) ; capture envoyée.
- Suite complète : **2494 passed / 2 skipped** (+2).

## Décision SW

**Bump v175 → v176** (contenu de la carte change) + les 5 gardiens.

## Suite

LOT 287 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
