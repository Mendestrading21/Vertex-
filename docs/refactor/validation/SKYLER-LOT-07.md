# SKYLER V2 — LOT 07 — PORTFOLIO INTELLIGENCE

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-07-portfolio-intelligence`
> Base : `agent/skyler-v2-lot-06-options-intelligence`
> Périmètre : PortfolioContext + garde-fous Skyler — moteurs portefeuille existants (guard/replacement/risk/stress/team) inchangés

## 1. Constat

Les briques existaient (`vertex/positions/repository.load_positions` = contrat de
positions canonique avec provenance MANUAL/SIMULATED/IBKR ; `vertex/portfolio/*` :
guard, replacement_engine, risk_engine, stress_tests, team_engine ; stress
portefeuille et pré-trade livrés pré-Skyler) mais le SkylerPacket n'avait AUCUN
contexte portefeuille : les portes LOSER_REINFORCEMENT / CONCENTRATION_EXCESSIVE
restaient inconnues et aucun sizing par niveau n'existait.

## 2. Décision

- **`vertex/engines/portfolio_context.py`** (pur) : depuis les positions
  CANONIQUES (simulées exclues, provenance conservée) et les cotes du scan —
  poids par titre, **HHI**, top, bornes **8-15** du profil V2 (`in_bounds`,
  `free_slots`), valorisation au coût ÉTIQUETÉE quand la cote manque ;
  **candidat** : détenu ?, poids, P&L exact, `is_loser`,
  `reinforcement_allowed` ∈ {False (perdant — JAMAIS), 'AFTER_CONFIRMATION'
  (gagnant — jamais un oui aveugle, conditions V2 échues), None (P&L inconnu ≠
  autorisé), 'NOT_HELD'} ; **sizing S+/S/A/B** : plafonds ANALYTIQUES V2 →
  montants sur base capital (ou valeur investie, étiquetée), **impact marginal**
  (`resulting_weight_pct`) et `concentration_breach` vs plafond 15 %/titre ;
  budget de risque `available: false` sans stops déclarés (jamais estimé) ;
  corrélations honnêtement absentes.
- **Skyler branché** : `portfolio_ctx` dans le packet ; portes réelles —
  **LOSER_REINFORCEMENT** (position perdante + verdict haussier → déclenchée ;
  P&L inconnu → None ; non détenue → False), **CONCENTRATION_EXCESSIVE** (poids
  actuel ≥ plafond) ; la décision porte le **sizing** analytique quand disponible.
- Route `/api/skyler/<sym>` : positions du desk (blob `desk_data.json` via le
  dépôt canonique) + cotes du scan.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/portfolio_context.py` | nouveau (pur) | faible |
| `vertex/engines/skyler_core.py` | `portfolio_ctx` + 2 portes réelles + sizing (additif) | faible |
| `vertex/app/routes/analysis_api.py` | /api/skyler nourrit le contexte desk | faible |
| `tests/test_portfolio_intelligence_lot7.py` | nouveau — 17 tests | faible |
| `tests/test_skyler_core.py` | 1 assertion de texte de raison (porte tjs None sans portefeuille) | nul |

## 4. Tests

```text
rouge : collection error (module inexistant)
vert  : 17 passed (lot 7)
suite : 1265 passed, 2 skipped · compileall exit 0
```

Cas à la main : poids 900/2500/1000 sur 4400 $ (AAA 20,45 %, BBB 56,82 %),
HHI exact, AAA −10 % → renforcement INTERDIT, BBB +25 % → AFTER_CONFIRMATION,
P&L inconnu → None, S+ sur 10 000 $ → [1 000, 1 500] $, ajout sur BBB → brèche
de concentration (> 15 %) → porte déclenchée → décision plafonnée malgré le
score, sizing porté par la décision, route de bout en bout (desk blob réel).

## 5. Validation runtime (DEMO=1 NO_IBKR=1)

Desk démo vide → `contexts.portfolio.available: false` (« aucune position réelle
déclarée ») — comportement honnête attendu ; le chemin complet (blob desk →
positions canoniques → contexte → portes) est prouvé par le test de route avec
un blob réel. `/api/client-log` = 0. Aucune UI modifiée (lot 8) → pas de bump SW.

## 6. Invariants vérifiés

- [x] jamais renforcer un perdant (porte + contexte, prouvé) ; gagnant = preuve exigée ;
- [x] allocations = plafonds analytiques V2, `never_triggers_orders` ;
- [x] inconnu ≠ autorisé (P&L absent → None) ; valorisation au coût étiquetée ;
- [x] budget de risque jamais estimé sans stops ; simulées exclues ; provenance conservée ;
- [x] READONLY ; moteurs portefeuille existants intacts.

## 7. Risques restants

1. Corrélations/facteurs non branchés (honnêtement absents) — source à venir.
2. Quota options (OPTIONS_QUOTA_EXCEEDED) reste None : le contexte ne compte pas
   encore les positions OPTIONS du desk — extension naturelle du contexte.
3. Le stress après ajout vit dans `/api/portfolio/stress` (pré-Skyler) — fusion
   dans le packet au lot 8/9.

## 8. Verdict

**GO** — 17 tests (calculs exacts à la main), garde-fous branchés et prouvés
prioritaires sur le score, suite 1265 verte.

## 9. Prochaine étape autorisée

`/vertex-skyler-v2 lot-8` (Expérience Neon Glass — exposer Skyler page par page).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**
