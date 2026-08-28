# WORK_MANIFEST — Lot 4 · Sécurité privée et exposition

## Objectif

Deux portes fermées par le contrat du skill :

1. **Un démarrage privé non-loopback sans authentification ÉCHOUE** — il ne
   démarre plus avec une phrase d'avertissement, il refuse en nommant les
   trois issues (VERTEX_CODE, DEMO=1, rester loopback).
2. **La démo exposée est non persistante** — un desk public en mode démo ne
   s'écrit plus sur disque ; l'écriture répond un refus honnête.

## Constat d'audit (mesuré)

Déjà en place, et vérifié : verrou VERTEX_CODE (anti-force-brute, temps
constant, session 30 j), cookies HttpOnly/SameSite=Lax/Secure(HTTPS),
en-têtes nosniff/SAMEORIGIN/Referrer/Permissions, HSTS sous HTTPS,
`no-store` sur `/api/desk`, plafond 2 Mo, JSON NaN→null,
`vertex/app/exposition.py` comme propriétaire unique de la règle d'écoute.

Les manques, contre le contrat :

| Exigence du skill | État mesuré |
|---|---|
| « Faire échouer tout démarrage privé non-loopback sans authentification » | `VERTEX_LAN=1` ou `PORT` sans code → **démarre** sur `0.0.0.0` avec une phrase d'avertissement |
| « Rendre la démo publique non persistante » | `/api/desk` et `/restore` **écrivent sur disque** en mode démo exposé |

## Décisions

- Le refus vit dans `exposition.py` (le propriétaire) : nouvelle clé
  `demarrage_refuse` + `raison`, calculée du même état ; `_start_app` la lit
  et sort en erreur. **Pas d'échappatoire** : le contrat n'en prévoit pas —
  la voie publique légitime est la démo, la voie protégée est le code.
- La non-persistance ne touche que la démo **exposée** (`DEMO_MODE` et
  ouverte au réseau) : la démo locale (`DEMO=1` sur loopback, notre propre
  mode de test) continue d'écrire. Un utilisateur local en démo garde son desk.

## Fichiers autorisés

`vertex/app/exposition.py` · `terminal.py` (`_start_app`, lecture du refus) ·
`vertex/app/routes/desk.py` (garde d'écriture) ·
`tests/test_exposition_lot04.py` (neuf) · bancs existants d'exposition ·
`docs/vertex-2-0/lot-04/**`.

## Données à préserver

`desk_data.json` local : intouché. La garde ne s'applique qu'à l'instance
démo exposée, qui par définition ne doit pas porter de données réelles.

## Tests

Rouge d'abord : (1) exposition LAN sans code → `demarrage_refuse` ;
(2) exposition PORT sans code ni démo → refusé ; (3) démo exposée → écriture
desk refusée avec réponse honnête ; (4) démo loopback → écriture permise ;
(5) verrou actif → tout permis. Puis suite complète.

## Rollback

Revert du commit : l'ancien comportement (démarrage permissif) revient.
