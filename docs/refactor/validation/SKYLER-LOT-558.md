# SKYLER LOT 558 — les « 35 accès imbriqués » enfin nommés : **presque la moitié n'étaient pas des lectures de contrat mais des méthodes JavaScript**, et 12 des 16 vraies sous-clés portent sur des routes dont je n'ai jamais mesuré le contrat

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-558` (base : lot 557 fusionné,
`84b3622d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — le corpus
JS du 553 et les mesures du 552 sont sur disque.

## Le choix

**(dd)** — le 553 comptait « accès IMBRIQUÉS (non comparables au premier niveau)
**35** » et **quatre lots les ont laissés à l'état de nombre**. Le 557 vient
d'établir (557-A) qu'un chiffre non nul du second contrôle est une **dette**.
Question : **quelles sont ces lectures, sur quelles routes, et que peut-on en
décider ?**

## L'arrêt du lot — **le nombre ne désignait pas ce qu'il avait l'air de désigner**

Une fois les 30 chaînes nommées, la lecture de leurs chemins tranche :

```text
chaînes relevées                                      30
   2ᵉ niveau = MÉTHODE ou PROPRIÉTÉ JAVASCRIPT        14
      `.map` · `.forEach` · `.filter` · `.length` · `.toLowerCase`
   2ᵉ niveau = VRAIE SOUS-CLÉ du contrat              16
```

`f.stages.map(…)`, `st.warnings.map(…)`, `r.steps.map(…)` ne lisent **rien** du
contrat au second niveau : ce sont des méthodes de tableau. Publier « 30 accès
imbriqués au contrat » aurait surestimé de **quatorze**.

**Arrêtés avant publication : 182 → 183 (+1).**

## L'alarme 557-C, levée par la mesure — et non par un raisonnement

Mon relevé donne **30** chaînes là où le 553 annonçait **35**. Un total qui
baisse après un enrichissement de l'instrument est un signal d'alarme (557-C).
Vérification faite en reproduisant **la convention du 553 elle-même** — une
unité par position de second niveau, ambiguïté comprise :

```text
convention du 553, marquage du 553   35
convention du 553, marquage du 557   43
```

**Le compte monte.** Ce n'était pas une perte de couverture mais un
**changement d'unité** : mes 30 comptent des **chaînes entières et non
ambiguës**, et **10 chaînes ambiguës** sont écartées à part. La calibration du
banc échoue si ce nombre baisse — c'est un contrôle, pas un commentaire.

## Les 16 vraies sous-clés

```text
/api/ai/enrichment       surfaces.news · surfaces.quotes            gardées
/api/briefing/editorial  daily.main_risk                            gardée
/api/market/regime       adjustments.new_risk_allowed               gardée
/api/market/summary      breadth.above200                           gardée
/api/skyler/calibration  brier.reason                               gardée
/api/skyler/memory       aggregates.by_engine_version · ledger_health.status  gardées
/api/skyler/memory       ledger_health.basis                        NUE
/api/system-status       scan.symbols                               gardée
/api/system/diagnostics  ai.total (×2, une gardée une nue) · tradingview.stored
                         (×2, idem) · ai.ok · scan.rows             4 NUES
```

**11 gardées, 5 nues.** Une chaîne « gardée » est protégée par un `&&` dont la
gauche lit un préfixe strict (`snap && snap.surfaces && snap.surfaces.quotes`)
ou par un chaînage optionnel : une sous-clé absente ne jette pas d'exception.

## Ce que le croisement peut décider — et ce qu'il ne peut pas

```text
vraies sous-clés                                      16
   dont la route a un contrat MESURÉ au 552            4
      dont la TÊTE du chemin est SERVIE                4
      dont la TÊTE est hors du contrat lu              0
   dont la route n'a AUCUN contrat mesuré             12
```

Les quatre décidables — `breadth.above200`, `adjustments.new_risk_allowed`,
`brier.reason`, `scan.symbols` — ont **toutes leur tête servie**. Aucune
divergence.

**Et le second niveau n'est PAS croisable** : le 552 n'a relevé que les clés de
**premier** niveau. Aucune sous-clé n'est déclarée existante **ni inexistante**
(550-B, 546-A). **Douze des seize portent sur des routes dont je n'ai jamais
mesuré le contrat** — `/api/ai/enrichment`, `/api/system/diagnostics`,
`/api/skyler/memory`, `/api/briefing/editorial`. Elles ne sont pas autorisées à
l'appel, et elles ne l'ont pas été.

## Second contrôle (481)

```text
chaînes de profondeur >= 3                             0
chaînes NUES (aucune garde `&&` ni `?.`)              16 sur 30 · 5 sur les 16 sous-clés
chaînes AMBIGUËS écartées                             10 · dont 7 vraies sous-clés
chemins cassés par un maillon construit                0
```

Le **zéro de profondeur 3** est un résultat, pas une absence de mesure : le
produit ne descend jamais à trois niveaux sur une valeur de route.

Les **10 ambiguës** viennent des collisions de nom déjà nommées au 556/557 —
`pk.data.age_s` quatre fois, `s.leader.symbol` deux fois, `st.nav_history.length`
partagée entre `/api/ai/status` et `/api/system-status`. Elles sont **comptées à
part, jamais attribuées**.

## Ce que le dépôt fait bien, mesuré

- **Aucune tête de chemin ne sort du contrat servi**, sur les quatre cas
  décidables.
- **Zéro chemin cassé par un accès construit** : tout ce que la page lit en
  profondeur est nommé en clair.
- **Zéro profondeur 3** : les structures lues restent plates.
- **11 des 16 sous-clés sont gardées** — une absence de sous-clé ne casse pas la
  page.

## Portée — ce que ce lot NE dit PAS

- **Le second niveau n'est pas confronté au serveur.** Rien n'est conclu sur
  l'existence des sous-clés.
- **Les 5 chaînes nues ne sont pas un défaut arbitré** : une lecture nue peut
  être sûre si la valeur est garantie en amont — non vérifié.
- **Les 8 pages seulement**, corpus du 553.
- **Aucune route appelée, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0**.

Aucun dossier. Ce lot solde une dette de cinq lots, et la règle 557-A a
fonctionné dès sa première application : un chiffre du second contrôle, repris
au sérieux, a livré seize sous-clés jamais nommées et un angle mort de douze
routes.

Mais il faut dire l'autre moitié : **le chiffre lui-même était trompeur.** Les
« 35 accès imbriqués » mélangeaient des lectures de contrat et des `.map()` sur
des tableaux. Un compteur qui agrège deux natures différentes ne devient pas
juste en grossissant — il devient seulement plus difficile à contredire.

Trois règles neuves :

- **558-A · UN ACCÈS AU SECOND NIVEAU N'EST PAS FORCÉMENT UNE LECTURE DE
  CONTRAT** — 14 des 30 étaient des méthodes JavaScript. Séparer les natures
  avant de publier le nombre.
- **558-B · UNE ALARME SE LÈVE PAR REPRODUCTION, PAS PAR RAISONNEMENT** — face
  à 30 contre 35, la seule réponse acceptable était de recompter *sous la
  convention d'origine* : 43.
- **558-C · CE QUI N'A PAS DE CONTRAT MESURÉ NE PEUT PAS ÊTRE CONFRONTÉ** —
  douze des seize sous-clés portent sur des routes hors de mon périmètre ; les
  nommer est tout ce que la lecture autorise.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 16 sous-clés, dont 12 sur des routes au contrat
non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35
clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans lecture
observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions de nom** ;
**les 3 ombres de `briefing.py`** ; **les 5 routes affamées hors intersection du
556** ; **les 14 candidates du 554, en attente d'un GO** ; **les 4 routes
construites `/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`,
hors corpus** ; **les 7 routes sans filet du 554/555** ; **les 21 tests de membre
ambigus du 551** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly`
rend un objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **les SEPT chiffres
lourds encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC serveur, jamais observé** ;
**les 4 noms de clé du 542** ; **les 15 messages d'erreur du 541** ; **les 95
atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 183 (+1)** ; publiés
puis corrigés **28** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
