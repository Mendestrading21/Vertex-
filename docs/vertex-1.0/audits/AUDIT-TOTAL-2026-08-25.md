# Audit produit, code et exploitation Vertex — 25 août 2026

## Verdict

Vertex possède déjà une profondeur inhabituelle : huit espaces produit, une
chaîne de décision déterministe, un domaine options riche, une intégration IBKR
strictement en lecture seule et plusieurs milliers de tests. Le projet n'a pas
besoin d'un nouveau « grand rebuild » concurrent. Il a besoin de faire converger
les nombreuses couches existantes vers une seule architecture mesurable.

**Décision : GO pour Vertex Intelligence 2.0 par lots empilés ; NO-GO pour une
réécriture big-bang, l'exécution d'ordres ou la fusion automatique.**

Les priorités qui conditionnent tout le reste sont :

1. sortir les appels réseau lents des requêtes UI ;
2. clore la preuve IBKR réelle et le replay ;
3. rendre les données point-in-time avant de promettre un backtest fiable ;
4. supprimer les propriétaires fonctionnels en double ;
5. unifier le modèle options et la validation quantitative ;
6. consolider les huit espaces autour d'une question unique par page ;
7. traiter les ETF comme des instruments de premier rang ;
8. rendre sécurité, fraîcheur, provenance et incertitude visibles partout.

## Baselines et méthode

Deux états ont été distingués pour ne pas mélanger les preuves :

| Baseline | SHA / branche | Usage |
|---|---|---|
| release publique | `d52a39d4baf1ae17d09f01e87b7fc70abee694d0` / `main` | mesures indépendantes et comportement réellement publié |
| programme RC | PR #793 puis PR #794 et descendantes | corrections déjà engagées, à ne pas dupliquer |

Mesures rejouées sur `main` dans un environnement propre :

| Mesure | Résultat |
|---|---:|
| compilation Python | PASS |
| tests | 3 247 PASS après exclusion du venv temporaire du dépôt |
| JavaScript `node --check` | 35/35 PASS |
| routes Flask | 194 |
| lignes Python | environ 53 800 |
| alertes Ruff | 1 160 |
| `except Exception` larges | 279 |
| `except/pass` silencieux | 75 |
| fonctions Radon CC > 30 | 63 |
| fonctions mesurées | 1 420 |
| vulnérabilités connues `pip-audit` | 0 détectée |

Sur la branche de la PR #794 enrichie par cet audit, la suite complète termine
à **3 575 passed, 7 skipped, 1 warning** après récupération des seules pointes
distantes requises par le gardien de gouvernance. Le premier passage local a
échoué honnêtement avec « trop peu de branches » parce que le clone superficiel
n'exposait que deux références ; aucune règle n'a été affaiblie pour le faire
passer.

Le dépôt contient environ 1 956 entrées suivies, dont 919 Markdown, 729 Python,
146 PNG, 39 JavaScript et 17 CSS. `terminal.py` sur `main` mesure environ 813 Ko
et 7 275 lignes. La branche RC a déjà commencé son extraction : l'audit doit
donc guider cette convergence et non recréer des modules parallèles.

## Bloquants P0

### P0.1 — La fiche Analyse peut bloquer sur le réseau

`/api/ticker/<sym>` appelle synchronement `options_pack()`. Même avec
`NO_IBKR=1` et `DEMO=1`, le paquet instancie `yfinance.Ticker`, puis consulte
prix, historique, informations, news, calendrier, expirations et chaînes. Un
smoke local a dépassé 120 secondes après une erreur de cotation à trois
secondes. Une PR descendante traite aussi un chemin IBKR lent sur des strikes
invalides : ce sont deux causes distinctes d'un même défaut d'architecture.

**Cible :** la route ne lance aucune collecte lourde. Elle sert un snapshot
borné, daté et éventuellement rassis, puis demande un rafraîchissement
asynchrone coalescé. Budget cible : p95 chaud < 400 ms ; p95 froid < 1,5 s pour
la réponse initiale ; chaque fournisseur a timeout, circuit breaker et métrique.

### P0.2 — La donnée historique n'est pas entièrement point-in-time

Une partie des fondamentaux et événements vient encore d'états actuels Yahoo.
Un backtest peut donc voir une révision ou une composition qui n'était pas
disponible à la date étudiée. Les PR #797 et #798 posent la bonne fondation
(`observed_at`, `available_at`, `received_at`, identité conId/CIK/ticker) ;
aucun nouveau score historique ne doit contourner ce socle.

### P0.3 — La frontière IBKR doit être prouvée, pas seulement connectée

L'invariant `readonly=True` est solide et les méthodes d'ordre sont absentes de
la façade. Il reste à prouver en replay et en session réelle : modes de marché,
entitlements, pacing, reconnexion, erreurs courantes, chaîne options, positions,
P&L, horodatages et réconciliation. Les PR #795, #800–#803 et #807 couvrent déjà
une grande partie de ce chemin ; elles sont la ligne d'exécution canonique.

### P0.4 — Le programme GitHub est trop fragmenté

Le dépôt expose environ 700 pointes distantes et des centaines de documents de
lots. La série #793–#808 contient déjà une architecture cohérente, mais son
empilement impose un ordre strict. Avant tout nouveau lot, Claude doit lire les
PR ouvertes, identifier l'ancêtre et le propriétaire canonique, puis continuer
le premier lot non terminé. Aucun doublon « V2 », « ultimate » ou « rebuild ».

## Audit page par page

### Aujourd'hui `/`

**Question cible :** que dois-je décider ou surveiller aujourd'hui, et pourquoi ?

Forces : régime, changements, opportunités, alertes et portefeuille sont déjà
réunis. Défauts : densité élevée, plusieurs récits concurrents, valeurs parfois
issues de pipelines d'âges différents et langage pouvant ressembler à une
injonction. L'écran doit devenir un brief en cinq blocs : état marché, trois
décisions maximum, changements depuis la dernière session, risques
portefeuille, prochaines échéances. Chaque bloc porte source, âge, qualité et
raison de dégradation. Aucun ranking ne paraît « live » si son intrant est
rassis.

### Marchés `/markets`

**Question cible :** quel régime domine et quelles expositions favorise-t-il ?

Les vues macro, secteurs, breadth et volatilité sont utiles mais encore trop
juxtaposées. La V2 doit ajouter cross-asset, courbe des taux, crédit, dollar,
matières premières, facteurs et calendrier officiel. Le régime doit montrer ses
features, sa confiance, ses transitions et les données manquantes. Une date
macro indicative ne peut ni activer ni lever un hard gate.

### Opportunités `/opportunities`

**Question cible :** quels dossiers méritent une recherche maintenant ?

Les onglets radar, actions, options, anomalies et calendrier dupliquent parfois
les fonctions de Marchés et Options. La page cible est une file de recherche
unique, pas une collection de screeners : univers Actions / ETF / Options,
filtres reproductibles, score décomposé, liquidité, catalyseur, risque,
compatibilité portefeuille et statut de preuve. Une anomalie crée une piste ;
elle ne crée jamais un verdict.

### Analyse `/analysis` et `/analysis/<sym>`

**Question cible :** la thèse est-elle vraie, opportune, falsifiable et adaptée
au portefeuille ?

La fiche actuelle agrège fondamentaux, catalyseurs, timing, sentiment,
anomalies, TradingView, plan, risques, IA, options, pré-trade et historique.
Cette profondeur est un atout, mais la page est un « God screen » et dépend
d'une route synchrone lente. La V2 conserve une URL et un `DecisionPacket`, avec
divulgation progressive : Synthèse, Entreprise/ETF, Valorisation, Prix et
volume, Catalyseurs, Options, Portefeuille, Preuves. Les calculs sont produits
par des moteurs déterministes ; l'IA explique les champs déjà présents et cite
leurs identifiants de preuve.

### Portefeuille `/portfolio`

**Question cible :** quels risques réels sont portés et quelle nouvelle idée
les augmente ou les diversifie ?

Positions, performance, risque, options et watchlist sont déjà riches. La
priorité est la vérité broker : positions et P&L réconciliés, source du mark,
devise, FX, cash, coût de revient et divergences visibles. La V2 ajoute
contributions beta/delta/gamma/vega/theta, concentration titre/secteur/facteur/
catalyseur, downside correlation, liquidité et stress. Le dimensionnement reste
une feuille analytique non transmissible, jamais un ticket exécutable.

### Options `/options`

**Question cible :** quel véhicule long à risque borné exprime le mieux une
thèse sur les prochaines semaines ?

Structure, positioning, échéances longues, positions, volatilité et événements
sont présents. La terminologie actuelle mélange « LEAPS 180–540 », swing et
tactique 20–60 jours. Le mandat canonique est : calls/structures longues à
débit borné, DTE préféré 120–240, cible 180, revues 2/4/6 semaines. À 180 jours,
parler d'« échéance longue tactique » plutôt que LEAPS conventionnel.

Un dossier contrat V2 contient : conId/localSymbol, spot et forward, bid/ask/
mid/mark avec âge, spread, tailles, volume, OI, IV broker et modèle, Greeks
broker et modèle, taux, dividendes, borrow si pertinent, skew, terme, surface,
événement, cube spot × temps × IV, liquidité, slippage, perte maximale et
invalidation. Les options 0DTE, ventes nues et bots d'exécution sont hors mandat.

### Journal `/journal`

**Question cible :** qu'avons-nous décidé, qu'avons-nous appris et la méthode
s'améliore-t-elle ?

Discipline, chronologie, apprentissages, progression et track record existent.
La V2 sépare physiquement : décisions déclarées, expériences hypothétiques,
shadow signals et résultats réels. Le packet original est immuable ; accepter,
refuser ou attendre est un événement distinct. Les évaluations montrent MFE,
MAE, résultat, thèse cassée, calibration, attribution et limites de cohorte.

### Système `/system`

**Question cible :** peut-on faire confiance au système maintenant ?

La page réunit connexions, données, jobs, paramètres et archives, mais le mot
« automatisations » peut être confondu avec l'exécution. Renommer en
« Collectes et calculs ». Montrer par source : configuration, entitlement,
mode, dernière réussite, âge, latence p50/p95, erreurs, quota/pacing, cache et
replay. Ajouter sauvegarde/restauration, migrations, version de schéma, build,
profil actif, sécurité, audit de dépendances et statut no-orders.

### Intelligence `/intelligence`

La page analyste/comité/recherche/mémoire recoupe Analyse, Journal et Système.
Elle ne doit pas devenir un neuvième cockpit ambigu. Deux choix acceptables :
un laboratoire expert sous Système, ou des panneaux spécialisés dans Analyse et
Journal. Tant qu'un arbitrage humain n'est pas pris, elle reste secondaire et
ne crée aucun nouveau verdict propriétaire.

### Tracking `/tracking`

Le suivi actif/clos est utile mais ne justifie pas une navigation primaire.
Il devient la vue cycle de vie depuis Portefeuille et Journal, alimentée par les
mêmes identifiants de packet et de position, sans second registre.

### Design system et Widget Lab

Ils restent des surfaces internes. Widget Lab est trop volumineux pour être une
page produit. Chaque composant promu doit résoudre une question réelle, utiliser
les tokens canoniques et remplacer un composant existant. Les noms historiques
`neon-glass`/`copper` peuvent survivre pendant une migration, pas créer une
nouvelle couche de thème. La doctrine reste obsidienne/graphite institutionnelle,
calme, contrastée, avec vert/rouge/ambre réservés au sens financier.

## Actions, ETF et options : trois dossiers, un même contrat

Les actions gardent les horizons 3/6/12 mois. Les options expriment une thèse
sur 2/4/6 semaines au moyen d'une échéance préférée 120–240 jours. Les ETF
deviennent first-class avec :

- émetteur, indice suivi, domicile, devise et couverture FX ;
- AUM, frais, spread, ADV, premium/discount et tracking difference ;
- distributions, fiscalité/domicile clairement étiquetés, sans conseil fiscal ;
- holdings point-in-time, concentration, overlap et look-through ;
- expositions pays, secteur, facteur, duration et matières premières ;
- risque de structure, prêt de titres, réplication et fermeture ;
- compatibilité portefeuille calculée sur les expositions sous-jacentes.

IBKR peut fournir contrats et cotations ; les holdings et documents doivent
venir de fichiers officiels d'émetteurs ou de fournisseurs licenciés, avec date
d'effet et provenance.

## Audit des calculs et de l'intelligence

### Options

Plusieurs générations de calculateurs coexistent. Le nouveau
`scenario_pricer` gère taux et dividendes continus, alors que des chemins legacy
ont des hypothèses plus simples. Créer un noyau canonique versionné et tester
chaque ancien consommateur contre lui. Ajouter : parité call-put, bornes,
monotonicité, cas limites, dividendes discrets, taux, IV crush, corporate
actions, convention American/European explicitée et comparaison indépendante.

### Backtests et probabilités

Le projet contient walk-forward, PSR/DSR et un PBO explicitement proxy. Ne pas
renommer ce proxy en PBO complet. La cible Research OS impose point-in-time,
univers sans survivorship, corporate actions, purging/embargo, coûts/spread/
slippage, contrôle de multiplicité, intervalles bootstrap, segmentation de
régime et calibration Brier/log-loss. Toute probabilité non calibrée reste un
score ou une fréquence descriptive.

### IA

L'IA n'accède jamais aux secrets, ne calcule jamais prix/Greeks/score/verdict et
ne choisit jamais une source silencieusement. Entrée et sortie sont des schémas
versionnés. Chaque phrase factuelle référence un champ du packet ; toute
interprétation est étiquetée ; toute contradiction est conservée.

## Intégrations

### IBKR

Garder une seule session propriétaire par rôle, des client IDs non conflictuels,
un scheduler de pacing, coalescence `singleflight`, cache stale-while-revalidate,
replay anonymisé et circuit breaker. IBKR reste source primaire pour cotations,
chaînes, positions et P&L lorsque l'entitlement le permet. Aucun objet `IB` brut
n'est exposé à l'UI et aucune méthode d'ordre n'entre dans la façade.

### TradingView

TradingView sert aux alertes et au contexte graphique, pas de broker ni de
source canonique. Le récepteur doit accuser réception en moins de trois
secondes, mettre en file le traitement, vérifier secret/certificat, taille et
schéma, dédupliquer par event ID, journaliser la livraison et ne jamais convertir
un webhook en ordre.

### Sources institutionnelles

Adopter SEC EDGAR/XBRL, FRED/ALFRED, BLS et calendriers officiels ; CFTC COT de
façon ciblée. Les données de marché Cboe servent à validation/market statistics
selon licence. Yahoo/Stooq restent des replis explicitement différés, jamais la
preuve canonique d'un historique fondamental.

## Sécurité, fiabilité et exploitation

Risques à corriger : parsing XML RSS par `minidom` sur contenu externe,
authentification optionnelle, exposition `0.0.0.0` possible avec `PORT` ou
`VERTEX_LAN=1`, secrets de webhook, HTML/JS fortement construit par chaînes et
dépendances non verrouillées. Mesures : `defusedxml`, authentification forte
par défaut hors localhost, CSRF sur écritures, CSP avec nonce, cookies sécurisés,
rate limiting, limites de payload, proxy de confiance explicite, journal sans
PII/secrets, lock reproductible et SBOM.

Le frontend ne doit pas être réécrit en bloc. Extraire progressivement templates,
modules de page et styles depuis les chaînes Python. Utiliser les schémas JSON
canoniques, un client fetch borné/annulable, états chargement/vide/dégradé/erreur,
tests Playwright desktop/mobile, axe, clavier et reduced-motion.

## Qualité cible

- Ruff sur le code modifié puis budget décroissant par domaine ;
- types sur modèles, providers et décisions ;
- propriété unique des routes et suppression de la collision anomalies ;
- aucune fonction d'orchestration critique CC > 20 ;
- property tests et golden vectors pour pricing/risque ;
- mutation tests sur hard gates et no-orders ;
- contrats/replays pour chaque provider ;
- p95, taux d'erreur, fraîcheur et hit ratio cache observables ;
- Playwright des huit espaces et matrice mobile ;
- lock, audit dépendances, SBOM et secret scan ;
- preuve complète toujours attachée au même SHA.

## Ordre d'exécution recommandé

1. Stabiliser et intégrer la pile #793–#808 dans son ordre réel.
2. Fermer le blocage `/api/ticker` par snapshots asynchrones bornés.
3. Clore G5 et le replay IBKR sans jamais relâcher `readonly=True`.
4. Généraliser le store point-in-time et l'identité instrument.
5. SEC/FRED/BLS/calendriers officiels, puis ETF metadata/holdings.
6. Unifier options pricing, chaînes, événements et contrats 120–240 DTE.
7. Construire Research OS puis Portfolio Intelligence.
8. Recomposer les pages sur les propriétaires canoniques.
9. Soumettre le profil V5 à décision humaine ; ne jamais modifier V4 en place.
10. Réduire dette, branches et archives après preuve de non-consommation.

## Définition de Vertex 2.0 réussi

Vertex 2.0 n'est pas « le plus de fonctionnalités possible ». C'est une
décision reproductible, datée, sourcée et falsifiable ; une perte bornée ; une
incertitude visible ; une comparaison honnête hors échantillon ; une UI qui
répond vite même quand une source tombe ; et l'impossibilité structurelle de
transmettre un ordre.
