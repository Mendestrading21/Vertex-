# SKYLER LOT 414 — Les 167 boutons servis sont tous câblés ; un bouton mort fabriqué par le JS servi ne serait vu par aucun test

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-414` (base : lot 413 fusionné,
1fa55af)

Un bouton qui ne fait rien est le défaut le plus banal d'une interface, et le
plus humiliant : le trader clique, rien ne se passe, il ne sait pas si c'est
l'application ou lui. Trois tests déclarent l'invariant. Personne n'avait mesuré
ce qu'ils couvrent **des octets servis**.

**Aucun code, aucun gardien, aucun test.**

## Le périmètre

Méthode du lot 413 : les 8 pages et leurs 26 scripts demandés au serveur en
mémoire — donc les octets que le navigateur reçoit, pas les sources.

```text
boutons dans le HTML rendu (scripts retirés)   85
boutons fabriqués par le JS servi              82   (inline de page 64 · /static 18)
────────────────────────────────────────────────
total                                         167
```

**Correction de cohérence interne** : une première passe annonçait **231**
boutons. Elle comptait deux fois ceux qui vivent dans un `<script>` inline —
une fois dans le HTML de la page, une fois dans le corpus JS. Chiffre retenu :
**167**.

## Le verdict, avec un critère durci

```text
câblés par un attribut inline (onclick / submit)    18
câblés par un id accroché dans le JS servi          87
câblés par un attribut data-* délégué               62
────────────────────────────────────────────────────
SANS ÉCOUTEUR                                        0
```

Le critère n'est pas « le nom apparaît quelque part » : l'id doit apparaître
comme **littéral cité** ET à moins de 70 caractères d'un accesseur
(`getElementById`, `querySelector`, `$(`, `addEventListener`, `closest`…). Les
62 `data-*` ont été **ouverts** : 16 attributs distincts, chacun avec son site
de consommation nommé — `data-open-analysis` (53 boutons), `data-entity-menu`
(10), `data-close-drawer`/`data-close-modal` (vx-shell.js), `data-filter-key`,
`data-i` (`btns.forEach(b => b.addEventListener(…))`, vx-entities.js:296)…

**Témoins** : bouton nu → mort · `data-zzz-lot414` inconnu → mort · id
inexistant → mort · `onclick` réel → câblé · `id="vx-collapse-btn"` (accroché
via l'aide `$()`) → câblé.

## L'instrument s'est encore trompé — et c'est la même faute

Un premier durcissement exigeait `getElementById('id')` ou `#id`. Résultat :
**55 boutons « morts »**, dont `vx-collapse-btn`, `vx-notifs-btn`,
`vx-mobile-nav-btn` — des boutons qui marchent manifestement. Un vivier qui mord
sur des boutons évidemment vivants accuse l'instrument, pas le produit.

Cause : `vx-shell.js` accroche par une **aide locale**, `$('vx-collapse-btn')`.
**Troisième répétition de la même faute** — lot 409 (`emptyCard`), lot 413
(`get(...)`), lot 414 (`$(...)`). Corrigé en cessant d'énumérer les accesseurs :
le critère est désormais « littéral cité **près** d'un accesseur, quel qu'il
soit ».

## Ce que les trois gardiens couvrent vraiment — mesuré par mutation

Un bouton mort (`data-zzz-lot414`, consommé par personne) a été déposé à deux
endroits, et les gardiens rejoués.

**Dépôt n°1 — dans le shell (`vertex/ui/shell/__init__.py`)** :

```text
test_production_guards_canonical.py::test_every_button_has_handler   MORD ✔
test_ui_v3.py::test_no_dead_buttons                                  passe
test_production_guards_canonical.py::test_no_dead_buttons            passe
```

`test_ui_v3` ne pouvait pas mordre : il **court-circuite** dès qu'un attribut
`data-` existe (`if 'onclick=' in attrs or 'data-' in attrs … : continue`), sans
vérifier qu'un écouteur le consomme. Sur le périmètre servi, cela **exempte 62
des 167 boutons**. Ce n'est pas grave en soi — l'autre gardien fait le travail.

**Dépôt n°2 — dans un fichier JS servi (`vertex/static/vertex/js/vx-entities.js`)** :

```text
les trois gardiens                                                   passent
suite complète                                                       1 failed
   └─ et l'unique échec est test_sw_cache_scope_lot361 (empreinte /static)
```

L'échec ne dit rien du bouton : il dit qu'un octet de `/static` a bougé. Et
comme le flux de travail impose de toute façon de remettre l'empreinte à jour :

```text
octet /static modifié · empreinte mise à jour · bouton mort servi
suite complète →  2864 passed
```

**Entièrement verte, avec un bouton inerte servi sur les 8 pages.**

Raison : `test_every_button_has_handler` balaie `vertex/ui/pages/*.py` et le
shell — **pas `vertex/static/**/*.js`**. Or **18 des 167 boutons servis** sont
fabriqués là. C'est le même défaut de périmètre que le lot 385 (recensement
s'arrêtant à `vertex/`) et le lot 381 (liste gardée qui n'est pas celle qui est
servie), sur un troisième objet.

## Ce que ce lot établit, et ce qu'il n'établit pas

**L'invariant tient aujourd'hui : 0 bouton mort sur 167 servis**, avec un critère
durci et cinq témoins. Le zéro est **substantiel**.

**Le filet, lui, a un trou mesuré** : un bouton mort ajouté dans un fichier JS
servi passerait les 2 864 tests. Je ne comble pas ce trou — un gardien livré
« parce qu'un trou existe » est exactement ce que la boucle s'interdit depuis le
384, et l'invariant n'est pas violé aujourd'hui. **Classé rang 3** : élargir le
périmètre de `test_every_button_has_handler` aux fichiers `vertex/static/**/*.js`
est une petite décision de conception (le critère `data-*` devrait alors accepter
la délégation inter-fichiers), pas une réparation urgente.

**Portée** : le contrôle établit qu'un écouteur **existe**, pas que le clic
produise le bon effet. Un bouton correctement câblé sur une action cassée
passerait. Et l'analyse est statique : un bouton dont l'attribut serait calculé
au vol (`'data-'+kind`) échapperait au recensement — mesuré à **0** occurrence
dans le corpus servi.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier livré modifié.** Les deux sondes (shell, `vx-entities.js`) et
  la mise à jour d'empreinte ont été **restaurées à l'octet**, puis vérifiées
  **par l'instrument lui-même** : `test_sw_cache_scope_lot361` → 5 passed,
  `git status` vide. Pas de preuve MD5 requise, pas de bump. SW :
  `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels ré-horodatés par les passes de suite, restaurés. Écart final
  **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée après restauration.

## Où en est la boucle

Dix-huitième lot court. Le point contrôlé change encore de famille : après les
chemins (413), les surfaces cliquables. Le résultat est double, et c'est le bon
équilibre — **le produit est sain, le filet ne l'est qu'à 149 boutons sur 167.**

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
