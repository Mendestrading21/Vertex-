# SKYLER — LOT 609 · LE PRODUCTEUR REND TROIS VALEURS, LE CONSOMMATEUR EN ATTEND MILLE

Le brief demandait de mesurer ce que le sentiment ternaire perd **réellement**,
et ajoutait : *s'il ne perd rien de décidable, ne rien changer et le dire.* La
mesure a trouvé autre chose, et **le lot ne change rien au comportement.**

## Ce que la mesure a trouvé

`news_plus.sentiment()` rend **exactement** `-1`, `0` ou `+1`. Ses deux
consommateurs de `news_impact.py` ont été écrits pour un score **continu** :

```python
score_importance :  if isinstance(senti, (int, float)) and abs(senti) >= 0.5: score += 5
potential_impact :  if senti >  0.15: {'direction': 'POSITIF_POTENTIEL',
                                       'confidence': min(0.7, abs(senti))}
                    if senti < -0.15: … même forme …
                    else            : {'direction': 'NEUTRE', 'confidence': 0.3}
```

**Énumération exhaustive du domaine** — trois valeurs, il n'existe pas d'autre
cas, ce n'est donc pas un échantillon mais une preuve :

| `senti` | `abs ≥ 0.5` → +5 | direction | confidence |
| --- | --- | --- | --- |
| **−1** | OUI (+5) | `NEGATIF_POTENTIEL` | **0.7** |
| **0** | non | `NEUTRE` | **0.3** |
| **+1** | OUI (+5) | `POSITIF_POTENTIEL` | **0.7** |

**Valeurs du domaine séparées par `0.15` mais pas par `0.5` : AUCUNE.** Les deux
seuils partitionnent le domaine **à l'identique** : écrits comme des seuils
d'intensité, ils ne distinguent que **signé** de **neutre**.

Et `confidence: min(0.7, abs(senti))` **a l'air calculé** ; sur le domaine réel
il ne prend **qu'une valeur par direction**. **C'est un littéral déguisé en
calcul.**

## Ce que ça coûte, exactement — et ce que ça ne coûte pas

**Ça ne ment à personne aujourd'hui** : `confidence` n'est affichée nulle part
(seule `direction` l'est, dans l'« Actualité dominante » de `/`). Le défaut n'est
pas un mensonge à l'écran, c'est un **désaccord silencieux entre deux moitiés du
code** — et il piégera quiconque touchera l'une des deux.

Le sentiment **a bien une conséquence visible**, mesurée : à catégorie égale, le
`+5` départage deux actualités (45 contre 40) et décide donc **laquelle est
affichée**. Deux états utiles, là où le code en suggère un continuum.

## Ce que le lot NE fait PAS, et pourquoi

**Il n'ajoute pas d'amplitude.** Une forme `(pos−neg)/(pos+neg)` donnerait des
décimales — donc l'apparence d'une mesure — bâties sur **22 mots positifs et
22 négatifs**. Un « 0,333 » issu de trois mots-clés a l'air d'une mesure et n'en
est pas une. **Tant qu'on ne peut pas montrer que l'amplitude est fondée, le
ternaire est plus honnête que le continu.**

Ce que le lot corrige, c'est **le silence** : le contrat est désormais écrit aux
deux bouts, et gardé.

## L'arrêt du lot — une mutation qui ne mutait pas

Mon test de mutation « déplacer le seuil `0.5` → `1.5` » a rendu **7 verts**. Je
l'ai d'abord lu comme « le gardien est faible ».

En vérifiant : `abs(senti) >= 0.5` apparaît **deux fois** dans le fichier — la
ligne de code, **et la docstring que je venais d'écrire pour la documenter**. Mon
`replace(…, 1)` a frappé la docstring. **La mutation n'a jamais muté quoi que ce
soit** ; le gardien n'avait rien à attraper.

C'est **600-A** dans une forme nouvelle : non pas une calibration qui passe sur
un ensemble vide, mais **une mutation qui passe parce qu'elle n'a pas eu lieu** —
et la cause est mon propre travail de documentation, qui a créé un leurre
textuel. Mutation refaite sur la **ligne de code**, ancrée par son indentation et
son `if` : **2 rouges**.

**Arrêtés avant publication : 241 → 242 (+1).**

## Le gardien, rouge dans les deux sens

`tests/test_sentiment_contrat_lot609.py` — **7 tests**, vérifiés par mutation
**des deux côtés** (608-B) :

- **producteur rendu continu** *(`(pos−neg)/(pos+neg)`)*, seuils inchangés →
  `test_le_producteur_est_ternaire` **rouge** ;
- **seuil du consommateur déplacé**, producteur inchangé →
  `test_les_deux_seuils_partitionnent_le_domaine_a_l_identique` et
  `test_le_lot_609_n_a_rien_change_au_comportement` **rouges**.

Le jour où quelqu'un rendra le sentiment continu, le gardien lui dira que ces
seuils et cette confiance ont été écrits pour un continuum **qu'ils n'ont jamais
reçu**. Plus un garde-fou de volume (591-C) : le banc doit exercer **les trois**
valeurs, sinon il ne vérifie rien.

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « le ternaire perd de l'information exploitable » | **CONFIRMÉ** — « 3 positifs / 2 négatifs » et « 1 positif » rendent la même chose |
| **(b)** | « la perte a une conséquence visible » | **CONFIRMÉ, mais pas où je croyais** — rien n'affiche l'agrégat de `/news-feed` ; la conséquence passe par le `+5` d'importance et le choix de l'actualité affichée |
| **(c)** | « le lexique couvre une part majoritaire des titres » | **NON MESURABLE** — aucun corpus de news hors ligne ; ne pas conclure vaut mieux qu'estimer |
| **(d)** | « le bon correctif est un score continu » | **RÉFUTÉ** — ce serait de la fausse précision ; le vrai défaut était le **désaccord de contrat**, pas la granularité |
| **global** | | **le piège visait la granularité ; le défaut était le contrat** |

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure `sentiment()` **sur des titres**. Le cas exclu : **le chemin
d'appel réel**, `terminal.py:1172`, qui concatène `title + ' ' + fr` — titre
**et** traduction française. Un texte deux fois plus long touche mécaniquement
plus de mots du lexique.

Vérifié : cela **ne change pas le domaine** — quel que soit le nombre de mots
touchés, la sortie reste `pos > neg`, donc `{-1, 0, +1}`. **Le second contrôle
confirme que la conclusion ne dépend pas de la longueur du texte**, ce que la
mesure sur titres seuls ne pouvait pas garantir.

## Ce que le lot n'établit pas

- **À quelle fréquence le lexique se déclenche en production.** Sans corpus hors
  ligne, la question reste ouverte — et c'est elle qui déciderait si une
  amplitude vaut le coup.
- **Qu'une amplitude serait pire.** Elle serait **non fondée**, ce qui n'est pas
  la même chose que fausse. Je refuse de l'ajouter faute de preuve, pas faute
  d'idée.
- Que les 22+22 mots soient les bons : le lexique n'a pas été audité.
- Que `confidence` ne sera jamais affichée. Si elle l'était un jour, elle
  deviendrait un chiffre inventé montré comme réel — le gardien préviendra.

## Règles neuves

- **609-A — DOCUMENTER UNE VALEUR PEUT ANNULER LE TEST QUI LA VÉRIFIE.** Écrire
  `abs(senti) >= 0.5` dans une docstring crée un **leurre textuel** : la mutation
  suivante frappe le commentaire et « passe ». Muter la **ligne de code**, ancrée
  par son indentation et sa syntaxe, jamais un motif qui existe aussi en prose.
- **609-B — UN LITTÉRAL DÉGUISÉ EN CALCUL EST PIRE QU'UN LITTÉRAL.**
  `min(0.7, abs(senti))` sur un domaine ternaire vaut toujours `0.7` : la forme
  promet une mesure que le domaine ne permet pas. Un `0.7` écrit franchement
  serait relisible ; celui-ci se lit comme une mesure et n'en est pas une.
- **609-C — REFUSER D'AJOUTER DE LA PRÉCISION EST UN RÉSULTAT.** Le brief
  autorisait « ne rien changer et le dire ». Des décimales sur un lexique de 44
  mots rendraient la mesure **plus crédible sans la rendre plus juste**.

## Ce que le dépôt fait bien

- **`potential_impact` refuse déjà d'affirmer** : `POSITIF_POTENTIEL`, jamais
  « causera ». Le vocabulaire de prudence était en place ; c'est la confiance
  chiffrée qui dépassait.
- **`score_importance` est déterministe et lisible** : chaque terme est une
  ligne, aucun poids caché.
- **`sentiment()` sépare honnêtement le neutre du mixte** : `pos == neg` rend `0`,
  pas un signe arbitraire.
- **Rien n'affiche `confidence`** — la valeur douteuse n'a jamais atteint
  l'écran. Le produit s'est protégé sans le savoir.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/services/news_plus.py`,
  `vertex/market/news_impact.py` — **docstrings uniquement, aucune ligne de
  logique modifiée**.
- **1 gardien neuf** (7 tests, rouge dans les deux sens).
- MD5 des 8 pages : **8 / 8 identiques**. **Aucun bump** — aucun octet servi ne
  change, SW inchangé à `td-shell-v193`.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2894 passed / 0 skipped** *(2887 + les 7 du gardien neuf)*.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **242 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 7** *(inchangé — ce lot ne corrige pas un défaut
  produit, il ferme un désaccord de contrat)*
