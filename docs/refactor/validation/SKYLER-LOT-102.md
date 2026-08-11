# SKYLER V2 — LOT 102 : boucle continue — gardien XSS des news figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-102`
(base : `integration/vertex-skyler-v2` @ `da162b2`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

La règle n°5 du projet — « tout texte externe passe par
`news_plus.sanitize_news()` avant d'être servi (rendu en innerHTML) » —
n'était testée qu'INDIRECTEMENT au point de sortie d'une route
(test_events_timeline). Le gardien lui-même (échappement, schémas de
liens, balises cassées), le sentiment lexical, le parse RSS et la
déduplication n'avaient AUCUN test direct.

## 2. Les 9 comportements figés (nés verts, dits — zéro réseau)

```text
<script> retiré PUIS méta-caractères échappés (& " ' < >) — sûr en
  innerHTML, en attribut ET en chaîne JS inline                        OK
balise JAMAIS fermée (<img onerror=…) → sort inerte (le < est encodé,
  rien à interpréter côté navigateur)                                  OK
liens : javascript:/data: SUPPRIMÉS (None) · http(s) seul autorisé
  (insensible à la casse, espaces tolérés) · quotes/chevrons
  pourcent-encodés (sûr en href ET window.open)                        OK
non-dicts ignorés · clés non textuelles préservées telles quelles ·
  None → []                                                            OK
sentiment lexical FR/EN : positif +1, négatif -1, mixte égal 0,
  vide/None 0                                                          OK
aggregate : arrondi 2 décimales, senti absent compte 0, item sans
  sym ignoré                                                           OK
parse_rss : suffixe « - Éditeur » retiré du titre, publisher extrait,
  cap n respecté                                                       OK
XML pourri ou titres vides → [] — jamais une exception qui remonte     OK
dedupe : même titre NORMALISÉ (casse/ponctuation) ou même lien → le
  premier conservé tel quel, ordre préservé, non-dicts ignorés         OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1856 passed, 2 skipped   (1847 + 9)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 103 : angle suivant ; lot 105 = mini-bilan tournée 101-105.
