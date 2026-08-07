# SKYLER LOT 261 — CLAUDE_VERTEX_REBUILD.md : ordre de mission périmé neutralisé

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-261` (base : lot 260 fusionné)

## Objet

Dernier `.md` racine jamais audité. Verdict : ce n'est pas une doc
d'accueil mais un **ORDRE DE MISSION pour Claude** datant de l'ère
« Total Rebuild » — et il est resté actif à la racine du dépôt.

## Le risque (réel, pas cosmétique)

Le document commande : « Travaille sur `git checkout
agent/vertex-total-rebuild` » + une liste de lectures et de livrables
de l'époque. C'est en **contradiction directe** avec la gouvernance
actuelle de CLAUDE.md (skill `vertex-skyler-v2`, branche
`integration/vertex-skyler-v2`, « les anciennes branches V4/Prism sont
des références historiques et ne doivent pas devenir la base »). Une
future session Claude qui tomberait dessus pouvait suivre l'ancien
ordre et travailler sur une branche morte.

## Vérifications AVANT de trancher (calibrage)

- Les fichiers pointés (`.claude/FRAMEWORK.md`, manifesto, skill
  total-rebuild, agents) existent — historiques.
- La branche `agent/vertex-total-rebuild` existe encore sur origin.
- Le document est référencé par les audits d'époque
  (`docs/refactor/FILE_INVENTORY.md`, `VERTEX_BASELINE_AUDIT.md`).

→ **Pas de suppression** (référencé + « ne rien purger sans accord ») :
bannière d'obsolescence en tête, qui neutralise l'ordre et redirige
vers la gouvernance actuelle.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs seulement.

## Preuves

- Diff limité à la bannière (1 bloc en tête de fichier).
- Suite complète : **2486 passed / 2 skipped**.

## État des .md racine après ce lot

Les 6 sont tous audités et sains : CLAUDE.md (214-218), README (257),
DEMARRER_ICI (258), SECURITE (259), .env.example (258, exact),
CLAUDE_VERTEX_REBUILD (261, neutralisé). Plus aucun document racine ne
contredit la réalité ou la gouvernance.

## Suite

LOT 262 : entretien espacé ou directive. La purge attend « GO purge
étape 1 ».
