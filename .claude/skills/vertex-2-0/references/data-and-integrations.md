# Données, intégrations et santé

Contrat de source transversal. Toute modification de connexion, cache, job ou
modèle exige un lot, des tests hostiles, une migration et un rollback.

## Sources

Inventorier les sources déjà présentes avant tout ajout : IBKR, TradingView, WMB, marchés, fondamentaux, news, calendrier, options, stockage local et services internes. Pour chacune : entitlement, licence, univers, champs, latence, fraîcheur, pacing, cache, timeout, provenance, qualité, panne partielle et fallback.

## IBKR

Données de marché uniquement. Autoriser contrats, quotes, barres, chaînes,
volume/OI, IV, Greeks et états de marché. Interdire comptes, positions, cash,
NAV, P&L, ordres, exécutions et réconciliation broker. Le gateway ne rend
jamais l'objet IB brut. La source du mark, son âge et son entitlement restent
visibles ; une panne de cote ne modifie aucune position déclarée.

## TradingView

Signal authentifié de réévaluation ou contexte, jamais vérité canonique ni déclencheur d'ordre. Conserver timestamp, règle, symbole et payload sanitizé/validé.

## WMB et macro

Brief daté et sourcé ; séparer faits, événements, interprétation et impacts possibles. Ne pas réutiliser un brief ancien sans badge stale.

## News et contenu externe

Sanitization obligatoire avant rendu ; dédupliquer ; conserver source, heure et lien. Une news n'est pas un catalyseur confirmé sans qualification.

## Centre Système

Connexions par capacité, santé, freshness par domaine, dernier scan, jobs,
caches, erreurs, mode, READONLY, sync, stockage, backups et préférences. Le
statut provient d'une preuve runtime. Aucun secret, identifiant de compte ou
patrimoine dans navigateur, logs, captures, télémétrie ou exports techniques.

## Observabilité

Healthz, logs client, erreurs provider, pacing, latence, cache hit, données stale, jobs et dérive de schéma. Une page qui paraît vide doit permettre d'identifier si la cause est source, moteur, endpoint ou rendu.
