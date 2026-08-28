# Runtime réel et manifeste de migration des pages

## Mesure du 28 août 2026

Mesure reproductible sur le commit `14f8988`, avec `DEMO=1`, `NO_IBKR=1`,
`START_ON_IMPORT=0`, sans worker et sans connexion fournisseur :

- 204 règles Flask, 199 endpoints et 29 blueprints ;
- 7 entrées dans `PRIMARY_NAV` : Dashboard, Opportunités, Analyse,
  Portefeuille, Options, Journal et Système ;
- Intelligence et Tracking sont des pages secondaires actives ;
- la page Aujourd'hui charge 18 feuilles CSS et 17 ressources JavaScript
  (shell, graphiques et code de page) ;
- le shell décrit une navigation persistante mais ne charge pas
  `vx-router.js` ; les tests qui l'attendent sont neutralisés ;
- General Sans et JetBrains Mono sont servis alors que la cible approuvée est
  Geist et Geist Mono ;
- deux routes ont plusieurs propriétaires.

Reproduire avec :

```bash
DEMO=1 NO_IBKR=1 START_ON_IMPORT=0 \
  python .claude/skills/vertex-2-0/scripts/audit_runtime.py
```

Le script nécessite les dépendances du dépôt. Son mode `--enforce-target` est
un garde de fin de migration, pas un prérequis de la baseline actuelle.

## Matrice vérité → cible

| Cible 2.0 | Runtime mesuré | Décision de migration | Ne pas perdre |
|---|---|---|---|
| Aujourd'hui `/` | 200, titre Dashboard ; contient aussi Marchés | Renommer et réduire au command center ; conserver des liens vers les propriétaires | brief, régime, alertes, événements, revues et snapshots |
| Calendrier `/calendar` | 301 vers `/opportunities?view=calendar` | Extraire une page depuis les producteurs déjà présents, puis garder l'ancienne URL en alias | macro, catalyseurs, earnings, expirations et fuseaux |
| Marchés `/markets` | 302 vers `/` ; un module `markets_page.py` existe | Restaurer la page dédiée seulement après inventaire des données déjà fusionnées dans Aujourd'hui | indices, cross-asset, secteurs, breadth, volatilité, macro |
| Opportunités `/opportunities` | 200 | Conserver, réorganiser et relier à un entonnoir canonique | actions, ETF, options, anomalies, catalyseurs et gates |
| Analyse `/analysis` | 200 | Conserver ; retirer les verdicts concurrents après AdviceEngine unique | dossier ticker, thèse, scénarios, preuves et contradictions |
| Options `/options` | 200 | Conserver et clarifier les sous-vues | chaîne, IV, Greeks, GEX, liquidité, événements, scénarios |
| Simulateur `/simulator` | 404 | Créer seulement après convergence des trois calculateurs existants | Actions, ETF, Options, Forex, unités, hypothèses, stress et comparaison |
| Portefeuille `/portfolio` | 200 | Conserver ; rendre manuel souverain | enveloppes, cash, positions, thèses, risque, marks et provenance |
| Suivi `/follow-up` | 404 ; `/tracking` est 200 | Migrer Tracking et les watchlists vers Suivi, puis rediriger `/tracking` | idées, positions, options, alertes, échéances et historique |
| Performance `/performance` | 301 vers `/journal` | Créer la page de mesure ; garder Journal comme sous-vue méthodologique | populations réelles/théoriques séparées, benchmark, drawdown et discipline |
| Vertex IA `/intelligence` | 200 mais hors navigation principale | Promouvoir après passage par l'unique gateway IA | assistant, brief, preuves, contradictions, mémoire et audit |
| Système `/system` | 200 | Conserver et consolider | connexions, données, jobs, sécurité, préférences et archives |

## Pages internes et aliases

- `/journal` reste actif pendant la migration, puis devient
  `/performance?view=journal` avec redirection compatible.
- `/tracking` reste actif pendant la migration, puis devient
  `/follow-up` avec redirection compatible.
- `/design-system` devient l'unique surface de composants, en développement.
- `/system/design-system` doit être fusionné dans la surface précédente après
  migration de ses consommateurs.
- `/widget-lab` reste un laboratoire interne ; ses démos ne prouvent pas qu'un
  widget est connecté à une donnée réelle.
- les dizaines de routes legacy ne sont supprimées qu'après inventaire des
  liens, favoris, tests, stores et deep links.

## Collisions P0

1. `GET /options/<sym>` appartient à `ticker_api.opt_ep` et
   `redesign.options_symbol_route`. Flask choisit le paquet JSON avant la page
   HTML : la fiche Options par sous-jacent est inaccessible.
2. `GET /api/anomalies/<sym>` appartient à `analysis_api.api_anomalies` et
   `strategy_os.anomalies_for`. Un seul schéma et un seul propriétaire doivent
   être choisis avant toute refonte visuelle de cette donnée.

## Ordre de cutover visuel

1. résoudre collisions, routeur, manifeste de navigation et typographie ;
2. figer les tokens et composants dans le Design System unique ;
3. Aujourd'hui ;
4. Marchés et Calendrier ;
5. Opportunités et Analyse ;
6. Options puis Simulateur ;
7. Portefeuille, Suivi et Performance/Journal ;
8. Vertex IA puis Système ;
9. aliases, suppression prouvée et audit responsive final.

Ne jamais modifier toutes les pages en une seule PR. Chaque page conserve ses
calculs, routes de données, stores et deep links jusqu'à preuve de parité.
