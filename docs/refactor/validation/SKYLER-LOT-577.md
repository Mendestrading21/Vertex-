# SKYLER LOT 577 — **le « 10 sur 10 » du 572 tombe à 17 sur 18** — et pourtant les huit disent pourquoi

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-577` (base : lot 576 fusionné,
`8e6b6565`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(ww)** — le 576 a établi que sur l'écran d'analyse d'un titre, le signalement
d'échec ne passe **pas** par le toast (aucun ton `error` parmi les trois) mais
par **8 bannières `vx-error-banner`**. Elles avaient été comptées, jamais lues.

Le 572 avait publié **10 bannières sur 10 interpolent la cause réelle** — la
seule affirmation « 100 % » de toute la série, jamais éprouvée hors de son
corpus. Les 8 nouvelles sont l'épreuve.

Piège écrit **avant** de mesurer (564, 568-B) : *je m'attends à ce que les 8
interpolent aussi — le produit est régulier. **Mais une affirmation à 100 % ne se
confirme pas, elle se réfute** : une seule bannière littérale la fait tomber.*
Second piège (576-B) : *« interpoler » est un critère **syntaxique** — une
bannière peut interpoler une variable qui ne contient aucune cause.*

## Deux instruments indépendants, le même nombre

```text
instrument du 570 (au 576), genre « bannière »   8
instrument du 572, rejoué tel quel               8
```

Contrairement au 574 — où deux « 25 » cachaient deux ensembles différents
(574-B) — les deux relevés portent ici sur les **mêmes 8 sites**, tous dans
`inline#1`.

## Le piège **échoue** : 7 sur 8, pas 8 sur 8

```text
bannières relevées                    8
   INTERPOLENT (critère du 572)       7
   LITTÉRALES                         1
```

La bannière littérale, lue :

```javascript
$('an-stale').innerHTML =
  '<div class="vx-error-banner">Titre hors du scan courant — dossier partiel. '
  + '<a class="vx-btn …';
```

Deux littéraux concaténés : aucune valeur interpolée. **Le « 10 sur 10 » devient
17 sur 18.**

Une affirmation à 100 % n'a pas survécu au **premier** corpus nouveau qu'on lui a
présenté. Ce n'est pas une erreur du 572 — sur son corpus, le compte était juste —
c'est la nature d'un « 100 % » : il se réfute, il ne se confirme jamais.

## Le second piège, lui, **tient** — « interpole » n'est pas « dit pourquoi »

Relevé feuille par feuille de ce qui est réellement interpolé :

```text
 1  @2544   LITTÉRALE
 2  @28583  exception          esc(e.message)
 3  @42259  autre + REPLI      esc(d.error || 'réponse indisponible')
 4  @42603  exception          esc(e.message)   « Copilote injoignable : »
 5  @44295  exception          esc(e.message)   « Vérification impossible : »
 6  @44828  exception          esc(e.message)   « Scanner injoignable : »
 7  @47660  exception          esc(e.message)   « Skyler injoignable : »
 8  @49619  exception          esc(e.message)   « Évidence injoignable : »

des 7 qui interpolent :
   relaient le message d'une EXCEPTION            6
   relaient un champ serveur AVEC repli littéral  1
```

La n° 3 est le cas exact que le piège annonçait : elle **interpole**, donc elle
compte dans le « 100 % » — mais si `d.error` est vide, elle affiche « réponse
indisponible », c'est-à-dire **rien sur la cause, au moment précis où la cause
manque**. Un critère syntaxique ne peut pas voir cette différence.

## Ce que la mesure établit malgré tout — **les huit disent pourquoi**

Trois moyens différents, tous honnêtes :

- **six relaient l'exception** (`e.message`), précédées d'un préfixe qui nomme le
  domaine en panne : Copilote, Scanner, Skyler, Évidence, Vérification ;
- **une relaie le champ d'erreur du serveur**, avec un repli qui, lui, ne dit
  rien ;
- **une énonce une cause constante en clair** — « Titre hors du scan courant —
  dossier partiel » — et n'a **rien à interpoler** : la cause ne varie pas.

C'est la contradiction intéressante du lot : **le critère du 572 tombe, sa
conclusion produit tient.** Le « 10 sur 10 » mesurait la forme ; ce que le
produit fait vraiment, c'est nommer le domaine et relayer la cause — y compris
quand la meilleure façon de le faire est un texte fixe.

## Second contrôle (481) — ce que la restriction de l'instrument exclut

L'instrument du 572 ne voit que les affectations à `innerHTML` / `textContent`.
Le 571 avait dû rattraper une bannière écrite dans un **ternaire** au milieu
d'une chaîne `+` (c'est ce qui a porté le plancher de 89 à 90). Contrôle par
comptage **brut** de la classe, sans aucun filtre par nom de fichier — la leçon
576-A :

```text
occurrences BRUTES de `vx-error-banner` dans le corpus   8   (toutes dans inline#1)
bannières vues par l'instrument du 572                   8
écart                                                    0
```

**Aucun angle mort ici** : sur ce corpus, la restriction `innerHTML` ne coûte
rien. Elle en coûtait un sur le corpus de base — la même restriction, deux
résultats : une limite d'instrument **se mesure sur chaque corpus** (547-B).

## Ce que le dépôt fait bien, mesuré

- **Huit bannières sur huit disent pourquoi**, par trois moyens distincts.
- **Cinq nomment le domaine en panne avant même la cause** (« Skyler
  injoignable : », « Scanner injoignable : ») : l'utilisateur sait *quoi* a
  échoué avant de lire *pourquoi*.
- **Tout ce qui est interpolé passe par `esc()`** — les 7 sans exception, ce qui
  ferme la porte à l'injection par un message d'erreur.
- **La bannière littérale propose une action** (`<a class="vx-btn …`) : elle ne
  se contente pas de constater.

## Portée — ce que ce lot NE dit PAS

- **`e.message` est relayé tel quel** : c'est honnête, ce n'est pas toujours
  intelligible (un échec réseau donne souvent un message technique). **Constat,
  pas jugement — et aucun message n'est réécrit.**
- Le « 17 sur 18 » est un ratio sur **deux corpus réunis**, pas un recensement du
  produit : d'autres bannières peuvent exister ailleurs.
- La n° 3 est signalée **parce que sa forme le permet**, pas parce qu'un échec
  réel a été observé : le repli n'a pas été déclenché ici.
- Le relevé reste un **plancher** : serveur en DÉMO, sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, bancs écrits **en fichier**, aucun tronqué avant d'avoir
  écrit son JSON. Banc de causes **écrit à part** : `l572_bannieres.js` n'a pas
  été touché.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu
  ni disparu (la rotation des sauvegardes desk, survenue au 576 au changement de
  date, ne s'est pas reproduite)
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents
- **Défaut de rendu, constaté par la règle 553** : ma substitution `%%MD5%%`
  portait déjà `**…**` et s'insérait dans une ligne déjà en gras — les rapports
  **574, 575 et 576** affichent donc `**8 / 8 identiques.****`, avec deux
  astérisques parasites. Corrigé **ici seulement** : les rapports publiés ne se
  réécrivent pas, les corrections sont en ajout. Le chiffre, lui, était juste
  dans les trois.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Et aucun compteur ne bouge** : rien n'a été arrêté avant
publication, rien de publié n'est corrigé, aucune interprétation retirée. Le
piège a échoué — et c'est publié comme tel. Un piège qui échoue n'est pas une
faute : c'est exactement ce pour quoi on l'écrit d'avance.

Ce que je retiens : **j'ai écrit « je m'attends à ce que les 8 interpolent
aussi » et la première bannière lue m'a donné tort.** Le 572 avait raison sur son
corpus et faux comme loi. Le seul geste qui a fait la différence est celui de
poser, dans le même souffle, l'attente **et** ce qui la réfuterait.

Et une leçon plus fine : **le critère qui tombe et la conclusion qui tient ne
sont pas la même chose.** Le 572 avait mesuré une forme et conclu sur un
comportement. La forme n'était pas universelle ; le comportement, lui, l'est
resté — mais il aurait été tout aussi possible que l'inverse se produise, et rien
dans le « 10 sur 10 » ne permettait de le savoir.

Trois règles neuves :

- **577-A · UNE AFFIRMATION À 100 % SE RÉFUTE, ELLE NE SE CONFIRME PAS** — « 10
  sur 10 » est devenu **17 sur 18** au premier corpus nouveau.
- **577-B · « INTERPOLE » N'EST PAS « DIT POURQUOI »** — `esc(d.error ||
  'réponse indisponible')` interpole, et n'apprend rien quand la cause manque.
- **577-C · UNE BANNIÈRE LITTÉRALE PEUT DIRE LA CAUSE MIEUX QU'UNE INTERPOLÉE** —
  « Titre hors du scan courant — dossier partiel » nomme une cause **constante** :
  interpoler n'aurait rien ajouté.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 6 bannières qui relaient `e.message` tel quel,
constatées et NON jugées** ; **le repli « réponse indisponible » de la n° 3, non
déclenché ici** ; **les 38 sites du relevé structurel neuf du 576** ; **les 29
branches de produit de la borne (B) neuve** ; **le filtre `chart.umd` des six
instruments, constaté et NON corrigé** ; **les 8 programmes d'`/analysis/AAPL`,
non lus ligne à ligne** ; **les 269 branches qui s'arrêtent sans rien dire** ;
**les 14 sites « ailleurs » du 573** ; **les 19 toasts d'erreur littéraux, non
jugés** ; **les 6 toasts sans ton** ; **`warn` et `warning`, non unifiés** ;
**les 23 toasts `success`** ; **les 57 sites qui ne signalent pas un échec** ;
**le total réel des signalements d'échec, toujours inconnu** ; **les 27 appelés
du relevé structurel du 570** ; **les 82 corps vides du 569, NON JUGÉS** ; **les
18 gardes portant un `VX.fetch`** ; **les 63 `empty` distincts du 568** ; **les
42 refus du 567, non lus un par un** ; **les 4 refus non-JSON du 542** ; **les 74
variables serveur sans atténuation** ; **les 67 atténuations non affichées** ;
**les 25 atténuations de la bibliothèque tierce** ; **`/options|chips`** ;
**`renderCalendar`** ; **les 4 limites distinctes du 564** ; **les 12 signatures
partagées du 562** ; **les 5 cas de réponse absents du corpus du 561** ; **les 8
unités encore ambiguës** ; **les 10 cas non tranchés du 559** ; **les 16
sous-clés du 558** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les
35 clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans
lecture observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions
de nom** ; **les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ;
**les 14 candidates du 554, en attente d'un GO** ; **les 4 routes construites
`/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **`initSettings`** ; **les 8 appels
hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les 92 rapports non additionnés du 526** ; **les quinze lots exposés du 525** ;
**le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente
d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 203** ; **publiés
puis corrigés 37** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
