# SKYLER LOT 425 — « 4 maturités réelles » : le compte est écrit en dur, la courbe se trace dès 2 points

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-425` (base : lot 424 fusionné,
05e6b60)

Neuvième lot dans la veine des moteurs, et le premier mené **dans l'autre
sens** : partir d'une phrase **réellement rendue**, puis remonter jusqu'au code
qui la produit. C'était la consigne, après trois lots dont la conséquence
s'arrêtait avant l'écran.

**Aucun code, aucun gardien, aucun test.**

## Le point de départ : les affirmations que le produit affiche vraiment

Les 8 pages et leurs scripts demandés au serveur (méthode du 413), puis
extraction des **affirmations littérales** que les cartes rendent — champs
`limits:` et `conclusion:` :

```text
affirmations littérales rendues : 17
   « 4 maturités réelles (3M/5A/10A/30A) »
   « σ = spot · IV_ATM · √(DTE/365) — estimation lognormale »
   « moyenne des % par trade — pas une performance composée »
   « historique breadth de l'univers scanné (partiel, pas tout le NYSE) »
   …
```

La première est une **affirmation de compte** — vérifiable, contrairement à une
formule ou à une convention. C'est celle-là qui a été ouverte.

## Ce qui est affiché — prouvé sur les octets servis

```text
vue           panneau statique « 4 maturités réelles » dans le MARQUAGE   chaîne limits servie
overview                       non                                              oui
macro                          OUI                                              oui
sectors                        non                                              oui
breadth                        non                                              oui
volatility                     non                                              oui
```

Sur `/markets?view=macro`, le **marquage servi** (hors `<script>`) contient :

> *« Courbe tracée sur les **4 maturités réelles** du scan (3M · 5A · 10A · 30A).
> Les maturités intermédiaires (2A/7A/20A) ne sont pas fournies par les moteurs —
> **non affichées plutôt qu'inventées**. »*

Et sur **les cinq vues**, la carte porte `limits:'4 maturités réelles
(3M/5A/10A/30A)'`. **Les deux sont des chaînes fixes : aucune n'est
conditionnelle.**

## Ce que le code fait réellement

Côté client, `markets_page.py:584-586` :

```javascript
const mats = [['^IRX','3M'],['^FVX','5A'],['^TNX','10A'],['^TYX','30A']];
const pts  = mats.filter(m => byId[m[0]] && byId[m[0]].value != null);
if (pts.length < 2) { emptyCard(…); return; }        // ← la courbe se trace dès 2 points
```

Côté serveur, `terminal.py:478-480` :

```python
for _tk, _nm, _un, _kind in _MACRO_TK:
    _v, _p = _mv(_tk)
    if _v is None:
        continue                                      # ← une maturité indisponible est OMISE
```

Le serveur **omet** toute maturité dont le téléchargement échoue ; le client
**accepte de tracer dès deux points**. Le seuil `< 2` existe précisément parce
que « moins de 4 » est un état prévu.

**Une courbe tracée sur 2 ou 3 maturités porte donc, en toutes lettres,
« 4 maturités réelles ».**

## La règle est dans la même phrase

Ce n'est pas un fichier négligent : la phrase affirme, deux propositions plus
loin, **« non affichées plutôt qu'inventées »**. Le panneau est explicitement
fier de ne pas fabriquer de maturité — et annonce un **compte** qu'il ne vérifie
jamais. La bonne pratique et sa faille ne sont pas à trois lignes l'une de
l'autre : elles sont dans la **même phrase**.

## Ce que je n'ai pas observé — et que je dis

Le payload `macro` présent au démarrage porte **4 maturités sur 4**. Je n'ai
donc **pas observé** de courbe à 2 ou 3 points : j'ai établi que le serveur les
omet quand elles manquent et que le client les trace quand même. **Le décalage
est démontré par construction, pas constaté sur des données réelles.** C'est une
différence, et elle est en faveur du produit.

## Classement

**Rang 1**, famille du 422 : les **valeurs** affichées sont réelles — aucune
maturité n'est inventée, la promesse d'honnêteté est tenue sur ce point. C'est le
**compte** qui est faux quand une source manque, dans une phrase qui se présente
comme une déclaration de limites.

Correction pressentie, minuscule : rendre le compte dynamique — `${pts.length}
maturités réelles` dans le `limits:` de la carte, et une formulation du panneau
qui n'annonce pas un nombre fixe. **Aucun GO, rien n'est engagé.**

## La décision de veine, prise

Le critère durci annoncé au 424 était : *sans un défaut dont la valeur est
**prouvée affichée**, déclarer la veine épuisée.* **Le critère est rempli** — la
phrase a été extraite du **marquage servi** de `/markets?view=macro`, pas d'un
fichier source. La veine reste ouverte pour le 426.

Ce lot valide aussi le **changement d'ordre** : partir de l'écran a produit, en
une seule mesure, ce que trois lots partis du moteur n'avaient pas atteint. À
reconduire.

## Portée

Une seule affirmation ouverte sur les 17 recensées. Les seize autres sont
**listées, non vérifiées** — en particulier « σ = spot · IV_ATM · √(DTE/365) »
et « moyenne des % par trade — pas une performance composée », qui sont des
affirmations de **méthode** et se testeraient contre leur moteur. Rien n'a été
mesuré sur elles.

Le recensement ne couvre que les littéraux `limits:`/`conclusion:` de 15 à 150
caractères ; une affirmation construite dynamiquement lui échappe.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde rend
  les pages en mémoire et n'écrit rien. Pas de preuve MD5 requise, pas de bump.
  SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-huitième lot court. Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ ·
421 ✗ · 422 ✓ · 423 ✗ · 424 ~ · 425 ✓ (affiché, prouvé)**.

Le motif tient une septième fois, et sous une forme nouvelle : jusqu'ici la règle
et son oubli étaient à quelques lignes d'écart — ici ils partagent **la même
phrase**.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
