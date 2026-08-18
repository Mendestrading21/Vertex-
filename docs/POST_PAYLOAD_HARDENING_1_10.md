# Vertex — durcissement des payloads POST 1.10

## Routes couvertes

Les routes analytiques `POST /api/options/analyze`, `POST /api/planning/ticket` et `POST /api/pretrade/check` vérifient désormais la forme de leur JSON avant toute analyse. Les payloads doivent être des objets, restent limités en nombre de champs et ne peuvent contenir de nombres non finis ou hors borne.

| Route | Limites structurelles | Rejet explicite |
|---|---|---|
| `/api/options/analyze` | au plus 8 champs, 1 à 16 jambes objet | JSON non objet, jambes absentes/hors borne, nom trop long, spot/IV/jours invalides |
| `/api/planning/ticket` | au plus 18 champs | symbole invalide, prix, budget ou risque non fini/hors borne |
| `/api/pretrade/check` | au plus 12 champs | symbole invalide ou montant non fini/hors borne |

Les échecs de validation retournent `400` et un code d’erreur compact. Ils ne deviennent pas une note de marché, un calcul partiel ou une instruction transactionnelle.

> Cette couche protège les calculs descriptifs ; elle ne transmet pas d’ordre, ne contacte pas de courtier et ne modifie aucune position.
