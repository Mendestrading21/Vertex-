# Lot 31 — Interactions peuplées vérifiées ; le simulateur tient sa promesse (RAPPORT)

Date : 2026-08-28

## Interactions vérifiées au navigateur (mode démo peuplé, console vide partout)

| Interaction | Résultat |
|---|---|
| Palette de commandes (Ctrl+K) → « simul » → Entrée | navigue vers /simulator |
| Opportunités : carte Top → « Analyser » | navigue vers /analysis/ACN |
| Dossier ACN : copilote (repli déterministe) | réponse ancrée dans le récit dealer réel, étiquetée ; case « inclure mes positions » présente et DÉCOCHÉE (contrat PII vivant) |
| Dossier ACN : ticket pré-trade 5 000 $ | verdict DÉFAVORABLE motivé (comité ✓, régime RISK-OFF ✕, dealer ✓) |
| Simulateur Actions : ACN × 10 | calcul complet — engagement 1 980 $, point mort 198,00, table théorique |

## Défaut trouvé et corrigé (né rouge)

**Le simulateur contredisait sa propre page** : classe Actions, titre
présent au scan, quantité saisie → « Simulation impossible : demande…
un prix de référence », alors que les Hypothèses de la page promettent
« le prix de référence est le prix RÉEL du scan courant ». Corrigé
(`simulator.js`) : le prix vient du scan quand il existe (198,00 $ ACN
mesuré), la saisie manuelle PRIME (déclaration utilisateur), le refus ne
subsiste que sans l'un ni l'autre — avec un message qui nomme la vraie
cause. La **provenance est DITE** dans le résultat (« Prix de référence :
prix du scan courant (198 $) » — vérifié en direct). Au passage : le titre
de résultat passe h3→h2 (même règle heading-order que le lot 28).

`tests/test_simulateur_prix_scan_lot31.py` (3 bancs). SW **v273**.

## Preuves

Suite : **4418 passés · 152 ignorés · 0 échec**.
