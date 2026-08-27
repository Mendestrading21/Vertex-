# CLAUDE.md — Vertex 1.0

## Instructions canoniques

Autorité produit, données, moteurs, sécurité et release :

```text
/vertex-1-0
```

Autorité unique pour toute interface, page, navigation, widget, tableau,
graphique, typographie, responsive ou refonte visuelle :

```text
/vertex-design-2-0
```

Les skills `vertex-skyler-v2`, `vertex-total-rebuild`, V4, Signal OS,
Neon Glass, Copper et les anciens `vertex-redesign-*` sont historiques.
Ne jamais relancer leurs workflows par lots.

## Autorité spécialisée Vertex Design 2.0

Pour toute demande d'interface, navigation, page, composant, widget, tableau, graphique, responsive, typographie ou refonte visuelle, invoquer exclusivement :

```text
/vertex-design-2-0
```

Skill : `.claude/skills/vertex-design-2-0/SKILL.md`. Il hérite de tous les invariants de `vertex-1-0` et devient l'unique autorité de design. En cas de conflit, sécurité, lecture seule et vérité financière restent prioritaires. Les anciens workflows Signal OS, Neon Glass, Copper, Signal Green et `vertex-redesign-*` sont historiques.

## Refonte « Vertex Black Glass — Signal Light »
- Direction visuelle canonique = **Vertex Black Glass — Signal Light** : fond obsidienne/graphite, verre noir translucide, structure blanc/argent, séparation par surfaces plutôt que bordures visibles, Geist + Geist Mono, **sémantique stricte** (vert = positif, rouge = négatif/risque, ambre = prudence/incertitude), **zéro bleu identitaire**, violet réservé aux options.
- Contrats de référence : `docs/VERTEX_GLASS_REDESIGN_MASTER_PLAN.md` + `docs/claude/` (`VERTEX_GLASS_VISUAL_CONTRACT.md`, `VERTEX_CHART_CONTRACT.md`, `VERTEX_REFACTOR_RULES.md`, `VERTEX_PAGE_MATRIX.md`, `VERTEX_ACCEPTANCE_CHECKLIST.md`).
- Skills d'orchestration : `.claude/skills/vertex-redesign-*` (orchestrator, foundations, une par espace, qa). Couche CSS = `vertex/static/vertex/css/glass.css` (chargée en dernier).

## Règles critiques (violations = données perdues ou app cassée)
1. **Clés de sync desk** : toute nouvelle clé localStorage à synchroniser doit être ajoutée dans **LES 4 listes** (`__DESK_KEYS` terminal.py, sSyncPush/Pull, `vertex/ui/journal.py`, `DESK_KEYS` de `vx_kit.py`) — sinon un push l'efface côté serveur. Test gardien : `tests/test_production.py::test_desk_sync_keys_single_source_of_truth`.
2. **Apostrophes françaises dans les chaînes JS** de terminal.py : toujours échapper (`aujourd\\'hui`) — deux SyntaxError silencieuses ont déjà vécu.
3. **Service worker** : tout changement de shell visible utilisateur → bump `td-shell-vN` dans `vertex/app/routes/system.py`.
4. **Données RÉELLES uniquement** : jamais de chiffre inventé affiché comme réel. Donnée absente → `—`/`n/d` honnête. Le mot « démo » ne s'affiche que si le serveur le confirme.
5. **News/textes externes** : toujours via `news_plus.sanitize_news()` avant de servir (XSS — rendus en innerHTML).
6. **desk_data.json** : ne jamais l'écraser à la main ; en cas de doute, backups `desk_backup_*.json` + `/api/desk/restore`.

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
4. `vertex/strategy/release_profiles/vertex_strategy_v4.json`;
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
- `vertex.runtime` active `release_profiles` avant le chargement applicatif;
- `terminal.py`: adaptateur historique et mode de rollback V3, à réduire; ne
  pas y ajouter de nouvelle capacité sauf correctif indispensable avant
  extraction.

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
