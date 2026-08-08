# SKYLER LOT 304 — Performance perçue : SAINE ; première baseline « contenu utile »

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-304` (base : lot 303 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — performance perçue (mesurée, pas supposée)

Sondeur : Navigation Timing (DCL) + échantillonnage 250 ms des
squelettes visibles et de la taille de texte → « temps avant contenu
utile » = 1er instant où le texte ≥ 60 % du final ET 0 squelette.

### Résultats (8 pages, DEMO, 1440)

| Page | DCL | Contenu utile |
|---|---|---|
| / | 264-341 ms* | 957 ms |
| /markets | 282 ms | 1 055 ms |
| /opportunities | 264 ms | 625 ms |
| /analysis | 280 ms | 363 ms |
| /portfolio | 291 ms | 362 ms |
| /options | 280 ms | 641 ms |
| /journal | 276 ms | 597 ms |
| /system | 311 ms | 682 ms |

\* la première mesure de / donnait 630 ms — artefact de FROID (premier
lancement navigateur + serveur) : re-mesures isolées 341/300/188 ms.

**Verdict : SAIN.** DCL dans la baseline du lot 72 (< 300 ms, /system
à 311 marginal), contenu utile < 1,1 s partout, 0 squelette visible à
1 s sur les 8 pages. Aucun défaut → aucun changement produit.

## Livré — l'outil et la PREMIÈRE référence « contenu utile »

`docs/refactor/validation/tools/probe_perceived_perf.py` — commité
avec usage, piège du froid documenté, et les baselines (DCL lot 72 +
contenu utile lot 304, jamais mesuré avant ce lot). Les prochaines
mesures ont désormais un point de comparaison.

## Preuves

Suite complète : **2516 passed / 2 skipped** ; compileall tools vert.

## Décision SW

**Pas de bump** (`td-shell-v186`) : outil/docs seulement.

## Suite

LOT 305 : purge É1 en PRIORITÉ dès déblocage ; sinon développement
(dernier angle d'audit neuf : parcours transverses à écriture locale ;
ensuite → améliorations produit calibrées).
