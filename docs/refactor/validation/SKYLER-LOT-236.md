# SKYLER LOT 236 — Modal d'ajout d'entité : parcours complet + READONLY (0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-236` (base : lot 235 fusionné)

## Objet

Le dernier FLUX interactif du shell jamais testé en navigateur : le
formulaire progressif « + Ajouter » (3 étapes), avec la vérification
READONLY la plus sensible — c'est le SEUL endroit du produit où
l'utilisateur saisit une « position ».

## Protocole et résultat — 0 défaut

| Étape | Mesuré |
|---|---|
| Bouton + | modal « Ajouter » ouvert, champ ticker, barre d'étapes 1/0/0 ✔ |
| NVDA + Continuer | **6 destinations** (Favori, Watchlist, Suivi, Position, Alerte, Thèse/note), étapes 1/1/0 ✔ |
| Watchlist | formulaire (priorité, zone, thèse, catalyseur) + bouton Confirmer, étapes 1/1/1 ✔ |
| Confirmer | modal fermé et **NVDA réellement écrit dans la watchlist du store** (`VXEntities.watchlist()` le contient) ✔ |
| **READONLY** | texte des 3 étapes balayé (y compris le formulaire Position) : **0 vocabulaire d'ordre** {acheter, vendre, transmettre, buy, sell, passer un ordre} ET la mention explicite « Registre déclaratif — Vertex n'envoie JAMAIS un ordre » est présente ✔ |
| Erreurs console | 0 ✔ |

Classification : le formulaire « Position » est un registre
DÉCLARATIF (quantité, prix, stop — enregistrés au journal personnel,
synchronisés desk) ; l'invariant READONLY est affirmé DANS l'interface
elle-même, au seul endroit où la confusion serait possible.

Avec ce lot, TOUS les flux interactifs du shell sont prouvés en
conditions réelles : drawer/modal (229), palette (231), menu
contextuel (234), ajout d'entité 3 étapes avec écriture au store
(236).

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : constat pur.

## Preuves

- JSON du parcours complet (6 états) dans ce rapport.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 237 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
