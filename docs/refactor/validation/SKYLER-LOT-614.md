# SKYLER — LOT 614 · LE PALIER `muted` PASSE LE SEUIL, ET LES DEUX RÔLES DE #8A8284 RESTENT SÉPARÉS

Le lot 613 avait **mesuré** le défaut et **refusé** de le corriger, en posant le
chiffre et en laissant la décision à l'humain. L'humain a tranché : « termine au
max ». Ce lot exécute cette décision — **et le vrai risque n'était pas le
correctif, c'était de le passer au mauvais endroit**.

## Ce que le 613 avait laissé ouvert

`--vx-text-muted` `#8A8284` tombait à **4,04:1** sous `.vx-meta`,
`.vx-kpi-label`, `.vx-card-footer`, `.vx-muted` — **sous le seuil WCAG AA sur 11
combinaisons page × largeur**, les deux méthodes d'accord. Le 613 ne l'avait pas
déplacé : **60 littéraux** (contre 1 pour `faint`), déficit contextuel, et poids
typographique de tout le produit.

## Le correctif, et pourquoi pas le minimum

| valeur | ratio sur le pire fond mesuré | marge |
| --- | --- | --- |
| `#8A8284` *(avant)* | 4,04 | **−0,46** |
| `#938a8c` *(minimum strict, publié au 613)* | 4,51 | **+0,01** |
| **`#989092` *(retenu)*** | **4,86** | **+0,36** |

Le minimum strict aurait donné une conformité **à un centième près** : le moindre
ajustement de surface la reperd, en silence, sans qu'aucun test ne bouge. Une
marge qui tient à 0,01 n'est pas une marge.

Luminance **0,2870**, entre `faint` (0,2028) et `secondary` (0,4910) — la
hiérarchie des quatre paliers tient, avec de l'air des deux côtés.

## LE PIÈGE, ET C'EST LUI LE LOT

**`#8A8284` portait DEUX rôles.** Un `sed` sur le littéral les aurait fusionnés.

| rôle | ce qu'il colore | sites | a suivi ? |
| --- | --- | --- | --- |
| **texte discret** | token, **39 replis** `var(--vx-text-muted,…)`, `palette.TEXT_MUTED`, `VXCharts.colors.muted` (2 miroirs JS), 1 repli de graphique | **43** | **oui → `#989092`** |
| **série neutre acier** | `--vx-steel-3`, `palette.COPPER`, `copper`, **dernière série des graphiques**, **lignes support/résistance** | **9** | **non → `#8A8284`** |

Confondre les deux aurait **changé la couleur d'une série de données** au
prétexte de rendre du texte lisible : un chiffre affiché dans une teinte qui ne
veut plus rien dire. C'est l'inverse exact de ce que le lot cherche, et c'est le
genre d'erreur qu'aucune suite verte n'aurait signalée — **jusqu'à ce lot**, où
un test la rend rouge.

## La mesure, avant / après

**8 pages servies × 2 largeurs, 2 700 feuilles de texte, 212 combinaisons.**

| | avant 613 | après 613 | **après 614** |
| --- | --- | --- | --- |
| combinaisons sous le seuil | **26** | 23 | **16** |

Les **sept** familles qui étaient sous le seuil **par les deux méthodes** l'ont
toutes quitté :

| famille | avant *(A / B)* | après |
| --- | --- | --- |
| `div.vx-card-footer` | 5,44 / **3,79** | conforme |
| `span.vx-kpi-label` 12 px | 5,22 / **3,88** | conforme |
| `div.vx-meta` | **4,04** / **3,93** | conforme |
| `span.vx-kpi-label` 13 px | **4,04** / **3,93** | conforme |
| `span.vx-meta` | **4,04** / **4,09** | conforme |
| `div.vx-muted` | **4,48** / **4,29** | conforme |
| `span.k` | 5,22 / **4,49** | conforme |

## Le piège, écrit avant de toucher le token

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « les 39 replis sont inertes ; les laisser divergents recrée le défaut du 613 à 39× » | **NON TRANCHÉ, et rendu sans objet** — je les ai alignés ; l'inertie n'a pas été prouvée |
| **(b)** | « `#989092` fait passer les 9 familles mesurées » | **CONFIRMÉ** — 7 conformes par les deux méthodes, 2 conformes par la méthode fondée *(voir plus bas)* |
| **(c)** | « les familles sous le seuil pour une AUTRE raison ne bougeront pas » | **CONFIRMÉ** — `span.vx-chip` en `#2bbe90` (vert) reste à 3,98 / 8,61, **inchangé au centième** |
| **(d)** | « la hiérarchie tient » | **CONFIRMÉ** — 0,2028 < 0,2870 < 0,4910 |
| **danger nommé** | « un `sed` aveugle fusionnerait les deux rôles » | **ÉVITÉ, et désormais gardé** |

**(c) est le volet utile** : il prouve que ma classification des causes était
juste. Si la puce verte avait bougé, c'est que j'aurais corrigé autre chose que
ce que j'avais mesuré.

## Ce que ce lot a appris sur l'instrument du 613

Le 613 avait posé le critère : **B (pixels peints) ne fait foi que là où la part
de la dominante est élevée**. Appliqué aux deux familles `#989092` encore
signalées par B :

| élément | forme | part de la dominante | verdict |
| --- | --- | --- | --- |
| `.vx-chip` | pilule, `border-radius:99px`, fond transparent | 70 % / 70 % — mais **les deux rangées se contredisent** *(69,69,70)* vs *(21,21,22)* : c'est **l'anneau de bordure**, pas le fond | **B non fondée** ; A = 6,54 |
| `.vx-freshness` | pilule, `border-radius:999px` | **17 % / 23 %** | **B non fondée** ; A = 6,54 |
| `.vx-meta` | bloc `border-radius:0`, **sans marge interne** | **20 % / 14 %** | **B non fondée AUSSI** |

**`.vx-meta` est la découverte** : c'est une famille où A et B *semblaient*
d'accord au 613 (4,04 vs 3,93). **L'accord était fortuit.** Le critère les
disqualifie tous les trois.

**Conséquence de méthode, plus nette que celle du 613** : pour du **texte en
ligne**, c'est **A qui porte le signal** ; B ne sert qu'à rattraper les fonds en
**dégradé**, là où A est structurellement aveugle. Les deux méthodes ne se
départagent pas par principe — **chacune a un domaine, et le domaine se mesure**.

## Ce que le lot n'établit pas

- **Que les 39 replis étaient inertes.** Je ne l'ai pas prouvé : je les ai
  alignés, ce qui rend la question sans objet mais ne l'a pas résolue.
- **Le texte des graphiques.** `VXCharts.colors.muted` a suivi le token, mais
  **aucun banc ne l'a mesuré** — un `<canvas>` n'expose aucun nœud de texte.
  L'argument retenu est un **raisonnement, pas une mesure** : le changement
  éclaircit le texte sur des fonds sombres, il ne peut donc pas dégrader la
  lisibilité. Si un jour un fond de graphique devient clair, cet argument tombe.
- **Les 16 combinaisons restantes.** 11 sont des artefacts d'instrument (texte
  SVG, puces arrondies, encre sombre sur dégradé — design correct), 2 sont les
  familles `#847a7c` du 613 (conformes par A), 1 est la puce verte `#2bbe90`
  **non examinée**, 2 sont les `#989092` traitées ci-dessus. **La puce verte
  reste ouverte.**
- **208 feuilles sur 2 700** demeurent injoignables en pixels.

## Règles neuves

- **614-A — AVANT DE CORRIGER UNE COULEUR, COMPTER SES RÔLES.** `#8A8284` en
  portait deux ; le nom du token ne le disait pas, seule la lecture de ses 52
  sites l'a montré. **Un littéral n'est pas une intention : c'est une valeur que
  plusieurs intentions peuvent partager.**
- **614-B — UNE CONFORMITÉ À +0,01 N'EST PAS UNE CONFORMITÉ.** Le minimum
  calculé est un point de départ, pas une cible : il place le produit sur la
  ligne exacte où le prochain ajustement le fera retomber, sans rougir un test.
- **614-C — QUAND DEUX MÉTHODES S'ACCORDENT, VÉRIFIER QUAND MÊME QU'ELLES ONT
  DU SIGNAL.** `.vx-meta` donnait 4,04 et 3,93 — un accord rassurant, et l'une
  des deux ne mesurait rien. **L'accord de deux instruments n'est pas une preuve
  si l'un des deux est hors de son domaine.**

## Ce que le dépôt fait bien

- **Les deux rôles étaient déjà nommés séparément** (`--vx-text-muted` et
  `--vx-steel-3`, `TEXT_MUTED` et `COPPER`) : la structure permettait de les
  séparer proprement. Seule la **valeur** était partagée.
- **Les listes de palette ont réclamé le nouveau littéral** — sept gardiens ont
  refusé la couleur inconnue avant qu'elle n'entre.
- **Le gardien du 613 s'est auto-fermé** : son message disait « si ce palier
  atteint le seuil, mettre à jour le rapport et retirer ce test ». C'est
  exactement ce qui s'est passé, quatre-vingt-dix minutes plus tard.
- **Les 4 empreintes de page qui ont bougé sont exactement celles qui SERVENT le
  littéral** — vérifié, pas supposé : le bloc d'`analysis_page.py` qui le porte
  n'est pas émis sur la vue par défaut (marqueur « Carte des risques » absent du
  HTML servi).

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **Fichiers de production** : `tokens.css`, **39 replis** répartis dans
  `vertex/ui/**` et `vertex/static/**`, `vertex/visualization/palette.py`,
  `chart-core.js`, `chart-theme-obsidian-copper.js`, `markets_page.py`,
  `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (6 tests, **6 mutations rouges** dont « la série acier a
  suivi le texte ») + **7 listes de palette élargies** + **1 test du 613 retiré**
  parce qu'il s'était fermé lui-même.
- **5 épingles** `td-shell-v196` → **`td-shell-v197`** + empreinte des assets et
  `_SW_VERSION` du gardien 361.
- MD5 des 8 pages : **4 changées, 4 identiques** — correspondance vérifiée avec
  les pages qui servent le littéral.
- `GET /api/client-log` : **0 erreur**.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2915 passed / 0 skipped** *(2910 − 1 retiré + 6 du gardien neuf)*.
- Navigateur : **19 chargements** — 8 pages × 2 largeurs après correctif, plus
  3 sondages d'échantillonnage ciblés.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **249** *(+1 : « les 4 empreintes changées
  correspondent aux pages qui portent un repli » — faux, `analysis_page.py` en
  porte 3 et n'a pas bougé ; l'énoncé juste est « les pages qui le SERVENT »)*
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 11**
