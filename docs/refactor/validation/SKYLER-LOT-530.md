# SKYLER LOT 530 — **Les 35 vues servies tiennent** : aucune n'est une coquille vide (403 à 1 643 caractères), 31 annoncent leur chargement, et les 4 restantes n'ont **aucun** conteneur muet. Mon témoin positif a échoué et je le publie

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-530` (base : lot 529 fusionné,
`395c6b90`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(m)** — rester sur le produit. Le 529 a montré que **le code se tient mieux que
ma prose** ; le rendement est là. La question neuve : **les 35 vues servies
peignent-elles toutes quelque chose ?**

Le 523 avait mesuré le **total** du texte rendu par le serveur — 25 454
caractères sur 37 URL — mais **jamais sa ventilation par vue**. Or c'est la
ventilation qui dit quelque chose d'utile.

Slugs **lus dans les registres** (**523-C**), jamais de mémoire.

## Mon témoin positif a ÉCHOUÉ — et c'est le premier résultat

```text
CALIB 1 · REGISTRES   35 vues (confirmé aux 518, 523 et 525)              OK
CALIB 2 · POSITIF     `/system?view=automations`, entièrement hydratée
                      par le JS, devait servir MOINS que la médiane :
                      749 caractères contre une médiane de 588        ÉCHEC
CALIB 3 · NÉGATIF     une vue FABRIQUÉE retombe sur la vue par défaut
                      (même MD5)                                          OK
CALIB 4 · VARIÉTÉ     32 longueurs distinctes sur 35                      OK
```

**Le volume de texte servi ne dit RIEN de la dépendance au JavaScript.** Une vue
peut servir beaucoup de texte *et* dépendre entièrement du JS pour ses chiffres.
**Je publie l'échec plutôt que de le corriger en silence** (**509-A**) — et je
change de **question**, pas de témoin.

## La mesure, qui reste juste

```text
35 vues · 24 060 caractères de texte servi · médiane 588
   la plus maigre   /markets?view=sectors        403 caractères
   la plus fournie  /system?view=settings      1 643 caractères
```

**Aucune des 35 vues ne sert moins de 400 caractères.** **Il n'existe pas de
coquille vide dans le produit** : chaque vue arrive avec ses titres, ses
libellés, ses en-têtes de tableau — **avant même que le JavaScript ne réponde**.

## Le discriminant qui marche : le squelette

Le shell rend `%%LOADING%%` en `vx-skeleton` : un conteneur qui attend doit
**annoncer** qu'il charge.

```text
vues portant AU MOINS UN squelette          31 / 35
vues n'en portant AUCUN                      4
   /markets?view=macro · /options?view=volatility
   /options?view=events · /options?view=scenarios
```

Le témoin fonctionne cette fois : `/system?view=automations` porte **3**
squelettes.

## L'arrêt du lot : « quatre conteneurs vides et muets » était FAUX

Le second contrôle a d'abord rendu **TROU MESURÉ** — quatre conteneurs visés par
un chargeur, vides, sans annonce de chargement. **Un par vue.** Le dossier était
là.

Les quatre sont **le même** : `vx-palette-input`.

C'est le **champ de recherche de la palette de commandes**, un `<input>` du
shell. **Un `<input>` n'a pas de texte intérieur — il est vide par nature.** Ce
n'était pas un contenu manquant, c'était mon crible qui confondait « vide » et
« sans texte intérieur ».

```text
conteneurs de CONTENU vides et muets, après correction :   0
=> AUCUN TROU
```

**Arrêtés avant publication : 133 → 134.**

## Ce que le dépôt fait bien, mesuré

- **35 vues sur 35 servent du texte réel** — de 403 à 1 643 caractères. La page
  n'est jamais blanche, même sans JavaScript.
- **31 vues sur 35 annoncent leur chargement** par un squelette. Le contrat
  `%%LOADING%%` est tenu à 89 %.
- **Les 4 sans squelette n'ont aucun conteneur de contenu muet.** Deux d'entre
  elles — `/options?view=events` et `?view=volatility` — attendent une **saisie
  utilisateur** et affichent « Saisis un symbole. » (lu au 520) : **ne pas
  annoncer un chargement qui n'a pas commencé est correct**.
- **Le repli sur la vue par défaut fonctionne** : une vue fabriquée rend un MD5
  identique à celui de la vue par défaut, sur la page testée.

## Portée — ce que ce lot NE dit PAS

- **Il mesure ce que le SERVEUR sert**, pas ce que le navigateur affiche après
  hydratation. Une vue bien servie peut mal se remplir ensuite.
- **Le contrôle du repli n'a été fait que sur `/system`**, pas sur les 8 pages.
- **« Aucun conteneur muet » vaut pour les 4 vues sans squelette**, pas pour les
  31 autres, dont les conteneurs n'ont pas été inventoriés un par un.
- La question de départ — « les 35 vues peignent-elles ? » — reste **répondue à
  moitié** : elles **servent** toutes, l'exécution complète des 35 chargeurs
  reste à faire.
- **Aucun navigateur, aucun POST, aucune route interdite** ; seules les 8 pages,
  leurs 35 vues et leurs scripts ont été lus, avec `terminal.scan()` en DÉMO.

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
0**.

Aucun dossier — et pour la deuxième fois d'affilée, **le produit sort mieux que
prévu**. Deux lots de retour au code ont donné : quatre chiffres de rang 4
vérifiés (529), puis une surface servie qui **tient sur les 35 vues**. Ce qui
cède, ce sont mes instruments — et cette fois **dès la calibration**, ce qui est
exactement là où il faut que ça cède.

Trois règles neuves :

- **530-A · LE VOLUME DE TEXTE SERVI NE DIT RIEN DE LA DÉPENDANCE AU
  JAVASCRIPT** — 749 caractères pour une vue entièrement hydratée, contre une
  médiane de 588.
- **530-B · UN CONTENEUR VIDE PAR NATURE N'EST PAS UN CONTENEUR MUET** — un
  `<input>` n'a pas de texte intérieur ; quatre « trous » n'en étaient pas.
- **530-C · QUAND UN TÉMOIN ÉCHOUE, CHANGER DE QUESTION, PAS DE TÉMOIN** — le
  squelette a remplacé la longueur comme discriminant, et il passe son témoin.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus** ; les cinq rangs 4 nommés, **deux confirmés au chiffre près**
(512-A, 513-A), un juste au mot près (519-A), deux non recomptables (511-A,
518-A).

Dettes nommées restantes : **exécuter les chargeurs des 35 vues** (la moitié
restante de la question) ; **la définition du corpus de routes du 511-A** ;
**l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs
fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **les 17 chargeurs
muets** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en
attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 134 (+1)** ; publiés
puis corrigés **20** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
