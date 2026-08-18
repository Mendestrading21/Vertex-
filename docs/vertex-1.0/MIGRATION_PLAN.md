# Plan de migration vers Vertex 1.0 final

## Phase 0 — Source de vérité

- [x] version produit et point d'entrée canoniques;
- [x] profil stratégique V4;
- [x] skill Claude unique;
- [x] corpus documentaire actif;
- [x] CI contractuelle;
- [ ] CI complète verte sur la PR;
- [ ] acceptation humaine de la fondation.

## Phase 1 — Inventaire exécutable

Générer depuis le commit courant:

- graphe import/appels;
- routes et propriétaires;
- pages, scripts et styles réellement servis;
- moteurs appelés/non appelés;
- fichiers runtime et données locales;
- tests par domaine;
- métriques de taille, complexité et dépendances.

Aucun chiffre historique n'est repris comme baseline sans reproduction.

## Phase 2 — Runtime modulaire

Extraire de `terminal.py`:

1. factory Flask;
2. enregistrement des blueprints;
3. lifecycle et workers;
4. scheduler;
5. configuration et observabilité;
6. caches/persistance.

Chaque extraction conserve un adaptateur, un test de parité et un rollback.

## Phase 3 — Domaines

Converger:

- `company` + `companies`;
- `data` + `data_sources`;
- `portfolio` + `positions` + `tracking`;
- endpoints options vers une façade versionnée;
- décision vers un packet et un propriétaire uniques.

Interdiction de renommer/supprimer avant preuve des consommateurs.

## Phase 4 — WMB

Créer un adapter WMB versionné:

- date de publication et période de marché;
- sources primaires;
- événements et chiffres;
- impacts par actif/secteur;
- niveau de confiance;
- statut de vérification;
- hash du contenu.

Le brief alimente le contexte macro, jamais les prix ou Greeks.

## Phase 5 — Design

- figer tokens et composants;
- charger une seule couche de thème;
- extraire sélectivement les meilleurs éléments Signal OS;
- réduire graphiques et KPI dupliqués;
- valider desktop, mobile, clavier, contraste et panne partielle;
- supprimer Neon/legacy seulement après preuve de non-usage.

## Phase 6 — Données et mémoire

- store canonique avec migrations et verrouillage;
- sauvegardes vérifiées;
- historique immuable des packets/décisions;
- calibration des probabilités et résultats aux horizons déclarés;
- séparation stricte données de compte, simulation et démo.

## Phase 7 — Release

- CI complète et reproductible;
- tests navigateur;
- test local sans IBKR, démo et panne partielle;
- test TWS/IB Gateway réel en lecture seule;
- audit secrets/dépendances;
- sauvegarde et rollback;
- protection de `main`;
- tag `v1.0.0` uniquement après acceptation humaine.
