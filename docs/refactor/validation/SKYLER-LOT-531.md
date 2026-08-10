# SKYLER LOT 531 — **531-A, rang 3 : deux vues d'Opportunités laissent un squelette de chargement PERPÉTUEL si la requête échoue.** Premier dossier visible depuis le 514. Et trois arrêts, dont un harnais qui rendait 39 caractères

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-531` (base : lot 530 fusionné,
`f3ecb613`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(p)** — fermer la moitié restante du 530 : il avait établi que les 35 vues
**servent** du texte réel, sans jamais exécuter l'**hydratation**. Règle
**517-C**.

## La carte vue → chargeurs, et ce qu'elle ne couvre pas

Le mécanisme de répartition **n'est pas uniforme** (mesuré au 530) :

```text
/markets · /journal · /system        chaînes `if(VIEW==='slug'){…}`
/opportunities · /portfolio          table `const RENDER={slug:fn,…}`
/options                             dispatch par `data-page-label` DANS UNE
                                     CLÔTURE — illisible par un crible simple
```

**Les 9 vues d'`/options` ne sont donc PAS couvertes, et je le dis** au lieu de
conclure qu'elles ne peignent pas (**523-B**).

```text
CALIB 1 · COUVERTURE   26 vues reçoivent des chargeurs                    OK
CALIB 2 · POSITIF      /system?view=automations → `loadAutomations`       OK
CALIB 3 · NÉGATIF      une vue FABRIQUÉE → aucun chargeur                 OK
CALIB 4 · VARIÉTÉ      24 listes distinctes sur 26                        OK
CALIB 5 · PEINTURE     le témoin écrit 1 940 caractères                   OK
```

Deux vues n'ont **aucun** chargeur : `/system?view=archive` et `?view=settings`
— elles sont **entièrement servies par le serveur**, ce que le 530 confirme
(`settings` est la vue la plus fournie, 1 643 caractères).

## Trois arrêts avant publication — le premier a failli faire publier n'importe quoi

**1. Le harnais rendait 39 caractères.** Je l'extrayais de
`l524_balayage.py` — qui ne le **définit pas**, il l'**extrait** lui-même de
`l523_balayage.py`. Résultat : **les 24 vues ressortaient MUETTES**, témoin
positif compris. J'allais publier « aucune vue ne peint ».

**2. Mon témoin ne portait pas sur la bonne étape.** Il calibrait la **carte**,
pas la **peinture** — l'exécution était cassée et **rien ne l'a arrêté**. J'ai
ajouté un **témoin de peinture** exécuté avant le balayage. Premier jet du
témoin : un tir unique **sans résolution des voisines**, qui échouait sur
« `esc is not defined` » et faisait croire que le harnais ne peignait rien. Une
**seule routine d'exécution** sert désormais au témoin et au balayage.

**3. « Deux vues ne peignent rien » était faux.** `/opportunities?view=options`
et `?view=stocks` rendent **`PARAMS is not defined`** — la limite **exacte** du
résolveur, nommée au 524 : `const VIEW=…;const PARAMS=…;` sur une seule ligne,
et mon motif exige un début de ligne. **Ce ne sont pas des vues muettes, c'est
mon instrument qui ne les atteint pas.**

**Arrêtés avant publication : 134 → 137.**

## Ce que les 22 vues mesurables peignent

```text
page             vue             riche     vide    échec
/journal         overview          851      851      601
/journal         track-record      367      321      192
/markets         macro             432      432      241
/markets         overview          627      627      627
/portfolio       risk              853      846      125
/system          automations       657      217      158
/system          connections       980      980      770
/opportunities   radar           1 526      143        0   ←
/opportunities   anomalies         122      122        0   ←
```

**Vingt-deux vues sur vingt-deux peignent quelque chose** en régime nominal.
Beaucoup peignent **la même chose sous les trois régimes** — elles lisent des
données **locales** (poste, `localStorage`), pas le réseau : c'est normal.

## 531-A — deux vues laissent un squelette PERPÉTUEL

**Deux vues peignent ZÉRO caractère quand la requête échoue.**

```text
/opportunities?view=radar        1 526 → 143 → 0
/opportunities?view=anomalies      122 → 122 → 0
```

Vérifié dans le code, chargeur par chargeur :

```text
renderRadar        AUCUN try · AUCUN catch
renderStocks       AUCUN try · AUCUN catch
renderAnomalies    AUCUN try
renderOptions      try · catch
renderCalendar     try · catch      → peint encore 50 caractères en échec
```

`renderRadar` commence par `const scan = await VX.fetch('/scan', …)`. **`VX.fetch`
LÈVE** en cas d'échec (établi au 520 : `throw new Error('HTTP ' + r.status)` puis
`throw lastErr`, après deux tentatives). L'exception n'est pas rattrapée, la
fonction s'interrompt, **et rien n'est écrit**.

Or le conteneur `op-body` est servi avec un squelette :

```text
<div class="vx-skeleton" style="height:120px"></div>
```

**Conséquence visible : l'utilisateur voit une barre de chargement qui ne
s'arrêtera jamais.** Le reste du produit fait l'inverse — `/system?view=automations`
affiche « Registre indisponible : HTTP 500 », et `/opportunities?view=calendar`,
qui a son `try/catch`, peint encore quelque chose.

### Classement — 531-A, rang 3

**Aucun chiffre faux n'est affiché** : c'est ce qui l'empêche d'être rang 2.
**Mais quelque chose de faux EST montré** — un **état de chargement en cours**
pour une donnée qui n'arrivera jamais : c'est ce qui l'empêche d'être rang 4,
où « rien de faux n'est montré » est le motif constant.

Ce qui le borne : il faut une **panne de la requête** pour l'atteindre, et le
produit **retente deux fois** avant de lever. En marche normale, la vue peint
1 526 caractères.

**Correction pressentie, non engagée** : entourer `renderRadar`,
`renderStocks` et `renderAnomalies` du même `try/catch` que leurs deux voisines,
et peindre `VX.states.error(...)`. **Aucun GO, rien n'est engagé.**

## Ce que le dépôt fait bien, mesuré

- **Vingt-deux vues sur vingt-deux peignent** en régime nominal ; aucune n'est
  inerte.
- **Trois vues sur cinq d'`/opportunities` ont déjà leur `try/catch`** — le bon
  motif existe **dans le même fichier**, à quelques lignes des trois qui ne
  l'ont pas.
- **La dégradation est graduelle et honnête là où elle est gérée** :
  `/system?view=automations` passe de 657 à 217 puis 158 caractères, en
  expliquant à chaque étage ; `/portfolio?view=risk` de 853 à 125.
- **Deux vues sans aucun chargeur sont entièrement servies par le serveur** —
  elles ne peuvent pas se vider.

## Portée — ce que ce lot NE dit PAS

- **Les 9 vues d'`/options` ne sont pas mesurées** : leur dispatch vit dans une
  clôture.
- **Deux vues d'`/opportunities` échappent au résolveur** (`PARAMS`), limite
  connue et non levée.
- Le régime d'échec simulé est **une levée de `VX.fetch`** ; une panne partielle
  (réponse tronquée, JSON invalide) n'est pas couverte.
- Les charges sont **fabriquées** ; les volumes peints ne valent pas pour les
  données réelles.
- **Aucun navigateur** : les stubs ne sont pas un DOM. **Aucun réseau** —
  `VX.fetch` stubé, `globalThis.fetch` lève « RESEAU INTERDIT ».
- **Aucune correction engagée.**

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
0, 3**.

**Premier dossier depuis le lot 514, et le premier VISIBLE depuis bien plus
longtemps.** Trois lots de retour au produit auront donné : quatre chiffres
vérifiés, une surface servie qui tient, et enfin un défaut réel — trouvé
exactement là où le 530 avait dit qu'il fallait regarder.

Trois règles neuves :

- **531-A · UN TÉMOIN DOIT PORTER SUR LA DERNIÈRE ÉTAPE, PAS LA PREMIÈRE** —
  calibrer la carte n'a pas empêché l'exécution d'être cassée.
- **531-B · UN OUTIL QUI EN EXTRAIT UN AUTRE N'EST PAS SA SOURCE** — 39
  caractères de harnais, 24 vues faussement muettes.
- **531-C · UNE LIMITE CONNUE DE L'INSTRUMENT DOIT ÊTRE RECHERCHÉE AVANT D'ÊTRE
  RÉINTERPRÉTÉE** — `PARAMS` était nommé au 524 ; je l'ai repris pour un défaut
  produit.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A**. Rangs 4 : 511-A, 512-A, 513-A, 518-A, 519-A.

Dettes nommées restantes : **les 9 vues d'`/options`, non mesurées** ; **les 2
vues bloquées par `PARAMS`** ; **la définition du corpus de routes du 511-A** ;
**l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs
fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 137 (+3)** ; publiés
puis corrigés **20** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
