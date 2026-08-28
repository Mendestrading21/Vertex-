# Lot 27 — le repli sans JavaScript, et la composition tablette

Deux contrôles de l'audit étaient `RÉUSSI partiellement` sur une limite
honnête : « pas mesuré ». Ils sont mesurables sur ce poste. Les mesurer a
révélé, dans les deux cas, des défauts réels qu'aucun contrôle existant ne
pouvait voir.

---

## 1. Contrôle 075 — JavaScript entièrement désactivé

### Ce que la mesure a montré

`tools/vertex_2_0_sans_js.py` sert les douze pages **moteur JS coupé** et pose
trois questions : la coque répond-elle ? reste-t-il des squelettes que rien ne
viendra résoudre ? la navigation reste-t-elle praticable ?

La coque et la navigation tenaient. Le reste, non :

```
/            22 squelettes visibles      /performance   6
/system       4                          /markets       3
/intelligence 3                          /calendar      2
/tracking     2                          /portfolio     1
/analysis     1                          /opportunities 1
```

Cinquante-trois rectangles pulsants promettant une donnée qu'**aucun script ne
viendrait chercher**. Un écran qui fait semblant de charger ment plus qu'un
écran qui dit non : l'utilisateur attend, et rien ne vient jamais.

### Ce qui a été fait

La coque porte deux choses :

1. un `<noscript><style>` qui **masque tous les squelettes** — sans script, ce
   ne sont plus des attentes mais des mensonges ;
2. un **bandeau** qui dit *pourquoi* l'écran est muet : la coque, la navigation
   et les liens fonctionnent, mais aucune donnée ne se charge, et rien de ce
   qui est affiché n'est à jour.

### Deux fautes commises en chemin, et dites

**La première a fait tomber toute l'application.** La coque est un `f-string` :
`{display:none !important}` y est lu comme un champ à formater. `NameError:
name 'display' is not defined`, gestionnaire d'erreur, redirection vers
elle-même — `ERR_TOO_MANY_REDIRECTS` sur les douze pages. Un `curl` l'a montré
en trois secondes ; aucune relecture statique ne l'aurait vu. Les accolades
sont doublées, et le gardien l'exige désormais explicitement.

**La seconde était visuelle.** Le bandeau, posé avant `.vx-app`, passait sous
la barre latérale fixe : ses premiers mots étaient coupés. Il vit maintenant
dans `#vx-content`, dans le flux, au-dessus du contenu.

### Preuve

`tools/vertex_2_0_sans_js.py` — **0 constat sur les 12 pages**. Contre-épreuve
exécutée : en retirant le `<noscript><style>`, l'outil signale à nouveau 22
squelettes visibles sur `/` et 4 sur `/system`. Gardien :
`tests/test_repli_sans_js_lot27.py`.

**Correction du chiffre :** le premier relevé annonçait 12 squelettes sur
`/system` ; il comptait la présence dans le DOM, pas la visibilité. Huit
d'entre eux vivaient dans des sous-vues masquées et ne promettaient rien à
personne. L'outil compte désormais ce qui **se voit**.

---

## 2. Contrôle 131 — la composition tablette

Le contrôle était partiel sur : « une composition **spécifiquement conçue**
pour la tablette n'a pas été dessinée ». En la regardant plutôt qu'en la
mesurant, deux fautes sont apparues — invisibles à toute autre largeur.

### La barre latérale se replie, ses titres ne suivent pas

`responsive.css` force la barre compacte sous 1024 px et masque
`.vx-nav-label`. Mais le traitement « repliée » — titres de groupe cachés,
filet de séparation à la place — est accroché à `[data-sidebar="collapsed"]`,
un attribut que la requête média ne pose pas.

Résultat mesuré à 768 px : « EXPLORER » rendu **« EXPLORE »**,
« INTELLIGENCE » rendu **« INTELLIG »**. Un mot coupé se lit comme un bug,
parce que c'en est un. Le même traitement s'applique désormais aux **deux**
causes de repli.

### Le raccourci clavier se posait sur le texte cherché

`.vx-kbd` est en position absolue à droite du champ de recherche, mais le champ
ne lui réservait aucune place : 12 px de rembourrage à droite. Tant que la
fenêtre est large, le texte n'atteint pas la pastille ; dès que le champ
rétrécit — tablette, ou barre latérale ouverte — « …une page » passe **dessous**.
Le champ réserve maintenant 46 px.

### Ce que la composition fait, une fois ces deux fautes retirées

**1024 px** : les actions remontent à côté du titre, la barre de contexte passe
à deux par rangée, les onglets tiennent sur une ligne, la barre latérale est
une colonne d'icônes.
**768 px** : les couples asymétriques 4/8, 5/7 et 3/9 passent en pile — chaque
panneau garde une largeur de lecture utile plutôt que deux colonnes trop
étroites.

---

## 3. Preuves (mises a jour au dernier passage)

```
python -m compileall -q vertex                 OK
python -m pytest -q                            4276 passés · 154 ignorés
                                               1 échec environnemental connu
python tools/vertex_2_0_sans_js.py             0 constat sur 12 pages
python tools/vertex_2_0_cartes_creuses.py      0 carte creuse sur 65 routes
python tools/vertex_2_0_a11y.py                0 défaut · 0 débordement
                                               65 routes × 8 largeurs
```

Service worker : `td-shell-v257`. Empreinte `/static` au même commit.

## 4. Un ecart structurel qui valait quatre valeurs

Mesure sur les **50 sous-vues** qui portent une barre d'onglets : l'ecart entre
cette barre et le premier bloc de contenu vaut

```
 0 px  x2        12 px  x28        16 px  x13        32 px  x7
```

C'est la **meme frontiere** -- on quitte la navigation, on entre dans le
contenu -- et elle se lit differemment d'une page a l'autre. En passant d'un
onglet a l'autre, le contenu saute.

L'ecart venait de trois endroits a la fois : une classe utilitaire posee au
coup par coup (`vx-mt3`, `vx-mt4`), la marge propre du premier bloc, ou rien du
tout. Il est desormais pose a **un seul endroit** -- la barre elle-meme -- a
20 px : entre les 16 px des ecarts internes et les 32 px des separations de
section.

Apres correction : **43 sous-vues a 20 px**, et 7 a 36 px. Ces sept-la ne sont
pas une exception de mise en page : sur Portefeuille, un conteneur de synthese
vide s'intercale entre les onglets et le contenu visible. **Verifie** en le
remplissant dans le navigateur : l'ecart retombe a 20 px. C'est la donnee
absente qui se voit, pas la regle qui manque.

## 5. Ce qui reste partiel, et pourquoi

**Huit** contrôles restent `RÉUSSI partiellement` — six lignes ci-dessous,
« 102–104 » en couvrant trois. Tous portent une limite que ce poste ne peut
pas lever :

- **061** — conclusion (51/72) et période (9/72) : une conclusion est une
  *lecture*, qu'un treemap de poids ne produit pas ; une période n'a de sens
  que pour une série temporelle. Les inventer fabriquerait du sens.
- **076** — le rendu CALL/strike/PUT **alimenté** exige une machine connectée.
- **087** — la distinction Marché/Portefeuille/Moteur/Saisie n'est pas
  systématique par valeur.
- **102–104** — heatmap mensuelle **déclarée absente** : la réécrire supposerait
  d'agréger des rendements dans l'UI, ce que `performance-center.md` interdit.
- **144** — **live** et **delayed** ne sont pas observables : l'egress vers les
  fournisseurs de marché est bloqué.
- **034** — Opportunités n'a pas de point focal unique.

Aucun n'est marqué `RÉUSSI` par optimisme.
