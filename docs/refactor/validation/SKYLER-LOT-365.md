# SKYLER LOT 365 — Un moteur qui annonçait une dimension qu'il ne calculait pas

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-365` (base : lot 364 fusionné,
b257d1a)

## Piste calibrée

Suite directe du lot 364 : celui-ci avait couvert trois formes d'auto-référence
(fichiers de tests, chemins de modules, routes `/api/`) et laissé les
**identifiants cités en prose** — la piste (a) proposée. On la prend.

Méthode : extraire des docstrings et commentaires de `vertex/` + `terminal.py`
les identifiants sous deux formes calibrées — constantes `CAPS_SNAKE` et appels
`nom()` — puis vérifier qu'ils apparaissent dans le code réel du dépôt
(`vertex/`, `terminal.py`, `tests/`, hors commentaires).

## Mesure

```text
CONSTANTES citées : 117 · introuvables dans le code : 16
APPELS cités : 23 · introuvables dans le code : 0
```

**Aucun appel de fonction cité n'est mort.** Les 16 constantes « introuvables »
ont été examinées une par une — elles ne sont, pour la plupart, pas des
identifiants Python :

- **noms de contrats de gouvernance** (`SKYLER_ARCHITECTURE`,
  `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS`, `SCENARIO_CALIBRATION`) —
  vérifiés présents dans `.claude/skills/vertex-skyler-v2/SKILL.md` et les
  rapports ;
- **notation mathématique** (`S_T` = cours à l'échéance) ;
- **nom de document** (`VERTEX_WIDGET_LIBRARY`) — *j'ai d'abord cru ce fichier
  disparu : ma vérification cherchait la chaîne dans le contenu des documents,
  pas dans les noms de fichiers.* `docs/visual/VERTEX_WIDGET_LIBRARY.md` existe
  bien ;
- **codes d'anomalie** (`VOL_SHIFT`) — le moteur émet `'vol_shift'` en
  minuscules, la docstring les présente en majuscules : convention d'écriture,
  pas une divergence.

**Une seule divergence réelle en est sortie.**

## La trouvaille

`vertex/positions/thesis_health.py` annonçait **sept** dimensions :

> Dimensions : FUNDAMENTAL, CATALYST, TECHNICAL, SENTIMENT, **PORTFOLIO_FIT**,
> RISK, DATA_QUALITY

Son code n'en évalue que **cinq sections** :

```text
29:    # FUNDAMENTAL
37:    # CATALYST
43:    # TECHNICAL — invalidation = franchissement CONFIRMÉ du stop
57:    # SENTIMENT
65:    # RISK / DATA_QUALITY
```

**Aucune ligne ne regarde l'adéquation au portefeuille.** Le module fait
97 lignes ; la vérification est exhaustive, pas un sondage.

Ce n'est pas anodin : `portfolio_fit` **existe vraiment ailleurs** —
`vertex/scanner/stages.py` (« compatibilité portefeuille non évaluée ») et
`vertex/strategy/executive_engine.py` (champ `portfolio_fit` du packet). Un
lecteur — ou un futur moi — pouvait donc raisonnablement croire que la santé de
thèse en tenait compte. Elle n'en tient pas compte, et cette santé alimente
l'état de thèse affiché sur Portefeuille.

## Correctif

La docstring dit désormais **ce que le module évalue et ce qu'il n'évalue
pas** : PORTFOLIO_FIT est explicitement signalé comme non calculé ici, avec
l'indication des modules qui le produisent réellement.

**Aucune dimension n'a été ajoutée.** Implémenter à la volée une adéquation au
portefeuille aurait été pire que le mensonge : un chiffre inventé dans un
verdict de santé. Si vous voulez la dimension, c'est une décision produit
(quelles données ? poids, concentration, corrélation ?) — **en attente de GO**.

## Gardien

`tests/test_thesis_health_dimensions_lot365.py` (3 tests) :

1. anti-vide : les sections attendues existent bien dans le code ;
2. **chaque dimension annoncée dans la docstring existe comme section** ;
3. **PORTFOLIO_FIT reste écrit comme NON évalué** tant qu'il n'est pas
   implémenté — et si un jour il l'est, le gardien réclame explicitement sa
   mise à jour.

### Preuve ROUGE

```text
ROUGE OK  la faute d'origine rejouée : PORTFOLIO_FIT réannoncé comme évalué | restauration identique
ROUGE OK  une dimension annoncée perd sa section dans le code               | restauration identique
après restauration : 3 passed
VERDICT : gardien mordant sur les 2 cas
```

Le premier cas **rejoue la faute réelle** trouvée ce lot.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 364, b257d1a) ; arbre propre.
- Un fichier de **production** a changé (`thesis_health.py`, docstring seule) —
  donc preuve exigée. Serveur DEMO (`/scan` 20 lignes, `source=demo`),
  **MD5 des 8 pages : 0 écart / 8**. Aucun octet servi n'a bougé.
- Suite complète : **2527 → 2530 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : les 8 MD5 le prouvent, `/static` inchangé.

## Une erreur de méthode, corrigée en cours de lot

Ma première vérification des noms de documents cherchait la chaîne dans le
**contenu** de `docs/`, pas dans les **noms de fichiers** — elle a déclaré
`VERTEX_WIDGET_LIBRARY.md` introuvable alors qu'il existe. Signalé ici parce
qu'un audit qui produit un faux positif silencieux est aussi dangereux qu'un
gardien qui ne mord pas.

## Suite

LOT 366 : veille active. Pistes ouvertes — variantes `?view=…` non balayées par
les gardiens JS (lot 359) ; `/memory/<id>` et `/memory/cell/<g>/<k>` non
couvertes (lot 359). Prochaine échéance périodique : ~lot 370.
