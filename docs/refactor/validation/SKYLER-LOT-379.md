# SKYLER LOT 379 — Les 46 `except: pass` jugés, une hypothèse réfutée, et une trouvaille à côté

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-379` (base : lot 378 fusionné,
a5f6465)

## Volet A — les 46 `except: pass`, cette fois JUGÉS

Le lot 378 les avait comptés **en déclarant ne pas les juger**. Ce qui décide,
c'est ce que le `try` **entoure** :

```text
nettoyage / fermeture      3   ← close, remove… : légitime par nature
journal / persistance      5   ← écrire un cache ne doit jamais casser l'appelant
autres                    38   ← lus un par un
```

Mon classificateur automatique laissait 38 cas sur 46 « à lire » : il n'a pas
fait le travail, et je le dis plutôt que de maquiller le résultat. Lus à la main,
ils se répartissent en **imports optionnels** (`ai/*`, Anthropic absent),
**lectures de configuration** (`config.py`, `.env`), **écritures de cache**
(`open` + `dump`), et **calculs métier** — la seule famille qui pouvait menacer
l'invariant n°4.

### Les calculs métier sont honnêtes par construction

Les cinq `try … except: pass` de `vertex/market/context.py` n'écrivent que dans
`out[...]` et des variables locales. Un échec produit une **absence**, jamais une
valeur périmée servie.

### `analysis.py:229` — hypothèse sérieuse, réfutée par la mesure

Ce cas méritait mieux qu'un coup d'œil :

```text
L204  score, grade, mom = sc['global'], sc['grade'], …     ← grade du score INITIAL
L228  score = int(max(0, min(100, base_score + struct_adj)))  ← score AJUSTÉ
L230  try: grade = config.grade(score)                        ← recalcul
      except Exception: pass
L303  'score': score, 'grade': grade                          ← les deux SERVIS
```

Si le recalcul échouait, un **grade calculé sur l'ancien score** serait servi à
côté du **nouveau score** : deux champs incohérents, sans rien pour le signaler.
C'est un défaut qu'aucun gardien existant n'attraperait.

Mesure : `config.grade` ne lève pour **aucun** nombre — testé sur 0, 1, 50, 99,
100, −5, 105, 50.5, NaN et l'infini, toujours une note — et la ligne 228 garantit
un `int`. **Le handler est inatteignable, l'incohérence ne peut pas se produire.**
Hypothèse précise, réfutée proprement ; le gardien verrouille les deux raisons.

## Ce que la sonde a trouvé à côté — et qui vaut plus que la piste

En vérifiant que `context()` dégrade bien par absence, j'ai mesuré son
comportement réel sur univers vide. Il est **mixte**, et ma lecture statique ne
l'aurait jamais montré :

```text
context(None, None, [], {}, [])
  vix, vix_band, vix_chg, spy_regime, spy_adx, spy_trend_txt  → None   ← honnête
  roro      → 'NEUTRE'
  roro_gap  → 0
  breadth   → {above50: 0, above200: 0, adv: 0, …}
  verdict   → 'MARCHÉ · NEUTRE · participation 0% au-dessus MM50'
```

Ce n'est **pas** un `except` qui avale : le bloc **réussit**, parce que ses
propres défauts (`ro = np.mean(…) if any(…) else 50`) le font aboutir sur zéro
donnée. Sur un univers vide, l'application **affirme** donc un régime « NEUTRE »
et une participation « 0 % » au lieu de dire qu'elle ne sait pas.

**Caractérisation, pas correction.** Toucher au moteur de contexte de marché sans
accord serait le changement gratuit que la boucle s'interdit — et la question est
jumelle du dossier ouvert depuis le lot 363. Le comportement est **gelé** par
test : s'il change un jour, ce sera délibérément.

**Verdict du lot : sain, rien touché.**

## Gardien

`tests/test_pass_et_contexte_lot379.py` (24 tests) : périmètre ; anti-vide et
**borne de dérive** des `except: pass` ; les handlers du contexte marché
n'écrivent que dans `out[...]` ; **`config.grade` total sur 10 valeurs
numériques** (la raison de l'inatteignabilité) ; **anti-dérive de la garantie
`int`** ; les 6 champs qui dégradent honnêtement en `None` ; les 4 champs
affirmatifs, **gelés** avec un message qui renvoie à ce rapport.

### Preuve ROUGE

```text
ROUGE OK  config.grade rendu faillible                         | restauration identique
          10 failed, 14 passed
ROUGE OK  garantie `int` retirée avant config.grade            | restauration identique
ROUGE OK  le contexte affirme une mesure au lieu de s'abstenir | restauration identique
ROUGE OK  population des `except: pass` au-delà de la borne    | restauration identique
après restauration : 24 passed
```

Le premier cas a d'abord répondu **NE MORD PAS** — mais c'était **ma mutation**
qui était inopérante (une définition insérée avant la vraie, donc écrasée), pas
le gardien. Corrigée en levant depuis le corps réel, elle fait tomber 10 tests.
La distinction compte : un cas qui ne mord pas accuse d'abord la preuve, pas
toujours le gardien.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 378, a5f6465) ; arbre propre.
- **Aucun fichier de production touché** — pas de preuve MD5 requise.
- Suite complète : **2730 → 2754 passed / 2 skipped** — verte (+24).
- SW inchangé : `td-shell-v187`.

---

# Volet B — MATÉRIAUX POUR LE BILAN DU LOT 380

## Les dix lots de la tranche

| Lot | Verdict en une ligne | Gardien (tests) | Production touchée |
|-----|----------------------|-----------------|--------------------|
| 370 | Checkpoint 360-369 : 8/8 MD5, 0 erreur console | — | non |
| 371 | Route sœur du 368 : **saine**, prouvée sur cellules réelles | `memoire_cellule` (5) | non |
| 372 | **XSS RÉELLE corrigée** : `json.dumps` nu dans un `<script>` | `json_script` (35) | **3 fichiers, MD5 0/8** |
| 373 | Faute du 372 sous d'autres habillages : **danger latent verrouillé** | `contexte_js` (27) | non |
| 374 | `<script>` concaténés : angle mort réel, **sans surface exploitable** | `script_concatene` (21) | non |
| 375 | Promesses de retour tenues ; promesses en un mot **non décidables** | `promesses_retour` (10) | non |
| 376 | Piste close par la mesure → **contrat de refus honnête** exhibé | `refus_honnete` (9) | non |
| 377 | **Le gardien du 376 n'en voyait qu'un tiers** (13/39) | `refus_api` (9) | non |
| 378 | Exceptions : **recensement gelé**, caractérisation du repli 50 | `replis_exception` (9) | non |
| 379 | 46 `except: pass` jugés ; hypothèse réfutée ; contexte gelé | `pass_et_contexte` (24) | non |

## Chiffres de la tranche

- Suite : **2610 → 2754 passed** / 2 skipped — **+144 tests**, jamais rouge.
- **9 gardiens** ajoutés (149 tests).
- **1 seule faille réelle** (lot 372), **1 seul lot touchant la production**
  (3 fichiers, **MD5 0/8**, navigateur 0 erreur).
- Service worker : **`td-shell-v187` sur les dix lots** — aucun octet servi n'a
  changé de toute la tranche.
- 10 PR : #402 → #411, toutes fusionnées en squash.

## Le fil rouge méthodologique — douze fois où l'outil était en cause

C'est le vrai enseignement de la tranche, et il s'est **inversé** en cours de
route :

1. **L'outil accuse du code sain** — 374 (×2 : invariant syntaxique mal choisi,
   puis résolution transitive insuffisante), 375 (`ast.walk` descendait dans les
   portées imbriquées), 376 (mots entre backticks pris pour des clés).
   → *Un gardien qui crie au loup finit désactivé.*
2. **Le périmètre de l'outil ment** — 373 (`os.listdir` masquait le producteur
   HTML central), 377 (`return <Dict>` manquait tous les `jsonify` : **33 % de
   couverture dans un gardien déjà fusionné**).
   → *Toujours se demander sous quelle ENVELOPPE la chose cherchée se présente.*
3. **L'outil m'empêche d'INNOCENTER** — 378 (`s = 50.0` n'était pas le neutre :
   à vide la fonction rend 76).
   → *Le raisonnement élégant se vérifie sur valeurs réelles, dans les deux sens.*
4. **La borne trop lâche** — 378 (tolérance 3 sur une mesure de 1).
   → *Une borne qui absorbe la première régression n'est pas une borne.*
5. **La preuve elle-même est fautive** — 379 (mutation écrasée par la vraie
   définition).
   → *Un cas qui ne mord pas accuse d'abord la preuve.*

## Dossiers en attente de GO — état à jour

purge É2 (25 defs / 1 866 lignes) · purge É3 · 24 fonctions de tête (326) ·
5 modules reliques `vertex/ui/` (327) · **7 constantes `PAGE_*` : 604 Ko de HTML
assemblés à chaque import, jamais servis (374) — candidat le mieux chiffré** ·
empreinte dans les URL d'actifs (361) · filet desk (362, option A recommandée) ·
« points réels du scan » sur `/markets` (363) · PORTFOLIO_FIT dans
`thesis_health` (365) · échappement centralisé des étiquettes (368-369, coût
mesuré : 1 page sur 8) · durcissement de `vocab_js` (373, **déconseillé**) ·
3 docstrings sous-déclarées (375) · marquage des replis `0` de
`_followed_count`/`_positions_count` (378) · **verdicts affirmés sur univers vide
dans `context()` (379, jumeau du 363)**.

## Portée du volet B

Les chiffres viennent des rapports de lot et de la suite exécutée à l'instant ;
je n'ai pas rejoué les mesures des lots antérieurs. Les nombres de tests par
gardien sont les **collectés** (paramétrage inclus), pas les `def test_`.

## Suite

**LOT 380 : bilan de la tranche 370-379**, à rédiger à partir de ces matériaux.
Pistes encore ouvertes pour la tranche suivante : refus construits en variable
(377) ; trois sites de concaténation à constantes (374) ; formes imbriquées des
promesses de retour (375) ; les 38 `except: pass` « autres » qu'un classificateur
plus fin pourrait trancher.
