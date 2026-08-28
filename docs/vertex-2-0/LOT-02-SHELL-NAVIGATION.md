# Lot 2 — Coque et navigation · 12 pages

## Le problème résolu

La navigation alignait **sept entrées à plat** : Dashboard, Opportunités, Analyse,
Portefeuille, Options, Journal, Système. Rien ne distinguait ce qu'on regarde tous
les matins de ce qu'on explore ponctuellement. Marchés n'avait pas de page — il
redirigeait vers une ancre du Dashboard, ce qui rendait « une visualisation
dominante par sous-vue » structurellement impossible.

## La navigation 2.0

Groupée par **travail**, pas par architecture technique :

| Groupe | Pages |
|---|---|
| **Piloter** — ce que je regarde maintenant | Aujourd'hui `/` · Calendrier `/calendar` |
| **Explorer** — ce que j'étudie | Marchés `/markets` · Opportunités `/opportunities` · Analyse `/analysis` · Options `/options` · Simulateur `/simulator` |
| **Gérer** — ce que je possède et surveille | Portefeuille `/portfolio` · Suivi `/follow-up` · Performance `/performance` |
| **Intelligence** — ce qui explique | Vertex IA `/intelligence` |
| **Épinglé** | Système `/system` |

`NAV_GROUPS` porte les groupes ; `PRIMARY_NAV` reste un **registre plat** dérivé
d'eux. Les consommateurs qui itèrent sur la navigation — tests, mesures QA, palette
de commandes — n'ont pas eu à changer.

## Aucune page n'a disparu

| Ancienne URL | Aujourd'hui |
|---|---|
| `/journal` | **200**, rendu identique. Journal devient une sous-vue de Performance. |
| `/tracking` | **200**, rendu identique. Suivis devient Suivi. |
| `/markets` | **200** — page propre retrouvée, cinq sous-vues (`markets_page` existait déjà). |
| `/calendar` | **200** — page propre. `/opportunities?view=calendar` reste servi. |
| `/performance` | **200** au lieu d'une redirection vers `/journal`. |

Rediriger `/journal` aurait été plus propre en apparence. Mais l'URL est en favori,
liée dans le produit et présente dans une trentaine de bancs : **une fonction
existante ne doit pas devenir introuvable pour la commodité d'un plan de nommage.**

## Deux pages nouvelles, composées de ce qui existait

### Simulateur — `/simulator`

Ce n'est pas un nouveau moteur : c'est la réunion de capacités qui existaient et
n'étaient réunies nulle part.

| Classe | Prise en charge | Moteur existant |
|---|---|---|
| **Options** | Complète — scénarios cours × temps, décroissance temporelle, sensibilité IV, payoff, points morts, probabilité de gain, Greeks | `/api/options/simulate` · `/api/options/analyze` |
| **Actions** | Complète — payoff, point mort, perte maximale, résultat théorique par cours | `/api/options/analyze` (jambe `stock`) · `/api/pretrade/check` |
| **ETF** | Partielle — le véhicule oui, le look-through non | `/api/options/analyze` |
| **Forex** | **Non prise en charge** — aucun moteur, aucune donnée | — |

**Une capacité dormante remise en service :** `vertex.engines.multileg_lab` accepte
depuis toujours une jambe `type:'stock'` (multiplicateur 1) et calcule un payoff
d'action correct. **Aucune interface ne l'exploitait.** Vérifié avant usage : 50
titres à 180 → engagement 9 000 USD, point mort 180,00, perte maximale −9 000,
gain non borné. Le Simulateur compose ce moteur ; il n'en écrit pas un.

Le sélecteur de classe **annonce la prise en charge avant la saisie**. Laisser
remplir un formulaire Forex pour répondre ensuite « non pris en charge » serait un
piège.

`simulator.js` **ne calcule aucune valeur financière**. Il lit les champs, appelle
les endpoints, affiche ce qui revient. Les limites du modèle sont rendues **avec**
le chiffre, pas en note de bas de page.

### Calendrier — `/calendar`

Composé de `GET /cal-feed`, l'unique source d'événements agrégés : résultats
(`items[]`), macro (`macro[]`) et couverture du calendrier officiel.

**Deux honnêtetés particulières.**

1. `/cal-feed` **ne porte aucun champ `ts`**. Trois pages du produit écrivent
   `cal.ts || Date.now()` : elles affichent donc l'heure du **navigateur** comme
   fraîcheur de la donnée — toujours verte, et fausse. `calendar.js` ne reproduit
   pas ce raccourci : il affiche `updated`, qui existe, et déclare l'horodatage
   absent sinon. *Corriger l'endpoint relève du backend et sort du périmètre ; le
   besoin est consigné ci-dessous.*
2. Le calendrier macro officiel a une **date de fin de publication**. Au-delà, le
   moteur ne rend que des dates de règle, qu'il marque « approximative ». La page
   affiche cette couverture au lieu de laisser croire à un horizon infini.

**Quatre catégories n'ont aucune source, et la page le dit** dans un tableau de
couverture visible — pas dans une note : dividendes et ex-dates · expirations
d'options et OPEX · catalyseurs hors résultats · revues planifiées. Aucune n'est
fabriquée pour remplir une grille.

## Deux défauts vus en pilotant la page, pas en la relisant

1. **Le Simulateur rendait une action impossible à renseigner.** Le champ « prix de
   référence » vivait dans le bloc réservé aux options : en basculant sur Actions,
   il disparaissait — alors qu'il est requis. Prix de référence et horizon sont
   remontés au niveau commun ; seuls type et strike restent propres aux options.
   Trouvé en pilotant réellement le formulaire dans Chromium.
2. **Deux boutons échappaient au gardien `test_every_button_has_handler`.** Mes
   chips construisaient leur attribut dynamiquement (`{attr}="{valeur}"`), donc
   ni la machine ni un lecteur humain ne voyaient le câblage. Corrigé en écrivant
   les attributs **littéralement** et en câblant par délégation — le gardien n'a pas
   été affaibli, le code a été rendu lisible.

## Gardiens mis à jour, avec leur motif

Ces bancs décrivaient la forme précédente. Le produit a légitimement changé ; c'est
le banc qui suit, et chaque mise à jour porte sa raison en commentaire.

`test_redesign_ui` (12 entrées groupées ; Marchés redevient une page) ·
`test_journal_page` (`/performance` sert au lieu de rediriger) ·
`test_options_routes` (12 entrées de nav) · `test_continuity_shell` et
`test_launch_readiness` (`/journal` porte l'espace `performance`) ·
`test_neon_glass_01` (couverture déclarée = 12 espaces ; la règle CSS effective
était déjà générique, aucune régression de style).

## Service worker

`v220` → **`v221`** : la coque servie change de forme et deux pages arrivent avec
leur JS. Sans bump, un visiteur en v220 garderait l'ancienne navigation en cache et
ne trouverait ni Calendrier ni Simulateur. Les six gardiens de version et
l'empreinte `/static` suivent.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4246 passés**, 154 ignorés, 1 échec environnemental connu |
| Routes | **12/12 en 200**, plus `/journal` et `/tracking` conservés |
| Console navigateur | 0 erreur page sur les 12 routes |
| Débordement horizontal | 0 px, desktop **et** mobile, sur les 12 routes |
| Captures | `docs/vertex-2-0/preuves/lot-02-apres/` |

Interaction réellement pilotée dans Chromium :
`simulator-option-refus.png` (refus honnête sans prix réel),
`simulator-action-resultat.png` (résultat du moteur multi-jambes),
`simulator-comparer.png`.

## Limites déclarées

- Un appel refusé volontairement (`422 spot indisponible`) apparaît dans la console
  du navigateur comme statut de ressource. **Ce n'est pas une erreur applicative** :
  `pageerror` reste vide. C'est la trace du refus honnête du moteur.
- **Besoin hors périmètre consigné :** `/cal-feed` devrait porter un champ `ts`.
  Trois pages du produit affichent aujourd'hui une fraîcheur fausse à cause de son
  absence. La correction touche l'endpoint et n'appartient pas à cette refonte.
- Les six vues du Calendrier partagent une même chronologie filtrée par horizon.
  Les rendus propres à Semaine, Mois et Agenda appartiennent au lot 6.

## Rollback

`git revert` du commit. Les routes ajoutées sont additives ; aucune route existante
n'a été supprimée, aucun moteur ni store touché.
