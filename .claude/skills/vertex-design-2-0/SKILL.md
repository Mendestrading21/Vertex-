---
name: vertex-design-2-0
description: Concevoir, restructurer, développer et vérifier toute l'interface Vertex 2.0 selon une identité Black Glass institutionnelle unique, en français, sans modifier les moteurs financiers ni l'invariant lecture seule.
---

# Vertex Design 2.0

## Mission

Faire converger toutes les surfaces de Vertex vers un terminal d'analyse personnel de niveau institutionnel : calme, dense, précis, immédiatement lisible et reconnaissable. La qualité visée est celle d'un produit financier premium construit sur mesure, jamais celle d'un template SaaS recoloré.

Ce skill est l'autorité spécialisée, orchestrée par `vertex-2-0`, pour l'interface, l'expérience, la typographie, les composants, les widgets, les graphiques, la navigation, le responsive et la recomposition des pages de Vertex. Il peut créer une nouvelle page, sous-vue, table ou visualisation lorsqu'elle répond à une question non couverte et qu'une donnée réelle existe. Il complète `vertex-1-0`, qui reste l'autorité pour le produit, les données, les moteurs, la sécurité et la lecture seule.

Il synthétise les méthodes utiles de **Interface Design** (mémoire et cohérence du système), **UI UX Pro Max** (design system, densité, typographie et choix de graphiques), **Vercel Web Design Guidelines** (audit UX/a11y) et **Anthropic Frontend Design** (caractère distinctif). Il ne dépend pas de leur installation : les décisions retenues pour Vertex sont codifiées ici afin d'éviter quatre autorités concurrentes.

## Invariants absolus

- Ne jamais modifier un calcul, score, verdict, hard gate, contrat de données ou pipeline financier pour satisfaire un visuel.
- Vertex reste strictement en lecture seule : aucun ordre, ticket exécutable ou action broker.
- Ne jamais inventer une donnée, une courbe ou un état. Donnée absente = état honnête.
- Tout le texte visible est en français clair, cohérent et professionnel. Les sigles financiers reconnus peuvent rester en anglais avec aide contextuelle.
- Ne pas migrer vers React, Vue ou un autre framework. Consolider Flask, Python HTML, CSS et JavaScript existants.
- Ne pas créer une nouvelle couche de thème au-dessus des anciennes. Remplacer, migrer, tester, puis retirer le legacy devenu sans consommateur.
- Un seul propriétaire par token, composant, route, format et primitive graphique.
- Ne jamais ajouter une page pour augmenter artificiellement le volume. Une nouvelle page doit posséder une question, un propriétaire, une source réelle, des états, une route et une place claire dans l'architecture.

## Sources de vérité

Lire d'abord `CLAUDE.md`, `.claude/skills/vertex-1-0/SKILL.md` et les fichiers réellement modifiés. Pour le design, l'ordre d'autorité est :

1. ce skill et ses références ;
2. `.interface-design/system.md` ;
3. `vertex/static/vertex/css/tokens.css` et la page `/design-system` une fois migrés ;
4. composants partagés et thème `VXCharts` ;
5. styles de page, uniquement lorsqu'ils expriment une exception justifiée.

Les documents Obsidian Copper, Signal Green, Signal OS, Neon Glass et V3 sont historiques. Ils servent à comprendre les régressions, jamais à définir la cible.

## Direction non négociable

Nom : **Vertex Black Glass — Signal Light**.

- Obsidienne et graphite presque noirs ; verre noir translucide, jamais gris opaque.
- Structure blanc cassé et argent. Aucune identité bleue, verte ou multicolore.
- Vert = positif ; rouge = négatif/risque ; ambre = prudence/donnée dégradée ; violet = options uniquement et rarement.
- Pas de bordures décoratives. Utiliser différences de surface, hairlines presque invisibles et espace négatif.
- Typographie canonique : Geist pour l'interface, Geist Mono pour les tickers, prix, pourcentages et mesures.
- Signature : un reflet linéaire argenté très discret, le **Vertex Beam**, uniquement sur un hero, une sélection importante ou un état actif. Aucun glow permanent.
- Motion courte et fonctionnelle. Le produit ne pulse pas, ne flotte pas et ne ressemble pas à un cockpit gaming.

Lire [brand-system.md](references/brand-system.md) avant les fondations visuelles ou la typographie.

## Routage par travail

- Navigation, regroupement ou nouvelle page : lire [information-architecture.md](references/information-architecture.md).
- Carte, KPI, tableau, filtre, formulaire, drawer, état ou widget : lire [components-and-widgets.md](references/components-and-widgets.md).
- Graphique, score visuel, série, tooltip ou provenance : lire [charts-and-data.md](references/charts-and-data.md).
- Refonte d'une page : lire [page-blueprints.md](references/page-blueprints.md), puis les références composants et graphiques utilisées par cette page.
- Nouvelle page, chaîne d'options, portefeuille avancé ou extension maximale : lire [product-expansion.md](references/product-expansion.md).
- Migration globale ou demande « tout refaire » : lire [execution-plan.md](references/execution-plan.md).
- Audit, validation ou livraison : lire [acceptance.md](references/acceptance.md).

## Méthode obligatoire

1. Établir la baseline sur le SHA courant : route, propriétaires, données, états, captures et tests.
2. Identifier les doublons et le composant partagé cible avant d'éditer une page.
3. Corriger d'abord le niveau le plus bas réellement responsable : tokens → shell → primitive → chart core → page.
4. Préserver les endpoints, clés localStorage, desk sync, IDs DOM et contrats JS, sauf migration explicitement cartographiée et testée.
5. Implémenter tous les états : loading, empty, partial, stale, delayed, offline, demo et error selon les données disponibles.
6. Vérifier navigateur, clavier, responsive, console et données réelles avant de conclure.
7. Livrer une PR cohérente et réversible avec captures avant/après, tests, risques et limites. Ne jamais fusionner automatiquement.

## Règle de décision visuelle

Chaque élément doit justifier sa présence par l'une de ces fonctions : orienter, comparer, décider, agir sans danger, expliquer ou prouver. S'il ne remplit aucune fonction, le retirer ou le déplacer dans un niveau secondaire.

La première hauteur d'écran répond toujours à : **que se passe-t-il, que dois-je regarder, pourquoi, et quel est le risque ?**

## Définition de terminé

Une page n'est pas terminée parce qu'elle est plus jolie. Elle est terminée lorsque sa hiérarchie est évidente en cinq secondes, qu'elle utilise seulement les primitives partagées, que ses données et états sont honnêtes, qu'elle fonctionne aux largeurs cibles, qu'elle est navigable au clavier, que la console est vide et que les tests restent verts.
