# SKYLER LOT 453 — J'ai tenté de généraliser le contrat rompu du 452 : le balayage rend 26 candidats, **tous faux sauf celui du 452**, et il a fallu corriger l'instrument QUATRE fois pour pouvoir le dire

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-453` (base : lot 452 fusionné,
089b975)

Trente-quatrième lot de la veine, troisième de la tranche 450-459. Le 452 avait
trouvé un genre neuf — **une carte qui lit le contrat d'une route masquée**. Ce
lot pose la question suivante : **est-ce un genre, ou un cas ?**

**Aucun code, aucun gardien, aucun test.** Résultat : **un bornage**, pas une
trouvaille — et je le dis dès le titre.

## L'instrument, et ses quatre corrections

Question mesurée : *combien de lectures `receveur.champ` dans le JS servi portent
sur des clés que la route interrogée ne rend jamais ?*

```text
corpus                  58 sources servies (25 pages/ui inline + 33 JS statiques)
                        1 exclu : vendor/lightweight-charts (minifié — 437)
appels VX.fetch                                87
liaisons receveur ↔ URL reconnues              72   (83 %)
   assign-await 57 · promise-allSettled 9 · promise-all 5 · then-arrow 1
lignes NON couvertes                           15   (17 %) — toutes nommées
routes distinctes                              47
   répondant 200 JSON                          46
   non concluante                               1   /api/options/simulate  400
```

Les 15 échappées sont des `.then(function (d) {...})` (fonction anonyme, pas
flèche), des helpers à paramètre `url` (`options-intel.js:96`, `tracking.js:8`),
des `return await` et un `VX.fetch.peek`. **Je les nomme et je ne les compte
pas** (règle 448).

### Quatre corrections, chacune avec sa cause

**1. Couverture 32 → 72.** La première passe n'acceptait que
`const X = await VX.fetch(...)`. Elle ratait l'affectation nue (`t=await …`),
`Promise.all` et `Promise.allSettled`. **37 % de l'usage manqué** — huitième
récidive du piège des enveloppes (409, 413, 414, 439, 442, 443).

**2. Fenêtre de lecture contaminée.** La fenêtre de 80 lignes après la liaison
avalait les lectures d'un **autre** receveur du même nom. Exemple mesuré :
`analysis_page.py:859` lie `d` à `/api/anomalies/`, et `:869` rebinde
`const d = r && r.decision` — l'instrument attribuait `d.gates`, `d.scenarios`,
`d.strongest_objection` à la route des anomalies. Corrigé en arrêtant la fenêtre
à **toute réaffectation du nom**. Fenêtre médiane après correction : **34
lignes** ; 12 sites restent bornés par le plafond de 80.

**3. Les enveloppes `Promise.allSettled` ne sont pas la charge utile.**
`stR.status === 'fulfilled' ? stR.value : null` — `.status` et `.value` sont les
propriétés du **wrapper**, pas des clés de réponse. **17 couples** en venaient.

**4. Une classe de caractères contenant `\s` franchit le retour à la ligne.**
Mon extracteur d'imports, `from\s+(vertex[\w.]*)\s+import\s+([\w,\s_]+)`, a
capturé `'series as _series\n    from vertex'` — **il a avalé l'instruction
suivante** et perdu le deuxième import de la vue. C'est le **miroir exact de la
leçon 435** (« `re` sans `DOTALL` ne franchit pas les retours à la ligne ») : ici
la classe `\s` les franchit, et c'est tout aussi faux.

**Quatre corrections avant publication.** Le compte des faux arrêtés avant
publication passe de **20 à 24**.

## Le crible, en quatre passes

```text
sites analysés                                        72
   SAINS — toutes les clés lues sont servies          40      ← témoin positif intégré
   avec écart                                         24
   sans lecture de champ (passe-plat vers un builder)  7
   sur route non concluante                            1

couples (site, clé) en écart                          78
   enveloppes allSettled                              17      artefact, écarté
   clé écrite littéralement dans la fonction de vue    2      optionnelle
   lue dans une chaîne de repli  X.a || X.b           26      lecture tolérante
   CANDIDATS                                          33
      expliqués par le module délégué (1 niveau)       7
      SURVIVANTS aux quatre cribles                   26
```

**Les 40 sites sains sont le témoin positif** : sans eux, un instrument qui
rendrait « tout est rompu » serait indistinguable d'un instrument juste. Exemples
mesurés : `/api/ticker/` (`company`, `detail`, `in_universe`, `risk_map`),
`/api/market/regime` (`adjustments`, `confidence`, `regime`),
`/api/briefing/editorial` (`daily`, `main_risk`).

## Les 26 survivants, tranchés un par un — 25 sont faux

```text
1   /api/anomalies/     a.anomalies          → LE DÉFAUT DU 452, retrouvé
7   /api/analyst/       eps_revisions, eps_trend, growth_fwd, holders,
                        insider, ratings_actions, surprises
                        → data_sources/analyst_deep.py écrit 7/7.
                          Route dans terminal.py, dépendante du RÉSEAU (yfinance) :
                          mon GET a échoué derrière le proxy, charge utile vide.
5   /api/evidence/      points, n_events, n_unmeasurable, up, down
                        → engines/evidence_lab.py:72-75 les écrit 5/5.
                          Manqués par la correction n°4 (regex avalant la ligne).
13  /api/validator      n, dsr, psr0, pbo_estimate, sharpe_ann, skew, kurtosis,
                        degradation, folds_positive_pct, n_trials,
                        sr_in_sample, sr_out_sample
                        → la vue rend validator.build(eq) SI scan_state['portfolio']
                          existe ; il vaut None au démarrage, donc la réponse servie
                          est le repli HONNÊTE :
                          {'ok': False, 'note': 'backtest indisponible (univers/
                           historique insuffisant)'}
1   /api/ai/enrichment  snap.as_of  → ai/enrichment.py l'écrit.
```

**Le cas `/api/validator` est la leçon 438 dans sa forme pure** : une clé absente
d'une réponse **vide au démarrage** n'est pas une clé absente du **contrat**. Et
le repli servi est honnête — il **nomme** ce qui manque.

## Ce que le lot établit

**Le contrat rompu du 452 n'est, à ce jour, PAS un genre : c'est un cas.** Sur
72 sites de lecture couvrant 46 routes, **un seul** survit à quatre cribles et à
l'examen à la main — et c'est celui qui était déjà publié.

**Cela borne le rang 1 du 452 au lieu de l'élargir**, et c'est un résultat que je
préfère publier plutôt que gonfler. Le 452 avait raison sur le fait ; il aurait eu
tort d'en faire une famille.

### Le contrôle 443, et son coût

La règle exige que l'instrument **retrouve seul** la trouvaille du lot précédent.
Elle a été tenue — mais **seulement à la deuxième variante**.

```text
variante « écrivain n'importe où dans la clôture du endpoint »
   → a.anomalies classé « optionnelle », car engines/analysis.py:314 et
     skyler_core.py:173 portent une clé 'anomalies' dans un AUTRE dictionnaire
   → RÈGLE 443 NON TENUE, variante rejetée

variante « clé littérale DANS la fonction de vue, puis délégation à 1 niveau »
   → a.anomalies SURVIT · RÈGLE 443 TENUE
```

**Nouvelle règle de méthode** : *chercher un écrivain de clé « quelque part dans
la clôture d'imports » ne prouve rien — la clé doit être écrite dans LE
dictionnaire RENDU.* La clôture d'imports, excellente pour l'atteignabilité au
452, est **le mauvais outil** pour un contrat de charge utile.

## Un sous-produit, classé rang 4

**26 couples sont lus dans une chaîne de repli** — `ob.contracts || ob.list ||
ob.best`, `exec.blocking_anomalies || exec.blocking`, `cal.ts || …`. Ce sont des
**branches de repli mortes** : la première clé citée n'existe pas, la suivante
oui. Rien n'est faux à l'écran, le lecteur est simplement plus tolérant que le
contrat. **Rang 4**, à ranger avec les autres poids morts.

## Portée

- Je mesure **83 %** des appels `VX.fetch` ; **17 % échappent** et sont nommés.
  **Aucun total n'est présenté comme exhaustif.**
- Les clés servies sont relevées **à un instant où `scan_state` est vide** —
  c'est la limite structurelle de la mesure, et c'est elle qui a produit les 13
  faux de `/api/validator`. Les 46 réponses sont donc des **contrats observés au
  démarrage**, pas des contrats prouvés.
- Le GET sur `/api/analyst/AAPL` a **tenté un appel réseau sortant** (yfinance),
  refusé par le proxy. Aucune écriture : vérifié au contrôle runtime.
- Je mesure des **lectures de champ**, jamais des jetons nus ; les lectures par
  **déstructuration ou par crochets** échappent (leçon 436) et ne sont pas
  quantifiées ici.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. 47 routes en **GET**, `persist` redirigé vers un
  répertoire temporaire ; `app.url_map`, `test_request_context` et l'analyse
  `ast`/`inspect` en mémoire.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-sixième lot court, troisième de la tranche.

Le 452 avait ouvert une porte ; ce lot la referme en montrant qu'elle ne donne
sur rien d'autre. C'est le rôle qu'un lot doit accepter quand la généralisation
échoue : **le dire, avec le compte exact de ce qui a été essayé.**

Le vrai acquis est ailleurs. Quatre corrections d'instrument dans un seul lot,
dont une — la classe `\s` qui franchit la ligne — est **le miroir d'une leçon
déjà payée au 435**. Une leçon apprise dans un sens ne protège pas de son
symétrique.

Comptes séparés : résultats faux **arrêtés avant publication** **24** (+4) ;
**publiés puis corrigés** **3**, inchangé.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
