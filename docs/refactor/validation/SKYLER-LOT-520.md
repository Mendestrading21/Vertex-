# SKYLER LOT 520 — Première mesure de ce que l'utilisateur **voit** : les chargeurs exécutés se comportent **correctement**, états vides honnêtes compris. Et j'ai failli publier un faux dossier de rang 2 — l'erreur JavaScript brute venait de **mon banc**, pas du produit

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-520` (base : lot 519 fusionné,
`6dddd28e`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)** — la dette que le 519 venait de créer. Il avait établi que les vues sans
test sont **câblées** ; il ne les avait pas **exécutées**. La question restait
entière : **qu'est-ce que l'utilisateur voit ?**

Cinq vues concernées — les sept du 518-A moins les deux que le 519 a montrées
inatteignables.

## L'instrument, et son interdit

Technique validée aux lots 504-511 : extraire la fonction du **JS servi**,
l'exécuter sous node avec des stubs, capturer ce qu'elle écrit. **`VX.fetch` est
un STUB : aucun appel ne sort.**

Ajout de ce lot : une **résolution automatique des voisines** — un chargeur
appelle des auxiliaires définis ailleurs dans le même script ; le harnais les
extrait à la demande, jusqu'à douze, plutôt que de me faire conclure « la vue est
cassée » quand seul mon stub manque.

## Le résultat, sur les trois vues exécutables

```text
/system?view=automations
   A · charge riche   3 conteneurs · 2208 o · tableau des jobs complet
   B · charge VIDE {} 3 conteneurs ·  329 o · « Registre de jobs vide. »
                                              « Rapport non généré (serveur
                                                fraîchement démarré ?) »
   C · fetch en ÉCHEC 3 conteneurs ·  182 o · « Registre indisponible : HTTP 500 »

/portfolio?view=options
   identique aux trois régimes · « Aucune position option — le sélecteur
   privilégie les CALLS (max 3, dont 1 PUT tactique). »

/journal?view=progression
   identique aux trois régimes · 967 o peints
```

**`/system?view=automations` est exemplaire** : trois comportements distincts,
tous honnêtes, tous en français. Données présentes → un tableau. Charge vide →
un état vide **qui explique pourquoi** (« serveur fraîchement démarré ? »).
Échec → une bannière qui nomme la cause (« HTTP 500 »).

Les deux autres peignent **la même chose dans les trois régimes**, et c'est
normal : elles lisent les **données du poste** (`E()`, localStorage), pas la
charge réseau. Leur état vide est honnête et explicite.

## J'ai failli publier un faux dossier de rang 2

Mon premier jet utilisait un régime « données absentes » où `VX.fetch` **rendait
`null`**. Résultat peint :

```text
« Registre indisponible : Cannot read properties of null (reading 'jobs') »
```

Un message d'erreur JavaScript brut, en anglais, dans l'interface. **J'avais là
un dossier visible de rang 2** — le premier depuis le 514.

Vérification avant publication, dans `vx-core.js` :

```js
VX.fetch = function (url, …) {
  …
      const r = await fetch(url, { signal: ctl.signal });
      if (!r.ok) throw new Error('HTTP ' + r.status);
  …
  throw lastErr;      // ← ELLE LÈVE. Elle ne rend JAMAIS null.
```

**Mon régime n'existe pas.** Les deux dégradations réelles sont une charge
**vide `{}`** — le 512 a mesuré que `/api/weekly` rend exactement cela — et une
**exception propagée**. Refait avec ces deux régimes : le produit répond
« Registre de jobs vide. » et « Registre indisponible : HTTP 500 ». **Honnête
dans les deux cas.**

**L'erreur brute venait de mon stub, pas du dépôt.** C'est le plus près que je
sois passé de publier un défaut inexistant.

**Arrêtés avant publication : 116 → 118.** Le second : les quatre « exceptions »
du premier passage (`behavioral is not defined`, `get is not defined`,
`E(...).positions is not a function`) étaient **mes stubs manquants**, pas des
vues cassées.

## Deux vues sur cinq n'ont pas été exécutées — et je ne les exécuterai pas

`loadEvents(sym)` et `loadVolatility(sym)` (`options-intel.js`) échouent dans mon
harnais sur un auxiliaire `get()` que la résolution automatique n'atteint pas.
Mais surtout, **lues**, elles appellent :

```js
get('/api/options/event-risk/' + encodeURIComponent(sym))
get('/api/options/volatility/'  + encodeURIComponent(sym))
```

**L'innocuité réseau des routes `/api/options/*` n'est pas établie** — c'est une
interdiction permanente. Même avec un harnais parfait, je ne mesurerais que ma
propre charge fabriquée. **Je m'arrête donc à la lecture**, et ce qu'elle montre
est correct :

```js
if (!sym) { el.innerHTML = '<div class="vx-empty">Saisis un symbole.</div>'; return; }
```

Un état vide honnête quand aucun symbole n'est saisi — ce qui est **l'état
d'arrivée** sur ces deux vues, puisqu'elles attendent une saisie.

## Ce que ce lot NE trouve pas — et c'est le résultat

**Aucun dossier.** Sur les trois vues exécutées, aucune n'affiche de chiffre
faux, aucune ne reste en squelette, aucune ne laisse fuir un message technique.
Les états vides sont en français, explicites, et distinguent « vide » de
« indisponible » — ce qui est précisément l'invariant produit (« donnée absente →
état honnête »).

Après quatre lots (518 → 520) sur l'axe du produit servi, la conclusion est
franche : **la surface visible se tient**. Ce qui manque, ce sont des **tests**
(518-A) et des **portes d'entrée** (519-A), pas de la correction.

## Le second contrôle — ce que le harnais exclut

- **Mes stubs ne sont pas un navigateur.** Le DOM est factice, `VXCharts` est un
  proxy qui compte les appels sans dessiner. Une vue peut se comporter
  différemment en vrai.
- **La charge riche du régime A est FABRIQUÉE par moi.** Qu'un chargeur peigne un
  tableau avec ma charge ne prouve pas qu'il peindra bien avec la vraie.
- **Ma calibration de variété est mal écrite** : elle compare des **paires** de
  régimes et ne peut pas aboutir avec trois. Mesuré directement, la variété est
  pourtant démontrée — `/system?view=automations` peint **2208 / 329 / 182
  octets** selon le régime. Je publie le défaut de la calibration plutôt que de
  le corriger en silence (règle 509-A).
- **Deux vues sur cinq non exécutées**, pour une raison de sécurité réseau qui ne
  se lèvera pas.

## Ce que le dépôt fait bien, mesuré

- **Trois régimes, trois réponses honnêtes** sur `/system?view=automations` — y
  compris un état vide qui **explique la cause probable**.
- **`VX.fetch` lève au lieu de rendre `null`** : c'est exactement ce qui empêche
  le message technique que je croyais avoir trouvé. Le contrat est propre, et il
  protège l'interface.
- **Deux tentatives de reprise** (`for attempt = 0; attempt < 2`) avant de lever,
  avec attente croissante : une panne passagère ne vide pas l'écran.
- Les états vides distinguent **« vide »** de **« indisponible »**.

## Portée — ce que ce lot NE dit PAS

- **Trois vues sur cinq**, et sous stubs.
- **Aucun navigateur, aucun POST, aucune route interdite appelée**, aucun appel
  réseau du tout : `VX.fetch` et `fetch` sont tous deux stubés, ce dernier levant
  « RESEAU INTERDIT » si jamais il était atteint.
- Mesuré en **DÉMO**, scan à 20 titres.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0**.

Ce lot ne rapporte aucun dossier et rapporte quelque chose de plus rare : **la
preuve qu'un défaut que je croyais tenir n'existait pas**. Cent dix-huit fois
maintenant qu'un résultat faux est arrêté avant publication — mais c'est la
première fois qu'il s'agissait d'un **défaut visible**, la catégorie qui manque
le plus à la feuille et donc celle que j'avais le plus envie de trouver.

C'est exactement là que la discipline sert : **le dossier le plus désirable est
celui qu'il faut vérifier le plus durement.**

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **mesurer le contenu des 23 routes non appelées**
(dette du 512, ouverte depuis neuf lots — la plus ancienne) ; **le français
construit en JavaScript** ; **l'assemblage entre fonctions** ; **la condition
`k ≤ 5` sur un scan réel** ; **recribler les chiffres publiés par motif
textuel** ; **le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 118 (+2)** ; publiés
puis corrigés **15** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
