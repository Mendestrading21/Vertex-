# SKYLER LOT 435 — La décision du jour est calculée sur zéro titre, et personne ne la lit : je referme le point laissé « non conclu » au 434

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-435` (base : lot 434 fusionné,
e9478f0)

Dix-huitième lot de la veine. Le 434 avait laissé **une seule** candidate
explicitement **non conclue** : « Aucune opportunité retenue par le comité. » sur
`/`, dont le chemin `/api/command` n'avait pas été exécuté. Ce lot l'exécute.

**Aucun code, aucun gardien, aucun test.**

## Ce que `/api/command` rend quand rien n'a été scanné

L'endpoint appelé pour de vrai via `test_client` (lecture seule, aucune
écriture) :

```text
/api/command → 200 · scan vide au démarrage : True

top_stocks   []
counts       {}
decision     {'action': 'ATTENDRE / SÉLECTIF',
              'msg': "Peu d'avantage statistique — n'acheter que l'exceptionnel, garder du cash."}
risk         {'n': 0, 'note': 'panier trop petit pour une analyse de corrélation'}
validation   {'ok': False, 'note': 'historique trop court pour valider'}
```

**Trois champs, trois attitudes.** `risk` et `validation` **avouent** qu'ils
manquent de matière — chacun avec sa phrase, écrite exprès. `decision`, lui,
**tranche** : « Peu d'avantage statistique », affirmation sur l'avantage
statistique du marché, produite à partir de **zéro observation**.

Le code, `vertex/app/routes/command.py:93-104` :

```python
n_act = len(top_stocks)
if roro == 'RISK-OFF' or reg == 'CHOP':      decision = {'action': 'RÉDUIRE / DÉFENSIF', …}
elif n_act >= 2 and (score or 0) >= 55:      decision = {'action': 'ATTAQUER', …}
else:                                        decision = {'action': 'ATTENDRE / SÉLECTIF',
                                                          'msg': 'Peu d\'avantage statistique …'}
```

Scan vide → `n_act = 0`, `score = None` → **le `else` final**. Il n'existe aucune
branche « je ne peux pas décider ». Les deux champs voisins en ont une chacun.

## Mais est-ce AFFICHÉ ? — et la réponse renverse le lot

Mesuré sur les octets servis :

```text
« ATTENDRE / SÉLECTIF »        AUCUN OCTET SERVI
« ATTAQUER »                   AUCUN OCTET SERVI
« RÉDUIRE / DÉFENSIF »         AUCUN OCTET SERVI
« Peu d'avantage statistique » AUCUN OCTET SERVI

/api/command appelé depuis `/` :        4 sites
   loadSummary → paint(sum, reg, cmd)   cmd.top_stocks ×2, « decision » ABSENT de paint
   loadOpportunities                    cmd.top_stocks
   loadAlerts                           cmd.alerts
```

**Le champ `decision` n'est lu par aucun consommateur servi.** La décision du
jour est calculée, sérialisée, envoyée au navigateur — et jamais rendue.

**Rang 4**, donc : défaut réel dans le moteur, **sans conséquence à l'écran**.
C'est la règle du 411/424 appliquée contre moi-même : j'avais là une phrase
spectaculaire, la chaîne dit qu'elle n'atteint personne, et c'est ce qu'il faut
écrire.

## Et la question du 434, elle, est refermée

« Aucune opportunité retenue par le comité. » est rendue quand `top_stocks` est
vide — donc **aussi quand aucun titre n'a été scanné**. La formule « retenue par
le comité » suppose une évaluation qui n'a pas eu lieu. Même famille que le 434.

Vérification de l'atténuation (critère posé au 434) : le voisinage rendu de la
carte — en-tête « Meilleures opportunités », lien « Toutes → », conteneur
`vx-opp-stocks` — **ne porte aucun compte de titres scannés**. **Pas d'atténuation.**

C'est donc, comme `renderAnomalies` au 434, une confusion **non atténuée** — mais
plus légère : la phrase ne prétend pas qu'une **détection** a eu lieu, seulement
qu'une sélection n'a rien retenu. **Rang 2.**

## Un troisième instrument fautif en deux lots, et je le dis

Ma première mesure des consommateurs a rendu **« 0 appel à `/api/command` dans
les octets servis »**. Faux : il y en a **16** (4 sites × 4 vues de `/`). Cause :
le motif `.{170}` autour de la cible, **sans `DOTALL`** — le point ne franchit
pas les retours à la ligne, et le JS servi en contient.

C'est la **troisième** fois en deux lots qu'un balayage rend une ligne propre et
fausse (434 : deux fois). Et une fois de plus, **le faux résultat allait dans le
sens de ma thèse** — « personne n'appelle cet endpoint » aurait fait un titre
plus fort. Le comptage littéral l'a démenti.

## Classement

- **La décision du jour sans données** → **rang 4** : le moteur tranche là où ses
  deux voisins avouent, mais **le champ n'atteint aucun écran**.
- **« Aucune opportunité retenue par le comité. »** → **rang 2** : confusion
  réelle et non atténuée, conséquence plus légère que celle du 434.

Correction pressentie pour la première, dans le style de ses propres voisins :
une branche `if not detail: decision = {'action': '—', 'msg': "univers non
scanné — aucune décision"}`, exactement comme `risk.note` et `validation.note`.
**Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne mentionne « ATTENDRE / SÉLECTIF » : **aucun gardien.**

## Portée

Une candidate refermée sur les 47 phrases du 433 ; **39 restent non vérifiées**.
Je n'ai ouvert qu'un seul champ de `/api/command` — `counts`, `exposure`,
`regime`, `portfolio_score`, `alerts` sont **servis et non vérifiés**.

La mesure est faite **sur le scan vide du démarrage**, état réel mais unique : je
n'ai **pas** fait tourner un scan pour observer la bascule vers `ATTAQUER`. Le
témoin est donc **lu dans le code**, pas exécuté — et je le dis plutôt que de
présenter la lecture comme une mesure.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. L'appel à `/api/command` est une lecture ; `persist`
  redirigé vers un répertoire temporaire.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-huitième lot court. Séquence : **432 ✓ · 433 ✓ · 434 ✓ (bornage qui
trie) · 435 ~**.

Ce lot ferme proprement un point que le précédent avait laissé ouvert, et il le
ferme **contre l'intuition** : la phrase la plus frappante que j'aie trouvée
depuis plusieurs lots — un terminal qui conseille « garder du cash » sur zéro
titre analysé — **n'arrive pas jusqu'à l'écran**. La trouvaille reste, mais au
rang qui lui revient.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
