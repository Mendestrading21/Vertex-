# SKYLER LOT 239 — Desk sync round-trip côté client RÉEL (constat, 0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-239` (base : lot 238 fusionné)

## Objet

Le desk sync est l'invariant n° 1 de CLAUDE.md (17 clés / 4 listes,
gardien pytest vert) et la préférence utilisateur centrale (« tout
synchronisé automatiquement au lancement ») — mais le CHEMIN CLIENT
réel (push débouncé, pull au boot, last-writer-wins) n'avait jamais
été prouvé en navigateur. Fait ici, en démo, avec sauvegarde préalable
de `desk_data.json` et nettoyage PAR LE PROTOCOLE de l'app (jamais
d'édition à la main — règle n° 6).

## Protocole et résultat — 0 défaut

| Étape | Mesuré |
|---|---|
| 1. Écriture locale | `toggleFavorite('TSLA')` → favori local ✔, `deskTs` posé ✔ |
| 2. Push débouncé (1200 ms) | serveur interrogé après 2,5 s : **ts serveur = ts client à la milliseconde près** (1786120727568) et TSLA présent dans `myFavs` du blob ✔ |
| 3. « Appareil neuf » | `localStorage.clear()` + rechargement → le pull au boot **restaure TSLA, le deskTs et 5 clés desk** ✔ |
| 4. Nettoyage | favori retiré côté client → push → **TSLA retiré du serveur** (l'état d'avant-test est rétabli par le protocole) ✔ |
| Erreurs console | 0 ✔ |

La chaîne complète — écriture → débounce → POST /api/desk →
persistance serveur → pull → réhydratation du store — fonctionne
exactement comme conçue. La préférence « tout synchronisé
automatiquement au lancement » est PROUVÉE côté client, pas seulement
gardée côté serveur (round-trip pytest du lot 84, backups du 178,
clés du gardien desk sync).

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : constat pur.

## Preuves

- JSON du protocole (4 étapes) dans ce rapport ; `desk_data.json`
  sauvegardé avant test (scratchpad) et remis en état par le protocole.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 240 : MINI-BILAN 236-240. Purge terminal.py toujours EN ATTENTE
d'accord humain explicite.
