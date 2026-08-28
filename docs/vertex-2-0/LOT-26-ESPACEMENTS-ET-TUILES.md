# Lot 26 — espacements, mise en page, et la dernière dette de composants

Ce lot répond à deux demandes : **identifier et corriger** les problèmes
d'espacement et de mise en page, et **fermer** le dernier `À CORRIGER` de
l'audit d'acceptation.

Il a surtout servi à découvrir que trois affirmations rassurantes, écrites
plus tôt dans cette refonte, étaient fausses — et qu'aucun contrôle existant
ne pouvait le dire.

---

## 1. Un outil de plus, parce que les autres ne voyaient pas ça

`tools/vertex_2_0_espacements.py` relève, sur la page **réellement rendue** :
rythme vertical, alignements rompus, espacements écrits en dur, titres collés
à leur contenu, rangées de grille orphelines.

**Premier relevé, et première leçon : l'outil se trompait.** Il annonçait
treize « titres collés », dont neuf sur la page d'accueil. Vérification :

```
Actualités marquantes || display:none sur DIV.
Appétit pour le risque || display:none sur DIV.
Pouls du marché       || display:none sur DIV.
```

Un élément replié rend une boîte à zéro : `top` et `bottom` valent 0, donc
l'écart calculé vaut 0. Le tableau de bord replie **quatre blocs par défaut**
(`DEFAULT_HIDDEN` dans `briefing.py`, ré-ouvrables par « + Contexte marché »).
Reprocher un défaut de mise en page à un bloc que l'utilisateur a choisi de ne
pas voir aurait été une correction inventée. L'outil n'inspecte plus que ce qui
occupe réellement de la place ; six relevés survivent, tous sur Options.

## 2. Une deuxième feuille non servie, un deuxième dégât visible

Les six relevés survivants disaient tous la même chose : sur les **neuf** vues
Options, le libellé « Symbole » se collait à 2 px du titre « Sous-jacent
actif ».

Cause : les **seules** règles de `.vx-options-context` vivent dans
`neon-glass.css`, une feuille qu'aucune page ne demande. Sans elles, la grille
à trois colonnes n'existait pas : titre, phrase, libellé, champ et deux boutons
retombaient les uns sous les autres en flux normal.

C'est la **deuxième fois** que cette feuille cause un dégât visible (la
pastille de régime de Marchés fut la première, au lot 17). On a donc cessé de
traiter les cas un par un et on a **mesuré l'ensemble** : quelles classes sont
stylées uniquement par `neon-glass.css` **et** réellement présentes dans le DOM
des 65 routes servies ?

Sept. Chacune traitée pour ce qu'elle vaut, aucune rapatriée en bloc :

| Classe | Où | Décision |
|---|---|---|
| `.vx-options-context*` | 9 vues Options | rapatriée — la grille manquait entièrement |
| `.an-disclosure` | Analyse | rapatriée — `<details>` rendait un triangle natif, sans carte, cible de 20 px au lieu de 48 |
| `.vx-mk-regime-compact` | Marchés | rapatriée — sans grille, ses lignes se collaient |
| `.vx-eyebrow`, `.vx-lead`, `.vx-verdict` | Options | rapatriées — trois niveaux de texte sans échelle |
| `.vx-freshness` | Système | **partiellement** : la forme de la pastille, oui ; le halo et la pulsation `ng-pulse` du point « live », **non** — la direction interdit l'animation continue et le halo permanent |
| `.vx-options-local-bridge` | 6 vues Options | **non rapatriée** : l'élément porte déjà `hidden`, le navigateur le masque sans nous |

`neon-glass.css` reste **étiquetée, pas supprimée** : cinq bancs la lisent comme
registre de règles. Sa suppression demeure une décision humaine.

## 3. Une carte qui promettait et ne rendait rien

`vertex_2_0_etats_vides.py` cherche un **rectangle** vide. Il ne peut pas voir
ceci, et c'est une limite de sa définition, pas un réglage :

```html
<section class="vx-card">
  <div class="vx-card-header">Meilleurs contrats (radar)  [Tout voir →]</div>
  <div id="…-body"></div>          <!-- vidé en silence -->
</section>
```

La carte n'est pas vide : son texte porte le titre. Son corps, lui, fait 0 px de
haut, donc il passe sous le seuil de visibilité. Résultat : une carte qui
annonce un contenu, n'en donne aucun, et ne dit pas pourquoi.

`tools/vertex_2_0_cartes_creuses.py` relève ce défaut. **Une seule** carte sur
les 65 routes : `options-intel.js` faisait `rEl.innerHTML = ''` quand le tableau
d'options est vide. L'absence est désormais nommée, avec sa cause.

## 4. Un en-tête de carte qui écrase son titre

`.vx-card-header` est un flex sans retour à la ligne : quand une question
accompagne le titre, c'est le **titre** qui rétrécit. « Payoff à l'échéance » se
cassait en deux lignes alors que la moitié droite de la carte était vide. Le
titre garde sa largeur naturelle ; c'est la question qui descend d'une ligne.
Le comportement que `responsive.css` réservait au mobile devient celui de toutes
les largeurs, au lieu d'une exception.

## 5. Contrôle 048 — la justification était fausse

L'audit portait, depuis le lot 14, la mention : les quatre familles de tuiles
sont « **déjà visuellement unifiées** par le remappage des jetons ; migrer ne
changerait rien pour l'utilisateur ». On l'a mesurée, en injectant le balisage
réel dans une page servie et en lisant les styles **calculés** :

```
.vx-card.vx-kpi   fond transparent            filet rgba(255,255,255,.07)    r16  p16
.vx-stat          fond rgba(255,255,255,.024) filet rgba(222,228,238,.075)   r12  p12/14
.vx-metric        même fond, même filet                                      r12  p11/13
```

Deux fonds, deux filets, deux rayons — et `vx-stat` séparée de `vx-metric` par
**un pixel** de rembourrage. Pas une différence assumée : l'écart accidentel,
celui qu'on ne voit pas mais qui empêche deux tuiles voisines de s'aligner.
Les libellés allaient de 11,5 px/400 à 10 px/600, les chiffres de 19 à 28 px.

### Ce qui a été unifié

L'**implémentation**, pas les 138 appels. `glass.css` déclare déjà la surface
canonique — « sous-surfaces imbriquées : verre creusé », onze classes, en
`!important`. On ne la redéfinit pas et on ne surenchérit pas : on **aligne**
`.vx-card.vx-kpi`, seule tuile que cette liste avait oubliée, sur ses valeurs.
Puis une règle partagée pose la disposition et le rembourrage des trois, une
autre le libellé, une autre le chiffre.

Résultat mesuré : surface, libellé et typographie du chiffre **identiques** ;
seule la **taille** du chiffre varie — 19 / 22 / 26 px, compacte, courante,
forte — et cette échelle est déclarée.

`.vx-stat-xl` est **exclue**, et dit pourquoi : ce n'est pas une tuile mais un
grand nombre (`-value` + `-label`), sans fond ni filet. La fusionner
inventerait une équivalence qui n'existe pas.

**Preuve rejouable :** `tools/vertex_2_0_tuiles.py` — 0 écart non voulu, sortie
non nulle au moindre écart. Contre-épreuve exécutée : en retirant le
rembourrage partagé, l'outil signale les quatre écarts et sort en erreur.
Gardien : `tests/test_tuiles_famille_unique_lot26.py` (quatre bancs,
contre-épreuves exécutées).

## 6. Un halo permanent, servi, contraire à la direction

`cockpit.css` **est servie** et pose `text-shadow:0 0 15px rgba(54,200,137,.30)`
sur tout chiffre positif, son symétrique rouge sur le négatif, et un halo au
survol des tuiles de bande. La direction Black Glass — Signal Light interdit le
halo permanent : la couleur porte le sens, l'auréole n'ajoute rien et salit le
noir.

Les **jetons** sont neutralisés plutôt que les règles : le halo disparaît
partout où ils servaient, y compris là où l'on n'a pas regardé.

**Non vérifié ici**, et déclaré comme tel : l'egress marché est bloqué sur ce
poste, aucun chiffre n'est ni positif ni négatif en mode démo — la règle ne
s'exerce pas. Ce qui est vérifié, c'est que les jetons ne portent plus de halo.

## 7. Ce qui a été relevé et **non** corrigé, avec sa raison

### Les bords bas décalés entre deux cartes voisines

Quinze relevés. Vérification, paire par paire :

```
/calendar?view=agenda   Chronologie 1455 px   Ce qui touche le portefeuille 277 px
/calendar?view=today    Chronologie  258 px   Ce qui touche le portefeuille 277 px
```

**La même grille**, deux jours différents. L'écart n'est pas un défaut de mise
en page : c'est la longueur du contenu. Étirer la carte courte alignerait les
bords à 19 px d'écart — et créerait un vide de 1 178 px dans l'autre cas. Une
règle CSS ne peut pas distinguer les deux, et forcer l'alignement serait une
correction pire que le relevé.

Le relevé reste dans l'outil : il montre où regarder, il ne juge pas.

### Les espacements écrits en dur

336 déclarations `margin`/`padding` en style *inline* dans le code de
présentation, dont **45 rendues** sur les 65 routes. La règle de design n°1
demande des jetons. Ce n'est pas fait ici : ce sont des valeurs de 4 à 12 px
qui, une fois posées, ne changent rien à l'écran. Les remplacer toucherait 34
fichiers pour un résultat **invisible** et un risque réel.

**Dette chiffrée, datée, mesurable** — `tools/vertex_2_0_espacements.py` la
recompte à toute heure. Elle n'est pas déclarée corrigée.

### Deux styles d'en-tête de carte coexistent

`.vx2-surface` (titre en casse normale + question en italique) et `.vx-card`
(titre en petites capitales avec filet). Ils se croisent sur une même page —
Performance en montre les deux. C'est la frontière entre le balisage 2.0 et le
balisage historique ; la réduire suppose de migrer les cartes, pas de les
restyler. **Relevé, non corrigé.**

## 8. Deux champs de filtre sans libelle

L'audit d'accessibilite, rejoue sur les 65 routes a 1440 et a 390, releve deux
champs sans nom accessible : le filtre par ticker d'Opportunites -> Options et
celui d'Opportunites -> Anomalies. Tous deux portaient un `placeholder`
« Ticker » -- qui n'est pas un libelle : il disparait des la premiere frappe et
n'est pas annonce de facon fiable. Chacun recoit un `aria-label` qui dit ce
qu'il filtre. Verifie : 0 defaut sur les deux vues, aux deux tailles.

## 9. Preuves

```
python -m compileall -q terminal.py vertex     OK
node --check … options-intel.js                OK
python -m pytest -q                            4274 passés · 154 ignorés
                                               1 échec environnemental connu
python tools/vertex_2_0_tuiles.py              0 écart non voulu
python tools/vertex_2_0_cartes_creuses.py      0 carte creuse sur 65 routes
python tools/vertex_2_0_a11y.py                0 défaut · 0 débordement
                                               65 routes × 8 largeurs, 1440 et 390
```

L'échec environnemental est `test_la_classification_est_discriminante` : il
exige plus de 100 références git, ce clone en porte 3. Relevé au lot 0, **avant**
toute modification. Il passe sur la CI, qui dispose du dépôt complet.

Service worker : `td-shell-v256`. Empreinte `/static` mise à jour dans le même
commit, comme l'exige son gardien.
