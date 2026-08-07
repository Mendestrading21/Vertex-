# SKYLER LOT 223 — Pages secondaires à 390px : balayage discriminant (constat, 0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-223` (base : lot 222 fusionné)

## Objet

Étendre le protocole discriminant du lot 222 aux pages JAMAIS balayées
en responsive : les pages secondaires, et en **contexte de
navigation** (2 pages visitées avant → bouton retour visible — c'est
exactement là que le défaut intermittent du lot 222 se cachait).

## Protocole

Serveur `DEMO=1 NO_IBKR=1` (healthz ok/demo) ; Playwright 390×844 ;
visite préalable de `/` puis `/portfolio` (contexte navigation), puis
balayage de **6 pages secondaires** : `/titre/AAPL`, `/company/AAPL`,
`/analysis/ACN`, `/intelligence`, `/login`, `/design-system`.
Par page : `overflowX` document, éléments visibles dépassant le
viewport à droite (hors scroll interne voulu et hors off-canvas
aria-hidden), marqueurs malhonnêtes affichés (NaN/undefined/Infinity),
erreurs console.

## Résultat — 0 défaut sur les 6 pages

| Page | overflowX | Dépassements droits | Marqueurs | Erreurs console |
|---|---:|---:|---:|---:|
| /titre/AAPL | 0 | 0 | 0 | 0 |
| /company/AAPL | 0 | 0 | 0 | 0 |
| /analysis/ACN | 0 | 0 | 0 | 0 |
| /intelligence | 0 | 0 | 0 | 0 |
| /login | 0 | 0 | 0 | 0 |
| /design-system | 0 | 0 | 0 | 0 |

Le correctif du lot 222 (fil d'Ariane + bouton retour en ellipse,
shell partagé) couvre bien ces pages aussi — le contexte navigation
qui piégeait /portfolio ne piège aucune page secondaire.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : constat pur.

## Preuves

- JSON complet du balayage (6 pages × 4 mesures) dans ce rapport.
- Suite complète : **2482 passed / 2 skipped** (référence maintenue).

## Suite

LOT 224 : entretien suivant ou directive. Mini-bilan 221-225 attendu
au lot 225. Purge terminal.py toujours EN ATTENTE d'accord humain.
