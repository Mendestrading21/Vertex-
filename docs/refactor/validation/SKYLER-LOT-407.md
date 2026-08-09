# SKYLER LOT 407 — Le `|| 0` qui fabrique une alerte de concentration

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-407` (base : lot 406 fusionné,
1b2f1b8)

Le lot 406 a montré que `myCapital` et `myTradesEquity` ne sont écrits nulle
part. Il n'avait regardé qu'une conséquence : la courbe d'équité qui ne
s'affiche jamais. **Ce lot suit la seconde — et elle est plus grave.**

**Aucun code, aucun gardien, aucun test.** Dossier de rang 1.

## D'abord, borner : y a-t-il d'autres accesseurs orphelins ?

```text
vx-entities.js — clés LUES par un accesseur      11
                 clés ÉCRITES                     9
                 LUES mais JAMAIS écrites          2   → myCapital, myTradesEquity
```

**Exactement deux, pas une de plus.** Et sur les 8 pages servies, un seul module
les consomme : `portfolio_page.py` (L296, L586, L718). Le périmètre du dossier
406 est donc **confirmé et clos** : 2 accesseurs, 1 page.

## La conséquence que le 406 n'avait pas suivie

```javascript
portfolio_page.py:718   cash: E().capital() || 0,  simulated: false
```

`E().capital()` vaut **toujours `null`** — rien n'écrit `myCapital`. Le `|| 0`
convertit donc silencieusement **une donnée absente en un zéro**, envoyé à
`/api/portfolio/team` avec `simulated: false`, c'est-à-dire **déclaré réel**
(`provenance='REAL'`, `strategy_os_api.py` L136-138).

Trois lignes plus haut, le fichier écrit lui-même la règle qu'il enfreint :

```javascript
portfolio_page.py:727
/* … « Manquant/insuffisant » n'est jamais présenté comme zéro. */
```

## Ce que ce zéro change, mesuré

Moteur exécuté deux fois sur les **mêmes positions**, `cash = 0` (ce qui part
réellement) contre `cash = 50 000` (un solde réel) :

```text
mesure          cash = 0        cash = 50 000    verdict
equity          4 100           54 100           DIFFÈRE
hhi             0.5003          0.0029           DIFFÈRE  (×170)
issue_gardien   True            False            DIFFÈRE
```

`hhi` est calculé sur l'équité **cash compris** : envoyer 0 gonfle la
concentration de deux ordres de grandeur. Et la page **affiche** ce chiffre :

```javascript
if (risk.hhi != null && risk.hhi >= 0.66)
    importants.push('Concentration très élevée (HHI ' + risk.hhi + ')');
```

Le seuil est-il franchi en pratique ? Mesuré :

```text
1 position     HHI cash=0  1.0      → ALERTE        | cash=50k  0.0015  → pas d'alerte   ★ ALERTE FABRIQUÉE
2 positions    HHI cash=0  0.5003   → pas d'alerte  | cash=50k  0.0029  → pas d'alerte
4 positions    HHI cash=0  0.3019   → pas d'alerte  | cash=50k  0.0073  → pas d'alerte
```

**Avec une seule position déclarée, le terminal affiche « Concentration très
élevée (HHI 1) » dans les risques importants — alors que le portefeuille réel
peut être très peu concentré.** L'alerte n'est pas une lecture du portefeuille :
c'est un artefact du `|| 0`.

Le blob desk actuel porte **2 positions**, donc l'alerte n'est pas déclenchée
aujourd'hui sur ce profil. Mais **le HHI affiché reste faux d'un facteur ~170**,
et il est servi comme une mesure réelle.

## Une conséquence qui, elle, n'atteint pas l'écran

`team_view` conclut **toujours** « pas de gardien (cash/monétaire) — réserve
d'opportunité absente » (`ROLE_TARGETS[GOALKEEPER] = (1, 1)` et `if
snapshot.cash > 0` jamais vrai). Mais la page **ne consomme pas** `d.team` — le
mot `team` n'y désigne que le nom de la vue « Synthèse ». Vérifié : cette
conclusion fausse est calculée, **pas affichée**. Je le dis plutôt que de
grossir le dossier.

## Ce qui est proposé — et ce que je ne fais pas

**Aucune correction n'est engagée** : les trois issues touchent un octet servi
ou un moteur, donc une décision.

1. **Ne pas envoyer un zéro pour une absence.** L'API accepte `cash` optionnel
   (`float(body.get('cash') or 0)`) — il faudrait un chemin « cash inconnu » qui
   n'entre pas dans le dénominateur du HHI, plutôt qu'un 0 déclaré réel.
2. **Ou alimenter `myCapital`** : un champ « capital / liquidités » dans le desk.
   C'est la même décision que le volet 1 du dossier 406 (`myTradesEquity`), et
   elle réglerait les deux d'un coup.
3. **Ou, a minima**, ne pas afficher le HHI ni son alerte quand le cash est
   inconnu — l'état honnête existe déjà partout ailleurs dans cette page.

**Recommandation : l'option 2.** Elle transforme deux accesseurs orphelins en
données réelles et supprime la cause commune, au lieu de traiter deux symptômes.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Les moteurs ont
  été exécutés en mémoire, sans serveur. Pas de preuve MD5 requise, pas de bump.
  SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Les chiffres proviennent d'une exécution directe de `risk_engine` et
`stress_tests` sur des positions fabriquées pour la mesure — c'est la **méthode**
qui est démontrée, pas le portefeuille du trader. `beta` et `pire_stress`
ressortent `None` faute de bêtas et de séries dans cette entrée : leur
sensibilité au cash **n'a pas été mesurée** et n'est pas affirmée.

## Où en est la boucle

Douzième lot court. Deux lots de suite (406, 407) ont trouvé un défaut visible,
et ils partagent **une seule cause** : deux clés du contrat de synchronisation
que le produit lit sans jamais les écrire.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388.
