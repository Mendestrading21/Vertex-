# SKYLER — LOT 618 · FONDATIONS VISUELLES OBSIDIAN COPPER

Ce lot exécute la refonte visuelle globale de Vertex sans toucher aux données,
aux calculs financiers ni aux routes métier. Il ne prétend pas transformer un
jugement esthétique en vérité mesurable : il rend vérifiables les fondations
dont une régression créerait une interface incohérente ou trompeuse.

## Identité : une source canonique, trois miroirs

Le registre CSS porte désormais l'identité **Obsidian Copper** : surfaces
graphite, marque cuivre **#D28A54**, interaction **#E1A06E**. Le nouveau gardien
résout les alias CSS et compare leur valeur à la palette Python, au thème JS et
au repli de `chart-core.js`.

La séparation sémantique est explicite et gardée :

- cuivre = identité, sélection, action prioritaire, série de référence ;
- émeraude = gain/hausse/confirmation réelle ;
- corail = perte/risque réel ;
- `palette.COPPER` reste l'alias historique de la série acier **#8A8284**.

Le cuivre ne peut donc pas devenir silencieusement une couleur de décision, et
la série acier ne peut pas suivre un changement de marque par accident.

## Le gardien a trouvé un défaut avant publication

Le premier passage du nouveau test donnait **6 passed / 1 failed**. La règle
responsive annonçait l'empilement des couples **4/8, 5/7 et 3/9** à 1024 px,
mais `.vx-col-3` manquait dans le sélecteur. La cascade réelle donnait
**3/12** : une carte pleine largeur suivie d'une carte orpheline sur un quart de
ligne.

Le test n'a pas été assoupli. L'intégrateur a ajouté `.vx-col-3` à la règle de
production ; le gardien passe ensuite **7/7**.

La vérification accepte trois géométries cohérentes : ratio natif totalisant 12,
deux demi-colonnes 6/6, ou pile 12/12. Elle refuse les combinaisons intermédiaires
qui laissent une ligne partiellement vide. Les largeurs dérivées de la cascade
sont 1440, 1280, 1100, 1024, 768, 640 et 390 px.

## Contrats graphiques gardés par le comportement

Les sondes JavaScript exécutent le code servi dans Node avec un DOM minimal.
Elles inspectent les objets et callbacks réellement produits, pas seulement la
présence d'une chaîne dans les sources.

| contrat | preuve encodée |
| --- | --- |
| Chart Shell | **Détails** n'existe que si au moins une rubrique `explain` contient un vrai texte ; le drawer ne fabrique aucune rubrique `—` |
| donut | au-delà de cinq catégories, les quatre premières restent nommées et la queue devient **Autres**, total conservé, couleur neutre |
| barres horizontales | `valueFmt` formate l'axe X de valeurs, le tooltip et la valeur dominante ; l'axe Y catégoriel ne reçoit pas ce formateur |
| heatmap | l'intensité reste dans fond/liseré, l'encre reste stable ; l'échelle expose minimum, zéro lorsqu'il est traversé et maximum |
| cartes inertes | aucun hover de `.vx-card`/`.vx-kpi` sans affordance interactive explicite |

Les données synthétiques de ces tests ne servent qu'à vérifier les
transformations visuelles. Elles ne sont ni servies ni persistées comme données
produit.

## Portée et limites

- Les **8 routes Flask canoniques répondent 200**.
- Une validation par navigateur réel n'a pas été possible dans cet
  environnement : Chromium est bloqué par la sandbox et le navigateur cloud ne
  voit pas `localhost`. **Aucune capture, mesure pixel ni affirmation “zéro
  erreur console” n'est fabriquée.** Cette réserve reste ouverte.
- Le responsive est dérivé de la cascade CSS aux sept largeurs citées ; ce
  n'est pas une mesure géométrique au pixel dans Chromium.
- La sonde Chart Shell couvre une explication absente, vide puis partielle ;
  elle ne juge pas la qualité éditoriale du texte.
- Le gardien de hover vérifie l'affordance déclarée dans toutes les feuilles CSS
  produit, pas la perception humaine du mouvement.
- Sources, fraîcheur, limites, états `n/d`, démo et données insuffisantes ne
  sont ni supprimés ni réinterprétés.

## Cycle

- Baseline : **2927 tests**.
- Nouveau gardien : `tests/test_visual_foundations_lot618.py`, **7 tests**, tous
  verts après le correctif responsive.
- Suite finale : **2934 passed / 0 skipped**.
- Mutations rouges : **non exécutées, donc non mesurées**.
- Production : **24 fichiers** — `system.py`, 10 CSS, 7 JS, 5 pages UI et
  `palette.py`.
- Tests existants adaptés par l'intégrateur : **15** ; avec le nouveau gardien,
  **16 fichiers de test** touchés.
- Diff suivi avant ajout du nouveau test et des rapports : **+474 / −392**.
- Service worker : **v199 → v200**.
- Empreinte finale :
  `5b21d0c4dc395fabc61376d7e3b58d72a20eae6f7f790afbb688f73984845dad`.
- **READONLY confirmé** par la suite et le garde d'absence d'exécution d'ordre ;
  aucune logique financière ni route métier modifiée.

## Verdict

**GO tests, avec réserve explicite de validation navigateur réelle.**
