# Lot 29 — les commandes qui invitent au clic et ne peuvent rien produire

La doctrine produit interdit la « fausse fonctionnalité » : un bouton sans
gestionnaire, un lien qui ne mène nulle part. **Rien ne la mesurait.** Un
bouton inerte a exactement la même apparence qu'un bouton qui marche.

Trois outils sont nés de ce lot. Deux se sont trompés avant de servir, et
c'est la partie la plus utile de ce document.

---

## 1. Liens internes et identifiants dupliqués

`tools/vertex_2_0_liens.py` vérifie deux choses que rien ne regardait :

- **chaque `href` interne mène-t-il à une page ?** Trois façons de rater : un
  404, une redirection en boucle, ou — le défaut de la collision
  `/options/:sym`, corrigé au lot 8 — une route qui existe mais sert du JSON,
  et déverse des accolades dans le navigateur ;
- **deux éléments portent-ils le même `id` ?** `getElementById` rend le
  premier. Deux id identiques, et la moitié du code écrit dans le mauvais —
  sans erreur, sans trace. Ce genre de panne se lit comme « la donnée
  n'arrive pas ».

**Résultat : 0 id dupliqué, 0 lien cassé** sur 84 cibles distinctes atteintes
depuis les 65 routes. Un lien d'export vers `/api/` sert un fichier : c'est
voulu, et compté à part.

Une correction en chemin : la première version *naviguait* vers chaque cible.
Un lien d'export déclenche un téléchargement, et `goto` lève dessus. L'outil
demande maintenant les cibles en HTTP — statut et type suffisent, sans rendre
la page.

## 2. Boutons morts — et pourquoi on ne lit pas les écouteurs

`tools/vertex_2_0_boutons_morts.py`.

### Première version, et sa contre-épreuve

Interroger `DOMDebugger.getEventListeners` sur le bouton, puis sur chacun de
ses ancêtres, `document` et `window` compris — pour tenir compte de la
délégation d'événements, omniprésente dans ce dépôt.

Contre-épreuve : un bouton témoin, **sans le moindre gestionnaire**, inséré
dans la coque. **L'outil ne l'a pas vu.**

La raison est structurelle : la coque pose un écouteur de clic sur `document`.
Tout bouton a donc un ancêtre qui « écoute », et la mesure répond toujours
« vivant ». Elle n'aurait jamais rien trouvé — un zéro rassurant et faux.

### Deuxième version : cliquer, et regarder

On clique, et on observe s'il se passe **quoi que ce soit** : mutation du DOM,
requête réseau, tentative de navigation, écriture de stockage, défilement.

Sûreté — Vertex est en lecture seule, mais on ne s'en remet pas à cela :

- toute requête **non-GET est bloquée** avant de partir ; elle compte comme un
  effet sans être exécutée ;
- toute **navigation est bloquée** ; elle compte comme un effet ;
- la page est **rechargée entre chaque bouton** : un clic ne peut pas
  influencer le suivant.

### Deuxième faux positif : le défilement est un effet

Premier passage : « Opportunités » déclaré mort sur la page d'accueil. Or les
pastilles d'ancre de cette page ne font **que** défiler vers un bloc — et le
défilement ne mutait rien que l'outil regardait. Le défilement est devenu le
cinquième effet observé.

### Troisième faux positif : le repli fermé garde ses boîtes

Deuxième passage : six boutons déclarés morts sur les vues Options
*Positionnement* et *LEAPS*, tous « sans texte » alors que leur `textContent`
en portait. Signature connue — et **déjà documentée dans ce dépôt**, par
`vertex_2_0_etats_vides.py` : dans Chromium, le contenu d'un `<details>`
**replié** garde ses boîtes de mise en page. `innerText` rend `''`, le
rectangle existe, et Playwright refuse pourtant de cliquer.

L'outil forçait le clic (`force=True`), l'envoyait à des coordonnées où il n'y
a rien, et lisait le silence comme une panne. Deux corrections : on ignore ce
qui vit dans un repli fermé, et **on ne force plus le clic** — si Playwright
refuse d'atteindre un élément, l'utilisateur ne l'atteindrait pas non plus.

*On ne corrige pas ce qu'un outil n'a pas prouvé.* **Trois faux positifs**,
écartés avant qu'une seule ligne de produit ne soit touchée.

---

## 3. Ce que la mesure a trouvé : neuf commandes inertes

`/calendar?view=options` — **9 commandes mortes sur 15**.

```
« Aujourd'hui »  « 7 jours »  « 14 jours »  « 30 jours »  « 120 jours »
« Tout »         « Macro »    « Résultats »
« Mes positions seulement »
```

### La cause

`calendar.js` sort de `boot()` **avant** de câbler le moindre filtre quand la
vue est `options` :

```js
if (vue === 'options') {
  rendreEcheances();
  …                       // fraîcheur, couverture, panneau latéral
  return;                 // ← les filtres ne sont jamais câblés
}
```

Et c'est **juste** : cette vue ne lit pas `/cal-feed`. Sa donnée est le desk
local — vos contrats déclarés. Un horizon de sept jours n'a aucun sens sur une
liste d'échéances que vous avez vous-même saisies.

Ce qui était faux, c'est que la **barre de contexte** rendait quand même les
neuf commandes, identiques à celles des six autres vues.

### La correction

`_filtres()` devient `_filtres(view)`. Sur la vue Options, elle ne rend plus
aucun filtre — et **dit ce qu'elle mesure à la place** :

> **SOURCE** — Vos **contrats déclarés** — pas le calendrier officiel. Ni
> horizon ni type : cette vue ne filtre pas un flux, elle date ce que vous
> détenez.

On ne désactive pas les commandes : un bouton grisé promet encore quelque
chose. On ne les rend pas. Retirer sans rien dire serait une perte ; la barre
explique.

Vérifié après correction : **0 mort sur les 6 commandes restantes**, et la
vue `today` garde ses 15.

## 4. Un helper appelé par un nom qui n'existe pas

`/simulator` — « **Ajouter à la comparaison** » déclaré mort. Le gestionnaire
est pourtant bien câblé :

```js
var d = window.__vxSimDernier;
if (!d) { if (window.vxToast) window.vxToast('Lance d'abord une simulation.'); return; }
```

`window.vxToast` **n'existe nulle part** dans le produit. Le helper servi
s'appelle `VX.toast` (`vx-core.js`). Les trois appels étaient gardés par un
`if` sur ce mauvais nom : aucune erreur, aucune trace — juste du **silence**.

Conséquence pour l'utilisateur : il clique « Ajouter à la comparaison » avant
d'avoir lancé une simulation, et **rien ne se passe**. Pas de message, pas
d'indice. Quand l'ajout réussit, la zone de comparaison se remplit — mais la
confirmation attendue n'arrive jamais.

C'est le même motif que deux défauts déjà trouvés dans cette refonte : une
garde défensive qui transforme un bug en silence d'apparence honnête. Un `if`
sur un nom faux ne lève pas d'erreur ; **il rend la panne invisible**.

Corrigé aux trois appels, derrière un helper local nommé une fois. Le même
défaut existait dans `design_system_page.py` (« Classe copiée : … ») —
corrigé aussi.

## 5. Preuves

```
python tools/vertex_2_0_liens.py           0 id dupliqué · 0 lien cassé
                                           84 cibles, 65 routes — COMPLET
python tools/vertex_2_0_boutons_morts.py   contre-épreuve : le bouton témoin
                                           est détecté ; restauré, 0 mort
                                           COUVERTURE PARTIELLE — voir ci-dessous
python -m pytest                           4299 passés · 154 ignorés
                                           1 échec environnemental connu
python -m pytest tests/test_calendrier_filtres_lot29.py
                                           23 bancs, contre-épreuve exécutée
```

### Couverture du relevé des boutons : partielle, et dite

Le balayage complet des 65 routes **n'a pas été mené à son terme** dans cette
session. Il exige un rechargement de page par bouton — c'est le prix de la
rigueur : sans cela, un clic influence le suivant. **18 routes sur 65** ont été
couvertes, sur trois passages successifs (dont deux invalidés par les faux
positifs décrits plus haut). Les deux défauts trouvés l'ont été dans ces 18.

L'outil porte désormais un `--budget` par route : une route lente est déclarée
**NON COUVERTE** au lieu de bloquer le relevé en silence. Le reste des routes
est à balayer ; ce n'est pas un résultat vert, c'est un travail inachevé.

*Correction d'une erreur de diagnostic, faite en cours de route :* j'ai d'abord
conclu que l'outil « bloquait » sur `/opportunities?view=options`. C'était faux.
Python tamponne sa sortie standard quand elle est redirigée vers un fichier :
je lisais un tampon vide, pas un blocage. Un balayage a été tué sur cette
mauvaise lecture. L'outil se lance maintenant avec `python -u`.

Le gardien tient les **deux** moitiés : les filtres disparaissent là où ils ne
peuvent pas agir, et restent sur les six vues où ils agissent. Il vérifie
aussi que `calendar.js` sort bien tôt — si un jour cette vue câble les
filtres, le banc le dit, et il faudra les lui rendre.
