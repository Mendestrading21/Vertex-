# SKYLER V2 — LOT 58 : polish Portefeuille + Options (ancienne palette purgée)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-58-polish-portfolio-options`
(base : `integration/vertex-skyler-v2` @ `9d6a328`, fraîchement fetchée) ·
Mode : arc « jusqu'au lot 60 » (5/7).

## 1. Inspection systématique (leçons lots 56-57)

Recherche ciblée des littéraux hors palette et des troncatures dans
`portfolio_page.py` et `options_intel_page.py` (la page servie par
`/options`). Trouvaille principale — un défaut ACTIF, pas dormant :

## 2. `/options` rendait réellement une ANCIENNE palette

`options_intel_page.py` portait ~28 fallbacks `var(--token,#hex)` d'une
ancienne palette chaude — dont l'**orange banni `#cf6128`** (tag démo) et
le cuivre `#b9683d`. Surtout : le token `--vx-text-dim` **n'existe pas**
dans tokens.css — son fallback `#8a837a` (gris chaud périmé) se rendait
donc RÉELLEMENT sur tous les textes atténués de la page. Corrigé :

- `--vx-text-dim` (inexistant) → `--vx-text-muted` / `--vx-text-secondary`
  (tokens réels) avec fallbacks aux valeurs actuelles ;
- tous les fallbacks réalignés sur les valeurs ACTUELLES des tokens
  (#F8F5F3, #BABABA, #8A8284, #2BBE90, #E9555F, #30292B, #0c0c0e,
  #121214) ;
- tag démo : couple orange → `var(--vx-warning,#D9BE3C)` (sémantique
  attention/démo, cohérent avec le badge DÉMO du briefing) ;
- `--vx-copper-light` → `var(--vx-brand,#DBE1E8)` (l'alias pointait déjà
  sur la marque).

## 3. `/portfolio` : 4 fallbacks périmés + libellé ellipsé

Fallbacks `#b7b2aa/#17191c/#dc6255/#39b878` réalignés sur la palette
actuelle. Le libellé de scénario (colonne fixe 150 px du graphique de
barres, ellipsé par construction) reçoit un `title` : l'information
complète est accessible au survol sans casser l'alignement (l'aria-label
la portait déjà pour les lecteurs d'écran).

## 4. Tests (rouges d'abord — 5 nouveaux)

`tests/test_polish_lot58.py` (rouge 5/5 confirmé) : tout fallback
`var(--x,#hex)` des deux pages doit appartenir aux valeurs ACTUELLES ·
`--vx-text-dim` absent + orange/cuivre bannis absents · libellé ellipsé
avec `title` · SW ≥ v115 et v114 absent.

## 5. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1666 passed, 2 skipped   (1661 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v115 servi,
  cycle souverain inclus)
Preuve navigateur APRÈS (balayage COMPLET des couleurs calculées) :
  aucun élément de /options ni /portfolio ne rend une couleur de
  l'ancienne palette (14 valeurs RGB périmées recherchées sur tous les
  éléments de #vx-content) — « palette OK » sur les deux pages,
  0 erreur console. Capture /options conservée.
```

SW `td-shell-v114` → `td-shell-v115` + 4 gardiens.

## 6. Invariants

READONLY intact · aucun moteur touché · zéro littéral couleur NOUVEAU
(28 littéraux périmés REMPLACÉS par les valeurs canoniques, 2 bannis
supprimés) · `main` intacte · fichiers runtime non commités.

## 7. Suite (arc)

Lot 59 : polish Journal + Système + cohérence transversale des états
vides/erreur. Puis 60 = RC finale + bilan consolidé n°4 + ARRÊT.

**Arrêt après ce lot — validation humaine requise.**
