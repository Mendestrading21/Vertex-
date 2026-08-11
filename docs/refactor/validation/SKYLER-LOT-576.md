# SKYLER LOT 576 — les cinq instruments rejoués sur le corpus neuf : **quatre tiennent, un compte 181 branches fantômes**

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-576` (base : lot 575 fusionné,
`6c5c456d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(vv)** — le 575 a trouvé 8 programmes que six lots n'avaient jamais vus, les a
comptés et situés, et n'y a relevé que le canal. Ce lot **rejoue les cinq
instruments déjà écrits** — 570 canal, 571 ton, 572 forme du message, 573
déclencheur, 574 refus — **sans en modifier une ligne** (ce sont des preuves), et
dit pour chacun de combien le chiffre publié était un plancher.

Piège écrit **avant** de mesurer (564, 568-B) : *`vendor/lightweight-charts`
pèse 163 684 octets, la plus grosse pièce du lot ; je m'attends à ce qu'il ne
porte **aucun** site du canal — c'est du code tiers, il ne parle pas français.
Publier « 241 516 octets non mesurés » comme s'il s'agissait de produit serait
exactement 550-B.*

## La part tierce, mesurée **avant** tout total

```text
volume neuf total                      241 516 octets
dont bibliothèque tierce (vendor/)     163 684 octets   (67,8 %)
volume PRODUIT réellement neuf          77 832 octets
```

Le 575 a donc annoncé un angle mort **trois fois plus gros qu'il n'est**, côté
produit. Le chiffre n'était pas faux — l'interprétation l'était.

**Interprétations retirées : 10 → 11 (+1).**

## Le piège : **vrai pour quatre instruments, faux pour le cinquième**

```text
                     sites relevés   dont dans le fichier tiers
570 · canal (A)              3                0
570 · bannières              8                0
571 · toasts                 3                0
572 · appels à message       3                0
573 · sites classés         11                0
574 · branches de refus    210              181
```

**Zéro site de canal sur 163 684 octets de code tiers** : le piège tient pour les
quatre instruments qui cherchent un vocabulaire. Il tombe pour le cinquième —
et la raison se lit dans son prédicat : la borne (B) du 574 est « un `if` à test
négatif dont la branche contient un `return` ». C'est du **JavaScript
générique**, que du code minifié produit en masse. **Ce n'est pas une mesure de
produit.**

```text
borne (B) brute sur le corpus neuf     210
   dont `vendor/lightweight-charts`    181
borne (B) de PRODUIT                    29
```

## La cause, lue dans les instruments — **un filtre écrit sur le seul cas présent**

```javascript
// l570_canal.js:99 · l571_ton.js:73 · l572_croise.js:111
// l573_declencheur.js:96 · l574_refus.js:102 · l541_ast.js:89
if (partie.nom.indexOf('chart.umd') >= 0) continue;
```

**Six instruments, six lots, le même filtre tiers écrit par NOM.** Il couvrait le
seul fichier tiers que le corpus de base servait. Dès qu'un second est apparu —
`lightweight-charts.standalone.production.js` — il est passé au travers, **sans
erreur, sans avertissement, sans trou dans les comptes** : juste 181 branches de
plus.

Et le corpus de base, ventilé fichier par fichier, confirme que le défaut n'était
pas visible avant :

```text
fichiers `/static/**` du corpus de base : 26
   dont chemin `/vendor/`                : AUCUN
branches de la borne (B) du 574 portées par un fichier tiers : 0
```

Les **290** de la borne (B) publiés au 574 sont donc bien du code de produit. Le
chiffre tient ; c'est l'**instrument** qui a une faiblesse, révélée seulement
maintenant.

## Le tableau à deux colonnes

```text
instrument / grandeur                         base    neuf   conclusion
570 · canal, relevé (A) noms lus                79      +3   tient
570 · bannières `vx-error-banner`               10      +8   dénominateur trop petit
570 · marqueur `dataset.state`                   1      +0   tient
570 · relevé (B) structurel                    209     +38   tient
571 · toasts portant un ton                     55      +3   tient
571 · appels sans ton                           24      +0   tient
572 · appels avec message                       79      +3   tient
573 · sites du canal classés                    90     +11   plancher relevé
574 · borne (A), branche appelant le canal      25      +2   plancher relevé
574 · borne (B), branche avec un `return`      290   +29 *   * après retrait du tiers
```

Ce que cela règle :

- **le plancher du canal est confirmé à ≥ 101** (90 + 11) — le 575 le disait, il
  est ici re-mesuré par un second instrument (573) ;
- **les bannières sont ≥ 18** (10 + 8). La colonne « base » est lue dans la
  sortie du **571**, qui portait 10 après sa propre correction — celle du 570 en
  portait 9, chiffre d'**avant** correction ;
- **aucune conclusion des cinq lots n'est renversée.** Deux dénominateurs étaient
  trop petits, un instrument est fragile hors de son corpus d'origine.

## Ce que le nouvel écran dit, lu

```text
tons des trois toasts neufs, clef `tons`
   ['success']  littéral  hors catch   'Ticket copié — à saisir manuellement dans IBKR'
   ['warn']     littéral  hors catch   'Écris une question'
   ['warn']     littéral  hors catch   'Montant envisagé requis'
```

**Aucun ton `error` dans les trois.** Sur cet écran, le signalement d'échec ne
passe pas par le toast : il passe par les **8 bannières**. C'est cohérent avec le
572 — la bannière est le registre long, le toast le registre court — mais c'est
la première fois qu'un écran le montre en n'utilisant **que** le premier.

## Un arrêt, sur ma propre lecture

Mon premier tableau imprimait « (clef `ton` absente) × 3 ». La clef n'est pas
`ton` : le banc du 571 stocke **`tons`** (une liste) et **`etatTon`**. C'est
**574-C appliqué à moi-même** — j'ai cité un nom de clef de mémoire au lieu
d'ouvrir la structure. L'instrument n'avait rien raté ; ma lecture était fausse,
et elle m'aurait fait écrire « les trois toasts neufs n'ont pas de ton ».

**Arrêtés avant publication : 202 → 203 (+1).**

## Second contrôle (481) — le cas que la restriction exclut

`/options` ne sert aucun script inline : l'instrument de ce lot ne peut rien y
voir par la voie qu'il emprunte partout ailleurs. Mesuré :

```text
les 9 vues d `/options`
   scripts inline servis, cumulé            9   (le shell commun, `inline#0`)
   fichiers `/static/**` référencés        17
   parmi eux, ABSENTS du corpus de base     0
```

**Aucun angle mort de ce côté** : les 9 vues ne servent pas un fichier que le
corpus ignore. `/options` est donc entièrement couvert par le corpus de base —
malgré une architecture qui ne ressemble à aucune des sept autres pages.

## Ce que le dépôt fait bien, mesuré

- **La bibliothèque tierce ne parle pas à l'utilisateur** : zéro toast, zéro
  bannière, zéro marqueur d'état sur 163 684 octets — tout le langage du produit
  est écrit par le produit.
- **Les trois toasts neufs sont littéraux et hors `catch`** : ce sont des refus
  et une confirmation, pas des rattrapages d'exception.
- **Le refus le plus sensible de l'écran est un refus de saisie** (`'Montant
  envisagé requis'`), posé **avant** tout calcul.
- **`/options` ne cache rien** : ses 17 fichiers statiques sont tous dans le
  corpus que six lots ont mesuré.

## Portée — ce que ce lot NE dit PAS

- Les 8 programmes sont **relevés par cinq instruments**, pas lus ligne à ligne ;
  le relevé (B) structurel du 570 (38 sites) reste **non lu**.
- **Rien n'est corrigé** : le filtre `chart.umd` reste tel quel dans les six
  instruments — ce sont des preuves, et les modifier effacerait la trace du
  défaut qu'ils viennent de révéler.
- Le « 29 » de la borne (B) de produit est obtenu en retirant un chemin
  (`/vendor/`) : **c'est un filtre de chemin, pas une preuve que le reste est du
  produit**.
- Serveur en **DÉMO sans IBKR** : tout relevé de ce lot reste un **plancher**.

## La sonde a bougé — **et c'est le produit qui a fait ce qu'il devait faire**

Pour la première fois de cette série, le contrôle d'apparition n'est pas vide :

```text
apparu   : desk_backup_20260811.json
disparu  : desk_backup_20260802.json
sauvegardes présentes après : 7
```

Explication, vérifiée avant d'écrire cette phrase : il est **00 h 14 UTC** — la
date a basculé pendant ce lot. La suite de tests écrit `desk_data.json`, ce qui
déclenche le **snapshot quotidien** ; la rotation garde 7 jours
(`vertex/app/routes/desk.py:29-51`, `BACKUP_KEEP = 7`) et a donc supprimé la plus
ancienne. **Sept sauvegardes exactement subsistent.**

**Rien n'a été supprimé à la main**, et je n'ai touché à aucun `desk_backup_*` —
c'est la rotation documentée, déclenchée par un changement de jour. Je le publie
au lieu de le lisser : une sonde qui bouge se raconte, même quand la cause est
bénigne.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, bancs écrits **en fichier**, aucun tronqué avant d'avoir
  écrit son JSON.
- `persist._BASE_DIR` redirigé, **redirection vérifiée** via `persist.cache_path()`.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : **8 / 8 identiques.****
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés** (`ai_enrichment.json`, `daily_prev.json`,
  `desk_data.json`, `weekly_snapshot.json`), **restaurés**. **Un fichier apparu et
  un disparu** : `desk_backup_20260811.json` créé, `desk_backup_20260802.json`
  supprimé — **rotation quotidienne documentée** (`BACKUP_KEEP = 7`) déclenchée par
  le passage à une nouvelle date pendant le lot ; 7 sauvegardes subsistent, rien
  supprimé à la main
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **quatre instruments sur cinq ont tenu hors de leur corpus
d'origine, et le cinquième a échoué exactement là où son prédicat était
générique.** Les quatre cherchaient un vocabulaire — un nom d'appel, un ton, une
forme de message ; le cinquième cherchait une forme syntaxique. Un vocabulaire
appartient à celui qui l'a écrit ; une forme syntaxique appartient à tout le
monde.

Et la cause profonde tenait en une ligne recopiée six fois : `indexOf('chart.umd')`.
Un filtre écrit sur le seul cas présent, qui a survécu six lots parce qu'aucun
second cas ne s'était présenté.

Trois règles neuves :

- **576-A · UN FILTRE ÉCRIT SUR LE SEUL CAS PRÉSENT NE GÉNÉRALISE À RIEN** — six
  instruments partagent `indexOf('chart.umd')` ; un second fichier tiers a
  produit **181 branches fantômes**, sans erreur ni avertissement.
- **576-B · UN INSTRUMENT QUI COMPTE UN MOTIF GÉNÉRIQUE NE MESURE PAS LE
  PRODUIT** — `if` négatif + `return` est du JavaScript ordinaire ; sur du code
  minifié, il explose.
- **576-C · UN VOLUME NEUF SE DÉCLARE APRÈS EN AVOIR RETIRÉ LE TIERS** — 241 516
  octets annoncés, **77 832** de produit (32,2 %).

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 38 sites du relevé structurel du 570 sur le
corpus neuf, non lus** ; **les 29 branches de produit de la borne (B) neuve** ;
**le filtre `chart.umd` des six instruments, constaté et NON corrigé** ; **les 8
programmes d'`/analysis/AAPL`, relevés mais non lus ligne à ligne** ; **les 269
branches qui s'arrêtent sans rien dire** ; **les 14 sites « ailleurs » du 573** ;
**les 19 toasts d'erreur littéraux, non jugés** ; **les 6 toasts sans ton** ;
**`warn` et `warning`, non unifiés** ; **les 23 toasts `success`** ; **les 57
sites qui ne signalent pas un échec** ; **le total réel des signalements d'échec,
toujours inconnu** ; **les 27 appelés du relevé structurel du 570** ; **les 82
corps vides du 569, NON JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ; **les
63 `empty` distincts du 568** ; **les 42 refus du 567, non lus un par un** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 203 (+1)** ;
**publiés puis corrigés 37** ; interprétations retirées **11 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
