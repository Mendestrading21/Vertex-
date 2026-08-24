# Sources, API et références open source

## Règle de sélection

Une source n'entre dans Vertex que si elle apporte une information absente,
améliore la preuve ou remplace un repli fragile. Chaque adaptateur doit exposer
valeur, unité, devise, instant de l'observation, instant de réception, source,
mode, fraîcheur, qualité, entitlement et erreur.

Les secrets restent en variables d'environnement. Aucun abonnement payant n'est
supposé actif avant une sonde réelle. Aucune bibliothèque externe ne devient le
calculateur canonique sans tests croisés et revue de licence.

## Pile recommandée

| Priorité | Source | Coût / accès | Usage Vertex | Décision |
|---|---|---|---|---|
| P0 | IBKR TWS / Gateway via `ib_async` | compte + entitlements | prix, options, positions, P&L, news, historique | **adopter et approfondir** |
| P0 | SEC `data.sec.gov` | gratuit, sans clé, fair-access | dépôts, XBRL, 8-K, 10-Q/K, Form 4, 13F | **adopter** |
| P0 | FRED | clé gratuite | taux, courbe, liquidité, crédit, macro | **adopter** |
| P0 | BLS API | v1 sans clé, v2 clé gratuite | CPI, emploi, salaires et séries officielles | **adopter** |
| P1 | calendriers officiels Fed/BLS/BEA | gratuit | dates exactes et révisions d'événements | **adopter** |
| P1 | CFTC COT PRE | gratuit, généralement sans jeton | positioning futures et options futures | **adopter ciblé** |
| P1 | WMB versionné | interne | contexte macro et catalyseurs | **adopter après spécimen réel** |
| P1 | IBKR WSH | abonnement requis | événements entreprise spécialisés | **sonder entitlement** |
| P2 | Massive stocks/options | plans gratuits et payants | historique options, snapshots, NBBO, news | **optionnel** |
| P2 | Benzinga via Massive | abonnement news | news structurées temps réel | **optionnel après gap analysis IBKR** |
| P2 | Finnhub | clé et limites selon plan | calendrier, news, transcripts, estimations | **secondaire, jamais canonique seul** |
| Repli | yfinance / Stooq | gratuit, non garanti | continuité différée/EOD | **conserver comme repli étiqueté** |

## Capacités IBKR à ajouter ou prouver

Vertex utilise déjà `reqMktData`, `reqHistoricalData`,
`reqSecDefOptParams`, positions, account summary et news. Les prochaines
capacités ne doivent passer que par un worker/scheduler unique :

1. capture explicite du type de donnée 1/2/3/4 (live/frozen/delayed/frozen
   delayed) par requête ;
2. `reqPnL` / `reqPnLSingle` pour réconcilier P&L compte et calcul Vertex ;
3. Greeks IBKR avec présence/absence par tick et quote age ;
4. snapshots de chaîne bornés, dédupliqués et priorisés ;
5. `reqRealTimeBars` pour les instruments réellement suivis, pas l'univers ;
6. tick-by-tick et depth uniquement pour mesurer liquidité/slippage sur une
   petite watchlist ;
7. scanners TWS comme source de candidats, jamais comme verdict ;
8. nouvelles IBKR en flux et historique, avec provider code, article id et
   entitlement ;
9. WSH pour earnings, splits, spinoffs et événements si l'abonnement existe ;
10. budget de pacing par classe de requête, backpressure, circuit breaker,
    cache et observabilité.

Le Web API IBKR n'est pas requis pour la V1 locale. Il ajoute OAuth et une
seconde pile d'authentification. Il ne doit être étudié que pour un futur accès
à distance, toujours avec scopes lecture seule et sans endpoint d'ordre exposé
par Vertex.

## Sources officielles gratuites

### SEC EDGAR / XBRL

Créer `vertex/data_sources/sec_edgar.py` et un store point-in-time :

- mapping ticker ↔ CIK ↔ conId ;
- submissions et accession numbers ;
- `companyfacts` XBRL avec période, unité, form, filed date et frame ;
- 8-K et exhibits pour événements ;
- Form 4 pour initiés ;
- 13F pour détention institutionnelle ;
- détection des restatements ;
- respect du User-Agent et du fair-access SEC ;
- cache immuable par accession number.

Ne jamais transformer automatiquement un tag XBRL manquant en zéro. Les ratios
Vertex sont calculés depuis des faits normalisés et conservent les faits sources.

### FRED et BLS

Créer un `MacroObservation` commun :

- `series_id`, valeur, unité, fréquence ;
- observation date, release timestamp, vintage/realtime period ;
- consensus si disponible séparé de la valeur officielle ;
- précédente valeur telle que connue avant révision ;
- surprise et z-score calculés seulement si les entrées sont présentes.

FRED fournit la profondeur historique et les vintages ; BLS reste la source
officielle des séries et calendriers emploi/inflation. Les dates réelles
remplacent les règles approximatives de `macro_calendar.py`.

### CFTC COT

Usage limité aux régimes macro et actifs liés aux futures : indices, taux,
dollar, énergie, métaux. Stocker date du relevé (mardi) et date de publication
(souvent vendredi) séparément pour éviter le look-ahead.

## Références open source évaluées

Métadonnées observées sur GitHub le 24 août 2026.

| Projet | Signal de maturité | Licence | Ce qu'on reprend | Décision |
|---|---:|---|---|---|
| `ib-api-reloaded/ib_async` | 1 720★, actif | BSD-2 | client IBKR sync/async | **dépendance actuelle** |
| `dgunning/edgartools` | 2 609★, actif | MIT | parsing SEC/XBRL, types, filings | **adapter ou dépendance optionnelle** |
| `microsoft/qlib` | 47 893★, actif | MIT | datasets, expérimentation, ML workflow | **référence laboratoire** |
| `QuantConnect/Lean` | 21 330★, actif | Apache-2 | modèle événementiel, point-in-time, backtest | **référence, pas intégration en bloc** |
| `polakowo/vectorbt` | 8 804★, actif | licence à vérifier | recherche vectorisée massive | **POC isolé uniquement** |
| `dcajasn/Riskfolio-Lib` | 4 456★, actif | BSD-3 | risk parity, CVaR, facteurs | **adapter derrière façade** |
| `PyPortfolio/PyPortfolioOpt` | 5 979★, actif | MIT | Black-Litterman, HRP, frontier | **référence allocation** |
| `ranaroussi/quantstats` | 7 579★, actif | Apache-2 | attribution et rapports | **adapter métriques** |
| `OpenBB-finance/OpenBB` | 72 228★, actif | licence spécifique/AGPL selon usage | contrats de providers | **architecture de référence seulement** |
| `AI4Finance-Foundation/FinRL` | 16 080★ | MIT | protocoles RL | **éviter en production avant preuve forte** |
| `nautechsystems/nautilus_trader` | 27 582★, actif | LGPL-3 | architecture événementielle déterministe | **ne pas importer : orienté exécution** |
| `erdewit/ib_insync` | archivé | BSD | héritage API IBKR | **ne pas adopter** |

Les étoiles ne sont pas une preuve de qualité. Les critères décisifs sont
activité, tests, licence, point-in-time, déterminisme, absence d'exécution dans
Vertex et coût d'intégration.

## Architecture d'adaptation

```text
provider externe
  → adapter mince
  → modèle canonique Vertex
  → validation schéma/unité/temps
  → point-in-time store
  → réconciliation multi-source
  → moteurs déterministes
```

Interdictions :

- retourner directement les objets d'une bibliothèque externe à l'UI ;
- mélanger deux sources dans une valeur sans lister les contributeurs ;
- utiliser un provider de news comme source de prix ;
- ajouter une dépendance AGPL ou LGPL sans décision de licence ;
- appeler une API payante dans les tests ;
- télécharger des données sous une licence incompatible avec la conservation
  ou l'affichage.

## Variables d'environnement proposées

```text
FRED_API_KEY=
BLS_API_KEY=
SEC_USER_AGENT="Vertex contact@example.com"
MASSIVE_API_KEY=
FINNHUB_API_KEY=
VERTEX_ENABLE_SEC=0
VERTEX_ENABLE_FRED=0
VERTEX_ENABLE_BLS=0
VERTEX_ENABLE_CFTC=0
VERTEX_ENABLE_MASSIVE=0
VERTEX_ENABLE_FINNHUB=0
```

Les sources officielles activables sans clé doivent quand même avoir un feature
flag, une politique de cache, un timeout et une limite de débit.

## Liens de référence

- IBKR Campus TWS API : https://ibkrcampus.com/campus/ibkr-api-page/twsapi-doc/
- IBKR market data subscriptions : https://ibkrcampus.com/campus/ibkr-api-page/market-data-subscriptions/
- SEC EDGAR APIs : https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- FRED API : https://fred.stlouisfed.org/docs/api/fred/
- BLS API : https://www.bls.gov/developers/home.htm
- CFTC COT : https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- OpenBB providers : https://docs.openbb.co/odp/python/extensions/providers
- Massive API : https://massive.com/docs/
