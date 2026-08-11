# SKYLER LOT 503 — La dette des huit rangs relatifs payée : aucun ne tient SEUL par comparaison. Mais en la payant je trouve mieux — le « NEUF sur vingt-quatre » du 480 est FAUX, il y en a QUINZE, et son lexique en avait raté six. Sa conclusion, elle, survit au recomptage

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-503` (base : lot 502 fusionné,
`0cb66c41`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé.**

## Le choix

**(a)**, les **huit rangs relatifs jamais re-vérifiés**. C'était la plus ancienne
dette de fond encore ouverte — nommée au **481**, reportée depuis — et surtout
la seule où le **bilan n°18 a publié une affirmation non mesurée** : « le stock
vieillit bien ». Vérifier ces huit rangs, c'est contrôler mes propres
conclusions publiées plutôt que d'en produire de nouvelles.

## La réponse, en deux temps

```text
LA QUESTION POSÉE AU 481
  les huit rangs « famille du 4xx » tiennent-ils SEULS par la comparaison ?
  → NON. 15 / 15 portent un critère ABSOLU dans la même section.  Zéro exception.

CE QUE LA MESURE A TROUVÉ EN PLUS — et que je ne cherchais pas
  rangs relatifs publiés par le 480      NEUF      37,5 % des 24
  rangs relatifs mesurés ici             QUINZE    62,5 % des 24
  ajoutés  417 · 424 · 433 · 454 · 461 · 464       (six)
  perdus                                 AUCUN     (sur-ensemble strict)

LE BORNAGE DU 480, RE-CROISÉ SUR LES QUINZE
  « un seul rang relatif affecté, hors plan, la feuille ne change pas »
  → CONFIRMÉ. Le recomptage n'ajoute aucun cas affecté.
```

Le 480 s'est trompé sur le **compte** et avait raison sur la **conclusion**.

## Pourquoi le « neuf » était faux — deux défauts, tous deux DANS MON CAMP

Mon premier détecteur a reproduit le neuf du 480 à l'identique. **C'est
exactement ce qui aurait dû m'alerter** : deux instruments écrits à trois lots
d'écart qui tombent sur la même liste peuvent partager la même erreur. Un second
banc, écrit pour contrôler ce que le premier EXCLUT (règle 481), a rendu **dix**.
L'écart d'UN entre mes deux propres bancs est ce qui a ouvert le dossier.

### Défaut 1 — un marqueur coupé par un retour à la ligne

Je découpais en phrases **avant** de rejoindre les lignes markdown. Le rapport
433 écrit :

```text
Ici la conséquence est plus
lourde qu'au 432
```

`plus lourd` ne matche pas à travers le `\n`. **Le 433 est comparatif** — il le
dit deux fois : « **Rang 1**, et **le même que le 432** » puis « la conséquence
est **plus lourde qu'au 432** ». Correctif : `re.sub(r'\s+', ' ', s)` **avant**
le découpage.

### Défaut 2 — un lexique comparatif trop étroit, et c'est le gros morceau

Mon régime exigeait `famille DE/DU/DES`. Cinq formulations lui échappaient, et
**aucune n'est marginale** :

```text
lot  la phrase, en propre                                              forme ratée
454  « C'est **la famille** 411/424/435/436/446 »                      « la famille » sans « de »
464  « Je le classe **au-dessus du 463**, et je dis sur quel critère »  « au-dessus du »
461  « pas une consigne d'action fausse **comme celle du 457**. Rang 2 » « comme celle du »
424  « Ce n'est **ni le 422** … **ni le 421/423** … c'est **entre les deux** » « ni … ni … entre les deux »
417  « il faut dire en quoi c'est **différent du 407** »                « différent du »
```

**Le 424 est le cas le plus embarrassant** : c'est le rang **le plus purement
relatif de toute la veine** — son rang 2 est littéralement *construit* en
encadrant deux autres dossiers (« ni le 422, rang 1 ; ni le 421/423, rang 4 :
c'est entre les deux ») — et c'est précisément celui que le 480 a manqué.

## Le contrôle qui décide si l'élargissement est honnête

Élargir un lexique est le moyen le plus facile de faire monter un compte. Le
contrôle négatif est donc **le vrai test de ce lot**, et il était posé d'avance :
le 480 **excluait explicitement** « citer un autre lot pour un FAIT (un site, une
mesure, une **méthode**) sans marqueur comparatif ». Cinq sections font
exactement cela :

```text
437  « C'est exactement le critère posé au 431 »
478  « Le critère posé au 431 »
446  « la règle que la boucle s'applique depuis le 411 et le 435 »
458  « règle 442/445 »
457  « motif 381/385/414/415 »
```

**Aucune des cinq ne devient comparative avec le lexique élargi — 0 sur 5.** Plus
le témoin hors veine (484) qui ne matche pas, le témoin positif (428, cité mot
pour mot par le 480) qui matche, la charge (24/24 sections trouvées) et la
variété (15 sur 24, population non uniforme). **Quatre étages, tous passés.**
L'élargissement corrige ; il ne relâche pas.

## La dette du 481, payée — et ce qu'elle vaut vraiment

**Zéro** des quinze sections comparatives est dépourvue de critère absolu. Un
zéro se lit mal (leçon 501), alors je l'ai contrôlé au lieu de le publier tel
quel : densité des marqueurs absolus dans les sections « Classement » contre les
sections **« Vérifications du cycle » des mêmes 24 rapports** — procédurales, sans
jugement sur l'effet d'un défaut.

```text
sections « Classement »              médiane 4,17 marqueurs / 1 000 car.
sections « Vérifications » TÉMOIN    médiane 0,00      ·  24 / 24 à ZÉRO
```

Le régime discrimine. **Mais je ne m'arrête pas au compteur** : le régime compte
aussi les occurrences **niées** (« aucune valeur n'est **inventée** », « ce n'est
**pas** un chiffre **faux** »), donc le nombre de marqueurs ne mesure aucune
force. **J'ai donc lu les quinze sections en entier**, et la forme est constante :
une négation de la charge la plus lourde, puis l'énoncé positif du défaut réel.

```text
425  « C'est le COMPTE qui est faux quand une source manque, dans une phrase qui
      se présente comme une déclaration de limites »
427  « C'est le NOM attaché à la couleur qui devient faux … sur une carte dont le
      rôle est précisément de comparer des indices entre eux »
432  « C'est la SYNTHÈSE qui est fausse, et elle est fausse dans le sens le plus
      coûteux pour un trader »
461  « une fausse quiétude en tête d'écran »
464  « change ce que l'utilisateur croit que le moteur vaut »
```

**La conclusion, et elle corrige un mot du 480** : la phrase publiée « 37,5 % des
rangs de la veine sont **justifiés** par comparaison » se trompe deux fois. Sur
le chiffre (62,5 %), et sur le verbe. Dans douze cas sur quinze la comparaison
**nomme la famille** pendant qu'un critère absolu porte le rang. Dans trois cas
seulement — **424, 461, 464** — la comparaison est **porteuse** du niveau ; et
même là, un critère absolu l'accompagne. **Aucun rang de cette veine ne repose
sur la seule comparaison.**

**Arrêtés avant publication : 80 → 81.** (le neuf reproduit par mon premier banc,
arrêté par mon second avant d'être écrit)

## Le second contrôle — le bornage du 480 re-croisé, et il tient

Six rangs relatifs de plus, c'est six occasions de casser le résultat principal
du 480 : « **sur neuf rangs relatifs, un seul est affecté** ». Les étalons qui
ont bougé sont **407, 416, 456** (mesure du 480). Croisement sur les quinze :

```text
lot  étalon bougé  la phrase                                    verdict
416     407        « nettement moins grave que le 407 »          DÉJÀ RÉSOLU au 479
418     416        « moins grave que le 416 et le 417 »          LE CAS UNIQUE, inchangé
422     407        « famille du 417, PAS du 407 »                négation — rien à casser
417     407        « en quoi c'est différent du 407 »            AJOUT — voir ci-dessous
```

Les onze autres ne citent aucun étalon qui a bougé (432, 421/422/423,
411/424/435/436/446, 457, 463, 417, 447, 425, 427, 428).

**Le seul cas ajouté qui touche un étalon mobile est le 417, et il ne casse
rien** — pour une raison qu'il faut dire précisément : sa comparaison
**différencie**, elle n'**ordonne** pas. Le 418 devient incohérent parce que
« moins grave que le 416 » est une *relation d'ordre* que la chute du 416 inverse.
« Différent du 407 » n'affirme aucun ordre : que le 407 soit rang 2 ou rang 1, le
417 reste rang 1 sans se contredire.

**Le bornage du 480 est donc CONFIRMÉ sur une population 67 % plus grande.**

### Et je dis franchement où le 417 est limite

Le 417 satisfait la **lettre** de la définition du 480 — « une même phrase
contient un marqueur comparatif *et* la référence à un autre lot » — mais pas son
**esprit**, « un classement **justifié** par comparaison » : son rang 1 est
justifié absolument (« un défaut d'honnêteté de présentation sur la page dont le
sujet est précisément la confiance qu'on peut accorder au moteur »), la
comparaison ne fait que le distinguer du 407. **Sans lui, quatorze.** Je le
compte parce que la règle écrite du 480 le compte, et je signale le cas plutôt
que de le trancher en silence.

## Portée — ce que ce lot NE dit PAS

- Il contrôle la **FORME des justifications de rang**, pas la **VÉRITÉ des défauts
  sous-jacents**. Qu'un dossier porte un critère absolu ne dit pas que ce critère
  est exact. Re-vérifier les défauts eux-mêmes est un autre travail, et il n'est
  pas fait ici.
- **La règle 491** (« vérifier que l'objet classé est bien celui qui est affiché »)
  **n'est appliquée à aucun des quinze** : elle demande de rouvrir chaque mesure.
  Je le nomme comme limite explicite, pas comme un point couvert.
- Les étalons mobiles sont **repris du 480** (407, 416, 456), non re-mesurés. Si
  cette liste est incomplète, mon croisement l'est aussi — et **le 480 avait
  lui-même corrigé son réveil sur ce point**, ce qui invite à la prudence.
- Le lexique comparatif reste un **choix de vocabulaire**. Il est maintenant
  contrôlé par le négatif à cinq cas, mais une seizième formulation exotique
  resterait invisible. **Le compte quinze est un plancher, pas un plafond.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; toutes les
  sorties en chemin **absolu** (incident 487).
- **Aucun fichier de production touché. Rien supprimé.** Pas de bump.
  SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** (`cache_path` suit la redirection) avant tout
  import de `terminal` ; aucune route réseau sortante appelée.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La plus ancienne dette de fond est payée, et elle rend **deux** résultats au lieu
d'un. Le résultat demandé est rassurant : aucun rang de la veine ne tient par la
seule comparaison, le stock ne s'effondre pas si un étalon bouge. Le résultat non
demandé l'est moins : **un de mes audits publiés comptait 37,5 % là où il y a
62,5 %**, et il l'a manqué parce que son lexique ignorait « la famille » sans
préposition et « au-dessus du ».

La leçon que je retiens est celle du **premier banc qui reproduit le chiffre
publié**. J'ai failli m'arrêter là — la reproduction ressemble à une
confirmation. **Deux instruments qui partagent une hypothèse partagent son
erreur ; seule une mesure qui attaque ce que le premier EXCLUT peut les
départager.** C'est la règle 481 qui a payé, pas la mesure principale.

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
La dette des huit rangs relatifs est **close**. Dettes nommées restantes :
**l'espion au troisième niveau** et **un retour au produit sur une surface jamais
auditée** (`/markets`, `/options`, `/journal`, `/system`).

Comptes séparés : résultats faux **arrêtés avant publication 81 (+1)** ; publiés
puis corrigés **11 → 12** (le « neuf sur vingt-quatre » du 480) ; interprétations
retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
