# SKYLER LOT 489 — La dette du 488 soldée en MOBILE : les trois atténuations survivent à 390 × 844 — mais la mesure trouve autre chose, une ATTÉNUATION CONDITIONNELLE, qui tombe en dessous de ~730 px de hauteur d'écran

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-489` (base : lot 488 fusionné,
`1abc5fee`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 488 avait nommé sa dette : « la co-visibilité n'a été vérifiée qu'en **un
seul viewport (1440 × 1400)** — une information co-visible en 1440 pourrait ne
plus l'être en 390, **non mesuré** ». Cinquième dette nommée payée d'affilée.

## Le banc, calibré par construction

Les **deux viewports dans le même script**, sur les trois atténuations validées
au 488 (455, 456 (i), 484-B). **La calibration est le viewport 1440 lui-même** :
le banc doit y retrouver « même carte = OUI » pour les trois, comme au 488.
**Retrouvé, trois fois.** Instrument valide.

```text
VIEWPORT 1440 × 1400 (témoin)      456 · 484-B · 455   MÊME CARTE = True  (reproduit le 488)
VIEWPORT  390 × 844  (mobile)      456 · 484-B · 455   MÊME CARTE = True
```

**Les trois atténuations survivent au mobile.** Aucune n'est masquée, aucune
n'est de taille nulle, aucune n'est rognée par un `overflow` — `display: block`,
`visibility: visible` dans les six mesures.

## Mon propre instrument était incomplet — attrapé en lisant sa sortie

Le premier banc mesurait la position **de l'atténuation seule**, et rendait :

```text
455 · mobile   atténuation à 5 357 px, écran 844 px → hors du viewport initial
```

J'allais publier « en mobile, l'atténuation du 455 sort de l'écran initial ».
**C'est vrai et sans intérêt** : au viewport 1440 elle est **aussi** hors de
l'écran initial (2 127 px pour 1 400 px de haut). Le défaut lui-même est tout
aussi bas. **La quantité qui décide n'est pas la position de l'atténuation, c'est
la DISTANCE entre le défaut et son atténuation.**

**Arrêtés avant publication : 53 → 54.**

## La mesure refaite — distance défaut ↔ atténuation

```text
viewport            456           484-B          455          écran
1440 × 1400        510 px         81 px         620 px       1400 px   → 3 × co-visibles
 390 × 844         406 px        119 px         681 px        844 px   → 3 × co-visibles
 375 × 667         391 px        137 px        681 px         667 px   → 455 : NON
 360 × 640         376 px        137 px        681 px         640 px   → 455 : NON
```

**La distance du 455 se fige à 681 px** sur les trois largeurs mobiles — elle ne
dépend pas de la largeur, seulement de la pile verticale des six contrôles. La
réponse **a cessé de bouger** (règle 459) : seule la **hauteur d'écran** décide.

## Le résultat — une atténuation CONDITIONNELLE

**456 et 484-B tiennent partout.** Le 484-B est même le plus robuste : 81 à
137 px de distance, la puce est collée au total.

**Le 455 tient sur un grand téléphone et tombe sur un petit.** Son atténuation
— les six contrôles avec leur détail honnête — est co-visible avec la narration
tant que l'écran fait **au moins ~730 px de haut** (681 px de distance plus la
hauteur du nœud) ; en dessous, il faut **défiler entre le défaut et ce qui le
corrige**.

```text
iPhone 14/15 (844 px)      co-visible      → l'atténuation joue
iPhone SE    (667 px)      NON co-visible  → l'atténuation ne joue plus
Android bas  (640 px)      NON co-visible
```

### Ce que j'en fais, et ce que je n'en fais pas

**Je ne promeus PAS le 455 au rang 1**, et je dis pourquoi. Le précédent du 487
promouvait le 486-A parce que son atténuation était sur une **autre vue** —
jamais simultanée, **sur aucun appareil**. Ici, l'atténuation est simultanée sur
l'appareil le plus probable. Promouvoir sur la base d'un écran que je ne sais pas
être celui de l'utilisateur serait une **aggravation non fondée**, et les
aggravations sont aussi fragiles que les atténuations (leçon 478).

**Je ne le confirme pas non plus sans réserve.** Le rang 2 du 455 devient
**conditionnel**, et la condition est écrite : *hauteur de viewport ≥ ~730 px*.

**Ce que je ne sais pas et que je ne devine pas** : la taille réelle de l'écran
de l'utilisateur. `CLAUDE.md` dit « LAN/iPhone », rien de plus. **Je ne sais donc
pas de quel côté de la borne il se trouve** — et c'est exactement le genre de
chose qu'un humain tranche en une seconde et qu'un agent ne doit pas inventer.

## Genre neuf pour la nomenclature

**UNE ATTÉNUATION PEUT ÊTRE CONDITIONNELLE — vraie sur un appareil, fausse sur un
autre. Un rang qui en dépend doit PORTER SA CONDITION, pas la taire.**

C'est le troisième affinement consécutif de la même notion : le 487 a exigé la
même **vue**, le 488 la même **carte**, le 489 y ajoute la **distance** et
l'**écran**. La co-visibilité n'est pas un fait binaire du code : c'est une
propriété **géométrique et matérielle** du rendu.

## Le second contrôle — un cas que le banc EXCLUT

`innerText` ignore `display:none`, mais **pas** un texte rogné par
`overflow:hidden` : un tel texte serait compté « présent » et resterait
invisible. Le banc mesure donc aussi, pour chaque nœud d'atténuation :
`display`, `visibility`, largeur/hauteur nulles, et le rognage par tout ancêtre
à `overflow` caché.

```text
six mesures (3 cas × 2 viewports) : display=block · visibility=visible
                                    taille nulle = False · rogné = False
```

**Le contrôle a tourné et n'a rien trouvé.** Ce n'est **pas** la même chose que
de l'avoir validé sur un cas positif : je n'ai **aucun** exemple de texte rogné
dans ce périmètre pour prouver que le détecteur mordrait. **Je le dis plutôt que
de compter ce contrôle comme concluant.**

## Portée

- **Trois atténuations, quatre viewports** — pas la matrice complète du produit.
  Les autres cartes des 8 pages ne sont **pas** mesurées.
- La distance du 455 est mesurée **avec le ticket pré-trade déclenché sur AAPL et
  un montant de 2 000** : un autre symbole ou un autre montant changerait le
  nombre de contrôles rendus, donc la distance. **Non exploré.**
- Le seuil « ~730 px » est **déduit** de 681 px de distance plus la hauteur du
  nœud (17 px) et une marge ; **je n'ai pas dichotomisé** entre 667 et 844 pour le
  situer exactement.
- **Aucune capture d'écran** : les verdicts viennent de `getBoundingClientRect`,
  pas de l'œil. Un texte visible géométriquement mais illisible (contraste,
  troncature par ellipse) **échapperait**.
- Les défauts eux-mêmes ne sont **pas rejoués** — seulement leurs atténuations.
- `/analysis/AAPL` **écrit** `skyler_decisions.json` et `skyler_memory.json` :
  prévu, déclaré, **restauré à l'octet**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert`, `os.chdir` **et sorties en chemin ABSOLU** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Serveur DEMO **arrêté** — port 5002 code 000, vérifié.
- Snapshot runtime **avec copie du contenu** : 6 fichiers touchés par les sessions
  navigateur (`ai_enrichment`, `breadth_history`, `daily_prev`,
  `session_digest_cache` — serveur DEMO, reproduction du 391 — plus
  `skyler_decisions` et `skyler_memory`, écrits par `/analysis/AAPL`).
  **21 fichiers, aucun apparu, aucun disparu, écart final AUCUN.**
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquième dette nommée payée d'affilée, et **la cinquième trouve autre chose que
ce qu'elle cherchait** : le 488 craignait que le mobile casse une co-visibilité ;
le mobile ne la casse pas, **c'est la taille de l'écran qui la conditionne**, et
la borne est la même en 390, 375 et 360.

Le fait notable est ailleurs, et il est de méthode : **mon premier banc posait la
mauvaise question**. « L'atténuation est-elle dans l'écran initial ? » a une
réponse vraie et inutile ; « à quelle distance du défaut est-elle ? » a une
réponse qui tranche. **Une mesure exacte peut répondre à côté** — et seule la
lecture de sa sortie le révèle.

Comptes séparés : résultats faux **arrêtés avant publication 54 (+1)** ; publiés
puis corrigés **10** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
