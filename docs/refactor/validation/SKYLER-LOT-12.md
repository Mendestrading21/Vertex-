# SKYLER V2 — LOT 12 — RED-TEAM, SÉCURITÉ ET RELEASE CANDIDATE

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-12-red-team-rc`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `1a63dd3`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Fin du programme Institutional+ : lots 10 (mémoire) et 11 (knowledge graph)
livrés. Restaient à prouver : la règle « une note S/S+ sans red-team complétée
est invalide » (ADVERSARIAL_COMMITTEE §8, non appliquée par le moteur), la
robustesse adversariale des moteurs récents et l'audit sécurité final.

## 2. Problème

- Le moteur 0.1.0 plafonnait S/S+ sur blocs insuffisants, mais RIEN n'imposait
  la red-team : un futur branchement du contexte fondamental aurait pu produire
  un S+ sans passe adversariale — violation directe du comité.
- Trouvaille adversariale RÉELLE (test rouge d'abord) : `decision_memory._num()`
  acceptait NaN/inf — un prix NaN à la décision aurait produit des rendements
  NaN sérialisés dans les résultats d'horizon.

## 3. Périmètre

### Inclus

- règle red-team dans le moteur de décision + **bump `ENGINE_VERSION`
  0.1.0 → 0.2.0** (changement de règle = changement de version, DECISION_ENGINE
  §13) ;
- correctif NaN/infini dans `decision_memory._num` ;
- batterie adversariale (17 tests) : séries hostiles, prix extrêmes, attaque
  look-ahead par empreinte dupliquée, déterminisme, labels hostiles, verbes
  d'ordre, fichiers runtime/secrets, performance bornée ;
- audit RC final (ce rapport).

### Hors périmètre

- fusion vers `main` (JAMAIS sans accord explicite — la RC vit sur
  l'intégration) ; UI (aucune touchée) ; Constitution intouchée (la règle
  red-team est une règle du MOTEUR versionnée, pas un poids du profil).

## 4. Décision

- `apply_red_team_rule(level, red_team)` : fonction pure — S/S+ sans
  `red_team.complete` → plafonné à A avec raison explicite ; appliquée dans
  `score40` après le plafond « blocs insuffisants ». `build_packet`/`decide`
  acceptent un paramètre optionnel `red_team` (défaut honnête :
  `{'complete': False, 'basis': 'aucune red-team exécutée'}`) et la décision
  expose `red_team {complete, required, basis}`.
- La Constitution n'est PAS modifiée : ses 13 hard_gates restent tels quels ;
  la règle vit dans le moteur, versionnée — les décisions historiques 0.1.0 en
  mémoire restent liées à leur version (prouvé sous bump réel).
- `_num()` de la mémoire refuse désormais NaN/infini (test rouge → vert).

## 5. Implémentation

### Fichiers modifiés

| Fichier | Rôle | Modification | Risque |
|---|---|---|---|
| `vertex/engines/skyler_core.py` | moteur décision | `apply_red_team_rule` + packet/décision `red_team` + ENGINE_VERSION 0.2.0 | faible |
| `vertex/engines/decision_memory.py` | mémoire | `_num` refuse NaN/inf ; commentaire versionné générique | faible |
| `tests/test_red_team_lot12.py` | tests (nouveau) | 17 tests red-team + adversarial + sécurité | faible |

### Contrats et unités

- `ENGINE_VERSION` 0.2.0 — les agrégats mémoire séparent 0.1.0/0.2.0 sans
  recalcul (prouvé) ;
- `red_team` : `{'complete': bool, 'basis': str}` en entrée ;
  `{'complete', 'required', 'basis'}` en sortie de décision ;
- aucun autre contrat modifié — champs additifs uniquement.

## 6. Tests rouges avant correction

```text
python -m pytest tests/test_red_team_lot12.py -q
8 failed, 9 passed
  - 7 échecs règle red-team (fonction absente, version 0.1.0, statut non exposé)
  - 1 échec adversarial RÉEL : prix NaN/inf accepté par decision_memory._num
    → rendements non finis dans les horizons
```

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex
résultat : exit 0

python -m pytest tests/test_red_team_lot12.py -q
résultat : 17 passed in 1.46s

python -m pytest tests/ -q
résultat : 1367 passed, 2 skipped in 12.48s     (test_no_orders inclus, vert)
```

Aucun test existant cassé par le bump de version (toutes les références étaient
dynamiques — vérifié avant le bump).

## 8. Audit RC (runtime `DEMO=1 NO_IBKR=1`)

| Vérification | Résultat |
|---|---|
| `/healthz` | 200, `data_source: demo`, `ibkr_enabled: false` |
| `/api/skyler/ACN` | `engine_version: 0.2.0`, `red_team {complete: false, required: false}` exposé |
| `/api/skyler/memory` | nouvelles décisions figées sous `0.2.0`, séparées |
| `/api/client-log` | `{"count":0,"errors":[]}` |

### Audit sécurité

- aucun verbe d'ordre dans les 6 moteurs Skyler (testé par balayage source) ;
- `readonly=True` IBKR intact ; `test_no_orders` vert ;
- aucun fichier runtime/secret suivi par git (`skyler_memory.json`,
  `skyler_decisions.json`, `desk_data.json`, `.env`, `.vertex_secret`,
  `market_context_last.json` — testé contre `git ls-files`) ;
- labels hostiles = données JSON, jamais interprétés (aucun HTML serveur dans
  les moteurs, testé) ; l'assainissement news reste au point de sortie.

### Audit robustesse

- séries NaN/inf/négatives : anomaly, evidence_lab, knowledge_graph — aucun
  crash, aucun non-fini sérialisé, aucune arête inventée ;
- prix extrêmes (0, négatif, NaN, inf) : horizons `NON_MESURABLE`, jamais un
  rendement inventé ;
- attaque look-ahead (empreinte dupliquée) : dernière occurrence utilisée —
  jamais plus de barres que le réel ;
- déterminisme : `decide()` répété = sortie identique ;
- performance : graphe 60 titres × 60 points < 5 s (borné par test).

## 9. Invariants vérifiés

- [x] READONLY, aucun ordre, `main` intacte ;
- [x] Constitution intouchée (règle red-team = moteur versionné) ;
- [x] version du moteur bumpée avec la règle ; historique séparé par version ;
- [x] NaN/infini refusés partout où testé ;
- [x] aucune donnée inventée ; limites dites ;
- [x] démo/sans IBKR vérifiés ; aucun secret/runtime dans le diff ;
- [x] suite complète verte (1367/2 skipped) ; SW v94 inchangé.

## 10. Comparaison avant/après

| Mesure | Avant | Après | Interprétation |
|---|---:|---:|---|
| Tests | 1350 passed / 2 skipped | 1367 passed / 2 skipped | +17 tests du lot |
| ENGINE_VERSION | 0.1.0 | 0.2.0 | règle red-team versionnée |
| S/S+ sans red-team | possible en théorie | impossible (plafonné A) | comité appliqué |
| NaN dans la mémoire | acceptés par `_num` | refusés | trouvaille adversariale corrigée |

## 11. Risques et limites restantes

1. **La red-team n'a pas encore de producteur** : aucun pipeline ne fournit
   `red_team.complete=True` — donc S/S+ est structurellement impossible
   aujourd'hui (prudent par défaut). Brancher le vrai processus red-team
   (10 questions du comité) est un travail futur avec validation humaine.
2. **Validation humaine sur appareil physique** (exigée par le skill pour la
   RC) : ne peut pas être exécutée depuis cette session — RESTE À FAIRE par
   l'utilisateur (TWS réel, iPhone/desktop).
3. Les limites documentées des lots 10 et 11 (alignement de série, watchlist
   statique, corrélation brute) restent ouvertes et documentées.

## 12. Rollback

`git revert` du commit du lot. Les décisions figées sous 0.2.0 restent en
mémoire liées à 0.2.0 (jamais réécrites) — comportement voulu du ledger.

## 13. Contradictions et opinion minoritaire

- Contradiction assumée : le skill liste « red-team absente pour S/S+ » parmi
  les hard gates minimum, mais l'ajouter au profil aurait modifié la
  Constitution automatiquement (interdit). Résolution : règle du moteur,
  versionnée, même effet bloquant — la proposition d'ajouter la gate au profil
  V3 est DOCUMENTÉE ici et attend validation humaine.
- Opinion minoritaire : brancher immédiatement un pipeline red-team automatisé
  (agents) aurait permis des S/S+ réels ; rejeté — une red-team générée sans
  revue humaine risquerait d'être une formalité, exactement ce que §8 interdit.

## 14. Verdict

`GO AVEC RÉSERVES`

Justification : tous les audits automatisables sont verts (adversarial,
sécurité, déterminisme, performance, modes) ; les réserves sont documentées et
non masquées — (1) validation humaine sur appareil physique restante,
(2) red-team sans producteur (défaut prudent), (3) limites héritées des lots
précédents. Aucun risque trompeur ou dangereux connu.

## 15. Prochaine étape autorisée

Une seule étape : validation humaine de la RC sur appareil physique (TWS réel,
`/healthz`, pages, iPhone) — puis, avec accord explicite uniquement, merge de
`integration/vertex-skyler-v2` vers `main`.

**Arrêt après ce lot — validation humaine requise.**
