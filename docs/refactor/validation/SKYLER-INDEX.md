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
| 62 | `SKYLER-LOT-62.md` | Purge finale des anciennes palettes (19 fallbacks JS de pages + tracking runtime) — gardien prospectif sur TOUT js/ : classe de défauts fermée | 0.9.0 | v118 | 1679 | GO |
| 63 | `SKYLER-LOT-63.md` | Mini-aires de Marchés lissées monotone Fritsch-Carlson (jamais de faux extrêmes, 4/4 en courbes prouvé) + code mort sparkSvg supprimé | 0.9.0 | v119 | 1684 | GO |
| 64 | `SKYLER-LOT-64.md` | Tour d'inspection : 8 usages vx-truncate sans title corrigés (info toujours lisible au survol) + gardien prospectif — re-balayage APRÈS : 0 restant | 0.9.0 | v120 | 1686 | GO |
| 65 | `SKYLER-LOT-65.md` | Tour angles neufs (ids 0, liens morts 0/13, focus 8/8, aria) : seul défaut = aria du runway (corrigé) — bascule en RC espacées, dit | 0.9.0 | v121 | 1688 | GO |
| RC5 | `SKYLER-RC-PERIODIQUE-5.md` | RC périodique n°5 — suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue après lots 51→65 | 0.9.0 | v121 | 1688 | GO |
| RC6 | `SKYLER-RC-PERIODIQUE-6.md` | RC périodique n°6 — suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue | 0.9.0 | v121 | 1688 | GO |
| RC7 | `SKYLER-RC-PERIODIQUE-7.md` | RC périodique n°7 — suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue | 0.9.0 | v121 | 1688 | GO |
| 66 | `SKYLER-LOT-66.md` | AUDIT TOTAL volet 1 : 137 routes (0×5xx), cohérence des chiffres — tuile Breadth incohérente (above50 non étiqueté vs >MM200) corrigée et étiquetée | 0.9.0 | v122 | 1692 | GO |
| 67 | `SKYLER-LOT-67.md` | AUDIT TOTAL volet 2 : 30 vues profondes × 2 viewports (60 chargements) — 0 erreur, 0 débordement, 0 texte cassé (NaN/undefined) — documentaire | 0.9.0 | v122 | 1692 | GO |
| 68 | `SKYLER-LOT-68.md` | AUDIT TOTAL volet 3 : IBKR lecture seule SAIN — readonly en dur ×4 verrous, refus honnêtes prouvés route→UI, 34 gardiens verts — documentaire | 0.9.0 | v122 | 1692 | GO |
| 69 | `SKYLER-LOT-69.md` | AUDIT TOTAL volet 4 : divergence des moteurs DITE aux deux endroits (sain) ; score shortlist portait pas d'échelle → « /100 » ajouté, prouvé | 0.9.0 | v123 | 1694 | GO |
| 70 | `SKYLER-LOT-70.md` | AUDIT TOTAL volet 5 (final) : états dégradés SAINS (10 états vides avec action, mémoire honnête) + BILAN n°5 — programme TERMINÉ, retour RC espacées | 0.9.0 | v123 | 1694 | GO |
| RC8 | `SKYLER-RC-PERIODIQUE-8.md` | RC périodique n°8 — première après l'AUDIT TOTAL : suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue | 0.9.0 | v123 | 1694 | GO |
| RC9 | `SKYLER-RC-PERIODIQUE-9.md` | RC périodique n°9 — suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue | 0.9.0 | v123 | 1694 | GO |
| RC10 | `SKYLER-RC-PERIODIQUE-10.md` | RC périodique n°10 — suite + audit + responsive 8×3 + cycle souverain : GO, 0 défaut, baseline tenue | 0.9.0 | v123 | 1694 | GO |
| 71 | `SKYLER-LOT-71.md` | PROGRAMME 100 % (ouverture) : docstring gateway citait un gardien inexistant → corrigée + gardien prospectif « toute référence tests/ citée doit exister » | 0.9.0 | v123 | 1696 | GO |
| 72 | `SKYLER-LOT-72.md` | PROGRAMME 100 % : audit performance — DCL <300 ms, 0 doublon, vendor lazy sur /analysis seul, budgets 64 kB gardés — SAIN, mesures publiées | 0.9.0 | v123 | 1699 | GO |
| 73 | `SKYLER-LOT-73.md` | PROGRAMME 100 % : a11y — tickers cliquables non focusables (4 défauts) → tabindex+role + délégation clavier Enter/Espace globale ; balayage APRÈS 0 défaut | 0.9.0 | v124 | 1702 | GO |
| 74 | `SKYLER-LOT-74.md` | PROGRAMME 100 % : robustesse données limites — 0×5xx sur symboles/vues/POST malformés, 404 API JSON+nosniff, refus honnêtes — SAIN, 4 gardiens | 0.9.0 | v124 | 1706 | GO |
| 75 | `SKYLER-LOT-75.md` | PROGRAMME 100 % (clôture) : RC FINALE — suite + audit + responsive + a11y 0 défaut sur base fraîche + BILAN n°6 — programme TERMINÉ, déclaration 100 % faite | 0.9.0 | v124 | 1706 | GO |
| 76 | `SKYLER-LOT-76.md` | Boucle continue : hygiène JS/HTML — 0 debug/dup/TODO ; 1 défaut réel (onglets démo href="#") corrigé + gardiens « plus jamais » | 0.9.0 | v125 | 1708 | GO |
| 77 | `SKYLER-LOT-77.md` | Boucle continue : sécurité en-têtes/contenu — 4 en-têtes partout, contenu 0 fuite ; défaut réel : blob desk perso sans Cache-Control → no-store gardé | 0.9.0 | v125 | 1710 | GO |
| 78 | `SKYLER-LOT-78.md` | Boucle continue : libellés FR — 0 anglais d'interface, 0 accent manquant, ponctuation conforme (espace avant ; = norme FR, faux positif dit) — SAIN + 2 gardiens | 0.9.0 | v125 | 1712 | GO |
| 79 | `SKYLER-LOT-79.md` | Boucle continue : fraîcheur — 2 passes navigateur, 5 signalements stricts tous faux positifs vérifiés (héritage d'en-tête + troncature) — SAIN + 2 gardiens | 0.9.0 | v125 | 1714 | GO |
| 80 | `SKYLER-LOT-80.md` | Boucle continue : 5 parcours bout-en-bout 14/14 OK (outil versionné) ; constat réel — polices sur CDN Google, à auto-héberger (lot 81) | 0.9.0 | v125 | 1714 | GO |
| 81 | `SKYLER-LOT-81.md` | Boucle continue : polices AUTO-HÉBERGÉES (2 woff2 variables locaux, 7 remplacements CDN, SW précache) — 0 requête externe prouvé, parcours 0 erreur console | 0.9.0 | v126 | 1718 | GO |
| 82 | `SKYLER-LOT-82.md` | Boucle continue : défaut MAJEUR — le shell canonique n'enregistrait jamais le SW (0 offline sur les 8 espaces) → vx-shell.js + preuve reload offline rendu du cache | 0.9.0 | v127 | 1720 | GO |
| 83 | `SKYLER-LOT-83.md` | Boucle continue : contrôles interactifs — 26 tris/onglets/selects cliqués en vrai sur 8 vues : 0 inerte, 0 erreur — SAIN, outil controls_audit.js versionné | 0.9.0 | v127 | 1720 | GO |
| 84 | `SKYLER-LOT-84.md` | Boucle continue : cycle desk 6/6 (push→serveur→pull→backups→restore par la route→remise en état) — aucune perte possible, 4 listes de clés alignées, 2 gardiens | 0.9.0 | v127 | 1722 | GO |
| 85 | `SKYLER-LOT-85.md` | Boucle continue : alertes 4/4 + SSE sain (2 faux positifs de sonde vérifiés au socket brut, dits) + mini-bilan tournée 81-85 — 3 gardiens | 0.9.0 | v127 | 1725 | GO |
| 86 | `SKYLER-LOT-86.md` | Boucle continue : 10 cas limites du decision stack FIGÉS par caractérisation (None, score illisible, bornes 56/66/80, CHOP, distribution, démo…) — moteur intact, 0 défaut | 0.9.0 | v127 | 1735 | GO |
| 87 | `SKYLER-LOT-87.md` | Boucle continue : façade recommendation + __VXVOCAB figées (10 tests — vocabulaire sans trou, discipline -20/-25 exacte, thêta, HOLD par défaut) — moteur intact | 0.9.0 | v127 | 1745 | GO |
| 88 | `SKYLER-LOT-88.md` | Boucle continue : evidence + reasoning figés (10 tests — gather(None) honnête, clamp 0-100, bornes catalyseur, fondamental 0 = absent, contradictions Loi 14) | 0.9.0 | v127 | 1755 | GO |
| 89 | `SKYLER-LOT-89.md` | Boucle continue : track_record figé (6 tests — n<5 jamais publié, division par zéro impossible, TP1 non résolu honnête, mémo 30 min) — moteur intact | 0.9.0 | v127 | 1761 | GO |
| 90 | `SKYLER-LOT-90.md` | Boucle continue : persist + connections figés (10 tests) + BILAN 86-90 — « moteurs blindés » complet : 46 caractérisations, 0 logique modifiée | 0.9.0 | v127 | 1771 | GO |
| 91 | `SKYLER-LOT-91.md` | Boucle continue : decide.py figé (9 tests — {} → None refus honnête, hard gates stop/régime/R:R 2.0 exact, CHOP jamais d'achat, IV-crush ≤14 j) | 0.9.0 | v127 | 1780 | GO |
| 92 | `SKYLER-LOT-92.md` | Boucle continue : committee.py — DÉFAUT RÉEL : « DANS LA ZONE D'ACHAT » était du code mort (garde contradictoire) → fenêtre promise s'ouvre enfin ; 9 tests | 0.9.0 | v127 | 1789 | GO |
| 93 | `SKYLER-LOT-93.md` | Boucle continue : pivots/structure figé (8 tests — cassure fraîche vs étendue, repli repris, piège baissier, measured move exact, ATR 0 sans crash) | 0.9.0 | v127 | 1797 | GO |
| 94 | `SKYLER-LOT-94.md` | Boucle continue : contrat POST figé — 12 routes sondées 0×5xx refus structurés + télémétrie client bornée (troncatures exactes, tampon 100) — 4 tests | 0.9.0 | v127 | 1801 | GO |
| 95 | `SKYLER-LOT-95.md` | Boucle continue : filtres durs options figés (6 tests — DTE inclusif, delta inconnu jamais classé, refus documentés) + MINI-BILAN 91-95 (1 défaut moteur corrigé) | 0.9.0 | v127 | 1807 | GO |
| 96 | `SKYLER-LOT-96.md` | Boucle continue : socle math du lab figé (7 tests — parité put-call 1e-9, golden BS recalculé à la main : le moteur avait raison, mon golden mémoire faux dit) | 0.9.0 | v127 | 1814 | GO |
| 97 | `SKYLER-LOT-97.md` | Boucle continue : scoring pur figé (8 tests — neutres exacts, ROC borné, proxy toujours signalé, −10 IV-crush exact, confiance auto-cohérente) | 0.9.0 | v127 | 1822 | GO |
| 98 | `SKYLER-LOT-98.md` | Boucle continue : earnings + barème figés (8 tests — modes post-earnings exacts, refus jamais muet, langage de certitude neutralisé, bornes grade 90/80/72/60/45) | 0.9.0 | v127 | 1830 | GO |
| 99 | `SKYLER-LOT-99.md` | Boucle continue : broker SSE + états système figés (9 tests — canal inconnu reclassé, replay Last-Event-ID, tampon borné, client lent jamais bloquant, framing SSE nommé exact, ok/warming/degraded, fraîcheur unknown honnête, mode demo>ibkr>cloud) | 0.9.0 | v127 | 1839 | GO |
| 100 | `SKYLER-LOT-100.md` | BILAN CONSOLIDÉ n°7 — tournée 76-100 : 24 lots, +133 tests (1706→1839), 4 défauts réels corrigés (href=#, /api/desk no-store, SW jamais enregistré→offline réel, code mort committee), 2 chantiers (polices locales, PWA offline), 114 caractérisations « moteurs blindés » 86-99, SW v124→v127, PR #109→#132 | 0.9.0 | v127 | 1839 | GO |
| 101 | `SKYLER-LOT-101.md` | Boucle continue : entonnoir de chaîne options figé (8 tests — bornes DTE inclusives, préférées d'abord triées au centre, fenêtre strikes ±35 % exacte, échantillonnage 14 gardant les 2 extrêmes, expiration sans strike jamais envoyée au broker) | 0.9.0 | v127 | 1847 | GO |
| 102 | `SKYLER-LOT-102.md` | Boucle continue : gardien XSS des news figé (9 tests — balises retirées puis échappement complet, balise cassée inerte, javascript:/data: supprimés, sentiment FR/EN, parse_rss sans exception, dedupe titre normalisé/lien) | 0.9.0 | v127 | 1856 | GO |
| 103 | `SKYLER-LOT-103.md` | Boucle continue : barème de liquidité figé (8 tests — refus bid/ask nommé, pénalité dégressive 4-10 % sans grief, spread > 10 % jamais traitable, OI inconnu < OI faible, volume silencieux vs nommé, cumul exact 15) | 0.9.0 | v127 | 1864 | GO |
| 104 | `SKYLER-LOT-104.md` | Boucle continue : environnement options figé (8 tests — formules exactes des 5 dimensions, IV rank inversé borné, event risk fraction ≤7 j, verdict 66/45, dimension inconnue exclue de la moyenne jamais zéro, confiance = connues/5) | 0.9.0 | v127 | 1872 | GO |
| 105 | `SKYLER-LOT-105.md` | Boucle continue : démarrage figé + mini-bilan 101-105 (8 tests — ordre §10 exact, _step jamais bloquant détail 200, ibkr jamais CONNECTED sans preuve, tradingview MISSING/CONFIGURED honnête, rapport copie, ran False avant séquence ; bilan : 5 lots, 41 tests, 1839→1880) | 0.9.0 | v127 | 1880 | GO |
| 106 | `SKYLER-LOT-106.md` | Boucle continue : score contextuel des contrats figé (8 tests — multiplicatif, R:R < 2 plafonné 10, non calculable plancher 5, liquidité ≤ ×1, IV rank ≥ 85 taxée malgré DTE long, ULTRA_CONVEX score 0 sans setup exceptionnel, prime minuscule ×0.3) | 0.9.0 | v127 | 1888 | GO |
| 107 | `SKYLER-LOT-107.md` | Boucle continue : courbe de taux figée (8 tests — fallback plat documenté jamais présenté comme marché, interpolation linéaire exacte, clamp sans extrapolation, points triés, to_dict, rate_sensitivity ±50 bp avec plancher 0 et None honnête) | 0.9.0 | v127 | 1896 | GO |
| 108 | `SKYLER-LOT-108.md` | Boucle continue : surface de volatilité figée (8 tests — realized_vol 0 exact/None honnête, spot invalide refusé, IV pourries filtrées, ATM au strike le plus proche, skew jamais inventé, dislocations nommées, rank/percentile exacts, IV_SPIKE et rank None sur historique plat) | 0.9.0 | v127 | 1904 | GO |
| 109 | `SKYLER-LOT-109.md` | Boucle continue : registre des jobs figé (8 tests — snapshot ordonné priorité produit, jamais exécuté sans ETA inventée, job non canonique jamais exposé, beat ok/erreur tronquée 200, ETA bornée jamais négative, snapshot copie infalsifiable) | 0.9.0 | v127 | 1912 | GO |
| 110 | `SKYLER-LOT-110.md` | Boucle continue : cas limites du flux figés + mini-bilan 106-110 (8 tests — repli mid×100, NaN/inf rejetés, jamais « frais » sans OI, skew 60/40 exact, top borne l'affichage pas le décompte ; bilan : 5 lots, 40 tests, 1880→1920) | 0.9.0 | v127 | 1920 | GO |
| 111 | `SKYLER-LOT-111.md` | Boucle continue : validation de configuration figée (8 tests — MISSING avec conséquence exacte, INVALID nommé, aucun secret jamais exposé, alias historique accepté, espaces = MISSING, enum insensible casse, compteurs exacts, aucune variable obligatoire) | 0.9.0 | v127 | 1928 | GO |
| 112 | `SKYLER-LOT-112.md` | Boucle continue : santé du runtime IA figée (8 tests — MISSING note honnête, clé ≠ preuve (CONFIGURED jamais CONNECTED sans appel réel), DEGRADED/reconnexion au dernier appel, modèle défaut+override, clé jamais dans le rapport) | 0.9.0 | v127 | 1936 | GO |
| 113 | `SKYLER-LOT-113.md` | Boucle continue : types de provenance figés (8 tests — missing() honnête, usable exige valeur ET qualité vivante (STALE utilisable, EXPIRED non), 0/False = vraies valeurs, warnings jamais partagés, AnalyticsPacket 5 familles + snapshot dict, aucun état partagé) | 0.9.0 | v127 | 1944 | GO |
| 114 | `SKYLER-LOT-114.md` | Boucle continue : frontière d'unités IV figée (8 tests — unité inconnue = ValueError, NaN/inf rejetés, conversions exactes, legacy board détection étiquetée jamais muette, seuil 1.5 exact, ordure = triple None, exports limités aux deux portes) | 0.9.0 | v127 | 1952 | GO |
| 115 | `SKYLER-LOT-115.md` | Boucle continue : backtest recherche figé + mini-bilan 111-115 (8 tests — rotation 0 = coût 0, chaque aller-retour se paie, vide = None honnête, avertissement walk-forward systématique, apply_costs formule exacte ; bilan : 5 lots, 40 tests, 1928→1960) | 0.9.0 | v127 | 1960 | GO |
| 116 | `SKYLER-LOT-116.md` | Boucle continue : catalyseurs non-earnings figés (8 tests — non confirmé jamais actionnable, type inconnu dénoncé, horizon 0-30 inclusif trié, fenêtre earnings 45 j inclusive, next_events cap 3, avertissement nommé avec compte exact) | 0.9.0 | v127 | 1968 | GO |
| 117 | `SKYLER-LOT-117.md` | Boucle continue : Research Factory figée (8 tests — transitions interdites refusées, RETIRED terminal, REJECTED renaît en IDEA, manquants nommés (11 champs/12 biais), « un beau backtest ne suffit jamais », embargo réel des splits, passed ≥ max(2, n−1)) | 0.9.0 | v127 | 1976 | GO |
| 118 | `SKYLER-LOT-118.md` | Boucle continue : lecture graphique figée (8 tests — {} → None honnête, hiérarchie de tendance, seuils RSI 78/60/48, accumulation prime sur distribution, chart_verdict 4 issues, thesis la méfiance prime, plays par profil) | 0.9.0 | v127 | 1984 | GO |
| 119 | `SKYLER-LOT-119.md` | Amélioration graphique n°1 (Aujourd'hui) : Catalyst Runway développé — zone d'imminence ≤ 5 j teintée, points dimensionnés par impact + halo, anneau sur le prochain, graduations hebdo, bornes nommées ; captures avant/après envoyées | 0.9.0 | v128 | 1984 | GO |
| 120 | `SKYLER-LOT-120.md` | Amélioration graphique n°2 (Marchés) + mini-bilan 116-120 : lignes ultra propres — endDotsPlugin (point net + nom de série en bout de ligne), softGlowPlugin (halo néon doux), traits 1.6, dégradé area 4 arrêts ; bénéfice transversal multiLine/area ; captures envoyées | 0.9.0 | v129 | 1984 | GO |
| 121 | `SKYLER-LOT-121.md` | Amélioration graphique n°3 (Opportunités) : entonnoir monochrome dégradé brand→cyan (opacité = déperdition, un chiffre par étage, −N sur la plus forte perte) + zone actionnable du scatter teintée en dégradé positif ; captures envoyées | 0.9.0 | v130 | 1984 | GO |
| 122 | `SKYLER-LOT-122.md` | Amélioration graphique n°4 (Analyse) : radar en dégradé radial (centre transparent → bord de marque), points sommets + halo, grille en opacité dégressive, trait 1.6 — tous les radars héritent ; captures fiche ACN envoyées | 0.9.0 | v131 | 1984 | GO |
| 123 | `SKYLER-LOT-123.md` | Amélioration graphique n°5 (Portefeuille) : treemap matière verre — dégradé diagonal par tuile (même le neutre honnête gagne de la profondeur), liseré fin de la couleur, part du total % sur les grandes tuiles ; captures envoyées | 0.9.0 | v132 | 1984 | GO |
| 124 | `SKYLER-LOT-124.md` | Amélioration graphique n°6 (Options) : payoff éducatif — breakeven enfin tracé (« BE $X »), spot tracé, zones gain/perte sur tokens, trait 1.6 + halo doux, arithmétique inchangée ; captures envoyées | 0.9.0 | v133 | 1984 | GO |
| 125 | `SKYLER-LOT-125.md` | Amélioration graphique n°7 (Journal) : barres matière verre (dégradé dense→doux + liseré, toutes les barres héritent), famille .vx-stat enfin stylée (répare 5 pages — « Trades3 » collés), hex track record → tokens ; captures envoyées | 0.9.0 | v134 | 1984 | GO |
| 126 | `SKYLER-LOT-126.md` | Amélioration graphique n°8 (Système — 1re tournée TERMINÉE 8/8) : jauge matière verre (dégradé + halo, toutes les jauges héritent), libellés kv protégés (fin des « Ét at »), badge canaux adaptatif ; captures envoyées | 0.9.0 | v135 | 1984 | GO |
| 127 | `SKYLER-LOT-127.md` | Passe n°2 — heatmaps matière verre : tuiles dégradées sur tokens (les derniers rgba hors palette éliminés), liseré inset, grille aérée — matrice scénarios options, secteurs Marchés et P&L mensuel héritent ; captures envoyées | 0.9.0 | v136 | 1984 | GO |
| 128 | `SKYLER-LOT-128.md` | Passe n°3 — donut : la catégorie dominante et sa part (« 55 % AVOID ») au CENTRE de l'anneau, dans la couleur de son arc (plugin vxDonutCenter, rien si total nul) — tous les donuts héritent ; captures envoyées | 0.9.0 | v137 | 1984 | GO |
| 129 | `SKYLER-LOT-129.md` | Passe n°4 — BUG visuel corrigé : rails CALME↔STRESS / DÉFENSE↔ATTAQUE invisibles (override noir !important) → dégradé sémantique rétabli ; courbe des taux « Actuelle » en cyan ; endDots anti-collision des étiquettes ; captures envoyées | 0.9.0 | v138 | 1984 | GO |
| 130 | `SKYLER-LOT-130.md` | Passe n°5 — fiche Analyse : « Performance multi-horizons » en matière verre (dégradé color-mix sur tokens, doux au zéro → dense à la valeur) + MINI-BILAN 126-130 ; captures envoyées | 0.9.0 | v139 | 1984 | GO |

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
