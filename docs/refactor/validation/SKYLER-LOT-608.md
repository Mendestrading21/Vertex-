# SKYLER — LOT 608 · UN ÉTAT VIDE QUI SAIT QU'IL N'EST PAS SYNCHRONISÉ

Le 607 a posé `VX.store.desk_sync` et affiche un **toast** : transitoire, global,
et parti avant que l'utilisateur n'arrive sur la zone. Ce lot met la mention
**là où la conviction se forme**.

## Le vrai travail était de ne PAS corriger trop large

Le brief demandait de mesurer avant d'agir, et il avait raison. **Sur les états
vides du produit, la grande majorité vient d'un moteur serveur** — « Secteurs non
calculés par le dernier scan », « Registre de jobs vide », « Aucun titre
scanné ». Y coller « bureau non synchronisé » serait **un mensonge d'un autre
genre** : exactement la faute que la boucle corrige depuis le 602, commise à
l'envers.

D'où un état **séparé**, `VX.states.emptyDesk`, et non une modification de
`VX.states.empty` — qui aurait menti sur la majorité des zones.

**21 zones basculées**, sur 5 fichiers : positions, alertes, suivis, watchlist,
options, thèse, entrées de journal, hypothèses, erreurs, leçons, états
émotionnels, trades réels, coffre, courbe d'équité, drawdown, saisonnalité.

## Trois instruments, trois corrections — le compte a bougé à chaque fois

| instrument | attribution | résultat | verdict |
| --- | --- | --- | --- |
| 1ᵉʳ | « la déclaration de fonction la plus proche en amont » | **43 sur 59 « ni bureau ni serveur »** | **faux** — il rattachait chaque état vide à un helper de deux lignes (`pos`, `srv`, `mk`, `kpi`, `$`) |
| 2ᵉ | fonction de **premier niveau** (colonne 0) | 6 bureau · 13 mixtes · 39 serveur | **incomplet** |
| 3ᵉ | + `E()` reconnu comme alias de `VXEntities` | **le double de zones bureau** | juste |

Le premier était **607-C**, la règle écrite au lot précédent : *une heuristique
positionnelle sur du code est fragile*. La proximité ne dit pas l'englobement.

Le deuxième ratait `E()` — `const E=()=>window.VXEntities;`, l'alias local des
quatre pages qui touchent le bureau. **Sans lui, tout `/journal` passait pour du
serveur** alors que ses hypothèses, erreurs, leçons et états émotionnels lisent
tous `vxJournal`.

## L'arrêt du lot — j'ai décidé sur une sortie tronquée

Entre le 2ᵉ et le 3ᵉ instrument, j'ai lu la classification **avec `head -40`** et
conclu que `/journal` ne portait que deux états vides. Il en porte **dix**. Les
huit autres étaient dans la partie coupée.

Ce n'est pas l'instrument qui a menti, **c'est ma lecture de sa sortie**. Le
défaut a été rattrapé parce qu'une passe navigateur a montré `/journal` avec des
états vides que je croyais avoir traités.

**Arrêtés avant publication : 240 → 241 (+1).**

## Le contrôle, deux fois vide avant d'être décisif

Il fallait prouver que la mention **n'apparaît pas** là où elle serait fausse.

- **1ᵉʳ jet — `/markets`** : 0 mention. **Mais 0 état vide affiché** : le contrôle
  passait à vide (**600-A**).
- **2ᵉ jet — `/system?view=connections`** : 0 mention, **0 état vide** encore.
  Mon propre garde-fou (`v4 > 0`) a refusé le verdict.
- **3ᵉ jet — `/journal?view=track-record`, la MÊME page, sous la MÊME panne** :

| | états vides | dont avec mention | dont sans |
| --- | --- | --- | --- |
| `/journal?view=track-record`, GET 500 | **2** | **1** *(« aucun trade réel déclaré » — bureau)* | **1** *(« pas assez de verdicts résolus » — moteur)* |

**Sur le même écran, sous la même panne, un vide parle et l'autre se tait.** Si
la mention était posée trop large, elle serait sur les deux. C'est la preuve que
le correctif est **ciblé**, pas seulement présent.

## La preuve complète, en vrai Chromium

Quatre passes, profil neuf, service worker bloqué (**602-B**) :

| passe | états vides | mentions |
| --- | --- | --- |
| `/journal?view=journal` **nominal** | 2 | **0** *(témoin immobile, 606-B)* |
| `/journal?view=journal` **GET 500** | 2 | **2** |
| `/journal?view=track-record` **nominal** | 2 | **0** |
| `/journal?view=track-record` **GET 500** | 2 | **1** *(le contrôle)* |

Le `GET /api/desk` a eu lieu sur les **quatre** passes : la voie est **exercée**
(602-A).

## Le gardien, rouge dans les DEUX sens

`tests/test_etats_vides_bureau_lot608.py` — **6 tests**. Vérifié par mutation
**des deux côtés**, ce qui est plus fort qu'un seul :

- **retirer** la mention d'une zone du bureau → `test_les_zones_du_bureau_disent_la_desynchro` échoue ;
- **ajouter** la mention à une zone du moteur → `test_les_zones_du_moteur_ne_mentent_pas` échoue.

Un gardien qui n'attrape que la sous-application laisserait passer la
sur-application — le mensonge inverse. Plus un **garde-fou de volume** (591-C)
sur les deux familles, et un test qui exige que `emptyDesk` **ne dise rien**
quand `desk_sync` vaut `'ok'` : un avertissement permanent ne veut plus rien dire.

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « une minorité des états vides dépend du bureau — moins d'un tiers » | **CONFIRMÉ** — 21 sur 59, ~36 % *(la borne « moins d'un tiers » est frôlée, pas franchie nettement)* |
| **(b)** | « concentrés sur `/journal` et `/portfolio` » | **CONFIRMÉ en majorité** — 16 des 21 ; mais `/`, `/analysis` et `/system` en portent aussi |
| **(c)** | « `VX.states.empty()` est le point unique à modifier » | **RÉFUTÉ** — le modifier aurait menti sur 38 zones ; il fallait un état **voisin**, pas un état **modifié** |
| **(d)** | « la distinction est lisible dans le code sans exécuter » | **CONFIRMÉ, au troisième instrument** |
| **global** | | **CONFIRMÉ, sauf (c) — et (c) était le volet décisif** |

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure les appels à `VX.states.empty`. Le cas exclu : **les états
vides qui n'y passent pas** — HTML écrit à la main, ou `states.error` employé
pour dire un vide.

Contrôlé sur le rendu : la passe navigateur compte les nœuds
`[data-state="empty"]`, **pas les appels dans la source**. Les comptes
concordent (2 zones vues = 2 zones attendues sur les deux vues de `/journal`),
ce qui borne le risque d'états vides échappant au dispositif — **sans l'annuler**
pour les vues non parcourues.

## Ce que le lot n'établit pas

- **Que les 21 zones soient exactement les bonnes.** C'est une **lecture**, zone
  par zone, du code qui alimente chaque vide. Chaque ligne est vérifiable ;
  aucune n'est produite par un programme.
- Que les 8 zones « mixtes » restantes soient bien du serveur : elles ont été
  lues une par une (prix, anomalie, TradingView, chaîne d'options, plan de
  niveaux, scan) — **lecture, pas mesure**.
- **La fréquence réelle d'un `GET /api/desk` en échec.** Injectée, pas rencontrée.
- Que la mention soit lisible sur mobile : mesurée à 1440×900 seulement.

## Règles neuves

- **608-A — UN CORRECTIF D'HONNÊTETÉ DOIT ÊTRE PLUS ÉTROIT QUE LA FAMILLE QU'IL
  VISE.** 59 états vides, 21 concernés. Modifier le point commun aurait menti sur
  38. Un état **voisin** vaut mieux qu'un état **élargi**.
- **608-B — UN GARDIEN D'HONNÊTETÉ DOIT ÊTRE ROUGE DANS LES DEUX SENS.** Trop peu
  de mentions est un défaut ; trop de mentions en est un autre, symétrique et
  aussi grave. Un gardien qui n'attrape qu'un côté autorise l'autre.
- **608-C — LIRE UNE SORTIE TRONQUÉE, C'EST MESURER AUTRE CHOSE.** `head -40` sur
  une classification m'a fait conclure que `/journal` portait deux états vides ;
  il en porte dix. L'instrument était juste, la lecture non.

## Ce que le dépôt fait bien

- **`VX.states` était déjà le point de passage unique** des états vides : la
  famille existait, il ne manquait qu'un membre.
- **Les messages existants sont déjà précis** — « le journal est la seule source
  de cette section », « renseigne le champ *erreur* à chaque sortie perdante ».
  La mention s'ajoute à une phrase qui disait déjà d'où vient le vide.
- **`emptyCard` de `/portfolio` acceptait un paramètre de plus sans réécriture** :
  trois de ses quatre appels sont du bureau, le quatrième dit « IBKR hors ligne »
  et reste au serveur. La distinction tenait déjà dans les mots.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **6 fichiers de production** : `vx-core.js` (état neuf) + `briefing.py`,
  `portfolio_page.py`, `analysis_page.py`, `performance_page.py`,
  `system_page.py` (21 bascules) + `system.py` (bump).
- **1 gardien neuf** (6 tests, **rouge dans les deux sens**) + **5 épingles**
  `td-shell-v192` → **`td-shell-v193`** + empreinte des assets et `_SW_VERSION`
  du gardien 361.
- MD5 des 8 pages : **4 / 8 identiques** — `/` **`409f3448505b`**, `/portfolio`
  **`d147c3031af0`**, `/journal` **`f70ee8986706`**, `/system`
  **`184653f28900`** bougent ; `/markets`, `/opportunities`, `/analysis` et
  `/options` sont identiques à l'octet. *(Les deux bascules d'`analysis_page.py`
  sont sur `/analysis/<sym>`, hors des 8 empreintes.)*
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2887 passed / 0 skipped** *(2881 + les 6 du gardien neuf)*.
- Navigateur : **4 passes**, dont un contrôle **deux fois refusé pour vacuité**
  avant d'être décisif.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **241 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 7**
