# SKYLER LOT 328 — Honnêteté d'affichage : la page Système citait un symbole disparu

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-328` (base : lot 327 fusionné,
4e1c43a)

## Le défaut

Page Système → réglages, carte du desk :

> Clés synchronisées — 17 (contrat **`__DESK_KEYS`** — aucune clé renommée)

`__DESK_KEYS` a disparu avec la purge É1 (lot 323) : c'était le nom de la liste
qui vivait dans le JS des pages mortes. Le contrat de clés, lui, existe
toujours — il s'appelle **`DESK_KEYS`** et vit dans `vertex/ui/vx_kit.py` et
`vertex/static/vertex/js/vx-entities.js`.

L'affirmation n'était pas fausse sur le fond (le contrat est bien tenu, aucune
clé n'est renommée), mais elle **nommait à l'utilisateur un symbole qui n'existe
nulle part** dans le code. Un trader qui irait vérifier ne trouverait rien.
C'est exactement le genre d'écart que l'invariant n°4 (« données réelles
uniquement, jamais d'affirmation invérifiable ») interdit.

Repéré au lot 327, mis en réserve parce qu'il change un octet servi ; traité ici
avec le protocole complet.

## Le correctif

`vertex/ui/pages/system_page.py` — une chaîne :

```diff
-  kv('Clés synchronisées', keys.length + ' (contrat __DESK_KEYS — aucune clé renommée)')
+  kv('Clés synchronisées', keys.length + ' (contrat DESK_KEYS — aucune clé renommée)')
```

## Preuves

- **Un seul octet servi change, et c'est le bon.** MD5 des 8 pages, serveur
  DEMO, scan terminé :

  | page | MD5 | vs lots 323-327 |
  |---|---|---|
  | `/` | fc15688d1af6 | identique |
  | `/markets` | c0bb91c6971a | identique |
  | `/opportunities` | 6a22a6abbd03 | identique |
  | `/analysis` | 113827718e99 | identique |
  | `/portfolio` | f1b41b665d4a | identique |
  | `/options` | 6387210de785 | identique |
  | `/journal` | 243699ace2d5 | identique |
  | **`/system`** | **73e917c0f2d0** | **changé** (était 85d1cb065d2e) |

  Nouvelle référence `/system` : **73e917c0f2d0**.
- Vérification directe du HTML servi : `contrat DESK_KEYS` présent,
  **0 occurrence de `__DESK_KEYS`**.
- Navigateur (`tools/probe_smoke.py`) : 8 × HTTP 200, **0 erreur
  console/pageerror**, `client-log count: 0`.
- Suite : **2501 passed / 2 skipped**.

## Service worker

Un octet servi change → **bump `td-shell-v186` → `td-shell-v187`**
(`vertex/app/routes/system.py`), avec l'entrée d'historique correspondante, et
les **5 gardiens SW** mis à jour : `test_production_guards_canonical`,
`test_reconstruction_today`, `test_redesign_ui`, `test_ui_v3`,
`test_design_system_page_lot187`. `/sw.js` sert bien `td-shell-v187`.

## Invariants

READONLY intact, moteurs intacts, aucune donnée ni logique touchée (une chaîne
d'affichage), `main` non touchée, aucun fichier runtime commité.

## Suite

LOT 329 : veille active. Quatre dossiers restent en attente de décision
humaine — purge É2, purge É3, les 24 fonctions du lot 326, les 5 modules
`vertex/ui/` reliques du lot 327. Prochaine échéance périodique : ~lot 330
(⚠️ nouvelle référence MD5 `/system` = 73e917c0f2d0).
