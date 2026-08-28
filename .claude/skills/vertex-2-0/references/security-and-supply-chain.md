# Sécurité, dépendances et supply chain

## Modèle de menace minimal

Protéger secrets, portefeuille déclaré, thèses, notes, prompts, webhooks,
stockage local/serveur, session TWS, données externes et chaîne de build.
Documenter frontières de confiance, attaquants plausibles, données sensibles,
écriture autorisée et conséquences d'une panne.

## Contrôles

- secrets hors Git, rotation et logs redacted ;
- cookies/session, CSRF sur écritures, authentification et rate limiting ;
- validation stricte des entrées, symboles, chemins, uploads et webhooks ;
- sanitization des news et texte externe avant `innerHTML` ;
- CSP et en-têtes adaptés après inventaire des scripts inline ;
- dépendances bornées, lock reproductible, audit de vulnérabilités et licences ;
- permissions minimales GitHub/CI, actions pinées et artefacts contrôlés ;
- backups testés, restauration et migrations idempotentes ;
- aucun PII financier dans télémétrie, cache, prompt ou fixture publique.
- un mode privé lié hors loopback refuse de démarrer sans authentification ;
- un mode démo public est synthétique, non persistant et sans store partagé ;
- toutes les routes portefeuille/journal/IA utilisent `private, no-store` ;
- le consentement au partage IA est explicite, finalisé, révocable et désactivé
  par défaut ;
- les GET sont purs et les écritures exigent authentification, CSRF et méthode
  HTTP appropriée.

## Données déjà présentes

Remplacer dans l'arbre courant compte, holding, quantité, coût et P&L réels par
des fixtures synthétiques clairement marquées. Scanner aussi `tests/fixtures`.
Une réécriture d'historique Git ne fait jamais partie d'un nettoyage ordinaire :
produire l'inventaire, expliquer l'irréversibilité et obtenir une autorisation
destructive distincte. Elle ne garantit pas l'effacement des clones ou index.

## Skills et plugins externes

Traiter un skill comme du code exécutable. Avant adoption : lire tous ses
fichiers, hooks, commandes, MCP, permissions, dépendances, licence et réseau ;
épingler une version ou un SHA ; tester en environnement isolé ; documenter la
raison et le retrait. Ne jamais installer un marketplace complet pour une seule
méthode.

Les méthodes externes sont d'abord distillées dans les règles Vertex. Une
dépendance n'est ajoutée que si elle fournit une capacité mesurable impossible
à maintenir raisonnablement dans le dépôt.

## Revue

- analyse statique ciblée et revue sémantique du diff ;
- tests d'autorisation et de frontière IBKR ;
- scan secrets et dépendances ;
- fuzz/properties sur parsers et conversions financières sensibles ;
- revue des erreurs silencieuses dans le code touché ;
- aucune correction automatique massive sans lot, tests et revue.

Anthropic Code Review/Security Review et Trail of Bits peuvent inspirer la
méthode. GitHub Awesome Copilot, Semgrep, CodeQL, `pip-audit` et OpenSSF
Scorecard sont des candidats contrôlés, jamais un bundle automatique. Le
résultat doit rester vérifié par les tests et contrats Vertex.
