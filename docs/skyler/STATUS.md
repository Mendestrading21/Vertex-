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
| Lot 10 — Mémoire et discipline décisionnelle | **À EXÉCUTER** | décisions immuables, classification des erreurs, biais récurrents, amélioration humaine contrôlée | `docs/refactor/validation/SKYLER-LOT-10.md` |
| Lot 11 — Knowledge Graph institutionnel | BLOQUÉ par Lot 10 | relations sociétés/secteurs/thèmes/catalyseurs/risques, propagation explicable | `docs/refactor/validation/SKYLER-LOT-11.md` |
| Lot 12 — Red-team et RC finale | BLOQUÉ par Lot 11 | stress adversarial, audit math/données/sécurité/UI, release candidate | `docs/refactor/validation/SKYLER-LOT-12.md` |

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

## Prochaine action unique

Exécuter uniquement :

```text
/vertex-skyler-v2 lot-10
```

Périmètre : mémoire décisionnelle, immutabilité, résultats par horizon, classification des erreurs et discipline comportementale.

Interdictions du Lot 10 :

- ne pas commencer le Knowledge Graph ;
- ne pas refaire l’UI ;
- ne pas modifier automatiquement les poids ou la Constitution ;
- ne pas fusionner dans `main` ;
- ne pas exécuter le Lot 11.

**Arrêt après le Lot 10 — validation humaine requise.**
