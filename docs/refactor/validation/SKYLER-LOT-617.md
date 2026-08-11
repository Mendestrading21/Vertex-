# SKYLER — LOT 617 · UN PLAFOND QUI NE ROGNAIT PAS, NE DÉBORDAIT PAS, ET COMPRIMAIT UNE ICÔNE

Dernière dimension non traitée des bandeaux d'état : **la hauteur**. Les lots 610
à 612 n'ont jugé que la géométrie horizontale, les 613 à 616 que le contraste.

**Le piège écrit d'avance est réfuté**, et c'est le lot.

## Ce que le code annonçait

```css
/* Un état honnête, compact, actionnable — jamais un rectangle géant vide. */
.vx-state{display:flex;flex-direction:column;…;max-height:240px;justify-content:center}
```

Un **plafond dur de 240 px**, **aucune règle `overflow`**, dans une colonne
flexible centrée. Mon énoncé (a), écrit avant de mesurer : *« sans `overflow`,
un contenu plus haut que le plafond n'est pas rogné — il DÉBORDE, et dans une
colonne centrée, en haut ET en bas. »*

## **RÉFUTÉ.** Un plafond dans une colonne flexible ne déborde pas : il comprime

Les enfants d'un conteneur flex sont **rétractables**. Au lieu de sortir de la
boîte, ils rétrécissent. Et **la compression est invisible à tout test de
débordement** :

| instrument | verdict | pourquoi il était aveugle |
| --- | --- | --- |
| 1. `scrollHeight > height` | **0** | `scrollHeight` rendait la valeur **déjà écrêtée** — 238, pas 249 |
| 2. rect des enfants vs rect de la boîte | **0** | les enfants **rétrécissent** au lieu de sortir |
| 3. `scrollHeight` de **chaque enfant** | **trouvé** | l'icône fantôme passait de **41 px à 31 px** |

**J'ai failli publier « 0 débordement, 0 zone atteignant 240 px ».** Les deux
étaient faux : une zone était **exactement** au plafond, et sa hauteur naturelle
était **249 px**.

Ce qui a fait basculer le lot n'est pas un instrument plus fin — c'est d'avoir
demandé **la distribution des hauteurs** au lieu du seul compte d'anomalies. Un
« 0 » sans marge ne dit rien : la zone la plus haute était à **99,2 % du
plafond**.

## L'effet réel, mesuré

`/journal?view=track-record`, **390 px**, état « Pas encore assez de verdicts
résolus » :

| | avec le plafond | sans |
| --- | --- | --- |
| hauteur de la boîte | **240 px** | **251 px** |
| hauteur naturelle du contenu | 249 px | 249 px |
| icône fantôme (`vx-state-ghost`) | **31 px** | **41 px** |
| texte perdu | **aucun** | aucun |
| chevauchement | **aucun** | aucun |
| rognage par un ancêtre | **aucun** | aucun |

**Les 9 px de compression étaient absorbés entièrement par l'icône décorative**,
que `states.css` documente lui-même comme « placeholder, **jamais une donnée** ».
Le même pictogramme mesurait 41 px partout ailleurs et 31 px là — une
incohérence visuelle, pas une perte d'information.

## Le piège, volet par volet

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « le plafond fait déborder le contenu » | **RÉFUTÉ** — il comprime |
| **(b)** | « une zone dépasse 240 px à 390 px » | **CONFIRMÉ** — 249 px naturels |
| **(c)** | « le débordement chevauche l'élément suivant » | **SANS OBJET** — (a) réfuté |
| **(d)** | « les `.vx-error-banner`, sans plafond, ne sont pas affectés » | **CONFIRMÉ** |
| **danger nommé** | « ne pas “régler” par `overflow:hidden` » | **respecté, et désormais gardé par un test** |

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure **les zones d'état**. Le cas exclu : **les cartes ordinaires
du produit**. Si elles plafonnaient aussi leur hauteur, le plafond serait un
motif de design assumé, pas un oubli propre aux états.

**0 des 20 cartes mesurées ne plafonne sa hauteur.** C'est ce contrôle qui rend
le retrait légitime : `.vx-state` était **seul** à porter cette contrainte.

## Le correctif — et ce qu'il ne prétend pas être

`max-height:240px` **retiré**. La boîte grandit ; l'icône retrouve ses 41 px.

**Le plafond est retiré parce qu'il ne servait rien et déformait une icône, PAS
parce qu'il faisait déborder du texte.** Le commentaire posé dans `states.css`
au moment du retrait affirmait le contraire — il a été **réécrit pour dire ce
que la mesure a montré**, avant publication.

L'en-tête du fichier promettait « **jamais un rectangle géant vide** » et
s'appuyait sur ce plafond. Le plafond parti, la promesse partait avec lui :
**612-B**. L'en-tête dit désormais que la compacité vient de la **brièveté des
messages**, pas d'une contrainte de hauteur.

## Ce que le lot n'établit pas

- **Que 240 px n'ait jamais mordu ailleurs.** Six écrans en échec, deux
  largeurs : **une seule zone** était concernée. D'autres états, sur des données
  ou des langues plus longues, pourraient l'atteindre — non mesuré.
- **Que la boîte plus haute soit préférable.** Elle est plus **cohérente** (même
  icône partout) ; « plus belle » n'a pas été jugé.
- **Le comportement en cas de contenu vraiment long** — aucun message du produit
  n'approche une longueur où la question se poserait, et je n'en ai pas fabriqué.
- **Les largeurs intermédiaires** : mesuré à 390 et 1440 px seulement.

## Règles neuves

- **617-A — DANS UN CONTENEUR FLEX, UN PLAFOND NE PRODUIT PAS DE DÉBORDEMENT :
  IL PRODUIT UNE COMPRESSION.** Et la compression ne déclenche **aucun** test de
  débordement — ni `scrollHeight`, ni comparaison de rectangles. Il faut
  descendre au `scrollHeight` de **chaque enfant**.
- **617-B — UN COMPTE D'ANOMALIES À ZÉRO NE VAUT RIEN SANS LA DISTRIBUTION.**
  « 0 zone en débordement » était vrai et trompeur : la plus haute était à
  99,2 % du plafond. **Demander la marge, pas seulement le verdict.**
- **617-C — UN COMMENTAIRE ÉCRIT AU MOMENT DU CORRECTIF DOIT ÊTRE RELU APRÈS LA
  MESURE.** Celui du retrait affirmait un débordement que la mesure a réfuté
  vingt minutes plus tard. **Écrire le pourquoi avant de savoir, c'est écrire
  une hypothèse dans du code de production.**

## Ce que le dépôt fait bien

- **L'icône fantôme est documentée comme décorative** (« placeholder, jamais une
  donnée ») : c'est cette ligne qui a permis de classer la compression comme
  cosmétique plutôt que comme perte d'information.
- **Aucune carte du produit ne plafonne sa hauteur** — la contrainte était une
  exception isolée, donc retirable sans casser un motif.
- **Aucun `overflow:hidden` n'avait été ajouté** pour « régler » le problème :
  le réflexe dangereux n'avait jamais été pris.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/static/vertex/css/states.css` (règle +
  en-tête + commentaire réécrit après mesure), `vertex/app/routes/system.py`.
- **1 gardien neuf** (4 tests, **4 mutations rouges** — dont « `overflow:hidden`
  ajouté », le réflexe que le lot interdit).
- **5 épingles** `td-shell-v198` → **`td-shell-v199`** + empreinte des assets et
  `_SW_VERSION` du gardien 361.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2927 passed / 0 skipped** *(2923 + les 4 du gardien neuf)*.
- Navigateur : **~30 chargements** — 6 écrans × 2 largeurs pour le banc
  principal, plus 3 bancs successifs sur l'écran décisif, avec le plafond
  réinjecté par le navigateur (jamais remis dans le fichier).
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **253** *(+2 : « 0 débordement, 0 zone à 240 px » —
  faux deux fois, une zone y était exactement ; et le commentaire de production
  qui affirmait un débordement réfuté par la mesure)*
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 13**
