# Checklist de release — Vertex 1.0

La release finale `v1.0.0` est interdite tant qu'un élément critique reste
non prouvé sur le commit candidat.

## Code

- [ ] `python -m compileall -q terminal.py vertex`;
- [ ] suite pytest complète verte, nombre enregistré par la CI;
- [ ] `tests/test_no_orders.py` vert isolément;
- [ ] `python -m vertex` démarre;
- [ ] `vertex.runtime:app` fonctionne sous Gunicorn;
- [ ] aucune dépendance cassée (`pip check`);
- [ ] aucun secret ou fichier de compte suivi.

## Données

- [ ] IBKR réel testé en lecture seule;
- [ ] mode sans IBKR;
- [ ] mode démo clairement étiqueté;
- [ ] delayed/stale/offline/missing vérifiés;
- [ ] TradingView anti-replay/déduplication;
- [ ] WMB daté, sourcé et non utilisé comme prix;
- [ ] sauvegarde/restauration des données desk.

## Décision

- [ ] profil V4 actif;
- [ ] options 2/4/6 semaines et DTE 120–240 testés;
- [ ] actions 3/6/12 mois testées;
- [ ] hard gates non contournables;
- [ ] packet immuable/versionné;
- [ ] unknown symbol → données insuffisantes;
- [ ] probabilités calibrées ou explicitement non calibrées.

## Interface

- [ ] huit espaces HTTP 200;
- [ ] desktop et mobile;
- [ ] clavier/focus/contraste/reduced motion;
- [ ] zéro erreur applicative dans `/api/client-log`;
- [ ] aucun graphique ou KPI contradictoire;
- [ ] sources, unités et fraîcheur visibles.

## Exploitation

- [ ] observabilité et health checks;
- [ ] procédure d'installation;
- [ ] rollback exécuté en environnement de test;
- [ ] `main` protégée;
- [ ] anciennes branches classifiées;
- [ ] acceptation humaine signée et datée.

## Verdict

- `NO-GO`: une case critique manque ou une preuve appartient à un autre commit;
- `RC`: contrats installés, validation finale incomplète;
- `GO`: toutes les preuves sont attachées au même SHA et acceptées humainement.
