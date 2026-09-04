# Vertex — RC1 Human Acceptance

> **Portail : validation humaine.** L'agent ne peut PAS certifier les critères visuels
> subjectifs ni la validation sur appareil physique. Ce document est la **checklist
> interactive** à exécuter par toi (humain), puis à compléter et signer.
>
> **Statut courant : `PENDING`.** Statuts autorisés à ce portail : `PENDING` ·
> `GO FOR PR` · `NO-GO FOR PR`. (Pas de `GO FOR MERGE` ici.)

## Métadonnées
- **SHA testé** : `84fbdc5` (+ bump SW v51 en cours de ce portail — voir §Décision SW)
- **Branche** : `agent/vertex-total-rebuild`
- **Date** : _(à remplir)_
- **Environnement** : `DEMO=1 NO_IBKR=1 python terminal.py` · port 5002
- **Navigateur(s)** : _(à remplir — ex. Chrome / Safari / Firefox)_
- **Appareils** : _(à remplir — ordinateur réel + téléphone/tablette réel)_

## Comment lancer (conditions proches du réel)
```
DEMO=1 NO_IBKR=1 python terminal.py     # démo, sans IBKR
# ou, avec IBKR lecture seule : TWS/Gateway ouvert + VERTEX_CODE défini, puis python terminal.py
```
Ouvre http://127.0.0.1:5002 (ou l'IP LAN pour le téléphone si `VERTEX_CODE` défini).

---

## Checklist des 8 espaces

Pour chaque espace : **URL · état attendu · interaction · résultat attendu · anomalie à
signaler · capture recommandée.** Coche `[x]` si conforme, note l'anomalie sinon.

### 1. Aujourd'hui — `[ ]`
- **URL** : `/`
- **État attendu** : Hero éditorial (régime + confiance + Freshness), 4 KPI cliquables, 1 risque, 1 action, Diff « depuis ta dernière visite ».
- **Interaction** : lire le Hero (< 10 s pour comprendre le régime) → cliquer un KPI (ex. Régime) → revenir (bouton navigateur).
- **Résultat attendu** : le KPI ouvre le domicile Marchés ; le retour revient à Aujourd'hui intact.
- **Anomalie à signaler** : chiffre sans source/unité/fraîcheur ; Diff fabriqué au 1er passage (doit dire « Aucun historique… »).
- **Capture** : Hero + KPI (desktop + mobile).

### 2. Marchés — `[ ]`
- **URL** : `/markets` (+ `?view=` sectors / breadth / macro / volatility ; cross-asset si présent)
- **État attendu** : Vue d'ensemble, Participation/Breadth, Secteurs, Macro, Volatilité — chaque graphique avec **conclusion + unité + source + fraîcheur**.
- **Interaction** : parcourir chaque sous-vue.
- **Résultat attendu** : graphiques lisibles, aucune duplication inter-pages, VIX jamais coloré directionnellement.
- **Anomalie à signaler** : graphique sans conclusion ; débordement ; 404 console (les 6 graphes supprimés ne doivent JAMAIS être demandés).
- **Capture** : Secteurs + Volatilité.

### 3. Opportunités — `[ ]`
- **URL** : `/opportunities` (+ `?view=radar`)
- **État attendu** : Hero (compte S+/S/A/B + meilleure opp + R:R), funnel, **op-scatter** (axes/quadrants/conclusion), classement.
- **Interaction** : repérer la meilleure opportunité → « Étudier le dossier → » (1 clic) → vérifier scatter + filtres.
- **Résultat attendu** : ouverture d'`/analysis/<sym>` en **1 clic**, contexte ticker préservé.
- **Anomalie à signaler** : scatter sans quadrants nommés ; > 2 clics vers Analyse.
- **Capture** : Hero + op-scatter.

### 4. Analyse — `[ ]`
- **URL** : `/analysis/<sym>` (ticker scanné) puis `/analysis/ZZZZZ` (inconnu)
- **État attendu** : **Carte-Verdict** (verdict + grade + confiance + entrée + invalidation), **3 scénarios** (pessimiste/probable/exceptionnel), graphique LWC, **raisonnement du comité**.
- **Interaction** : vérifier verdict → scénarios → invalidation → graphique → comité ; puis tester `ZZZZZ`.
- **Résultat attendu** : sur `ZZZZZ`, **DATA_INSUFFICIENT** honnête (« Vertex ne tranche pas »), aucune probabilité inventée.
- **Anomalie à signaler** : scénario avec probabilité chiffrée fabriquée ; verdict positif sans données.
- **Capture** : Carte-Verdict + DATA_INSUFFICIENT.

### 5. Portefeuille — `[ ]`
- **URL** : `/portfolio` (+ `?view=positions` / `performance` / `risk`)
- **État attendu** : Synthèse (Hero + risque dominant + action + 4 KPI + Diff), tableau canonique avec **état de thèse**, **garde-fou perdants**, concentration S+/S/A/B, Performance (équité/drawdown/contribution).
- **Interaction** : vérifier concentration → états de thèse → garde-fou (un perdant sans confirmation → « Renforcement interdit ») → ouvrir une position dans Analyse → ouvrir Performance.
- **Résultat attendu** : « cassée » seulement si invalidation franchie ; aucun « renforcer » sur un perdant sans confirmation.
- **Anomalie à signaler** : « cassée » sur simple baisse ; suggestion de renforcer une perte.
- **Capture** : Synthèse + tableau (mobile = cartes).

### 6. Options — `[ ]`
- **URL** : `/options` (défaut = **Structure**) (+ `?view=leaps` / `positions`)
- **État attendu** : **Carte-Verdict d'asymétrie**, Carte-Scénario (échéance), **payoff canonique**, **Greeks interprétés**, **liquidité**, LEAPS explicable.
- **Interaction** : choisir un sous-jacent → vérifier verdict/payoff/Greeks/liquidité → LEAPS → vue positions (un perdant sans confirmation).
- **Résultat attendu** : PoP/Greeks étiquetés « estimation » (jamais garantis) ; « Renforcement interdit » sur option perdante sans confirmation ; Greeks « Insufficient » sans IV.
- **Anomalie à signaler** : PoP 100 % ; Greeks aberrants ; verdict positif si liquidité insuffisante.
- **Capture** : Structure (verdict + payoff) + positions.

### 7. Journal — `[ ]`
- **URL** : `/journal` (défaut = **Discipline**) (+ `?view=journal` / `learnings` / `progression` / `track-record`)
- **État attendu** : Hero éditorial **calculé sur tes décisions** (jamais « 92 % » inventé), KPI comportementaux, hypothèses, erreurs, leçons, biais, progression.
- **Interaction** : vérifier que le Hero reflète les vraies décisions ; parcourir erreurs/hypothèses/leçons ; confirmer **absence de courbe de performance de portefeuille**.
- **Résultat attendu** : la performance de portefeuille n'apparaît PLUS au Journal (elle est dans Portefeuille).
- **Anomalie à signaler** : pourcentage de discipline non expliqué ; courbe d'équité/drawdown présente ici.
- **Capture** : Discipline (Hero + KPI).

### 8. Système — `[ ]`
- **URL** : `/system` (+ `?view=data`)
- **État attendu** : **Hero technique** (« Système opérationnel/dégradé » + IBKR + fraîcheur + erreurs + lecture seule), cockpit (moteurs, canaux honnêtes, diagnostics, version).
- **Interaction** : vérifier IBKR (état honnête), **READONLY affiché + confirmé serveur**, fraîcheur par domaine, moteurs, version SW.
- **Résultat attendu** : « READONLY — aucun ordre possible » ; états démo/offline honnêtes.
- **Anomalie à signaler** : « connecté » sans preuve de session ; READONLY non confirmé.
- **Capture** : Hero technique + Données.

---

## Scénario humain complet (A→H)
Exécuter le parcours décrit ci-dessus dans l'ordre A (Aujourd'hui) → H (Système), en
vérifiant à chaque étape les conclusions, unités, sources, fraîcheurs, la lisibilité
des graphiques, le retour navigateur et le contexte ticker. Noter toute anomalie.

## Accessibilité (manuelle) — `[ ]`
- `[ ]` Navigation **Tab** sur toute la page ; ordre de focus logique.
- `[ ]` **Focus visible** sur chaque élément interactif.
- `[ ]` Activation **Entrée/Espace** sur boutons/onglets.
- `[ ]` **Escape** ferme modales et drawers.
- `[ ]` Compréhension **sans couleur** (P&L/verdicts lisibles par le texte).
- `[ ]` **Zoom navigateur 200 %** : pas de perte de contenu ni de débordement.
- `[ ]` **prefers-reduced-motion** respecté (si testable).
- `[ ]` **Tableaux** lisibles (en-têtes, `data-label` en mobile).
- `[ ]` **Titre clair (H1)** unique par page.

## Responsive sur appareil physique — `[ ]`
- `[ ]` **Ordinateur réel** : navigation, scroll, drawers, modales, graphiques, retour navigateur.
- `[ ]` **Téléphone/tablette réel** : touch targets, tableaux → cartes, portrait, lisibilité, **aucun zoom forcé**.
- ⚠️ **Règle** : sans validation sur appareil physique, le statut final reste **NO-GO POUR FUSION** (même si RC1 technique = GO).

## Anomalies observées
_(à remplir : espace · sévérité · description · capture)_

## Corrections appliquées pendant ce portail
- **Service worker v50 → v51** (purge du cache runtime pré-suppression ; empêche un
  client hors-ligne de servir une ancienne page Marchés référençant les 6 graphes
  supprimés). Gardiens : `test_sw_cache_safety_rc1.py` (4 tests) + gardiens de version.
- _(autres corrections éventuelles : bugs constatés, débordements, liens morts, erreurs
  console, incohérences éditoriales, erreurs cache/SW — un commit séparé chacun.)_

## Décision service worker : **v51**
Le précache n'épingle que `manifest` + `icône` (aucun asset obsolète possible), mais le
cache **runtime** (network-first) pouvait conserver une ancienne page Marchés. Le bump
**v51** force la purge de tout cache ≠ v51 à l'activation → aucun asset obsolète servi
durablement. Mise à jour v50→v51 : à l'activation, `caches.keys()` supprime `td-shell-v50`,
`clients.claim()` prend la main ; le prochain chargement re-fetch tout en réseau-first.

## Décision humaine
- **Statut** : `PENDING` → _(à mettre à `GO FOR PR` ou `NO-GO FOR PR` par l'humain)_
- **Appareils physiques testés** : `[ ] oui  [ ] non`  → si **non**, statut = `NO-GO FOR PR`.
- **Confirmation explicite de l'utilisateur** : _(signature / phrase d'accord)_
- **Date de décision** : _(à remplir)_

> Tant que ce document reste `PENDING`, **aucune Pull Request n'est ouverte**, aucune
> action sur `main`, aucun tag, aucune release.
