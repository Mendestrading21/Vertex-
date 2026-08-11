# SKYLER LOT 298 — Gardien transversal : plus jamais un « live » menteur

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-298` (base : lot 297 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — généraliser la leçon des lots 296/297

Deux mensonges corrigés coup sur coup avaient la MÊME cause : un mode
de fraîcheur « live » codé EN DUR pour des données de marché qui ont
un repli ou une variante démo. Inventaire complet
(`,'live')` + `mode:'live'` sur terminal.py, vertex/ui/**,
vertex/static/js/**) : il ne reste que 2 sites, tous deux dans
system_page — et le calibrage les juge HONNÊTES : registre des jobs et
rapport de démarrage sont l'état INTERNE du serveur, lu à l'instant,
sans repli ni variante démo possible. Rien à corriger : le livrable
est le gardien qui codifie cette règle à l'échelle de l'app.

## Livré — `tests/test_freshness_mode_guard_lot298.py` (2 tests)

Interdit tout `,'live')` (updateIndicator) et `mode:'live'` (VXCharts)
codé en dur dans terminal.py, vertex/ui/** et vertex/static/js/**,
avec 2 exceptions DOCUMENTÉES dans le test :
- `system_page.py` — état interne du serveur ;
- `widget_lab.py` — bibliothèque de design figée (pastilles « live » =
  spécimens d'exposition, pas des affirmations sur des données).

1er run ROUGE (méthode) : le gardien a attrapé widget_lab — jugé
spécimen légitime, exception ajoutée avec sa justification.

## Preuves

- Inventaire : 0 offenseur hors exceptions (le gardien le fige).
- Suite complète : **2512 passed / 2 skipped** (+2).

## Décision SW

**Pas de bump** (`td-shell-v184`) : tests seuls, aucun octet servi
modifié.

## Suite

LOT 299 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
LOT 300 = échéance périodique (smoke-check + mini-bilan 288-299).
