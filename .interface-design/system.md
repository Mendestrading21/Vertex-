# Vertex — Système d'interface canonique

> Mémoire de craft alignée sur `.claude/skills/vertex-design-2-0/SKILL.md`.
> En cas de divergence, le skill et ses références font autorité.

## Direction

**Vertex Black Glass — Signal Light** : terminal financier personnel, calme, dense, précis et strictement en lecture seule. Fond obsidienne, verre noir translucide, structure blanc/argent, très peu de couleur. Le produit ne doit ressembler ni à un template SaaS, ni à une plateforme crypto, ni à un cockpit gaming.

Signature : le V argent et le **Vertex Beam**, reflet linéaire de 1 px utilisé avec parcimonie sur un hero ou une sélection importante. Aucun glow permanent.

## Autorités d'exécution

- Tokens : `vertex/static/vertex/css/tokens.css`.
- Composants : primitives partagées VX, jamais une variante ad hoc de page.
- Graphiques : `VXCharts` + thème JS + `vertex/visualization/palette.py`.
- Pages : `vertex/ui/pages/` dans le shell commun.
- Méthode et critères : `.claude/skills/vertex-design-2-0/references/`.

Toute migration remplace progressivement les couches Signal Green, Copper, Neon Glass, Signal OS et V3. Ne pas empiler un nouveau thème.

## Couleurs

- Fond profond `#050607`, fond principal `#090b0e`, graphite `#0e1116`.
- Verre : blanc à .025/.045/.070 d'opacité ; fallback graphite.
- Texte : principal `#f5f7fa`, secondaire `#b8bec8`, discret `#7a828f`.
- Argent `#c9ced8` : structure, sélection, focus, série principale.
- Positif `#36c889` ; négatif/risque `#ed655c` ; prudence/stale `#dda23b`.
- Violet `#9c79d0` : options seulement et rarement.
- Aucun bleu identitaire, cuivre de marque, vert décoratif ou arc-en-ciel.

La séparation vient d'abord des niveaux de surface et de l'espace. Hairlines presque invisibles uniquement ; aucune bordure lourde décorative.

## Typographie

`Geist` pour l'interface ; `Geist Mono` pour tickers, prix, pourcentages, dates et mesures. Fallbacks : Inter et JetBrains Mono. Chiffres tabulaires partout. Texte visible en français clair ; titres courts ; pas de capitales longues.

## Géométrie et densité

Grille 4 px ; espaces 8/12/16/20/24/32 ; cartes 14–16 px ; contrôles 9–10 px ; grille 12 colonnes ; contenu max ~1600 px. Trois densités réelles : compact, confortable, dense. Les tables conservent unités, colonnes prioritaires et accès au détail.

## Profondeur et motion

Verre + contraste tonal + espace négatif. Ombre noire diffuse uniquement sur surfaces élevées. Hover tonal et déplacement maximal 1 px ; press .98 ; 140/200/260 ms ease-out ; aucune animation infinie ; reduced motion respecté.

## Composants

Une famille unique pour cartes, MetricCard, badges, contrôles, tables, drawers, états et ChartCard. Chaque widget de données porte question, conclusion, source, timestamp, fraîcheur et état. Loading/empty/partial/stale/delayed/offline/demo/error sont traités honnêtement.

## Navigation

Huit espaces principaux : Aujourd'hui, Marchés, Opportunités, Analyse, Portefeuille, Options, Performance, Intelligence. Journal est un raccourci de Performance ; Système est un utilitaire épinglé ; Tracking appartient à Performance ; Design System reste une route interne de QA.

## Garde-fous

READONLY intact ; aucune donnée inventée ; aucun calcul dans l'UI ; source et fraîcheur visibles ; focus clavier ; sens jamais porté par la couleur seule ; responsive 390 à 1600+ ; console vide ; tests verts ; bump service worker pour toute livraison visible.
