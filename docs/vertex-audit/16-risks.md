# 16 — Risques & garde-fous

## Risques produit (les plus graves)
| Risque | Gravité | Garde-fou |
|---|---|---|
| **Introduction d'un chemin d'ordre** (rupture lecture seule) | CRITIQUE | `READONLY=True`, workers `readonly=True`, 17 outils interdits, gardiens `test_no_order_execution_in_ui`, `test_ai_api.py`. Aucun lot ne touche ce périmètre sans re-vérifier ces tests. |
| **Chiffre faux présenté comme réel** (0-masquerade, mock silencieux) | ÉLEVÉ | Règle produit n°4 ; DAT-01 en Phase 2 ; badges DÉMO/MOCK ; provenance visible ; « je ne sais pas » autorisé. |
| **Statut live menteur** | ÉLEVÉ | `_sync_ibkr_state` (fraîcheur 75 s), badge dérivé du socket, jamais d'un flag config. |
| **Perte de données desk** (clé sync hors des 4 listes) | ÉLEVÉ | Gardien `test_desk_sync_keys_single_source_of_truth` ; `desk_backup_*` + `/api/desk/restore`. |

## Risques techniques de refonte
| Risque | Gravité | Garde-fou |
|---|---|---|
| Casse d'une page en fusionnant les cartes/tuiles (CMP-01/02) | Moyen | Migration progressive + alias temporaires + capture avant/après par page. |
| Suppression prématurée de la nav/sidebar legacy (IA-01/CMP-03) | Moyen | Confirmer zéro dépendance de rendu avant retrait ; redirections 301 internes ; bump SW + 3 tests. |
| Régression de précision par optimisation (perf) | Moyen | Preuve **byte-identique** (hash de scan) ; aucun chiffre affiché ne change. |
| SyntaxError silencieuse (apostrophe FR non échappée en JS) | Moyen | Échapper systématiquement (`aujourd\\'hui`) ; relancer l'app + `/api/client-log`=0. |
| Oubli de bump `td-shell-vN` → shell figé chez l'utilisateur | Moyen | Checklist par lot ; 3 tests d'épinglage. |
| Cloud sans IBKR/Claude → vérif live impossible | Faible | Valider en DEMO (`DEMO=1 NO_IBKR=1`), vérif live en local ; ne jamais présenter la démo comme réelle. |

## Risque de méthode
- **Réécriture aveugle** (interdite par l'utilisateur) : toujours lire le vrai code, comprendre les consommateurs,
  changer par lots limités et prouvés. On consolide, on ne reconstruit pas.
- **Divergence local/office** : synchroniser par fast-forward avant de reprendre (déjà appliqué : merge propre
  des 11 commits bureau sans perte).
