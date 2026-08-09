# SKYLER LOT 441 — La page d'analyse que la boucle n'avait jamais servie : `/analysis/<sym>` fait 75 829 octets, porte 20 graphiques et 12 routes — et aucun des zéros publiés ne bouge

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-441` (base : lot 440 fusionné,
366be7b)

Vingt-troisième lot de la veine, **premier de la tranche 440-449**. Le 439 avait
laissé `/analysis` en **piste, pas en constat** — « non ouverte avec un symbole ».
Ce lot l'ouvre.

**Aucun code, aucun gardien, aucun test.**

## `/analysis` n'est pas une page d'analyse : c'est un lanceur

```text
                        octets     VXCharts   vx-card   routes /api   data-open-analysis
/analysis  (index)      22 359            0        17             1                    3
/analysis/AAPL          75 829           20        77            12                    1
```

L'index cite **une seule** route (`/api/names`) et porte **trois** boutons
d'ouverture ; la page à symbole en cite **douze** :

```text
/api/analyst/   /api/anomalies/   /api/copilot/ask   /api/decision/
/api/evidence/  /api/options-for/ /api/planning/ticket /api/pretrade/check
/api/skyler/    /api/strategy/decision/  /api/ticker/  /api/tradingview/signals
```

**La piste du 439 est refermée, et dans le sens négatif** : `/analysis` n'est pas
une exception dans les huit pages, c'est un **écran de saisie** dont le contenu
vit à `/analysis/<sym>`. La phrase du 439 — « au chargement elle ne porte ni
moteur de graphique ni contrat d'explication » — reste **exacte pour l'index**, et
elle ne dit rien de la page que le trader lit vraiment.

`render(sym)` (`analysis_page.py:954-966`) est un **pur assembleur de chaînes** :
aucun moteur, aucun appel réseau. Mesuré : `/analysis/AAPL` et `/analysis/MSFT`
font **exactement la même taille**. Tout le contenu est hydraté côté client.

## Le corpus des 95 objets était incomplet — bornage de l'écart

Les mesures de la boucle depuis le 427 portent sur un corpus de **95 objets,
3 829 722 octets** : 8 pages, 44 vues `?view=`, 43 fichiers `/static`. **Aucune
route à paramètre n'y figurait.** Il y en a sept :

```text
/analysis/<sym>       200    75 829 o   ← la page manquante
/company/<sym>        301       215 o   → redirige vers /analysis/<sym>
/titre/<sym>          301       215 o   → redirige vers /analysis/<sym>
/desc/<sym>           200       495 o   fragment
/options/<sym>        200       301 o   fragment
/memory/<id>          404    16 679 o
/memory/cell/<g>/<k>  404    16 725 o
```

**L'écart tient donc à une seule vraie page**, `/analysis/<sym>` — **+2 % du
corpus**, mais c'est l'écran où se prend la décision par titre.

### Est-ce que cela invalide un zéro déjà publié ? Non — vérifié, pas supposé

```text
435 « ATTENDRE / SÉLECTIF »        dans /analysis/AAPL :  0
435 « ATTAQUER »                                       :  0
435 « RÉDUIRE / DÉFENSIF »                             :  0
435 « Peu d'avantage statistique »                     :  0
436 /api/command appelé depuis cette page              :  0
```

**Aucun des zéros publiés ne bouge.**

Un piège évité au passage : le motif `.decision` rend **8 occurrences** sur cette
page. Ce n'est **pas** le champ `decision` de `/api/command` — cette page n'appelle
jamais `/api/command` ; ce sont les payloads de `/api/decision/` et
`/api/strategy/decision/`. *Un nom d'identifiant peut désigner plusieurs
payloads* (leçon 438) : la règle a servi, cette fois avant la faute.

## Une trouvaille qui n'en était pas — et le quinzième instrument

Le recensement d'affirmations a rendu, sur `/analysis/AAPL` :
`question` · `shows` · `why` · `confirm` — **et pas d'`invalidate`**. Sur une page
dont le sous-titre est « Cette entreprise et cette opportunité méritent-elles du
capital maintenant ? », une carte qui liste ce qui **confirmerait** sans dire ce
qui **invaliderait**, c'était une trouvaille toute faite. Le `why` de la même carte
dit même : « l'invalidation est définie AVANT d'engager du capital ».

**C'est faux.** `analysis_page.py:414` :

```javascript
invalidate:`Clôture sous le stop ${VX.fmt.nd(plan.stop)} — la thèse est invalidée, pas « en retard ».`
```

Le champ est là. Il est écrit en **littéral gabarit** (accents graves), et mon
motif ne connaissait que les **guillemets simples** — la limite que le 439
déclarait sans la chiffrer. **Quinzième instrument arrêté avant publication**,
par le contrôle « lire la source brute ».

## La zone d'ombre, enfin chiffrée : 3,2 %

Recensement refait sur les **trois** formes de littéral, HTML de page :

```text
page               simples   doubles   gabarits   TOTAL   manqué par l'instrument 427-439
/                        1         0          0       1     0
/markets                37         0          0      37     0
/opportunities          16         0          2      18    +2
/analysis                0         0          0       0     0
/portfolio              18         0          0      18     0
/options                 0         0          0       0     0
/journal                 8         0          0       8     0
/system                  6         0          0       6     0
/analysis/AAPL           4         0          1       5    +1
                        ──        ──         ──      ──
                        90         0          3      93    +3  →  3,2 %
```

**Témoin positif** : `/journal` rend **8**, exactement le chiffre du 439.
L'instrument mord là où il doit.

La zone d'ombre annoncée depuis le 427 est donc **réelle et petite**. Mais les
trois rattrapées sont précisément celles qui **interpolent une donnée vivante** :

```text
/opportunities  conclusion  Breakeven ${VX.fmt.nd(c.be)} · prime ${VX.fmt.nd(c.cost)}
/opportunities  conclusion  R:R simulé ${VX.fmt.nd(s.sim.reward_risk)} · perte planifiée ${…} %
/analysis/AAPL  invalidate  Clôture sous le stop ${VX.fmt.nd(plan.stop)} — …
```

La deuxième est **le dossier 422** (le R:R dont le mouvement attendu est fabriqué
par le moteur). Autrement dit : **la classe d'affirmations la plus exposée était
la seule que l'instrument ne voyait pas** — 3,2 % en nombre, mais pas 3,2 % en
risque.

## Un chiffre publié au 439, corrigé

Le 439 annonce « **22 248 octets** » pour `/analysis`. Mesuré ici :
**22 359 octets**, md5 `113827718e99` — l'empreinte de référence, donc la page n'a
pas changé. **22 248 est le nombre de CARACTÈRES**, pas d'octets : la différence
est faite par les accents en UTF-8.

Mécanisme confirmé sur l'autre page : `/analysis/AAPL` fait **75 829 octets** pour
**75 216 caractères**. C'est une **unité mal étiquetée**, deuxième récidive après
le « quatorze » du 440 — et, comme lui, sans conséquence sur une conclusion.

## Classement

**Aucun défaut de produit nouveau.** Le lot rend quatre résultats :

1. la piste `/analysis` du 439 est **refermée négativement** — l'index est un
   lanceur, pas une exception ;
2. le corpus de la boucle était **incomplet d'une page servie de 75 829 octets**,
   et **aucun zéro publié n'en est affecté** — vérifié route par route ;
3. la zone d'ombre du recensement vaut **3,2 %**, et elle est **biaisée vers les
   phrases à donnée interpolée** ;
4. un chiffre du 439 est **corrigé** (caractères comptés comme octets).

Rien à ajouter aux dossiers, rien à retirer.

## Portée

Le recensement ne porte que sur le **HTML de page** : les 35 affirmations que le
439 a comptées dans le JS de `/options` servi depuis `/static` **ne sont pas dans
les 93**, et restent **recensées, non vérifiées**.

Je n'ai **ouvert aucune** des cinq affirmations de `/analysis/<sym>` : elles sont
recensées, pas vérifiées. Et la page étant **hydratée côté client**, ce qui
s'affiche réellement dépend de douze routes que je n'ai pas appelées — la mesure
porte sur le **squelette servi**, pas sur un écran peuplé.

`/options/<sym>` a déclenché un appel réseau sortant (échoué derrière le proxy) ;
je le classe **fragment** sur sa taille servie, sans conclure sur son contenu.

Aucun navigateur ouvert.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad — l'incident du 435 s'est reproduit
  une fois (module `vertex` introuvable depuis le scratchpad) et a été corrigé
  sur-le-champ.
- **MD5 des 8 pages** : `/analysis` remesurée à `113827718e99`, identique à la
  référence — la page corrigée en taille n'a pas changé d'un octet.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Toutes les routes appelées en **GET** (lecture) ;
  `persist` redirigé vers un répertoire temporaire.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

### Un témoin positif involontaire

Le premier passage de la suite a été lancé **avant** l'insertion de la ligne
d'index, et `tests/test_skyler_index_integrity_lot228.py::test_tout_rapport_du_perimetre_a_sa_ligne_d_index`
a **échoué** — exactement ce qu'il promet. Suite relancée après les trois
documents : **2864 passed**. C'est un **témoin positif accidentel** sur ce
gardien : il mord réellement quand un rapport arrive sans sa ligne d'index, ce
qu'aucun lot n'avait vérifié.

## Où en est la boucle

Quarante-quatrième lot court, premier de la tranche.

Le 440 venait de conclure que la méthode se durcit ; ce lot le vérifie dans les
deux sens. Il **referme** une piste au lieu de la gonfler, il **corrige** un
chiffre du lot précédent, et il **arrête un quinzième résultat faux** — compté
dans la convention arrêtée au 440 — avant qu'il n'entre dans un rapport.

Et il déplace une frontière : depuis le 427, tout ce que la boucle affirme sur
« les octets servis » se disait d'un corpus qui **oubliait une page**. Cette page
est maintenant mesurée, et elle ne renverse rien.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
