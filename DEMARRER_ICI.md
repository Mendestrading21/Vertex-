# ▲ VERTEX — Démarrer ici

Vertex est un terminal d'analyse local. Il lit les données et positions, mais ne
passe **jamais** d'ordre.

## Lancer en un clic

### Windows

Double-cliquer sur `Lancer_VERTEX.bat`. Pour découvrir l'interface sans TWS,
utiliser `Lancer_VERTEX_DEMO.bat`.

### macOS

Double-cliquer sur `Lancer_VERTEX.command`. La première fois, macOS peut demander
un clic droit puis **Ouvrir**. Pour le mode hors ligne, utiliser
`Lancer_VERTEX_DEMO.command`.

**Garde la fenêtre noire ouverte.** Le navigateur s'ouvre **tout seul** sur
<http://localhost:5002> **dès que le serveur est prêt** (le lanceur attend qu'il
réponde — plus de « site inaccessible » dû à un navigateur ouvert trop tôt). Au
premier lancement, l'installation des dépendances peut prendre 1 à 2 minutes.

## Mode démo

Le mode `DEMO=1 NO_IBKR=1` sert aux contrôles visuels et au développement hors
ligne. Toute donnée synthétique doit rester explicitement marquée **DÉMO**.

## Données réelles via IBKR

1. Ouvrir TWS ou IB Gateway.
2. Dans **Configuration globale → API → Settings**, activer les clients socket.
3. Activer impérativement **Read-Only API**.
4. Utiliser `127.0.0.1` comme IP de confiance.
5. Vérifier le port : TWS `7496/7497`, Gateway `4001/4002`.
6. Lancer `Lancer_VERTEX` et contrôler le statut dans **Système**.

Les statuts LIVE, DELAYED, STALE, FALLBACK et OFFLINE reflètent l'état réel de la
connexion. Une donnée absente reste absente ; Vertex ne la remplace pas par un
chiffre inventé.

## Accès depuis un téléphone ou une tablette

Par défaut, Vertex reste accessible uniquement sur l'ordinateur. Pour l'ouvrir sur
le réseau local :

1. copier `.env.example` vers `.env` ;
2. définir `VERTEX_CODE` avec un code privé ;
3. relancer Vertex ;
4. ouvrir `http://<IP-locale>:5002` depuis le même Wi-Fi.

Ne jamais publier `.env`, `.vertex_secret` ou une capture contenant un identifiant
de compte.

## Où trouver quoi

- **Briefing** : situation du jour et marchés.
- **Opportunités** : dossiers qui méritent une analyse.
- **Portefeuille** : positions, risque et watchlist.
- **Analyse** : dossier complet d'un titre.
- **Options** : convexité, volatilité, scénarios et événements.
- **Performance** : journal et mesure de la méthode.
- **Intelligence** : raisonnement, comité et mémoire.
- **Système** : connexions, données, automatisations et réglages.

## Si Vertex ne démarre pas / « site inaccessible »

- **Le navigateur s'ouvre automatiquement une fois le serveur prêt** (~10 à 30 s,
  plus au 1er lancement). Si tu ouvres la page toi-même trop tôt, **rafraîchis**
  <http://localhost:5002> après quelques secondes — ce n'est pas cassé, ça démarre.
- **Garde la fenêtre noire (terminal) OUVERTE** tant que tu utilises Vertex :
  la fermer arrête le serveur.
- **Python manquant** : installer Python 3.12 (ou compatible) et cocher
  **Add Python to PATH** sous Windows, puis relancer le lanceur.
- **Bon dossier / bonne version** : vérifier que tu es sur la branche
  `integration/vertex-v4-clean` (`git checkout integration/vertex-v4-clean`
  puis `git pull`) avant de double-cliquer le lanceur.
- **Échec d'installation** : les erreurs pip s'affichent désormais dans la
  fenêtre — les lire ; souvent il suffit de relancer (réseau) ou de mettre à
  jour Python.
- **Port occupé** : fermer l'autre instance de Vertex, ou définir un autre `PORT`.
- Pour recréer l'environnement local, supprimer uniquement `.venv`, puis relancer.
- Consulter `/healthz` et la console du terminal avant de modifier le code.

Vertex fournit une analyse éducative et probabiliste. Il ne garantit aucune
performance et ne remplace pas une décision humaine.
