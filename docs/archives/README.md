# Archives

Rapports historiques rangés par thème. Aucun n'était référencé par le code, les
tests, la CI ou un autre document au moment du rangement : ils ont été
**déplacés, jamais réécrits ni supprimés**, conformément à l'invariant « aucun
nettoyage par nom ou ancienneté ».

| Thème | Fichiers | Contenu |
|---|---|---|
| [`options-volatilite/`](options-volatilite/) | 45 | disponibilité et intégrité des entrées options, DTE, IV, liquidité, scénarios, volatilité |
| [`intelligence-decision/`](intelligence-decision/) | 44 | packets SKYLER, gates, contrats de décision, calibration, régimes, moteurs de stratégie |
| [`vertex-audit/`](vertex-audit/) | 21 | audit produit en 18 volets (cartographie, provenance, sécurité, accessibilité, roadmap) |
| [`portefeuille-positions/`](portefeuille-positions/) | 20 | couverture du risque portefeuille, cycle de vie et modèles de positions, réconciliation |
| [`interface-visuel/`](interface-visuel/) | 19 | audits UI V3, jetons de design, plans Glass / Obsidian, registres de widgets |
| [`audits-baselines/`](audits-baselines/) | 15 | audits complets, baselines, rapports de tests, migration de namespace |
| [`donnees-sources/`](donnees-sources/) | 15 | qualité et fraîcheur des sources, événements, macro, taux, intégrations externes |
| [`securite-performance/`](securite-performance/) | 9 | durcissement des payloads, erreurs d'API sûres, limitation de débit, intégrité webhook |
| [`plateforme/`](plateforme/) | 9 | architecture, matrice de routes, séquence de démarrage, automatisations, limites connues |
| [`claude/`](claude/) | 5 | contrats de refonte et checklist d'acceptation d'une itération antérieure |
| [`release/`](release/) | 5 | changelog, checklist, acceptation humaine, problèmes connus et rollback RC1 |
| [`research/`](research/) | 1 | veille de méthodes quantitatives externes |

## Règle d'usage

Une archive documente un commit passé. Elle ne dit rien de fiable sur le commit
courant : ni les chiffres, ni les statuts, ni les listes de pages, ni les
« NON_IMPLÉMENTÉ ». Pour décider aujourd'hui, remesurer sur le SHA candidat et
lire le skill maître.

Ces fichiers restent en place tant qu'ils ne sont pas remplacés par une preuve
plus récente sur le même sujet. Les supprimer demanderait la preuve qu'aucun
rollback, aucune enquête et aucun consommateur n'en dépend — cette preuve n'a
pas été faite.
