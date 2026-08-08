# SKYLER LOT 371 — La route sœur de la faille du lot 368 : saine, prouvé avec des cellules réelles

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-371` (base : lot 370 fusionné,
0167a48)

## Piste calibrée

Le lot 368 a trouvé une faille XSS sur `/memory/<decision_id>` et n'avait
**pas** couvert sa jumelle `/memory/cell/<group>/<key>` — même fichier, même
auteur, même motif de rendu. Forte probabilité du même défaut : c'est la piste
la plus rentable des trois ouvertes.

## Correction de méthode, avant tout résultat

Première sonde : records hostiles écrits avec un résultat `{'hit': bool}`.

```text
cellules formées : AUCUNE
=== segments de chemin hostiles ===
/memory/cell/by_level/%22%3E%3Cimg…   HTTP 404 · brut=non · actif=non
```

Des 404 partout, donc des « non » rassurants et **vides** — exactement le piège
du lot 368. La vraie forme d'un résultat mesuré est
`{'horizons': {'H5'|'H20'|'H60': {'status': 'MESURE', 'return_pct': …}}}`
(cf. `_measured_class`). Sans horizon au statut `MESURE`, **aucune cellule
n'existe** et la sonde ne prouve rien.

C'est la **cinquième fois** de la boucle qu'un doute sur l'outil change le
résultat.

## Mesure — sonde corrigée

```text
cellules formées : [('by_level', 'S'), ('by_decision', 'BUY'),
                    ('by_regime', '"><img src=x onerror=alert(1)>'),
                    ('by_catalyst', 'avec_catalyseur'),
                    ('by_catalyst_type', '"><img src=x onerror=alert(1)>')]

/memory/cell/by_level/S                    HTTP 200 · 19 168 octets
/memory/cell/by_decision/BUY               HTTP 200 · 19 176 octets
/memory/cell/by_regime/%22%3E%3Cimg…       HTTP 200 · 19 252 octets
/memory/cell/by_catalyst/avec_catalyseur   HTTP 200 · 19 204 octets

   charge BRUTE      : non
   balise active     : non
   version échappée  : oui
   balises <title>   : 1 / 1
```

**4 cellules rendues en 200**, dont une — `by_regime` — dont **la clé elle-même
est la charge hostile** : elle traverse alors **à la fois l'URL et la donnée**.
Aucune fuite dans aucun cas.

## Pourquoi cette route tient là où l'autre a cédé

Deux différences décisives avec `/memory/<decision_id>` :

1. son `title=` est une **constante** (`'Cellule de calibration'`) — la faille
   du lot 368 venait précisément d'un titre nourri par la donnée ;
2. chaque valeur du corps passe par `markupsafe.escape`, y compris la clé de
   cellule reconstruite (`'%s=%s' % (group, key)`, à l'intérieur du `_e(...)`).

**Verdict : saine. Rien touché.**

## Gardien

`tests/test_memoire_cellule_lot371.py` (5 tests), sur une mémoire
**temporaire** (le vrai `skyler_memory.json` n'est jamais touché) :

- **anti-vide** : la fixture doit former ≥ 4 cellules — si la forme des
  résultats change, le test le dit **avant** que les autres ne tournent à vide ;
- chaque cellule réelle échappe le contenu de la mémoire ;
- le cas le plus dur : clé hostile traversant l'URL **et** la donnée ;
- groupe/clé inconnus → 404 sans réflexion de la charge ;
- **le titre reste une constante** — s'il est un jour nourri par la donnée, le
  gardien réclame son échappement (la faute du lot 368).

### Preuve ROUGE

```text
ROUGE OK  faute du lot 368 transplantée : titre nourri par la donnée | restauration identique
          3 failed, 2 passed
ROUGE OK  un échappement retiré d'une colonne du tableau             | restauration identique
          2 failed, 3 passed
après restauration : 5 passed
VERDICT : gardien mordant sur les 2 cas
```

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 370, 0167a48) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2605 → 2610 passed / 2 skipped** — verte (+5).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Une seule route auditée, avec cinq classes de charge. La piste (a) — les
interpolations serveur dans le `content=` de **chaque page** — reste ouverte et
demande son propre lot. Les pages produit s'hydratent surtout côté client, donc
la surface serveur y est mince, mais elle n'a pas été mesurée.

## Suite

LOT 372 : veille active. Pistes ouvertes — (a) interpolations serveur dans le
`content=` des pages ; (b) promesses de docstrings en un seul mot majuscule et
docstrings de fonctions. Prochaine échéance périodique : **~lot 380**.
