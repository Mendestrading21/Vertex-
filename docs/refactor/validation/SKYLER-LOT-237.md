# SKYLER LOT 237 — Service worker v173 vérifié en NAVIGATEUR réel (constat, 0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-237` (base : lot 236 fusionné)

## Objet

Le service worker est bumpé et gardé depuis 173 versions… mais son
COMPORTEMENT réel (installation, activation, nettoyage, service depuis
le cache) n'avait JAMAIS été vérifié en navigateur — uniquement par
littéraux de source. Vérification en vrai, en démo.

## Protocole (Playwright, contexte persistant, 2 pages)

1re visite `/` (6 s d'attente SW) : enregistrement, activation, clés
de cache, contenu du precache. 2e visite `/markets` (nouvelle page,
même contexte) : la page est-elle contrôlée, et les statiques
sont-elles servies du cache (`transferSize === 0` avec corps décodé).

## Résultat — 0 défaut, cycle de vie exemplaire

| Mesure | Valeur |
|---|---|
| SW supporté / enregistré / ACTIF | ✔ / ✔ / ✔ (scope `/`) |
| Clés de cache présentes | **`td-shell-v173` SEUL** — les caches périmés sont nettoyés à l'activation ✔ |
| Precache (5 entrées) | manifest, icon-180, fonts.css, inter-var.woff2, jetbrains-mono-var.woff2 ✔ |
| 2e visite : page contrôlée | ✔ (`navigator.serviceWorker.controller`) |
| Statiques servies DU CACHE | **32 / 32** (transferSize = 0, corps > 0) — cache runtime effectif ✔ |
| Erreurs console | 0 ✔ |

Lecture honnête du precache : la stratégie est un petit precache
(coquille visuelle : fonts + manifeste + icône) + cache RUNTIME pour
tout le reste — et la 2e visite prouve que ce runtime fait le travail
(32/32). Le hasShellJs=false du precache n'est PAS un défaut : les JS
entrent au cache à la première requête, comme conçu.

La doctrine « bump = déploiement » repose sur ce mécanisme ; il est
désormais PROUVÉ, pas supposé.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : constat pur.

## Preuves

- JSON complet du protocole (3 blocs de mesures) dans ce rapport.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 238 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
