# SKYLER LOT 537 — Les 51 appels non protégés du 534, exécutés un par un : **neuf chargeurs peignent, quatre se taisent — et les quatre sont ceux qu'on connaît déjà**. `loadLeaps` est disculpé par la lecture, `chips` par ses arguments

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-537` (base : lot 536 fusionné,
`39163692`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(z)** — la dette produit la plus lourde qui restait. Le 534 avait compté **51
appels de récupération non protégés sur 33 fonctions**, sans savoir, pour la
plupart, **ce que leur zone affiche en cas de panne**. Le 532 puis le 534 ont
montré deux fois que le statique accuse et que l'exécution disculpe. Il fallait
donc **exécuter**.

Liste des 33 **lue dans `l534_parseur.json`**, jamais recopiée (**522-A**).

```text
CALIB 1 · POSITIF   renderAnomalies (muet aux 531/532/534)    0 car.   OK
CALIB 2 · NÉGATIF   renderCalendar  (protégé)                50 car.   OK
```

## Trois arrêts — le premier allait publier huit routeurs comme « chargeurs muets »

**1. Mon filtre de limite d'instrument était trop étroit.** Je ne retenais que
« *X is not defined* ». Or `navigate` — le routeur, présent sur les **huit**
pages — échoue sur « *Cannot read properties of undefined (reading 'pathname')* » :
il lui faut un vrai DOM et un historique. **J'allais publier huit fonctions de
routeur comme chargeurs muets.** La bonne règle est l'inverse : **la seule erreur
légitime est celle que le régime INJECTE** (`HTTP 500`) ; toute autre erreur est
un harnais qui casse.

**2. `chips` sortait muette — parce que mon harnais l'appelait sans argument.**
Sa signature est `chips(hostId, inputId, load)` ; appelée à vide, elle fait
`$(undefined)` et **retourne immédiatement**. Ré-exécutée avec ses arguments,
elle **peint 19 caractères**.

**3. `loadLeaps` — la lecture réfute mon instrument.** Le 533 l'avait nommée
« candidat, non promu ». Elle pose bien un squelette puis appelle `board()`
sans `.catch`. Mais `board()` **rattrape sa propre panne** :

```js
function board() {
  if (_board) return Promise.resolve(_board);
  return VX.fetch('/api/options', { ttl: 120000 })
    .then(function (d) { _board = (d && d.board) || []; return _board; })
    .catch(function () { return []; });        // ← ne rejette JAMAIS
}
```

`board()` ne rejette jamais : le `.then` de `loadLeaps` s'exécute toujours, et
avec une liste vide il écrit **« Aucun LEAPS exploitable »**, un état vide
honnête. **Mon harnais mesure 0 ; le code dit le contraire, et c'est le code qui
a raison** (**532-B**). Cause du 0 identifiée : la résolution des fonctions
voisines injecte une déclaration qui **masque le `$` du harnais**, si bien que
`$('vx-lp-out')` rend `null` et que la fonction sort par sa première ligne.

**Arrêtés avant publication : 149 → 152.**

## La feuille — 25 fonctions nommées, et elle s'additionne

Les 33 entrées du 534 se répartissent d'abord en **8 appels hors de toute
fonction** (`(programme)`, non exécutables comme telles) et **25 fonctions
nommées**.

```text
   PEIGNENT en régime d'échec                        9
   MUETTES (0 caractère, sans limite d'instrument)   4
   LIMITES D'INSTRUMENT (comptées à part)           12
                                             TOTAL  25   FEUILLE : OK
```

## Ce qui peint

```text
/system      loadConnections      770 caractères
/portfolio   renderPerformance    569
/system      loadData             314
/            boot                 248
/portfolio   renderSynthese       221
/portfolio   renderOptions        147
/portfolio   renderPositions       61
/options     chips                 19   (avec ses arguments)
/options     loadStructure          7
```

## Ce qui se tait — **exactement le dossier déjà connu**

```text
/opportunities   renderRadar        0 caractère
/opportunities   renderStocks       0
/opportunities   renderOptions      0
/opportunities   renderAnomalies    0
```

Les quatre prennent **zéro paramètre** : leur mesure n'est pas dégénérée, et le
piège n°2 ne les concerne pas.

**Le dossier 531-A garde exactement son ampleur : quatre chargeurs, tous sur
`/opportunités`.** C'est la **quatrième** mesure indépendante — et la première
qui balaie **toutes** les fonctions non protégées du dépôt, pas un sous-ensemble.

## Les limites d'instrument, nommées une par une

```text
navigate            ×8   « Cannot read properties of undefined (pathname) »
/markets  boot           « VX.fetch.peek is not a function »
/system   initSettings   « keys.forEach is not a function »
/portfolio risk          introuvable — forme non `function NOM`
/options  loadLeaps      `$` masqué par la résolution des voisines
```

**Un « 0 caractère » causé par un harnais qui casse n'est pas un défaut
produit** (**531-C**). Ces douze cas sont comptés à part, jamais mélangés aux
quatre muets.

## Ce que le dépôt fait bien, mesuré

- **Neuf des treize fonctions réellement mesurables peignent en régime de
  panne**, dont `loadConnections` (770 caractères) et `renderPerformance` (569).
  Le motif dominant est **la dégradation honnête**.
- **`board()` rattrape sa propre panne et rend une liste vide** : un seul
  `.catch`, placé dans le helper, **désamorce tous ses appelants**. C'est le bon
  endroit pour le mettre.
- **`loadLeaps` écrit un état vide argumenté** — « Un LEAPS exige delta
  0,70-0,90, OI élevé et spread faible — non évaluable sans ces données. »
- **Les 51 appels non protégés ne sont pas 51 défauts** : après exécution, il en
  reste **quatre**, tous déjà connus et déjà documentés.

## Portée — ce que ce lot NE dit PAS

- **Douze fonctions sur vingt-cinq n'ont pas pu être exécutées** ; leur régime de
  panne reste inconnu. C'est la plus grosse réserve du lot, et elle est comptée.
- Les **8 appels hors de toute fonction** (`(programme)`) ne sont pas couverts.
- Le régime d'échec simulé est **une levée** ; une réponse tronquée ou un JSON
  invalide ne sont pas couverts.
- Les charges sont **fabriquées** ; les volumes peints ne valent pas pour les
  données réelles.
- **Aucun navigateur** : les stubs ne sont pas un DOM. **Aucun réseau** —
  `VX.fetch` stubé, `globalThis.fetch` lève.
- **Aucune correction engagée**, ni sur 531-A ni ailleurs.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** ; harnais pris dans `l523_balayage.py`
  (**531-B**) et contrôlé non vide.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Le lot **ferme deux dettes nommées** — `loadLeaps` (réfuté par la
lecture) et `loadStructure` (7 caractères, confirmé qu'il peint) — et **confirme
une quatrième fois** que 531-A ne dépasse pas `/opportunités`.

Ce qu'il faut dire sans le maquiller : **trois arrêts, et le premier était le
plus grave de la série récente**. Un filtre trop étroit et je publiais huit
fonctions de routeur comme des chargeurs muets — un faux dossier deux fois plus
gros que le vrai.

Trois règles neuves :

- **537-A · UN HARNAIS QUI APPELLE TOUT SANS ARGUMENT MESURE UN ÉTAT DÉGÉNÉRÉ** —
  `chips(hostId, inputId, load)` sortait muette ; avec ses arguments elle peint.
- **537-B · LA SEULE ERREUR LÉGITIME EST CELLE QU'ON INJECTE** — toute autre
  erreur est un harnais qui casse ; il faut filtrer par *ce qu'on a injecté*, pas
  par une liste de messages connus.
- **537-C · UN HELPER QUI RATTRAPE SA PROPRE PANNE DÉSAMORCE SES APPELANTS** —
  `board()` fait `.catch(() => [])`, donc aucun de ses appelants ne peut rester
  en squelette, quoi qu'en dise mon harnais.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, inchangée après
quatre mesures indépendantes).

Dettes nommées restantes : **les 12 fonctions non exécutables et les 8 appels
hors fonction** ; **les 36 accès DOM non suivis et les 255 sélecteurs littéraux
sans identifiant** ; **la définition du corpus de routes du 511-A** ; **l'ampleur
du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ;
**les 33 identifiants reconstruits** ; **les 92 rapports non additionnés du
526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ;
**mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 152 (+3)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé — quatre lots l'ont mesuré, aucun
ne l'a touché.**
