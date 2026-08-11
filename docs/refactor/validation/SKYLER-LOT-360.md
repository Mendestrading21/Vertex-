# SKYLER LOT 360 — Checkpoint de la tranche 350-359 : 8/8 MD5 identiques, et ce que le smoke mesure vraiment

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-360` (base : lot 359 fusionné,
f8c9e8d)

## 1. Mesure — serveur DEMO, 8 pages

Serveur `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1`, `/scan` sert **20 lignes**
(vertex_ready atteint).

| page | HTTP | MD5 (12) | réf MD5 | verdict |
|---|---|---|---|---|
| `/` | 200 | `fc15688d1af6` | `fc15688d1af6` | ✅ |
| `/markets` | 200 | `c0bb91c6971a` | `c0bb91c6971a` | ✅ |
| `/opportunities` | 200 | `6a22a6abbd03` | `6a22a6abbd03` | ✅ |
| `/analysis` | 200 | `113827718e99` | `113827718e99` | ✅ |
| `/portfolio` | 200 | `f1b41b665d4a` | `f1b41b665d4a` | ✅ |
| `/options` | 200 | `6387210de785` | `6387210de785` | ✅ |
| `/journal` | 200 | `243699ace2d5` | `243699ace2d5` | ✅ |
| `/system` | 200 | `73e917c0f2d0` | `73e917c0f2d0` | ✅ |

**8/8 identiques.** Aucun octet servi n'a bougé depuis le lot 350 — cohérent
avec les 10 lots de la tranche, tous docs/tests uniquement.

Navigateur réel (Chromium 1194, 1440×900, après hydratation) sur les 8 pages :
**0 erreur console, 0 `pageerror`**.

## 2. Le smoke ne mesure pas ce que les références supposent

Toutes les tailles smoke sauf une s'écartent des références. Avant de conclure
quoi que ce soit, deux vérifications.

**a) La mesure hors navigateur n'est pas comparable.** Extraction du texte
depuis le HTML brut (curl) : `/` 510, `/journal` 1259 — très loin des
références. Normal : les pages s'hydratent côté client, le HTML serveur ne
contient presque aucun texte. Les références ont été établies **après
hydratation**. Toute mesure de ce lot est donc faite en navigateur.

**b) À MD5 identique, le smoke bouge.** Deux passes espacées de 90 s, même
serveur, même code :

```text
page               passe1   passe2   delta   md5 passe1     md5 passe2
/                    3367     3385     +18   fc15688d1af6   fc15688d1af6   MD5 STABLE
/markets             2814     2814      +0   c0bb91c6971a   c0bb91c6971a   MD5 STABLE
/opportunities       4586     4586      +0   6a22a6abbd03   6a22a6abbd03   MD5 STABLE
/portfolio           1612     1612      +0   f1b41b665d4a   f1b41b665d4a   MD5 STABLE
/options             2958     2958      +0   6387210de785   6387210de785   MD5 STABLE
/system              4127     4127      +0   73e917c0f2d0   73e917c0f2d0   MD5 STABLE
```

`/` gagne **+18 caractères en 90 secondes à octets servis identiques** : les
libellés de fraîcheur (« il y a 2 min » → « il y a 4 min ») changent de
longueur. Le smoke n'est donc **pas** un invariant d'octets.

**Conclusion d'instrument** : le MD5 est la seule preuve stricte
inter-sessions ; le smoke mesure le **contenu hydraté** et dépend (i) de
l'horloge, (ii) du jeu de données DEMO régénéré à chaque session, (iii) du
`desk_data.json` local. Les tailles restent **stables à l'intérieur d'une
session** (delta 0 sur 5 pages/6) mais dérivent d'une session à l'autre.

### Chaque écart, expliqué

| page | mesuré | réf | écart | cause |
|---|---|---|---|---|
| `/analysis` | 923 | 923 | 0 | page peu dépendante du scan |
| `/` | 3367→3385 | 3371 | ±18 | libellés de fraîcheur (prouvé ci-dessus) |
| `/portfolio` | 1607→1612 | 1609 | ±5 | idem |
| `/options` | 2958 | 2960 | −2 | idem |
| `/system` | 4126→4127 | 4122-4124 | +2/+3 | la page imprime de nombreux âges ; la plage figée au lot 340 est structurellement trop étroite |
| `/markets` | 2814 | 2794 | +20 | jeu DEMO de cette session (stable en session, delta 0) |
| `/opportunities` | 4586 | 4679 | −93 | idem — nombre de lignes/listes du scan DEMO |
| `/journal` | 3686 | 2676 (desk vide) | +1010 | `desk_data.json` local porte les sondes du lot 305 — écart documenté depuis le lot 330 |

**Aucun de ces écarts n'est une régression** : les 8 MD5 sont identiques aux
références, donc le HTML servi est le même octet pour octet.

### Références smoke — requalifiées en indicatives

Le smoke reste utile comme détecteur de gros décrochage (page vide, hydratation
cassée), pas comme égalité exacte. Plage indicative de cette session, à ne
jamais opposer au MD5 :

```text
/ 3360-3390 · /markets ~2814 · /opportunities ~4586 · /analysis 923
/portfolio 1605-1615 · /options ~2958 · /journal ~3686 (desk local ; 2676 desk vide)
/system 4120-4130
```

## 3. Bilan de la tranche 350-359

| Lot | Verdict |
|---|---|
| 350 | Checkpoint complet (mesure de référence de la tranche) |
| 351-357 | **Veille active** — 7 lots, état identique, rien touché, suite 2501/2 |
| 358 | **Trouvé** : la règle n°5 décrivait UNE famille de sorties de news, il y en a **deux**. `/api/ai/enrichment` sert le titre non neutralisé, sûr par `esc()` au rendu mais **gardé par rien**. Gardien neuf (5 tests, preuve ROUGE ×3) + règle corrigée |
| 359 | **Trouvé** : `/analysis` (index) était la **seule** page HTML servie absente des gardiens JS 182/186. Ajoutée. Preuve ROUGE en rejouant le bug historique d'apostrophe française |

- Suite : **2501 → 2506 passed / 2 skipped** (+5 gardiens au lot 358).
- Service worker : **`td-shell-v187`** inchangé sur toute la tranche (dernier
  bump : lot 328) — cohérent, aucun octet servi modifié.
- 10 PR fusionnées (#382 → #391), toutes en squash sur
  `integration/vertex-skyler-v2`. `main` jamais touchée.
- Deux lots sur dix ont trouvé quelque chose ; huit ont conclu « sain ». Les
  deux trouvailles viennent de la **même question** : « la règle écrite
  décrit-elle vraiment ce que fait le code servi ? » — c'est la piste la plus
  productive de la tranche, à continuer.

## 4. Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 359, f8c9e8d) ; arbre propre
  avant et après le serveur DEMO (aucun fichier runtime touché).
- Suite complète : **2506 passed / 2 skipped** — verte.

## 5. Décision SW

**Pas de bump** (`td-shell-v187`) : les 8 MD5 le prouvent, aucun octet servi n'a
changé. Le lot ne touche que `docs/`.

## 6. Reste en attente de décision humaine

Purge É2 (25 défs / 1 866 l.) · purge É3 (dépendances croisées, dont le rendu
brut de `/news-feed` dans les constantes `PAGE_*`) · les 24 fonctions top-level
du lot 326 (façades IBKR = chemin de lecture du compte réel) · les 5 modules
`vertex/ui/` reliques du lot 327. Pistes ouvertes du lot 359 : variantes
`?view=…` non balayées séparément ; `/memory/<id>` et `/memory/cell/<g>/<k>`
(HTML, exigent un identifiant réel) non couvertes.

## 7. Suite

LOT 361 : veille active. Prochaine échéance périodique : ~lot 370.
