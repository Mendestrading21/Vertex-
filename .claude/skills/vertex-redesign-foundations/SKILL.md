---
name: vertex-redesign-foundations
description: Implémenter les fondations Black Glass de Vertex : tokens, surfaces, shell, primitives et thème graphique, sans refaire les pages métier.
argument-hint: "[tokens seulement | shell | primitives | charts-core | tout le socle]"
disable-model-invocation: true
---

# Fondations Black Glass

Lire d’abord `CLAUDE.md`, le plan directeur et tous les contrats dans `docs/claude/`.

Demande :

> $ARGUMENTS

## Périmètre

- `tokens.css` et aliases legacy ;
- documentation design ;
- surfaces verre gris ;
- shell, sidebar et topbar ;
- overlays, drawers, modales, palette et toasts ;
- boutons, tabs, champs, tables, badges et états ;
- thème global `VXCharts` ;
- page `/design-system` ;
- responsive et reduced motion des primitives.

## Décisions obligatoires

- marque/sélection neutre argentée ;
- vert uniquement positif ;
- rouge uniquement négatif/risque ;
- orange uniquement incertitude/prudence ;
- aucun bleu dominant ;
- verre gris transparent sur fond noir ;
- fallback sans `backdrop-filter`.

## Exclusions

- ne pas réorganiser les pages métier ;
- ne pas modifier les moteurs ou calculs ;
- ne pas changer les contrats de données ;
- ne pas supprimer une compatibilité avant inventaire.

## Validation

- page Design System ;
- toutes les routes principales ;
- focus, contrastes et clavier ;
- desktop, laptop et tablette ;
- tests palette et UI ;
- console vide ;
- service worker bumpé si nécessaire.
