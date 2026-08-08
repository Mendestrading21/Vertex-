# SKYLER LOT 384 — 6/6 : la veine « auditer les gardiens » se conclut

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-384` (base : lot 383 fusionné,
3609d94)

## Résultat de la passe

```text
snapshot quotidien du desk désactivé                     MORD
garde-fou de taille du snapshot neutralisé               MORD
redirection héritée /heatmap supprimée                   MORD
entrée Options retirée de PRIMARY_NAV                    MORD
/healthz vidé de son contenu réel                        MORD
collecte de /api/client-log neutralisée                  MORD
[témoin] commentaire reformulé                            ne mord pas — correct
```

**Six sur six.** Le témoin négatif reste muet, ce qui donne son sens au résultat.
**Aucun trou.**

## La veine se conclut — bilan honnête

Quatre lots, **environ 27 mutations** sur les gardiens que `CLAUDE.md` désigne
comme protégeant les règles critiques :

| lot | mutations utiles | trouvailles |
|-----|------------------|-------------|
| 381 | 4 | **1 trou** (repli `deskKeys()` servi non gardé) + **1 constat** (`vx_kit.JS` servi nulle part) |
| 382 | 5 | **1 écart** (« aucun littéral couleur » : 53 servis, gardien limité aux bleus) |
| 383 | 5 | 0 — deux « AUCUN » qui accusaient à tort |
| 384 | 6 | 0 |

**Les deux trouvailles sont concentrées dans les deux premiers lots.** Les deux
derniers n'ont rien donné, avec un protocole pourtant plus rigoureux à chaque
passe. C'est le signal convenu au lot 383 : **la veine est épuisée, je la ferme
plutôt que de m'y acharner.**

## Ce que ces quatre lots ont ÉTABLI — l'actif réel

Ce n'est pas rien : dix-sept invariants sont désormais **prouvés tenus par
mutation**, non plus supposés.

- **READONLY** basculé à False → mord.
- **Service worker** : version rétrogradée → mord ; fichier `vertex/static`
  modifié **sans bump d'empreinte** → mord.
- **Clés de sync desk** : renommage dans la source de comparaison → mord ;
  retrait dans le fichier statique servi → mord ; retrait dans le repli servi de
  `/system` → **ne mordait pas, désormais gardé** (lot 381).
- **Sorties news assainies** : `sanitize_news` retiré de `/news-feed` → mord ;
  retiré de la construction des événements → mord.
- **Filet desk** : rotation à 0 → mord ; snapshot désactivé → mord ; garde-fou de
  taille neutralisé → mord.
- **Navigation** : redirection héritée supprimée → mord ; entrée de `PRIMARY_NAV`
  retirée → mord.
- **Observabilité** : `/healthz` vidé → mord ; `/api/client-log` neutralisé → mord.
- **Vocabulaire des verdicts** vidé → mord.
- **Apostrophes françaises** déséchappées dans un bloc JS **servi** → mord.
- **Nom personnel** injecté dans une page servie → mord.
- **`scan_state`** réassigné dans un consommateur → mord.
- **Version du cœur** en recul → mord (plancher `>= 0.9.0`, précisé au 383).

Avant cette tranche, aucun de ces énoncés n'avait été vérifié autrement que par
la présence d'un test au vert. **Un test au vert qui ne mesure rien est plus
dangereux qu'un test absent** — c'était l'hypothèse de départ, et elle a produit
deux corrections réelles avant de s'épuiser.

## Rien touché, et c'est délibéré

Aucun fichier de production, aucun test ajouté : **il n'y a rien à corriger**.
Ajouter un gardien là où six mutations sur six sont déjà attrapées serait le
changement gratuit que la boucle s'interdit.

Un seul item mineur reste connu et **volontairement différé** : le commentaire
en tête de `vertex/static/vertex/js/vx-entities.js` — « MIROIR EXACT de
`__DESK_KEYS` (terminal.py) » — est faux depuis la purge É1. Le corriger
changerait un octet **servi**, donc imposerait un bump de service worker (donc
une invalidation de cache chez l'utilisateur), la mise à jour de `_EMPREINTE` et
une preuve MD5 complète. **Disproportionné pour un commentaire** ; il reste au
dossier.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 383, 3609d94) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Suite : **2793 passed / 2 skipped**, inchangée. SW : `td-shell-v187`.

## Portée

Vingt-sept mutations sur 2 793 tests restent un **sondage**, pas une preuve de
couverture. « MORD » signifie « attrape CETTE faute-là ». Les gardiens non ciblés
— la grande majorité — restent non vérifiés ; ce que je conclus, c'est que
**cibler les invariants critiques ne rend plus rien**, pas que toute la suite est
saine.

## Suite — et une question qui revient

Les pistes restantes de la veine sécurité/honnêteté sont fines : refus construits
en variable (377), formes imbriquées des promesses de retour (375), trois sites
de concaténation à constantes (374), les 38 `except: pass` « autres » (379). Elles
valent d'être prises à l'occasion, **pas comme programme**.

Le constat du bilan 380 tient plus que jamais : **le vrai goulot, ce sont les
quinze dossiers en attente de décision humaine**, dont plusieurs sont chiffrés à
l'unité — 604 Ko de HTML mort assemblés à chaque import, le filet desk qui perd
le travail de la journée, deux questions d'honnêteté d'affichage jumelles (363 et
379), et `vx_kit.JS` servi nulle part. L'agent les a mesurés et documentés ; il ne
peut pas les trancher.

LOT 385 : veille à cadence réduite sur les pistes fines, en attendant ces GO.
Prochaine échéance périodique : **~lot 390**.
