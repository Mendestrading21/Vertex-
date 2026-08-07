# SKYLER LOT 297 — Honnêteté : le chip « Live » du stress test suivait le mode

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-297` (base : lot 296 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — honnêteté des 18 vues profondes

Le sondeur du lot 296 étendu aux 18 vues (?view= + fiche analyse +
/tracking) : étiquette démo, lignes .vx-update, et CHASSE aux
revendications « réel(les) » dans le texte affiché en DEMO. Tri des
~30 occurrences : presque toutes légitimes (déclarations d'honnêteté
« jamais présentées comme réelles », questions, adverbes, trades
déclarés par l'utilisateur — qui restent SES données en tout mode).

**Un cas reproduisait exactement le défaut du lot 296** :
`/portfolio?view=risk` affichait « À l'instant · risk_engine
(positions réelles) · **Live** » en plein DEMO — le mode « live »
était codé EN DUR (`portfolio_page.py` L801), alors que les 4 cartes
jumelles de la même page suivent honnêtement `window.__pfLive`
(live/fallback selon /api/pos-quotes). Le libellé « positions
réelles » est quant à lui le vocabulaire établi de la page (positions
déclarées par l'utilisateur, par opposition aux candidats du
scanner — l'état vide L712 le dit explicitement) : conservé.

## Livré

`portfolio_page.py` L801 : `'live'` → `window.__pfLive?'live':'fallback'`
— aligné sur les cartes jumelles (L560/573/654/704).

## Gardien neuf — `tests/test_risk_footer_mode_lot297.py` (2 tests)

Le pied suit __pfLive + plus AUCUN `,'live')` codé en dur dans la page.

## Preuves (navigateur réel, DEMO)

- /portfolio?view=risk : « risk_engine (positions réelles) ·
  **Secours** » (`__pfLive:false`) — le chip Live a disparu en repli ;
  0 erreur console. Capture envoyée.
- Suite complète : **2510 passed / 2 skipped** (+2).

## Décision SW

**Bump v183 → v184** (JS de page servi change) + les 5 gardiens.

## Suite

LOT 298 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
