# SKYLER LOT 369 — Les 62 étiquettes du shell auditées : 18/18 sûres, et le coût du durcissement mesuré

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-369` (base : lot 368 fusionné,
96ba72b)

## Piste calibrée

Suite directe de la faille du lot 368 : `render_shell(title=…)` interpole sans
échapper. **Un seul site était fautif — les autres n'avaient jamais été
audités.** Ce lot les passe tous.

## Ce que le shell fait vraiment — l'asymétrie

`vertex/ui/shell/__init__.py` a **deux chemins de rendu** :

| chemin | `title` | `space_label` | `sub_label` | `page_label` |
|---|---|---|---|---|
| **fragment** (l. 188-192) | `escape(…, quote=True)` | ✅ | ✅ | ✅ |
| **page complète** | `<title>{title}` **brut** | `<b>{space_label}</b>` brut | `<span>{sub_label}</span>` brut | `data-page-label="{…}"` **brut, dans un attribut** |

Le dernier est le plus dangereux : **un simple guillemet suffirait à sortir de
l'attribut** — pire qu'un `</title>`.

**La cause est identifiée** : `from html import escape` est un import **local à
`_render_fragment`** (ligne 187). L'échappement n'existe que là où l'import
existe.

## Audit des sites d'appel — 18/18 sûres

```text
appels render_shell — étiquettes CONSTANTES : 44 · INTERPOLÉES : 18
```

Les 18 interpolées, tracées **une par une** jusqu'à leur source :

| Origine | Protection |
|---|---|
| `analysis_page` (`title`, `sub_label`, `page_label`) | `safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')` — **filtre de caractères explicite** |
| `markets`, `opportunities`, `portfolio`, `performance`, `system`, `intelligence` | `label`/`sub` lus dans un **dict de vues** après normalisation (`if view not in dict(_VIEWS): view = '…'`) |
| `options_intel` (`page_label='options:%s' % view`) | `view` **normalisé à la première ligne** de `render()` |
| `analysis_api` (post-mortem) | échappée depuis le lot 368 |

**Aucun autre site fautif.** La faille du lot 368 était isolée.

## Le dossier en attente de GO, désormais chiffré

« Échapper les étiquettes directement dans `render_shell` » attendait votre
décision sans qu'on sache ce qu'il coûterait. **Mesuré** — durcissement appliqué
temporairement, MD5 des 8 pages comparés, shell restauré (MD5 du fichier
vérifié identique) :

```text
page             avant          après
/                fc15688d1af6   9dfde1030043   ≠
/markets         c0bb91c6971a   c0bb91c6971a   identique
/opportunities   6a22a6abbd03   6a22a6abbd03   identique
/analysis        113827718e99   113827718e99   identique
/portfolio       f1b41b665d4a   f1b41b665d4a   identique
/options         6387210de785   6387210de785   identique
/journal         243699ace2d5   243699ace2d5   identique
/system          73e917c0f2d0   73e917c0f2d0   identique

PAGES DONT LES OCTETS CHANGERAIENT : 1 / 8
```

**7 pages sur 8 seraient inchangées à l'octet près.** Seule `/` bouge, et la
cause est connue : son titre est `"Aujourd'hui"` — l'apostrophe devient
`&#x27;`. **Visuellement identique** (le navigateur décode l'entité) ; le coût
réel est donc : un bump SW + une nouvelle référence MD5 pour `/`.

**Rien n'est engagé** : le dossier reste en attente de votre GO, mais vous
décidez maintenant avec le chiffre.

### Correction de méthode (encore une)

La **première** mesure annonçait « 8/8 pages changeraient » — avec le **même
MD5 sur les 8**, ce qui n'a aucun sens pour 8 pages différentes. C'était une
page d'erreur : ma mutation appelait `escape` hors de la portée de son import
local → `NameError`. Sans ce doute, j'aurais rapporté un chiffre faux et
peut-être fait renoncer à un durcissement quasi gratuit.

## Gardien

`tests/test_etiquettes_shell_lot369.py` (**27 tests**) : 3 charges hostiles ×
7 routes via `?view=`, puis via le segment `/analysis/<sym>` — la charge
n'atteint aucune étiquette, `<title>` reste une balise unique et close, et
aucun `data-page-label` ne contient `"` ou `<`. Plus deux tests de contrat : le
chemin fragment échappe bien les quatre étiquettes, et **le chemin page
complète reste le seul non échappé** — si le shell est durci un jour, ce test
réclame sa mise à jour.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 368, 96ba72b) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise pour le lot lui-même.
- Suite complète : **2578 → 2605 passed / 2 skipped** — verte (+27).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

L'audit couvre les 4 étiquettes de `render_shell`. Les autres interpolations
serveur (le `content=` de chaque page) ne sont pas dans son périmètre : elles
sont construites par les modules de page, avec leurs propres `esc()`.

## Suite

**LOT 370 — checkpoint périodique complet** : serveur DEMO + navigateur +
smoke + MD5 des 8 pages + **bilan de la tranche 360-369**.
