# SKYLER LOT 447 — « Max pain à J-3 de la plus proche échéance » : l'aimant annoncé est celui de TOUTES les échéances mélangées, et la phrase s'affiche en clair sur le portefeuille

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-447` (base : lot 446 fusionné,
afae073)

Vingt-neuvième lot de la veine. Le 444 avait cartographié les phrases composées
au serveur ; le 446 avait montré que **le rang dépend d'abord de l'affichage**. Ce
lot va donc droit aux phrases **les plus vues** : les champs lus par **quatre
écrans**.

**Aucun code, aucun gardien, aucun test.**

## L'affichage d'abord — la leçon du 446 appliquée dès le début

Trois des sept phrases composées du champ `detail` viennent de
`positions_api.py:202/213/219`, servies par `/api/positions/alerts`.

```text
/api/positions/alerts cité par            /portfolio  (1 fois)
portfolio_page.py:484   ((alerts&&alerts.gamma)||[]).forEach(g => survRows.push({…, txt: g.detail}))
portfolio_page.py:488   <li><span class="vx-ticker">…</span> — ${esc(r.txt||'')}</li>
```

**Lecture de champ confirmée** (`.detail`, pas un jeton nu — leçon 444/446), et
le rendu est du **texte visible** dans la carte « Surveillance — N signal(aux) sur
tes positions », pas une infobulle.

C'est la **première fois de cette veine** que je trouve des phrases écrites par le
serveur **affichées en clair**. Tout défaut ici est donc un candidat rang 1.

## Deux phrases sur trois : l'inégalité imprimée EST la garde

```python
if pw is not None and spot < pw:
    'Spot sous le mur put (%s < %s) — le support de positionnement a cédé.' % (spot, pw)
if zg is not None and spot < zg:
    'Spot sous la bascule zero-gamma (%s < %s) — les dealers amplifient…' % (spot, zg)
```

La comparaison affichée est **littéralement la condition testée**, avec les mêmes
deux variables. **Je le dis comme une lecture, pas comme une mesure** — il n'y a
rien à exécuter : les deux expressions sont sur la même ligne.

## La troisième, mesurée : l'aimant n'est pas celui de l'échéance nommée

```python
'Spot collé au max pain (%s ~ %s) à J-%d de la plus proche échéance —
 risque d\'épinglage (pinning) vers ce niveau.' % (spot, mp, int(min(dtes)))
```

`mp` vient de `gex.max_pain(contracts)`. Et `max_pain` — lu ligne à ligne —
parcourt **tous** les contrats, ne garde que `(strike, oi, is_call)`, et **ne
filtre ni ne groupe jamais par échéance**. Sa propre docstring parle pourtant de
« l'**aimant d'expiration** », au singulier.

**Banc sur la fonction réelle**, cas sain et cas dégradé côte à côte :

```text
A. CAS SAIN — une seule échéance sur le board
   max_pain(J-3 seule)        100.0
   max_pain(tout le board)    100.0        → ACCORD          ← témoin positif

B. CAS RÉEL — deux échéances, aimants différents
   max_pain(J-3 seule, « la plus proche échéance »)   100.0
   max_pain(TOUT le board, ce que le code calcule)    130.0
   écart                                               30 points

C. LA PHRASE RENDUE, spot 129,0 — condition « collé » : 0,78 % ≤ 1,5 % → vraie
   « Spot collé au max pain (129.0 ~ 130.0) à J-3 de la plus proche échéance
     — risque d'épinglage (pinning) vers ce niveau. »

   l'aimant annoncé (130,0) est celui de TOUTES les échéances ;
   celui de l'échéance J-3 citée vaut 100,0.
```

**La phrase nomme une échéance et lui attribue une statistique qui n'est pas la
sienne.**

### Ce n'est pas un cas de bord : le board est multi-échéances par conception

`options_lab.py:81` isole les LEAPS par `dte >= 300` ; `terminal.py:3770` range
les contrats en **buckets « court / moyen / long »**. Un même symbole porte
plusieurs échéances sur le board — c'est le fonctionnement prévu, pas une
anomalie. La condition de déclenchement (`min(dtes) <= 7`) exige justement une
échéance proche **pendant que le board en contient de lointaines**.

## Classement

**Rang 1.** La phrase est **affichée en texte visible** sur `/portfolio`, elle
porte sur les **positions réelles** de l'utilisateur, et elle **attribue à une
échéance nommée un chiffre calculé sur toutes les autres**. Un trader qui lit
« max pain 130 à J-3 » en déduit une force d'épinglage à trois jours qui, sur
cette échéance, n'existe pas.

Correction pressentie : filtrer les contrats sur l'échéance la plus proche avant
d'appeler `max_pain`, **ou** retirer l'attribution d'échéance de la phrase. Le
premier geste est le bon — c'est aussi ce que la docstring de `max_pain` promet
déjà. **Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne compare le max pain global à celui d'une échéance :
**aucun gardien.**

## Un détail relevé, non classé

`int(min(dtes))` **tronque** : une échéance à 6,9 jours s'affiche « J-6 ». C'est
une imprécision d'un jour au plus, dans le sens qui **rapproche** l'échéance. Je
le note et **je ne le classe pas** — la troncature d'un DTE fractionnaire n'est
pas une affirmation fausse.

## Portée

Le banc appelle la **fonction réelle** `gex.max_pain` sur un board **fabriqué** :
il établit que la fonction mélange les échéances, **pas la fréquence des cas où
les deux aimants divergent** sur un board réel. Le board est vide au démarrage et
je ne l'ai pas peuplé.

**Je n'ai pas observé la carte dans un navigateur** : la chaîne est établie sur
les octets servis (`g.detail` lu, rendu en `<li>`) et sur le code du producteur.

Les deux autres phrases de `_gamma_events` sont vérifiées **par lecture**, pas par
exécution — et je le dis plutôt que de gonfler le compte.

**Trois phrases ouvertes sur les 19** que portent les quatre champs à quatre
écrans (`reason` 7, `detail` 7, `source` 4, `narrative` 1) ; `reason`, `source` et
`narrative` **ne sont pas ouverts**. Sur les 110 phrases concluantes du 444,
**100 restent fermées**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `gex.max_pain` est une fonction pure appelée en mémoire ;
  routes en **GET** ; `persist` redirigé vers un répertoire temporaire.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquantième lot court. Séquence : **444 ✗ (correction) · 445 ✗ (famille saine) ·
446 ~ (nuance) · 447 ✓ rang 1**.

Trois lots sans défaut affiché, puis celui-ci — et il arrive exactement là où le
446 avait dit d'aller : **sur les phrases que quatre écrans lisent**. Le tri par
affichage, décidé après coup au 446, a produit une trouvaille au premier essai.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **20** ;
**publiés puis corrigés** **1**.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
