# Lot 13 — Options et simulateur multi-actifs (WORK_MANIFEST)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Constat mesuré (audit préalable)

La convergence demandée est LARGEMENT ACQUISE par les programmes antérieurs
— propriétaires uniques mesurés :

| Capacité | Propriétaire unique | Preuve existante |
|---|---|---|
| Chaîne | `vertex/options/chain_loader.py` + `chaine_a_la_demande.py` | tests chaîne |
| Identité contrat | `quote_resolver.contract_id` (symbole seul refusé : ambigu) | test_refus_honnete |
| Unités IV | `iv_units.from_legacy_board` (frontière unique étiquetée) | multileg:529-566 |
| Filtres | `contract_filter.py` | bancs dédiés |
| Greeks/BS | legacy_engine (+ `gamma` source unique du GEX), scenario_pricer, multileg `_leg_greeks` | golden BS + parité + accord legacy↔scenario_pricer |
| GEX | `gex.py` (gamma importé de la source unique) | bancs GEX |
| Scénarios | `scenario_pricer.simulate` (2 routes → 1 moteur) | golden scénarios + refus DTE |
| Recommandations | `recommendation.py`, `rank_strategies` (mandat) | bancs |
| Simulateur consolidé | page `/simulator` compose les 4 moteurs propriétaires (scenario_pricer, multileg [jambe stock ⇒ Actions/ETF], pretrade, portfolio_stress) ; Forex = absent HONNÊTE | simulator_page.py:1-50 |

**Trous mesurés restants** :

1. **Accord inter-moteurs incomplet** : `test_legacy_and_new_bs_agree` couvre
   legacy ↔ scenario_pricer, mais la TROISIÈME implémentation
   (`multileg_lab._leg_greeks`) n'est comparée à personne — une dérive
   silencieuse entre le labo multi-jambes et le reste serait invisible.
   (r=0.045 et q=0 identiques des deux côtés — l'accord est attendu.)
2. **Parité call/put des Greeks multileg** non testée (delta_C − delta_P =
   e^(−qT) ; gamma/vega identiques).
3. **Devise jamais déclarée** : `_net_premium` et les P&L multileg sont « en
   dollars » implicites ; le bloc `model` ne porte pas `currency`. Aucune
   conversion n'existe (c'est bien) mais l'hypothèse USD n'est pas DITE.

## Fichiers propriétaires

- `vertex/engines/multileg_lab.py` — `'currency': 'USD'` + note dans le bloc
  `model` (déclaration, zéro changement de calcul).
- **NEUF** `tests/test_options_convergence_lot13.py` — accord inter-moteurs
  (caractérisations attendues vertes, DITES), parité, devise (né rouge).

## Hors périmètre (consigné)

- Bibliothèque de pricing externe : uniquement via PR moteur dédiée (ADR).
- Multi-devises réel : aucun besoin reproduit (US only) — refus honnête.
- Widgets simulateur : phase D.

## Rollback

`git revert` du commit du lot.
