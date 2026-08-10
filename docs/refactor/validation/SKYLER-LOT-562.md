# SKYLER LOT 562 — le premier des sept chiffres lourds : **178 se reproduit exactement**, mais c'est un **cumul par page** — les sites d'appel distincts sont **94**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-562` (base : lot 561 fusionné,
`0ad511c4`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — tout est
relu sur disque.

## Le choix

**(hh)** — sept chiffres traînent depuis vingt lots dans la liste des dettes. Le
557-A dit qu'un chiffre non recompté est une dette ; le 561 vient de montrer
qu'un chiffre hérité peut être faux de plusieurs manières à la fois. **On n'en
prend qu'un** : les **178 appels du 534**.

## Le banc existe — c'est une reproduction, pas une reconstruction

Le brief prévoyait qu'il puisse avoir disparu. `ls` du scratchpad : `l534_ast.js`,
`l534_ast.json`, `l534_parseur.py`, `l534_corpus.json`, `l534_temoins.py` sont
tous là. **Aucune reconstruction n'a été nécessaire.**

## Vérifié à la source (559-A) — ce que 178 comptait exactement

- `SKYLER-LOT-534.md:82`, colonne « B · acorn » : « appels au total **178** ».
- `l534_parseur.py:143-159` en donne la définition littérale :

```python
for a in d['appels']:
    if a['porteurHelper']:
        continue            # le helper lui-même n'est pas un chargeur
    B[(a['page'], a['fonction'])]['appels'] += 1
```

**Reproduction exacte : 183 entrées − 5 portées par le helper = 178.**
La dette « non recompté » est donc soldée sur le plan de la reproductibilité.

## Ce que le chiffre ne dit pas — **178 est un cumul par page**

```text
entrées brutes de `appels`                    183
portées par le helper lui-même (exclues)        5
APPELS AU TOTAL — cumul par page              178
SITES D'APPEL DISTINCTS (signature)            94
   signatures vues sur plus d'une page          12
   unités en double                             84
```

Un fichier JavaScript **statique** servi sur les huit pages est analysé **huit
fois**, et ses appels comptés huit fois. Les douze signatures concernées sont
nommées : `(programme)` ×4, `VX.swr`, `_warm`, `loadStatus`, `navigate`, `run`,
`tick`, `tickerMatches`, `watchSession` — **chacune sur les 8 pages**, soit
**84 unités en double**.

**Le nombre 178 n'est pas faux** : le prédicat était « appels au total sur le
corpus servi », et le corpus servi contient bien huit fois ces fichiers. **Mais
« 178 appels » se lit spontanément comme 178 endroits dans le code, et il y en a
94.** C'est exactement la distinction 561-B, un lot plus tard, sur un autre
chiffre.
**Interprétations retirées : 5 → 6 (+1).**

## L'arrêt du lot — **les corrections des 555-560 ne s'appliquent pas ici**

Le brief demandait « que vaut cette mesure avec les corrections de portée des
555-560 ? ». Les appliquer aurait été une faute. Mesuré, en lisant les champs
que porte chaque entrée :

```text
champs d'une entrée : chaine · cloture · declaration · fonction · forme ·
                      helper · page · porteurHelper · pos · proprietaire ·
                      protection
champs décrivant la VALEUR RENDUE par l'appel :  AUCUN
```

**Le 534 compte des sites d'appel, pas des variables de résultat.** Or les
corrections des 555 à 560 — portée par fonction, `Promise.allSettled`, espace de
noms plat — portent **toutes** sur le marquage de la valeur rendue. Elles n'ont
aucune prise sur un compteur de sites d'appel. **Les appliquer par analogie
aurait produit un chiffre faux** (560-A).

**Arrêtés avant publication : 187 → 188 (+1).**

## Ce que le dépôt fait bien, mesuré

- **Le banc du 534 est intégralement conservé et rejouable** vingt-huit lots plus
  tard, avec zéro erreur d'analyse sur 113 programmes et 3 345 728 octets.
- **La comparaison 120 contre 178 reste valide** : les deux colonnes emploient la
  même convention de cumul, sur le même corpus, dans le même processus — le 534
  avait respecté 546-A avant que la règle n'existe.
- **Le corpus du 534 est plus large que celui du 553** (113 programmes contre
  41 ; 3,3 Mo contre 0,8 Mo) parce que le 553 **dédoublonne** les fichiers
  statiques et pas le 534. Deux choix légitimes, deux grandeurs différentes.

## Second contrôle (481) — ce que ce lot ne décide pas

- **Aucun des six autres chiffres lourds n'est touché** : 112 atténuations, 103
  états, 53 refus, 156 variables serveur, 25 fonctions exécutées, 11 limites
  levées restent non recomptés.
- **94 n'est pas « le vrai chiffre »** qui remplacerait 178 : ce sont deux
  grandeurs, un cumul et un distinct, et le rapport 534 mesurait bien le cumul.
- La signature retenue est (fonction, position, helper, forme) ; **deux appels
  réellement distincts qui partageraient ces quatre valeurs seraient fusionnés**.
  Le cas n'est pas exclu par construction.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Un des sept chiffres lourds est enfin sorti de la liste** — non
parce qu'il était faux, mais parce qu'il est maintenant **reproduit et
qualifié** : 178 en cumul, 94 en distinct, et la raison de l'écart nommée
fichier par fichier.

Ce qui mérite d'être dit : **le brief me demandait de recompter avec des
corrections qui n'avaient rien à voir.** Six lots de suite ont trouvé le même
type de défaut — un marquage trop large — et l'habitude s'installe de le
chercher partout. Le 560 avait déjà prévenu (« un défaut ne se généralise pas
par analogie ») ; il a fallu ouvrir les champs d'une entrée pour vérifier que
cette fois, il n'y avait rien à corriger.

Trois règles neuves :

- **562-A · UN COMPTEUR DE SITES N'EST PAS UN COMPTEUR DE VALEURS** — les
  corrections de marquage des 555-560 n'ont aucune prise sur un décompte
  d'appels ; le vérifier prend une minute, l'appliquer à tort fausse tout.
- **562-B · UN CORPUS QUI NE DÉDOUBLONNE PAS MULTIPLIE LES PARTAGÉS** — 12
  signatures dans du JS statique valent 96 unités sur 178.
- **562-C · UNE DETTE PEUT SE SOLDER SANS QU'UN CHIFFRE CHANGE** — 178 reste
  178 ; ce qui manquait n'était pas une correction, c'était une définition.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **SIX chiffres lourds encore NON RECOMPTÉS** — 112
atténuations (539), 103 états (541), 53 refus (542), 156 variables serveur
(540), 25 fonctions exécutées (537), 11 limites levées (538) ; **les 5 cas de
réponse absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10
cas non tranchés du 559** ; **les 16 sous-clés du 558, dont 12 sur des routes au
contrat non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ;
**les 35 clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans
lecture observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions
de nom** ; **les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ;
**les 14 candidates du 554, en attente d'un GO** ; **les 4 routes construites
`/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **les 95 atténuations non
affichées** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 188 (+1)** ; publiés
puis corrigés **30** ; interprétations retirées **6 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
