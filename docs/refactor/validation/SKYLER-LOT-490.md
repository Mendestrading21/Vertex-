# SKYLER LOT 490 — BILAN n°17 de la tranche 480-489 : le taux d'auto-correction N'A PAS monté, il a PLAFONNÉ — et la moitié de la tranche a mesuré la boucle, pas le produit

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-490` (base : lot 489 fusionné,
`aa8366b9`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**
Bilan fait **sur pièces** : les dix rapports relus, les chiffres vérifiés dans le
dépôt, **aucune trouvaille rejouée**. Seule mesure fraîche : les MD5.

## Calibration, écrite dans le code

Le bilan repose sur une série objective : le compteur « **publiés puis
corrigés** » que chaque rapport porte. Deux réponses connues d'avance, avec
sortie programmée en cas d'échec :

```text
487 (a corrigé le 486)  compteur = 10   attendu 10   OK
488 (n'a corrigé personne) compteur = 10   attendu 10   OK
```

## 1. Les chiffres de la tranche

```text
suite            2864 passed / 0 skipped — déclaré par les DIX rapports, jamais rouge
service worker   td-shell-v187 — sur les DIX
MD5 des 8 pages  8/8 à chaque lot, et remesuré 8/8 aujourd'hui
production       touchée ZÉRO fois (les dix rapports : « aucun fichier de production touché »)
gardiens         ZÉRO ajouté — aucun fichier tests/*lot48*, total inchangé à 301 fichiers
PR               dix, une par lot
```

**Rien n'a bougé dans le produit sur dix lots.** Ni un octet servi, ni un test,
ni une version de SW. C'est la discipline tenue — et c'est aussi le problème,
voir §4.

## 2. Le fil rouge — la tranche s'est corrigée trois fois. Est-ce une dérive ?

Le compteur donne les incréments **exacts**, lot par lot :

```text
469 (+1) · 471 (+1) · 477 (+1) · 479 (+1) · 481 (+1) · 485 (+1) · 487 (+1)

par tranche :   460-469 → 1      470-479 → 3      480-489 → 3
```

**Le taux n'a PAS monté entre les deux dernières tranches : il a plafonné à 3.**
Le saut réel a eu lieu **entre 460-469 et 470-479**, et il n'a pas continué.

**Ce que la mesure confirme du 480.** Ce lot avait tranché une question voisine
en disant que les révisions se groupent dans les lots dont le travail est la
**ré-examination** d'un dossier ancien. Vérifié ici : les trois auto-corrections
de la tranche sont **481** (ré-examen du 480), **485** (ré-examen du 484) et
**487** (ré-examen du 486). **Les trois, sans exception.** La thèse du
« changement de tâche » tient avec dix lots de plus.

**Ce que je ne maquille pas** : 3 sur 10, c'est **30 % des lots qui corrigent un
prédécesseur**, contre 10 % à la tranche 460-469. Le plateau est réel, mais il
est **haut**. Un tiers des lots publie quelque chose qu'un lot suivant devra
reprendre — et les trois corrections portaient sur des **chiffres publiés**
(6 orphelins → 1 · plafond 35 → 29 · rang 2 → rang 1), pas sur des détails.

## 3. Le rendement réel, dit franchement

```text
lots qui mesurent LA BOUCLE      480 · 481 · 482 · 483 · 488     = 5
lots qui mesurent LE PRODUIT     484 · 485 · 486 · 487 · 489     = 5
```

**La moitié de la tranche a mesuré la boucle elle-même.** Et sur les cinq lots
« produit », **deux seulement ont trouvé du neuf** — le 484 et le 486. Les trois
autres (485, 487, 489) **vérifient ou corrigent ces deux trouvailles**.

Défauts produit réellement ajoutés : **484-A** (rang 1, S et S+ inatteignables),
**484-B** (rang 2, « /40 » plafonné à 29), **486-A** (rang 1 après le 487, barre
de poids toujours verte). **Trois.**

**Dix lots pour trois défauts neufs.** C'est le chiffre, sans habillage.

À sa décharge : les trois sont **substantiels** — deux rangs 1 dont l'un touche
la carte de décision de `/analysis`, et les cinq lots de vérification ont
**empêché trois publications fausses de survivre**. Une trouvaille non vérifiée
n'a pas la même valeur qu'une trouvaille exécutée au navigateur.

## 4. Ce que la tranche a coûté — la question que je pose sans y répondre

```text
corrections engagées          0
gardiens ajoutés              0
octets servis modifiés        0
feuille de décision      20 → 24 dossiers   (+4)
dettes ouvertes          à chiffrer 6 · arbitrages humains 7 ·
                         observations non classées 5 · barèmes non tracés 7 ·
                         rangs relatifs non re-vérifiés 8
```

**La boucle produit des dossiers plus vite qu'elle n'en solde**, et elle ne peut
en solder aucun sans GO. Dix lots ont ajouté quatre entrées à une liste que
personne ne consomme.

**Est-ce soutenable ?** Je pose la question et **je ne réponds pas à la place de
l'utilisateur**. Ce que je peux dire : la valeur produite est **réelle et
mesurée** (deux rangs 1 documentés, reproductibles, avec bancs et preuves
navigateur), mais elle est **entièrement immobilisée**. Le stock ne devient utile
qu'au moment d'une décision.

## 5. Le second contrôle — les chiffres du RÉVEIL, que le bilan exclurait

Un bilan lit les rapports. **Il ne vérifie pas son propre brief** — et les
réveils se sont déjà trompés (480, 482). Deux chiffres du réveil passés à la
mesure :

**(a) « la feuille a grossi de 2 dossiers » → FAUX.** Mesuré sur les lignes
d'index : **20** (480, 481, 482) → **21** (483) → **23** (484) → **24** (486,
487, 488, 489). **+4, pas +2.** Le « +2 » est le chiffre du **484 seul**.

**(b) « PR #513 → #521 » → INCOMPLET.** Neuf numéros pour dix lots. Vérifié sur
pièces dans `git log` : 482→#514, 483→#515, 484→#516, 485→#517, 486→#518,
487→#519, 488→#520, 489→#521. Les deux premiers (#512 pour le 480, #513 pour le
481) viennent du registre antérieur et **je ne les ai PAS re-vérifiés** — ils
précèdent la fenêtre de journal que j'ai lue. La tranche est donc **#512 → #521**
sous cette réserve.

**Troisième réveil consécutif porteur d'une erreur factuelle** (480, 482, 490).
Ce n'est plus un accident : **le brief est une source comme une autre, et il doit
être vérifié comme telle.**

## Un défaut de mon propre instrument, attrapé en lisant sa sortie

Mon premier détecteur cherchait « N dossiers » **dans les rapports** : il rendait
« absent » pour les lots 483 à 489. La taille de la feuille est déclarée **dans
les lignes d'index**, pas dans le corps des rapports. Corrigé, la série sort
proprement. **Arrêtés avant publication : 54 → 55.**

## Portée

- **Aucune trouvaille rejouée.** Les verdicts des dix lots sont **cités**, pas
  re-mesurés. Ce bilan établit ce que la tranche **dit avoir fait**, plus les
  chiffres transverses que j'ai vérifiés au dépôt.
- La série d'auto-corrections repose sur **un compteur que j'incrémente
  moi-même**. Il est fidèle si je l'ai toujours incrémenté à bon escient — **je
  n'ai pas audité chacune des sept occurrences**, seulement vérifié deux réponses
  connues en calibration.
- Le classement « lot boucle » / « lot produit » est **mon jugement**, pas une
  mesure : le 482 se présente comme un « retour au produit » alors que son objet
  était ma propre liste — **je l'ai compté côté boucle, et un autre lecteur
  pourrait en décider autrement**.
- **#512 et #513 non re-vérifiés** (voir §5b).
- Les MD5 sont la seule mesure fraîche.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert`, `os.chdir` **et sorties en chemin ABSOLU** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; écart final **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où va la boucle

La tranche 470-479 avait produit un devis. La tranche 480-489 a produit **trois
défauts et une méthode** — et la méthode est devenue son objet principal : cinq
lots sur dix. Les règles accumulées (critère absolu, deux contrôles, co-visibilité
sur la même vue puis la même carte puis à la bonne distance) sont **bonnes**, et
elles ont toutes été payées par une erreur réelle.

Mais une boucle qui passe la moitié de son temps à s'auditer, qui ne peut rien
corriger, et dont la liste de dossiers ne cesse de croître, **a atteint la limite
de ce qu'elle peut apporter seule**. Ce n'est pas un constat d'échec : c'est le
constat qu'il manque une décision.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
