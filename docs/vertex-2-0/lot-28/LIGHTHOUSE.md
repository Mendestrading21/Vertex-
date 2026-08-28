# Lighthouse — mesures réelles et budgets (lot 28, ticket VX2-LIGHTHOUSE)

Date : 2026-08-28 · Lighthouse (npm, Chromium /opt/pw-browsers) · émulation
mobile standard (slow 4G simulé, CPU ×4) · serveur démo local, mode dégradé
(réseau sortant coupé — donnée absente honnête).

| page | perf | a11y | best-practices | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|
| accueil | 69 | 100 | 100 | 3.5 s | 7.0 s | 40 ms | 0 |
| analysis | 68 | 100 | 100 | 3.6 s | 6.7 s | 60 ms | 0 |
| calendar | 71 | 100 | 100 | 3.2 s | 6.4 s | 70 ms | 0 |
| follow-up | 71 | 100 | 100 | 3.2 s | 6.4 s | 0 ms | 0 |
| intelligence | 70 | 100 | 100 | 3.3 s | 6.3 s | 60 ms | 0 |
| markets | 70 | 100 | 100 | 3.3 s | 6.6 s | 60 ms | 0 |
| opportunities | 70 | 100 | 100 | 3.4 s | 6.8 s | 30 ms | 0 |
| options | 69 | 100 | 100 | 3.2 s | 7.4 s | 70 ms | 0 |
| performance | 69 | 100 | 100 | 3.5 s | 6.5 s | 10 ms | 0 |
| portfolio | 69 | 100 | 100 | 3.3 s | 6.9 s | 40 ms | 0 |
| simulator | 71 | 100 | 100 | 3.2 s | 6.2 s | 20 ms | 0 |
| system | 69 | 100 | 100 | 3.3 s | 6.8 s | 90 ms | 0 |

## Correctifs issus de ce passage (nés rouges → verts, SW v270)

- **heading-order** (accueil, simulateur) : le titre de carte vx2 était un
  `<h3>` directement sous le `<h1>` de page — passé en `<h2>` (propriétaire
  unique vx2.py, styles par classe inchangés). A11y : 98/99 → **100**.
- **target-size** (performance) : `<summary>` repliables sous 24 px —
  cible tactile minimale posée dans la couche finale. A11y : 96 → **100**.

## Budgets approuvés (contrôle 131 — régression = échec)

| catégorie | minimum mesuré | budget (plancher) |
|---|---|---|
| performance | 68 | **≥ 65** |
| accessibilité | 100 (après correctifs) | **≥ 98** |
| best-practices | 100 | **≥ 95** |
| CLS | 0 partout | **≤ 0,02** |

Lecture des scores perf (68-71) : l’émulation mobile ralentie paie la
chaîne de 19 feuilles CSS (LCP 6-7 s simulés). Piste d’amélioration
nommée, hors périmètre du ticket : concaténation/inline critique des
feuilles — un lot performance dédié, jamais un raccourci discret.

Reproduction : `npx lighthouse http://127.0.0.1:5002/<page>
--only-categories=performance,accessibility,best-practices
--chrome-flags="--headless=new --no-sandbox"` (CHROME_PATH=Chromium).
