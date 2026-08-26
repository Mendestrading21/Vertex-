# Matrice des dépôts proposés — 25 août 2026

## Décision générale

Les 60 dépôts uniques proposés ont été classés. Ils ne sont pas des briques à
fusionner en bloc. Vertex reste analyse-only et choisit une référence selon
quatre décisions :

- **ADOPTER/PILOTER** : dépendance ou adaptateur isolé après licence, tests et
  contrat de données ;
- **INSPIRER** : reprendre un patron d'architecture ou une idée, sans copier le
  moteur ;
- **RECHERCHE SEULE** : formule ou hypothèse à revalider indépendamment ;
- **REJETER** : exécution, domaine inadéquat, abandon, licence absente ou valeur
  insuffisante.

Aucun code n'est adopté par ce document. Toute licence marquée « vérifier » est
un blocage légal jusqu'à examen du fichier de licence au SHA choisi.

## IBKR, connexion et exploitation

| Dépôt | Décision | Usage possible / motif |
|---|---|---|
| `InteractiveBrokers/tws-api-public` | **INSPIRER** | artefact officiel historique ; préférer IBKR Campus et l'API installée, tester les contrats sans importer l'exécution |
| `csingley/ibflex` | **PILOTER** | parser de Flex Queries utile à l'historique et à la réconciliation P&L ; lecture seule et stockage point-in-time |
| `antequant/ib-gateway-docker` | **INSPIRER** | healthcheck, cycle de vie Gateway et déploiement reproductible ; aucune ouverture réseau non sécurisée |
| `utilmon/EasyIB` | **ÉVALUER** | comparer les patrons Client Portal ; ne pas ajouter une seconde pile IBKR tant que TWS couvre le besoin |
| `ib-controller/ib-controller` | **REJETER comme dépendance** | héritage opérationnel/JVM et contraintes de licence ; quelques idées de supervision seulement |
| `erdewit/tws_async` | **REJETER** | ancien/archivé ; `ib_async` est déjà la façade retenue |
| `areed1192/interactive-broker-python-api` | **INSPIRER** | exemples pédagogiques d'API native ; pas de dépendance produit |
| `pavankishoremullapudy/InteractiveBrokers_TWS_API` | **RECHERCHE SEULE** | exemples TWS à vérifier ; aucune autorité sur l'API |
| `anthonyng2/ib` | **RECHERCHE SEULE** | petits patrons IB à mesurer ; valeur produit non démontrée |
| `jsarbach/ib-trading` | **RECHERCHE SEULE** | architecture éventuelle de données ; isoler toute surface d'ordre |

## Options, market data et recherche quantitative

| Dépôt | Décision | Usage possible / motif |
|---|---|---|
| `9600dev/mmr` | **INSPIRER** | architecture de recherche/options et observabilité à étudier ; licence à vérifier, aucun copier-coller |
| `rburkholder/trade-frame` | **INSPIRER** | ingestion événementielle et market data ; C++/licence à vérifier, aucune intégration directe |
| `aicheung/option-data-service` | **INSPIRER** | séparation collecte/normalisation/store pour chaînes options ; pas de source canonique sans validation |
| `jonboh/ib_options_collector` | **INSPIRER** | replay et collecte bornée des chaînes ; pacing et entitlement Vertex restent canoniques |
| `mcf-long-short/ibkr-options-volatility-trading` | **RECHERCHE SEULE** | hypothèses vol à retester point-in-time, après coûts et sans exécution |
| `AlexShakaev/backtesting_and_algotrading_options_with_Interactive_Brokers_API` | **RECHERCHE SEULE** | idées de backtest options ; vérifier biais, modèle, licence et données |
| `webclinic017/Options-Strategy-API-Integration` | **RECHERCHE SEULE** | formules/présentation à comparer aux golden vectors Vertex |
| `freqtrade/freqtrade` | **INSPIRER** | qualité des tests, plugins, protections et observabilité ; crypto/GPL/exécution, donc aucune intégration de code |
| `gvolpe/trading` | **INSPIRER** | architecture événementielle typée et supervision ; ne pas importer l'exécution |
| `rsheftel/pandas_market_calendars` | **PILOTER** | calendriers de séances et tests DST/holidays ; dates macro restent issues des organismes officiels |
| `jamesmawm/High-Frequency-Trading-Model-with-IB` | **REJETER** | HFT et exécution incompatibles avec la stratégie et l'infrastructure Vertex |
| `rediar/InteractiveBrokers-Algo-Trading-API` | **REJETER** | bot/exécution et exemples non adaptés au produit analyse-only |

## TradingView

| Dépôt | Décision | Usage possible / motif |
|---|---|---|
| `fabston/TradingView-Webhook-Bot` | **INSPIRER** | réception webhook, file et journal ; supprimer toute sortie broker |
| `atilaahmettaner/tradingview-mcp` | **INSPIRER prudemment** | contrat d'outils et extraction ; non officiel, jamais source de marché primaire |
| `tradesdontlie/tradingview-mcp` | **REJETER en production** | automatisation navigateur/CDP fragile et licence à vérifier |
| `Mathieu2301/TradingView-API` | **REJETER en production** | API non officielle/scraping et maintenance/contrat incertains |
| `Weebapp003/tradingview-mcp` | **REJETER en production** | MCP non officiel et valeur différenciée non prouvée |
| `AnalyzerREST/python-tradingview-ta` | **REJETER** | projet archivé/non officiel ; les signaux doivent être calculés ou reçus officiellement |
| `hackingthemarkets/tradingview-interactive-brokers` | **REJETER** | pont alerte → ordre explicitement hors invariant produit |

## Bots options ou IBKR incompatibles

| Dépôt | Décision | Motif |
|---|---|---|
| `code-rabi/interactive-brokers-mcp` | **REJETER** | surface MCP pouvant agir sur le compte ; Vertex ne délègue aucun ordre à un LLM |
| `ArjunDivecha/ibkr-mcp-server` | **REJETER** | surface d'action et projet archivé |
| `Vincentho711/Interactive-Brokers-Trading-Bot` | **REJETER** | bot d'exécution |
| `PlusGenie/tbot-tradingboat` | **REJETER** | automatisation broker/TradingView et projet ancien |
| `aicheung/0dte-trader` | **REJETER** | 0DTE et exécution, opposés au mandat 120–240 DTE |
| `Jake0303/RiskyOptionsBot` | **REJETER** | exécution options et risque incompatible |
| `Hoary-Stock/ibkr-options-stock-trader` | **REJETER** | trader automatisé |
| `selvanponraj/Earnings-calendar-spread-bot` | **REJETER** | spread bot autour earnings ; événement risqué et exécution |
| `NadirAliOfficial/ibkr-strangle-bot` | **REJETER** | vente/strangle automatisé, risque non borné ou mal adapté |
| `Jake0303/InteractiveBrokersPythonBot` | **REJETER** | bot d'exécution |
| `zoharbabin/quantum-trader` | **REJETER comme intégration** | moteur autonome/exécution ; claims à valider avant toute idée de recherche |
| `daviddme/py-trading-bot` | **REJETER** | framework de bot, pas une source ni un moteur de preuve |
| `ozdemirozcelik/pairs-ibkr` | **RECHERCHE SEULE** | hypothèse pairs trading à valider ; aucun ordre ni stratégie active |
| `jahanzaib-codes/ibkr-ai-trading-bot-gui` | **REJETER** | IA + exécution broker, contraire à la frontière IA |
| `IBKR-BouncyBot/IBKR-Trading-Bot` | **REJETER** | exécution autonome |
| `ppratikcr7/AlgoTradeBot_IB` | **REJETER** | exécution algorithmique |

## Applications et architectures génériques

| Dépôt | Décision | Usage possible / motif |
|---|---|---|
| `mapr-demos/finserv-application-blueprint` | **INSPIRER faiblement** | vieux blueprint data/finserv ; comparer observabilité, pas le produit |
| `AxonFramework/Axon-trader` | **INSPIRER faiblement** | CQRS/event sourcing pour journal immuable ; stack Java sans adoption |
| `SingletonSean/SimpleTrader` | **REJETER** | exemple pédagogique, profondeur insuffisante |
| `evdubs/renegade-way` | **RECHERCHE SEULE** | vérifier la pertinence réelle avant toute utilisation |
| `mitalisalvi/Stock-Trading-application` | **REJETER** | application générique sans avantage institutionnel démontré |
| `sreenivasdoosa/sdoosa-algo-trade-app` | **REJETER** | app d'algo trading/exécution |
| `IBM-Blockchain-Archive/cp-web` | **REJETER** | archive blockchain sans rapport direct avec Vertex 2.0 |
| `kweinmeister/agentic-trading` | **REJETER en production** | agentic trading : un LLM ne doit pas contrôler la décision ni l'ordre |
| `SongoMen/Trader24` | **REJETER** | application générique, valeur et licence à prouver |
| `rubykube/peatio-trading-ui` | **INSPIRER visuellement seulement** | UI exchange crypto ; aucune logique d'exécution ou dépendance |
| `softage0/algorithm-trading-webapp` | **REJETER** | application d'algo trading, architecture non canonique |
| `jiowcl/MQL-CopyTrade` | **REJETER** | copy trading/exécution |
| `pivotal-bank/cf-SpringBootTrader` | **REJETER** | démo Spring/finance, pas une brique Vertex |
| `docker-production-aws/microtrader` | **REJETER** | microservice de démonstration/fictif, pas une source financière |
| `Exslims/MercuryTrade` | **REJETER** | projet sans rapport avec la recherche institutionnelle Vertex |

## Patrons retenus

Les dépôts proposés confirment six idées utiles, mais celles-ci sont réécrites
selon les contrats Vertex :

1. **un broker adapter lecture seule** avec replay et pacing ;
2. **un collecteur options séparé** de l'API web ;
3. **un journal événementiel immuable** pour décisions et changements ;
4. **un scheduler observable** avec backpressure et circuit breakers ;
5. **des calendriers de séances testés** séparés des calendriers macro ;
6. **un receiver TradingView asynchrone** qui ne devient jamais un exécuteur.

Tout le reste est subordonné au point-in-time store, aux golden tests et à la
licence. La popularité GitHub, une capture d'écran ou un README prometteur ne
constituent jamais une preuve de qualité.
