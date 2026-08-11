# SKYLER LOT 540 — **Les DIX-SEPT atténuations qui atteignent un écran ont toutes été lues : aucune n'invente un chiffre.** Le point fixe a multiplié les variables serveur par 26 et n'a reclassé aucune atténuation — c'est un résultat, pas un échec

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-540` (base : lot 539 fusionné,
`49b4242d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(h)** — le 539 a répondu « aucun chiffre inventé » sur **6 atténuations
reliées au serveur sur 112**. Les **106 autres** avaient une racine que mon lien
n'avait pas su prouver. C'était la réserve la plus grosse et la plus fraîche.

## Le point fixe de la provenance — et son résultat inattendu

La mécanique du 536 (suivre le paramètre jusqu'à ses appelants), appliquée cette
fois au **flux de données** :

```text
(base)      la variable vient d un `await` ou d un `VX.fetch(`
(champ)     `const rows = scan.rows`, enracinée dans une variable serveur
(paramètre) paramètre n° i d une fonction dont AU MOINS UN appelant passe une
            valeur serveur en position i
```

**Sur-approximation assumée** : un paramètre est marqué serveur dès qu'**un
seul** appelant lui passe une valeur serveur. L'écart va donc dans le sens des
**candidats en trop**, jamais des candidats manquants — réserve **à sens unique**
(**536-A**). Un faux « serveur » sera lu et disculpé ; un cas manqué ne le
serait jamais.

```text
CALIB 4 · POSITIF   les racines serveur du 539 restent serveur        OK
CALIB 5 · NÉGATIF   `myTrades`, `vxJournal` (localStorage) non serveur OK
```

Résultat :

```text
variables classées SERVEUR au point fixe        156   (539, base seule : 6)
atténuations reclassées                           0
```

**Vingt-six fois plus de variables serveur, et pas une seule atténuation qui
change de camp.** Les racines des `|| 0` ne sont, en effet, pas des valeurs
réseau.

## « Racine inconnue » n'est pas une réponse — je l'ai nommée

```text
paramètre                     50
calcul local                  37
appel local                   10
objet reconstruit              5
non déclarée dans la page      4
                             ───
                             106   FEUILLE : OK
```

## Le vrai résultat : **les 17 atténuations affichées, lues une par une**

Ce qui compte n'est pas la provenance, c'est **ce qui atteint l'écran**. Le 539
en avait lu 4 ; ce lot lit les **13 autres**.

**Onze sur `/journal`** — toutes des **compteurs d'opération**, initialisés à
zéro puis incrémentés côté serveur (`skyler_journal.py:56` :
`{'added_entries': 0, 'skipped_entries': 0, 'corrupted_entries': 0}`) :

```js
'décisions : ' + (s.added_decisions||0) + ' ajoutée(s), ' + (s.skipped_decisions||0)
  + ' déjà présente(s) (la donnée locale gagne) · séances : ' + (ses.added_sessions||0)
  + ' ajoutée(s) · journal : ' + (j.added_entries||0) + ' ajoutée(s)'
```

C'est le compte rendu d'une restauration qui vient d'avoir lieu. **Afficher 0
ajout quand rien n'a été ajouté est vrai** (**539-A**). Mieux : les entrées
corrompues ne s'affichent **que si la somme dépasse zéro**.

`oc.unmeasured||0` porte d'ailleurs, dans la même phrase, la mention
**« sans cote — jamais inventé »**.

**Deux sur `/system`** :

```js
${j.runs||0}                                        // compteur d exécutions
VX.fmt.<…>(s.received_ts||0)                        // formateur honnête
```

Et juste au-dessus du premier, le code **distingue explicitement l'absence du
zéro** :

```js
const st = j.last_run === null ? ['frozen','jamais exécuté']
                               : (j.last_ok ? ['live','OK'] : ['offline','erreur']);
```

**Les dix-sept atténuations qui atteignent un écran sont toutes légitimes. Les
95 autres ne s'affichent nulle part.**

## Ce que le dépôt fait bien, mesuré

- **Le produit distingue `null` de `0` là où ça compte** :
  `j.last_run === null → « jamais exécuté »`. C'est exactement l'invariant, écrit
  dans le code.
- **Les entrées corrompues ne sont affichées que si elles existent** — pas de
  « 0 entrée corrompue » inutile.
- **La phrase du journal dit elle-même « sans cote — jamais inventé »** : le
  vocabulaire de l'honnêteté est dans l'interface, pas seulement dans la
  documentation.
- **Aucune des 156 variables reconnues comme venant du réseau n'est la racine
  d'un `|| 0`.** La couche réseau et la couche des compteurs sont séparées.

## Portée — ce que ce lot NE dit PAS

- **La sur-approximation joue dans un seul sens.** Elle peut créer de faux
  candidats serveur (aucun n'est apparu), pas en cacher.
- **Les 95 atténuations non affichées ne sont pas innocentées** : elles sont
  **hors sujet**, puisque la question porte sur ce qui s'affiche. Si l'une
  alimentait un calcul affiché plus loin, mon crible d'« affichage » ne le verrait
  pas.
- Restent hors de portée : une valeur passée par un **événement**, par le store
  global `VXEntities`, ou par une **clôture**.
- **Les champs nuls sont relevés en DÉMO** (24 sur les routes sûres) ; en réel,
  la liste peut différer.
- **Aucun navigateur, aucune route interdite, aucune correction engagée.**

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
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. L'invariant « données réelles uniquement » tient sur **tout ce
qui atteint un écran** — et c'est désormais une phrase complète, pas une phrase
avec une réserve de 106 cas.

Ce qu'il faut dire sans le maquiller : **le point fixe que ce lot a construit
n'a rien changé au classement.** Ce qui a fermé la question, c'est d'avoir lu
treize expressions dans le code. Deuxième lot d'affilée où l'outil coûte cher et
où la réponse vient de la lecture (**538-A**). J'en tire la leçon pour de bon :
**compter d'abord ce qui atteint l'écran, chercher la provenance ensuite.**

Trois règles neuves :

- **540-A · UN POINT FIXE PEUT NE RIEN CHANGER, ET C'EST UN RÉSULTAT** — 156
  variables serveur au lieu de 6, zéro atténuation reclassée : la séparation des
  couches est mesurée, pas supposée.
- **540-B · « RACINE INCONNUE » N'EST PAS UNE RÉPONSE** — la nommer (50
  paramètres, 37 calculs locaux, 10 appels locaux, 5 objets reconstruits, 4 non
  déclarées) transforme une réserve en carte.
- **540-C · CE QUI COMPTE N'EST PAS LA PROVENANCE MAIS L'AFFICHAGE** — 17
  atténuations atteignent un écran, toutes lues ; les 95 autres n'en atteignent
  aucun.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 95 atténuations non affichées** ;
**`initSettings`, mesurée partiellement** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis et les 255 sélecteurs littéraux sans
identifiant** ; **la définition du corpus de routes du 511-A** ; **l'ampleur du
518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les
33 identifiants reconstruits** ; **les 92 rapports non additionnés du 526** ;
**les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 154** ; publiés puis
corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
