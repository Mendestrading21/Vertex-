# VERTEX PRODUCT BIBLE

> La référence absolue du produit **VERTEX OBSIDIAN — Institutional Intelligence
> System**. Design System : **OBSIDIAN COPPER**. Écrit comme Head of Product +
> Design Director. Aucun code : la conception du meilleur terminal
> d'investissement possible. Toute décision de refonte se réfère à ce document.
> Fondations amont : `PRODUCT_EXPERIENCE_REVIEW.md`, `.claude/manifesto/VERTEX.md`.

## Nord magnétique

> **Vertex transforme des données complexes en décisions claires, explicables et
> disciplinées.** Il ne cherche pas beaucoup de signaux — il isole quelques
> asymétries exceptionnelles (perdre peu si tort, gagner beaucoup si raison).
> Trois lois d'or : *une page = une mission · une section = une question · un
> graphique = une conclusion exploitable.*

Sept vérités qui gouvernent tout le reste :
1. **Réponse d'abord**, preuve ensuite, expertise à la demande.
2. **Une donnée, un domicile** — jamais la même métrique racontée deux fois.
3. **L'honnêteté est premium** — « je ne sais pas » élégant > chiffre inventé.
4. **La couleur a un sens financier stable** — une hausse n'est pas « verte » par défaut.
5. **Le calme est une fonctionnalité** — pas de casino, pas de néon, pas de flottement.
6. **La densité doit être ordonnée** — dense ≠ encombré (leçon Bloomberg bien appliquée).
7. **READONLY absolu** — Vertex analyse, ne commande jamais.

---

# 1. Storyboard utilisateur complet

Le récit d'une semaine type de l'investisseur (persona unique : un allocateur
asymétrique, discipliné, IBKR réel en lecture seule).

**Lundi 08:30 — Le réveil.** Il ouvre Vertex. **Briefing** lui parle en une
phrase : *« Régime RISK-OFF, prudence. Risque n°1 : CPI mercredi. 2 nouvelles
opportunités S. »* Un diff « depuis vendredi » liste ce qui a changé. Émotion :
**clarté**. Il sait : observer aujourd'hui, préparer mercredi.

**Lundi 08:40 — Le terrain.** Il passe à **Marchés** pour confirmer : un régime,
une jauge de confiance, la participation (breadth), la rotation dominante. Trente
secondes. Émotion : **maîtrise**.

**Mardi 10:00 — La chasse.** **Opportunités** : l'entonnoir a réduit 517 titres à
3 dossiers S+/S. Il ouvre le meilleur → **Analyse**. La Carte-Verdict le frappe :
*Achat sur repli · 34/40 · confiance 72 · entrée 142 · invalidation 128*. Les
trois scénarios (pessimiste/probable/exceptionnel) sont côte à côte. Il lit
l'asymétrie, le catalyseur 90 j. Émotion : **conviction lucide**. En deux clics
il écrit sa thèse et pose une alerte d'invalidation à 128.

**Mardi 10:15 — La convexité.** **Options** : l'environnement paie-t-il la
convexité ? Stratégie, coût, perte max, breakevens, PoP. Il compare un LEAPS
(delta 0.80, échéance 12 mois). Émotion : **précision**.

**Mercredi 14:35 — Le choc.** CPI sort. Une position approche son invalidation.
**Portefeuille** le signale calmement : *thèse à surveiller, −6 %, invalidation à
−8 %*. Pas de bouton « renforcer ». Émotion : **sérénité vigilante**. Il décide de
tenir, la thèse est intacte.

**Vendredi 17:00 — L'apprentissage.** **Performance / Journal** : ses verdicts à
+20 j tiennent-ils ? Une règle apprise ce mois-ci s'ajoute à la mémoire.
Émotion : **honnêteté**.

**En continu — La confiance.** À tout moment, **Système** répond : *données
fiables / dégradées / démo*. **Intelligence** explique *pourquoi* un verdict, sur
quoi le comité s'accorde. Émotions : **fiabilité, confiance**.

---

# 2. Parcours utilisateur (les 4 rituels canoniques)

Chaque parcours a un déclencheur, une intention, un chemin d'espaces, et un état
de sortie (« done »). **Cible : ≤ 2 clics du signal à la thèse.**

**P1 — Rituel du matin (2 min).**
`Briefing` → (si action) `Analyse` → poser alerte.
Sortie : « j'agis / j'observe », décidé.

**P2 — Chasse à l'asymétrie (10 min, hebdo).**
`Opportunités` (entonnoir → short-list) → `Analyse` (dossier) → `Options` (véhicule)
→ écrire la thèse + alerte.
Sortie : thèse écrite ou rejet argumenté.

**P3 — Gestion de position (30 s/position, quotidien).**
`Portefeuille` (état de thèse) → (si signal) `Analyse` (diagnostic) → tenir/alléger.
Sortie : décision de gestion tracée, jamais un renforcement de perte.

**P4 — Apprentissage (hebdo/mensuel).**
`Performance` (track record) → `Intelligence · Mémoire` (règle apprise).
Sortie : une règle ajoutée, un biais corrigé.

**Fils conducteurs (le liant qui manque aujourd'hui) :** chaque écran propose la
**prochaine action analytique** contextuelle (« Ouvrir le dossier », « Poser une
alerte d'invalidation », « Journaliser »). Le ticker actif **voyage** d'un espace
à l'autre (contexte préservé). Une **Command Palette (⌘K)** permet le saut direct.

---

# 3. Wireframes de toutes les pages

Convention : `[H]` hero/réponse (niveau 1) · `[J]` justification (niveau 2) ·
`[E]` expertise dépliable (niveau 3). Grille 12 colonnes, max 1600 px, sidebar
240 px (72 px compacte). Contrainte de densité initiale : **1 message · ≤4 KPI ·
≤3 graphiques · ≤3 alertes · ≤3 actions · 1 tableau**.

### 3.0 App-shell (commun)
```
┌────────────────────────────────────────────────────────────────────┐
│ SIDEBAR (9 espaces, icônes+labels)        TOPBAR: fil · ⌘K · fraîcheur globale · alertes │
│ ● Briefing                     ┌─────────────────────────────────────────────┐        │
│ ● Marchés                      │  CONTENU (vx-content, max 1600, padding s4)   │  DRAWER │
│ ● Opportunités                 │                                               │ (détail/│
│ ● Portefeuille                 │                                               │  inspec-│
│ ● Analyse                      │                                               │  teur)  │
│ ● Options                      │                                               │         │
│ ● Performance                  │                                               │         │
│ ● Intelligence                 │                                               │         │
│ ● Système                      └─────────────────────────────────────────────┘        │
│ ─ fraîcheur · compte · démo    MOBILE: sidebar → bottom-bar, drawer → plein écran      │
└────────────────────────────────────────────────────────────────────┘
```

### 3.1 Briefing `/` — *« Dois-je agir aujourd'hui ? »*
```
[H] BANDEAU RÉGIME (1 phrase) : « RISK-OFF · prudence »   + confiance (jauge unique)
[H] ┌ Risque n°1 ┐ ┌ Action du jour ┐ ┌ Ce qui a changé (diff) ┐   ← 3 tuiles
[J] ┌ 3 catalyseurs datés (timeline) ┐   ┌ Top opportunités (2, R:R) ┐
[J] ┌ Marché US (mini, → Marchés) ┐      ┌ Posture du comité (donut) ┐
[E] ▸ Détails macro · internals (déplié)
```
Coupe : SPY/rotation/calendrier *détaillés* (domiciliés dans Marchés).

### 3.2 Marchés `/markets` — *« Le vent est-il dans le dos ? »*
```
[H] RÉGIME + confiance (jauge unique) · Breadth (participation) · Rotation dominante
[J] ┌ Indices comparés (multi-ligne) ┐   ┌ Rotation sectorielle : 1 vue décisionnelle (RRG) ┐
[J] ┌ Courbe des taux ┐  ┌ Tendance de participation (multi-séances) ┐
[E] ▸ Heatmap secteurs détail · waterfall santé · volatilité (déplié)
```
Sous-vues : overview · macro · sectors · breadth · volatility. **Une** jauge par
métrique. **Deux** vues secteurs maximum (RRG + heatmap détail).

### 3.3 Opportunités `/opportunities` — *« Quoi mérite un dossier ? »*
```
[H] COMPTE : « 3 idées S+/S trouvées » + la meilleure (carte compacte, asymétrie)
[J] ENTONNOIR (univers → notés → dossiers) · Scatter qualité×timing (décisionnel)
[J] ┌ TABLE classée (score, R:R, catalyseur) — 1 tableau principal, tri ┐
[E] ▸ Anomalies · calendrier catalyseurs · comparaison (déplié)
```
Action ligne : « → Ouvrir le dossier » (1 clic vers Analyse).

### 3.4 Analyse `/analysis/<sym>` — *« J'entre, j'attends, ou j'évite ? »*
```
[H] CARTE-VERDICT : Verdict · Score /40 · Niveau (S+/S/A/B) · Confiance · Prix · Entrée · Invalidation
[H] CARTE-SCÉNARIO : Pessimiste | Probable | Exceptionnel  (+ risque max, asymétrie, catalyseur 90j)
[J] GRAPHIQUE PRINCIPAL (chandeliers LWC + MM + plan entrée/stop/TP + événements)
[J] ┌ Facteurs (fonda/technique/momentum/risque) ┐ ┌ Scorecard (radar unique) ┐
[E] ▸ Données brutes · méthodologie · analystes · corrélations (déplié)
DATA_INSUFFICIENT → état honnête « Vertex ne tranche pas », aucune fausse conviction.
```

### 3.5 Portefeuille `/portfolio` — *« Où est mon risque, qu'a changé ? »*
```
[H] Exposition · Concentration (HHI) · P&L latent · CE QUI A CHANGÉ depuis hier
[J] ┌ TABLE positions : état de thèse (intacte/surveiller/invalidée), perte max, palier gain ┐
[J] ┌ Allocation (1 vue : treemap OU donut rôles) ┐  ┌ Exposition sectorielle ┐
[E] ▸ Payoff combiné options · stress · corrélations (déplié)
Règles gagnants (+20/+30/+50/+75/+100) surfacées ; JAMAIS « renforcer la perte ».
```
Sans IBKR : état vide premium honnête, pas de faux chiffres.

### 3.6 Options `/options` — *« L'environnement paie-t-il la convexité ? »*
```
[H] Environnement long-option (jauge) · Biais · Régime de vol
[H] STRATÉGIE : coût · gain/perte max · breakevens · PoP · rendement/risque · échéance · delta · theta
[J] PAYOFF interactif (spot/temps) · Scénarios (spot×temps×IV) · Décroissance temps
[E] ▸ Gamma · vega · vanna · vomma · surface de vol (déplié — expert)
```

### 3.7 Performance `/performance` — *« Mon edge tient-il ? »*
```
[H] Win rate réel · Asymétrie moyenne · Edge tient-il (oui/non) · Discipline
[J] ┌ Courbe d'équité ┐ ┌ Drawdown ┐ ┌ Rendement moyen +20j par verdict ┐
[J] ┌ Distribution des rendements ┐  ┌ P&L par mois (heatmap) ┐
[E] ▸ Journal détaillé · enseignements/règles (déplié)
```

### 3.8 Intelligence `/intelligence` — *« Pourquoi ce verdict ? »*
```
[H] VERDICT expliqué (1 titre) : décision + raison en une phrase
[J] ┌ Comité : accord / désaccord (net, pas de fausse conviction) ┐ ┌ Scorecard (radar) ┐
[J] ┌ Chaîne de raisonnement (audit trail ordonné) ┐
[E] ▸ Walk-forward (Sharpe par fenêtre) · stratégie/constitution · mémoire (déplié)
```
Mission resserrée : le *raisonnement*. DATA_INSUFFICIENT → état calme et explicite.

### 3.9 Système `/système` — *« Puis-je faire confiance aux données ? »*
```
[H] UN VERDICT : « Données fiables / dégradées / démo » (vert/ambre) + fraîcheur globale
[J] ┌ Connexions (IBKR/TV/IA : configuré? impact?) ┐ ┌ Qualité des données (donut) ┐
[J] ┌ Moteurs OK ┐  ┌ Automatisations / jobs ┐
[E] ▸ Diagnostics · réglages avancés · archive · design system (déplié)
```

---

# 4. Hiérarchie exacte des informations

Trois niveaux, non négociables, sur **chaque** page :

- **Niveau 1 — RÉPONSE** : que se passe-t-il · importance · confiance · risque ·
  **prochaine action analytique**. Visible sans scroll. Poids typographique le
  plus fort.
- **Niveau 2 — JUSTIFICATION** : facteurs, graphiques essentiels, scénarios,
  catalyseurs, invalidations. Poids moyen.
- **Niveau 3 — EXPERTISE** : données brutes, méthodologie, diagnostics, métriques
  avancées — dans des **panneaux dépliables** (`<details>`/drawer). Poids faible,
  jamais bloquant.

Hiérarchie visuelle par **poids + couleur**, **pas par la taille** (leçon
Linear/Vercel). Un seul « héros » par page. Ordre de lecture imposé :
verdict → preuve → profondeur.

---

# 5. Transitions entre les pages

- **Espace → espace** : le **ticker actif voyage** (Opportunités → Analyse garde
  le symbole). Fondu court, jamais de rechargement brutal.
- **Ticker → dossier** : composition en cascade *courte* (verdict d'abord, puis
  graphique, puis détails) — la hiérarchie devient temporelle.
- **Niveau 1 → 3** : dépliage fluide d'un panneau « Expertise » in-place.
- **Liste → détail** : ouverture du **Drawer** latéral (slide + fade), le contexte
  liste reste visible dessous.
- **Vide → rempli** : skeleton → contenu (jamais écran blanc ni saut).
- **Frais → périmé** : transition douce du **Freshness Badge** (LIVE → DELAYED →
  STALE) — signale la dégradation *sans* alarmer.
- **Mobile** : sidebar ↔ bottom-bar ; drawer → plein écran.

Durées 140–260 ms, courbe `--vx-ease-out` (`cubic-bezier(.23,1,.32,1)`).

---

# 6. Animations utiles (liste fermée — tout le reste est interdit)

**Autorisées** (chacune communique un changement d'état ou guide l'attention) :
1. **Apparition de valeur** — une donnée qui change *pulse* brièvement.
2. **Ouverture drawer/détail** — slide + fade (< 260 ms).
3. **Transition d'onglet/sous-vue** — glissement latéral discret.
4. **Chargement progressif / skeleton shimmer** — « ça arrive ».
5. **Focus clavier** — halo net (accessibilité).
6. **Press tactile** — `scale(.97)` (le produit répond au doigt).
7. **Apparition d'alerte** — entrée latérale calme.

**Interdites** : flottement permanent, halos pulsants décoratifs, animations
répétitives en boucle, cascades longues, tout mouvement incompatible avec
`prefers-reduced-motion` (qui doit tout désactiver).

---

# 7. Composants premium (bibliothèque canonique — une seule version de chacun)

**Signature produit (nouveaux/prioritaires)**
- **Carte-Verdict** — hero de dossier : verdict + score/40 + niveau + confiance +
  entrée + invalidation. Tonalité par sens financier.
- **Carte-Scénario** — pessimiste | probable | exceptionnel + risque max +
  asymétrie + catalyseur.
- **Freshness Badge** — LIVE · DELAYED · STALE · DEMO · OFFLINE · MISSING. Sur
  *chaque* donnée. Langage visuel de l'honnêteté.
- **Chart-Shell** — cadre commun : titre · question · **conclusion** · période ·
  unité · source · fraîcheur · légende · aide · résumé accessible · états.
- **État Insufficient** — « Vertex ne tranche pas », calme, explicite.
- **Command Palette (⌘K)** — saut ticker/page instantané.
- **Diff « depuis ta dernière visite »** — bloc d'ouverture du Briefing.
- **Tiroir de Thèse** — thèse écrite, éditable, reliée à la position.
- **Barre d'action contextuelle** — les 3 gestes de la page.

**Fondamentaux (existants, à garder canoniques)**
Card (hero/analytical/compact) · KPI · Badge (décision/risque/statut/entité) ·
Alert/Insight · Table · Tabs · Segmented control · Chip · Button (primary/soft/
ghost/icon) · Tooltip · Drawer · Modal · Skeleton.

Règle : **aucune palette ni variante locale par page**. Un composant nouveau
naît dans la bibliothèque, jamais dans une page.

---

# 8. Tous les états possibles (matrice universelle)

Chaque bloc de données déclare explicitement son état — jamais un rectangle vide
ni un zéro ambigu.

| État | Signification | Rendu |
|---|---|---|
| **Loading** | en cours | skeleton (dimensions du contenu final) |
| **Ready · Live** | temps réel | contenu + badge LIVE (point vert) |
| **Ready · Delayed** | différé | contenu + badge DELAYED (ambre) |
| **Stale** | périmé | bannière + badge STALE (gris) — dernière valeur connue |
| **Empty** | aucune donnée | état honnête « indisponible — voici pourquoi » |
| **Missing** | donnée absente | `—` / `n/d`, jamais 0 |
| **Insufficient** | trop peu pour décider | état Insufficient, aucune conviction |
| **Error** | échec de chargement | état erreur + action « réessayer » |
| **Offline** | IBKR/source absente | bannière offline calme + impact expliqué |
| **Demo** | données synthétiques | badge DÉMO explicite partout |

Distinctions obligatoires : **0 ≠ absent ≠ N/A ≠ indisponible ≠ estimation ≠
retardée ≠ périmée**. Une estimation est toujours étiquetée comme telle.

---

# 9. Règles de densité

- Premier écran : **1 message principal · ≤ 4 KPI · ≤ 3 graphiques majeurs ·
  ≤ 3 alertes · ≤ 3 actions · 1 tableau principal.**
- Un seul **héros** par page. Le reste se subordonne visuellement.
- La profondeur existe mais **ne bloque jamais** la compréhension immédiate
  (niveau 3 dépliable).
- Densité **ordonnée** : chemin de lecture clair (verdict → preuve → profondeur).
- Interdits : deux graphiques pour la même question · donut décoratif · radar
  plus d'une fois par vue · jauge pour une métrique non bornée · KPI redondant
  avec un graphique voisin.

---

# 10. Règles de couleurs (OBSIDIAN COPPER — une couleur = un sens)

**Identité / surfaces**
- Surfaces : obsidienne → graphite (`#040504 → #202621`). Texte : ivoire
  `#f2f5f1` (primaire), sable `#b8beb7` (secondaire), gris `#818980` (muté).
- **Vert Signal `#84aa31`** = identité / marque / série de référence / action
  principale / sélection. **⚠️ NE signifie PAS « hausse ».**

**Sémantique financière (stable)**
- **Émeraude `#36c889`** = gain / résultat positif.
- **Corail `#ed655c`** = perte / risque.
- **Ambre `#dda23b`** = attente / avertissement / donnée retardée.
- **Violet désaturé `#9c79d0`** = options / IV / Greeks (usage limité).
- **Acier / gris chaud `#9d978e` / `#747d75`** = benchmark / neutre / indisponible.

**Lois**
- Une hausse n'est pas automatiquement verte ; une baisse pas automatiquement
  rouge — la couleur suit le **sens financier réel** (un taux, le DXY restent
  neutres sans contexte).
- **Zéro bleu, zéro cyan en identité** (garde-fou testé).
- La couleur ne doit **jamais** être la seule porteuse d'information
  (accessibilité) : toujours doublée d'un label/forme.
- **Une source canonique** : `palette.py` (Python) = vérité, thème JS + tokens
  CSS en miroir (test de cohérence sur la série entière).

---

# 11. Règles typographiques

- **UI : Inter** (400→900). **Numérique / mono : JetBrains Mono** (chiffres,
  prix, tickers, tabular-nums). Ce sont les **deux seules** polices officielles.
- Hiérarchie **par poids + couleur**, pas par une inflation de tailles.
- Échelle : page 32 · section 19 · sous-titre 14 · carte/corps 13 · méta 11 ·
  KPI 28 / 20.
- **Tabular numbers** obligatoires sur toute donnée chiffrée alignée (tables, KPI,
  scénarios) — les colonnes de chiffres ne dansent pas.
- Titres de carte : 13 px, 600, **majuscules discrètes**, letter-spacing +0.6.
- Jamais de texte critique dépendant uniquement de la couleur ou d'un tooltip.

---

# 12. Règles de spacing

- Échelle unique (multiples de 4) : **4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 ·
  64** (`--vx-s1 … --vx-s16`). Aucune valeur hors échelle.
- Rythme vertical : gouttière de carte 16 (s4) ; entre sections 24–32.
- Rayons : petit 8 · défaut 12 · large 14 · modal 16. Cohérents par famille.
- Grille 12 colonnes, gouttière 16, largeur max **1600 px**, contenu centré.
- Densité tactile : zones ≥ 40 px (boutons, onglets, chips) sur mobile.
- Le **vide est un matériau** : l'air autour du héros crée la hiérarchie autant
  que le poids typographique.

---

# 13. Règles d'interactions

- Les **3 actions les plus fréquentes** de chaque page sont atteignables sans
  chercher (barre d'action contextuelle, pas menu enfoui).
- **⌘K** ouvre la Command Palette (ticker, page, action).
- Hover discret (jamais agressif) ; **press `scale(.97)`** ; **focus visible** au
  clavier partout.
- Tout est **navigable au clavier** ; ordre de tabulation logique ; `Échap` ferme
  drawer/modal/palette.
- Chaque graphique porte un bouton **« Comprendre ce graphique »** (ce qu'il
  montre / pourquoi / ce qui confirmerait / ce qui invaliderait).
- Poser une **alerte d'invalidation** depuis un niveau du graphique = 1 geste.
- Aucune action destructive sans confirmation ; **aucun chemin d'ordre**, jamais.

---

# 14. Règles de responsive

Points de rupture : **1280** (compact) · **1024** (sidebar compacte) · **768**
(tablette) · **640** (mobile : sidebar → bottom-bar, drawer plein écran).

- **La priorité décisionnelle est préservée** à toutes les tailles : le héros reste
  le héros sur mobile.
- KPI s'empilent ; les en-têtes de carte et lignes inline **se replient**
  (jamais de débordement horizontal du contenu).
- Les **tableaux financiers** : scroll horizontal **intentionnel** et contrôlé
  (dans un conteneur), plutôt qu'une conversion systématique en cartes qui casse
  la comparaison. Convertir en cartes seulement quand la lecture y gagne.
- **Aucun débordement horizontal** du contenu (règle testée à 390/768/1440).
- Pas de graphique miniature illisible ; les heatmaps/scatter denses scrollent ou
  se simplifient sous 380 px.
- Cibles tactiles ≥ 40 px ; pas de tooltip *indispensable* sur mobile.

---

# 15. Règles d'accessibilité

- **Compréhension sans couleur** : toute information colorée est doublée d'un
  label, d'une forme ou d'un signe.
- **Contraste** : texte primaire/secondaire lisible sur obsidienne (viser AA).
- **Clavier** : tout activable, focus visible, ordre logique, `Échap` universel.
- **Graphiques** : `role="img"` + **résumé accessible** textuel (la conclusion
  lisible par lecteur d'écran), pas seulement un canvas muet.
- **`prefers-reduced-motion`** : désactive toutes les animations.
- **Zones tactiles** ≥ 40 px ; pas d'information réservée au survol.
- États vides/erreur **explicites et lisibles** (pas d'icône seule ambiguë).
- Langue : interface FR cohérente ; libellés honnêtes (`—`/`n/d` pour l'absence).

---

# 16. Émotions recherchées par page

| Page | Émotion cible | Anti-émotion bannie |
|---|---|---|
| Briefing | **Clarté** — « je sais quoi faire » | anxiété du flux |
| Marchés | **Maîtrise** — « je situe le terrain » | vertige du bruit |
| Opportunités | **Excitation disciplinée** | fièvre du casino |
| Analyse | **Conviction lucide** — « et où j'ai tort » | fausse certitude |
| Options | **Précision** | complexité intimidante |
| Portefeuille | **Sérénité vigilante** | panique / déni |
| Performance | **Honnêteté** | flatterie de l'ego |
| Intelligence | **Confiance** — raisonnement lisible | boîte noire |
| Système | **Fiabilité** | doute silencieux |

Fil rouge : **calme · précis · premium · honnête.** Vertex rassure par la clarté,
n'excite jamais par le clignotement.

---

# 17. Ce qui différencie Vertex d'un Bloomberg ou d'un TradingView

1. **La décision, pas la donnée.** Bloomberg/TradingView sont des *fournisseurs de
   données* : à l'utilisateur de conclure. Vertex **conclut d'abord** (verdict,
   asymétrie, invalidation) et met la donnée *au service* de la décision.
2. **L'honnêteté comme identité.** Là où les terminaux remplissent tout écran,
   Vertex assume « je ne sais pas » : donnée absente = état premium, jamais un
   chiffre de remplissage. La **fraîcheur et la source** sont des composants de
   première classe.
3. **Une thèse, pas un flux.** TradingView optimise le *trading* (bruit, tick).
   Vertex optimise la *conviction 1–24 mois* : scénarios, catalyseur 90 j,
   invalidation — la discipline d'un allocateur, pas l'adrénaline d'un scalpeur.
4. **Le calme institutionnel.** Ni casino crypto, ni dashboard SaaS multicolore,
   ni néon Bloomberg saturé : obsidienne + cuivre, densité *ordonnée*, motion
   discret. Le luxe est la lisibilité.
5. **La couleur a un sens financier**, pas décoratif — et jamais bleu d'identité.
6. **L'explicabilité intégrée.** Chaque verdict est traçable (comité, audit
   trail, « comprendre ce graphique ») — l'inverse d'une boîte noire.
7. **READONLY par conception.** Vertex n'exécute jamais : c'est un instrument de
   *jugement*, pas de passage d'ordre — ce qui autorise une honnêteté qu'un
   broker-terminal ne peut se permettre.
8. **Personnel, pas générique.** Vertex encode *une* stratégie (asymétrie forte,
   S+/S/A/B, LEAPS delta 0.70–0.90) et apprend des décisions de son unique
   utilisateur — un terminal grand public ne le fait pas.

> **Test ultime de réussite :** l'utilisateur comprend plus vite, décide mieux,
> voit son risque plus clairement, et peut **expliquer chaque verdict** sans
> traverser dix écrans contradictoires. Si un écran ne sert pas ce test, il ne
> mérite pas d'exister.

---

## Statut

Document de référence **absolu** du produit. Toute PR de refonte (navigation,
pages, graphiques) doit s'y conformer et le citer. Il ne contient aucun code et
n'autorise aucune donnée inventée, aucun chemin d'ordre, aucune couche visuelle
supplémentaire : il sert à **hiérarchiser et retrancher** vers le meilleur
terminal d'investissement possible.
