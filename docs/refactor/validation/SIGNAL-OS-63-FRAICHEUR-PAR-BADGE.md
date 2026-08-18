# SIGNAL OS · LOT 63 — QUATRE ÉTIQUETTES DE FRAÎCHEUR ÉTAIENT DES CONSTANTES

Branche : `agent/vertex-signal-os-v1` · SW **v243 → v244** (octets servis modifiés,
`/static` compris) · Suite **3 507 passed** (3 498 → +9)

Réserve SIGNAL-OS-62 §6.1, de ma main : *« Options n'a aucun vocabulaire de
fraîcheur. »*

**Ce verdict était faux, et c'est par là que ce lot commence.**

---

## 1. Deux fautes de méthode, dont une bien plus grave

**1.1 — Mon inventaire des grammaires était incomplet.** Il y en a **trois** :

| sélecteur | émis par |
| --- | --- |
| `.vx-fresh-chip[data-state]` | `VX.freshness.chip()` |
| `.vx-freshness[data-live]` | `freshBadge()` / `VXCharts.freshnessBadge()` |
| `.vx-freshness[data-state]` | **écrit à la main** |

La troisième est celle qu'Options utilise. Mon rapport du lot 62 annonçait « DEUX
grammaires, pas une » avec l'assurance d'une mesure — et il énumérait en réalité
ce que je connaissais. C'est la même faute que les sept corrections d'inventaire
des lots 55 à 58.

Conséquence directe : j'ai rendu « **absence de vocabulaire** » là où il y avait
un **mensonge**, et je l'ai fait *le jour même où je corrigeais ce mensonge
ailleurs*.

**1.2 — Ma granularité était la page, pas le badge.** C'est la faute plus grave,
parce qu'elle est silencieuse. L'outil du lot 62 rendait **DIT** dès qu'**une**
étiquette réagissait. Une page portant un badge honnête *et* un badge constant
était donc déclarée **saine** — et trois pages étaient exactement dans ce cas.

> *Un verdict par page masque un défaut par badge.*

---

## 2. L'instrument : apparier les étiquettes par leur chemin DOM

`tools/mesurer_fraicheur_par_badge.py` charge chaque espace **deux fois** —
nominal, puis avec les réponses **vieillies en vol** à 2 h — récolte **chaque**
étiquette visible des trois grammaires, l'identifie par son **chemin DOM**, et
compare son état et son texte.

- l'étiquette change → **RÉAGIT** ;
- l'étiquette ne bouge pas alors que *tout* a vieilli de deux heures →
  **CONSTANTE**.

### Un témoin POSITIF pris dans le produit

Le témoin n'est pas fabriqué : c'est l'étiquette d'Aujourd'hui, dont le lot 62 a
**mesuré** qu'elle réagit. Si l'instrument ne la voit pas bouger, il rend 2.

Un témoin pris dans le produit vaut mieux qu'un témoin fabriqué : il prouve la
chaîne entière — interception, vieillissement, identification, comparaison — dans
les conditions **exactes** de la mesure.

### Et il m'a repris dès le premier passage

Premier lancement : le témoin est déclaré **CONSTANTE**, l'outil rend AVEUGLE.
Il avait raison. En mode démonstration, les pages court-circuitent l'évaluation
(`if(demo){…DÉMO…}`) : le chemin mesuré n'est jamais exercé et **tout** paraît
constant. C'est la leçon §3.1 du lot 62 — que je venais de re-commettre.

L'outil abaisse donc `demo` dans les réponses, **sur les deux visites**. Le
détail compte : ne l'abaisser que sur la visite vieillie ferait paraître
**réactif** ce qui ne fait que sortir du mode démo. Intervention sur la mesure,
jamais sur le produit — déclarée ici et dans l'outil.

---

## 3. Le résultat : cinq constantes, et un motif qui désigne la cause

| espace | étiquette | avant |
| --- | --- | --- |
| **Analyse** | carte-Verdict | `demoState()?'fallback':'delayed'` |
| **Opportunités** | hero | `m==='fallback'?'fallback':'delayed'` |
| **Portefeuille** | synthèse | `__pfLive?'live':'delayed'` |
| **Options** | carte-Verdict | `d.demo?'demo':'delayed'`, texte « DELAYED » |
| **Système** | hero | décrit la CONNEXION |

Le motif est net, et il ne désigne pas les pages :

> **Les cinq puces issues de `VX.freshness.chip()` réagissaient TOUTES.
> Les quatre badges écrits à la main mentaient TOUS.**

Le défaut ne venait pas d'une négligence page par page. Il venait de ce
qu'**écrire l'étiquette soi-même était plus court que d'aller chercher un âge**.

Deux d'entre elles étaient sur une **carte-Verdict** — l'objet où la page conclut.
Et sur Options, ce sont des primes, une IV et un spread, qui vieillissent en
**minutes**.

---

## 4. Le correctif : rendre l'honnêteté plus courte que le mensonge

`VX.freshness.domainChip(nom)` lit `domains.<nom>.age_s` de `/api/live/status`,
que le shell pose déjà sur `window.__vxStatus` de **chaque** page. Chaque domaine
(`prices`, `options`, `news`, `calendar`…) porte son propre âge et son propre
seuil serveur. Âge inconnu → `assess` rend « — », l'aveu honnête, jamais une
valeur inventée.

| page | source d'âge retenue |
| --- | --- |
| Analyse (Verdict) | `domainChip('prices')` — **le même** que la puce du prix au-dessus |
| Options (Verdict) | `domainChip('options')` — seuil serveur propre, 1 800 s |
| Opportunités (hero) | `opFreshHtml()` — **le même** âge de session que `#op-fresh` |
| Portefeuille (synthèse) | le même âge de session que `#pf-fresh` |

Sur Opportunités et Portefeuille, `boot()` **attend** désormais le calcul de
fraîcheur : sans quoi le hero peindrait « — » là où l'âge est connaissable une
fraction de seconde plus tard.

Sur Options, « DELAYED » — de l'anglais dans une interface française — cède la
place au vocabulaire du reste de l'application.

### La cinquième : un mot honnête dans le mauvais vêtement

Sur Système, l'étiquette dit « **Système opérationnel** » : elle décrit la
connexion, pas l'âge. Son **texte** était juste ; c'est sa **classe** qui mentait
— et c'est très exactement cette classe qui l'a fait prendre pour une étiquette
de fraîcheur au lot 62, puis pour une constante au lot 63. Elle passe à
`vx-badge-status`, la pilule d'état **déjà utilisée six fois sur cette même
page**.

### Mesure après correction

```text
RESUME — etiquettes de fraicheur CONSTANTES
  aucune. Toutes les etiquettes affichees reagissent a l'age.
EXIT=0
```

Huit espaces. Zéro erreur console (les six `ERR_FAILED` observés sont mes propres
coupures des routes sortantes interdites — vérifié, pas supposé) ;
`/api/client-log` à `{"count":0}`.

---

## 5. Le gardien et ses huit mutations

`tests/test_signal_os_fraicheur_par_badge_lot63.py` (9 tests).

| mutation | résultat |
| --- | --- |
| M1 — Analyse redevient constante | **tombe** ✅ |
| M2 — Options redevient constante | **tombe** ✅ |
| M3 — Portefeuille sans âge | **tombe** ✅ |
| M4 — Opportunités écrit son badge à la main | **tombe** ✅ |
| M5 — démo neutralisée sur la seule visite vieillie | **tombe** ✅ |
| M6 — troisième grammaire oubliée dans l'outil | **tombe** ✅ |
| M7 — témoin positif non exigé | **tombe** ✅ |
| M8 — Système reprend le vêtement de la fraîcheur | **tombe** ✅ |

Aucun gardien creux cette fois — mais il a fallu écrire les assertions **en
sachant** que le piège existe : mes propres commentaires citent les anciennes
formes (`demoState()?'fallback':'delayed'`, « DELAYED »), donc affirmer leur
*absence* aurait échoué sur un fichier parfaitement correct. Les assertions
visent la **présence de la forme juste**. Et `opFreshHtml()` est une sous-chaîne
de sa propre définition `function opFreshHtml(){` — troisième fois que ce piège
précis se présente (lots 57, 62, ici) : l'assertion vise le **site d'appel**,
`+opFreshHtml()+`.

---

## 6. Réserves

1. **Journal n'affiche aucune étiquette de fraîcheur.** Mesuré, pas supposé.
   C'est défendable — le journal montre des décisions passées, pas des cotes —
   mais ce n'est pas un choix que j'ai trouvé écrit quelque part.
2. **Système n'en affiche plus non plus**, par construction de ce lot : la pilule
   d'état a quitté la grammaire de la fraîcheur, et la page n'a pas d'étiquette
   d'âge en hero. La fraîcheur par domaine reste accessible d'un clic
   (« Fraîcheur par domaine → »), mais elle n'est plus résumée au premier écran.
3. **La pilule d'état de Système répète le titre `<h2>` qui la suit
   immédiatement.** Vu en passant, hors sujet de ce lot, non corrigé.
4. **`VXCharts.freshnessBadge()` n'est appelé avec une valeur par personne** :
   `opts.freshness` n'est passé par aucun appelant de `VXCharts.card`. Le « badge
   de fraîcheur canonique » du Chart Shell est donc du **code mort**. À trancher :
   le câbler ou le retirer.
5. **Mode démonstration.** La branche non-démo est forcée *par l'instrument* ;
   la validation en conditions réelles (IBKR, marché ouvert) reste à faire.
6. **Un seul titre (`ACN`), une seule largeur (1440).**
