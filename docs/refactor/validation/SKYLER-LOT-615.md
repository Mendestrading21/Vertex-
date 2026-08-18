# SKYLER — LOT 615 · L'ÉTIQUETTE QUI NOMME CHAQUE VALEUR SOUS 720 PX, ENFIN RENDUE

Les lots 613 et 614 l'avaient **recensée dans le CSS et jamais mesurée**, en le
disant à chaque fois. Ce lot la rend, la mesure — et découvre qu'elle était
conforme **à zéro marge**.

## Ce qu'aucun banc ne pouvait voir

```css
@media (max-width:720px){
  .vx-table-cards td::before{content:attr(data-label); font-size:9.5px;
                             color:var(--vx-text-faint)}
}
```

Sous 720 px, la table se transforme en cartes et **cette étiquette est le seul
texte qui dit de quelle colonne vient un chiffre**. Deux obstacles l'avaient
tenue hors de portée :

1. **Un pseudo-élément n'est pas un nœud du DOM.** Le balayage du 613 les lisait
   déjà (`getComputedStyle(n, '::before')`) — ce n'était pas le blocage.
2. **Les tables du produit sont vides** dans un environnement sans positions ni
   opportunités : `.vx-table-cards td` **n'existe pas**, donc il n'y a rien sur
   quoi lire un pseudo-élément.

### Un faux arrêté en cours de route

J'ai d'abord compté `data-label` dans les octets servis — **28 sur `/portfolio`,
32 sur `/opportunities`** — et j'allais en conclure que les étiquettes étaient
rendues. **Faux** : ce compte incluait le texte `data-label` présent dans la
**source JS** des gabarits. Le navigateur, lui, répondait **0 cellule en mode
cartes**. *Compter une chaîne dans des octets servis n'est pas mesurer un
attribut rendu.*

## La mesure, par injection DOM

Une ligne **synthétique** injectée dans une page réelle à 390 px. On mesure **le
CSS**, pas une donnée produit : rien n'est affiché à un utilisateur, rien n'est
persisté, aucune donnée n'est inventée.

| | avant 613 | après 613 | **après 615** |
| --- | --- | --- | --- |
| couleur | `#655d5f` | `#847a7c` | **`#8f8587`** |
| ratio sur la carte *(fond composé `(18,18,20)`)* | **2,93** | **4,50** | **5,23** |
| marge | −1,57 | **+0,00** | **+0,73** |

À 1440 px, `content` vaut `none` : l'étiquette **n'existe pas**, comme prévu par
le design. Vérifié, pas supposé.

## Pourquoi 4,50 n'était pas une conformité

Le correctif du 613 avait été **borné par la position d'alors du palier
`muted`** : viser plus haut aurait rendu `faint` plus lumineux que `muted` et
inversé la hiérarchie. Il tombait donc **exactement sur le seuil**, sur la
surface `--vx-surface-elevated` — précisément celle de la carte mobile.

Le lot 614, en remontant `muted` à `#989092`, a **libéré la place**. Le 615 en
profite pour appliquer à `faint` la règle que le 614 avait posée pour `muted` :

> **614-B — une conformité à +0,01 n'est pas une conformité.** Elle place le
> produit sur la ligne exacte où le prochain ajustement le fera retomber, sans
> rougir aucun test.

**Les trois lots forment une chaîne** : 613 mesure et corrige ce qu'il peut, 614
lève la contrainte, 615 termine le travail que 613 ne pouvait pas finir.

## Le nouveau palier

`--vx-text-faint` : **`#847a7c` → `#8f8587`** (L = 0,2436).

| surface | avant | après |
| --- | --- | --- |
| `canvas` | 4,97 | **5,77** |
| `shell` | 4,85 | **5,63** |
| `surface` | 4,71 | **5,47** |
| `surface-elevated` *(carte mobile)* | **4,50** | **5,23** |
| `surface-selected` | 4,08 ✗ | **4,74** ✓ *(fermée)* |
| `warm-depth` | 3,76 ✗ | 4,37 ✗ *(seule limite restante)* |

`warm-depth` **n'est pas fermée volontairement** : aucun texte n'y a jamais été
mesuré, et éclaircir davantage sans mesure reviendrait à corriger un défaut
qu'on n'a pas constaté. La limite est documentée dans `tokens.css` **et tenue
par un test**.

Pas entre `faint` (0,2436) et `muted` (0,2870) : **facteur 1,18** — resserré par
rapport à 1,42, mais toujours un palier distinct. Un test refuse qu'il descende
sous 1,10.

## Effet de bord mesuré : le cas « indéterminé » du 613 se ferme

Le 613 avait publié **« indéterminé »** pour les étiquettes de momentum à 8 px
(4,47 par les pixels, 4,85 par la composition — le seuil passait entre les deux,
et 8 px de large ne donnent que 3 pixels échantillonnés). Après le 615, elles
**quittent la liste par les deux méthodes**.

**Balayage complet, 8 pages × 2 largeurs, 2 700 feuilles :**

| | avant 613 | après 613 | après 614 | **après 615** |
| --- | --- | --- | --- | --- |
| combinaisons sous le seuil | **26** | 23 | 16 | **15** |

## L'état de clôture du dossier contraste

Les **15 restantes**, triées par la méthode qui a du signal sur chacune :

| famille | verdict |
| --- | --- |
| 5 × `<text>` SVG *(#f8f5f3)* | **artefact** — la boîte échantillonnée est le glyphe ; A donne 18,77 à 18,88 |
| 3 × encre sombre sur `var(--vx-brand-gradient)` *(grades, logo)* | **les deux méthodes fausses** ; la lecture du CSS montre un design correct |
| 3 × `a.vx-tab`, `span.vx-hide-mobile` | **artefact** ; A donne 15,95 à 17,40 |
| `div.vx-state-icon` | **artefact** *(part de dominante 45 %)* ; A = **5,73** |
| `span.vx-chip` / `span.vx-freshness` *(#989092)* | **artefact** *(pilules, 17–23 %)* ; A = **6,54** |
| `span.vx-chip` *(#2bbe90, vert)* | fond transparent, donc **A est fondée** : **8,61** — conforme |

**Par la méthode qui a du signal sur chaque cas, il ne reste aucune famille de
texte sous le seuil WCAG AA sur les 8 pages servies.** C'est une conclusion
bornée par ce que l'instrument atteint — pas une certification.

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « l'étiquette est rendue à 390 px, il suffit de charger les pages » | **RÉFUTÉ** — 0 cellule ; les tables sont vides |
| **(b)** | « le correctif du 613 la couvre » | **CONFIRMÉ mais insuffisant** — 4,50, zéro marge |
| **(c)** | « la place libérée par le 614 permet une vraie marge » | **CONFIRMÉ** — +0,73, et `selected` fermée en prime |
| **(d)** | « le pas entre `faint` et `muted` reste visible » | **CONFIRMÉ** — facteur 1,18, gardé à ≥ 1,10 |

## Ce que le lot n'établit pas

- **Que l'étiquette soit lisible en usage réel** : elle a été mesurée sur une
  ligne **injectée**, dans une carte au fond `--vx-surface-elevated`. Une carte
  posée sur un autre fond n'a pas été mesurée.
- **Que `warm-depth` ne porte aucun texte** : personne ne l'a vérifié — c'est
  une **absence de mesure**, pas une absence de risque.
- **Les 208 feuilles injoignables en pixels** restent injoignables.
- **Le texte des graphiques** n'est toujours pas mesuré *(canvas)*.
- **Survol, focus, et tout ce qui n'est pas le contraste** — taille, graisse,
  interlignage, ordre de lecture — restent hors du dossier.

## Règles neuves

- **615-A — COMPTER UNE CHAÎNE DANS DES OCTETS SERVIS N'EST PAS MESURER UN
  ATTRIBUT RENDU.** `data-label` apparaissait 28 fois dans `/portfolio` et zéro
  fois dans le DOM : la source JS des gabarits est servie avec la page. **Le
  seul juge d'un rendu est le navigateur.**
- **615-B — QUAND UN ÉTAT NE SE PRODUIT PAS, L'INJECTER EST LÉGITIME SI L'ON
  MESURE LE CODE ET NON LA DONNÉE.** Une ligne de table synthétique ne fabrique
  aucun chiffre affiché : elle expose une règle CSS qui, autrement, resterait
  éternellement « recensée, non mesurée ».
- **615-C — UN CORRECTIF BORNÉ PAR UNE CONTRAINTE DOIT ÊTRE REVISITÉ QUAND LA
  CONTRAINTE TOMBE.** Le 613 s'était arrêté à 4,50 **à cause** de la position de
  `muted` ; le 614 l'a déplacée. Sans relecture, le produit serait resté sur la
  ligne — conforme et fragile — **alors que la raison de s'y arrêter avait
  disparu**.

## Ce que le dépôt fait bien

- **Le mode cartes est une vraie transformation, pas un masquage** : les
  en-têtes disparaissent et chaque cellule reprend son intitulé. Le soin est là ;
  seule la couleur du palier ne suivait pas.
- **Le `content:none` à 1440 px** : l'étiquette n'existe pas hors du mode cartes,
  donc aucun texte fantôme lu par un lecteur d'écran au bureau.
- **Le commentaire de `tokens.css` datait déjà sa décision** — c'est ce qui a
  permis au 615 de retrouver *pourquoi* le 613 s'était arrêté à `#847a7c`, et de
  voir que la raison n'existait plus.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **3 fichiers de production** : `tokens.css` (`--vx-text-faint` + commentaire
  réécrit), `polish.css` (repli aligné), `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (4 tests, **5 mutations rouges** — dont « la règle
  repointée sur un autre token » et « la bascule descendue à 640 px ») +
  **1 constante du gardien 613 réduite** (`surface-selected` fermée).
- **5 épingles** `td-shell-v197` → **`td-shell-v198`** + empreinte des assets et
  `_SW_VERSION` du gardien 361.
- MD5 des 8 pages : **8 / 8 identiques** — seuls des octets CSS ont changé.
- `GET /api/client-log` : **0 erreur**.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2919 passed / 0 skipped** *(2915 + les 4 du gardien neuf)*.
- Navigateur : **19 chargements** — injection DOM à 390 et 1440 px, avant et
  après, plus le balayage 8 pages × 2 largeurs.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **250** *(+1 : « `data-label` est servi 28 fois
  donc l'étiquette est rendue » — le navigateur disait 0)*
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 12**
