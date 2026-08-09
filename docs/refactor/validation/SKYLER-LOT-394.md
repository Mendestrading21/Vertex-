# SKYLER LOT 394 — Les gardiens anciens, jamais rejoués : 7 sur 8 mordent encore

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-394` (base : lot 393 fusionné,
652f8da)

## Pourquoi une vérification et non une piste

Le lot 393 a constaté que les pistes fines sont épuisées. Plutôt que d'inventer
du travail, ce lot répond à une **question laissée ouverte par le bilan n°8** :

> *« Les gardiens non ciblés — la grande majorité — restent non vérifiés. »*

**Aucun gardien n'est ajouté.** Une seule correction, dans un fichier de test.

## Le dénominateur

```text
fichiers de test                        300
   estampillés d'un lot < 380           179   ← jamais rejoués
   sans numéro de lot                   111   ← jamais rejoués non plus
   tranche 380-393                       10   ← rejoués au lot 390
```

**290 sur 300 n'ont jamais été confrontés à une faute réelle.** Le bilan n°8
avait raison de le dire ; voici la mesure.

## L'échantillon, choisi par un critère et non au hasard

Rejouer 290 gardiens n'a pas de sens dans un lot. Le critère retenu : **ceux que
`CLAUDE.md` désigne nommément** comme protégeant ses règles critiques. Si l'un
d'eux a pourri, c'est une règle du produit qui n'est plus tenue.

```text
règle              faute rejouée                                    verdict
n°1 clés sync      clé retirée du fichier statique SERVI            NE MORD PLUS ⚠
n°1 clés sync      clé retirée de l'ancre de comparaison vx_kit     MORD
n°2 JS servi       JS servi rendu syntaxiquement invalide           MORD
n°3 service worker fichier /static modifié SANS bump d'empreinte    MORD
n°5 news assainies sanitize_news retiré de la sortie IBKR           MORD
n°5 sortie IA      filtre d'URL de la sortie IA neutralisé          MORD
n°6 filet desk     rotation des sauvegardes desk à 0                MORD
couleurs           bleu NON-MARQUE injecté dans un octet servi      MORD
[témoin]           commentaire reformulé, valeur inchangée          ne mord pas — correct
```

**7 sur 8.** Le témoin reste muet. État runtime après la passe : aucun écart.

## Le huitième — et ce qu'il révèle vraiment

`test_desk_sync_keys_single_source_of_truth` ne tombe pas quand on retire une clé
de `vertex/static/vertex/js/vx-entities.js`. **Ce n'est pas un gardien pourri** :
la lecture de son corps montre qu'il compare `vx_kit.JS` et `journal.JS`, et
**n'a jamais regardé le fichier statique**.

Le lot 381 avait déjà trouvé ce trou de couverture et l'avait comblé avec
`tests/test_desk_keys_servies_lot381.py`. Ce qu'il n'avait **pas** corrigé, c'est
la docstring de l'ancien gardien, qui affirmait :

> *« La source de vérité servie est vx_kit (kit global, présent sur toutes les
> pages) »*

**Cette phrase est fausse depuis le lot 381**, qui a mesuré que `vx_kit.JS`
(21 727 o) n'atteint **aucune** des 8 pages, et que `journal.py` est un module
mort. Un lecteur — humain ou agent — qui ouvre ce test pour comprendre la règle
n°1 y lisait donc le contraire de ce que le dépôt fait.

**Corrigé.** La docstring dit désormais ce que le test couvre réellement, ce
qu'il ne couvre pas, et renvoie au gardien du 381. Les deux sont complémentaires :
celui-ci verrouille l'**ancre de comparaison**, celui du 381 verrouille ce que
**le navigateur reçoit**. Fichier de test, aucune production touchée.

## Deux ancres fautives, corrigées avant de conclure

La règle n°3 a d'abord affiché « ancre absente » : j'avais visé `--vx-radius`,
qui n'existe pas dans `tokens.css`. Rejouée sur `--vx-canvas` (5 occurrences,
remplacement global pour que la faute soit réelle), elle **mord**. Sans cette
reprise, j'aurais compté 6/7 au lieu de 7/8 — et laissé croire à un trou sur le
service worker.

*Une ancre absente n'est pas un résultat : c'est une mesure qui n'a pas eu lieu.*

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de
  bump. La seule modification est une docstring de test.
- Copies de sûreté des 21 fichiers runtime, contrôle d'apparition inclus
  (leçon du 392) : écart final **aucun**.
- Suite : **2862 passed / 2 skipped**, **inchangée** — aucun test ajouté, et
  c'est délibéré.

## Portée

Huit gardiens sur 290 : c'est un **sondage**, pas une couverture. Le critère de
sélection le rend représentatif des *règles critiques*, pas de la suite entière.
Et « MORD » signifie « attrape CETTE faute-là » — un gardien peut mordre sur la
faute évidente et rater ses variantes.

Ce que ce lot établit précisément : **les gardiens des règles critiques de
`CLAUDE.md` n'ont pas pourri**, et le seul écart trouvé était une documentation
périmée, pas une protection perdue.

## Suite

Le constat du 393 tient : **aucune piste fine ne mérite un lot**. Cette
vérification-ci était bornée et ne se répète pas utilement à court terme — la
rejouer sur les 282 gardiens restants serait un programme, pas un lot, et son
rendement attendu est faible au vu de ce résultat.

La matière utile reste dans les **dossiers du rang 1**, en attente de décision —
à commencer par la purge des 7 points MSFT fabriqués (coût quasi nul, risque
nul).

Prochaine échéance périodique : bilan n°9 **~lot 400**.
