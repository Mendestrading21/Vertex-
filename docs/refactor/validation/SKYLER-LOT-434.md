# SKYLER LOT 434 — « Aucune anomalie détectée sur le scan courant » quand il n'y a pas de scan — et la garde correcte est vingt lignes plus haut, dans le même fichier

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-434` (base : lot 433 fusionné,
a9cd1cb)

Dix-septième lot de la veine. Le 433 avait ouvert trois phrases rassurantes de
`/portfolio` et laissé **43 des 47** non vérifiées, en nommant les candidates des
autres pages. Ce lot les ouvre.

**Aucun code, aucun gardien, aucun test.**

## La question, la même qu'au 433

*La carte distingue-t-elle « rien à signaler » de « je ne peux pas mesurer » ?*

## Un instrument écarté, et je le dis

J'ai d'abord voulu répondre par balayage : extraire la fonction englobant chaque
phrase et y chercher une formule d'absence d'entrée. **Deux versions de ce
détecteur ont rendu des lignes propres, alignées et fausses.**

La première testait la présence de la garde **dans toute la page** au lieu de
**dans la fonction** : elle rendait « OUI » pour `renderRadar` *et* pour
`renderAnomalies`, alors que la garde n'existe que dans la première. La seconde,
corrigée par appariement d'accolades, remontait à la mauvaise fonction englobante
(`paint` au lieu de `renderAnomalies`) et retrouvait un « indisponible » qui
concernait un autre onglet.

**Les deux confirmaient commodément ce que j'attendais.** J'ai jeté le balayage
et mesuré par **exécution**. Le résultat ci-dessous ne doit rien au détecteur.

## Ce qui a été mesuré, en exécutant les octets servis

`renderAnomalies` extraite du marquage servi de `/opportunities` (**3 523
octets**, appariement d'accolades), exécutée sous Node 22 avec `VX.fetch` stubé :

```text
état du scan                                       rendu de la carte
3 titres, 2 anomalies                              tableau des anomalies      ← témoin positif
2 titres RÉELS, aucune anomalie                    « Aucune anomalie action détectée
                                                     sur le scan courant. »   ← phrase LÉGITIME
AUCUN SCAN (rows vide — jamais lancé, /scan KO)    « Aucune anomalie action détectée
                                                     sur le scan courant. »   ← MÊME PHRASE
/scan indisponible (payload vide)                  idem
```

**Trois états distincts, une seule phrase.** Et cette phrase affirme deux choses
qui ne sont pas vraies dans les deux derniers cas : qu'une **détection** a eu
lieu, et qu'il existe un **scan courant**.

## La garde correcte est dans le même fichier

`renderRadar`, **7 652 octets**, même page, même source `/scan` :

```javascript
const rows = (scan.rows||[]).filter(r => r.score !== undefined);
if (!rows.length) { $('op-body').innerHTML =
  VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.'); return; }
```

Mesuré par extraction : la garde `!rows.length` est **présente dans
`renderRadar`, absente de `renderAnomalies`**. Ce n'est plus un contre-exemple
sur une autre page comme au 433 (`/system`) — c'est le **même fichier**, la
**même page**, la **même donnée**.

Conséquence de bord : la vue radar étant protégée, les deux autres phrases que
j'avais mises en cause sur `/opportunities` — « Aucune asymétrie exceptionnelle
détectée. Attendre est une décision valide. » et « Aucun candidat en zone
actionnable » — sont **inatteignables sans scan**. **Elles sortent du dossier**,
et je le dis parce que ça réduit ma propre liste.

## Un troisième comportement, et il nuance le constat

`/markets` : `moversRows` rend « Aucune variation exploitable dans le dernier
scan. » sans garde amont — mais son appelant écrit, **juste en dessous** :

```javascript
`… ${VX.updateIndicator(…)} · ${rows.length} titres scannés</div>`
```

Sans scan, la carte affiche donc la phrase **et** « **0 titres scannés** ». La
confusion existe dans la phrase, l'information honnête est **à côté**. Ce n'est
pas le cas de la vue anomalies, qui n'affiche aucun compte.

**Trois comportements sur la même donnée** :

```text
renderRadar (/opportunities)     garde explicite, phrase distincte        ✓
moversRows  (/markets)           pas de garde, mais « 0 titres scannés »  ~ atténué
renderAnomalies (/opportunities) pas de garde, aucun compte affiché       ✗ défaut
```

## Ce que les autres candidates donnent

- `/` « Aucune alerte active. » — les alertes sont des **données utilisateur** :
  vide signifie que l'utilisateur n'en a pas. **Honnête.**
- `/` « Aucun catalyseur imminent identifié. » — c'est l'`emptyText` du builder,
  et l'échec de `/cal-feed` est traité par un `catch` **distinct**. **Honnête.**
- `/` « Aucune opportunité retenue par le comité. » — dépend de `/api/command` ;
  je n'ai **pas exécuté** ce chemin. **Non conclu, et je ne le compte pas.**

## Classement

**Rang 1**, famille des 432/433 : aucune valeur inventée, c'est la phrase qui
affirme une détection qui n'a pas eu lieu. Moins lourd que le 433 — une seule
carte, dans une vue secondaire (`/opportunities?view=anomalies`) — mais du même
sens : **elle rassure**. Un trader qui ouvre la vue anomalies après un
redémarrage lit « aucune anomalie détectée » alors que rien n'a été scanné.

Correction pressentie, déjà écrite vingt lignes plus haut : la garde
`if(!rows.length)` de `renderRadar`, avec sa phrase « Aucun titre scanné ».
**Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne mentionne `renderAnomalies` : **aucun gardien.**

## Portée

Sept candidates ouvertes sur les 47 phrases recensées au 433 ; **quarante
restent non vérifiées**. Sur les sept : **1 défaut**, 1 atténuée, 2 retirées du
dossier (inatteignables), 2 honnêtes, **1 non conclue faute d'exécution**.

Je n'ai **pas observé** l'application sans scan dans un navigateur : la mesure
exécute le code servi avec un payload `/scan` fabriqué. Le fait que le scan soit
vide au démarrage est connu depuis le 425, mais il n'est pas re-mesuré ici.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-septième lot court. Séquence : **431 ~ · 432 ✓ · 433 ✓ (bornage qui
aggrave) · 434 ✓ (bornage qui TRIE)**.

Ce bornage-ci ne dit ni « exception » ni « motif général » : il **trie**. Sur
sept phrases suspectes, une seule est un défaut, deux sortent du dossier parce
qu'une garde amont les rend inatteignables, une est atténuée par un chiffre
voisin. La famille ouverte au 432 existe, mais elle est **moins large que ce que
le 433 pouvait laisser croire** — et le dire vaut mieux que de gonfler la liste.

Le point le plus dur reste celui-ci : **deux versions de mon détecteur m'ont
donné la réponse que j'attendais, et les deux étaient fausses.** Seule
l'exécution a tranché.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
