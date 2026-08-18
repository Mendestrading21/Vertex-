# SIGNAL OS · LOT 47 — LA SONDE N'AVAIT QU'UN ŒIL

Branche : `agent/vertex-signal-os-v1` · SW **v235** (aucun octet servi touché)

Réserve n°2 du lot 41, écrite de ma main : « `innerText` ne voit pas les
pseudo-éléments (`::before`/`::after`). Un pictogramme injecté par CSS
échapperait à la sonde. »

Un angle mort qu'on déclare sans le fermer reste un angle mort. Ce lot le ferme,
et **il y avait bien quelque chose derrière**.

---

## 1. Ce que la sonde ne pouvait pas voir

`innerText` rend le texte des nœuds. Une règle
`::before { content: "…" }` peint un glyphe **sans créer de nœud de texte** :
l'écran le montre, la sonde ne le lit pas. Le produit s'en sert (puces,
chevrons), donc l'angle mort n'était pas théorique.

La sonde lit désormais aussi la propriété calculée `content` des deux
pseudo-éléments de chaque élément, en ignorant `none`/`normal` et les valeurs
non littérales (`attr()`, `counter()`) — qui ne portent pas de glyphe par
elles-mêmes.

---

## 2. Le témoin devait doubler, lui aussi

La sonde a maintenant **deux organes**, et un témoin qui n'en éprouve qu'un ne
prouve que celui-là. L'injection de contrôle pose donc deux choses : un nœud de
texte **et** une règle CSS `::before`. L'outil exige de revoir le témoin
**par les deux chemins** — sinon il rend 2 :

```text
temoin : revu dans le TEXTE et dans un PSEUDO-ELEMENT — les deux organes
         de la sonde repondent
```

---

## 3. Ce que le second œil a trouvé

Un **cinquième** pictogramme peint, invisible au relevé du lot 41 :

```text
◇ U+25C7 ×2   WHITE DIAMOND   /options /system
```

Origine : `components.css` —
`.vx-readonly-shield::before { content:"◇"; color: var(--vx-brand-strong) }`,
le préfixe de « Analyse uniquement · aucun ordre ».

**Ce n'est pas un défaut, et c'est ce qui rend la trouvaille intéressante** : le
signe est monochrome, sa couleur vient d'un token, et il marque l'invariant le
plus important du produit. Le lot 41 avait donc raison sur le fond et faux sur
le compte — il annonçait « 2 signes peints », il y en avait 3 sur les écrans
d'accueil.

Le verdict de tête, lui, tient et sur un instrument plus fort :
**aucun emoji peint**, sur 10 URL, texte et pseudo-éléments confondus.

---

## 4. Le gardien suit le même chemin

Les tests du lot 41 lisent le **HTML servi**. Un pictogramme posé par CSS n'y
est pas — il vit dans une feuille de style. Le gardien gagne donc un test qui
cherche un emoji dans les déclarations `content:` des feuilles servies.

Vérifié par mutation : remplacer `content:"◇"` par un cadenas dans
`components.css` fait échouer le test. Le losange, lui, passe — il n'est pas un
emoji, et la règle ne porte que sur les icônes multicolores.

---

## 5. Ce qui reste ouvert

1. **Les états conditionnels** (tiroir ouvert, bandeau d'erreur, watchlist
   remplie) restent hors du relevé navigateur — même réserve qu'au lot 41.
2. **Les pseudo-éléments sous survol ou focus** ne sont pas mesurés : la sonde
   lit l'état au repos.
3. **Une image de fond** (`background-image`) portant un pictogramme dessiné
   échapperait aux deux organes. Aucun n'est utilisé aujourd'hui pour cela, mais
   la sonde ne le vérifie pas.
