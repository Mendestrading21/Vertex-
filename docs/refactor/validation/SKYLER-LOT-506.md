# SKYLER LOT 506 — `/portfolio` calcule le risque affiché sur un capital de ZÉRO, en permanence : `myCapital` est dans le contrat de synchronisation mais **aucune ligne du dépôt ne l'écrit**. Sur un portefeuille concentré, la page peint « Concentration très élevée (HHI 1.000) » et « Pire scénario : −15,0 % » — deux alertes qui disparaissent dès qu'on renseigne du cash

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-506` (base : lot 505 fusionné,
`d5eb27db`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** et `/system`, comme recommandé — précisément la **règle critique n°1** de
`CLAUDE.md`, les clés de synchronisation, « la seule où un défaut peut coûter des
données ». Le gardien `test_desk_keys_servies_lot381.py` couvre déjà la
comparaison **liste à liste** et **liste à contrat**. Reproduire cela n'aurait
rien prouvé (règle 503-A). J'ai donc pris ce qu'il **exclut** :

> les listes servies correspondent-elles aux **écritures réelles** ?

Ce chemin a mené ailleurs que prévu, sur `/portfolio`. Je raconte le trajet parce
que c'est lui qui a produit le dossier.

## La réponse

```text
LA CHAÎNE, établie sur pièces
  vx-entities.js:235   capital() { const c = get('myCapital', null);
                                   return c === null ? null : Number(c); }
  myCapital            AUCUN ÉCRIVAIN DANS TOUT LE DÉPÔT — la clé n'apparaît que
                       dans les 4 listes DESK_KEYS et dans cet accesseur.
                       Aucune interface ne permet de saisir un capital.
  portfolio_page.py:718   cash: E().capital() || 0        →  0, TOUJOURS
  POST /api/portfolio/team  cash = float(body.get('cash') or 0)
                       → PortfolioSnapshot(positions, cash=0, provenance='REAL')
  la réponse peint « Risques priorisés » : HHI, bêta, garde-fous, stress
```

Mesuré en appelant les moteurs en processus, positions **fabriquées en mémoire** :

```text
       cash        HHI     bêta    pire stress
          0      0.279     1.05        -10.46 %
      5 000      0.234        ·         -9.15 %
     25 000      0.130        ·         -6.82 %
    100 000      0.034     0.37         -3.49 %
    250 000      0.009        ·         -1.77 %
```

**Le zéro n'est pas neutre : c'est l'hypothèse la plus alarmiste possible**
— cent pour cent investi, concentration maximale, bêta maximal, stress maximal.

## Et les phrases basculent — pas seulement les nombres

Les trois messages de la carte sont **à seuil** (`HHI >= 0.66`, `bêta >= 1.3`,
`pire <= -15 %`). Un nombre faux n'est donc visible que s'il franchit un seuil.
**Il le franchit** :

```text
portefeuille   cash                HHI   « Concentration    pire      « Pire
                                          très élevée »              scénario »
1 ligne           0              1.000        AFFICHÉ      -15.00 %   AFFICHÉ
1 ligne    30 % de la valeur      0.592           —        -11.54 %      —
2 lignes          0              0.504           —         -15.00 %   AFFICHÉ
2 lignes   30 % de la valeur      0.298           —        -11.54 %      —
```

Sur un portefeuille concentré, la page affiche à un utilisateur qui détient du
cash **deux risques « importants » qui sont des artefacts du capital qu'il n'a
jamais pu saisir.**

Sur un portefeuille diversifié (3 lignes et plus), les nombres restent faux mais
**aucun seuil n'est franchi** : la visibilité est **conditionnelle** (leçon 497),
et je le dis plutôt que de laisser entendre que tout le monde voit l'alerte.

## Le second contrôle — il a fait tomber DEUX de mes propres résultats

### 1. Un contrôle négatif VACUEUX, et sa réparation me contredit

J'avais écrit : « le bêta ne bouge pas avec le cash, comme mon modèle le
prédit ». **C'était un faux réconfort** : mes positions de banc ne portaient pas
de bêta, donc je comparais `None` à `None`. Un contrôle qui compare deux absences
ne teste rien.

Refait avec des bêtas fournis :

```text
bêta à cash=0       1.05
bêta à cash=100 000 0.37     → IL BOUGE. Mon modèle mental était FAUX.
```

Le bêta est pondéré sur la valeur **totale**, cash compris. Donc le troisième
message à seuil est lui aussi calculé sur l'hypothèse zéro-cash. **Ma correction
agrandit le défaut au lieu de le réduire** — raison de plus pour la publier.

### 2. J'allais accuser deux clés à tort

Le premier banc a trouvé **six clés écrites hors des deux listes servies** :
`vxDashboardLayout`, `vxNotificationPrefs`, `vxSidebarState`, `vxRecentTickers`
(préférences d'interface), et surtout `vxTodayBaseline`, `vxPortfolioBaseline`.
J'allais classer ces deux dernières en perte de données — ce sont des
**historiques**, absents de `desk_data.json` et de toute sauvegarde.

**Lecture faite : ce n'est pas un défaut.** Les deux sont explicitement libellées
« Depuis ta dernière visite », documentées « baseline locale », et leur état vide
est honnête : « Aucun historique de comparaison disponible — la référence se pose
à cette visite ». Une clé non synchronisée **suivie d'un repli qui marche** n'est
pas un défaut (leçons 499, 501). **Accusation retirée.**

### 3. Un zéro produit par mon propre banc

Mon détecteur de sous-vues a rendu « `/system` : 0 sous-vue ». **Faux** : il
cherchait `_VIEWS` alors que `system_page` expose `VIEWS`. `/system` en a
**cinq**. Le brief du réveil, lui, en annonçait « au moins une (`connections`) » —
**il se trompait aussi**, et dans l'autre sens.

**Arrêtés avant publication : 83 → 86.**

## Le sens inverse, cherché (règle 504)

Le défaut **sur-alerte** : il ne peut pas sous-estimer le risque pour un
utilisateur sans `myCapital`, puisque `null || 0` ne produit que zéro. Mais il y a
bien un cas inverse, et il est structurel : **un utilisateur dont un ancien blob
porte un `myCapital` hérité verra cette valeur figée à jamais** — aucune interface
ne peut la corriger, et elle ne peut donc que se périmer. Sur-alerte pour les uns,
valeur gelée pour les autres.

## Ce que la mesure a trouvé d'autre — et qui ne mérite pas un dossier

**Cinq des dix-sept clés synchronisées ne sont NI écrites NI lues** dans les
octets servis : `myRecosClosed`, `simCash`, `simClosed`, `simStart`, `simTrades`.
Elles sont transportées à chaque push, restaurées à chaque pull, présentes dans
`desk_data.json` et dans tous les `desk_backup_*`. **C'est du poids mort, pas un
défaut** : rien de faux n'est affiché. Je l'ancre comme fait, sans le classer.

`myCapital` et `myTradesEquity`, elles, sont **lues** — et c'est `myCapital` qui a
ouvert le dossier.

## Sous-produit : la couverture des empreintes de la boucle est très partielle

Le 505 avait montré que `/journal` sert cinq vues et que la boucle n'en empreinte
qu'une. Le fait est **général** :

```text
page             sous-vues servies   empreintées par la boucle
/journal                  5                  1
/portfolio                6                  1   (team ; risk = 4c3e254d476d)
/markets                  5                  1
/options                  6                  1
/system                   5                  1
/ · /opportunities · /analysis   1 chacune    3
─────────────────────────────────────────────────────────
TOTAL                    30                  8
```

**Vingt-deux vues servies ne sont dans aucune empreinte de la boucle.** Le
« MD5 8/8 » que je publie à chaque lot est exact, mais il couvre **huit
trentièmes** des vues servies — et il faut le dire ainsi désormais.

Empreintes relevées ici : `/portfolio?view=positions` `f865bcc0e657` ·
`performance` `ca4f80dfb445` · `risk` `4c3e254d476d` · `options` `3845674a9934` ·
`watchlist` `d64daf73055e` · `/markets?view=macro` `0a8fa6db73de` · `sectors`
`fac1ef8cec54` · `breadth` `0aff8be05045` · `volatility` `0f09bf629ee6` ·
`/options?view=positioning` `b2c90ae64496` · `leaps` `cf40e418bcd7` ·
`positions` `7068e323850a` · `volatility` `c7d5d574d2f8` · `events`
`fb54164b7ffa` · `/system?view=data` `11af6d5fe3c6` · `automations`
`b38f811ee10e` · `settings` `93fa965e5ba8` · `archive` `85cc48db3d27`.

## Aucun gardien

Un seul test touche au cash de cette route : `tests/test_strategy_os_routes.py:73`
poste `{'cash': 5000, 'simulated': True}` — un instantané **simulé**, avec un cash
**non nul**. **Le chemin réel — `simulated:false`, `cash:0` — n'est couvert par
rien**, et aucun test ne vérifie qu'une clé du contrat DESK_KEYS possède un
écrivain.

## DOSSIER 506-A — Classement

**Rang 2, et je dis pourquoi ni plus ni moins.**

Pour le **rang 1** : le chiffre est peint, il est faux pour tout utilisateur sans
donnée héritée, la cause est **structurelle et permanente** (une clé du contrat
sans aucun écrivain), et elle touche trois messages de risque à la fois.

Ce qui l'en empêche :

1. **Ce n'est pas la vue par défaut** — il faut ouvrir `/portfolio?view=risk`,
   comme au 505.
2. **Le défaut SUR-alerte.** L'étalon est le **478** (« le produit sur-alerte au
   lieu de rassurer », rang 2). Une fausse alarme est moins coûteuse qu'une fausse
   quiétude sur un outil de décision — c'est le critère qui sépare le 461 du 432.
3. **Visibilité conditionnelle** : sur un portefeuille diversifié, aucun seuil
   n'est franchi.

Ce qui l'empêche d'être **rang 3** : ce n'est pas du poids mort. C'est peint, ça
concerne le risque, et la cause ne peut pas se résorber seule.

Correction pressentie, non engagée : distinguer `null` de `0` jusqu'au moteur
(`cash: capital()` sans `|| 0`, et un `cash` absent traité comme **inconnu**
plutôt que comme zéro) ; afficher « capital non renseigné » à côté des risques
qui en dépendent ; et **soit** offrir une saisie du capital, **soit** retirer
`myCapital` du contrat de synchronisation. **Aucun GO, rien n'est engagé.**

## Portée — ce que ce lot NE dit PAS

- **`desk_data.json` n'a pas été ouvert.** Je ne sais pas si l'utilisateur porte
  un `myCapital` hérité. Je montre ce que le **code** produit.
- **Je n'ai pas appelé `POST /api/portfolio/team`.** J'ai appelé les moteurs
  (`risk_engine`, `portfolio_guard`, `stress_tests`) en processus, avec la même
  construction de `PortfolioSnapshot` que le handler. C'est une reconstitution
  fidèle du chemin, pas le chemin lui-même.
- Les positions et les niveaux de cash sont **fabriqués**. Les seuils, eux, sont
  lus dans les octets servis.
- **Aucun navigateur ouvert.**
- Le régime d'écritures ne voit que les clés **littérales** ; les trois
  identifiants variables relevés (`k`, `key` dans `vx-entities.js`, `t` dans
  `chart.umd.min.js` minifié) se résolvent aux clés listées ou au code
  vendeur — mais mon inventaire reste une **borne**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les quatre scripts.
  Aucune route réseau sortante ; **aucun POST**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Troisième lot d'affilée dans le produit, troisième dossier. Mais celui-ci est
différent des deux précédents : **je n'ai pas trouvé ce que je cherchais.** Je
partais auditer les clés de synchronisation de `/system` ; le défaut est sur
`/portfolio`, et c'est la question « quelles clés sont écrites ? » qui y a mené
par un chemin que je n'avais pas prévu — une clé du contrat **sans aucun
écrivain**.

Et le second contrôle a encore fait son travail, deux fois contre moi : il a
retiré une accusation (les baselines) et **réfuté mon modèle du bêta**, ce qui a
agrandi le défaut. Un contrôle qui ne peut que confirmer n'est pas un contrôle —
celui du bêta, dans sa première version, comparait `None` à `None` et je l'avais
noté « passé ».

Feuille : **29 dossiers · seize rang 1 · onze rang 2 · trois rang 3**.
Dettes nommées restantes : **`/markets` et `/options`** (jamais auditées) ; **les
trois sous-vues de `/journal`** ; **les vingt-deux vues servies hors empreinte** ;
**l'espion au troisième niveau** (toujours déconseillé) ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 86 (+3)** ; publiés
puis corrigés **12** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
