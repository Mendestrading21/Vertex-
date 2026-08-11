# SKYLER LOT 578 — la bannière canonique de Vertex est **une fonction**, appelée **30 fois**, que cinq lots n'ont jamais vue

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-578` (base : lot 577 fusionné,
`e3e5e340`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(xx)** — le 577 a fait tomber le « 10 sur 10 » du 572 sur un corpus neuf, et a
montré mieux : **« interpole » et « dit pourquoi » ne coïncident pas**. Cette
lecture n'avait jamais été appliquée aux **10 bannières d'origine**.

Piège écrit **avant** de mesurer : *je m'attends à trouver **au moins un repli
littéral parmi les 10** — le motif `x || 'texte'` est idiomatique ici. Si j'en
trouve, le « 10 sur 10 interpolent la cause **réelle** » devient faux **sur son
propre corpus**.* Garde-fou posé en même temps (577-A retourné contre moi) : *ne
pas partir en chasse d'une réfutation — un repli peut être la seule chose honnête
à écrire.*

## Le piège est vérifié — **le « 10 sur 10 » tombe sur son propre corpus**

```javascript
// /static/vertex/js/pages/options-gex.js
out.innerHTML = '<div class="vx-error-banner">'
              + esc(d.error || 'réponse indisponible') + '</div>';
```

Elle **interpole**, donc elle comptait dans le « 100 % ». Mais si `d.error` est
vide, elle affiche « réponse indisponible » — **rien sur la cause, au moment
précis où la cause manque**. Le 572 n'était pas faux dans son compte : il était
faux dans le mot **« réelle »**.

**Publiés puis corrigés : 37 → 38 (+1).**

## Deux arrêts — **mes propres instruments, deux biais opposés**

**Premier.** `l577_cause.js` relève les feuilles non littérales de **toute
l'affectation**. Sur le corpus neuf, chaque affectation *était* une bannière : le
défaut ne pouvait pas se voir. Sur le corpus de base, `/system|inline#1 @23129`
construit **un panneau entier** :

```javascript
$('vx-conn-sync').innerHTML = kv('Mode', esc(live.mode || '—'))
  + kv('Domaines', names.map(esc).join(', ') || '—')
  + (errs.length ? `<div class="vx-error-banner vx-mt2">⚠ ${…}` : '')
```

Le `|| '—'` qui remontait **n'appartient pas à la bannière**. J'allais publier
« 2 replis » là où il y en a un.

**Second.** Ma correction — prendre le **plus petit nœud** contenant la classe —
a basculé dans le biais inverse : le plus petit nœud est **le littéral
d'ouverture**, ce qui coupe le `+ esc(e.message)` qui suit. Le banc rendait
alors « 1 interpolent, 9 littérales » — absurde, et **rattrapé par le témoin de
calibration** (« Copilote injoignable » doit ressortir interpolée).

**Aucun critère de taille ne délimite une bannière** dans `'<div …>' +
esc(e.message) + '</div>'` : c'est une **sous-chaîne d'une chaîne plate**. Il
faut la délimiter **par son contenu** — du littéral qui ouvre `vx-error-banner`
jusqu'à celui qui porte `</div>`. Troisième banc, écrit à part.

**Arrêtés avant publication : 203 → 205 (+2).**

## La découverte — **la bannière canonique est une fonction**

```javascript
// vertex/static/vertex/js/vx-core.js
error(cause, retryFn) {
  return `<div class="vx-error-banner" data-state="error">⚠ ${cause || 'Erreur de chargement'}`
    + `<button class="vx-btn vx-btn-sm" onclick="${retryFn || 'location.reload()'}">Réessayer</button>`
    + `<a class="vx-btn vx-btn-sm vx-btn-ghost" href="/system?view=data">Ouvrir Système</a></div>`;
},
```

`VX.states.error` est servi sur **les 8 pages**. Aucun instrument depuis le 570
ne pouvait le voir : tous cherchaient une **affectation** `innerHTML`, or ceci
est un **`return`**.

```text
appels à `VX.states.error(` — corpus de base    28
appels — corpus neuf                             2
                                                ──
                                                30
positions communes avec les 18 écrites à la main  0
fichiers portant les DEUX formes                  2
```

**Le plancher des bannières passe de 18 à au moins 48.** Et les deux ensembles
ne se recouvrent pas : **aucune position commune** — j'ai mesuré le recouvrement
avant d'additionner (546-A).

## Les 30 appels, classés — l'argument **lu**, jamais deviné

```text
classe                          base   neuf   total
phrase fixe                       17      2      19
phrase fixe + interpolation        8      0       8
identifiant nu                     2      0       2
repli littéral                     1      0       1
                                 ───    ───     ───
                                  28      2      30
```

Dix-neuf appels passent une **phrase fixe qui nomme le domaine** — « Régime
indisponible », « Alertes indisponibles », « Live Engine injoignable », « Moteur
d'anomalies injoignable ». C'est exactement **577-C** : un texte fixe dit la
cause quand la cause ne varie pas.

## Le tableau à deux colonnes — les bannières écrites à la main

```text
grandeur                                         base  neuf  total
bannières écrites à la main                        10     8     18
   INTERPOLENT (critère du 572)                    10     7     17
   LITTÉRALES                                       0     1      1
      dont relaient une EXCEPTION                   7     6     13
      dont un REPLI littéral peut effacer la cause  1     1      2
```

## Second contrôle (481) — ce que la restriction excluait, **nommé**

Comptage brut de la classe, **clef `(page, nom)`** et non le nom seul — le
comptage du 577 écrasait `inline#1` de `/system` et de `/journal` sur la même
clef (532-A) :

```text
/…/vx-core.js   1 occurrence brute par page × 8 pages   0 vue par l'instrument
```

**C'est l'angle mort, et c'est la fabrique.** Une occurrence, servie huit fois,
qu'aucun relevé n'expliquait — et c'est le cœur du langage d'erreur du produit.

## Ce que le dépôt fait bien, mesuré

- **Une bannière canonique unique** : 30 des 48 sites passent par la même
  fonction — même balisage, même `data-state="error"`, même ton.
- **Chacun de ces 30 sites offre deux issues** : un bouton **« Réessayer »** et
  un lien **« Ouvrir Système »**. Aucun lot ne l'avait rapporté ; c'est la seule
  partie du canal qui propose systématiquement une action.
- **19 appels nomment le domaine en panne** dans une phrase fixe, sans dépendre
  d'un message d'exception.
- **13 des 18 bannières écrites à la main relaient une exception réelle**, toutes
  via `esc()`.

## Portée — ce que ce lot NE dit PAS

- **48 est un plancher**, pas un recensement : deux corpus réunis, DÉMO sans
  IBKR, et la fabrique peut avoir d'autres appelants hors corpus.
- Les **2 appels à « identifiant nu »** sont signalés **par leur forme** : ce que
  contient la variable n'a pas été suivi.
- **Rien n'est corrigé.** Le repli `cause || 'Erreur de chargement'`, le
  « réponse indisponible » et les 6 relais bruts de `e.message` **restent tels
  quels** — constatés, non jugés.
- Le classement des arguments repose sur la **forme lue** de l'appel, pas sur ce
  qui s'affiche à l'exécution.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu**. `l572_bannieres.js` et `l577_cause.js` **non touchés** : les deux
  bancs correctifs sont **écrits à part**.
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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **neuf lots ont mesuré un canal d'erreur en ne voyant que la
moitié la moins canonique.** Les 18 bannières écrites à la main étaient les
exceptions ; les 30 appels à une fabrique commune étaient la règle. Et la raison
de cet aveuglement tient en un choix fait au 570 et jamais réinterrogé : chercher
une **affectation** au DOM. Une fabrique rend une chaîne ; elle n'affecte rien.

Deuxième leçon, plus inconfortable : **mes deux tentatives de corriger un biais
ont produit le biais inverse.** Trop large, j'attrapais le voisin ; trop étroit,
je coupais la cause. Seul un témoin lu dans le code *avant* la mesure a permis de
voir que la seconde version était fausse — le compte, lui, avait l'air propre.

Trois règles neuves :

- **578-A · AUCUN CRITÈRE DE TAILLE NE DÉLIMITE UN FRAGMENT DANS UNE CHAÎNE
  PLATE** — trop large on capte le voisin, trop étroit on coupe la cause : il
  faut délimiter **par le contenu**.
- **578-B · UN CANAL PEUT AVOIR UNE FABRIQUE QUE TOUS LES INSTRUMENTS IGNORENT** —
  30 sites invisibles à cinq lots, parce qu'ils passent par un `return` et non
  par une affectation.
- **578-C · UN REPLI AU CENTRE VAUT POUR TOUS LES APPELANTS** — `cause ||
  'Erreur de chargement'` couvre **30 sites d'un coup**.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 30 appels à la fabrique, classés mais non suivis
jusqu'à ce qu'ils affichent** ; **les 2 appels à « identifiant nu »** ; **le repli
`cause || 'Erreur de chargement'` de la fabrique, constaté et NON corrigé** ;
**les 6 bannières qui relaient `e.message` tel quel** ; **le repli « réponse
indisponible »** ; **les 38 sites du relevé structurel neuf du 576** ; **les 29
branches de produit de la borne (B) neuve** ; **le filtre `chart.umd` des six
instruments** ; **les 8 programmes d'`/analysis/AAPL`, non lus ligne à ligne** ;
**les 269 branches qui s'arrêtent sans rien dire** ; **les 14 sites « ailleurs »
du 573** ; **les 19 toasts d'erreur littéraux, non jugés** ; **les 6 toasts sans
ton** ; **`warn` et `warning`, non unifiés** ; **les 23 toasts `success`** ;
**les 57 sites qui ne signalent pas un échec** ; **le total réel des signalements
d'échec, toujours inconnu** ; **les 27 appelés du relevé structurel du 570** ;
**les 82 corps vides du 569, NON JUGÉS** ; **les 18 gardes portant un
`VX.fetch`** ; **les 63 `empty` distincts du 568** ; **les 42 refus du 567** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 205 (+2)** ;
**publiés puis corrigés 38 (+1)** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
