# Rapport — Lot 4 · Sécurité privée et exposition

## Les deux portes fermées

**1. Un démarrage privé non-loopback sans code ÉCHOUE.**
Avant : `VERTEX_LAN=1` ou `PORT` sans code démarrait sur `0.0.0.0` avec une
phrase d'avertissement — honnête, mais le portefeuille restait lisible par
tout le réseau. Désormais le processus **sort en erreur** (code 2) avec la
raison et les trois issues : `VERTEX_CODE`, `DEMO=1`, ou loopback. La
décision vit dans le propriétaire unique (`vertex/app/exposition.py`,
nouvelle clé `demarrage_refuse` + `raison`), calculée du même état que la
phrase — pas d'échappatoire, le contrat n'en prévoit pas.

**2. La démo exposée n'écrit pas.**
`POST /api/desk` et `/api/desk/restore` répondent `{ok:false, demo_exposee}`
quand `DEMO_MODE` **et** exposition réseau **et** pas de code. La **lecture**
reste servie (la démo se visite) ; la démo **locale** (loopback) continue
d'écrire — c'est le mode de travail quotidien, et notre propre mode de test.

## Déjà en place, vérifié et non refait

Verrou `VERTEX_CODE` (anti-force-brute, `hmac.compare_digest`, session 30 j) ·
cookies HttpOnly/SameSite=Lax/Secure(HTTPS) · nosniff · SAMEORIGIN ·
Referrer-Policy · Permissions-Policy · HSTS sous HTTPS · `no-store` sur
`/api/desk` · plafond 2 Mo · JSON NaN→null.

## Preuves

- gardien `tests/test_exposition_lot04.py` — **7 rouges d'abord**, 7 verts ;
- preuve fonctionnelle en client de test : POST exposé → refus honnête,
  GET exposé → 200, POST local → 200 ok ;
- refus de démarrage exercé : `exposition(False, {VERTEX_LAN:1, DEMO:0})` →
  `demarrage_refuse=True` avec la raison complète ;
- suite complète : **4301 passés · 0 échec**.

## Limites

- `PORT` + `VERTEX_CODE` reste le chemin hébergeur supporté (Render) : le
  refus ne s'applique qu'à l'absence de code hors démo.
- La minimisation IA et le scan secrets/PII du contrat lot 4 ne sont PAS
  traités ici — portée déclarée : les deux portes d'exposition. Le scan
  secrets existe déjà en gardiens de nommage ; la minimisation IA est à
  instruire avec le lot 10 (AdviceEngine).

## Rollback

Revert du commit : le comportement permissif revient (et les gardiens
repassent au rouge, ce qui est voulu).
