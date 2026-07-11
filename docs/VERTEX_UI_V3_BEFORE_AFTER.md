# Vertex UI V3 — Avant / Après

Captures : `docs/redesign/v3-before/` (thème Master Redesign bleu) →
`docs/redesign/v3-after/` (Experience OS — Dark Financial Luxury).
Tailles après : desktop 1600 & mobile 390 (pleine page, 8 pages) +
1440 / 1024 / 768 (viewport, 8 pages). Données fictives de démonstration
en mode DÉMO étiqueté.

| Page | Avant | Après (1600) | Après (390) |
|---|---|---|---|
| Briefing | v3-before/desktop/01-briefing.png | v3-after/desktop/01-briefing.png | v3-after/mobile/01-briefing.png |
| Marchés | …/02-marches.png | …/02-marches.png | …/02-marches.png |
| Opportunités | …/03-opportunites.png | …/03-opportunites.png | …/03-opportunites.png |
| Portefeuille | …/04-portefeuille.png | …/04-portefeuille.png | …/04-portefeuille.png |
| Analyse | …/05-analyse.png | …/05-analyse.png | …/05-analyse.png |
| Performance | …/06-performance.png | …/06-performance.png | …/06-performance.png |
| Intelligence | …/07-intelligence.png | …/07-intelligence.png | …/07-intelligence.png |
| Système | …/08-systeme.png | …/08-systeme.png | …/08-systeme.png |

## Changements globaux

- **Direction artistique** : bleu froid → Dark Financial Luxury (fonds
  anthracite chauds, identité orange/ambre maîtrisée, halos diffus ≤ 5 %,
  vignettage subtil).
- **Composants** : cartes 3 niveaux (hero/analytical/compact) avec
  élévation au hover ; système de boutons complet (primary dégradé brand,
  loading/success/error) ; tabs à indicateur orange ; chips avec compteur
  de filtres ; états premium (démo bannière + badge, live 5 états).
- **Shell** : logo brand, item actif orange à trait dégradé, bouton
  Ajouter de marque, état marché à point de vie, recherche focus brand,
  bouton Réduire corrigé (style navigateur par défaut visible avant).
- **Graphiques** : thème unique orange/ambre (`chart-theme.js`), tooltip
  premium, sémantique couleur documentée.

## Changements par page

- **Briefing** : Brief Vertex passe en carte HERO rangée 1 ; cross-asset
  regroupé en une carte compacte (avant : une rangée entière de « n/d ») ;
  bannière démo propre.
- **Marchés** : bandeau indices RÉPARÉ (le mapping objet/liste affichait
  n/d alors que les valeurs existaient) ; nouveau graphique multi-indices
  rebasés 0 % ; nouvelle heatmap performance/momentum par secteur
  cliquable ; `[object Object]` du leader sectoriel corrigé.
- **Opportunités** : le point sélectionné du radar ouvre un dossier
  complet (scores, R:R, setup, secteur) avec 7 actions rapides.
- **Portefeuille** : nouvelle synthèse (valeur, P&L latent, équipe X/10,
  options X/3) ; **options tactiques séparées de l'équipe (jamais
  gardien)** ; contributeurs/détracteurs ; cohérence des unités de coût
  (le poids d'une option pouvait afficher 98 % du portefeuille).
- **Analyse** : workspace 2 colonnes — rail sticky avec décision finale +
  audit trail, plan & niveaux, risques identifiés.
- **Performance** : heatmap P&L moyen par mois + distribution des
  rendements par trade (sur les clôtures déclarées) ; journal de clôture
  corrigé (un ×100 erroné pouvait classer un gain en LOSS).
- **Intelligence** : exemples de questions cliquables + tickers
  récents/favoris (page anciennement quasi vide au-dessus du pli).
- **Système** : moteurs différenciés prêt / chargé-sans-données / KO ;
  endpoints techniques déplacés dans un drawer.

## Responsive

7 viewports (1600/1440/1280/1024/768/430/390) × 8 pages vérifiés en
Chromium : **0 débordement horizontal, 0 erreur page**.
