# SKYLER LOT 508 — `/markets`, dernière page jamais auditée : `climate()` note l'ABSENCE de donnée comme une donnée MOYENNE. Un objet marché ne contenant qu'une clé non pertinente rend un verdict complet — **score 46, « NEUTRE »** — sur la même échelle que les verdicts réels. Et trois de mes quatre pistes se sont effondrées sous leurs propres contrôles

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-508` (base : lot 507 fusionné,
`5a57e7ed`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** et `/markets` — la dernière des huit pages jamais auditée. Avec ce lot,
**les huit pages produit ont toutes été regardées au moins une fois.**

## La réponse

```text
BARÈME de market_lens.climate(), lu dans le code
  régime    TREND 35 · NEUTRAL 18 · CHOP  6 · ABSENT 14   ← absent NOTÉ AU-DESSUS de CHOP
  roro      RISK-ON 25 · RISK-OFF 2      · ABSENT 12      ← absent au-dessus de RISK-OFF
  above50   (a50/100)×25                 · ABSENT → 50 SUBSTITUÉ, soit 12,5
  vix       calme 15 · stress 2          · ABSENT  8      ← absent au-dessus de stress

CE QUE LA FONCTION REND
  marché {}                              → None                      ← honnête
  marché {'foo': 1}                      → score 46 · « NEUTRE »     ← VERDICT COMPLET
  marché {'breadth': {}}                 → score 46 · « NEUTRE »
  tout à None sauf une clé               → score 46 · « NEUTRE »
  le PIRE marché réel (CHOP/RISK-OFF/stress/a50=5)  → score 11 · « DANGEREUX »
  le MEILLEUR marché réel                           → score 99 · « FAVORABLE »
```

**Aucune donnée réelle produit 46 ; le pire marché réellement mesurable produit
11.** L'absence n'est donc pas seulement notée — elle est notée **plus haut que
la réalité la plus mauvaise**, sur la même échelle, avec la même étiquette
qu'un marché médiocre authentique. Rien ne distingue à l'écran « je ne sais
pas » de « c'est moyen ».

C'est l'invariant du produit, cité dans `CLAUDE.md` : *données RÉELLES
uniquement — donnée absente → `—`/`n/d` honnête*.

## Pourquoi l'état est atteignable

`market_context._num()` porte sa propre docstring : « Nombre fini ou **None** —
l'état réel du scan porte parfois des dicts/chaînes là où un nombre est attendu ;
on extrait **honnêtement**, jamais de TypeError ». **`None` est donc la forme
CHOISIE pour représenter une donnée manquante** — et c'est précisément la forme
que `climate()` note comme moyenne. Une source qui échoue (VIX indisponible,
régime non calculé) ne vide pas `market_ctx` : elle y laisse des `None`.

**Ce que je ne peux pas montrer** : le scan DEMO remplit ses dix clés, donc je
n'ai **pas** observé l'état dégradé en vrai. Je montre que le code le produit
et que `None` est la forme documentée de l'absence, pas qu'il se produit chez
l'utilisateur.

## Le gardien teste exactement le cas qui marche

```text
tests/test_market_lens.py:20    assert ml.climate(None) is None
```

Le seul cas d'absence couvert est le **seul qui soit honnête**. Le cas partiel —
celui où la fonction fabrique — n'est vérifié par rien.

## Le second contrôle — TROIS de mes quatre pistes se sont effondrées

C'est le lot où mes propres contrôles ont le plus détruit. Je les publie parce
que chacune aurait fait un dossier faux.

### 1. Le waterfall de santé du marché — il RÉCONCILIE

`markets_page.py` dessine `0.30·>MM50 + 0.25·>MM200 + 0.25·Breadth + 0.20·Adv/Déc`
avec `health` en **total**. Un waterfall dont les barres ne somment pas au total
serait un défaut net. Vérifié contre le moteur :

```text
terminal.py:1466  health = max(0, min(100, round(0.30*pa50 + 0.25*pa200
                                                 + 0.25*breadth + 0.20*advpct)))
clés émises       'pct_a50', 'pct_a200', 'advpct', 'breadth', 'health'
clés lues par le JS   inter.pct_a50 · inter.pct_a200 · inter.breadth · inter.advpct
```

**Les poids sont identiques, les noms de clés aussi.** Et comme les quatre poids
somment à 1,00 avec chaque terme dans [0, 100], le `clamp` ne peut jamais mordre.
**Le waterfall est juste. Retiré.**

### 2. Deux seuils pour la même étiquette — INVISIBLE

`climate()` déclare FAVORABLE à **62** ; `/api/market/summary` recalcule une
étiquette à **65**. Sur 62–64 les deux se contredisent. Mais :

```text
occurrences de « climate » dans 473 509 caractères servis : ZÉRO
la réponse de /api/market/summary contient 'score' et 'verdict' — PAS 'label'
```

**L'étiquette de `climate()` n'atteint aucun écran.** La contradiction est
interne, l'utilisateur n'en voit qu'une. **Retiré.**

### 3. La jauge « > MM50 » qui affiche `above200` — RÉELLE mais NON ATTEINTE

Le code est bien ce que je soupçonnais, et l'effet mesuré est spectaculaire :

```text
cas                                     jauge   étiquette   phrase de lecture
above50=42 ET above200=71 (témoin)        42    > MM50      Participation étroite
above200=71 SEUL                          71    > MM50      Participation SAINE
above50=42 SEUL (non accusé)              42    > MM50      Participation étroite
```

Dans le cas de repli, **le même écran se contredit** : la jauge affiche 71 sous
« > MM50 » pendant que la carte de détail juste en dessous écrit « Titres >
MM200 : 71 % ». Et le verdict bascule d'« étroite » à « saine ».

**Mais `above50` est TOUJOURS présente** dans la charge utile mesurée :

```text
breadth du scan DEMO : {'above50': 50, 'above200': 45, 'adv': 8, 'dec': 12,
                        'nh': 4, 'nl': 3, 'buy': 10}
```

**Ma propre règle 507-A l'interdit : un défaut théorique n'est pas un dossier.**
Je l'ancre comme fragilité, je ne le classe pas. (Contrôle 504 tout de même
appliqué : le repli **n'est pas orienté** — il rassure quand MM200 > MM50 (42 →
71), il accuse dans l'autre sens (78 → 22).)

**Arrêtés avant publication : 89 → 92.**

## DOSSIER 508-A — Classement

**Rang 3, et je dis par rapport à quoi.**

L'étalon naturel est le **432** (« la synthèse est fausse, et elle est fausse
dans le sens le plus coûteux », rang 1) et à l'opposé le **454** (rang 4, « rien
de faux n'est montré »). Celui-ci est entre les deux :

**Ce qui le tient au-dessus du rang 4** : quelque chose de faux **est** montré.
Un score et une étiquette de verdict sont peints à partir de données qui
n'existent pas, sur la même échelle que les verdicts réels — et notés **plus
haut que le pire marché mesurable**. Ce n'est pas une conséquence calculée puis
jetée : c'est une conclusion fabriquée puis affichée.

**Ce qui l'empêche d'aller plus haut** :

1. **Je n'ai pas démontré l'état dégradé en production.** Sur le scan DEMO les
   dix clés sont pleines. Je montre le code, le barème et la forme documentée de
   l'absence — pas une occurrence réelle. C'est exactement la limite qui m'a fait
   refuser un dossier au 507, et je ne peux pas être plus indulgent ici sans être
   incohérent.
2. **Le cas totalement vide est honnête** (`None`), donc la fonction sait
   s'abstenir : le défaut est un trou dans une garde qui existe, pas une absence
   de garde.

Correction pressentie, non engagée : compter les dimensions réellement
disponibles et **rendre `None` en dessous d'un minimum**, ou servir le score avec
un compte explicite (« 2 dimensions sur 4 disponibles ») ; et remplacer la
substitution `else 50` par une exclusion du terme avec repondération. **Aucun GO,
rien n'est engagé.**

## Ce que `/markets` fait BIEN, mesuré (règle 505)

- Le **waterfall réconcilie exactement** — poids et clés alignés sur le moteur.
- La carte de détail de breadth **étiquette correctement** MM50 et MM200, et
  n'affiche que les lignes réellement fournies.
- Elle écrit d'elle-même sa limite : « Calculé sur l'univers des leaders scannés
  (partiel, pas tout le NYSE). Advance/decline cumulés multi-séances non fournis
  — **non affichés plutôt qu'inventés**. »
- `climate({})` rend `None`.

## Portée — ce que ce lot NE dit PAS

- **L'état dégradé n'a pas été observé en production.** Tout le dossier repose
  sur le barème lu et sur la forme documentée de l'absence.
- Les charges utiles de la jauge sont **fabriquées** ; le scan DEMO, lui, est
  réel et c'est lui qui montre que le cas de repli n'est pas atteint.
- **Aucun navigateur ouvert.** `loadBreadth` (6 336 caractères) a été extraite
  des octets servis et exécutée sous node avec `VX.fetch` bouchonné.
- Seules `/scan`, `/api/market/summary`, `/api/market/regime` et `/cal-feed`
  sont impliquées — toutes sur la liste vérifiée sûre. Aucun POST.
- **Les quatre autres sous-vues de `/markets`** (`overview`, `macro`, `sectors`,
  `volatility`) ne sont pas auditées ici.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les trois scripts.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Le tour est fini : les huit pages produit ont toutes été auditées au moins une
fois** (504 et 505 `/journal`, 506 `/portfolio`, 507 `/options`, 508 `/markets`,
les trois autres plus tôt). Cinq lots, cinq dossiers — mais d'un rang qui
décroît : rang 1, rang 2, rang 2, rang 3, rang 3. **La veine des surfaces
vierges s'épuise, et c'est une information.**

Ce lot est celui où mes contrôles ont le plus détruit : **trois pistes sur
quatre retirées**, dont une — la jauge — dont l'effet mesuré était le plus
spectaculaire du lot et que ma propre règle 507-A m'interdit de classer. Je note
que si je n'avais pas écrit cette règle la semaine dernière, j'aurais publié un
rang 2 sur un cas que le producteur n'atteint jamais.

Il faut maintenant **décider** : continuer en profondeur sur les vingt-neuf vues
hors empreinte, ou changer de registre. Je ne tranche pas seule ; je note que la
décroissance des rangs est un argument pour changer.

Feuille : **31 dossiers · seize rang 1 · onze rang 2 · cinq rang 3**.
Dettes nommées restantes : **les vingt-neuf vues servies hors empreinte** (dont
les quatre autres de `/markets`) ; **les trois sous-vues de `/journal`** ;
**l'espion au troisième niveau** (toujours déconseillé) ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 92 (+3)** ; publiés
puis corrigés **13** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
