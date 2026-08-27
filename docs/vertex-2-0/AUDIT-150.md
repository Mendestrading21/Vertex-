# Audit final — 150 contrôles Vertex 2.0

> **Règle appliquée :** un contrôle sans preuve n'est pas réussi. Les contrôles
> qui portent sur une page **non encore refondue dans son contenu** sont marqués
> `À CORRIGER` avec le lot qui les traitera — jamais `RÉUSSI` par optimisme.
>
> Cet audit porte sur la refonte visuelle. Il ne donne aucun droit de modifier le
> backend, et n'en a exercé aucun.

## Périmètre réellement livré

| Lot | État |
|---|---|
| 0 · Baseline | **Livré** |
| 1 · Source de vérité | **Livré** |
| 2 · Coque et navigation | **Livré** |
| 3 · Primitives | **Livré** (bibliothèque `vx2` + 0 rectangle vide) |
| 4 · Graphiques | **Livré** (thème ; migration des conteneurs non faite) |
| 5 · Aujourd'hui | **Livré** (point focal ; sections non réordonnées) |
| 6 · Calendrier et Marchés | **Partiel** — Calendrier livré, Marchés remis en page propre sans refonte de contenu |
| 7 · Opportunités et Analyse | **Non livré** |
| 8 · Options | **Non livré** |
| 9 · Simulateur | **Livré** |
| 10 · Portefeuille et Suivi | **Non livré** |
| 11 · Performance et Vertex IA | **Partiel** — deux squelettes perpétuels corrigés |
| 12 · Système | **Non livré** |
| 13 · Responsive et accessibilité | **Livré** |
| 14 · Nettoyage visuel | **Non livré** |
| 15 · Acceptation | **Cet audit** |

Les pages non refondues **héritent** de l'identité 2.0 par la couche de jetons, et
passent les contrôles transverses (accessibilité, débordement, états vides, console).
Ce qu'elles n'ont pas reçu, c'est une refonte de leur **hiérarchie d'information**.

---

## A. Périmètre, sécurité et vérité — 001 à 015

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 001 | Aucun moteur, formule, score, gate, stratégie ou verdict modifié | **RÉUSSI** | `git diff --name-only main...HEAD` → 0 fichier sous `engines/ options/ portfolio/ strategy/ quant/ data/ …` ni `terminal.py`. Mesuré par `tools/vertex_2_0_audit150.py`. |
| 002 | Aucun provider, endpoint financier, worker, job ou intégration modifié | **RÉUSSI** | Même mesure. Le seul fichier de route touché est `redesign.py` (blueprint d'UI) ; `system.py` ne change que la version du service worker (+4/−4 lignes). |
| 003 | Aucun store, schéma métier, desk sync ou donnée utilisateur modifié | **RÉUSSI** | Aucun fichier sous `storage/ positions/ tracking/ data/`. Les 4 listes de clés de sync desk sont intactes ; `test_desk_sync_keys_single_source_of_truth` vert. |
| 004 | `READONLY`, `ANALYSIS_ONLY` et IBKR readonly restent vrais | **RÉUSSI** | `config.py` : `READONLY = True`, `ANALYSIS_ONLY = True`. 13 occurrences de `readonly=True` dans `vertex/`. `tests/test_no_orders.py` vert. |
| 005 | Aucun bouton, libellé ou raccourci ne prépare ou transmet un ordre | **RÉUSSI** | Balayage des 6 surfaces ajoutées : aucun libellé d'ordre. Le Simulateur écrit explicitement « Vertex ne transmet aucun ordre ». Un faux positif a été trouvé puis **corrigé à la source** : `calendar.js` portait une copie du vocabulaire des verdicts (`ACHETER`/`VENDRE`) ; il lit désormais `window.__VXVOCAB`, la vérité du moteur. |
| 006 | Aucun calcul financier nouveau dans template, CSS ou JavaScript | **RÉUSSI** | `simulator.js` : aucune fonction de pricing, aucune annualisation, aucun `Math.exp/log/sqrt/pow`. Sa seule arithmétique est `toLocaleString`. Toute valeur affichée vient de `/api/options/simulate`, `/api/options/analyze` ou `/api/pretrade/check`. |
| 007 | Aucune donnée fictive n'est affichée comme réelle | **RÉUSSI** | `vx2.valeur(None)` rend `—`. Aucune valeur numérique par défaut dans la bibliothèque. Les exemples de `/design-system` sont étiquetés « aucune n'est une mesure ». |
| 008 | `—`, `n.d.` et états manquants employés honnêtement | **RÉUSSI** | `vx2.capacite_absente()` existe et est **réellement utilisé** : Forex au Simulateur, 4 catégories au Calendrier, verdict de discipline à Performance. |
| 009 | Live, delayed, stale, demo, offline et missing restent distinguables | **RÉUSSI** | `vx2.ETATS` porte 9 états, chacun avec son **libellé français écrit** : la couleur ne porte jamais seule le sens. Visible sur `/design-system`. |
| 010 | Source, timestamp et fraîcheur survivent à la recomposition | **RÉUSSI** | `vx2.estampille()` rend source · horodatage · qualité et **avoue l'absence de chacun**. Le Calendrier affiche « Horodatage indisponible » plutôt qu'une heure fabriquée. |
| 011 | Positions, signaux, idées, simulations et trades réels restent séparés | **RÉUSSI** | Aucune fusion introduite. Le Simulateur écrit « Aucun enregistrement — pas de store de simulations » ; ses sorties ne rejoignent aucune population de performance. |
| 012 | Les scénarios ne sont jamais présentés comme des prédictions certaines | **RÉUSSI** | Titre de carte « Résultats théoriques », sous-titre « Scénarios, pas prévisions », bandeau permanent, et les limites du moteur rendues **avec** le chiffre. Capture `simulator-action-resultat.png`. |
| 013 | Aucun secret, identifiant compte ou payload sensible dans l'UI/log | **RÉUSSI** | Aucun secret ajouté. `test_production_guards_canonical` et `test_namespace_guards` verts ; le nom personnel que portait le skill importé a été neutralisé. |
| 014 | Les textes externes rendus conservent leur sanitization | **RÉUSSI** | Aucun chemin de rendu de news touché. `calendar.js` échappe toute valeur externe via `esc()` ; le Calendrier ne rend aucun texte de news. |
| 015 | Les limites non vérifiées sont déclarées dans la PR | **RÉUSSI** | Section « Limites » dans chaque rapport de lot et dans le récapitulatif final. |

---

## B. Architecture de l'information — 016 à 030

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 016 | Sidebar Piloter/Explorer/Gérer/Intelligence/Système | **RÉUSSI** | `NAV_GROUPS` = `['Piloter','Explorer','Gérer','Intelligence']`, `PINNED_NAV` = Système seul. Capture de la sidebar, lot 2. |
| 017 | Aujourd'hui est la destination initiale claire | **RÉUSSI** | Première entrée = « Aujourd'hui » → `/`. La page porte son surtitre « Piloter » et sa question. |
| 018 | Calendrier global sans dupliquer ses propriétaires spécialisés | **RÉUSSI** | `/calendar` consomme `/cal-feed`, le **seul** agrégat d'événements. `/opportunities?view=calendar` reste servi ; aucun second agrégat n'a été créé. |
| 019 | Marchés, Opportunités, Analyse, Options et Simulateur distincts | **RÉUSSI** | Cinq routes distinctes, chacune en 200. Marchés a retrouvé sa page propre. |
| 020 | Portefeuille, Suivi et Performance ont des responsabilités distinctes | **RÉUSSI** | Trois routes distinctes en 200, trois espaces actifs distincts. |
| 021 | Vertex IA n'absorbe pas les pages métier | **RÉUSSI** | `/intelligence` reste une entrée unique du groupe Intelligence ; aucune page métier n'y a été déplacée. |
| 022 | Système reste utilitaire et épinglé | **RÉUSSI** | `PINNED_NAV` ne porte que Système, hors des quatre groupes de travail. |
| 023 | Journal appartient à Performance | **RÉUSSI** | `/performance` est l'espace ; Journal est sa sous-vue. `/journal` répond toujours 200 et porte `data-active="performance"`. |
| 024 | Watchlist appartient à Suivi/Portefeuille | **RÉUSSI** | `/watchlist` redirige vers `/portfolio?view=watchlist` (inchangé) ; `/follow-up` porte le suivi transversal. |
| 025 | Design System reste interne à la QA | **RÉUSSI** | `/design-system` hors navigation, atteignable par lien depuis Système. |
| 026 | Chaque route secondaire conserve breadcrumb, origine et retour | **RÉUSSI** | Fil d'Ariane cliquable `Vertex / Espace / Sous-vue` sur les 12 pages ; bouton Retour dans la topbar. Visible sur toutes les captures. |
| 027 | Drawer pour comparer/scanner ; page pour profondeur/historique | **RÉUSSI** | Aucune inversion introduite. La comparaison du Simulateur est une **sous-vue** (elle a une URL partageable) ; les détails de ligne restent en drawer. |
| 028 | La recherche globale retrouve ticker, page et fonction existante | **RÉUSSI** | La palette listait les 8 anciens espaces : Calendrier, Simulateur, Suivi et Performance étaient **introuvables** à la recherche. Elle porte désormais les 12 pages et leurs approfondissements, y compris les anciennes URL sous leur nouveau nom. Vérifié au navigateur : « simul » → 3 résultats, « calend » → 6. |
| 029 | Libellés de navigation français, courts et non ambigus | **RÉUSSI** | 12 libellés français, 14 caractères au plus. « Dashboard » a disparu de la navigation et du titre de page. |
| 030 | Aucune fonction existante ne devient introuvable | **RÉUSSI** | `/journal`, `/tracking`, `/design-system` répondent 200. `/markets` est passé de redirection à page. 15/15 routes testées en 200. |

---

## C. Hiérarchie et clarté page — 031 à 045

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 031 | Chaque page formule sa question métier | **RÉUSSI** | `vx2.page_header()` rend la question **obligatoire**. Les 12 pages en portent une, vérifié sur les captures du lot 13. |
| 032 | Le point focal est compris en cinq secondes | **RÉUSSI** pour Aujourd'hui, Calendrier, Simulateur ; **À CORRIGER** pour les 9 autres | Aujourd'hui : DecisionTrace en tête (capture `hero`). Calendrier : chronologie dominante. Simulateur : paramètres → résultats. Les autres pages gardent leur hiérarchie d'origine. → **lots 6-8, 10-12**. |
| 033 | Le premier viewport répond à situation, attention, raison, risque | **RÉUSSI** pour Aujourd'hui ; **À CORRIGER** ailleurs | La DecisionTrace répond aux quatre. → lots de page. |
| 034 | Une seule visualisation ou table domine la page | **À CORRIGER** | Vrai sur Calendrier et Simulateur. Non vérifié sur les pages non refondues. → lots de page. |
| 035 | Les KPI secondaires ne rivalisent pas tous au même niveau | **RÉUSSI** pour Aujourd'hui | La bande de 12 tuiles égales n'est plus le premier écran : elle passe **après** le point focal. Ailleurs : → lots de page. |
| 036 | PageHeader expose périmètre et fraîcheur | **RÉUSSI** pour les pages 2.0 | `vx2.page_header` accepte `surtitre` et `fraicheur`. Calendrier expose sa fraîcheur en ContextBar. |
| 037 | ContextBar expose période, univers, filtres et source | **RÉUSSI** pour Calendrier et Simulateur | Capture `calendrier-agenda-desktop.png` : Horizon · Type · Périmètre · Fraîcheur. |
| 038 | DecisionZone contient le point focal réel | **RÉUSSI** pour Aujourd'hui | La DecisionTrace **est** la DecisionZone, et elle lit `scan_state`, pas un texte figé. |
| 039 | EvidenceZone explique sans répéter | **À CORRIGER** | Non vérifié systématiquement. → lots de page. |
| 040 | WorkZone porte la tâche principale | **RÉUSSI** pour Calendrier (chronologie) et Simulateur (formulaire → résultats) |
| 041 | DepthZone contient méthode, historique et détails | **RÉUSSI** pour Simulateur (Hypothèses, Prise en charge par classe) et Calendrier (Couverture) |
| 042 | Les actions sûres sont proches de leur objet | **RÉUSSI** | « Ouvrir le dossier » sur la ligne de l'événement ; « Ouvrir Système » dans l'état vide qui la motive. |
| 043 | Les explications longues sont progressives | **RÉUSSI** | Tables équivalentes en `<details>` repliés ; disclosures conservées sur Système et Performance. |
| 044 | Les états vides donnent cause et prochaine action sûre | **RÉUSSI** | `vx2.etat()` rend `cause` **obligatoire**. 0 rectangle vide sur 13 routes (`preuves/etats-vides.json`). |
| 045 | Le test de distance confirme une hiérarchie nette | **NON APPLICABLE — jugement humain** | Vérifiable seulement à l'œil, sur les captures. Les captures desktop/mobile sont fournies pour que ce jugement puisse être porté ; je ne le porte pas à la place de l'humain. |

---

## D. Composants, tables et widgets — 046 à 060

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 046 | Chaque primitive a un propriétaire visuel unique | **RÉUSSI** pour les primitives 2.0 | Une classe `.vx2-*` n'est écrite que dans `vertex/ui/vx2.py`. Les familles historiques coexistent encore → **lot 14**. |
| 047 | Tokens, pas de valeurs répétées en dur | **RÉUSSI** pour `vertex-2-0.css` | Aucun hex en dur dans les pages ajoutées ; tout passe par `var(--vx-*)`. Les pages historiques gardent des littéraux → lot 14. |
| 048 | Une famille unique de cartes et MetricCard est utilisée | **À CORRIGER** | `vx2.surface` et `vx2.metric` existent et sont démontrés, mais les 4 familles historiques (`vx-kpi`, `vx-metric`, `vx-stat`, `vx-stat-xl`) n'ont pas migré. Elles sont **visuellement unifiées** par le remappage des jetons ; leur suppression est → **lot 14**. |
| 049 | Boutons, tabs, filtres, champs, badges et drawers cohérents | **RÉUSSI** pour les pages 2.0 | Galerie complète sur `/design-system`. |
| 050 | Les tables utilisent chiffres tabulaires et alignement numérique | **RÉUSSI** | `font-variant-numeric: tabular-nums` sur toute cellule et toute valeur dynamique ; `.vx2-num` aligne à droite. Capture `simulator-action-resultat.png`. |
| 051 | Unités et devises visibles dans colonnes ou valeurs | **RÉUSSI** | L'unité vit dans l'**en-tête** (`vx2-th-unit`), pas répétée par cellule. Vu sur la table du design system (`DERNIER (USD)`, `VARIATION (%)`). |
| 052 | Headers et colonnes clés sticky sans recouvrement | **RÉUSSI** | `th` sticky en haut, `.vx2-sticky-col` à gauche, fond **opaque** — la couture visible sur verre translucide a été corrigée au lot 1. |
| 053 | Tri, filtre et recherche annoncent leur état | **RÉUSSI** pour Calendrier et Simulateur | `aria-pressed` sur chaque chip de filtre ; compteur « 12 sur 12 événements ». Ailleurs → lots de page. |
| 054 | Densité compacte/confortable ne masque aucune donnée critique | **NON APPLICABLE ici** | Le contrôle de densité existant (Compact/Confort/Dense) n'a pas été modifié. |
| 055 | Drawer de ligne conserve contexte et focus | **RÉUSSI** | `role="dialog"`, `aria-modal="true"`, `inert` quand fermé — mesuré au navigateur. |
| 056 | Loading, empty, partial, stale, delayed, offline, demo, error existent | **RÉUSSI** | Les 9 états dans `vx2.ETATS`, rendus sur `/design-system`. Deux squelettes **perpétuels** de `/performance` remplacés par des états honnêtes. |
| 057 | ValueFlash est court, tonal et désactivé en reduced motion | **NON APPLICABLE** | Aucun ValueFlash n'a été introduit. Le mécanisme existant n'a pas été touché. |
| 058 | DataLedger expose couverture et données absentes | **RÉUSSI** | Le Calendrier porte une table de **couverture par catégorie** (4 catégories déclarées sans source) ; le Simulateur une table de **prise en charge par classe**. C'est le DataLedger, sous un nom français. |
| 059 | Aucun widget décoratif ne survit sans question utile | **RÉUSSI** pour les pages 2.0 | Chaque carte ajoutée porte une `question`. `vx2.surface` la propose ; aucune carte 2.0 n'en est dépourvue. |
| 060 | Le registre page → widget correspond au catalogue canonique | **À CORRIGER** | Aucun registre n'a été produit. → **lot 14**. |

---

## E. Graphiques et visualisation — 061 à 075

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 061 | Chaque graphique formule question, conclusion, source, unité, période | **À CORRIGER** | `vx2.chart_card` porte le contrat complet, mais les graphiques existants **n'y ont pas migré**. → lots de page. |
| 062 | Séries, valeurs, agrégations et timeframes inchangés | **RÉUSSI** | Le lot 4 n'a changé que des **couleurs** et deux appels de couleur. Aucune série, aucun calcul. |
| 063 | Les axes ne trompent pas et le zéro apparaît quand nécessaire | **NON APPLICABLE ici** | Aucun axe modifié. Non vérifiable avec des séries : les sources de marché sont injoignables dans cet environnement. |
| 064 | Les gaps ne sont pas reliés silencieusement | **NON APPLICABLE ici** | Idem — aucune série réelle à tracer. |
| 065 | Une hausse n'est pas automatiquement colorée comme positive | **RÉUSSI** | `vx2.valeur()` n'attribue **aucun** ton : il faut le passer explicitement, depuis une lecture du moteur. Le module ne compare jamais une valeur à un seuil. |
| 066 | Argent, gris, vert, rouge, ambre, violet et cyan respectent leur sémantique | **RÉUSSI** | Vérifié **au runtime** : `blue` et `cyan` ne rendent plus le vert de marque abandonné ni un beige ; le cyan analytique vit sous `crosshair`. Séries = argent, gris, pierre, violet, ambre, acier — aucune verte ni rouge. |
| 067 | Tooltip, légende et formatters centralisés | **RÉUSSI** | Un seul `VXChartTheme.tooltip`, réaligné sur les surfaces 2.0. |
| 068 | ResizeObserver ne crée ni boucle ni débordement | **RÉUSSI** | 0 débordement horizontal sur 8 largeurs × 12 pages, après `networkidle` + 1,5 s. |
| 069 | Instances, listeners et observers détruits au démontage | **NON APPLICABLE ici** | Mécanisme existant non touché. |
| 070 | Canvas/SVG reste net en HiDPI | **RÉUSSI** | Toutes les captures sont produites en `device_scale_factor=2`. |
| 071 | Un tableau équivalent existe pour toute visualisation critique | **RÉUSSI** pour les pages 2.0 | Simulateur : table du payoff + matrice cours × temps en tables. Calendrier : agenda tabulaire sous la chronologie. `vx2.chart_card` porte `table_equivalente`. |
| 072 | Le résumé accessible annonce les valeurs clés | **RÉUSSI** pour les pages 2.0 | `<caption class="vx2-sr-only">` sur chaque table ; `resume_accessible` dans `chart_card`. |
| 073 | Une bibliothèque externe possède licence et attribution documentées | **RÉUSSI** | Geist / Geist Mono : **SIL OFL 1.1**, copie intégrale dans `vertex/static/vertex/fonts/licences/GEIST-OFL.txt`. **Aucune** autre dépendance ajoutée — aucun code n'a été copié d'un dépôt tiers. |
| 074 | Les plugins proof-of-concept sont durcis avant production | **NON APPLICABLE** | Aucun plugin introduit. |
| 075 | Le fallback fonctionne quand Canvas/WebGL/JS échoue | **RÉUSSI partiellement** | `@supports not (backdrop-filter)` → graphite plein. Les tables équivalentes sont du **HTML**, donc lisibles sans Canvas. Le cas « JS entièrement désactivé » n'a pas été mesuré. |

---

## F. Options et Simulateur — 076 à 090

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 076 | La chaîne garde CALL/strike/PUT et ATM neutre | **À CORRIGER** | Page Options non refondue. → **lot 8**. |
| 077 | Bid, ask, mid, spread, volume, OI, IV et Greeks absents restent absents | **RÉUSSI** au Simulateur | `/api/options/simulate` refuse sans prix réel : « spot indisponible — simulation refusée (aucune donnée inventée) ». Capture `simulator-option-refus.png`. Page Options → lot 8. |
| 078 | Multiplicateur, coût par contrat et coût total non confondus | **RÉUSSI** au Simulateur | Champ « Prime (mid) » avec l'aide « Par action, pas par contrat » ; métrique séparée « Coût par contrat — prime × multiplicateur ». |
| 079 | Le drawer contrat expose mark, source, heure, qualité et limites | **À CORRIGER** | → lot 8. |
| 080 | Term structure et smile/skew ont table et unités | **À CORRIGER** | → lot 8. |
| 081 | OI/GEX montrent zéro et provenance des niveaux | **À CORRIGER** | → lot 8. |
| 082 | Payoff étiquette date, hypothèses, breakevens et nature théorique | **RÉUSSI** | Simulateur : « Points morts — 180,00 · cours auquel le résultat théorique est nul », carte « Résultats théoriques », section Hypothèses permanente, limites du modèle rendues avec le chiffre. |
| 083 | Vol surface possède une alternative 2D accessible | **NON APPLICABLE** | Aucune surface de volatilité 3D n'existe dans le produit. |
| 084 | Le Simulateur accepte seulement les classes réellement supportées | **RÉUSSI** | Forex est **désactivé** dans le sélecteur et étiqueté « non pris en charge » ; ETF est étiqueté « partiel ». L'état est annoncé **avant** la saisie, pas après. |
| 085 | Montant et quantité explicitement distingués | **RÉUSSI** | Deux champs séparés, avec leurs aides : « En devise du compte. Distinct d'une quantité. » et « Titres pour une action, contrats pour une option. » |
| 086 | Action, ETF, Option et Forex gardent leurs unités spécifiques | **RÉUSSI** | Le libellé du champ de prix bascule entre « Prime (mid) » et « Prix de référence » selon la classe ; les résultats portent `USD` ou `%` selon ce que rend le moteur. |
| 087 | Chaque valeur est marquée Marché/Portefeuille/Moteur/Saisie | **RÉUSSI partiellement** | L'estampille de provenance rend modèle, taux, dividende et base des primes. La distinction à quatre niveaux n'est pas systématique par valeur. |
| 088 | Scénarios A/B/C utilisent la même base de date et devise | **RÉUSSI** | La comparaison écrit « Les trois colonnes partagent la même base de date et la même devise ». Les scénarios viennent d'un **seul** appel moteur, donc d'une seule base. |
| 089 | Aucune sauvegarde n'apparaît sans store canonique | **RÉUSSI** | Aucun bouton « Enregistrer ». La ContextBar écrit « Enregistrement : Aucun — pas de store de simulations ». La sous-vue « Historique » a été **volontairement omise** pour cette raison. |
| 090 | Aucun libellé du Simulateur ne ressemble à une action d'ordre | **RÉUSSI** | Libellés : « Calculer les scénarios », « Ajouter à la comparaison ». Mention permanente « Vertex ne transmet aucun ordre ». |

---

## G. Portefeuille, suivi et performance — 091 à 105

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 091–098 | Valeur/cash/exposition, réconciliation IBKR, tables distinctes, allocation, treemap, contribution, corrélation, concentration | **À CORRIGER** | Page Portefeuille non refondue. → **lot 10**. |
| 099 | Impact simulé séparé du portefeuille réel | **RÉUSSI** | L'impact du Simulateur porte un bandeau permanent : il décrit la **concentration résultante**, ne calcule ni résultat ni bêta ni repli maximal, et « Vertex ne transmet aucun ordre ». |
| 100 | Suivi conserve statut workflow et verdict financier séparés | **À CORRIGER** | → **lot 10**. |
| 101 | Performance sépare toutes les populations | **À CORRIGER** | Non revérifié. → **lot 11**. |
| 102–104 | Equity/drawdown même période, benchmark et limites visibles, heatmap mensuelle | **À CORRIGER** | → **lot 11**. |
| 105 | Journal conserve sync, backups et liens aux dossiers | **RÉUSSI** | Aucune clé de sync desk touchée ; `test_desk_sync_keys_single_source_of_truth` vert. `/journal` sert le même rendu qu'avant. |

---

## H. Identité visuelle et français — 106 à 120

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 106 | Black Glass domine sans devenir gris opaque | **RÉUSSI** | Trois niveaux de verre translucide (`.025 / .045 / .070`) + hairlines `.045–.14`. Captures des 12 pages. |
| 107 | Distribution 82/13/5 approximativement respectée | **RÉUSSI** | Sur les captures : fond obsidienne dominant, structure argent, sémantique rare. Non mesuré au pixel — **appréciation portée sur capture**. |
| 108 | Une lumière dominante maximum par carte | **RÉUSSI** | Vérifié sur les cartes 2.0 : le vert/rouge n'apparaît qu'au chiffre directionnel, l'ambre qu'aux limites. |
| 109 | Deux accents maximum par écran hors rouge/vert directionnels | **RÉUSSI** | Ambre (prudence) et violet (options) sont les seuls accents non directionnels. |
| 110 | Aucune bordure néon permanente n'encadre les cartes | **RÉUSSI** | Bordures à `.045–.075` d'opacité ; aucune ombre colorée, aucun glow permanent. |
| 111 | Les niveaux de surface et l'espace assurent la séparation | **RÉUSSI** | Une seule stratégie de profondeur : verre + contraste tonal + espace négatif. |
| 112 | Geist et Geist Mono chargées avec fallbacks corrects | **RÉUSSI** | `@font-face` local, `font-display: swap`, préchargées dans la coque, précachées par le SW. Repli : General Sans / JetBrains Mono, puis système. **Aucune requête externe.** |
| 113 | Prix, dates, tickers et mesures utilisent tabular nums | **RÉUSSI** | Règle globale sur `.vx-mono`, `[data-numeric]`, `td`, `th` et toutes les valeurs 2.0. |
| 114 | Les titres français sont courts et naturels | **RÉUSSI** | « Aujourd'hui », « Calendrier », « Simulateur », « Suivi », « Performance », « Vertex IA ». |
| 115 | Le jargon anglais inutile a été remplacé | **RÉUSSI** | « Dashboard » → « Aujourd'hui ». DTE devient « Horizon » au Simulateur, avec son aide. |
| 116 | Les sigles financiers conservés ont une aide contextuelle | **RÉUSSI** | CALL/PUT, IV, DTE, NFP, CPI, FOMC : chacun accompagné de son explication en français dans le contexte où il apparaît. |
| 117 | Decision Trace seulement aux cinq emplacements canoniques | **RÉUSSI** | La contrainte est **imposée par le code** : `vx2.decision_trace()` lève une `ValueError` hors de `TRACE_EMPLACEMENTS`. Un sixième emplacement décoratif est impossible à livrer par inadvertance. Actuellement utilisée à **deux** des cinq (Aujourd'hui, et la démonstration `/design-system`). |
| 118 | Vertex Beam reste un reflet de matière discret | **RÉUSSI** | `.vx2-hero::after` : une hairline blanche à 10 % sur le bord supérieur d'une surface élevée. Non animée. |
| 119 | Le test de permutation confirme une identité non générique | **NON APPLICABLE — jugement humain** | Les captures sont fournies pour porter ce jugement. |
| 120 | Le test des tokens ne trouve pas de mini-design-system de page | **RÉUSSI** pour les pages 2.0 | Les pages ajoutées n'écrivent aucun hex ; elles consomment `vx2` et `var(--vx-*)`. Les pages historiques gardent leurs styles inline → **lot 14**. |

---

## I. Accessibilité, responsive et performance — 121 à 135

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 121 | Contraste AA vérifié pour textes et contrôles | **RÉUSSI** | Mesuré au navigateur sur le **texte réellement rendu**, fond résolu en remontant les ancêtres et en composant les alphas. **0 défaut** sur 12 pages × 2 viewports. Deux jetons corrigés : `--vx-smoke` 3,96 → 5,91:1 ; `--vx-text-faint` 2,66 → 5,16:1. |
| 122 | Focus visible jamais masqué | **RÉUSSI** | `:focus-visible` → anneau argent 2 px, `outline-offset: 2px`, sur tout `a, button, summary, [tabindex]`. |
| 123 | Ordre clavier suit l'ordre visuel | **RÉUSSI** | Premier `Tab` sur `/` atteint le lien d'évitement ; aucun `tabindex` positif introduit. |
| 124 | Skip link atteint le contenu principal | **RÉUSSI** | Mesuré : premier `Tab` → `A.vx-skip-link` « Aller au contenu principal ». |
| 125 | Modales/drawers piègent puis restaurent le focus | **RÉUSSI** | Mesuré : `role="dialog"`, `aria-modal="true"`, `inert` quand fermé, sur drawer **et** modale. |
| 126 | Labels, erreurs et aides reliés aux champs | **RÉUSSI** | `vx2.champ()` relie `label[for]`, `aria-describedby` vers l'aide et vers l'erreur, avec `role="alert"`. **0 champ sans étiquette** sur les 12 pages. |
| 127 | Le sens ne dépend jamais de la couleur seule | **RÉUSSI** | `vx2.badge_etat()` écrit **toujours le mot** (« Temps réel », « Différée », « Périmée »…). Les valeurs directionnelles portent leur signe. |
| 128 | Reduced motion supprime les transitions non essentielles | **RÉUSSI** | Mesuré sous `prefers-reduced-motion: reduce` : **0 élément sur 878** conserve une transition ou animation > 50 ms. |
| 129 | Zoom 200 % conserve contenu et actions | **RÉUSSI** | Mesuré à 720 px CSS (équivalent 1440 à 200 %) : **0 débordement horizontal** sur les 12 pages. |
| 130 | 390 et 430 px réellement utilisables | **RÉUSSI** | 0 débordement, 0 défaut d'accessibilité à 390×844. Captures mobiles des 12 pages. |
| 131 | 768 et 1024 px ont une composition dédiée | **RÉUSSI partiellement** | 0 débordement mesuré aux deux largeurs. La grille 2.0 replie `col-3/4 → span 6` sous 1180 px et `→ span 12` sous 760 px. Une composition **spécifiquement conçue** pour la tablette n'a pas été dessinée. |
| 132 | 1280, 1440, 1600 et écran large gardent une ligne de lecture saine | **RÉUSSI** | `--vx2-content-max: 1660px`. 0 débordement à 1280/1440/1600/1920. |
| 133 | Aucun overflow horizontal global | **RÉUSSI** | **0 px** sur 8 largeurs × 12 pages. `overflow-x: clip` sur `html, body`. |
| 134 | Tables et graphiques conservent l'accès aux données sur mobile | **RÉUSSI** pour les tables 2.0 | `vx2.table(cartes_mobile=…)` : sous 760 px la table est masquée au profit de cartes-lignes structurées, **jamais compressée**. Démontré sur `/design-system`. |
| 135 | Budget performance et poids des bibliothèques respectés | **RÉUSSI** | **Aucune bibliothèque ajoutée.** Deux polices variables auto-hébergées : 69 ko + 71 ko. Une feuille CSS : 802 lignes. |

---

## J. Runtime, tests et livraison — 136 à 150

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 136 | Captures avant/après : mêmes données, route, viewport, état | **RÉUSSI** | Même outil, mêmes viewports (1440×1000 / 390×844), `device_scale_factor=2`, locale `fr-FR`, fuseau `Europe/Zurich`, même état de données (sources externes injoignables — état **déterministe**). |
| 137 | Console navigateur sans erreur applicative | **RÉUSSI** | **0 erreur page** sur les 12 routes, desktop et mobile. Un `422` volontaire (refus honnête du moteur sans prix réel) apparaît comme statut de ressource — ce n'est pas une erreur applicative, `pageerror` reste vide. |
| 138 | `/api/client-log` sans erreur liée au lot | **RÉUSSI** | `{"count":0,"errors":[]}` |
| 139 | `/healthz` reste conforme | **RÉUSSI** | `200` |
| 140 | Compileall passe | **RÉUSSI** | `python -m compileall -q terminal.py vertex` → 0 |
| 141 | Suite pytest ciblée passe | **RÉUSSI** | **4246 passés**, 154 ignorés. Un seul échec, **environnemental** : `test_la_classification_est_discriminante` exige `> 100` références git ; ce clone frais en porte 3. Présent **avant** toute modification (relevé au lot 0). |
| 142 | Suite no-orders passe | **RÉUSSI** | `tests/test_no_orders.py` vert. |
| 143 | Les tests des routes et contrats JS passent | **RÉUSSI** | 15/15 routes en 200, y compris les 3 URL historiques conservées. |
| 144 | Modes live/delayed/stale/demo/offline/missing vérifiés | **RÉUSSI partiellement** | **demo**, **missing** et **offline** sont vérifiés au navigateur — c'est l'état réel de cet environnement, et il est exercé sur les 12 pages. **live** et **delayed** ne sont **pas** observables : l'egress vers les fournisseurs de marché est bloqué. Limite déclarée. |
| 145 | Service worker bumpé si le contrat l'exige | **RÉUSSI** | `v219` → **`v224`**, cinq bumps motivés. `tools/vertex_2_0_bump_sw.py` synchronise les six gardiens et l'empreinte `/static` d'un seul geste. |
| 146 | Les caches servent bien les nouveaux actifs visuels | **RÉUSSI** | `vertex-2-0.css` et les deux `.woff2` Geist sont dans le précache du service worker servi. |
| 147 | Aucun consommateur legacy actif supprimé sans preuve | **RÉUSSI** | `/journal`, `/tracking`, `/design-system` répondent 200. Aucun fichier supprimé. |
| 148 | Le rollback est documenté et réalisable | **RÉUSSI** | `git revert` par lot. La couche `vertex-2-0.css` est **additive** : retirer sa ligne de la coque restaure l'identité précédente. |
| 149 | La PR reste brouillon avec risques, limites et preuves | **RÉUSSI** | PR brouillon ; rapports de lot avec limites ; aucune fusion automatique. |
| 150 | Une validation humaine du commit candidat précède toute fusion | **EN ATTENTE — décision humaine** | Rien n'a été fusionné. |

---

## Récapitulatif

| État | Nombre |
|---|---|
| **RÉUSSI** (avec preuve) | 104 |
| **RÉUSSI partiellement** (limite déclarée) | 7 |
| **NON APPLICABLE** (justifié) | 9 |
| **À CORRIGER** (lot nommé) | 29 |
| **En attente de décision humaine** | 1 |

Les 29 `À CORRIGER` se concentrent sur les **lots de page non livrés** : Opportunités,
Analyse, Options, Portefeuille, Suivi, Performance, Système, et le nettoyage. Aucun
n'est une régression : ce sont des refontes de contenu qui n'ont pas encore eu lieu.
