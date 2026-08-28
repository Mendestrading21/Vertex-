# DESIGN_CONVERGENCE_REPORT — lot 0

Mesuré sur la branche `agent/vertex-2-0-integration-20260828` @ `cb33d90`.
Aucun écart n'est corrigé ici : le lot 0 mesure, il ne modifie pas.

## 1. Cible unique désignée

**`Vertex Black Glass — Signal Light`** est la seule direction visuelle
active. Sa palette canonique est celle de
`.claude/skills/vertex-2-0/references/design-system-final.md`, et elle est
**identique** à celle transmise dans la consigne — vérifié jeton par jeton.
Il n'y a donc pas deux cibles à départager.

## 2. Palette : où chaque jeton canonique est défini, et avec quelle valeur

| Jeton | Valeur cible | Définitions dans le CSS servi | Valeur qui gagne | État |
|---|---|---:|---|---|
| `--vx-night` | `#050607` | 1 (vertex-2-0.css) | `#050607` | conforme |
| `--vx-shell` | `#090b0e` | 1 (vertex-2-0.css) | `#090b0e` | conforme |
| `--vx-graphite` | `#0e1116` | 1 (vertex-2-0.css) | `#0e1116` | conforme |
| `--vx-glass-subtle` | `rgba(255,255,255,.025)` | 2 (glass.css, vertex-2-0.css) | `rgba(255,255,255,.025)` | conforme |
| `--vx-glass-card` | `rgba(255,255,255,.045)` | 2 (glass.css, vertex-2-0.css) | `rgba(255,255,255,.045)` | conforme |
| `--vx-glass-raised` | `rgba(255,255,255,.070)` | 1 (vertex-2-0.css) | `rgba(255,255,255,.070)` | conforme |
| `--vx-ink` | `#f5f7fa` | 1 (vertex-2-0.css) | `#f5f7fa` | conforme |
| `--vx-silver` | `#c9ced8` | 2 (glass.css, vertex-2-0.css) | `#c9ced8` | conforme |
| `--vx-mist` | `#b8bec8` | 1 (vertex-2-0.css) | `#b8bec8` | conforme |
| `--vx-smoke` | `#7a828f` | 1 (vertex-2-0.css) | `#9aa1ad` | **ÉCART** |
| `--vx-positive` | `#36c889` | 2 (tokens.css, vertex-2-0.css) | `#36c889` | conforme |
| `--vx-negative` | `#ed655c` | 2 (tokens.css, vertex-2-0.css) | `#ed655c` | conforme |
| `--vx-caution` | `#dda23b` | 1 (vertex-2-0.css) | `#dda23b` | conforme |
| `--vx-options` | `#9c79d0` | 1 (vertex-2-0.css) | `#9c79d0` | conforme |
| `--vx-analysis-light` | `#65d8e8` | 1 (vertex-2-0.css) | `#65d8e8` | conforme |

**1 écart(s) sur 15 jetons.**

### Le seul écart, et pourquoi il n'est pas tranché ici

`--vx-smoke` rend `#9aa1ad` au lieu de `#7a828f`. Ce n'est pas une dérive :
c'est un relèvement délibéré fait pour le contraste, dans la refonte
graphique. Le skill classe pourtant l'accessibilité **au-dessus** du design en
cas de conflit — alors il faut savoir s'il y a conflit. Mesure WCAG :

| Fond | Cible `#7a828f` | Servi `#9aa1ad` |
|---|---:|---:|
| `--vx-night` `#050607` | 5,23:1 | 7,80:1 |
| `--vx-shell` `#090b0e` | 5,08:1 | 7,58:1 |
| `--vx-graphite` `#0e1116` | 4,88:1 | 7,27:1 |

Seuil AA texte normal : 4,50:1.

**La valeur canonique passe AA sur les trois fonds.** Il n'y a donc aucun
conflit à arbitrer : le relèvement n'était pas nécessaire pour ces fonds, et la
convergence doit ramener `--vx-smoke` à `#7a828f`.

**Réserve à lever avant de le faire :** ces trois fonds sont les fonds de base.
`--vx-smoke` s'affiche aussi sur les surfaces de verre, plus claires. La
convergence devra mesurer le contraste **rendu**, ancêtres résolus
(`tools/vertex_2_0_a11y.py` le fait déjà), et non le seul calcul sur le fond de
base. → **lot design, ticket VX2-DESIGN-01.**

## 3. Feuilles CSS : qui possède quoi

19 feuilles sont servies, dans cet ordre — la dernière gagne :

```
fonts · tokens · base · layout · components · buttons · states · animations
forms · tables · charts · utilities · responsive · polish · control-surface
cockpit · premium · glass · vertex-2-0
```

| Feuille | Poids | Rôle mesuré | Propriétaire canonique proposé |
|---|---:|---|---|
| `tokens.css` | 7,4 ko | 163 jetons `--vx-*` | **propriétaire des jetons** |
| `glass.css` | 38,9 ko | 74 jetons + surfaces en `!important` | à réduire → `vertex-2-0` |
| `vertex-2-0.css` | 61,8 ko | 121 jetons + couche de vérité finale | **propriétaire du rendu** |
| `premium.css` | 17,0 ko | tuiles, cartes, métriques historiques | à absorber |
| `cockpit.css` | 5,2 ko | 5 jetons, **halos permanents** | à absorber, halos refusés |
| `control-surface.css` | 3,8 ko | 19 jetons | à absorber |
| `responsive.css` | 9,7 ko | points de rupture | conserver |
| les 12 autres | 47,9 ko | base, formes, tables, états | conserver |
| **total servi** | **196,7 ko** | | |
| `neon-glass.css` | 56,5 ko | **NON SERVIE** — aucune page ne la demande | **archiver** |

**Quatre feuilles définissent des jetons `--vx-*` en plus de `tokens.css`** —
`glass`, `vertex-2-0`, `control-surface`, `cockpit`. C'est la cause directe du
seul écart de palette : la dernière définition gagne, et personne ne sait
laquelle sans mesurer. → **ticket VX2-DESIGN-02 : un seul propriétaire de
jetons.**

**45 couleurs hexadécimales en dur** subsistent hors définition de jeton dans
le CSS servi, dont **32 dans `glass.css`**. → **ticket VX2-DESIGN-03.**

### `neon-glass.css` — 56,5 ko jamais servis, et déjà nuisibles

Aucune page ne la demande, vérifié au navigateur. Elle a pourtant causé
**trois dégâts visibles**, parce qu'elle portait les **seules** règles de
classes réellement rendues : la pastille de régime de Marchés, la disposition
entière de la barre de contexte des Options sur neuf vues, et le repli de la
fiche Analyse. Un relevé au navigateur a établi la liste complète : **sept**
classes stylées uniquement par elle et présentes dans le DOM des 65 routes.
Cinq ont été rapatriées, une partiellement (son halo et sa pulsation sont
refusés), une écartée.

Elle est **étiquetée, pas supprimée** : cinq bancs la lisent comme registre de
règles. → **ticket VX2-CLEANUP-01, décision humaine requise.**

## 4. Design Systems concurrents

| Surface | État mesuré | Décision proposée |
|---|---|---|
| `/design-system` | page servie, 200 | **conserver** — surface interne de développement, comme l'exige la consigne |
| `.interface-design/system.md` | document | preuve historique |
| `docs/vertex-audit/05-component-inventory.md` | inventaire de dette | preuve historique |
| `VERTEX_DESIGN_TOKENS.md`, `VERTEX_CHART_LIBRARY.md` | décrivent une palette orange/bleu **abandonnée** | **archiver** — `CLAUDE.md` avertit déjà de ne pas s'y fier |

## 5. Bibliothèques graphiques réellement servies

| Bibliothèque | Poids | Chargée par | Rôle |
|---|---:|---|---|
| Chart.js (`chart.umd.min.js`) | — | **la coque**, toutes les pages | tout le reste |
| Lightweight Charts | 159,8 ko | `analysis_page.py` **seule** | chandeliers |
| 29 modules maison (`js/charts/*.js`) | — | par page | cartes, contrats, états |

**ECharts, Plotly et Perspective sont absents du dépôt.** La cible du skill les
nomme comme propriétaires possibles ; les introduire exige un lot dédié avec
besoin reproduit, licence, poids, maintenance, accessibilité, fallback et plan
de retrait — et **jamais** dans le même lot qu'une refonte de page.

`chart-theme-obsidian-copper.js` porte un **nom historique** : son contenu est
déjà aligné sur Black Glass — Signal Light, et le fichier le dit lui-même. La
coque et plusieurs bancs l'épinglent par ce nom. → **ticket VX2-CLEANUP-02,
renommage dans un lot de nettoyage.**

## 6. Ce que la consigne demande et que la mesure confirme déjà

| Règle | État mesuré |
|---|---|
| aucun bleu identitaire | `--vx-info` / `--vx-blue` remappés argent/acier |
| cyan analytique rare | `--vx-analysis-light` défini, usage limité au crosshair |
| violet options seulement | `--vx-options` défini, employé sur Options |
| Geist / Geist Mono | servis par `fonts.css` |
| aucune bordure néon permanente | `neon-glass.css` non servie |
| **aucun halo derrière un texte** | **ÉCART** — `cockpit.css` **est servie** et posait `text-shadow: 0 0 15px` sur tout chiffre positif ou négatif. Les jetons `--vx-glow-*` ont été neutralisés dans la refonte ; **non vérifiable sur ce poste** faute de chiffre coloré en mode démo → **ticket VX2-DESIGN-04** |

## 7. Tickets ouverts par ce rapport

| Ticket | Objet | Lot cible |
|---|---|---|
| VX2-DESIGN-01 | `--vx-smoke` → `#7a828f`, après mesure du contraste **rendu** sur verre | design |
| VX2-DESIGN-02 | un seul propriétaire de jetons ; 4 feuilles en définissent | design |
| VX2-DESIGN-03 | 45 hex en dur hors jeton, dont 32 dans `glass.css` | design |
| VX2-DESIGN-04 | vérifier l'absence de halo sur un poste avec données de marché | qa |
| VX2-CLEANUP-01 | `neon-glass.css` — 56,5 ko non servis, 5 bancs la lisent | cleanup, décision humaine |
| VX2-CLEANUP-02 | renommer `chart-theme-obsidian-copper.js` | cleanup |
| VX2-CLEANUP-03 | **128 Mo de captures PNG** déjà suivies dans `docs/` (393 fichiers), + 15 Mo ajoutés par ce lot. Le dépôt porte ses preuves visuelles en binaire ; décider d'un seuil, d'une rétention ou d'un stockage externe | cleanup, décision humaine |

Aucun n'est traité dans le lot 0.
