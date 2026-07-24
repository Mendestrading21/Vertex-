# Validation — PR n°7 (finale) : Refonte Journal + Système

> Branche `agent/vertex-total-rebuild`. Dernière PR de la refonte produit.
> Journal répond à « **Suis-je en train de devenir un meilleur investisseur ?** ».
> Système répond à « **Puis-je faire confiance à Vertex aujourd'hui ?** ».
> Conforme à `VERTEX_CONSTITUTION.md` (§6, §17-22), `VERTEX_PRODUCT_BIBLE.md`,
> `PRODUCT_EXPERIENCE_REVIEW.md`. **READONLY absolu**, aucun moteur modifié.

## 1. Fichiers modifiés

- `vertex/ui/pages/performance_page.py` — Journal refondu : **discipline uniquement**
  (Hero éditorial + stats comportementales + hypothèses + progression + biais).
- `vertex/ui/pages/system_page.py` — **Hero technique** (cockpit de confiance) en
  tête de la vue Connexions.
- `vertex/app/routes/redesign.py` — `/journal` atterrit désormais sur **Discipline**
  (`view=overview`) et non plus sur la Timeline.
- `vertex/app/routes/system.py` — bump service worker `td-shell-v49 → v50`.
- Tests : `tests/test_journal_system_07.py` (**6 gardiens**) + gardiens SW v50.

## 2. Journal — discipline uniquement

### Ce qui a été RETIRÉ définitivement
La **performance de portefeuille** (courbe d'équité, drawdown, saisonnalité,
contribution) — déjà migrée vers Portefeuille → Performance en PR n°5 — ne réapparaît
nulle part. Gardien : `equityCard/drawdownCard/heatmapCard` **absents** du Journal.

### Sous-vues (avant → après)
| Avant | Après |
|---|---|
| Vue d'ensemble · Journal · Track record · Enseignements | **Discipline** (défaut) · **Timeline** · **Apprentissage** · **Progression** (nouvelle) · Track record |

### Discipline (premier écran)
- **Hero éditorial honnête** : phrase construite UNIQUEMENT sur des faits comptés
  (« Tu as documenté un plan sur **80 %** de tes décisions », « 2 erreurs déclarées »,
  « 2 hypothèses validées · 2 invalidées »). **Aucun pourcentage inventé** (le « 92 % »
  de l'exemple n'est jamais codé en dur) ; au premier passage, onboarding honnête.
- **4 KPI comportementaux** : respect de la méthode · qualité des entrées · qualité
  des sorties · respect des invalidations — chacun `n/d` honnête si la donnée manque.
- **Revue des hypothèses** : validées / invalidées / en cours (déclarations).
- **Distribution des rendements par trade** conservée (mesure d'asymétrie = discipline).

### Autres vues
- **Timeline** : décisions récentes + erreurs déclarées + ajout d'entrée.
- **Apprentissage** : leçons apprises + erreurs récurrentes + **biais comportementaux**
  (décompte des états émotionnels déclarés : FOMO, impatience…).
- **Progression** : paliers débloqués (5/10/20/30 décisions) + **erreurs déclarées par
  mois** (la fréquence baisse-t-elle ?) — honnête, « aucune progression fabriquée ».
- **Track record** : signaux moteur vs trades réels (deux mondes, jamais confondus).

## 3. Système — Hero technique cockpit

- **Hero technique** en tête (`vx-sys-hero`) : verdict de confiance synthétique depuis
  les payloads réels — « **Système opérationnel** » / « partiellement dégradé », puis
  « IBKR désactivé · 3 domaine(s) en différé/rassis · aucune erreur critique · lecture
  seule confirmée (aucun ordre) ». Badges DÉMO / READONLY. Aucun chiffre inventé.
- Le reste du cockpit (déjà institutionnel) est conservé : jauge % moteurs OK, bande
  KPI (moteurs, données fraîches, erreurs, scan, appels IA, lecture seule), canaux
  honnêtes (IBKR/TradingView/Claude/stockage/scheduler/live stream), cerveau Claude,
  synchronisation, moteurs, diagnostics, réglages, archive, design system.
- Rien de décoratif : chaque bloc répond à « puis-je faire confiance aux données ? ».

## 4. Invariants

READONLY absolu (affiché + confirmé serveur `disabled-by-design`) · aucun ordre ·
aucune logique de trading ajoutée · **aucun moteur modifié** · états honnêtes
(live/demo/offline/n/d) · sources/unités/fraîcheur partout.

## 5. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **950 passed, 2 skipped** (+6 gardiens PR7).
- Gardiens PR7 : `test_journal_is_discipline_not_portfolio_performance`,
  `test_journal_hero_is_honest_no_fabricated_percent`, `test_journal_new_views_present`,
  `test_journal_routes_200`, `test_system_hero_technique_present`,
  `test_system_route_200_and_readonly`. Routes `/journal?view=…` (5 vues) et `/system`
  à 200 ; invariant READONLY affiché.

## 6. Contrôle navigateur (390 / 768 / 1440)

| Viewport | Débordement | Erreurs console |
|---|---|---|
| **390 mobile** | **0 px** (7/7) | **0** (7/7) |
| **768 tablet** | **0 px** (7/7) | **0** (7/7) |
| **1440 desktop** | **0 px** (7/7) | **0** (7/7) |

7 vues testées : Journal (Discipline/Timeline/Apprentissage/Progression/Track) +
Système (Connexions/Données). Vérifié : Hero éditorial honnête (80 % réel), KPI
comportementaux, hypothèses, biais, Hero technique « Système opérationnel ».
Captures : scratchpad `pr7shots/`.

## 7. Erreurs restantes

- Console applicative : **0**. (`ERR_CONNECTION_RESET` = Google Fonts via proxy
  sandbox, non applicatif.)

## 8. Risques techniques

- Le **temps moyen de conservation** n'est pas calculé (les entrées de journal ne
  portent qu'une date unique, pas open+close) → non affiché plutôt qu'inventé.
- Les stats comportementales dépendent de la **complétude des déclarations** (raison,
  stop, leçon, émotion) ; sans ces champs, `n/d` honnête.
- Progression : la tendance d'erreurs exige ≥ 2 mois datés, sinon paliers + note
  honnête.

---

# PLAN RC1 — Vers la Release Candidate

## A. Éléments terminés (refonte produit)
- **Gouvernance** : Constitution, Product Bible, Experience Review (PR n°1).
- **Design system & Chart Shell** OBSIDIAN COPPER (PR Design n°1).
- **Navigation** 8 espaces canoniques + redirections (PR n°2).
- **Aujourd'hui + Marchés** (résumé vs explication, 30→15 graphiques) (PR n°3).
- **Opportunités + Analyse** (Hero, op-scatter, Carte-Verdict, Carte-Scénario, comité)
  (PR n°4).
- **Portefeuille** (Synthèse, tableau canonique état-de-thèse, garde-fou perdants,
  performance migrée) (PR n°5).
- **Options** (Carte-Verdict asymétrie, payoff canonique multileg_lab, Greeks
  interprétés, LEAPS, positions ; **bug IV corrigé avec preuve**) (PR n°6).
- **Journal + Système** (discipline seule, Hero technique) (PR n°7).
- **Qualité** : 950 tests verts ; 0 débordement / 0 console sur toutes les vues ;
  READONLY intact ; service worker v50.

## B. Éléments restants avant RC1
1. **Nettoyage des vues legacy Options** (`overview/radar/scenarios` encore servies
   hors barre) — retirer proprement avec mise à jour des tests.
2. **Passe d'accessibilité complète** (audit clavier/focus/lecteur d'écran sur les 8
   espaces ; vérifier `prefers-reduced-motion` partout ; contrastes AA mesurés).
3. **Passe responsive 1920×1080 + appareil physique** (validation hors headless).
4. **Revue éditoriale FR** (cohérence des libellés, tutoiement, ponctuation) sur les 8
   espaces.
5. **Parcours de bout en bout** re-testés (Aujourd'hui → Opportunité → Analyse →
   Portefeuille → Options → Journal) avec données démo et sans IBKR.

## C. Dette technique
- `terminal.py` reste un monolithe (~10 500 lignes) : poursuivre l'extraction vers
  `vertex/ui/pages/*` et `vertex/app/routes/*` (déjà bien engagée).
- Vues Options legacy + scripts de charts dormants (`sector-chart.js`,
  `breadth-chart.js`) à retirer après preuve de non-usage.
- `options-intel.js` (610 lignes) et `options-structure.js` cohabitent : envisager une
  fusion une fois les vues legacy retirées.
- Uniformiser les helpers dupliqués entre pages (esc/kv/fmt) vers un module partagé.

## D. Optimisations finales
- Réduire le nombre de scripts chargés par page (bundling ciblé des charts réellement
  utilisés par vue).
- Vérifier le cache du service worker (précache des seuls assets critiques).
- Mesurer le temps de rendu initial par espace (budget < 2 s en démo).

## E. Suppression de code mort (après preuve)
- Vues Options legacy, factories de charts dormantes, endpoints non référencés.
- Protocole : `grep` des imports/routes/refs + tests verts avant retrait (Constitution
  §24 : le code mort n'est supprimé qu'après preuve ; l'historique Git suffit).

## F. Performances
- Profiler `/scan`, `/api/options/*`, `/api/system/*` (latence P95) ; borner les
  agrégations client sur gros journaux.
- Vérifier l'absence de re-render en cascade (les vues re-fetchent proprement).

## G. Accessibilité
- Navigation clavier + focus visible sur tous les composants interactifs.
- Résumés textuels de chaque graphique (Chart Shell `summary`) — audit de couverture.
- P&L / verdicts compréhensibles sans couleur (badges + texte) — audit.
- `prefers-reduced-motion` respecté (désactiver transitions non essentielles).

## H. Sécurité
- `VERTEX_CODE` (verrou d'accès) et `VERTEX_SECRET` documentés ; sans code, écoute
  127.0.0.1 uniquement.
- `news_plus.sanitize_news()` sur tout texte externe rendu en innerHTML (XSS).
- IBKR `readonly=True` toujours ; aucun endpoint d'ordre (gardiens `test_no_orders`,
  `_ORDER_WORDS`).
- Revue finale : échappement systématique des données externes côté client.

## I. Préparation Release Candidate
1. Geler la branche `agent/vertex-total-rebuild` après les points B.
2. Exécuter la suite complète + un smoke-test navigateur des 8 espaces (démo + sans
   IBKR + mode dégradé).
3. Rédiger `docs/refactor/RC1_CHECKLIST.md` (états attendus par espace, captures de
   référence, versions).
4. Bump service worker final + note de version ; tag `rc1`.
5. Décision explicite de l'utilisateur avant toute mise à jour de `main`
   (version canonique — jamais touchée sans accord).

## Verdict

**GO.** La refonte produit est **complète** : les 8 espaces répondent chacun à une
question unique, avec des états honnêtes, des composants premium cohérents et zéro
donnée inventée. Journal = discipline (« deviens-je meilleur ? ») ; Système = confiance
(« puis-je faire confiance aux données ? »). **950 tests verts**, **0 débordement**,
**0 erreur console**, **READONLY intact**. La base est prête pour la stabilisation
**RC1** (nettoyage legacy, accessibilité, responsive 1920, revue éditoriale).
