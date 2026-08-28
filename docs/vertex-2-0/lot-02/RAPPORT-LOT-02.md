# Rapport — Lot 2 · Frontière IBKR market-data-only

## Ce que le lot a fermé

`readonly=True` empêche l'ordre ; il ne protège pas la confidentialité du
compte. Ce lot ferme cette seconde frontière : **plus un seul appel** de
compte, de positions, de portefeuille ou de P&L courtier dans `terminal.py`,
`vertex/` et `tools/` — vérifié par l'AST, pas par grep.

```
python .claude/skills/vertex-2-0/scripts/check_ibkr_boundary.py --enforce
    OK: aucun appel IBKR sensible détecté        (13 → 0)
```

Le gardien `tests/test_frontiere_ibkr_lot02.py` exécute ce scanner en
`--enforce` : écrit **avant** la migration (rouge, 13 appels), vert depuis.
Toute réintroduction — « juste en lecture seule » comprise — le remet au rouge.

## Capacités retirées, une par une

| Capacité | Où elle vivait | Ce qui la remplace |
|---|---|---|
| Carte « COMPTE IBKR » (valeur nette, cash, pouvoir d'achat, P&L latent, liste des positions) | legacy V3, `renderIbkrDash` | carte « IBKR — données de marché » : preuve de socket + phrase disant où vit le portefeuille |
| `/ibkr` → champs de compte | `_ibkr_worker`/`_ibkr_snapshot` | `{connected, mode, error}` seulement |
| Worker `kind='positions'` | `terminal.py` | retiré — le worker ne sert plus que du marché |
| `/api/ibkr/positions` (import desk) | `desk.py` | **404** ; les positions déjà importées restent lisibles — on retire la capacité, pas les données acceptées |
| `/api/positions/pnl-reconciliation` (4 sources de P&L) | `positions_api.py` + `ibkr_compte.py` | **404** ; le P&L reste calculé sur les positions déclarées, cotées par symbole |
| `ibkr_compte.py`, `ibkr_positions.py` | `data_sources/` | **supprimés** |
| `from_ibkr_positions` (snapshot REAL depuis le compte) | `portfolio/models.py` | retiré — REAL = positions déclarées |
| Capture des positions dans les fixtures de rejeu | `ibkr_replay.py` | `positions_brutes` reste vide |
| Réconciliation broker de l'outil G5 | `mesurer_g5_live.py` | `{'mesure': 'RETIREE', 'raison': …}` — l'outil le DIT au lieu de rendre un accord vide |

## Découverte en chemin

L'hôte UI de la carte de rapprochement (`pf-pnl-recon`) **n'existait dans
aucune vue** : `renderPnlRecon` sortait en silence dès sa première ligne.
La route interrogeait donc le compte (~55 s mesurées) pour une carte qui ne
se peignait jamais. On a retiré une capacité déjà morte à l'écran.

## Tests

- 8 fichiers de bancs épinglaient l'ancienne capacité — **réécrits, jamais
  écartés** : chacun garde désormais la vérité inverse (module supprimé,
  route en 404, snapshot sans champ de compte, outil qui avoue) et documente
  pourquoi l'ancienne intention est tombée ;
- la garde « une quantité ne se devine jamais » survit là où elle a un objet :
  le dépôt du desk ;
- suite complète : voir preuve ci-dessous.

## Préservé

- positions déclarées, thèses, enveloppes, `desk_data.json` : intouchés ;
- positions historiques `source: IBKR` déjà acceptées : toujours lisibles ;
- **tout le flux marché IBKR** : cotations (`/api/pos-quotes`), chaînes,
  historiques, Greeks de marché, états de connexion.

## Runtime vérifié

```
GET /ibkr                                  {connected, mode, error} seulement
GET /api/positions/pnl-reconciliation      404
GET /api/ibkr/positions                    404
GET /api/positions/state                   200 — desk seul, aucun champ compte
captures /portfolio et /system             1600/1024/390 · 0 erreur console
```

## Limites

- Aucun poste TWS ici : le comportement **connecté** (preuve de socket à vrai)
  n'est pas observable — la forme de la réponse l'est, et elle est gardée.
- Les paramètres `ibkr_positions` de `repository/recalculator/detector`
  subsistent (toujours `None`) : leur retrait de signature est l'étape
  « retirer » de la convergence, après parité — pas ce lot.

## Rollback

`git revert` du commit : aucune migration de données, la capacité revient
entière (et le gardien repasse au rouge, ce qui est voulu).
