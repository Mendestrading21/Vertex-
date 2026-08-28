# Rapport — Lot 7 · Automatisations honnêtes (tranche : le silence se voit)

## Déjà honnête, vérifié et non refait

Le registre (`vertex/scheduler/registry.py`) relie déjà chaque job à un
exécuteur réel **ou** le marque `NON_IMPLEMENTE` — 16 des 27 jobs le sont, et
l'écran Système le dit sans les accuser d'une panne. C'était l'exigence
« relier ou marquer » du programme, faite au travail G1.

## Le défaut trouvé, et corrigé

Le battement (`beat`) existait ; son **absence** n'était pas détectée. Une
boucle qui avait battu une fois puis était morte restait **`ACTIF` pour
toujours** — un vert de façade sur des alertes que personne n'évalue plus.

Deux ajouts, gardés par cinq bancs rouges d'abord :

1. **`SILENCIEUX`** — implémenté, cadencé, déjà battu avec succès, et muet
   depuis plus de **2× sa cadence**. Distinct d'`ERREUR` (le dernier passage
   a échoué — et l'échec **prime** sur le silence) et d'`ACTIF`. Les jobs
   évènementiels (`interval_s: None`) ne deviennent jamais silencieux : sans
   cadence, le silence n'y est pas une panne.
2. **`echecs_consecutifs`** — compté par `beat(ok=False)`, remis à zéro par
   un succès : le signal de tempête de retries, lisible par l'écran et par un
   futur circuit breaker, sans toucher aux boucles.

L'écran Système affiche `silencieux` en **ambre** (prudence, pas erreur : le
dernier passage avait réussi).

## Leçon d'import, payée en chemin

`vertex/scheduler/__init__.py` ré-exporte l'**objet** `registry`, qui masque
le sous-module du même nom sur `import a.b as x`. Le banc passe par
`importlib.import_module` pour atteindre le module.

## Dette consignée, pas absorbée

Idempotence, retries bornés dans les boucles elles-mêmes, reprise après
redémarrage (le registre est en mémoire : un restart remet `EN_ATTENTE`, ce
qui est honnête), arrêt propre et bancs de panne complets : le corps du
lot 7 du programme, à instruire avec la refonte de la file (lot 6 complet).

## Preuves

5 bancs rouges d'abord → verts · suite complète **4313 passés · 0 échec** ·
service worker v263.
