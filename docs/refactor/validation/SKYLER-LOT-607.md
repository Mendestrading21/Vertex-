# SKYLER — LOT 607 · UNE DONNÉE RÉELLE PRÉSENTÉE COMME ABSENTE

Le brief proposait `sendBeacon`. En lisant le code pour y répondre, le trou
était ailleurs : **le 604 a corrigé les trois écritures de la synchro du bureau
et n'a pas regardé la lecture.**

## L'invariant, pris à l'envers

Tout ce que la boucle corrige depuis le 602 relève du même principe : *donnée
absente → mention honnête*. Ce lot en trouve la **forme symétrique**, plus
dangereuse : **une donnée réelle présentée comme absente.**

```javascript
async function pull() {
  try {
    const r = await fetch('/api/desk'); const d = await r.json();
    …
  } catch (e) {}
}
```

**`r.ok` n'était jamais lu** — c'est exactement `604-A`, sur l'autre chemin — et
le `catch` était vide.

Conséquence, mesurée : sur un profil **neuf** dont le `GET` échoue, le bureau
s'affiche **vide**. « Aucun trade déclaré » et « bureau non synchronisé »
deviennent **indiscernables** — alors que le serveur, lui, a les données.

Le coût est d'une autre nature que celui du 604. Une écriture ratée se rattrape
toute seule au chargement suivant (`pull` compare les horodatages et repousse).
**Une lecture ratée, elle, fabrique une conclusion fausse dans la tête de
l'utilisateur** : il croit son journal vide.

## La preuve, rouge puis verte, dans le même banc

`/journal?view=track-record`, profil neuf à chaque passe, service worker bloqué
(**602-B**), `GET /api/desk` intercepté :

| | GET observés | bureau affiché | message | `desk_sync` |
| --- | --- | --- | --- | --- |
| **AVANT — nominal** | 1 | vide | aucun | `null` |
| **AVANT — GET 500** | 1 | **vide** | **aucun** | `null` |
| **APRÈS — nominal** | 1 | vide | aucun | **`'ok'`** |
| **APRÈS — GET 500** | 1 | vide | **« Bureau non synchronisé : tes données du serveur n'ont pas pu être chargées (HTTP 500). Ce qui s'affiche vient de cet appareil — n'en conclus pas que c'est vide. »** | **`'read-error'`** |

Le `GET` a eu lieu dans les **quatre** passes : la voie d'échec est **exercée**
(602-A). Et **la passe nominale ne dit rien d'anormal, avant comme après** —
le témoin immobile de `606-B`.

## L'arrêt du lot — j'ai failli publier « aucun message »

Mon banc échantillonnait les toasts **à 7 secondes**. Un toast vit **5,2 s** plus
0,35 s de fondu. Le message était donc **parti** quand je regardais, et mon
premier verdict après correctif annonçait « toasts : AUCUN ».

J'ai d'abord cru à un défaut du correctif et installé un `MutationObserver` —
qui n'a rien attrapé non plus. C'est une mesure **directe et datée** qui a
tranché : `.vx-toast` présent à 1,5 s, présent à 3 s, **absent à 6 s**. Le
message existait ; mon instrument arrivait après la fin.

**Deux instruments successifs ont dit « rien » sur une chose qui était là.** Le
banc échantillonne désormais **à 3 s, dans la vie du toast**.

**Arrêtés avant publication : 238 → 239 (+1).**

## Le second arrêt — une heuristique positionnelle sur du code

Mon gardien devait vérifier que le `catch` **englobant** de `pull()` n'est plus
vide. Je l'ai d'abord identifié comme « le dernier `catch` du bloc ». C'est
faux : le dernier est le `catch (e2) {}` interne de `VX.store.set`, un « au
mieux » parfaitement légitime. Le test **échouait sur le code corrigé**.

Identifié désormais **par sa profondeur**, pas par sa position.

**Arrêtés : 239 → 240 (+1).**

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « le silence de `sendBeacon` est irrémédiable » | **RÉFUTÉ dans sa conséquence** — l'échec n'est pas observable *à l'instant*, mais `pull()` le **répare tout seul** au chargement suivant (`localTs > d.ts → pushNow()`) |
| **(b)** | « le code de vérification est déjà là » | **CONFIRMÉ, et mieux que prévu** : ce n'est pas une détection, c'est une **réparation** |
| **(c)** | « le flush est rare » | **NON MESURÉ** — je n'ai pas instrumenté `pagehide` ; laissé ouvert plutôt que supposé |
| **(d)** | « si l'envoi échoue, la donnée est perdue » | **RÉFUTÉ** — `localStorage` garde tout et le push suivant rattrape, exactement comme au 604 |
| **global** | | **le piège a envoyé au bon endroit pour la mauvaise raison** |

**Le brief recommandait `sendBeacon` comme dossier n°1.** En allant vérifier,
le chemin s'est révélé **déjà réparé** — et le vrai trou était dans la fonction
même qui assure cette réparation. **Le brief est une source comme une autre.**

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure le **chemin d'écriture**. Le cas exclu : **le chemin de
lecture quand le serveur est plus récent** — un correctif du push qui casserait
le pull serait pire que le mal.

Vérifié, et **encodé dans le gardien** : `pull()` contient **exactement deux**
écritures `localStorage` (les clés du serveur, puis `deskTs`), **zéro**
`removeItem`, **zéro** `clear`. La lecture est restée une lecture.

## Ce que le lot n'établit pas

- **Que les états vides des pages disent eux-mêmes la vérité.** Le message est
  un toast global ; « Aucun trade réel déclaré » reste écrit tel quel sur
  `/journal`. Relier les deux — un état vide qui sait qu'il n'est pas synchronisé —
  demande de toucher chaque page : **nommé, non traité.**
- **La fréquence réelle d'un `GET /api/desk` en échec.** Injectée pour être
  observée, pas rencontrée.
- Que `sendBeacon` dise son échec : il ne le dira jamais. Ce que ce lot
  établit, c'est que **sa conséquence est déjà rattrapée** — ce qui n'est pas la
  même chose, et vaut mieux.

## Règles neuves

- **607-A — UNE DONNÉE RÉELLE PRÉSENTÉE COMME ABSENTE EST PIRE QU'UNE ZONE
  MUETTE.** Une zone vide se voit et se recharge ; un bureau vide se **croit**.
  Le chemin de LECTURE mérite la même exigence que le chemin d'écriture.
- **607-B — UN MESSAGE ÉPHÉMÈRE SE MESURE DANS SA VIE, PAS APRÈS.** Échantillonner
  un toast de 5,2 s à 7 s le rate et fait conclure au silence. Comparer l'instant
  de mesure à la durée de vie de ce qu'on mesure.
- **607-C — UNE HEURISTIQUE POSITIONNELLE SUR DU CODE EST FRAGILE ; LA
  PROFONDEUR, NON.** « Le dernier `catch` » attrapait un `catch` interne. Ce qui
  définit un bloc englobant est sa profondeur, pas son rang.

## Ce que le dépôt fait bien

- **`pull()` réparait déjà le beacon perdu** sans que personne ne l'ait écrit
  comme tel : la comparaison d'horodatages fait le travail. Le dossier nommé au
  604 était moins grave qu'annoncé.
- **Les `catch` vides internes de `pull()` sont justes** : une écriture
  `localStorage` qui échoue par quota ne doit pas casser la lecture. Le défaut
  était l'englobant, pas eux — et mon premier gardien confondait les deux.
- **Le correctif du 604 tient** : le gardien de ce lot vérifie aussi que
  `pushNow` continue de lire `r.ok`.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/static/vertex/js/vx-entities.js`,
  `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (6 tests, **4 rouges par mutation**) + **5 épingles**
  `td-shell-v191` → **`td-shell-v192`** + l'empreinte des assets et
  `_SW_VERSION` du gardien 361 (un octet sous `/static` a changé).
- MD5 des 8 pages : **8 / 8 identiques** — `vx-entities.js` est un fichier
  statique, **aucune page ne change d'un octet alors que leur comportement de
  synchro change**.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2881 passed / 0 skipped** *(2875 + les 6 du gardien neuf)*.
- Navigateur : **4 passes** (2 avant, 2 après), rouge puis vert sur le **même
  banc**, plus une mesure datée intermédiaire pour lever l'arrêt.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **240 (+2)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 6**
