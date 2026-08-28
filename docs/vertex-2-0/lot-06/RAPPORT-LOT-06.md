# Rapport — Lot 6 · Gateway et snapshots (tranche : servir sans attendre)

## Le défaut, mesuré

Un seul worker IBKR (ib_async non thread-safe) sert TOUT : chaîne 75 s,
fondamentaux 90 s, scan 45 s, cotations 45 s — sérialisés. `/api/pos-quotes`
tenait un cache de 45 s ; au-delà, la requête UI **bloquait jusqu'à 45 s**
derrière la rotation des chaînes (20/33/56 s relevés dans le code), alors
qu'une cotation vieille de 46 s existait en mémoire.

## Livré — stale-while-revalidate

1. **Le périmé se sert immédiatement, étiqueté** : entre TTL et purge
   (20×TTL), la cotation part telle quelle et la réponse porte
   `stale: [clés]` — l'UI peut dire « cote conservée » au lieu de laisser un
   âge faux passer pour frais. Le rafraîchissement part en **arrière-plan**
   sur la même file.
2. **Clé jamais cotée** : l'attente reste, bornée **12 s** (au lieu de 45),
   puis le repli honnête existant (SECONDARY / mid du board) prend la main —
   le passage suivant lit le cache que le worker aura rempli.
3. L'ordre broker-avant-repli est inchangé et toujours gardé par son banc.

## Testabilité sans état global

Première version : crochets dans un global de module — **écrasé par le
premier banc venu** qui reconstruit un blueprint (échec en suite complète,
vert en isolation : la définition même de la pollution d'état). Les crochets
vivent désormais **sur le blueprint** (`bp._vx_hooks`) : chaque application
porte les siens, un banc atteint ceux de l'app réelle par
`app.blueprints['desk']._vx_hooks`.

## Preuves

- banc rouge d'abord : cache périmé + worker à 5 s → réponse < 3 s exigée
  (échouait : la route attendait), verte après ; borne 12 s prouvée par
  interception du worker ;
- suite complète : **4308 passés · 0 échec** ; le banc historique du repli
  a suivi le renommage d'ancre, son intention (broker avant repli) intacte.

## Dette d'architecture consignée — le corps du lot 6 du programme

- la **file unique** reste : un worker par domaine, coalescence des demandes
  identiques, circuit breakers et snapshots atomiques complets exigent un
  banc de charge et une session dédiée ;
- `positions_api._quotes` garde sa borne de 45 s (même file) — même
  traitement à faire ;
- les timeouts worker (75/90/45) restent des constantes locales sans budget
  global.

## Rollback

Revert du commit — le comportement bloquant revient.
