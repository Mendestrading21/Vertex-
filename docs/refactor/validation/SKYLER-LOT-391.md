# SKYLER LOT 391 — Un scan de démo écrit dans l'historique breadth réel, et servi

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-391` (base : lot 390 fusionné,
10768f9)

## Piste

Observation non engagée du lot 390 : lancer le serveur DEMO modifie ~8 fichiers
runtime. La question laissée ouverte était la bonne — **ces valeurs de démo
sont-elles ensuite servies comme réelles ?**

## Ce que les données disaient avant toute manipulation

`breadth_history.json` portait **16 points strictement identiques** —
`a50 50 · a200 45 · net −4 · health 37` — du 2026-07-21 au 2026-08-08, un par
jour. La participation réelle d'un marché ne reste pas figée seize séances de
suite. **C'est la signature exacte de la pollution GEX du lot 388**, sur un autre
fichier.

## Le lien causal, prouvé

```text
avant scan DEMO : 16 points, dernier {"d": "2026-08-08", "a50": 50, "a200": 45, "net": -4, "health": 37}
après scan DEMO : 17 points, dernier {"d": "2026-08-09", "a50": 50, "a200": 45, "net": -4, "health": 37}
dates ajoutées  : ['2026-08-09']
```

Le site d'écriture (`terminal.py`, section « BAROMÈTRE / INTERNALS ») est
**inconditionnel** — aucun test de `DEMO_MODE`. Et il ne fait pas qu'ajouter :

```python
if _bh and _bh[-1].get('d') == _today:
    _bh[-1] = _snap          # ← ÉCRASE le point du jour
```

Un scan de démo lancé après un scan réel **remplace la mesure du jour**.

## Pourquoi c'est un enjeu d'honnêteté

`internals['history']` part dans `/scan` — **17 points servis, mesuré** — et
`markets_page.py` le consomme pour « Tendance de participation ». Le commentaire
du code dit lui-même « historique breadth **RÉEL** ».

Pendant une session de démo, l'utilisateur est prévenu : `/markets` sert un
`vx-demo-banner` et `/scan` expose `source = 'demo'`. **Mais le point persisté ne
porte aucune provenance** — `{d, a50, a200, net, health}`. Lors d'une session
**réelle** ultérieure, sans bannière et avec une source réelle, les points de
démo sont servis au milieu des vrais, indistinguables.

Le contre-exemple est dans le dépôt : `market_context_last.json` **est** écrit
avec un champ `demo` (`_mcx.build(..., demo=_demo)`). Le mécanisme honnête
existe ; il n'est pas appliqué à l'historique breadth.

## Ce que ce lot ne fait pas — et pourquoi

**Aucun fichier de production n'est modifié.**

Ajouter un garde `DEMO_MODE` autour de la persistance serait une **décision de
conception**, pas la réparation d'une incohérence : mesuré, **aucune persistance
du dépôt ne garde ce mode**. Trois issues sont défendables — ne pas persister en
démo · marquer le point et l'afficher comme tel · assumer que la démo peuple
l'historique. Ce choix appartient à l'utilisateur ; le dossier part au **rang 1**
du classement du lot 390.

La purge des 16 points déjà accumulés relève de la même décision. Donnée runtime,
non supprimée d'office.

## Une part de cette pollution vient de la boucle elle-même

Les vérifications de tranche de l'agent lancent le serveur DEMO ; les points
antérieurs en portent la trace. **Le rituel de copie de sûreté et de restauration
adopté aux lots 388-390 a arrêté cette contribution** — le point du 2026-08-09
créé par la mesure de ce lot a été restauré à l'octet, `breadth_history` est
revenu à 16 points.

Ce qui demeure n'en dépend pas : dès que l'utilisateur lance une démo, le même
mécanisme opère.

## Gardien

`tests/test_persistance_demo_lot391.py` (7 tests). Il verrouille **les mécanismes
de distinction qui existent**, jamais le défaut — un gardien qui figerait
l'absence de marqueur accuserait la correction future (leçon du lot 383) :

- **anti-vide** : le site de persistance existe (exactement 1) et l'historique
  atteint bien `/markets` — sans quoi tout le reste serait sans objet ;
- `market_context_last` reste écrit **avec sa provenance** — c'est le
  contre-exemple honnête, et le modèle d'une correction éventuelle ;
- `/scan` continue de marquer `source = 'demo'` ;
- `/markets` et `/` gardent leur `vx-demo-banner` ;
- les **champs de mesure** du point persisté sont figés — pas l'absence de
  provenance.

### Preuve ROUGE

```text
persistance de l'historique breadth retirée            ROUGE OK
/markets ne consomme plus l'historique                 ROUGE OK
provenance du contexte marché neutralisée              ROUGE OK
le scan ne marque plus sa source démo                  ROUGE OK
bannière de démo retirée de /markets                   ROUGE OK
champ de mesure renommé dans le point persisté         ROUGE OK
[témoin] marqueur de provenance AJOUTÉ                 ne mord pas — correct
après restauration : 7 passed
```

**Le témoin est le test le plus important du lot** : il simule *la correction
future* — ajouter `'demo': DEMO_MODE` au point persisté — et vérifie que le
gardien **ne s'y oppose pas**. C'était l'objectif de conception.

Une ancre a dû être corrigée : `vx-demo-banner` apparaît **4 fois** dans
`markets_page.py`, la mutation devait donc être globale pour que la bannière
disparaisse réellement. Compter les occurrences avant de muter, encore.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- Arbre propre ; **aucun fichier de production touché** — pas de preuve MD5
  requise, pas de bump.
- Copies de sûreté des 21 fichiers runtime avant toute sonde. Serveur DEMO lancé
  puis **arrêté** (port 5002 fermé, aucun processus Python vivant) ; état runtime
  **restauré à l'identique**, écart final : aucun.
- Suite : **2835 → 2842 passed / 2 skipped** (+7). SW : `td-shell-v187`.

## Portée

Le gardien est **statique**. Il ne mesure pas les écritures à l'exécution : c'est
la sonde de ce lot qui l'a fait, une fois. Et le verdict « servi comme réel » vaut
pour la chaîne mesurée aujourd'hui (`/scan` → `internals.history` → « Tendance de
participation ») ; les autres caches touchés par un scan de démo — `daily_prev`,
`skyler_memory` — **n'ont pas été analysés**. Ce lot traite le cas le plus grave,
pas la famille entière.

## Suite

**Ne pas enchaîner** sur les autres caches sans décision : la question est la même
et elle est posée. Le lot 392 reprendra les pistes fines (refus construits en
variable 377 · formes imbriquées des promesses de retour 375 · trois sites de
concaténation à constantes 374), à moins qu'un GO n'arrive.

Prochaine échéance périodique : bilan n°9 **~lot 400**.
