# SKYLER LOT 535 — **Aucune barre de chargement éternelle.** Les 63 conteneurs qui portent un squelette ont tous du code qui les remplit. Et deux « coupables » ont été disculpés par la restriction que j'avais nommée d'avance

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-535` (base : lot 534 fusionné,
`04fbe766`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(x)** — se servir de l'analyseur du 534 sur une question que lui seul peut
trancher. Le produit annonce un chargement par un `vx-skeleton` ; le 530 a
mesuré que 31 vues sur 35 en portent au moins un. **Personne n'avait vérifié
qu'un code existe pour remplir chacun de ces conteneurs.**

L'enjeu est plus grave que le 531-A : un squelette que personne ne remplit,
c'est une barre de chargement perpétuelle **en marche normale**, sans qu'aucune
panne réseau ne soit nécessaire.

## Deux vrais analyseurs, pas un seul

Le JavaScript par acorn (113 programmes, 3 345 728 octets, **zéro erreur**), et
**le HTML par `html.parser`** : le conteneur d'un squelette est **le plus proche
ancêtre portant un `id`** — pas ce qui suit un `id=` dans une fenêtre de N
caractères. Le 534 vient de montrer ce que coûte une fenêtre fixe (**534-B**).

```text
CALIB 1 · REGISTRES   35 vues, slugs lus dans les registres              OK
CALIB 2 · POSITIF     `op-body` porte un squelette et est visé            OK
CALIB 3 · NÉGATIF     un identifiant FABRIQUÉ n'est visé par personne     OK
CALIB 5 · le `$` de `chart.umd.min.js` est ÉCARTÉ                         OK
CALIB 6 · le `$` des scripts en ligne est RETENU                          OK
```

## Premier arrêt — **`$` n'est pas toujours le `$` du produit**

Mon premier jet comptait **tous** les `$(…)` du corpus servi. Or le corpus
contient `/static/chart.umd.min.js`, 205 125 octets, qui déclare **son propre
`$`** :

```js
function $(t){return t*(C/180)}      // degrés → radians
```

**Compte gonflé : 220 « sélecteurs construits » au lieu de 132.** C'est la
famille **521-B / 532-A**, cette fois sur le `$` lui-même — et un analyseur n'en
protège pas : il a fallu résoudre `$` **par programme**, en ne le retenant que si
sa liaison contient un `getElementById`.

## Second arrêt — **la restriction que j'avais nommée d'avance a disculpé mes deux seuls coupables**

Le crible a d'abord rendu **deux conteneurs jamais référencés** :

```text
/markets?view=breadth   vx-mk-breadth-gauge
/system                 vx-sys-gauge
```

**Le dossier était là.** Sauf que la règle **481** m'obligeait à nommer, *avant
de mesurer*, ce que l'instrument ne peut pas voir : **les sélecteurs
construits**. Vérification par lecture du code servi :

```js
VXCharts.gauge('vx-sys-gauge', { value:_pct, min:0, max:100, label:'Moteurs OK', … })
VXCharts.gauge('vx-mk-breadth-gauge', { value:brNum, …, label:'> MM50', … })
emptyCard('vx-mk-breadth-gauge', 'Participation non calculée par le dernier scan.', SCAN_ACTION)
```

**L'identifiant n'est pas visé, il est CONFIÉ.** Le constructeur le résout
lui-même, par l'un des 132 sélecteurs construits. **Les deux conteneurs sont
remplis — et `vx-mk-breadth-gauge` a même un état vide honnête.**

**Arrêtés avant publication : 146 → 148.**

## La mesure, après les deux corrections

```text
63 conteneurs distincts portant un squelette, sur 43 URL servies

   visés DIRECTEMENT (`$('id')` / `getElementById('id')` littéral)   61
      dont ÉCRITS (affectation directe ou par liaison)               61
   CONFIÉS à une fonction (littéral passé en argument)                2
   INTROUVABLES dans le JS servi                                      0
```

**Aucun squelette servi n'est orphelin.** Et les 61 visés directement sont
**tous** écrits : pas un seul conteneur n'est simplement lu.

## Ce que le dépôt fait bien, mesuré

- **63 conteneurs sur 63 ont du code qui les remplit.** Le contrat
  « squelette = chargement en cours » est **tenu partout**.
- **61 sur 61 des conteneurs visés directement sont ÉCRITS**, pas seulement lus :
  l'annonce de chargement correspond à une écriture réelle.
- **`vx-mk-breadth-gauge` porte un état vide honnête** —
  « Participation non calculée par le dernier scan. » avec un lien d'action —
  au lieu de laisser tourner sa jauge.
- **113 programmes servis, zéro erreur de syntaxe**, deuxième lot consécutif.

## Portée — ce que ce lot NE dit PAS

- **Il prouve qu'un code EXISTE pour remplir chaque conteneur, pas que ce code
  s'exécute toujours.** Le 531-A reste entier : quatre chargeurs
  d'`/opportunités` n'écrivent rien **en cas de panne**.
- **132 sélecteurs construits et 279 `querySelector` échappent à l'analyseur.**
  Un conteneur écrit uniquement par eux serait invisible à ce crible — c'est
  exactement ce qui a sauvé les deux « coupables », et ça vaut dans l'autre sens.
- « Écrit » couvre l'affectation directe et l'idiome
  `const el = $('id'); el.innerHTML = …` ; une écriture passant par un troisième
  détour n'est pas suivie.
- Les conteneurs **sans** squelette ne sont pas dans le périmètre.
- **Aucun navigateur, aucun réseau, aucune correction engagée.**

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
0, 3, 0, 0, 0, 0**.

Aucun dossier — et c'est le bon résultat. La question posée était grave : un
squelette orphelin aurait été un défaut visible **sans aucune panne**. La
réponse est nette : **il n'y en a pas un seul**.

Ce qu'il faut dire sans le maquiller : **j'ai failli publier un dossier de plus,
et ce n'est pas ma prudence qui l'a évité, c'est une règle écrite** — la 481, qui
oblige à nommer la restriction de l'instrument **avant** de mesurer. Sans elle,
« deux conteneurs jamais référencés » partait en dossier.

Trois règles neuves :

- **535-A · UN IDENTIFIANT PEUT ÊTRE CONFIÉ, PAS VISÉ** — chercher `$('id')` ne
  suffit pas ; `VXCharts.gauge('id', …)` remplit le conteneur sans jamais écrire
  `$('id')`.
- **535-B · `$` N'EST PAS TOUJOURS LE `$` DU PRODUIT** — un homonyme minifié
  dans une bibliothèque servie a gonflé le compte de 132 à 220.
- **535-C · LE HTML AUSSI MÉRITE UN ANALYSEUR** — le conteneur d'un squelette
  est le plus proche ancêtre portant un `id`, pas ce qui suit un `id=` dans une
  fenêtre de caractères.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, inchangée).

Dettes nommées restantes : **`loadLeaps`** ; **`loadStructure` et ses 7
caractères** ; **les 132 sélecteurs construits et 279 `querySelector`, hors de
portée du crible** ; **la définition du corpus de routes du 511-A** ; **l'ampleur
du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ;
**les 33 identifiants reconstruits** ; **les 92 rapports non additionnés du
526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ;
**mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 148 (+2)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
