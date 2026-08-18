# SIGNAL OS · LOT 48 — LES ÉTATS CONDITIONNELS, ET UN CLASSIFIEUR QUI SE TROMPAIT

Branche : `agent/vertex-signal-os-v1` · SW **v235** (aucun octet servi touché)

La même réserve revenait dans **trois** rapports — 41 §6.1, 46 §4.3, 47 §5.1 :

> Les états conditionnels (tiroir ouvert, bandeau d'erreur, watchlist remplie)
> restent hors du relevé navigateur.

Une réserve qui revient trois fois est une dette, pas une nuance.

---

## 1. Le verdict

Les trois états sont atteints, et la sonde du lot 47 y passe :

```text
watchlist remplie        atteint ·  2 pictogrammes peints
menu d'entite ouvert     atteint ·  2 pictogrammes peints
bandeau d'erreur         atteint ·  3 pictogrammes peints

AUCUN EMOJI PEINT DANS LES ETATS CONDITIONNELS.
```

Quatre signes peints, tous monochromes : `⚠` (×6), `→` (×5), `⌘` (×3),
`↗` (×1).

---

## 2. Trois montages faux avant le bon — et ils se ressemblent

### 2.1 Le service worker répondait à ma place

Premier jet : coupure totale des points de données, et l'écran affichait
« **Analyse à jour** ». Je mesurais un **cache**, pas une dégradation : sans
`service_workers='block'`, le SW sert sa copie et la panne simulée n'atteint
jamais la page. `mesurer_degradation.py` bloquait déjà le SW ; je ne l'avais pas
repris.

### 2.2 Le magasin n'est pas le chemin du produit

Pour remplir la watchlist, j'écrivais `myFavs` dans `localStorage` avant le
chargement. Mesure : la clé revenait à `[]`. **L'hydratation de démarrage
rapatrie le blob du serveur et écrase ce qui a été posé avant elle.** Le chemin
du produit est `VXEntities.toggleFavorite` — la fonction qu'appelle « Ajouter
aux favoris ».

### 2.3 Une attente fixe transforme une course en tirage au sort

Même avec la bonne fonction, l'état paraissait tantôt atteint, tantôt non. Cause
mesurée : à 3,5 s le geste passait, puis l'hydratation arrivait **ensuite** et
l'effaçait. L'outil repose donc le geste jusqu'à ce qu'il tienne, et renonce
franchement s'il ne tient jamais.

Le point commun des trois : **je ne reproduisais pas le chemin réel du
produit.** C'est la leçon du lot 38, pour la troisième fois, sous trois
déguisements de plus.

---

## 3. Le classifieur portait le jumeau du défaut qu'il traque

Une fois les trois états atteints, l'outil a accusé `⚠` — **6 emoji peints**
dans le bandeau d'erreur.

Vérifié avant de corriger le produit : la page peint `U+26A0` **nu**, sans aucun
`U+FE0F` sur tout l'écran. C'est de la présentation **texte** — monochrome, à la
couleur du texte. Un signe de casseau, comme `→` ou `✕`. La règle ne le vise
pas.

D'où venait l'accusation ? De ceci :

```python
return cp >= 0x1F300 or ch in '✅❌⚠️🔴🟠🟡🟢'
```

Cette chaîne contient `⚠` **suivi** de `U+FE0F`. Parcourue caractère par
caractère, elle rend le `⚠` **nu** membre de l'ensemble. Le classifieur
confondait donc `⚠` et `⚠️`.

**C'est exactement la faute corrigée dans le produit au lot 41** — `sev === '🔴'`
cassé par un sélecteur de variante. Mon instrument portait le jumeau du défaut
qu'il sert à traquer, et il a fallu qu'il accuse à tort pour que je le voie.

La règle est désormais celle d'Unicode, pas une liste de goût :

| cas | verdict |
| --- | --- |
| plan astral (≥ U+1F300) | emoji — multicolore par nature |
| BMP à présentation emoji par défaut (`✅`, `❌`, `⭐`…) | emoji |
| BMP suivi de `U+FE0F` | emoji — la couleur est demandée |
| BMP nu (`⚠`, `→`, `✕`, `◇`) | **signe** |

La sonde relève donc la **séquence**, pas le caractère isolé. Contrôle
unitaire : `⚠`→signe, `⚠️`→emoji, `✅`→emoji, `🔴`→emoji, `→`/`◇`/`✕`→signes.

---

## 4. Ce qui reste ouvert

1. **Trois états, pas tous.** Le tiroir du comparateur d'options, la modale
   d'import et le formulaire de journal ne sont pas parcourus.
2. **Le survol et le focus** ne sont pas mesurés : la sonde lit l'état au repos.
3. **Une image de fond** portant un pictogramme dessiné échapperait encore aux
   deux organes de la sonde.
