# SKYLER V2 — LOT 69 : AUDIT TOTAL (volet 4) — cohérence fiche ↔ Opportunités

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-69-fiche-opps`
(base : `integration/vertex-skyler-v2` @ `9af3edd`, fraîchement fetchée).

## 1. Méthode

Sur les 3 premiers symboles de `/api/command` (ACN/AOS/MMM), croisement
réel : endpoints (`/api/command`, `/api/skyler/<SYM>`) ↔ page
Opportunités ↔ fiche `/analysis/<SYM>` en navigateur. Critères : (1) même
champ = même valeur partout ; (2) toute divergence de verdict entre
moteurs EXPLIQUÉE à l'écran ; (3) tout score porte son ÉCHELLE.

## 2. Constat principal : la divergence des moteurs est DITE — sain

Les deux moteurs divergent légitimement (command : ACHETER/RENFORCER ·
Skyler canonique : REFUSER 18-19/40, niveau REFUS_WATCH — gates
fondamentaux non branchés = 0, jamais estimés). La hiérarchie est
affichée aux deux endroits :

- Opportunités : deux sections distinctement étiquetées (« score
  Vertex /100 » · « CLASSEMENT SKYLER — SCORE CANONIQUE /40 ») avec la
  note « un score ne déclenche jamais un ordre » ;
- Fiche : « la décision finale unique reste REFUSER — les verdicts
  techniques sont des entrées du moteur exécutif ».

Aucun même champ n'affiche deux valeurs différentes. Critères 1 et 2 :
**SAINS, vérifiés en navigateur, dits.**

## 3. Critère 3 : UNE lacune de traçabilité réelle, corrigée

Les cartes SHORTLIST d'Opportunités affichaient le score nu (« 81 »,
« 74 », « 73 ») sans échelle, alors que la dominante dit « 84 /100 ».
Corrigé : le score des cartes shortlist porte « /100 » (style meta
discret). Preuve APRÈS en navigateur : « 81 /100 · 74 /100 · 73 /100 ».
**Tout score affiché porte désormais son échelle, partout.**

## 4. Tests (rouges d'abord — 2 nouveaux)

`tests/test_audit_lot69.py` : la ligne du score shortlist contient /100 ·
SW ≥ v123. (Un regex de MON test corrigé en cours de lot — dit.)

## 5. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1694 passed, 2 skipped   (1692 + 2)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v123 servi,
  cycle souverain inclus)
Navigateur APRÈS : shortlist « 81 /100 » etc. ; hiérarchie des moteurs
  dite sur Opportunités ET sur la fiche ; 0 erreur console.
```

SW `td-shell-v122` → `td-shell-v123` + 4 gardiens.

## 6. Suite

Lot 70 : états dégradés restants (/markets sans scan, mémoire Skyler
vide), puis BILAN CONSOLIDÉ n°5 (lots 66→70) et retour RC espacées.

**Arrêt après ce lot — boucle continue ré-armée (~2 min).**
