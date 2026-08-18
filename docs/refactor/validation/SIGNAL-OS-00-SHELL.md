# SIGNAL OS · LOT 00 — SHELL

Branche : `agent/vertex-signal-os-v1` · Service worker : v206 → **v207**
Suite : **3024 passed / 0 failed**

Premier lot de la reconstruction visuelle. Il porte deux choses : remettre la
base d'aplomb, et faire du shell le socle unique de Signal OS.

---

## 0. La base — ce qu'il fallait mesurer avant d'écrire une ligne

La branche `agent/vertex-signal-os-v1` était greffée sur `2b4fa70`, **avant les
lots 602 → 629**.

| mesure | valeur |
| --- | --- |
| commits de `main` absents | **21** (lots 602 → 629) |
| suite telle que poussée | **5 failed / 2866 passed** |
| `--vx-text-muted` | `#8A8284` — valeur d'**avant** le lot 614 |
| `--vx-text-faint` | `#655d5f` — **3,23:1** sur la surface la plus favorable du produit, soit un palier de texte qui ne peut atteindre le seuil WCAG AA **nulle part** |
| garde `'UNKNOWN'` de `regime-aura.js` | **absent** |
| `((r&&r.confidence)\|\|0)*100` dans `briefing.py` | **présent** |
| fixes de défaillance silencieuse (602-608) | **absents** |

Reconstruire par-dessus cette base aurait donc **commencé par annuler 28 lots**
de corrections d'honnêteté et d'accessibilité — et aucun test ne l'aurait
signalé, puisque les tests seraient partis avec.

**Résolution.** `main` fusionnée dans la branche, `main` l'emportant sur les 56
fichiers en conflit. Les pages et les feuilles seront de toute façon
**reconstruites une par une** selon le skill : résoudre 56 conflits ligne à
ligne dans du code voué à la réécriture aurait été du risque pur, pour un
bénéfice nul.

**Conservé intégralement de la branche** : le skill
`rebuilding-vertex-visual-system` (9 fichiers), `docs/design/VERTEX_SIGNAL_OS.md`,
`signal-os.css`, `signal-os.js`, `tests/test_signal_os_contract.py`.

---

## 1. Audit du shell

| Élément | Rôle | Décision | Motif |
| --- | --- | --- | --- |
| Sidebar, 8 espaces, Système en pied | navigation | **KEEP** | conforme : une famille d'icônes outline, actif par `aria-current`, aucun glow |
| Chargement de Signal OS | identité | **REWRITE** | injecté en JS à l'exécution |
| Pastille d'état sidebar | état | **REWRITE** | 4 déclarations en ligne, rien de dynamique |
| Placeholder de recherche | micro-copy | **MOVE** | réécrit dans le DOM après coup |
| Bouton « Ajouter » | action | **REWRITE** | libellé réécrit en JS ; « Analyser » dit ce que ça fait |
| Topbar : 3 icônes utilitaires + primaire + session | contrôles | **KEEP** | exactement la limite fixée par `VISUAL_SYSTEM.md` |
| Fil d'Ariane cliquable | orientation | **KEEP** | — |
| Barre mobile 5 espaces + « Plus » | navigation | **KEEP** | vérifiée sans débordement à 390 px |

---

## 2. Le défaut principal : la couche arrivait après le rendu

`live-updates.js` finissait par `loadSignalOS()` — un `<link>` et un `<script>`
**créés en JavaScript** puis injectés dans le `<head>`.

1. **Le document se peignait une fois sans la feuille.** Le navigateur a le HTML
   et les 17 feuilles historiques bien avant que `live-updates.js` (`defer`) ne
   s'exécute : l'ancien thème est peint, puis remplacé.
2. **Le service worker ne la voyait pas.** Il met en cache le HTML de shell ; ce
   HTML ne mentionnait pas `signal-os.css`. Le repli hors-ligne servait donc un
   shell dont la couche visuelle n'était pas dans la même copie.
3. **L'ordre de cascade dépendait du temps.** Un `<link>` ajouté par script se
   place là où le script tourne : la position de Signal OS dans la cascade était
   une conséquence de l'ordonnancement, pas une décision.

Corrigé : `<link>` déclaré dans le shell, **en dernier**, après `neon-glass.css`.

---

## 3. Trois gardiens du produit mordaient sur la couche livrée — et les trois disaient vrai

### (a) Lot 618 — survol sur carte inerte

`signal-os.css` posait `.vx-card:hover` et `.vx-kpi:hover` **sans condition**.
Les six règles de survol du produit sont, elles, **toutes** gardées par
`:is(a,button,[role="button"],[data-clickable])`.

La règle avait été écrite pour **neutraliser** un soulèvement hérité
(`transform:none`) — sauf que ce soulèvement **n'existe plus**. Il n'en restait
que l'effet de bord : un fond et une bordure qui bougent au survol d'une carte
**inerte**, c'est-à-dire la promesse d'un clic qui n'arrivera pas.

### (b) Lot 611 — deux bandes de largeur jamais mesurées

Bascules `1180 px` et `960 px`. Recensement mesuré :
`(520, 640, 720, 768, 820, 900, 1024, 1280)`. Deux bascules **neuves** créent
deux bandes que le banc des neuf bandes n'a jamais exercées, et rendent périmée
en silence la conclusion « les neuf bandes sont saines ».

Retargetées sur **1280** et **1024** — déjà mesurées, et qui sont par ailleurs
les bascules décrites par `VISUAL_SYSTEM.md`. Les blocs sont inchangés : seule
la largeur à laquelle ils s'appliquent bouge.

### (c) Son propre contrat — la couleur du risque était absente

`test_signal_os_contract.py` réclamait `var(--vx-negative)` ; la feuille ne
l'employait **nulle part**, alors que son propre en-tête annonce « rouge = perte
ou risque réel ». En pratique : **démo** et **périmé** étaient habillés, **erreur**
et **hors ligne** gardaient le rayon et la bordure hérités.

Quatre bandeaux, **une seule famille** — et c'est précisément la famille qui
existe pour dire que la donnée n'est pas ce qu'elle paraît. Deux à 11 px et deux
à l'ancien rayon, c'est l'utilisateur qui doute du message.

---

## 4. Micro-copy : écrite à la source, pas réécrite dans le DOM

`signal-os.js` remplaçait des libellés **après** le rendu. Une réécriture laisse
**deux vérités** : celle que le serveur envoie et celle que l'utilisateur lit.
Tout gardien qui lit les octets servis garde alors l'ancienne, et la nouvelle
n'est gardée par rien.

Le placeholder de recherche, son `aria-label` et le bouton principal sont
désormais dans `vertex/ui/shell/__init__.py`.

**Le reste de la table de réécriture est CONSERVÉ pour l'instant** : elle porte
les titres des pages, qui seront réécrits à la source page par page. Chaque
entrée disparaîtra avec le lot de sa page. C'est une dette **datée**, pas un
choix d'architecture.

---

## 5. Mesures navigateur — 8 espaces × 4 largeurs

Serveur dont le code servi est **vérifié** (`/sw.js` → `td-shell-v207`).

| | 1440 | 1024 | 768 | 390 |
| --- | --- | --- | --- | --- |
| Signal OS chargé | 8/8 | 8/8 | 8/8 | 8/8 |
| déclaré après `neon-glass` | 8/8 | 8/8 | 8/8 | 8/8 |
| défilement horizontal de page | 0 | 0 | 0 | 0 |
| erreurs console | 0 | 0 | 0 | 0 |
| sidebar | 224 px | rail 72 px | rail 72 px | hors-champ (−212) |

**32 chargements de page, 0 erreur console.**

### Un faux positif de mon propre banc, corrigé avant publication

Le premier instrument comptait « déborde du viewport » et rendait **197 défauts**
à 390 px sur `/opportunities`. Faux : une table large dans une boîte
`overflow-x:auto` **doit** dépasser — c'est le défilement voulu, et la **page**,
elle, ne défile pas. Second instrument : un dépassement ne compte que si
l'élément n'a **aucun ancêtre défilant**.

| | 768 | 390 |
| --- | --- | --- |
| débordements **réels** | **0** | **2** |
| dépassements dans un conteneur défilant (voulus) | 66 | 236 |

### Le seul défaut réel trouvé

`/markets` à 390 px : `vx-mk-idx-rel` ×2, `332..430` et `329..427` pour un
viewport de 390 — **~40 px coupés**, hors de tout conteneur défilant.
**Antérieur à ce lot** (les bascules de Signal OS ne concernent pas 390 px).
Il appartient au lot **Marchés** et y est reporté avec sa mesure, plutôt que
d'ouvrir une deuxième page avant d'avoir fini celle-ci.

---

## 6. Gardiens

`tests/test_shell_signal_os.py` — **19 tests**, mesurés sur les **octets servis**
et non sur la source (leçon du lot 381 : `vx_kit.py` portait bien `DESK_KEYS` et
n'atteignait aucune des huit pages).

| mutation | résultat |
| --- | --- |
| `<link>` Signal OS retiré du shell | 16 échecs |
| Signal OS placé **avant** `neon-glass` | 8 échecs |
| placeholder de nouveau réécrit en JS | 1 échec |
| injection à l'exécution revenue | 1 échec |

`tests/test_signal_os_contract.py::test_signal_os_assets_are_loaded_globally_after_the_historical_theme`
réécrit : même propriété, mesurée là où elle est désormais vraie.

---

## 7. Dette explicite

- **Table de micro-copy de `signal-os.js`** : ~45 libellés encore réécrits dans
  le DOM. Disparaît page par page.
- **`MutationObserver` sur `#vx-content` (`subtree:true`)** : relance la passe de
  réécriture à chaque changement du DOM, donc à chaque mise à jour live. Son coût
  n'a **pas été mesuré**. Il tombe avec la table.
- **`!important` sur les quatre grades** dans `signal-os.css` — dette legacy, non
  justifiée par un style en ligne. À reprendre quand les badges de grade seront
  refaits.
- **`/markets` à 390 px** : 2 éléments coupés d'environ 40 px (mesure ci-dessus).
- **La palette violette n'est pas encore dans `palette.py`** : `signal-os.css`
  redirige `--vx-brand` vers `--vx-option`, un token qui existe déjà. Les
  graphiques restent donc sur la série cuivre. À trancher explicitement, avec
  gardiens, plutôt qu'à moitié.

---

## 8. Suite

Lot **01 — Aujourd'hui**. Un défaut est déjà repéré et sera traité là :
la tuile KPI « Régime » affiche **`UNKNOWN (0%)`** — même fabrication de zéro que
celle corrigée au lot 629 dans l'objet Regime Aura, mais dans le résumé, à un
autre site d'appel.
