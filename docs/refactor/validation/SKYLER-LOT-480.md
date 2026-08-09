# SKYLER LOT 480 — L'audit des rangs relatifs : NEUF sur vingt-quatre, UN SEUL est affecté, et il n'est pas dans le plan — mais l'audit trouve autre chose : CINQ des vingt dossiers du plan portent un rang que leur propre rapport n'a JAMAIS déclaré

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-480` (base : lot 479 fusionné,
`ac61760`)

Le 479 a posé une question et a refusé d'y répondre à la légère :

> « Combien d'autres rangs de la veine ont été posés par comparaison à un dossier
> dont le rang a bougé depuis ? »

**Ce lot y répond. La réponse est UN, et ce n'est pas la trouvaille du lot.**

**Il ne corrige rien.** Aucun fichier de production touché.

## PORTÉE, posée d'emblée — ce lot ne mesure PAS le produit

**Aucune conclusion de ce lot ne porte sur Vertex.** Toutes portent sur **mes
propres rapports**. C'est légitime — le 470, les 471-475 et le 479 l'ont déjà
fait — mais cela doit être dit avant les chiffres, pas après.

---

# LA CALIBRATION, POSÉE AVANT LA PREMIÈRE MESURE

**Un RANG RELATIF est un classement justifié par comparaison à un autre dossier.**
Trois conditions, **toutes écrites dans le code du détecteur** (leçon 463) :

```text
(a) le rapport déclare un rang PROPRE — dans une section « Classement »,
    le rang du TITRE s'il y est, sinon le premier **Rang N** en gras
(b) dans la ZONE DE JUSTIFICATION (titre + corps de cette section)
(c) une MÊME PHRASE contient un marqueur COMPARATIF *et* une référence
    à un AUTRE numéro de lot

EXCLU EXPLICITEMENT : citer un autre lot pour un FAIT (un site, une mesure,
une méthode) sans marqueur comparatif — ce n'est pas un rang relatif.
```

**Contrôle, choisi d'avance sur un cas connu** : le détecteur **doit** trouver le
416, dont le 479 a établi qu'il se compare au 407. → **CONTRÔLE PASSÉ.**

---

# LA POPULATION — et deux défauts d'instrument attrapés EN LISANT

```text
rapports SKYLER-LOT-*                                    482
rapports déclarant au moins un « rang »                   81
déclarations de rang, toutes occurrences                 371   ← BAVARDAGE
```

**371 pour 81 rapports : l'instrument comptait les rangs CITÉS, pas les rangs
POSÉS.** Les bilans et les devis énumèrent les rangs des autres. C'est la
leçon 462 : *le signal du bavardage, c'est la taille de la population*.

Restriction **structurelle** aux sections « Classement » : **35**. Et la lecture
de ces 35 a montré **deux défauts de plus** :

```text
défaut 1   « Classement coût/risque » (430, 450, 460, 470) est LE TABLEAU DU PLAN,
           pas le rang d'un dossier. SEIZIÈME récurrence du piège des homonymes :
           le mot « Classement » désigne DEUX choses dans ce dépôt.
défaut 2   mon regex prenait le PREMIER rang trouvé — donc « pourquoi pas rang 1 »
           l'emportait sur le verdict réel. Les 477 et 478 étaient lus « rang 1 »
           alors qu'ils sont rang 2.
```

Corrigé : **VINGT-QUATRE rangs propres.**

```text
rang 1  14   416 417 422 425 427 428 432 433 434 437 447 457 464 476
rang 2   6   418 424 458 461 477 478
rang 3   2   436 469
rang 4   2   446 454
```

---

# LA RÉPONSE — NEUF RANGS RELATIFS, UN SEUL AFFECTÉ

## Les neuf, et leur étalon

```text
lot   rang   étalon(s)          la phrase, en propre
416    1     407                « nettement moins grave que le 407 »
418    2     416, 417           « moins grave que le 416 et le 417 »
422    1     417 (et PAS 407)   titre : « Classement — famille du 417, pas du 407 »
425    1     422                « famille du 422 »
427    1     422, 425           « famille des 422 et 425 »
428    1     422, 425, 427      « famille des 422/425/427 »
432    1     422, 425, 428      « famille des 422/425/428 »
434    1     432, 433           « famille des 432/433 »
476    1     447                « la même famille que le 447 … classé rang 1 lui aussi »
```

**Neuf sur vingt-quatre — 37,5 % des rangs de la veine sont justifiés par
comparaison.** Et ils forment une **chaîne** : 434 → 432 → 428 → 427 → 425 → 422
→ 417. Sept dossiers suspendus à un seul étalon d'origine.

## Les mouvements de rang, mesurés — et le réveil se trompe une QUATRIÈME fois

Détecteur indépendant sur les 482 rapports, cherchant les phrases qui
**reclassent un autre dossier** :

```text
459 → 456   « Requalification : rang 4 "par lecture" → RANG 2, établi par exécution »   ↑ HAUSSE
478 → 407   le dossier fusionné 406+407 classé RANG 2                                    ↓ BAISSE
479 → 416   rang 1 → rang 3                                                              ↓ BAISSE
```

**Mon réveil listait « 407, 416, 469, 465, 462 ».** Mesuré : **469, 465 et 462 ne
sont pas des mouvements de rang** (le 469 réfute une insinuation, les 465 et 462
sont des bornages qui n'ont rien classé), **et la requalification 459 → 456
manquait**. **Quatrième compte de réveil faux** (après 470, 473, 479).

**Compte : arrêté avant publication, 45 → 46.**

## Le croisement — et il rend UN seul cas

```text
étalon qui a bougé   qui s'y compare      verdict
   407               416                  DÉJÀ RÉSOLU au 479 (rang 1 → rang 3)
   416               418                  ← LE SEUL AUTRE CAS
   456               personne             aucun rang relatif ne s'y compare
```

Les sept autres (422, 425, 427, 428, 432, 434, 476) se comparent à **417, 422,
425, 427, 428, 432, 433 et 447** — **aucun de ces étalons n'a bougé**.

## Le cas unique — le 418, et il produit une INVERSION

Le 418 est **rang 2**, justifié par « moins grave que le 416 et le 417 ». Le 417
est resté rang 1 ; **le 416 est passé à rang 3**.

**Le 418 est donc désormais classé PLUS GRAVE que l'un des deux dossiers dont il
se déclarait strictement moins grave.** Son ordonnancement interne est
contradictoire.

**Mais je ne le reclasse pas, et je dis pourquoi** : le 418 **n'est pas dans les
vingt dossiers du plan**. Le reclasser demanderait de rouvrir sa mesure, ce qui
est un lot en soi, et **cela ne changerait rien à la feuille de décision**. Je le
**nomme comme incohérence ouverte** et je le laisse.

## LE BORNAGE — c'est le résultat principal, et il est rassurant

**Sur neuf rangs relatifs, un seul est affecté, et il est hors plan. La feuille
de décision ne change pas.**

C'est un résultat que j'aurais préféré plus spectaculaire, et c'est précisément
pour cela qu'il faut le publier tel quel. **La question du 479 était bonne ; sa
réponse est « presque personne ».**

Une raison mesurée à cette robustesse : **le 422 s'est explicitement DISSOCIÉ de
son étalon voisin** — son titre dit « famille du 417, **pas du 407** ». Il a
anticipé exactement le problème que le 479 a découvert cinquante-sept lots plus
tard. **Toute la chaîne de sept dossiers pend au 417, pas au 407, à cause de
cette seule précision.**

---

# CE QUE L'AUDIT TROUVE ET QU'IL NE CHERCHAIT PAS

En vérifiant quels dossiers du plan portent un rang propre :

```text
LES 20 DOSSIERS DU PLAN — leur rapport déclare-t-il un rang ?
   déclarent un rang         15
   AUCUNE section Classement  5   →  378 · 406 · 455 · 456 · 463
```

**Cinq des vingt dossiers du plan portent un rang que leur propre rapport n'a
jamais déclaré.** Leur classement vient **uniquement du tableau coût/risque** des
bilans — c'est-à-dire de moi, en aval, sans que le rapport d'origine ait posé ni
justifié le rang.

Et **le 407 est dans le même cas** : c'est **l'étalon du 416**, il portait
« rang 1 » dans le tableau du plan, et **son rapport ne déclare aucun rang**. La
transitivité du 479 reste valide — elle portait sur le rang **du plan** — mais
elle reposait sur un rang **jamais justifié dans un rapport**.

**C'est plus grave que la question posée par le 479**, et cela ne se voyait pas
sans cet audit : la boucle a des rangs **orphelins de justification**.

---

# LA RÈGLE — posée parce que la mesure la porte

```text
UN RANG DOIT PORTER AU MOINS UN CRITÈRE ABSOLU.
La comparaison à un autre dossier est un ARGUMENT D'APPOINT, jamais le seul.
Et un rang inscrit dans le tableau du plan sans être déclaré dans un rapport
est un rang SANS JUSTIFICATION — il doit être marqué comme tel.
```

Les 477, 478 et 479 la respectaient déjà sans la nommer : chacun a écrit
« pourquoi pas rang N » avec des **critères propres** (sens de l'erreur, chemin
d'exception, écrivabilité de la clé), la comparaison venant **en plus**. Les 425,
427, 428 et 432 ne la respectent pas : « famille des 422/425/427 » **est** leur
justification.

---

# L'AUTRE QUESTION DU 479 — « instrument qui se calibre, ou juge qui se fatigue ? »

Le 479 a observé que **les deux derniers lots ont réduit un dossier**, après vingt
lots où la mesure aggravait. Les données mesurées ici tranchent — pas dans le
sens d'une dérive :

```text
révisions du rang d'un AUTRE dossier, sur 482 rapports :  TROIS
   459 → 456   HAUSSE (rang 4 → rang 2)
   478 → 407   BAISSE
   479 → 416   BAISSE
```

**Deux baisses, une hausse.** Et surtout, **les trois ont eu lieu dans des lots
dont le travail était la RÉ-EXAMINATION d'un dossier ancien** — le 459
requalifiait le 456, le 478 rouvrait 406+407, le 479 rouvrait le 416.

**La réponse est donc : ni l'un ni l'autre — c'est un changement de TÂCHE.** Un
lot qui classe une trouvaille fraîche ne révise rien par construction ; un lot
qui rouvre un dossier ancien révise dans les deux sens. Les baisses se sont
groupées aux 478-479 parce que **la reprise de mesure a commencé au 476**, pas
parce que le juge s'émousse.

**Ce que je ne peux pas exclure**, et je le dis : trois révisions sont un
échantillon trop petit pour distinguer « pas de biais » de « biais faible ». **Ce
que la mesure exclut, c'est l'explication par la fatigue** ; elle ne prouve pas
l'absence totale de dérive.

---

# CE QUE LE LOT NE PRÉTEND PAS

- **Le détecteur de mouvements est une heuristique de phrases.** Il a trouvé la
  requalification du 459 que j'ignorais, mais **il n'a PAS trouvé le 478** — dont
  le reclassement du 407 est formulé sans aucun de ses marqueurs. **Je connais ce
  mouvement par mon propre lot, pas par l'instrument.** Il peut donc en manquer
  d'autres, et **je ne publie pas « trois mouvements » comme un total exhaustif**
  mais comme **trois mouvements connus, dont un que l'instrument aurait raté**.
- **Je n'ai pas rouvert le 418.** Son incohérence est **nommée**, pas résolue.
- **Je n'ai pas rouvert les cinq dossiers sans rang propre.** Leur situation est
  **mesurée**, pas corrigée.
- Le seuil « même phrase » du critère (c) est un **choix** : une justification
  comparative étalée sur deux phrases échapperait au détecteur. **Je n'ai pas
  mesuré combien de cas cela peut représenter.**
- **Aucune conclusion ne porte sur Vertex.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Lecture de fichiers Markdown uniquement ; pages en **GET** pour les MD5 ;
  `persist` redirigé vers un `mkdtemp` **et la redirection vérifiée par
  `cache_path()`** ; **aucun moteur appelé** ; **`/api/portfolio/team`,
  `/options/<sym>`, `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON
  appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## La feuille de décision — INCHANGÉE

**20 dossiers · 55 à 63 lignes · 20 gardiens · douze rang 1 · sept rang 2 · un
rang 3.** Les dix lots A à J sont **inchangés**. **C'est le résultat de l'audit,
pas son absence.**

**Deux dettes ouvertes, nommées et non traitées** : l'incohérence du **418**
(hors plan), et les **cinq dossiers du plan sans rang propre** (378, 406, 455,
456, 463) — plus le **407**, étalon du 416, dans le même cas.

## Où en est la boucle

Quatre-vingt-deuxième lot court.

Le lot répond à sa question et la réponse est **modeste** : un seul rang relatif
affecté, hors plan, feuille inchangée. Un audit qui ne trouve presque rien est un
audit qui a fait son travail — et le 462 avait déjà posé qu'**un bornage est un
résultat**.

Mais il trouve **autre chose**, et c'est le vrai apport : **cinq dossiers du plan,
plus l'étalon du 416, portent un rang que personne n'a jamais justifié dans un
rapport.** Le classement du plan s'est constitué **en aval**, dans les tableaux
des bilans, et il a fini par servir de référence à des raisonnements de
transitivité — dont le mien, au 479.

Le fait de méthode :

**UNE MESURE FAITE POUR RÉPONDRE À UNE QUESTION TROUVE SOUVENT AILLEURS QUE LÀ OÙ
ELLE CHERCHE.** La question portait sur les rangs **relatifs** ; la trouvaille
porte sur les rangs **orphelins**. Il fallait construire l'instrument pour la
première pour rencontrer la seconde.

Et un détail qui rachète une pratique ancienne : **le 422 a écrit « famille du
417, PAS du 407 » — et cette dissociation, faite cinquante-sept lots plus tôt,
est ce qui empêche aujourd'hui une chaîne de sept dossiers de vaciller.** La
précision inutile d'hier est la robustesse d'aujourd'hui.

Comptes séparés : résultats faux **arrêtés avant publication** **46** (+1, la
liste de mouvements du réveil) ; **publiés puis corrigés** **7** ;
**interprétations retirées** **3** ; re-localisation **0** ; **incohérences de
rang ouvertes : 1** (le 418) ; **rangs sans justification : 6** (378, 406, 407,
455, 456, 463).

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre vingt
dossiers, douze de rang 1, pour 55 à 63 lignes, et il est INCHANGÉ par cet
audit.**
