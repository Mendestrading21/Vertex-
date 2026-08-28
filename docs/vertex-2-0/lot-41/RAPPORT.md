# Lot 41 — Banc de charge de la file IBKR (RAPPORT)

Date : 2026-08-28 · Première des deux dettes dites au rapport du lot 40.

## Objet

Le lot 40 a testé la mécanique de la file À FROID. Ce lot la met SOUS
CONTENTION avec un worker simulé (mêmes appels `prochain`/`terminer` que
terminal.py, durée de job contrôlée à 20 ms) et prouve les promesses en
situation de charge. Les asserts portent sur des ordres et des comptes,
jamais sur des durées serrées — le banc est stable (6 exécutions
consécutives vertes, 0,5 s chacune).

## Bancs (`tests/test_charge_file_ibkr_lot41.py`)

1. **Saturée de 15 lots de fond, la cotation sort en position ≤ 2** — au
   plus derrière le job déjà en cours, jamais derrière la file.
2. **Sous charge mixte (fund/scan/chain/meta/posq), l'ordre de service
   suit strictement les priorités** dès le 2e job servi.
3. **Tempête de 25 demandes identiques → UN appel courtier**, les 25
   demandeurs reçoivent le même résultat.
4. **Un backlog de 10 demandes abandonnées ne coûte RIEN au worker** —
   journal d'exécution : uniquement le demandeur vivant.
5. **Latence posq bornée par ~2 durées de job** sous un backlog de 30
   lots de fond (assert < 300 ms, marge large pour machine chargée).

## Mesure (machine de dev, 5 runs file / 3 runs FIFO)

Backlog de 30 lots de fond à 20 ms/job, puis une cotation posq :

| | médiane | min | max |
|---|---|---|---|
| File lot 40 | **36 ms** | 36 | 37 |
| FIFO nue (référence) | **625 ms** | 625 | 625 |

**17× plus rapide** pour la requête que l'utilisateur regarde — et l'écart
croît linéairement avec le backlog (la FIFO paie TOUTE la file, la file à
priorités paie au plus un job en cours).

## Preuves

Suite complète : **4420 passés · 173 ignorés · 0 échec**.

## Dette résiduelle (dite)

Snapshots atomiques complets de l'état scan — dernière moitié du lot 6
historique, chantier suivant.
