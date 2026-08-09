# SKYLER LOT 413 — Les 156 chemins que le client peut demander : aucun ne pointe dans le vide

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-413` (base : lot 412 fusionné,
b7a13d6)

Un chemin d'API mal écrit côté client ne casse rien de visible : la requête part,
le serveur répond 404, la carte reste sur son état vide — **honnête en apparence,
mais pour une mauvaise raison**. Personne n'avait vérifié que tous les chemins
demandés par le navigateur correspondent à une route enregistrée.

**Aucun code, aucun gardien, aucun test.**

## Le périmètre : ce que le navigateur reçoit vraiment

Pas les sources — les **octets servis**. Les 8 pages sont demandées au serveur en
mémoire (`test_client`, HTTP 200), puis **chaque `<script src>` est demandé au
serveur à son tour**.

```text
pages servies                     8   (8 × HTTP 200)
scripts externes réellement servis 26
blocs de JS inline                15
corpus                            1 243 931 octets
```

La résolution n'est pas devinée : elle passe par `app.url_map.bind(...).match()`,
donc par les **190 routes réellement enregistrées**.

## L'instrument s'est trompé deux fois — et c'est mesuré

**1. Les 26 fichiers `/static` n'étaient pas dans le corpus.** La première
version les cherchait sur disque en transformant `/static/vertex/js/…` en
`vertex/js/…` : chemin faux, fichiers introuvables, corpus amputé.

```text
v1 (disque, chemin faux)   515 108 octets   42 chemins
v2 (demandés au serveur)   798 881 octets   52 chemins
```

*Demander le fichier au serveur, c'est aussi éviter d'avoir raison sur
l'arborescence.*

**2. Le détecteur ne connaissait que `fetch(`.** `options-intel.js:466` appelle
`get('/api/options/strategies/' + encodeURIComponent(sym))` — une **aide
locale**. C'est exactement la faute du lot 409, refaite avec une autre
enveloppe. Corrigé en extrayant **tout littéral de chemin, quel que soit
l'appelant**.

**3. Trois faux morts par la normalisation.** `'/api/options/gex/' +
encodeURIComponent(sym)` était rendu `/api/options/gex/` → `NotFound`. La
concaténation **en queue** est maintenant reconnue comme segment dynamique.

## Témoins

```text
route réelle      /api/market/summary        → OK
route inventée    /api/zzz-inexistant-lot413 → NotFound     ← discrimine
segment dynamique /api/options/gex/X         → OK
```

Et **de bout en bout**, sur les trois formes d'écriture — appel direct, appel via
une aide locale, concaténation en queue — l'extracteur retrouve les trois
chemins. Un `fetch('/api/reco-inexistante-413')` déposé dans un fichier servi
**serait** rapporté.

## Le résultat

```text
chemins distincts confrontés à l'url_map     156
   résolvent                                 149   (dont 8 par segment dynamique)
   ne résolvent pas                            7   ← ouverts un par un
appels /api distincts                          55   tous résolus
```

**Les 7 candidats, ouverts un par un — 7 faux positifs de l'extracteur, aucune
requête :**

```text
/1%IV            options-intel.js:492   unité affichée (« Vega … /1%IV »)
/100             intelligence_page.py, opportunities_page.py   unité (« 72/100 »)
/api             vx-router.js:42        test de préfixe : indexOf('/api')===0
/static          vx-router.js:42        même test
/api/ibkr        vx-core.js:228/272     préfixe de politique de cache
/api/positions   vx-core.js:228/272     préfixe de politique de cache
/api/account     vx-core.js:228/272     préfixe de politique de cache
```

**Zéro chemin mort.** Le zéro est **substantiel** : 156 littéraux confrontés à un
`url_map` exécuté, et les 7 restants lus dans leur ligne — pas comptés.

## Ce que la vérification a trouvé au passage — trivial, et dit comme tel

`/api/account` figure dans **les deux** listes de politique de cache du client
(`PERSIST_DENY` et `LIVE_TTL`, `vx-core.js:228` et `272`). Or :

```text
routes enregistrées commençant par /api/account   0   (sur 190)
appels du client commençant par /api/account      0   (sur 55)
occurrences ailleurs dans le dépôt                0
```

C'est une **entrée morte dans une politique de cache** : elle ne dénie rien, elle
ne raccourcit aucun TTL. **Aucune conséquence visible pour le trader** — ni
chiffre faux, ni carte absente. Classé **rang 4**, et je ne le corrige pas : ce
serait exactement le « changement gratuit » que la boucle s'interdit.

*Les cinq autres préfixes, eux, mordent* (`/api/ibkr` → `/api/ibkr/positions`,
`/api/positions` → 2 appels, `/api/desk`, `/api/pos-quotes`, `/api/tracking`) —
c'est le témoin positif qui rend le `0` de `/api/account` lisible.

## Portée — et pourquoi elle est plus étroite qu'elle en a l'air

L'extraction est **statique** : un chemin entièrement calculé
(`'/api/' + kind + '/' + id`) lui échapperait. Mesuré plutôt qu'affirmé :

```text
appels `fetch(` dans le corpus servi                    91
   1ᵉʳ argument = littéral commençant par « / »          85
   1ᵉʳ argument = variable                                6
```

Les **6** sont ouverts : `url`, `u`, `href` — ce sont les **tuyaux eux-mêmes**
(l'implémentation de `VX.fetch`, le `fetch` de fragment du routeur), qui
reçoivent les URL construites aux 85 sites littéraux. **Aucun endpoint distinct
ne s'y cache.**

Ce lot ne dit rien de ce que les routes **renvoient** : il établit qu'elles
**existent**. Une route présente qui répondrait n'importe quoi passerait ce
contrôle.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout, la sonde vit
  entièrement dans le scratchpad. Pas de preuve MD5 requise, pas de bump.
  SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Dix-septième lot court. Cinquième bornage sur les six derniers lots — et celui-ci
ferme une question qui n'avait jamais été posée : *le client demande-t-il des
choses qui n'existent pas ?* **Non.**

Ce qu'il faut retenir de la méthode : l'instrument a encore fauté **deux fois sur
un même lot**, dont **une répétition exacte de la leçon du 409** (compter une
fonction sans ses enveloppes). Une règle écrite ne suffit pas — c'est le témoin
qui l'attrape.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
