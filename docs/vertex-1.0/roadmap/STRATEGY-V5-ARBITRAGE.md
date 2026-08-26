# Stratégie V5 — arbitrage requis

Ce document ne change pas la doctrine active. Il isole les contradictions à
trancher avant de créer `vertex_strategy_v5.json`.

| Sujet | V4 active | Constitution utilisateur | Arbitrage proposé |
|---|---|---|---|
| delta option primaire | `DYNAMIC` 0,28–0,45 | LEAPS 0,70–0,90 | séparer tactique convexe et LEAPS conviction |
| risque option | perte planifiée 25–35 %, jusqu'à 50 % | asymétrie idéale autour de -10 % | définir risque de thèse, stop analytique et perte prime séparément |
| objectif | 35–100 % dynamique, 80–200 % LEAPS | +50 %, exceptionnel +100–300 % | scénarios non garantis, calibrés par cohorte |
| gestion gagnants | sécuriser 60–70 % dès +50 % | conserver à +50 %, revue +75 %, vendre 25–50 % à +100 % | backtester deux politiques avant activation |
| taille | max action 15 %, 3 options | S+ 10–15 %, S 7–10 %, A 3–5 %, B 1–2 % | conserver les plafonds mais ajouter budget de risque |
| concentration | 8–15 lignes | 8–15 lignes | aligné |
| renforcement | partiellement décrit | gagnants uniquement après confirmation | rendre le gate explicite |
| horizon | options 2/4/6 semaines, DTE 120–240 | options 2/4/6 semaines, parfois échéance 6 mois | aligné |

## Point essentiel

Une perte cible de -10 % sur une option longue peut être incompatible avec le
bruit normal de la prime, surtout pour une option à six mois. V5 doit distinguer :

- invalidation de la thèse sur le sous-jacent ;
- stop de risque portefeuille ;
- baisse temporaire de la prime ;
- perte maximale contractuelle au débit ;
- taille initiale permettant de survivre à la volatilité normale.

Fixer mécaniquement `stop option = -10 %` sans étude augmenterait le nombre de
sorties prématurées. Le bon objet à calibrer est la perte de portefeuille par
thèse, puis la trajectoire attendue de la prime selon spot, temps et IV.

## Expériences exigées

Comparer au minimum :

1. delta 0,30–0,45 vs 0,50–0,65 vs 0,70–0,90 ;
2. DTE 120/180/240 ;
3. sortie à invalidation sous-jacent vs stop prime fixe ;
4. sécurisation à +50 % vs +100 % ;
5. vente partielle 25/50/70 % ;
6. exposition identique en capital et identique en delta ;
7. régimes haussier, baissier, volatil et sans direction ;
8. avec et sans earnings dans la fenêtre ;
9. après spread et slippage réels ;
10. résultats par cohorte de liquidité.

V5 ne devient active que si elle améliore l'espérance après coûts sans dégrader
la perte extrême au-delà du budget accepté, et après validation humaine.
