# SKYLER LOT 455 — La veine des phrases composées refermée : 11 dernières phrases tranchées, et la toute dernière cache un défaut affiché — « 0 contrôle défavorable, 1 à surveiller, sur 6 » quand **5 des 6 sont INCONNUS**

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-455` (base : lot 454 fusionné,
b6eddd0)

Trente-sixième lot de la veine, cinquième de la tranche 450-459. Le 454 avait
conclu franchement que la veine des phrases composées rendait **surtout du poids
mort** — trois lots d'affilée sans écran. Ce lot la **solde** : les 11 phrases
restantes, en un seul balayage, avec l'instrument déjà écrit et validé.

**Aucun code, aucun gardien, aucun test.**

## Les 11 dernières, tranchées

Détecteur AST **aux quatre formes dès la première passe** (leçon 454) ; affichage
d'abord sur le **corpus des 42 objets servis** ; payload identifié par sa forme.

```text
champ       producteur                          verdict
impact      options_lab.py:788                  NON AFFICHÉE — /api/options-lab citée nulle part
summary     ai/fallback.py:34                   JAMAIS PRODUITE — module non atteignable (452)
summary     decide.py:128                       NON LUE — même payload que l'`action` du 454
summary     decision_memory.py:546              NON LUE — aucune lecture `.summary` sur ce payload
summary     analysis_api.py:498, :501           NON ÉTABLIES (2) — branche MESURE, non atteinte
summary     widget_lab.py:1759                  AFFICHÉE — bandeau de curation de /widget-lab
question    knowledge_graph.py:355, :360, :366  AFFICHÉES (3) — carte de /portfolio
narrative   pretrade.py:163                     AFFICHÉE — carte pré-trade de /analysis/<sym>

               11 tranchées · 5 affichées · 4 non affichées ou jamais produites · 2 non établies
```

**Les deux `summary` de `analysis_api` sont NON ÉTABLIES, pas absentes.** La route
`/memory/cell/<g>/<k>` rend **404** au démarrage — mais son 404 est une page
honnête (« Cellule inconnue — aucune décision mesurée ne la forme »). Les deux
phrases vivent sur la branche `MESURE`, que `scan_state` vide n'atteint pas.
**C'est la leçon 438 : je les nomme et je ne les compte pas** (règle 448).

### Toutes les lectures voisines appartiennent à d'autres payloads

Neuvième récidive du piège de nom, et elle est massive sur ces quatre champs :

```text
.impact     lu 4 fois — anomalie (x.impact), stress (v.impact_pct), news (n.impact)
.summary    lu 4 fois — analyste (su.summary), contrat de carte (opts.summary), tracking
.question   lu 6 fois — dont 5 = contrat de CARTE VXCharts (opts.question)
.narrative  lu 6 fois — éditorial (ed.narrative), scanner d'anomalies (d.narrative)
```

Une seule lecture de `.question` sur les six correspond à la forme de
`knowledge_graph` (`{symbol, kind, status, question}`) : `portfolio_page.py:862`,
`qs.map(x => … esc(x.symbol) + ' — ' + esc(x.question))`, nourri par
`d.research_questions`. **C'est la forme qui tranche, jamais le nom.**

## Les trois `question` : exactes

```python
'Quels sont les fournisseurs, clients et concurrents critiques de %s ?
 Aucune source branchée — relation jamais inventée.'          # inconditionnelle
'%s est hors watchlist sectorielle — quel est son secteur réel ?'   # if not sector_map.get(s)
'Aucun catalyseur daté ≤ %d j connu pour %s — lequel manque au calendrier ?'  # if not dated
```

Les deux dernières **impriment littéralement leur propre garde** — c'est une
**lecture**, pas une mesure (règle 447). La première est inconditionnelle : elle
affirme « aucune source branchée » pour **tout** symbole. Vérifié — **aucune
source de chaîne de valeur n'existe dans le dépôt** ; l'affirmation est vraie.
Carte titrée « Questions de recherche (relations non documentées — jamais
inventées) ». **Rien à signaler.**

## La trouvaille : la phrase pré-trade compte les défavorables, jamais les inconnus

`pretrade.py:163`, rendue sur `/analysis/<sym>` par `analysis_page.py:850`
(`esc(d.narrative||'')`, carte `an-pretrade`, après un clic utilisateur avec un
montant) :

```python
n_ko   = statuses.count(KO)
n_warn = statuses.count(WARN)
narrative = ('Vérification pré-trade %s : %d contrôle(s) défavorable(s), '
             '%d à surveiller, sur %d. …' % (sym, n_ko, n_warn, len(checks)))
```

**Il n'existe aucun `statuses.count(UNKNOWN)`.** Le dénominateur est le total, les
deux numérateurs ne couvrent que deux statuts sur quatre.

**Banc sur le moteur réel `pretrade.build()`, cas dégradé et cas sain côte à côte :**

```text
A. ÉTAT DU DÉMARRAGE — rien de branché
   statuts réels        inconnu 5 · attention 1
   badge affiché        MITIGÉ
   phrase affichée      « 0 contrôle(s) défavorable(s), 1 à surveiller, sur 6. »
   ce que le lecteur soustrait :  6 − 0 − 1 = 5 contrôles « qui vont bien »
   ce qu'ils sont vraiment     :  5 contrôles IMPOSSIBLES À ÉVALUER

C. TOUT BRANCHÉ — R:R 3:1, position gagnante
   statuts réels        ok 3 · attention 2 · defavorable 1
   phrase affichée      « 1 contrôle(s) défavorable(s), 2 à surveiller, sur 6. »
   les 3 restants sont VRAIMENT ok — la phrase tombe juste
```

**Le cas sain tombe exactement juste.** C'est le même gabarit de phrase qui, dans
le cas A, invite à conclure l'inverse de la réalité. La phrase **ne peut pas
distinguer 3 contrôles réussis de 5 contrôles inévaluables**.

Et le cas A **n'est pas un cas de bord** : au démarrage, `scan_state` est vide —
verdict du comité, régime, GEX, résultats et concentration sont tous `inconnu`.
**C'est l'état normal du produit tant qu'aucun scan n'a tourné.**

### Pourquoi rang 2, et pas rang 1

C'est la famille 432/433 — *une synthèse qui range l'INCONNU avec le SAIN ment du
côté qui rassure*, qui y valait rang 1. **Ici je descends d'un cran, et je dis
pourquoi** : l'information honnête est **co-visible**. Les six contrôles sont
rendus **juste au-dessus** de la phrase, chacun avec son icône de statut et un
détail qui nomme ce qui manque — « Régime indisponible », « Date de résultats
inconnue », « Titre hors du scan courant — aucun verdict ». Aux 432/433, cette
correction n'existait pas à l'écran.

**L'atténuation n'efface pas** (règle 442) : la phrase est la **conclusion** de la
carte, la ligne qu'on lit en dernier et qu'on retient. Elle donne un total et en
cache la moitié.

**Rang 2.** Correction pressentie : ajouter `statuses.count(UNKNOWN)` à la phrase
— une ligne, dans un fichier, sans moteur. **Aucun GO, rien n'est engagé.** Aucun
test ne compare la phrase aux statuts réels : **aucun gardien.**

### Ce que le lot ne prétend pas

`n_ko` et `n_warn` sont **exacts**, et `statuses` dérive de la liste `checks`
elle-même rendue : **rien de faux n'est affiché**, c'est une **omission**. Je le
dis pour que le classement ne soit pas sur-lu (règle 451/454).

## L'état de la veine

```text
carte du 444 : 38 champs distinctifs, 110 phrases concluantes
tranchées à ce jour : basis (445) · measure (446) · detail (447) · reason (448-449)
                      source (451) · action (454) · impact + summary + question
                      + narrative (455)

TOUS les champs annoncés à 3 écrans ou plus sont désormais tranchés.
Restent de la liste nommée : `volume` et `spread_pct` (1 phrase chacun, 1 écran).
72 des 110 phrases concluantes restent fermées.
```

**Bilan de la veine, sur les 8 champs ouverts** : **2 rang 1** (447 max pain,
452 par ricochet), **2 rang 2** (448/449 les vidages, 455 la phrase pré-trade),
**1 famille entièrement saine** (445), et **le reste en poids mort**. La veine ne
s'éteint pas sur un échec : elle s'éteint sur un rang 2 trouvé au dernier lot.

## Portée

- Un GET sur `/api/options-lab` n'a **pas** été tenté : la conclusion « citée
  nulle part » porte sur la **présence de l'URL littérale dans les octets
  servis** (méthode 454), pas sur la réponse de la route.
- Le banc appelle le **moteur réel** sur des entrées **fabriquées** : il établit
  le comportement du **code**, pas la fréquence des cas réels. Le cas A reproduit
  toutefois l'état effectif du démarrage, `scan_state` étant vide.
- Déstructuration, crochets et helpers à paramètre **échappent** au comptage des
  lectures de champ (leçon 436) — **non quantifiés**.
- **Aucun navigateur ouvert.** La chaîne d'affichage de la phrase pré-trade est
  établie sur les octets servis (`analysis_page.py:850`, line-exact) et sur le
  code du producteur.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `pretrade.build()` appelé en mémoire (fonction pure) ;
  routes en **GET** ; `persist` redirigé ; **`/options/<sym>`, `/api/analyst/` et
  `/api/correlations/` volontairement NON appelées** (réseau sortant).
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-huitième lot court, cinquième de la tranche.

La consigne du réveil était de solder la veine et, si elle se soldait vite,
d'enchaîner plutôt que de publier un lot maigre. Elle ne s'est pas soldée vite :
**la onzième et dernière phrase portait un défaut affiché**, et c'est elle qui a
demandé le banc. Le lot n'avait pas besoin d'être enchaîné.

L'enseignement de méthode est net et il contredit à moitié le 454 : la veine
rendait du poids mort **parce que les champs examinés étaient choisis par leur
nombre d'écrans annoncé** — un chiffre de la carte du 444 qui, on le voit ici,
**compte des homonymes**. Les quatre champs de ce lot étaient annoncés à 3 écrans
(`impact`), 4 (`narrative`) et 1 (`summary`, `question`) ; le défaut était dans
celui annoncé à **4 écrans dont 5 lectures sur 6 sont des homonymes**.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **25** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
