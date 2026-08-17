# SIGNAL OS · LOT 42 — LA PORTE DE SORTIE, MESURÉE CRITÈRE PAR CRITÈRE

Branche : `agent/vertex-signal-os-v1` · SW **v234** · Suite **3211 passed**
(conditions de la CI : Playwright rendu inimportable)

`VALIDATION.md` finit par un « Final release gate » de huit points. Ce document
ne dit pas qu'ils sont tenus : il **mesure** chacun, nomme l'instrument, et dit
où la mesure s'arrête. Il répond aussi à la question posée pour les trois
skills : *que reste-t-il pour que tout soit à 100 % ?*

---

## 1. Le fait structurel qui commandait tout le reste

Deux lignes longues coexistaient dans le dépôt, et personne n'avait mesuré leur
rapport. C'est fait :

| comparaison | mesure |
| --- | --- |
| `agent/vertex-signal-os-v1` vs `main` | **835 devant, 0 derrière** |
| `agent/vertex-signal-os-v1` vs `integration/vertex-skyler-v2` | **81 devant, 0 derrière** |
| `integration/vertex-skyler-v2` vs `main` | 774 devant, **20 derrière** |

**Il n'y a pas deux lignes : il y en a une.** `agent/vertex-signal-os-v1`
contient l'intégralité de `main` **et** l'intégralité des 601 lots Skyler V2, plus
81 commits. La branche d'intégration Skyler, elle, a pris 20 commits de retard
sur `main` — la garder comme cible de fusion serait une régression.

Conséquence pratique : **une seule branche à valider, une seule à fusionner**.

---

## 2. Les huit critères

| # | critère du gate | instrument | mesure | verdict |
| --- | --- | --- | --- | --- |
| 1 | les 8 pages ont passé leur DoD | intégrité + dégradation + panne partielle + clavier + rognage | voir §3 | **partiel — matrice responsive incomplète** |
| 2 | shell cohérent | registre de navigation + gardiens de shell | suite verte | tenu |
| 3 | palette Python/JS/CSS synchronisée | `test_obsidian_theme`, `test_litteraux_couleur_servis_lot382` | 54 tests verts | tenu |
| 4 | cache PWA cohérent | `test_sw_cache_scope_lot361` | empreinte ↔ v234 | tenu |
| 5 | suite complète verte | pytest en conditions CI | **3211 passed** | tenu |
| 6 | sécurité READONLY verte | `test_no_orders`, surface IBKR (lot 34) | 22 capacités, toutes en lecture | tenu |
| 7 | aucune dette visuelle majeure cachée | §4 de ce document | dette **nommée**, pas cachée | tenu au sens propre |
| 8 | le PR décrit les limitations | §4 + rapports 38/40/41 | à reporter dans le PR | reste à faire au moment du PR |

---

## 3. Ce que les instruments ont rendu aujourd'hui

| invariant | verdict mesuré |
| --- | --- |
| intégrité des pages (1440 + 320) | 0 id dupliqué · 0 erreur de page · 0 débordement · 65 liens, 0 cassé |
| rognage silencieux (1440 + 390) | 0 élément rogné sans ellipse ni défilement |
| opérabilité clavier | 45 contrôles non natifs × 2 touches, **1 muet** — le conteneur défilable, faux positif documenté |
| contrat de focus des surcouches | modale et tiroir : **6 critères sur 6** chacun (ouverture, focus dedans, focus piégé, Échap, `inert`, focus rendu) |
| dégradation honnête (33 vues × 3 pannes) | 0 fuite · 0 vue muette · 0 erreur |
| panne partielle (10 sources) | 0 chiffre, 0 tracé en silence |
| sorties de texte externe (155 routes) | aucune ne sert la charge |
| routes à identifiant (9) | 9/9 couvertes, aucune ne sert la charge |
| pictogrammes peints (10 URL) | **aucun emoji peint** |
| surface IBKR | 22 capacités, toutes en lecture, aucun nom calculé |

---

## 4. Ce qui manque vraiment — la liste, sans arrondi

### 4.1 Ce que j'ai comblé dans ce lot — l'instrument, pas encore son verdict

**À lire avec précision** : ce lot livre les deux instruments qui manquaient et
leur premier relevé complet est **en cours au moment où ce document est
commité**. Je n'écris donc aucun chiffre que je n'ai pas vu. Ce qui est acquis :
le rognage silencieux rend **0 élément rogné à 1440 px** ; les autres largeurs
et l'inventaire des actifs seront ajoutés ici, mesurés, dans un commit de suite.
Poser l'instrument est le travail ; en publier le résultat avant de l'avoir lu
serait exactement la faute que les lots 35 à 38 ont appris à ne plus commettre.


1. **La matrice responsive n'avait que ses deux bouts.** `VALIDATION.md` en
   demande cinq largeurs ; l'outil ne mesurait que 1440 et 320. Or les défauts
   de grille naissent aux **bascules** — 1024 (sidebar compacte), 768 (rail vers
   mobile), 390 (une colonne). Un débordement propre à 768 px passait entre les
   deux mesures. L'outil balaie désormais les cinq.
2. **Le poids réellement chargé n'était pas mesuré.** « Suppression CSS/JS
   legacy devenu inutile » figure dans la passe finale, et la gouvernance exige
   *une preuve d'inutilisation* avant toute suppression. `mesurer_actifs_charges.py`
   produit cette preuve : il visite les 40 vues **dérivées des modules de page**
   plus des fiches par symbole (42 URL), service worker bloqué, et liste les
   fichiers qu'aucune vue ne demande.

   **Son premier verdict était faux, et c'est la partie utile de l'histoire.**
   Il annonçait « 54 fichiers jamais demandés » — c'est-à-dire *tous*. Cause :
   l'inventaire était relatif à `vertex/static` (`vertex/css/tokens.css`) et la
   requête coupée à `/static/vertex/` (`css/tokens.css`). Les deux ensembles ne
   se croisaient jamais. Le garde-fou anti-vacuité existant ne l'a pas vu : il
   vérifiait qu'on observe des requêtes, ce qui était vrai. **Voir des requêtes
   ne suffit pas — encore faut-il qu'elles se raccordent à l'inventaire.**
   L'outil coupe désormais au point commun (`/static/`) et refuse de conclure
   (sortie 2) si l'intersection est vide, en disant que c'est un désaccord de
   chemins et non un produit sans actifs.

   **Et le deuxième verdict était encore trop court.** Corrigé, il rendait
   « 51 fichiers chargés sur 54, trois jamais demandés » — dont
   `js/pages/tracking.js`. Or ce fichier n'est servi que par `/tracking`, une
   route **que je ne visitais pas** : mes 42 URL couvraient les huit espaces,
   pas `/intelligence`, `/tracking`, `/system/design-system` ni `/widget-lab`.
   Déclarer mort un fichier parce qu'on n'a pas ouvert sa page, c'est fabriquer
   la preuve qu'on cherchait. Le balayage couvre maintenant **toutes** les pages
   servies, et c'est de ce relevé-là — et de lui seul — que sortira une
   éventuelle suppression.

### 4.2 Ce qui reste, et qui n'est pas à moi

- **La validation humaine sur appareil physique.** TWS réel, les huit pages,
  l'iPhone. Aucun instrument ici ne la remplace : tout ce qui précède est mesuré
  en démonstration, sans courtier.
- **La fusion vers `main`.** Elle demande un accord explicite ; la règle est
  écrite et je ne la contourne pas.
- **Vingt-six dossiers Skyler V2 en attente de décision.** Le bilan n°18 de
  `docs/skyler/STATUS.md` le dit dans ses propres termes : « 7 à chiffrer,
  7 arbitrages humains », « corrections engagées 0 · gardiens 0 · octets servis
  modifiés 0, sur vingt lots », et « **dix bilans — n°9 à n°18 — attendent une
  réponse** ». Cette file ne se vide pas par du travail : elle se vide par des
  arbitrages.

### 4.3 Les réserves de mesure, toutes ouvertes

1. Les points hors limites (`/api/ticker/`, `/desc/`, `/api/analyst/`…) restent
   raisonnés à la lecture, jamais appelés — consigne de session.
2. Balayage **GET seul** ; `/api/skyler/memory/import` (POST) reste la porte non
   balayée par laquelle du texte arbitraire entre dans la mémoire.
3. Une seule source en panne à la fois.
4. `innerText` ne voit pas les pseudo-éléments CSS.
5. Le jeu de démonstration n'ouvre pas toutes les branches (bandeau d'erreur,
   tiroir ouvert, watchlist remplie).
6. Analyse statique pour IBKR : un ordre par un chemin que l'AST ne relie pas à
   un objet `IB` n'est pas vu ; la défense de fond reste `readonly=True`.

---

## 5. Deux mesures faites au passage, et un faux positif écarté

**Titres.** Sur les huit espaces, le nom de page n'apparaît qu'une fois — dans
le `<h1>` de la page, ce qui est sa place. Une seule redondance réelle :
« Performance de portefeuille » sur la vue `performance` de Portefeuille, où
« Performance » suffirait au sens de `COPY.md`.

**Je ne la corrige pas, et je dis pourquoi.** Ce titre est né au lot 15 avec la
migration de la performance depuis le Journal, et un gardien en fige le libellé
exact. Le mot « portefeuille » y porte le **domicile unique** — c'est ce que le
Journal renvoie chercher ici. Raccourcir gagnerait trois mots et affaiblirait
une règle produit. Déviation assumée, écrite, pas oubliée.

**Composants.** 247 classes `vx-*` servies, dont 110 sur une seule page. Ce
n'est **pas** une divergence : ce sont des blocs nommés par espace (`vx-mk-*`
pour Marchés, `vx-op-*` pour Opportunités, `vx-today-*` pour Aujourd'hui). Trois
« classes » suspectes — `vx-op-metric${hot?'`, `vx-op-cmp-cell${win?'`,
`vx-ss-dot'+(live?'` — se sont révélées être des **gabarits JS non évalués**,
capturés parce que ma sonde lisait aussi l'intérieur des `<script>`. Vérifié
dans la source avant d'accuser.

---

## 6. Ce que ce document permet de dire, et ce qu'il ne permet pas

Il permet de dire que **six des huit critères du gate sont tenus et mesurés**,
que le septième l'est au sens propre (la dette est écrite, pas cachée), et que
le huitième est un geste à faire au moment du PR.

Il ne permet pas de dire « 100 % » : deux choses n'appartiennent pas à
l'instrument — la validation sur appareil réel, et vingt-six arbitrages qui
attendent une réponse humaine depuis dix bilans.
