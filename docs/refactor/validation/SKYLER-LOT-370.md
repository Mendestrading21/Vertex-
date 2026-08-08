# SKYLER LOT 370 — Checkpoint de la tranche 360-369 : 8/8 MD5, 0 erreur console, une faille réelle corrigée

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-370` (base : lot 369 fusionné,
d545573)

## 1. Mesure — serveur DEMO + navigateur réel

Serveur `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1`, `/scan` sert **20 lignes**
(`source=demo`).

### MD5 des 8 pages — la preuve stricte

| page | MD5 (12) | réf | verdict |
|---|---|---|---|
| `/` | `fc15688d1af6` | `fc15688d1af6` | ✅ |
| `/markets` | `c0bb91c6971a` | `c0bb91c6971a` | ✅ |
| `/opportunities` | `6a22a6abbd03` | `6a22a6abbd03` | ✅ |
| `/analysis` | `113827718e99` | `113827718e99` | ✅ |
| `/portfolio` | `f1b41b665d4a` | `f1b41b665d4a` | ✅ |
| `/options` | `6387210de785` | `6387210de785` | ✅ |
| `/journal` | `243699ace2d5` | `243699ace2d5` | ✅ |
| `/system` | `73e917c0f2d0` | `73e917c0f2d0` | ✅ |

**8/8 identiques.** Aucun octet servi n'a bougé de toute la tranche — cohérent
avec dix lots dont **un seul** a touché un fichier de production (lot 368, une
ligne d'échappement dans une route non servie parmi les 8).

### Navigateur (Chromium 1194, 1440×900, après hydratation)

```text
page                smoke          plage verdict
/                    3367      3360-3390 OK
/markets             2794      2795-2835 hors plage
/opportunities       4582      4560-4610 OK
/analysis             923        923-923 OK
/portfolio           1607      1605-1615 OK
/options             2958      2940-2975 OK
/journal             3686      3660-3710 OK
/system              4122      4120-4130 OK

ERREURS CONSOLE : 0
```

**0 erreur console, 0 `pageerror`** sur les 8 pages.

### L'unique écart, expliqué — et c'est ma plage qui était fausse

`/markets` mesure **2794**, soit exactement la **référence historique**
d'origine. Ma plage `2795-2835` avait été construite autour des **2814**
mesurés au lot 360… en excluant la référence elle-même. **Erreur de
construction de plage, pas une régression de la page** — le MD5 identique le
prouve.

Cet écart illustre au passage la conclusion du lot 360 : le smoke dépend du jeu
DEMO régénéré à chaque session. Deux sessions donnent 2814 et 2794 pour des
octets servis identiques.

**Plage `/markets` corrigée : 2790-2835** (couvre les deux valeurs observées).

## 2. Bilan de la tranche 360-369

| Lot | Verdict |
|---|---|
| 360 | Checkpoint : 8/8 MD5 ; **smoke requalifié en plage indicative** (à MD5 identique, `/` gagne +18 car. en 90 s) |
| 361 | **Trou** — règle n°3 : le SW met en cache **tout `/static`**, pas « le shell » ; 27 commits/144 sans bump, **conformes à la règle écrite** |
| 362 | **Promesse plus étroite** — règle n°6 : le filet rend l'état d'**avant la 1ʳᵉ sync du jour** ; push `data: {}` accepté |
| 363 | **Saine** — règle n°4 prouvée en navigateur, et gardée contre sa **3ᵉ** rechute (lots 296/297 rejoués) |
| 364 | **Trou** — la purge É1 avait emporté **ses propres gardiens** sans l'écrire |
| 365 | **Trouvaille** — `thesis_health` annonçait **PORTFOLIO_FIT** sans le calculer |
| 366 | **Isolée** — 110 moteurs passés à la même question, rien d'autre |
| 367 | **Trou inexistant** — le diff a montré 2 lignes d'écart ; mais la liste blanche `?view=` n'était gardée par rien |
| 368 | **VRAIE FAILLE XSS** — titre du post-mortem non échappé (`</title><script>` sortait de la balise) → **corrigée** |
| 369 | **18/18 étiquettes sûres** ; coût du durcissement **chiffré à 1 page sur 8** |

**Comptes de la tranche :**

- **9 gardiens neufs** (`test_sw_cache_scope_lot361` → `test_etiquettes_shell_lot369`) ;
- suite **2530 → 2605 passed / 2 skipped** (**+75 tests**) ;
- **10 PR fusionnées** (#392 → #401), toutes en squash sur
  `integration/vertex-skyler-v2` ; `main` jamais touchée ;
- service worker **`td-shell-v187` inchangé** sur toute la tranche — cohérent
  avec les 8 MD5 ;
- **1 fichier de production modifié** en dix lots (lot 368, une ligne).

### Ce que la tranche a appris sur la méthode

**Trois fois**, vérifier l'outil avant de conclure a changé le résultat :

- **lot 367** — « 16 blocs JS jamais parsés » : le diff a révélé **2 lignes**
  d'écart (`const VIEW=…`). Sans lui, un gardien inutile et une faille
  imaginaire annoncée ;
- **lot 368** — 28 « non » rassurants et **vides** : les charges contenant `/`
  finissaient en 404 Werkzeug **avant tout rendu** ;
- **lot 369** — « 8/8 pages changeraient » avec le **même MD5 partout** :
  c'était une page d'erreur (`NameError`). Un chiffre faux aurait pu faire
  renoncer à un durcissement quasi gratuit.

Et ce lot-ci ajoute la quatrième : le seul « hors plage » du checkpoint venait
d'une plage que j'avais mal construite.

## 3. Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 369, d545573) ; arbre propre
  avant et après le serveur DEMO (aucun fichier runtime touché).
- Suite complète : **2605 passed / 2 skipped** — verte.

## 4. Décision SW

**Pas de bump** (`td-shell-v187`) : les 8 MD5 le prouvent. Le lot ne touche que
`docs/`.

## 5. En attente de votre décision

Purge É2 (25 défs / 1 866 l.) · purge É3 · les 24 fonctions top-level du
lot 326 (façades IBKR) · les 5 modules `vertex/ui/` reliques du lot 327 ·
empreinte dans les URL d'assets (lot 361) · filet desk du lot 362 —
**option A (snapshot avant perte) recommandée**, B (refus 409), C (fusion par
clé) · reformulation « points réels du scan » sur `/markets` (lot 363) ·
implémentation de PORTFOLIO_FIT dans `thesis_health` (lot 365) ·
**échappement centralisé des étiquettes dans `render_shell`** (lots 368-369) —
**coût mesuré : 1 page sur 8**, `/` seulement, apostrophe de « Aujourd'hui » →
`&#x27;`, visuellement identique, + bump SW + nouvelle référence MD5.

## 6. Suite

LOT 371 : veille active. Prochaine échéance périodique : **~lot 380**.
