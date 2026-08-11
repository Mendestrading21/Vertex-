# SKYLER LOT 406 — Sept clés synchronisées que rien n'écrit, et une promesse intenable sur `/portfolio`

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-406` (base : lot 405 fusionné,
1c18ac4)

Après trois lots négatifs (403, 404, 405), celui-ci trouve quelque chose — et
c'est visible par l'utilisateur.

**Aucun code, aucun gardien, aucun test.** Le défaut est de rang 1 : il demande
une décision, pas une correction d'agent.

## La question

Le contrat `DESK_KEYS` — règle critique n°1 de `CLAUDE.md` — liste **17 clés**
synchronisées entre le navigateur et `desk_data.json`. Question jamais posée :
**ces 17 clés sont-elles réellement produites par le client ?** Une clé listée que
rien n'écrit, c'est la synchronisation d'un fantôme.

## L'instrument s'est trompé une première fois

Ma première passe annonçait **13 clés sur 17 sans écrivain**, dont `myTrades` —
la clé des positions du trader. Absurde : c'était l'instrument.

J'avais exclu `vertex/static/vertex/js/vx-entities.js` du corpus parce qu'il
porte la **liste** `DESK_KEYS` — sans voir qu'il porte aussi **les écrivains**
(`set('myTrades', list)` et quinze autres). *Exclure un fichier pour ce qu'il
déclare, c'est se priver de ce qu'il fait.*

Corrigé : exclusion des **lignes** de déclaration, pas des fichiers. Témoin
négatif : une clé inventée (`myGhostXYZ406`) ne trouve aucun site.

## La mesure

```text
clés du contrat DESK_KEYS                              17
   avec au moins un site d'écriture en production      10
   SANS aucun site d'écriture                           7
```

Les sept : `myTradesEquity` · `myRecosClosed` · `myCapital` · `simCash` ·
`simStart` · `simTrades` · `simClosed`.

Vérification exhaustive des écritures littérales (`setItem('my…`, `setItem('sim…`,
`setItem('vx…`, `set('…')`) sur tout `vertex/**` et `terminal.py` : **aucune** ne
vise ces sept clés.

Et dans le blob desk **réel** :

```text
clés présentes dans desk_data.json : 6 / 17
   myTrades (2) · myTradesClosed (3) · myFavs (0) · vxJournal (0)
   vxAlerts (0) · vxWatchlist (1)
   → aucune des 7 clés sans écrivain n'est présente
clés du blob hors contrat : aucune
```

## Le défaut visible — `/portfolio`

Trois de ces clés sont **lues** par du code servi :

```text
portfolio_page.py:296   const cash = E().capital();        → myCapital,       jamais écrit
portfolio_page.py:586   const eq   = E().equity();         → myTradesEquity,  jamais écrit
portfolio_page.py:718   cash: E().capital() || 0;          → idem
```

`vx-entities.js` :
`capital() { return get('myCapital', null) … }` · `equity() { return get('myTradesEquity', []); }`

Conséquence sur la page servie : `eq` vaut **toujours** `[]`, donc la branche
`if (eq.length >= 2 …)` est **inatteignable** — la **courbe d'équité** et le
**drawdown** ne peuvent jamais s'afficher. Et `cash` vaut toujours `null` / `0`.

**Le problème n'est pas la carte vide — c'est ce qu'elle promet** :

> *« Courbe d'équité indisponible — elle se construit au fil des clôtures de
> positions déclarées. »*

Or clôturer une position exécute `set('myTrades', list); set('myTradesClosed',
closed);` (`vx-entities.js:171`) — **jamais** `myTradesEquity`. Le trader peut
déclarer autant de clôtures qu'il veut : la courbe n'apparaîtra pas. **L'état
vide donne une consigne qui ne peut pas aboutir.**

Ce n'est pas un chiffre inventé, donc pas une violation de l'invariant n°4 au
sens strict ; c'est son cousin : **une promesse que le code ne peut pas tenir**.

## L'« évidence » à ne surtout pas faire

La conclusion apparente serait : « sept clés mortes, on élague `DESK_KEYS` de 17
à 10 ». **Ce serait une perte de données, pas un nettoyage.**

Le mécanisme est celui du lot 362 : le push desk est **last-writer-wins total** —
le blob serveur est remplacé par les clés présentes dans la liste. Un profil de
navigateur plus ancien qui détiendrait encore `simCash`, `simTrades` ou
`simClosed` (l'ère du simulateur, cf. les fichiers `paper_bot` retirés) verrait
ces clés **cesser d'être synchronisées, puis disparaître du serveur** au premier
push suivant.

Le blob mesuré aujourd'hui ne les contient pas — mais il ne prouve rien sur les
autres profils, et il n'y a pas de retour en arrière.

## Ce qui est proposé, et pour qui

**Dossier de rang 1** — deux volets indépendants, aucun engagé :

1. **La promesse de `/portfolio`.** Deux issues honnêtes : soit alimenter
   `myTradesEquity` à la clôture (le comportement que le texte promet), soit
   réécrire l'état vide pour dire ce qui est vrai. La première est un ajout de
   fonctionnalité, la seconde une correction de texte servi — **les deux
   touchent un octet servi** (bump SW, MD5, gardiens). C'est une décision.
2. **Les 7 clés.** Recommandation : **les garder**. Le coût de les conserver est
   nul (le push n'envoie que les clés réellement présentes) ; le coût de les
   retirer est un risque de perte irréversible.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve
  MD5 requise, pas de bump. SW : `td-shell-v187`.
- `desk_data.json` **lu seulement**, jamais écrit. Snapshot des 22 fichiers
  runtime avec contrôle d'apparition ; la suite a ré-horodaté les trois fichiers
  habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

La recherche d'écrivains porte sur les **écritures littérales** dans le dépôt.
Une écriture par clé variable (`set(k, v)` dans une boucle) ne serait pas
attribuée — j'ai vérifié les 53 sites `set(<variable>, …)` du dépôt : aucun ne
concerne le magasin desk. Et « présente dans le blob » est une observation sur
**un** profil, celui de cette machine : elle ne dit rien des autres navigateurs
du trader — c'est précisément pourquoi l'élagage est déconseillé.

## Où en est la boucle

Onzième lot court, onzième point de contrôle distinct — et le premier depuis le
402 à trouver un défaut **visible par l'utilisateur**. Il rejoint les dossiers de
rang 1, qui attendent tous la même chose.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388.
