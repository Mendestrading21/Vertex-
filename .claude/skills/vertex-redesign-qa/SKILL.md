---
name: vertex-redesign-qa
description: Auditer et valider une branche de refonte Vertex contre le plan Black Glass, les invariants métier, les tests et la cohérence graphique.
argument-hint: "[branche, phase ou page]"
disable-model-invocation: true
---

# QA Black Glass

Lire `CLAUDE.md`, le plan directeur, le contrat visuel, le contrat graphique et la checklist d’acceptation.

Cible :

> $ARGUMENTS

## Audit

- diff Git et fichiers touchés ;
- invariants READONLY ;
- contrats et honnêteté des données ;
- palette et tokens ;
- surfaces et transparence ;
- shell et navigation ;
- cohérence de tous les graphiques ;
- états loading/empty/error/stale/partial/demo ;
- responsive et accessibilité ;
- performance et fuites de charts ;
- console ;
- tests ;
- service worker ;
- documentation et rollback.

## Sortie

Classer chaque constat : bloquant, majeur, mineur ou polish. Donner chemins, lignes, reproduction et correction recommandée.

Ne corriger automatiquement que si l’utilisateur demande explicitement l’exécution. Sinon produire uniquement le rapport.
