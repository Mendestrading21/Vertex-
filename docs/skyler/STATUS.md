# SKYLER V2 — EXECUTION STATUS

> Branche d’intégration : `integration/vertex-skyler-v2`  
> Base : `agent/vertex-neon-glass-graphs`  
> Statut : gouvernance installée, aucun moteur modifié.

## Source de vérité

Skill : `.claude/skills/vertex-skyler-v2/SKILL.md`

Commande initiale obligatoire :

```text
/vertex-skyler-v2 audit
```

## Lots

| Étape | Statut | Validation | Rapport |
|---|---|---|---|
| Audit convergence | À FAIRE | — | `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md` |
| Lot 0 — Baseline | BLOQUÉ par audit | — | `docs/skyler/BASELINE.md` |
| Lot 1 — Correctness options | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-01.md` |
| Lot 2 — Constitution V2 | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-02.md` |
| Lot 3 — Market Intelligence | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-03.md` |
| Lot 4 — News/catalyseurs/anomalies | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-04.md` |
| Lot 5 — Skyler Core | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-05.md` |
| Lot 6 — Options Intelligence | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-06.md` |
| Lot 7 — Portfolio Intelligence | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-07.md` |
| Lot 8 — Neon Glass | BLOQUÉ | — | rapports par espace |
| Lot 9 — Calibration et RC | BLOQUÉ | — | `docs/refactor/validation/SKYLER-LOT-09.md` |

## Décisions établies

- `main` ne sera pas modifiée sans accord explicite.
- Neon Glass est la base fonctionnelle actuelle.
- Les branches V4 concurrentes ne sont pas des bases de développement.
- Une invocation Claude = un seul lot.
- Chaque lot se termine par un arrêt et une validation humaine.
- Les calculs sont déterministes ; Claude rédige mais ne crée pas les chiffres.
- IBKR reste strictement READONLY.

## Risques prioritaires à vérifier pendant l’audit

1. divergence RC1/Neon Glass ;
2. commit RC1 potentiellement absent de la branche Neon ;
3. perte théoriquement illimitée des expositions nettes vendeuses de calls ;
4. unités d’IV ambiguës aux frontières ;
5. stratégies hors mandat encore classables ;
6. profil V1 non aligné avec LEAPS delta 0,70–0,90 / DTE 180–540 ;
7. OHLCV artificiel dans certains chemins d’anomalies ;
8. moteurs plus riches que les données réellement injectées ;
9. documentation et branches concurrentes ;
10. dette de `terminal.py` et endpoints legacy.

## Prochaine action unique

Exécuter `/vertex-skyler-v2 audit` sur une branche de travail dédiée issue de `integration/vertex-skyler-v2`.

**Ne pas commencer le Lot 0 avant validation de l’audit.**
