# SKYLER LOT 374 — L'angle mort des `<script>` concaténés : réel, mais sans surface exploitable

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-374` (base : lot 373 fusionné,
a3dee84)

## Piste calibrée

Angle mort déclaré par le lot 373 lui-même : son balayage ne voyait que les
interpolations situées dans **une** chaîne littérale contenant `<script`. Un bloc
ouvert dans une constante et fermé dans une autre lui échappait entièrement —
tout ce qui est concaténé entre les deux vit en contexte JS sans qu'aucun gardien
ne le sache.

## Mesure — l'angle mort existe bien

Balayage `os.walk` (52 fichiers Python, périmètre vérifié dès le départ) des
chaînes littérales dont les balises `<script>` ne s'équilibrent pas :
**15 littéraux déséquilibrés**, soit **4 points de concaténation**.

```text
terminal.py:5883/5894   PAGE_DAILY   ← _OPP_BRIEF_JS, _sync_ui.JS   (constantes)
terminal.py:6302        _inject_vx   ← _VX_JS_FULL                  (constante)
vertex/ui/home_art.py:137            ← ART_CSS, ART_JS              (constantes)
terminal.py:6474        _vpage       ← js  ⚠ PARAMÈTRE
```

Trois sites n'assemblent que des **constantes de module**. Le quatrième —
`_vpage(title, body, head='', js='')`, qui fait
`'…</div><script>' + js + '</script>…'` — est le seul à recevoir un **paramètre**.

## Pourquoi c'est sain quand même

Deux raisons, la seconde décisive :

1. Les **7 appelants** de `_vpage` passent tous une constante de module
   (`js=_SETTINGS_JS`, `js=_BORDEL_JS`…), évaluée à l'import.
2. **Les 7 pages ainsi construites ne sont plus servies.** Sondé :

```text
/bordel    HTTP 301 → /intelligence              /equipe    HTTP 301 → /intelligence?view=strategy
/review    HTTP 301 → /intelligence?view=committee  /settings HTTP 301 → /system?view=settings
/research  HTTP 301 → /intelligence?view=research   /health   HTTP 301 → /system?view=data
/heatmap   HTTP 301 → /markets?view=sectors
```

La table `_LEGACY` de `vertex/app/routes/redesign.py` les masque toutes. Les
constantes `PAGE_*` sont construites, mutées par la boucle d'onglets, puis
**jamais renvoyées**.

Contrôle croisé sur les octets réellement servis — balises équilibrées partout :

```text
/ 12/12 · /markets 15/15 · /opportunities 17/17 · /analysis 10/10
/portfolio 18/18 · /options 18/18 · /journal 11/11 · /system 12/12
```

**Verdict : l'angle mort est réel, il n'a aucune surface exploitable. Rien touché.**

## Deux corrections de méthode — sur mon propre gardien

**(a) L'invariant syntaxique criait au loup.** Ma première version exigeait que
`js` soit un littéral ou un nom lié à un littéral. Elle signalait `_BORDEL_JS`
comme « calculé ». Vérification : `_BORDEL_JS` concatène des littéraux **et trois
noms de constantes**. Détecteur trop étroit → résolution **transitive** par point
fixe.

**(b) Toujours rouge — et c'était encore moi.** Deux de ces trois constantes sont
produites par `_extract(PAGE_DAILY, …)` : constantes **à l'import**, mais pas
littérales au sens statique. J'ai alors compris que l'invariant syntaxique est le
**mauvais outil**. La propriété qui protège réellement n'est pas « `js` est un
littéral » mais « **la valeur de `js` ne contient pas de balise fermante** ». Le
gardien vérifie désormais cela sur les **valeurs réelles**, et ne garde le
contrôle statique que pour interdire un `js` calculé **par requête**.

**8ᵉ et 9ᵉ fois** de la boucle qu'un doute sur l'outil change le résultat. Les
deux fois ici, mon gardien accusait du code sain — l'erreur symétrique de celle
qu'on redoute d'habitude, et tout aussi coûteuse : un gardien qui crie au loup
finit désactivé.

## Constat de poids mort — mesuré, non engagé

Ces 7 constantes représentent **618 527 octets (604 Ko) de HTML assemblés à
chaque import** de `terminal.py`, pour n'être jamais renvoyés :

```text
PAGE_BORDEL   109 291      PAGE_HEATMAP   85 274      PAGE_HEALTH    82 134
PAGE_EQUIPE    89 387      PAGE_REVIEW    82 329      PAGE_SETTINGS  82 719
PAGE_RESEARCH  87 393                                 (import : 1,91 s)
```

Candidat naturel pour les purges É2/É3 — **dossier en attente de GO, rien n'est
engagé ici.** Je ne mesure pas quelle part des 1,91 s leur revient : il faudrait
les retirer pour le savoir, ce qui est précisément ce que je n'ai pas le droit de
faire sans accord.

## Gardien

`tests/test_script_concatene_lot374.py` (21 tests) :

- **anti-vide** ×3 : ≥ 4 littéraux déséquilibrés, ≥ 7 appels `_vpage`, ≥ 7 `js` ;
- **la vraie propriété** : aucune valeur `js` ne contient de balise fermante ;
- **complément statique** : `js` reste une valeur d'import, jamais une expression
  calculée par requête ;
- balises `<script>` équilibrées sur les 8 pages servies, avec exigence de ≥ 8
  blocs — sinon l'équilibre serait vrai sur une page vide ;
- **le fait dont dépend le verdict** : les 7 routes héritées redirigent toujours,
  vers une cible **interne** ; si l'une redevient servie, le message d'échec
  réclame le réaudit du bloc concaténé ;
- **anti-péremption** : si les constantes disparaissent (purge engagée), le
  gardien exige d'être mis à jour plutôt que de passer à vide.

### Preuve ROUGE

```text
ROUGE OK  balise fermante dans un JS concaténé       | restauration identique
          1 failed, 20 passed
ROUGE OK  `js` calculé par requête (angle mort)      | restauration identique
          1 error
ROUGE OK  route héritée /bordel reservie             | restauration identique
          1 failed, 20 passed
ROUGE OK  balise <script> non refermée dans le shell | restauration identique
          8 failed, 13 passed
après restauration : 21 passed
VERDICT : gardien mordant sur les 4 cas
```

Précision honnête sur le cas 2 : il remonte en **erreur de collecte**, pas en
échec d'assertion — un `js` lu depuis `request` casse l'import du module hors
contexte de requête. L'assertion statique l'attraperait aussi (le nœud est un
`Call`, ni littéral ni nom de constante), mais ce n'est pas elle qu'on voit
mordre ici.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 373, a3dee84) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2672 → 2693 passed / 2 skipped** — verte (+21).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Le déséquilibre est mesuré **par chaîne littérale**. Un bloc `<script>` ouvert et
fermé dans la même constante mais interpolé par une variable au milieu relève du
lot 373, pas d'ici. Les trois sites à constantes n'ont pas été sondés
individuellement : leur sûreté vient de ce qu'aucune donnée externe n'y entre,
pas d'une mesure sur charge hostile. Et la sûreté de `_vpage` est **conditionnelle
à l'inaccessibilité des 7 pages** — c'est un fait de routage, pas une propriété
du code, d'où le gardien qui l'ancre.

## Suite

LOT 375 : veille active. Pistes ouvertes — (b) promesses de docstrings en un seul
mot majuscule et docstrings de **fonctions** ; (c) les trois sites de
concaténation à constantes, sondés pour eux-mêmes. Prochaine échéance
périodique : **~lot 380**.
