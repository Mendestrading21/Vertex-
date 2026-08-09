# SKYLER LOT 467 — L'intervalle [22, 37] du 466 se résout à 28 : neuf des quinze suspectes étaient des redirections de compatibilité, et mon CONTRÔLE obligatoire était lui-même mal spécifié — il rejetait un instrument juste

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-467` (base : lot 466 fusionné,
5a21dfb)

Quarante-septième lot de la veine, septième de la tranche 460-469. Le 466 a
publié un **intervalle** faute d'avoir tranché quinze routes citées uniquement
depuis `terminal.py`. Ce lot les tranche (modèle 449/455/457/459/465).

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Chaque citation est classée par sa **position syntaxique** (`ast`), pas par sa
présence :

```text
A  DÉCLARATION    argument d'un `@…route(...)` ou d'un `add_url_rule(...)`
                  → c'est la règle, pas un consommateur
B  APPEL PYTHON   argument de `redirect`, `url_for`, `requests.*`,
                  `client.get/post`…  → un VRAI consommateur serveur
C  TEXTE CLIENT   tout autre littéral → HTML/JS destiné au navigateur,
                  vivant SEULEMENT si l'octet est servi
```

**Verdict posé d'avance** : une route dont toutes les citations sont A ou C est
orpheline confirmée ; **une seule citation B suffit à la déclarer consommée.**

## Le fait de méthode : mon CONTRÔLE était faux, et il rejetait un instrument juste

Le réveil exigeait un contrôle — « retrouver au moins une citation en appel
Python réel, sinon le détecteur est aveugle ». Je l'ai écrit, il a **échoué** :
`citations de classe B dans tout le dépôt : 0 → *** AVEUGLE AUX APPELS —
VERDICT NUL ***`.

**Le classeur n'était pas aveugle. Le contrôle était mal spécifié.** Il cherchait
un B **parmi les quinze suspectes** — or « aucun B parmi les suspectes » est
précisément **le résultat cherché**, pas une preuve de bon fonctionnement. Un
contrôle doit porter sur un cas **dont je connais la réponse**.

Refait en deux volets :

```text
V1  FIXTURE SYNTHÉTIQUE (réponse connue d'avance)
    @app.route('/x/decl')      attendu A → obtenu A   OK
    redirect('/x/call')        attendu B → obtenu B   OK
    "<a href='/x/text'>"       attendu C → obtenu C   OK
    client.get('/x/testclient')attendu B → obtenu B   OK
                                          → CLASSEUR SAIN

V2  TÉMOIN RÉEL DU DÉPÔT : /analysis/     A=1  B=2  C=2
    B → redesign.py:256  redirect(f'/analysis/{sym.upper()}', code=301)
                                          → DÉTECTEUR VOYANT
```

**Jusqu'ici mes contrôles n'attrapaient que des faux positifs — un instrument
qui bavarde ou qui est aveugle. Celui-ci a produit un faux NÉGATIF : il
condamnait un classeur correct.** Le contrôle peut donc être faux **dans les
deux sens**, et c'est neuf.

## La cinquième correction : K4 se lit dans le CORPS de la vue, pas dans un dictionnaire

Le témoin V2 a révélé autre chose. `redesign.py:256` est le corps de
`legacy_titre`, décorée `@bp.route('/titre/<sym>')` et `@bp.route('/company/<sym>')` :
**`/titre/<sym>` est une redirection 301**, pas une orpheline.

Le 466 avait bâti sa classe K4 depuis le **dictionnaire** `LEGACY_REDIRECTS` —
il ne pouvait donc pas voir les redirections **déclarées par décorateur**.
Reclassement des 37 candidates **par le corps de la vue** :

```text
K4 redirections découvertes parmi les 37        9
   /analyse-entreprise · /bordel · /catalysts · /entreprises · /ma-page
   /review · /settings · /stocks · /titre/<sym>
```

Toutes ont le même corps : `dest = target ; extra = request.query_string… ;
return redirect(dest, 301)`.

## Le verdict des quinze — et l'intervalle se referme

```text
                        A    B    C     verdict
/titre/<sym>            0    0   12     K4 redirection 301
/settings               0    0    7     K4 redirection 301
/bordel                 0    0    7     K4 redirection 301
/review                 0    0    7     K4 redirection 301
/catalysts              0    0    5     K4 redirection 301
/entreprises            0    0    5     K4 redirection 301
/ma-page                0    0    5     K4 redirection 301
/analyse-entreprise     0    0    5     K4 redirection 301
/stocks                 0    0    1     K4 redirection 301
────────────────────────────────────────────────────────────
/api/rescan             1    0    5     ORPHELINE CONFIRMÉE
/api/company/<sym>      1    0    0     ORPHELINE CONFIRMÉE
/api/committee-review   0    0    1     ORPHELINE CONFIRMÉE
/api/strategie          0    0    1     ORPHELINE CONFIRMÉE
/api/risk               0    0    0     ORPHELINE CONFIRMÉE
/api/validator          0    0    0     ORPHELINE CONFIRMÉE

   9 redirections · 6 orphelines confirmées · 0 consommée
```

**Aucune des quinze n'était consommée par un appel Python.** La question du 466
avait donc deux réponses possibles et c'est la seconde : ce n'étaient pas des
appels serveur, mais **neuf d'entre elles n'étaient pas mortes pour autant**.

### Le compte devient EXACT

```text
189 règles déclarées
    98  K1 consommée par un objet servi
    28  K2 serveur interne          (43 − 15 tranchées)
     9  K3 navigation
    21  K4 redirection 301          (12 du 466 + 9 découvertes ici)
     5  E3 infrastructure
    28  ORPHELINES                  (22 du 466 + 6 confirmées ici)
   ───
   189                              ✓  28 / 189 = 14,8 %
```

**L'intervalle [22, 37] se résout à 28 — il tombe dedans, et le plafond de 37
était gonflé de neuf par des redirections que l'instrument du 466 ne pouvait pas
voir.**

## Deux corrections d'unité que je publie

**Les « 53 citations de `/titre/<sym>` » du 466 étaient des occurrences de
sous-chaîne, pas des sites.** Mesuré par nœud `ast` : **12 littéraux distincts**.
Le fait tenait, l'unité était fausse — un long fragment de JS peut contenir le
même chemin dix fois.

Et ces douze pointent vers une redirection **qui fonctionne** : ce sont des liens
d'un HTML mort vers une URL vivante, pas des liens cassés.

## Les lignes mortes de `terminal.py` — beaucoup moins qu'attendu

```text
/desc/<sym>              desc_ep             30 lignes
/api/correlations/<sym>  api_correlations    26 lignes
/weekly-regen            weekly_regen_ep     13 lignes
/api/company/<sym>       api_company          6 lignes
/api/rescan              api_rescan           5 lignes
/api/alerts/status       api_alerts_status    3 lignes
                         total   83 lignes sur 7 154  =  1,2 %
```

**Limite dite franchement** : ce compte ne couvre que les **handlers de routes
orphelines**. Les 18 citations « texte client » vivent, elles, **au niveau
module** (constantes de gabarit assemblées à l'import) et **pas dans une
fonction** — je ne peux donc pas les attribuer à une page, et **elles ne sont pas
dans les 83 lignes**.

## Ce que le lot ne prétend pas

- La classe B repose sur une **liste fermée d'appelants**. Un appel par un
  mécanisme non listé — `getattr`, une table de dispatch, un client HTTP
  maison — serait classé C et **gonflerait** le compte d'orphelines.
- Le reclassement K4 lit le corps de la vue par `inspect.getsource` et le juge
  sur « contient `redirect(` et ne fait rien d'autre ». Une vue qui redirige
  **conditionnellement** après un vrai travail serait mal classée. **Aucune des
  neuf n'est dans ce cas** — les neuf ont un corps identique — mais la règle
  reste grossière.
- Les **28 orphelines** héritent des limites du 466 : appariement par préfixe,
  coût établi par motifs. **Le compte est exact pour la méthode, pas absolu.**
- **Aucune route n'a été appelée.** `/desc/<sym>`, `/api/correlations/<sym>` et
  `/options/<sym>` en particulier **NON appelées** (réseau sortant, écriture).
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Analyse `ast` et `inspect.getsource` en mémoire ;
  `persist` redirigé ; **aucun écrivain appelé**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-dixième lot court, septième de la tranche.

La dette du 466 est **soldée par un nombre** : **28 routes orphelines sur 189,
14,8 %**, et le plafond annoncé hier était **trop haut de neuf**. **Neuvième
bornage consécutif** — et le neuvième va, comme les précédents, dans le sens qui
**réduit** ce que la boucle croyait avoir trouvé.

Le fait de méthode est le plus utile depuis longtemps, parce qu'il porte sur
l'outil de vérification lui-même : **un contrôle mal spécifié rejette un
instrument juste.** Depuis le 461, j'ai appris que le contrôle attrape la cécité
mais pas le bavardage (462), et que seule la lecture attrape le reste
(463-466). Il manquait ce quatrième cas : **le contrôle peut condamner à tort.**

*Un contrôle doit porter sur un cas dont on connaît déjà la réponse. Un contrôle
qui porte sur la question posée ne contrôle rien.*

Comptes séparés : résultats faux **arrêtés avant publication** **39** (+2 : le
contrôle mal spécifié, et la classe K4 lue dans un dictionnaire) ; **publiés puis
corrigés** **3** ; **interprétations retirées** **1** ; **et une correction
d'UNITÉ publiée sur un chiffre du 466** (53 occurrences → 12 sites).

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
