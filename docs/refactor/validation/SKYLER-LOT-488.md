# SKYLER LOT 488 — La règle du 487 appliquée à TOUTES les atténuations qui ont fait descendre un rang : les trois autres TIENNENT, vérifiées à l'écran — et la boucle avait déjà la méthode aux lots 442 et 471 avant de la perdre au 486

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-488` (base : lot 487 fusionné,
`89514b3b`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 487 a posé une règle neuve — *une information « co-visible » doit l'être sur
la MÊME VUE, pas seulement dans les mêmes octets* — et ne l'a appliquée qu'à
**un** cas, le sien. La règle 485 exige de l'appliquer à **tous les objets de
même genre** : toutes les atténuations qui ont fait **descendre un rang**.

## Le recensement, et son tri par lecture

Balayage des **490 rapports** sur le vocabulaire d'atténuation (« co-visible »,
« ce qui atténue », « note honnête », « pourquoi pas rang 1 », « empêche de
monter », « reste rang 2 »).

**Calibration écrite dans le code** : le 486 — qui a classé rang 2 explicitement
sur une co-visibilité, réfutée au 487 — **doit** être dans la population brute.
**Trouvé.** Sortie programmée sinon.

```text
population brute : 30 rapports sur 490
```

**Et c'est en LISANT la liste que l'instrument se corrige** : douze de ces trente
ne contiennent que « note honnête » **au sens d'un état vide honnête** — rien à
voir avec l'atténuation d'un rang. Le vocabulaire ratisse large ; le tri se fait
à la lecture, pas au `grep`.

**Reste QUATRE atténuations qui ont réellement fait descendre un rang** :

| dossier | atténuation invoquée | statut avant ce lot |
|---|---|---|
| 455 | « les six contrôles sont rendus **juste au-dessus** de la phrase » | non vérifiée |
| 456 (i) | « une note **honnête et co-visible** » | non vérifiée |
| 484-B | « la puce **Fondamentaux 0/5** est bel et bien affichée » | non vérifiée |
| 486-A | « l'alerte de concentration Top1 > 25 % » | **RÉFUTÉE au 487** |

## Une lecture qui tranche avant le navigateur

La note du 456 est passée au Chart Shell canonique comme **`limits: dq.note`**.
Or le 442 avait établi que le **tiroir** « Comprendre ce graphique » ne rend que
`shows`, `why`, `confirm`, `invalidate`. Si `limits` n'était rendu que là, la
note serait **derrière un clic** — et l'atténuation tomberait.

Mesuré dans `chart-core.js` : **deux** sites de rendu.

```text
L161   ${opts.limits ? `<span class="vx-meta">${opts.limits}</span>` : ''}
       → à l'intérieur de <div class="vx-chart-foot">, le PIED VISIBLE de la carte
L174   … dans la ligne « Source : … » du tiroir (répétition)
```

**Le pied de carte, pas le tiroir.** L'atténuation tient par lecture. Restait à
l'exécuter (leçon 476 : *la lecture propose, l'exécution décide*).

## Au navigateur — les trois tiennent

Serveur DEMO, Chromium préinstallé par `executable_path`. Mesure : existe-t-il
**une même carte rendue** (`.vx-card`/`section`) contenant **à la fois** le texte
du défaut **et** celui de l'atténuation ?

### 456 — `/system?view=data`

```text
Qualité des données (20 titres) · Les données sont-elles utilisables pour décider ?
Dominante : DEMO (20 / 20) · source demo · À l'instant · scan demo · Secours
qualité au niveau scan (source unique) — la provenance valeur par valeur
arrive avec le routage data_sources · Comprendre ce graphique
                                                       → même carte : OUI
```

**L'atténuation est dans le pied visible de la carte, sans aucun clic.** Le
rang 2 du 456 (i) **tient**.

**Un faux résultat arrêté en chemin** : mon premier passage a mesuré `/system`
nu et rendu « CARTE ABSENTE » — j'allais conclure que l'atténuation n'était pas
vérifiable. La carte vit sur **`/system?view=data`**, une **vue serveur
distincte** (`VIEWS` déclare `('data','Données')`, défaut `connections`).
**Diagnostiqué, pas conclu.** Arrêtés avant publication : 52 → **53**.

### 455 — ticket pré-trade de `/analysis/AAPL`

Déclenché par le formulaire (montant 2 000, bouton « Vérifier ») :

```text
DÉFAVORABLE AAPL · 2 000 · Verdict du comité — Titre hors du scan courant — aucun verdict.
✕ Régime de marché — RISK-OFF — risque neuf déconseillé par le régime.
· Positionnement dealer — Profil GEX indisponible pour ce titre.
· Résultats — Date de résultats inconnue.
✕ Concentration résultante — AAPL pèserait 50 % du book après l'ajout (trop concentré).
⚠ Plan de niveaux — Aucune invalidation définie …
                                                       → même carte : OUI
```

Les six contrôles, **avec leurs icônes de statut et le détail qui nomme ce qui
manque**, sont rendus dans la **même carte** que la narration. Le rang 2 du 455
**tient**, exactement comme son rapport l'affirmait.

### 484-B — carte Skyler de `/analysis/AAPL`

```text
SKYLER — DÉCISION CANONIQUE · Score /40 par blocs de la Constitution V2 …
REFUSER 8/40 niveau REFUS_WATCH · plafonnée par NO_INVALIDATION
Fondamentaux 0/5   Catalyseurs 2/5   Technique 0/6   Flux/anomalies 0/4
Régime 4/4   Asymétrie 0/6   Option 0…
                                                       → même carte : OUI
```

Le rang 2 du 484-B **tient**.

**Et la carte confirme au passage deux mesures antérieures, à l'écran** :
« Catalyseurs **2/5** » et « Flux/anomalies **0/4** » — les blocs bridés du 485,
visibles ; et « Dominante : DEMO (**20 / 20**) » — le camembert à une seule part
du 456 (ii), visible aussi. **Je ne recompte ni l'un ni l'autre comme trouvaille.**

## Le second contrôle — un cas que le recensement EXCLUT

Mon recensement retient les rangs abaissés **par une co-visibilité**. Il exclut
donc un rang 2 justifié **autrement**. Cas : le **442**.

Son rapport écrit, mot pour mot : « **Rang 2** : défaut affiché, atténué par une
légende honnête **non co-visible** » — et il ajoute « **Ce que je n'ai pas
établi** : je n'ai **pas observé** de titre réel à moins de 200 barres ».

**Le 442 ne repose PAS sur une co-visibilité — il la nie explicitement**, et son
rang tient sur une **accessibilité non établie**, comme le rang 3 du 483.
**L'exclusion est justifiée**, et pour la bonne raison, pas par chance.

## Le fait de méthode — la boucle avait la règle, et l'a perdue

C'est le résultat le plus inconfortable, et il ne porte pas sur Vertex.

- **Lot 442** : « atténué par une légende honnête **non co-visible** » — il
  distingue déjà co-visible et non co-visible, et refuse de créditer la seconde.
- **Lot 471** : « Ils sont donc co-visibles sur **`risque`, et là seulement** » —
  il mesure la co-visibilité **vue par vue**, exactement la règle du 487.
- **Lot 486** : affirme « une information co-visible existe » **sans vérifier la
  vue** — et le 487 le réfute au navigateur.

**UNE RÈGLE PEUT ÊTRE APPLIQUÉE AVANT D'ÊTRE NOMMÉE, ET OUBLIÉE APRÈS L'AVOIR
ÉTÉ.** Le 487 croyait poser une règle neuve ; il **redécouvrait** une pratique
que les 442 et 471 tenaient déjà. Ce qui manquait n'était pas l'idée, c'était
**de l'écrire** — quarante-quatre lots plus tôt.

## Le résultat, et je le publie tel quel

**Trois atténuations sur quatre tiennent. Aucun rang ne bouge. La feuille de
décision est inchangée.**

C'est un résultat de **bornage**, comme au 480 : le 487 avait trouvé une
atténuation fausse, et la question légitime était « combien d'autres ? ».
Réponse mesurée : **aucune autre**. J'aurais préféré plus spectaculaire — et
c'est précisément pour cela qu'il faut le publier ainsi.

## Portée

- **Je n'ai pas rejoué les défauts eux-mêmes**, seulement leurs **atténuations**.
  Que le 456 (i) reste un défaut n'est pas remis en question ici.
- Le **plafond de 200** du 456 **ne mordait pas** dans cette session : le scan
  DEMO comptait **20 titres**. La carte affiche « 20 titres », ce qui est exact.
  **Je n'ai donc PAS observé le cas fautif à l'écran** — seulement que
  l'atténuation est co-visible.
- **Un seul viewport (1440 × 1400)**, un seul thème, pas de mobile. Une
  atténuation co-visible en 1440 pourrait ne plus l'être en 390 — **non mesuré**.
- Le test « même carte » repose sur l'ancêtre `.vx-card`/`section` **et sur le
  texte rendu** ; une atténuation hors de tout conteneur de carte échapperait.
- Douze rapports de la population brute écartés **par lecture** (« note honnête »
  au sens d'état vide) : **je les nomme comme écartés, ils ne sont comptés dans
  aucun total.**
- `/analysis/AAPL` **écrit** (`skyler_decisions.json`, `skyler_memory.json`) : je
  l'ai su, assumé, et **restauré à l'octet** — voir le cycle.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert`, `os.chdir` **et sorties en chemin ABSOLU** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Serveur DEMO **arrêté** — port 5002 en refus de connexion, vérifié.
- Snapshot runtime **avec copie du contenu** : 6 fichiers touchés par la session
  navigateur — `ai_enrichment`, `breadth_history`, `daily_prev`,
  `session_digest_cache` (serveur DEMO, reproduction du 391) et
  **`skyler_decisions` + `skyler_memory`** (écrits par `/analysis/AAPL`, prévu et
  déclaré). **21 fichiers, aucun apparu, aucun disparu, écart final AUCUN.**
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinq lots de suite ont payé une dette nommée par le précédent. Les quatre
premiers ont trouvé autre chose ; **celui-ci confirme**, et c'est aussi un
résultat — le premier depuis le 482 où la mesure ne déplace rien.

Ce qu'il déplace est ailleurs : il montre que la boucle **produit des règles
qu'elle possédait déjà**. Le 487 a nommé une règle que le 442 appliquait
quarante-quatre lots plus tôt. Relire ses propres rapports est un acte de mesure
(leçon 471) — **et ce lot en est la démonstration la plus nette : la meilleure
source de méthode de la boucle, c'est la boucle elle-même, à condition de la
relire.**

Comptes séparés : résultats faux **arrêtés avant publication 53 (+1)** ; publiés
puis corrigés **10** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
