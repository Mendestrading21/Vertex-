# SKYLER V2 — INDEX DES LOTS INSTITUTIONAL+ ET DU TRAVAIL CONTINU

> Branche d'intégration : `integration/vertex-skyler-v2` · `main` jamais touchée.  
> Chaque lot : tests rouges d'abord → moteur → suite complète verte → rapport → PR fusionnée.  
> Historique des versions de moteur : chaque changement de règle = bump ; les décisions figées restent liées à leur version (jamais recalculées).

## Lots Institutional+ (10 → 12)

| Lot | Rapport | Objectif | Moteur | SW | Tests (fin de lot) | Verdict |
|---|---|---|---|---|---:|---|
| 10 | `SKYLER-LOT-10.md` | Mémoire décisionnelle immuable (ledger 31 champs, anti-look-ahead, taxonomie d'erreurs, 10 biais) | 0.1.0 | v94 | 1332 | GO |
| 11 | `SKYLER-LOT-11.md` | Knowledge Graph prouvable (4 relations sourcées, propagation explicable, questions de recherche) | 0.1.0 | v94 | 1350 | GO |
| 12 | `SKYLER-LOT-12.md` | Red-team obligatoire S/S+, batterie adversariale, RC | 0.2.0 | v94 | 1367 | GO AVEC RÉSERVES |

## Travail continu (13 → 23)

| Lot | Rapport | Objectif | Moteur | SW | Tests | Verdict |
|---|---|---|---|---|---:|---|
| 13 | `SKYLER-LOT-13.md` | États opérationnels + confiance factorisée (plafonds §7) | 0.3.0 | v94 | 1386 | GO |
| 14 | `SKYLER-LOT-14.md` | Producteur red-team déterministe (10 questions fondées ou UNANSWERED) | 0.4.0 | v94 | 1398 | GO |
| 15 | `SKYLER-LOT-15.md` | Série datée par séance — horizons réels de la mémoire | 0.4.0 | v94 | 1410 | GO |
| 16 | `SKYLER-LOT-16.md` | Surfaçage UI : carte Mémoire + Dépendances cachées | 0.4.0 | v95 | 1416 | GO |
| 17 | `SKYLER-LOT-17.md` | Corrélation partielle vs SPY (résidus étiquetés) + groupes ≥ 3 | 0.4.0 | v96 | 1427 | GO |
| 18 | `SKYLER-LOT-18.md` | Robustesse MESURÉE par 11 perturbations fixes | 0.5.0 | v96 | 1438 | GO |
| 19 | `SKYLER-LOT-19.md` | Calibration réelle (scenario hit rate, seuil 20 mesures, borné [0,50, 0,90]) | 0.6.0 | v96 | 1450 | GO |
| 20 | `SKYLER-LOT-20.md` | Drill-down + post-mortem par décision (containment des scénarios) | 0.6.0 | v97 | 1463 | GO |
| 21 | `SKYLER-LOT-21.md` | Repricing spot×IV red-team (pricer BS canonique, F3 chiffré) | 0.6.0 | v97 | 1472 | GO |
| 22 | `SKYLER-LOT-22.md` | Calibration PAR CONTEXTE (§13 — cellule niveau/décision, portée explicite) | 0.7.0 | v97 | 1481 | GO |
| 23 | `SKYLER-LOT-23.md` | Vue lisible du post-mortem (`/memory/<id>`, XSS échappé) + cet index | 0.7.0 | v98 | 1488 | GO |
| 24 | `SKYLER-LOT-24.md` | Exposition sectorielle du portefeuille + concentration sectorielle des groupes | 0.7.0 | v99 | 1498 | GO |
| 25 | `SKYLER-LOT-25.md` | Revue de simplification (docstrings 0.7.0, dédup calibration/mesure/red-team) — zéro changement de comportement | 0.7.0 | v99 | 1498 (identique) | GO |
| 26 | `SKYLER-LOT-26.md` | Calibration par RÉGIME (régime figé, by_regime, priorité niveau → régime → global) | 0.8.0 | v100 | 1508 | GO |
| 27 | `SKYLER-LOT-27.md` | RC courte du travail continu — audit complet 13 → 26 (aucun code moteur) | 0.8.0 | v100 | 1508 | GO AVEC RÉSERVES |
| 28 | `SKYLER-LOT-28.md` | Découpe by_catalyst (observation) + propagation 1–3 sauts avec garde de volume dite | 0.8.0 | v100 | 1515 | GO |
| 29 | `SKYLER-LOT-29.md` | Export souverain de la mémoire (`/api/skyler/memory/export`, lecture seule prouvée, bouton Exporter) | 0.8.0 | v101 | 1522 | GO |
| 30 | `SKYLER-LOT-30.md` | catalyst_kind figé au freeze (fait du moteur events, jamais re-parsé) + découpe by_catalyst_type (observation) | 0.9.0 | v101 | 1531 | GO |
| 31 | `SKYLER-LOT-31.md` | Fuzz déterministe des chemins récents — 7 crashs réels trouvés et corrigés en refus honnêtes | 0.9.0 | v101 | 1543 | GO |
| 32 | `SKYLER-LOT-32.md` | RC courte périodique outillée (`tools/rc_short_audit.js`) — 8 pages, 0 défaut, client-log 0, SW v101 servi | 0.9.0 | v101 | 1543 | GO |
| 33 | `SKYLER-LOT-33.md` | by_catalyst/by_catalyst_type dans la carte Mémoire (même mécanique badges, « observation » dit) + RC courte GO | 0.9.0 | v102 | 1547 | GO |
| 34 | `SKYLER-LOT-34.md` | Fuzz HTTP graphe/mémoire — 4 crashs 500 réels corrigés (magasin corrompu servi en refus honnête, jamais 500) | 0.9.0 | v102 | 1555 | GO |
| 35 | `SKYLER-LOT-35.md` | Santé du ledger (`ledger_health` : doublons/orphelins/mélanges de versions/corruption — dit, jamais réparé) + badge UI | 0.9.0 | v103 | 1565 | GO |
| 36 | `SKYLER-LOT-36.md` | Fuzz du cœur HTTP `/api/skyler/<sym>` — 0 défaut (route déjà robuste, contrat documenté par les tests) | 0.9.0 | v103 | 1572 | GO |
| 37 | `SKYLER-LOT-37.md` | Fraîcheur du ledger (dernière décision figée, J-N calendaire UTC) — défaut J-1 attrapé en preuve navigateur | 0.9.0 | v104 | 1576 | GO |
| 38 | `SKYLER-LOT-38.md` | Bilan consolidé lots 29-37 en tête de STATUS (synthèse sourcée pour la validation humaine — documentaire) | 0.9.0 | v104 | 1576 | GO |
| 39 | `SKYLER-LOT-39.md` | Drill-down cellule de calibration (`cell_decisions`, règle d'appartenance en source unique, badges cliquables) | 0.9.0 | v105 | 1586 | GO |
| 40 | `SKYLER-LOT-40.md` | Vue HTML lisible de la cellule (`/memory/cell/…`, markupsafe prouvé sur contenu hostile, 404 lisibles, badges → vue) | 0.9.0 | v106 | 1593 | GO |
| 41 | `SKYLER-LOT-41.md` | RC courte étendue au parcours mémoire (décision → /memory/<id> → cellule ou 404 lisible dit) — GO, défaut d'outil (casse CSS) corrigé | 0.9.0 | v106 | 1593 | GO |
| 42 | `SKYLER-LOT-42.md` | Intégrité de l'export souverain (ledger_health embarqué + content_sha256 canonique vérifiable hors ligne) | 0.9.0 | v106 | 1599 | GO |
| 43 | `SKYLER-LOT-43.md` | Fuzz clés encodées des routes cellule (2 routes, 0 défaut — trou de couverture du lot 36 fermé, non-interférence prouvée) | 0.9.0 | v106 | 1606 | GO |
| 44 | `SKYLER-LOT-44.md` | Bilan consolidé n°2 (29→43) en tête de STATUS + bascule dite vers RC périodiques espacées (backlog code épuisé) | 0.9.0 | v106 | 1606 | GO |
| RC1 | `SKYLER-RC-PERIODIQUE-1.md` | RC périodique n°1 — suite complète + audit navigateur 8 pages + parcours mémoire : GO, 0 défaut, baseline tenue | 0.9.0 | v106 | 1606 | GO |
| RC2 | `SKYLER-RC-PERIODIQUE-2.md` | RC périodique n°2 — suite complète + audit navigateur 8 pages + parcours mémoire : GO, 0 défaut, baseline tenue | 0.9.0 | v106 | 1606 | GO |
| RC3 | `SKYLER-RC-PERIODIQUE-3.md` | RC périodique n°3 — suite complète + audit navigateur 8 pages + parcours mémoire : GO, 0 défaut, baseline tenue | 0.9.0 | v106 | 1606 | GO |
| 45 | `SKYLER-LOT-45.md` | Restauration souveraine (`POST /api/skyler/memory/import` — empreinte vérifiée avant écriture, rejeu append-only, historique local gagne) | 0.9.0 | v106 | 1615 | GO |
| 46 | `SKYLER-LOT-46.md` | Restauration étendue séances + journal (rejeu honnête, donnée locale gagne, triple de dédup en source unique, périmètre complet) | 0.9.0 | v106 | 1622 | GO |
| 47 | `SKYLER-LOT-47.md` | Bouton Importer (flux fichier réel prouvé en navigateur) + empreinte stable au round-trip JS (défaut réel 100.0→100 corrigé) | 0.9.0 | v107 | 1627 | GO |
| 48 | `SKYLER-LOT-48.md` | Cycle souverain dans la RC outillée (export → altération refusée dite → restauration par le vrai bouton) — re-prouvé à chaque RC | 0.9.0 | v107 | 1627 | GO |
| 49 | `SKYLER-LOT-49.md` | Bilan consolidé n°3 (29→48) en tête de STATUS + bascule en RC périodiques espacées (cycle souverain fermé) | 0.9.0 | v107 | 1627 | GO |
| RC4 | `SKYLER-RC-PERIODIQUE-4.md` | RC périodique n°4 — première RC avec cycle souverain (altération refusée + restauration bouton) : GO, 0 défaut | 0.9.0 | v107 | 1627 | GO |
| 50 | `SKYLER-LOT-50.md` | Profilage routes chaudes (toutes < 15 ms p95, double calcul vérifié : 0,7 ms/7,4 %) — NO-GO optimisation dit, baseline publiée | 0.9.0 | v107 | 1627 | GO |
| 51 | `SKYLER-LOT-51.md` | Graphiques niveau app 2026 (lissage monotone jamais de faux extrêmes, dégradé 3 arrêts, glow, pastille dernier prix) — central `C.area`, zéro fork | 0.9.0 | v108 | 1633 | GO |
| 52 | `SKYLER-LOT-52.md` | Crosshair app au survol (`vxCrosshair` : visée verticale + point actif, jamais hors survol) + `multiLine` harmonisé signature 2026 | 0.9.0 | v109 | 1638 | GO |
| 53 | `SKYLER-LOT-53.md` | Sparkline/bars/donut sur la signature 2026 (mini-aire dégradée, barres arrondies pleines au survol, donut arcs espacés) — tronc commun complet | 0.9.0 | v110 | 1643 | GO |
| 54 | `SKYLER-LOT-54.md` | Prix d'Analyse (signature complète + pastille) & chandeliers 2026 (corps arrondis, mèches 1 px, visée) — défaut réel axe Y à 0 corrigé | 0.9.0 | v111 | 1650 | GO |
| 55 | `SKYLER-LOT-55.md` | Connexions entre pages : fil d'Ariane cliquable (serveur + SPA, source unique) + retour contextuel couvrant les 8 espaces | 0.9.0 | v112 | 1655 | GO |
| 56 | `SKYLER-LOT-56.md` | Polish Aujourd'hui+Marchés : séries comparées contrastées (cyan technique, 3 miroirs alignés par la source) + crumb mobile sans slash orphelin | 0.9.0 | v113 | 1658 | GO |
| 57 | `SKYLER-LOT-57.md` | Polish Opportunités+Analyse : libellés kv jamais tronqués (perte d'info corrigée) + littéral hors palette supprimé (étoile → token) | 0.9.0 | v114 | 1661 | GO |
| 58 | `SKYLER-LOT-58.md` | Polish Portefeuille+Options : ancienne palette purgée (~28 fallbacks dont orange banni ; `--vx-text-dim` inexistant rendait un gris périmé) — balayage APRÈS : palette OK | 0.9.0 | v115 | 1666 | GO |
| 59 | `SKYLER-LOT-59.md` | Transversal : ~45 fallbacks périmés purgés (7 pages), 2e token inexistant (`--vx-neutral`), doc /design-system honnête, gardiens prospectifs | 0.9.0 | v116 | 1670 | GO |
| 60 | `SKYLER-LOT-60.md` | RC FINALE de l'arc (suite + audit + responsive 8×3 : 0 défaut) + bilan consolidé n°4 (51→60) + ARRÊT de la boucle | 0.9.0 | v116 | 1670 | GO |
| 61 | `SKYLER-LOT-61.md` | Runway anti-collision (2 rangées/côté, déterministe, 0 chevauchement mesuré) + 25 fallbacks périmés purgés des charts JS (3e token fantôme) | 0.9.0 | v117 | 1675 | GO |

## Architecture atteinte

```text
Données réelles → moteurs déterministes → SkylerPacket (red-team produite 1.1.0)
  → décision canonique 0.7.0
      · état opérationnel dérivé (8 états, base explicite)
      · confiance = data_quality × agreement × robustness(11 perturbations mesurées)
                    × calibration(hit rate réel PAR CONTEXTE, seuil d'échantillon)
        avec plafonds §7 — jamais 100 %
  → mémoire immuable (31 champs, versions séparées, séances datées réelles)
      → résultats par horizon → classification d'erreurs → biais → post-mortem
      → calibration ← (la boucle se referme, avec preuves uniquement)
  → knowledge graph prouvable (résidus vs SPY, groupes, questions de recherche)
  → UI : Performance (Mémoire + post-mortem) · Portefeuille/Risque (dépendances)
```

Invariants tenus sur tous les lots : READONLY absolu, données réelles uniquement
(absent → n/d), `main` intacte, aucune modification automatique de la
Constitution, fichiers runtime gitignorés, gardiens de version prospectifs.
