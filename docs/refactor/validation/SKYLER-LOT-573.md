# SKYLER LOT 573 — les sites hors `catch` : ils sont **80, pas 79** — et **25 d'entre eux signalent un échec sans qu'aucune exception ne soit levée**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-573` (base : lot 572 fusionné,
`a2e8d9f8`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix

**(ss)** — le 570 avait compté les sites du canal vivant hors de toute clause
`catch` ; **personne ne les avait lus**. C'est la plus grosse surface non
explorée du canal, et elle touche l'invariant produit de plein fouet : **un échec
peut être signalé sans qu'aucune exception ne soit levée.**

Deux témoins **lus dans le code avant toute mesure** le montraient déjà :

```javascript
if (!sets.length) { emptyCard('vx-mk-multi', 'Séries indices indisponibles…') }
if (!/^[A-Z.\-]{1,7}$/.test(sym)) { VX.toast('Ticker invalide', 'error') }
```

## La calibration a échoué sur un seul terme — **80, pas 79**

Le 570 publiait « 89 sites, 10 dans un `catch`, **79** hors ». Le 571 a corrigé
le plancher à **90** — la bannière de `system_page.py:594`, écrite dans un
ternaire au milieu d'une chaîne `+`. **Mais personne n'a re-dérivé le
complément.**

```text
site supplémentaire, vérifié   /system inline @23129
   genre bannière · classe « branche if » · dansCatch : NON
recompté : 90 sites · 10 dans un `catch` · 80 hors
```

C'est exactement **565-A** : un chiffre né d'une soustraction hérite des défauts
de ses deux termes, et **il ne se met pas à jour tout seul quand un terme
bouge**. La dette « les 79 sites hors `catch` » circulait déjà dans trois
rapports.

**Publiés puis corrigés : 34 → 35 (+1).**

## Ce qui déclenche les 80 sites hors `catch`

```text
garde négative      25      événement           12
branche if          20      promise-catch        5
ailleurs            14      fonction nommée      4
                                              ────
                                                80
```

Traits bruts, publiés à côté de la classe (569-B) :

```text
dansIf 46 · fonctionNommée 27 · testNégatif 25 · dansEvent 21
· promiseCatch 5 · dansThen 2 · portent plusieurs traits 12
```

## Le piège, vérifié — **des échecs sans exception**

```text
sites hors `catch` déclenchés par une garde négative   25
sites hors `catch` dans un `.catch(` de PROMESSE        5
                                                      ───
chemins d'échec potentiels sans `CatchClause`          30   (38 % des 80)
```

**Un `.catch(fn)` de promesse n'est pas une `CatchClause`** : cinq chemins
d'échec que tout comptage par clause range mécaniquement « hors `catch` ».

## L'arrêt du lot — **« garde négative » décrit le test, pas l'issue**

J'allais écrire « 30 chemins d'échec sans exception ». Mais la classe mesure la
**forme du test** (`!x`, `x === null`), pas ce qui en sort — et la sortie du banc
contenait déjà `setNet('online')` et `VX.toast(bits.join(' · '), 'success')`.
**Des issues positives dans une garde négative.**

Croisé avec le ton, en redéclarant le dénominateur (572-C — seuls les toasts en
ont un) :

```text
les 30 sites                                     30
   dont `VX.toast` (ont un ton)                  21
      ton `error`                                17
      autre ton                                   3
      ton `success`                               1
   dont SANS argument de ton                      9
      5 bannières `vx-error-banner` (injoignable + cause)
      3 `emptyCard` (« indisponible », « non calculé »)
      1 `setNet('online')`   ← issue POSITIVE dans une garde négative
```

**Recomposé : 25 des 30 signalent un échec** (17 toasts `error` + 5 bannières +
3 `emptyCard`), **un est franchement positif**, et quatre portent un autre ton.

Nommer le seau d'après le test aurait fait passer `setNet('online')` pour une
panne.

**Arrêtés avant publication : 198 → 199 (+1).**

## Ce que la mesure établit — **un troisième registre : la validation de saisie**

Les gardes négatives à ton `error`, lues :

```text
VX.toast('Position invalide (ticker/quantité)', 'error')
VX.toast('Ticker invalide', 'error')          VX.toast('Niveau requis', 'error')
VX.toast('Position introuvable', 'error')     VX.toast('Quantité invalide', 'error')
VX.toast('Montant de sortie requis', 'error')
```

Ce ne sont ni des pannes réseau ni des exceptions : ce sont des **refus de
saisie**. Le canal en compte au moins dix-sept, et **aucun lot ne les avait
distingués** — le 541 ne voyait pas le canal, le 569 ne regardait que les
`catch`, le 571 ne lisait que le ton, le 572 ne croisait que la forme.

C'est aussi ce qui explique la brièveté mesurée au 572 : **« Ticker invalide »
n'a pas de cause à donner** — la cause, c'est ce que l'utilisateur vient de
taper.

## Second contrôle (481) — les 10 sites dans un `catch`, même grille

```text
fonctionNommée 8 / 10 · dansIf 2 / 10 · testNégatif 1 / 10 · dansEvent 1 / 10
```

Les deux distributions **ne se comparent pas terme à terme** — 10 contre 80, et
la classe `catch` absorbe tout par priorité. Ce qui se compare, ce sont les
**traits** : un site en `catch` peut aussi être dans un `if`, ce que la classe
seule masquerait.

## Ce que le dépôt fait bien, mesuré

- **La validation de saisie est explicite** : dix-sept refus nommés, avec le ton
  `error`, avant tout appel réseau.
- **Cinq `.catch(` de promesse** signalent l'échec sans `try` — le produit ne
  dépend pas d'une seule forme de rattrapage.
- **Vingt et un sites sont dans un gestionnaire d'événement** : la notification
  est attachée à l'action de l'utilisateur, pas à un cycle de fond.
- **Aucun des 80 n'est orphelin** : chacun tombe dans une classe structurelle
  identifiable, et 14 seulement dans « ailleurs ».

## Portée — ce que ce lot NE dit PAS

- **La classe décrit un contexte syntaxique, pas une intention.** Un `if` peut
  garder autre chose qu'un échec.
- Les 14 « ailleurs » **ne sont pas lus** — comptés et situés seulement.
- **Un ton `error` prouve une intention de signalement**, pas qu'un échec réel a
  eu lieu.
- **Rien n'est corrigé** ; le « 79 » du 570 reste écrit là où il l'était, la
  correction est en ajout.

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Cinquième lot sur le canal, et le premier à en faire apparaître
**un registre entier que quatre lots successifs avaient traversé sans le voir**.

Ce que je retiens : **quatre instruments différents ont regardé le même code sans
voir la validation de saisie.** Le 541 mesurait un vocabulaire, le 569 des
clauses `catch`, le 571 un argument de ton, le 572 une forme de message. Aucun
n'était faux ; aucun ne posait la question « qu'est-ce qui déclenche ça ». Il
aura fallu cinq lots pour demander **quand**, après avoir demandé quoi, combien,
de quel ton et sous quelle forme.

Trois règles neuves :

- **573-A · UN COMPLÉMENT NE SE MET PAS À JOUR TOUT SEUL** — le plancher est
  passé de 89 à 90 au 571 ; le « 79 hors `catch` » est resté trois rapports.
  90 − 10 = 80.
- **573-B · UN SEAU NOMMÉ D'APRÈS LE TEST NE DIT RIEN DE L'ISSUE** — « garde
  négative » contient `setNet('online')`.
- **573-C · UN `.catch(` DE PROMESSE N'EST PAS UNE `CatchClause`** — cinq
  chemins d'échec que tout comptage par clause range « hors `catch` ».

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 14 sites « ailleurs », comptés et situés mais
non lus** ; **les 17 refus de saisie, non inventoriés pour eux-mêmes** ; **les 19
toasts d'erreur littéraux, non jugés** ; **les 6 toasts sans ton** ; **`warn` et
`warning`, non unifiés** ; **les 23 toasts `success`** ; **les 57 sites qui ne
signalent pas un échec** ; **le total réel des signalements d'échec, toujours
inconnu — deux bornes, aucun recensement** ; **les 27 appelés du relevé
structurel** ; **les 82 corps vides du 569, NON JUGÉS** ; **les 18 gardes portant
un `VX.fetch`** ; **les 63 `empty` distincts du 568** ; **les 42 refus du 567** ;
**les 4 refus non-JSON du 542** ; **les 74 variables serveur sans atténuation** ;
**les 67 atténuations non affichées** ; **les 25 atténuations de la bibliothèque
tierce** ; **`/options|chips`** ; **`renderCalendar`** ; **les 4 limites
distinctes du 564** ; **les 12 signatures partagées du 562** ; **les 5 cas de
réponse absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10
cas non tranchés du 559** ; **les 16 sous-clés du 558** ; **les 5 chaînes nues** ;
**les 10 chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
candidates** ; **les 6 clés sans lecture observée** ; **les 26 routes à lectures
ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ;
**les 5 routes affamées du 556** ; **les 14 candidates du 554, en attente d'un
GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du
554/555** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly` rend un
objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 199 (+1)** ;
**publiés puis corrigés 35 (+1)** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
