# IBKR — données de marché uniquement

## Contrat

IBKR est un fournisseur de marché, pas une source de patrimoine. Vertex peut
ouvrir une session TWS/IB Gateway en `readonly=True` seulement pour obtenir des
données de marché autorisées.

### Autorisé

- qualification et identité des contrats ;
- bid, ask, last, close, mark et tailles disponibles ;
- chandeliers et historiques ;
- état et type de marché live/delayed/frozen ;
- chaînes d'options, expirations et strikes ;
- volume, open interest, IV et model Greeks disponibles ;
- métadonnées de source, entitlement, timestamp, latence et pacing.

### Interdit

- identifiant, nom ou liste de comptes ;
- `managedAccounts`, `accountSummary`, valeurs de compte, cash, NAV ou marge ;
- `positions`, `portfolio`, positions multi-comptes ou coût de revient broker ;
- `reqPnL`, `reqPnLSingle`, P&L journalier/réalisé/non réalisé ;
- ordres ouverts, historique d'ordres, exécutions et commissions personnelles ;
- transactions, transferts, relevés ou données fiscales ;
- rapprochement automatique entre compte IBKR et portefeuille Vertex.

L'interdiction vaut même si une méthode est techniquement en lecture seule.
`readonly=True` empêche l'ordre ; il ne protège pas la confidentialité du
compte.

## Migration obligatoire

1. Inventorier appels directs, wrappers, workers, routes, caches, tests, docs et
   champs UI liés aux données de compte.
2. Ajouter d'abord un gardien qui échoue sur les appels interdits dans le code
   produit, avec allowlist temporaire documentée pour la migration.
3. Créer ou consolider une façade `MarketDataGateway` n'exposant que les
   méthodes autorisées.
4. Remplacer la dépendance aux positions broker par les positions déclarées du
   desk ; obtenir les cotes par symbole/contrat, jamais par compte.
5. Retirer routes de compte, réconciliation P&L broker, caches, variables de
   configuration et textes associés après migration de leurs consommateurs.
6. Supprimer toute donnée de compte déjà persistée en suivant une migration
   réversible, sans écrire ni afficher son contenu dans les logs.
7. Rejouer mode sans IBKR, delayed, frozen, entitlement partiel, timeout,
   reconnexion et fermeture de TWS.

## Configuration cible

- aucun `IBKR_ACCOUNT_ID` requis ;
- client IDs techniques dédiés aux flux de marché seulement ;
- connexion depuis le backend local, jamais le navigateur ;
- secrets et paramètres sensibles hors Git ;
- statuts basés sur une preuve de socket et la fraîcheur, pas un flag ;
- la page Système affiche `IBKR — données de marché`, jamais `compte connecté`.

## États UI

`LIVE`, `DELAYED`, `FROZEN`, `STALE`, `PARTIAL`, `OFFLINE`, `ERROR`,
`ENTITLEMENT_MISSING`. Chaque widget conserve source et âge. Une absence de
donnée de marché n'affecte jamais la position manuelle ; elle affecte seulement
sa valorisation estimée.

## Garde-fous

- test statique des symboles interdits dans production Python/JS ;
- test de la surface publique du gateway ;
- test qu'aucun endpoint ne renvoie compte, cash, position broker ou P&L ;
- test qu'aucun prompt Claude ne reçoit une donnée de compte ;
- test que logs, captures et télémétrie ne contiennent pas d'identifiant ;
- test que le portefeuille fonctionne avec `NO_IBKR=1` ;
- test que l'activation IBKR enrichit les cotes mais ne crée, ferme ou modifie
  aucune position.

Le lot n'est terminé qu'après disparition de l'allowlist temporaire.
