# CLAUDE.md — Vertex

## Routage des skills

Pour toute refonte visuelle, navigation, page, sous-vue, composant, widget,
tableau, graphique, typographie, responsive, accessibilité ou microcopy :

```text
/vertex-2-0
```

Skill maître : `.claude/skills/vertex-2-0/SKILL.md`.

`vertex-design-2-0` est un alias historique de compatibilité vers
`vertex-2-0`. Il ne définit plus une doctrine indépendante.

Pour une demande non visuelle concernant moteurs, données, stratégie,
sécurité, intégrations ou release, utiliser exclusivement :

```text
/vertex-1-0
```

## Verrou de la refonte visuelle Vertex 2.0

La refonte est strictement une migration de présentation. Elle peut
réorganiser navigation, templates, mise en page, CSS, tokens, composants,
tables, drawers, formulaires, états, rendu des graphiques et texte visible en
français.

Elle ne modifie jamais :

- moteur, formule, score, gate, scénario, stratégie ou verdict ;
- modèle métier, store, persistance, desk sync ou donnée utilisateur ;
- provider, API, endpoint financier, worker, job ou intégration ;
- connexion IBKR, TradingView, WMB, news ou Claude ;
- fonction existante, comportement financier ou invariant lecture seule.

Une nouvelle vue est autorisée seulement si elle compose les routes,
fonctions, endpoints et données existants. Si une capacité manque, afficher un
état honnête et la consigner hors périmètre ; ne pas développer le backend.

## Invariants absolus

1. Vertex reste `READONLY=True` et `ANALYSIS_ONLY=True`.
2. IBKR reste `readonly=True`.
3. Aucun ordre, ticket broker, bouton achat/vente ou automatisation
   d'exécution.
4. Aucune donnée financière inventée ; absence = `—`, `n.d.` ou état explicite.
5. L'IA explique ; elle ne calcule ni ne change le verdict canonique.
6. Toute donnée conserve source, timestamp, fraîcheur et état.
7. Toute modification visible du shell/statique respecte les contrats de
   service worker et les tests existants.

## Direction visuelle canonique

**Vertex Black Glass — Signal Light** : obsidienne et graphite, verre noir,
structure argent/blanc cassé, bordures presque invisibles, Geist + Geist Mono,
densité professionnelle et mouvement très mesuré.

- Vert = positif ; rouge = négatif/risque ; ambre = prudence/donnée dégradée.
- Violet = options ; cyan = focus technique/crosshair exceptionnel.
- Une couleur lumineuse dominante maximum par carte.
- Aucun glow permanent, arc-en-ciel, template SaaS ou esthétique gaming.
- Signature unique : **Decision Trace**, ligne argentée reliant
  Données → Moteur → Décision → Portefeuille sur cinq emplacements définis.

## Sources de vérité

Pour le chantier visuel :

1. ce fichier ;
2. `.claude/skills/vertex-2-0/SKILL.md` et ses références ;
3. `.interface-design/system.md` ;
4. tokens, composants partagés et thème graphique du dépôt ;
5. styles de page seulement pour une exception justifiée.

Les doctrines Copper, Signal Green, Signal OS, Neon Glass, V3 et les anciens
`vertex-redesign-*` sont historiques. Ne pas empiler un nouveau thème.

## Livraison

- partir du dernier `main` ;
- un lot visuel cohérent et réversible par PR brouillon ;
- captures avant/après aux mêmes dimensions ;
- tests, console, clavier, responsive et états dégradés vérifiés ;
- aucune fusion automatique.
