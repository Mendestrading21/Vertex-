# Baseline du dépôt et dettes prioritaires

Cette référence est une photographie de départ, pas une vérité éternelle.
Claude la remesure sur le dernier `main` avant chaque programme et met les
écarts dans le rapport du lot.

## Photographie mesurée

Audit du `main` `26b9589b7c49f89f90f8f8d9ccc21d5348870c00` :

- environ 2 083 fichiers visibles par l'inventaire de travail et plus de 1 000
  documents Markdown ;
- 467 fichiers de tests Python et 382 modules Python sous `vertex/` ;
- 204 règles Flask, 199 endpoints et 29 blueprints mesurés par inspection du
  runtime ;
- `terminal.py` reste un adaptateur historique d'environ 7 400 lignes ;
- 18 dossiers de skills et 17 prompts d'agents sur `main`, avec plusieurs
  doctrines concurrentes ;
- 4 401 tests collectés sur la baseline d'audit ; la suite complète n'a pas
  été déclarée verte, seuls 62 tests ciblés l'ont été ;
- plus de 700 références de branches distantes, majoritairement historiques ;
- profils stratégiques V1–V3 dupliqués byte pour byte entre `profiles/` et
  `release_profiles/` ; ne pas les retirer sans décider le contrat de rollback.

Ces nombres servent à détecter une dérive. Ils ne justifient aucune suppression
à eux seuls.

L'audit exécutable du 28 août 2026 sur `14f8988` confirme 204 règles, 199
endpoints et 29 blueprints. Il mesure aussi la matrice HTTP page par page,
les deux collisions, l'absence du routeur pourtant documenté et le décalage
typographique. Voir `runtime-page-manifest.md` et reproduire avec
`scripts/audit_runtime.py` ; cette mesure prime sur les commentaires historiques.

## Capacités réelles déjà présentes

- moteurs déterministes, constitution versionnée, hard gates et moteur
  exécutif ;
- agent Claude avec schéma de réponse, contrôle des chiffres et fallback
  déterministe ;
- marchés, opportunités, analyse, options, portefeuille déclaratif, journal,
  tracking, performance, système et mémoire ;
- chaînes, Greeks, volatilité, GEX, scénarios, stress et simulateurs options ;
- provenance, qualité, fraîcheur, états dégradés, healthz/readyz et SSE ;
- desk déclaratif synchronisé, sauvegardes et restauration ;
- garde-fous no-orders et plusieurs milliers de tests historiques.

Consolider ces capacités avant d'en créer une parallèle.

## P0 connus à reproduire

1. **Vie privée IBKR** : des chemins lisent encore positions, compte et P&L du
   courtier. Exemples : `terminal.py`, `vertex/data_sources/ibkr_positions.py`,
   `vertex/data_sources/ibkr_compte.py`, `vertex/app/routes/desk.py`,
   `vertex/app/routes/positions_api.py` et `vertex/portfolio/models.py`.
2. **Exposition privée** : non-loopback peut fonctionner sans authentification,
   plusieurs réponses personnelles ne sont pas `no-store` et des holdings/P&L
   réels subsistent dans l'arbre. L'historique Git contient un identifiant de
   compte ; sa réécriture exige une autorisation destructive séparée.
3. **Décision concurrente** : Analyse affiche Executive, DecisionStack et
   Skyler ; terminal ajoute comité, scorecard, decide et quant. Des sondes
   identiques donnent `ATTENDRE`, `ACHETER`, `ACCEPTÉ` ou `STRONG_BUY` selon le
   chemin. Le moteur Executive manque actuellement le `guard` requis.
4. **Collisions de routes** : `/options/<sym>` sert le JSON avant la page HTML
   et rend le dossier options par titre inaccessible ;
   `/api/anomalies/<sym>` possède aussi deux propriétaires. Des tests figent la
   dette au lieu de l'interdire.
5. **Automatisations inexactes** : 27 jobs sont déclarés, 9 marqués implémentés
   et 18 sans émetteur. Plusieurs heartbeats restent verts après erreur ou ont
   une cadence différente du registre ; l'initialisation complète n'est pas
   appelée sous Gunicorn.
6. **Requêtes lentes** : options, company, analyst, correlations, copilote et
   quotes font encore du réseau synchrone ; certains timeouts atteignent 20 à
   45 s. `/scan` invalide presque chaque seconde son ETag par des champs d'âge.
7. **Cache non borné** : le plafond d'âge du magasin de snapshots n'est pas
   appliqué, un thread peut naître par miss et plusieurs caches n'ont pas de
   limite mémoire/entrées.
8. **Navigation incohérente** : runtime à sept entrées, cible à douze pages,
   registres desktop/mobile/JS/legacy concurrents. Journal est introuvable sur
   mobile et le routeur SPA annoncé n'est pas chargé.
9. **Design à deux vérités** : 18 CSS globaux, tokens surchargés, quatre familles
   KPI, pages monolithiques et 148 tests neutralisés. Le texte faible mesuré à
   environ 3,05:1 échoue AA pour du petit texte.
10. **Doctrines concurrentes** : anciens skills, agents et docs historiques
    donnaient des ordres opposés. Le cutover doit laisser un seul skill et six
    auditeurs subordonnés sans autorité produit.

## Dette mesurée à traiter sans big bang

- 331 captures larges d'exception et au moins 93 corps réduits à
  `pass/continue` dans la baseline runtime ;
- quatre registres de navigation et deux collisions de routes mesurées ;
- familles CSS, cartes, tuiles et thèmes successifs ;
- appels fournisseur dans le chemin de réponse UI ;
- tests navigateur présents mais pas systématiquement exécutés en CI ;
- CI pytest/no-orders sans Chromium réellement installé, budget Lighthouse,
  lock reproductible, couverture, Ruff, audit dépendances/SBOM ou preuve
  visuelle obligatoire ;
- documents de lot nombreux qui ne doivent plus piloter le présent.

## Règle d'usage

Pour chaque constat, produire : preuve actuelle, impact utilisateur, impact
financier, propriétaire, reproduction, décision conserver/regrouper/migrer/
retirer, tests, rollback et statut. Ne jamais recopier un ancien chiffre de
baseline comme preuve actuelle.
