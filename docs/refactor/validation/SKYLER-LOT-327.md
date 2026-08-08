# SKYLER LOT 327 — `CLAUDE.md` redevient vrai (et une de mes affirmations corrigée)

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-327` (base : lot 326 fusionné,
fd39bba) · **Aucun code applicatif modifié**

## La piste

Les lots 323-325 ont retiré 33 % de `terminal.py`. Une dette classique reste :
la **documentation de pilotage** décrit encore l'état d'avant. `CLAUDE.md` est
le fichier que chaque session lit en premier — s'il ment, toutes les sessions
futures partent sur une carte fausse.

Trois affirmations vérifiées, trois fausses.

## 1. « Monolithe `terminal.py` (~10 500 lignes) » — faux

Il en fait **7 153**. Corrigé, avec l'historique (10 743 avant É1) pour que le
chiffre reste interprétable.

## 2. « Pages extraites : nav, options_lab, journal, vault, signals, sync_center, vx_kit, design_system » — trompeur

Vérification, module par module, du nombre de consommateurs **hors tests** :

| module `vertex/ui/` | consommateurs en production |
|---|---|
| `nav`, `vx_kit`, `sync_center`, `design_system`, `home_art` | 1 chacun — **servis** |
| `options_lab`, `journal`, `vault`, `signals`, `strategy_os` | **0** |

Ces cinq modules sont des **reliques** : leurs pages sont mortes (les imports
correspondants ont d'ailleurs été retirés de `terminal.py` au lot 324). Les
présenter comme « pages extraites » de l'architecture vivante induit en erreur.
Corrigé, avec un renvoi explicite vers ce rapport.

**Je ne les supprime pas** : elles rejoignent le dossier ouvert du lot 326
(24 fonctions + É2 + É3), qui attend une décision produit.

## 3. La règle critique n°1 — mon erreur du lot 323, corrigée

Au lot 323 j'ai réécrit la règle des clés de sync desk en annonçant « LES 3
listes servies : `vx_kit.py`, `journal.py`, `vx-entities.js` ». **`journal.py`
n'est pas servi** — je l'avais repris du gardien existant sans vérifier que le
module avait encore un consommateur.

Les listes réellement servies sont :

1. `vertex/ui/vx_kit.py` — `DESK_KEYS`, kit global présent sur toutes les pages
   (source de vérité) ;
2. `vertex/static/vertex/js/vx-entities.js` — `DESK_KEYS` ;
3. `vertex/ui/pages/system_page.py` — le **repli** de `deskKeys()`, utilisé si
   `VXEntities` n'est pas chargé. Cette troisième liste n'était citée nulle
   part dans la règle : c'est celle qu'on aurait pu oublier de mettre à jour.

La 4ᵉ copie, dans `vertex/ui/journal.py`, est signalée comme sans effet.
Le journal de l'utilisateur (`vxJournal`) est bien géré en production par
`vx-entities.js` (lecture, écriture, sync) — aucune donnée n'est en jeu.

## Constat mis en réserve pour un lot dédié

`system_page.py` affiche à l'utilisateur : « Clés synchronisées — N (contrat
`__DESK_KEYS` — aucune clé renommée) ». Le symbole `__DESK_KEYS` **n'existe
plus** depuis la purge É1. Le libellé n'est pas faux sur le fond (le contrat de
clés est bien tenu) mais il cite un nom disparu.

Le corriger change un octet servi → bump SW + mise à jour des 5 gardiens. Ce
n'est pas le périmètre de ce lot ; c'est noté comme candidat propre pour un
prochain lot, assumé avec son bump.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 326, fd39bba) ; arbre propre.
- Suite complète : **2501 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v186`) : seuls `CLAUDE.md` et les docs changent,
aucun octet servi.

## Suite

LOT 328 : veille active. Dossiers en attente de décision humaine — purge É2,
purge É3, les 24 fonctions du lot 326, les 5 modules `vertex/ui/` reliques,
et le libellé `__DESK_KEYS` de la page Système. Prochaine échéance
périodique : ~lot 330.
