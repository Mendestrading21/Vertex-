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

Le navigateur s'ouvre sur <http://localhost:5002>. Au premier lancement,
l'installation des dépendances peut prendre quelques minutes.

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

## Si Vertex ne démarre pas

- Installer Python 3.12 ou une version compatible et cocher **Add Python to PATH** sous Windows.
- Attendre quelques secondes, puis ouvrir manuellement <http://localhost:5002>.
- Si le port est occupé, fermer l'autre instance ou définir un autre `PORT`.
- Pour recréer l'environnement local, supprimer uniquement `.venv`, puis relancer le lanceur.
- Consulter `/healthz` et la console du terminal avant de modifier le code.

Vertex fournit une analyse éducative et probabiliste. Il ne garantit aucune
performance et ne remplace pas une décision humaine.
