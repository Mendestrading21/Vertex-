# SIGNAL OS · LOT 41 — DEUX EMOJI QUE HUIT PAGES NE MONTRAIENT PAS

Branche : `agent/vertex-signal-os-v1` · SW **v233 → v234** (octets servis modifiés)

Règles en cause, citées telles quelles :

- `COPY.md`, interdits : « Emoji comme ponctuation de produit. »
- `VISUAL_SYSTEM.md`, icônes : « Une seule famille outline. » ; anti-patterns :
  « Icônes multicolores façon crypto template. »

Un emoji est multicolore par construction : **aucun token ne peut le repeindre**.
Il échappe donc entièrement au système de couleur que les lots 21, 22 et 382 ont
mis en place.

---

## 1. La question, et pourquoi un `grep` n'y répond pas

La bonne question n'est pas « trouve-t-on des emoji dans le code ? » — on en
trouve, beaucoup, dans des modules qui n'atteignent aucune page servie. C'est
**« l'écran en montre-t-il ? »**.

`tools/mesurer_pictogrammes.py` sépare donc deux populations et ne les confond
jamais :

| population | définition | verdict |
| --- | --- | --- |
| **PEINT** | présent dans `innerText` ou dans un attribut lisible (`aria-label`, `title`, `alt`) | ce que l'interface montre |
| **SERVI SEULEMENT** | présent dans les octets, absent de l'écran | du poids, parfois une fragilité — pas une faute visuelle |

Avant de conclure, l'outil **injecte** un pictogramme témoin dans la page et
exige de le revoir. Sans ce témoin, un zéro ne prouverait rien : il rend 2
(aveugle) plutôt qu'un faux vert.

---

## 2. Le relevé, et le piège qu'il a failli me faire

Sur les **huit écrans d'accueil** : **2 pictogrammes peints**, `→` (×37, dans
des libellés de lien) et `⌘` (×10, le raccourci de la palette de commandes).
**Aucun emoji.**

Conclusion tentante : « la règle est respectée ». Elle est fausse.

Deux emoji vivaient sur **`/analysis/<sym>`**, dans une branche qui ne s'ouvre
que si la donnée remplit la condition :

```text
/analysis/ABNB → « TTM Squeeze  🔒 en compression (BB dans Keltner) »
/analysis/ALL  → « TTM Squeeze  🚀 sortie de compression »
```

Vérifié au navigateur, texte rendu à l'appui. **L'état d'accueil est l'état le
plus pauvre du produit.** Le mesurer seul et appeler ça une couverture, c'est la
faute du lot 38 sous un nouveau déguisement — un instrument qui ne reproduit pas
les états que le produit atteint.

L'outil ouvre désormais ces branches, et les symboles ne sont **pas inventés** :
ils sont lus dans le scan servi (`ttm_squeeze`, `ttm_fired`). Si aucun symbole
n'ouvre une branche, l'outil le **dit** — « BRANCHE NON MESUREE » — au lieu de
balayer une page morte et de compter un vert.

---

## 3. Les deux corrections

### 3.1 Le pictogramme ne portait aucune information

`🔒 en compression (BB dans Keltner)` : le cadenas ne disait rien que les mots
ne disaient déjà. Il est retiré. La compression **sans** sortie n'avait plus de
marque une fois le cadenas parti — elle prend `vx-warn` : jaune =
attente/prudence dans la sémantique de couleur du système. **Le sens revient
par la palette, pas par un dessin.**

### 3.2 Un défaut réel, silencieux, évité

Le serveur transporte la sévérité d'alerte **comme un emoji** (premier élément
du tuple). La page Aujourd'hui comparait la chaîne entière :

```js
danger = (sev === '🔴')
```

Un sélecteur de variante (U+FE0F) ajouté en amont — ce que fait n'importe quelle
normalisation d'emoji — rend cette égalité fausse **en silence**, et une alerte
de danger se peint alors en jaune. La lecture porte désormais sur le point de
code du caractère de base :

```js
const ROUGE = 0x1F534;              // LARGE RED CIRCLE
danger = (sev.codePointAt(0) === ROUGE)
```

Le contrat du serveur n'est pas touché — c'est la lecture qui devient robuste.
Effet de bord utile : plus aucun emoji ne subsiste dans le **code vivant** servi
par les huit espaces.

---

## 4. Le relevé après correction, et ce qui reste servi sans être peint

Dix URL — les huit espaces **plus** les deux branches conditionnelles, ouvertes
par des symboles lus dans le scan :

```text
temoin : pictogramme injecte et revu — la sonde voit l'ecran
branche ouverte : /analysis/ABNB   ttm_squeeze — compression Bollinger/Keltner
branche ouverte : /analysis/ALL    ttm_fired   — sortie de compression
AUCUN EMOJI PEINT.
```

**Peints : 4 signes, tous monochromes** — `→` (×57), `⌘` (×12), `↓` (×2),
`↗` (×2). Ils prennent la couleur du texte et restent donc dans le système ; la
règle qui les concerne est celle de la famille unique, pas celle de la
ponctuation emoji.

**Servis mais jamais peints : 17** — `←`, `↑`, `↓`, `↔`, `↗`, `─`, `═`, `★`,
`⚠`, `✅`, `✓`, `✗`, `✕`, `🔒`, `🔴`, `🚀`, `🟠`. Ils vivent dans des
commentaires servis — qui **documentent précisément pourquoi tel pictogramme a
été retiré**, 🚀 et 🔒 y figurent désormais pour cette raison même — et dans des
branches non ouvertes par l'état de démonstration (bandeau d'erreur, tiroir
fermé, watchlist vide).

Le gardien ne les juge pas. Effacer ces commentaires ferait gagner quelques
octets et perdrait la raison.

Les signes de casseau peints (`→`, `⌘`, et `⚠`/`✕`/`✓` dans leurs branches) ne
sont **pas** des emoji : monochromes, ils prennent la couleur du texte et
restent dans le système. La règle qui les concerne est celle de la famille
unique, pas celle de la ponctuation emoji.

---

## 5. Le gardien

`tests/test_signal_os_pictogrammes_lot41.py` — 10 tests, sans navigateur : il
interroge les pages servies et regarde le **code vivant**, commentaires de bloc
retirés. Un emoji dans du code vivant est soit peint, soit du code mort ; les
deux méritent d'échouer.

Vérifié par mutation, une à la fois :

| mutation appliquée sur disque | ce qui tombe |
| --- | --- |
| remettre 🚀 dans la ligne TTM | le test de la fiche en compression |
| revenir à `sev === '🔴'` | 2 tests (page Aujourd'hui + lecture par point de code) |

Le test de la fiche **ouvre lui-même la condition** (`ttm_squeeze` posé dans
`scan_state`) : sans cet état, il passerait sans jamais atteindre la ligne qu'il
garde — et il vérifie que le mot « compression » est bien rendu avant de
conclure.

---

## 6. Réserves

1. **L'état de démonstration ne montre pas tout.** Deux branches sont ouvertes
   par symbole ; le bandeau d'erreur, le tiroir ouvert et la watchlist remplie
   restent hors du relevé navigateur (le gardien de code, lui, les couvre).
2. **`innerText` ne voit pas les pseudo-éléments** (`::before`/`::after`). Un
   pictogramme injecté par CSS échapperait à la sonde.
3. **Modules non servis non traités.** `nav.py`, `home_art.py`, `vx_kit.py`,
   `widget_lab.py` et les pages de laboratoire portent encore des emoji ; le lot
   381 a mesuré que le JS de `vx_kit` n'atteint aucune des huit pages. Les
   nettoyer serait un autre lot, et il faudrait d'abord mesurer ce qui les sert.
4. **Le serveur continue d'envoyer la sévérité comme un pictogramme.** La
   lecture est robuste ; le contrat, lui, reste discutable — le changer touche
   d'autres consommateurs et mérite son propre lot.
