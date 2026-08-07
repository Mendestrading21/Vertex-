# SKYLER LOT 290 — Échéance périodique : smoke-check complet (4e mesure)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-290` (base : lot 289 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Protocole (lot 251, inchangé)

Serveur DEMO, navigateur réel 1440×900 : 8 pages racines, écoute
`console error` + `pageerror`, `/api/client-log`, `/healthz`.

## Résultat — SAIN, écart unique EXPLIQUÉ

- **8 × HTTP 200**, titres corrects.
- **0 erreur** console/pageerror sur les 8 pages.
- `/api/client-log` : `count: 0`. `/healthz` : `status: ok`, moteurs
  complets, univers 517.
- Tailles de texte vs référence (lots 251/270/280 — 3 mesures
  identiques) : **7 pages sur 8 STRICTEMENT identiques** (/ 3370,
  /markets 2794, /opportunities 4679, /analysis 923, /portfolio 1609,
  /options 2955, /journal 2676).
- **/system : 3897 → 4124 (+227)** — expliqué, pas masqué : la vue par
  défaut de /system est `connections` (`_DEFAULT_VIEW`), précisément la
  vue où le lot 283 a livré la carte « Verrou d'accès » (badge d'état +
  faits + marche à suivre). C'est la SEULE modification de cette vue
  depuis le lot 280 ; les cartes des lots 284/286 vivent dans
  `?view=settings`, hors de cette mesure. Écart = fonctionnalité
  livrée, base saine.

Les tailles des lots 288/289 n'apparaissent pas ici : CSS mobile
(≤640px) — la mesure est à 1440.

## Autres vérifications

- Suite complète : **2498 passed / 2 skipped** (référence maintenue).
- Nouvelle référence pour les prochaines mesures : /system = **4124**
  (les 7 autres inchangées).

## Décision SW

**Pas de bump** (`td-shell-v178`) : docs seulement, aucun octet servi
modifié.

## Suite

LOT 291 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
Prochaine échéance périodique : ~lot 300.
