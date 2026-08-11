# SKYLER LOT 514 — Le schéma du 513-A a une COPIE, et elle est **SERVIE**. Sur la fiche d'un titre, en facteur positif d'un ACHAT FORT : « **Parmi les meilleurs de l'univers scanné (top 0 %)** ». Premier dossier VISIBLE depuis quatre lots

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-514` (base : lot 513 fusionné,
`6d8dd2a4`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(c)** — la règle **509-B** (« chercher la copie ») appliquée au dossier du
513. Le 513-A n'est pas un bug de percentile : c'est un `round()` posé **avant**
une dérivation, qui détruit la résolution au moment de l'arrondi. Trois rangs 4
d'affilée, tous **latents** ; il fallait un instrument capable d'atteindre du
**visible**.

## L'instrument, et sa première calibration ÉCHOUÉE

Le dépôt porte **777 `round(`**, **132 `int(`**, **83 `Math.round(`** et
**148 `toFixed(`** — 1 140 sites. Un grep ne trie rien. J'ai écrit un crible
**AST** à trois étages :

```text
S1  arrondi imbriqué dans l'arithmétique   `100 - round(x)`
S2  arrondi passé par une variable locale  `p = round(x)` … `100 - p`
S3  arrondi passé par un CHAMP             producteur → clé de dict → relecture
```

Calibration obligatoire : **le 513-A doit être retrouvé**. Premier jet :

```text
CALIB 2 · POSITIF — le 513-A est-il retrouvé par S3 ?   NON
          « _pct_rank » reconnu comme producteur ?      NON
```

**Échec.** Cause : je définissais un « producteur d'arrondi » comme une fonction
dont **tous** les `return` sont arrondis. Or `_pct_rank` commence par
`if not vals or x is None: return None` — **la garde d'absence honnête**. Ma
définition excluait donc exactement les producteurs **bien écrits**. Corrigée en
ignorant les `return None`, la calibration passe 4/4 et retrouve
`context.py:98`.

**Un crible qui rate le défaut dont il est né aurait tout raté.** C'est la
deuxième fois en trois lots qu'une calibration à réponse connue m'évite de
publier un zéro.

## Le résultat

```text
1 140 arrondis dans le dépôt
  155 signalés par le crible (S1 12 · S2 66 · S3 77)
        F1  complément de pourcentage « 100 - X »      4
        F2  différence de deux arrondis                0
        F3  division par un arrondi                   24
        reste (arithmétique sans perte notable)      127
```

**F1 tient en quatre lignes**, dont deux sont le même site de `demo.py` compté
deux fois (génération de données de démonstration : `100 - score` pour un PUT,
complément légitime, aucun percentile en jeu). Restent **deux vrais sites** :

```text
vertex/engines/context.py:98    'Top %d%% de l'univers' % (100 - sc['pct_universe'])   ← le 513-A
vertex/engines/evidence.py:151  f'… (top {100 - sc["pct_universe"]}%)'                 ← LA COPIE
```

## Le piège d'homonyme, 29ᵉ récurrence — cette fois sur un nom de MODULE

J'ai d'abord conclu que la copie était servie **parce que `/api/evidence/<sym>`
existe et que la page détail l'appelle**. **Faux.** Cette route utilise
`evidence_lab`, un **autre module**. `vertex/engines/evidence.py` n'a rien à voir
avec elle.

La vraie chaîne, retrouvée en **lisant** :

```text
evidence.relative_analyst(context)              engines/evidence.py:143
  ← evidence.gather(...)                        engines/evidence.py:216
  ← decision_stack.evaluate(context=...)        engines/decision_stack.py:270
  ← /api/decision/<sym>   (ctx = _ctx_for)      routes/decision_api.py:79-86
  ← page /analysis/<sym>                        route CITÉE (établie au 511)
```

## 514-A — mesuré de bout en bout

Carte de **517 titres fabriquée en mémoire**, sommet unique (le cas ordinaire),
`decision_stack.evaluate` appelé en processus :

```text
n =   20 → « Parmi les meilleurs de l'univers scanné (top 2%) »       sensé
n =   50 → « … (top 1%) »                                             sensé
n =  100 → « … (top 0%) »                                        ← BASCULE
n =  517 → « … (top 0%) »                                        ← PRODUCTION
```

Et la décision complète, avec tous les champs requis :

```text
decision  : STRONG_BUY · Achat fort
bloque ?  : False · grade A
pros      :
   - Surperforme le marché (force relative 90)
   - Marché RISK-ON — appétit pour le risque
   - Régime de marché en tendance
   - Parmi les meilleurs de l'univers scanné (top 0%)      ← ICI
   - Leader de son secteur (SEC0)

dernier titre · cons :
   - Parmi les plus faibles de l'univers scanné (bas 0%)
```

Ce n'est **pas** un état dégradé : `blocks_decision` est `False`, la qualité de
données est **grade A**, la décision est **ACHAT FORT**. Et la page peint bien
ces lignes :

```js
'<div class="vx-meta vx-mb1">Facteurs positifs</div>'
  + pros.map(p => '<div class="vx-pos" …>+ ' + esc(p) + '</div>')
```

**La phrase est affichée, sous « Facteurs positifs », en soutien d'un achat.**

## Classement — rang 2

C'est le premier dossier **visible** depuis le 508. Un chiffre absurde est peint
sur une page servie, dans une ligne d'aide à la décision : « parmi les meilleurs
(top 0 %) » se contredit — un titre qui figure dans la liste ne peut pas être
dans le « top 0 % ».

**Pas rang 1** : l'affirmation qualitative reste **vraie** (le titre est bien
parmi les meilleurs), aucune décision ne bascule, aucun ordre n'est passé,
READONLY intact. Le défaut porte sur le **nombre entre parenthèses**, pas sur le
sens de la phrase.

**Pas rang 3 ou 4** : contrairement au 512-A et au 513-A, ce n'est pas latent.
La ligne atteint l'écran d'un utilisateur, dans le contexte le plus sensible qui
soit — la justification d'un achat fort.

Correction pressentie, non engagée : la même que celle du 513 — plancher la
formulation, ou passer à l'ordinal. **Deux sites à traiter ensemble, pas un.
Aucun GO, rien n'est engagé, rien n'est supprimé.**

## Le second contrôle — mon crible est PYTHON, et je le borne

Le crible ne voit **rien du JavaScript**, c'est-à-dire rien de ce qui est le plus
proche de l'écran. Mesuré dans les octets servis : **154 `Math.round(`** et
**213 `toFixed(`**.

```text
arrondi JS en aval d'une soustraction/division    0
arrondi JS en amont d'une soustraction/division  24   → 24 contextes distincts
```

**Les 24 sont tous l'idiome de précision `Math.round(x*p)/p`** (« arrondir à n
décimales »), et presque tous viennent du vendor minifié `lightweight-charts`.
**Aucun n'est le schéma destructeur.** L'angle mort est donc mesuré et **vide** —
mais c'est une mesure, pas une supposition.

Restent deux angles morts que je n'ai **pas** criblés du tout : **253 `//`** et
**82 `%`** numériques en Python. **Le « 4 en F1 » est un compte PYTHON, pas un
compte du dépôt.** (Règle 510-B.)

## Ce que le crible retrouve d'autre, et qui n'est pas neuf

Les 24 sites de **F3** sont en bonne partie les conversions IV du **507-A**
(`options_intel_api.py:64`, `redesign.py:221/224`). Le crible a donc **retrouvé
un dossier connu sans que je le lui indique** — confirmation faible mais réelle
de l'instrument. Je ne les recompte pas comme neufs.

## Arrêts avant publication

1. **La calibration du détecteur de producteurs** — sans la réponse connue
   d'avance, je publiais « 0 site en F1, le 513-A est isolé », faux.
2. **L'homonyme `evidence` / `evidence_lab`** — j'allais écrire que la copie est
   servie via `/api/evidence/<sym>`. Elle l'est, mais par une **tout autre
   chaîne** ; la raison que j'allais donner était fausse.

**Arrêtés avant publication : 105 → 107.**

## Portée — ce que ce lot NE dit PAS

- **Aucun scan de production lancé.** Les 517 titres sont une carte **fabriquée
  en mémoire** passée à `context_for` et `decision_stack.evaluate` (liste sûre,
  en processus). Aucun réseau.
- **La condition `k ≤ n/100` reste non vérifiée sur données réelles** (dette du
  513, toujours ouverte). En DÉMO (n = 20) la phrase est correcte : le défaut est
  invisible dans le seul environnement exécutable.
- Le crible est **littéral et Python**. Il ne suit qu'**un** saut de champ, ignore
  le JS, `//` et `%`.
- `_standing`, les percentiles bruts sérialisés et la partie « Leader de son
  secteur » restent **corrects à toutes les tailles** (règle 509-C).
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les quatre bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2**. **La veine
repart.** Trois lots latents d'affilée m'avaient fait écrire que « la chasse aux
défauts ne rend plus rien » ; c'était vrai de l'instrument, pas du dépôt. En
changeant d'angle — chercher le **schéma** plutôt que le symptôme — le même
défaut ressort sur un chemin **servi**.

L'enseignement de méthode est net : **le 513-A était la moitié du dossier.** Je
l'ai classé rang 4 parce que je l'avais trouvé dans du code non affiché, sans
chercher si la même faute vivait ailleurs. La règle 509-B existait déjà. Je ne
l'avais pas appliquée à mon propre dossier.

Feuille : **35 dossiers · seize rang 1 · **douze** rang 2 · cinq rang 3 · trois
rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **mesurer le
contenu des 23 routes non appelées** ; **la condition `k ≤ 5` sur un scan réel** ;
**cribler `//` et `%`** (dette neuve) ; **un producteur de synthèse d'une autre
forme** ; **l'espion au troisième niveau** ; **le compte des rangs relatifs
postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 107 (+2)** ; publiés
puis corrigés **13** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
