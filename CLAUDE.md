# VERTEX — Guide de travail Claude Code

Vertex est un terminal d'analyse Flask local, en français, sur le port `5002`.
Il est **strictement en lecture seule** : aucun ordre ne peut être envoyé.

## Point de départ obligatoire

Branche d'intégration V4 :

```text
integration/vertex-v4-clean
```

Lire dans cet ordre avant toute modification :

1. `CLAUDE.md`
2. `docs/README.md`
3. `docs/canonical/READONLY.md`
4. `docs/canonical/DATA_CONTRACT.md`
5. `docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`
6. `docs/vertex-v4/DECISIONS.md`
7. `docs/vertex-v4/STATUS.md`
8. `.claude/skills/vertex-v4-redesign/SKILL.md`

L'unique commande de refonte active est `/vertex-v4-redesign`. Les anciens
programmes Black Glass, Signal Green et Obsidian Copper sont supprimés de la
documentation active.

## Invariants absolus

- Conserver `READONLY=True` dans `vertex/app/config.py`.
- Toute connexion IBKR reste `readonly=True`.
- Ne créer aucun chemin d'ordre, même en paper trading.
- Ne modifier aucun calcul, score, verdict, moteur ou contrat API dans un lot visuel.
- Ne jamais fabriquer une donnée. Absence = `—`, `n/d` ou état vide honnête.
- Préserver provenance, fraîcheur et statut LIVE/DELAYED/STALE/DEMO.
- Aucun secret, identifiant de compte ou nom personnel dans le dépôt ou les captures.
- Ne jamais travailler directement sur `main`.

## Vérifier avant et après chaque lot

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
```

Puis démarrer en mode contrôlé :

```bash
DEMO=1 NO_IBKR=1 python terminal.py
```

Contrôles requis :

- `GET /healthz` doit être sain ;
- `GET /api/client-log` doit rester sans erreur réelle ;
- toutes les routes principales doivent répondre ;
- vérification en navigateur desktop, tablette et mobile ;
- aucune erreur console ni overflow horizontal.

## Architecture actuelle

- `terminal.py` : monolithe historique et orchestration restante ; ne pas le déplacer en bloc.
- `vertex/app/routes/` : blueprints Flask.
- `vertex/ui/shell/` et `vertex/ui/pages/` : shell et pages actuelles.
- `vertex/engines/`, `vertex/options/`, `vertex/strategy/` : logique métier protégée.
- `vertex/app/state.py` : `scan_state` doit être muté en place, jamais réassigné.
- `vertex/static/vertex/` : CSS, JavaScript, graphiques et polices auto-hébergées.
- `tests/` : contrats exécutables ; un test ne se désactive pas pour faire passer un lot.

## Direction V4 canonique

- Nom : **Vertex V4 — Obsidian Prism**.
- Référence maître : `docs/vertex-v4/reference/00-master-obsidian-prism.jpg`.
- Marque : violet, magenta et corail ; jamais pour signifier un gain ou une perte.
- Sémantique : vert positif, rouge négatif/risque, ambre attente/incertitude.
- Typographies : General Sans pour l'interface, JetBrains Mono pour les nombres.
- Cible : neuf espaces, dont Marchés explicite.
- Les CSS historiques encore chargés sont des dépendances de migration, pas des
  sources de vérité. Suivre `docs/vertex-v4/MIGRATION_MAP.md`.

## Pièges connus

1. Les apostrophes françaises dans les chaînes JavaScript Python doivent être échappées.
2. Toute modification du shell visible impose un bump `td-shell-vN` et ses tests.
3. Toute nouvelle clé localStorage synchronisée doit être ajoutée aux registres canoniques.
4. Les textes externes passent par `news_plus.sanitize_news()` avant `innerHTML`.
5. `desk_data.json` ne se modifie jamais à la main ; utiliser les backups et l'API de restauration.
6. Ne pas supprimer une couche CSS legacy avant preuve qu'aucun rendu ne la consomme encore.

## Workflow Git

- Un lot à la fois, avec périmètre annoncé.
- Branche temporaire autorisée : `claude/v4-XX-description`.
- Tests et captures avant commit.
- Commit atomique `feat(v4-XX): ...` ou `fix(v4-qa): ...`.
- Mise à jour obligatoire de `docs/vertex-v4/STATUS.md`.
- PR brouillon vers la branche d'intégration pendant les lots.
- Fusion vers `main` uniquement après QA finale et autorisation explicite.

## Préférences produit

Interface française, données réelles, raisonnement transparent, densité maîtrisée
et zéro erreur silencieuse. Une bonne visualisation aide une décision précise ;
sinon elle doit être simplifiée ou supprimée.
