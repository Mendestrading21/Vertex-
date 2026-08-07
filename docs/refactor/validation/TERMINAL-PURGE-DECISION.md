# DOSSIER DE DÉCISION — Purge du code hérité de terminal.py

> Préparé au lot 248. **AUCUN code n'a été touché** : ce document
> rassemble les preuves et le plan pour que l'humain tranche.
> Décision demandée : **GO / NO-GO sur l'Étape 1** (les étapes
> suivantes seront soumises une par une, jamais en bloc).

## 1. Les preuves (mesurées au lot 248, reproductibles)

### 1a. Joignabilité runtime — l'argument décisif

Import réel de l'app (DEMO), croisement `app.url_map` × fonctions de
terminal.py retournant une constante `PAGE_*` :

- **21 fonctions de rendu héritées trouvées → 0 routée, 21
  ORPHELINES** (home, journal_page, vault_page, titre_page,
  strategie_page, compare_page, options_desk/lab, settings, review,
  research, health, suivi, anomalies, heatmap, equipe, bordel,
  stocks, sectors, catalysts…).
- Les 43 commentaires « [redesign] route migrée » confirment : chaque
  route vit désormais dans `vertex/app/routes/redesign.py` et sert les
  pages de `vertex/ui/pages/*` — PAS ces fonctions.

**Aucun utilisateur ne peut atteindre ces pages.** Le lot 246 l'a
constaté en conditions réelles : `/journal` sert `performance_page`,
pas `PAGE_JOURNAL`.

### 1b. Qui référence encore ce code ?

- **32 constantes `PAGE_*`** : hors terminal.py, référencées UNIQUEMENT
  par des tests de caractérisation (`test_legacy_pages_life_lot183.py`
  — écrit précisément pour épingler ce code hérité en attendant la
  purge — plus quelques épingles dans test_nav/test_options_lab/
  test_journal_page/test_home_art_lot181/test_legacy_layers_lot184).
- **Exception à traiter à part** : `PAGE_DAILY` est aussi référencée
  par `vertex/ui/home_art.py` et `vertex/ui/vault.py` (modules
  eux-mêmes hérités) → dépendance croisée, étape dédiée.

### 1c. Volume

terminal.py = **10 743 lignes**. La cartographie historique estime
**25-30 % de mort** (fonctions orphelines + constantes PAGE_* + les
blocs BODY/CSS/JS géants qu'elles sont seules à consommer). Le chiffrage
exact par bloc sera fait à l'Étape 1 (le retrait des consommateurs
révèle mécaniquement les blocs devenus non référencés).

## 2. Le plan — par étapes SÛRES, une PR par étape, rollback = revert

| Étape | Contenu | Filet |
|---|---|---|
| **É1** | Retirer les 21 fonctions orphelines + les constantes `PAGE_*` qu'elles sont seules à consommer + adapter/retirer les tests de caractérisation devenus sans objet (lot 183 & épingles associées — ils existaient POUR ce moment) | pytest 100 % + serveur DEMO + balayage navigateur 8 pages + 0 erreur console ; PR séparée, revert trivial |
| **É2** | Chiffrer puis retirer les blocs BODY/CSS/JS devenus non référencés après É1 (mesure outillée, pas d'estimation) | idem É1 |
| **É3** | Dépendances croisées : `PAGE_DAILY` ↔ `home_art.py` / `vault.py` — décider leur sort (hérités eux aussi) | idem, décision humaine dédiée |

Invariants pendant TOUTE la purge : READONLY intact, moteurs intacts,
desk sync intact (les 4 listes de clés ne bougent pas), `main` jamais
touchée, service worker bumpé seulement si un octet servi change.

## 3. Ce que la purge N'EST PAS

- Pas une réécriture : uniquement du retrait de code prouvé
  injoignable.
- Pas un big-bang : trois étapes, chacune verte et fusionnée avant la
  suivante.
- Pas une perte : tout reste dans l'historique git (revert possible à
  tout moment).

## 4. Décision demandée

**GO Étape 1 ?** — Répondre « GO purge étape 1 » (ou équivalent) dans
la conversation. Sans cet accord explicite, la boucle continue son
entretien sans toucher au code hérité.
