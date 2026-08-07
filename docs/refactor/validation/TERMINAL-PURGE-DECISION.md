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

### 1c. Volume — CHIFFRÉ au lot 249 (outillé, reproductible)

terminal.py = **10 743 lignes / 1 222 911 octets**. Mark-and-sweep sur
l'AST (outil : `tools/purge_e2_sizing.py` — racines vivantes = fonctions
routées mesurées en runtime + fonctions décorées + code module-level +
références externes) :

- **Borne BASSE certaine : 3 370 lignes mortes (31,4 %) / 408 168
  octets (33,4 %)** — 82 définitions top-level injoignables même en
  comptant vivantes toutes les références par chaîne.
- **Borne HAUTE : 5 236 lignes (48,7 %) / 692 382 octets (56,6 %)** —
  107 définitions, si les boucles d'injection module-level
  (`globals()['PAGE_…']`, lignes ~6537-6588) partent avec les 12
  constantes PAGE_* qu'elles traitent et leurs blocs JS/CSS nourriciers
  (_PORTSIM_JS 495 l., _TRADES_JS 439 l., _DESK_COCKPIT_JS 427 l.,
  _SI_JS 360 l., …).

L'écart entre les deux bornes est EXACTEMENT la machinerie d'injection
par chaîne — d'où la découverte 1d ci-dessous.

### 1d. Piège mesuré : références par CHAÎNE (invisibles au grep de noms)

Deux mécaniques module-level compliquent l'Étape 2 et sont maintenant
cartographiées :

1. **Boucles d'injection** `for _pg in ('PAGE_DAILY', 'PAGE_WATCHLIST',
   …): globals()[_pg] = …` (nav unique, kit VX) — 12 constantes PAGE_*
   n'apparaissent qu'en chaînes ; les retirer sans adapter ces boucles
   = `KeyError` à l'import.
2. **Dépendance croisée supplémentaire (en plus de PAGE_DAILY ↔
   home_art/vault)** : `_OPP_BRIEF_JS` est EXTRAIT de
   `PAGE_ENTREPRISES` à l'import puis injecté dans `PAGE_DAILY`
   (lignes ~6088-6097, avec assert). PAGE_ENTREPRISES est donc une
   dépendance de build de la page vivante → à traiter en Étape 3, pas
   avant.

## 2. Le plan — par étapes SÛRES, une PR par étape, rollback = revert

| Étape | Contenu | Filet |
|---|---|---|
| **É1** | Retirer les 21 fonctions orphelines + les constantes `PAGE_*` qu'elles sont seules à consommer + adapter/retirer les tests de caractérisation devenus sans objet (lot 183 & épingles associées — ils existaient POUR ce moment) | pytest 100 % + serveur DEMO + balayage navigateur 8 pages + 0 erreur console ; PR séparée, revert trivial |
| **É2** | Retirer les blocs BODY/CSS/JS devenus non référencés après É1 — chiffrage DÉJÀ fait (lot 249, § 1c : 31,4 % → 48,7 % selon le sort des boucles d'injection § 1d) ; l'outil `tools/purge_e2_sizing.py` se rejoue après É1 pour la liste exacte | idem É1 |
| **É3** | Dépendances croisées : `PAGE_DAILY` ↔ `home_art.py` / `vault.py` **et** `PAGE_ENTREPRISES` → `_OPP_BRIEF_JS` → `PAGE_DAILY` (§ 1d) — décider leur sort (hérités eux aussi) | idem, décision humaine dédiée |

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
