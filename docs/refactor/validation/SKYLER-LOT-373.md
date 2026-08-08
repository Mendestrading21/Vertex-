# SKYLER LOT 373 — La faute du lot 372 sous ses autres habillages : un danger latent sur les 8 pages

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-373` (base : lot 372 fusionné,
e3074e8)

## Piste calibrée

Le lot 372 a corrigé `json.dumps` nu **vers un gabarit `%%…%%`**, dans **trois
pages**. Mais la faute réelle est plus large : **toute valeur non littérale
interpolée à l'intérieur d'une région `<script>`** peut fermer la balise. Restait
à balayer les autres formes (f-strings, `%`-format) et les autres producteurs de
HTML.

## Correction de méthode — avant tout résultat

Ma première passe listait les fichiers avec `os.listdir` sur `vertex/ui`,
`vertex/ui/pages` et `vertex/app/routes`. `os.listdir` **ne descend pas dans les
sous-dossiers** : `vertex/ui/shell/__init__.py` — le producteur HTML **central**,
celui qui assemble les 8 pages — n'a **jamais été lu**. Elle concluait
« 1 interpolation directe, dans le Widget Lab ».

Passe corrigée en `os.walk` : **2** interpolations — et la seconde est
précisément celle qui comptait. **Septième fois** de la boucle qu'un doute sur
l'outil change le résultat, et la première où c'est mon **périmètre de balayage**,
non ma logique, qui mentait.

## Ce que l'audit corrigé trouve

**Gabarits `%%…%%` situés dans un bloc `<script>` : 7 substitutions.**

```text
analysis_page.py:962      %%SYM_JSON%%     sûr   json_for_script(safe)
opportunities_page.py:710 %%PARAMS%%       sûr   json_for_script(p)
opportunities_page.py:710 %%VIEW%%         sûr   json_for_script(view)
opportunities_page.py:710 %%DEMO_BORDER%%  sûr   littéral
portfolio_page.py:1005    %%VIEW%%         sûr   json_for_script(view)
markets_page.py:941       %%VIEW%%         ⚠     view          (brut)
performance_page.py:701   %%VIEW%%         ⚠     view          (brut)
```

**Interpolations directes (f-string / `%`) dans un `<script>` : 2.**

```text
widget_lab.py:1821        f-string  js       ← constante de module (_JS)
vertex/ui/shell/__init__.py:233  f-string  vocab   ← json.dumps NU
```

## Le danger latent — `window.__VXVOCAB`, sur les 8 pages

```python
# vertex/engines/recommendation.py
def vocab_js():
    return json.dumps(_labels_map(), ensure_ascii=False)
```

```html
<script id="vx-vocab">window.__VXVOCAB={vocab};</script>
```

C'est un `json.dumps` **nu** injecté dans un bloc `<script>` **sur les huit
pages** — l'endroit le plus exposé de l'application. Il ne tient aujourd'hui que
parce que `_labels_map()` n'assemble que des **tables littérales du module**
(`DECISIONS`, `HELD`, `_ALIAS`, `TONE_CLS`) : aucune donnée externe, et le
résultat servi (3 689 octets, identique sur les 8 pages) ne contient **ni `<`, ni
`>`, ni `&`**. **Rien ne le vérifiait.** Une seule étiquette future contenant `<`
ferait sortir le script sur les huit pages à la fois.

**Pas exploitable aujourd'hui — donc rien touché.** Le durcissement a été
mesuré et écarté pour une raison précise : `vocab_js` sérialise avec
`ensure_ascii=False`, alors que `json_for_script` laisse la valeur par défaut.
Y appliquer le helper transformerait **tous les accents en `\uXXXX`**, changerait
les octets servis sur les 8 pages et imposerait un bump de service worker — pour
**zéro gain de sécurité**, puisque le contenu ne contient aucun caractère de
balise. Un durcissement qui coûte un bump pour rien n'en est pas un.

Ce qui protège vraiment ici, c'est l'**invariant**, pas le durcissement : le
gardien exige que `vocab_js()` ne contienne jamais `<`, `>` ni `&`, et dit dans
son message d'échec quoi faire le jour où c'est le cas.

## Les deux `%%VIEW%%` bruts — sains, prouvé

```text
markets_page.py / performance_page.py :  const VIEW='%%VIEW%%';
```

Une chaîne JS entre apostrophes : une charge s'en échapperait. Ils tiennent par
la **liste blanche appliquée avant la substitution** (`if view not in
dict(_VIEWS): view = …`). Sondé sur un rendu réel, 4 charges × 2 routes :

```text
/markets  sortie d'apostrophe  HTTP 200 · 70 288 o · VIEW='overview' · brut=non · ACTIF=non
/markets  sortie de balise     HTTP 200 · 70 288 o · VIEW='overview' · brut=non · ACTIF=non
/journal  concaténation JS     HTTP 200 · 55 492 o · VIEW='overview' · brut=non · ACTIF=non
/journal  apostrophe nue       HTTP 200 · 55 492 o · VIEW='overview' · brut=non · ACTIF=non
            (8 cas, tous sur des pages complètes de 55-70 Ko)
```

**Verdict d'ensemble : aucune faille exploitable. Rien touché.**

## Gardien

`tests/test_contexte_js_lot373.py` (27 tests) :

- **anti-vide** : le détecteur doit trouver ≥ 5 substitutions en contexte JS ;
- **anti-angle-mort** : le balayage doit inclure `vertex/ui/shell/__init__.py` —
  la faute exacte de ma première passe, verrouillée ;
- toute interpolation en contexte JS est un littéral, un `json_for_script`, ou
  figure dans une liste d'exceptions **justifiées** ; un test réclame le retrait
  des exceptions **périmées**, pour que la liste ne se périme pas en silence ;
- `vocab_js()` sans `<`, `>` ni `&`, JSON valide et non dégénéré ; bloc
  `vx-vocab` **unique et clos** sur chacune des 8 pages ;
- 4 charges × 2 routes sur les `const VIEW='…'`, avec exigence d'un rendu
  supérieur à 20 Ko — sinon la sonde ne prouverait rien ;
- **pas trop strict** : une vue légitime (`sectors`, `overview`) doit traverser.

### Preuve ROUGE

```text
ROUGE OK  étiquette de vocabulaire contenant `<`      | restauration identique
          9 failed, 18 passed
ROUGE OK  liste blanche des vues retirée              | restauration identique
          4 failed, 23 passed
ROUGE OK  json_for_script remplacé par json.dumps nu  | restauration identique
          1 failed, 26 passed
après restauration : 27 passed
VERDICT : gardien mordant sur les 3 cas
```

Note : le premier cas a d'abord été **sauté** (mon motif de transplantation ne
correspondait à aucune ligne réelle) — un `SKIP` que le script signale au lieu de
le passer sous silence. Corrigé sur la vraie table `HELD`, il mord.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 372, e3074e8) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2645 → 2672 passed / 2 skipped** — verte (+27).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Le balayage couvre `terminal.py`, `vertex/ui/**` et `vertex/app/**`. Il détecte
les gabarits `%%…%%`, les f-strings et le `%`-format **dans des chaînes littérales
contenant `<script`**. Il ne verrait pas un bloc `<script>` assemblé par
concaténation à travers plusieurs constantes, ni du JS injecté depuis une route
hors de ces arbres. Le contenu de `vocab_js` est vérifié tel qu'il est produit,
pas prouvé constant par analyse statique.

## Suite

LOT 374 : veille active. Pistes ouvertes — (b) promesses de docstrings en un seul
mot majuscule et docstrings de **fonctions** ; (c) blocs `<script>` assemblés par
concaténation, angle mort déclaré ci-dessus. Prochaine échéance périodique :
**~lot 380**.
