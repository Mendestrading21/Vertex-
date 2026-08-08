# SKYLER LOT 330 — Échéance périodique (8e mesure) + bilan de la tranche 320-329

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-330` (base : lot 329 fusionné,
1d02508) · **Aucun code modifié**

## (a) Smoke-check complet

Serveur DEMO, scan terminé avant mesure (`vertex_ready=20`) :

- **8 × HTTP 200**, **0 erreur console/pageerror**, `client-log count: 0`.
- Tailles de texte : **7 pages sur 8 strictement identiques aux références**
  (/ 3371 · /markets 2794 · /opportunities 4679 · /analysis 923 ·
  /portfolio 1609 · /options 2960 · /system 4124).
- **`/journal` : 3 690 au lieu de 2 676.** Écart expliqué, pas masqué (voir
  ci-dessous).

### L'écart de `/journal`, tranché

Le `desk_data.json` local de cette session contient les trades laissés par la
sonde de round-trip du lot 305 (`myTrades` 196 o, `myTradesClosed` 310 o). Le
texte rendu le confirme mot pour mot : « **3 trade(s) clôturé(s) : 33 % de
réussite, P&L cumulé -700** », « Récidive de pertes sur : NVDA ».

Preuve que ce n'est pas une régression produit : **le MD5 du HTML servi pour
`/journal` est INCHANGÉ** (`243699ace2d5`, identique depuis le lot 323). Le
serveur envoie exactement les mêmes octets ; tout l'écart naît de l'hydratation
par les données locales du navigateur. La référence 2 676 correspond à un desk
vide.

La valeur oscille aussi légèrement d'une mesure à l'autre (3 684 → 3 690 →
3 671) : la page affiche des durées et des dates, donc du contenu daté.

## (b) MD5 des 8 pages — tous conformes

| page | MD5 | référence |
|---|---|---|
| `/` | fc15688d1af6 | ✔ |
| `/markets` | c0bb91c6971a | ✔ |
| `/opportunities` | 6a22a6abbd03 | ✔ |
| `/analysis` | 113827718e99 | ✔ |
| `/portfolio` | f1b41b665d4a | ✔ |
| `/options` | 6387210de785 | ✔ |
| `/journal` | 243699ace2d5 | ✔ |
| `/system` | 73e917c0f2d0 | ✔ (référence du lot 328) |

`/sw.js` sert bien **`td-shell-v187`**. Suite : **2501 passed / 2 skipped**.

## (c) Mini-bilan de la tranche 320-329

**Caractère : la tranche qui a enfin coupé.** Après dix lots de croisière
(310-319), le blocage de permissions qui bloquait la purge depuis le lot 285 est
tombé — et la tranche a basculé du régime « veille » au régime « travail de
fond », sans jamais perdre la discipline de preuve.

| lot | ce qui a été fait |
|---|---|
| 320 | échéance périodique (7e) : smoke parfait + bilan 310-319 |
| 321-322 | veille active, état identique |
| **323** | **PURGE É1 : 82 définitions mortes retirées, terminal.py 10 743 → 7 164 lignes (-33 %)** |
| 324 | hygiène post-purge : 11 imports orphelins de `terminal.py` + gardien AST |
| 325 | même audit étendu aux 183 modules de `vertex/` : 11 morts retirés, **1 piège gardé** |
| 326 | trois pistes instruites : assets (SAIN), routes (SAIN), 24 fonctions → laissé à l'humain |
| 327 | `CLAUDE.md` remis au vrai + **correction de ma propre erreur du lot 323** |
| 328 | honnêteté d'affichage : libellé `__DESK_KEYS` corrigé, **bump SW v186 → v187** |
| 329 | vérification que c'était un cas isolé : 30 identifiants affichés, 0 périmé |

**Chiffres.** Suite **2516 → 2501** — la baisse est saine et documentée : les
17 tests retirés étaient des tests de caractérisation écrits *pour* le moment de
la purge. SW **v186 → v187** (un seul bump, justifié par un seul octet servi
modifié). **10 PR fusionnées** (#352 → #361). `terminal.py` **-3 590 lignes**
au total (-33,4 %).

**Ce que je retiens de la tranche.** Trois fois, le réflexe évident aurait été
une erreur : l'import `BROKER` qui *est* un diagnostic (325), les 24 façades
IBKR qui sont le chemin de lecture du compte réel (326), et ma propre règle du
lot 323 qui citait un fichier mort (327). Un compteur ne distingue pas le mort
de l'endormi — c'est la leçon de fond de ces dix lots.

**Ce qui reste ouvert** (décision humaine, rien n'est engagé) : purge É2
(25 défs / 1 866 l.), purge É3 (dépendances croisées), les 24 fonctions du lot
326, les 5 modules `vertex/ui/` reliques du lot 327.

## Décision SW

**Pas de bump** (`td-shell-v187`) : aucun code touché, docs seulement.

## Suite

LOT 331 : retour au canevas de veille active. Prochaine échéance périodique :
~lot 340.
