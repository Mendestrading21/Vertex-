# SKYLER LOT 547 — **51 sur 51 : aucun squelette ne disparaît au rendu.** La chaîne des chiffres source devient 150 → 100 → 89, le servi en est un sous-ensemble EXACT, et il ne reste que 11 identifiants. J'ai failli publier une trouvaille de production qui était une frontière entre deux constantes Python

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-547` (base : lot 546 fusionné,
`2c726fdf`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(q)** — le 546 a expliqué l'écart des 51 par la **fenêtre de 400
caractères**, mais **ne l'a prouvé que sur UN cas** (`vx-hero`). Les cinquante
autres étaient une hypothèse. Deux issues possibles, qui ne se valent pas :

- **(i)** voisin mal attribué — le marqueur appartient à un autre identifiant ;
- **(ii)** porteur réel en source **dont le squelette disparaît au rendu** —
  ce serait une **trouvaille de production**.

## L'instrument — la pile du 535, portée sur la source

Pour chaque marqueur (`vx-skeleton` ou `%%LOADING%%`), on cherche l'`id="…"`
**le plus proche AVANT lui** : c'est son **propriétaire**. Un marqueur a **un
seul** propriétaire — là où la fenêtre en donnait plusieurs. C'est le principe
du CHEMIN 2a du 544, qui coïncidait exactement avec `html.parser` sur les
octets (63 = 63).

```text
FENÊTRE  (critère des lots 544-546, proximité 400 caractères)    150
PILE     (propriétaire d'au moins un marqueur)                   100
                                                          écart   50
```

**50 des 51 sont des voisins mal attribués.** L'hypothèse (i) tient sur
cinquante cas, plus seulement sur un.

## L'arrêt du lot — **le 51ᵉ était la trouvaille, et il n'en était pas une**

Un seul identifiant ressortait **porteur réel en source sans squelette dans les
octets** : `vx-demo-banner`, dans `options_intel_page.py`. C'était, en
apparence, exactement l'issue (ii). Lecture du fichier :

```python
_HEADER = """ … <div id="vx-demo-banner"></div> """
_LOADING = '<div class="vx-skeleton" style="height:120px"></div>'
```

**Le marqueur est dans une AUTRE constante Python.** `_LOADING` est injecté
ailleurs, là où un `%%LOADING%%` l'appelle ; il n'a aucune relation HTML avec
`vx-demo-banner`. **Ma pile a franchi une frontière que le HTML ne franchit
pas** — précisément la limite que j'avais nommée au second contrôle, et que
j'allais publier comme une découverte.

**Arrêtés avant publication : 166 → 167.**

## La limite, mesurée au lieu d'être supposée

Plutôt que de retirer un cas à la main, un second banc mesure la frontière :
pour chaque propriétaire, l'identifiant et son marqueur sont-ils dans la
**même chaîne littérale Python** ? Les spans sont pris dans l'**arbre**
(`ast`), pas devinés.

```text
propriétaires DANS LA MÊME chaîne littérale                       89
propriétaires À CHEVAL sur deux constantes                        11
marqueurs sans aucun `id=` avant eux                               0
```

## Le résultat — quatre critères, et un emboîtement exact

```text
FENÊTRE  (544-546, proximité 400 caractères)                     150
PILE     (propriétaire, toutes chaînes confondues)               100
STRICT   (propriétaire DANS LA MÊME chaîne)                       89
SERVI    (octets servis, `html.parser`, 44 URL)                   78

STRICT ∩ SERVI                                                    78
SERVI mais PAS dans STRICT                                         0
STRICT mais PAS servi                                             11
```

**Zéro servi hors du strict.** Tout conteneur à squelette réellement servi est
un porteur strict côté source : dans ce sens-là, l'instrument ne rate rien.

## Verdict sur les 51 — **l'hypothèse (ii) est réfutée**

```text
mal attribués par la FENÊTRE                                      50
mal attribués par la FRONTIÈRE entre deux constantes                1
porteurs réels dont le squelette disparaîtrait au rendu             0
```

**Aucun squelette ne disparaît entre la source et les octets.** Le paradoxe des
51 n'était pas un défaut du produit : c'était **entièrement** un défaut de mes
deux instruments successifs.

## Ce qu'il reste : 11 identifiants, tous adressés

```text
pf-risk-gauge          vertex/ui/pages/portfolio_page.py       (chaîne JS, 544-A)
vx-committee-body      vertex/ui/pages/intelligence_page.py
vx-committee-gauge     vertex/ui/pages/intelligence_page.py
vx-imp-feed            vertex/ui/pages/intelligence_page.py
vx-memory-body         vertex/ui/pages/intelligence_page.py
vx-research-body       vertex/ui/pages/intelligence_page.py
vx-strategy-core       vertex/ui/pages/intelligence_page.py
vx-strategy-gates      vertex/ui/pages/intelligence_page.py
vx-strategy-options    vertex/ui/pages/intelligence_page.py
vx-trk-active-body     vertex/ui/pages/tracking_page.py
vx-trk-summary-body    vertex/ui/pages/tracking_page.py
```

**La dette, mesurée quatre fois, a suivi : 87 (544) → 72 (545) → 21 (546) →
11 (547).** Et elle n'a jamais changé de nature : les mêmes deux pages routées
jamais mesurées, plus le conteneur JavaScript du 544.

## Second contrôle (481) — ce que la pile côté source ne voit pas

```text
marqueurs `%%LOADING%%` (remplacés au rendu)                      87
marqueurs `vx-skeleton` littéraux                                 25
                                                          total  112
`id=` écrits en APOSTROPHES, invisibles au crible                  7
```

Et surtout : **la profondeur est invisible.** La pile ne sait pas si l'`id=` le
plus proche est un **ancêtre** ou un **frère déjà fermé**. Le 544 a montré que
cette approximation coïncidait exactement avec `html.parser` sur les octets
(63 = 63), et le `SERVI mais PAS dans STRICT = 0` de ce lot va dans le même
sens — **mais rien ne le garantit sur la source**, et c'est dit.

## Ce que le dépôt fait bien, mesuré

- **Aucun squelette ne se perd entre la source et le rendu** : les 78
  conteneurs servis sont tous des porteurs stricts de la source.
- **Zéro conteneur servi qui n'existe pas côté source** — dans les deux sens,
  la source et les octets se répondent.
- **Le désordre était dans mes instruments, pas dans le produit** : trois
  lots de chiffres corrigés, et le produit n'a pas bougé d'un octet.

## Portée — ce que ce lot NE dit PAS

- **Il ne dit pas que les 11 sont sans chargeur** : ils ne sont pas servis par
  les 44 URL mesurées. Mesurer `/intelligence` et `/tracking` demande un GO.
- **Le 89 est une borne, pas une vérité** : la profondeur reste invisible côté
  source.
- Les 7 `id=` en apostrophes et les identifiants **construits** échappent au
  crible ; ils sont comptés, pas résolus.
- **Aucun navigateur, aucune correction engagée, aucune route neuve appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés pendant le lot** (`ai_enrichment.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Une question ouverte au 544 se ferme : **il n'y a pas de
squelette fantôme**, et le chiffre source a enfin une définition qui se
compare à celle des octets.

Ce qu'il faut dire sans le maquiller : **j'avais une trouvaille de production
entre les mains, et elle était fausse.** Un identifiant, un marqueur, deux
lignes de suite dans un fichier — et rien qui les relie, parce qu'une
accolade de chaîne Python se referme entre les deux. **Quatre lots pour
qu'un chiffre cesse de mentir**, et chacun a corrigé le précédent avec un
instrument un peu moins naïf.

Trois règles neuves :

- **547-A · UNE FRONTIÈRE DE CONSTANTE N'EST PAS UNE RELATION HTML** —
  `_HEADER` finit, `_LOADING` commence : deux lignes voisines, zéro lien.
- **547-B · UNE LIMITE SE MESURE, ELLE NE SE RETIRE PAS À LA MAIN** — plutôt
  que d'écarter un cas gênant, on a compté les 11 franchissements de frontière.
- **547-C · L'EMBOÎTEMENT EST UNE PREUVE** — `SERVI ⊂ STRICT` avec zéro
  exception vaut mieux qu'un total qui tombe juste.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 11 identifiants de `/intelligence`, `/tracking`
et `pf-risk-gauge` — en attente d'un GO** ; **les 4 zones sous attente sans
annonce du 545 — candidat, non arbitré** ; **129 routes GET sans paramètre hors
corpus** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** (112 atténuations,
103 états, 53 refus, 178 appels, 156 variables serveur, 25 fonctions, 11
limites) ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé
du 542** ; **les 15 messages d'erreur sans pourquoi du 541** ; **les 95
atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 167 (+1)** ; publiés
puis corrigés **23** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
