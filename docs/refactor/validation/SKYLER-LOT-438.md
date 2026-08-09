# SKYLER LOT 438 — Six contrats rompus, six faux positifs : trois objets différents s'appellent `scan`, et `cal.ts` reste seul

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-438` (base : lot 437 fusionné,
8ef77a6)

Vingt et unième lot de la veine, **bornage du 437**. Le 437 avait ouvert une
veine neuve : le client lit `cal.ts`, un champ que le serveur n'émet pas.
Question : **combien d'autres contrats de champ sont rompus ?**

**Aucun code, aucun gardien, aucun test.**

## L'instrument — la question du 437, inversée

Pour chaque route à **identifiant receveur distinctif** (la leçon du 437 : un
receveur d'une ou deux lettres est indistinguable du Chart.js minifié), lister
les champs que le **client lit** (`ident.champ`) et les comparer aux champs que le
**serveur émet**.

```text
route                      receveur    lus  servis   lus MAIS ABSENTS
/api/command               cmd           2      10   —
/scan                      scan         18      24   last_scan_ts, market, options_source,
                                                     scan_ts, source, symbols
/cal-feed                  cal           3       3   ts
/api/system/diagnostics    diag          4       5   —
/api/positions/state       posState      0       4   —
```

**Témoin positif** : `/cal-feed` fait bien remonter `ts` — la trouvaille du 437,
retrouvée par un instrument écrit dans l'autre sens. L'instrument mord là où il
doit.

Et il annonce **six contrats rompus de plus** sur `/scan`.

## Les six sont faux. Tous les six.

C'est le résultat du lot, et il tient à une seule cause : **trois objets
différents s'appellent `scan` dans les octets servis.**

```text
champ lu           l'identifiant `scan` désigne…              verdict
last_scan_ts       diag.scan  (/api/system/diagnostics)       PRÉSENT ✓
options_source     diag.scan                                  PRÉSENT ✓
source             diag.scan                                  PRÉSENT ✓
symbols            st.scan    (/api/system-status)            PRÉSENT ✓
market             scan_state, écrit par terminal.py:520/615  absent car AUCUN SCAN N'A TOURNÉ
scan_ts            scan_state, écrit par terminal.py:522/617  absent car AUCUN SCAN N'A TOURNÉ
```

Mesuré, payload par payload : `diag['scan']` porte
`last_scan_ts, options_source, rows, source` ; `st['scan']` porte
`error, last_scan, symbols`. Et `system_page.py` écrit, en toutes lettres, le
repli du seul cas ambigu :

```javascript
var _sym = (st && st.scan && st.scan.symbols);
if (_sym == null && diag && diag.scan) _sym = diag.scan.rows;
```

**Le code avait déjà prévu l'absence** — mon détecteur, lui, ne savait pas de quel
`scan` il parlait.

Quant à `market` et `scan_ts` : `terminal.py` les écrit dans `scan_state` à
chaque scan (`:520`/`:522`, `:615`/`:617`). Ils manquent **parce que le scan est
vide au démarrage**, pas parce que le contrat est rompu. C'est le piège de l'état
unique, celui que la boucle se répète depuis le 425 — et il m'a eu quand même.

## Le résultat

**Sur le périmètre mesurable, `cal.ts` reste le seul contrat rompu.** La veine
ouverte au 437 ne s'étend pas : elle avait un cas, elle en a toujours un.

C'est un **bornage négatif**, et c'est utile : il empêche de transformer une
trouvaille isolée en « motif d'architecture » sur la foi d'un compteur.

## Une hypothèse, que je marque comme telle

`/api/system-status` **émet** bien un `ts` (mesuré :
`2026-08-09T10:30:32+00:00`), et `system_page.py` le lit correctement
(`st.ts || Date.now()`, deux fois). Il est **plausible** que le `cal.ts` du 437
soit cette forme, recopiée vers une route qui n'a pas le champ.

**Je ne l'ai pas testé** — c'est une hypothèse d'explication, pas une mesure, et
la règle du 421 dit de le dire plutôt que de le raconter.

## Ce que ce lot dit de l'instrument

Trois lignes propres, alignées et fausses de plus. Le compte monte à **dix en
cinq lots** (430, 434 ×2, 435, 437 ×3, 438 ×3). La cause est nouvelle : ce n'est
plus un motif trop large ni un receveur trop court, c'est une **collision de noms
entre payloads**. `scan` désigne trois objets ; un instrument qui indexe par nom
d'identifiant ne peut pas les séparer.

Ce qui a arrêté les trois : **l'invraisemblance**. Six contrats rompus d'un coup
sur une route centrale, après des semaines de mesures, était trop gros pour être
vrai. *Un pool qui mord sur des objets manifestement sains accuse l'instrument*
(règle 414) — appliquée pour la troisième fois, et pour la troisième fois elle
avait raison.

## Classement

**Aucun défaut nouveau.** Rien à classer, rien à ajouter aux dossiers. Le seul
effet sur la liste est **négatif** : le contrat rompu du 437 reste **isolé**, et
ne devient pas une famille.

## Portée

Cinq routes mesurées sur les huit du 437 — les trois à receveur d'une lettre
restent **hors d'atteinte** de cette méthode. Le périmètre couvre les champs de
**premier niveau** : un contrat rompu sur un sous-objet (`d.x.y`) échappe au
détecteur, et je ne l'ai pas quantifié.

La mesure est faite sur le **scan vide du démarrage**. Les six faux positifs le
prouvent à eux seuls : sur un scan peuplé, `market` et `scan_ts` seraient
présents et la ligne n'aurait jamais été levée.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Toutes les routes appelées en **GET** (lecture).
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Quarante et unième lot court. Séquence : **435 ~ · 436 ~ · 437 ✓ · 438 ✗
(bornage négatif)**.

Le 437 avait trouvé en échouant à généraliser ; celui-ci ne trouve rien en
réussissant à mesurer. Les deux sont des résultats. Ce qui compte pour la suite :
**la veine des contrats de champ est refermée** au niveau où je sais la mesurer,
et le prochain lot doit chercher ailleurs.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
