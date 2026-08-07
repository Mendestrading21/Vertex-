# 🔒 Sécuriser l'accès à VERTEX

VERTEX peut être protégé par un **code d'entrée**. Tant que le code n'est pas
saisi, aucune page ni donnée n'est accessible. C'est activé par **une variable
d'environnement** — jamais écrit dans le code (donc jamais visible sur GitHub).

## Activer le verrou

Il suffit de définir la variable **`VERTEX_CODE`** avec ton mot de passe.

### Sur Render (le site en ligne / mobile)
1. Ouvre ton service sur **render.com** → onglet **Environment**.
2. **Add Environment Variable** :
   - Key : `VERTEX_CODE`  ·  Value : *ton mot de passe*
   - (recommandé) Key : `VERTEX_SECRET`  ·  Value : *une longue chaîne aléatoire*
3. **Save** → Render redéploie tout seul. L'app demande désormais le code.

### En local (sur ton ordinateur)
1. Copie `.env.example` en **`.env`**.
2. Mets dedans :
   ```
   VERTEX_CODE=TonMotDePasse
   VERTEX_SECRET=une-longue-chaine-aleatoire
   ```
3. Lance l'app normalement — le `.env` est chargé automatiquement.
   > `.env` est dans `.gitignore` : il n'est **jamais** envoyé sur GitHub.

## Désactiver le verrou
Supprime la variable `VERTEX_CODE` (ou laisse-la vide). L'app ne demande
plus de code — **et par sécurité, sans code, le serveur n'écoute plus que
`127.0.0.1`** (plus d'accès depuis le WiFi/LAN, sauf `VERTEX_LAN=1` posé
en connaissance de cause).

## Comment ça marche
- Session par **cookie signé** (httponly, SameSite=Lax), valable **30 jours** :
  tu entres le code une fois par appareil.
- **Anti-force-brute** : après 5 essais ratés, blocage progressif par IP (jusqu'à 5 min).
- Comparaison du code à **temps constant** (pas de fuite d'information).
- Pour verrouiller un appareil : visiter **`/logout`** (la session du
  cookie est révoquée, le code sera redemandé).
- Pages publiques (pas de code requis) : `/login`, `/logout`, `/healthz`,
  `/api/healthz`, favicon, manifeste, service worker, et le webhook
  TradingView (qui porte sa propre authentification par secret signé).

## Conseils
- Choisis un mot de passe **long et pas évident** (évite les noms + 123).
- Mets un **`VERTEX_SECRET`** aléatoire : ça protège les sessions même si le code change.
- Ne partage jamais ton `.env`. Pour changer le mot de passe : change `VERTEX_CODE` et redéploie.
