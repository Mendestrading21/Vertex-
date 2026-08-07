# SKYLER LOT 228 — Intégrité SKYLER-INDEX ↔ rapports : constat + périmètre écrit + gardien

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-228` (base : lot 227 fusionné)

## Objet

Le journal de bord de la boucle (SKYLER-INDEX.md + rapports
SKYLER-LOT-N.md) est la mémoire du travail : une référence morte ou un
rapport orphelin la corrompent en silence. Vérification croisée des
deux sens, puis pérennisation.

## Mesure

- **218 rapports cités** dans l'index → **tous existent sur disque
  (0 référence morte)** ;
- **231 rapports** sur disque → 13 sans ligne d'index :
  `SKYLER-LOT-01` → `09` (dont 08A-E) — le batch correctness
  PRÉ-Institutional+, antérieur au périmètre déclaré de l'index
  (« Lots Institutional+ (10 → 12) » et suite) et retracé par
  `docs/skyler/STATUS.md`. **Hors champ PAR CONSTRUCTION — mais ce
  périmètre n'était écrit nulle part.**

## Livré

1. **Périmètre écrit** dans l'en-tête de l'index : les lots 01-09
   vivent hors index (STATUS.md), par construction — plus d'ambiguïté
   pour un lecteur futur.
2. **Gardien `tests/test_skyler_index_integrity_lot228.py`
   (4 tests)** :
   - toute référence de l'index existe sur disque (les références
     mortes cassent la suite) ;
   - tout rapport du périmètre (hors 01-09, exemption bornée par
     regex) a sa ligne d'index (les orphelins cassent la suite) ;
   - le périmètre reste documenté dans l'en-tête ;
   - anti-vide : ≥ 200 références réellement vérifiées (si le format
     des lignes change, le gardien casse au lieu de tourner à vide).

Le rituel de la boucle (rapport + ligne d'index à chaque lot) est
désormais VÉRIFIÉ par la suite au lieu d'être seulement une habitude.

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : docs/tests seulement.

## Preuves

- Nouveau gardien : **4/4 passed** (né vert, calibré avant écriture).
- Suite complète : **2486 passed / 2 skipped** (2482 + 4).

## Suite

LOT 229 : entretien suivant ou directive. Mini-bilan 226-230 attendu
au lot 230. Purge terminal.py toujours EN ATTENTE d'accord humain.
