# SKYLER LOT 571 — le canal que j'avais appelé « d'erreur » : **33 de ses 90 sites signalent un échec** — 23 toasts sont des confirmations — et **le plancher du 570 était sous-compté : 90, pas 89**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-571` (base : lot 570 fusionné,
`d5b31401`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix — un lot qui porte contre moi

**(qq)** — au 569 j'ai baptisé ce canal « **second canal d'erreur** » sur la foi
de **quatre** `VX.toast` lus à l'intérieur de clauses `catch`. Au 570 j'ai
inventorié **89 sites** sous ce nom, **sans jamais lire le second argument de
`VX.toast(message, ton)`**.

Ce lot le lit.

## La calibration a échoué deux fois, et les deux fois c'était instructif (556-B)

**(a) 8 bannières au lieu de 9.** Cause : **mon banc neuf était plus étroit que
celui du 570.** Son lecteur ignorait `ConditionalExpression` et
`LogicalExpression`, et perdait, dans `options-intel.js` :

```javascript
el.innerHTML = (window.VX && VX.states) ? VX.states.error(cause)
                                        : '<div class="vx-error-banner">…'
```

une bannière écrite dans la **branche de repli** d'un ternaire. Le 570 n'était
pas en cause.

**(b) après correction du lecteur : 10, pas 9.** Le site supplémentaire, **lu
dans le code** (`system_page.py:594`), est une bannière bien réelle :

```javascript
+(errs.length ? `<div class="vx-error-banner vx-mt2">⚠ ${…}</div>` : '')
```

Le lecteur du 570 descendait une chaîne `+` en ne gardant que le littéral **le
plus à gauche** : il ne pouvait pas voir un ternaire au **milieu** de la chaîne.

**Le plancher du 570 vaut donc 90, pas 89.** L'erreur va exactement dans le sens
que le 570 annonçait lui-même — **un plancher est un plancher**, et il vient de
monter en un seul lot. Correction **en ajout** ; le 570 n'est pas réécrit.

**Publiés puis corrigés : 33 → 34 (+1).**
**Arrêtés avant publication : 196 → 197 (+1)** — le lecteur trop étroit aurait
publié un canal amputé sans que rien ne le signale.

## Le premier constat — **le ton des 55 toasts, relevé et non deviné**

```text
ton littéral            48        `success`   24 sites
ton absent               6        `error`     22
ternaire littéral        1        `warn`       2
                                  `warning`    1
                                  `info`       1
```

```text
toasts pouvant porter `error`               22
toasts `success` sans jamais `error`        23
toasts sans `error` ni `success`            10
```

**Mon attente était juste, et elle ne valait rien tant qu'elle n'était pas
mesurée** (568-B) : j'avais écrit « je m'attends à ce que beaucoup de toasts
soient des succès ». Ils sont **23**, contre 22 qui peuvent porter `error`.
Presque un partage égal — pas la majorité écrasante que j'imaginais.

Détail relevé au passage : **`warn` (2 sites) et `warning` (1 site)** — deux
orthographes pour la même idée, exactement comme les quatre noms de clé du 542.
C'est un **constat**, il n'est pas corrigé.

## Le second — **le canal réellement « d'erreur » compte 33 sites, pas 90**

```text
sites du canal, plancher corrigé                  90
   toasts pouvant porter `error`                  22
   bannières `vx-error-banner`                    10
   marqueur `dataset.state = 'error'`              1
                                                 ───
   signalement d'échec ASSUMÉ par le code         33
sites qui ne signalent PAS un échec               57
   dont `emptyCard` / `setStatus` / `setNet`      24
   dont toasts `success` ou autre ton             33
```

**Le nom que j'avais donné au canal était trop large d'un facteur trois.** Le 570
inventoriait un **canal de notification**, dont le signalement d'échec n'est
qu'un usage sur trois. La correction est en ajout ; le titre du 570 reste, avec
cette qualification à côté.

## Le troisième — **les trois sans ton, relevés et non classés** (563-A)

```text
emptyCard   14 sites   premiers arguments : vx-mk-multi · vx-mk-spy
                       · vx-mk-yield · vx-mk-macro-cal   (identifiants de zone)
setStatus    5 sites   LIVE · FALLBACK · OFFLINE · DELAYED   (noms d'état)
setNet       5 sites   offline · online
```

Ces trois-là **n'ont aucun argument de ton**. Leur appliquer la grille du toast
aurait été rejouer une méthode les yeux fermés. Ils sont **relevés**, pas
classés : `setStatus('LIVE')` n'est pas un signalement d'échec, et
`setStatus('OFFLINE')` n'est pas un message.

## Second contrôle (481) — ce que l'instrument ne peut pas lire

```text
ton NON littéral (variable, expression)            0
ton ABSENT (appel à un seul argument)              6
ton ternaire à deux littéraux (les DEUX comptés)   1
   VX.toast(d.note||'Enrichissement Claude lancé', r.ok?'success':'error')
```

**Zéro ton illisible** — un zéro mesuré, pas une absence de mesure. Le ternaire
est compté dans les **deux** seaux qu'il peut atteindre : il signale un échec
**dans une branche sur deux**, et le ranger d'un seul côté aurait été un choix,
pas une mesure.

## Ce que le dépôt fait bien, mesuré

- **Le ton est presque toujours explicite** : 48 littéraux sur 55, zéro
  expression illisible.
- **Le vocabulaire est court** — cinq valeurs seulement, dont trois marginales.
- **`setStatus` porte quatre états nommés** (`LIVE`, `FALLBACK`, `OFFLINE`,
  `DELAYED`) : la connexion n'a pas deux états mais quatre, et ils sont écrits.
- **La bannière existe en repli du canal principal** : `options-intel.js` écrit
  la bannière à la main **si `VX.states` n'est pas chargé** — le produit prévoit
  l'absence de son propre outil d'état.

## Portée — ce que ce lot NE dit PAS

- **Un ton `'error'` prouve une intention de signalement, pas qu'un échec réel a
  eu lieu.** Le lot mesure ce que le code dit.
- Les 23 toasts `success` **ne sont pas jugés** : une confirmation est un usage
  légitime, ce lot corrige un **nom**, pas un comportement.
- **`warn` / `warning` n'est pas unifié** — constat, pas correction.
- Le plancher reste un plancher : **90 est une borne basse**, et elle a bougé une
  fois.

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Troisième lot consécutif sur le même objet du produit, et le seul
des trois qui **corrige les deux précédents** — le mien du 569 pour le nom, le
mien du 570 pour le compte.

Ce que je retiens : **j'ai nommé avant de mesurer, et le nom a survécu deux
lots.** « Second canal d'erreur » sonnait juste : quatre toasts lus dans des
`catch`, tous des erreurs. Il a fallu aller lire un argument que je n'avais
jamais regardé pour voir que les deux tiers du canal font autre chose. Un nom
n'est pas une hypothèse neutre : **il oriente tout ce qu'on compte ensuite**, et
personne ne le remet en cause parce qu'il a l'air d'un simple libellé.

Trois règles neuves :

- **571-A · UN NOM EST UNE MESURE QUI S'IGNORE** — « canal d'erreur » a servi de
  titre à deux lots avant qu'on lise l'argument qui le contredisait aux deux
  tiers.
- **571-B · UNE RÉIMPLÉMENTATION DU MÊME PRÉDICAT N'EST PAS LE MÊME PRÉDICAT** —
  mon lecteur neuf a d'abord perdu un site, puis en a trouvé un que l'ancien
  n'avait jamais vu ; seule la calibration a rendu les deux écarts visibles.
- **571-C · UN PLANCHER QUI MONTE CONFIRME QU'IL ÉTAIT UN PLANCHER** — 89 → 90
  en un lot ; l'erreur est allée dans le sens annoncé, et c'est la meilleure
  preuve que l'annonce était honnête.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **`warn` et `warning`, deux orthographes non
unifiées** ; **les 23 toasts `success`, non jugés** ; **les 57 sites du canal qui
ne signalent pas un échec** ; **le total réel des signalements d'échec, toujours
inconnu — deux bornes, aucun recensement** ; **les 27 appelés du relevé
structurel, non triés** ; **les 46 littérales courtes du canal** ; **les 79 sites
hors `catch`, comptés mais non lus** ; **les 82 corps vides du 569, NON JUGÉS** ;
**les 18 gardes portant un `VX.fetch`** ; **les 63 `empty` distincts du 568** ;
**les 42 refus du 567** ; **les 4 refus non-JSON du 542** ; **les 74 variables
serveur sans atténuation** ; **les 67 atténuations non affichées** ; **les 25
atténuations de la bibliothèque tierce** ; **`/options|chips`, douzième limite
jamais levée ni nommée** ; **`renderCalendar`, exécutée hors périmètre au 537** ;
**les 4 limites distinctes du 564** ; **les 12 signatures partagées du 562** ;
**les 5 cas de réponse absents du corpus du 561** ; **les 8 unités encore
ambiguës** ; **les 10 cas non tranchés du 559** ; **les 16 sous-clés du 558** ;
**les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35 clés du contrat
non gardé** ; **les 28 candidates** ; **les 6 clés sans lecture observée** ;
**les 26 routes à lectures ambiguës** ; **les 4 collisions de nom** ; **les 3
ombres de `briefing.py`** ; **les 5 routes affamées du 556** ; **les 14
candidates du 554, en attente d'un GO** ; **les 4 routes construites
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

Comptes séparés : résultats faux **arrêtés avant publication 197 (+1)** ;
**publiés puis corrigés 34 (+1)** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
