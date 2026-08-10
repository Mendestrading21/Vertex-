# SKYLER LOT 539 — « Données réelles uniquement » : **112 atténuations `|| 0` dans le JS servi, quatre seulement touchent une valeur du serveur ET s'affichent — et les quatre sont des COMPTES**. Aucun chiffre inventé

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-539` (base : lot 538 fusionné,
`822f3bc4`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(f)** — changer d'axe. Cinq lots (534 → 538) ont travaillé le même objet : le
JavaScript servi, ses conteneurs, ses chargeurs. Le compte est fermé. L'axe le
plus rentable qui reste, sans aucun GO : **l'invariant produit le plus fort du
dépôt** — « donnée absente → `—`/`n/d` honnête » — que **personne n'avait mesuré
de bout en bout**.

Le danger n'est ni `x || '—'` (honnête) ni `x || []` (conteneur vide) : c'est
**`x || 0`**, qui transforme une **absence** en **chiffre**.

## Les deux moitiés de la question, mesurées séparément

**Côté serveur — l'absence existe vraiment.** Les routes sûres, appelées en
DÉMO :

```text
/api/live/status        10 champs nuls   domains.calendar.age_s · .ts · companies.count …
/api/system/status       6               engines[0].last_error · latency_ms · freshness.*.age_s
/api/positions/state     6               portfolio.delta_global · theta_global · unrealized_pnl …
/api/cockpit             2               action.sector · opportunities[0].sector
                        ──
                        24 champs nuls réellement servis
```

**Côté client — les formateurs honnêtes dominent.**

```text
appels à un format HONNÊTE (`nd`/`num`/`pct`/`price`/`ago`)      272
valeurs neutres non comptées (`|| []`, `|| '—'`, `|| {}`)      2 072
atténuations `|| 0` sur une lecture de champ                     112
```

`VX.fmt.nd/num/pct/price` rendent **tous** `'—'` pour `null`/`undefined`/non
fini — lu dans `vx-core.js:42-73`.

```text
CALIB 1 · POSITIF   112 atténuations trouvées                     OK
CALIB 2 · NÉGATIF   272 formateurs honnêtes reconnus              OK
CALIB 3 · NÉGATIF   2 072 valeurs neutres NON comptées            OK
```

## Le tri — et ce qui reste vraiment suspect

```text
   atténuations `|| 0`                             112
      dont racine SERVEUR prouvée                    6
      dont AFFICHÉES (gabarit / VX.fmt / innerHTML)  17
      dont SERVEUR **ET** AFFICHÉES                   4
   racine INCONNUE (comptée à part)                 106
```

## Les quatre, lues une par une — **toutes disculpées**

**Un risque quantifié n'est pas un risque réalisé** (**524-B**), et cette règle a
déjà disculpé six accusés aux 532 et 534. Lecture du **serveur**, pas du client :

```text
/journal   tr.entries || 0     track_record.py:168  ->  'entries': len(entries)
/journal   tr.resolved || 0    track_record.py:168  ->  'resolved': resolved
/journal   d.n_outcomes || 0   analysis_api.py:290  ->  len(mem['outcomes'])
```

**Ce sont des COMPTES.** `len()` ne rend jamais `null` : afficher `0` quand il y
a zéro élément **est vrai**. Et le contexte le confirme — la phrase est un état
vide honnête :

```js
VX.states.empty('Pas encore assez de verdicts résolus pour mesurer la fiabilité ('
  + (tr.entries||0) + ' verdict(s) enregistré(s), ' + (tr.resolved||0)
  + ' résolu(s) — minimum 5 par verdict). Le registre se remplit à chaque scan.', …)
```

Le quatrième est encore plus net :

```js
VX.updateIndicator((r.ts||0)*1000, 'séquence de démarrage', 'live')
```

`0 * 1000 = 0`, qui est **falsy** — et `VX.fmt.ago` commence par
`if (!ts) return '—';`. **L'atténuation alimente un formateur honnête, qui rend
`'—'`.**

**Arrêtés avant publication : 153 → 154.** Sans cette lecture, je publiais
« quatre chiffres potentiellement inventés ».

## Ce que le dépôt fait bien, mesuré

- **Aucun chiffre inventé sur le périmètre mesurable.** Sur 112 atténuations, 4
  atteignent l'écran depuis une valeur serveur, et les 4 sont **vraies**.
- **272 appels de formateur honnête** contre 112 atténuations : le motif
  dominant est **le `'—'`**, pas le zéro.
- **2 072 valeurs neutres** (`|| []`, `|| {}`, `|| '—'`) : le code se protège
  massivement **sans** fabriquer de nombres.
- **Le serveur dit franchement ce qu'il ignore** : 24 champs `null` réellement
  servis, dont `unrealized_pnl` et `delta_global` — il n'envoie pas des zéros à
  la place.
- **`VX.fmt.ago` refuse un horodatage nul** dès sa première ligne, ce qui
  neutralise l'atténuation qui l'alimente.

## Portée — ce que ce lot NE dit PAS

- **106 atténuations ont une racine INCONNUE** : mon lien « valeur venue du
  serveur » n'est prouvé que si la variable est déclarée à partir d'un `await`
  ou d'un `VX.fetch`. Un champ passé dans un objet reconstruit, ou reçu en
  paramètre, échappe au lien. **C'est la plus grosse réserve du lot.**
- **Le corpus est le JS servi des 8 pages**, hors bibliothèque `chart.umd`.
- **Les champs nuls sont relevés en DÉMO** ; en réel, la liste peut différer.
- « Affichée » couvre le gabarit, `VX.fmt.*` et `innerHTML` — pas un troisième
  détour.
- **Aucun navigateur, aucune route interdite, aucune correction engagée.**

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
0, 3, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier — et cette fois sur **l'invariant que l'utilisateur a écrit
lui-même** dans le CLAUDE.md : « données RÉELLES uniquement ». Il tient sur tout
ce que j'ai su relier.

Ce qu'il faut dire sans le maquiller : **le chiffre brut « 112 atténuations »
n'aurait rien voulu dire publié seul.** C'est le tri — racine serveur, puis
affichage, puis lecture du code serveur — qui le ramène à quatre cas, tous
légitimes. Un compte sans tri est un compte trompeur.

Trois règles neuves :

- **539-A · `|| 0` SUR UN COMPTE N'EST PAS UNE INVENTION** — `len()` ne rend
  jamais `null` ; afficher 0 quand il y a zéro élément est **vrai**.
- **539-B · UNE ATTÉNUATION PEUT ALIMENTER UN FORMATEUR HONNÊTE** —
  `(r.ts||0)*1000` arrive dans `VX.fmt.ago`, qui rend `'—'` pour 0.
- **539-C · MESURER LA SOURCE ET LE RENDU, PAS L'UN OU L'AUTRE** — 24 champs
  nuls réellement servis d'un côté, 272 formateurs honnêtes de l'autre : c'est
  le **croisement** qui répond, pas l'un des deux comptes.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 106 atténuations à racine inconnue** ;
**`initSettings`, mesurée partiellement** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis et les 255 sélecteurs littéraux sans
identifiant** ; **la définition du corpus de routes du 511-A** ; **l'ampleur du
518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les
33 identifiants reconstruits** ; **les 92 rapports non additionnés du 526** ;
**les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 154 (+1)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
