# Vertex — Thème Obsidian Copper Deep (§30)

Voir `VERTEX_DESIGN_TOKENS.md` (V3) pour la structure ; ce document fixe la
palette FINALE (source : `tokens.css`).

- Fonds : obsidienne #050505→#0f1011, graphites #121315→#25282d, surfaces
  rgba(15-34, …, .97-.98).
- Texte : #f3f1ed / #b7b3ad / #817d77 / #5e5b56.
- Orange brûlé 950-400 (#3e1607→#df7739) : CTA = 600/500, hover = 700,
  sélection = 800, fond actif = 950 transparent. Grandes surfaces jamais
  orange.
- Cuivre #66321c/#914b2b/#b9683d — les LIENS sont cuivre clair.
- États : positif #38b879 · négatif #dc5f52 · warning #ce8a29 ·
  option #85609f · neutre graphique #8f8a83.
- **Zéro bleu identitaire** : aucun bouton, lien, bordure ou série
  principale bleue (tests `test_no_blue_primary_theme/buttons/main_series`,
  heuristique de dominante bleue sur chaque hex).
- Graphiques : série principale cuivrée, benchmark gris clair, secondaire
  beige/ambre, options violet limité
  (`charts/chart-theme-obsidian-copper.js`).
