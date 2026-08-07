# SKYLER LOT 249 — Chiffrage outillé de l'Étape 2 de la purge (AUCUNE purge)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-249` (base : lot 248 fusionné)

## Objet

Le dossier de décision (lot 248) estimait le mort de terminal.py à
« 25-30 % (chiffrage exact à l'Étape 1) ». Ce lot REMPLACE l'estimation
par une mesure outillée, reproductible — sans purger un seul octet.

## Livré

### 1. L'outil — `tools/purge_e2_sizing.py` (commité, rejouable)

Mark-and-sweep sur l'AST de terminal.py. Racines vivantes :
fonctions **routées** (vérité runtime `app.url_map`, 14), fonctions
**décorées** (18 — `@app.after_request`/`@app.errorhandler` s'exécutent
à l'import), noms référencés par le **code module-level** (26),
références **externes** du dépôt. Deux passes : stricte, puis
« références par chaîne comptées vivantes » (borne basse certaine).

### 2. Le chiffre — une FOURCHETTE honnête (terminal.py = 10 743 l.)

| Borne | Défs mortes | Lignes | Octets |
|---|---|---|---|
| **BASSE** (certaine) | 82 | **3 370 (31,4 %)** | 408 168 (33,4 %) |
| **HAUTE** (boucles d'injection retirées avec) | 107 | **5 236 (48,7 %)** | 692 382 (56,6 %) |

L'écart = exactement la machinerie d'injection par chaîne. Plus gros
blocs morts : _PORTSIM_JS (495 l.), PAGE_ME (449), PAGE_OPTIONS_DESK
(443), _TRADES_JS (439), _DESK_COCKPIT_JS (427), _SI_JS (360)…

### 3. Deux pièges MESURÉS (gravés au dossier, § 1d)

1. **Références par chaîne** : les boucles `for _pg in ('PAGE_DAILY',
   'PAGE_WATCHLIST', …): globals()[_pg] = …` (l. ~6537-6588) touchent
   12 constantes PAGE_* invisibles au grep de noms — les retirer sans
   adapter ces boucles = `KeyError` à l'import.
2. **Dépendance croisée NOUVELLE** (en plus de PAGE_DAILY ↔
   home_art/vault) : `_OPP_BRIEF_JS` est extrait de `PAGE_ENTREPRISES`
   à l'import puis injecté dans `PAGE_DAILY` (l. ~6088-6097, assert).
   PAGE_ENTREPRISES = dépendance de build de la page vivante → Étape 3.

### 4. Méthode (doctrine tenue)

Le premier passage donnait 49,2 % avec 4 faux positifs
(`_gzip_response`, `_security_headers`, `_err_404`, `_err_500` —
enregistrés par décorateurs). Vérifiés dans la source AVANT conclusion,
script corrigé (décorées = racines), chiffre final publié seulement
après contre-vérification par grep d'échantillons.

## Mise à jour du dossier de décision

`TERMINAL-PURGE-DECISION.md` : § 1c réécrit (estimation → fourchette
mesurée), § 1d ajouté (les deux pièges), plan É2/É3 précisé (l'outil se
rejoue après É1 pour la liste exacte). **La décision demandée reste
inchangée : « GO purge étape 1 » — rien ne sera purgé sans.**

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : docs + outil seulement,
aucun octet servi ne change.

## Preuves

- Sortie complète de l'outil (bornes, top blocs, défs sauvées par
  réf-chaîne) rejouable : `python3 docs/refactor/validation/tools/purge_e2_sizing.py`.
- Suite complète : voir commit (référence 2486 passed / 2 skipped).

## Suite

LOT 250 : mini-bilan 246-250 attendu. La purge ne démarre QUE sur
« GO purge étape 1 » de l'humain.
