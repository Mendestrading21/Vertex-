# SKYLER LOT 505 — `/journal?view=progression`, sous-vue jamais auditée : sous la question « Mes erreurs récurrentes diminuent-elles ? », la page écrit « la discipline progresse » sur une série STRICTEMENT PLATE — et « Vigilance » après DIX MOIS SANS UNE SEULE ERREUR. Ce n'est pas une tendance, c'est une comparaison de deux bornes sur une série amputée

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-505` (base : lot 504 fusionné,
`d01e428d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)** — les sous-vues jamais auditées de `/journal`, que le 504 avait
signalées comme **servies mais absentes de toute empreinte MD5 de la boucle**.
Le 504 désignait `progression` comme « un candidat évident ». Il avait raison.

## Sous-produit immédiat : les quatre empreintes qui manquaient

La boucle n'avait d'empreinte que pour la vue par défaut. Les cinq, mesurées :

```text
?view=overview       55 492 o   243699ace2d5   (la référence connue)
?view=journal        53 493 o   87b254ef362f   ← jamais empreinte
?view=learnings      53 682 o   6a7e51204b30   ← jamais empreinte
?view=progression    52 957 o   3c02ad9be276   ← jamais empreinte
?view=track-record   53 755 o   d9d406cc9135   ← jamais empreinte
```

## La phrase mise en cause

Sous un graphique intitulé « Erreurs déclarées par mois » et sous la question
« Mes erreurs récurrentes diminuent-elles ? », la page écrit une conclusion :

```js
conclusion: byMonth[months[months.length-1]] <= byMonth[months[0]]
            ? 'Tendance à la baisse — la discipline progresse.'
            : 'Vigilance : les erreurs ne diminuent pas encore.'
```

**Ce n'est pas une tendance.** Seuls le premier et le dernier mois sont
comparés ; et le test est `<=`, donc l'égalité est annoncée comme un progrès.

## La réponse

```text
forme de la série d'erreurs             la page écrit    vérité       verdict
TÉMOIN + décroissante franche 10→8→1    progresse        progresse    conforme
TÉMOIN − croissante franche  1→4→10     Vigilance        Vigilance    conforme
PLATE            5 → 5 → 5              progresse        Vigilance    ** FAUX **
V INVERSÉ        2 → 20 → 2             progresse        Vigilance    ** FAUX **
CREUX PUIS PIC   9 → 1 → 9              progresse        Vigilance    ** FAUX **
PIC PUIS CHUTE   1 → 20 → 2             Vigilance        progresse    ** FAUX **
DEUX MOIS ÉGAUX  3 → 3                  progresse        Vigilance    ** FAUX **
```

**Cinq formes sur sept.** Et — règle 504 appliquée d'avance — **le défaut n'est
pas orienté** : la ligne « 1 → 20 → 2 » montre une amélioration massive depuis
le pic, et la page répond « Vigilance ».

Sur une série **monotone**, en revanche, la phrase est **juste**. Les deux
témoins le montrent, et mon dossier ne l'accuse pas là.

## Le second contrôle — et c'est lui qui trouve le pire

Mon premier banc ne faisait varier que des mois **qui ont tous une erreur**. Il
excluait donc le soupçon le plus grave, celui du dénominateur temporel :
`byMonth` n'est incrémenté **que si `e.mistake` est non vide**, donc **un mois
sans erreur n'existe pas dans la série**.

```text
A1 · 3 erreurs en janvier · DIX MOIS PARFAITS (200 décisions, zéro erreur) · 3 en décembre
     206 décisions au journal, 12 mois d'activité
     MOIS SUR L'AXE : ['2026-01', '2026-12']   →  DEUX sur DOUZE
     valeurs        : [3, 3]
     la page écrit  : « Tendance à la baisse — la discipline progresse. »

A2 · 5 erreurs en janvier · LES MÊMES DIX MOIS PARFAITS · 6 en décembre
     MOIS SUR L'AXE : ['2026-01', '2026-12']
     valeurs        : [5, 6]
     la page écrit  : « Vigilance : les erreurs ne diminuent pas encore. »
```

**Dix mois sans une seule erreur, deux cents décisions propres, sont absents de
la série qui prétend mesurer si les erreurs diminuent.** Exactement les mois qui
prouveraient la discipline. Et là encore l'effet joue dans les deux sens : A1
flatte, A2 accuse.

### Ce que le contrôle a fait RETIRER de mon brouillon

J'allais écrire que **l'axe du graphique masque les trous** — deux barres
voisines pour janvier et décembre. **Le contrôle dit que c'est atténué** : les
étiquettes passées à `VXCharts.bars` sont bien `['2026-01', '2026-12']`, donc le
trou est **nommé**. Un lecteur attentif du graphique peut voir qu'il n'y a que
deux mois. Je retire l'accusation sur l'axe et je ne garde que la phrase.

**Arrêtés avant publication : 82 → 83.**

### Et un point où la page a RAISON, qu'il faut dire

Avec **moins de deux mois** portant une erreur, `loadProgression()` **ne rend
aucun verdict** : `VXCharts.card` n'est pas appelée (mesuré : `card=False`), et
la page affiche à la place « La courbe de progression apparaîtra avec au moins
deux mois de décisions datées. […] Aucune progression fabriquée avant d'avoir
des faits. » **C'est honnête, c'est mesuré, et ça mérite d'être écrit.**

## « Servi mais jamais pris » — écarté par la mesure

`loadProgression()` est extraite des **octets servis** par
`?view=progression` (1 989 caractères) et exécutée telle quelle sous node.
`chart-core.js` et `chart.umd.min.js` sont bien chargés par la page, donc la
condition `months.length>=2 && window.VXCharts && VXCharts.card` est
franchissable. Mesuré avec un DOM bouchonné : `VXCharts.card` est appelée sur
l'hôte `vx-pf-prog-chart`, et **857 caractères sont écrits dans
`#vx-pf-prog`**. La phrase atteint l'écran.

## Aucun gardien

```text
tests/test_journal_system_07.py:53-59   « la vue existe, la fonction existe »
tests/test_journal_system_07.py:61-67   « la route rend 200 »
```

Trois assertions nomment `progression` ; **aucune ne touche à ce que la phrase
affirme**. Elles passeraient à l'identique si la conclusion était tirée à pile
ou face. Encore la règle de la veine : **matcher un MOT n'est pas matcher la
CHOSE.**

## DOSSIER 505-A — Classement

**Rang 2, et je dis pourquoi ce n'est pas rang 1.**

Ce qui plaiderait pour le rang 1 : la phrase est une **affirmation éditoriale
explicite sur le progrès de l'utilisateur**, elle est fausse dans cinq formes
sur sept **et dans les deux sens**, elle repose sur une série dont on a retiré
les mois vertueux, et **aucun gardien** ne la couvre.

Ce qui l'en empêche, et je le retiens :

1. **Ce n'est pas la vue par défaut.** Il faut cliquer « Progression ». Le
   504-A, lui, est peint dès l'ouverture de `/journal`.
2. **L'utilisateur n'est pas laissé sans signal** — motif du 461. Le graphique
   est affiché **à côté** de la phrase, avec les étiquettes de mois réelles et
   les valeurs : un lecteur attentif voit deux barres nommées janvier et
   décembre et peut corriger de lui-même.
3. **La page s'abstient honnêtement** quand les faits manquent (contrôle D).

Correction pressentie, et je ne l'engage pas : compter les mois **avec zéro
erreur** dans la série plutôt que de les omettre ; comparer une **pente** (ou
deux moyennes de fenêtres) plutôt que deux bornes ; réserver « progresse » à une
baisse **stricte** ; et se taire quand le nombre de mois est trop faible pour
conclure — ce que la page sait déjà faire. **Aucun GO, rien n'est engagé.**

## Portée — ce que ce lot NE dit PAS

- **`desk_data.json` n'a pas été ouvert.** Les journaux sont **fabriqués en
  mémoire**. Je montre que le code **produit** ces verdicts sur ces formes, pas
  la fréquence des formes chez l'utilisateur.
- La « vérité » de chaque ligne est **mon jugement** sur ce qu'une phrase
  honnête devrait dire. Les deux témoins monotones fixent les bornes où ce
  jugement n'est pas discutable ; les cinq autres le sont moins, et je préfère
  le dire que le masquer. **Le cas le moins discutable est A1 : dix mois sans
  erreur absents de la série.**
- **Aucun navigateur ouvert.** Le rendu est mesuré par exécution de la fonction
  servie sur un DOM bouchonné.
- **Les trois autres sous-vues restent non auditées** (`journal`, `learnings`,
  `track-record`) — leurs empreintes sont désormais prises, leur contenu non.
- `track-record` appelle `/api/track-record` et `/api/skyler/calibration` :
  **non exploré ici.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu** (incident 487).
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import de `terminal`, dans les
  deux scripts. Seuls des `GET /journal?view=…` ont été appelés — des lectures ;
  aucune route réseau sortante.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Deuxième lot d'affilée dans le produit, deuxième dossier. La veine des surfaces
jamais regardées continue de rendre — et elle rend **plus vite** que l'audit des
moteurs.

Ce que je retiens : **c'est encore le second contrôle qui a trouvé le pire.** Le
premier banc mesurait la formule ; il ne pouvait pas voir que la série
elle-même est amputée, parce que toutes mes formes avaient une erreur chaque
mois. La règle 481 ne sert pas seulement à se prémunir contre un faux positif —
**au 504 comme au 505, elle a produit le résultat principal.**

Et le même contrôle m'a fait **retirer** une accusation sur l'axe du graphique :
les étiquettes nomment les mois. Un lot honnête retire autant qu'il ajoute.

Feuille : **28 dossiers · seize rang 1 · dix rang 2 · trois rang 3**.
Dettes nommées restantes : **`/markets`, `/options`, `/system`** (jamais
auditées) ; **les trois autres sous-vues de `/journal`** ; **l'espion au
troisième niveau** (toujours déconseillé) ; **le compte des rangs relatifs sur
les lots postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 83 (+1)** ; publiés
puis corrigés **12** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
