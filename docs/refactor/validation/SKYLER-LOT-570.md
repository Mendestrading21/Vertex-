# SKYLER LOT 570 — le second canal d'erreur, inventorié : **89 sites au PLANCHER** — et **79 d'entre eux vivent hors de toute clause `catch`**, là où le 569 ne pouvait pas regarder

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-570` (base : lot 569 fusionné,
`b3ad2faa`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix, et pourquoi le titre dit « plancher »

**(pp)** — le 569 a découvert, en lisant 123 clauses `catch`, qu'il existe un
**second canal de signalement d'échec** que l'instrument du 541 ne connaissait
pas : `VX.toast(…, 'error')`, `emptyCard(…)`, `setStatus(…)`, `setNet(…)`, la
bannière `vx-error-banner`, le marqueur `dataset.state = 'error'`.

**Ces noms viennent d'un échantillon de 41 clauses.** Un inventaire qui ne
chercherait qu'eux **se confirmerait lui-même**. D'où deux relevés indépendants,
et la publication de l'écart :

- **(A)** relevé par les noms lus — **plancher assumé, annoncé dans le titre** ;
- **(B)** relevé **structurel, aveugle aux noms** — tout appel portant un
  argument littéral d'au moins trois mots contenant une lettre.

```text
CALIB 1 · POSITIF     les sites lus au 569 se retrouvent : 4 `VX.toast`
          et 1 `emptyCard` dans un `catch`, 9 bannières            OK
CALIB 2 · COHÉRENCE   105 programmes, 0 erreur                     OK
CALIB 3 · NÉGATIF     un nom FABRIQUÉ                              OK
```

## (A) — le plancher

```text
                distinct   cumul
VX.toast              55     251
emptyCard             14      14
setNet                 5      40
setStatus              5      40
bannière               9       9
marqueur               1       8
                     ───
PLANCHER              89 sites distincts
```

## La grille du 541, appliquée au canal découvert

```text
littérale           58        littérales de 3 mots ou moins   46
construite          18        position de l'argument porteur :
repli littéral       1           index 0 → 75 · index 1 → 2 · aucun → 2
absent               2
                   ───
                    79 sites d'appel
```

**La position de l'argument porteur varie selon l'appelé** — `VX.toast(msg, …)`
mais `emptyCard(id, msg)`. Une grille qui aurait supposé « argument 0 » aurait
manqué une partie du canal (563-A) ; celle-ci prend le **premier argument de
type message**, quel que soit son rang.

## L'écart (A)/(B) — **et ce qu'il établit vraiment**

```text
(B) sites distincts portant un message littéral   209
    appelés distincts                              31
       déjà connus (canal 569 + canal 541)          4
       INCONNUS des deux canaux                    27

les plus fréquents : kv 15 · VX.updateIndicator 9 · cell 9
   · VX.shell.openModal 6 · kvr 6 · tile 6 · out.push 5 · H 4 · esc 3 · row 3
```

Le contrôle anti-auto-confirmation a fonctionné **dans les deux sens**, et c'est
le résultat le plus utile du lot :

1. **(A) est bien un plancher** — 27 appelés portent des messages sans être dans
   la liste lue.
2. **Mais (B) n'est pas un recensement non plus.** Ces 27 appelés sont
   massivement des **aides de rendu** — `kv`, `cell`, `tile`, `row`, `esc`,
   `out.push` construisent des étiquettes de tableau, pas des annonces d'échec.
   **Un balayage purement structurel ne distingue pas un message d'erreur d'un
   libellé de colonne.**

Les deux relevés sont bornés, chacun à sa façon. **Aucun des deux ne donne le
total, et le dire est le résultat.**

## L'arrêt du lot — **13 et 89 ne comptent pas la même chose**

Le 569 publie « **13** clauses `catch` signalent l'échec hors instrument ». Ce
lot publie « **89** sites du canal ». La phrase qui s'écrit toute seule — « le
569 en avait vu 13, il y en a 89 » — **compare des clauses à des sites d'appel**.

Mesuré plutôt que supposé :

```text
sites du canal DANS une clause `catch`            10
   VX.toast 4 · setNet 1 · setStatus 1 · emptyCard 1
   bannière 2 · marqueur 1
écart avec les 13 clauses du 569                   3
```

L'écart de 3 s'explique par le **périmètre**, pas par une erreur : le 569
comptait aussi les écritures DOM de contenu et des appels (`fallbackPolling`)
qu'il avait classés « appelle », alors que ce lot ne retient que les six formes
nommées du canal. **Les deux comptes sont justes ; ils ne mesurent pas la même
chose** (546-A).

**Arrêtés avant publication : 195 → 196 (+1).**

## Second contrôle (481) — ce que la restriction du 569 cachait

```text
sites du canal, distincts                         89
   dont DANS une clause `catch`                   10
   dont HORS de toute clause `catch`              79
```

Le 569 n'avait regardé que l'**intérieur** des clauses `catch`. **Quatre-vingts
pour cent du canal vit ailleurs** — dans des chemins nominaux, des gardes de
validation, des retours d'action utilisateur. La restriction n'était pas
neutre, et sa taille est maintenant chiffrée.

## Ce que le dépôt fait bien, mesuré

- **Le canal existe et sert largement** : 89 sites au plancher, 251 appels
  `VX.toast` en cumul sur les 8 pages.
- **Dix-huit messages sont construits** — préfixe de contexte **plus** cause
  réelle. La forme la plus riche du 541 existe aussi dans ce canal.
- **`emptyCard(id, msg)` porte son message en deuxième argument** : le canal n'a
  pas de signature unique, et il fonctionne quand même — c'est l'instrument qui
  doit s'adapter, pas le code.
- **Neuf bannières `vx-error-banner` distinctes** : l'échec a une forme visuelle
  dédiée, pas seulement un texte.

## Portée — ce que ce lot NE dit PAS

- **(A) est un plancher, (B) n'est pas un recensement.** Le nombre total de
  signalements d'échec du produit **reste inconnu**, et ce lot ne prétend pas le
  donner.
- **Les 46 littérales courtes ne sont pas jugées** — le 541 avait déjà posé
  qu'on compte les mots, on ne note pas la qualité d'une phrase.
- Un message construit dans une variable puis passé à un appel **échappe aux
  deux relevés**.
- **Rien n'est corrigé, rien n'est ajouté.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Deuxième lot consécutif sur un objet du produit plutôt que sur un
chiffre ancien, et le second canal d'erreur a maintenant une taille — bornée par
le bas, et **dite comme telle**.

Ce que je retiens : **le contre-relevé m'a donné l'inverse de ce que j'espérais,
et c'est mieux.** J'attendais qu'il révèle un troisième canal ; il a révélé que
la forme d'un message ne dit pas sa fonction — `kv('Prix', '…')` et
`VX.toast('Mise à jour impossible', 'error')` sont structurellement jumeaux et
sémantiquement étrangers. Je repars donc avec **deux bornes et aucun total**, ce
qui est la seule chose vraie que je pouvais rapporter.

Trois règles neuves :

- **570-A · UN INVENTAIRE FONDÉ SUR DES NOMS LUS DANS UN ÉCHANTILLON EST UN
  PLANCHER** — et cela se dit dans le titre, pas dans une note de bas de page.
- **570-B · UN BALAYAGE STRUCTUREL N'EST PAS UN RECENSEMENT NON PLUS** — 27
  appelés inconnus, presque tous des aides de rendu : la forme ne distingue pas
  un message d'échec d'une étiquette.
- **570-C · DEUX COMPTES JUSTES PEUVENT NE PAS ÊTRE COMPARABLES** — 13 clauses
  et 89 sites ; l'unité se déclare **avant** la comparaison, pas après.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **le total réel des signalements d'échec, toujours
inconnu — deux bornes, aucun recensement** ; **les 27 appelés du relevé
structurel, non triés** ; **les 46 littérales courtes du canal, non jugées** ;
**les 79 sites hors `catch`, comptés mais non lus** ; **les 82 corps vides du
569, comptés et situés, NON JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ;
**les 63 `empty` distincts du 568** ; **les 42 refus du 567** ; **les 4 refus
non-JSON du 542** ; **les 74 variables serveur sans atténuation** ; **les 67
atténuations non affichées** ; **les 25 atténuations de la bibliothèque tierce** ;
**`/options|chips`, douzième limite jamais levée ni nommée** ; **`renderCalendar`,
exécutée hors périmètre au 537** ; **les 4 limites distinctes du 564** ; **les 12
signatures partagées du 562** ; **les 5 cas de réponse absents du corpus du
561** ; **les 8 unités encore ambiguës** ; **les 10 cas non tranchés du 559** ;
**les 16 sous-clés du 558** ; **les 5 chaînes nues** ; **les 10 chaînes
ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28 candidates** ; **les
6 clés sans lecture observée** ; **les 26 routes à lectures ambiguës** ; **les 4
collisions de nom** ; **les 3 ombres de `briefing.py`** ; **les 5 routes affamées
du 556** ; **les 14 candidates du 554, en attente d'un GO** ; **les 4 routes
construites `/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`,
hors corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies
non nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6
points d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ;
**les 43 points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **`initSettings`** ; **les 8 appels
hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les 92 rapports non additionnés du 526** ; **les quinze lots exposés du 525** ;
**le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente
d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 196 (+1)** ; publiés
puis corrigés **33** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
