# SKYLER LOT 549 — **L'angle mort tombe de 67 à 43**, et le témoin négatif du brief était faux : `/bordel` est bel et bien appelé par un test, dans une boucle sur des littéraux. Correction d'une phrase du 548

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-549` (base : lot 548 fusionné,
`89297264`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(t)** — le 548 a publié **67 points d'entrée couverts par personne** en disant
que c'était une **borne haute** : **90 appels à chemin construit** n'avaient pas
été résolus. Ce lot les résout.

## L'arrêt du lot — **le témoin négatif du brief était faux, et il dénonçait une erreur du 548**

Le brief proposait `/bordel` comme exemple de route qu'aucun test n'atteint.
Lecture du code **avant** d'écrire une ligne d'instrument :

```python
# tests/test_smoke.py:49
for path in ["/", "/brief", "/review", … "/bordel", "/settings"]:
    assert c.get(path, follow_redirects=True).status_code == 200, path
```

**`/bordel` est appelé par un test.** L'appel s'écrit `c.get(path)` où `path`
est la variable d'une **boucle sur une liste de littéraux** — donc, pour le
crible du 548, un « chemin construit », donc non compté.

**Et c'est exactement le motif qui appelle les redirections héritées**, la
famille que le 548 mettait en avant. L'instrument de ce lot n'est donc pas le
préfixe : c'est la **résolution des boucles sur littéraux**.

**Arrêtés avant publication : 168 → 169.**

## Correction d'une phrase du 548

Le 548 écrivait, à propos des 36 redirections héritées : *« Aucun test ne
vérifie qu'elles redirigent. »* **C'est faux pour seize d'entre elles** :
`tests/test_smoke.py` les appelle avec `follow_redirects=True` et exige un 200.
Le chiffre **67** restait juste — le 548 l'avait explicitement donné comme
**borne haute**, et la présente mesure est le resserrage annoncé — mais cette
phrase-là, non.

**Publiés puis corrigés : 23 → 24.**

## Deux mécanismes, deux statuts — jamais mélangés

- **RÉSOLU EXACTEMENT** — la variable est la cible d'une boucle dont l'itérable
  est une liste de chaînes littérales. Appariement ensuite **par la règle**
  (546-A). **Aussi solide qu'un littéral.**
- **ATTEINT PAR PRÉFIXE** — `'/api/skyler/' + s` : on ne connaît que le début.
  **Borne haute de couverture, donc borne basse d'angle mort.**

```text
appels à chemin non littéral, triés
   RÉSOLUS EXACTEMENT (boucle sur littéraux)         22
   ATTEINTS PAR PRÉFIXE (au moins un segment)        31
   préfixes ÉCARTÉS (trop courts, garde 548-A)        7
   SANS LIAISON résoluble (comptés à part)           33
```

```text
chemins littéraux distincts tirés des boucles        83
points d'entrée couverts par ces boucles             54
préfixes distincts retenus                            5
points d'entrée ATTEINTS par un préfixe              13
   /api/skyler/ 10 · /api/skyler/memory/ 4 · /memory/ 2 · /analysis/ 1 · /api/skyler/graph/ 1
```

## La garde du 548-A — **et ce qu'elle a coûté, mesuré**

Un préfixe trop permissif (`'/'`, `'/api/'`) **effacerait** l'angle mort. La
garde exige donc au moins un segment complet. Sept préfixes sont écartés
(`'/journal?view='`, `'/intelligence?view=%s'`, `'/options?view='`,
`'/opportunities?view=radar&%s=%s'`).

**Une garde qui écarte à tort laisse une route dans l'angle mort.** On ne l'a
pas supposé, on l'a mesuré :

```text
points d'entrée désignés par ces 7 préfixes           4
   parmi eux, encore dans les 43 restants             0
VERDICT : la garde n'a rien coûté
```

## Le résultat — **67 → 43**

```text
couverts par PERSONNE, annoncé au 548                67
   en fait couverts, boucle sur littéraux (CERTAIN)  24
   peut-être atteints par un préfixe (INCERTAIN)      0
   restent couverts par PERSONNE                     43

borne basse (on croit les préfixes)                  43
borne haute (on ne les croit pas)                    43
```

**Les deux bornes coïncident** : aucun des 43 n'est effleuré par un préfixe. Le
resserrage ne doit **rien** à l'incertitude — il vient entièrement de la
résolution exacte.

```text
les 43, par famille
   redirections héritées      20   (36 au 548, dont 16 rattrapées)
   points d'entrée /api/…     19
   autres                      4   /ibkr · /options/<sym> · /quotes · /weekly-regen
```

## Une nuance qu'il faut dire

**`/intelligence` et `/tracking` sont appelés par la suite de tests** —
`tests/test_full_system_integration.py:155` exige un 200 sur `/tracking`. Ils ne
sont donc dans aucun des 43. Ce que je n'ai jamais fait, c'est **mesurer leurs
octets servis moi-même** ; le 546 disait « jamais dans mon corpus », et cela
reste exact. Mais « jamais appelées par personne » serait faux, et je ne veux
pas que la demande de GO repose sur une exagération.

## Ce que le dépôt fait bien, mesuré

- **`test_smoke.py` appelle 16 redirections héritées** et exige un 200 après
  redirection : le filet existait, c'est mon crible qui ne le voyait pas.
- **83 chemins littéraux** vivent dans des listes parcourues en boucle — un
  idiome de test compact et lisible, que seul un lecteur d'arbre retrouve.
- **Aucun des 43 n'est effleuré par un préfixe** : le résultat ne dépend
  d'aucune approximation.

## Portée — ce que ce lot NE dit PAS

- **43 reste une BORNE HAUTE** : **33 appels sans liaison lisible** (`url`,
  `route`, `p`, `path`, un `Subscript`, un `Call`…) ne sont **jamais** convertis
  en couverture. Ils peuvent atteindre n'importe quelle règle.
- **« Couvert » ne veut toujours pas dire « bien testé »** : `test_smoke.py`
  vérifie un code 200, rien de plus.
- La résolution de boucle ne couvre que l'itérable **littéral** ou une constante
  de module littérale ; une liste construite reste invisible.
- **Aucun appel réseau, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans chaque banc.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés pendant le lot** (`ai_enrichment.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. L'angle mort perd un tiers de sa taille en un lot, **et le
resserrage vient d'une mesure exacte, pas d'une hypothèse**.

Ce qu'il faut dire sans le maquiller : **le brief m'a donné un témoin négatif
faux pour la troisième fois**, et cette fois il pointait une erreur réelle de
mon lot précédent. Une phrase du 548 — « aucun test ne vérifie qu'elles
redirigent » — était fausse pour seize routes. Le chiffre était protégé par son
étiquette de borne haute ; **la phrase, elle, ne l'était pas**. C'est la
différence entre un chiffre prudent et une prose qui ne l'est pas.

Trois règles neuves :

- **549-A · UNE VARIABLE DE BOUCLE N'EST PAS UN CHEMIN INCONNU** — 22 appels
  et 83 chemins littéraux se cachaient derrière un `for path in [...]`.
- **549-B · UN CHIFFRE PRUDENT NE PROTÈGE PAS LA PHRASE QUI L'ENTOURE** — le
  67 était donné comme borne haute ; « aucun test ne vérifie » ne l'était pas.
- **549-C · UNE GARDE SE MESURE AUSSI** — la garde anti-préfixe-permissif a
  écarté 7 préfixes ; on a vérifié qu'aucun des 43 ne lui échappait, au lieu de
  l'affirmer.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 43 points d'entrée couverts par personne, dont
20 redirections héritées — borne haute, 33 appels restent irrésolus** ; **les 11
identifiants de `/intelligence`, `/tracking` et `pf-risk-gauge` — en attente
d'un GO** ; **les 4 zones sous attente sans annonce du 545 — candidat, non
arbitré** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** (112 atténuations,
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

Comptes séparés : résultats faux **arrêtés avant publication 169 (+1)** ; publiés
puis corrigés **24 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
