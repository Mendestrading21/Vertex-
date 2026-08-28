# Couverture des sous-vues, mesurée

`navigation-and-pages.md` fixe, page par page, le jeu de sous-vues attendu. Ce
document dit ce qui est servi, et **pourquoi** six entrées ne le sont pas.

Le décompte est obtenu en important chaque module de page et en lisant son
`_VIEWS`, pas en le supposant.

| Page | Couverture | Manque |
|---|---:|---|
| Calendrier | 7/7 | — |
| Marchés | 6/6 | — |
| Opportunités | 6/6 | — |
| Options | 7/7 | — |
| Simulateur | 3/3 | — |
| Portefeuille | 6/6 | — |
| **Suivi** | **2/7** | Watchlist · Opportunités suivies · Positions · Options · Alertes |
| **Performance** | **5/6** | Tracking hypothétique |
| Vertex IA | 6/6 | — |
| Système | 8/8 | — |
| **Total** | **56 / 62** | **6** |

## Les six manquantes ne sont pas des oublis

### Suivi — cinq entrées qui appartiennent à d'autres pages

`/api/tracking` distingue exactement **trois** statuts : `ACTIVE`,
`DATA_REQUIRED`, `STOPPED`. Suivi en sert trois, une par statut. On n'en
invente pas un quatrième pour remplir une barre d'onglets.

Les cinq autres entrées du contrat ont **déjà un propriétaire** :

| Entrée du contrat | Propriétaire réel |
|---|---|
| Watchlist | Portefeuille → **Thèses** (le store desk y vit, avec son workflow) |
| Opportunités suivies | **Opportunités** (le funnel et les verdicts y vivent) |
| Positions | Portefeuille → **Positions** |
| Options | Portefeuille → **Options** |
| Alertes | Système → **Alertes techniques** et le desk local |

Les dupliquer ferait exister deux endroits où lire la même vérité — la faute
que le contrat lui-même interdit ailleurs (« chaque carte renvoie vers son
propriétaire ; aucune logique dupliquée »). La page **y renvoie** dans son
panneau « Ailleurs dans Vertex », en disant pourquoi.

### Performance — « Tracking hypothétique »

C'est la population des **idées suivies**, servie par `/api/tracking` et
mesurée par **Suivi**. Le panneau « Populations mesurées » de Performance la
nomme, dit sa nature (« hypothétique — jamais encaissé ») et renvoie à son
propriétaire. En faire un onglet dupliquerait une population que Performance
prend soin, par ailleurs, de ne jamais mélanger aux autres.

## Ce que ce document ne dit pas

Il mesure la **présence** des sous-vues, pas la qualité de leur contenu. Les
contrôles d'acceptation (`AUDIT-150.md`) s'en chargent.

## Comment le remesurer

Le tableau ci-dessus est produit en important chaque module de page et en
lisant `_VIEWS` / `VIEWS`. Deux entrées sont ajoutées à la main parce qu'elles
sont des **pages** et non des sous-vues, tout en figurant dans la barre
d'onglets : `Design System` (Système) et `Chaîne` (Options → `/options/dossier/`).
