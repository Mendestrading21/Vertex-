# SKYLER LOT 465 — Les deux dettes du 464 soldées, toutes deux en NÉGATIF : l'élargissement du détecteur ne trouve AUCUN nouvel accumulateur, et l'alerte déclenchée par un prix de démo n'atteint aucun écran parce que son consommateur n'est pas servi

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-465` (base : lot 464 fusionné,
09a3215)

Quarante-cinquième lot de la veine, cinquième de la tranche 460-469. Le 464 a
rendu un rang 1 **et laissé deux dettes explicites**. Un lot qui solde vaut un
lot qui ouvre (modèle 449/455/457/459).

**Les deux dettes sont soldées. Toutes deux en négatif.**

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Deux critères **repris du 464 et reposés explicitement** : **(C1)** ne compte que
ce qui persiste de la donnée **dérivée du marché** ; **(C2) écraser n'est pas
accumuler** — seul un journal peut perpétuer.

Mécanismes cherchés, **liste posée d'avance** : `save_json` (le détecteur du
464), `open(…, 'w'/'a'/'x')`, `Path.write_text/bytes`, `json.dump` / `pickle.dump`,
`shutil.copy*`/`move`, `os.replace`/`rename`, `csv.writer`, `to_csv`/`to_json`.

Exclus d'emblée, nommés : **`vertex/services/persist.py` lui-même** — c'est la
**primitive**, l'y compter reviendrait à compter le mécanisme — et `tests/**`.

## Dette (ii) — combien d'écrivains le détecteur du 464 avait-il manqués ?

```text
détecteur du 464 (save_json seul)        28 sites
détecteur ÉLARGI                         46 sites          +18
   M1 save_json        28      M4 json.dump / pickle   6
   M2 open(w/a/x)       8      M5 shutil.copyfile      1
   M3 Path.write_*      2      M6 os.replace           1
```

**Contrôle obligatoire, double, passé dès la première exécution** :
`track_record.record` retrouvé **par ses deux mécanismes** (`open(…,'a')` ligne
45 *et* `save_json` ligne 64 pour son méta) — c'est bien lui que le 464 avait
manqué ; `gex_history.record` retrouvé.

### Les 18 sites manqués font 11 écrivains distincts — et je les ai lus un par un

```text
écrivain                                   ce qu'il persiste            verdict
track_record.record        edge_ledger     verdicts du scan             DÉJÀ TROUVÉ au 464
config._local_secret       .vertex_secret  secret local                 SANS OBJET
desk._backup_desk          desk_backup_*   donnée UTILISATEUR           SANS OBJET
constitution.propose_…     version V(n+1)  CONFIGURATION                SANS OBJET
company._save              company_cache   fondamentaux                 CACHE — écrase
constituents._save_cache   cache d'indices composition                  CACHE — écrase
analyst_deep._save_cache   cache notes     notes d'analystes            CACHE — écrase
terminal.desc_ep           cache descript. descriptions (fetch réussis)  CACHE — écrase
daily.save_state           daily_prev      cur + prev                   FENÊTRE DE 2 JOURS
weekly.save_snapshot       weekly_snapshot 1 par semaine ISO, os.replace ÉCRASE
strategy/memory/store      —               —                            JAMAIS INSTANCIÉ
```

**Résultat : sur les onze écrivains que le détecteur du 464 avait manqués, ZÉRO
est un nouvel accumulateur de donnée de marché.** Trois sans objet, quatre
caches, un snapshot écrasé atomiquement, une fenêtre bornée à deux jours, un mort,
un déjà trouvé.

**Le compte du 464 — sept accumulateurs — TIENT. L'élargissement ne l'augmente
pas.** C'est le meilleur résultat qu'une dette d'instrument puisse rendre : la
mesure précédente était **complète pour ce qu'elle prétendait mesurer**.

### Deux faits mesurés qui méritent d'être nommés

**`strategy/memory/store` n'est instancié NULLE PART en production** — mesuré,
aucun `MemoryStore(` hors `tests/`. Son `_persist()` n'écrit donc jamais rien.
C'est un **écrivain mort**, et je le dis plutôt que de le compter.

Et il porte pourtant **une garde exemplaire** : `add()` refuse le statut actif
sans `confirmed_by_human=True` (`PermissionError`), et `active()` ne retourne que
les entrées `CONFIRMED`. **Second témoin positif de la veine** — mais un témoin
de **conception**, pas d'exécution, et il garde l'**activation**, pas la
**provenance**. Je ne le compte pas comme une garde de démo.

**`daily.save_state` conserve `prev` — la veille.** Un jour de démo peut donc
survivre **un jour** dans le « Diff marché depuis la dernière session » de `/`.
C'est borné à deux fentes, ce n'est **pas** de la perpétuation au sens du 463.
**Nommé, non classé.**

## Dette (i) — `alerts_fired.json` : non gardé, mais sans consommateur servi

Le 462 l'avait pressenti, le 464 l'avait nommé sans le trancher. Mesuré :

```text
_alert_price(sym)   IBKR si connecté, SINON scan_state['detail'][sym]['price']
                    → en DEMO, un prix SYNTHÉTIQUE
_ALERTS_FIRED[aid]  {'id','sym','cond','level','price','ts','note'}
                    → AUCUN champ de provenance
_save_json('alerts_fired.json', …)   accumule, borné à 200, aucune expiration
boucle              `if aid in _ALERTS_FIRED: continue`
                    → une alerte déclenchée n'est PLUS JAMAIS réévaluée
```

**Sur le papier, c'était un rang 1** : un prix synthétique consomme
définitivement une alerte réelle de l'utilisateur, et `vx_kit.py:292` écrit
`al.fired=true; al.active=false; al.firedPrice=f.price` — l'alerte est désactivée
et estampillée d'un prix fabriqué.

**Et c'est faux, parce que ce consommateur n'est pas servi.**

```text
recherche de l'URL LITTÉRALE dans les 42 objets servis (règle 454/455)
   /api/alerts/status   →  AUCUN OBJET SERVI
   firedPrice           →  AUCUN OBJET SERVI
   al.fired             →  AUCUN OBJET SERVI

routes d'alertes déclarées côté serveur   /api/alerts/active · /api/alerts/status
                                          /api/positions/alerts
routes d'alertes CITÉES dans les octets servis   /api/alerts/active
                                                 /api/positions/alerts
```

`vx_kit.py` est le module dont le CLAUDE.md du dépôt dit qu'il **n'atteint aucune
des 8 pages**. La chaîne existe **dans le code**, elle **ne s'exécute pas dans le
produit servi**.

**Verdict : `alerts_fired.json` est NON GARDÉ — l'écriture a bien lieu — mais la
CONSÉQUENCE n'atteint aucun écran. Règle 442/445 : je ne le classe pas.**

### Le faux que j'ai arrêté, et il était à une inférence de la publication

J'avais la chaîne complète, le mécanisme, la ligne de code du client et la
conséquence — « une alerte réelle consommée par un prix de démo ». **Il ne
manquait qu'une vérification : l'URL est-elle citée dans les octets servis ?**
Elle ne l'est pas.

C'est la règle 454/455 qui a payé, et elle a payé **contre moi**. **Un faux
arrêté avant publication. Total : 33 → 34.**

## Ce que le lot ne prétend pas

- Les onze écrivains sont classés **par lecture** de leur corps, pas par
  observation d'un cycle réel. Pour `weekly.save_snapshot` et `daily.save_state`,
  « écrase » est établi sur `os.replace` et sur la structure à deux fentes.
- Le détecteur élargi couvre **huit mécanismes nommés d'avance**. Une écriture
  par un neuvième — un sous-processus, une bibliothèque tierce, un `exec` —
  échapperait encore. **Non quantifié**, mais la marge s'est réduite : le
  précédent élargissement n'a rien ajouté à la population.
- **Aucun fichier runtime n'a été ouvert.** `alerts_fired.json`,
  `edge_ledger.jsonl`, `weekly_snapshot.json` existent sur le disque et leur
  contenu n'était nécessaire à aucune des deux démonstrations.
- L'absence de consommateur servi est établie sur les **42 objets servis**
  mesurés ce lot. Une page hors de ce corpus — il n'y en a pas dans la
  navigation — échapperait.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Analyse **`ast`** et routes en **GET** uniquement ;
  `persist` redirigé ; **aucun écrivain appelé ce lot** ; **`/options/<sym>`,
  `/api/analyst/` et `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-huitième lot court, cinquième de la tranche.

Un lot **entièrement négatif**, et c'est ce qu'on lui demandait. Les deux dettes
du 464 sont closes **dans le sens qui resserre** : l'instrument du 464 était
complet, et le cas qu'il avait laissé en suspens n'atteint pas l'écran.
**Septième bornage consécutif.**

Le fait de méthode est le plus inconfortable de la tranche, et il ne porte pas
sur l'instrument cette fois — il porte sur **moi**. Quatre lots de suite, mon
détecteur était faux et la lecture l'a rattrapé. Ici le détecteur était **juste
du premier coup** ; c'est mon **raisonnement** qui allait publier un rang 1, avec
la chaîne complète et la ligne de code du client sous les yeux. **La parade n'a
pas été la lecture de la liste, mais une règle plus vieille — chercher l'URL
LITTÉRALE dans les octets servis (454/455) — appliquée à la toute dernière
minute.**

*Une chaîne causale complète dans le code n'est pas une chaîne causale dans le
produit tant qu'on n'a pas prouvé que le consommateur est servi.*

Comptes séparés : résultats faux **arrêtés avant publication** **34** (+1) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
