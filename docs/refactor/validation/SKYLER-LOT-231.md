# SKYLER LOT 231 — Palette de commande : constat comportemental complet (0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-231` (base : lot 230 fusionné)

## Objet

La palette de commande (⌘K, §14 du shell) n'avait JAMAIS été testée en
navigateur — uniquement par présence de littéraux dans la source.
Déroulé du vrai parcours clavier, en démo.

## Protocole (Playwright, DEMO, 1440×900, page `/`)

Ctrl+K → filtrage (`march`) → flèches bas ×2 / haut ×1 → Échap →
clic sur la barre de recherche → Échap → Ctrl+K + `archive` + Entrée.
À chaque étape : `data-open`, nombre d'items, item sélectionné
(aria-selected), focus dans l'input, groupes rendus, URL finale.

## Résultat — 0 défaut, parcours exemplaire

| Étape | Mesuré |
|---|---|
| Ctrl+K | ouverte, input focusé, **11 items** en 3 groupes (Positions / Pages / Actions), 1er sélectionné ✔ |
| Filtre `march` | 4 items (groupe Pages seul), sélection réinitialisée ✔ |
| ↓ ↓ | sélection → idx 2 « Marchés · Volatilité » (aria-selected suit) ✔ |
| ↑ | sélection → idx 1 « Marchés · Secteurs » ✔ |
| Échap | fermée (open=0), focus rendu ✔ |
| Clic barre de recherche | ouverte à nouveau (le blur→openPalette fonctionne) ✔ |
| `archive` + Entrée | **navigation réelle** vers `/system?view=archive`, palette fermée ✔ |
| Erreurs console | 0 ✔ |

À noter : en démo la palette liste bien la position réelle du store
(ACN) dans le groupe Positions — le câblage VXEntities est vivant, pas
décoratif.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : constat pur.

## Preuves

- JSON du parcours complet (8 états) produit par le protocole ;
  synthèse ci-dessus.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 232 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
