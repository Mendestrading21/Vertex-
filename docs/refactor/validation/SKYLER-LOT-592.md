# SKYLER — LOT 592

## Ce que le lot établit

**La prose d'un gardien n'est pas sa règle.** Le gardien du lot 364 énonce dans
sa docstring :

> « un document **vivant** peut citer un gardien disparu **à condition de dire
> qu'il a été retiré, sur la même ligne** »

Son code fait autre chose :

```python
dit = any(nom in ligne and 'RETIRÉ' in ligne for ligne in src.splitlines())
```

— **n'importe où dans le document**, une ligne qui *nomme* le fichier et
contient le littéral `RETIRÉ` **en majuscules**. Pas la ligne citante.

**Deux écarts : la portée et le mot.** Appliquées aux mêmes citations, la règle
**exécutée** échoue sur **0** ; la règle **écrite** échouerait sur **3**.

**Le 591 a repris la formulation de la docstring sans vérifier le code. Je
retire cette interprétation — 12 → 13.**

## Le choix (lll)

Les rapports `SKYLER-LOT-NNN.md` échappent au gardien **par construction** : ce
sont des archives. Personne n'avait mesuré ce qu'elles contiennent.

## Le piège, écrit avant la mesure, classe MIXTE prévue (590-A)

| volet | verdict |
| --- | --- |
| **(a) nombre** — « des dizaines de références mortes » | **RÉFUTÉ** : **10** |
| **(b) cause** — « majoritairement la purge É1 du lot 323 » | **CONFIRMÉ** : **9 sur 10** |
| **global** | **MIXTE** |

**Deuxième MIXTE prévu d'avance, deux lots de suite.**

## Les 38 sites, lus par nature — et non comptés

Le relevé syntaxique donne **38 sites**. La lecture les sépare :

| nature | sites | part |
| --- | --- | --- |
| **PLACEHOLDER** — `lot4xx`, `SKYLER-LOT-N/XX/NNN.md` | **23** | 61 % |
| **MORTE** — a existé, a disparu, citée comme réelle | **10** | 26 % |
| **DIT L'ABSENCE** — le texte dit lui-même qu'elle n'existe pas | **3** | 8 % |
| **MON INCIDENT (590)** — le nom cité *est* la description d'une faute | **2** | 5 % |

**Un comptage syntaxique aurait annoncé 38 : 3,8 fois le nombre réel.**
Le contre-piège 591-A a payé massivement.

Les 23 placeholders sont des **gardiens proposés** dans les rapports 471→479,
avec un jeton `4xx` explicitement non résolu :
`tests/test_rr_structurel_lot4xx.py`, `tests/test_capital_inconnu_lot4xx.py`…
**Un rapport qui propose un gardien ne prétend pas qu'il existe.**

### Les quatre seules cibles réellement mortes

| cible | citée par |
| --- | --- |
| `tests/test_dead_functions_lot185.py` | rapports 185, 364 |
| `tests/test_legacy_layers_life_lot184.py` | rapports 184, 364 |
| `tests/test_legacy_pages_life_lot183.py` | rapports 183, 364 |
| `vertex/services/skyler_sweep.py` | rapport 214 |

Les trois premières sont les gardiens **supprimés par la purge É1 du lot 323** —
la cause que le piège annonçait. La quatrième est un module de service disparu,
cité dans un tableau « SANITIZED ✔ » du lot 214 : **la seule référence morte que
la purge n'explique pas**.

## Le « 7 » du lot 364, recalculé (587-A)

Le 364 annonce « **7** références de tests inexistants, toutes dans `docs/` ».
Recalculé aujourd'hui sur **son** périmètre — tout `docs/`, hors placeholders —
j'en compte **18**. L'écart se décompose, il ne s'explique pas :

| fichier | sites |
| --- | --- |
| `SKYLER-LOT-183.md` · `184` · `185` | 2 + 2 + 2 = **6** |
| `SKYLER-LOT-71.md` | **1** |
| `SKYLER-LOT-364.md` *(son propre tableau)* | **5** |
| `ANNEXE-E1-RETRAITS.md` | **6** |
| **total** | **18** |

**Les 7 du lot 364 sont exactement les 6 + 1 des rapports antérieurs à lui.**
Son nombre était **juste à sa date** ; les 11 autres sont son propre tableau et
l'annexe des retraits, écrits *pendant ou après*. **Aucune erreur — une
croissance documentée.**

## Second contrôle (481) — les documents vivants

La restriction « archives » exclut les quatre documents vivants. Le gardien les
couvre : **il passe**. Les quatre citations concernées sont dans
`ANNEXE-E1-RETRAITS.md` (3) et `SKYLER-INDEX.md` (1, un placeholder `lot4xx`).

**Le contrat tient — au sens de ce qui est exécuté.**

## L'arrêt du lot — j'ai failli contredire un test vert

Mon second contrôle, écrit avec ma propre définition (« mention de retrait sur
la ligne citante », famille de mots accentués), a conclu :

> « le contrat **NE TIENT PAS** — 3 manquements »

**La suite est verte : le gardien passe.** Un résultat qui contredit un test vert
est faux jusqu'à preuve du contraire. J'ai lu le gardien plutôt que de le
publier, et la cause était dans **ma** définition, pas dans le dépôt.

Le banc fautif est **conservé tel quel**.

**Arrêtés avant publication : 217 → 218 (+1).**

## Ce que le lot n'établit pas

- **Que ces 10 références mortes soient un problème.** Ce sont des **archives** :
  le dépôt les autorise explicitement (591-B). Rien n'est corrigé.
- Que les 23 placeholders soient tous des propositions jamais retenues : leur
  **nom** dit qu'ils sont non résolus, leur **destin** n'a pas été retracé.
- Que l'écart prose/code du gardien 364 soit un défaut : **il rend le gardien
  plus permissif que sa description**, ce qui est un constat, pas une accusation.
- Que le module `skyler_sweep.py` ait disparu au lot 323 : **non vérifié**.

## Limites déclarées

- Mon relevé compte **594 rapports**, le 591 en comptait **587** : les deux
  motifs diffèrent (`SKYLER-LOT-[\w.-]+\.md` ici, `SKYLER-LOT-\d+\.md` là — les
  variantes `08A`…`08E` entrent dans l'un et pas dans l'autre). **Deux mesures,
  deux définitions — je le déclare plutôt que de les confondre (546-A).**
- La classe PLACEHOLDER repose sur le **nom** (`4xx`, `N`, `XX`, `NNN`), pas sur
  une vérification que le gardien n'a jamais été écrit sous un autre numéro.
- Le mot `RETIRÉ` du gardien est cherché **en majuscules accentuées** : une
  variante minuscule ne le satisferait pas. Mesuré, pas supposé.

## Règles neuves

- **592-A — UN RÉSULTAT QUI CONTREDIT UN TEST VERT EST FAUX JUSQU'À PREUVE DU
  CONTRAIRE.** Lire le test avant de l'accuser.
- **592-B — LA PROSE D'UN GARDIEN N'EST PAS SA RÈGLE.** Docstring et code
  peuvent diverger sur la portée **et** sur les mots ; c'est le code qui garde.
- **592-C — UN PLACEHOLDER N'EST PAS UNE RÉFÉRENCE MORTE.** 61 % des
  « références mortes » syntaxiques sont des noms **proposés** ou des gabarits
  de prose.

## Ce que le dépôt fait bien

- **Les archives sont franches** : les rapports 471→479 nomment leurs gardiens
  proposés avec un `4xx` visible — impossible de les confondre avec un fichier
  réel si on lit.
- **`ANNEXE-E1-RETRAITS.md` existe** : un document dédié aux retraits, qui
  nomme chaque gardien supprimé et le mot `RETIRÉ` à côté.
- **Le lot 71 et le lot 364 citent `test_readonly_gateway.py` en disant qu'il
  n'a jamais existé** — la citation d'un mensonge passé, étiquetée comme telle.
- **Dix références mortes sur 594 rapports** : la mémoire du projet est
  remarquablement propre pour une archive de cette taille.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucune référence
  corrigée** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 592) **vides**

## Comptes

- Arrêtés avant publication : **218 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **13 (+1 — le « sur la même ligne » du 591)**
