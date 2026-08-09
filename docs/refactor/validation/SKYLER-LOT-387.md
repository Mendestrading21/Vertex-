# SKYLER LOT 387 — Un test pouvait effacer les notes du trader

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-387` (base : lot 386 fusionné,
e1f8e8d)

## Piste

Le lot 386 avait mesuré que la suite complète **réécrit** `desk_data.json`
(md5 `f30f5d7da49a` → `c6beebcf97f0`) mais **sans perte** — 6 clés avant et
après, `data` byte-identique. Verdict prudent, versé au 16ᵉ dossier. Ce lot
descend au fichier de test. **La conclusion change.**

## Le dénominateur — trois fois trop étroit avant d'être juste

| tentative | méthode | trouvés |
|-----------|---------|---------|
| 1 | `grep desk/push\|desk/restore` | 4 fichiers |
| 2 | `grep desk_data\|desk/push\|desk/restore` | 15 fichiers |
| 3 | le gardien lui-même (POST `/api/desk` + `save_json`) | **17 fichiers** |

La 1ʳᵉ manquait tous les `persist.save_json('desk_data.json', …)` directs — dont
certains n'écrivent **qu'une seule clé**. La 2ᵉ manquait `test_desk_routes.py` et
`test_production.py`, qui postent sur `/api/desk` sans jamais nommer
`desk_data`. C'est mon propre gardien qui a corrigé mon périmètre.

Mesure empirique finale, chaque fichier rejoué depuis un état de référence
restauré à l'octet :

```text
16 / 17   n'écrivent PAS dans le vrai desk
           · 12 redirigent (`persist.cache_path` OU `persist._BASE_DIR`)
           ·  1 pousse 3 Mo → rejeté 413 avant la route
           ·  3 ne font que lire
 1 / 17   écrit                              test_desk_cycle_lot84.py
```

## Ce que le seul écrivain faisait vraiment

`test_desk_roundtrip_is_faithful` lit le desk réel, **écrase `myNotes`** par un
marqueur, pousse, vérifie la fidélité, puis restaure. `myNotes` n'est pas une clé
de test : c'est une **clé synchronisée** — `{"NVDA": "note"}`, les notes par
titre du trader — présente dans les trois listes de sync avec ses accesseurs
(`VXEntities.notes()`).

**La restauration n'était pas protégée.** Prouvé par mutation, l'assertion de
fidélité inversée :

```text
cas 1 — test au vert       : note rendue = True
cas 2 — assertion en échec : note rendue = False
        contenu laissé      : {"guard": "lot84-guard-1786233158"}
```

**Une assertion en échec laissait les notes du trader remplacées par un marqueur
de test, définitivement.** Et le filet ne rattraperait pas : le lot 362 a établi
que le snapshot est pris **une fois par jour, avant la première écriture** — la
suite consomme ce créneau.

### Pourquoi le lot 386 n'avait rien vu

Parce que **l'utilisateur n'a aujourd'hui aucune note** : le desk porte 6 clés,
`myNotes` n'en fait pas partie. Le chemin de perte existait sans matière à
perdre. *Un « aucune perte constatée » ne vaut que si l'on vérifie qu'il y avait
quelque chose à perdre* — le pendant exact de la règle du dénominateur.

## Correction

Un `try/finally` autour du marqueur dans `tests/test_desk_cycle_lot84.py` —
**fichier de test, aucune production touchée**, donc ni preuve MD5 ni bump.

## Gardien

`tests/test_desk_ecritures_lot387.py` (9 tests) :

- **dénominateur** — le détecteur doit voir ≥ 12 fichiers touchant au desk (17
  mesurés) et au moins une écriture, sinon la propriété serait vraie pour la
  mauvaise raison ;
- **LA propriété** — aucun test n'écrit dans le vrai desk sans rediriger
  `cache_path` ou `_BASE_DIR` ;
- **anti-péremption** du recensement des écrivains autorisés ;
- **le `finally` est verrouillé** par AST sur l'écrivain autorisé, et la remise
  en état doit bien repousser l'état initial `d0` (un `finally` qui pousse autre
  chose ne protège rien) ;
- **l'exemption est vérifiable et bornée** : le rejet 413 doit rester testé, et
  le **nombre de sites** d'écriture du fichier exempté est gelé ;
- `myNotes` doit rester une clé de sync servie — sinon tout ce qui précède
  change de nature.

### Preuve ROUGE

```text
`finally` retiré de l'écrivain autorisé                ROUGE OK  | restauration identique
remise en état vidée (ne repousse plus d0)             ROUGE OK  | restauration identique
nouvel écrivain sans redirection                       ROUGE OK  | restauration identique
myNotes retirée du repli servi de /system              ROUGE OK  | restauration identique
[témoin] écriture dans un fichier QUI REDIRIGE         ne mord pas — correct
après restauration : 9 passed
```

## Deux fois où l'outil était en cause — et une exemption trop grossière

**Ma première mutation ne mordait pas.** J'avais écrit `assert cond, ('msg' and
False)` : le `and False` portait sur le **message**, pas sur la condition. Le
test passait toujours. Corrigé en inversant `==` → `!=` dans la condition.

**Mon premier gardien accusait deux fichiers sains.** `test_desk_routes.py`
redirige par `persist._BASE_DIR` — un second mécanisme parfaitement valide que
mon détecteur ignorait — et `test_production.py` pousse 3 Mo pour vérifier le
plafond, **rejeté en 413 avant d'atteindre la route**. Un gardien qui accuse du
code sain finit désactivé (leçon du 383) : détecteur élargi, exemption motivée
et **vérifiable**.

**Mon exemption était trop grossière.** La preuve ROUGE l'a montré : exemptée au
niveau du **fichier**, elle laissait passer un écrivain ajouté après coup dans
`test_production.py`. Contrôle du lot 385 appliqué — le même défaut dans un
fichier non exempté **mord** —, puis l'exemption resserrée au **nombre de
sites**, gelé à la mesure.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- `integration/vertex-skyler-v2` à jour (tête = lot 386, e1f8e8d) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Desk : copie de sûreté prise avant toute sonde ; après la suite, `data`
  **identique à la référence**, seul `ts` diffère.
- Suite : **2817 → 2826 passed / 2 skipped** (+9). SW : `td-shell-v187`.

## Portée

Le risque corrigé était **conditionnel** : il fallait qu'une assertion tombe (ou
que la session soit interrompue) *et* que l'utilisateur ait des notes. Aucune
perte réelle n'a eu lieu. Ce que ce lot supprime, c'est le **chemin**, pas un
dégât constaté. Par ailleurs le gardien est **statique** : il lit le code des
tests, il n'observe pas leurs écritures à l'exécution — un test qui écrirait par
un chemin non textuel lui échapperait.

## Suite

Le 16ᵉ dossier est **traité et refermé**, pas seulement documenté. Restent les
pistes fines : refus construits en variable (377) · formes imbriquées des
promesses de retour (375) · trois sites de concaténation à constantes (374) · le
commentaire périmé de `vx-entities.js`.

Les quinze dossiers en attente de décision humaine n'ont pas bougé, plus celui du
lot 386 (badge de provenance temps réel). Prochaine échéance périodique :
**~lot 390**.
