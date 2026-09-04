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

Ces valeurs sont une base de travail. Claude doit les valider en navigateur et les ajuster à la lisibilité réelle.

### Règles

- les surfaces ne doivent jamais devenir des rectangles gris opaques ;
- la transparence doit rester visible sur le fond noir ;
- les bordures doivent être fines, argentées et non lumineuses en permanence ;
- les ombres doivent rester discrètes ;
- le blur ne doit pas nuire aux performances ;
- prévoir un fallback sans `backdrop-filter`.

## Couleurs

### Structure

- blanc cassé : texte principal ;
- gris argent : chiffres neutres, série principale, sélection, focus ;
- gris moyen : légendes, benchmark, axes ;
- gris sombre : grilles, separators, disabled.

### Sémantique stricte

- vert : gain, hausse, validation, état sain, signal favorable ;
- rouge : perte, baisse, risque, blocage, invalidation, détérioration ;
- orange : prudence, attente, surveillance, incertitude, données partielles ou différées.

La couleur ne sert jamais à décorer. La navigation active et les boutons principaux doivent être argent/blanc/graphite, pas verts.

### Bleu

Le bleu ne doit pas être utilisé comme identité, série par défaut, bordure active ou halo global. Les alias legacy bleus doivent être remappés vers des neutres.

### Violet

Le violet « options » existant doit être fortement réduit. Il peut rester uniquement si une distinction de série impossible à exprimer par forme, motif ou gris est indispensable. Il ne doit jamais porter un verdict.

## Typographie

- Inter pour l’interface ;
- IBM Plex Mono pour chiffres, tickers et mesures ;
- chiffres tabulaires partout ;
- titre de page 30–32 px ;
- titre de section 17–19 px ;
- titre de carte 12–14 px ;
- KPI principal 24–30 px ;
- meta 11–12 px ;
- limiter la quantité de texte visible dans les cartes.

## Densité

Les modes Compact, Confort et Dense doivent modifier réellement les espacements, hauteurs de lignes, labels secondaires et tailles de graphiques sans masquer une donnée critique.

## Formes

- rayon carte : 14–16 px ;
- rayon contrôle : 8–10 px ;
- bordures 1 px ;
- grille 12 colonnes ;
- alignement strict sur une base 4 px.

## Interaction

- hover : légère augmentation de surface et bordure, déplacement maximal de 1 px ;
- press : `scale(.98)` ;
- transitions 140–220 ms, ease-out ;
- focus visible argenté ;
- aucune animation permanente ;
- les mises à jour temps réel peuvent pulser une seule fois, discrètement.

## États

Chaque bloc doit disposer de :

- loading : skeleton cohérent avec le contenu ;
- empty : explication utile et action éventuelle ;
- error : source en échec, sans secret ;
- stale : âge de la donnée ;
- partial : dimensions présentes et manquantes ;
- demo : étiquette explicite, jamais confondue avec le réel.

## Interdictions

- aucun chiffre inventé ;
- aucune grande nappe colorée ;
- aucun glow néon permanent ;
- aucun graphique décoratif ;
- aucun vert utilisé pour un bouton ou une sélection non positive ;
- aucun rouge pour une simple accentuation ;
- aucun orange pour un élément de marque ;
- aucune réécriture React/Vue : respecter l’architecture Flask + Python HTML + JS existante.
