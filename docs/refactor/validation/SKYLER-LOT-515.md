# SKYLER LOT 515 — La dette du 514 est close par un **zéro mesuré** : les 38 divisions entières du dépôt sont toutes légitimes. Mais le 514 avait publié **253**, un chiffre faux d'un facteur 6,7 — et j'ai attrapé **trois artefacts de banc dans ce seul lot**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-515` (base : lot 514 fusionné,
`c514ef7a`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** — la dette que le 514 venait lui-même de créer en écrivant, dans son
second contrôle : « restent **253 `//`** et **82 `%`** numériques jamais
criblés ». La division entière est la forme la plus brutale du schéma
« détruire la résolution » que les 513 et 514 ont établi. Il fallait la
regarder.

## D'abord : le chiffre du 514 était faux

Ce 253 vient d'un `grep -rnE '[^/]//[^/]' vertex terminal.py` — **sans
`--include=*.py`**. Vérifié :

```text
253 lignes au total
 17 contiennent « :// »            → des URLs
129 seulement sont dans un .py     → le reste est du JS et du CSS,
                                     où « // » est un COMMENTAIRE
```

Et même dans les `.py`, l'essentiel des `//` vit **à l'intérieur de chaînes
Python qui construisent du JavaScript** — c'est toute l'architecture de
`terminal.py` et de `vertex/ui/*.py`. Compté par **AST**, immune aux
commentaires, aux URLs et aux chaînes :

```text
                        publié au 514      mesuré au 515
division entière  //          253                38     ← faux d'un facteur 6,7
modulo numérique  %            82                16     ← faux d'un facteur 5,1
formatage '%d' % x              —               688     ← écartés : ce ne sont pas
                                                          des opérations numériques
```

**Publiés puis corrigés : 13 → 14.**

## Le résultat : zéro défaut

Les 38 divisions entières, classées :

```text
19  MÉDIANE / INDEX          xs[len(xs)//2], half = n//2
      un index DOIT être entier — aucune information détruite
 9  SEUIL DE TRANCHE         max(1, n//3), int(s//10), len(g2)//5
 5  QUANTITÉ DE CONTRATS     int(capital // cost_per_contract)
      le plancher est CONSERVATEUR pour le risque : on achète moins, jamais plus
 3  LIBELLÉ DE DURÉE         'il y a %d h' % (age_s // 3600)
 2  autres                   6//2 (plafond constant) · n_samples//(n_folds+1)
```

**Aucune ne détruit une résolution qui compte.** Je le dis franchement, c'est le
résultat (règle 509-C : quand le dépôt fait bien, le dire).

Deux cas méritaient un examen et l'ont eu :

**Le libellé de durée.** `age_s // 3600` tronque : 7 199 s (1 h 59) affiche
« il y a 1 h ». La troncature va **toujours** dans le sens « plus frais qu'en
réalité », ce qui serait la mauvaise direction pour un indicateur de fraîcheur.
Deux raisons de ne pas en faire un dossier : c'est la **convention de tous les
formateurs de temps relatifs**, et surtout **l'état** (`ok` / `stale` /
`offline`) est calculé sur `age_s` **brut**, pas sur le libellé
(`live_engine.py:98`). Le verdict de fraîcheur est donc juste ; seule
l'étiquette humaine tronque. **Ce n'est pas un défaut, c'est une convention.**

**Le « tiers supérieur ».** `market_lens.py:46` — `'in_favor': (i+1) <= max(1,
n//3)`, commenté « tiers supérieur = porteur ». Avec 11 secteurs : `11//3 = 3`,
soit **27 %**, pas un tiers ; avec 1 secteur, `max(1, 0) = 1`, soit **100 %**.
L'étiquette n'est exacte qu'à n = 3, 6, 9. Mais mesuré : **`market_lens`
apparaît 0 fois dans le corpus servi.** Son seul lecteur est
`vertex/ui/pages/intelligence_page.py:277`, **page non servie**. Le champ est
produit par `/api/decision/<sym>` et lu par personne — nouvelle instance de la
famille **512-A**, pas un dossier neuf.

## Le second contrôle — et deux artefacts de plus

Mon AST ne voit ni le JavaScript, ni la troncature écrite autrement.

**Angle mort I — troncature Python autrement orthographiée** : `int(a/b)`,
`math.floor`, `math.trunc`, `math.ceil` → **mesurés**, à comparer aux 38.

**Angle mort II — le JS servi.** Premier comptage : 103 `Math.floor(`, 15
`parseInt(`, **44 `| 0`**. J'ai voulu séparer le vendor en soustrayant les
fichiers dont le chemin contient `lightweight` ou `vendor` → « 39 hors vendor ».
**Faux** : `chart.umd.min.js` (Chart.js, 205 ko minifiés) ne porte ni l'un ni
l'autre dans son nom. Refait **par attribution fichier par fichier** :

```text
lightweight-charts.standalone.production.js   floor 64 · parseInt  9
chart.umd.min.js                              floor 37 · parseInt  3
──────────────────────────────────────────────────────────────────
vendor                                        floor 101 · parseInt 12
CODE APPLICATIF SERVI                         floor   2 · parseInt  3
les 9 pages elles-mêmes                       floor   0 · parseInt  0
```

**Et le `| 0` était un homonyme.** Le motif `| 0` capture la fin de `|| 0`, la
coalescence — l'idiome des lots 506 et 510. Mesuré :

```text
motif naïf « | 0 »                44
dont « || 0 » (coalescence)       43
vrai décalage binaire              1
```

**Trentième récurrence de la famille homonyme, forme « collision de préfixe ».**

Les **6** vraies troncatures du code applicatif servi, lues une par une :

```text
chart-core.js  ×2   lbl.slice(0, Math.floor(r.w / 7))     tronquer un LIBELLÉ à la largeur en pixels
candlestick-lwc.js ×2  parseInt(mm, 10)                   lire un numéro de mois
heatmap.js     ×1   parseInt(m[1], 16)                    lire une couleur hexadécimale
vx-core.js     ×1   line: line | 0                        forcer un n° de ligne d'erreur en entier
```

**Aucune n'est le schéma destructeur.**

## Arrêts avant publication

1. **Le 253 du 514** — j'allais le reprendre tel quel dans ce brief.
2. **Le « 39 hors vendor »** — ma soustraction ratait Chart.js.
3. **Le « 44 `| 0` »** — 43 sur 44 étaient `|| 0`.

**Arrêtés avant publication : 107 → 110.** Trois dans un seul lot, tous
attribuables à mes propres bancs.

## Ce que ce lot vaut, dit franchement

**Aucun dossier neuf.** C'est le troisième lot de rang 0 de la veine (après le
509 et le 510). Ce qu'il rapporte :

- il **ferme** la dette du 514 par un zéro **mesuré**, pas supposé ;
- il **corrige un chiffre que j'avais publié**, faux d'un facteur 6,7 ;
- il établit que sur les 38 `//`, les 16 `%` et les 6 troncatures JS servies,
  **le dépôt fait juste** — les médianes passent par un index, les quantités de
  contrats sont planchées dans le sens conservateur, l'état de fraîcheur ne
  dépend pas de son étiquette.

Le 514 avait raison de ne pas conclure « isolé » sans borner son crible. Il
avait tort sur le nombre. Les deux se disent.

## Portée — ce que ce lot NE dit PAS

- Le crible AST ne couvre que **Python**. Les 6 sites JS servis ont été lus, pas
  criblés par un instrument.
- **Aucun scan de production, aucun navigateur, aucun POST, aucune route
  interdite.** Corpus servi obtenu par `test_client`, `persist` redirigé et
  vérifié.
- Je n'ai **pas** rejugé les 155 sites du 514 ni les 4 de sa famille F1 : ce lot
  porte sur `//` et `%`, la dette annoncée.
- Le cas `market_lens` est signalé comme **instance** de 512-A, pas compté comme
  dossier neuf.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0**.

Le 514 avait fait repartir la veine ; le 515 la referme sur cette piste-là, et
c'est le bon résultat : **on ne trouve pas un défaut là où il n'y en a pas**.
L'enseignement est ailleurs — **trois de mes propres chiffres se sont révélés
faux dans un seul lot**, tous par la même cause : un motif textuel appliqué sans
vérifier ce qu'il capture réellement. Le grep du 514 balayait du CSS ; ma
soustraction de vendor ratait un fichier ; mon motif `| 0` attrapait `|| 0`.
**L'AST n'a fait aucune de ces trois erreurs.** C'est un argument pour préférer
l'analyse structurelle au motif textuel chaque fois que c'est possible.

Feuille **inchangée : 35 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
trois rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **mesurer le
contenu des 23 routes non appelées** ; **la condition `k ≤ 5` sur un scan réel** ;
**les autres phrases calculées qui atteignent l'écran** (piste (d), la plus
prometteuse) ; **un producteur de synthèse d'une autre forme** ; **l'espion au
troisième niveau** ; **le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 110 (+3)** ;
**publiés puis corrigés 14 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
