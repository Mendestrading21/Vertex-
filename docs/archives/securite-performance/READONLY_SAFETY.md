# VERTEX — Sûreté : LECTURE SEULE, ANALYSE UNIQUEMENT

VERTEX est un **terminal d'intelligence décisionnelle**. Ce n'est pas une application
de trading. Il n'exécute **jamais** d'ordre et ne le fera **jamais**.

## Invariant produit (non négociable)

> **ANALYSIS ONLY — NO ORDER EXECUTION**

Interdits pour toujours dans ce dépôt :

- `placeOrder`, `submitOrder`, `bracketOrder`, `MarketOrder`, `LimitOrder`, `StopOrder`
- `reqGlobalCancel`, tout appel d'exécution ou d'annulation d'ordre
- trading automatique, rééquilibrage exécuté, logique d'ordre cachée
- recommandations présentées comme des certitudes, promesses de performance
- exposition de secrets / clés API

## Garde-fous structurels

| Couche | Garde-fou | Où |
|---|---|---|
| **Configuration** | `READONLY = True`, `ANALYSIS_ONLY = True` (constantes affirmées) | `vertex/app/config.py` |
| **IBKR** | Toute connexion force `readonly=True` (verrou côté courtier) | `ib_reader.py` |
| **API** | `/api/system-status` renvoie `readonly: true`, `order_execution: "disabled-by-design"` | `vertex/services/status_service.py` |
| **Tests** | `tests/test_no_orders.py` échoue si un chemin d'ordre apparaît, ou si `readonly=True` disparaît | CI bloquante |
| **CI** | Job `safety` isolé et bloquant sur chaque push / PR | `.github/workflows/ci.yml` |
| **UI** | Chaque page affiche « ANALYSE ÉDUCATIVE · AUCUN ORDRE » | templates |

## Vérification automatique

```bash
pytest tests/test_no_orders.py -q
```

Ce test :
1. scanne **tout** le code applicatif à la recherche de motifs d'exécution d'ordre → **0 autorisé** ;
2. vérifie que toute connexion IBKR utilise `readonly=True` ;
3. vérifie l'invariant de configuration `READONLY`.

Ce test tourne dans un **job CI dédié et bloquant** : aucune fusion possible s'il échoue.

## Cadrage des sorties

Toute sortie de moteur est **analytique, éducative et probabiliste**. Les scores sont
bornés [0, 100], décomposés, et l'incertitude est explicite (confiance, fraîcheur des
données). VERTEX aide à **décider**, il ne décide jamais à la place de l'utilisateur.
