# Exécution Claude Code — Vertex Intelligence 2.0

## Prompt de démarrage

Copier ce bloc dans Claude Code après avoir placé le dépôt sur la branche de
travail autorisée :

```text
/vertex-1-0

Tu travailles sur le dépôt GitHub Vertex actuellement ouvert.

Lis entièrement et dans cet ordre :
1. CLAUDE.md
2. .claude/skills/vertex-1-0/SKILL.md
3. docs/vertex-1.0/README.md
4. docs/vertex-1.0/audits/AUDIT-TOTAL-2026-08-25.md
5. docs/vertex-1.0/audits/AUDIT-TOTAL-2026-08-24.md
6. docs/vertex-1.0/roadmap/SOURCES-APIS-OPEN-SOURCE.md
7. docs/vertex-1.0/roadmap/USER-REPOSITORIES-2026-08-25.md
8. docs/vertex-1.0/roadmap/VERTEX-INTELLIGENCE-2.0.md
9. docs/vertex-1.0/QUALITY_STANDARD.md
10. docs/vertex-1.0/RELEASE_GATES.md

Commence par le premier lot non terminé dont toutes les dépendances sont
satisfaites. Ne lance jamais plusieurs lots en parallèle et ne crée pas une
branche par micro-tâche.

Avant de choisir le lot, inspecte les PR #793 à #808 et leurs dépendances. Si le
problème est déjà traité dans une PR ouverte, complète cette PR ou son prochain
lot canonique ; ne crée jamais un propriétaire concurrent.

Avant de coder :
- relève le SHA exact et l'état CI ;
- exécute compileall, la suite complète et no-orders ;
- cartographie producteurs, consommateurs, routes, caches, scheduler,
  persistance et tests du périmètre ;
- cherche les doublons et le code déjà présent ;
- écris les critères d'acceptation et les témoins négatifs ;
- refuse de déclarer PASS ce que l'environnement ne peut pas mesurer.

Pendant le lot :
- aucune capacité d'ordre ;
- aucun nouveau code métier dans terminal.py ;
- chaque donnée a source, observation time, available time, received time,
  unité, devise, mode, fraîcheur, qualité et erreur ;
- aucun fallback silencieux et aucun zéro inventé ;
- aucune probabilité non calibrée présentée comme probabilité de gain ;
- aucune donnée actuelle utilisée comme donnée historique point-in-time ;
- l'IA explique, elle ne calcule ni score ni verdict ;
- tout provider externe passe par un modèle Vertex canonique ;
- toute nouvelle dépendance exige licence, pin, audit et rollback.
- aucune requête de page ne lance directement une collecte lourde IBKR/Yahoo ;
  servir un snapshot daté puis rafraîchir de façon asynchrone et coalescée ;
- actions = 3/6/12 mois ; options = risque borné, DTE 120–240 cible 180,
  revues 2/4/6 semaines ; ETF = look-through, liquidité, tracking et frais ;
- un dépôt externe sert d'inspiration tant que sa licence, ses tests, son
  domaine et son absence de surface d'ordre ne sont pas prouvés.

À la fin :
- compileall ;
- pytest complet ;
- tests/test_no_orders.py ;
- tests spécifiques du lot, mutation/témoins ;
- smoke runtime et huit espaces si runtime/UI ;
- mesure p50/p95 des routes modifiées et budget explicite ;
- modes dégradés et panne partielle ;
- rapport avec preuves du même SHA, risques, limites, rollback et décision
  humaine restante ;
- PR brouillon, jamais de fusion ni tag automatique.

Pour le lot 1 G5, conserve la preuve live du SHA `d77b06d` et ne refais que
les cases manquantes du protocole. Si TWS/IB Gateway réel n'est pas disponible,
produis la commande exacte et marque ces cases `HUMAN_REQUIRED`. Ne simule
jamais une preuve.

Pour le lot 9 V5, ne modifie jamais V4 en place. Crée un profil candidat et
demande l'arbitrage humain avant activation.
```

## Commandes de base

```bash
git status --short --branch
git log -1 --oneline
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
python tools/vertex_1_0/mesurer_g5_live.py --help
```

## Format obligatoire d'un lot

1. Hypothèse et problème mesuré.
2. Propriétaire canonique avant/après.
3. Source, licence, entitlement et fraîcheur.
4. Schéma et migration.
5. Comportement nominal, différé, rassis, hors ligne et manquant.
6. Tests rouges avant correction.
7. Tests de contrat, replay et témoins négatifs.
8. Mesure avant/après.
9. Risques et rollback.
10. Limites et décisions humaines.

## Définition de succès

Le succès n'est pas « plus de fonctions ». C'est :

- plus de décisions reproductibles ;
- moins de données ambiguës ;
- une meilleure calibration hors échantillon ;
- une perte maximale réellement bornée ;
- des recommandations que l'on peut auditer des mois plus tard ;
- aucun affaiblissement de la lecture seule.
