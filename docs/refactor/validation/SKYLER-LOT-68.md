# SKYLER V2 — LOT 68 : AUDIT TOTAL (volet 3) — IBKR lecture seule : sain

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-68-ibkr-readonly`
(base : `integration/vertex-skyler-v2` @ `32178d8`, fraîchement fetchée) ·
Programme AUDIT TOTAL — lot DOCUMENTAIRE (aucun code produit modifié).

## 1. Audit statique du code IBKR — les 4 verrous en place

| Verrou | Constat |
|---|---|
| `readonly=True` | **EN DUR** dans `ibkr_gateway.py` (« codé en dur et non paramétrable » — la façade ne PEUT PAS ouvrir une session d'ordre) |
| `RequestTimeout` | `REQUEST_TIMEOUT_S = 45` appliqué à la connexion ET aligné dans `ibkr_scheduler.py` (anti-blocage, CLAUDE.md) |
| Registre IA | `FORBIDDEN_TOOLS` bloque TOUS les verbes d'ordre (`place/modify/cancel/submit/transmit_order`, `exercise_option`, `transfer_cash`, `auto_execute`…) |
| Config produit | `READONLY = True` dans `vertex/app/config.py` |

Aucun verbe d'ordre actif nulle part dans vertex/ (grep : seules les
listes d'interdiction et les docstrings « ne passe JAMAIS d'ordre »).

## 2. Routes servant les données du compte — refus honnêtes prouvés

Sous `NO_IBKR=1` (serveur démo) :

- `GET /api/ibkr/positions` → `{"ok":false, "positions":[], "err":"IBKR
  non connecté (mode cloud/démo) — ouvre TWS ou Gateway puis réessaie."}`
  en 200 (choix documenté dans le code : broker hors ligne = état
  attendu, pas une panne serveur) — jamais de position inventée ;
- `POST /api/pos-quotes` → `{"results":{}, "live":false, "ts":…}` —
  drapeau de fraîcheur/source (`live`, `ts`) TOUJOURS porté ; le handler
  documente « ⛔ Lecture seule : cote les contrats, ne passe JAMAIS
  d'ordre » ; cache borné avec purge (anti-fuite mémoire).

## 3. État dégradé dans l'UI — honnêteté exemplaire

Navigateur sans IBKR : Portefeuille affiche « P&L latent indisponible
(marques IBKR hors ligne — **aucun chiffre inventé**) », valeurs `n/d` ;
le briefing affiche « 2 position(s) · marques indisponibles ».
0 erreur console.

## 4. Gardiens dédiés

`tests/test_no_orders.py`, `tests/test_ibkr_honesty.py`,
`tests/test_order_ticket.py` : **34 tests verts** (sélection
`-k "readonly or no_orders or ibkr"`). (Note honnête : la docstring du
gateway cite un « test_readonly_gateway.py » qui s'appelle en réalité
`test_ibkr_honesty.py` — divergence purement documentaire, notée.)

## 5. Verdict du volet : SAIN — aucun correctif requis

L'âme du produit (READONLY absolu) est verrouillée à QUATRE niveaux
indépendants (gateway en dur, registre IA, config, gardiens de tests) et
l'honnêteté des données du compte est prouvée bout en bout (route → UI).

## 6. Preuves

```text
python -m pytest tests/ -k "readonly or no_orders or ibkr" → 34 passed
Baseline suite : 1692 passed / 2 skipped (lot documentaire)
Moteur 0.9.0 · SW v122 (pas de bump) · main intacte
```

## 7. Suite

Lot 69 : cohérence fiche ↔ opportunités (mêmes scores/verdicts pour le
même symbole). Puis 70 (états dégradés globaux), bilan consolidé n°5.

**Arrêt après ce lot — boucle continue ré-armée (~2 min).**
