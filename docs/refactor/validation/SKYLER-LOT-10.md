# SKYLER V2 — LOT 10 — MÉMOIRE ET DISCIPLINE DÉCISIONNELLE

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-10-decision-memory`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `d9b5221`  
> SHA après : `2192691`  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Avant ce lot, la trace des décisions Skyler se limitait au journal léger du
lot 9 (`vertex/engines/skyler_journal.py`) : symbole, décision, score, prix,
horodatage. Il manquait tout le ledger institutionnel exigé par
`SCENARIO_CALIBRATION.md` §10 : versions du packet et du moteur, thèse,
catalyseur, déclencheur, invalidation, scénarios figés, objection adverse,
opinion minoritaire, inconnues, portefeuille au moment de la décision — et
toute la machinerie §11–§12 : résultats aux horizons déclarés, classification
des erreurs, biais récurrents.

## 2. Problème

- Aucune décision n'était figée avec sa version de moteur : une évolution du
  moteur aurait rendu l'historique inauditable (recalcul silencieux possible).
- Aucun résultat mesuré par horizon déclaré (5/20/60 séances, catalyseur) —
  seule une comparaison prix enregistré/cote actuelle existait, sans notion de
  séance ni protection look-ahead.
- Aucune taxonomie d'erreur ni détection de biais comportementaux.
- Sévérité : moyenne (aucun calcul faux, mais mémoire institutionnelle
  inexistante — impossible d'apprendre honnêtement des décisions passées).

## 3. Périmètre

### Inclus

- moteur pur `vertex/engines/decision_memory.py` (gel, mémoire append-only,
  anti-look-ahead, mesure par horizon, classification, biais, agrégats par
  version, recommandations en attente de validation humaine) ;
- branchement fail-safe dans `/api/skyler/<sym>` + endpoint lecture seule
  `GET /api/skyler/memory` ;
- persistance runtime `skyler_memory.json` (gitignorée) ;
- 32 tests dédiés.

### Hors périmètre (interdictions du lot respectées)

- Knowledge Graph (Lot 11) : non commencé ;
- interface : aucune page modifiée, aucun bump service worker (aucun shell
  visible touché) ;
- poids, seuils, Constitution : intouchés (le module ne les importe même pas) ;
- `main` : non modifiée ; aucun ordre ; IBKR READONLY intact.

## 4. Décision

Un module pur et injecté (horloge, mémoire, séries passées en paramètres),
append-only, avec ces choix structurants :

- **Identité par version** : `decision_id = sha1(symbole|as_of|décision|version
  moteur|démo)`. Une nouvelle version de moteur produit un AUTRE id — les deux
  records coexistent, séparés ; jamais de recalcul silencieux.
- **Immutabilité** : un `decision_id` existant n'est JAMAIS remplacé, même si
  le contenu diffère (falsification refusée, l'original gagne).
- **Anti-look-ahead par empreinte de série** : le record fige les 8 dernières
  clôtures (`tail_at_decision`) ; la mesure retrouve cette empreinte dans la
  série actuelle et ne voit QUE les clôtures postérieures. Série non alignée
  (fenêtre roulée, données révisées) → `None` : non mesurable, jamais deviné.
- **Honnêteté des champs** : confiance, facteurs, EV, probabilités, état
  opérationnel, horizon de thèse et instrument option = `None` avec raison
  explicite tant que le moteur 0.1.0 ne les produit pas — champs présents dans
  le ledger, valeurs jamais inventées.

Alternative rejetée : mesurer les horizons en jours calendaires depuis
`recorded_at` (simple mais faux — un horizon « 5 séances » n'est pas « 7
jours ») ; retenu uniquement pour l'horizon catalyseur, en conversion
jours→séances (× 5/7) ÉTIQUETÉE `estimated: true`.

## 5. Implémentation

### Fichiers modifiés

| Fichier | Rôle | Modification | Risque |
|---|---|---|---|
| `vertex/engines/decision_memory.py` | moteur mémoire (nouveau) | gel/mesure/classification/biais/agrégats/recommandations | faible |
| `vertex/app/routes/analysis_api.py` | routes analyse | hook fail-safe de gel dans `/api/skyler/<sym>` + `GET /api/skyler/memory` | faible |
| `tests/test_decision_memory_lot10.py` | tests (nouveau) | 32 tests rouges→verts | faible |
| `.gitignore` | hygiène | + `skyler_memory.json` | faible |

### Contrats et unités

- sources : décision canonique `skyler_core.decide()`, packet
  `skyler_core.build_packet()`, série canonique `vertex.data.series.closes()`,
  `PortfolioContext` lot 7 ;
- unités : rendements en %, séances (jamais confondues avec les jours —
  conversion catalyseur étiquetée estimée), horodatage unix injecté ;
- fraîcheur : `as_of` du scan figé dans le record ; mode démo figé ;
- versions : `memory_schema` 1, `packet_schema_version` 1,
  `engine_version` 0.1.0 figés par record ; agrégats séparés par version ;
- taxonomie : `ERREUR_DE_DONNEES / ERREUR_DE_MODELE / ERREUR_DE_SCENARIO /
  ERREUR_DE_TIMING / ERREUR_INSTRUMENT / ERREUR_DE_SIZING /
  ERREUR_DE_DISCIPLINE / VARIANCE_NORMALE` (+ `DECISION_CORRECTE`,
  `NON_CLASSIFIABLE`) — règles ordonnées, base explicite par classement ;
- biais : 10 comportements ; ceux qui exigent des trades réels (poursuite du
  prix, sortie prématurée, options trop courtes, spreads trop larges) restent
  honnêtement `INSUFFISANT` ; renforcement perdant et risque portefeuille
  ignoré sont comptés depuis les gates plafonnantes figées.

### Compatibilité

- API : `/api/skyler/<sym>` inchangé pour ses clients (hook interne) ; nouvel
  endpoint additif `GET /api/skyler/memory` ;
- données : `skyler_memory.json` runtime, gitignoré, borné (2000 décisions) ;
- UI : aucune modification, aucun bump SW requis ;
- mode démo : décisions figées avec `demo: true` (vérifié en runtime) ;
- sans IBKR : vérifié (`NO_IBKR=1`) ;
- rollback : revert du commit ; suppression éventuelle de
  `skyler_memory.json` (fichier runtime, aucune donnée utilisateur).

## 6. Tests rouges avant correction

```text
python -m pytest tests/test_decision_memory_lot10.py -q
ImportError: cannot import name 'decision_memory' from 'vertex.engines'
1 error in 0.20s
```

Les 32 tests décrivent le contrat complet (immutabilité, versioning,
anti-look-ahead, horizons, classification, biais, routes) avant toute ligne de
moteur — le module n'existait pas, la preuve du manque est totale.

En cours de lot, un gardien existant a réagi correctement :
`tests/test_portfolio_executive.py::test_single_decision_source` a refusé la
présence du vocabulaire décisionnel complet dans `decision_memory.py` (un
commentaire listait ATTENDRE/REDUIRE/REFUSER). Corrigé en reformulant le
commentaire — la mémoire ENREGISTRE les décisions, elle n'en produit aucune.

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex
résultat : exit 0

python -m pytest tests/ -q
résultat : 1332 passed, 2 skipped in 7.86s

python -m pytest tests/test_no_orders.py -q
résultat : 3 passed in 1.30s

python -m pytest tests/test_decision_memory_lot10.py -q
résultat : 32 passed in 9.61s
```

Couverture demandée par le lot : immutabilité (3 tests), versioning/séparation
par moteur (3), anti-look-ahead (3), résultats par horizon 5/20/60/catalyseur/
thèse/option (5), gel des champs du ledger (4), classification des erreurs
(8), biais récurrents (3), agrégats/recommandations (2), routes + démo/sans
IBKR + gitignore (3).

## 8. Validation manuelle et navigateur

Aucun changement d'interface — validation runtime API en mode
`DEMO=1 NO_IBKR=1 START_ON_IMPORT=1` :

| Vérification | Résultat |
|---|---|
| `/healthz` | 200 — `data_source: demo`, `ibkr_enabled: false` |
| `GET /api/skyler/ACN` | 200 — décision REFUSER 19/40 figée en mémoire |
| record figé | `decision_id`, versions, thèse, catalyseur (J-2), déclencheur, invalidation, portefeuille (2 positions), `tail` 8 clôtures ; confiance/EV `None` honnêtes |
| `GET /api/skyler/memory` | 200 — agrégats par version `{0.1.0: …}`, 10 biais (statuts ABSENT/INSUFFISANT honnêtes), recommandations vides |
| `/api/client-log` | `{"count":0,"errors":[]}` |

- console : n/a (aucune UI touchée) ;
- overflow/clavier/reduced-motion : n/a ;
- fichiers runtime supprimés après la preuve — absents du diff.

## 9. Invariants vérifiés

- [x] READONLY — IBKR intact, `test_no_orders` vert ;
- [x] aucun ordre ;
- [x] aucune donnée inventée — tout champ non produit par le moteur est `None`
      avec raison explicite ;
- [x] unités explicites (%, séances ; conversion jours→séances étiquetée) ;
- [x] fraîcheur réelle (`as_of` figé, démo figée) ;
- [x] démo/sans IBKR vérifiés en runtime ;
- [x] stale/missing/insufficient — statuts `EN_ATTENTE`/`NON_MESURABLE`/
      `NON_APPLICABLE`/`INSUFFISANT` distincts et testés ;
- [x] sécurité/secrets — aucun secret ni fichier runtime dans le diff ;
- [x] tests complets verts (1332/2 skipped) ;
- [x] décision historique immuable ; résultats séparés par version ; aucun
      look-ahead ; aucune recalibration automatique.

## 10. Comparaison avant/après

| Mesure | Avant | Après | Interprétation |
|---|---:|---:|---|
| Tests | 1300 passed / 2 skipped | 1332 passed / 2 skipped | +32 tests du lot |
| Champs figés par décision | 9 (journal lot 9) | 31 (ledger complet) | ledger §10 réalisé |
| Horizons de mesure | 0 | 6 déclarés (3 mesurables aujourd'hui) | §11 réalisé honnêtement |
| Classes d'erreur | 0 | 8 + 2 statuts honnêtes | taxonomie du lot |
| Biais surveillés | 0 | 10 | 6 calculables, 4 honnêtement INSUFFISANT |
| Service worker | v94 | v94 | aucune UI touchée — pas de bump |

## 11. Risques et limites restantes

1. **Mesure dépendante de l'alignement de série** : si la fenêtre canonique
   roule au-delà de l'empreinte de 8 clôtures avant la prochaine visite, les
   horizons restent `EN_ATTENTE`/non mesurables — honnête mais lent à se
   remplir. Une source de série datée par séance (lot ultérieur) lèverait la
   limite proprement.
2. **Horizon de thèse et échéance option `NON_APPLICABLE`** : le moteur 0.1.0
   ne déclare ni horizon de thèse ni instrument choisi ; les champs existent
   dans le ledger et s'activeront quand une version ultérieure du moteur les
   produira (sous une nouvelle `engine_version`, séparée).
3. **Biais d'exécution `INSUFFISANT`** : sans lien décision↔trade réel, la
   poursuite du prix, la sortie prématurée et les biais options restent
   inobservables — dits tels quels, jamais devinés.
4. **Conversion jours→séances du catalyseur** : estimation (× 5/7) étiquetée
   `estimated: true` — imparfaite les semaines fériées.

## 12. Rollback

`git revert` du commit du lot (module + routes + tests + gitignore sont
additifs) ; supprimer `skyler_memory.json` si présent (fichier runtime,
aucune donnée utilisateur, jamais commité).

## 13. Contradictions et opinion minoritaire

- Contradiction assumée : le lot exige « instrument choisi » et « probabilités »
  dans le ledger alors que le moteur 0.1.0 ne les produit pas. Résolution :
  champs présents, valeurs honnêtement absentes avec raison — l'alternative
  (inventer) violerait l'invariant n° 1 du produit.
- Opinion minoritaire : mesurer les horizons en jours calendaires aurait rempli
  la mémoire plus vite ; rejetée car « 5 séances » ≠ « 5 jours » — la lenteur
  honnête bat la vitesse fausse.

## 14. Verdict

`GO`

Justification : ledger complet figé par version de moteur, immutabilité et
anti-look-ahead prouvés par tests rouges→verts, résultats uniquement aux
horizons déclarés, classification déterministe avec base explicite, biais
honnêtes, recommandations en attente de validation humaine, suite complète
verte (1332/2), READONLY intact, diff limité au lot, aucun fichier runtime.

## 15. Prochaine étape autorisée

Une seule étape : validation humaine de ce lot, puis `/vertex-skyler-v2 lot-11`
(Knowledge Graph) — non commencé ici.

**Arrêt après ce lot — validation humaine requise.**
