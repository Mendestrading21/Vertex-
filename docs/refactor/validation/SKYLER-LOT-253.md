# SKYLER LOT 253 — Annexe É1 : la liste exacte des retraits (0 purge)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-253` (base : lot 252 fusionné)

## Objet

Rendre le « GO purge étape 1 » EXÉCUTABLE sans ambiguïté : quand
l'accord tombera, la liste des retraits ne sera pas à reconstruire —
elle est générée, triée et gardée dans le dépôt. **Rien n'est purgé.**

## Livré

### 1. Mode `--e1` ajouté à l'outil officiel

`tools/purge_e2_sizing.py --e1` émet en markdown : la liste exacte des
**82 défs** du périmètre É1 (borne basse certaine — injoignable sans
toucher aux boucles d'injection) avec genre/spans de lignes/taille, et
les fichiers de tests qui les référencent. Corrigé au passage : le grep
des tests matchait un artefact binaire `__pycache__` → `--include=*.py`.

### 2. `ANNEXE-E1-RETRAITS.md` — triage en 3 catégories d'action

- **A — retrait sec** : défs non référencées par tests/ (la majorité).
- **B — retrait avec leurs tests** : défs épinglées par les tests de
  caractérisation écrits POUR ce moment (lot183 : 13 réfs, lot184 : 20,
  lot185 : 29, + épingles nav/options_lab/journal_page/home_art).
- **C — re-cibler le test, PUIS retirer l'alias** : découverte du lot —
  `_rsi`/`_atr`/`_adx`, `_demo_one`, `_vehicle_of`, `_swing_project`
  sont des ALIAS de compatibilité re-exportant des moteurs VIVANTS
  (`vertex/engines/indicators`, `vertex/data/demo`, `strategy_fit`,
  swing) ; les tests fonctionnels qui les importent via terminal
  gardent leur valeur — seul l'import doit changer avant le retrait.

### 3. Faux positifs documentés (doctrine)

`home` matché dans `test_auth_routes.py` (fonction LOCALE du test) et
`test_live_engine.py` (mot dans un commentaire) — vérifiés dans la
source, marqués « à ignorer » dans l'annexe au lieu d'être promus
en dépendances.

## Mise à jour du dossier

`TERMINAL-PURGE-DECISION.md` : ligne É1 du plan → pointe l'annexe et
la catégorie C. La décision demandée reste inchangée.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs + outil seulement.

## Preuves

- Annexe régénérable : `python3 docs/refactor/validation/tools/purge_e2_sizing.py --e1`.
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 254 : entretien ou directive. La purge attend « GO purge étape 1 » —
désormais avec sa liste d'exécution prête.
