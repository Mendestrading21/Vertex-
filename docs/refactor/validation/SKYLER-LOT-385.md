# SKYLER LOT 385 — Le recensement des replis s'arrêtait à `vertex/`

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-385` (base : lot 384 fusionné,
2040ad3)

## Piste

La veine « auditer les gardiens par mutation » est fermée au lot 384. Ce lot
part d'ailleurs : de la liste des pistes fines, **les 38 `except: pass`
« autres »** du lot 379. En allant les compter, je suis tombé sur la frontière
avant de tomber sur les handlers.

## La mesure qui a tout décidé

Le lot 378 a gelé le recensement des replis numériques — *« un `except` qui
renvoie un nombre substitue une valeur plausible à une donnée manquante :
l'utilisateur ne peut pas distinguer la mesure du repli »*. C'est le filet de
l'invariant n°4, et sa propriété centrale porte un `RACINE = 'vertex'` en dur.

```text
handlers `except` dans vertex/     254   ← périmètre du recensement 378
handlers `except` hors vertex/     113   ← jamais comptés
    dont terminal.py               101
         verifier_vertex.py          9   ← script d'audit, non importé
         ib_reader.py                2
         test_connection.py          1   ← script de diagnostic, non importé
```

**31 % des handlers de production étaient hors du filet**, dont la totalité du
monolithe qui sert encore des routes.

## Le trou, prouvé — et distingué d'un gardien inutile

Un `except: return 50` **neuf** dans `terminal.py`, exactement ce que la
propriété du lot 378 interdit :

```text
repli numérique NEUF dans terminal.py (50)      AUCUN   2793 passed
[témoin] même forme mais repli None             AUCUN   2793 passed   ← correct
```

Le témoin seul ne suffisait pas : deux « AUCUN » côte à côte pourraient
signifier que le gardien ne sert à rien. **Contrôle décisif** — le même défaut,
mot pour mot, dans le périmètre déclaré :

```text
même repli 50 dans vertex/engines/stats.py      MORD    1 failed, 8 passed
```

Le gardien 378 fait donc précisément ce que son code dit. **Ce n'est pas une
myopie du détecteur, c'est sa frontière** — la catégorie exacte du trou trouvé
au lot 381 (le repli servi de `deskKeys()` que rien ne gardait).

## Les trois replis existants de `terminal.py` : honnêtes, et pourquoi

Aucun n'est une faute. Mais la raison compte plus que le verdict, et elle n'est
pas la même pour les trois.

**`_seed_fund_from_company` (L162) → `0`.** Compteur de titres enrichis ; `0`
signifie exactement « aucun enrichi ». Même famille que `track_record` au
recensement 378 : le nombre **est** la mesure, pas un substitut.

**`_i` (L203) → `0` et `_f` (L210) → `0.0`.** Coercitions numériques. Leur `0`
**est** un substitut à une donnée absente — c'est la forme dangereuse, vérifiée
sur valeurs réelles (`_i(None) = _i('abc') = _i(NaN) = 0`). Ce qui les rend
inoffensives n'est pas la fonction : **c'est le site d'appel.** Les trois seuls
appels du dépôt sont dans la chaîne d'options, où le `0` est immédiatement
écarté :

```python
iv = _f(row.get('impliedVolatility')); oi = _i(row.get('openInterest'))
if iv <= 0 or oi <= 0:
    continue                      # ← le repli ne devient jamais une mesure
```

**C'est ce garde-fou qui tient l'invariant, pas la coercition.** S'il
disparaissait, un `0` de repli entrerait dans la médiane d'IV ATM et dans le GEX
**servis**. C'est la seule pièce fragile des trois, et le gardien la verrouille
explicitement — ainsi que le fait que les coercitions n'aient pas essaimé
ailleurs, car toute la démonstration repose là-dessus.

## Gardien

`tests/test_replis_racine_lot385.py` (13 tests) :

- **le dénominateur d'abord** — le détecteur doit voir ≥ 80 handlers dans
  `terminal.py` (101 mesurés) et retrouver les 3 replis connus ; sans cela une
  propriété au vert ne prouverait rien (leçon des lots 375-377) ;
- **LA propriété**, portée à la frontière que le 378 n'a jamais franchie :
  aucun repli numérique non recensé hors `vertex/` ;
- **anti-péremption** du recensement (une entrée qui ne correspond plus à rien
  doit être retirée) ;
- **borne de dérive des `except: pass` fixée À la mesure** (38), pas au-dessus :
  *une borne qui absorbe la première régression n'est pas une borne* ;
- **anti-rot du périmètre lui-même** : un nouveau module racine porteur de
  handlers tomberait aujourd'hui dans l'angle mort des DEUX recensements — le
  test force la décision (`RACINES` ou `HORS_PRODUCTION`, avec justification) ;
- les **exclusions restent vraies** : si un script exclu devenait importé par la
  production, ses replis deviendraient servables et l'exclusion silencieusement
  fausse ;
- la caractérisation **sur valeurs réelles**, et le garde-fou du site d'appel.

### Preuve ROUGE

```text
repli numérique NEUF (50) dans terminal.py            ROUGE OK  | restauration identique
garde-fou du site d'appel affaibli (le 0 passe)       ROUGE OK  | restauration identique
coercitions appelées sur de nouveaux sites            ROUGE OK  | restauration identique
après restauration : 13 passed
```

Les trois mutations visent le **vrai fichier de production**, jamais mon propre
test — la faute du lot 383, qui ne se reproduira pas.

## Un risque de test évité

Ma première version appelait `_seed_fund_from_company()` pour vérifier son
retour. Mesure faite : ici aucune écriture (`mtime` de `fund_cache.json`
inchangé), **parce que le cache est déjà plein sur cette machine**. Sur un cache
incomplet, la fonction aurait sauvegardé un fichier runtime depuis un test. Le
risque est neutralisé (`_save_json` interceptée, et le test échoue si une
écriture est tentée) plutôt que constaté puis oublié.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- `integration/vertex-skyler-v2` à jour (tête = lot 384, 2040ad3) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Aucun fichier runtime muté (`fund_cache.json` inchangé, vérifié par `mtime`).
- Suite : **2793 → 2806 passed / 2 skipped** (+13). SW : `td-shell-v187`.

## Portée — ce que ce lot ne prétend pas

Il **étend le recensement**, il ne juge pas les 38 `except: pass` de
`terminal.py` un par un — le lot 379 l'a fait pour les 46 de `vertex/`, et cette
lecture reste à faire. Il ne dit pas non plus que la population actuelle est
bonne : une borne rend la **dérive** visible, rien de plus. Enfin, `_i`/`_f` sont
déclarées honnêtes **par leur site d'appel**, pas dans l'absolu — c'est
exactement pourquoi ce site est verrouillé.

## Suite

Le trou de frontière refermé, la piste voisine devient lisible : **les 38
`except: pass` de `terminal.py`, lus un par un** comme le lot 379 l'a fait pour
`vertex/` — c'est la seule des pistes fines qui porte encore une question
d'honnêteté non tranchée. Les autres restent minces : refus construits en
variable (377), formes imbriquées des promesses de retour (375), trois sites de
concaténation à constantes (374).

Les quinze dossiers en attente de décision humaine n'ont pas bougé. Prochaine
échéance périodique : **~lot 390**.
