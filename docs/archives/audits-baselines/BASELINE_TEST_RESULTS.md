# Baseline des tests — avant Vertex Strategy OS

Date : 2026-07-11
Branche : `claude/vertex-strategy-os-h17dso`
Commit de départ : `45ba412` (feat(secu+lancement): verrou facile (.env), exposition reseau sure, embeds repares, CLAUDE.md)
Python : 3.11.15

## Commande

```
python -m pytest tests/ -q
```

## Résultat

```
250 passed in 5.41s
```

Aucun échec, aucun skip signalé. Cette baseline sert de référence : toute phase
de la migration Vertex Strategy OS doit maintenir 100 % de réussite (les
nouveaux tests s'ajoutent, les anciens ne doivent jamais régresser sans
justification documentée).

## État initial de l'arbre

- Ancien package legacy à nom personnel (23 modules, ~3 872 lignes) —
  importé par `terminal.py`, `vertex/engines/analysis.py`,
  `vertex/app/routes/{command,analysis_api,system,content}.py`,
  `vertex/data/company.py`, `tests/test_vertex.py`.
- Occurrences de noms personnels (recherche insensible à la casse, hors
  `.git`) : 55 occurrences réparties dans 39 fichiers (code, docs, CI, tests).
- Monolithe `terminal.py` : ~1,2 Mo, HTML/JS générés en chaînes Python.
