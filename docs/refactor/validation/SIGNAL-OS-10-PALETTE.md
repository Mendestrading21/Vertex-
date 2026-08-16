# SIGNAL OS · LOT 10 — L'IDENTITÉ VIOLETTE DESCEND DANS LA BASE

Branche : `agent/vertex-signal-os-v1` · SW v216 → **v217** · Suite **3088 passed**

Décision utilisateur, attendue depuis quatre lots : **« violet néon presque bleu »**.
`VISUAL_SYSTEM.md` du skill le disait déjà — « Brand : violet Vertex », « le
violet peut identifier la série principale ». Les graphiques ne le savaient pas.

---

## 1. Ce qui se passait vraiment — et pourquoi c'était invisible

`tokens.css` déclarait une marque **cuivre** (`--vx-ember-500: #D28A54`).
`signal-os.css`, chargée en dernier, repeignait `--vx-brand` en violet
**par-dessus**.

- L'**interface** lisait l'override → violette.
- Les **graphiques** lisaient la base — `palette.py` et ses deux miroirs JS —
  → cuivre.

Deux identités dans un même produit. Le défaut n'était visible que sur un écran
montrant simultanément un bouton et une courbe, et aucun gardien ne pouvait le
voir : chaque couche était cohérente **avec elle-même**.

### La correction

La **rampe canonique** s'appelle désormais `--vx-violet-950 … 300` et porte les
littéraux ; `--vx-ember-*` en devient un alias — comme `signal-*` et `orange-*`
avant lui. L'override de `signal-os.css` est **supprimé** : il ne corrigeait
plus rien, il masquait d'où venait la couleur.

Un nom de rampe qui annonce une couleur qu'elle n'a pas est exactement ce qui a
permis la divergence. D'où la rampe renommée, et les alias conservés — renommer
40 références n'apporte rien, les garder muets aurait tout recommencé.

---

## 2. Trois défauts que l'override portait, mesurés en le retirant

| défaut | mesure |
| --- | --- |
| `--vx-brand-hover` et `--vx-brand-pressed` valaient **la même valeur** | survol et enfoncement indiscernables |
| le survol **assombrissait** | la rampe éclaircit au survol, n'assombrit qu'à l'enfoncement |
| `.vx-btn-primary` peignait son texte en quasi-blanc sur le violet | **2,90:1** — sous le seuil WCAG AA, sur l'action principale du produit |

L'encre sombre donne **6,24:1** au repos et **9,04:1** au survol. Le stop
« pressé » passe de `#7F5DF0` à `#8767F2` : le premier ne rendait que **4,42**
avec l'encre sombre, donc échouait aussi — sur un état atteignable au clavier
comme à la souris.

Ces trois-là ne sont **pas** causés par le changement de couleur : ils étaient
en production. C'est la mesure du violet qui les a exposés.

---

## 3. Le gardien anti-bleu a trouvé un défaut que je venais d'introduire

Ma première rampe assombrissait `#9B7BFF` à teinte constante. Or en descendant,
**le rouge chute plus vite que le bleu** : `#2B2270` et `#4635A8` basculent en
bleu franc, et `test_no_blue_primary_theme` les a refusés.

**Ce n'était pas un faux positif.** Un fond `#2B2270` se lit « fintech bleue » —
soit précisément l'invariant produit. Stops foncés recalculés sous contrainte
(`b ≤ 90` ou `r ≥ 110`), rampe vérifiée stop par stop avant écriture.

---

## 4. Une collision mesurée, résolue sans inventer de teinte

`OPTION` valait déjà `#9B7BFF`. La marque prenant la même valeur, les deux rôles
**fusionnent** — ce que l'interface faisait déjà depuis la couche Signal OS
(`--vx-brand: var(--vx-option)`), et Options est un espace de premier rang dont
la couleur est celle du produit.

Conséquence assumée : deux rôles partageant une valeur **ne peuvent plus se
distinguer sur un même graphique**. J'ai cherché qui en dépendait : **un seul
appelant** — la barre divergente **Open interest par strike**, où `brand`
peignait les CALL et `violet` les PUT, côte à côte.

Le PUT prend le **neutre acier**, déjà une série déclarée du registre. Inventer
une couleur pour un unique appelant aurait rendu le registre moins lisible ; et
vert/rouge est exclu — CALL/PUT n'est pas gain/perte.

`OPTION` sort de `SERIES` : deux séries de même couleur ne sont pas deux séries,
et `VISUAL_SYSTEM.md` classe « 6 couleurs de série sans besoin » parmi les
anti-motifs. La série passe de 6 à **5, toutes distinctes**.

---

## 5. Le cyan était devenu la couleur par défaut des graphiques

Trouvé en regardant la capture, pas en lisant le code : la **série de référence
de Marchés** était peinte en cyan. Remonté à la cause — `C.area` a pour couleur
par défaut `C.colors.blue`, qui est un **alias du cyan technique**, alors que le
registre le réserve à la « comparaison technique UNIQUEMENT ».

Deux graphiques phares en dépendaient : la série de référence de Marchés (par le
défaut) et la **courbe d'équité du Journal** (explicitement `C.colors.cyan`).
Les deux passent à la marque ; un appelant qui compare passe désormais le cyan
explicitement.

---

## 6. Un défaut latent trouvé au passage

Le résolveur d'alias de la page **design-system** ne suivait qu'**un** saut. La
rampe ajoutant un maillon (`orange-500 → ember-500 → violet-500 → #hex`), il
aurait affiché `var(--vx-violet-500)` à l'utilisateur — une indirection à la
place d'une couleur, **sur la page qui existe pour montrer les couleurs**.

Résolution complète, bornée à 8 sauts : un alias circulaire aurait fait tourner
un résolveur naïf indéfiniment, à l'import du module, donc au démarrage.
Vérifié : **0 alias non résolu** sur tout `tokens.css`.

---

## 7. Un gardien qui épinglait le mécanisme au lieu de la propriété

`test_signal_os_contract` vérifiait la **présence de la ligne**
`--vx-brand:var(--vx-option)` dans `signal-os.css`. Deux conséquences, les deux
vécues dans ce lot :

- il restait **vert** alors que la base déclarait une marque cuivre sous
  l'override — donc pendant toute la durée du défaut ;
- il est devenu **rouge** quand l'override a été supprimé, c'est-à-dire au moment
  précis où le défaut était corrigé.

Réécrit comme propriété : *la marque servie résout au violet, et vaut l'option*,
peu importe la feuille qui la déclare.

---

## 8. Mesures — version servie vérifiée avant chaque lecture

`/sw.js` → `td-shell-v217`.

| espace | `--vx-brand` | `VXCharts.colors.brand` | bouton primaire | erreurs |
| --- | --- | --- | --- | --- |
| les 8 | `#9B7BFF` | `#9B7BFF` | **6,24:1** | 0 |

Série graphique servie : `#9B7BFF · #45D6E8 · #c8bfae · #D9BE3C · #8A8284` —
**aucun doublon**. `audit_no_blue()` → `[]`.

Défilement horizontal de **page** — 1440 / 768 / 390 px : **aucun, 8/8**.

---

## 9. Dette

- **Le nom `chart-theme-obsidian-copper.js` ment** et est conservé : le renommer
  entraînerait shell, service worker, empreinte des assets et cinq épinglages de
  version **dans le même commit qu'un changement de couleur**. Deux choses
  distinctes ; à solder seule.
- Les alias `--vx-ember-*`, `--vx-orange-*`, `--vx-copper-*`, `--vx-signal-*`
  portent tous des noms de couleurs qu'ils n'ont plus. Ils résolvent
  correctement ; c'est de la dette de nommage, pas de comportement.
- Contenus non audités rang par rang : Marchés (6 vues), Opportunités,
  Portefeuille (5 vues sur 6), Options, Journal (6 rangs, 5 visualisations —
  l'inventaire mesuré de ce lot est prêt et sera exploité au suivant).
- Étiquetage démo : figé en caractérisation (lot 08).
- Fiche `/analysis/<ticker>` inaccessible ici.
- Aucun instrument ne détecte le rognage silencieux.
