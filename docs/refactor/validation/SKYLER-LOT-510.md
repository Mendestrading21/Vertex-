# SKYLER LOT 510 — La chasse aux copies rend ZÉRO copie… et trouve **les versions CORRECTES**, écrites trois fois dans le dépôt. Puis le second contrôle établit que **les trois sont dans du code MORT** — aucune n'atteint le navigateur. Deuxième lot sans nouveau dossier, deux arrêts avant publication

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-510` (base : lot 509 fusionné,
`da778ff5`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(c)**, la règle 509-B appliquée aux quatre dossiers ouverts restants : *avant
de clore un dossier, grepper la formule caractéristique du défaut dans tout le
dépôt.* Le 509 avait montré que `_strat_tilt` dupliquait `climate` mot pour mot.

## La réponse

```text
signature (une FORME de code, pas un mot)            occurrences   origine retrouvée
TÉMOIN 508-A/509 · (a50 if a50 is not None else 50)        2       OUI — les 2 du 509
504-A · const num=(x)=>{…isFinite(n)?n:null}               3       OUI
504-A bis · idiome isFinite(x)?x:null, toutes lettres      4       OUI
505-A · conclusion sur les DEUX BORNES d'une série         1       OUI
506-A · accesseur pouvant rendre null, aplati par « || 0 » 2       OUI
```

**Aucune copie d'aucun des quatre défauts.** Le 505-A est unique. Le 506-A n'a
qu'un second site, et c'est du **vendor minifié** (`lightweight-charts`) —
coïncidence, pas copie.

Le crible rend autre chose : **les versions CORRECTES.**

## Les trois précédents — et le second contrôle les tue

Les deux autres occurrences de l'idiome `num()` **font ce que le 504-A ne fait
pas** : elles gardent `null` **et** `''` **avant** de convertir.

```js
vx_kit.py:92            function _n(v){ if(v==null||v==='') return null; … }
candlestick-lwc.js:18   function num(v){ if (v===null||v===undefined||v==='') return null; … }
performance_page.py:192 const num=(x)=>{const n=Number(x); return isFinite(n)?n:null;}   ← LE DÉFAUT
```

Et `journal.py:157` porte la version **direction-aware** que le 504-A n'a pas :
`var r = (t.dir==='SHORT') ? (e-x)/(s-e) : (x-e)/(e-s)`.

**J'allais écrire que la version correcte est DÉJÀ SERVIE** — `candlestick-lwc.js`
est un fichier statique, j'ai supposé qu'il était chargé. **Mesuré :**

```text
témoin POSITIF  vx-entities.js   chargé par 8 / 8 pages   (le 381 dit 8)  OK
témoin NÉGATIF  vx_kit           présent sur 0 / 8 pages  (le 381 dit 0)  OK

vx_kit.py:92           _n()     0 / 8 pages   ← CODE MORT
candlestick-lwc.js:18  num()    0 / 8 pages   ← CODE MORT
journal.py:157         rMult()  0 / 8 pages   ← CODE MORT
```

**Les trois précédents sont morts. Aucun n'atteint le navigateur.** Le précédent
existe dans le dépôt, pas dans le produit. C'est beaucoup plus faible que ce que
j'allais publier, et c'est la deuxième fois en deux lots qu'une supposition de
« servi » me trompe — le 381 avait déjà établi la leçon, je l'ai réapprise.

## L'observation qui reste, avec son n

**Sur trois idiomes examinés, la version correcte est dans le code mort et la
version fautive dans le code servi.** Trois cas, pas une loi — je l'écris avec
son effectif plutôt que d'en faire une règle. Mais le sens est net : quelqu'un a
écrit le bon traitement de l'absence au moins trois fois, et aucune de ces trois
fois n'est celle que le navigateur exécute.

## Le second contrôle borne aussi MON crible

`|| 0` n'est qu'une orthographe parmi d'autres pour « aplatir un inconnu en
zéro ». Mesuré, hors vendor :

```text
JS  x() || 0             1        ← le seul motif que j'ai criblé
JS  x ?? 0              13
JS  Number(x) || 0       7
JS  parseFloat(x) || 0   0
PY  float(x or 0)        4
PY  (x or 0)            30
────────────────────────────
TOTAL de la famille     55
```

**Mon motif couvre 1 occurrence sur 55.** Je peux donc affirmer que **la FORME
EXACTE du 506-A est isolée** ; je ne peux **pas** affirmer que la famille l'est.
Conclure « 506-A est un cas unique » aurait été abusif d'un facteur cinquante-cinq.

**Arrêtés avant publication : 95 → 97.**

## Ce que ce lot établit vraiment

1. **Les quatre dossiers ouverts n'ont pas de copie littérale.** 504-A, 505-A,
   506-A, 507-A restent des cas uniques *dans leur forme exacte*. La feuille est
   donc plus solide qu'elle n'aurait pu l'être — c'était le résultat annoncé
   comme possible par le 509, et c'est celui-là.
2. **Le 508-A reste le seul dossier dupliqué** (deux modules, établi au 509).
3. **La règle 509-C ne s'applique PAS ici comme je l'espérais.** « Le dépôt sait
   déjà faire » était vrai au 509 (`scorecard.verdict` est vivant et servi) ;
   c'est **faux** ici — les précédents sont morts. La règle tient, son
   application à ce cas non.

## Portée — ce que ce lot NE dit PAS

- **Le crible est LITTÉRAL.** Une copie sémantique écrite autrement lui échappe,
  et le contrôle II chiffre cet angle mort à **54 occurrences sur 55** pour une
  seule des quatre familles. Les « zéro copie » sont des zéros **de forme**, pas
  des zéros de fond.
- Je n'ai criblé **que** les quatre dossiers ouverts, avec **une à deux
  signatures chacun**. Un défaut a plus d'une forme caractéristique.
- Le 507-A n'a pas été criblé par une signature de code : son défaut est une
  ABSENCE de consommateur, qu'un grep de formule ne capture pas. **Il reste hors
  de ce lot**, et je le dis plutôt que de le compter comme « sans copie ».
- **Aucun navigateur, aucun POST, aucune route réseau.** Lecture de sources et
  récupération des huit pages servies.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Deuxième lot consécutif sans nouveau dossier.** Le 509 en avait donné zéro, le
510 aussi. Ce que ces deux lots rapportent, ce sont des **bornes sur mes propres
conclusions** : le 509 a doublé la portée du 508-A et publié l'échec de son
contrôle négatif ; le 510 établit que les défauts ouverts n'ont pas de copie
littérale, et que trois précédents corrects existent — mais morts.

La série des rangs est maintenant **1, 2, 2, 3, 3, 0, 0**. Sept lots. Je l'écris
sans l'adoucir : **la chasse aux défauts ne rend plus rien de neuf**, et les deux
derniers lots ont surtout servi à mesurer la fiabilité de ce qui est déjà publié.
C'est utile, mais ce n'est plus du développement.

Je ne décide pas seule de changer de registre. Je note que les trois pistes
restantes (vues hors empreinte, espion au troisième niveau, rangs relatifs
postérieurs au 480) sont toutes de l'audit, et qu'**aucune n'est du produit**.

Feuille **inchangée : 31 dossiers · seize rang 1 · onze rang 2 · cinq rang 3**.

Comptes séparés : résultats faux **arrêtés avant publication 97 (+2)** ; publiés
puis corrigés **13** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
