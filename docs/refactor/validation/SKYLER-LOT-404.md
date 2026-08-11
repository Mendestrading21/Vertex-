# SKYLER LOT 404 — Les assertions avalées par un `except` : zéro, et le zéro est substantiel

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-404` (base : lot 403 fusionné,
ddb821a)

Le lot 403 a cherché les tests qui **n'affirment rien**. Celui-ci cherche le
symétrique exact : des tests qui **affirment, mais dont l'affirmation ne peut pas
les faire tomber** parce qu'un `except` l'attrape.

```python
try:
    assert quelque_chose        # ← ne fera JAMAIS échouer le test
except Exception:
    pass
```

Balayage AST, quelques secondes. **Aucun code, aucun gardien, aucun test ajouté.**

## Ce que le détecteur signale, et ce qu'il laisse passer

Un `assert` n'est signalé que si les trois conditions tiennent :

1. il est dans le **`body`** d'un `try` ;
2. ce `try` a un handler qui attrape `AssertionError` — `except:` nu,
   `except Exception`, `except BaseException`, `except AssertionError`, ou un
   tuple en contenant un ;
3. ce handler ne **relance pas** et n'appelle pas `pytest.fail`.

Sont donc exclus, à dessein : `except ValueError` (n'attrape pas
`AssertionError`), un handler qui relance, un `try/finally` sans handler, et un
`assert` situé **dans** le handler.

**Témoin obligatoire avant emploi** — 3 fautes plantées, 6 cas légitimes :

```text
except Exception / except: nu / except AssertionError   → 3 signalées
except ValueError · raise · pytest.fail · finally seul
   · assert hors try · assert dans le handler           → 0 signalé
```

## Le résultat, avec ses dénominateurs

```text
                        assert au total   dans un `try`   AVALÉS
tests/                          5 663             91         0
vertex/                             2              0         0
terminal.py                         1              0         0
```

**Côté tests, le zéro est substantiel** : 91 assertions vivent réellement dans un
`try`, et la répartition est sans exception —

```text
91  try/finally SANS handler (motif de remise en état)
 0  handler attrapant AssertionError
```

Autrement dit, les 91 candidates sont **toutes** dans le motif imposé depuis le
lot 387 : `try: … finally: remise en état`. Aucun `except` de la suite n'est en
position d'avaler une assertion.

**Côté production, le zéro est trivial, et il faut le dire** : `vertex/` contient
**2** `assert` en tout, `terminal.py` **1**. Un « 0 avalé » sur 3 assertions ne
prouve presque rien — le mentionner comme un succès serait un zéro décoratif.

## Ce que les 3 assertions de production font, puisqu'on les a comptées

```text
terminal.py:5887                     extraction de l'Opportunity Brief JS vérifiée à l'import
vertex/options/call_selector.py:21   précondition : direction LONG uniquement
vertex/strategy/executive_engine.py:161   assert decision in FINAL_DECISIONS
```

La troisième garde le **vocabulaire canonique du verdict final** — c'est un
invariant produit. Or un `assert` **disparaît** sous `python -O`.

Vérifié plutôt que supposé : **aucun lanceur n'utilise `-O`**, et
`PYTHONOPTIMIZE` n'apparaît nulle part dans le dépôt (`Lancer_VERTEX.bat`,
`Lancer_VERTEX_DEMO.bat`, `Installer_Demarrage_Auto.bat`, scripts, configs).
Les trois assertions sont donc **actives sur tous les chemins de lancement
documentés**. Ce n'est pas un défaut ; c'est une fragilité latente — si un jour
un lancement passait `-O`, deux vérifications disparaîtraient en silence.
**Classé rang 4**, non corrigé : ajouter une garde ici serait le changement
gratuit que la boucle s'interdit.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — ni production, ni test ; `git status` vide de bout
  en bout. Pas de preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**,
  aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Le détecteur raisonne sur la **structure syntaxique**. Une assertion neutralisée
autrement — par un `pytest.mark.xfail`, par un `contextlib.suppress`, ou par une
aide qui capture l'exception elle-même — ne serait pas vue. Et il ne dit rien de
la **justesse** des 5 663 assertions : seulement qu'aucune n'est bâillonnée par
un `except`.

## Où en est la boucle

Neuvième lot court, neuvième point de contrôle distinct. Avec le 403, la question
« la suite peut-elle échouer ? » est traitée sous ses deux angles : assertions
**absentes** (403) et assertions **muselées** (404). Les deux réponses sont
négatives, et les deux dénominateurs sont mesurés.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388, tous les dossiers de rang 1 à l'arrêt.
