# SKYLER LOT 462 — Les phrases-seuil servies : 26 sur 28 citent EXACTEMENT le seuil que le code applique, le défaut du 461 est un accident isolé — et la seule autre divergence trouvée porte sur une branche INATTEIGNABLE

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-462` (base : lot 461 fusionné,
68a2e5e)

Quarante-deuxième lot de la veine, deuxième de la tranche 460-469. Le 461 a
nommé un genre neuf — **un classeur qui cite un seuil et en applique un autre** —
et ce lot applique la règle de succession : **attaquer la classe entière** que
cette forme désigne, **les phrases servies qui citent un nombre à côté d'un
prédicat**.

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure (règle 458/461)

Une **PHRASE-SEUIL SERVIE** est un littéral de chaîne des octets servis qui
**(a)** est destiné à l'affichage, **(b)** contient un nombre, et **(c)** présente
ce nombre comme une **référence ou une limite** — c'est-à-dire que la phrase porte
elle-même un **mot de comparaison** (`plafond`, `maximum`, `minimum`, `repère`,
`seuil`, `limite`, `au-delà`, `au-dessus`, `jusqu'à`, `cible`, `borne`, `≥`, `≤`,
ou un chevron suivi d'un chiffre).

**Le critère (c) est le cœur du calibrage.** Sans lui, tout nombre affiché entre
dans la population et le total est contaminé par des homonymes — la leçon des 28
valeurs exclues du 458. **Un nombre n'est décidable que si la phrase dit
elle-même qu'il sert de borne.**

Exclus d'emblée, nommés, comptés dans aucun total : l'habillage (CSS, SVG, URL),
les nombres purement **descriptifs** sans mot de comparaison, et les nombres
**interpolés** (`${x}`) — une valeur mesurée n'est pas un seuil cité.

## Deux corrections d'instrument — et la seconde était grossière

Le contrôle obligatoire — *le détecteur doit retrouver le cas connu du 461* — a
été branché **dès la première exécution**, comme le 461 l'a imposé. Il passait ;
c'est la **taille de la population** qui a trahi l'instrument.

```text
#   défaut de l'instrument                        effet mesuré
1   la regex `'…'` appariait le guillemet         186 « phrases » dont des
    FERMANT d'un littéral avec l'OUVRANT du       fragments de CODE :
    suivant, capturant le CODE entre les deux     `,opp.actionable>0?`
    → remplacée par un VRAI tokeniseur            (même famille que la classe
                                                   de caractères du 453)
2   `<` et `>` NUS figuraient dans la liste des   tout le BALISAGE HTML entrait
    mots de comparaison                           dans la population
```

Après correction : **186 → 30**. Les deux fautes gonflaient la population d'un
facteur six, et **aucune ne faisait échouer le contrôle** — le cas du 461 était
retrouvé dans les deux versions. **Un contrôle qui passe ne prouve pas que
l'instrument est juste ; il prouve seulement qu'il n'est pas aveugle.** C'est une
précision utile à la règle du 461.

**Deux faux arrêtés avant publication. Total : 29 → 31.**

## La population

```text
corpus : 42 objets servis · 841 916 caractères
littéraux portant un nombre, après calibrage        30 phrases-seuil
   écartés E1 (habillage / SVG / CSS)                  279
   écartés E2 (nombre DESCRIPTIF, non décidable)       319
   écartés E3 (nombre INTERPOLÉ, pas cité)               1
```

Sur les 30, **2 sont écartées à la lecture** : ce sont des **en-têtes de tableau**
(`Sous-jacent · Catégorie · … · R:R cible` sur `/opportunities`, `Biais ·
Bascule 0-γ · Mur call · Mur put · Max pain` dans `options-gex.js`) — des listes
de colonnes, pas des phrases-seuil. **Restent 28 phrases tranchées.**

## Le résultat : 26 sur 28 concordent

```text
phrase servie                                    seuil appliqué par le code       verdict
« Distribution … à partir de 3 clôtures »        withPl.length < 3                CONCORDE
« Saisonnalité … à partir de 3 clôtures »        même garde                       CONCORDE
« minimum 5 par verdict »                        track_record.py:171  n >= 5      CONCORDE
« (n≥5) — mesure, pas une promesse »             même règle                       CONCORDE
« <-20 »  (histogramme journal)                  bucket [-1e9, -20]               CONCORDE
« >+50 »  (histogramme journal)                  bucket [50, 1e9]                 CONCORDE
« breadth > 55 % »            /markets           55 appliqué :266 et :617         CONCORDE
« max 5 catégories »          /markets           C.donut → slice(0, 5)            CONCORDE
« Gain ≥ +100/75/50/30/20 % » /portfolio         winnerRule, 5 paliers            CONCORDE ×5
« option(s) à échéance ≤ 7 j »/portfolio         <= 7   (deux sites, :224 :683)   CONCORDE
« max 3, dont 1 PUT tactique »/portfolio         Constitution : 3 et 1            CONCORDE
« plafond 15 % par titre »    /portfolio         topOver = top_weight_pct > 15    CONCORDE
« —/40 » et « /40 »           /opportunities     8 blocs sommant 40 (cf. 457)     CONCORDE ×2
« zone ≤ 5 j »                catalyst-runway    dangerX = xOf(min(5, horizon))   CONCORDE
« prime élevée (>12 % du notionnel) » options    capital/(spot*100) > 0.12        CONCORDE
« Gain ≥ +100/75/50/30/20 % » options-structure  optNextAction, 5 paliers         CONCORDE ×5
« max 3, dont 1 PUT tactique »options-structure  Constitution : 3 et 1            CONCORDE
« P(valeur terminale ≥ 2× coût) » options-scan   S_T ≥ K + 2×prime  (équivalent)  CONCORDE
« évaluée … toutes les 60 s » vx-entities        _alerts_loop : time.sleep(60)    CONCORDE
────────────────────────────────────────────────────────────────────────────────────────
« au-delà d’un repère prudent (~15 % …) »        m.top1.w > 25                    DIVERGE (461)
« cible 1 »                   /analysis          peut afficher tp2                BORNÉE — voir ci-dessous
```

**Vingt-six phrases sur vingt-huit citent exactement le nombre que le code
applique.** Le défaut du 461 n'est pas la pointe d'un massif : **c'est un
accident isolé dans sa propre famille.** Troisième bornage consécutif du même
type — 453 sur 452, 458 sur 457, 461 sur 458, et maintenant 462 sur 461.

Le témoin le plus serré est `« P(doubler) = P(valeur terminale ≥ 2× coût) »` :
le moteur écrit `S_T ≥ K + 2×prime`, ce qui est **la même condition sous une
autre forme** — une phrase qui reformule le prédicat sans le trahir.

## La seule autre divergence — et elle porte sur une branche INATTEIGNABLE

`analysis_page.py:788` :

```javascript
scen('base','Probable', tgts.tp1 != null ? tgts.tp1 : tgts.tp2, rBase, 'cible 1')
scen('up','Exceptionnel', tgts.tp3 != null ? tgts.tp3 : tgts.tp2, rUp, 'cible étendue')
```

Sur le papier c'est exactement le genre du 461 : la note dit « **cible 1** » alors
que la valeur affichée peut être **tp2**. Pire, si `tp1` **et** `tp3` manquaient
ensemble, les cartes « Probable » et « Exceptionnel » afficheraient **le même
prix et le même rendement**.

**Sauf que la branche n'est pas atteignable.** `dec.targets` vient de
`decision_stack.py:322`, qui relaie le plan de `analysis.py:261` — **l'unique
producteur**, et il écrit les trois cibles **dans la même expression** :

```python
'tp1': round(last + risk, 2), 'tp2': round(last + 2 * risk, 2),
'tp3': round(last + 3 * risk, 2),
```

`tp1` est donc présent chaque fois que `tp2` l'est. Les sept autres écrivains de
`tp1`/`tp2` recensés (`order_ticket`, `track_record`, `weekly`, `positions/models`,
`committee`, `terminal.py:1601`) **n'alimentent pas `dec.targets` de `/analysis`**.

**Règle 442/445 : une étiquette fausse sur une branche inatteignable n'est pas un
mensonge à l'écran. Je ne la classe pas.** Je la publie parce qu'elle est le seul
autre candidat de la famille et parce que **le repli existe dans le code servi** —
si un jour un producteur partiel alimente cette carte, la divergence devient
réelle.

## Deux observations nommées, non classées

**(i) La borne de l'histogramme du journal.** Le libellé `>+50` couvre le bucket
`[50, 1e9]` : un trade à **exactement +50 %** est compté dans « >+50 ». Frontière
d'un point, cosmétique. **Nommé, non classé.**

**(ii) Hors calibrage, et je le signale quand même.** La même bulle d'aide qui
porte le « toutes les 60 s » — exact — affirme aussi « **sur données réelles** ».
Or `_alert_price` (`terminal.py:7012`) retombe sur `scan_state['detail'][sym]`
quand IBKR est absent, et ce détail est **synthétique en mode DEMO**. Ce n'est pas
un **nombre** cité, donc c'est **hors de la population de ce lot** ; et c'est le
genre du dossier ouvert 391/396. **Je le nomme, je ne le compte pas, je ne le
classe pas.**

## Ce que le lot ne prétend pas

- La population vaut **pour les phrases dont le mot de comparaison figure dans ma
  liste fermée**. Une phrase-seuil qui dirait « on s'arrête à 30 » sans mot de
  comparaison **échapperait** — c'est le prix du calibrage, et il est
  **non quantifié**.
- Les 319 phrases écartées en E2 **n'ont pas été relues une par une** : elles sont
  écartées **par construction**, pas par lecture. Un seuil déguisé en phrase
  descriptive y resterait.
- Les concordances sont établies **par lecture du prédicat voisin**, pas par
  exécution : aucun banc n'a été monté ce lot, aucun moteur appelé hors
  `load_profile()`.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Routes en **GET** ; `persist` redirigé ;
  **`/options/<sym>`, `/api/analyst/` et `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-cinquième lot court, deuxième de la tranche.

C'est un lot **à résultat négatif**, et c'est ce qu'il a de plus utile : la
famille désignée par le 461 est **saine à 26 sur 28**. Le défaut d'hier reste un
défaut — la fenêtre 15-25 % est mesurée et tient — mais il ne se généralise pas,
et le dire **borne le dossier au lieu de l'enfler**. Quatre lots consécutifs
bornent leur prédécesseur.

Le fait de méthode affine la règle du 461. Hier : *un détecteur qui ne retrouve
pas le défaut d'hier ne mesure rien.* Aujourd'hui, le contrôle **passait dès la
première version** et l'instrument était pourtant faux d'un facteur six.
**Corollaire : le contrôle par un cas connu détecte la CÉCITÉ de l'instrument,
jamais son BAVARDAGE.** Pour le bavardage, le signal est la **taille de la
population** — 186 phrases-seuil dans un produit de huit pages était
invraisemblable, et c'est cette invraisemblance qui m'a fait rouvrir le
tokeniseur.

Comptes séparés : résultats faux **arrêtés avant publication** **31** (+2) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
