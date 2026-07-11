# Vertex UI V3 — Limitations connues

Complète `VERTEX_KNOWN_LIMITATIONS.md` (produit) pour la couche interface.

1. **Alias tokens legacy conservés** (`--vx-bg`, `--vx-blue`, `--vx-*-dim`)
   — mappés sur les tokens V3 le temps que chaque page consomme les noms
   canoniques ; à retirer lors d'une passe ultérieure.
2. **Réordonnancement des widgets** : la personnalisation du Briefing
   permet masquer/densité — pas de drag-and-drop libre (choix produit :
   grille contrôlée, ordre des rangées fixe).
3. **Widgets macro (DXY, pétrole, or, BTC, taux)** : le scan démo ne
   fournit pas ces séries — la carte cross-asset affiche « n/d » honnête ;
   avec IBKR/TWS branché, les valeurs se remplissent.
4. **Candlesticks** : uniquement si des barres OHLC complètes sont
   fournies par les moteurs — sinon repli clôtures étiqueté.
5. **Heatmap mensuelle & distribution (Performance)** : moyennes simples
   des % par trade déclaré — pas une performance composée ni un benchmark
   (SPY n'est pas disponible côté client — aucune comparaison inventée).
6. **Term structure / smile / gamma** : rendus seulement quand la chaîne
   IBKR les fournit ; en démo, la surface de vol refuse honnêtement
   (« historique IV insuffisant »).
7. **Virtualisation des tableaux** : bornage à 80 lignes + tri/filtres —
   pas de virtual scrolling (aucune table > 500 lignes dans l'univers
   actuel).
8. **Export** : JSON desk + vault ; pas d'export CSV/PNG par widget
   (fonction absente des moteurs — non simulée).
9. **`?view=compare`** d'Analyse : accepté mais non exploité — le
   comparateur multi-titres reste redirigé vers la recherche.
10. **Bruit de fond optionnel** non implémenté (texture) — les halos +
    vignettage suffisent sans risquer la lisibilité.
