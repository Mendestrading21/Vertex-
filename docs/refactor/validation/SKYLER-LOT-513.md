# SKYLER LOT 513 — La règle 507-A retournée contre mon propre dossier d'hier. **512-A survit : la phrase est non vide 100 % du temps.** Mais à l'échelle de production, elle annonce **« Top 0 % de l'univers »** au meilleur titre du scan — la correction que je proposais aurait livré une absurdité

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-513` (base : lot 512 fusionné,
`b466694a`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(c)**. Le 512 a publié un dossier de rang 4 et proposé, en correction
pressentie, d'afficher `context.headline` sur la fiche d'un titre. Or ma propre
règle **507-A** dit : *un défaut théorique n'est pas un dossier — mesurer
l'ATTEIGNABILITÉ avant de classer.* Un dossier publié la veille mérite d'être
borné avant d'en ouvrir un autre. Je l'ai donc retourné contre moi.

## Premier résultat : 512-A tient, et il tient mieux que publié

`_headline` peut rendre `None` — la partie « univers » exige un `score`
numérique, la partie « secteur » exige `sector` non vide **et ≥ 2 pairs**, et
`' · '.join(parts) or None` rend `None` si les deux manquent. Mesuré sur les
20 titres du scan DÉMO :

```text
titres scannés                          20
phrase NON VIDE                         20   (100 %)
   dont DEUX parties (univers+secteur)  10
   dont univers seulement               10
phrase VIDE                              0
19 phrases DISTINCTES pour 20 titres  → pas une tautologie (règle 496)
```

**Aucune phrase vide.** La partie secteur manque une fois sur deux, mais
uniquement parce que le scan DÉMO éparpille 20 titres sur 10 secteurs — mesuré à
n = 50 et au-delà, elle est présente **100 %** du temps. Mon 50 % est une
**borne basse**, pas un plafond.

## Second contrôle (règle 481) — et il change tout

Ma mesure porte sur **20** titres. `terminal.py:368` :
`syms_scan = UNIVERSE[:20] if DEMO_MODE else UNIVERSE`, et
`vertex/data/universe.py:161` donne **517** titres. **Mon banc mesure un univers
26 fois plus petit que la production.**

`_pct_rank` est un mid-rank : `pct = round((inférieurs + 0,5 × égaux) / n × 100)`.
Pour le meilleur titre, `pct = round(100 − 50k/n)` où *k* est le nombre d'ex
aequo au sommet. Quand `50k/n < 0,5`, l'arrondi rend **100**, et
`'Top %d%%' % (100 - pct)` écrit **« Top 0 % »**.

```text
     n   meilleur titre                dernier titre
     3   Top 17% de l'univers          Bas 17% de l'univers
    10   Top 5%                        Bas 5%
    20   Top 2%   ← ce que le 512 a cité             Bas 2%
    50   Top 1%                        Bas 1%
   100   Top 0%   ← BASCULE            Bas 0%
   517   Top 0%   ← LA PRODUCTION      Bas 0%
```

**Seuil exact : n = 100.** Au-delà, le meilleur titre de l'univers se voit
annoncer qu'il est dans le **« Top 0 % »**, et le pire dans le **« Bas 0 % »**.

## Troisième contrôle — il RÉFUTE partiellement le second, et je le publie

Mon second banc imposait des scores **tous distincts** (1000, 999, 998…). Les
vrais scores sont des **entiers** : mesurés sur le scan, 20 scores, **17 valeurs
distinctes**, type `int`. Avec des entiers sur 517 titres, les ex aequo montent,
`k` monte, et l'absurdité peut disparaître. Il fallait le vérifier.

```text
scores distincts (mon 2e banc)              sommet partagé par  1  → « Top 0% »
entiers 0-100 répartis uniformément         sommet partagé par  3  → « Top 0% »
multiples de 5                              sommet partagé par 13  → « Top 1% »
distribution du scan DÉMO étirée à 517      sommet partagé par 25  → « Top 2% »
```

**Le « Top 0 % » n'est donc PAS systématique.** Il dépend de *k*. La condition
exacte, vérifiée point par point à n = 517 :

```text
k au sommet   1   2   3   4   5  |  6   7  10  20  30
phrase      Top 0% ............. | Top 1% ... Top 2% Top 3%
                    k ≤ 5 (= n/100)          k ≥ 6
```

Et je dois aussi dire que **ma « distribution réelle étirée » est elle-même un
artefact** : étirer 20 valeurs sur 517 fentes multiplie chaque ex aequo par 26.
Ce n'est pas un modèle de scan à 517 titres, c'est mon rééchantillonnage. Le
chiffre honnête est celui de la condition, pas celui de ce tirage.

**Ce que je peux affirmer** : dans le scan DÉMO réel, le score maximum (84) est
**unique** — `k = 1`. Un sommet unique est le cas ordinaire. À 517 titres,
`k = 1` donne **« Top 0 % de l'univers »**.

**Ce que je ne peux pas affirmer** : que la production a bien `k ≤ 5`. Il
faudrait un scan réel de 517 titres, donc du réseau, que je n'ai pas le droit
d'appeler. **Le défaut est conditionnel, sa condition est nommée, et elle est
très probablement remplie.**

**Arrêtés avant publication : 103 → 105.** Deux : (1) j'allais publier
« l'absurdité est systématique en production » alors qu'elle dépend des ex
aequo ; (2) ma première vérification de la condition était **fausse** —
`range(0, n-k)` fabriquait des valeurs supérieures à 100, donc « le maximum »
n'en était pas un, et le banc rendait `Bas 20%` pour tous les *k*. Refaite
proprement, elle donne le tableau ci-dessus.

## Ce que cela fait au dossier 512-A

Le 512 concluait : *« Correction pressentie : afficher `context.headline` sur la
fiche d'un titre. »* Le 513 dit : **pas en l'état.** Brancher la phrase telle
quelle livrerait, au meilleur titre du scan, la mention « Top 0 % de l'univers ».
Ce serait une violation directe de l'invariant **« données RÉELLES uniquement,
jamais de chiffre inventé affiché comme réel »** — non parce que le nombre est
faux au sens strict (le percentile *est* ~99,9), mais parce que la **formulation**
`100 − round(pct)` détruit l'information au moment de l'écrire.

C'est le résultat le plus utile du lot : **le 512 avait raison sur le fond et
tort sur la marche à suivre.**

## Classement — rang 4, et je dis pourquoi pas plus haut

Rien de faux n'est montré **aujourd'hui** : la phrase n'atteint aucun écran
(c'est 512-A) et le seul environnement que je peux exécuter (DÉMO, n = 20) rend
« Top 2 % », qui est sensé. **Le défaut est invisible dans tous les
environnements où je peux le faire tourner** — c'est précisément pour cela qu'il
reste au rang 4.

Mais il est d'une autre nature que son parent : le jour où la phrase est
affichée, il devient **un chiffre faux peint à l'écran**, soit un rang 2. C'est
un dossier **conditionné à sa propre correction**, cas nouveau dans la feuille.

Correction pressentie, non engagée : borner la formulation (« Top 1 % » comme
plancher, ou passer à l'ordinal « 1ᵉʳ sur 517 » qui ne perd rien). **Aucun GO,
rien n'est engagé, rien n'est supprimé.**

## Portée — ce que ce lot NE dit PAS

- **Je n'ai pas fait tourner un scan de production.** Tout ce qui concerne
  n = 517 est obtenu en appelant `context.context_for` (liste sûre, en
  processus) sur des cartes **fabriquées en mémoire**. Aucun réseau.
- **La condition `k ≤ 5` n'est pas vérifiée sur données réelles à 517 titres.**
  Elle l'est sur le scan DÉMO à 20 titres, où `k = 1`.
- Le défaut d'arrondi ne touche **que la phrase**. `_standing` (leader / fort /
  médian / faible / retardataire) utilise le même percentile et reste **correct**
  à toutes les tailles — le dépôt fait bien à côté, et je le dis (règle 509-C).
- Les `dimensions[].pct_universe` et `pct_sector` sérialisés ne sont **pas**
  affectés : ce sont les percentiles bruts, justes. Seul le `100 - pct` de
  `_headline` détruit l'information.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les trois bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4**. Trois rangs 4
d'affilée — mais celui-ci n'est pas un troisième constat d'inutilité : c'est le
premier lot de la veine qui **corrige la correction proposée par le lot
précédent**. Le 512 disait « il ne manque qu'un consommateur » ; le 513 mesure
qu'il manque aussi une **formulation**.

C'est aussi la quatrième fois que le troisième contrôle réfute mon second, et la
deuxième fois en deux lots que je publie l'écart plutôt que le seul chiffre
final. La discipline paie : sans lui je publiais « absurdité systématique »,
faux.

Feuille : **34 dossiers · seize rang 1 · onze rang 2 · cinq rang 3 · trois
rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **mesurer le
contenu des 23 routes non appelées** ; **la condition `k ≤ 5` sur un scan réel de
517 titres** (dette neuve — exige du réseau, donc un GO humain) ; **un producteur
de synthèse d'une autre forme** ; **l'espion au troisième niveau** ; **le compte
des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 105 (+2)** ; publiés
puis corrigés **13** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
