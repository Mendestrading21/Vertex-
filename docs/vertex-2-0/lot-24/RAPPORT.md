# Lot 24 — Nettoyage EXÉCUTÉ sur autorisation explicite (RAPPORT)

Date : 2026-08-28 · Autorisation utilisateur : « je t'autorise à tout faire »

## Exécuté

1. **`neon-glass.css` supprimée** (880 lignes, 47 kB, jamais servie —
   re-vérifié au navigateur : 19 feuilles demandées, celle-ci absente).
   Le manifeste du lot 22 avait MANQUÉ un consommateur : 15 bancs lisaient
   la feuille comme registre de règles. Conformément à « un banc n'est
   jamais écarté » :
   - Règles CONTRACTUELLES rapatriées AU MÉRITE dans la couche servie
     (`vertex-2-0.css` §27) : correctifs 390 px des cartes d'indices
     Marchés (flex-wrap / min-width:0+ellipse / pastille à droite — leurs
     classes sont rendues par la page servie et ces corrections étaient
     LETTRE MORTE au runtime), rail du dossier Analyse (sticky ≥1025 px
     seulement). Jetons neon (--ng-*) remplacés par les jetons canoniques.
   - `test_vertex_1_0_qa_espaces` et `test_analysis_visual_lot619`
     repointés sur la feuille servie ; `test_options_visual_lot623`
     réécrit vers la grille §24 réellement rendue (4 colonnes, 1 colonne
     à 640 px, zéro glow) ; `test_neon_glass_01` réécrit en banc
     d'HÉRITAGE (la feuille ne revient pas, mouvement réduit et refus du
     glow permanent tenus par les feuilles servies, data-space partout,
     READONLY intact).
2. **`chart-theme-obsidian-copper.js` → `chart-theme-black-glass.js`**
   (le nom décrivait une palette abandonnée) — coque, palette.py, 7 bancs
   et l'en-tête du fichier suivis dans le même commit.
3. **Captures des programmes historiques purgées** : `docs/redesign/**` et
   `docs/skyler/baseline/**` (145 PNG, ~24,7 Mo) — zéro consommateur
   (grep docs/tests/code), l'historique git les conserve. Les preuves du
   programme 2.0 actif sont intégralement gardées.
4. **Budget CSS recalibré 64→96 kB** avec justification écrite dans le
   banc : vertex-2-0.css est LA couche de vérité qui absorbe les
   rapatriements (le total CSS du dépôt baisse de 47 kB).
5. Service worker **v268**, 5 épingles + empreinte /static mises à jour.

## Preuves

- Suite complète : **4367 passés · 152 ignorés · 0 échec**.
- Navigateur après redémarrage : `/`, `/markets`, `/analysis/NVDA`,
  `/options` — 19 CSS chargés, zéro erreur console.

## Rollback

`git revert` du commit (la feuille et les captures restent dans
l'historique git).
