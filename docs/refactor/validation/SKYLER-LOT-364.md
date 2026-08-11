# SKYLER LOT 364 — « Ce que le projet dit de lui-même » : la purge É1 a emporté ses propres gardiens sans le dire

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-364` (base : lot 363 fusionné,
6fdb033)

## Piste calibrée

La veine « règle écrite vs code servi » est épuisée sur les 6 règles de
`CLAUDE.md`. Même question, portée cette fois sur les **auto-références** du
projet : *ce qu'un fichier ou un document dit de lui-même est-il encore vrai ?*

Précédent : le **lot 71** avait trouvé une docstring citant un gardien
inexistant (`tests/test_readonly_gateway.py`) et posé un contrat — toute
référence `tests/test_*.py` **dans `vertex/`** doit exister. Deux angles morts
subsistaient : le monolithe `terminal.py`, et les **documents**.

## Mesure — trois familles d'auto-références

```text
═══ A. références tests/ HORS du périmètre du lot 71 ═══
fichiers balayés : terminal.py + docs/**.md
références de tests INEXISTANTS : 7

═══ B. chemins de modules vertex/**.py cités ═══
références de modules INEXISTANTS : 0

═══ C. routes /api/... citées en docstring/commentaire ═══
routes citées distinctes : 29 · INCONNUES de l'url_map : 0
```

**B et C sont sains** : aucun chemin de module mort, et les 29 routes citées en
commentaire existent toutes dans l'`url_map`. `terminal.py` ne cite non plus
aucun gardien inexistant.

**A : les 7 références mortes sont toutes dans `docs/`**, et l'enquête git les
explique entièrement :

| Fichier cité | Créé | Supprimé |
|---|---|---|
| `tests/test_dead_functions_lot185.py` | lot 185 (`5fba96d`) | **lot 323** (`80a1729`, PR #355) |
| `tests/test_legacy_layers_life_lot184.py` | lot 184 (`dbd22e0`) | **lot 323** |
| `tests/test_legacy_pages_life_lot183.py` | lot 183 (`b560cdd`) | **lot 323** |
| `tests/test_readonly_gateway.py` | jamais existé | — (citation historique du défaut du lot 71) |

## Le constat

**La purge É1 (lot 323) a supprimé trois gardiens — comme le plan le prévoyait
— et a laissé intacts les documents qui les citent.** En particulier
`ANNEXE-E1-RETRAITS.md`, qui est le document de **preuve** de la purge : sa
catégorie B s'appelle littéralement « retrait avec leurs tests » et nomme les
trois fichiers. Un lecteur qui veut vérifier les preuves de la purge cherche ces
gardiens, ne les trouve pas, et rien ne lui dit pourquoi.

Ce n'est pas un mensonge du plan — c'est un **plan sans trace d'exécution**. Et
c'est mon propre travail (lot 323) qui a créé l'écart.

## Ce que le lot livre

1. **Statut d'exécution ajouté à `ANNEXE-E1-RETRAITS.md`** : le document dit
   désormais qu'il a été exécuté au lot 323 (commit, PR, ampleur) et liste les
   trois gardiens **RETIRÉ**s avec leur lot de création. Les rapports
   `SKYLER-LOT-183/184/185.md` ne sont **pas** touchés : ce sont des archives,
   elles décrivent l'état de leur époque ; les réécrire falsifierait l'histoire.
2. **Gardien neuf** `tests/test_references_vivantes_lot364.py` (7 tests) :
   - le contrat du lot 71 **étendu à `terminal.py`** (angle mort comblé) ;
   - même contrat sur les **chemins de modules** `vertex/**.py` cités ;
   - pour les **documents vivants** (`CLAUDE.md`, `ANNEXE-E1-RETRAITS.md`,
     `SKYLER-INDEX.md`, `STATUS.md`) : citer un gardien disparu est permis **à
     condition de dire qu'il a été retiré**, sur la ligne qui le nomme ;
   - anti-vide (≥5 références suivies, ≥150 sources Python balayées).

### Preuve ROUGE

```text
ROUGE OK  faute du lot 71 rejouée dans terminal.py (angle mort du gardien 71) | restauration identique
ROUGE OK  la mention explicite de retrait disparaît de l'annexe               | restauration identique
après restauration : 7 passed
VERDICT : gardien mordant sur les 2 angles morts
```

Le premier cas rejoue la **faute historique réelle** du lot 71, mais dans le
fichier que son gardien ne regardait pas.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 363, 6fdb033) ; arbre propre.
- Suite complète : **2520 → 2527 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : le lot ne touche que `tests/` et `docs/` —
aucun octet servi, `/static` inchangé.

## Portée — ce que ce lot ne prétend pas

Aucun code n'était faux ; le produit ne s'est jamais comporté autrement que
documenté. Le défaut était une **piste de preuve rompue** dans le dossier de la
purge. Les rapports historiques restent tels quels, volontairement.

L'audit couvre trois formes de référence (fichiers de tests, chemins de modules,
routes `/api/`). Non couvert : les noms de **constantes** et de **fonctions**
cités en prose (`DESK_KEYS`, `sanitize_news()`…) — vérifiables mécaniquement
mais avec un fort taux de faux positifs ; piste possible pour un lot ultérieur.

## Suite

LOT 365 : veille active. Pistes ouvertes — noms de constantes/fonctions cités en
prose (ci-dessus) ; variantes `?view=…` non balayées par les gardiens JS
(lot 359) ; `/memory/<id>` et `/memory/cell/<g>/<k>` non couvertes (lot 359).
Prochaine échéance périodique : ~lot 370.
