# ADR — Aucune infrastructure distribuée nouvelle (lot 8)

## Décision

Vertex reste **Flask + threads + fichiers locaux**. Ni Redis, ni PostgreSQL,
ni Celery, ni Kafka, ni Temporal, ni React, ni plateforme financière
intégrée.

## Justification par la mesure, pas par principe

| Candidat | Manque qu'il résoudrait | Mesure actuelle | Verdict |
|---|---|---|---|
| Redis (cache partagé) | caches multi-processus | **1 processus** ; caches en mémoire + TTL suffisent ; `/scan` gzip ~10× | non justifié |
| PostgreSQL | volume/concurrence d'écriture | desk = blob JSON **< 2 Mo**, 1 écrivain, backups quotidiens + fusion anti-perte (lot 362) | non justifié |
| Celery/Kafka | files de jobs distribuées | 11 jobs implémentés, cadence min 45 s, **un seul worker broker par contrainte ib_async** — une file distribuée ne lèverait PAS cette contrainte | non justifié |
| Temporal | orchestration durable | jobs idempotents simples ; registre honnête (`SILENCIEUX`, échecs consécutifs) | non justifié |
| React | interactivité | 12 pages servies en ~2 ms, JS première partie sous budget gardé par test | non justifié |

## Seuils qui rouvriraient la question

- plus d'un processus serveur nécessaire (alors : cache partagé) ;
- desk > 10 Mo ou multi-utilisateurs (alors : vraie base) ;
- un besoin mesuré de parallélisme broker que ib_async autoriserait.

Chaque franchissement exige : manque reproduit, seuil mesuré, ADR, test de
panne, licence, plan de migration ET de retrait — règle du skill.

## Ce qui est renforcé À LA PLACE (fait dans ces lots)

stale-while-revalidate (lot 6) · état `SILENCIEUX` + compteur d'échecs
(lot 7) · p50/p95/**p99** sans PII (lot 8) · healthz/readyz honnêtes ·
budgets CSS/JS gardés par tests · gzip.
