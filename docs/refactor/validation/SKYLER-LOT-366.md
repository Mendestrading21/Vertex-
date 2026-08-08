# SKYLER LOT 366 — La trouvaille du lot 365 était isolée : 110 moteurs passés à la question

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-366` (base : lot 365 fusionné,
0fea9f3)

## Piste calibrée

Le lot 365 a trouvé un moteur — `thesis_health` — qui annonçait la dimension
PORTFOLIO_FIT sans jamais la calculer. Question de ce lot : **est-ce isolé, ou
est-ce un motif ?** Les 110 modules de `vertex/engines`, `vertex/positions`,
`vertex/options`, `vertex/scanner`, `vertex/strategy` et `vertex/ai` sont passés
à la même question.

## Deux erreurs de méthode, payées comptant

La règle de ce lot était explicite : *si un audit produit un résultat
surprenant, vérifier la méthode avant de conclure.* Elle a servi deux fois.

**1. Premier filtre trop large.** Tout jeton majuscule de ≥ 4 lettres →
**139 « suspects »**, noyés dans les mots français en capitales (ANOMALIES,
PORTEFEUILLE, CROISSANCE, INVESTISSEMENT…). Inexploitable. Filtre retenu : un
**souligné exigé** — un identifiant machine, pas un mot de prose.
**139 → 10 candidats**, triables un par un.

**2. Périmètre de recherche trop étroit.** Chercher l'identifiant dans le
**seul module** qui l'annonce produit des faux positifs :

| Candidat | Verdict |
|---|---|
| `ULTRA_CONVEX` (`call_selector.py`) | **produit** — `CATEGORY_ULTRA_CONVEX` dans `options/models.py`, servi via `CALL_CATEGORIES` |
| `MODEL_ESTIMATE` (`scenario_pricer.py`) | **produit** — `GREEKS_MODEL = 'MODEL_ESTIMATE'` dans `options/models.py`, et deux tests l'asserted |

La recherche doit couvrir le **paquet**, pas le fichier.

## Verdict : aucune autre promesse non tenue

Les 10 candidats, triés :

| Famille | Jetons | Statut |
|---|---|---|
| Contrats de gouvernance | `SKYLER_ARCHITECTURE`, `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS` | légitimes — vérifiés présents dans le SKILL et les rapports |
| Notation mathématique | `S_T` | légitime (cours à l'échéance) |
| Constantes d'un module frère | `ULTRA_CONVEX`, `MODEL_ESTIMATE` | produites, via `options/models.py` |
| Absence assumée | `PORTFOLIO_FIT` | c'est la note du lot 365 elle-même, qui dit qu'il n'est PAS évalué |

**La trouvaille du lot 365 était isolée.** Rien d'autre à corriger — et rien n'a
été touché : « sain » est le verdict, pas un aveu d'échec.

## Ce que le lot livre quand même

Ce qui manquait n'était pas un correctif, c'était la **permanence de la
vérification** : deux lots de suite ont posé la question avec un script jetable.

**Gardien neuf** `tests/test_promesses_docstrings_lot366.py` (3 tests) :

1. anti-vide (≥ 90 modules balayés, ≥ 60 docstrings de module) ;
2. **tout identifiant machine cité dans une docstring de moteur doit exister
   dans le code du paquet `vertex/`** — sauf les familles tolérées, recensées et
   justifiées ci-dessus ;
3. **chaque tolérance de gouvernance doit rester justifiée** : un contrat cité
   mais absent du SKILL et des rapports fait échouer le gardien — une tolérance
   sans preuve deviendrait un trou.

Le message d'échec rappelle la règle du lot 365 : **corriger la doc, jamais
implémenter à la volée le calcul manquant.**

### Preuve ROUGE

```text
ROUGE OK  faute du lot 365 rejouée dans un AUTRE moteur : sortie annoncée, jamais produite | restauration identique
ROUGE OK  une tolérance de gouvernance sans justification dans le SKILL ni les rapports    | restauration identique
après restauration : 3 passed
VERDICT : gardien mordant sur les 2 cas
```

Le premier cas ajoute à `anomaly.py` une anomalie `GAP_RUPTURE` annoncée et
jamais produite — la faute du lot 365, transplantée dans un autre moteur. Le
gardien l'attrape.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 365, 0fea9f3) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise (aucun octet servi ne peut avoir bougé).
- Suite complète : **2530 → 2533 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Le filtre exige un souligné : une promesse écrite en un seul mot majuscule
(`BALANCED`, `EXTREME`) échappe au gardien. C'est le prix du bruit évité — et
c'est dit ici plutôt que caché. Les docstrings de **fonctions** ne sont pas
balayées, seules celles de modules.

## Suite

LOT 367 : veille active. Pistes ouvertes — variantes `?view=…` non balayées par
les gardiens JS (lot 359) ; `/memory/<id>` et `/memory/cell/<g>/<k>` non
couvertes (lot 359) ; promesses en un seul mot majuscule (ci-dessus).
Prochaine échéance périodique : ~lot 370.
