# Audit total Vertex — 24 août 2026

## Verdict exécutif

Vertex n'est plus un prototype. La branche `integration/vertex-1-0-rc`
constitue une base cohérente, riche et largement testée. Elle n'est cependant
pas une release finale ni encore un système institutionnel prouvé en conditions
réelles.

Le verrou principal n'est pas le nombre de fonctionnalités. Il est la qualité
de la preuve aux frontières : broker réel, données point-in-time, événements
réels, calibration hors échantillon et attribution des décisions.

Verdict au 24 août 2026 :

- **GO** pour poursuivre le développement sur une branche empilée sur la RC ;
- **NO-GO** pour fusionner ou taguer `v1.0.0` sans clôture formelle de G5 et
  CI verte ;
- **NO-GO** pour ajouter un nouveau moteur de score avant d'avoir un registre
  point-in-time et un protocole de validation commun ;
- **GO** pour les sources officielles SEC, FRED, BLS et CFTC, derrière des
  adaptateurs versionnés et des feature flags ;
- **GO conditionnel** pour une source payante de news/options, après preuve que
  les abonnements IBKR existants ne couvrent pas le besoin.

## Périmètre et base auditée

- dépôt : dépôt GitHub Vertex connecté ;
- branche : `integration/vertex-1-0-rc` ;
- SHA initial des mesures statiques :
  `dd3eecc0f46fd76f17c81d2598f1270b0c26b83e` ;
- base rafraîchie avant publication :
  `d77b06d4836bbe1ef91b6ca2e8220561dd5bbd46` ;
- base `main` observée : `d52a39d4baf1ae17d09f01e87b7fc70abee694d0` ;
- PR candidate : #793, ouverte et brouillon ;
- écart RC / `main` : 169 fichiers, +35 864 / -1 015 lignes ;
- inventaire de travail : 1 973 fichiers hors `.git`, environ 700 branches
  distantes recensées par les instruments existants.

Cet audit a relu le corpus canonique, l'architecture, les profils stratégiques,
les sources, les moteurs, le runtime, les tests, la CI, l'intégration IBKR et les
références open source pertinentes.

## Preuves rejouées

| Mesure | Résultat |
|---|---:|
| `compileall` | PASS |
| suite locale propre au SHA initial | 3 571 passed, 7 skipped, 1 warning |
| suite après rebase sur `d77b06d` | 3 575 passed, 7 skipped, 1 warning |
| tests collectés après rebase | 3 582 |
| gardiens namespace + no-orders | 6 passed |
| couverture Python `vertex/` | 87 % (20 478 statements, 2 651 manquants) |
| audit dépendances connues | aucune vulnérabilité connue trouvée par `pip-audit` |
| complexité Radon | moyenne B, 8,24 |
| blocs complexité E/F | 63, dont 40 classés F |
| alertes Ruff | 1 256 |

La base rafraîchie ajoute une preuve de session réelle : TWS live sur le port
7496, `readonly=True`, les rôles cotations, indices, options et passerelle
connectés sans échec, huit espaces servis et aucun journal client en erreur.
Cette preuve rend faux l'ancien état « G5 vide », mais elle ne clôt pas seule
la matrice complète du protocole G5 (modes de marché, panne partielle,
reconnexion, pacing, réconciliation et artefact anonymisé reproductible).

La première exécution locale avait un faux échec : l'environnement virtuel
temporaire, créé dans le dépôt, était parcouru par le gardien de noms
personnels. Après déplacement hors du dépôt, la suite est verte. Le test reste
fragile parce qu'il inspecte les fichiers non suivis sans exclure les
environnements virtuels arbitrairement nommés.

## Défaut CI bloquant découvert

Le workflow GitHub Actions associé au SHA candidat est rouge : run
`32708784860`, job `test` en échec.

Cause : `tools/vertex_1_0/mesurer_exploitation.py` exige `origin/main`, mais
`actions/checkout` utilise un clone superficiel qui ne crée pas cette référence.
Le test G6 agrégé traite alors l'absence de preuve comme une anomalie :
`origin/main introuvable`. Le job `safety` passe, mais le smoke runtime est
ignoré après l'échec du job principal.

Le premier correctif, limité à `origin/main`, a fait passer G6 mais révélé le
second contrat : `tests/test_vertex_1_0_branches.py` classe le dépôt distant et
refuse de conclure avec une seule référence. La correction finale récupère les
pointes de toutes les branches distantes avec `--depth=1 --no-tags`, puis un
gardien statique tient ce prérequis. Elle ne récupère pas leur historique
complet.

## Forces réelles

1. **Sécurité structurante** : analyse uniquement, `READONLY`,
   `ANALYSIS_ONLY`, IBKR en lecture seule, aucun chemin d'ordre accepté.
2. **Décision déterministe** : l'IA explique mais ne possède ni prix, ni Greek,
   ni score, ni hard gate, ni verdict.
3. **Provenance et dégradation** : états `LIVE`, `DELAYED`, `STALE`, `DEMO`,
   `OFFLINE`, `MISSING`, replis visibles et absence honnête.
4. **Architecture de décision** : packet versionné, hard gates, scénarios,
   compatibilité portefeuille, mémoire et journal.
5. **Options** : chaîne, liquidité, IV/HV, skew, terme, surface, GEX, scénarios,
   événements et sélection de contrats déjà présents.
6. **Portefeuille** : corrélation, facteurs, stress historiques, risque,
   réconciliation et suivi de thèse.
7. **Qualité UI** : huit espaces, mesures desktop/mobile/clavier/contraste,
   erreurs client observables et mode dégradé explicite.
8. **Discipline de preuve** : de nombreux instruments possèdent des témoins
   négatifs et des tests de mutation manuels documentés.

## Faiblesses prioritaires

### P0 — La RC n'est pas releasable

- PR #793 encore brouillon et non fusionnée ;
- CI rouge sur le SHA candidat ;
- une vraie session TWS/IBKR est désormais prouvée, mais G5 n'est pas encore
  clôturé par un artefact complet et reproductible ;
- spécimen WMB réel encore manquant ;
- aucun tag final autorisé.

### P0 — Frontière IBKR non couverte

La couverture globale de 87 % masque une zone critique :

| Module | Couverture mesurée |
|---|---:|
| `ibkr_contracts.py` | 0 % |
| `ibkr_market_data.py` | 0 % |
| `ibkr_option_chain.py` | 0 % |
| `ibkr_positions.py` | 0 % |
| `ibkr_news.py` | 19 % |
| `ibkr_historical.py` | 57 % |
| `ibkr_gateway.py` | 78 % |
| `ibkr_link.py` | 94 % |

Les tests valident surtout les contrats, replis et faux brokers. La session
réelle prouve la connexion et les rôles principaux, mais pas encore toute la
matrice : modes de marché, rythme, callbacks, Greeks, erreurs 354/100/10167,
reconnexion ni cohérence compte réel/papier.

### P0 — Fondamentaux non point-in-time

Le domaine fondamental repose surtout sur `yfinance.Ticker.info`, avec cache six
heures. Cette source est pratique mais :

- ne fournit pas un historique point-in-time reproductible ;
- peut intégrer des révisions inconnues au moment étudié ;
- n'explicite pas toujours période, devise, unité et méthode comptable ;
- ne permet pas un backtest propre des facteurs fondamentaux ;
- est lente et sujette au throttling.

Conséquence : un score historique peut bénéficier d'informations futures.

### P0 — Calendrier macro partiellement fabriqué par règle

`macro_calendar.py` contient les dates FOMC 2026 en dur, déduit NFP par
« premier vendredi » et place CPI au 13 avec `approx=True`. L'étiquette
indicative évite le mensonge total, mais ce n'est pas suffisant pour un moteur
d'événements qui doit protéger des options autour d'une publication.

Une date approximative ne doit jamais déclencher ou lever un hard gate.

### P1 — Monolithe et complexité

- `terminal.py` approche 800 Ko et conserve les boucles de fond ;
- 283 captures larges `Exception`, dont 71 motifs `except/pass` ;
- 40 fonctions classées F par Radon ;
- complexités maximales observées : 168 pour la détection d'anomalies, 137 pour
  une analyse, 124 pour une route d'analyse ;
- 1 256 alertes Ruff, dont erreurs potentielles inutilisées, temps sans timezone
  et captures silencieuses.

La suite verte protège le comportement connu, pas tous les états cachés par une
exception silencieuse.

### P1 — Sources d'information incomplètes

Absents du code de production : SEC EDGAR/XBRL, FRED, BLS réel, CFTC COT, WSH,
P&L IBKR, depth, tick-by-tick, real-time bars et scanners IBKR canoniques.

Les données « 13F » et initiés affichées viennent de Yahoo, sans accès direct au
dépôt SEC ni conservation de la date de dépôt originale.

### P1 — Validation quantitative encore insuffisante

Vertex contient backtests, walk-forward, calibration et track record, mais il
manque une chaîne unique qui impose à chaque facteur et recommandation :

- dataset point-in-time immuable ;
- univers survivorship-bias-safe ;
- coûts, spread, slippage et délai de décision ;
- purging/embargo pour les fenêtres qui se chevauchent ;
- segmentation par régime et liquidité ;
- calibration hors échantillon ;
- intervalle d'incertitude ;
- attribution factorielle et comparaison à une baseline simple ;
- critères de promotion, quarantaine et retrait d'un signal.

### P1 — Doctrine stratégique à arbitrer

Le profil V4 contient une catégorie primaire `DYNAMIC` delta 0,28–0,45 et des
pertes planifiées de 25–35 %, alors que la constitution utilisateur la plus
récente privilégie les LEAPS delta 0,70–0,90 et une asymétrie idéale proche de
-10 % / +50 % / +100 % et plus.

Ce n'est pas une correction technique. Il faut une V5 explicite, revue
humainement et rétrotestée ; V4 ne doit pas être modifiée en place.

### P2 — Dépôt et gouvernance

- environ 700 branches ;
- 1 973 fichiers ;
- documentation historique très volumineuse ;
- un index Skyler dépasse 1,3 Mo ;
- 63 règles CSS prouvées inatteignables mais conservées ;
- plusieurs fichiers UI dépassent 1 000 lignes ;
- le nombre de tests par lot rend la navigation et la propriété difficiles.

Le nettoyage doit rester prouvé et réversible ; il ne doit pas concurrencer la
stabilisation live.

## Ce qu'il ne faut pas faire

- copier un bot GitHub complet dans Vertex ;
- brancher un moteur d'exécution ou un carnet d'ordres ;
- remplacer IBKR par dix API redondantes ;
- présenter une probabilité ML non calibrée comme une chance de gain ;
- rétrotester des fondamentaux actuels sur le passé ;
- ajouter des indicateurs sans hypothèse, baseline et protocole de retrait ;
- fusionner Signal OS, OpenBB, LEAN, Qlib ou NautilusTrader en bloc ;
- modifier V4 silencieusement ;
- déclarer la release verte tant que GitHub Actions et la clôture formelle de
  G5 ne le sont pas.

## Priorité d'investissement technique

1. Corriger CI et rejouer la RC sur le même SHA.
2. Transformer la preuve TWS réelle déjà obtenue en artefact G5 complet,
   anonymisé et reproductible.
3. Installer un registre point-in-time et un identifiant instrument canonique.
4. Ajouter SEC/FRED/BLS/CFTC derrière contrats de provenance.
5. Construire le moteur d'événements et le dossier de thèse versionné.
6. Unifier le laboratoire de validation et l'attribution.
7. Renforcer options et portefeuille avec scénarios réellement alimentés.
8. Proposer V5 et la soumettre à validation humaine.
9. Réduire `terminal.py`, les exceptions silencieuses et la dette de dépôt.

Les lots détaillés et leurs critères d'acceptation sont définis dans
`../roadmap/VERTEX-INTELLIGENCE-2.0.md`.
