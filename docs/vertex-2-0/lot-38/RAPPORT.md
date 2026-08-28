# Lot 38 — Onglets Options honnêtes : chaque onglet dit ce qu'il ouvre

## Problème (dette consignée au lot 32)

Noms croisés hérités dans la barre d'onglets d'Options :
- l'onglet « **Scanner** » ouvrait la carte « **Radar des contrats** » ;
- l'onglet « **LEAPS** » ouvrait la carte « **Scanner LEAPS** » — le vrai
  scanner du contrat (critères, lancement, « Simuler ce contrat »).

## Correctif

Libellés seulement, clés d'URL intactes (favoris et liens préservés) :
`('radar', 'Radar')` et `('leaps', 'Scanner LEAPS')`. Le commentaire
d'architecture explique que la vue `leaps` honore la sous-vue « Scanner » du
contrat (`navigation-and-pages.md` §6). Épingle historique de
test_options_structure_06 mise au niveau. SW **v278**.

## Preuves

- Banc né rouge : tests/test_options_onglets_nommage_lot38.py (3/3).
- Navigateur (DEMO) : barre mesurée « Vue d'ensemble · Structure · Volatilité
  · Radar · Scénarios · Positions · Événements · Positionnement · Scanner
  LEAPS » ; ?view=radar → « Radar des contrats — qualité décroissante » ;
  ?view=leaps → « Scanner LEAPS — quels contrats… » ; console vide.
- Suite complète : **4417 passés · 152 ignorés · 0 échec**.

## Rollback

git revert du commit unique.
