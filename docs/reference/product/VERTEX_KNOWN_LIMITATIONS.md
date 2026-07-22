# Vertex — Limitations connues et déclarées

Honnêteté avant tout : ces limitations sont assumées, visibles dans l'UI
quand elles s'appliquent, et aucune n'est masquée par une donnée inventée.

## Données

1. **OHLC intrajournalier/quotidien complet non exposé par le scan** — les
   graphiques prix tracent les clôtures ; le mode chandelier ne s'active que
   si des barres OHLC complètes sont fournies (repli honnête + limitation
   affichée sur la carte).
2. **Moyennes mobiles en série non fournies** par les moteurs (valeurs
   ponctuelles seulement) — non tracées, jamais recalculées côté UI.
3. **Advance/decline et nouveaux hauts/bas** non calculés par les moteurs —
   la vue Breadth l'indique au lieu d'afficher un proxy douteux.
4. **Breadth calculée sur les leaders scannés** (univers partiel) — légende
   explicite sur la carte.
5. **Univers = constituants actuels** des indices : biais du survivant
   documenté (`vertex/research/dataset.py`) pour toute recherche historique.
6. **IV Rank/percentile** refusés tant que l'historique d'IV < 20
   observations (« honnêteté » affichée par la surface de vol).
7. **Secteurs en anglais** (« Technology ») dans les filtres — valeurs
   moteur exactes.

## Intégrations (dépendances externes — procédures de résolution)

8. **IBKR absent dans l'environnement cloud** : brancher TWS/Gateway local,
   retirer `NO_IBKR=1` — la passerelle est `readonly=True` en dur ; sans
   broker : marques desk/EOD, Greeks MODEL_ESTIMATE, alertes Actionnables
   bloquées par la qualité de données.
9. **TradingView** : définir `TRADINGVIEW_SECRET` dans `.env` puis installer
   `tradingview/vertex_signals.pine` (guide `tradingview/README.md`) ; sans
   secret le webhook répond 503 et l'UI affiche « non configuré ».
10. **Claude** : définir `ANTHROPIC_API_KEY` ; sans clé, brief et analyste
    servent la synthèse déterministe (même schéma, étiquetée).

## Produit

11. **Comparateur multi-titres** : redirigé vers Analyse — la comparaison
    côte à côte reviendra comme sous-vue dédiée.
12. **Simulateur paper-trading legacy** (`simCash`/`simTrades`) : données
    préservées et synchronisées, sans UI dédiée dans la nouvelle expérience
    (export possible depuis Système/Préférences).
13. **Brief IA** : le paquet structuré et la validation stricte existent ;
    la reformulation Claude n'est pas branchée par défaut (brief
    déterministe servi, étiqueté comme tel).
14. **Drill-down secteurs au clic canvas** : nécessite de viser la barre
    (hit-test Chart.js) — le tableau des leaders offre le même drill-down.
15. **Course de sync theoriquement possible entre deux appareils écrivant
    la même seconde** (last-writer-wins par blob) — atténuée par le flush
    `sendBeacon` et les backups quotidiens restaurables.
16. **Hypothesis (property-based) non ajouté** : les propriétés sont testées
    par grilles déterministes (31 tests golden) pour ne pas ajouter de
    dépendance non épinglée au runtime de production.

## Périmètre volontairement exclu

17. Aucun chemin d'exécution d'ordre — par conception, pour toujours.
18. Aucune donnée synthétique hors mode DÉMO explicitement étiqueté
    (bannière + badges + sources « demo »).
