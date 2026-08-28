# Connexions, données et résilience

## Décision d'architecture

Vertex reste local-first et simple tant que les mesures ne prouvent pas le
contraire. Renforcer la façade Flask, les snapshots atomiques et le scheduler
existant avant d'ajouter Redis, PostgreSQL, Celery, Kafka, Temporal ou un autre
service. Toute nouvelle infrastructure exige un seuil mesuré, un ADR, un test
de panne, un runbook et un plan de retrait.

## Matrice de connexion

| Domaine | Source prioritaire | Usage | Cache/snapshot | Dégradation sûre |
|---|---|---|---|---|
| Quotes, barres, contrats, options, IV/Greeks autorisés | IBKR market-data-only | marché live/delayed/frozen selon entitlement | snapshot atomique court + âge | dernier snapshot clairement stale, puis missing |
| Alertes de tracés et règles | webhook TradingView signé | événement de réévaluation | journal idempotent avec nonce/timestamp | conserver l'événement non traité, aucun ordre |
| Identité instrument | OpenFIGI + métadonnées de place déjà autorisées | ticker/FIGI/place/type | cache long versionné | demander désambiguïsation |
| Dépôts et fondamentaux US | SEC EDGAR officiel | faits, documents, XBRL | snapshot par accession/date | champ absent, lien officiel, jamais estimation IA |
| Macro US | FRED/ALFRED | séries et vintages | point-in-time avec date d'observation | dernière valeur stale nommée |
| Macro euro | ECB Data Portal | taux et séries euro | point-in-time | dernière valeur stale nommée |
| ETF | émetteur/factsheet/holdings officiels lorsque accessibles | frais, indice, holdings, dates | snapshot daté par document | couverture partielle visible |
| Résultats/dividendes/calendrier | émetteur, bourse ou source existante qualifiée | événements | déduplication par identité + heure | conflit visible, pas de date inventée |
| News | sources existantes qualifiées + relations investisseurs | contexte, jamais vérité unique | URL canonique + hash + timestamp | liste partielle avec couverture |
| Portefeuille | saisie Vertex uniquement | positions, cash, enveloppes, thèses | store utilisateur sauvegardé/versionné | lecture seule du dernier état local |

OpenBB est une référence utile pour le motif « connecter une fois, normaliser,
consommer partout ». Ne pas l'ajouter comme méta-dépendance tant que les
connecteurs Vertex existants peuvent être consolidés directement.

## Enveloppe canonique

Chaque valeur externe traverse une enveloppe :

```text
value · unit · currency · source_id · observed_at · received_at · age
mode(live/delayed/frozen/eod/demo) · quality · entitlement · fallback
instrument_id · snapshot_id · schema_version · lineage · error
```

Un adaptateur valide identité, schéma, unité, timestamp, plage et doublons avant
publication. Une valeur invalide va en quarantaine ; elle ne pollue ni cache
canonique ni score. Publier un snapshot complet de manière atomique, jamais une
moitié de rafraîchissement.

## Machine fiable

- **Request path** : sert uniquement un snapshot local ; aucun fournisseur ou
  LLM lent dans une requête page.
- **Single flight** : une collecte identique en cours est partagée, pas
  multipliée par les consommateurs.
- **Budgets** : timeout connexion/lecture/total, concurrence et poids définis
  par source.
- **Retries** : bornés, jitter, uniquement erreurs transitoires et opérations
  idempotentes ; respecter pacing et `Retry-After`.
- **Circuit breaker** : fermé/ouvert/sonde, avec raison et prochaine tentative.
- **SWR** : le stale reste visible et daté pendant un rafraîchissement ; jamais
  renommé live.
- **Backpressure** : priorité aux objets visibles/suivis, files bornées et
  abandon explicite du travail obsolète.
- **Atomicité** : écriture temp + validation + replace, empreinte et sauvegarde
  pour les stores persistants.
- **Reprise** : jobs idempotents, checkpoints, verrous avec expiration et arrêt
  propre.
- **Schéma** : version, compatibilité et migration ; dérive détectée avant UI.

## Intelligence connectée

La gateway IA reçoit seulement un `DecisionPacket` minimisé. Elle n'appelle que
des outils de lecture allowlistés, chaque résultat étant validé et cité avant
composition. Ordre : récupérer → valider → calculer par moteur → assembler →
expliquer. Ne jamais laisser le modèle choisir une source, recalculer un nombre
ou combler une absence sans trace.

Prévoir un jeu d'évaluation versionné : questions simples, contradictions,
données stale, unités adverses, prompt injection dans news/document, citation
absente, nombres incompatibles, outil indisponible et packet tronqué. Comparer
exactitude factuelle, fidélité numérique, citations, refus, latence et coût.

## Observabilité utile

Pour chaque source/job : succès, erreur typée, fraîcheur produite, durée,
payload, cache hit/miss, retries, circuit, profondeur de file et dernier
snapshot valide. Pour chaque page : LCP/INP/CLS si mesurables, taille HTML/CSS/JS,
requêtes, erreurs console et temps jusqu'à donnée utile. Pour l'IA : modèle,
version de prompt/schéma, tokens/coût, latence, outils, validations et statut de
grounding, sans contenu privé.

Les traces portent des identifiants techniques opaques. Aucune position, solde,
thèse privée, secret, payload provider brut ou réponse IA complète dans les
logs par défaut.

## Portes d'adoption

Une nouvelle connexion ou bibliothèque entre seulement si :

1. le manque est reproduit et son propriétaire défini ;
2. la licence, les conditions et l'entitlement autorisent l'usage ;
3. le schéma, les unités et la provenance sont contractés ;
4. le quota, les timeouts, le cache et la panne sont testés ;
5. aucune donnée de compte IBKR n'est accessible ;
6. l'impact bundle/runtime et le coût d'exploitation sont mesurés ;
7. le fallback et le retrait sont réalistes ;
8. la PR dédiée conserve Vertex fonctionnel sans la source.

La multiplication des connecteurs n'est pas un indicateur de qualité. La
couverture vérifiable, la fraîcheur et la capacité à expliquer une panne le
sont.
