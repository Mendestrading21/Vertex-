# Vertex — Limitations (Ultimate)

Reprend et met à jour `VERTEX_KNOWN_LIMITATIONS.md` (produit) et
`VERTEX_UI_KNOWN_LIMITATIONS.md` (interface). Ajouts de cette passe :

1. **Actualités en environnement cloud** : le flux (yfinance/RSS) exige le
   réseau — en démo le Brief déclare « flux hors ligne » au lieu d'inventer.
   En local avec réseau, le pipeline valide/déduplique/classe réellement.
2. **Greeks agrégés du portefeuille** : broker uniquement — sans IBKR ils
   restent n/d (jamais une somme de modèles présentée comme exposition).
3. **Scénarios dans le drawer position option** : renvoyés vers le desk
   options (exigent IV + spot frais) — le payoff (arithmétique) est tracé.
4. **Graphe d'impact (§27)** : la vue Impacts montre le flux d'événements
   réel et la chaîne d'impact ; la propagation automatique
   événement→recalcul complet est partielle (change_detector fournit
   recalc_required ; le déclenchement systématique reste manuel/scan).
5. **Jobs « jamais exécuté »** : PREMARKET/INTRADAY/CLOSE_BRIEF et
   POSITION_REFRESH n'émettent pas encore de battements propres (brief à
   la demande, cotations par requête) — affichés honnêtement comme tels.
6. **Deep link IBKR** : pas de lien fiable universel — l'UI propose la
   copie du contrat (conId/ticker/strike/échéance), jamais un lien fictif.
7. Virtualisation des tables, export CSV/PNG par widget : non implémentés
   (voir limitations UI V3).
