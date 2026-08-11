# SKYLER — LOT 600 · BILAN n°19 de la tranche 590-599

## Ce que le lot établit

**La boucle ne s'est pas repliée sur elle-même — elle s'est ouverte.** Mon
attente disait que la majorité des dix lots n'aurait lu que des rapports. C'est
faux : **4 sur 10 ont ouvert un fichier de production, 6 sur 10 un fichier de
`tests/`, et 4 seulement n'ont lu que des rapports.**

Et la tranche précédente était **plus** refermée :

| tranche | ouvre du produit | ouvre `tests/` | n'ouvre que des rapports |
| --- | --- | --- | --- |
| **580-589** | 2 / 10 | **0 / 10** | **8 / 10** |
| **590-599** | **4 / 10** | **6 / 10** | 4 / 10 |

En revanche, **aucun des dix lots n'a modifié un seul octet de `vertex/`,
`terminal.py` ou `tests/`** — vérifié par `git show --stat`, pas par ce que les
rapports affirment.

## BILAN n°19 — la tranche sur pièces

| grandeur | valeur |
| --- | --- |
| lots livrés et fusionnés | **10** (590 → 599) |
| verdicts de piège | **MIXTE 7 · RÉFUTÉ 1 · CONFIRMÉ 1 · non publié 1** |
| arrêts avant publication | **+14** (215 → 229) |
| règles neuves | **30** |
| … déjà citées par un lot ultérieur | **17 (57 %)** |
| … jamais citées | **13** |
| … retirées | **1** — `594-C`, au lot suivant |
| **nombres publiés puis corrigés** | **0** — le compteur n'a pas bougé de 40 |
| fichiers de production modifiés | **0** |

**Le chiffre le plus fort de la tranche est un zéro** : sur dix lots et
quatorze arrêts, **aucun nombre publié n'a eu besoin d'être corrigé après
coup**. Les quatorze fautes ont toutes été prises avant la publication.

Le lot **590** n'a pas de verdict global : il précède la forme du tableau à
volets (née au 591). **Compté comme non publié, pas réparti au jugé** (588-A).

Les règles les plus reprises : **590-A** (8 citations), **594-C** (7 — puis
retirée), **590-C** (5), **591-A** (5), **591-B** (4), **596-B** (4).

## Le piège, classe MIXTE prévue d'avance (590-A)

| volet | verdict |
| --- | --- |
| **(a)** « aucun des dix lots n'a touché un fichier de production » | **CONFIRMÉ** — **0 / 10**, par le diff |
| **(b)** « la majorité n'a lu que des rapports » | **RÉFUTÉ** — **4 / 10**, pas une majorité |
| **global** | **MIXTE** |

Le volet (a) est confirmé **par `git show --stat`**, pas par la prose des
rapports : c'est le diff qui dit ce qui a changé.

## La distinction qui décide tout, posée avant de compter

| acte | exemple | compte ? |
| --- | --- | --- |
| **TOUCHER** | modifier un octet de `vertex/**` | oui |
| **LIRE** | un banc ouvre `vertex/scanner/stages.py` | **oui** |
| **VÉRIFIER** | `import terminal` pour le MD5 rituel | **NON** |

Le contrôle MD5 tourne **à chaque lot par rituel**. Le compter aurait donné
« dix sur dix ont mesuré le produit » — vrai au sens littéral, faux au sens de
la question (599-B).

## Les arrêts du lot — une calibration qui passe à vide, puis un préfixe trompeur

**1. La calibration du premier banc a PASSÉ, et c'était un faux succès.**
`l600_portee.py` annonçait « calibration PASSÉE ». Ses deux témoins sortaient du
bon côté **pour de mauvaises raisons** :

- `l594_force.py` — « n'ouvre que des rapports » : il n'affichait **aucun chemin
  du tout**, donc la condition était vraie **par vacuité** ;
- `l598_role.py` — un seul chemin (`terminal.py`) alors qu'il parcourt aussi
  `vertex` et `tests` par `os.walk(racine)`, où `racine` est une variable.

Cause : l'extracteur ne voyait que `open('littéral')`. Or **tous mes bancs
construisent leurs chemins depuis une constante de module** (`DOCS =
'docs/refactor/validation'`). **Une calibration qui passe à vide est pire qu'une
qui échoue : la seconde alerte, la première endort.**

**2. Le critère corrigé comptait `tests_garde` comme un chemin.** `c.startswith('tests')`
attrapait des **clés JSON** — `tests_garde`, `tests_pertinent`,
`tests_dans_gardiens` — et une **regex**, `vertex/[A-Za-z0-9_/]+\.py`.
**Cinquième morsure de 596-B dans cette série** : le préfixe est bon, le rôle ne
l'est pas. Critère resserré : racine exacte ou suivie d'un `/`, et **aucun
métacaractère de regex**.

Les deux bancs fautifs sont **conservés tels quels**.

**Arrêtés avant publication : 229 → 231 (+2).**

## Second contrôle (481) — la tranche 580-589, et il réfute le récit

La restriction est « la tranche 590-599 ». Le cas exclu : les dix lots
précédents, mesurés au **même critère resserré**.

**Le repli sur soi n'est pas récent — il est en recul.** La tranche 580-589
n'ouvrait **jamais** `tests/` et lisait **8 fois sur 10** uniquement des
rapports. Si la boucle s'était refermée, les chiffres iraient dans l'autre sens.

**Ce que la mesure ne dit pas** : que lire du produit soit utile. Ouvrir
`vertex/scanner/candidate_pipeline.py` pour constater que « candidate » est un
mot de métier **n'améliore pas le produit** — cela évite une conclusion fausse.
C'est une mesure de portée, pas de valeur.

## Ce que le lot n'établit pas

- **Si mesurer ses propres instruments vaut le coût.** Dix lots, trente règles,
  quatorze arrêts — **rien ici ne dit ce que ces arrêts valent pour le
  produit**. Le lot compte ; il ne juge pas.
- **Ce que l'humain attendait de cette tranche.** Il n'a pas répondu ; **son
  silence n'est pas un mandat**, c'est une absence de réponse, et je la nomme
  comme telle.
- Que les 13 règles jamais citées soient mortes : **le silence n'est pas la
  mort** (596-C, mesurée au 597 sur `550-B`).
- Que « 0 nombre corrigé » signifie « 0 nombre faux » : **cela signifie qu'aucun
  n'a été détecté après publication**. Le dénominateur reste inconnu (599).

## Limites déclarées

- Le relevé « LIRE » porte sur les **constantes de chemin des bancs Python** du
  scratchpad. Un banc JavaScript, ou un chemin construit à l'exécution, échappe.
- « toucher » vient de `git log --grep 'lot N '` : **un commit qui ne nomme pas
  son lot dans ce format échapperait**. Les dix lots en ont deux ou trois
  chacun, ce qui est cohérent avec le rituel.
- Les trois comptes (produit / tests / docs) **ne s'additionnent pas** : un lot
  peut ouvrir les trois.
- **Aucun rapport n'a été corrigé** — bilan sur pièces (591-B).

## Règles neuves

- **600-A — UNE CALIBRATION QUI PASSE À VIDE EST PIRE QU'UNE QUI ÉCHOUE.**
  Vérifier que le témoin produit une **valeur non vide** avant de conclure qu'il
  satisfait la condition. « Aucun chemin de produit » est vrai pour un banc qui
  n'affiche aucun chemin.
- **600-B — LE DIFF DIT CE QUI A CHANGÉ ; LE RAPPORT DIT CE QU'ON A CRU
  FAIRE.** Le volet « aucun fichier touché » se vérifie par `git show --stat`,
  jamais par la prose du cycle.
- **600-C — UN BILAN DOIT MESURER SA PROPRE TRANCHE CONTRE LA PRÉCÉDENTE.**
  Sans les 580-589, j'aurais publié « la boucle s'est refermée » ; avec, la
  tendance est inverse.

## Ce que le dépôt fait bien

- **Zéro nombre publié puis corrigé sur dix lots.** Quatorze fautes, toutes
  prises avant publication — la discipline du piège écrit d'avance tient.
- **57 % des règles neuves sont déjà reprises** par un lot ultérieur, et la
  seule fausse a été retirée **au lot suivant**, en append, sans réécrire son
  rapport d'origine.
- **La production n'a pas bougé d'un octet en dix lots** : SW `td-shell-v187`,
  MD5 8/8 à chaque fois, suite 2864 à chaque fois. **L'invariant READONLY tient
  sans exception.**
- **La tranche ouvre plus de fichiers du produit que la précédente** — le
  mouvement va vers le dépôt, pas vers le miroir.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucun rapport
  corrigé, aucun bloc BILAN de `STATUS.md` déplacé** — pas de bump, SW
  `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 600) **vides**

## Comptes

- Arrêtés avant publication : **231 (+2)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
