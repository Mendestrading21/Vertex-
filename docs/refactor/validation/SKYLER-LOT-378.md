# SKYLER LOT 378 — Les exceptions : recensement gelé, et deux fois où la vérification m'a corrigé

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-378` (base : lot 377 fusionné,
58f0c83)

## Piste calibrée

Angle mort déclaré au lot 377. Risque produit précis : un `except` qui avale une
erreur transforme une donnée **manquante** en **blanc muet**, ou pire en
**chiffre plausible**. L'utilisateur lit « rien à signaler » ou « 50 » là où la
vérité est « je n'ai pas pu savoir ». C'est l'invariant n°4.

## Mesure — 254 handlers `except`

```text
except → repli NU (ni trace ni marque)   124   48,8 %
except → autre (continue/assign…)         66   26,0 %
except: pass (avale tout)                 46   18,1 %
except → repli MARQUÉ                     17    6,7 %
except → trace conservée                   1    0,4 %
```

124 « replis nus » : le chiffre fait peur, et mon premier classement confondait
deux choses opposées. Ce que le handler **renvoie** tranche :

```text
None          70   ← contrat « valeur ou None » : HONNÊTE, l'appelant affiche —
expression    35
NOMBRE        12   ← seule famille qui menace l'invariant
liste vide     8
dict vide      7
dict           5
booléen        4
```

Un `except: return None` dans un utilitaire de coercition est exactement ce que
l'invariant demande. Seuls les **12 replis numériques** substituent une valeur
plausible à une donnée absente.

## Première correction : la vérification m'a empêché d'innocenter le code

Deux des douze renvoient **50** (`quant_engine.entry_quality`,
`target_room_score`). J'allais les excuser : 50 est le point de départ de la
fonction (`s = 50.0`) et le défaut de ses entrées (`_f(…, 50)`), donc « le neutre
déclaré de l'échelle ». **Exécution faite, c'est faux :**

```text
entry_quality({})    = 76      ← entrée VIDE, tout par défaut
entry_quality(None)  = 50      ← chemin except
entry_quality(réel)  = 95
```

À entrée vide la fonction rend **76**, pas 50. `s = 50.0` est un point de départ
**interne**, pas une sortie naturelle. Le repli 50 est donc bien un score
**plausible et indiscernable** d'une mesure.

C'est la première fois de la boucle que la vérification sur valeurs réelles me
corrige **dans ce sens** : d'habitude elle m'empêche d'accuser du code sain ; ici
elle m'a empêché de l'innocenter.

## Verdict : CARACTÉRISATION, pas de faute prouvée

Le chemin est **défensif** : il exige que `d` ne soit pas un dict (`None`), alors
que les appelants passent des lignes de scan. Je n'ai trouvé aucune entrée réelle
qui l'atteigne. **Mais s'il l'était, l'utilisateur verrait 50 sans rien qui le
distingue d'une mesure.**

Je ne touche donc à rien — modifier un moteur de scoring sur un défaut non
démontré serait exactement le changement gratuit que la boucle s'interdit. Ce que
ce lot livre, c'est le **recensement gelé**.

Observation adjacente, versée aux dossiers : `opportunities_api._followed_count`
et `_positions_count` renvoient `0` sur exception, rendant « desk illisible » et
« desk vide » indiscernables. Portée limitée : la route qui les consomme marque
bien ses propres erreurs (`500` + `error`).

## Seconde correction : ma borne absorbait la première régression

La preuve ROUGE a d'abord donné **NE MORD PAS** sur le cas « `raise` privé de son
message ». Diagnostic : j'avais écrit une tolérance de 3 `raise` muets sur un
chiffre annoncé de 2. Mesure refaite avec le critère du gardien lui-même :
**39 `raise` portant une exception, 1 seul muet** — mon « 40 dont 2 » venait d'un
critère plus large où les messages construits par `%` passaient pour absents.

Borne ramenée à la mesure (`<= 1`). **Une borne qui absorbe la première
régression n'est pas une borne** — elle donne le confort d'un gardien sans son
effet, comme la myopie du lot 377 donnait le confort d'une couverture.

## Gardien

`tests/test_replis_exception_lot378.py` (9 tests) :

- **périmètre** + **anti-vide** (≥ 150 handlers) — sans dénominateur, les bornes
  ne prouveraient rien ;
- **le recensement gelé** : aucun repli numérique non recensé, avec sa
  justification par entrée ;
- **anti-péremption** : une entrée qui ne correspond plus à rien doit être
  retirée, sinon la liste blanche pourrit et couvre des cas disparus ;
- **bornes de dérive** (`≤ 14` replis numériques, `≤ 50` `except: pass`) qui ne
  jugent pas le code mais rendent la **dérive** visible ;
- **la caractérisation en exécution** : le repli 50 doit rester distinct de la
  sortie à entrée vide — si les deux coïncident un jour, la caractérisation
  change et ce rapport doit être relu ;
- **anti-vide de la caractérisation** : le chemin `except` doit rester
  atteignable ;
- **`raise` muets ≤ 1**, borne fixée à la mesure.

### Preuve ROUGE

```text
ROUGE OK  nouveau repli numérique introduit          | restauration identique
ROUGE OK  borne de dérive des `except: pass` franchie| restauration identique
ROUGE OK  repli aligné sur la sortie à entrée vide   | restauration identique
ROUGE OK  entrée périmée dans le recensement         | restauration identique
ROUGE OK  raise privé de son message                 | restauration identique
après restauration : 9 passed
VERDICT : gardien mordant sur les 5 cas
```

Deux cas ont d'abord été **sautés** (motifs visant des lignes inexistantes sous
cette forme) : signalés par le script, puis corrigés sur les vraies lignes. Le
cinquième a d'abord **échoué à mordre** — c'est ce qui a révélé la borne trop
lâche.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 377, 58f0c83) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2721 → 2730 passed / 2 skipped** — verte (+9).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Les 46 `except: pass` sont **comptés, pas jugés** : je n'ai pas examiné ce que
chacun avale, et la borne ne dit rien de leur légitimité. Les 35 replis en
« expression » (une variable, un appel) ne sont pas classés — leur valeur n'est
pas connue statiquement. La caractérisation de `entry_quality` vaut pour cette
fonction ; les 10 autres replis numériques sont recensés et sommairement
justifiés, pas individuellement sondés en exécution. Enfin, « recensé » ne veut
pas dire « acceptable » : le gel empêche la dérive, il ne valide pas l'existant.

## Suite

LOT 379 : **préparer le bilan de tranche**. Rassembler les chiffres de 370→379
(verdicts, gardiens ajoutés, corrections de méthode, suite, dossiers en attente)
pour que le LOT 380 soit un vrai bilan et non une compilation improvisée. Pistes
encore ouvertes : les 46 `except: pass` examinés un par un ; les refus construits
en variable (angle mort du 377) ; les trois sites de concaténation du 374 ; les
formes imbriquées du 375.
