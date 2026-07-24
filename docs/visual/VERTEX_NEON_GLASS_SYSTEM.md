# VERTEX NEON GLASS — Graph System V2 (issue #14, Phase 1)

> ⚠️ **SUPERSÉDÉ par [`VERTEX_NEUE_EMBER_SYSTEM.md`](VERTEX_NEUE_EMBER_SYSTEM.md).**
> Ce document décrit la 1ʳᵉ passe (littéraux orange locaux `#ff7a1e`, scope CSS).
> L'identité est désormais fixée **à la racine** (`tokens.css`) en **Orange Ember
> `#FF6D29`** avec 3 miroirs graphiques synchronisés. Conservé pour l'historique.

> Langage visuel officiel de la refonte : **fond noir profond légèrement bleuté**,
> **cartes glass premium**, identité **orange néon / cuivre incandescent**. Terminal
> institutionnel + application premium, **jamais casino**. Implémenté d'abord comme
> **prototype scopé à Aujourd'hui** (`vertex/static/vertex/css/neon-glass.css`,
> scope `.vx-content[data-space="briefing"]`) — aucun autre espace touché tant que
> le prototype n'est pas validé. **Aucun moteur/donnée/calcul modifié.**

## 1. Principes

1. Une carte = une question claire (le contrat `C.card` est préservé).
2. Chaque graphique porte titre, question, conclusion, unité, période, source,
   fraîcheur et **états honnêtes** (loading/empty/stale/error/demo/insufficient/offline).
3. Chaque carte est identifiable par sa **hiérarchie, son bord chaud, son espace et sa
   profondeur** (glass).
4. Micro-graphiques **vivants** : ligne fluide, area fill discret, points clés, tooltip
   verre, transitions courtes (120-240 ms).
5. **Glow uniquement** sur sélection / live / point actif / alerte — jamais permanent.
6. Pas de gradient décoratif sans fonction.
7. La couleur suit **le sens financier** (jamais hausse=vert hors contexte).
8. Zéro donnée inventée · READONLY absolu · responsive 390/768/1440/1920 sans débordement.

## 2. Tokens officiels (implémentés dans `neon-glass.css`)

### Fond (noir profond, très légèrement bleuté)
| Token | Valeur | Rôle |
|---|---|---|
| `--ng-bg-0` | `#05070c` | le plus sombre (fond de page) |
| `--ng-bg-1` | `#080b12` | fond intermédiaire |
| `--ng-bg-2` | `#0b0f18` | fond haut |

Fond de page = superposition de deux halos radiaux **fonctionnels** (cuivre en haut-
droite pour le focus, bleu très discret en haut-gauche) sur un dégradé vertical
sombre. Aucun bleu comme couleur **identitaire**.

### Surfaces glass
| Token | Valeur | Rôle |
|---|---|---|
| `--ng-glass` | `rgba(20,26,38,.55)` | surface de carte |
| `--ng-glass-raised` | `rgba(28,35,50,.62)` | carte surélevée |
| `--ng-glass-hover` | `rgba(34,42,60,.72)` | survol |
| `--ng-blur` | `14px` (10px ≤768) | `backdrop-filter` |

### Bordures (fines, chaudes — cuivre)
`--ng-border rgba(255,150,70,.16)` · `--ng-border-strong rgba(255,150,70,.32)` ·
`--ng-border-soft rgba(230,236,255,.07)`.

### Identité — orange néon / cuivre incandescent
| Token | Valeur | Rôle |
|---|---|---|
| `--ng-neon` | `#ff7a1e` | identité, sélection, action principale |
| `--ng-neon-bright` | `#ff934a` | accent vif |
| `--ng-copper` | `#c9631f` | cuivre incandescent (accent secondaire) |
| `--ng-neon-soft` | `rgba(255,122,30,.14)` | fond d'accent |
| `--ng-glow` | `0 0 0 1px …,.35 + 0 0 18px …,.45` | halo (états actifs seulement) |

Réécriture locale : `--vx-brand`, `--vx-brand-strong`, `--vx-copper-light` → orange néon
(dans le scope Aujourd'hui uniquement).

### Sémantiques (inchangées — le sens financier prime)
Vert `--vx-positive #36c889` (gain/confirmation) · Rouge `--vx-negative #ed655c`
(perte/risque) · Ambre `--vx-warning #dda23b` (attente/alerte) · Violet `--vx-violet
#9c79d0` (options/volatilité uniquement).

### Profondeur, rayons, motion
`--ng-shadow` / `--ng-shadow-raised` (ombres douces + filet interne) · `--ng-radius
16px` (14px ≤768) · `--ng-motion 180ms cubic-bezier(.22,.61,.36,1)`.

## 3. Variantes de carte

| Variante | Traitement |
|---|---|
| **standard** | glass + bordure chaude fine + filet cuivre en tête + ombre douce |
| **premium** (`.vx-card--hero`) | halo cuivre fonctionnel + bordure forte + ombre surélevée + titre orange vif |
| **active** | bordure forte + `--ng-glow` (sélection) |
| **warning** | accent ambre (bord + badge) |
| **critical** | accent corail (bord + badge) |
| **live** | `.vx-live-dot[data-live=…]` : point vert + halo pulsé (glow réservé au live) |

## 4. Chart Shell V2

Le contrat `C.card` est **conservé intégralement** (title/question/conclusion/unit/
timeframe/source/timestamp/mode/summary/legend/explain/states/render). V2 = habillage
neon-glass **autour** du même contrat :
- conteneur `canvas` en verre (`border-radius`, fond `rgba(0,0,0,.18)`) ;
- en-tête : titre (orange vif en premium), badges période/unité, **Freshness Badge V2**
  (pastille + libellé, glow seulement si live) ;
- pied : `VX.updateIndicator` + unité + limites + bouton « Comprendre ce graphique » ;
- **états honnêtes V2** : skeleton shimmer glass → contenu (reveal 180 ms) ; empty/stale/
  error/insufficient/offline en glass sobre bordé pointillé (aucun faux canvas).

## 5. Tooltip V2 / Légendes V2 / Axes-grilles V2 / Annotations V2

- **Tooltip verre** : fond `rgba(10,14,20,.82)` + blur, bordure chaude fine, texte
  ivoire, valeur en mono ; apparition 120 ms. *(spec — appliqué à la migration des
  charts Chart.js ; le prototype Aujourd'hui pose le langage CSS.)*
- **Légendes V2** : pastilles rondes + label discret, alignées en pied de carte.
- **Axes/grilles V2** : grille `rgba(255,255,255,.06)`, ticks `--vx-text-muted`, ligne
  zéro renforcée, unités explicites.
- **Annotations V2** : lignes de référence pointillées (spot cuivre, breakeven ambre,
  niveau d'invalidation corail) — déjà présentes sur le payoff canonique.

## 6. États (loading / empty / stale / error / demo / insufficient / offline)

Servis par `VX.states.*` + `C.cardState` (inchangés) et **restylés en glass** :
skeleton shimmer, cadre pointillé chaud, bannière démo glass. Jamais de faux graphe,
jamais un zéro inventé — `n/d` honnête.

## 7. Animations autorisées (120-240 ms, reduced-motion respecté)

reveal de série · skeleton → contenu · point actif · changement de période · pulse
bref live · drawer/modal · hover léger. `@media (prefers-reduced-motion: reduce)` coupe
toutes les animations et transitions du prototype.

## 8. Périmètre du prototype (Phase 2) & suite

- **Fait** : `neon-glass.css` scopé Aujourd'hui — fond bleuté, cartes glass, KPI glass,
  bouton action orange néon, live-dot pulsé, skeleton shimmer, reveal, reduced-motion,
  responsive. Le Hero, les 4 KPI, le Régime (jauge), la Diff, les opportunités, alertes,
  catalyseurs et portefeuille adoptent le glass **sans changer une seule donnée**.
- **Non fait (volontaire, après validation)** : migration page par page (Marchés →
  Système) et convergence des ~41 graphes vers les ~15 primitives (cf. AUDIT §6), avec
  Chart Shell V2 appliqué aux canvas Chart.js. **Pas de big-bang.**

## 9. Invariants

Aucun moteur/donnée/calcul modifié · READONLY absolu, aucun chemin d'ordre · pas de
duplication de graphiques · pas de nouvelle route métier · pas de suppression sans
preuve · pas de bleu identitaire · pas de merge `main`, pas de tag, pas de release.
