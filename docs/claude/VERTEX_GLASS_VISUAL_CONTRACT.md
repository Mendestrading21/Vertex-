# VERTEX — Contrat visuel « Black Glass Institutional »

## Référence

La capture fournie par l’utilisateur est la référence de direction. Elle fixe l’atmosphère, la hiérarchie et la matière visuelle, mais les données, routes et comportements restent ceux du dépôt.

## Intention

Vertex doit être un cockpit d’analyse personnel, sérieux et institutionnel. Le produit doit sembler précis, calme, transparent et immédiatement exploitable. Il ne doit ressembler ni à un template SaaS multicolore, ni à une interface gaming, ni à une démo remplie de chiffres fictifs.

## Fond

- noir profond et neutre ;
- graphite très sombre ;
- aucune dominante bleue ou verte ;
- gradients presque imperceptibles ;
- textures et halos uniquement pour créer de la profondeur.

## Surfaces en verre gris

Créer trois niveaux réutilisables :

```css
--vx-glass-subtle: rgba(255,255,255,.025);
--vx-glass-card: rgba(255,255,255,.045);
--vx-glass-elevated: rgba(255,255,255,.070);
--vx-glass-hover: rgba(255,255,255,.085);
--vx-glass-border-faint: rgba(255,255,255,.055);
--vx-glass-border: rgba(255,255,255,.105);
--vx-glass-border-strong: rgba(255,255,255,.180);
--vx-glass-blur-sm: 10px;
--vx-glass-blur-md: 16px;
--vx-glass-blur-lg: 24px;
```

Ces valeurs sont une base de travail à valider dans le navigateur.

### Règles

- surfaces transparentes, jamais gris opaque ;
- bordures argentées fines ;
- ombres discrètes ;
- blur performant ;
- fallback sans `backdrop-filter`.

## Couleurs

### Structure

- blanc cassé : texte principal ;
- gris argent : chiffres neutres, sélection, focus et série principale ;
- gris moyen : légendes, benchmark et axes ;
- gris sombre : grilles, séparateurs et disabled.

### Sémantique stricte

- vert : gain, hausse, validation, état sain, signal favorable ;
- rouge : perte, baisse, risque, blocage, invalidation, détérioration ;
- orange : prudence, attente, surveillance, incertitude, données partielles ou différées.

La navigation active et les boutons principaux doivent être argent/blanc/graphite, pas verts.

### Bleu

Le bleu ne doit pas être identité, série par défaut, bordure active ou halo global. Les alias legacy bleus sont remappés vers des neutres.

### Violet

Le violet options est fortement réduit et ne porte jamais un verdict.

## Typographie

- Inter pour l’interface ;
- IBM Plex Mono pour chiffres, tickers et mesures ;
- chiffres tabulaires ;
- titre page 30–32 px ;
- section 17–19 px ;
- carte 12–14 px ;
- KPI 24–30 px ;
- meta 11–12 px.

## Densité

Compact, Confort et Dense modifient réellement espacements, lignes, labels et graphiques sans masquer une donnée critique.

## Formes et interaction

- cartes 14–16 px ; contrôles 8–10 px ;
- grille 12 colonnes sur base 4 px ;
- hover subtil, déplacement maximal 1 px ;
- press `scale(.98)` ;
- transitions 140–220 ms ease-out ;
- focus argenté ;
- aucune animation permanente.

## États

Chaque bloc gère loading, empty, error, stale, partial et demo.

## Interdictions

- aucun chiffre inventé ;
- aucune grande nappe colorée ;
- aucun glow néon permanent ;
- aucun graphique décoratif ;
- aucun vert pour bouton/sélection non positive ;
- aucun rouge décoratif ;
- aucun orange de marque ;
- aucune réécriture React/Vue : conserver Flask + Python HTML + JS.
