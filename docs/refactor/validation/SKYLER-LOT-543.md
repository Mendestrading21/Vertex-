# SKYLER LOT 543 — Bilan sur pièces des dix lots de mesure : **la chaîne des arrêts s'additionne sur les dix, la série des rangs s'allonge d'exactement un par lot, et les 8 MD5 mesurés aujourd'hui confirment ce que les dix rapports annoncent**. Deux arrêts, dont un « OK » creux

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-543` (base : lot 542 fusionné,
`3234eabd`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(k)** — dix lots consécutifs (533 → 542) ont mesuré le produit sous dix
angles. **Un seul dossier en est sorti — 531-A — et il n'a pas bougé d'un
chargeur en cinq mesures indépendantes.** Avant d'ouvrir un onzième angle, on
vérifie ce que ces dix rapports avancent.

**Ce genre de lot est celui où j'ai déjà dérapé** : le 526 a montré qu'une
feuille peut ne pas s'additionner, le 527 qu'un relevé n'est pas un arbitrage,
le 528 qu'une phrase n'est pas une attribution. Le bilan ne porte donc **que sur
des chiffres recomptables**.

## Deux arrêts — le second est le plus instructif de la série

**1. Le gras n'était pas où je le croyais.** Mes motifs cherchaient
`arrêtés avant publication **143` alors que les rapports écrivent
`**arrêtés avant publication 143 (+4)**` — **le gras enveloppe la phrase, il ne
précède pas le chiffre**. Plusieurs lots ressortaient à `None`.

**2. Et ma chaîne imprimait « OK » sans avoir rien vérifié.** Ma boucle
**sautait** les paires dont une valeur manquait… puis affichait
`CHAINE : OK — elle s'additionne sur les dix`. **Un contrôle qui saute ses
données manquantes rend un OK creux** — et celui-là aurait été publié comme une
preuve.

**Arrêtés avant publication : 158 → 160.**

## Ce que les dix rapports annoncent, extrait par lecture

```text
lot   arrêts  (+)   corrigés   suite   SW              MD5
533    143     4       21      2864   td-shell-v187   8/8
534    146     3       22      2864   td-shell-v187   8/8
535    148     2       22      2864   td-shell-v187   8/8
536    149     1       22      2864   td-shell-v187   8/8
537    152     3       22      2864   td-shell-v187   8/8
538    153     1       22      2864   td-shell-v187   8/8
539    154     1       22      2864   td-shell-v187   8/8
540    154     —        —      2864   td-shell-v187   8/8
541    155     1       22      2864   td-shell-v187   8/8
542    158     3       22      2864   td-shell-v187   8/8
```

Le tiret du 540 n'est pas un trou du rapport : **sa phrase est coupée par un
retour à la ligne** (`publiés puis` / `corrigés **22**`), ce que mon extracteur
ne franchit pas. Vérifié à la main : **22**. Limite d'instrument, nommée.

## (1) La chaîne des arrêts s'additionne — vraiment, cette fois

```text
533 -> 534 : 143 + 3 = 146   annoncé 146   OK
534 -> 535 : 146 + 2 = 148   annoncé 148   OK
535 -> 536 : 148 + 1 = 149   annoncé 149   OK
536 -> 537 : 149 + 3 = 152   annoncé 152   OK
537 -> 538 : 152 + 1 = 153   annoncé 153   OK
538 -> 539 : 153 + 1 = 154   annoncé 154   OK
539 -> 540 : 154 + 0 = 154   annoncé 154   OK
540 -> 541 : 154 + 1 = 155   annoncé 155   OK
541 -> 542 : 155 + 3 = 158   annoncé 158   OK
                                   NEUF transitions vérifiées, zéro écart
```

**Quinze arrêts sur dix lots**, et la comptabilité tient bout à bout. C'est
exactement ce que le 526 avait trouvé en défaut sur une autre période : ici, la
feuille s'additionne.

## (2) La série des rangs s'allonge d'exactement un par lot

```text
533 : 30 rangs (origine)   534 : 31   535 : 32   536 : 33   537 : 34
538 : 35   539 : 36   540 : 37   541 : 38   542 : 39            OK
```

**Aucun lot n'a oublié d'inscrire son rang, aucun n'en a inscrit deux.**

## (3) Le témoin positif — mesuré aujourd'hui, pas recopié

```text
MD5 mesurés MAINTENANT            8 / 8
SW mesuré MAINTENANT              td-shell-v187
les dix rapports annoncent SW     td-shell-v187   (valeur unique)
les dix rapports annoncent MD5    8/8             (valeur unique)
les dix rapports annoncent        2864 passed     (valeur unique)
```

**Ce que dix rapports affirment coïncide avec ce que le dépôt rend
aujourd'hui.** Témoin négatif : le nombre fabriqué « 999 » **n'apparaît dans
aucun des dix**.

## (4) Trente règles de méthode, trois par lot, sans exception

```text
533-A/B/C · 534-A/B/C · 535-A/B/C · 536-A/B/C · 537-A/B/C
538-A/B/C · 539-A/B/C · 540-A/B/C · 541-A/B/C · 542-A/B/C     = 30
```

## (5) NON RECOMPTÉ — et c'est dit

Les chiffres lourds de ces dix lots **ne sont pas confirmés par ce bilan** : les
revérifier demanderait de rejouer chaque banc (**522-A** : la méthode d'un
chiffre est dans le script qui l'a produit).

```text
533  5 helpers · 102 fonctions · 120 appels
534  130 fonctions · 178 appels · 71 divergences
535  63 conteneurs à squelette
536  132 accès non littéraux · 279 querySelector
537  25 fonctions : 9 peignent · 4 muettes · 12 limites
538  11 limites levées · 633 et 125 caractères peints
539  112 atténuations · 272 formateurs · 24 champs nuls
540  156 variables serveur · 106 racines nommées
541  103 états · 28 erreurs · 75 vides
542  53 refus · 4 noms de clé
```

**Aucun n'est confirmé par recopie. Aucun n'est infirmé non plus.** Ils restent
tels que leur banc les a produits.

## Ce que le dépôt fait bien, mesuré

- **Dix lots, dix rapports, zéro manquant.**
- **Le produit n'a pas bougé d'un octet sur dix lots** : mêmes 8 MD5, même
  version de service worker, même suite verte.
- **La comptabilité des erreurs tient** : quinze arrêts déclarés, chaîne
  vérifiée sur neuf transitions.
- **Un seul dossier en dix lots de mesure**, et il est borné par cinq mesures
  indépendantes.

## Portée — ce que ce lot NE dit PAS

- **Il ne recompte AUCUN chiffre de mesure produit.** Il vérifie la
  comptabilité, pas les trouvailles.
- **Un « OK » de chaîne ne dit pas que les arrêts étaient justifiés** : il dit
  que leur compte est cohérent.
- L'extraction est textuelle : **un retour à la ligne suffit à la mettre en
  défaut** (cas du 540), et ce qui n'est pas écrit selon la même formule
  n'est pas vu.
- **Aucune exécution de banc, aucun navigateur, aucune correction engagée.**

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
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Onze lots sans dossier neuf, et un bilan qui, pour une fois,
**confirme** au lieu de trouver un trou : la comptabilité de ces dix lots tient,
et le produit n'a pas bougé pendant qu'on le mesurait.

Ce qu'il faut dire sans le maquiller : **j'ai failli publier un « OK » qui ne
vérifiait rien.** Ma boucle sautait les données manquantes puis affichait que la
chaîne s'additionnait. Ce n'est pas une coquille : c'est la forme la plus
dangereuse d'erreur pour un travail comme celui-ci — **un contrôle qui se
déclare satisfait sans avoir rien contrôlé.**

Trois règles neuves :

- **543-A · UN CONTRÔLE QUI SAUTE SES DONNÉES MANQUANTES REND UN OK CREUX** —
  ma chaîne imprimait « OK » sans avoir vérifié une seule paire.
- **543-B · LE GRAS N'EST PAS À L'ENDROIT QU'ON CROIT** —
  `**arrêtés avant publication 143**` : le gras enveloppe la phrase entière.
- **543-C · UN BILAN NE CONFIRME QUE CE QU'IL RECOMPTE** — les dix chiffres
  lourds sont marqués NON RECOMPTÉ, jamais validés par recopie.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les dix chiffres lourds, NON RECOMPTÉS** ; **le
contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les
15 messages d'erreur sans pourquoi du 541** ; **les 95 atténuations non
affichées** ; **`initSettings`, mesurée partiellement** ; **les 8 appels hors de
toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 160 (+2)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
