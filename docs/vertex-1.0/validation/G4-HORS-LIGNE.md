# G4 — Quand le réseau tombe, le produit le dit-il ?

Instrument : `tools/vertex_1_0/mesurer_hors_ligne.py`
Gardien : `tests/test_vertex_1_0_hors_ligne.py` (8 tests, 8 mutations éprouvées)
Correctif : `vertex/static/vertex/js/vx-core.js`, `vertex/ui/pages/briefing.py`, SW v211

---

## D'où vient la question

La preuve de non-usage du CSS (#781) a classé `.vx-offline-banner` « prouvée
inatteignable » : stylée dans `states.css`, rendue par personne. La conclusion
facile était « CSS mort, à supprimer ». La question utile était l'inverse : *le
produit a-t-il seulement une façon de dire qu'il est hors ligne ?*

Le balayage QA couvrait le mode démo, l'absence d'IBKR et la panne partielle. Il
ne couvrait pas le cas le plus banal : **le réseau tombe pendant qu'on regarde
l'écran** — métro, ascenseur, wifi qui décroche.

## Protocole

Chargement **en ligne** (personne n'ouvre un terminal déjà déconnecté), puis
`context.set_offline(True)`, puis deux relevés :

- **à 12 s** — la coupure vient d'avoir lieu ;
- **à 2 h** — l'horloge de la page est avancée de deux heures, réseau toujours
  coupé. C'est la phase décisive, et elle n'est pas un raffinement : **à 12 s
  une donnée est réellement fraîche** au sens des seuils du produit (20 s live,
  30 min analyse). Une puce qui dit « Analyse » à 12 s **dit vrai**. Le mensonge
  ne peut apparaître qu'au-delà du seuil.

## Ce que la première lecture disait — et pourquoi elle était fausse

Le premier tableau donnait : *8 espaces sur 8 avouent la coupure, 7 gagnent un
aveu nouveau, 12 chiffres sur 15 sont datés*. Rassurant, et faux **deux fois**,
toujours dans le sens de l'indulgence :

1. la bannière « **Démo** » était comptée comme un énoncé d'âge. Elle qualifie
   la **nature** de la donnée, pas sa date. Sur Aujourd'hui, c'était la *seule*
   marque de la carte : les quatre chiffres de tête étaient en réalité **nus** ;
2. la fenêtre d'observation (26 s) était **plus courte que la période du
   re-datage** (30 s) : on reprochait au produit un mensonge qu'il n'avait pas
   encore eu l'occasion de corriger.

Une troisième indulgence, en sens inverse : `.vx-update[data-mode="live"]` était
lu comme une affirmation de fraîcheur. C'est une **provenance** (« d'où vient la
donnée »), pas un âge — les quatre chiffres de Système ressortaient « datés
faux » à tort, leur portée contenant une ligne `/healthz Live`.

L'instrument a été corrigé avant le produit, comme aux cinq fois précédentes.

## Le défaut, mesuré

> **Un âge affiché est vrai à la seconde où il est peint, et faux ensuite.**

Horloge de la page avancée de 2 h, **réseau vivant** :

| espace | lignes de provenance | figées |
| --- | --- | --- |
| Marchés | 11 | **11** |
| Système | 7 | 3 (les 4 autres se rejouent) |

Sur Marchés, « Il y a 21 min » **indéfiniment**. Un onglet laissé ouvert deux
heures affiche un âge de vingt et une minutes.

Le calcul n'était pas en cause — vérifié dans la page, sous horloge décalée :

```
ago(même ts)          → « Aujourd'hui à 14:49 »   (juste)
assess({ageMs: 2 h})  → { state: 'stale', label: 'À actualiser' }   (juste)
```

**C'est le rendu qui n'était jamais rejoué.** `markets` et `portfolio`
n'enregistrent aucune tâche `VX.refresh` : la ligne de provenance est peinte au
chargement et plus jamais. Système, qui rafraîchit à 60 s, servait de contrôle —
et discriminait : 4 lignes sur 7 s'y rejouaient correctement.

Et réseau coupé, **plus aucune page ne repeint**, y compris celles qui
rafraîchissent d'habitude — le `fetch` échoue, le loader s'arrête, le DOM reste.

Second défaut, sur la page d'accueil : `freshBadge()` de `briefing.py` est une
étiquette **écrite à la main** qui traduit un *mode*, jamais un âge. Ses entrées
`stale`/`offline` existent dans la table mais rien ne les atteint : « Périmé »
et « Hors ligne » y sont **structurellement inatteignables**. C'est exactement le
motif de la règle 7 de `CLAUDE.md`.

## Le correctif

Le principe : **re-dater doit être possible sans réseau**, puisque c'est
précisément quand le réseau manque que le problème se pose. L'horodatage est
déjà dans le DOM ; il suffit de le rendre lisible et de rejouer le seul calcul
qui ne demande rien.

- `VX.updateIndicator` émet `data-ts` et isole l'âge dans `.vx-update-age` ;
- `VX.freshness.assess` conserve l'instant de référence, `chip` l'inscrit en
  `data-at` ;
- `VX.freshness._retick()` réécrit les âges et ré-évalue les puces, **sans
  aucune requête** (le gardien interdit `fetch` dans son corps) ;
- une tâche de **shell** (persistante, donc survivant aux navigations) l'appelle
  toutes les 30 s ;
- les quatre KPI d'Aujourd'hui reçoivent l'âge réel du scan (`scan_age`, déjà
  servi par `/api/market/summary`) via `VX.freshness` — jamais un libellé écrit
  à la main.

**Aucun chiffre n'est retiré de l'écran.** Il cesse seulement de se présenter
comme frais.

## Résultat

| | avant | après |
| --- | --- | --- |
| lignes de provenance figées (Marchés) | 11 / 11 | **1 / 11** |
| lignes re-datables (8 espaces) | 0 / 22 | **21 / 22** |
| chiffres **datés faux** à 2 h | 7 | **0** |
| chiffres **nus** à 2 h | 4 | **0** |
| chiffres **datés** à 2 h | 4 | **15 / 15** |

La ligne restante affiche `—` : âge inconnu, aveu honnête, jamais une valeur
inventée.

Les deux trajectoires qui prouvent que le mécanisme fonctionne **de lui-même** :

```
portfolio   0 / 3 / 0  (à 12 s)  →  3 / 0 / 0  (à 2 h)
briefing    0 / 4 / 0  (à 12 s)  →  4 / 0 / 0  (à 2 h)
```

À 12 s la puce dit « Analyse » — et elle **dit vrai**. À 2 h, sans réseau et
sans donnée nouvelle, elle est passée seule à « À actualiser ».

## Ce que le gardien tient

`tests/test_vertex_1_0_hors_ligne.py` garde **le produit et l'instrument**. Le
second n'est pas de la coquetterie : c'est l'instrument qui s'était trompé le
premier, et un gardien qui ne tiendrait que le produit laisserait l'indulgence
revenir.

Mutations appliquées sur disque, résultat attendu = échec :

| mutation | issue |
| --- | --- |
| M1 `data-ts` retiré de `updateIndicator` | détectée |
| M2 le re-datage devient une tâche de page | détectée |
| M3 le re-datage refait un `fetch` | détectée |
| M4 période 30 s → 45 s | **passe, à juste titre** — l'instrument lit la période, les deux restent d'accord |
| M5 l'âge des KPI redevient écrit à la main | détectée |
| M6 `assess` ne conserve plus l'instant | détectée |
| M7 l'instrument **recopie** la période au lieu de la lire | détectée |
| M8 le classement range tout dans « daté » | détectée |

M4 est le cas intéressant : ce n'est pas un trou, c'est la propriété recherchée.
M7 vérifie l'autre moitié — que la lecture est réelle.

## Observation pour la fusion, sans action

Deux éléments décrits par `CLAUDE.md` sont **absents de cette branche** :

- `VX.freshness.domainChip` n'existe **nulle part** dans l'arbre ;
- `test_signal_os_fraicheur_lot62.py` et `..._par_badge_lot63.py` ne sont
  présents que sous forme de `.pyc` périmés dans `tests/__pycache__/` — leurs
  sources ne sont pas sur cette ligne.

C'est probablement ce qui explique que `freshBadge` ait survécu ici alors que
les lots 62–64 avaient corrigé quatre badges du même genre ailleurs. **Aucune
action prise** : importer ces gardiens reviendrait à fusionner Signal OS, ce que
le mandat interdit. Le fait est consigné pour la décision humaine de fusion.

## Vérification

- `python -m compileall -q terminal.py vertex` → 0
- `python -m pytest tests/ -q` → **3 447 passed**
- `tests/test_sw_cache_scope_lot361.py` a exigé le bump (v210 → **v211**) et la
  mise à jour de son empreinte dans le même commit — fait.
- Mesure en vrai Chromium, 8 espaces, 1440 px, coupure réseau réelle
  (`set_offline`) : 0 erreur console.
