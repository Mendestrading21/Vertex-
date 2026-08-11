# SKYLER V2 — LOT 11 — KNOWLEDGE GRAPH INSTITUTIONNEL

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-11-knowledge-graph`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `40110ac`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Aucune représentation des RELATIONS n'existait : les moteurs Skyler analysent
chaque titre isolément (contexts par symbole), le portefeuille agrège des poids
et corrélations mais rien ne relie explicitement sociétés ↔ secteurs ↔
catalyseurs ↔ portefeuille avec provenance, et aucune dépendance cachée n'était
détectée ni expliquée.

## 2. Problème

- Deux positions du même secteur, co-mouvantes et exposées au même catalyseur
  paraissaient indépendantes dans l'analyse par titre — risque caché invisible.
- Aucune propagation d'impact : « si X bouge, qu'est-ce qui est relié et
  pourquoi » n'était répondable nulle part.
- Danger inverse : un knowledge graph naïf INVENTE des relations (fournisseurs,
  clients, concurrents) qu'aucune source réelle de Vertex ne documente.

## 3. Périmètre

### Inclus

- moteur pur `vertex/engines/knowledge_graph.py` : graphe typé versionné,
  4 relations prouvables, provenance obligatoire par arête, propagation
  explicable, dépendances cachées (≥ 2 liens indépendants), questions de
  recherche automatiques ;
- routes lecture seule `GET /api/skyler/graph` et `GET /api/skyler/graph/<sym>` ;
- 18 tests dédiés.

### Hors périmètre

- UI (aucune page touchée, SW inchangé) ; Lot 12 non commencé ; aucune
  modification de poids/seuils/Constitution ; `main` intacte ; aucun ordre.

## 4. Décision

**Seules les relations PROUVABLES par une source réelle branchée existent :**

| Relation | Source réelle | Niveau |
|---|---|---|
| `MEMBER_OF_SECTOR` | watchlist statique `vertex/market/sectors.py` (citée dans l'arête) | F1 |
| `CO_MOVES_WITH` | corrélation des rendements log sur séries canoniques (≥ 40 points partagés, seuil 0,75, fenêtre affichée) | F2 |
| `EXPOSED_TO_CATALYST` | événements DATÉS du calendrier réel (≤ 90 j) | F1 |
| `HELD_IN_PORTFOLIO` | positions desk réelles | F1 |

Fournisseurs/clients/concurrents : **aucune source branchée → aucune arête,
jamais** — l'énumération `RELATIONS` ne contient même pas ces types (testé).
À la place, des questions de recherche typées `NON_DOCUMENTE` (`value_chain`,
`sector` hors watchlist, `catalyst` manquant) — c'est exactement « questions de
recherche automatiques, sans invention de relation » du skill.

Une dépendance cachée exige **≥ 2 liens indépendants** entre deux titres
(secteur partagé + co-mouvement + même catalyseur) — un seul indice ne suffit
jamais ; priorité aux paires détenues en portefeuille. La propagation
d'impact renvoie des chemins ≤ 2 sauts, chaque saut portant relation, base et
niveau de preuve — explicable arête par arête.

Alternative rejetée : enrichir le graphe par news/mots-clés (relations F4
« thème ») — refusée pour ce lot, trop proche de l'invention de relation ;
possible plus tard avec étiquetage inference explicite.

## 5. Implémentation

### Fichiers modifiés

| Fichier | Rôle | Modification | Risque |
|---|---|---|---|
| `vertex/engines/knowledge_graph.py` | moteur graphe (nouveau) | build/propagate/dépendances/questions | faible |
| `vertex/app/routes/analysis_api.py` | routes analyse | `_kg_build()` + 2 endpoints lecture seule | faible |
| `tests/test_knowledge_graph_lot11.py` | tests (nouveau) | 18 tests rouges→verts | faible |

### Contrats et unités

- versions : `SCHEMA_VERSION` 1, `GRAPH_ENGINE_VERSION` 0.1.0 dans chaque sortie ;
- corrélation : rendements log, Pearson, fenêtre partagée affichée (`window`),
  seuil `CORR_STRONG` 0,75, minimum `MIN_POINTS` 40 — série trop courte =
  limite DITE, jamais devinée ;
- catalyseurs : `dte` en jours calendaires déclarés du calendrier ;
- chaque arête : `relation`, `src`, `dst`, `source`, `evidence_level`
  (F1/F2/F3/F4), `basis` — provenance obligatoire testée sur toutes les arêtes.

### Compatibilité

- API : endpoints additifs uniquement ; `/api/skyler/<sym>` intact (le segment
  statique `graph` gagne sur le convertisseur) ;
- UI : aucune — pas de bump SW ;
- démo/sans IBKR : vérifiés en runtime ;
- rollback : revert du commit (fichiers additifs + un bloc de routes).

## 6. Tests rouges avant correction

```text
python -m pytest tests/test_knowledge_graph_lot11.py -q
ImportError / module vertex.engines.knowledge_graph inexistant
1 error in 0.25s
```

Défaut réel trouvé par les tests en cours de lot : le premier fixture de
corrélation produisait des rendements quasi constants (variance ~1e-18) — le
bruit d'arrondi dominait et la corrélation était dénuée de sens (−0,18 sur deux
séries « identiques »). Corrigé dans le FIXTURE (covariation réelle injectée),
pas dans le moteur — le moteur refusait déjà honnêtement (pas d'arête sous le
seuil), comportement conservé.

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex
résultat : exit 0

python -m pytest tests/ -q
résultat : 1350 passed, 2 skipped in 11.43s

python -m pytest tests/test_no_orders.py -q
résultat : 3 passed (inclus dans la suite complète)

python -m pytest tests/test_knowledge_graph_lot11.py -q
résultat : 18 passed in 2.53s
```

Couverture : provenance obligatoire sur toutes les arêtes, appartenance
sectorielle sourcée, co-mouvement F2 avec fenêtre, minimum de points honnête,
catalyseurs datés seulement, détention desk, AUCUN type de relation inventé
(gardien explicite), déterminisme (même entrée = même graphe), graphe vide
honnête, propagation expliquée saut par saut, nœud inconnu → vide, dépendance
cachée ≥ 2 liens (et contre-test à 1 lien), questions de recherche
(value_chain/sector/catalyst), 2 routes.

## 8. Validation manuelle et navigateur

Aucune UI — validation runtime API en `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1` :

| Vérification | Résultat |
|---|---|
| `/healthz` | 200 — `data_source: demo` |
| `GET /api/skyler/graph` | 200 — 44 nœuds, 25 arêtes (4 secteurs, 20 catalyseurs datés, 1 détention), 0 arête sans provenance, 36 questions de recherche, limites dites |
| `GET /api/skyler/graph/ACN` | 200 — 2 chemins expliqués (catalyseur daté, détention desk), questions `value_chain`+`sector` |
| `/api/client-log` | `{"count":0,"errors":[]}` |

Dépendances cachées : 0 en démo (une seule position desk réelle, pas de paire) —
résultat honnête, le mécanisme est prouvé par tests unitaires.

## 9. Invariants vérifiés

- [x] READONLY — aucun ordre, IBKR intact, `test_no_orders` vert ;
- [x] aucune relation inventée — provenance et niveau de preuve sur 100 % des
      arêtes ; fournisseurs/clients/concurrents absents PAR CONSTRUCTION ;
- [x] données réelles uniquement (watchlist du code citée, séries canoniques,
      calendrier, desk) ;
- [x] limites dites (`limits`), jamais devinées ;
- [x] déterminisme prouvé ; versions de schéma et moteur dans chaque sortie ;
- [x] démo/sans IBKR vérifiés ; aucun secret/runtime dans le diff ;
- [x] suite complète verte (1350/2 skipped).

## 10. Comparaison avant/après

| Mesure | Avant | Après | Interprétation |
|---|---:|---:|---|
| Tests | 1332 passed / 2 skipped | 1350 passed / 2 skipped | +18 tests du lot |
| Relations tracées | 0 | 4 types, provenance obligatoire | graphe prouvable |
| Dépendances cachées | invisibles | ≥ 2 liens indépendants, expliquées | risque caché détectable |
| Questions de recherche | 0 | typées `NON_DOCUMENTE` | manque documenté, jamais comblé en douce |
| Service worker | v94 | v94 | aucune UI touchée |

## 11. Risques et limites restantes

1. **Watchlist sectorielle statique** (45+ leaders) : un titre hors watchlist
   n'a pas de secteur — question de recherche générée, pas d'arête. Source
   sectorielle par titre (IBKR/fondamentaux) = amélioration future.
2. **Co-mouvement = corrélation brute** (pas de contrôle du facteur marché) :
   étiqueté F2 avec méthode ; une corrélation partielle (résidu vs SPY) serait
   plus discriminante — lot ultérieur.
3. **Pas de relations chaîne de valeur** : assumé et documenté — questions de
   recherche à la place ; brancher une source réelle exigerait validation.
4. **Dépendances cachées limitées aux paires** : les groupes ≥ 3 apparaissent
   comme plusieurs paires — suffisant pour alerter, pas encore synthétisé.

## 12. Rollback

`git revert` du commit du lot — moteur et tests additifs, un seul bloc ajouté
dans `analysis_api.py`. Aucune donnée persistée par ce lot.

## 13. Contradictions et opinion minoritaire

- Contradiction assumée : le skill demande de relier « fournisseurs, clients,
  concurrents » mais aucune source réelle n'existe dans Vertex. Résolution :
  questions de recherche typées — prévu explicitement par le skill (« questions
  de recherche automatiques, sans invention de relation »).
- Opinion minoritaire : extraire des relations depuis les titres de news
  (co-mentions) aurait densifié le graphe ; rejetée ici car la frontière avec
  l'invention de relation est trop fine sans cadre d'étiquetage inference —
  conservée comme piste future documentée.

## 14. Verdict

`GO`

Justification : graphe institutionnel prouvable (provenance sur chaque arête,
niveaux F1/F2 corrects), propagation explicable, dépendances cachées à double
preuve, manque documenté au lieu d'être comblé, déterminisme et versions
testés, suite complète verte, READONLY intact, diff minimal.

## 15. Prochaine étape autorisée

Une seule étape : `/vertex-skyler-v2 lot-12` (red-team, sécurité, release
candidate) — non commencé ici.

**Arrêt après ce lot — validation humaine requise.**
