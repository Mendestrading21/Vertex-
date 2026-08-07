# SKYLER LOT 219 — Audit des états vides honnêtes en démo (constat navigateur, 8 pages)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-219` (base : lot 218 fusionné)

## Objet

Piste jamais réalisée jusqu'ici : vérifier EN NAVIGATEUR (DOM rendu
après hydratation JS, pas seulement le HTML servi) l'invariant n° 4 de
CLAUDE.md — « jamais de chiffre inventé affiché comme réel ; donnée
absente → —/n/d honnête ; le mot démo ne s'affiche que si le serveur le
confirme ».

## Protocole

Serveur `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1` (healthz OK,
`data_source: demo`) ; Playwright Chromium (1440×900,
domcontentloaded + 4500 ms d'hydratation) sur les **8 espaces** :
`/`, `/markets`, `/opportunities`, `/portfolio`, `/journal`,
`/options`, `/system`, `/tracking`. Pour chaque page, sur
`document.body.innerText` :

- recherche des marqueurs de MALHONNÊTETÉ technique affichés à
  l'utilisateur : `NaN`, `undefined`, `null`, `Infinity` ;
- comptage des états honnêtes (`—`, `n/d`) ;
- présence de l'étiquette démo (le serveur la confirme :
  `data_source: demo`) ;
- erreurs console.

## Résultat — invariant TENU sur les 8 pages, 0 défaut

| Page | Marqueurs malhonnêtes | États honnêtes (—/n/d) | Étiquette démo | Erreurs console |
|---|---|---:|---|---:|
| / | aucun | 17 | ✔ | 0 |
| /markets | aucun | 8 | ✔ | 0 |
| /opportunities | aucun | 21 | ✔ | 0 |
| /portfolio | aucun | 9 | ✔ | 0 |
| /journal | aucun | 15 | ✔ | 0 |
| /options | aucun | 11 | ✔ | 0 |
| /system | aucun | 17 | ✔ | 0 |
| /tracking | aucun | 1 | ✔ | 0 |

Complément : `/api/client-log` → `{"count": 0, "errors": []}` après le
balayage complet.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.
(Un gardien pytest n'est pas pertinent ici : les marqueurs
apparaîtraient APRÈS hydratation JS, hors de portée du test_client ;
c'est précisément pourquoi ce balayage navigateur avait sa place.)

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : constat pur.

## Preuves

- Balayage JSON complet dans le corps du rapport (8 pages × 5 mesures).
- Suite complète : **2482 passed / 2 skipped** (référence maintenue).

## Suite

LOT 220 : MINI-BILAN 216-220. Purge terminal.py toujours EN ATTENTE
d'accord humain explicite.
