# SKYLER — LOT 591

## Ce que le lot établit

**La suite compte quatre gardiens documentaires — 12 tests sur 2864, soit
0,42 %.** Ils surveillent mes propres livrables : l'INDEX, les rapports, les
documents vivants, et jusqu'aux promesses écrites dans les docstrings.

Et l'un d'eux encode une règle que je croyais n'exister que dans mes briefs :

> « Les rapports `SKYLER-LOT-NNN.md` sont des **archives** : ils décrivent
> l'état de leur époque, **on ne les réécrit pas**. »
> — `tests/test_references_vivantes_lot364.py`, docstring

**La politique d'ajout-seulement est écrite dans un test.** Ce n'est pas une
convention que je m'impose : c'est un contrat du dépôt.

## Le choix (kkk)

Le 590 a découvert **par accident** qu'un gardien surveillait ma ligne d'INDEX.
Personne ne les avait jamais inventoriés.

## Le piège, écrit avant la mesure (564), avec sa classe MIXTE prévue (590-A)

| volet | verdict |
| --- | --- |
| **(nombre)** — « une poignée, moins de dix » | **CONFIRMÉ** : **4** |
| **(nature)** — « surtout des références de fichiers » | **RÉFUTÉ** : **4 exigences sur 8** seulement |
| **verdict global** | **MIXTE** |

**C'est la première fois qu'un piège est classé MIXTE parce que la classe était
prévue d'avance**, et non reconstruite après coup. La règle 590-A, écrite hier,
a servi aujourd'hui.

*Et l'aveu écrit avant la mesure tient* : c'était la **cinquième** fois que
j'écrivais une attente « peu nombreux / surtout technique ». Sur le nombre, elle
est enfin juste ; sur la nature, non.

## Les quatre gardiens, lus

| fichier | tests retenus | ce qu'il garde |
| --- | --- | --- |
| `test_skyler_index_integrity_lot228.py` | 4 sur 4 | l'INDEX ↔ les rapports |
| `test_references_vivantes_lot364.py` | 4 sur 4 | « ce que le projet dit de lui-même est-il vrai ? » |
| `test_promesses_docstrings_lot366.py` | 3 sur 3 | un moteur annonce-t-il une sortie qu'il ne produit pas ? |
| `test_postmortem_view_lot23.py` | **1 sur 7** | la couverture des lots dans l'INDEX |

**Compter par fichier aurait surestimé de six** : le quatrième ne consacre
qu'**un seul** de ses sept tests à la documentation. Le comptage est fait
fonction par fonction.

### Les huit exigences, lues dans les assertions

| exigence | ce qu'elle impose |
| --- | --- |
| référence morte | aucun `SKYLER-LOT-*.md` cité par l'INDEX ne doit manquer sur disque |
| rapport orphelin | tout rapport du périmètre doit avoir sa ligne d'index |
| périmètre documenté | l'en-tête de l'INDEX doit dire que les lots 01-09 vivent hors index |
| **garde-fou de volume** | l'INDEX doit citer **au moins 200** rapports |
| gardien inexistant | aucune source Python ne cite un `tests/test_*.py` disparu |
| **document vivant honnête** | un document vivant **peut** citer un gardien retiré — **à condition de le dire sur la même ligne** |
| promesse de docstring | tout identifiant `CAPS_SNAKE` cité dans une docstring de moteur doit exister dans le paquet |
| couverture des lots | chaque lot doit figurer dans l'index |

**Quatre portent sur des références, quatre non.** D'où le MIXTE.

## Trois gardiens sur quatre se surveillent eux-mêmes

`test_skyler_index_integrity_lot228`, `test_references_vivantes_lot364` et
`test_promesses_docstrings_lot366` portent **chacun** un test nommé
`test_le_gardien_ne_tourne_pas_a_vide`. Le commentaire du 228 le dit :

> « si le format des lignes changeait, `_cited()` rendrait vide et les deux
> tests ci-dessus passeraient **sans rien vérifier** — on exige du volume. »

**Un gardien sans garde-fou de volume peut passer en vérifiant zéro chose.**
Trois sur quatre s'en prémunissent ; le quatrième (le test unique du lot 23) non.

## Neuf fichiers ne sont pas des gardiens

Sur les **13** fichiers de `tests/` qui contiennent le mot `docs`, **neuf** ne
font que le **mentionner** : sept en commentaire (« validé au navigateur, voir
tel rapport »), deux en **exclusion** (`':!docs/redesign'` dans un `git grep`,
`'/docs'` dans une liste de chemins ignorés). Les compter aurait triplé le
résultat.

## Second contrôle (481) — aucun gardien ne surveille les bancs

La restriction de l'instrument est « lit un fichier de `docs/` ». Elle exclut un
gardien qui surveillerait le **scratchpad** ou les **bancs**. Cherché sur les
301 fichiers, cinq motifs (`scratchpad`, `claude-0`, `l###_`, « banc », `/tmp/`) :

**zéro.** L'unique correspondance sur « banc » est le mot **« bancaire »** dans
un commentaire d'arrondi — un faux positif de recherche par sous-chaîne, écarté
après lecture.

**Une absence mesurée est un résultat (556-B)** : les bancs qui produisent
**chaque chiffre publié depuis soixante lots** ne sont ni versionnés, ni testés,
ni sauvegardés. Ils vivent dans un répertoire temporaire, et rien ne les garde.

## L'arrêt du lot — un critère syntaxique n'est pas un critère comportemental

Mon premier banc cherchait le littéral `docs/` dans la source. **Le témoin en
était absent** : `test_skyler_index_integrity_lot228.py` construit son chemin
par segments —

```python
DOCS = pathlib.Path(__file__).resolve().parent.parent / 'docs' / 'refactor' / 'validation'
```

— et ne contient **aucun** littéral `docs/`. Le second banc, élargi au mot
`docs`, est tombé dans l'excès inverse : **13 fichiers**, mentions et exclusions
comprises.

**Deux bornes, aucune juste : 9 (trop étroit, témoin absent) et 13 (trop large).
La bonne réponse — 4 — vient de la lecture, pas d'un motif.**

Les deux bancs sont **conservés tels quels** : ce sont eux qui ont montré les
deux bords.

**Arrêtés avant publication : 216 → 217 (+1).**

## Ce que le lot n'établit pas

- **Que ces quatre gardiens soient suffisants.** Ils sont lus et comptés ;
  aucun n'a été mis en échec exprès pour vérifier ce qu'il attrape vraiment.
- Que les neuf mentions soient sans valeur : elles **documentent** où la
  validation navigateur a eu lieu — ce n'est pas rien, ce n'est pas un test.
- Que 0,42 % soit peu ou beaucoup : **aucun point de comparaison** n'existe.
- Que l'absence de gardien sur le scratchpad soit un défaut : les bancs sont
  des **preuves d'un lot**, pas du code de production.

## Limites déclarées

- Le critère final (« lit un document et exige quelque chose de lui ») a été
  appliqué **à la main sur 13 fichiers**. Il est reproductible parce que les 13
  sont nommés, mais ce n'est pas un programme.
- Le comptage « 12 tests sur 2864 » compare des fonctions `test_` à un total de
  cas pytest ; **un test paramétré compte pour plusieurs cas** — le rapport est
  donc un ordre de grandeur, pas une fraction exacte (546-A).
- Seuls les fichiers de `tests/` ont été balayés : un gardien vivant ailleurs
  (hook, CI) n'est pas mesuré.

## Règles neuves

- **591-A — UN CRITÈRE SYNTAXIQUE N'EST PAS UN CRITÈRE COMPORTEMENTAL.**
  « cite `docs/` » ≠ « lit un document ». Quand deux motifs donnent 9 et 13, la
  réponse n'est ni l'un ni l'autre : elle se lit.
- **591-B — LA RÈGLE D'AJOUT-SEULEMENT EST UN CONTRAT DU DÉPÔT, PAS UNE
  CONVENTION DE LA BOUCLE.** Elle est écrite dans
  `test_references_vivantes_lot364.py`.
- **591-C — UN GARDIEN SANS GARDE-FOU DE VOLUME PEUT PASSER EN VÉRIFIANT ZÉRO
  CHOSE.** Trois des quatre portent `test_le_gardien_ne_tourne_pas_a_vide` ;
  c'est le motif à copier, pas à inventer.

## Ce que le dépôt fait bien

- **Le contrat le plus fin du lot est un contrat d'honnêteté** : un document
  vivant **peut** citer un gardien disparu, **à condition de le dire sur la même
  ligne**. Il autorise la mémoire sans autoriser le mensonge.
- **Trois gardiens sur quatre se prémunissent contre eux-mêmes.**
- **La distinction document vivant / archive est écrite**, pas implicite : on
  sait lesquels doivent dire vrai aujourd'hui.
- **Les quatre gardiens portent leur numéro de lot dans leur nom** (`lot228`,
  `lot364`, `lot366`, `lot23`) : on remonte à la décision qui les a créés.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié** — pas de bump,
  SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` **vide** — aucun test modifié

## Comptes

- Arrêtés avant publication : **217 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **12**
