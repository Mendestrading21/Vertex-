# Règles de design Vertex

1. **Tokens uniquement.** Jamais de couleur/rayon/espacement en dur dans une page. Utiliser les variables
   `--vx-*` (source : `vertex/static/vertex/css/glass.css`, dérivées de `tokens.css`). Nouveau besoin → nouveau
   token sémantique, pas un hex.
2. **Palette sémantique STRICTE** (« une couleur = une signification », `tokens.css:3-8`) :
   vert `#36c889` = positif/validation · rouge/corail `#ed655c` = négatif/perte/alerte · orange/ambre `#dda23b` =
   incertitude/prudence · **argent `#c9cdd4` = structure/marque/neutre** · **violet `#9c79d0` = OPTIONS uniquement**.
   **Zéro bleu** (`--vx-info`/`--vx-blue` remappés argent/acier). Une même sémantique = une même couleur sur toutes
   les pages et graphiques.
3. **Pas d'hex moteur.** Les moteurs renvoient parfois `state_col` (dont du bleu) → toujours mapper `state` →
   `C.colors`, jamais l'hex brut.
4. **Cartes = système partagé.** Dériver de `vx-card` + modificateurs. Ne pas créer une carte ad hoc si une
   variante existe. (Dette connue à consolider : `.vx-card` redéfini 8× ; 4 systèmes de tuiles KPI `vx-kpi`/
   `vx-metric`/`vx-stat`/`vx-stat-xl` → fusionner en un MetricCard. Voir `docs/vertex-audit/05-component-inventory.md`.)
5. **Graphiques = `VXCharts` + contrat.** source · timestamp · question · conclusion · état vide honnête ·
   palette `C.colors`. Jamais deux couleurs pour une même sémantique.
6. **Typo & format centralisés.** Échelle `--vx-fs-*` ; chiffres tabulaires (`.vx-mono`/`tabular-nums`) alignés à
   droite ; formats via `VX.fmt.*`.
7. **Densité maîtrisée.** compact = tableaux ; confortable = cartes de décision. Badges/jauges/sparklines plutôt
   que du texte partout.
8. **Accessibilité.** Contraste AA ; focus visible ; clavier ; le risque ne dépend jamais UNIQUEMENT du rouge/vert
   (ajouter signe/icône/label).
9. **Service worker.** Tout changement de shell visible → bump `td-shell-vN` (`vertex/app/routes/system.py`) +
   mettre à jour les tests qui l'épinglent.
10. **Docs de design périmées** (`VERTEX_DESIGN_TOKENS.md`, `VERTEX_CHART_LIBRARY.md` décrivent une palette
    orange/bleu abandonnée) : ne PAS s'y fier ; la vérité runtime = `glass.css` (Black Glass). À corriger.
