# SKYLER LOT 579 — **cinq fabriques d'état, 106 appels** — et une fabrique morte dont l'état, lui, est bien vivant

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-579` (base : lot 578 fusionné,
`d5694ba6`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(yy)** — le 578 a trouvé `VX.states.error` en poursuivant une occurrence brute
que l'instrument n'expliquait pas. En la lisant, **deux sœurs** apparaissaient
dans le même objet. Aucune n'avait jamais été inventoriée.

Piège écrit **avant** de mesurer : *`empty` sera la plus appelée, `stale` sera
rare. Mais un compte d'appels ne dit pas ce qui s'**affiche**, et **chaque
fabrique peut avoir son propre repli au centre** (578-C).*

## Les cinq fabriques de `VX.states`, **lues** dans l'AST

```text
fabrique                        octets  data-state   replis internes
empty(reason, action, opts)        313  empty        'Aucune donnée' + 2 vides
error(cause, retryFn)              336  error        'Erreur de chargement',
                                                     'location.reload()'
ghost(type)                       1487  —            'currentColor'
loading(rows = 3)                  257  loading      AUCUN
stale(ageText, source, impact)     238  stale        ' — décision ACTIONABLE bloquée'
```

**Quatre états nommés** (`empty`, `error`, `loading`, `stale`) plus un auxiliaire
graphique (`ghost`, le plus gros des cinq : 1 487 octets de SVG). **Quatre des
cinq portent un repli au centre** — celui de `loading` n'en a pas, et n'a rien à
remplacer.

## Les appels, par fabrique et par corpus

```text
fabrique     base   neuf   total
empty          63     10      73
error          28      2      30
ghost           1      0       1
loading         2      0       2
stale           0      0       0
             ────   ────    ────
               94     12     106
```

**Le piège tient, et va plus loin que prévu** : `empty` est bien la plus appelée
(73), et `stale` n'est pas *rare* — elle est à **zéro**.

## L'arrêt du lot — **une fabrique morte ne prouve pas un état mort**

J'allais écrire « la bannière rassise n'existe pas dans le produit ». Comptage
brut des octets servis :

```text
`vx-stale-banner` — corpus de base : 5 fichiers DISTINCTS, 19 occurrences
   8  /static/vertex/js/vx-core.js            ← la fabrique morte elle-même
   8  /static/vertex/js/charts/chart-core.js  ← une SECONDE fabrique
   1  /opportunities|inline#1   « Mode DÉMO — données synthétiques… »
   1  /portfolio|inline#1       « IBKR hors ligne — marques desk/EOD utilisées »
   1  /system|inline#1          « ⏳ ${st.warnings…} »
`vx-stale-banner` — corpus neuf : 1   « ⛔ Préparation bloquée par la stratégie »
`states.stale`  : 0 occurrence, sur les deux corpus
```

L'état **rassis est bien vivant** : six sites le produisent. Ce qui est mort,
c'est **la fabrique canonique** — et le produit rend le même état par une
**seconde fabrique**, dans `chart-core.js` :

```javascript
if (state === 'stale')
  return `<div class="vx-stale-banner">⏱ Données périmées — ${msg || 'dernière val…'}`;
```

Deux fabriques, deux vocabulaires : **« Donnée rassise »** d'un côté,
**« Données périmées »** de l'autre. Constat, non jugé.

C'est **578-B une seconde fois** : chercher les `return`, pas seulement les
affectations — et ne pas conclure d'un compte d'appels nul à l'absence d'un
état.

**Arrêtés avant publication : 205 → 206 (+1).**

## Le « 63 » du 568 — **cette fois, deux nombres égaux SONT le même ensemble**

Mon relevé donne **63 appels distincts à `VX.states.empty`** sur le corpus de
base. Le 568 publiait **63 `empty` distincts**. Croisé **par identité de site**,
comme l'impose 574-B :

```text
dans les deux            63
seulement dans le 568     0
seulement dans le 579     0
```

**Identiques, site pour site.** Le 574 avait montré que deux « 25 » pouvaient
cacher deux ensembles différents ; ici l'égalité est réelle — et 574-B ne dit pas
que l'égalité trompe toujours, il dit qu'elle **doit être vérifiée**.

Nuance qui en découle, publiée telle quelle : les données du 568 portaient déjà
`{'error': 28, 'empty': 75}` — **les 28 appels à la fabrique d'erreur y étaient
depuis le début**, rangés sous le mot « états ». Le 578 disait vrai (aucun
instrument **depuis le 570** ne pouvait les voir) ; ce qui manquait n'était pas
la donnée, c'était **le lien**.

## Second contrôle (481) — ce que le comptage direct pourrait rater

```text
appels INDIRECTS `states[expr](…)`   base 0 · neuf 0
ALIAS `X = ….states`                 base 0 · neuf 0
```

**Aucun.** La restriction « appel pointé explicite » ne coûte rien sur ces deux
corpus — mesuré, pas supposé (547-B).

## Ce que le dépôt fait bien, mesuré

- **106 rendus d'état passent par une fabrique commune** : même balisage, même
  `data-state`, sur les 8 pages.
- **Quatre états sont nommés dans le DOM** (`data-state="empty|error|loading|stale"`)
  — un lecteur d'écran, un test ou un humain peut les distinguer sans lire le
  texte.
- **`empty` accepte une action** (`empty(reason, action, opts)`) : l'état vide
  n'est pas un cul-de-sac par construction.
- **`loading` n'a aucun repli** — et c'est correct : un squelette n'a pas de
  cause à donner.
- **Zéro appel indirect, zéro alias** : le vocabulaire d'états n'est jamais
  atteint par un chemin dynamique.

## Portée — ce que ce lot NE dit PAS

- **Un compte d'appels n'est pas une surface d'écran** : une fabrique appelée
  une fois dans une boucle couvre plus qu'une appelée dix fois en garde. Le
  « 106 » compte des **sites d'appel**, rien d'autre.
- **La seconde fabrique de `chart-core.js` n'est pas inventoriée** ici : elle est
  nommée, située, non comptée.
- **Rien n'est corrigé** : `VX.states.stale` reste dans le code, les deux
  vocabulaires restent tels quels, les replis restent tels quels.
- Les deux corpus sont ceux du 541 et du 575 : **plancher**, DÉMO sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu** ; aucun banc antérieur touché.
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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **le 568 avait la réponse dans ses données depuis onze
lots.** Il comptait 28 `error` et 75 `empty` sans savoir qu'il comptait des
appels de fabrique ; les cinq lots suivants ont mesuré le même canal avec un
instrument qui ne pouvait plus les voir. Ce qui manquait n'était ni une mesure ni
un chiffre : c'était de relire ce qui était déjà écrit.

Et une deuxième fois en deux lots, une conclusion négative a failli passer :
« zéro appel » ne veut pas dire « zéro écran ». Le seul geste qui l'a arrêtée est
le comptage **brut**, celui qui ne suppose rien de la façon dont le code s'écrit.

Trois règles neuves :

- **579-A · UNE FABRIQUE MORTE NE PROUVE PAS UN ÉTAT MORT** — `VX.states.stale` :
  **0 appel**, et pourtant **6 sites** produisent `vx-stale-banner`.
- **579-B · DEUX FABRIQUES POUR LE MÊME ÉTAT, C'EST DEUX VOCABULAIRES** —
  « Donnée rassise » et « Données périmées » désignent la même chose.
- **579-C · QUAND DEUX NOMBRES ÉGAUX SONT VRAIMENT LE MÊME ENSEMBLE, LE DIRE
  AUSSI** — 63 = 63, **63 en commun** : 574-B exige une vérification, pas un
  soupçon systématique.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **la seconde fabrique d'état de `chart-core.js`,
nommée et non inventoriée** ; **`VX.states.stale`, morte et NON supprimée** ;
**les deux vocabulaires du même état, NON unifiés** ; **les replis internes des
quatre fabriques** ; **les 73 appels à `empty`, comptés et non lus** ; **les 30
appels à la fabrique d'erreur** ; **les 2 appels à « identifiant nu »** ; **les 6
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

Comptes séparés : résultats faux **arrêtés avant publication 206 (+1)** ;
**publiés puis corrigés 38** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
