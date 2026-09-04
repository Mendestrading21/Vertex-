# Vertex — intégrité et bornes des webhooks de signaux

## Garanties appliquées

Les webhooks TradingView restent une source d’information uniquement. Un signal accepté crée une action `REEVALUATE`; il ne peut jamais créer, transmettre ou exécuter un ordre.

| Contrôle | Valeur | Effet de sécurité |
|---|---:|---|
| Secret | comparaison constante | Refuse les payloads non authentifiés avant l’ajout au store. |
| Fenêtre anti-replay | 15 minutes | Refuse les événements trop anciens et les timestamps futurs incohérents. |
| Déduplication | 10 minutes | Refuse le même couple symbole/signal dans la fenêtre définie. |
| Cadence globale | 30 livraisons / 60 secondes | Répond `429 webhook_rate_limited` sans stocker IP, user-agent ou contenu client. |
| Structure reçue | 32 champs au maximum | Répond `400 webhook_payload_invalid` avant la validation analytique. |
| Payload persistant | 12 champs plats, 256 caractères par chaîne | Écarte les objets/listes et ne conserve jamais le secret. |

## Principes de confidentialité

Le limiteur de cadence ne conserve qu’une liste bornée d’horodatages serveur. Il ne stocke aucune identité d’émetteur. Les payloads sont normalisés : les champs de contexte `price`, `volume`, `timeframe`, `strategy`, `note` et `exchange` sont conservés en priorité si présents, puis les autres champs primitifs jusqu’à la limite.

> Une réponse `webhook_rate_limited` ou `webhook_payload_invalid` indique une protection de transport. Elle ne constitue ni une recommandation ni une invalidation d’analyse de marché.
