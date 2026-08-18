# Vertex 1.0 — Prompt maître Claude Code

Utiliser ce prompt après `/vertex-1-0` pour les grands chantiers de convergence.

```text
/vertex-1-0

Tu travailles exclusivement sur Vertex 1.0 depuis le dernier main.

OBJECTIF
Faire converger le dépôt vers une application institutionnelle unique, fiable, rapide, sobre et mesurable. Ne crée aucune nouvelle architecture parallèle et ne relance aucun ancien workflow Skyler/Total Rebuild/V4/Signal OS.

ORDRE DE TRAVAIL
1. Lire CLAUDE.md, docs/vertex-1.0/, le profil V4 et l'issue GitHub ciblée.
2. Relever le SHA de départ et exécuter la baseline complète.
3. Cartographier les propriétaires, consommateurs, routes, tests, caches et données avant toute suppression/renommage.
4. Chercher les doublons avant d'ajouter un fichier ou une abstraction.
5. Implémenter la plus petite convergence architecturale qui supprime une responsabilité concurrente.
6. Préserver un adaptateur et un rollback tant que les consommateurs ne sont pas prouvés migrés.
7. Tester les modes live-compatible, NO_IBKR, DEMO, OFFLINE/MISSING et panne partielle selon le périmètre.
8. Exécuter compileall, pytest complet et tests anti-ordre.
9. Pour runtime/UI, vérifier /healthz, /api/client-log et les huit espaces desktop/mobile.
10. Ouvrir une PR brouillon avec preuves, risques, rollback et limites. Ne jamais fusionner automatiquement.

RÈGLES NON NÉGOCIABLES
- aucune exécution d'ordre ;
- aucune donnée inventée ou zéro silencieux ;
- aucun hard gate contourné ;
- aucune logique financière canonique confiée à Claude ;
- aucun nouveau code métier dans terminal.py ;
- aucune suppression massive de branches/fichiers sans classification ;
- aucune nouvelle couche CSS/thème si une couche existante doit être remplacée ;
- aucune déclaration « terminé » avec une validation appartenant à un autre SHA.

STANDARD
Appliquer docs/vertex-1.0/QUALITY_STANDARD.md à chaque changement.
```
