# SKYLER — LOT 588

## Ce que le lot établit

**Le produit compare deux grandeurs plus souvent qu'il ne dessine : 49 contre
26.** Mon attente disait l'inverse — je pensais que la géométrie dominerait,
parce que les droites les plus fréquentes relevées au 587 étaient `a.right`,
`a.left`, `a.top`, `a.bottom`. **Elle arrive troisième en part, derrière les
comparaisons de marché.**

Et le brief proposait **trois** familles. La lecture en impose une **quatrième**
qu'il ne nommait pas : **BORNE DE BOUCLE** — 23 sites, 21 %.

## Le choix (hhh)

Le 587 avait écrit : « elles n'ont pas été lues, seulement comptées. C'est la
dette que ce lot ouvre à son tour. » **36 % de toutes les comparaisons de seuil
du produit**, que six lots d'affilée n'avaient jamais regardées.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

| piège | verdict |
| --- | --- |
| **Attente principale** — la GÉOMÉTRIE domine | **RÉFUTÉE** : géométrie **26 (24 %)**, derrière **DEUX GRANDEURS 49 (45 %)** |
| **Contre-piège 1 (587-B)** — « ce dépôt juge plus qu'il ne dessine » | **CONFIRMÉ une seconde fois**, sur un jeu de sites entièrement différent |
| **Contre-piège 2 (587-A)** — recalculer le 108 avant de s'en servir | **reproduit à l'identique : 108** (2 680 bruts → dédupliqués → tiers retirés) |

## Les 108, lues par famille

| famille | sites | part |
| --- | --- | --- |
| **DEUX GRANDEURS** — une comparaison de marché ou de portefeuille | **49** | **45 %** |
| **GÉOMÉTRIE** — coordonnées de dessin | **26** | 24 % |
| **BORNE DE BOUCLE** — *absente du brief* | **23** | 21 % |
| **GRANDEUR / RÉGLAGE** — filtre, constante, limite configurée | **10** | 9 % |
| non tranché | **0** | — |

Couverture **108/108**, **98 couples distincts** tous déclarés.

### Les 49 « deux grandeurs », par page

`/portfolio` 8 · `chart-core.js` 6 · `options-gex.js` 5 · `/analysis/AAPL` 4 ·
`/markets` 4 · `/journal` 3 · `/opportunities` 3 · `candlestick-lwc.js` 3 ·
`options-structure.js` 3 · `vx-entities.js` 3 · `candlestick-chart.js` 2 ·
`options-intel.js` 2 · `/system` 2 · `heatmap.js` 1.

### Les 20 qui produisent un libellé ou une couleur — lues

```javascript
sm.beats >= sm.total*0.7   → vx-pos       // /analysis : les surprises de résultats
sm.beats <= sm.total*0.4   → vx-neg
b.points >= b.max*0.66     → vx-pos
bo.adv >= bo.dec           → vx-pos       // /markets : la participation
bo.nh  >= bo.nl            → vx-pos
inter.nh > inter.nl        → vx-pos
inter.nl > inter.nh        → vx-neg
(c.oi||0) > (m.oi||0)      → « OI supérieur »          // /opportunities
mark <= stop               → « cassée » · neg          // /portfolio : la thèse
mark <= stop*1.04          → « fragilisée » · warn
wgt > tr.max*1.5           → vx-warn
_worst <= -15              → « Pire scénario de stress : »
d.n_positions < b.min      → « sous la cible »
r.strike <= g.spot         // options-gex
(calls||0) >= (puts||0)    → « CALLS »
px <= payoff[0].price      // option-payoff : bornes de la courbe
d.ts > localTs             → `vx:data-refreshed`       // vx-entities
recovered >= invested      → « WIN »
server > local             → « mise à jour disponible »  // /system
```

**`mark <= stop` est la comparaison la plus conséquente du relevé** : elle
décide qu'une thèse est **cassée**, et elle ne compare aucun littéral — elle
confronte un prix vivant à un stop saisi par l'utilisateur.

### Cinq comparaisons d'horodatages — un cinquième lieu où la fraîcheur se décide

```javascript
t  <= lastT            // candlestick-chart.js
tk <= lt               // candlestick-lwc.js
d.ts > localTs         // vx-entities.js  → émet `vx:data-refreshed`
localTs > d.ts         // vx-entities.js  → le sens inverse, même fichier
server > local         // /system         → « mise à jour disponible »
```

Les lots 580 et 581 avaient trouvé **quatre** vocabulaires d'état de fraîcheur.
En voici un **cinquième lieu de décision**, qui n'utilise aucun d'eux : il
compare deux horodatages nus et en tire un événement ou une phrase.

## Second contrôle (481) — l'égalité, exclue par la restriction

L'instrument ne relève que les opérateurs d'ordre. Les comparaisons **d'égalité**
sur une grandeur numérique sont pourtant des décisions aussi :

**36 sites de produit**, dont `i===0` ×6 · `_warn===0` ×3 · `i === 0` ×2 ·
`args.index !== 0` ×2 · `i === 5` ×2 · `e.key.length === 1` ×2 ·
`rDown!==0` · `tt.opacity === 0` · `row.length === 0` ·
`url.indexOf(PERSIST_DENY[i]) === 0` · `step === 1` · `step === 2`.

**La grande majorité sont des tests de position ou d'index**, pas des jugements
de marché — mais `_warn===0` et `rDown!==0` en sont, et ils échappaient à six
lots d'instruments.

## L'arrêt du lot — j'ai recopié mes clefs depuis un affichage tronqué

Mon premier classement (`l588_familles.py`) rendait **23 non tranchés**. La
cause n'est pas dans le dépôt : **j'avais écrit mes clefs de classement en
recopiant l'affichage d'un `Counter`, tronqué à 30 caractères**, alors que les
valeurs stockées en font 40. `Math.abs(Number(values[b]) || 0` ne correspondait
donc à rien.

**C'est la règle 574-C** — ne jamais lire une valeur dans un rapport quand la
donnée est disponible — **enfreinte à nouveau, et cette fois mécanisée** : la
troncature était dans mon propre affichage.

Le banc fautif est **conservé tel quel** ; un second a été écrit, partant des
**98 couples distincts réellement stockés**. Résultat : **0 non tranché**.

**Arrêtés avant publication : 214 → 215 (+1).**

## Ce que le lot n'établit pas

- **Que ces 49 comparaisons soient justes.** Elles sont lues et nommées ; aucune
  n'a été confrontée à ce que le serveur produit.
- Que `mark <= stop` se comporte correctement quand `stop` est absent : **non
  mesuré ici** — c'est le prolongement naturel du 586.
- Que les 26 géométries soient sans conséquence : elles n'ont pas été jugées.
- Que les 36 égalités soient toutes techniques : **12 formes distinctes lues**,
  les autres non.

## Limites déclarées

- **226 comparaisons ont une gauche non nommable** (expression composée) et sont
  écartées par **les deux relevés**, le 587 comme le 588. Le relevé reste un
  **plancher** (550-B) — et ce plancher-là n'a jamais été mesuré.
- Le classement porte sur le **couple (gauche, droite)** : deux sites au même
  couple mais d'intention différente seraient rangés ensemble.
- Le corpus reste les 8 pages à leur URL de base + `/analysis/AAPL`.

## Règles neuves

- **588-A — LES FAMILLES QU'UN BRIEF PROPOSE NE COUVRENT PAS FORCÉMENT
  L'ENSEMBLE.** Ici il en manquait une entière (borne de boucle, 21 %). Compter
  les non-tranchés est le seul moyen de s'en apercevoir.
- **588-B — UNE CLEF DE CLASSEMENT SE COPIE DEPUIS LA DONNÉE, JAMAIS DEPUIS SON
  AFFICHAGE.** Un affichage tronque ; une donnée non.
- **588-C — LE PRODUIT COMPARE DEUX GRANDEURS PLUS SOUVENT QU'IL NE DESSINE.**
  49 contre 26 — le 587-B se confirme sur un jeu de sites entièrement différent.

## Ce que le dépôt fait bien

- **Les comparaisons de marché sont écrites en clair** : `bo.adv >= bo.dec`,
  `inter.nh > inter.nl`, `mark <= stop` — on lit l'intention sans commentaire.
- **Les deux sens sont écrits explicitement** (`inter.nh > inter.nl` **et**
  `inter.nl > inter.nh`) plutôt qu'un `else` implicite : le cas d'égalité ne
  tombe dans aucune des deux couleurs.
- **Les réglages sont des constantes nommées en majuscules** (`PF_MAX`,
  `PERSIST_MAX`, `SESSION_TTL`, `PF_CONC`) — impossible de les confondre avec
  une grandeur de marché.
- **Aucun des 108 n'est resté non tranché** après lecture : le code se laisse
  lire.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **215 (+1)**
- Publiés puis corrigés : **39**
- Interprétations retirées : **12**
