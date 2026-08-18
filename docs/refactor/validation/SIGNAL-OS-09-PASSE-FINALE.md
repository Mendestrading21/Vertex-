# SIGNAL OS · LOT 09 — LA FAMILLE D'ICÔNES, ET LE PONT QUI LUI MANQUAIT

Branche : `agent/vertex-signal-os-v1` · SW v214 → **v216** · Suite **3088 passed**

Ce lot est en deux temps parce qu'il a fallu **deux instruments** pour voir le
même défaut. Le premier ne cherchait que des emojis. Le second — écrit après
que le premier eut été déclaré concluant — en a trouvé **vingt-six de plus**.

---

## 1. Le premier instrument mesurait ce que je cherchais, pas ce qui était là

`VISUAL_SYSTEM.md` : « une seule famille d'icônes outline », « ne jamais mélanger
pictogrammes remplis, outline, multicolores et emojis dans la même surface ».

**Passe 1** — recherche d'**emojis** sur les huit espaces. Trois trouvés,
corrigés : `🔴`/`🟠` (sévérité des alertes, accueil), `✅`/`🔒` (jalons, Journal).

Le rapport aurait pu s'arrêter là. Il aurait été **faux**.

**Passe 2** — même mesure, prédicat élargi : *tout élément dont le texte propre
tient en un ou deux caractères non alphanumériques*. Résultat immédiat :

| glyphe | occurrences visibles | rôle |
| --- | --- | --- |
| `✕` | **8 sur 8 espaces** | bouton Fermer du drawer et de la modale |
| `⋯` | 3 sur l'accueil | boutons « Actions » |
| `✓` | 1 sur Système | **valeur** de la tuile « Lecture seule » |
| `⌘K` | 9 | légende de touche — **conservée**, voir §6 |

`✕` est le seul pictogramme que **les huit espaces partagent**. Il appartient au
shell : un caractère, au milieu d'un produit dont les 24 à 48 autres icônes de
chaque page sont des tracés SVG au même `stroke-width: 1.7`.

---

## 2. La cause n'était pas de la négligence — et c'est ce qui compte

`_ICONS` vit en Python, dans `vertex/ui/shell/__init__.py`. Il ne servait que le
HTML **rendu au serveur** : sidebar, barre mobile, topbar.

Or les pages construisent une grande part de leur DOM **en JavaScript**. Elles
n'avaient **aucun moyen d'atteindre la famille**. Le caractère n'était pas un
oubli : c'était la seule option disponible à l'endroit où le code était écrit.

Corriger les glyphes un à un aurait laissé la cause intacte, et le prochain
bouton écrit en JS aurait porté un caractère de plus.

### Le pont

La table est **publiée au client** — `window.VX.__icons`, bloc `#vx-icons`,
sérialisé comme tout bloc inline (`json_for_script`) — et relue par `VX.icon()`
dans `vx-core.js`.

**Une table, deux consommateurs.** Dupliquer le dictionnaire côté JS aurait
recréé une seconde vérité : exactement ce que la table de micro-copy du lot 05
avait produit, et qu'il a fallu fermer entièrement. Un gardien interdit
désormais à `VX.icon` de déclarer le moindre tracé.

Sept pictogrammes ajoutés au même trait : `close`, `more`, `follow`, `alert`,
`option`, `caret`, `clock`. **Un nom inconnu rend une icône VIDE**, jamais un
caractère de repli — un glyphe de secours aurait réintroduit par la porte de
derrière ce que le pont existe pour supprimer.

---

## 3. Le gardien a trouvé sept défauts de plus que moi

J'ai d'abord écrit le gardien comme *« un élément ne se réduit pas à un
glyphe »*. Testé par mutation : **deux régressions sur neuf passaient au vert**.
Réécrit comme *« aucun pictogramme dans un nœud de texte »*, il a trouvé, dans
le code que je venais de relire :

| site | glyphe | traitement |
| --- | --- | --- |
| Opportunités — classement | `★` sur le meilleur candidat | texte pour lecteurs d'écran (la colonne porte déjà `class="sym best"`) |
| Opportunités — porte plafonnante | `✕` | trait `close` |
| Analyse — préparation bloquée | `⛔` | **retiré** (le texte dit « bloquée ») |
| Analyse — portes non franchies | `✕` | trait `close` |
| Portefeuille — revues obligatoires | `⚠` | **retiré** |
| Portefeuille — favoris | `★` | trait `star` |
| Système — avertissements | `⏳` | **retiré** |

**Aucun n'était rendu lors du relevé navigateur** : tous vivent dans une branche
conditionnelle — une porte plafonnée, un avertissement. Un pictogramme latent
est un pictogramme : il apparaîtra le jour où la condition sera vraie,
c'est-à-dire le jour où l'écran comptera le plus.

Le traitement n'est **pas uniforme, et c'est délibéré** : là où le mot dit déjà
la chose, le glyphe est retiré ; là où il était le seul marqueur, il devient un
trait.

---

## 4. Puis le gardien s'est révélé aveugle sur la moitié du produit

Mesure finale au navigateur, serveur en `td-shell-v216` **vérifié avant de
lire** : un pictogramme subsistait sur l'accueil — `▸`, devant le verdict du
Catalyst Runway. **Le gardien était vert pendant que le navigateur l'affichait.**

Sa portée s'arrêtait à `vertex/ui/pages/**`. Or les builders de graphiques et
les modules de page sous `vertex/static/vertex/js/**` construisent du DOM
exactement comme les pages. Douze pictogrammes de plus, de l'autre côté de la
frontière :

| fichier | glyphe |
| --- | --- |
| `charts/catalyst-runway.js` · `charts/regime-aura.js` | `▸` devant le verdict — **retiré** (le verdict est déjà mis en forme comme tel) |
| `charts/chart-core.js` | `⏱` ×2 (bandeau + case d'icône) et `!` — bandeau nettoyé, cases → traits `clock` / `alert` |
| `vx-entities.js` | `★ Favori` → trait `star` |
| `pages/options-gex.js` | `⚡` marqueur + sa légende → trait `bolt`, légende reformulée |
| `pages/options-structure.js` | `★` marqueur + sa légende → trait `star`, légende reformulée |
| `pages/options-intel.js` | `★ Recommandée` → trait ; `⚠ ' + e.message` → message sans jargon réseau |
| `pages/tracking.js` | `⚠ ' + e.message` → message sans jargon réseau |

**Un gardien dont la portée s'arrête avant le code qui produit le défaut ne
garde rien.** Portée étendue : **45 fichiers, dont 35 JS** (`vendor/` exclu,
bibliothèques tierces).

C'est la **sixième fois** dans cette refonte qu'une assertion de portée
insuffisante me trompe. Le motif ne varie pas, seule sa forme change : cette
fois ce n'était pas « chercher une chaîne au lieu de lire un bloc », c'était
*lire les bons blocs dans le mauvais répertoire*.

---

## 5. Deux composants dupliqués, trouvés au passage

Le glyphe `=` sur l'accueil n'était pas une icône égarée : c'était le **symptôme
d'un état construit à la main**. Deux zones de `/` recopiaient le balisage de
`.vx-state` au lieu d'appeler `VX.states.empty()`, et remplissaient la case
réservée au pictogramme avec un caractère (`—`, `=`) là où tous les états
canoniques portent la silhouette SVG de `VX.states.ghost`.

Un composant dupliqué **pour changer une icône** est précisément ce que le
système existe pour éviter. Les deux passent désormais par la fabrique ; mesuré
après correction : `data-state="empty"`, silhouette SVG présente, aucun glyphe.

Même mécanique pour la tuile **« Lecture seule »** de Système : sa valeur était
`✓`, là où ses trois voisines portent un nombre — et pour l'invariant le plus
important du produit. Un signe ne se lit pas à voix haute, ne se copie pas, et
surtout ne distingue pas « confirmé par le serveur » de « pas encore su ». D'où
**« Active » / « Inconnue »**, et jamais « Non » : « Non » affirmerait que le
terminal peut passer un ordre.

---

## 6. Ce que je NE corrige pas, et pourquoi

- **`⌘K`** (9 occurrences) — ce n'est pas une icône, c'est le **nom d'une
  touche**. Le lot 288 l'avait déjà masqué au tactile pour cette raison même.
- **Les flèches de libellé** (`Marchés →`, `Ouvrir le desk →`) — vocabulaire
  directionnel du produit, écrit *dans* un libellé. Mon premier motif les
  accusait à tort ; le domaine du gardien commence à U+2200 pour les exclure, et
  un contre-exemple tenu par mutation vérifie qu'elles restent permises.
- **Les opérateurs mathématiques** (`−`, `≥`, `≤`, `×`…) — du texte.
- **`vertex/ui/sync_center.py`** porte encore un `✕`. **Mesuré** : il n'atteint
  aucun des huit espaces — il n'est injecté que dans `_NAVJS_BLOCK` du monolithe
  historique, et `curl /` n'en contient aucune trace. Hors portée, dit comme tel.
- **Le préfixe emoji des notes du comité** (`✅ ENTRÉE CONFIRMÉE — …`,
  `vertex/engines/committee.py`) : **le moteur n'est pas touché** — la chaîne est
  son contrat et d'autres consommateurs la lisent. Le préfixe n'est plus
  **peint**, la pastille de verdict juste à gauche disant déjà « ACHAT ». Le
  retrait ne porte **que sur la tête de chaîne** : une note amputée en son milieu
  serait une note falsifiée.

---

## 7. Une accusation que je n'ai pas portée

Ma capture du drawer affichait `[object Object]` en titre et `undefined` en
corps. J'allais le signaler.

**C'était mon banc.** `VX.shell.openDrawer(title, html, options)` prend des
arguments positionnels ; je lui avais passé un objet. Rappelé correctement, le
drawer rend « Aperçu » et son texte. Troisième artefact de banc arrêté avant
publication dans cette refonte.

---

## 8. Mesures — version servie vérifiée avant chaque lecture

`/sw.js` → `td-shell-v216`. Serveur relancé après chaque modification.

| espace | pictogrammes textuels visibles | icônes SVG | `stroke-width` | erreurs page |
| --- | --- | --- | --- | --- |
| `/` | **0** | 29 | `1.7` | 0 |
| `/markets` | **0** | 48 | `1.7` | 0 |
| `/opportunities` | **0** | 35 | `1.7` | 0 |
| `/analysis` | **0** | 24 | `1.7` | 0 |
| `/portfolio` | **0** | 25 | `1.7` | 0 |
| `/options` | **0** | 24 | `1.7` | 0 |
| `/journal` | **0** | 26 | `1.7` | 0 |
| `/system` | **0** | 24 | `1.7` | 0 |

*(hors `⌘K` et opérateurs mathématiques, conservés — §6)*

Bouton Fermer mesuré : `viewBox 0 0 24 24`, `stroke-width 1.7`, cible 36 px,
aucun texte. `Escape` referme (`data-open` → `0`).

`window.VX.__icons` : **25 noms** publiés, `VX.icon` disponible.

Défilement horizontal de **page** — 1440 / 768 / 390 px : **aucun, 8/8 à chaque
largeur**.

---

## 9. Gardien

`tests/test_signal_os_famille_icones_lot09.py` — 5 tests, **45 fichiers**
balayés.

| mutation | résultat |
| --- | --- |
| `✕` revenu dans le shell | 2 échecs |
| `⋯` revenu sur l'accueil | 1 échec |
| `⋯` + étiquette revenu (fiche) | 1 échec |
| `★` revenu dans la copy | 1 échec |
| `★` revenu dans le classement | 1 échec |
| `⏳` revenu (Système) | 1 échec |
| `⚠` revenu (Portefeuille) | 1 échec |
| `▸` revenu (Catalyst Runway) | 1 échec |
| `⏱` revenu (Chart Shell) | 1 échec |
| `★` revenu (favoris, `vx-entities.js`) | 1 échec |
| `⚡` revenu (GEX) | 1 échec |
| seconde table côté client | 1 échec |
| caractère de repli dans `VX.icon` | 1 échec |
| pont client retiré | 1 échec |
| `✓` revenu comme valeur | 1 échec |
| « Non » au lieu de « Inconnue » | 1 échec |
| **contre-exemple** : flèche de libellé (`Marchés →`) | **reste vert** |

16 régressions tuées, 1 contre-exemple tenu.

### Un gardien voisin mis à jour

`test_regime_aura_lot629.py` épinglait `'▸ Risque neuf autorisé · …'` dans sa
chaîne attendue. Le `▸` n'a jamais été son sujet — la propriété qu'il garde est
que l'invalidation ne répète pas le verdict, et elle est intacte. Attente mise à
jour, raison écrite dans le fichier.

---

## 10. Dette — inchangée sauf mention

- **Palette : interface violette, graphiques cuivre.** *Décision de l'utilisateur,
  toujours en attente.* Elle conditionne la cohérence des graphiques sur les huit
  espaces et **ne sera pas prise unilatéralement**.
- **Étiquetage démo** : figé en caractérisation (lot 08), correction subordonnée
  à l'établissement de quelle donnée est réellement synthétique.
- Contenus non audités rang par rang : Marchés (6 vues), Opportunités (rangs),
  Portefeuille (5 vues sur 6), Options (profil de lecture), Journal (6 rangs,
  5 visualisations).
- Fiche `/analysis/<ticker>` inaccessible ici (appel réseau interdit dans cet
  environnement) — ses corrections sont vérifiées **en source**, pas au rendu.
- Aucun instrument ne détecte le **rognage silencieux**.
- 5 modules UI morts (146 Ko, 0 consommateur) non supprimés.
