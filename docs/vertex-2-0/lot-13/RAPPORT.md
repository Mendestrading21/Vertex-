# Lot 13 — Options et simulateur multi-actifs (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Conclusion d'audit

La consolidation demandée était largement ACQUISE (propriétaires uniques
mesurés : chaîne, identité contrat `contract_id`, unités `iv_units`,
filtres, GEX sur gamma source unique, scénarios `scenario_pricer` [2 routes
→ 1 moteur], recommandations, simulateur `/simulator` composant les 4
moteurs — jambe `stock` ⇒ Actions/ETF ; Forex = absence honnête). Le lot
livre ce qui MANQUAIT mesurablement : la preuve d'accord de la troisième
implémentation BS et la déclaration de devise.

## Livré

1. **Accord inter-moteurs verrouillé** : `multileg_lab._leg_greeks` ↔
   `legacy_engine._greeks` coïncident à 1e-9 sur delta/gamma/theta/vega
   (4 cas : ATM court, OTM 6 mois, ITM, haute vol 1 an — call ET put),
   taux par défaut épinglés égaux (0.045). La boucle est fermée :
   legacy ↔ scenario_pricer (existant) + legacy ↔ multileg (nouveau).
2. **Propriétés** : parité call/put des Greeks multileg (Δc−Δp=1, γ/vega
   identiques) ; parité des prix legacy (C−P = S−K·e^(−rT)) ; jambe stock
   linéaire (delta=qty, multiplicateur 1 vs 100) ; multiplicateur porté
   dans le P&L à l'échéance (attendu exact au point de grille).
3. **Devise déclarée** (né ROUGE → vert) : le bloc `model` de
   `analyze_strategy` porte `currency: 'USD'` + note « aucune conversion
   n'existe ni n'est estimée ». Zéro changement de calcul.

## Preuves

- `tests/test_options_convergence_lot13.py` : 6 bancs (5 caractérisations
  attendues vertes — DITES ; 1 né rouge devise → vert).
- Suite complète : **4360 passés · 153 ignorés · 0 échec** (136 s).

## Limites consignées

- Bibliothèque de pricing externe : uniquement via PR moteur dédiée (ADR).
- Multi-devises réel : aucun besoin reproduit (options US) — refus honnête.
- `scenario_pricer` ne porte pas de bloc devise équivalent (sa sortie est
  en % du sous-jacent, pas en montants) — non requis, consigné.
- Widgets simulateur (matrice, payoff…) : phase D.

## Rollback

`git revert` du commit du lot.
