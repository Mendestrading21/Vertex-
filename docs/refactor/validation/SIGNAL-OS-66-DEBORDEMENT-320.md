# SIGNAL OS · LOT 66 — LE DÉTECTEUR NE POUVAIT PAS SE DÉCLENCHER

Branche : `agent/vertex-signal-os-v1` · SW **v245 → v246** (CSS servi + HTML de
Marchés) · Suite **3 527 passed** (3 520 → +7)

Réserve SIGNAL-OS-65 §D3, de ma main : le balayage responsive était *« la mesure
encore faisable la plus utile — la seule qui touche un usage réel déclaré
(consultation iPhone), et la seule dont un défaut serait visible tous les jours
plutôt que pendant un incident »*.

Deux instruments existaient déjà. **Aucun des deux n'avait de témoin de
détection, et l'un des deux était structurellement aveugle.**

---

## 1. L'aveuglement, prouvé des deux côtés

`tools/mesurer_integrite_pages.py` lisait
`documentElement.scrollWidth - clientWidth`. Or `html` et `body` portent
**`overflow-x: clip`** — et dans ce mode, `scrollWidth` du `documentElement` ne
dépasse **jamais** `clientWidth`.

Vérifié en injectant 400 px de contenu de trop :

```text
doc.scrollWidth  : 1440   ← inchangé, quoi qu'on ajoute
body.scrollWidth : 1840   ← le vrai débordement
```

Son « **0 débordement horizontal** » sur cinq largeurs, publié depuis le lot 26,
ne prouvait donc rien. C'est la **même famille d'erreur que le lot 64** : une
mesure incapable, par construction, de rendre un résultat positif.

Le fichier avait pourtant un témoin — mais un témoin de **largeur** (le
navigateur a-t-il appliqué le gabarit ?), pas de **détection**. Les deux se
ressemblent et ne prouvent pas la même chose.

---

## 2. Ce que l'aveuglement cachait

À **320 px** (WCAG 1.4.10 « reflow »), le cluster droit de la barre supérieure
sortait du gabarit de **4 à 34 px** selon la page.

Et `overflow-x: clip` **interdit tout défilement**. Le bouton d'actualisation
n'était donc pas seulement hors écran : il était **hors d'atteinte**.

### La cause, mesurée et non devinée

```text
gabarit 320 · marges 36 · gouttières 42
cluster droit  180 px  (trois boutons 40 px + un bouton 36 px, incompressibles)
champ recherche 98 px  ← plancher INTRINSÈQUE, pas un choix
```

`flex: 1 1 0%` ne suffit pas : **`min-width: auto` interdit à un élément flex de
descendre sous sa taille intrinsèque**, ici imposée par le `padding-left: 34px`
qui loge l'icône de recherche.

---

## 3. Et ma première correction était fautive

`min-width: 0` supprimait bien le débordement. Mais le fil d'Ariane, lui aussi en
`flex: 1 1 0`, réclamait alors toute la place libre et écrasait le champ à
**0 px de large sur quatre pages sur cinq**, à 320 comme à 390 px.

J'avais échangé un défaut contre un autre : le bouton redevenait atteignable, la
recherche disparaissait — alors que le **lot 289** avait précisément établi que
ce champ est *le* chemin tactile vers la palette de commandes.

**Un plancher, pas un zéro : 44 px.** Le fil d'Ariane cède le reste — c'est lui
qui doit céder, il tronque déjà en ellipse par dessein (lot 222).

### Le piège de mesure qui a failli me faire conclure « c'est bon »

Une première sonde lisait 38 px et 73 px, et me montrait un champ sain. Elle
mesurait **avant** que le fil d'Ariane ne se remplisse. Deux mesures qui se
contredisent ne sont pas un fait, c'est une course : trois échantillons espacés
ont tranché — **0 px, stable, sur quatre pages**.

---

## 4. Le dernier défaut : la seule table sans son patron

`/markets?view=sectors` portait la **seule** `<table class="vx-table">` du dépôt
qui ne soit pas enveloppée dans `.vx-table-wrap`. À 320 px elle sortait de 21 px
sans qu'aucun ancêtre ne puisse défiler : la colonne « **Leader** » était
purement **coupée**, ni visible ni atteignable.

---

## 5. Résultat

| largeur | débordement | ids dupliqués | liens cassés | rognage silencieux |
| --- | --- | --- | --- | --- |
| 1920 | — | — | — | **0** |
| 1440 | **0** | 0 | 0 | **0** |
| 1024 | **0** | 0 | 0 | — |
| 768 | **0** | 0 | 0 | **0** |
| 390 | **0** | 0 | 0 | **0** |
| 320 | **0** | 0 | 0 | — |

36 vues, lues **depuis la source** (jamais écrites de mémoire). Et cette fois
avec des détecteurs **prouvés mordants**.

---

## 6. Ce que ce lot ajoute aux instruments

- **trois témoins de détection** sur l'intégrité — un id dupliqué, un
  débordement, un lien interne cassé, fabriqués en mémoire et exigés dénoncés ;
- **un témoin** sur le rognage silencieux, plus les largeurs **768 et 1920** que
  la réserve D3 signalait comme jamais balayées ;
- l'exclusion de ce qui **défile** : une table large dans un conteneur
  `overflow-x: auto` sort du gabarit et reste atteignable ; l'accuser noierait le
  signal réel sous le patron le plus courant du produit ;
- le balayage porte sur **`body`**, plus sur `#vx-content` : le coupable vivait
  dans le shell, et chercher dans le contenu seul, c'était chercher la clé sous
  le lampadaire — 36 vues rendaient « élément non identifié » ;
- le chemin Chromium passe par un **glob** au lieu d'une version épinglée en dur.

---

## 7. Le gardien et ses huit mutations

`tests/test_signal_os_debordement_320_lot66.py` (7 tests).

| mutation | résultat |
| --- | --- |
| M1 — lecture aveugle sur `documentElement` | **tombe** ✅ |
| M2 — balayage limité à `#vx-content` | **tombe** ✅ |
| M3 — exclusion des ancêtres défilants retirée | **tombe** ✅ |
| M4 — témoin de débordement fabriqué mais non vérifié | **tombe** ✅ |
| M5 — témoin du rognage retiré | **PASSAIT** ❌ → corrigé |
| M5b — verdict du témoin supprimé | **tombe** ✅ |
| M6 — plancher du champ remis à zéro | **tombe** ✅ |
| M7 — enveloppe de table retirée | **tombe** ✅ |

**M5 était creux — neuvième de la série, toujours le même mécanisme.** Le test
cherchait `TEMOIN_TXT` ; renommer la variable à sa **définition** laisse le nom
présent dans ses deux usages plus bas. Retargeté sur l'affectation exacte
(`TEMOIN_TXT = 'TEMOIN ROGNAGE`), la mutation rejouée échoue correctement.

---

## 8. Réserves

1. **`overflow-x: clip` reste en place, et c'est un choix qui mérite un mot.**
   Il empêche tout défilement horizontal accidentel — mais il fait aussi qu'un
   futur débordement sera **coupé en silence** plutôt que rendu accessible. Le
   détecteur le voit désormais ; l'utilisateur, non.
2. **Une seule hauteur par largeur**, et le mode démonstration.
3. **Les états de panne ne sont pas croisés avec les largeurs** : tout est mesuré
   en nominal. Un état vide ou une bannière d'erreur peut avoir sa propre
   géométrie.
4. **Le rognage silencieux n'est pas mesuré à 1024 ni 320** — l'outil couvre
   1920/1440/768/390, l'intégrité couvre 1440/1024/768/390/320. Les deux grilles
   ne coïncident pas.
