# SKYLER V2 — EXECUTION STATUS

> Branche d’intégration : `integration/vertex-skyler-v2`  
> Base historique : `agent/vertex-neon-glass-graphs`  
> Statut : **Skyler V2 Core livré — phase Institutional+ ouverte**.

## Source de vérité

Skill : `.claude/skills/vertex-skyler-v2/SKILL.md`

Références avancées ajoutées :

- `references/DECISION_ENGINE.md`
- `references/ADVERSARIAL_COMMITTEE.md`
- `references/DECISION_PACKET_SCHEMA.md`
- `references/SCENARIO_CALIBRATION.md`
- `references/ANOMALY_INTELLIGENCE.md`

## Phase Core — historique validé

| Étape | Statut | Preuve principale |
|---|---|---|
| Audit convergence | ✅ GO | `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md` |
| Lot 0 — Baseline | ✅ GO | `docs/skyler/BASELINE.md` |
| Lot 1 — Correctness options | ✅ GO | `docs/refactor/validation/SKYLER-LOT-01.md` |
| Lot 2 — Constitution V2 | ✅ GO | `docs/refactor/validation/SKYLER-LOT-02.md` |
| Lot 3 — Market Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-03.md` |
| Lot 4 — News/catalyseurs/anomalies | ✅ GO | `docs/refactor/validation/SKYLER-LOT-04.md` |
| Lot 5 — Skyler Core | ✅ GO | `docs/refactor/validation/SKYLER-LOT-05.md` |
| Lot 6 — Options Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-06.md` |
| Lot 7 — Portfolio Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-07.md` |
| Lot 8 — Neon Glass | ✅ GO | `docs/refactor/validation/SKYLER-LOT-08A.md` à `08E.md` |
| Lot 9 — Calibration infrastructure | ✅ GO infrastructure | `docs/refactor/validation/SKYLER-LOT-09.md` |

État observé avant l’expansion : environ 1 300 tests verts, service worker v94, IBKR READONLY intact, `main` non modifiée.

## Phase Institutional+ — nouvelle expansion

### Gouvernance installée

- [x] moteur de décision institutionnel documenté ;
- [x] comité contradictoire de 12 rôles documenté ;
- [x] Président Skyler unique producteur du verdict final ;
- [x] avocat du diable obligatoire ;
- [x] red-team obligatoire pour S/S+ ;
- [x] schéma canonique `SkylerPacket` défini ;
- [x] scénarios/probabilités/calibration renforcés ;
- [x] intelligence des anomalies renforcée ;
- [x] agents spécialisés installés ;
- [x] runbook et checklist étendus.

### Lots Institutional+

| Étape | Statut | Objectif | Rapport attendu |
|---|---|---|---|
| Lot 10 — Mémoire et discipline décisionnelle | ✅ FAIT — validé (« go sans validation humaine ») et fusionné | décisions immuables, classification des erreurs, biais récurrents, amélioration humaine contrôlée | `docs/refactor/validation/SKYLER-LOT-10.md` |
| Lot 11 — Knowledge Graph institutionnel | ✅ FAIT — en attente de validation | relations sociétés/secteurs/catalyseurs/portefeuille prouvables, propagation explicable, questions de recherche | `docs/refactor/validation/SKYLER-LOT-11.md` |
| Lot 12 — Red-team et RC finale | ✅ FAIT — GO AVEC RÉSERVES (validation physique restante) | stress adversarial, audit math/données/sécurité, release candidate | `docs/refactor/validation/SKYLER-LOT-12.md` |

## Agents Institutional+

- `.claude/agents/skyler-chair.md`
- `.claude/agents/skyler-devils-advocate.md`
- `.claude/agents/skyler-market-regime.md`
- `.claude/agents/skyler-options-risk.md`
- `.claude/agents/skyler-data-auditor.md`
- `.claude/agents/skyler-portfolio-risk.md`

Aucun sous-agent ne peut publier `final_decision`. Le Président Skyler est l’unique source canonique.

## Décisions établies

- `main` ne bouge pas sans accord explicite.
- Neon Glass/Skyler reste la base fonctionnelle.
- Une invocation Claude = une mission ou un lot.
- Aucun lot Institutional+ ne commence sans validation du précédent.
- Les calculs et décisions canoniques restent déterministes.
- Claude rédige mais ne crée ni ne modifie les chiffres.
- IBKR reste strictement READONLY.
- Aucune note S/S+ sans red-team indépendante.
- Aucune recalibration ou modification de Constitution automatique.

## Lot 10 — livré (2026-08-05)

- moteur `vertex/engines/decision_memory.py` : ledger immuable par version de
  moteur (gel de 31 champs), anti-look-ahead par empreinte de série, résultats
  aux horizons déclarés (5/20/60 séances, catalyseur estimé étiqueté, thèse et
  option honnêtement NON_APPLICABLE), taxonomie d'erreurs déterministe,
  10 biais surveillés, recommandations `EN_ATTENTE_VALIDATION_HUMAINE` ;
- routes : gel fail-safe dans `/api/skyler/<sym>` + `GET /api/skyler/memory` ;
- persistance runtime `skyler_memory.json` (gitignorée, bornée) ;
- 1332 tests verts / 2 skipped (+32) ; SW inchangé v94 (aucune UI touchée) ;
- interdictions respectées : pas de Knowledge Graph, pas d'UI, pas de
  modification automatique des poids/Constitution, `main` intacte, aucun ordre.

## Lot 11 — livré (2026-08-05)

- moteur `vertex/engines/knowledge_graph.py` : 4 relations prouvables
  (secteur F1 sourcé, co-mouvement F2 fenêtré, catalyseur daté F1, détention
  desk F1), provenance obligatoire par arête, propagation explicable saut par
  saut, dépendances cachées ≥ 2 liens indépendants, questions de recherche
  `NON_DOCUMENTE` — fournisseurs/clients/concurrents JAMAIS inventés ;
- routes lecture seule : `GET /api/skyler/graph` + `GET /api/skyler/graph/<sym>` ;
- 1350 tests verts / 2 skipped (+18) ; SW inchangé v94 (aucune UI touchée).

## Lot 12 — livré (2026-08-05)

- règle red-team du comité appliquée par le moteur : S/S+ sans red-team
  complétée = plafonné à A — `ENGINE_VERSION` 0.1.0 → **0.2.0** (règle changée
  = version changée), historique 0.1.0 séparé en mémoire, Constitution
  intouchée (proposition de gate profil V3 documentée, en attente humaine) ;
- trouvaille adversariale corrigée : NaN/infini refusés par la mémoire ;
- batterie adversariale : séries hostiles, prix extrêmes, attaque look-ahead,
  déterminisme, labels hostiles, verbes d'ordre, fichiers runtime/secrets,
  performance bornée — 17 tests ;
- 1367 tests verts / 2 skipped (+17) ; SW v94 inchangé.

## Lot 13 — livré (2026-08-05, travail continu autorisé)

- moteur **0.3.0** : `operational_state` déterministe (8 états DECISION_ENGINE
  §2.2, base explicite, jamais une décision finale) + `confidence` factorisée
  §7 (4 facteurs bornés avec base, plafonds UNKNOWN ≤ 0,55 / conflit ≤ 0,50 /
  contradiction ≤ 0,60, calibration figée à 0,50 sans historique — jamais
  100 %) ;
- le ledger mémoire fige désormais ces champs (31/31 champs vivants) ;
- 1386 tests verts / 2 skipped (+19).

## Lot 14 — livré (2026-08-05, travail continu)

- moteur **0.4.0** + `vertex/engines/red_team.py` (1.0.0) : les 10 questions
  d'ADVERSARIAL_COMMITTEE §8 évaluées depuis les données réelles du packet —
  réponse fondée (F1/F2, données citées) ou UNANSWERED avec raison, jamais
  inventée ; `complete=True` seulement à 10/10 ; revue servie dans
  `/api/skyler/<sym>` (`red_team_review`) et injectée dans la décision ;
- le chemin S/S+ a désormais sa clé — mais reste fermé par les blocs
  insuffisants tant que les fondamentaux ne sont pas branchés (voulu) ;
- 1398 tests verts / 2 skipped (+12).

## Lot 15 — livré (2026-08-05, travail continu)

- `vertex/engines/session_log.py` : UNE clôture par symbole et par jour de
  scan RÉEL (date d'observation UTC, jamais inventée ; dédup par date ; borné ;
  NaN/dates malformées refusés) — `skyler_sessions.json` runtime gitignoré ;
- la mémoire fige `session_date` et les horizons 5/20/60 comptent des séances
  RÉELLES (log autoritaire, empreinte de série en secours pour les anciens
  records) — limite n° 1 du lot 10 levée ;
- 1410 tests verts / 2 skipped (+12).

## Lot 16 — livré (2026-08-05, travail continu)

- surfaçage UI : carte « Mémoire décisionnelle » sur Performance (ledger par
  version de moteur, biais badgés, propositions en attente humaine, état vide
  honnête) + section « Dépendances cachées » sur Portefeuille → Risque
  (paires ≥ 2 liens, questions de recherche) ;
- SW **v95** + 4 gardiens à jour ; preuve navigateur 390/1440 : 0 erreur
  console, 0 overflow, captures `docs/skyler/baseline/lot16-*.png` ;
- 1416 tests verts / 2 skipped (+6).

## Lot 17 — livré (2026-08-05, travail continu)

- co-mouvement du graphe en **corrélation partielle** (résidus OLS vs SPY,
  `method: residual_vs_SPY` + R² par titre) — le faux co-mouvement « les deux
  suivent le marché » est filtré (prouvé par test) ; sans SPY, fallback
  `method: raw` ÉTIQUETÉ + limite dite, jamais silencieux ; SPY exclu des
  paires ;
- `hidden_groups` : composantes connexes ≥ 3 titres synthétisées dans l'API
  et affichées sur Portefeuille → Risque ;
- SW **v96** + gardiens (lot 16 rendu prospectif ≥ 95) ; navigateur 390/1440 :
  0 erreur console, captures lot17-*.png ;
- 1427 tests verts / 2 skipped (+11).

## Lot 18 — livré (2026-08-05, travail continu)

- moteur **0.5.0** : `robustness` MESURÉE par analyse de perturbation — 11
  variations fixes documentées (score ±10, R:R ±0,5, régime ±0,2, un contexte
  retiré à la fois), fraction stable bornée, bascules listées, non applicable
  exclu (jamais compté stable) ; cœur de verdict partagé anti-divergence ;
  aucun aléatoire (gardien) ; prouvé : un ACHETER frontière bascule sous
  −10 points techniques (fragilité détectée) ;
- 1438 tests verts / 2 skipped (+11) ; SW v96 inchangé.

## Lot 19 — livré (2026-08-05, travail continu)

- moteur **0.6.0** : la boucle décision → mémoire → confiance est FERMÉE —
  `calibration_factor` = scenario hit rate des résultats MESURÉS de la mémoire
  pour la version courante uniquement (0,50 + 0,40 × hit rate, borné
  [0,50, 0,90], jamais 1,0) ; échantillon < 20 mesures → 0,50 « insuffisant »,
  jamais inventé ; route fail-safe ; versions jamais mélangées (testé) ;
- 1450 tests verts / 2 skipped (+12) ; SW v96 inchangé.

## Lot 20 — livré (2026-08-05, travail continu)

- drill-down `GET /api/skyler/memory/<decision_id>` : record figé complet +
  résultat mesuré + **post-mortem déterministe** (classification par horizon,
  scénario ayant contenu le résultat : HORS_FOURCHETTE_BASSE / PESSIMISTE /
  PROBABLE / EXCEPTIONNEL_ATTEINT, MFE/MAE, résumé) — honnête si rien n'est
  mesuré, discipline jamais devinée ; 404 structuré sur id inconnu ;
- carte Mémoire : tableau « Dernières décisions figées » avec lien détail ;
  SW **v97** + gardiens prospectifs ; navigateur 390/1440 : 0 erreur console ;
- 1463 tests verts / 2 skipped (+13).

## Lot 21 — livré (2026-08-05, travail continu)

- red-team **1.1.0** : Q05 chiffrée (repricing Black-Scholes CANONIQUE du
  candidat à IV −10 pts — en démo réelle : « IV 34 % → 24 % : −30,6 % », F3
  avec modèle et hypothèses) ; Q08 en grille stop/TP2/TP3 × IV −10/0/+10 avec
  convexité vs action ; fallbacks F2 et UNANSWERED intacts ; entrées invalides
  jamais chiffrées ; cas manuel BS gardé par test (ATM 1 an vol 20 % ≈ 7,97 %) ;
- 1472 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 22 — livré (2026-08-05, travail continu)

- moteur **0.7.0** : calibration PAR CONTEXTE (§13) — découpe par niveau et
  par décision, chaque cellule avec son propre hit rate seulement si ≥ 20
  mesures (sinon INSUFFISANT dit, valeur None) ; sélection à portée explicite
  contextuel → global → 0,50 ; la route sert la cellule du niveau courant
  (prouvé bout en bout : cellule REFUS_WATCH 0,90 servie au moteur) ;
  `/api/skyler/memory` expose la découpe ; versions jamais mélangées ;
- 1481 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 23 — livré (2026-08-05, travail continu)

- vue lisible `GET /memory/<decision_id>` : record figé, résultat mesuré et
  post-mortem rendus dans le shell produit — contenu de la mémoire ÉCHAPPÉ
  serveur (XSS testé avec script hostile), états honnêtes, 404 lisible ;
  lien de la carte Mémoire mis à jour ; SW **v98** ; parcours prouvé en
  navigateur (clic carte → vue, 0 erreur console) ;
- **`docs/refactor/validation/SKYLER-INDEX.md`** : index consolidé des lots
  10 → 23 (objectifs, versions moteur/SW, tests, verdicts) + architecture ;
- 1488 tests verts / 2 skipped (+7).

## Lot 24 — livré (2026-08-05, travail continu)

- `sector_exposure` dans le graphe : positions réelles agrégées par secteur
  déclaré, poids en % SEULEMENT si toutes les positions sont cotées (sinon
  None avec raison — jamais estimé), hors watchlist étiqueté ; groupes cachés
  mono-secteur flaggés **CONCENTRATION SECTORIELLE** ; affiché sur
  Portefeuille → Risque ; SW **v99** ; navigateur prouvé (0 erreur console) ;
- 1498 tests verts / 2 skipped (+10).

## Lot 25 — livré (2026-08-05, travail continu)

- revue de simplification SANS changement de comportement (suite identique
  1498/2, aucun test modifié) : docstrings resynchronisées sur 0.7.0,
  formule de calibration unique (`_hit_factor`), boucle de mesure réutilisée
  (`_measured_hits`), fallbacks red-team dédupliqués ; dette restante
  documentée et assumée.

## Lot 26 — livré (2026-08-05, travail continu)

- moteur **0.8.0** : calibration par RÉGIME — le record mémoire fige le label
  du régime au moment de la décision (None honnête, anciens records
  compatibles) ; découpe `by_regime` (mêmes règles d'échantillon, régime
  inconnu ≠ cellule) ; sélection prioritaire documentée niveau → régime →
  global avec portée explicite ; route passe le régime courant ; badges de
  calibration par contexte dans la carte Mémoire (masqués sans mesures —
  honnête) ; SW **v100** ;
- 1508 tests verts / 2 skipped (+10).

## Index des lots

Voir `docs/refactor/validation/SKYLER-INDEX.md` — tableau complet 10 → 23.

## Programme Institutional+ — TERMINÉ (RC sur intégration)

Les 12 lots + audit sont livrés sur `integration/vertex-skyler-v2`.
Verdict RC : **GO AVEC RÉSERVES** — voir `SKYLER-LOT-12.md` §11.

## Prochaine action unique

Validation humaine de la RC sur appareil physique (TWS réel, pages, iPhone).
Ensuite, avec accord explicite UNIQUEMENT, merge `integration/vertex-skyler-v2`
→ `main`.

**Arrêt — validation humaine requise.**
