# SKYLER V2 — EXECUTION STATUS

> Branche d’intégration : `integration/vertex-skyler-v2`  
> Base historique : `agent/vertex-neon-glass-graphs`  
> Statut : **Skyler V2 Core livré — phase Institutional+ ouverte**.

## Source de vérité

Skill : `.claude/skills/vertex-skyler-v2/SKILL.md`

Références avancées ajoutées :

- `references/DECISION_ENGINE.md`
- `references/ADVERSARIAL_COMMITTEE.md`
- `references/DECISION_PACKET_SCHEMA.md`
- `references/SCENARIO_CALIBRATION.md`
- `references/ANOMALY_INTELLIGENCE.md`

## Phase Core — historique validé

| Étape | Statut | Preuve principale |
|---|---|---|
| Audit convergence | ✅ GO | `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md` |
| Lot 0 — Baseline | ✅ GO | `docs/skyler/BASELINE.md` |
| Lot 1 — Correctness options | ✅ GO | `docs/refactor/validation/SKYLER-LOT-01.md` |
| Lot 2 — Constitution V2 | ✅ GO | `docs/refactor/validation/SKYLER-LOT-02.md` |
| Lot 3 — Market Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-03.md` |
| Lot 4 — News/catalyseurs/anomalies | ✅ GO | `docs/refactor/validation/SKYLER-LOT-04.md` |
| Lot 5 — Skyler Core | ✅ GO | `docs/refactor/validation/SKYLER-LOT-05.md` |
| Lot 6 — Options Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-06.md` |
| Lot 7 — Portfolio Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-07.md` |
| Lot 8 — Neon Glass | ✅ GO | `docs/refactor/validation/SKYLER-LOT-08A.md` à `08E.md` |
| Lot 9 — Calibration infrastructure | ✅ GO infrastructure | `docs/refactor/validation/SKYLER-LOT-09.md` |

État observé avant l’expansion : environ 1 300 tests verts, service worker v94, IBKR READONLY intact, `main` non modifiée.

## Phase Institutional+ — nouvelle expansion

### Gouvernance installée

- [x] moteur de décision institutionnel documenté ;
- [x] comité contradictoire de 12 rôles documenté ;
- [x] Président Skyler unique producteur du verdict final ;
- [x] avocat du diable obligatoire ;
- [x] red-team obligatoire pour S/S+ ;
- [x] schéma canonique `SkylerPacket` défini ;
- [x] scénarios/probabilités/calibration renforcés ;
- [x] intelligence des anomalies renforcée ;
- [x] agents spécialisés installés ;
- [x] runbook et checklist étendus.

### Lots Institutional+

| Étape | Statut | Objectif | Rapport attendu |
|---|---|---|---|
| Lot 10 — Mémoire et discipline décisionnelle | ✅ FAIT — validé (« go sans validation humaine ») et fusionné | décisions immuables, classification des erreurs, biais récurrents, amélioration humaine contrôlée | `docs/refactor/validation/SKYLER-LOT-10.md` |
| Lot 11 — Knowledge Graph institutionnel | ✅ FAIT — en attente de validation | relations sociétés/secteurs/catalyseurs/portefeuille prouvables, propagation explicable, questions de recherche | `docs/refactor/validation/SKYLER-LOT-11.md` |
| Lot 12 — Red-team et RC finale | ✅ FAIT — GO AVEC RÉSERVES (validation physique restante) | stress adversarial, audit math/données/sécurité, release candidate | `docs/refactor/validation/SKYLER-LOT-12.md` |

## Agents Institutional+

- `.claude/agents/skyler-chair.md`
- `.claude/agents/skyler-devils-advocate.md`
- `.claude/agents/skyler-market-regime.md`
- `.claude/agents/skyler-options-risk.md`
- `.claude/agents/skyler-data-auditor.md`
- `.claude/agents/skyler-portfolio-risk.md`

Aucun sous-agent ne peut publier `final_decision`. Le Président Skyler est l’unique source canonique.

## Décisions établies

- `main` ne bouge pas sans accord explicite.
- Neon Glass/Skyler reste la base fonctionnelle.
- Une invocation Claude = une mission ou un lot.
- Aucun lot Institutional+ ne commence sans validation du précédent.
- Les calculs et décisions canoniques restent déterministes.
- Claude rédige mais ne crée ni ne modifie les chiffres.
- IBKR reste strictement READONLY.
- Aucune note S/S+ sans red-team indépendante.
- Aucune recalibration ou modification de Constitution automatique.

## Lot 10 — livré (2026-08-05)

- moteur `vertex/engines/decision_memory.py` : ledger immuable par version de
  moteur (gel de 31 champs), anti-look-ahead par empreinte de série, résultats
  aux horizons déclarés (5/20/60 séances, catalyseur estimé étiqueté, thèse et
  option honnêtement NON_APPLICABLE), taxonomie d'erreurs déterministe,
  10 biais surveillés, recommandations `EN_ATTENTE_VALIDATION_HUMAINE` ;
- routes : gel fail-safe dans `/api/skyler/<sym>` + `GET /api/skyler/memory` ;
- persistance runtime `skyler_memory.json` (gitignorée, bornée) ;
- 1332 tests verts / 2 skipped (+32) ; SW inchangé v94 (aucune UI touchée) ;
- interdictions respectées : pas de Knowledge Graph, pas d'UI, pas de
  modification automatique des poids/Constitution, `main` intacte, aucun ordre.

## Lot 11 — livré (2026-08-05)

- moteur `vertex/engines/knowledge_graph.py` : 4 relations prouvables
  (secteur F1 sourcé, co-mouvement F2 fenêtré, catalyseur daté F1, détention
  desk F1), provenance obligatoire par arête, propagation explicable saut par
  saut, dépendances cachées ≥ 2 liens indépendants, questions de recherche
  `NON_DOCUMENTE` — fournisseurs/clients/concurrents JAMAIS inventés ;
- routes lecture seule : `GET /api/skyler/graph` + `GET /api/skyler/graph/<sym>` ;
- 1350 tests verts / 2 skipped (+18) ; SW inchangé v94 (aucune UI touchée).

## Lot 12 — livré (2026-08-05)

- règle red-team du comité appliquée par le moteur : S/S+ sans red-team
  complétée = plafonné à A — `ENGINE_VERSION` 0.1.0 → **0.2.0** (règle changée
  = version changée), historique 0.1.0 séparé en mémoire, Constitution
  intouchée (proposition de gate profil V3 documentée, en attente humaine) ;
- trouvaille adversariale corrigée : NaN/infini refusés par la mémoire ;
- batterie adversariale : séries hostiles, prix extrêmes, attaque look-ahead,
  déterminisme, labels hostiles, verbes d'ordre, fichiers runtime/secrets,
  performance bornée — 17 tests ;
- 1367 tests verts / 2 skipped (+17) ; SW v94 inchangé.

## Lot 13 — livré (2026-08-05, travail continu autorisé)

- moteur **0.3.0** : `operational_state` déterministe (8 états DECISION_ENGINE
  §2.2, base explicite, jamais une décision finale) + `confidence` factorisée
  §7 (4 facteurs bornés avec base, plafonds UNKNOWN ≤ 0,55 / conflit ≤ 0,50 /
  contradiction ≤ 0,60, calibration figée à 0,50 sans historique — jamais
  100 %) ;
- le ledger mémoire fige désormais ces champs (31/31 champs vivants) ;
- 1386 tests verts / 2 skipped (+19).

## Programme Institutional+ — TERMINÉ (RC sur intégration)

Les 12 lots + audit sont livrés sur `integration/vertex-skyler-v2`.
Verdict RC : **GO AVEC RÉSERVES** — voir `SKYLER-LOT-12.md` §11.

## Prochaine action unique

Validation humaine de la RC sur appareil physique (TWS réel, pages, iPhone).
Ensuite, avec accord explicite UNIQUEMENT, merge `integration/vertex-skyler-v2`
→ `main`.

**Arrêt — validation humaine requise.**
