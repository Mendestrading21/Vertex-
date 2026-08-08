# SKYLER LOT 361 — Règle n°3 : le bump SW ne couvre pas ce que le cache contient

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-361` (base : lot 360 fusionné,
7fb9469)

## Piste calibrée

Même question que celle qui a donné les lots 358 et 359 — « la règle écrite
décrit-elle vraiment le code servi ? » — appliquée cette fois à la **règle
n°3** : « tout changement de **shell visible utilisateur** → bump
`td-shell-vN` ».

## Ce que le service worker fait réellement

Lecture de `vertex/app/routes/system.py` (`_SW_JS`) :

```js
const cacheable = (req.mode==='navigate'
                || url.pathname.startsWith('/static')
                || url.pathname==='/manifest.webmanifest');
```

- Le cache couvre les **navigations**, **tout `/static`** (54 fichiers servis :
  34 JS, 17 CSS, 2 polices, 1 md) et le manifeste — pas seulement « le shell ».
- La lecture est **network-first** : `Promise.race([fetch, timeout 4500 ms])`,
  le cache ne sert qu'en **repli** (hors-ligne ou réseau lent).
- `activate` supprime **tous** les caches dont la clé diffère de `CACHE`.

Deux conséquences que la règle écrite ne disait pas :

1. **Le périmètre est plus large que « le shell »** — un changement de
   `neon-glass.css` ou d'un builder `js/charts/*.js` est un octet servi mis en
   cache, au même titre qu'une page.
2. **Le bump ne sert pas à « faire voir » la nouvelle interface** — le
   network-first s'en charge en ligne. Le bump est ce qui **purge la copie de
   repli hors-ligne**.

Fenêtre d'exposition réelle, sans bump : visiteur déjà venu, **hors-ligne ou
réseau > 4,5 s**, servi depuis un cache assemblé au fil de visites différentes —
le HTML peut dater d'un passage et le CSS d'un autre.

## Mesure sur l'historique

Chaque commit touchant `vertex/static` (hors fusions), comparé à la version du
shell de son parent :

```text
commits touchant vertex/static (hors fusions) : 144
SANS BUMP alors qu'un asset statique change : 27 / 144
```

Exemples : `98c983f4` (v53, `neon-glass.css`), `100305cd` (v38, 4 CSS),
`79cfb2d9` (v20, `tokens.css` + 3 CSS), `3da17d1f` (v42, `chart-core.js` +
thème). Ces commits sont **conformes à la règle écrite** — ils ne touchaient pas
« le shell ». Ils sont simplement hors du périmètre réel du cache. Le défaut est
dans la règle, pas dans la discipline de ceux qui l'ont suivie.

## Ce que le lot livre

1. **Gardien neuf** `tests/test_sw_cache_scope_lot361.py` (5 tests) :
   - la **sémantique** du SW est figée (périmètre du cache, network-first,
     purge à l'activation) — un changement de politique devient délibéré ;
   - le **contrat** : empreinte SHA-256 agrégée des 54 fichiers servis sous
     `/static`, enregistrée avec la version de shell. Un asset change →
     échec, avec le message qui donne la marche à suivre (bumper, puis
     rafraîchir les deux constantes dans le même commit).
   - Le contrat est **daté d'aujourd'hui**, il ne juge pas l'historique ; un
     bump sans changement d'asset reste légitime (`_SW_VERSION <= version`).
2. **Règle n°3 de `CLAUDE.md` corrigée** : périmètre réel (`/static` inclus),
   effet réel (purge du repli hors-ligne, pas « faire voir »), fenêtre
   d'exposition, et le gardien qui l'applique.

### Preuve ROUGE

Chaque propriété retirée une par une, fichiers restaurés MD5 identique :

```text
ROUGE OK     un octet servi sous /static change sans bump   | restauration identique
ROUGE OK     le périmètre du cache change                   | restauration identique
ROUGE OK     la politique network-first change              | restauration identique
ROUGE OK     la purge à l'activation disparaît              | restauration identique
VERDICT : gardien mordant sur les 4 propriétés
```

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 360, 7fb9469) ; arbre propre.
- Suite complète : **2506 → 2511 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : le lot ne touche que `tests/`, `CLAUDE.md`
et `docs/` — aucun octet servi, `/static` inchangé (c'est d'ailleurs ce que le
nouveau gardien vérifie).

## Portée — ce que ce lot ne prétend pas

Aucun bug utilisateur n'a été observé : en ligne, le network-first sert toujours
le frais. Le lot rend la règle **exacte et applicable**, il ne répare pas un
incident. Il introduit en revanche une **friction assumée** : tout changement
d'asset servi exigera désormais un bump + la mise à jour de deux constantes.
C'est le prix de la correction hors-ligne — si cette contrainte n'est pas
souhaitée, le gardien du contrat (`test_les_assets_servis_correspondent_a_la_version_enregistree`)
est le seul à retirer ; les quatre autres tests restent utiles.

**Solution de fond non engagée** (demande un GO humain) : donner une empreinte
aux URL d'assets (`/static/…?v=187`) rendrait le problème structurellement
impossible, mais touche toutes les pages servies.

## Suite

LOT 362 : veille active. Règles n°1 (clés desk), n°4 (données réelles) et n°6
(`desk_data.json`) n'ont pas encore été passées à la question. Prochaine
échéance périodique : ~lot 370.
