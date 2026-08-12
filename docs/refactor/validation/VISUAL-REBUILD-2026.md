# Validation — Vertex Visual Rebuild 2026

Date : 12 août 2026
Branche : `agent/vertex-total-rebuild-obsidian-v2`

## Périmètre livré

- fondations Obsidian Copper, grille 12 colonnes et composition hero + rail ;
- shell graphique commun, quatre tailles de tracé, axes/tooltips/touch/mobile ;
- tableaux, disclosures et drawer accessible ;
- Aujourd'hui, Marchés, Opportunités, Analyse, Portefeuille, Options, Journal
  et Système harmonisés ;
- hiérarchie Réponse → Justification → Expertise ;
- données manquantes, démo, fraîcheur, source, limites et READONLY préservés ;
- cache hors-ligne aligné sur `td-shell-v202`.

## Preuves automatisées

- suite complète : **3 005 tests réussis** ;
- `node --check` sur chaque JavaScript modifié : réussi ;
- `py_compile` sur chaque page Python modifiée : réussi ;
- `git diff --check` : réussi ;
- garde-fou des assets hors-ligne : empreinte
  `647e05ab61249668ecd3fabc8a8df3d312a4ab4f113d6c62969a519e1f94eeaa`.

## Preuves navigateur

Matrice Playwright en `DEMO=1`, `NO_IBKR=1`, `VERTEX_AUTH=0` :

- **41 routes/sous-vues** ;
- **6 largeurs** : 390, 768, 1024, 1366, 1440 et 1920 px ;
- **246 rendus** ;
- 0 statut HTTP inattendu ;
- 0 erreur console ou `pageerror` finale ;
- 0 débordement horizontal non contenu ;
- 0 identifiant dupliqué ;
- 0 tracé de taille aberrante ;
- un seul onglet sélectionné au maximum par vue.

Une course de chargement du thème graphique sur Système → Données a été
détectée, corrigée, puis rejouée 30 fois sur les six largeurs sans erreur.
L'inspection des captures 390/1440 a également trouvé une matrice de connexions
trop comprimée sur mobile : elle est désormais rendue en lignes à deux niveaux,
avec libellés français courts et code technique conservé dans le détail.

La RC courte finale confirme :

- huit espaces à HTTP 200 ;
- journal client vide ;
- service worker v202 ;
- bundle mémoire altéré refusé avec `empreinte_invalide` ;
- restauration par le vrai parcours utilisateur réussie ;
- **RC COURTE : GO — 0 défaut**.

## Invariants

Aucun moteur financier, calcul, endpoint métier ou chemin d'exécution d'ordre
n'a été ajouté ou modifié. IBKR reste strictement READONLY. Les changements
portent sur la hiérarchie, la présentation, l'accessibilité, la cohérence des
graphiques et la divulgation progressive.
