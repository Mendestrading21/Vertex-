# SKYLER LOT 529 — Retour au produit. Sur les quatre chiffres qui portent des dossiers de rang 4 : **deux confirmés, un juste avec un mot faux — « 21 621 octets » sont des CARACTÈRES — et un non reproductible**. Et j'ai failli réfuter 512-A sur huit homonymes

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-529` (base : lot 528 fusionné,
`7345d1b3`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix, et pourquoi je change d'axe

**(k)** — vérifier sur le **code réel** les quatre chiffres porteurs de rang 4
que le relevé du 527 signalait comme non vérifiés.

Quatre lots d'affilée (525 → 528) ont mesuré **ma comptabilité** plutôt que
Vertex. Chacun a trouvé du vrai, et chacun cédait moins loin que le précédent —
mais **la suite de ce travail demande une décision humaine que je n'ai pas**, et
**l'utilisateur ne lit pas mes compteurs**. Insister serait tourner en rond.

```text
CALIB 1 · POSITIF   deux lectures indépendantes de la taille de
                    `options_intel_page.py` coïncident (21 808 = 21 808)   OK
CALIB 2 · NÉGATIF   un chiffre FABRIQUÉ (999 lignes) ne coïncide pas       OK
```

## 513-A — **CONFIRMÉ, au chiffre près**

```text
univers scanné en DÉMO            n = 20        publié : 20        JUSTE
symboles portant « Top X % »      10
valeur MINIMALE observée          Top 2 %       publié : 2 %       JUSTE
   (c'est ACN ; A rend « Top 43 % », ADBE « Top 48 % »…)
```

**C'est le seul des cinq dossiers de rang 4 dont la définition était ÉCRITE dans
son rapport** — environnement et taille d'univers cités. **C'est aussi le seul
qui se vérifie exactement.** L'argument de la règle **525-A** ne pouvait pas être
mieux illustré.

## 512-A — **CONFIRMÉ**, après un piège que j'ai failli publier

`context.headline` est bien **produite** :

```text
context_for('A')['headline'] = « Top 43% de l'univers · #1/3 dans Healthcare »
```

Et la recherche dans les octets servis rend **8 occurrences de « headline »**.
**J'ai un instant cru le dossier réfuté.**

Les huit, vérifiées **une par une** :

```text
/options   options-gex.js   `s.headline` — la charge d'un scénario GEX
/system    ×7               `_headline`, variable LOCALE de la carte d'état
                            + `n.headline`, le titre d'une NOUVELLE
```

**Aucune n'est `context.headline`.** Huit homonymes — exactement la famille
**521-B / 528-A**. **Le dossier tient : la phrase est calculée et n'atteint
toujours aucun écran.**

**Arrêtés avant publication : 132 → 133.**

## 519-A — le chiffre est juste, **le mot est faux**

```text
lignes    publié 358        mesuré 358        JUSTE
octets    publié 21 621     mesuré 21 808     ÉCART +187
vues héritées, relues par AST : 3 (overview, radar, scenarios)   JUSTE
```

Le fichier **n'a pas changé** depuis le lot 296 — bien avant le 519. L'écart
n'est donc pas une dérive. La cause, trouvée :

```text
len(texte)  = 21 621   ← ce que le 519 a compté
len(octets) = 21 808   ← ce qu'il a écrit
```

**Le 519 comptait des CARACTÈRES et les a appelés « octets ».** Les 187 de
différence sont les accents français, encodés sur deux octets en UTF-8.

**Le chiffre est exact ; le mot ne l'est pas.** Le dossier est intact ; sa
formulation doit dire « caractères ».

**Publiés puis corrigés : 19 → 20.**

## 511-A — **non reproductible**

Le 511 publiait « **103** routes de données, **62** citées, **41** jamais, soit
**39,8 %** ». Sa définition — « routes de données exposées en GET (`app.url_map`,
hors `/static`) » — a été appliquée sous **quatre lectures plausibles** :

```text
prédicat                       total   jamais citées   part
toutes GET hors /static          173         89        51,4 %
idem, hors les 9 pages           164         88        53,7 %
/api + les feeds                 102         45        44,1 %
/api seul                         99         43        43,4 %
                                 ────
publié au 511                    103         41        39,8 %
```

**Aucun des quatre ne rend 103.** Le corpus du 511 n'est pas retrouvable depuis
ce qui est écrit — **511-A rejoint 518-A : un dossier de rang 4 dont le chiffre
n'est pas recomptable** (**525-A**).

**Mais la conclusion, elle, tient et se trouve même RENFORCÉE** : sous les quatre
prédicats, la part jamais citée va de **43 % à 54 %**, toutes **au-dessus** des
39,8 % publiés. **Le dossier n'était pas gonflé — il était prudent.**

## Le tableau, après vérification

| dossier | chiffre porteur | verdict |
|---|---|---|
| **513-A** | « Top 2 % », DÉMO n = 20 | **CONFIRMÉ au chiffre près** — définition écrite |
| **512-A** | phrase calculée, jamais consommée | **CONFIRMÉ** — 8 homonymes écartés |
| **519-A** | 3 vues · 358 lignes · 21 621 « octets » | **JUSTE, mot faux** : ce sont des **caractères** |
| **511-A** | 41 / 103 · 39,8 % | **NON REPRODUCTIBLE** — conclusion renforcée (43–54 %) |
| **518-A** | 77 % | **ENCADRÉ** (57 %–94 %), établi au 525 |

**Deux dossiers sur cinq ont un chiffre exactement vérifiable. Les deux ont ceci
en commun : leur définition était écrite.**

## Ce que le dépôt fait bien, mesuré

- **`context.headline` produit une phrase correcte et informative** — « Top 43 %
  de l'univers · #1/3 dans Healthcare » : rang transversal **et** rang sectoriel,
  en français, sans chiffre inventé. **Ce n'est pas la phrase qui est en défaut,
  c'est l'absence de consommateur.**
- **Le 511 était prudent** : sa part réelle est plus élevée que celle qu'il a
  publiée, sous les quatre lectures.
- **Le 513 avait écrit sa définition**, et c'est exactement pour cela qu'il se
  vérifie deux lots plus tard sans discussion.

## Portée — ce que ce lot NE dit PAS

- **512-A est vérifié en DÉMO** et par une recherche **textuelle** : une
  consommation construite dynamiquement (`obj['head'+'line']`) échapperait.
- **511-A n'est pas tranché.** Quatre prédicats, quatre valeurs, aucun 103.
- **Aucune correction n'est engagée** — ni le mot « octets » du 519, ni la
  définition du 511. **Ce sont des constats.**
- Le lot ne touche **aucun dossier des rangs 1 à 3**.
- **Aucun navigateur, aucun POST, aucune route interdite** ; seules les 8 pages
  et leurs scripts ont été lus, et `terminal.scan()` en DÉMO.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier — et le retour au produit paye immédiatement : **deux dossiers
consolidés, un vocabulaire corrigé, un quatrième dont l'imprécision est
maintenant nommée**. Après quatre lots à mesurer mes comptes, celui-ci mesure le
**code**, et le code se tient mieux que ma prose : sur les quatre chiffres, **un
seul était vraiment imprécis, et sa conclusion était sous-estimée**.

Trois règles neuves :

- **529-A · UN CHIFFRE JUSTE PEUT PORTER UN MOT FAUX** — « 21 621 octets » est un
  compte de **caractères** ; l'écart de 187 est en accents.
- **529-B · UN DOSSIER DONT LA DÉFINITION EST ÉCRITE SE VÉRIFIE ; LES AUTRES SE
  DISCUTENT** — 513-A tombe juste au chiffre près, 511-A n'est pas reproductible.
- **529-C · CHERCHER UN NOM DANS LES OCTETS SERVIS TROUVE SES HOMONYMES** — huit
  occurrences, zéro pertinente ; vérifier chacune avant de conclure.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; **relevé strict 35 + 5
candidats ambigus** ; les cinq rangs 4 nommés, **deux désormais confirmés au
chiffre près (512-A, 513-A)**, un juste au mot près (519-A), deux non
recomptables en l'état (511-A, 518-A).

Dettes nommées restantes : **la définition du corpus de routes du 511-A** ;
**l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs
fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **les 17 chargeurs
muets** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en
attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 133 (+1)** ;
**publiés puis corrigés 20 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
