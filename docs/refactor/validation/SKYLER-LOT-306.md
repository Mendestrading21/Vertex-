# SKYLER LOT 306 — Cartographie moteur → UI : couverture complète (6 pistes)

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-306` (base : lot 305 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste — une donnée moteur servie mais non affichée ? (calibrage strict)

Méthode : lire les payloads RÉELS des API en DEMO, puis vérifier dans
le code des pages où chaque donnée vit. 6 candidates, verdicts :

| Donnée servie | Verdict | Domicile |
|---|---|---|
| `regime.adjustments` (priorité setups, confirmations, nouveau risque) | AFFICHÉE | Marchés (chips) + Aujourd'hui (résumé) |
| `regime.notes[]` | rien à afficher | régime CONNU → toujours `[]` (moteur L93) ; INCONNU → déjà éditorialisé dans Marchés (« Moins de 3 dimensions qualifiées… ») |
| `top_stocks[1..]` + bloc `vertex` (p_win, edge) | AFFICHÉS | Opportunités (shortlist : « p XX % », comparateur pwin/edge) |
| `scan detail.vx_*` | AFFICHÉS | Opportunités (grep L99/151/167) |
| `command.validation` (DSR, PBO, dégradation, note prudence) | AFFICHÉE | Intelligence (rows DSR/Dégradation/PBO, L553-558) |
| `command.portfolio_score` | consommé UNIQUEMENT par les pages legacy ORPHELINES de terminal.py (L3051/5870) — celles que la purge É1 supprime ; l'afficher sur /portfolio dupliquerait la synthèse existante (domicile unique) | aucun changement — sort lié à É1 |

**Conclusion : couverture moteur → UI complète sur le périmètre
calibré — aucune lacune ne justifie un changement.** Le seul reliquat
(`portfolio_score`) est un argument de PLUS pour la purge É1 (données
calculées pour du code mort).

## Preuves

Suite complète : **2516 passed / 2 skipped** (référence maintenue).

## Décision SW

**Pas de bump** (`td-shell-v186`) : docs seulement.

## Suite

LOT 307 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
