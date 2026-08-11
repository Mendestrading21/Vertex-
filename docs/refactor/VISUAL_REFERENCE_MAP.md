# VERTEX — Carte des références visuelles (Phase 2)

> Branche `agent/vertex-total-rebuild` @ `362c7d4`. Lecture seule.

## Constat central (à lire en premier)

**Il n'existe AUCUNE image de référence externe (moodboard / inspiration /
capture d'un produit tiers) versionnée dans le dépôt.**

- Aucun `.svg`, `.jpg`, `.jpeg`, `.webp`, `.pdf`, `.gif`, `.avif` suivi par git.
- Les **121 `.png` sous `docs/redesign/`** sont des **captures auto-générées de
  Vertex lui-même** (états « avant/après » de ses propres itérations, en démo
  étiquetée), **pas** des références d'inspiration. Baseline « d'où l'on part ».
- Seul autre raster : `static/icon-180.png` (885 o, icône PWA).
- `docs/screenshots/` est **gitignoré** (`docs/VERTEX_REPO_AUDIT.md:60`).

**La direction visuelle canonique est donc portée par des SPÉCIFICATIONS
TEXTUELLES, pas par des images.** Les « références » sont des **noms de produits
cités en prose** (Apple, Linear, Vercel, Raycast, Arc, TradingView, Bloomberg,
Stripe, Tesla UI, Notion, Obsidian), explicitement **à ne jamais copier
littéralement** — seulement en étudier hiérarchie / densité / interactions.

> ✅ **Identité tranchée** (voir `CONTRADICTIONS_REGISTER.md` C-04) : la mention
> « Obsidian Prism / General Sans » venait du `CLAUDE.md` de la branche
> d'intégration ; elle **n'existe pas** sur `agent/vertex-total-rebuild`.
> L'identité canonique est **VERTEX OBSIDIAN COPPER**, polices **Inter** (UI) +
> **IBM Plex Mono** (chiffres, `tokens.css:120-121`). Décision utilisateur :
> conserver Obsidian Copper / Inter. (Écart mineur restant : les specs citent
> « JetBrains Mono », le code utilise « IBM Plex Mono » — à réconcilier PR n°2.)

## Documents canoniques de direction visuelle (autorité décroissante)

1. **`.interface-design/system.md`** — source de craft la plus complète.
   « VERTEX OBSIDIAN COPPER INSTITUTIONAL » : palette obsidienne/graphite + cuivre
   (~60/30/10), 4 niveaux de texte, profondeur par bordures+surfaces (ombres en
   appoint), typo Inter/JetBrains, hiérarchie **par poids + couleur** (pas par
   taille), motion *felt-not-watched* (`cubic-bezier(.23,1,.32,1)`, press
   `scale(.97)`, <300 ms), mesures composants exactes. Refs : Linear/Vercel/
   Stripe + terminal Bloomberg. Rejette : SaaS multicolore, néon, glow permanent,
   donuts décoratifs.
2. **`docs/VERTEX_DESIGN_TOKENS.md`** — tokens V3 adossés à `tokens.css` (gardien
   `test_v3_tokens_are_canonical`). Règle « une couleur = un sens ». Hex exacts,
   échelle typo, grille 12 col / max 1600px / sidebar 240-72px.
3. **`docs/VERTEX_OBSIDIAN_COPPER_DEEP.md` (§30)** — palette **finale** :
   obsidiennes `#050505→#0f1011`, orange brûlé CTA, cuivre liens, **zéro bleu
   identitaire** (tests `test_no_blue_primary_*`), sémantique série cuivrée /
   benchmark gris / options violet → `chart-theme-obsidian-copper.js`.
4. **`.claude/manifesto/VERTEX.md`** — identité « VERTEX OBSIDIAN — Institutional
   Intelligence System » + liste des références nommées.
5. **`.claude/agents/ui-designer.md`** — hiérarchie 3 niveaux, densité plafonnée
   (≤4 KPI, ≤3 graphiques, ≤3 alertes), composants canoniques, matrice responsive.
   **C'est ce fichier qui commande la création du présent livrable.**
6. **`docs/VERTEX_INSTITUTIONAL_VISUAL_BASELINE.md`** — infra `VXCharts`, 5 types
   réutilisables, garde-fous READONLY / pas de bleu-cyan dominant.

Assets de code faisant foi : `vertex/static/vertex/css/tokens.css` (couleurs),
`js/charts/chart-theme-obsidian-copper.js` (thème graphes), `vertex/ui/design_system.py`,
`vertex/ui/pages/design_system_page.py`/`design_system_demo.py`,
`vertex/visualization/palette.py`.

## Table des captures baseline (auto-générées, PAS de l'inspiration)

| Jeu | Nb | Poids | Ce qu'il représente | À en tirer | À NE PAS reproduire |
|---|---|---|---|---|---|
| `docs/redesign/before/*` | 20 | ~4,2 Mo | État AVANT refonte (2 navs concurrentes, densité anarchique) | l'anti-modèle à corriger | tout |
| `docs/redesign/after/*` | 29 | ~2,7 Mo | Après Master Redesign (8 espaces) | structure des espaces | thème orange/ambre V3 dépassé |
| `docs/redesign/v3-before/*` | 16 | ~3,9 Mo | Thème « Master bleu » | — | **bleu froid identitaire = à bannir** |
| `docs/redesign/v3-after/*` | 40 | ~6,5 Mo | « Dark Financial Luxury » orange/ambre V3 | responsive 8 pages ×5 tailles | palette orange/ambre dépassée |
| `docs/redesign/obsidian/*` | 16 | ~3,0 Mo | Thème **Obsidian Copper** (le plus proche de la cible) | fidélité obsidienne+cuivre, densité cockpit | rester une baseline, pas un plafond |
| `static/icon-180.png` | 1 | 885 o | Icône PWA | — | — |

**Total raster suivi : 122 PNG. 0 SVG/JPG/WEBP/PDF. 0 image d'inspiration externe.**

## Références nommées (prose — à étudier, jamais à copier)

| Référence | À en tirer | Cité dans |
|---|---|---|
| Linear / Vercel / Stripe | densité maîtrisée, hover discrets, hiérarchie par poids | manifesto, system.md |
| Bloomberg (terminal) | densité de données, honnêteté (pas de remplissage cosmétique) | manifesto, system.md |
| TradingView | interactions graphiques, densité financière | manifesto |
| Apple / Raycast / Arc / Tesla UI / Notion / Obsidian | hiérarchie, transitions, lisibilité, systèmes de composants | manifesto |

**Interdit explicite** : copie littérale d'un tiers ; esthétique casino
crypto / néon / multicolore SaaS ; bleu identitaire ; glow/halo permanent ;
donuts décoratifs ; cascades d'animation longues ; tout chiffre inventé.

## Conséquence pour la refonte

La refonte **ne dispose pas d'images cibles** : elle doit s'appuyer sur les
specs textuelles ci-dessus et sur les captures `obsidian/` comme meilleure
approximation existante. Toute « référence visuelle » supplémentaire devra être
fournie par l'utilisateur (captures d'inspiration) — elles ne sont pas dans le
dépôt aujourd'hui. Identité canonique **tranchée** : « Obsidian Copper / Inter »
(le code fait foi). Toute référence d'inspiration supplémentaire devra être
fournie par l'utilisateur.
