# SKYLER LOT 574 — les refus de saisie : **deux nombres égaux, deux ensembles différents**, et un corpus qui n'a jamais vu **les 35 vues**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-574` (base : lot 573 fusionné,
`aa514747`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix

**(tt)** — le 573 a fait apparaître un registre que quatre lots avaient traversé
sans le voir : **le produit refuse des saisies, et il le dit**. Il en annonçait
« au moins dix-sept ». Ce lot inventorie l'objet pour lui-même.

Piège écrit **avant** de mesurer, et vérifié comme le reste (568-B) : **le « 17 »
du 573 est un plancher tiré d'un sous-ensemble** — les 30 sites « garde négative
+ promise-catch » **du canal de notification**. Le publier comme un total serait
exactement 570-A.

Contre-mesure : balayer **tous** les `if` à test négatif du corpus, quel que soit
ce qu'ils déclenchent, puis dire combien touchent le canal et combien non —
**deux bornes, comme au 570**.

## L'arrêt du lot — **un témoin lu dans la SOURCE n'est pas un témoin dans le SERVI**

Deux témoins avaient été lus dans le code avant toute mesure. Le premier ressort.
Le second, non :

```javascript
// vertex/ui/pages/analysis_page.py
if (!(a > 0)) { VX.toast && VX.toast('Montant envisagé requis', 'warn'); … }
```

`/analysis` **est** l'une des 8 pages. La chaîne est pourtant **absente du
corpus** :

```text
'Montant envisag'      -> ABSENT du corpus servi
'Ticker invalide'      -> /journal :: inline#1, /static/…/options-gex.js, …
'Position introuvable' -> /static/vertex/js/vx-entities.js
corpus : 8 pages · 105 programmes analysés, 0 erreur
```

Raison, vérifiée : le corpus a été construit en appelant les 8 pages **à leur URL
de base**. **Les 35 vues (`?view=…`) n'y sont pas.** Un écran qui ne se rend que
pour une vue n'a **jamais** été mesuré — ni au 539, ni au 540, ni au 541, ni dans
les lots 569 à 574 qui réutilisent ce corpus.

L'attente a donc été **réécrite et vérifiée** : le second témoin doit être
**absent**. C'est une borne de portée qui touche **six lots**, pas une anomalie
de ce lot-ci.

**Arrêtés avant publication : 199 → 200 (+1).**

## Les deux bornes — **aucune n'est un recensement**

```text
(A) branche appelant le CANAL                  25
(B) branche contenant un `return`             290
    dans les DEUX                              21
    dans (A) seulement — parle sans s'arrêter    4
    dans (B) seulement — s'arrête sans rien dire 269
    union des deux bornes                     294
```

(A) ne voit que **ce qui parle**, (B) que **ce qui s'arrête**. **269 branches
arrêtent la fonction sans rien afficher** : ce n'est pas un défaut en soi — un
`return` précoce est souvent un simple garde-fou de flux — mais c'est la mesure
qui dit pourquoi un inventaire « par le canal » ne peut pas être un total.

Nuance vérifiée avant publication : la borne (A) compte des **branches**, et
**une d'entre elles est un `else`** (`if (G && brNum != null) { gauge } else
{ emptyCard(…) }`). Le test négatif décrit alors le **`if`**, pas la branche
retenue — 573-B, sous une autre forme. La branche reste une absence honnête,
donc le compte ne bouge pas ; c'est l'étiquette qui aurait menti.

## Ce que le refus refuse — **forme du test, relevée, jamais devinée**

```text
forme                    (A) canal   (B) return
expression regulière            3           4
Number / isNaN                  1           2
comparaison numérique           2          20
.length                         4          58
appartenance                    0           5
vérité simple                  15         201
                             ────        ────
                               25         290
```

## Le cœur du lot — **25 = 25, et pourtant 24 en commun**

Le 573 publie « garde négative **25** ». La borne (A) rend **25**. Écrire « ce
sont les mêmes » sans mesure aurait été **546-A**. Croisé sur la clé du 573 —
`(fichier, position de l'APPEL)`, via un **banc séparé** (on ne touche jamais à
un banc déjà écrit) :

```text
appels du canal sous test négatif — banc 574   25
classe « garde negative » du 573               25
      dans les deux                            24
      seulement dans le banc 574                1   setNet('offline')  — DANS un `catch`
      seulement dans le 573                     1   bannière `vx-error-banner`
```

**Deux différences, en sens contraire, qui se compensent exactement — par
coïncidence.** Le 573 excluait `setNet('offline')` parce qu'il ne comptait que
les sites **hors `catch`** ; mon relevé l'exclut de rien mais ignore le genre
**bannière**, absent de mon ensemble de quatre noms. Deux instruments, deux
angles morts, **le même nombre**.

C'est aussi ce qui rend la borne (A) **plancher dans son propre corpus** : elle
ne connaît que `VX.toast` / `emptyCard` / `setNet` / `setStatus`, quand le canal
du 570 en comptait six genres.

## Un second arrêt — **une valeur enregistrée se lit, elle ne se cite pas**

Le premier croisement a rendu « **0 en commun** ». Cause : le rapport 573
**imprime** « garde négative » (accentué) ; le banc **stocke** `'garde negative'`
(sans accent). Filtrer sur la chaîne du **rapport** rendait un ensemble vide, et
j'allais publier deux ensembles disjoints là où 24 sites sur 25 coïncident.

C'est **545 appliqué à une valeur** et non à une clé : ne jamais deviner la forme
d'une structure enregistrée — l'**ouvrir**. Le banc lit désormais les classes
réellement présentes et échoue si la classe attendue n'y est pas.

**Arrêtés avant publication : 200 → 201 (+1).**

## Ce que les 25 refusent — **lecture, site par site**

Classement **lu dans le code**, pas dérivé d'un prédicat ; le programme vérifie
seulement que la lecture couvre **exactement** les 25, et mesure le ton :

```text
SAISIE   ce que l'utilisateur vient de taper / choisir / importer   12
ABSENCE  une donnée attendue n'est pas là                           10
ÉTAT     réseau / session — ni refus ni absence                      3
                                                                   ──
                                                                    25

ton mesuré : error 16 · sans ton lisible 6 · warning 1 · warn 1 · info 1
```

Les douze **SAISIE**, lues : `Ticker invalide` (×3, trois fichiers), `Quantité
invalide`, `Niveau requis`, `Titre requis`, `Montant de sortie requis`, `P&L
requis quand un résultat est déclaré`, `Position invalide (ticker/quantité)`,
`Écris une question`, `Structure inattendue — export desk attendu`, `Aucune clé
desk reconnue dans ce fichier`.

## La correction — **le « 17 » du 573 ne comptait pas des refus de saisie**

```text
sites à ton `error` DANS la borne (A)     16
   dont SAISIE                            11
   dont ABSENCE                            5   « Prime indisponible — suivi
                                               impossible », « Position
                                               introuvable » (×4)
```

Le 573 écrivait « le canal en compte au moins dix-sept ». Ce 17 était le compte
des toasts **à ton `error`** parmi 30 sites — un seau défini par le **ton**, pas
par la nature. Cinq d'entre eux annoncent une **donnée manquante**, pas un refus
de saisie. Et le dix-septième n'est même pas dans la borne (A) : il vient du
groupe `.catch(` de promesse.

**Le compte lu est 12 refus de saisie**, dont 11 à ton `error`.

C'est le même défaut que 573-B, d'un cran plus haut : le 573 avait bien vu que
nommer un seau d'après son **test** ment sur l'issue — puis a nommé un seau
d'après son **ton**.

**Publiés puis corrigés : 35 → 36 (+1).**

## Second contrôle (481) — le versant serveur, unité déclarée

```text
refus JSON distincts mesurés au 567   42
refus client de la borne (A)          25
```

**Les deux ne se comparent pas terme à terme** (570-C) : un refus serveur est un
`return jsonify(…), 4xx` — une **sortie de route** ; un refus client est un
**appel dans une branche**. Deux objets, deux unités. Ce qui se compare
honnêtement, c'est la **présence des deux moitiés** : le produit refuse **des
deux côtés**, et les deux le disent. Le croisement nom à nom demanderait de lire
les 42 messages serveur — le 567 l'avait explicitement laissé ouvert, et ce lot
ne le fait pas non plus.

## Ce que le dépôt fait bien, mesuré

- **La validation de saisie est explicite et précoce** : douze refus nommés, onze
  au ton `error`, **avant** tout appel réseau.
- **Le refus est spécifique** : `Niveau requis`, `Quantité invalide`, `Montant de
  sortie requis` nomment le champ, pas « erreur ».
- **Le refus existe des deux côtés** : 42 refus JSON au serveur, 12 refus de
  saisie au client — le client ne délègue pas sa validation au réseau.
- **Trois fichiers différents refusent un ticker avec la même grammaire**
  (`/^[A-Z.\-]{1,7}$/`, `{1,12}` sur options) : la règle est écrite là où la
  saisie a lieu.

## Portée — ce que ce lot NE dit PAS

- **Le corpus est celui des 8 pages à leur URL de base.** Les 35 vues en sont
  absentes : tout chiffre de ce lot est un **plancher d'écran**, pas un total
  produit.
- **La borne (A) ignore trois genres du canal** (bannière, `dataset.state`, et ce
  qui n'est pas dans les quatre noms) : plancher aussi de ce côté.
- **La classification SAISIE / ABSENCE / ÉTAT est une lecture**, reproductible
  par relecture, pas par exécution d'une règle.
- Les **269 branches qui s'arrêtent sans rien dire** sont comptées, **pas
  jugées** : un `return` précoce n'est pas un défaut.
- **Rien n'est corrigé** : les messages restent tels qu'ils sont écrits, le « 17 »
  du 573 reste écrit là où il l'est, la correction est en ajout.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON, bancs
  écrits **en fichier**, jamais en `python3 -c`.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : **8 / 8 identiques.****
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Sixième lot sur le canal de notification.

Ce que je retiens : **deux instruments peuvent rendre le même nombre en ne
voyant pas la même chose.** 25 et 25, 24 en commun, et les deux différences
s'annulaient. Sans le croisement, j'aurais écrit « le 573 et le 574 mesurent le
même objet » — une phrase juste à 96 %, et fausse comme méthode. Le seul moyen de
le savoir a été d'ouvrir la structure du lot précédent et de croiser **par
identité de site**, pas par égalité de compte.

Et une borne de portée, qui vaut pour six lots : **le corpus de 539 à 574 est un
corpus de pages, pas d'écrans**.

Trois règles neuves :

- **574-A · UN CORPUS DE PAGES N'EST PAS UN CORPUS D'ÉCRANS** — les 8 pages ont
  été prélevées à leur URL de base ; **les 35 vues n'y sont pas**. Un témoin lu
  dans la **source** n'est pas un témoin présent dans le **servi**.
- **574-B · DEUX NOMBRES ÉGAUX NE SONT PAS DEUX ENSEMBLES ÉGAUX** — 25 = 25 avec
  **24 en commun** ; deux angles morts opposés se compensaient exactement.
- **574-C · UNE VALEUR ENREGISTRÉE SE LIT, ELLE NE SE CITE PAS DEPUIS LE
  RAPPORT** — le rapport imprime « garde négative », le banc stocke
  `'garde negative'` ; filtrer sur la chaîne du rapport rendait un ensemble vide.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 35 vues, absentes du corpus de six lots** ; **les
269 branches qui s'arrêtent sans rien dire, comptées et NON JUGÉES** ; **les 14
sites « ailleurs » du 573** ; **les 19 toasts d'erreur littéraux, non jugés** ;
**les 6 toasts sans ton** ; **`warn` et `warning`, non unifiés** ; **les 23 toasts
`success`** ; **les 57 sites qui ne signalent pas un échec** ; **le total réel des
signalements d'échec, toujours inconnu — deux bornes, aucun recensement** ; **les
27 appelés du relevé structurel** ; **les 82 corps vides du 569, NON JUGÉS** ;
**les 18 gardes portant un `VX.fetch`** ; **les 63 `empty` distincts du 568** ;
**les 42 refus du 567, non lus un par un** ; **les 4 refus non-JSON du 542** ;
**les 74 variables serveur sans atténuation** ; **les 67 atténuations non
affichées** ; **les 25 atténuations de la bibliothèque tierce** ;
**`/options|chips`** ; **`renderCalendar`** ; **les 4 limites distinctes du 564** ;
**les 12 signatures partagées du 562** ; **les 5 cas de réponse absents du corpus
du 561** ; **les 8 unités encore ambiguës** ; **les 10 cas non tranchés du 559** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 201 (+2)** ;
**publiés puis corrigés 36 (+1)** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
