# SKYLER LOT 380 — Bilan de la tranche 370-379

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-380` (base : lot 379 fusionné,
8535a66) · **Checkpoint, pas une piste.**

## 1. Vérification en vrai

Serveur DEMO, `/scan` d'abord (20 lignes servies), puis les 8 pages produit.

```text
/                fc15688d1af6 = réf      /portfolio   f1b41b665d4a = réf
/markets         c0bb91c6971a = réf      /options     6387210de785 = réf
/opportunities   6a22a6abbd03 = réf      /journal     243699ace2d5 = réf
/analysis        113827718e99 = réf      /system      73e917c0f2d0 = réf

DIVERGENCES MD5 : 0 / 8
```

Navigateur réel (Chromium, 1440×900), les 8 pages :

```text
page             erreurs   texte  squelettes résiduels
/                      0    3369   0        /portfolio         0    1590   0
/markets               0    2775   0        /options           0    2937   0
/opportunities         0    4660   0        /journal           0    3673   0
/analysis              0     899   0        /system            0    4106   0

TOTAL erreurs console : 0
```

**Les octets servis n'ont pas bougé d'un bit sur les dix lots**, et les huit pages
s'hydratent sans une erreur. Le « smoke » sort une fois de plus « hors plage » :
c'est le faux signal tranché au lot 372 (il mesure le HTML brut contre des
références du DOM hydraté) — les longueurs de DOM ci-dessus, elles, retombent
bien sur les ordres de grandeur attendus.

## 2. Les neuf gardiens mordent-ils encore ?

Un gardien fusionné mais devenu muet est le défaut le plus coûteux de la tranche
— c'est exactement ce qu'a révélé le lot 377. Une faute réelle rejouée par
gardien, restauration vérifiée :

```text
test_memoire_cellule_lot371.py    MORD   titre nourri par la donnée (faute du 368)
test_json_script_lot372.py        MORD   json.dumps nu pour PARAMS (la XSS du 372)
test_contexte_js_lot373.py        MORD   étiquette de vocabulaire contenant `<`
test_script_concatene_lot374.py   MORD   route héritée /bordel reservie
test_promesses_retour_lot375.py   MORD   clé promise retirée de la sortie anticipée
test_refus_honnete_lot376.py      MORD   motif de refus vidé en chaîne vide
test_refus_api_lot377.py          MORD   refus d'API rendu muet
test_replis_exception_lot378.py   MORD   repli numérique non recensé
test_pass_et_contexte_lot379.py   MORD   config.grade rendu faillible

VERDICT : les 9 gardiens de la tranche mordent encore
```

## 3. Les dix lots

| Lot | Verdict | Gardien | Production |
|-----|---------|---------|------------|
| 370 | Checkpoint 360-369 : 8/8 MD5, 0 erreur console | — | non |
| 371 | Route sœur du 368 : **saine**, prouvée sur cellules réelles | 5 | non |
| 372 | **XSS RÉELLE corrigée** — `json.dumps` nu dans un `<script>` | 35 | **3 fichiers, MD5 0/8** |
| 373 | Même faute ailleurs : **danger latent verrouillé** sur 8 pages | 27 | non |
| 374 | `<script>` concaténés : angle mort réel, **sans surface exploitable** | 21 | non |
| 375 | Promesses de retour tenues ; promesses en un mot **non décidables** | 10 | non |
| 376 | Piste close par la mesure → **contrat de refus honnête** exhibé | 9 | non |
| 377 | **Le gardien du 376 n'en voyait qu'un tiers** (13 sur 39) | 9 | non |
| 378 | Exceptions : **recensement gelé**, repli 50 caractérisé | 9 | non |
| 379 | 46 `except: pass` jugés ; hypothèse réfutée ; contexte gelé | 24 | non |

## 4. Les chiffres

- Suite : **2610 → 2754 passed** / 2 skipped — **+144 tests**, jamais rouge.
- **9 gardiens** ajoutés (149 tests collectés).
- **1 seule faille réelle** sur dix lots, **1 seul lot touchant la production**
  (3 fichiers, MD5 0/8, navigateur 0 erreur).
- Service worker : **`td-shell-v187` sur les dix lots** — pas un octet servi
  modifié.
- **10 PR** (#402 → #411), toutes fusionnées en squash. `main` jamais touchée,
  aucun push forcé, aucun fichier runtime commité.

## 5. Le fil rouge — douze fois où l'outil était en cause

C'est le véritable apport de la tranche, et il s'est présenté sous **cinq formes
distinctes** :

1. **L'outil accuse du code sain** — 374 (×2), 375, 376.
   *Un gardien qui crie au loup finit désactivé.*
2. **Le périmètre de l'outil ment** — 373 (`os.listdir` masquait le producteur
   HTML central), 377 (`return <Dict>` manquait tous les `jsonify` : **33 % de
   couverture dans un gardien déjà fusionné**).
   *Toujours se demander sous quelle ENVELOPPE la chose cherchée se présente.*
3. **L'outil m'empêche d'INNOCENTER** — 378 : `s = 50.0` n'était pas le neutre de
   l'échelle, la fonction rend 76 à vide.
   *Le raisonnement élégant se vérifie sur valeurs réelles — dans les deux sens.*
4. **La borne trop lâche** — 378 : tolérance de 3 sur une mesure de 1.
   *Une borne qui absorbe la première régression n'est pas une borne.*
5. **La preuve elle-même est fautive** — 379 : mutation écrasée par la vraie
   définition, d'où un faux « ne mord pas ».
   *Un cas qui ne mord pas accuse d'abord la preuve.*

## 6. Jugement franc sur le rendement

**Ce que la tranche a apporté.** Une vraie faille, sérieuse : `/opportunities`
laissait passer les valeurs de paramètres d'URL dans un bloc `<script>`, ce qui
rendait une XSS **déclenchable à distance par un simple lien**, dans une session
ayant accès au desk local. Elle a été trouvée, corrigée, prouvée MD5-neutre et
verrouillée. À elle seule, elle justifie la tranche.

**Ce qu'elle n'a pas apporté, et il faut le dire.** Après le lot 372, **sept lots
n'ont trouvé aucune nouvelle faille exploitable**. Uniquement des dangers
latents, des caractérisations et des verdicts « sain ». Sur la veine
sécurité/honnêteté prise seule, **le rendement décroît nettement** : 1 faille sur
les 6 premiers lots de la séquence 367-372, **0 sur les 7 suivants**. Continuer à
la creuser au même rythme donnerait surtout des lots honnêtes mais maigres.

**Ce qui, en revanche, s'est révélé fertile.** Le lot 377 n'a pas audité le code
mais **un gardien déjà fusionné**, et y a trouvé 33 % de couverture là où le vert
laissait croire à 100 %. C'est une veine neuve et sérieuse : la suite compte
2 754 tests dont personne n'a vérifié qu'ils voient ce qu'ils prétendent voir.
Un test au vert qui ne mesure rien est plus dangereux qu'un test absent.

**Et un point de blocage réel.** Les dossiers en attente de GO sont désormais
**quatorze**, dont plusieurs mesurés au chiffre près — 604 Ko de HTML mort
assemblés à chaque import, le filet desk qui perd le travail de la journée, deux
questions d'honnêteté d'affichage jumelles (363 et 379). L'agent ne peut pas les
trancher : ce sont des décisions produit. **C'est maintenant le vrai goulot**, pas
le manque de pistes.

## 7. Dossiers en attente de GO — quatorze, à jour

**Purges** : É2 (25 defs / 1 866 lignes) · É3 · 24 fonctions de tête (326) ·
5 modules reliques `vertex/ui/` (327) · **7 constantes `PAGE_*` — 604 Ko de HTML
assemblés à chaque import, jamais servis (374), le mieux chiffré**.

**Robustesse** : empreinte dans les URL d'actifs (361) · filet desk (362, **option
A recommandée** : instantané supplémentaire avant perte) · marquage des replis
`0` de `_followed_count`/`_positions_count` (378).

**Honnêteté d'affichage** : « points réels du scan » sur `/markets` (363) ·
**verdicts affirmés sur univers vide dans `context()` (379)** — les deux sont la
même question posée à deux endroits, et méritent une réponse commune.

**Moteur** : PORTFOLIO_FIT dans `thesis_health` (365).

**Cosmétique / à éviter** : échappement centralisé des étiquettes (368-369, coût
mesuré : 1 page sur 8) · 3 docstrings sous-déclarées (375) · durcissement de
`vocab_js` (373, **déconseillé en l'état** — changerait les octets sur 8 pages
pour zéro gain).

## 8. Ce que la tranche suivante devrait viser

1. **Auditer les gardiens eux-mêmes** (prolongement du 377). 2 754 tests, dont on
   ne sait pas lesquels mordent. Commencer par les plus anciens et les plus
   structurants, en mutant le code qu'ils prétendent protéger. C'est la piste au
   meilleur rendement attendu.
2. **Traiter les caractérisations gelées** dès qu'un GO arrive, en priorité les
   deux questions d'honnêteté jumelles (363 + 379).
3. **Ne pas prolonger artificiellement la veine sécurité.** Il reste des pistes
   (refus construits en variable, formes imbriquées, trois sites de concaténation
   à constantes) mais elles sont fines : les prendre à l'occasion, pas comme
   programme.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 379, 8535a66) ; arbre propre.
- **Aucun fichier de production touché** ; aucun fichier runtime commité.
- Suite : **2754 passed / 2 skipped**. SW : `td-shell-v187`.

## Portée de ce bilan

Une faute rejouée par gardien, pas l'ensemble des cas de chacun : « mord encore »
signifie « n'est pas devenu muet », pas « couvre tout ». Les chiffres des lots
antérieurs viennent de leurs rapports, non rejoués. Et le rendement décroissant
est un constat sur dix lots, pas une loi.

## Suite

**LOT 381 : retour en veille active**, tranche 380-389, avec pour piste
prioritaire l'audit des gardiens existants. Prochaine échéance périodique :
**~lot 390**.
