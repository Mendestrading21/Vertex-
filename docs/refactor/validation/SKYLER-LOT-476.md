# SKYLER LOT 476 — Le devis clos, la mesure reprend : le 417 est CLASSÉ RANG 1 et chiffré à 5 lignes — le tableau du track record affiche `N` à côté d'un rendement qui ne repose pas sur `N`, et la bonne pratique est DANS LA MÊME LIGNE, sur une colonne sur quatre

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-476` (base : lot 475 fusionné,
`b2181a2`)

Le devis est clos (475) : seize dossiers, 40 à 48 lignes, huit lots de travail,
**et rien ne sera corrigé sans GO humain**. La boucle reprend donc son travail
normal — **la mesure** — sur les **dix-huit dossiers jamais classés**.

Ce lot en ouvre **un**, le **classe** et le **chiffre**.

**Il ne corrige rien.** Aucun fichier de production touché.

## Le contrôle — réponse connue, et il passe

```text
attendu (relu au 473)   track_record.py:52-59 — le record à 12 champs, sans provenance
mesuré                  :52 rec = {'ts': time.time(), 'ticker': sym, 'price': …
                        :59 'outcome': None}
verdict                 CONTRÔLE PASSÉ
```

## Pourquoi le 417, et pas un autre des dix-huit

Trois raisons, dans l'ordre où elles ont pesé :

1. **La forme du défaut est déjà calibrée.** « Un dénominateur qui n'est pas le
   dénominateur » est la famille des 456 (plafonné à 200) et 457 (borne V1), tous
   deux mesurés et classés. J'ai donc **un étalon** pour ranger celui-ci, au lieu
   d'un jugement à main levée.
2. **Le devis a déjà ouvert `track_record.py`** (464, lot de travail B). La
   mesure y est moins chère, et **la mutualisation était à vérifier** — elle
   existe, et je la dis plus bas.
3. **L'enjeu est le plus élevé du lot des dix-huit** : c'est la page qui dit au
   trader **à quel point le moteur est fiable**. Un dénominateur trompeur y
   contamine la confiance dans tout le reste.

Écarté sciemment : le **416 (RSI 100)**, pourtant proche du genre neuf du 475.
Raison honnête — **je viens de nommer ce genre, et je me méfie de l'aller
chercher tout de suite** : la tentation de retrouver ce qu'on vient d'inventer
est exactement ce que le 463 appelle « multiplier un dossier connu ».

---

# LE DOSSIER, MESURÉ

## Le mécanisme, relu dans le fichier réel

```text
track_record.py:119   groups.setdefault(key, {'n': 0, 'f1': [], 'f5': [], 'f20': [], 'tp': [0,0]})
              :133-134  f20, _ = _fwd(closes, dates, day, 20)
                        if f1 is None and f5 is None and f20 is None:  → l'entrée est ignorée
              :149-150  if f20 is not None: b['f20'].append(f20)
              :171-173  'by_verdict' / 'by_grade' / 'by_regime' … if b['n'] >= 5
```

**`n` compte les entrées résolues à AU MOINS UN horizon** ; `f20` ne se remplit
que si l'horizon +20 séances existe. **Le filtre `n >= 5` protège le paquet, pas
chaque nombre publié.**

## Et `agg()` ne calcule même pas les vrais dénominateurs

```text
track_record.py:163-166
   return {'n': b['n'], 'avg_1j': …, 'avg_5j': …, 'avg_20j': avg(b['f20']),
           'win_1j': …, 'win_5j': …, 'win_20j': win(b['f20']),
           'tp1_rate': …, 'tp1_resolved': b['tp'][1]}
```

**`len(b['f5'])` et `len(b['f20'])` ne sont exposés nulle part.** Le moteur *sait*
combien d'observations portent chaque colonne — il ne le dit pas. C'est ce qui
fixe le coût : la correction touche **le moteur ET la page**, pas la page seule.

## Le témoin positif est DANS LA MÊME LIGNE

```text
performance_page.py:446   <td>${VX.fmt.nd(s.n)}</td>                      ← N
                    :447   Rdt +5 séances    ${VX.fmt.pct(s.avg_5j)}      ← aucun dénominateur
                    :448   Rdt +20 séances   ${VX.fmt.pct(s.avg_20j)}     ← aucun dénominateur
                    :449   % gagnants +5 s   ${VX.fmt.num(s.win_5j,0)}    ← aucun dénominateur
                    :450   TP1 avant stop    ${…tp1_rate…+' % ('+s.tp1_resolved+')'}  ← LE DÉNOMINATEUR EST LÀ
```

**Quatre colonnes chiffrées, une seule expose son dénominateur.** C'est le motif
exact du 457 — *deux dénominateurs justes et un faux sur la même carte* — et il
joue ici le même rôle : **l'instrument n'accuse pas la table en bloc, il désigne
trois colonnes sur quatre**, et il prouve que la bonne pratique est connue de
l'auteur, appliquée à un quart de son propre tableau.

## ATTEIGNABILITÉ — mesurée par exécution, et elle a failli me tromper

`performance_page.py` ne correspond à aucune des huit pages servies, et
`/performance` **n'est pas servie** :

```text
GET /performance             → 301  (redirection)
GET /portfolio?view=performance → 200
```

J'allais en conclure que la table n'atteint pas l'écran. **C'est faux, et
l'exécution le prouve :**

```text
redesign.py:108-111   @bp.route('/journal') → performance_page.render(...)
GET /journal   55 492 octets   « Rdt +20 séances » PRÉSENT · « tp1_resolved » PRÉSENT
```

**`performance_page.py` est le moteur de rendu de `/journal`**, l'une des huit
pages servies. La table est **servie**, et les deux littéraux sont **dans les
octets envoyés au navigateur**.

**Quatorzième récurrence du piège des homonymes, sous une forme neuve encore** :
`vertex/ui/journal.py` est une **page morte** (documentée dans `CLAUDE.md`),
tandis que `vertex/ui/pages/performance_page.py` **est** le journal vivant. **Le
fichier qui porte le nom est mort ; le fichier qui rend la page porte un autre
nom.** Chercher « journal » pour trouver le journal mène au mauvais fichier.

**Compte : arrêté avant publication, 42 → 43.**

## Classement — RANG 1

Ce qui est établi : sur une page servie, **une même ligne affiche `N = 5` et
« +20,0 % à 20 séances »**, alors que le second peut reposer sur **une seule
observation**. Le banc du 417 l'avait mesuré ; la relecture confirme les sites et
ajoute que **le moteur ne publie pas les vrais dénominateurs**.

Rang 1, et je dis pourquoi ce n'est pas moins :
- c'est la page qui **mesure la fiabilité du moteur** — l'endroit où un chiffre
  trompeur coûte le plus cher ;
- le biais est **structurel et permanent**, pas un cas de bord : mesuré au 417
  sur un registre réaliste de 40 séances, la colonne +20 repose sur **51 % de
  `N`** ;
- et **la page elle-même sait faire mieux**, une colonne sur quatre.

Rang 1, et pas plus : **aucun nombre n'est fabriqué.** `avg_20j` est exact **sur
son propre sous-ensemble**. Le défaut est une **attribution de dénominateur** —
la même famille que le 447 (un max pain global attribué à une échéance nommée),
classé rang 1 lui aussi. La cohérence de l'étalon est respectée.

## La mutualisation avec le lot de travail B — mesurée, et elle est partielle

```text
464  track_record.record()  :52-58   ÉCRITURE du ledger — ajouter la provenance
417  track_record.evaluate() :163-166  LECTURE/agrégation — exposer les dénominateurs
```

**Même fichier, deux fonctions différentes, deux gestes indépendants.** Ce n'est
pas la mutualisation forte du 474 (461 et 433 dans la même fonction) : ici on
ouvre le même fichier deux fois, mais on ne touche pas les mêmes lignes.

**Recommandation : les faire ensemble quand même** — une seule ouverture de
`track_record.py`, un seul examen de régression sur les mêmes tests
(`test_track_record_lot89.py` couvre les deux zones). **Le lot de travail B passe
de 6 à 8 lignes et gagne un second rang 1.**

---

# LE CHIFFRAGE

```text
MOTEUR — vertex/engines/track_record.py
  :163-166   exposer 'n_5j': len(b['f5']) et 'n_20j': len(b['f20'])        2 lignes

PAGE — vertex/ui/pages/performance_page.py
  :447  Rdt +5 séances   → suffixer ' (' + s.n_5j + ')'                     1 ligne
  :448  Rdt +20 séances  → suffixer ' (' + s.n_20j + ')'                    1 ligne
  :449  % gagnants +5 s  → suffixer ' (' + s.n_5j + ')'                     1 ligne
                                                                    ─────────
                                                              TOTAL  5 lignes
```

**2 fichiers · 5 lignes · moteur touché OUI** — mais c'est un **ajout de deux
clés** dans un dictionnaire de retour, aucun calcul modifié, aucun seuil déplacé.

**Ce qu'il ne faut PAS faire** : durcir `n >= 5` en `len(f20) >= 5`. Cela
supprimerait des colonnes légitimes (+1 et +5 séances sont valides bien avant
+20) et **cacherait l'information au lieu de la qualifier**. Le geste juste est
d'**afficher le dénominateur**, exactement comme la quatrième colonne le fait
déjà.

## Gardien et régression

```text
gardien       tests/test_denominateurs_track_record_lot4xx.py
assertion     agg() expose un dénominateur par colonne chiffrée, ET les octets servis
              de /journal affichent ce dénominateur pour « Rdt +20 séances »
échoue-t-il aujourd'hui ?   OUI — mesuré ligne à ligne : agg() (:163-166) renvoie
              `tp1_resolved` et AUCUN équivalent pour f5/f20 ; la page (:447-449)
              n'affiche aucune parenthèse sur trois colonnes sur quatre
gardiens existants   « Rdt +20 » → 0 · « avg_20j » → 0 · « n >= 5 » → 0
                     « tp1_resolved » → 1 et « by_verdict » → 3, tous dans
                     tests/test_track_record_lot89.py
régression    test_track_record_lot89.py touche `agg()` par `by_verdict` : ajouter
              DEUX CLÉS à un dictionnaire de retour ne casse pas une assertion
              d'égalité sur une clé existante — mais un `assert set(d.keys()) == {…}`
              le casserait. À VÉRIFIER AVANT correction. RISQUE FAIBLE À MOYEN.
octet servi ?  OUI (/journal) → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# LA FEUILLE DE DÉCISION — DIX-SEPT DOSSIERS

```text
avant ce lot   16 dossiers · 40 à 48 lignes · 16 gardiens · 11 rang 1
ce lot         +1 dossier (417, RANG 1) · +5 lignes · +1 gardien
après          17 DOSSIERS · 45 à 53 LIGNES · 17 GARDIENS · DOUZE DE RANG 1
```

**Lot de travail B révisé** :

```text
B « les journaux »   464 + 417   8 lignes · 2 fichiers · DEUX RANG 1
                     464 : provenance à l'ÉCRITURE (track_record.py:52-58 + 2 autres moteurs)
                     417 : dénominateurs à la LECTURE (track_record.py:163-166 + performance_page.py)
                     → 417 exige un bump SW (page /journal) ; 464 n'en exigeait aucun.
                       Le lot B passe donc de « aucun bump » à « un bump » — je le signale
                       parce que c'était son principal avantage.
```

Les sept autres lots (A, C, D, E, F, G, H) sont **inchangés**.

## Ce qui reste hors devis

**Dix-sept dossiers jamais classés** (18 − 1) : 388 · 406 · 407 · 408 · 409 ·
411 · 426 · 416 · 422 · 391/396 · 379 · 363 · 378 · 386+431 · 452 (volet rang 2)
· 456+459 · 461 `winnerRule`. Plus les **trois dossiers de DÉCISION** (469, 468,
466/467).

## Ce que le lot ne prétend pas

- **Je n'ai pas rejoué le banc du 417.** Les chiffres du banc (N=5 avec une seule
  observation à +20 ; 51 % de `N` sur 40 séances) sont **ceux de son rapport**, et
  je les cite comme tels. **Ce que ce lot mesure**, c'est que les **sites tiennent**
  et que **le moteur n'expose pas les dénominateurs** — cela suffit à classer et à
  chiffrer.
- **Aucun test n'a été écrit** ; l'échec du gardien est établi **par lecture** de
  `:163-166` et `:447-450`.
- Le risque de régression est qualifié **faible à moyen** parce que je n'ai pas
  ouvert `test_track_record_lot89.py` ligne à ligne pour savoir s'il compare des
  jeux de clés. **Je le nomme comme un point à vérifier, pas comme un fait.**
- **Aucun navigateur.** Le rendu est établi sur les **octets servis** de
  `/journal`, obtenus en `GET` via `test_client`.
- **Aucun réseau. Aucun écrivain appelé. Aucun fichier de production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `app.url_map` lu ; `persist` redirigé vers un `mkdtemp`
  **et la redirection vérifiée par `cache_path()`** ; **`track_record.record()`
  NON appelée** (lecture seule) ; **`/options/<sym>`, `/api/analyst/`,
  `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-dix-huitième lot court, **premier après la clôture du devis**.

Le retour à la mesure produit immédiatement un **douzième rang 1**, et il le
produit vite — parce que le dossier avait déjà été mesuré au 417 et qu'il ne
manquait que **le classement et le chiffrage**. C'est un enseignement de rythme :
**dix-sept dossiers attendent dans cet état**, mesurés mais ni pesés ni chiffrés.
Les ouvrir un par un est peu coûteux et rend un résultat à chaque fois.

Le fait de méthode du lot est une variante inattendue d'un piège connu :

*Le fichier qui porte le nom d'un espace peut être mort, et l'espace rendu par un
fichier qui porte un autre nom.* `vertex/ui/journal.py` est une relique ;
`/journal` est rendu par `performance_page.py`. J'allais conclure « non servi »
sur la foi d'un nom de fichier et d'un `/performance` en 301. **Seul le GET sur
`/journal` a tranché** — et il a montré les deux littéraux dans les octets
envoyés.

**C'est la deuxième fois en trois lots qu'une exécution renverse une conclusion
de lecture** (474 : `app.url_map` pour la collision ; ici : le corps de
`/journal`). La règle mérite d'être posée nettement : **quand une question porte
sur ce que le produit FAIT, l'exécution tranche et la lecture propose.**

Comptes séparés : résultats faux **arrêtés avant publication** **43** (+1, le
« `performance_page` non servi ») ; **publiés puis corrigés** **5** ;
**interprétations retirées** **3** ; re-localisation **0**.

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre désormais
dix-sept dossiers, douze de rang 1, pour 45 à 53 lignes.**
