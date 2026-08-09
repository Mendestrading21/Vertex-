# SKYLER LOT 479 — Le 416 DESCEND de rang 1 à rang 3, par transitivité avec ma propre mesure du 478 — et « les quinze jamais classés » est un compte FAUX : trois d'entre eux portent déjà un rang

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-479` (base : lot 478 fusionné,
`b406f1d`)

Quatrième dossier de la reprise. **Il ne corrige rien.** Aucun fichier de
production touché.

**Ce lot produit un résultat que je n'avais pas prévu et qui ne m'arrange pas :
il fait BAISSER un rang 1 en rang 3, et il invalide le compte que mon propre
réveil utilisait pour se repérer.**

## Le contrôle — réponse connue du lot précédent, et il passe

```text
attendu (mesuré au 478)   portfolio_page.py:200 et :208, les deux (cash||0)
mesuré                    :200  const netValue=grossVal+(cash||0);
                          :208  const denom=grossVal+(cash||0);
verdict                   CONTRÔLE PASSÉ
```

---

# LE COMPTE EST FAUX — et c'est le premier résultat du lot

Mon réveil parle de **« quinze dossiers jamais classés »**. Mesuré, rapport par
rapport :

```text
dossier   rang déclaré dans SON PROPRE rapport
  388     aucun          408     aucun          409     aucun
  411     aucun          426     aucun          391     aucun
  379     aucun          363     aucun          386     aucun
  456     aucun          459     aucun
  416     RANG 1   ←
  422     RANG 1   ←
  431     RANG 4   ←
                          ────────────────────────────────
                          3 sur 14 portent DÉJÀ un rang
```

**« Jamais classés » confond deux choses : ne pas être RANGÉ et ne pas être
CHIFFRÉ.** Onze dossiers n'ont aucun rang ; trois en ont un et n'ont jamais été
devisés. **Le travail restant n'est donc pas « quinze classements » — c'est onze
classements et quatorze devis.**

**Compte : arrêté avant publication, 44 → 45.** Le chiffre venait de mon propre
réveil, comme au 470 et au 473.

---

# POURQUOI LE 416, ET CE QUE LA MESURE EN FAIT

## Le choix

Le 416 est **le seul candidat dont le rang déclaré peut être testé par
transitivité** : il justifie son rang 1 en se comparant explicitement au 407 —
et **je viens de re-mesurer le 407 au lot 478**. C'est la seule occasion de la
reprise où deux de mes propres mesures se contredisent, et c'est plus instructif
qu'un dossier neuf.

## Les sites, relus — et une forme que mon premier grep a manquée

```text
vertex/engines/indicators.py:14   docstring : « dn==0 (aucune baisse) → 100, jamais NaN »
vertex/engines/indicators.py:18   (100 - 100/(1 + up/dn.replace(0, np.nan))).fillna(100)
vertex/market/indicators.py:86    round(100.0 - 100.0/(1.0+rs), 1) if avg_l > 0 else 100.0
vertex/engines/analysis.py:304    'rsi': round(r)                       ← la valeur servie
vertex/ui/pages/analysis_page.py:472   +kv('Force relative',d.rs)+kv('RSI',d.rsi)
```

**Deux implémentations, DEUX FORMES SYNTAXIQUES DIFFÉRENTES du même choix** :
`.fillna(100)` d'un côté, `if avg_l > 0 else 100.0` de l'autre. Mon premier
`grep 'else 100'` n'a trouvé **que la seconde**. **Quinzième récurrence du piège
du détecteur à une seule forme** — attrapée en lisant le fichier, pas en comptant.

## Atteignabilité — prouvée par exécution, et elle PRÉCISE le dossier

```text
GET /analysis        200 ·  22 248 o  ·  « kv('RSI' » : NON
GET /analysis/AAPL   200 ·  75 216 o  ·  « kv('RSI' » : OUI
```

**Le RSI n'est servi que sur la fiche d'un symbole, pas sur `/analysis` nu.** Le
416 écrivait « le nombre 100 est montré au trader » sans cette distinction. Elle
ne change pas le fond — `/analysis/AAPL` fait partie des 42 objets servis — mais
elle est **plus juste**, et je la pose.

## Un témoin positif, dans le même fichier que le producteur

```text
analysis.py:291   'rsi': [None if math.isnan(x) else round(float(x), 1) for x in rsi120.values]
analysis.py:304   'rsi': round(r)
```

**La SÉRIE de RSI mappe `NaN` vers `None` — donc vers `—` à l'écran. Le SCALAIRE,
treize lignes plus bas, ne le fait pas.** Le motif est celui des 457, 476, 477 et
478 : *la pratique honnête existe, appliquée à un consommateur sur deux, dans le
même fichier*.

Réserve honnête : `rsi()` faisant déjà `fillna(100)`, il est possible qu'aucun
`NaN` n'atteigne jamais la ligne 291. **Je n'ai pas mesuré si cette garde tire
jamais** — je constate qu'elle est écrite, pas qu'elle sert.

---

# LE CLASSEMENT — LE 416 DESCEND À RANG 3

## La chaîne qui l'impose, et elle est faite de mes propres mesures

```text
416 (son rapport)   « Rang 1 … mais NETTEMENT MOINS GRAVE QUE LE 407 »
478 (ma mesure)     le 407 est RANG 2, pas rang 1
                    ────────────────────────────────────────────────
                    416 « nettement moins grave » qu'un rang 2  ⇒  RANG 3
```

**Le 416 n'a pas changé ; c'est son étalon qui a bougé.** Sa prémisse
comparative reste littéralement vraie — le 478 n'a pas contesté le facteur
« ×170 » du 407, il a contesté son **interprétation** (sens prudent de l'erreur,
clé non écrivable, lecture alternative). Mais un rang est **relatif**, et quand
la référence descend, ce qui était déclaré strictement en dessous descend aussi.

## Et la mesure directe donne le même résultat

Indépendamment de la transitivité, le 416 tient un **rang 3** par ses propres
faits, tels que son rapport les établit :

- le cas fautif est **un titre plat depuis le début de la fenêtre** — `up == 0`
  **et** `dn == 0` ;
- le 416 mesure lui-même que le cas voisin, plus fréquent (plateau après hausse),
  **n'est pas une faute** : « aucune baisse ⇒ RSI 100 » est **la définition de
  Wilder** ;
- et il écrit que sa propre sonde a **rétréci** le défaut : « le défaut est donc
  plus étroit que je ne l'ai cru ».

**Un cas de bord strict, sur une valeur qui est correcte dans le cas dominant,
et dont la convention est celle du métier. Rang 3.**

**Pourquoi pas rang 4** : le chiffre est **affiché**, sur un objet **servi**, et
il est **indiscernable** d'une mesure — un titre halté est présenté comme aussi
suracheté qu'une envolée. Ce n'est pas une imperfection interne.

## La prémisse du docstring reste fausse, et je le maintiens

Le 416 a mesuré que `jsonify({'x': float('nan')})` rend `{"x":null}` — **Flask
assainit déjà**. La justification écrite en `indicators.py:14` (« jamais NaN,
casserait le JSON ») **ne tient pas dans cette pile**. Cela ne relève pas le
rang — un commentaire faux n'est pas un chiffre faux — mais **cela rend le
correctif plus facile à défendre** : l'obstacle invoqué n'existe pas.

---

# LE CHIFFRAGE

```text
MOTEURS — deux implémentations, deux formes
  vertex/engines/indicators.py:18   .fillna(100) → ne combler que dn==0 ET up>0        1 ligne
  vertex/market/indicators.py:86    if avg_l > 0 else 100.0 → idem                      1 ligne
  vertex/engines/indicators.py:14   docstring : retirer la prémisse fausse              1 ligne
                                                                             ─────────
                                                                      TOTAL   3 lignes
fichiers            2 (+ la docstring dans l'un des deux) · moteur touché : OUI
                    et cette fois c'est un VRAI calcul, pas un ajout de champ
RENDU               aucune ligne : `analysis_page.py:472` passe par kv(), et le
                    contrat « null → — » est déjà celui de la page (témoin :291)
```

**C'est le premier dossier du plan dont la correction touche un calcul de
moteur.** Les dix-neuf autres ajoutaient un champ, une garde ou un libellé. Cela
justifie une prudence supplémentaire, et **c'est un argument pour le traiter
seul**.

## Gardien et régression

```text
gardien       tests/test_rsi_indefini_lot4xx.py
assertion     une série strictement plate (up==0 ET dn==0) rend None, pas 100 ;
              une hausse monotone rend bien 100 (convention de Wilder préservée)
échoue-t-il aujourd'hui ?   OUI — mesuré par lecture : `.fillna(100)` (:18) comble
              indistinctement, et `if avg_l > 0 else 100.0` (:86) aussi
gardiens existants   « RSI 100 » → 0 · « fillna(100) » → 1 (test_timeframes_lot144.py)
                     « rsi » → 5 fichiers · « indicators » → 5 fichiers
                     dont tests/test_market_indicators.py et _lot157.py
régression    MOYENNE — cinq fichiers de test touchent le RSI ou les indicateurs.
              Un test qui vérifie « série plate → 100 » deviendrait faux, et le 416
              signale précisément un gardien « dont le nom dit neutre et qui accepte
              l'extrême » : IL FAUT LE RELIRE AVANT, pas après.
octet servi ?  NON — les deux fichiers sont des moteurs ; la page ne change pas
               → AUCUN BUMP, AUCUN _EMPREINTE
```

## Mutualisation — absente, et c'est mesuré

Aucun des dix-neuf dossiers du plan ne touche `vertex/engines/indicators.py` ni
`vertex/market/indicators.py`. Le 442+443 (lot G) vit dans `analysis_page.py`,
pas dans les moteurs d'indicateurs. **Le dossier est isolé.**

---

# LA FEUILLE DE DÉCISION — VINGT DOSSIERS

```text
avant ce lot   19 dossiers · 52 à 60 lignes · 19 gardiens · douze rang 1 · sept rang 2
ce lot         +1 dossier (416, RANG 3 — et non rang 1) · +3 lignes · +1 gardien
après          20 DOSSIERS · 55 à 63 LIGNES · 20 GARDIENS
               DOUZE RANG 1 · SEPT RANG 2 · UN RANG 3
```

**Nouveau lot de travail** :

```text
J « le RSI »   416   3 lignes · 2 moteurs · RANG 3 · aucun octet servi
               ISOLÉ · SEUL dossier du plan dont la correction touche un CALCUL
               → à traiter seul, et en dernier
```

Les neuf lots A à I sont **inchangés**.

## Ce qui reste hors devis

**Dix classements** (11 sans rang − 1 : aucun traité ici, le 416 en avait déjà
un) : 388 · 408 · 409 · 411 · 426 · 391/396 · 379 · 363 · 386 · 456+459. **Plus
deux dossiers déjà rangés mais non chiffrés** : **422 (rang 1)** et **431
(rang 4)**. Plus les **trois dossiers de DÉCISION** (469, 468, 466/467) et le
quatrième candidat ouvert au 478 (*faut-il un champ « capital » dans le desk ?*).

## Ce que le lot ne prétend pas

- **Je n'ai pas rejoué le banc du 416** (les quatre séries, les quatre plateaux).
  Ses chiffres sont **les siens**, cités comme tels. Ce que **ce lot** mesure :
  les deux formes syntaxiques, l'atteignabilité exacte, le témoin de la ligne 291,
  et **la contradiction entre son rang et ma mesure du 478**.
- **Je n'ai pas mesuré si la garde de `analysis.py:291` tire jamais.** Elle est
  écrite ; je ne dis pas qu'elle sert.
- **Je n'ai pas relu `test_timeframes_lot144.py`** ni les cinq fichiers
  d'indicateurs ligne à ligne. Le risque « moyen » est une **estimation de
  périmètre**, pas une mesure — et le 416 signale lui-même un gardien à revoir.
- **Aucun navigateur.** L'affichage est établi sur les octets servis de
  `/analysis/AAPL`, obtenus en `GET` via `test_client`.
- **Aucun réseau. Aucun écrivain appelé. Aucun fichier de production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** (dont `/analysis/AAPL`, objet servi du corpus) ; `persist`
  redirigé vers un `mkdtemp` **et la redirection vérifiée par `cache_path()`** ;
  **`/api/analyst/`, `/api/correlations/`, `/options/<sym>`, `/desc/<sym>` NON
  appelées** ; `rsi()` **non exécutée** — les deux implémentations sont établies
  **par lecture**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quatre-vingt-unième lot court, **quatrième de la reprise**.

Quatre lots, cinq dossiers traités (417, 378, 406+407, 416). Et pour la première
fois, **un lot a fait DESCENDRE un dossier au lieu de le monter** — et pas d'un
cran discret : **de rang 1 à rang 3.**

Le fait de méthode est neuf et il a une portée qui dépasse ce dossier :

**UN RANG EST RELATIF. Quand une référence bouge, tout ce qui s'est classé PAR
RAPPORT À ELLE doit bouger aussi.** Le 416 s'est déclaré rang 1 « nettement moins
grave que le 407 » ; le 478 a mesuré que le 407 est rang 2 ; **le 416 est donc
descendu sans qu'un seul fait le concernant ait changé**.

Cela ouvre une question que je pose sans y répondre, parce qu'elle dépasse ce
lot : **combien d'autres rangs de la veine ont été posés par comparaison à un
dossier dont le rang a bougé depuis ?** Je ne le mesure pas ici — ce serait un
lot entier — mais **je le nomme, parce que ne pas le nommer serait la même faute
que les atténuations du 477.**

Et une observation de cohérence, à mon crédit comme à ma charge : **les deux
derniers lots ont tous deux réduit un dossier** (478 : rang 1 pressenti → rang 2 ;
479 : rang 1 publié → rang 3). Après vingt lots où la mesure aggravait, elle
allège deux fois de suite. **Je ne sais pas encore si c'est un instrument qui se
calibre ou un juge qui se fatigue, et je préfère l'écrire que le taire.**

Comptes séparés : résultats faux **arrêtés avant publication** **45** (+1, le
compte des « quinze jamais classés ») ; **publiés puis corrigés** **7** (+1, le
rang 1 du 416) ; **interprétations retirées** **3** ; re-localisation **0**.

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre vingt
dossiers, douze de rang 1, pour 55 à 63 lignes.**
