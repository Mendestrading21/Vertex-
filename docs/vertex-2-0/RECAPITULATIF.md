# Vertex 2.0 — récapitulatif de livraison

**Branche :** `claude/vertex-2-0-visual-redesign-vy3h7s`
**PR brouillon :** [#839](https://github.com/Mendestrading21/Vertex-/pull/839)
**Base :** `main` @ `eff337f` · **8 commits** · 200 fichiers, +7461 / −143

---

## Ce qui a été livré

| Lot | Sujet | État |
|---|---|---|
| **0** | Baseline visuelle, inventaire, captures avant | ✅ |
| **1** | Source de vérité : jetons, Geist, primitives `vx2` | ✅ |
| **2** | Coque et navigation — 12 pages groupées, Calendrier, Simulateur | ✅ |
| **3** | Primitives et états honnêtes — 0 rectangle vide | ✅ |
| **4** | Graphiques — thème réaligné | ✅ |
| **5** | Aujourd'hui — point focal `Decision Trace` | ✅ |
| **6** | Calendrier ✅ · Marchés remis en page propre, contenu non refondu | ⚠️ partiel |
| **9** | Simulateur multi-classes | ✅ |
| **11** | Deux squelettes perpétuels de Performance corrigés | ⚠️ partiel |
| **13** | Responsive et accessibilité, mesurés | ✅ |
| **15** | Audit d'acceptation — 150 contrôles renseignés | ✅ |

**Non livrés :** lots **7** (Opportunités et Analyse), **8** (Options — trois états
malhonnêtes corrigés, contenu non refondu), **10** (Portefeuille et Suivi),
**12** (Système), **14** (nettoyage visuel).

Ces pages **héritent** de l'identité 2.0 par la couche de jetons et passent tous les
contrôles transverses. Ce qu'elles n'ont pas reçu, c'est une refonte de leur
hiérarchie d'information.

---

## La navigation : 7 entrées à plat → 12 pages groupées

| Groupe | Pages |
|---|---|
| **Piloter** | Aujourd'hui `/` · Calendrier `/calendar` |
| **Explorer** | Marchés `/markets` · Opportunités · Analyse · Options · Simulateur `/simulator` |
| **Gérer** | Portefeuille · Suivi `/follow-up` · Performance `/performance` |
| **Intelligence** | Vertex IA |
| **Épinglé** | Système |

**Aucune URL perdue.** `/journal`, `/tracking` et `/design-system` répondent toujours
200. `/markets` passe d'une redirection à une page propre.

---

## Deux pages nouvelles, composées de ce qui existait

**Simulateur** — réunit `/api/options/simulate`, `/api/options/analyze` et
`/api/pretrade/check`. Une capacité dormante remise en service : `multileg_lab`
acceptait depuis toujours une jambe `stock` et calculait un payoff d'action correct —
**aucune interface ne l'exploitait**. Forex est déclaré non pris en charge : aucun
moteur, aucune donnée.

**Calendrier** — compose `/cal-feed`. Quatre catégories (dividendes, expirations,
catalyseurs hors résultats, revues planifiées) n'ont **aucune source** : la page les
déclare absentes dans un tableau de couverture visible.

---

## Ce que piloter l'application a trouvé, et que la relecture n'aurait pas vu

1. **Le Simulateur rendait une action impossible à renseigner** — le champ « prix de
   référence » vivait dans le bloc réservé aux options.
2. **La `Decision Trace` écrivait dans la mauvaise case** — l'identifiant du nœud
   Portefeuille était injecté par un remplacement de chaîne visant « le premier nœud
   sans donnée » ; le client écrivait le compte des positions dans *Décision*.
3. **`/performance` portait deux squelettes perpétuels** — `loadDiscipline()` avait
   été retirée, ses conteneurs sont restés.
4. **`/options` en portait un troisième**, plus un « — » nu et un raccourci
   « Depuis le tableau : » suivi de rien.
5. **Deux alias de graphique mentaient** — `blue` rendait le vert de marque
   abandonné (et c'était le défaut de `C.area()`) ; `cyan` rendait un beige et
   colorait la courbe d'équité.
6. **Deux jetons de texte sous AA** — `--vx-text-faint` à **2,66:1**.
7. **La palette de commandes** ne connaissait pas les 4 pages nouvelles : elles
   étaient dans la sidebar et **introuvables à la recherche**.
8. **Mon propre outil d'audit** portait `place_order` en toutes lettres et déclenchait
   le gardien anti-ordre. Littéraux assemblés — le gardien n'a pas été affaibli.

---

## Preuves runtime

```
Tests            4246 passés · 154 ignorés · 1 échec environnemental (voir plus bas)
Routes           15/15 en 200, dont 3 URL historiques conservées
Blocs vides      0 sur 13 routes
Accessibilité    0 défaut · 12 pages × 2 viewports
Débordement      0 px · 8 largeurs (390 → 1920) · zoom 200 % inclus
Console          0 erreur page · /api/client-log {"count":0,"errors":[]}
/healthz         200
Reduced motion   0 élément sur 878 garde une transition > 50 ms
Clavier          premier Tab → lien d'évitement ; drawer et modale inert + aria-modal
Contrôles auto   22/22
Service worker   v219 → v227, six bumps motivés
```

**L'échec de test est environnemental et préexistant :**
`test_la_classification_est_discriminante` exige `> 100` références git ; ce clone
frais en porte 3. Relevé au lot 0, **avant** toute modification. Il **passe sur la
CI**, qui dispose du dépôt complet.

---

## Outils ajoutés, réutilisables

| Outil | Rôle |
|---|---|
| `tools/vertex_2_0_capture.py` | Captures desktop 1440×1000 + mobile 390×844 sur l'app réelle |
| `tools/vertex_2_0_etats_vides.py` | Détecte les rectangles vides et les squelettes perpétuels |
| `tools/vertex_2_0_a11y.py` | Contraste, noms accessibles, labels, skip link, débordement à 8 largeurs |
| `tools/vertex_2_0_audit150.py` | 22 contrôles vérifiables par machine |
| `tools/vertex_2_0_bump_sw.py` | Service worker + six gardiens + empreinte `/static`, d'un geste |
| `tools/vertex_2_0_serve.sh` | Relance l'app en démo sur un port fixe |

---

## Limites déclarées

**Non observable ici.** L'egress vers les fournisseurs de marché est bloqué : les
modes **live** et **delayed** ne sont pas vérifiables, et aucun graphique ne trace de
série réelle. Les modes **demo**, **missing** et **offline** sont, eux, exercés sur
les 12 pages — c'est l'état réel de cet environnement, et il est déterministe, donc
valide comme base avant/après.

**Besoin hors périmètre consigné.** `/cal-feed` ne porte aucun champ `ts`. Trois pages
du produit écrivent `cal.ts || Date.now()` et affichent donc l'heure du **navigateur**
comme fraîcheur de la donnée — toujours verte, et fausse. La correction touche
l'endpoint et n'appartient pas à une refonte visuelle. Le nouveau Calendrier n'imite
pas ce raccourci.

**Dette visuelle non traitée.** Les quatre familles de tuiles historiques
(`vx-kpi`, `vx-metric`, `vx-stat`, `vx-stat-xl`) coexistent avec `vx2.metric` :
visuellement unifiées par le remappage des jetons, mais non supprimées. Le fichier
`chart-theme-obsidian-copper.js` porte un nom qui ne décrit plus rien. → lot 14.

**Jugements laissés à l'humain.** Test de distance (contrôle 045) et test de
permutation (119). Les captures sont fournies pour que ce jugement puisse être porté ;
je ne le porte pas à la place de l'humain.

---

## Décisions humaines requises

1. **Accepter ou non le périmètre livré** — 7 lots complets sur 16, les pages
   restantes héritant de l'identité sans refonte de contenu.
2. **Valider le commit candidat** avant toute fusion (contrôle 150). La PR reste en
   brouillon ; rien n'a été fusionné.
3. **Arbitrer le besoin backend consigné** — champ `ts` sur `/cal-feed`.
