# SKYLER LOT 260 — Mini-bilan de la tranche 256-260

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-260` (base : lot 259 fusionné)

## Caractère de la tranche : mesurer le neuf, aligner les portes d'entrée

Deux mouvements : (1) une baseline de performance serveur jamais
chiffrée ; (2) l'audit systématique des documents d'ACCUEIL du dépôt —
ceux qu'un humain lit en premier — contre la réalité du code. Bilan :
**10 défauts de documentation corrigés, dont 2 touchant la sécurité.**

## Les 5 lots

| Lot | Livré | PR |
|---|---|---|
| 256 | BASELINE perf serveur : import terminal.py 11,68 s à froid / ~2 s à chaud ; TTFB 8 pages 1,3-1,9 ms — service instantané, coût du mort à l'IMPORT (métrique avant/après purge) | #289 |
| 257 | README ↔ réalité : 4 défauts dont 1 de SÉCURITÉ (« écoute 0.0.0.0 » prétendue vs réalité 127.0.0.1 gardée lot 218) | #290 |
| 258 | DEMARRER_ICI ↔ réalité : 3 défauts (dossier périmé, table d'espaces pré-refonte, badge inexistant) ; .env.example audité EXACT | #291 |
| 259 | SECURITE.md ↔ réalité : 3 corrections dont le BOUTON FANTÔME (« Se déconnecter » ne vivait que dans PAGE_SETTINGS orpheline → /logout) + repli 127.0.0.1 précisé | #292 |
| 260 | Ce mini-bilan | #293 |

## Les chiffres de la tranche

- **10 défauts docs corrigés** (4+3+3), dont 2 de sécurité — tous
  calibrés AVANT correction (chaque affirmation tracée vers sa ligne
  de code ; ce qui était vrai a été conservé et dit vrai).
- Défauts produit : **0** (28 lots consécutifs depuis le 232).
- Code produit touché : **0 ligne** (15 lots consécutifs, 246-260).
- Suite : **2486 passed / 2 skipped** — inchangée. SW : **v173**.
- 5 PR (#289 → #293), toutes squash. 1 redémarrage worker (256),
  reprise sans perte.

## La leçon de la tranche

Les documents d'accueil dérivent silencieusement : personne ne les
teste, et ils finissent par décrire un produit qui n'existe plus —
jusqu'à contredire la sécurité réelle (« déjà ouvert au réseau » alors
que le serveur est verrouillé sur 127.0.0.1). L'audit systématique
« affirmation par affirmation, tracée vers la ligne de code » les a
remis au vrai. Reste un candidat : `CLAUDE_VERTEX_REBUILD.md` (doc de
travail, pas une porte d'entrée — priorité basse).

## Ce qui attend l'humain

1. **« GO purge étape 1 »** — dossier complet : preuves (248),
   fourchette 31,4-48,7 % (249), outil robuste (252), liste É1 triée
   A/B/C (253), baseline de gain (256).
2. **Bouton de verrouillage visible** (ex. dans Système) — petit lot
   produit SUR DEMANDE (/logout couvre le besoin en attendant).
3. Validation physique TWS réel + iPhone (vider le cache → SW v173).
4. Merge vers `main` — accord explicite uniquement.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs seulement.

## Suite

LOT 261 : entretien espacé ou directive.
