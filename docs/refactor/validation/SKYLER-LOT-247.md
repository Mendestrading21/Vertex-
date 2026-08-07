# SKYLER LOT 247 — GRANDE SYNTHÈSE de la campagne de preuve (lots 214 → 246)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-247` (base : lot 246 fusionné)

## Ce que cette campagne était

Après la clôture de la tournée graphique TV (lot 204), la boucle a
basculé d'un mode « construire » à un mode « PROUVER » : 33 lots
(214 → 246) pour vérifier, mesurer et garder tout ce qui avait été
construit — sans jamais toucher au code sans raison mesurée.

## Les chiffres de la campagne

| Mesure | Début (lot 214) | Fin (lot 246) |
|---|---|---|
| Tests verts | 2472 / 2 skipped | **2486 / 2 skipped** (+14) |
| Service worker | v171 | **v173** (2 bumps, chacun porté par un correctif réel) |
| PR fusionnées | — | **33** (#247 → #279), toutes squash |
| Gardiens NEUFS | — | **6** (timeout IBKR, scan_state, écoute réseau, intégrité index, + hex nus 212/213 en amont) |
| Correctifs produit | — | **3** (crumb topbar, bouton retour, ligne de fraîcheur) — tous mesurés, minimaux, vérifiés |
| Protocoles navigateur | — | **~30** (Playwright, DEMO, discriminants) |

## Ce qui est PROUVÉ (pas supposé)

1. **Les 8 invariants de CLAUDE.md** (214-218) : desk sync 17 clés/4
   listes, sanitize_news 6 sorties, JS généré valide, IBKR readonly +
   timeout 45, scan_state jamais réassigné, filet desk_data, écoute
   127.0.0.1 sans code — 8/8 TENUS, 3 lacunes de garde comblées.
2. **Le rendu honnête** (219) : 8 pages, 0 NaN/undefined affiché,
   états —/n/d partout, étiquette démo confirmée serveur.
3. **La navigation** (221) : 31 liens × HTTP 200, 177 boutons câblés.
4. **Le responsive COMPLET** (222-224, 232-233, 244) : 8 racines
   (390+768) + 6 secondaires + 15 vues internes — 3 débordements
   réels trouvés et corrigés (ellipse crumb/retour v172, repli
   .vx-update v173), 0 faux correctif.
5. **Le shell interactif** (229-236) : drawer/modal (focus revient au
   déclencheur), palette ⌘K (Entrée navigue), menu contextuel
   (READONLY jusque dans le vocabulaire), modal d'ajout 3 étapes
   (« Vertex n'envoie JAMAIS un ordre » dans l'UI).
6. **L'infrastructure** (237-239) : service worker v173 réel
   (nettoyage des caches + 32/32 servies du cache — la doctrine
   bump=déploiement PROUVÉE), docs 0 référence morte, desk sync
   round-trip client (pull qui restaure tout après localStorage vidé).
7. **Les 4 parcours métier** (241-243, 246) : plan d'analyse actions
   (8 canvas + 32 SVG), contrat options (payoff/R:R « estimation
   modèle, pas une promesse »), positionnement GEX (radar 18/18,
   « n/d » honnête), journalisation d'une décision (écriture →
   serveur → persistance).

**0 défaut produit trouvé depuis le lot 232.** Le produit n'est plus
supposé correct : il est MESURÉ correct, du pixel au blob de sync.

## La doctrine qui a tenu la campagne

Calibrer AVANT de toucher ; jamais de changement gratuit ; jamais un
défaut déclaré sur la foi d'une heuristique (2 faux positifs d'outil
corrigés par vérification visuelle avant conclusion) ; chaque bump
justifié par un correctif déployable ; chaque constat chiffré et dit
honnêtement — y compris les 2 erreurs de la boucle elle-même
(balayage « complet » du 211, « payoff absent » du 242).

## Ce qui RESTE — et attend l'humain

1. **Purge de terminal.py** (~25-30 % de code mort cartographié, dont
   la page Journal héritée croisée au lot 246) — EN ATTENTE de ton
   accord explicite ; aucun octet ne sera purgé sans.
2. **Validation physique** : TWS réel + iPhone (vider le cache pour
   recevoir SW v173).
3. **Merge vers `main`** — uniquement sur ton accord explicite.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : synthèse, docs seulement.

## Preuves

- Suite complète : **2486 passed / 2 skipped**.
- Chaque affirmation ci-dessus est traçable vers son rapport
  SKYLER-LOT-214 → 246 (gardien d'intégrité index↔rapports vert).

## Suite

LOT 248 : entretien ou directive. La boucle continue.
