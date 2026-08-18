# SKYLER — LOT 602 · LE DOSSIER 531-A EST CORRIGÉ

**Premier lot de CORRECTION depuis le 514.** L'humain a donné son accord
explicite pour finaliser le produit ; la boucle sort du mode « mesurer sans rien
toucher ».

## Ce que le lot corrige

**Deux zones d'Opportunités échouaient en silence.** Sur erreur réseau, elles
retournaient sans un mot — laissant une colonne vide et muette, contraire à
l'invariant produit « donnée absente → mention honnête ».

| site | avant | après |
| --- | --- | --- |
| `renderFunnel` — colonne entonnoir | `catch(e){return;}` → **colonne vide et muette** | `VX.states.error('Entonnoir indisponible')` |
| `renderFunnel` — étages vides | `return;` → **rien** | `VX.states.empty('Entonnoir vide — aucun etage retourne par le moteur.')` |
| `loadSkylerRank` — classement | `catch(e){return;}` → **section absente** | la section existe et affiche `VX.states.error('Classement Skyler indisponible')` |

Les deux états portent les boutons d'action de `VX.states.error` — **Réessayer**
et **Ouvrir Système** — comme partout ailleurs dans le produit.

## La preuve, en vrai Chromium, avec l'échec injecté

Trois passes sur `/opportunities`, viewport 1440×900 :

| passe | erreurs console | texte rendu | zone |
| --- | --- | --- | --- |
| **1. nominal** | **0** | 4 662 car. | — |
| **2. entonnoir en échec (500)** | 2 *(les 500 injectés)* | 4 382 car. | `⚠ Entonnoir indisponible · Réessayer · Ouvrir Système` |
| **3. sweep en échec (500)** | 2 *(les 500 injectés)* | 3 027 car. | `CLASSEMENT SKYLER — …` + `⚠ Classement Skyler indisponible` |

Les deux erreurs console des passes 2 et 3 **sont les 500 que j'injecte
moi-même** — pas un défaut.

## L'arrêt du lot — mon harnais de vérification a passé À VIDE

Premier jet : les trois passes rendaient **exactement 4 662 caractères** et mon
contrôle annonçait « 531-A CORRIGÉ : OUI ». **Faux succès.** Le contrôle testait
la **non-vacuité** de la zone, et la zone était pleine **parce que le fetch avait
réussi** : l'échec n'avait jamais eu lieu.

Cause : **Playwright n'intercepte pas les requêtes qui passent par un service
worker.** Sans `service_workers='block'`, `page.route` ne voit rien.

Deux durcissements : blocage du service worker, et **vérification du TEXTE
attendu** (`'Entonnoir indisponible'`) au lieu de la non-vacuité. C'est
exactement **600-A** — une calibration qui passe à vide est pire qu'une qui
échoue — appliquée le lot suivant, sur mon propre harnais.

**Arrêtés avant publication : 232 → 233 (+1).**

## Ce qui a changé, et ce qui n'a pas bougé

- **2 fichiers de production** : `vertex/ui/pages/opportunities_page.py`,
  `vertex/app/routes/system.py` (bump du cache).
- **5 gardiens** qui épinglent la version du service worker, mis à jour de
  `td-shell-v187` à **`td-shell-v188`** — c'est la procédure documentée, pas une
  complaisance : un octet servi change, le cache hors-ligne doit être purgé.
- **MD5 des 8 pages : 7 identiques, 1 changée** — seule `/opportunities` bouge
  (`6a22a6abbd03` → **`c1b5c52e18c5`**). Les sept autres sont identiques à
  l'octet, ce qui borne le changement exactement là où il devait être.
- **Suite : 2864 passed / 0 skipped.** Aucun test ajouté, aucun retiré.
- **Sondes** : snapshot pris avant, restauré après, **écart final AUCUN**.
- **READONLY intact** : aucun ordre, aucun chemin d'écriture touché.

## Ce que le lot n'établit pas

- **Que les autres pages n'aient pas le même défaut.** Seule `/opportunities`
  a été corrigée ; les silences équivalents ailleurs sont **nommés, pas
  traités** — ils viennent ensuite.
- Que ces deux zones soient les seules d'Opportunités : les cinq vues
  principales étaient déjà couvertes par le `catch` de `boot()`, **vérifié par
  lecture**, mais je n'ai pas exercé chacune en échec.

## Règles neuves

- **602-A — UN HARNAIS DE VÉRIFICATION DOIT PROUVER QUE LA VOIE D'ÉCHEC A ÉTÉ
  EXERCÉE.** Un texte rendu identique dans la passe nominale et dans la passe
  en échec est le signe que l'échec n'a pas eu lieu. Comparer les tailles.
- **602-B — UN SERVICE WORKER REND UNE INTERCEPTION RÉSEAU INVISIBLE.**
  `page.route` de Playwright ne voit pas les requêtes servies par le SW ;
  `service_workers='block'` est obligatoire pour tester une voie d'échec.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **2 fichiers de production modifiés, 5 gardiens de version mis à jour**, bump
  SW `td-shell-v187` → **`td-shell-v188`**.
- MD5 des 8 pages : **7 / 8 identiques**, `/opportunities` = `c1b5c52e18c5`
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**
- Suite : **2864 passed / 0 skipped**
- Navigateur : **3 passes, 0 erreur console en nominal**, voie d'échec exercée
  et prouvée.

## Comptes

- Arrêtés avant publication : **233 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
- **Dossiers produit corrigés : 1** *(531-A, ouvert au lot 531, fermé ici)*
