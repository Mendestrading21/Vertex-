# SKYLER LOT 581 — **quatre vocabulaires d'état**, et le `—` honnête est écrit à l'endroit exact où l'âge est inconnu

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-581` (base : lot 580 fusionné,
`c9684fa4`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(aaa)** — le 580 a trouvé `VX.freshness` en lisant le contexte d'un nom, en a
relevé 8 noms, et n'a jamais suivi ce qu'ils affichent. Or cette famille touche
l'invariant le plus fort du dépôt : **« donnée absente → `—`/`n/d` honnête »**.

Deux pièges écrits **avant** de mesurer : *(a) l'un des huit noms n'aura pas de
libellé — `unknown` est rendu par un `return` direct portant `label: '—'`, et ce
tiret est précisément le « — honnête » de l'invariant. (b) `chip()` pose
`data-state=` par **concaténation** : tout comptage littéral rendra **zéro**
alors que le produit en pose — ne pas conclure d'un zéro littéral à une absence.*

**Les deux sont vérifiés.**

## Piège (a) — vérifié : **sept libellés pour huit noms**

```text
nom          libellé affiché    ordre de décision, lu dans `assess`
offline      'Hors ligne'       1er  si o.offline
error        'Erreur'           2e   si o.error
refreshing   'Recalcul…'        3e   si o.refreshing
saved        'Sauvegardé'       4e   si o.saved
unknown      (ABSENT de LABEL)  5e   si ageMs == null  →  label: '—'
live         'Live'             6e   si o.live && âge < 20 s
snapshot     'Analyse'          7e   si âge < 30 min
stale        'À actualiser'     8e   sinon
```

**`unknown` est le seul nom sans libellé** — et c'est volontaire : quand l'âge
n'est **pas connu**, `assess` court-circuite la table et renvoie `label: '—'`.

L'invariant produit n'est pas seulement respecté : **il est écrit à l'endroit
exact où il compte**, dans la branche `ageMs == null`, avant toute tentative de
classer la donnée. Le produit ne dit pas « Live » par défaut, ni « À actualiser » :
il dit **`—`**.

## Piège (b) — vérifié : **zéro littéral, et pourtant six valeurs posées**

```text
data-state="live"        0        data-state="offline"     0
data-state="saved"       0        data-state="unknown"     0
data-state="snapshot"    0        data-state="stale"       2  ← autres familles
data-state="refreshing"  0        data-state="error"       2  ← autres familles
```

`chip()` construit l'attribut par concaténation :

```javascript
chip(a) { … return '<span class="vx-fresh-chip" data-state="' + a.state + '" …' }
```

Un relevé littéral aurait conclu **« la famille fraîcheur n'atteint jamais le
DOM »**. Elle l'atteint par **8 sites d'appel distincts** (`assess` 4 · `chip` 4,
sur `/markets`, `/opportunities`, `/portfolio`, `/system`). Et les deux valeurs
non nulles (`stale`, `error`) viennent des **autres** familles — pas de
celle-ci.

## L'arrêt du lot — **j'ai cherché le nom que le brief m'avait donné**

Mon banc a rendu « `_freshness` **absente** des octets servis ». C'est faux comme
conclusion : la fonction existe, elle s'appelle **`C.freshnessBadge`**.

J'avais cherché `_freshness` **parce que le brief l'appelait ainsi**. Le brief est
une source comme une autre — et je n'ai pas lu le nom, je l'ai recopié. C'est
**521-B appliqué à moi-même**, sur la source la plus proche de moi.

**Arrêtés avant publication : 207 → 208 (+1).**

## Le quatrième vocabulaire, correctement nommé — `C.freshnessBadge`

```text
nom d'entrée   valeur `data-live=`   libellé affiché
live           live                  'Live'
delayed        delayed               'Différé'
stale          frozen                'Périmé'
demo           fallback              'Démo'
offline        offline               'Hors ligne'
missing        offline               'Indisponible'

repli : map[f] || ['fallback', freshness]
```

Trois observations, mesurées :

- **Un nom d'état n'est pas sa valeur d'attribut** : `stale → frozen`,
  `demo → fallback`, `missing → offline`.
- **Deux noms tombent sur la même valeur** (`offline` et `missing` → `offline`)
  **tout en gardant deux libellés distincts** — « Hors ligne » et
  « Indisponible ».
- **Le repli affiche la valeur inconnue telle quelle.** Rien n'est inventé —
  mais le libellé n'est alors plus une chaîne française contrôlée.

## Les deux familles de fraîcheur, croisées **par nom**

```text
(3) VX.freshness      (8)  error, live, offline, refreshing, saved,
                           snapshot, stale, unknown        → data-state=
(4) freshnessBadge    (6)  delayed, demo, live, missing,
                           offline, stale                  → data-live=

communs          live, offline, stale
propres à (3)    error, refreshing, saved, snapshot, unknown
propres à (4)    delayed, demo, missing
```

Deux vocabulaires de fraîcheur, **deux attributs différents**, trois mots
communs. Avec les deux familles d'états de rendu du 580, cela fait **quatre
vocabulaires** — et **`stale` est le seul mot présent dans les quatre**.

## Second contrôle (481) — le site unique qui couvre tout l'écran

```text
appelants de `freshnessBadge`   1 occurrence · 1 fichier
   /static/vertex/js/charts/chart-core.js
```

**Un seul site d'appel** — mais il est **dans `C.card`**, le constructeur de
carte canonique. Chaque carte-graphique du produit rend donc ce badge. C'est la
démonstration littérale de ce que le 579 énonçait : **un compte d'appels n'est
pas une surface d'écran** — ici, 1 appel couvre plus que les 8 de la famille
voisine.

Et `data-live="…"` en littéral : **zéro**, pour la même raison qu'au piège (b).

## Ce que le dépôt fait bien, mesuré

- **Le `—` honnête est à l'endroit exact** : `ageMs == null` court-circuite la
  table avant toute classification. C'est l'invariant produit, écrit dans le
  code, au point le plus délicat.
- **L'ordre de décision d'`assess` est lisible et défendable** : l'indisponible
  et l'erreur passent **avant** l'âge ; on ne calcule pas une fraîcheur sur une
  donnée qu'on sait absente.
- **Sept libellés français** pour sept états connus — aucun mot anglais à
  l'écran, alors que les clefs internes sont anglaises.
- **Les seuils sont écrits en clair** (20 s / 30 min / 35 min) et commentés comme
  alignés sur la cadence de la session d'analyse.
- **Le repli du badge n'invente rien** : il affiche la valeur reçue plutôt que de
  la traduire en une étiquette fausse.

## Portée — ce que ce lot NE dit PAS

- Les libellés sont **lus dans les tables**, pas observés à l'écran.
- **Aucun défaut n'a été constaté** : les quatre vocabulaires coexistent, ce lot
  mesure leur forme, pas leur effet.
- Le repli `['fallback', freshness]` est signalé **par sa forme** — aucune valeur
  inconnue n'a été observée en circulation.
- **Rien n'est corrigé** : les quatre vocabulaires restent, les trois renommages
  restent, le repli reste.
- Corpus du 541 : **plancher**, DÉMO sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu**, une variable par objet ; aucun banc antérieur touché — celui qui a
  cherché `_freshness` **reste tel quel**, c'est la preuve de l'arrêt.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- MD5 des 8 pages remesurés : **8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu
  ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **c'est le premier lot où la mesure confirme l'invariant
produit au lieu de mesurer un instrument.** Depuis le 570, je comptais des
canaux, des fabriques, des vocabulaires ; ici, j'ai trouvé la ligne exacte où le
dépôt tient sa promesse — `if (a == null) return { state: 'unknown', label: '—' }` —
et elle est placée **avant** toute tentative de classer. Ce n'est pas un hasard
d'écriture : c'est un ordre de décision choisi.

Et une leçon désagréable : **j'ai cherché un nom que le brief m'avait soufflé.**
Le brief se trompait, mon banc a répondu « absente », et j'ai failli publier
l'absence d'une fonction qui existe et qui est appelée dans le constructeur de
carte canonique. La source la plus proche de soi est la plus facile à ne pas
vérifier.

Trois règles neuves :

- **581-A · LE MOT D'UN BRIEF N'EST PAS LE NOM DU CODE** — j'ai cherché
  `_freshness` ; la fonction s'appelle `freshnessBadge`.
- **581-B · UN NOM D'ÉTAT N'EST PAS SA VALEUR D'ATTRIBUT** — `stale → frozen`,
  `demo → fallback`, `missing → offline` ; deux noms tombent sur la même valeur
  avec deux libellés différents.
- ~~**581-C · UN SEUL SITE D'APPEL PEUT COUVRIR TOUT L'ÉCRAN** — `freshnessBadge`
  est appelée **une fois**, dans le constructeur de carte canonique.~~

  > ⚠ **CORRECTION (lot 64) — 581-C ÉTAIT FAUX, ET SON ÉNONCÉ EST À RETOURNER.**
  >
  > La conclusion tirée ici était : *« un seul site d'appel, mais il est dans
  > `C.card` — **chaque carte-graphique du produit rend donc ce badge** »*.
  > C'est l'inverse, mesuré des deux côtés :
  >
  > - statiquement, `opts.freshness` n'était passé par **aucun** appelant du
  >   produit, et la fonction rend `''` sans valeur ;
  > - au navigateur, **4 cartes-graphiques peintes, 0 badge de fraîcheur**.
  >
  > Le raisonnement sur la **portée** du site d'appel était juste ; il a été
  > appliqué à un appel **qui ne produit rien**. Ce lot venait précisément de
  > corriger « un compte d'appels n'est pas une surface d'écran » — et a commis
  > aussitôt le défaut symétrique :
  >
  > **581-C (corrigé) · UNE PORTÉE N'EST PAS UNE SORTIE.** Un site d'appel bien
  > placé ne prouve rien tant qu'on n'a pas vérifié qu'il **produit** quelque
  > chose. Compter les appels, puis mesurer leur portée, puis oublier de
  > regarder l'écran : trois étapes, et l'erreur s'est déplacée à chaque fois
  > d'un cran sans jamais atteindre le seul juge qui compte.
  >
  > `C.freshnessBadge` a été **retirée** au lot 64 — retrait à rendu identique,
  > puisque la branche était inatteignable. Voir
  > `SIGNAL-OS-64-CONTRAT-CHART-SHELL.md`. Cela referme aussi une des « dettes
  > nommées » ci-dessous : les quatre vocabulaires d'état passent à trois.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les quatre vocabulaires d'état, coexistants et NON
unifiés** ; **les trois renommages nom → attribut** ; **le repli
`['fallback', freshness]` qui affiche une valeur inconnue telle quelle** ; **les
8 sites de `VX.freshness`, comptés et non suivis jusqu'à l'écran** ;
**l'ambiguïté de `data-state=` entre trois familles** ; **les 3 branches de
`_stateBody` qui ne délèguent pas** ; **`VX.states.stale`, morte et NON
supprimée** ; **les 73 appels à `empty`, comptés et non lus** ; **les 30 appels à
la fabrique d'erreur** ; **les 2 appels à « identifiant nu »** ; **les 6
bannières qui relaient `e.message`** ; **le repli « réponse indisponible »** ;
**les 38 sites du relevé structurel neuf du 576** ; **les 29 branches de produit
de la borne (B) neuve** ; **le filtre `chart.umd` des six instruments** ; **les 8
programmes d'`/analysis/AAPL`, non lus ligne à ligne** ; **les 269 branches qui
s'arrêtent sans rien dire** ; **les 14 sites « ailleurs » du 573** ; **les 19
toasts d'erreur littéraux** ; **les 6 toasts sans ton** ; **`warn` et `warning`,
non unifiés** ; **les 23 toasts `success`** ; **les 57 sites qui ne signalent pas
un échec** ; **le total réel des signalements d'échec, toujours inconnu** ; **les
27 appelés du relevé structurel du 570** ; **les 82 corps vides du 569, NON
JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ; **les 42 refus du 567** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 208 (+1)** ;
**publiés puis corrigés 38** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
