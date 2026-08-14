# SKYLER — LOT 616 · LE TEXTE DES GRAPHIQUES, MESURÉ AU LIEU D'ÊTRE RAISONNÉ

Le lot 614 avait changé `VXCharts.colors.muted` **sur un raisonnement**, et
l'avait écrit noir sur blanc :

> « L'argument retenu est un **raisonnement, pas une mesure** : le changement
> éclaircit le texte sur des fonds sombres, il ne peut donc pas dégrader la
> lisibilité. Si un jour un fond de graphique devient clair, cet argument tombe. »

C'est la seule dette que le 614 s'était reconnue. **Ce lot la solde.** Il ne
change aucun octet servi : il transforme une inférence en fait.

## Pourquoi c'était hors de portée

Deux sites peignent ce token **comme texte** :

```js
chart-core.js:445     ctx.fillStyle = C.colors.muted;  ctx.font = '10px …'   // étiquette d'anneau
markets_page.py:722   g.fillStyle = …colors.muted;     g.font  = '9px …'    // étiquettes d'axe
```

Un `<canvas>` n'expose **aucun nœud de texte**. Les deux méthodes du 613 sont
inopérantes : la composition CSS n'a rien à composer, et il n'existe pas de
boîte à échantillonner. **Seuls les pixels peints existent.**

## Le premier banc a été vide, et il l'a dit

Sonder **l'intérieur entier** de chaque canvas donnait des parts de dominante de
**17 % à 41 %** — sous le seuil de fiabilité de 55 % établi aux lots 613/614.
Les 4 canvas ont été **écartés**, et le banc a rendu « aucun échantillon
fiable ». C'est le comportement correct : *l'intérieur d'un graphique n'est pas
un fond, c'est un dessin.*

## Le second banc sonde là où le texte est peint

Trois régions par canvas — **centre de l'anneau** (`chart-core.js` peint son
étiquette à `meta.data[0].{x,y}`, le centre du donut), **bande d'axes**,
**bande haute** :

| | régions |
| --- | --- |
| sondées | **12** |
| **retenues** *(part de dominante 59 % à 84 %)* | **5** |
| écartées faute de signal *(8 % à 49 %)* | **7** |

| couleur peinte | pire ratio sur fond retenu | seuil |
| --- | --- | --- |
| `colors.muted` *(9 px et 10 px)* | **6,16** | 4,5 |
| `colors.text` | **9,89** | 4,5 |

Fonds réellement échantillonnés : de **(6, 6, 7)** à **(14, 15, 15)** — la plage
des surfaces de carte du produit, ce qui **confirme que les canvas sont
transparents** et laissent voir la carte.

**Le raisonnement du 614 est confirmé par la mesure.** Aucune correction.

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « aucune méthode DOM ne peut voir ce texte » | **CONFIRMÉ** — il a fallu lire des pixels |
| **(b)** | « l'intérieur d'un canvas est un fond échantillonnable » | **RÉFUTÉ** — 17 % à 41 % de dominante ; c'est un dessin |
| **(c)** | « le raisonnement du 614 tient » | **CONFIRMÉ** — 6,16 au pire, marge +1,66 |
| **(d)** | « les canvas sont transparents et montrent la carte » | **CONFIRMÉ** — fonds (6,6,7) à (14,15,15) |

## Un faux positif de mon propre gardien

En écrivant le test qui vérifie qu'aucun `<canvas>` ne peint un fond clair,
j'ai cherché les blocs CSS avec `canvas[^{}]*\{`. Il a signalé un
`radial-gradient(…, rgba(255,255,255,.010), …)` comme **fond clair de canvas**.

**Faux** : la regex partait d'un `--vx-canvas` référencé dans une déclaration
précédente et courait jusqu'à l'accolade suivante — le bloc ne visait aucun
`<canvas>`. Corrigé en découpant les blocs `sélecteur { déclarations }` et en
exigeant `canvas` comme **jeton de sélecteur**.

*Chercher une sous-chaîne dans du CSS n'est pas lire un sélecteur* — même
famille que le faux du 615 (compter une chaîne dans des octets servis n'est pas
mesurer un attribut rendu).

## Le seul canvas qui peint un fond

`#op-scatter canvas{background:rgba(0,0,0,.14)}` — du **noir transparent**. Il
ne peut qu'**assombrir**, donc qu'augmenter le contraste d'un texte clair. Le
modèle tient ; un fond **clair** le casserait sans qu'aucun test de token ne
bouge, et c'est exactement ce que le quatrième test garde.

## Ce que le lot n'établit pas

- **Que les 5 régions retenues couvrent tout le texte des graphiques.** Elles
  couvrent les fonds *là où j'ai su regarder* — 7 régions sur 12 restent sans
  verdict, et je ne conclus **ni** qu'elles sont conformes **ni** qu'elles ne le
  sont pas.
- **Le texte peint par-dessus une série colorée.** Le pourcentage central du
  donut est peint dans la **couleur de son arc** (19 px gras) : mesuré nulle
  part. Si un jour une étiquette passe **sur** un arc clair, la mesure de ce lot
  ne dit rien de ce cas.
- **Les infobulles de graphique** (rendues par Chart.js, hors de nos couleurs).
- **Les autres largeurs** : mesure faite à 1440 px uniquement.

## Règles neuves

- **616-A — UN INSTRUMENT QUI REND « AUCUN SIGNAL » A FONCTIONNÉ.** Le premier
  banc n'a rien conclu et c'était juste : l'intérieur d'un graphique n'est pas un
  fond. Le réflexe d'abaisser le seuil pour « obtenir un résultat » aurait
  produit un chiffre calculé sur un dessin.
- **616-B — CHERCHER UNE SOUS-CHAÎNE DANS DU CSS N'EST PAS LIRE UN SÉLECTEUR.**
  `--vx-canvas` a fait passer un test pour un défaut. Suite directe du 615-A :
  *la forme du texte n'est pas la structure qu'il décrit.*
- **616-C — UNE DETTE QU'ON S'EST RECONNUE DOIT ÊTRE SOLDÉE, PAS SEULEMENT
  DOCUMENTÉE.** Le 614 avait écrit « raisonnement, pas mesure » ; c'était
  honnête, mais l'honnêteté ne remplace pas la mesure. **Deux lots plus tard,
  la dette est payée** — et elle aurait pu ne jamais l'être si elle n'avait pas
  été écrite.

## Ce que le dépôt fait bien

- **Les canvas sont transparents**, donc le texte des graphiques hérite des
  surfaces de carte : le contraste se raisonne au même endroit que le reste.
- **Le seul fond de canvas est du noir transparent** — un choix qui va dans le
  sens de la lisibilité, pas contre elle.
- **`chart-core.js` centralise ses couleurs** (`C.colors`) : deux sites de
  peinture, un seul réglage. C'est ce qui a rendu le lot 614 possible en une
  ligne.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **0 fichier de production** — **aucun octet servi n'a changé**, donc **aucun
  bump de service worker** : il n'y avait rien à purger. Vérifié, pas supposé.
- **1 gardien neuf** (4 tests, **6 mutations rouges** — dont « un canvas peint
  un fond clair » et « le site de peinture repointé sur une autre couleur »).
- MD5 des 8 pages : **8 / 8 identiques**.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2923 passed / 0 skipped** *(2919 + les 4 du gardien neuf)*.
- Navigateur : **16 chargements** (8 pages × 2 bancs), **12 régions sondées**.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **251** *(+1 : un `radial-gradient` clair signalé
  comme fond de canvas — la regex partait d'un `--vx-canvas`)*
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 12** *(inchangé — ce lot ne corrige rien, il
  solde une dette de mesure)*
