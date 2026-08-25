"""vertex/app/origine.py — UNE PAGE TIERCE N'ÉCRIT PAS DANS TON BUREAU.

## Le défaut, démontré le 25 août 2026

Vertex tourne en local pendant que l'utilisateur navigue. Toute page visitée
peut faire émettre à son navigateur un POST vers `http://localhost:5002` — une
requête *simple*, donc **sans preflight CORS**, à condition d'utiliser un
`Content-Type` autorisé comme `text/plain`.

Or `/api/desk` lit son corps avec `request.get_json(force=True)` : `force`
**ignore le `Content-Type`**. Mesuré, sur le vrai produit :

```text
POST /api/desk  Content-Type: text/plain
                Origin: https://site-malveillant.example
-> 200 {'ok': True, ...}   et l'ecriture a bien eu lieu
```

Quatorze routes `POST` existent. Rien ne vérifiait l'origine.

## Ce qui limitait déjà les dégâts, et ce qui ne les limitait pas

Le correctif du lot 362 empêche un push partiel d'effacer les clés absentes, et
un instantané `desk_avantperte_*.json` est pris avant écriture : les données
existantes ne sont **pas détruites**, et il existe un point de retour.

Ce qui restait possible : **injecter**. Un faux trade, une fausse entrée de
journal, une fausse thèse — dans le registre même qui sert à juger les
décisions passées. Une corruption discrète du journal vaut mieux qu'une
destruction bruyante pour qui veut nuire.

## Pourquoi l'origine, et pas un jeton CSRF

Un jeton exige une session ; or **sans `VERTEX_CODE` il n'y a pas de session**,
et c'est justement la configuration par défaut. `SESSION_COOKIE_SAMESITE='Lax'`
protège le cookie — mais protéger un cookie qui n'existe pas ne protège rien.

Le navigateur, lui, **envoie toujours `Origin` sur une requête cross-origin**.
Le comparer à l'hôte servi est la protection exacte pour une application
locale, sans dépendance ni état.

## Pourquoi une requête SANS `Origin` est acceptée

`curl`, les bancs de test et les appels serveur-à-serveur n'en envoient pas. Un
navigateur, lui, ne peut pas l'omettre sur un POST cross-origin : l'absence
d'`Origin` n'est donc pas un contournement de la protection contre le CSRF —
c'est la marque d'un client qui n'est pas une page web.
"""
from __future__ import annotations

#: Méthodes qui MODIFIENT. `GET` et `HEAD` ne sont jamais bloqués : la
#: protection viserait alors la simple consultation, et casserait les liens.
METHODES_ECRITURE = frozenset({'POST', 'PUT', 'PATCH', 'DELETE'})


def _hote(valeur: str) -> str:
    """`https://exemple.com:443/x` -> `exemple.com:443`. Vide si illisible."""
    v = str(valeur or '').strip()
    if not v:
        return ''
    sans_schema = v.split('://', 1)[-1]
    return sans_schema.split('/', 1)[0].lower()


def origine_etrangere(*, methode: str, origine: str, hote_servi: str) -> bool:
    """Cette écriture vient-elle d'une AUTRE origine que celle servie ?

    Rend `False` — donc autorise — quand :

    - la méthode ne modifie rien ;
    - aucune `Origin` n'est envoyée (client non navigateur, voir le docstring
      du module) ;
    - l'origine correspond à l'hôte servi.

    Le port fait partie de l'identité : `localhost:5002` et `localhost:9999`
    sont deux origines différentes pour le navigateur, et les confondre
    rouvrirait la porte à une autre application locale.
    """
    if str(methode or '').upper() not in METHODES_ECRITURE:
        return False
    o = _hote(origine)
    if not o:
        return False
    return o != _hote(hote_servi)
