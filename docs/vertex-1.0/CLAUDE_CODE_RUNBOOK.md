# Runbook Claude Code

## Commande

```text
/vertex-1-0
```

Ajouter ensuite l'objectif concret, par exemple:

```text
/vertex-1-0
Audite puis consolide la façade Options sans modifier les calculs. Pars du
dernier main, identifie tous les endpoints et consommateurs, écris les tests de
parité, implémente sur une branche agent/vertex-1-0-options-api et ouvre une PR
brouillon avec preuves et rollback.
```

## Préflight

```bash
git fetch --all --prune
git switch main
git pull --ff-only
git switch -c agent/vertex-1-0-<sujet>
python -m compileall -q terminal.py vertex
python -m pytest -q
```

Relever le SHA, les tests collectés et les limitations d'environnement.

## Analyse

- lire les contrats canoniques;
- déterminer le propriétaire actuel de chaque donnée;
- identifier routes, pages, tests, caches et fichiers utilisateurs;
- rechercher les doublons et branches historiques pertinentes;
- annoncer les suppressions/renommages proposés.

## Implémentation

- tests rouges quand le comportement change;
- migration ou adaptateur pour toute interface consommée;
- état dégradé explicite;
- aucune donnée inventée;
- aucune nouvelle logique métier dans `terminal.py`;
- aucune modification de profil sans nouvelle version.

## Validation

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

Pour l'UI/runtime: lancer en `NO_IBKR=1 DEMO=1`, vérifier les huit espaces,
`/healthz` et `/api/client-log`.

## Rapport de PR

- objectif et non-objectifs;
- architecture avant/après;
- fichiers canoniques;
- migrations et compatibilité;
- preuves;
- risques;
- rollback;
- limites non testées;
- décisions humaines.

S'arrêter à la PR brouillon; ne pas fusionner.
