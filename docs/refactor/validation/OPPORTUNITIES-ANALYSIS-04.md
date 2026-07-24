# Validation — PR n°4 : Refonte Opportunités + Analyse

> Branche `agent/vertex-total-rebuild`. Transforme le **parcours central** :
> opportunité détectée → dossier → asymétrie → thèse → risque → décision expliquée.
> Conforme à `VERTEX_CONSTITUTION.md`, `VERTEX_PRODUCT_BIBLE.md` (§3.3, §3.4),
> `PRODUCT_EXPERIENCE_REVIEW.md`. Aucun moteur financier modifié, IBKR READONLY
> intact, pas de migration big-bang.

## 1. Fichiers modifiés

- `vertex/ui/pages/opportunities_page.py` — Hero éditorial + `op-radar → op-scatter`.
- `vertex/ui/pages/analysis_page.py` — Carte-Verdict + Carte-Scénario + comité +
  DATA_INSUFFICIENT honnête + réordonnancement.
- `vertex/app/routes/system.py` — bump service worker `td-shell-v46 → v47`.
- `tests/test_pages_opportunities_analysis_04.py` (nouveau, 8 gardiens) + gardiens SW.

## 2. Structure avant / après

### Opportunités (`/opportunities?view=radar`)
| Avant | Après |
|---|---|
| Top cards + funnel + « Radar des opportunités » (scatter mal nommé) + ranking (scoreBar) | **Hero éditorial** (compte S+/S/A/B + meilleure opp + R:R + Freshness + message honnête) + 4 KPI cliquables + action · Top cards · funnel unique · **op-scatter** (axes/quadrants/conclusion) · ranking |

### Analyse (`/analysis/<sym>`)
| Avant | Après |
|---|---|
| Hero flex (ticker/prix/badge) → thèse → graphique → dimensions → scénarios Bull/Base/Bear (bas de page) | **Carte-Verdict** (signature) → **Carte-Scénario** (pessimiste/probable/exceptionnel) → graphique LWC → **Raisonnement du comité** → justification → expertise |
| Scénarios en double position potentielle | **Domicile unique** des scénarios (Bull/Base/Bear retiré) |

## 3. Graphiques avant / après

| Espace | Avant | Après | Note |
|---|---|---|---|
| **Opportunités** (radar) | scatter + funnel (2) | **op-scatter + funnel (2)** | scatter renommé/explicité, Hero ajouté (composant, pas graphique) |
| **Analyse** | scorecard radar + LWC (2) + cartes Bull/Base/Bear | **scorecard radar + LWC (2)** | scénarios consolidés en Carte-Scénario (composant) ; comité = composant |

Aucun graphique décoratif ajouté ; les nouveaux éléments sont des **composants
premium** (Verdict/Scénario/Comité), pas des graphiques.

## 4. op-radar → op-scatter

- Renommé partout (`op-radar`, `op-radar-sel` → `op-scatter`, `op-scatter-sel`) —
  `grep op-radar` = **0**.
- Vrai scatter explicite via Chart Shell : titre « Scatter d'asymétrie — qualité ×
  timing », **axes** (X qualité/conviction, Y timing/momentum), **quadrants
  nommés** (À ÉTUDIER / À ÉVITER / …), **conclusion** textuelle, **unité** (score
  0-100), **résumé accessible**. Taille = anomalies, couleur = verdict (sens
  financier).

## 5. Carte-Verdict

`section.vx-verdict-card` alimentée par `/api/decision/<sym>` (decision stack) :
verdict (label + tonalité) · grade · confiance /100 · prix · entrée · invalidation
· conviction · véhicule · qualité des données · **actions** (« Alerte sur
l'invalidation », « Journaliser l'hypothèse », « Voir les scénarios »). Freshness
Badge. Hiérarchie : verdict → asymétrie → invalidation → confiance → détails.

## 6. Carte-Scénario

`div.vx-scenario-grid` : **pessimiste / probable / exceptionnel** dérivés du plan
réel (entrée → invalidation / cibles tp1/tp3), avec rendement %, cible, note
(invalidation / cible étendue) et **ratio d'asymétrie** (gain exceptionnel /
perte max). **Aucune probabilité inventée** (labels par nom uniquement). Repli
honnête si le plan de niveaux est insuffisant.

## 7. Intégration Intelligence → Analyse

Section **« Raisonnement du comité »** (`#an-committee`) depuis `/api/decision` :
consensus (view + accord), facteurs positifs/négatifs (pros/cons), **avocat du
diable**, inconnues. « L'IA explique, ne décide jamais. » Le scorecard radar
reste à domicile unique (Analyse) — pas de duplication (Intelligence est hors
nav depuis la PR n°2).

## 8. Parcours signal → thèse & nombre de clics mesuré

Contrôle navigateur : depuis `/opportunities`, **1 clic** sur « Étudier le dossier
X → » du Hero ouvre `/analysis/X` avec la **Carte-Verdict visible en premier**.
**Clics mesurés = 1** (cible ≤ 2 respectée). Contexte ticker préservé ; retour
arrière navigateur revient à la sélection. Ordre de composition perçu : Verdict →
Scénarios → graphique → comité.

## 9. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **916 passed, 2 skipped** (+8 gardiens PR4).
- Gardiens PR4 : `test_opportunities_scatter_renamed`,
  `test_opportunities_hero_editorial_honest`, `test_opportunities_scatter_has_shell_contract`,
  `test_analysis_verdict_card_present`, `test_analysis_scenario_card_single_home`,
  `test_analysis_committee_integrated`, `test_analysis_data_insufficient_honest`,
  `test_analysis_no_invented_probability`. Routes 200
  (`test_every_primary_route_returns_200`, `test_subviews_return_200`) ;
  `test_no_orders` (READONLY) vert.

## 10. Contrôle navigateur (390 / 768 / 1440)

| Viewport | Opportunités | Analyse |
|---|---|---|
| **390 mobile** | OK | OK |
| **768 tablet** | OK | OK |
| **1440 desktop** | OK | OK |

- Rendu vérifié : Hero (`vx-card--hero`), op-scatter (canvas), Carte-Verdict
  (`vx-verdict-card`), **3 scénarios** (`vx-scenario`), comité intégré, LWC (1).
- **DATA_INSUFFICIENT** (`/analysis/ZZZZZ`) : état `vx-insufficient` présent,
  aucune carte scénario (aucune conviction) — honnête.
- **0 erreur console applicative** ; `/api/client-log` = `{"count":0,"errors":[]}`.
- Démo : badge/bannière présents ; sans-IBKR : états honnêtes.
- Captures : scratchpad `pr4shots/` (desktop opp/analysis, mobile analysis).

## 11. Erreurs restantes

- Console applicative : **0**. (`ERR_CONNECTION_RESET` = Google Fonts via proxy
  sandbox, non applicatif.)

## 12. Risques

- **Score /40** : la Carte-Verdict affiche grade + confiance + conviction (données
  réelles du decision stack) ; un « /40 » canonique n'existe pas tel quel dans le
  moteur → non fabriqué (honnêteté). À réconcilier si un score /40 canonique est
  exposé plus tard.
- **Comparaison 2-4 titres** et **grille des 7 questions** : non implémentées dans
  ce lot (périmètre resserré sur Verdict/Scénario/Comité) — à finaliser en
  finition Analyse ; le scoreBar HTML du ranking Opportunités reste (pas de
  composant canonique équivalent).
- Ancien rendu scénarios (plan `d.plan`) retiré ; la Carte-Scénario utilise
  `/api/decision` — si l'ancien affichait des cibles différentes, c'est désormais
  la source decision stack qui fait foi (domicile unique).
- Validation Chromium **headless** (pas d'appareil physique).

## 13. Plan précis de la prochaine PR — Portefeuille

- **Premier écran** : exposition · concentration (HHI) · P&L latent · **ce qui a
  changé** depuis hier. ≤4 KPI, 1 tableau principal (positions avec **état de
  thèse** : intacte / à surveiller / invalidée, perte max, palier de gain).
- **Règles gagnants/perdants** surfacées (+20/+50/+100 ; **jamais** « renforcer la
  perte » ; invalidation ≠ volatilité).
- **Performance de portefeuille** (equity/drawdown) **migrée depuis Journal** vers
  Portefeuille (finalise la décision PR n°2).
- **Allocation** : 1 vue (treemap OU donut rôles) ; exposition sectorielle.
- Sans IBKR : état vide premium honnête (aucun faux chiffre).
- Chart Shell complet ; 0 débordement 390/768/1440 ; 0 console ; SW bump ;
  READONLY intact ; captures avant/après + comptes de graphiques.

## Verdict

**GO.** Le parcours central est transformé : **1 clic** de l'opportunité à une
thèse compréhensible ; Carte-Verdict + Carte-Scénario + raisonnement du comité ;
DATA_INSUFFICIENT honnête ; 916 tests verts ; 0 débordement ; 0 erreur console.
Fondations posées pour la refonte du Portefeuille.
