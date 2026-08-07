# SKYLER LOT 238 — Liens .md dans docs/ hors validation : constat (0 mort réel)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-238` (base : lot 237 fusionné)

## Objet

La piste proposée cinq fois, enfin prise : chercher les références
mortes vers des fichiers `.md` dans `docs/**` HORS
`refactor/validation/` (déjà couvert par le gardien du lot 228).

## Protocole

94 fichiers .md balayés. Deux formes cherchées :
- **liens markdown formels** `[…](chemin.md)` → résolution relative
  au fichier ;
- **mentions en backticks** `` `chemin.md` `` → résolution
  multi-candidats, puis pour chaque introuvable : recherche du NOM de
  fichier dans tout le dépôt (l'heuristique de chemin ne suffit pas —
  les docs citent souvent un fichier par son nom seul).

## Résultat — 0 lien mort réel

| Mesure | Valeur |
|---|---:|
| Fichiers .md balayés (hors validation) | 94 |
| Liens markdown formels vers .md | 1 → **1 valide** |
| Mentions backticks .md | 162 → 17 signalées par l'heuristique |
| … dont fichiers EXISTANTS ailleurs dans le dépôt | **14** (docs/refactor/, docs/release/, .claude/skills/vertex-skyler-v2/references/, .claude/FRAMEWORK.md) |
| … dont gabarits/raccourcis (pas des références) | **3** (`SKYLER-LOT-XX.md` ×2 — placeholder de prose ; « 08A.md à 08E.md » — raccourci de plage, SKYLER-LOT-08E.md existe) |
| **Références réellement mortes** | **0** |

Chaque signalement a été vérifié individuellement (find par nom dans
tout le dépôt) avant d'être classé — pas de « mort » déclaré sur la
foi d'une heuristique de chemin.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.
(Un gardien n'est pas pertinent ici : les mentions par nom seul sont
un usage légitime de prose ; le seul lien formel est déjà valide et
la zone à risque — validation/ — est gardée depuis le lot 228.)

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : constat pur.

## Preuves

- Détail des 17 signalements et leur résolution dans le corps du lot.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 239 : entretien suivant ou directive. Mini-bilan 236-240 attendu
au lot 240. Purge terminal.py toujours EN ATTENTE d'accord humain.
