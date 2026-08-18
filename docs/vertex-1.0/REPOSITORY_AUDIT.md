# Audit de consolidation du dépôt

Date de référence: 18 août 2026.
Base initiale: `main` au commit `edfca5155073416e9aaacb55eb4b862421f5f202`.

## Forces

- moteurs déterministes nombreux et testés;
- constitution stratégique versionnée;
- séparation explicite décision / narration IA;
- IBKR lecture seule et tests anti-ordre;
- options: chaîne, liquidité, Greeks, GEX, flow, scénarios et filtres;
- TradingView authentifié et limité à la réévaluation;
- modes démo, différé, sans IBKR et observabilité;
- huit espaces produit déjà définis.

## Risques critiques

### Gouvernance Git

- au moins 300 branches de lots Skyler;
- plusieurs branches d'intégration concurrentes;
- quatre PR historiques ouvertes avec doctrines différentes;
- `main` non protégée au moment de l'audit;
- anciennes métriques de tests non comparables car issues de commits
  différents.

### Runtime

- `terminal.py` dépasse 800 Ko et concentre composition, workers, routes,
  caches et HTML/JS historique;
- plusieurs lanceurs et entrées de déploiement pointaient directement vers le
  monolithe;
- routes modulaires et routes historiques coexistent.

### Domaines

- doublons de responsabilité: `company/companies`, `data/data_sources`,
  `portfolio/positions/tracking`, plusieurs surfaces options;
- registres de navigation et sources de tokens/couleurs multiples;
- plusieurs implémentations de graphiques similaires;
- constantes de synchronisation et contrats API parfois dupliqués.

### Documentation et agents

- deux skills actifs concurrents avant cette consolidation;
- onze agents spécialisés sans orchestrateur produit unique;
- `docs/skyler/STATUS.md` supérieur à 1 Mo;
- nombreux documents « master », « ultimate », audits et micro-lots;
- chiffres de baseline historiques incompatibles entre eux.

### Design

- empilement de feuilles CSS, dont une couche `neon-glass.css` volumineuse;
- anciennes directions Obsidian Copper, Neon Glass, V4/Prism et Signal OS;
- PR Signal OS riche mais fondée sur une branche très divergente de `main`;
- extraction sélective nécessaire, jamais une fusion globale aveugle.

## Décision

`main` récent reste la base de consolidation. Vertex 1.0 installe une couche
canonique non destructive: version, runtime, profil, skill, docs et CI. Les
capacités uniques des branches historiques seront récupérées uniquement après
comparaison par composant et tests sur la base courante.

## Ce que cet audit ne prétend pas

Il ne remplace pas une exécution locale de la suite complète, un audit
navigateur, un audit de performance, un test IBKR réel ou une acceptation
humaine. Ces preuves appartiennent au commit candidat de release.
