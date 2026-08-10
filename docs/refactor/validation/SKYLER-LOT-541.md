# SKYLER LOT 541 — Ce que l'utilisateur lit quand ça casse : **103 états, dont 28 erreurs. Huit disent le POURQUOI, quinze ne disent que le QUOI** — et le bon motif existe déjà dans le produit, à quelques lignes des autres

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-541` (base : lot 540 fusionné,
`93c401ad`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix, et la leçon appliquée

**(i)** — le 538 et le 540 ont construit des instruments coûteux dont la réponse
est finalement venue de la **lecture**. La règle écrite au 540 : *compter d'abord
ce qui atteint l'écran*. Ce lot l'applique à ce que l'utilisateur voit **quand
quelque chose casse** : `VX.states.error(cause)` et `VX.states.empty(raison,
action)`.

**J'ai lu le témoin AVANT d'écrire une ligne d'instrument** :

```js
}catch(e){ $('vx-auto-jobs').innerHTML =
    VX.states.error('Registre indisponible : ' + esc(e.message)); }
```

**La cause la plus informative du produit n'est donc pas un littéral : c'est une
cause CONSTRUITE** — contexte du produit **plus** message réel. Classer
« construite » comme une catégorie inférieure aurait faussé le lot dès sa
première ligne.

```text
CALIB 1 · POSITIF   « Registre indisponible : » ressort CONSTRUITE   OK
CALIB 2 · NÉGATIF   un texte FABRIQUÉ n'apparaît nulle part          OK
```

## L'arrêt : un repli littéral n'est pas une cause illisible

Premier jet : `VX.states.empty(o.stateMessage || 'Régime indéterminé — Vertex ne
tranche pas.')` sortait **« non lisible »**. Or le repli **est** une phrase
française explicite, et c'est elle que l'utilisateur lit quand la valeur
dynamique manque. Les ranger parmi les pauvres aurait été faux (**481**).

**Arrêtés avant publication : 154 → 155.**

## La mesure — 103 états, sur 105 programmes servis

```text
`VX.states.error(...)`    28 appels
`VX.states.empty(...)`    75 appels
                         ───
                         103
```

### Les causes d'erreur

```text
construite (contexte + cause réelle)     8
littérale                               17
repli littéral                           1
non lisible                              2
                                       ───
                                        28    FEUILLE : OK

littérales : 2 mots au minimum · 2 à la MÉDIANE · 4 au maximum
littérales de 3 mots ou moins : 15
```

```text
/               « Régime indisponible »        « Opportunités indisponibles »
/               « Alertes indisponibles »      « Calendrier indisponible »
/markets        « Régime indisponible » ×2
/opportunities  « Calendrier indisponible »
/system         « Connexions indisponibles »   « Cerveau Claude injoignable »
/system         « Live Engine injoignable »    « /healthz injoignable »
```

**Quinze messages d'erreur sur vingt-huit disent CE QUI a échoué, pas POURQUOI.**
Huit autres, dans le même produit, disent les deux.

### Les raisons d'état vide

```text
construite   8 · littérale 54 · repli littéral 4 · non lisible 9   = 75   OK
littérales : 3 mots au minimum · 7 à la MÉDIANE · 18 au maximum
```

**Les états vides sont trois fois plus bavards que les erreurs** (médiane 7 mots
contre 2). C'est exactement l'inverse du besoin : un état vide est souvent normal,
une erreur demande une explication.

### L'action proposée

```text
action absente     40 · construite 14 · littérale 13 · chaîne vide 8   = 75   OK
```

## Les onze causes « non lisibles », lues une par une (481)

Aucune n'est un message pauvre :

```text
×3   `emptyCard(host, reason, action)` — /markets, /portfolio, /journal :
     la raison vient de l'APPELANT (`SCAN_ACTION` et consorts, lus au 524).
×6   `esc((d.reason || 'classement indisponible') + '.')` — un repli littéral
     que mon classeur rate à cause de l'enveloppe `esc(…) + '.'`. Limite
     d'instrument NOMMÉE, pas un défaut produit.
×1   `/options fail(el, cause)` — helper dont les appelants passent
     « Chargement overview: » + le message réel (lu au 534).
×1   `/portfolio boot()` — `.catch(e => … VX.states.error(e.message))` : le
     FILET DE DERNIER RECOURS de la page.
```

## Ce que le dépôt fait bien, mesuré

- **Le bon motif existe déjà et il est utilisé 8 fois** :
  `'Registre indisponible : ' + e.message` donne le contexte **et** la cause.
- **`/portfolio` a un filet de dernier recours** : `boot()` rattrape ce que le
  rendu de vue laisse échapper et peint le message. C'est une deuxième ligne de
  défense, en plus des `try/catch` locaux.
- **`/options` centralise ses erreurs** dans un `fail(el, cause)` unique — un
  seul endroit à corriger si la forme doit changer.
- **Les états vides sont argumentés** : jusqu'à 18 mots, avec un lien d'action
  dans 27 cas sur 75.
- **103 états explicites pour 8 pages** : le produit prévoit l'échec partout, ce
  n'est pas une interface qui suppose que tout marche.

## Ce que ce lot NE tranche PAS

**Je n'ouvre pas de dossier.** « Régime indisponible » n'affiche **rien de
faux** ; c'est une question de qualité d'information, pas d'exactitude. Le
relevé est posé, l'arbitrage appartient à l'humain (**527-A**) :

> *quinze messages d'erreur donnent le quoi sans le pourquoi, alors que le
> produit sait faire les deux et le fait huit fois.*

## Portée — ce que ce lot NE dit PAS

- **Le nombre de mots n'est pas la qualité.** « /healthz injoignable » fait deux
  mots et dit l'essentiel ; « Régime indisponible » aussi, sauf qu'il ne dit pas
  si c'est le réseau, le serveur ou la donnée.
- **Les 40 états vides sans action ne sont pas un défaut** : « Aucune alerte
  active. » n'appelle aucune action.
- Six causes portent un repli littéral que mon classeur rate (enveloppe
  `esc(…)`) : la limite est nommée, non levée.
- **Aucune exécution** : ce lot lit le code servi, il ne rend pas les messages.
- **Aucun navigateur, aucune route interdite, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier — mais un **relevé qui pose une question de produit**, pour la
première fois depuis longtemps : le dépôt possède un bon motif de message
d'erreur et ne l'applique qu'à huit endroits sur vingt-huit.

Ce qu'il faut dire sans le maquiller : **la leçon du 540 a marché.** Lire le
témoin d'abord a évité de bâtir un classement où « construite » aurait été la
catégorie faible — alors que c'est la meilleure. Un instrument conçu après la
lecture est un instrument qui mesure la bonne chose.

Trois règles neuves :

- **541-A · LA FORME LA PLUS RICHE PEUT ÊTRE CELLE QU'ON CROIT ILLISIBLE** — la
  cause construite (`contexte + e.message`) bat la cause littérale ; un classeur
  bâti sans lecture l'aurait rangée en dernier.
- **541-B · UN REPLI LITTÉRAL N'EST PAS UNE CAUSE ILLISIBLE** — `x || 'phrase'`
  est ce que l'utilisateur lit quand `x` manque.
- **541-C · COMPTER DES MOTS N'EST PAS JUGER UNE PHRASE** — la mesure est
  mécanique et le dit ; l'arbitrage sur la qualité revient à l'humain.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 15 messages d'erreur sans pourquoi — relevé
posé, arbitrage humain** ; **les 6 replis littéraux non classés** ; **les 95
atténuations non affichées** ; **`initSettings`, mesurée partiellement** ; **les
8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil
prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 155 (+1)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
