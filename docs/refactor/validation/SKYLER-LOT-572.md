# SKYLER LOT 572 — quand Vertex annonce un échec, dit-il pourquoi ? **Deux registres** : 2 toasts d'erreur sur 22 sont construits, mais **10 bannières sur 10 portent la cause réelle** — et lire le tableau seul aurait donné l'inverse de la vérité

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-572` (base : lot 571 fusionné,
`15e47548`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix

**(rr)** — le 571 a séparé le canal en **33 signalements d'échec** et 57 autres.
Le 570 avait appliqué la grille du 541 (construite / littérale / repli / absent)
**mais sur les 89 sites mélangés**, avant que le tri par ton n'existe. Le
croisement n'avait jamais été fait, et c'est la seule question de produit qui
compte : **un message d'échec explique-t-il davantage qu'une confirmation ?**

## Les dénominateurs, déclarés avant de remplir la moindre case (570-C)

```text
grille du 541   →  79 sites d'appel portant un argument de message
                   (`VX.toast` 55 + `emptyCard` 14 + `setNet` 5 + `setStatus` 5)
TON             →  55 sites (`VX.toast` seul)
bannière + marqueur → 11 sites, AUCUNE forme de message au sens du 541
plancher total  →  90
```

**Quatre dénominateurs pour un seul objet.** Le croisement n'en utilise qu'un :
**55**. Croiser sans les redéclarer aurait refait le « 156 sur 6 » du 566.

```text
CALIB 1 · REPRODUCTION  79 sites (55/14/5/5) · 10 bannières · 1 marqueur = 90
          · grille du 570 : 58 littérales / 18 construites / 1 repli / 2 absents   OK
CALIB 2 · POSITIF       le témoin lu dans le code —
          `VX.toast('Mise à jour impossible : '+e.message,'error')`
          tombe bien dans la case **construite × error**                          OK
CALIB 3 · NÉGATIF       aucune bannière ni marqueur ne porte de forme             OK
```

## Le croisement — dénominateur : les 55 `VX.toast`

```text
forme              error   success   autre ton   sans ton   total
construite             2        11           0          3      16
littérale             19        12           4          1      36
repli littéral         1         0           0          0       1
absent                 0         0           0          2       2
                     ───       ───         ───        ───     ───
TOTAL                 22        23           4          6      55
```

```text
longueur des littérales, par ton
error      19 littérales · min 2 · médiane 2 · max 7 · ≤ 3 mots : 13
success    12 littérales · min 1 · médiane 3 · max 5 · ≤ 3 mots :  9
autre ton   4 littérales · min 3 · médiane 6 · max 6 · ≤ 3 mots :  1
```

**L'asymétrie est mesurée : 11 confirmations sur 23 sont construites, contre 2
erreurs sur 22.** Quand Vertex confirme, il nomme souvent l'objet précis ; quand
il annonce un échec **par toast**, il rend le plus souvent une phrase fixe et
courte.

## L'arrêt du lot — **le tableau seul aurait dit l'inverse de la vérité**

La colonne `error` invite à conclure « les échecs n'expliquent pas ». **Les 11
sites que le tableau exclut par construction sont précisément ceux qui portent
la cause.** Mesuré :

```text
bannières `vx-error-banner` distinctes            10
   INTERPOLENT une valeur (cause réelle)          10
   texte fixe                                      0
```

Toutes, sans exception :

```javascript
'<div class="vx-error-banner">Radar injoignable : ' + esc(e.message)
'<div class="vx-error-banner">Scanner injoignable : ' + esc(e.message)
'<div class="vx-error-banner">Calibration injoignable : ' + esc(e.message)
'<div class="vx-error-banner">Mémoire injoignable : ' + esc(e.message)
'<div class="vx-error-banner">' + esc(d.error || 'réponse invalide')
`<div class="vx-error-banner vx-mt2">⚠ ${errs.map(e => esc(e.domain+' : '+e.error))}`
```

**Recomposé honnêtement : sur les 33 signalements d'échec, 12 portent la cause
réelle** — 2 toasts construits **et les 10 bannières**. Pas 2 sur 22.

J'avais écrit d'avance que les bannières seraient hors grille, et je l'ai
respecté. **Ce que je n'avais pas prévu, c'est que l'exclusion emporterait la
réponse.**

**Arrêtés avant publication : 197 → 198 (+1).**

## Ce que la mesure établit vraiment — **deux registres, pas un défaut**

- **La bannière est le registre long** : elle vit dans une carte, elle a la
  place, et elle interpole la cause **dix fois sur dix**.
- **Le toast est le registre court** : éphémère, superposé, il nomme l'échec
  sans le détailler — médiane de **deux mots**.
- **Les deux toasts construits sont dans des clauses `catch`** (`'Mise à jour
  impossible : ' + e.message`) : là où la cause existe vraiment, le toast la
  prend aussi.

Comparer la longueur d'un toast et celle d'une bannière **sans dire qu'ils
n'ont pas la même place** serait un jugement déguisé en mesure.

## Second contrôle (481) — ce que le croisement ne couvre pas

```text
toasts SANS ton (comptés, pas rangés)              6
   `${sym} retiré des favoris` · `${sym} retiré de la watchlist`
   `Suivi retiré sur ${sym}` · sym + ' copié' · t.sym + ' copié'
   'Entrée supprimée'
toasts à ton ternaire (comptés en `error`)         1
sites d'appel sans argument de ton                24
bannière + marqueur, hors grille                  11
                                                 ───
exclus du croisement par construction             35 sur 90
```

Les 6 toasts sans ton sont **tous des confirmations d'action utilisateur** —
lues, pas supposées. Le ton y est superflu : la phrase dit déjà ce qui s'est
passé.

## Ce que le dépôt fait bien, mesuré

- **Dix bannières sur dix portent la cause**, toutes échappées par `esc()`.
- **Le préfixe nomme le sous-système** : « Radar injoignable », « Scanner
  injoignable », « Calibration injoignable », « Mémoire injoignable » —
  l'utilisateur sait *quoi* est en panne avant de savoir *pourquoi*.
- **`d.error || 'réponse invalide'`** : même quand le serveur ne dit rien, la
  bannière a un repli honnête.
- **Aucune bannière à texte fixe** : le registre long ne se contente jamais
  d'une phrase toute faite.

## Portée — ce que ce lot NE dit PAS

- **Une littérale courte n'est pas une faute** — le 541 avait posé qu'on compte
  les mots, on ne note pas la qualité d'une phrase. « Régime indisponible » dit
  ce qui manque.
- **Un ton `'error'` prouve une intention de signalement**, pas qu'un échec réel
  a eu lieu.
- Les 24 `emptyCard`/`setNet`/`setStatus` **n'ont pas de ton** et restent hors
  du croisement.
- **Rien n'est corrigé, rien n'est unifié.**

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Quatrième lot sur le même objet, et le premier qui **répond à une
question de produit** plutôt qu'à une question de comptage : oui, Vertex dit
pourquoi — dans le registre qui en a la place.

Ce que je retiens : **j'ai construit une exclusion correcte, et elle a failli me
faire publier le contraire de la vérité.** Écarter les bannières de la grille du
541 était juste — une bannière n'est pas un argument. Mais un tableau ne dit rien
de ce qu'il exclut, et il ne prévient pas. Deux lignes de plus dans le rapport
auraient annoncé « 2 sur 22 » et laissé croire que le produit tait ses causes,
alors que dix bannières sur dix les portent.

Trois règles neuves :

- **572-A · UN TABLEAU CROISÉ EXCLUT, ET CE QU'IL EXCLUT PEUT PORTER LA
  RÉPONSE** — 11 sites hors grille, et ce sont les seuls à interpoler une cause,
  dix fois sur dix.
- **572-B · DEUX REGISTRES NE SE JUGENT PAS À LA MÊME AUNE** — un toast
  éphémère et une bannière dans une carte n'ont pas la même place ; comparer
  leur longueur sans le dire serait un jugement déguisé en mesure.
- **572-C · LE DÉNOMINATEUR SE DÉCLARE AVANT LA CASE** — 79, 55, 33, 90 :
  quatre dénominateurs pour un seul objet, et le tableau n'en emploie qu'un.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 19 toasts d'erreur littéraux, non jugés** ;
**les 6 toasts sans ton** ; **`warn` et `warning`, deux orthographes non
unifiées** ; **les 23 toasts `success`, non jugés** ; **les 57 sites du canal qui
ne signalent pas un échec** ; **le total réel des signalements d'échec, toujours
inconnu — deux bornes, aucun recensement** ; **les 27 appelés du relevé
structurel, non triés** ; **les 79 sites hors `catch`, comptés mais non lus** ;
**les 82 corps vides du 569, NON JUGÉS** ; **les 18 gardes portant un
`VX.fetch`** ; **les 63 `empty` distincts du 568** ; **les 42 refus du 567** ;
**les 4 refus non-JSON du 542** ; **les 74 variables serveur sans atténuation** ;
**les 67 atténuations non affichées** ; **les 25 atténuations de la bibliothèque
tierce** ; **`/options|chips`, douzième limite jamais levée ni nommée** ;
**`renderCalendar`, exécutée hors périmètre au 537** ; **les 4 limites distinctes
du 564** ; **les 12 signatures partagées du 562** ; **les 5 cas de réponse
absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10 cas non
tranchés du 559** ; **les 16 sous-clés du 558** ; **les 5 chaînes nues** ; **les
10 chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
candidates** ; **les 6 clés sans lecture observée** ; **les 26 routes à lectures
ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ;
**les 5 routes affamées du 556** ; **les 14 candidates du 554, en attente d'un
GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du
554/555** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly` rend un
objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 198 (+1)** ; publiés
puis corrigés **34** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
