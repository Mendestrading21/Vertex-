# VERTEX FULL SYSTEM INTEGRATION — BASELINE

> Baseline honnête prise au début de la mission « Full System Integration &
> Production Readiness ». Sert de point de référence au rapport final.

## Branche & commits
- **Branche de travail** : `claude/vertex-strategy-os-h17dso` (branche désignée
  de la session). La consigne du prompt demandait `feature/vertex-full-system-integration` ;
  la directive de session impose de rester sur la branche désignée — je n'ai donc
  **pas** créé de nouvelle branche et je ne touche pas `main`.
- **Commit initial (avant cette passe)** : `d8f8275`.

## Tests initiaux
- `python -m pytest tests/ -q` → **673 passed** (avant cette passe), 0 échec.

## Endpoints d'observabilité — état initial
| Endpoint | Avant |
|---|---|
| `/healthz` | ✅ présent |
| `/readyz` | ❌ absent |
| `/api/system/status` | ❌ absent (existait `/api/system-status`) |
| `/api/system/diagnostics` | ✅ présent |
| `/api/system/connections` | ❌ absent |
| `/api/system/jobs` | ❌ absent (existait `/api/system/automations`) |
| `/api/data-quality` | ✅ présent |
| `/api/live/status` | ✅ présent |

Total routes Flask détectées : **138**.

## READONLY — état initial
- `READONLY=True` en dur (`vertex/app/config.py`) — invariant produit.
- Scan initial des chemins d'ordre (appels/définitions, hors tests) :
  **1 occurrence** — `closePosition` dans `vx-entities.js`/`portfolio_page.py`,
  qui est une **clôture déclarative localStorage** (aucun ordre), mais dont le
  NOM figurait sur la denylist.

## Connexions configurées (environnement de dev)
- IBKR : configuré via `IBKR_*` mais **aucune session TWS/Gateway** (cloud).
- TradingView : `TRADINGVIEW_WEBHOOK_SECRET` absent → webhook désactivé (503 honnête).
- Claude : `ANTHROPIC_API_KEY` absent → fallback déterministe.
- Stockage desk : lisible.
- Scheduler : 24 jobs enregistrés.
- Live Stream (SSE) : présent.

## Données
- Mode démo (`DEMO=1 NO_IBKR=1`) : univers scanné de 20 titres, board options
  synthétique clairement étiqueté DÉMO.
