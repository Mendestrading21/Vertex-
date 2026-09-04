# Vertex — protection anti-rafale du rescan

## Objectif

`GET` et `POST /api/rescan` restent disponibles pour conserver la compatibilité avec les commandes et interfaces existantes. Le déclencheur accepte toutefois une seule demande globale toutes les 30 secondes par défaut. Cette fenêtre ne dépend ni d’une adresse IP, ni d’un compte, ni d’un identifiant ou du contenu de la requête.

> Cette protection ne réalise aucune opération de marché. Elle empêche uniquement que des rafraîchissements répétés réveillent inutilement le cycle analytique et provoquent des appels concurrents aux sources de données.

## Contrat HTTP

| Cas | Code | Réponse compacte | Effet sur le scan |
|---|---:|---|---|
| Première demande après la fenêtre | `200` | `ok=true`, `status=rescan_queued`, `cooldown_seconds` | Le signal de réveil est posé ; la boucle de fond fait le travail. |
| Demande pendant la fenêtre | `429` | `ok=false`, `error=rescan_rate_limited`, `retry_after` | Aucun second réveil n’est produit. Le dernier état de scan reste servi. |

L’en-tête HTTP `Retry-After` reprend la valeur entière de `retry_after`. Le compteur exposé par `GET /scan` sous `rescan_cooldown_remaining` est strictement global et descriptif ; il ne permet pas d’identifier un demandeur.

## Paramétrage et garanties

La variable d’environnement `VERTEX_RESCAN_COOLDOWN_SEC` règle la durée en secondes, avec une borne plancher d’une seconde. En l’absence de variable, Vertex utilise 30 secondes. La limite complète le verrou single-flight : la première limite réduit les réveils inutiles, le second empêche tout téléchargement global concurrent si un scan est déjà en cours.

La réponse de rejet ne contient ni exception, ni adresse, ni identité, ni jeton. La couche de présentation doit afficher ce cas comme un état technique temporaire, jamais comme un signal, un verdict ou une instruction d’exécution.
