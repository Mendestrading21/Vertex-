# SKYLER LOT 437 — Le test de consommation ne se généralise pas (trois instruments, trois contrôles) — mais il a trouvé une carte qui se déclare fraîche « à l'instant », toujours

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-437` (base : lot 436 fusionné,
dc8767a)

Vingtième lot de la veine, **bornage du 436**. Le 436 avait mesuré que
`/api/command` sert dix champs dont le produit n'en lit que deux. Question :
**exception, ou motif d'architecture ?** Réponse partielle — et une trouvaille
inattendue en chemin.

**Aucun code, aucun gardien, aucun test.**

## Trois instruments, trois contrôles qui mordent

C'est l'histoire du lot, et elle vaut mieux que son résultat.

**Passe 1 — motif `\.champ\b` sur tout le corpus.** Résultat : 86 % des champs
lus sur sept routes, quatre routes à 100 %. Propre, aligné — et **faux**. Le
témoin positif l'a dit : sur `/api/command`, dont le 436 avait établi **2 lus sur
10**, la passe 1 annonçait **5 sur 10**. Cause : `.regime`, `.risk`, `.decision`
matchent **n'importe quel objet** du corpus, pas le payload.

**Passe 2 — n'accepter que `ident.champ`, où `ident` reçoit la réponse de cette
route.** Le témoin retombe juste : `/api/command` = **2/10**, exactement le 436.
Mais une ligne devient invraisemblable : `/api/positions/state` à **0/4**. Un
payload servi dont **aucun** champ ne serait lu ? *Un pool qui mord sur un objet
manifestement sain accuse l'instrument* (règle 414).

**Passe 3 — détecter les payloads transmis EN BLOC** (`f(posState)`), qui
échappent forcément à `ident.champ`. Elle a trouvé le vrai cas —
`actionListHtml(posState)` — **et une bouillie** : `Bo`, `Number`, `fillText`,
`_resolveTickFontOptions`… Cause : les identifiants receveurs d'une ou deux
lettres (`c`, `r`, `s`, `d`, `ed`) sont **indistinguables du Chart.js minifié**
présent dans le corpus.

## Ce que je peux conclure, et ce que je ne peux pas

```text
route                        lus/champs  receveur   verdict
/api/command                    2/10      cmd       CONCLUANT (paint lu à la main au 436)
/api/system/diagnostics         4/5       diag      CONCLUANT — mort : alerts
/cal-feed                       2/3       cal       CONCLUANT — mort : updated
/api/positions/state            0/4       posState  INCONCLUANT — payload passé à actionListHtml
/scan                          12/24      scan      BORNE BASSE — passé à crossAsset, idxByName,
                                                     loadBreadth, demoBanner…
/api/market/summary             9/18      s,r,ed    INUTILISABLE — receveurs d'une lettre
/api/market/regime              5/6       r,ed      INUTILISABLE
/api/skyler/sweep               5/6       d         INUTILISABLE
```

**Trois routes sur huit sont concluantes.** Sur ces trois, `/api/command` à
**20 %** se détache nettement de `/api/system/diagnostics` (**80 %**) et de
`/cal-feed` (**67 %**).

**Le 436 n'est donc pas généralisé — il est indiqué.** La méthode du 436 avait
marché parce que j'avais lu `paint` à la main ; elle ne se déploie pas à coût
constant. C'est un résultat de méthode, et il limite ce que la boucle peut
affirmer sur les autres routes.

## La trouvaille, sortie du bornage

`/cal-feed` sert trois champs : `items`, `macro`, **`updated`**. Le client, lui,
lit :

```javascript
// briefing.py, servi — et la même forme sur /markets et /opportunities
VXCharts.catalystRunway('vx-calendar', { …, timestamp: cal.ts || Date.now(), … })
```

**`cal.ts` n'existe pas.** Mesuré sur le payload réel : les clés servies sont
`items`, `macro`, `updated` — **jamais `ts`**. Le repli `|| Date.now()` s'applique
donc **toujours**.

Et `VX.updateIndicator` rend ce timestamp en clair :

```javascript
const parts = [VX.fmt.ago(ts)];      // vx-core.js, servi
```

**La carte « Catalyseurs imminents » annonce donc en permanence que ses données
datent de l'instant présent**, quel que soit l'âge réel du calendrier. Trois
pages la portent : `/`, `/markets`, `/opportunities`.

### Le contrat n'a jamais existé des deux côtés

Ce n'est pas un simple nom mal orthographié. Le champ que le serveur produit,
`cal_state['updated']`, est **une chaîne d'affichage** :

```python
cal_state['updated'] = datetime.now().strftime('%H:%M %d/%m')   # terminal.py:1200, :1220
```

Un `VX.fmt.ago()` ne saurait rien en faire. **Le serveur émet un libellé, le
client attend un horodatage, et personne n'a jamais rapproché les deux.** Le champ
`updated` est mort **parce que** le client cherche autre chose ; et ce qu'il
cherche n'existe pas.

## Classement

**Rang 1.** C'est une **affirmation de fraîcheur**, elle est affichée sur trois
pages, elle est **toujours fausse**, et elle penche du côté qui **rassure** — les
données paraissent plus fraîches qu'elles ne sont. C'est exactement le critère
posé au 431 : une étiquette conservatrice ne compte pas, une étiquette flatteuse
compte.

Correction pressentie : émettre côté serveur un horodatage exploitable à côté du
libellé, et le lire ; ou, à moindre coût, retirer le repli `|| Date.now()` pour
que l'absence se voie. **Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne mentionne `cal.ts` : **aucun gardien.**

## Portée

Cinq routes sur huit restent **non conclues**, et je ne les compte pas. Le taux
de 51 % rendu par la passe 2 sur l'ensemble est **une borne basse contaminée** par
ces cinq lignes : je ne le publie pas comme un chiffre.

Je n'ai **pas observé** la carte dans un navigateur : la chaîne est établie sur
les octets servis (`cal.ts` lu, payload sans `ts`, `ago(ts)` rendu). Le calendrier
au démarrage est vide, donc `updated` valait `None` lors de ma mesure — le
désaccord de contrat, lui, se lit sur le producteur, pas sur cet état.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Les huit routes ont été appelées en **GET** (lecture).
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Quarantième lot court. Séquence : **434 ✓ · 435 ~ · 436 ~ · 437 ✓**.

Après deux lots qui avaient dû **descendre** leur propre trouvaille faute de
consommateur, celui-ci en remonte une : une carte affichée sur trois pages qui
ment sur sa propre fraîcheur. Et il la trouve **par accident**, en cherchant à
généraliser une méthode qui, elle, ne se généralise pas.

Le compte des instruments fautifs monte à **sept en quatre lots** (430, 434 ×2,
435, 437 ×3). La différence, ici : les trois ont été **arrêtés par leurs propres
contrôles** — témoin positif, invraisemblance, lecture de la sortie — avant
d'entrer dans le rapport.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
