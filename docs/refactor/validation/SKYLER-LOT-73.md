# SKYLER V2 — LOT 73 : PROGRAMME 100 % — accessibilité, angles restants

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-73-a11y`
(base : `integration/vertex-skyler-v2` @ `12a9ddb`, fraîchement fetchée).

## 1. Balayage outillé (8 pages, Playwright)

Angles NON couverts par les lots passés (64/65) : noms accessibles des
boutons et liens, labels des inputs, focusabilité clavier des contrôles
non natifs. Résultat AVANT : 7 pages à **0 défaut** ; **4 défauts réels**
sur /opportunities.

## 2. Défaut réel corrigé : tickers inutilisables au clavier

Les tickers cliquables (`span.sym vx-ticker` avec `data-open-analysis` —
dominante + shortlist + vue détail) n'étaient PAS focusables (span sans
tabindex), et la délégation globale de vx-entities.js n'écoutait que
`click` : un utilisateur clavier ne pouvait PAS ouvrir l'analyse depuis
Opportunités. Corrigé :

- `role="button" tabindex="0"` sur les 3 gabarits de tickers cliquables
  d'opportunities_page.py ;
- délégation clavier GLOBALE dans vx-entities.js : Enter/Espace activent
  tout `[data-open-analysis]/[data-entity-menu]/[data-position-menu]`
  non natif (même chemin que le clic) — prospectif, couvre les usages
  futurs sur toutes les pages.

Preuve APRÈS : balayage 8 pages → **TOTAL défauts a11y = 0**.

## 3. Tests (rouges d'abord — 3, dont un durci en cours de lot, dit)

`tests/test_a11y_lot73.py` : tout ticker cliquable porte tabindex ·
délégué keydown document présent et couvrant data-open-analysis (le
1er jet du test passait sur des sous-chaînes sans rapport — durci en
slice du délégué) · SW ≥ v124.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1702 passed, 2 skipped   (1699 + 3)
Balayage a11y APRÈS → 0 défaut (8 pages)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut
Responsive 8 × 3 → 0 débordement, 0 erreur
```

SW `td-shell-v123` → `td-shell-v124` + 4 gardiens (v123 absent).

## 5. Suite

Lot 74 : robustesse données limites, puis lot 75 = RC FINALE + BILAN n°6
+ déclaration 100 %.
