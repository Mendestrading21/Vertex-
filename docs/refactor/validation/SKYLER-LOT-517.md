# SKYLER LOT 517 — L'instrument du 516 est **réparé** : il retrouve enfin son propre cas de référence. La zone aveugle contenait **exactement un** cas — et c'est le 513-A, que je connaissais déjà. Le « 8 » du 516 devient **9**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-517` (base : lot 516 fusionné,
`f2db5903`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** — la dette que le 516 venait de créer, et la plus embarrassante : mon
recensement des phrases calculées **ratait mon propre dossier 513-A**, parce que
`context._headline` s'assemble morceau par morceau et que son plus long fragment
littéral (« de l'univers », 13 caractères) passe sous le seuil de prose.

La règle 516-A dit : *un instrument doit retrouver son propre cas de référence ;
s'il ne le peut pas, publier la borne plutôt que le chiffre.* **Le 516 a borné.
Le 517 répare.**

## L'instrument neuf — l'unité n'est plus l'expression, c'est la fonction

```text
A. repérer les fonctions ASSEMBLEUSES  (x.append(…) / x += … puis SEP.join(x))
B. agréger TOUS leurs fragments littéraux, tester la prose sur l'AGRÉGAT
C. marquer NUMÉRIQUE si un morceau interpole une arithmétique
D. mesurer l'atteignabilité comme au 516 (octets servis ou charge d'une route sûre)
```

## La réparation a échoué au premier jet, et pour une raison précise

```text
CALIB 2 · POSITIF — `context._headline` retrouvée ?   NON
```

Cause : `parts.append('Top %d%% …' % (…) if pct >= 50 else 'Bas %d%% …' % pct)`.
L'argument de `append` n'est **ni un f-string ni un `%`** : c'est un **ternaire**
(`ast.IfExp`) qui les **contient**. Mon extracteur ne descendait pas dedans.

Corrigé en récursant dans `IfExp`, `BoolOp` et les arguments d'appel :

```text
CALIB 2 · POSITIF — `context._headline` retrouvée ?   OUI
   vertex/engines/context.py:93   numérique=True   atteinte=CHARGE D'UNE ROUTE APPELÉE
   agrégat « Top de l'univers Bas de l'univers # / dans »
```

**Sans la calibration à réponse connue, je publiais « la famille assemblée ne
contient rien » avec un extracteur cassé.** C'est la deuxième fois en quatre lots
(514, puis 517) qu'un crible rate le défaut dont il est né. **Arrêtés avant
publication : 112 → 113.**

## Le résultat — et il est modeste, je le dis

```text
fonctions assembleuses à prose française            38
   dont ATTEIGNENT l'écran                          11
   dont porteuses d'un NOMBRE CONSTRUIT              1   ← le 513-A
```

```text
comptage corrigé des phrases à nombre construit atteignant l'écran
   516 (plus long morceau)      8
   517 (agrégat par fonction)  +1
   ─────────────────────────────
   TOTAL                        9
```

**Le « 8 » du 516 était une borne basse — d'exactement un.** Et ce un n'est pas
une découverte : c'est le dossier que je traquais depuis le 513. **La zone
aveugle était réelle, elle était petite, et elle ne contenait rien de neuf.**

C'est un résultat décevant et c'est le bon : une borne annoncée vaut d'être
fermée, même quand elle se ferme sur zéro nouveauté.

## Le second contrôle — ce que l'agrégateur par fonction exclut

**Angle mort I — l'assemblage ENTRE fonctions** : un auxiliaire rend un morceau,
l'appelant le joint ; aucune fonction ne porte l'agrégat. **Mesuré : 7
jointures** dont les morceaux viennent d'appels et non de littéraux locaux
(`skyler_core.operational_state`, `response_validator.validate_analysis`,
`design_system_page._swatches`…).

**Angle mort II — les tables de libellés au niveau MODULE** : la fonction ne
contient aucun littéral, elle lit un dictionnaire. Mesuré :

```text
tables de libellés français au niveau module      ~30
libellés qu'elles portent                         380
   dont porteurs d'un GABARIT (%d, %s, {x})         1   ← et c'est du BALISAGE
                                                        (system_page._VIEW_CONTENT)
```

**C'est le point décisif du contrôle.** Ces 380 libellés échappent bien à mon
crible — mais **379 sur 380 sont STATIQUES**. Un libellé sans gabarit ne peut
pas, par construction, porter un **nombre construit**. **L'angle mort est donc
réel pour le comptage des phrases, et vide pour le comptage qui m'intéresse.**
Le **9** tient.

Je le souligne parce que c'est exactement le genre de nuance que j'aurais pu
manquer : compter 380 échappées et en conclure « mon chiffre est très
sous-estimé » aurait été faux d'un raisonnement, pas d'une mesure.

## Ce que le dépôt fait bien

- Les 380 libellés en tables de constantes sont un **bon schéma** : le texte
  utilisateur est regroupé, relisible, séparé de la logique. C'est précisément
  parce qu'il est bien rangé qu'il est statique, donc sans risque de nombre
  faux.
- Sur les 11 phrases assemblées qui atteignent l'écran, **dix ne portent aucun
  nombre** : ce sont des énumérations de conditions, de raisons, de
  confirmations. Aucune ne peut afficher un chiffre erroné.

## Portée — ce que ce lot NE dit PAS

- **Aucun dossier neuf.** Le seul cas numérique retrouvé est le 513-A, déjà
  publié et déjà classé.
- L'atteignabilité se mesure comme au 516 : fragment présent dans les octets
  servis **ou** dans la charge utile d'une route appelée. **Qu'un octet reçu soit
  peint reste une question distincte** — et le 516 a montré, avec la coupe à
  cinq, qu'elle se juge mal sans mesure.
- Le crible reste **Python**. Le français assemblé en JavaScript (dette du 516,
  majorant grossier 336) **n'est pas traité ici**.
- Mesuré sur le scan **DÉMO (20 titres)**, avec **les 20 titres interrogés**
  (règle 516-C).
- **Aucun navigateur, aucun POST, aucune route interdite appelée.** 61 routes
  sûres.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0**.

**Trois lots consécutifs sans dossier neuf**, et je ne vais pas l'habiller : les
515, 516 et 517 ont tous les trois été consacrés à **réparer ou borner mon
propre appareil de mesure**. Le 515 a corrigé un chiffre publié faux d'un facteur
6,7 ; le 516 a corrigé la vitrine du 514 et découvert que son crible ratait le
513-A ; le 517 a réparé ce crible pour découvrir que la zone aveugle ne
contenait que le 513-A.

C'est de l'hygiène, et l'hygiène était nécessaire — **quinze chiffres publiés
puis corrigés** en dit assez. Mais trois lots de suite à mesurer mes propres
instruments plutôt que le produit, cela mérite d'être dit sans détour :
**la veine d'audit sur cet axe est épuisée.** Les dettes qui restent sont soit
anciennes et jamais entamées (les 29 vues hors empreinte, les 23 routes non
mesurées), soit coûteuses et de rendement incertain (l'analyseur JS).

Je ne décide pas seule de changer de registre. Je constate.

Feuille **inchangée : 35 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
trois rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** (la plus
ancienne, jamais entamée) ; **mesurer le contenu des 23 routes non appelées** ;
**le français construit en JavaScript** ; **l'assemblage entre fonctions**
(7 cas, dette neuve) ; **la condition `k ≤ 5` sur un scan réel** ; **recribler les
chiffres publiés par motif textuel** ; **le compte des rangs relatifs postérieurs
au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 113 (+1)** ; publiés
puis corrigés **15** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
