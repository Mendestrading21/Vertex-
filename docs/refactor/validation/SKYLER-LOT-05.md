# SKYLER V2 — LOT 05 — SKYLER CORE

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-05-skyler-core`
> Base : `agent/skyler-v2-lot-04-events-ohlcv`
> Périmètre : nouveau moteur pur + 1 route additive — aucun moteur existant modifié

## 1. Constat

Les briques existaient (decision_stack = vérité des verdicts, market_context,
events, anomaly, Constitution V2 avec score/40, niveaux et hard_gates codifiés)
mais rien ne les assemblait : pas de SkylerPacket, pas de score par blocs, pas
d'évaluation des hard gates, pas de scénarios structurés, pas d'audit trail.

## 2. Décision

`vertex/engines/skyler_core.py` — 5 fonctions PURES, déterministes :

- **`build_packet`** : agrège les contextes DÉJÀ calculés (technique du scan,
  MarketContext, timeline, anomalies) sans recalcul ni mutation ; contextes non
  branchés (fondamentaux, options, portefeuille) = `available: false` + raison —
  jamais remplis ; `schema_version/engine_version/profile_version` ;
  `freshness_floor` ; **détecteur de contradictions** (verdict haussier vs régime
  bloquant, vs extrême bas de fenêtre, conflits de sources) ; **audit trail**.
- **`score40`** : blocs lus dans la Constitution V2 (jamais codés en dur) ;
  chaque point porte sa justification (`basis`) ; bloc non branché = 0 +
  INSUFFICIENT listé ; catalyseurs plafonnés PARTIAL 2/5 (interdiction de noter
  une simple date de résultats) ; anomalies seules plafonnées 1/4 (flux
  institutionnels non branchés) ; niveau S+/S/A/B/REFUS depuis les seuils V2,
  **S+/S impossibles si un bloc manque** (constitution).
- **`hard_gates`** : portes de la V2 — évaluables (RR_BELOW_2 sur le R:R
  structurel réel, NO_INVALIDATION sur le stop moteur, DATA_QUALITY_CRITICAL,
  SOURCES_CONFLICT, THESIS_BROKEN) déclenchées ou non ; **non évaluables =
  `triggered: null`** (« jamais supposée fermée »), jamais False silencieux.
- **`scenarios`** : pessimiste/probable/exceptionnel depuis les NIVEAUX RÉELS du
  plan moteur (stop/TP2/TP3, rendements exacts) ; **`probability: null` assumé**
  (« modèle non calibré — aucune probabilité affichée », calibration = lot 9) ;
  plan absent → `available: false`, jamais inventé.
- **`decide`** : décision du VOCABULAIRE CANONIQUE (ACHETER/…/REFUSER) ; hard
  gate déclenchée → plafonnée ATTENDRE/REFUSER (`capped_by_gate`) — **le score ne
  contourne jamais une porte** ; jamais plus agressive que le verdict canonique
  existant (désaccord → plafonné + contradiction tracée) ; risque max (distance
  au stop en %), catalyseur daté le plus proche, invalidation réelle, objection
  la plus forte JAMAIS vide, inconnues, audit trail complet.

Route additive `GET /api/skyler/<sym>` : assemble détail + MarketContext +
timeline (news assainies) + anomalies (série canonique) → `{packet, decision}`.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/skyler_core.py` | nouveau (pur, ~330 l.) | faible |
| `vertex/app/routes/analysis_api.py` | +1 route additive | faible |
| `tests/test_skyler_core.py` | nouveau — 18 tests | faible |

## 4. Tests

```text
rouge : collection error (module inexistant)
vert  : python -m pytest tests/test_skyler_core.py -q → 18 passed
suite : python -m pytest tests/ -q → 1232 passed, 2 skipped · compileall exit 0
```

Couverture : versions/audit trail, non-invention (contextes absents INSUFFISANTS),
blocs = profil V2 exactement (bornés bloc par bloc, basis obligatoire), niveau V2,
gates rouges (R:R 1.2, plan absent), gates inconnues ≠ fausses, scénarios exacts
(−6 %/+18 % à la main) SANS probabilité, contradictions (régime bloquant) et
absence de fausses contradictions, décision plafonnée par gate, forme complète,
**déterminisme JSON strict**, conservatisme vs verdict canonique, route.

## 5. Validation runtime (DEMO=1 NO_IBKR=1)

`/api/skyler/GOOGL` → décision `REFUSER`, niveau REFUS_WATCH, **15/40** justifié
bloc par bloc (asymétrie 6/6 — R:R structurel réel ; technique 2/6 ; catalyseurs
2/5 PARTIAL ; fondamentaux/options 0 INSUFFISANTS ; régime 0 — UNKNOWN en démo),
0 gate déclenchée, scénarios servis avec `probability: null`, catalyseur « Emploi
US (NFP) (J-3) », invalidation 173.47 (stop réel), risque max 3.63 %, objection
explicite (blocs non branchés), audit trail 6 étapes. `/api/client-log` = 0.

## 6. Invariants vérifiés

- [x] Claude ne crée AUCUN chiffre (moteur 100 % déterministe, prouvé par test) ;
- [x] hard gates prioritaires sur le score ; non évaluable ≠ non déclenché ;
- [x] aucune probabilité sans modèle ; scénarios sur niveaux réels uniquement ;
- [x] jamais plus agressif que le verdict canonique (decision_stack respecté) ;
- [x] READONLY (note explicite dans chaque décision) ; aucun secret.

## 7. Risques restants

1. Blocs fondamentaux/options/portefeuille à 0 tant que leurs contextes ne sont
   pas branchés (lots 6-7) — le score est bas PAR CONSTRUCTION et le dit.
2. Probabilités des scénarios : calibration au lot 9 (Brier/calibration).
3. Couche Claude (rédaction du packet réduit) non branchée — le copilote actuel
   reste indépendant ; intégration à faire après lots 6-7.
4. UI : `/api/skyler/<sym>` n'est pas encore affiché (lot 8).

## 8. Verdict

**GO** — 18 tests, déterminisme prouvé, honnêteté par construction, suite 1232
verte, décision canonique servie en runtime.

## 9. Prochaine étape autorisée

`/vertex-skyler-v2 lot-6` (Options Intelligence — scanners TACTICAL/SWING/LEAPS,
OptionsContext branché dans le score).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**
