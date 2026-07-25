# WIDGET LAB — CURATION & SIGNATURE PASS 05 · GALERIE DE DESIGN

> Mission Design Director : faire dire « waouh », pas « c'est un dashboard ».
> Le Widget Lab n'est plus une bibliothèque — il **ouvre sur une galerie**.
> Dix objets, pas dix cartes : chacun a une **matière**, une **lumière**, une
> **profondeur**, une **identité**. Le luxe vient de la précision.
> **Aucune page produit. Aucun moteur. Aucune route. Aucun calcul.** Tout est
> scopé `/widget-lab` et `.wl / .gx-*` — `tokens.css` produit **intact**.

## 1. Ce qui change

Le haut de `/widget-lab` devient une **galerie musée** : un manifeste
(« Dix objets. Pas dix cartes. »), puis dix plaques. Chaque plaque = un objet
signature qui **flotte sur une scène noir-chaud éclairée**, posé sur une
**matière** choisie, avec une **question justificative** et une lecture d'une
ligne. La bibliothèque curée complète (P04, 60 widgets classés) reste en dessous,
introduite par un séparateur. Rien n'est perdu ; tout monte d'un cran.

## 2. Système de matières (11)

Vraies matières, pas des rectangles gris — dégradés multi-couches + bord de
lumière intérieur + occlusion + micro-texture + reflets/sheen propres :

**MATTE · SMOKED · FROSTED · OBSIDIAN · CARBON · CERAMIC · ANODIZED · POLISHED ·
BRUSHED · SOFT GLASS · METAL**. Chaque objet de la galerie **choisit** sa
matière (obsidian pour l'instrument de prix, carbon pour le filament, ceramic
pour le champ de breadth, metal pour le canyon, soft-glass pour l'aurora…).
Étiquette de matière discrète sur chaque plaque.

## 3. Système de lumière

- **Scène** (`gx-stage`) : lumière haute chaude (radial en haut-gauche) +
  **occlusion basse** (vignette sombre) + fond noir-chaud dégradé.
- **Profondeur** : ombres portées longues + bord intérieur clair + contour noir.
- **Glow local** : au survol seulement, un halo de la couleur sémantique de
  l'objet monte dans le panneau (`::after` en `color-mix`). **Jamais permanent.**
- **Lumière interne aux objets** : dégradés + flou (`feGaussianBlur`) sous les
  traits → filaments et nœuds **lumineux**, pas des lignes plates.

## 4. Palette (scopée `.wl`)

- **20 gris CHAUDS** `--g0…--g19` : du noir chaud `#0a0807` au blanc ivoire
  `#f5efe7` (rouge > bleu partout — jamais de noir uniforme).
- **Oranges** : `--o-ember` (identité) · `--o-copper` (matière) · `--o-glow`
  (interaction/point actif) · `--o-light` (accent) · `--o-burn` (alerte) ·
  `--o-deep` (surface).
- **Verts** (jamais fluo) : `--gr-trading` · `--gr-institution` · `--gr-profit` ·
  `--gr-live` · `--gr-strength`.
- **Rouges** (jamais saturés) : `--r-risk` · `--r-loss` · `--r-critical` ·
  `--r-bear` · `--r-stop`.
- L'orange reste **réservé** à l'identité, l'interaction et le point actif
  (gardien zéro-bleu vert). `tokens.css` produit inchangé.

## 5. Typographie

Hiérarchie de galerie (référence **Neue Montreal**, repli Inter/système) :
titre-manifeste très fin `300` en `clamp(40–82px)`, titres d'objets fins
`clamp(30–44px)`, eyebrow domaine en petites capitales espacées, question en
`350`, lecture en tabular-nums discret. Tout respire : espaces négatifs
`clamp(48–92px)` entre plaques.

## 6. Les 10 objets

| # | Objet | Domaine | Matière | Pourquoi le regarder |
|---|---|---|---|---|
| 01 | **Aurora** | Régime | soft glass | l'atmosphère du marché en une lumière |
| 02 | **Instrument** | Prix | obsidian | chandeliers de précision + filament MM |
| 03 | **Filament** | Momentum | carbon | la force relative comme un fil lumineux |
| 04 | **Cone** | Volatilité | frosted | l'enveloppe de vol balayée de lumière |
| 05 | **Terrain** | Options | anodized | le payoff sculpté, crête lumineuse |
| 06 | **Field** | Breadth | ceramic | la participation en paysage de points |
| 07 | **Constellation** | Rotation | smoked | les secteurs comme une carte du ciel |
| 08 | **Canyon** | Drawdown | metal | le repli comme un relief creusé |
| 09 | **Beam** | Risque/Récompense | brushed | l'asymétrie comme une balance qui penche |
| 10 | **Depth** | Liquidité | polished | deux versants qui se rejoignent au mid |

Chacun redessiné **à neuf** (dégradés, flou, nœud lumineux actif), pas amélioré.

## 7. Test du regard

Cachez textes, chiffres, labels, logo, orange : **l'objet reste reconnaissable**
par sa forme et sa lumière — une aurore, un instrument à chandeliers, un
filament, un cône, un terrain, un champ, une constellation, un canyon, une
balance, une profondeur. C'est le critère de réussite, et il est tenu.

## 8. Validation

- `python -m compileall -q terminal.py vertex` → exit 0.
- `python -m pytest tests/ -q` → **985 passed, 2 skipped** (dont 5 gardiens P05 :
  galerie présente, 10 objets SVG, 11 matières, palette chaude + gammes, lumière
  & typographie ; + zéro-bleu toujours vert).
- Navigateur **1440 & 390** : **0 débordement de page, 0 débordement d'élément,
  0 erreur console**.
- Captures : `lab5-hero.png` (manifeste + Aurora), `lab5-plate-instrument.png`
  (obsidian), `lab5-plate-constellation.png` (smoked), `lab5-mobile-hero.png`,
  `lab5-mobile-plate.png` (galerie empilée, matières distinctes).

## 9. Limites restantes / prochaine passe

- Les **variantes compacte/mobile dédiées par objet** (au contrat P04) restent à
  rendre en tuiles séparées ; ici le mobile est un reflow soigné.
- Les **11 matières** sont posées ; un second polish (occlusion par angle de
  lumière, réflexions dynamiques) est possible sur OBSIDIAN/POLISHED/ANODIZED.
- La galerie montre **10 objets phares** ; l'extension du langage (matière +
  lumière) au reste de la bibliothèque curée est l'étape suivante logique.
- **Neue Montreal** est référencée dans la pile de polices ; à embarquer comme
  webfont auto-hébergée si validée (aucun CDN — cohérent CSP/offline).

## Verdict

Le Widget Lab **ouvre désormais sur une galerie**. Dix objets sur scènes
éclairées, onze matières réelles, vingt gris chauds, gammes orange/vert/rouge,
lumière locale non permanente, typographie fine et espaces généreux. Le rendu
vise le niveau Apple / Linear / B&O invoqué — **précision, pas surenchère**.
**10 objets · 11 matières · 985 tests verts · 0 débordement · 0 erreur console ·
READONLY · aucune donnée réelle · aucune page produit touchée.** **Arrêt pour
validation humaine.** Dis-moi les objets à graver et la matière à pousser.
