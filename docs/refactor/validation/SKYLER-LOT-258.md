# SKYLER LOT 258 — DEMARRER_ICI.md ↔ réalité (3 défauts) · .env.example : exact

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-258` (base : lot 257 fusionné)

## Objet

Suite de l'audit des docs d'accueil (README au lot 257) : les deux
autres portes d'entrée du dépôt — `DEMARRER_ICI.md` (guide de
démarrage) et `.env.example` (modèle de configuration) — auditées
contre la réalité.

## `.env.example` — verdict : EXACT, non touché

Vérifié ligne par ligne : sémantique de `VERTEX_CODE` correcte (« Vide
→ écoute 127.0.0.1 seulement » — conforme au comportement gardé lot
218), invariant READONLY énoncé, sections IBKR/TradingView/fuseaux à
jour. Rien à corriger.

## `DEMARRER_ICI.md` — 3 défauts corrigés

1. **Nom de dossier périmé** : « Ouvre le dossier `IBKT-DASHBORD-` »
   (×2, Mac et Windows) → le dossier du projet s'appelle `Vertex-`.
2. **Table des espaces pré-refonte** : Overview / Matinal / Comité /
   Recherche / Décisions / Santé / Fiche titre → remplacée par les
   **8 espaces canoniques réels** (Aujourd'hui, Marchés, Opportunités,
   Analyse, Portefeuille, Options, Journal, Système — mesurés 8×200 au
   lot 251).
3. **Badge inexistant** : « En haut à droite, le badge passe à 🟢 LIVE
   IBKR » → la réalité (vx-shell.js L205-209) est un état de source
   IBKR « Live / Différé / Hors ligne » dans le panneau d'état et
   l'espace Système → reformulé.

## Vérifications AVANT correction (calibrage)

- `Lancer_VERTEX_DEMO.command` / `.bat` : existent (la section DÉMO du
  guide est correcte — conservée).
- Indicateur live : cherché dans le shell réel avant de trancher —
  l'état IBKR existe bien, seule sa forme/son emplacement étaient faux.
- Le reste du guide (installation, TWS read-only, dépannage, rappel
  READONLY) : conforme — conservé.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs d'accueil seulement.

## Preuves

- Diff limité à DEMARRER_ICI.md (3 blocs).
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 259 : entretien espacé ou directive. Les 3 portes d'entrée du
dépôt (README, DEMARRER_ICI, .env.example) sont désormais alignées sur
la réalité. La purge attend « GO purge étape 1 ».
