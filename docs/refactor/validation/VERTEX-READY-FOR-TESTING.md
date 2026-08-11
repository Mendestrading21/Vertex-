# VERTEX — PRÊT POUR UNE SEMAINE DE TEST (identité bleue · verre blanc · sans orange)

> État figé et stable pour une campagne de test d'une semaine. Design finalisé
> (bleu = identité, verre blanc translucide, zéro orange), 8 espaces unifiés,
> validés navigateur sur 3 tailles d'écran. **Moteurs, calculs, contrats de
> données et IBKR READONLY : inchangés.** Branche `agent/vertex-neon-glass-graphs`.

## 1. Ce qui est FINI

- **Identité couleur** : bleu électrique `#3B82F6` (marque/action/sélection),
  vert `#2ED6A1` (gain), rouge `#FF5F69` (perte), **jaune `#EBD24E`** (attente/
  warning), violet `#9B7BFF` (options), cyan `#45D6E8` (technique). **Aucun
  orange nulle part** (favicon, bordures, warnings, fallbacks compris).
- **Surfaces** : verre **blanc translucide** neutre (`rgba(255,255,255,.03–.08)`),
  bord blanc fin, flou 20 px. Le bleu ne sert qu'aux **accents/actions**, jamais
  au fond des cartes.
- **Unification** : le style verre couvre les **8 espaces** (Aujourd'hui · Marchés
  · Opportunités · Analyse · Portefeuille · Options · Journal · Système).
- **Aujourd'hui** : objets Regime (halo + confiance + grammaire) et Catalyseurs
  (piste DTE), câblés aux vrais moteurs, états honnêtes.
- **Stabilité responsive** : correctif `.vx-kv` (clé ellipsée / valeur repliable)
  → plus aucun débordement mobile.

## 2. Validation exhaustive (navigateur)

**8 pages × 3 tailles = 24 combinaisons, toutes propres :**

| Page | 1440 | 768 | 390 |
|---|---|---|---|
| Aujourd'hui `/` | ✅ | ✅ | ✅ |
| Marchés | ✅ | ✅ | ✅ |
| Opportunités | ✅ | ✅ | ✅ |
| Analyse `/analysis/NVDA` | ✅ | ✅ | ✅ |
| Portefeuille | ✅ | ✅ | ✅ |
| Options | ✅ | ✅ | ✅ |
| Journal | ✅ | ✅ | ✅ |
| Système | ✅ | ✅ | ✅ |

Critères par combinaison : **0 débordement de page**, **0 débordement d'élément**,
**0 erreur console réelle**. (Seule exception environnementale : le CDN Google
Fonts est bloqué par le bac à sable de dev — sans effet en local/déploiement réel
où la police se charge ; le rendu reste correct via le fallback Inter.)

- `python -m pytest tests/ -q` → **991 passed, 2 skipped**.
- `python -m compileall -q terminal.py vertex` → exit 0.
- Service worker : **td-shell-v60** (cache à jour).

## 3. Comment tester (checklist d'une semaine)

**Lancer** : `python terminal.py` (port 5002) — ou en démo :
`DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python terminal.py`. Santé : `GET /healthz`.
Erreurs JS clients : `GET /api/client-log` (doit rester à 0).

À parcourir chaque jour, sur desktop ET mobile :

1. **Navigation** — les 8 espaces + sous-vues (`?view=…`), la palette de commandes
   (⌘K), la recherche globale, le repli de la sidebar, la barre mobile.
2. **Aujourd'hui** — brief, 4 KPI cliquables, diff « depuis ta dernière visite »,
   régime, catalyseurs, opportunités, alertes, portefeuille.
3. **Marchés** — régime, indices, secteurs, breadth, volatilité (onglets).
4. **Opportunités** — radar, dominante, comparaison, scatter, funnel, options.
5. **Analyse** — ouvrir plusieurs tickers (`/analysis/NVDA`…), chandeliers, plan,
   scénarios, comité.
6. **Portefeuille** — déclarer une position (localStorage), positions, risque,
   watchlist ; vérifier la synchro desk.
7. **Options** — structure, payoff, Greeks, IV, theta.
8. **Journal** — décisions, track-record, apprentissages.
9. **Système** — connexions, données, automatisations, réglages, archive ;
   confirmer **READONLY** partout.
10. **États honnêtes** — couper les données (démo) et vérifier que chaque widget
    affiche un état vide/périmé/erreur assumé (jamais un chiffre inventé).
11. **Couleur** — confirmer **zéro orange**, identité bleue, verre blanc, sur
    toutes les pages.

Signaler tout : débordement, erreur console (`/api/client-log`), chiffre douteux,
état non honnête, ou incohérence visuelle.

## 4. Invariants garantis (non touchés)

- **READONLY** absolu : aucun chemin d'ordre (`placeOrder`/`transmit`…) ; IBKR
  en lecture seule.
- **Moteurs & calculs inchangés** : la refonte est 100 % présentation (CSS +
  couche graphique) ; aucune donnée inventée ; contrats de données intacts.
- **Clés de sync desk** : inchangées.

## 5. Reste optionnel (hors périmètre « prêt à tester »)

- **BLUE-04** — convertir les 2 objets sur-mesure d'Aujourd'hui (Regime, Catalyst)
  en graphiques 100 % conventionnels (jauge standard + timeline) façon Findexa.
  Non bloquant : les objets actuels sont fonctionnels, neutres et validés. À faire
  sur demande.

## Verdict

Vertex est **cohérent, stable et complet** pour une semaine de test : identité
bleue, verre blanc, zéro orange, 8 espaces validés sur 3 écrans, 991 tests verts,
0 débordement, 0 erreur console, READONLY et moteurs intacts. **Bon pour tester.**
