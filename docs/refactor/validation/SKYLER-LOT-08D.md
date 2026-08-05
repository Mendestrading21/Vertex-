# SKYLER V2 — LOT 08d — NEON GLASS · PORTEFEUILLE (Discipline V2)

> Date : 2026-08-05
> Branche : `agent/skyler-v2-lot-08d-portfolio-discipline`
> Base : `agent/skyler-v2-lot-09-calibration`
> Périmètre : UNE vue (Portefeuille → Risque), une carte + un endpoint — aucun moteur modifié

## 1. Constat

Le PortfolioContext (lot 7 : poids, HHI, bornes 8-15, plafond par titre,
provenance) n'était visible que via `/api/skyler/<sym>` — aucun endpoint dédié,
aucune surface UI.

## 2. Décision

- Endpoint additif `GET /api/portfolio/context` (positions_api) : positions
  canoniques du desk (`repository.load_positions`) + cotes réelles du scan →
  `portfolio_context.build` + fraîcheur.
- Carte « **Discipline du portefeuille (Constitution V2)** » dans la vue Risque
  (son domicile : risque & concentration), idempotente (même motif que
  Stress-scénarios) : Lignes vs bornes 8-15 (badge dans/sous/au-dessus),
  plus gros titre + poids vs plafond 15 % (rouge si dépassé), HHI, valeur
  suivie + provenance, note de valorisation au coût si cote absente ;
  état vide honnête si aucune position déclarée.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/app/routes/positions_api.py` | +1 route additive | faible |
| `vertex/ui/pages/portfolio_page.py` | `renderDiscipline()` dans la vue risk (additif) | faible |
| `vertex/app/routes/system.py` | SW v90 → **v91** | faible |
| 4 gardiens SW + 3 tests (route pleine/vide + gardien de page) | v91 | nul |

## 4. Tests

```text
tests/test_portfolio_intelligence_lot7.py → 20 passed (route desk réel, vide honnête, page)
suite : 1282 passed, 2 skipped · compileall exit 0
```

## 5. Validation navigateur (DEMO=1 NO_IBKR=1, Chromium réel)

1440×900 et 390×844 : carte rendue avec les **positions réelles du desk
serveur** (source canonique — pas le localStorage local) : « Lignes 2 · sous la
cible », « Plus gros titre ACN 100,0 % · > plafond 15 % » (dépassement affiché
en rouge), HHI 1,000 — chiffres réels, aucune invention. **0 erreur console,
0 débordement** ; `/api/client-log` = 0 ; SW v91.

## 6. Invariants vérifiés

- [x] source canonique = desk serveur (jamais le localStorage seul) ;
- [x] dépassement de plafond AFFICHÉ, jamais adouci ; vide honnête sans positions ;
- [x] carte idempotente (re-boots) ; bump SW + gardiens ; READONLY.

## 7. Verdict

**GO** — suite 1282 verte, carte prouvée sur données desk réelles, 2 tailles, 0 erreur.

## 8. Prochaine étape

Lot 8e : Journal/Performance — carte « Calibration Skyler » (journal du lot 9).

**Arrêt de lot — validation humaine groupée (accord utilisateur).**
