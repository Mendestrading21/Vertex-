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
| 7 · Opportunités et Analyse | **Livré** |
| 8 · Options | **Livré** |
| 9 · Simulateur | **Livré** |
| 10 · Portefeuille et Suivi | **Partiel** — Suivi livré, Portefeuille non refondu |
| 11 · Performance et Vertex IA | **Partiel** — deux squelettes perpétuels corrigés |
| 12 · Système | **Livré** |
| 13 · Responsive et accessibilité | **Livré** |
| 14 · Nettoyage visuel | **Livré** — dette chiffrée, feuille morte étiquetée |
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
| 031 | Chaque page formule sa question métier | **RÉUSSI** | `vx2.page_header()` rend la question **obligatoire**. Les **12 pages** portent la question canonique du contrat, vérifié au navigateur : chacune se termine par « ? ». Quatre portaient une *description* et non une question (« Le régime d'abord, une tendance principale, les détails ensuite ») — corrigées. |
| 032 | Le point focal est compris en cinq secondes | **RÉUSSI** pour les douze pages | Analyse porte désormais sa DecisionTrace **et** son verdict canonique — qui était calculé puis jeté faute de conteneur. Suivi ouvre sur son résumé et ses suivis actifs. |
| 033 | Le premier viewport répond à situation, attention, raison, risque | **RÉUSSI** pour les douze pages | La DecisionTrace répond aux quatre sur Aujourd'hui et Analyse. Ailleurs, la ContextBar 2.0 porte périmètre, nature de la donnée et fraîcheur dès le premier viewport. |
| 034 | Une seule visualisation ou table domine la page | **RÉUSSI** sur onze pages ; **RÉUSSI partiellement** sur Opportunités | Sur Analyse, la réparation du balisage a rétabli la hiérarchie : le dossier ne s'imbrique plus dans la carte d'identité. |
| 035 | Les KPI secondaires ne rivalisent pas tous au même niveau | **RÉUSSI** pour Aujourd'hui | La bande de 12 tuiles égales n'est plus le premier écran : elle passe **après** le point focal. Ailleurs : → lots de page. |
| 036 | PageHeader expose périmètre et fraîcheur | **RÉUSSI** | Les **12 pages** annoncent désormais leur groupe de travail en surtitre — `PILOTER`, `EXPLORER`, `GÉRER`, `INTELLIGENCE`, `UTILITAIRE` — et leur nom canonique. Vérifié au navigateur sur les 12. Sans lui, une page n'annonçait pas où elle se situe dans une navigation devenue groupée. |
| 037 | ContextBar expose période, univers, filtres et source | **RÉUSSI** pour Calendrier, Simulateur, Opportunités, Suivi | Opportunités : Univers · Dernier scan · Source · Fraîcheur, peinte par les **cinq** sous-vues. Suivi : Population · Nature du rendement · Référence · Fraîcheur. |
| 038 | DecisionZone contient le point focal réel | **RÉUSSI** pour Aujourd'hui | La DecisionTrace **est** la DecisionZone, et elle lit `scan_state`, pas un texte figé. |
| 039 | EvidenceZone explique sans répéter | **RÉUSSI** (lot 20) | **Mesuré**, pas affirmé : `tools/vertex_2_0_repetitions.py` relève chaque texte visible des douze pages et signale ce qui apparaît deux fois. Sept répétitions trouvées, quatre corrigées — le verdict Système rendu **deux fois** (pastille puis titre, l'un sous l'autre) ; « À retenir » qui redonnait les **mêmes premières lignes** du brief que la carte voisine ; deux tuiles disant « lecture indisponible » pour deux absences différentes ; trois cartes de Vertex IA portant la **phrase identique**. Résultat : **0 texte explicatif répété sur 12 pages**. Les 4 signalements restants sont des boutons d'état vide et des badges — ils se répètent par contrat (chaque état vide offre sa sortie), et l'outil les classe séparément. Les pieds de carte sont exclus : « · scan Différé » sur trois cartes est la règle de provenance appliquée trois fois, pas une redite. |
| 040 | WorkZone porte la tâche principale | **RÉUSSI** pour Calendrier (chronologie) et Simulateur (formulaire → résultats) |
| 041 | DepthZone contient méthode, historique et détails | **RÉUSSI** pour Simulateur (Hypothèses, Prise en charge par classe) et Calendrier (Couverture) |
| 042 | Les actions sûres sont proches de leur objet | **RÉUSSI** | « Ouvrir le dossier » sur la ligne de l'événement ; « Ouvrir Système » dans l'état vide qui la motive. |
| 043 | Les explications longues sont progressives | **RÉUSSI** | Tables équivalentes en `<details>` repliés ; disclosures conservées sur Système et Performance. |
| 044 | Les états vides donnent cause et prochaine action sûre | **RÉUSSI** | `vx2.etat()` rend `cause` **obligatoire**. 0 rectangle vide sur 13 routes. Le détecteur a d'abord laissé passer un **squelette perpétuel de 60 px** sur `/options` : son seuil de hauteur était à 70 px, et un squelette comptait comme du contenu. Seuil abaissé à 48 px, et un conteneur qui ne porte qu'un squelette compte désormais comme vide — un squelette n'est pas du contenu, c'est une promesse. |
| 045 | Le test de distance confirme une hiérarchie nette | **NON APPLICABLE — jugement humain** | Vérifiable seulement à l'œil, sur les captures. Les captures desktop/mobile sont fournies pour que ce jugement puisse être porté ; je ne le porte pas à la place de l'humain. |

---

## D. Composants, tables et widgets — 046 à 060

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 046 | Chaque primitive a un propriétaire visuel unique | **RÉUSSI** pour les primitives 2.0 | Une classe `.vx2-*` n'est écrite que dans `vertex/ui/vx2.py`. Les familles historiques coexistent encore → **lot 14**. |
| 047 | Tokens, pas de valeurs répétées en dur | **RÉUSSI** pour `vertex-2-0.css` | Aucun hex en dur dans les pages ajoutées ; tout passe par `var(--vx-*)`. Les pages historiques gardent des littéraux → lot 14. |
| 048 | Une famille unique de cartes et MetricCard est utilisée | **RÉUSSI — mesuré au navigateur** | La mention « déjà visuellement unifiées » était **fausse**, et le lot 26 l'a établi en injectant le balisage réel dans une page servie : `.vx-card.vx-kpi` rendait un fond transparent, un filet `rgba(255,255,255,.07)`, un rayon de 16 px et 16 px de rembourrage ; `.vx-stat` un fond `rgba(255,255,255,.024)`, un filet `rgba(222,228,238,.075)`, 12 px de rayon, 12/14 de rembourrage ; `.vx-metric` la même chose à **un pixel près** (11/13). Trois familles rendent désormais une **surface identique** — fond, filet, rayon, ombre, rembourrage, disposition — et un libellé identique ; seule la **taille du chiffre** varie (19 / 22 / 26 px), et cette échelle est déclarée. Les 138 appels ne sont pas migrés : c'est l'**implémentation** qui est unique, pas le nom. `.vx-stat-xl` est exclue et dit pourquoi : ce n'est pas une tuile mais un grand nombre (`-value` + `-label`), sans fond ni filet. Preuve rejouable : `tools/vertex_2_0_tuiles.py` (0 écart non voulu, sortie non nulle au moindre écart — contre-épreuve exécutée) ; gardien `test_tuiles_famille_unique_lot26.py`. |
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
| 060 | Le registre page → widget correspond au catalogue canonique | **RÉUSSI** (lot 19) | `docs/vertex-2-0/REGISTRE-GRAPHIQUES.md` — **72 cartes** dans 12 fichiers, relevées en lisant les sites d'appel. Un premier relevé **runtime** n'a trouvé qu'**une seule** carte sur 24 sous-vues : sans accès aux fournisseurs de marché, presque tous les graphiques tombent en état vide avant d'être construits. La limite est déclarée dans le registre, et l'outil de relevé runtime (`vertex_2_0_graphiques.py`) est livré pour redevenir la mesure de référence sur une machine connectée. |

---

## E. Graphiques et visualisation — 061 à 075

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 061 | Chaque graphique formule question, conclusion, source, unité, période | **RÉUSSI partiellement** (lot 19) | Mesuré, puis comblé : **unité 20→72/72**, **source 66→72/72**, **question 64→69/72** au site d'appel et **72/72 à l'écran** (trois treemaps dont la carte hôte pose déjà la question — la redire l'affichait deux fois). Découverte au passage : `treemap` et `waterfall` rendent un SVG **nu** et **ignoraient silencieusement** `unit`, `source` et `question` — le contrat ne pouvait pas y être tenu, et rien ne le signalait ; elles les portent désormais. **Conclusion 51/72 et période 9/72 assumées** : une conclusion est une *lecture*, qu'un treemap de poids ne produit pas ; une période n'a de sens que pour une série temporelle, et l'inventer sur un instantané fabriquerait une fenêtre qui n'existe pas. Justifié au registre. |
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
| 075 | Le fallback fonctionne quand Canvas/WebGL/JS échoue | **RÉUSSI — mesuré** (lot 27) | `@supports not (backdrop-filter)` → graphite plein ; les tables équivalentes sont du **HTML**, donc lisibles sans Canvas. Le cas « JS entièrement désactivé » **est désormais mesuré**, moteur JS coupé, et il a révélé un défaut réel : **53 squelettes visibles sur dix pages** — 22 sur la seule page d'accueil — promettaient une donnée qu'aucun script ne viendrait chercher. Un écran qui fait semblant de charger ment plus qu'un écran qui dit non. La coque porte maintenant un `<noscript><style>` qui masque tous les squelettes, et un bandeau qui dit **pourquoi** l'écran est muet — placé dans la colonne de contenu après qu'une première version, posée avant `.vx-app`, ait vu ses premiers mots passer sous la barre latérale fixe. Preuve rejouable : `tools/vertex_2_0_sans_js.py` — **0 constat sur les 12 pages**, contre-épreuve exécutée ; gardien `test_repli_sans_js_lot27.py`. |

---

## F. Options et Simulateur — 076 à 090

| № | Contrôle | État | Preuve |
|---|---|---|---|
| 076 | La chaîne garde CALL/strike/PUT et ATM neutre | **RÉUSSI partiellement** | La chaîne existait mais était **inaccessible** : `/options/<sym>` est déclaré deux fois et c'est le JSON qui gagne — neuf liens internes déversaient du JSON brut. La page a désormais `/options/dossier/<sym>`, les neuf liens la suivent, et un bouton l'ouvre depuis l'espace Options en suivant le symbole actif. Le rendu CALL/strike/PUT **alimenté** reste à vérifier sur une machine connectée. |
| 077 | Bid, ask, mid, spread, volume, OI, IV et Greeks absents restent absents | **RÉUSSI** au Simulateur | `/api/options/simulate` refuse sans prix réel : « spot indisponible — simulation refusée (aucune donnée inventée) ». Capture `simulator-option-refus.png`. Page Options → lot 8. |
| 078 | Multiplicateur, coût par contrat et coût total non confondus | **RÉUSSI** au Simulateur | Champ « Prime (mid) » avec l'aide « Par action, pas par contrat » ; métrique séparée « Coût par contrat — prime × multiplicateur ». |
| 079 | Le drawer contrat expose mark, source, heure, qualité et limites | **RÉUSSI** (lot 18) | `/api/pos-quotes` renvoyait **déjà** `mark_source`, `spread_pct`, `bid`, `ask` et `ts` ; **seul `mark` était lu**. Le tiroir expose marque, source de la marque (dernier échange / milieu / clôture veille), fourchette, écart de fourchette avec son seuil d'incertitude, heure de la cotation, mode (temps réel / différé / repli) et limites. Rien n'est calculé : tout vient du serveur tel quel. Capture `lot-18-peuple/options-tiroir-contrat-desktop.png`. |
| 080 | Term structure et smile/skew ont table et unités | **RÉUSSI** (lot 18) | Trois tables équivalentes ajoutées, l'unité dans l'**en-tête** et jamais répétée en cellule : « Échéance (jours) · IV ATM (%) · Strike retenu », « Strike · IV call (%) · IV put (%) · Écart put − call (pts) », « OI call (contrats) · OI put · Solde ». Elles ne recalculent rien — ce sont les nombres de la courbe. Un graphique seul exclut le lecteur d'écran, le zoom fort, l'impression et la copie d'une valeur. |
| 081 | OI/GEX montrent zéro et provenance des niveaux | **RÉUSSI** (lot 18) | Un strike sans contrat et un strike à zéro contrat ouvert se ressemblent sur une barre : la conclusion compte désormais les strikes à zéro, « 0 » s'écrit et ne devient jamais un tiret, et la limite dit d'où viennent les niveaux — **agrégés depuis les contrats du scan, aucun « mur » n'est déduit** : Vertex ne possède pas de moteur de niveaux. |
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
| 091–098 | Valeur/cash/exposition, réconciliation IBKR, tables distinctes, allocation, treemap, contribution, corrélation, concentration | **RÉUSSI** (lot 15) | Sous-vue **Allocation** créée : bande valeur/lignes/plus-gros-titre/HHI, **treemap** des poids, mix par type d'actif, exposition sectorielle avec sa couverture honnête (« 25,6 % de la valeur hors référentiel sectoriel — non répartie »), budget de risque au stop par position, heatmap de corrélations. Tout vient de `/api/portfolio/context` ; **aucun chiffre n'est recalculé dans l'UI**. Réconciliation IBKR et contribution : `renderPnlRecon` et `divBars` existants, vue Synthèse. Captures `lot-15-peuple/`. |
| 099 | Impact simulé séparé du portefeuille réel | **RÉUSSI** | L'impact du Simulateur porte un bandeau permanent : il décrit la **concentration résultante**, ne calcule ni résultat ni bêta ni repli maximal, et « Vertex ne transmet aucun ordre ». |
| 100 | Suivi conserve statut workflow et verdict financier séparés | **RÉUSSI** | Suivi a désormais trois sous-vues correspondant aux **trois statuts réellement servis** par `/api/tracking` (ACTIVE, DATA_REQUIRED, STOPPED) — pas un quatrième inventé. La ContextBar sépare explicitement la population (« Idées suivies ») du rendement (« Hypothétique — jamais encaissé »). |
| 101 | Performance sépare toutes les populations | **RÉUSSI** (lot 16) | Panneau **« Populations mesurées »** : les cinq populations du contrat nommées côte à côte, chacune avec sa nature de résultat (réalisé / latent / théorique / hypothétique / scénario), sa source et son propriétaire. La ContextBar dit laquelle les indicateurs de la page mesurent, avec son échantillon. Les mesures de discipline ont leur propre conteneur — elles écrasaient la bande des résultats déclarés. Capture `lot-16-peuple/performance-desktop.png`. |
| 102–104 | Equity/drawdown même période, benchmark et limites visibles, heatmap mensuelle | **RÉUSSI partiellement** (lot 16) | Equity et drawdown **existaient sans conteneur** : `loadEquity` écrivait dans `vx-pf-equity` et `vx-pf-drawdown`, absents du DOM de toute vue, et `equity-chart.js`/`drawdown-chart.js` n'étaient pas servis. Les deux se dessinent désormais sur la même série, avec limites (« dérivé de la série déclarée — pas un indicateur de marché »). **Heatmap mensuelle : DÉCLARÉE ABSENTE** — son code de rendu avait été remplacé par le corps d'un `loadDiscipline()` retiré, et la réécrire supposerait d'agréger des rendements par mois dans l'UI, ce que `performance-center.md` interdit. Besoin consigné. |
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
| 131 | 768 et 1024 px ont une composition dédiée | **RÉUSSI** (lot 27) | 0 débordement aux deux largeurs, et la composition tablette est **regardée**, pas seulement mesurée. Deux fautes en sont sorties, invisibles à toute autre largeur : (a) `responsive.css` force la barre latérale compacte sous 1024 px et masque `.vx-nav-label`, mais le traitement « repliée » — titres de groupe cachés, filet à la place — est accroché à `[data-sidebar="collapsed"]`, que la requête média ne pose pas : à 768 px, « EXPLORER » rendait « EXPLORE » et « INTELLIGENCE » rendait « INTELLIG » ; (b) le raccourci `⌘K`, en position absolue à droite du champ de recherche, se posait **sur** le texte dès que le champ rétrécissait, faute de rembourrage réservé. Les deux sont corrigées. La composition à 1024 px déplace les actions à côté du titre, met la barre de contexte à deux par rangée et garde les onglets sur une ligne ; à 768 px, l'asymétrie 4/8, 5/7 et 3/9 passe en pile pour garder une largeur de lecture utile. |
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
|---|---:|
| **RÉUSSI** (avec preuve) | 132 |
| **RÉUSSI partiellement** (limite déclarée) | 8 |
| **NON APPLICABLE** (justifié) | 9 |
| **À CORRIGER** | 0 |
| **En attente de décision humaine** | 1 |
| **Total** | **150** |

*Décompte obtenu en LISANT le tableau ligne à ligne — chaque plage groupée est
dépliée (« 091–098 » couvre huit contrôles, « 102–104 » en couvre trois),
chaque numéro de 001 à 150 est attribué une fois et une seule ; aucun n'est
absent. 132 + 8 + 9 + 0 + 1 = 150.*

**Plus aucun `À CORRIGER`.** Le dernier (048) a été fermé au lot 26 — et il a
d'abord fallu admettre que la justification qui le tenait ouvert était fausse :
les quatre familles de tuiles n'étaient **pas** « déjà visuellement unifiées ».
La mesure au navigateur a montré deux fonds, deux filets, deux rayons, et un
pixel de rembourrage d'écart entre `vx-stat` et `vx-metric` — l'écart
accidentel, celui qu'on ne voit pas mais qui empêche deux tuiles voisines de
s'aligner. Ce qui a été unifié, c'est l'**implémentation**, pas les 138 noms
d'appel : les trois familles rendent la même tuile, mesurée, et seule la taille
du chiffre varie.

Le seul `EN ATTENTE` est le **contrôle 150** : la validation humaine du commit
candidat, qui ne peut par définition pas être portée ici — rien n'a été fusionné.
Deux autres contrôles (045, test de distance ; 119, test de permutation) sont
`NON APPLICABLE — jugement humain` : ils se vérifient à l'œil, sur les captures,
qui sont fournies. Je ne porte pas ce jugement à la place de l'humain.

### Ce que la seconde passe a réellement corrigé

Les lots 7, 8, 10, 12 et 14 n'ont pas produit de la décoration : ils ont retiré
des **mensonges structurels**, tous préexistants à la refonte.

| Défaut | Conséquence réelle |
|---|---|
| `</div>` orphelin fermant une `<section>` | **Tout** le dossier Analyse s'imbriquait dans la carte d'identité — cartes empilées, colonnes d'un mot |
| `#an-verdict` référencé, absent du DOM | Le verdict canonique était calculé, récupéré, puis **jeté** |
| Collision de route `/options/<sym>` | **Neuf liens** internes déversaient du JSON brut |
| Règle de base absente (seule la surcharge mobile écrite) | Matrice des connexions illisible sur desktop |
| Alias `blue` → vert de marque, `cyan` → beige | Couleur par défaut de `C.area()`, courbe d'équité |
| `render(view)` ignorant son paramètre | Suivi n'avait aucune sous-vue |
| Emplacements de fraîcheur jamais remplis | Opportunités et Suivi sans provenance |

### Ce que la troisième passe a trouvé — lots 15 à 17

| Défaut | Conséquence réelle |
|---|---|
| `loadKpis`, `loadEquity`, `loadMonthlyAndDist` définis, **jamais appelés** | Bande d'indicateurs, courbe d'équité et drawdown morts sur Performance ; cinquième squelette perpétuel |
| `vx-pf-equity`, `vx-pf-drawdown`, `vx-pf-monthly` absents du DOM de **toute** vue | Trois chargeurs écrivaient dans le vide |
| `heatmap.js`, `equity-chart.js`, `drawdown-chart.js` non servis sur `/performance` | `VXCharts.heatmapCard` restait `undefined` |
| Corps de `loadDiscipline()` collé **dans** `loadMonthlyAndDist` | `b is not defined` dès trois clôtures — et plus une ligne dessinant la heatmap |
| `addEventListener('load', …, {once:true})` après que `load` a tiré | Garde muette : deux blocs attendaient pour toujours, sans rien dire |
| `.vx-kpi-strip` sans **aucune** règle desktop (seule la surcharge mobile) | Onze tuiles empilées sur toute la largeur — même cause qu'au lot 12 |
| `neon-glass.css` portait les seules règles de la pastille de régime | « Régime non qualifié Lecture du marché en cours » — une phrase incohérente, produite par un style absent |
| `VX.fmt.ago(null)` rend « — » dans un pied de carte | Un tiret à l'emplacement d'un âge **se lit comme un âge** — trois pages concernées |
| `allocBars` suffixait « % » en dur | Le budget de risque, en dollars, s'affichait « 3280,0 % » |
| Une part de 0,03 % arrondie à « 0,0 % » | Un zéro de façade pour une ligne qui existe |
| Treemap laissant tomber les tuiles minuscules | Troncature muette, lue comme « tout est là » |

**Aucun de ces défauts n'était détectable** par les contrôles existants :
zéro débordement, zéro erreur console, zéro bloc vide, suite verte. Il a fallu
regarder les captures **et piloter les pages avec des données** — quatre des
défauts ci-dessus n'apparaissent que sur une page peuplée.
