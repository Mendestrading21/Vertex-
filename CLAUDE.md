# CLAUDE.md — Vertex 1.0

## Instruction active unique

Utiliser exclusivement:

```text
/vertex-1-0
```

Skill actif: `.claude/skills/vertex-1-0/SKILL.md`.
Les skills `vertex-skyler-v2`, `vertex-total-rebuild`, V4 et Signal OS sont
historiques. Ne jamais relancer leurs workflows par lots.

## Invariants absolus

1. Vertex est **analyse uniquement**.
2. `vertex.app.config.READONLY` et `ANALYSIS_ONLY` restent toujours `True`.
3. IBKR reste `readonly=True`.
4. Aucun endpoint, bouton, fonction, ticket ou agent ne transmet un ordre.
5. Aucune donnée financière n'est inventée ou remplacée silencieusement par
   zéro.
6. Un score élevé ne contourne jamais un hard gate.
7. Claude n'est jamais le calculateur canonique.
8. La constitution stratégique ne change qu'au moyen d'une nouvelle version
   explicite et revue humainement.

## Sources de vérité

Ordre d'autorité:

1. ce fichier;
2. `.claude/skills/vertex-1-0/SKILL.md`;
3. `docs/vertex-1.0/`;
4. `vertex/strategy/profiles/vertex_strategy_v4.json`;
5. code et tests du composant;
6. documents historiques, uniquement comme preuves.

En cas de contradiction, ouvrir ou mettre à jour
`docs/vertex-1.0/DECISIONS.md`; ne pas créer une nouvelle doctrine.

## Produit

- Options: détention typique 2/4/6 semaines; DTE préféré 120–240; cible 180.
- Actions: horizons 3/6/12 mois.
- WMB Brief: contexte macro quotidien, daté et sourcé.
- TradingView: signal authentifié de réévaluation, jamais un déclencheur
  d'achat.
- Huit espaces: Aujourd'hui, Marchés, Opportunités, Analyse, Portefeuille,
  Options, Journal, Système.

## Architecture canonique

```text
sources
  → normalisation + provenance + fraîcheur
  → moteurs déterministes
  → packet immuable
  → hard gates
  → scénarios + score + portefeuille
  → décision canonique
  → explication Claude
  → UI + journal + audit
```

Entrées:

- local: `python -m vertex`;
- WSGI: `vertex.runtime:app`;
- `terminal.py`: adaptateur historique, à réduire; ne pas y ajouter de
  nouvelle capacité sauf correctif indispensable avant extraction.

## Données et états

Toute surface doit distinguer au minimum:
`LIVE`, `DELAYED`, `STALE`, `DEMO`, `OFFLINE`, `MISSING`.

Les objets décisionnels doivent conserver:

- source et timestamp;
- fraîcheur et qualité;
- faits, métriques, estimations et interprétations séparés;
- contradictions et opinion minoritaire;
- thèse, catalyseurs, invalidation et scénarios;
- version des moteurs, du profil et du packet.

## Rôle de Claude

Autorisé: résumer, synthétiser, comparer, expliquer, rédiger le brief et
signaler les contradictions.

Interdit: inventer prix/prime/Greek/probabilité/source; modifier score,
scénario, risque ou verdict; contourner un hard gate; rendre une donnée
absente conforme; transmettre ou préparer un ordre.

## Workflow Git

- partir du dernier `main`;
- branche `agent/vertex-1-0-<sujet>`;
- un objectif cohérent par PR, pas une branche par micro-tâche;
- PR brouillon vers `main`;
- aucune fusion automatique;
- les centaines de branches `agent/skyler-v2-lot-*` sont historiques et ne
  servent jamais de base.

## Validation minimale

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

Pour un changement runtime/UI, vérifier aussi:

- `/healthz`;
- `/api/client-log` = 0 erreur applicative;
- les huit espaces en desktop et mobile;
- mode démo, sans IBKR et panne partielle;
- absence de fuite de secret ou de donnée de compte.

## Conditions de livraison

La PR doit documenter: objectif, fichiers propriétaires, preuve de tests,
données/fraîcheur, risques, rollback, limites non vérifiées et décision humaine
restante. Ne jamais déclarer « prêt à 100 % » sans CI verte et acceptation
humaine du commit candidat.
