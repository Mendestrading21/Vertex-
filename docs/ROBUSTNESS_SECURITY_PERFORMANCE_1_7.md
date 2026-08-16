# Vertex — robustesse, sécurité et performance 1.7

## Persistance résiliente

Les caches JSON analytiques sont désormais écrits dans un fichier temporaire du même répertoire, synchronisés, puis substitués atomiquement. Une erreur pendant la sérialisation ou l’écriture ne remplace donc pas le dernier cache valide. Les écritures demeurent non bloquantes pour une analyse : l’application rend un résultat prudent plutôt qu’une erreur de persistance.

| Protection | Comportement |
|---|---|
| Validation de chemin | Un nom de cache ne peut pas sortir de la racine Vertex. |
| Plafond de lecture | Un cache de plus de 32 Mio est ignoré et renvoie la valeur de repli. |
| Écriture atomique | Le cache précédent survit à une interruption ou une écriture partielle. |
| Lecture mémorisée | Les lectures identiques sont servies depuis un cache mémoire borné à 64 entrées ; une empreinte de contenu invalide le cache lorsqu’un fichier est réécrit localement, même très rapidement et à taille égale. |
| Isolation | Chaque lecture renvoie une copie profonde afin qu’un appelant ne modifie pas le cache partagé. |

## Observabilité non sensible

`GET /api/skyler/health` expose uniquement les compteurs de persistance : lectures, échecs, écritures, hits/misses de cache et occupation mémoire. Il ne retourne ni chemin local, ni nom de fichier, ni contenu de cache, ni donnée utilisateur.

## Limites

Cette itération sécurise le cache local et les parcours de lecture. Elle ne transforme pas Vertex en infrastructure de courtage : le système reste sans passage d’ordre, et les caches sont toujours des aides de continuité plutôt qu’une source de vérité de marché.
