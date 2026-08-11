# SKYLER LOT 198 — Tournée TV : rails de Marchés — chip de valeur sur le pointeur

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-198` (base : lot 197 fusionné)

## Livré

### Bandes CALME↔STRESS et DÉFENSE↔ATTAQUE alignées (Marchés)

Les rails linéaires avaient déjà leur dégradé continu (grammaire TV
native) et leur flèche de pointeur. Le lot ajoute le maillon manquant :

1. **`cockpit.css` — `.vx-rail-chipline` / `.vx-rail-chip`** : chip de
   VALEUR posé au-dessus du pointeur du rail — fond clair
   (`--vx-text-primary`), texte sombre (`--vx-graphite-850`), gras 800,
   chiffres tabulaires — le même langage que le pointeur blanc des
   jauges (lot 189) et les chips de bord. Positionné par
   `--vx-rail-pos`, **borné aux extrémités** (`clamp`) pour ne jamais
   déborder de la carte. Classe réutilisable par tous les rails.
2. **Calme ↔ Stress (VIX)** : le chip porte la valeur RÉELLE du VIX
   (`VX.fmt.nd(vix)`) à sa position sur l'échelle 10→40.
3. **Défense ↔ Attaque (positionnement)** : le chip porte la confiance
   réelle du régime (`conf %`) — et « n/d » HONNÊTE quand le régime
   est indéterminé (jamais un pourcentage inventé sur UNKNOWN).

## Accros

Aucun.

## Preuves

- Import Python OK ; gardien de syntaxe JS inline (lot 182) couvre la
  page dans la suite.
- Serveur DEMO port 5002 : `lot198-vix-rail-card.png` (jauge VIX 12.7 +
  rail dégradé vert→rouge avec chip blanc « 12.7 » sous le pointeur),
  `lot198-position-rail-card.png` (rail positionnement, chip « n/d »
  honnête — régime démo indéterminé), pages 1440 + 390 — envoyées,
  **0 erreur console**.
- SW `td-shell-v161` → `v162` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 199 : suivant de TV-CHARTS-INVENTORY.md — price-chart niveaux,
radar, vol cone, barres S+/S/A/B, discipline Journal, aires indices,
GEX, sensibilité IV. MINI-BILAN 196-200 au lot 200.
