# Données, intégrations et santé

## Sources

Inventorier les sources déjà présentes avant tout ajout : IBKR, TradingView, WMB, marchés, fondamentaux, news, calendrier, options, stockage local et services internes. Pour chacune : entitlement, licence, univers, champs, latence, fraîcheur, pacing, cache, timeout, provenance, qualité, panne partielle et fallback.

## IBKR

Lecture seule stricte. Séparer comptes, positions, quotes, chaînes et P&L. Afficher source du mark et état de marché. Réconcilier sans écraser une donnée utilisateur silencieusement.

## TradingView

Signal authentifié de réévaluation ou contexte, jamais vérité canonique ni déclencheur d'ordre. Conserver timestamp, règle, symbole et payload sanitizé/validé.

## WMB et macro

Brief daté et sourcé ; séparer faits, événements, interprétation et impacts possibles. Ne pas réutiliser un brief ancien sans badge stale.

## News et contenu externe

Sanitization obligatoire avant rendu ; dédupliquer ; conserver source, heure et lien. Une news n'est pas un catalyseur confirmé sans qualification.

## Centre Système

Connexions, santé, freshness par domaine, dernier scan, jobs, caches, erreurs, mode, READONLY, sync, stockage, backups et préférences. Aucun secret dans le navigateur, les logs, captures ou exports.

## Observabilité

Healthz, logs client, erreurs provider, pacing, latence, cache hit, données stale, jobs et dérive de schéma. Une page qui paraît vide doit permettre d'identifier si la cause est source, moteur, endpoint ou rendu.

