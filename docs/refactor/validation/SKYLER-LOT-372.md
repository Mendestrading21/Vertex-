# SKYLER LOT 372 — `json.dumps` nu dans un `<script>` : une XSS déclenchable par un simple lien

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-372` (base : lot 371 fusionné,
1f40933)

## Piste calibrée

Dernière grande surface non auditée de la veine sécurité : les **interpolations
serveur** dans le `page_js` des pages. Les lots 367-371 avaient couvert `?view=`,
les segments de chemin, les 4 étiquettes de `render_shell` et les deux routes
`/memory/`.

## Mesure — 35 interpolations, une seule non filtrée

Passe AST sur les fonctions `render*` de `vertex/ui/pages/` : **35**
interpolations non littérales. La très grande majorité reçoit `view` (liste
blanche, couverte au lot 367) ou `_tabs(view)`. Quatre sites envoient du JSON
dans un bloc `<script>` :

```text
analysis_page.py:963    %%SYM_JSON%% ← json.dumps(safe)    safe = filtre alnum + « .- »
opportunities_page.py   %%VIEW%%     ← json.dumps(view)    liste blanche
opportunities_page.py   %%PARAMS%%   ← json.dumps(p)       ⚠ VALEURS NON FILTRÉES
portfolio_page.py:1006  %%VIEW%%     ← json.dumps(view)    liste blanche
```

La route sert `params=request.args` — brut — et `p` n'en retient que les
**CLÉS** :

```python
p = {k: v for k, v in (params or {}).items() if k in ('sym','sector','setup','decision')}
```

Les **valeurs** ne sont jamais filtrées. Or `json.dumps` échappe `"` et `\` mais
**ni `<` ni `/`** : l'analyseur HTML voit la balise fermante et termine le script.

## La faille, sondée sur un rendu réel

```text
=== /opportunities — charge dans le HTML ACTIF (hors <script>) ===
sym       sortie de balise   HTTP 200 · brut=OUI · HTML ACTIF pollué=OUI ⚠
sym       sortie casse       HTTP 200 · brut=OUI · HTML ACTIF pollué=OUI ⚠
sector    sortie de balise   HTTP 200 · brut=OUI · HTML ACTIF pollué=OUI ⚠
setup     sortie de balise   HTTP 200 · brut=OUI · HTML ACTIF pollué=OUI ⚠
decision  sortie de balise   HTTP 200 · brut=OUI · HTML ACTIF pollué=OUI ⚠
            (4 clés × 2 charges = 8 injections confirmées, pages de 66 Ko)

const PARAMS={"sym": "</script><img src=x onerror=alert(1)>"};
```

Les six autres pages recevant des paramètres d'URL (`/markets`, `/portfolio`,
`/journal`, `/options`, `/system`, `/analysis`) : **aucune fuite**.

**Cette faille est plus grave que celle du lot 368.** Celle-là exigeait que le
moteur de décision produise lui-même un symbole hostile ; celle-ci se déclenche
**à distance, par un simple lien** — et le JS injecté s'exécute dans une session
qui a accès au desk local (`myTrades`, `myRecos`, `vxJournal`…).

## Correction de méthode, avant le verdict

Le premier détecteur cherchait `<img …>` dans **toute** la page et répondait
« actif » même quand la balise restait **à l'intérieur** d'un bloc `<script>` non
refermé — où elle est **inerte**. Il gonflait le résultat (4 charges sur 4 au
lieu de 2). Le détecteur corrigé retire d'abord les blocs `<script>…</script>`,
comme le fait l'analyseur, puis cherche dans ce qui reste. **Sixième fois** de la
boucle qu'un doute sur l'outil change le résultat.

## Correctif

`vertex.ui.shell.json_for_script` neutralise `<`, `>` et `&` en échappements
`\uXXXX`. Un moteur JS les relit à l'identique dans un littéral de chaîne : le
**comportement client est inchangé** (vérifié par aller-retour `json.loads` sur
10 valeurs, dont un dict et des charges hostiles), mais l'analyseur HTML ne peut
plus voir de balise fermante. Appliqué aux **4** sites — les trois déjà filtrés
inclus, pour que le contrat soit vérifiable statiquement plutôt que déduit du
filtrage amont. `import json` devenu mort, retiré des trois pages.

Sonde rejouée après correctif : **16 cas sur 16 → `brut=non`, `ACTIF pollué=non`**.

## Gardien

`tests/test_json_script_lot372.py` (35 tests) :

- **anti-vide** : la sonde doit atteindre une page de plus de 20 Ko contenant
  `const PARAMS=` et la valeur légitime — sinon les « non » ne prouveraient rien
  (piège des lots 368 et 371) ;
- 3 charges de sortie de balise × 4 clés, sur les octets servis **et** sur le
  HTML actif ; le littéral `PARAMS` ne doit contenir aucun `</` ;
- **préservation du comportement** : `json.loads(json_for_script(v)) == v` ;
- **pas trop strict** : une valeur normale reste lisible telle quelle
  (`{"sym": "AAPL"}`) — sinon le débogage deviendrait impossible ;
- **contrat statique** : aucune page n'injecte un `json.dumps` nu dans un
  gabarit `%%…%%`, avec un test qui vérifie que ce détecteur mord vraiment.

### Preuve ROUGE

```text
ROUGE OK  faute historique rejouée : json.dumps nu pour PARAMS | restauration identique
          17 failed, 18 passed
ROUGE OK  correctif affaibli : `<` n'est plus neutralisé       | restauration identique
          5 failed, 30 passed
après restauration : 35 passed
VERDICT : gardien mordant sur les 2 cas
```

## Preuve MD5 — trois fichiers de production touchés

```text
/                fc15688d1af6 = réf      /portfolio   f1b41b665d4a = réf
/markets         c0bb91c6971a = réf      /options     6387210de785 = réf
/opportunities   6a22a6abbd03 = réf      /journal     243699ace2d5 = réf
/analysis        113827718e99 = réf      /system      73e917c0f2d0 = réf

DIVERGENCES MD5 : 0 / 8
```

Attendu et vérifié : une valeur légitime ne contient ni `<`, ni `>`, ni `&`, donc
`json_for_script` rend exactement ce que rendait `json.dumps`. Le trafic normal
est **octet pour octet identique**.

Navigateur réel (1440×900, Chromium) sur filtre légitime, filtre secteur et
charge hostile : **0 erreur console**, `img[onerror]` = 0, `window.__PWN` jamais
défini, page rendue normalement dans les trois cas.

## Une question de méthode enfin tranchée : le « smoke »

Les 8 pages sortaient **toutes** « hors plage » au smoke (`/` à 510 pour une
plage 3360-3390) alors que les MD5 étaient identiques aux références. Or MD5
identique ⟹ octets identiques ⟹ texte visible identique : les deux chiffres ne
pouvaient pas décrire la même mesure. Le script du lot 360 **non modifié** donne
les mêmes valeurs basses — ce n'est donc pas mon correctif.

Explication, confirmée par le navigateur : le texte visible du DOM **hydraté**
de `/opportunities` mesure **4662**, très près de la référence 4679 ; le HTML
**brut** en mesure 410. Les constantes `SMOKE_REF` sont des mesures du **DOM
hydraté**, alors que le script mesure le **HTML brut** — deux grandeurs sans
rapport. Cela explique aussi la « dérive de +18 caractères à MD5 constant »
notée au lot 360, impossible sur du HTML brut.

Conséquence : **le smoke de ce script n'a jamais rien prouvé** ; seul le MD5
porte la preuve. Le lot 370 a élargi une plage (`/markets` 2795→2790) pour
accommoder un chiffre issu de l'autre grandeur — correction inutile, sans
dommage. Je n'ajuste plus ces plages : elles sont retirées du raisonnement.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 371, 1f40933) ; arbre propre.
- 3 fichiers de production touchés → **preuve MD5 fournie, 0/8**.
- Suite complète : **2610 → 2645 passed / 2 skipped** — verte (+35).
- Aucun fichier runtime commité.

## Décision SW

**Pas de bump** (`td-shell-v187`) : aucun octet servi ne change (0/8). Aucun
fichier `vertex/static` touché — `_EMPREINTE` et `_SW_VERSION` de
`tests/test_sw_cache_scope_lot361.py` restent valides.

## Portée — ce que ce lot ne prétend pas

Le contrat statique couvre la forme exacte de la faute (`json.dumps` nu vers un
gabarit `%%…%%`) dans les trois pages concernées. Il ne couvre pas les f-strings
injectant du JSON, ni les pages hors `vertex/ui/pages/`. Les 31 autres
interpolations recensées reçoivent `view` ou `_tabs(view)` — déjà sous gardien
depuis le lot 367 — mais je ne les ai pas re-sondées une par une.

## Suite

LOT 373 : veille active. Pistes ouvertes — (b) promesses de docstrings en un seul
mot majuscule et docstrings de **fonctions** ; (c) interpolations JSON par
f-string hors `vertex/ui/pages/`. Prochaine échéance périodique : **~lot 380**.
