# SKYLER LOT 498 — La famille `PAGE_*` auditée : les DOUZE constantes sont mortes, zéro atteint une surface servie — 61,1 % de `terminal.py` est du HTML jamais servi, et 1,43 Mo est reconstruit en mémoire à chaque démarrage

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-498` (base : lot 497 fusionné,
`9dec6710`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
AUCUNE SUPPRESSION — c'est un audit, pas une purge.**

## Le choix

J'ai pris **(a)**. La dette avait été nommée au 495, reportée au 496, reportée au
497. **Une dette reportée trois fois cesse d'être une dette et devient un
évitement**, et c'était écrit dans le réveil. **(b)** — la symétrie ROW/DÉTAIL —
**reste une dette nommée**.

## Le brief avait raison sur un point qu'il demandait de re-vérifier

Il citait « `PAGE_ME` vers L4741 » d'après le 483, en demandant de re-vérifier.
**Mesuré : `PAGE_ME` commence exactement à L4741.** Le chiffre tient.

## L'instrument, et sa PREMIÈRE calibration qui a échoué

Deux méthodes indépendantes : **(1)** chercher six fragments distincts de la
valeur finale de chaque constante dans les 42 objets servis ; **(2)** énumérer
tous les usages dans `terminal.py`, y compris les accès dynamiques.

**Calibration — témoin de CHARGE d'abord** (règle durcie au 497) :

```text
(0)  corpus       42 objets · 841 916 caracteres      = référence        OK
(0b) famille      12 constantes PAGE_* (5 littérales + 7 par `_vpage`)   OK
(A)  POSITIF      le MÊME test sur vertex/ui/pages/*.py
(B)  NÉGATIF      zzz_inexistant_498 → 0                                 OK
```

**La première version du témoin (A) a ÉCHOUÉ et le script s'est arrêté.**
J'avais pris `gnavFresh` (`terminal.py:2574`) comme témoin positif : **0 objet
servi**. Un instrument qui n'a jamais démontré qu'il sait voir un « présent » ne
peut rien conclure d'un « absent » (règles 481, 494). Témoin remplacé par le
**même test appliqué aux constantes de `vertex/ui/pages/*.py`** — des chaînes
HTML de niveau module elles aussi, mais dont on sait qu'elles sont servies
(règle 485 : un test appliqué à un objet doit s'appliquer à tous les objets du
même genre).

```text
CALIB A : 10 constantes de vertex/ui/pages/*.py TROUVÉES (jusqu'à 6/6)
          analysis_page:_JS 6/6 · briefing:_CONTENT 6/6 · briefing:_JS 6/6 …
          5 NON trouvées : design_system_demo:_CHARTS_JS · design_system_page:_DS_CSS
                           intelligence_page:_JS · widget_lab:_CSS …
```

**L'instrument distingue servi et non-servi sur le même genre d'objet** — et les
cinq non trouvées sont exactement les modules d'interface déjà connus comme
morts. Calibration valide.

## Le résultat : ZÉRO sur DOUZE

```text
constante            ligne     octets construits   lignes déf.   servie ?
PAGE_DAILY           L2353         368 428            1 486        NON
PAGE_ENTREPRISES     L5193         139 808              683        NON
PAGE_ME              L4741         111 879              449        NON
PAGE_BORDEL          L6969         109 291                –        NON
PAGE_OPTIONS_DESK    L4292         100 994              443        NON
PAGE_WATCHLIST       L3956          91 726              333        NON
PAGE_EQUIPE          L6859          89 387                –        NON
PAGE_RESEARCH        L6616          87 393                –        NON
PAGE_HEATMAP         L6716          85 274                –        NON
PAGE_SETTINGS        L6492          82 719                –        NON
PAGE_REVIEW          L6560          82 329                –        NON
PAGE_HEALTH          L6668          82 134                –        NON
                                  ─────────          ───────
                                  1 431 362 o          3 394 lignes
```

**Aucune route ne retourne aucune des douze.** Les seuls usages hors
réaffectation sont les boucles d'injection `globals()[_pg] = …` (L6256-6310,
L6999-7002), qui recopient de la navigation et des onglets **d'une constante
morte vers une autre**.

## Le faux positif que j'ai failli publier

Quatre constantes sont d'abord ressorties **« 1/6 fragments · SERVIE »** :
`PAGE_OPTIONS_DESK`, `PAGE_WATCHLIST`, `PAGE_EQUIPE`, `PAGE_RESEARCH`. J'allais
écrire « quatre des douze sont servies ». **Un seul fragment sur six est la
signature d'un morceau partagé, pas d'une page servie.** Lus :

```text
PAGE_OPTIONS_DESK  « "cls": "p-good"}, "ACHAT": {"label": "Achat", "tone": "gr »
PAGE_WATCHLIST     « cls": "p-good"}, "ACHETER": {"label": "Acheter", "tone" »
PAGE_EQUIPE        « efusé", "tone": "red", "cls": "p-bad"}, "REFUSE": … »
PAGE_RESEARCH      « SER": {"label": "Sécuriser", "tone": "strong-green" … »
```

Les quatre sont des morceaux du **dictionnaire `__VXVOCAB`**, injecté à la fois
dans les `PAGE_*` et dans les huit pages réellement servies. **C'est du
boilerplate partagé, pas la page.** Tri à la lecture (règle 488).

## Le second contrôle — une constante morte peut être la SOURCE d'octets servis

Mon instrument teste la **présence** de la valeur. Il exclut le cas où une
constante morte serait **extraite** pour nourrir une page vivante — et ce cas
existe littéralement dans le fichier :

```python
terminal.py:6263  _NAV_CSS_CANON   = _extract(PAGE_DAILY, '<style id="nav-css">', '</style>')
terminal.py:6264  _NAV_BUILD_CANON = _extract(PAGE_DAILY, '(function(){var L=', '})();')
terminal.py:6310  _VXSCATTER_JS    = _extract(PAGE_DAILY, 'function vxScatter(pts){', …)
```

Mesuré sur les extraits eux-mêmes : `_NAV_CSS_CANON` **6 068 o → 0/6 servis**,
`_NAV_BUILD_CANON` **20 252 o → 0/6**, `_VXSCATTER_JS` **3 375 o → 0/6**. **La
chaîne d'extraction reste interne à la famille morte.** Le contrôle a tourné, et
il confirme au lieu d'infirmer — je le dis plutôt que de le compter comme une
trouvaille.

**Trouvaille latérale du même contrôle** : `_SCATTER_HELP_JS` (L6311) vaut
**la chaîne vide**. L'extraction n'a pas trouvé son marqueur et `_extract` a
rendu `''` **en silence**. Sans conséquence ici — c'est du code mort — mais
c'est un mode d'échec muet, et il est mesuré.

## La mesure large : 61,1 % de `terminal.py`

Le même test appliqué à **toutes** les constantes chaîne de niveau module de plus
de 400 octets (règle 485) :

```text
19 constantes, TOUTES absentes des octets servis
  PAGE_DAILY 1486 · PAGE_ENTREPRISES 683 · PAGE_ME 449 · PAGE_OPTIONS_DESK 443
  PAGE_WATCHLIST 333 · _OV_EXTRA_JS 326 · _BORDEL_MARKET_JS 112
  _PLAYBOOK_JS 104 · _PIPELINE_SVG 103 · _RAIL_CSS 82 · _RESEARCH_JS 47
  _VPAGE_CSS 38 · _HEALTH_JS 34 · _HEATMAP_JS 33 · _REVIEW_JS 30
  _READ_CSS 26 · _PLAYBOOK_CSS 25 · _SETTINGS_JS 14 · _PLAYBOOK_BODY 1

TOTAL 4 369 lignes / 7 153 = 61,1 %
```

**Six lignes sur dix de `terminal.py` sont du HTML, du CSS et du JS qu'aucune
page ne sert**, et **1,43 Mo** de cet ensemble est **reconstruit en mémoire à
chaque démarrage** par les passes d'injection.

## Ce que je n'en fais pas

**Aucun dossier.** C'est du **code mort**, pas un défaut affiché : un utilisateur
ne peut pas être trompé par une page qui n'existe pas (règles 486, 491, 492,
494). `CLAUDE.md` dit déjà que la purge É1 du lot 323 a laissé des reliques ; ce
lot ne découvre pas leur existence, **il les chiffre** — et le chiffre était
inconnu.

**Le coût de démarrage n'est PAS mesuré en temps.** Je donne des octets, pas des
millisecondes, parce que je n'ai pas isolé le coût des constructions dans le
temps d'import. **Observation, non chiffrée.**

**Et je ne supprime rien.** L'invariant est explicite : aucune correction sans GO
humain. Ce que ce lot fournit, c'est le devis d'une purge éventuelle — **4 369
lignes, 19 constantes, 12 pages, zéro consommateur** — pas la purge.

## Portée

- « Servie » signifie ici : présente dans les **42 objets servis** du corpus de
  référence. Une page atteignable par une route hors de ce corpus
  **échapperait** — mais la méthode (2) a énuméré tous les usages, et **aucune
  route ne retourne une `PAGE_*`**.
- Les **7 constantes construites par `_vpage`** n'ont pas de « lignes de
  définition » propres : leur poids est dans les JS/CSS qui les alimentent,
  comptés séparément dans les 4 369.
- Le seuil **400 octets** pour le recensement large est **mon choix** ; en
  dessous, je n'ai pas mesuré.
- **Aucun navigateur ouvert** : la question porte sur les octets servis, que le
  `test_client` établit exactement.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** ; aucune route réseau sortante.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La dette est payée, et elle rend un chiffre que dix-huit lots de veille n'avaient
pas : **61,1 %**. C'est le genre de mesure qui ne se déduit pas — il fallait
construire le corpus servi, appliquer le test à toutes les constantes du même
genre, et **trier les faux positifs à la lecture**.

Deux faits de méthode, tous deux payés dans ce lot : **une calibration positive
mal choisie arrête le lot au lieu de le fausser** — c'est la deuxième fois après
le 496, et c'est ce qu'on attend d'elle. Et **un seul fragment trouvé sur six
n'est pas une présence : c'est un partage.** Le seuil compte autant que le test.

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
Ce lot n'ajoute pas de dossier ; il ajoute **un devis**.

Comptes séparés : résultats faux **arrêtés avant publication 75 (+2)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
