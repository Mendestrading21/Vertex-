# Lot 32 — Le parcours du blueprint câblé ; delta prouvé sur deux scans (RAPPORT)

Date : 2026-08-28

## Livré

1. **« Simuler le contrat » existe enfin** (action primaire d'Options du
   blueprint, jamais câblée) : le tiroir d'un candidat du scanner LEAPS
   porte « Simuler ce contrat → » avec les paramètres RÉELS
   (`sym/right/strike/dte`, prime mid = coût par contrat ÷ 100 — rien
   d'inventé : sans coût, pas de mid et le refus honnête s'applique).
   Le simulateur lit le contexte d'URL (`prefillDepuisContexte`),
   préremplit et lance — le clic en amont EST l'action explicite.
   **Vérifié de bout en bout** : LEAPS → tiroir GOOGL P 175,1 →
   `/simulator?...&mid=38.12` → matrice de scénarios calculée (coût
   3 812 $ identique au board), console vide.
2. **Refus Options en français d'interface** : « paramètres invalides
   (sym, strike, dte, mid requis) » (brut d'API) devient « …demande
   Strike, Horizon (jours) et la prime au mid — reprends-les depuis le
   scanner ou la chaîne ».
3. **Delta d'entonnoir prouvé sur deux VRAIS scans** (premier jamais
   observé) : `premier_scan: true` → rescan manuel → `baseline_ts` =
   as_of du scan 1, `premier_scan: false`, zéro entrant/sortant honnête
   (données démo stables).
4. **Compte de rescan honnête** : `/api/rescan` annonçait « 517 titres »
   en démo alors que la boucle en scanne 20 — le compte annoncé est
   désormais le compte RÉEL, avec `DEMO_UNIVERSE_N` en source unique
   (constants.py, terminal.py, scan_api.py). Banc historique réécrit vers
   ce contrat.

SW **v274**. Bancs : 4 nés rouges → verts + 1 réécrit.

## Preuves

Suite : **4417 passés · 152 ignorés · 0 échec**.

## Note d'audit consignée

L'onglet « Scanner » (= vue radar) et la vue LEAPS (= le scanner à
candidats) portent des noms croisés hérités — dette cosmétique de
nommage, consignée sans renommage d'URL (favoris).
