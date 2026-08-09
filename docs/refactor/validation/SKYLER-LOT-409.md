# SKYLER LOT 409 — Les 8 pages balayées : une seule consigne impossible, celle du 406

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-409` (base : lot 408 fusionné,
7e8fd74)

Le lot 406 a trouvé **un** état vide qui donne au trader une consigne que le code
ne peut pas honorer. Les 8 pages n'avaient pas été balayées. Ce lot le fait.

**Aucun code, aucun gardien, aucun test.**

## L'instrument s'est trompé, et le témoin l'a montré

Premier détecteur : compter les appels `states.empty(`. Il en trouvait 85 — **mais
pas le site du lot 406**. C'est le témoin positif qui l'a révélé.

La raison : `portfolio_page.py` et `performance_page.py` passent par une **aide
locale** (`emptyCard(host, reason, action)`), et mon détecteur comptait la
**définition** de l'aide, jamais ses appels.

Corrigé — les aides locales qui enveloppent `states.empty` sont identifiées, puis
leurs appels comptés :

```text
sites d'état vide réellement affichés   88   (direct 83 · via une aide locale 5)
aides locales détectées : emptyCard (portfolio_page.py, performance_page.py)
```

Témoin après correction : `portfolio_page.py:623` — la carte « Courbe d'équité
indisponible » — **est retrouvée**.

*Compter les appels d'une fonction sans compter ceux de ses enveloppes, c'est
mesurer la mécanique et rater l'usage.*

## Le filtre : un état vide qui DÉCRIT n'est pas un état vide qui PROMET

La grande majorité des 88 décrivent honnêtement une absence : « VIX non fourni
par le dernier scan », « Aucun titre scanné ». Rien à leur reprocher.

Le défaut du 406 a une forme précise : **le message dit à l'utilisateur de faire
quelque chose, et le faire ne produira pas le résultat annoncé.** Filtrage sur
les tournures d'instruction ou de promesse (« se construit », « renseigne »,
« marque une », « ajoutez », « créez », « lancer un scan », « au fil des »…) :

```text
états vides porteurs d'une consigne ou d'une promesse   12 / 88
```

## Les 12, vérifiés un par un

Pour chacun, le mécanisme promis a été cherché dans le code — pas supposé.

```text
promesse                                        mécanisme                        verdict
« lancer un scan depuis Système » ×3            /api/rescan (7 réf.)             TENABLE
« Marque une idée Suivre »                      followStock() + bouton servi     TENABLE
« créez un suivi depuis une analyse »           followStock(entry/stop/tgt)      TENABLE
« ajoutez les titres à surveiller »             set('vxWatchlist') ×2            TENABLE
« ouvrir une analyse pour le détail »           route /analysis                  TENABLE
« le flux se remplit au rythme des scans »      flux d'événements live           TENABLE
« renseigne le champ erreur »                   champ j-mistake → e.mistake      TENABLE
« renseigne le champ leçon »                    champ j-lesson  → e.lesson       TENABLE
« renseigne état émotionnel »                   champ j-emo     → e.emo          TENABLE
« elle se construit au fil des clôtures »       set('myTradesEquity') → 0 site   ★ IMPOSSIBLE
```

Les trois consignes du Journal méritaient l'examen : elles nomment des champs
précis. Vérifié — `performance_page.py` L338-341 construit bien les champs
`j-lesson`, `j-mistake`, `j-emo`, et L355 les écrit dans l'entrée
(`lesson: v('j-lesson'), mistake: v('j-mistake'), emo: v('j-emo')`). Le trader
peut donc les renseigner, et les cartes se rempliront.

**Une seule consigne est impossible : celle du lot 406.** Aucun site n'écrit
`myTradesEquity` — vérifié une nouvelle fois, **0**.

## Ce que ce lot établit

Le défaut du 406 est **unique sur les 8 pages servies**. Comme le 408 l'a fait
pour le `|| 0` du 407, ce lot **borne** le dossier plutôt que de l'élargir :

- 88 états vides affichés, 12 porteurs d'une consigne, **11 tenables, 1 non** ;
- la correction reste **un texte ou un mécanisme, sur une seule carte**.

Le zéro est ici **substantiel** : 12 promesses examinées une par une, pas un
comptage global.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve
  MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Le filtre de promesses repose sur une liste de tournures françaises. Une consigne
formulée autrement — « il suffit de… », une phrase à l'infinitif — passerait au
travers ; la liste est écrite dans le rapport pour qu'on puisse la contester. Et
« TENABLE » signifie *le mécanisme existe et écrit la donnée lue* : cela ne dit
pas que le parcours soit ergonomique ni que le bouton soit trouvable.

## Où en est la boucle

Quatorzième lot court. Trois lots consécutifs autour d'une même veine : 406 et
407 ont trouvé, 408 et 409 ont **borné**. Le dossier de rang 1 est maintenant
complètement délimité — une cause, un site pour le `|| 0`, une carte pour la
promesse.

**Prochaine échéance : bilan n°10 au lot 410.**

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388.
