# SIGNAL OS · LOT 40 — LES NEUF ROUTES À IDENTIFIANT, MESURÉES

Branche : `agent/vertex-signal-os-v1` · SW **v233** (aucun octet servi touché)

La réserve n°2 de `SIGNAL-OS-38` §4 disait, depuis le lot 39, exactement ceci :
neuf règles GET portent un identifiant, aucun id valide n'existe dans le jeu de
démonstration, en inventer un rendrait un 404 qui ne prouve rien, et **les
remplir demande un jeu de données porteur d'identités**. Ce lot fabrique ce jeu.

Verdict : **9 routes sur 9 couvertes, aucune ne sert la charge**, témoin vivant.

---

## 1. Comment les identités sont fabriquées

La règle du lot 38 — *un instrument doit reproduire l'état que le produit peut
réellement atteindre* — commande tout, et deux fois.

**Le poison est déposé comme la production le dépose.** `news_state['items']`
reçoit le titre BRUT (c'est ce que fait la boucle d'actualités) ;
`scan_state['detail'][sym]['news']` reçoit la forme ASSAINIE (ce store a un
écrivain unique qui assainit avant de déposer). Le lot 38 avait accusé `/scan` à
tort en empoisonnant `detail` brut ; l'erreur n'est pas refaite dans l'autre sens.

**Les identités passent par les portes du produit**, jamais par un magasin
écrit à la main avec une forme devinée :

| identifiant | porte empruntée |
| --- | --- |
| `decision_id` | `GET /api/skyler/TSTQ` — cette route **gèle** la décision dans la mémoire |
| `group`/`key` | 25 décisions + un résultat chacune, puis la clé est **lue** dans `calibration_by_context` (jamais choisie d'avance) |
| `tracking_id` | `tracking.repository.create` — l'appel exact du gestionnaire POST |
| `position_id` | blob desk au schéma réel (`data.myTrades`, chaîne JSON, comme le navigateur pousse) |
| `chart_id` | pas un magasin : un **vocabulaire**, lu dans le gestionnaire |

La cellule de calibration a coûté deux passages : elle n'existe qu'à partir de
`MIN_CALIBRATION_SAMPLE` = 20 décisions **mesurées**, et « mesurée » ne veut pas
dire « avec un résultat » mais `horizons[H5|H20|H60].status == 'MESURE'` — la
forme du résultat est lue dans `_measured_class`, pas supposée.

---

## 2. Le témoin, et pourquoi il était indispensable ici plus qu'ailleurs

Ces neuf routes ne servent pas de texte externe **parce qu'elles n'en reçoivent
pas** (§3). Un balayage qui ne trouve rien là où il n'y a rien à trouver rend un
zéro parfaitement vide.

L'outil fabrique donc un défaut : un second suivi dont le champ libre `decision`
porte le balisage brut, puis exige de le voir ressortir. Mesuré :
`temoin : 1/4 marqueur(s) ressorti(s) ['<script>alert(1)']` — la chaîne
semis → magasin → route → détection est vivante. Sans ce marqueur, l'outil
**refuse de conclure** (code de sortie 2).

Le témoin dit aussi un fait à ne pas perdre : **`/api/tracking/<id>` sert ses
champs libres tels quels.** Ce n'est pas un défaut aujourd'hui — le moteur n'y
écrit qu'un verdict d'un vocabulaire fermé — mais c'est le point exact où un
futur champ nourri de texte externe fuirait.

---

## 3. Pourquoi le zéro est vrai : deux barrières, pas une

Le seul chemin par lequel un titre d'actualité pourrait atteindre ces routes est
la mémoire décisionnelle : `catalyst` est **gelé** dans le record immuable, et
le record est servi par `/api/skyler/memory/<decision_id>`. Deux barrières
indépendantes l'interdisent :

1. **La route assainit avant le moteur** — `analysis_api` passe
   `sanitize_news(detail['news'])` à `events.build`, jamais le brut.
2. **Le catalyseur ne retient que des événements DATÉS**, et `events.build` ne
   date jamais une actualité (`dte=None` — une news a une heure de publication,
   pas une échéance). Les seuls événements datés sont les résultats
   (`'Résultats %s' % sym`, symbole borné à 12 caractères) et la macro, dont les
   libellés sont **écrits en dur** dans `vertex/data/macro_calendar.py` — aucun
   réseau, aucune source externe.

L'une ou l'autre suffirait. Elles peuvent s'éroder séparément, donc elles sont
gardées séparément : `tests/test_signal_os_identites_lot40.py`, cinq tests, tous
vérifiés par mutation.

| mutation appliquée sur disque | ce qui tombe |
| --- | --- |
| `dte=None` → `dte=0` pour les news (`events.py`) | 2 tests (timeline **et** catalyseur) |
| `sanitize_news(...)` retiré de `/api/skyler/<sym>` | le test de la route |
| `os.environ` remonté au niveau du module de l'outil | le test d'innocuité à l'import |

---

## 4. Un défaut d'outillage nommé au passage

`/api/positions/<id>/changes` sortait d'abord en « pas de réponse ». Cause
mesurée : `opt_job` est **capturé dans la fermeture** du blueprint des positions
(`make_blueprint(..., opt_job=_opt_job)`), tandis que `neutraliser_le_worker`
remplace les liaisons de **module** par identité d'objet — une cellule de
fermeture lui échappe, et la route attendait le worker 45 s (`RequestTimeout`).

Correction : déclarer l'absence de courtier (`NO_IBKR=1`) **avant** le premier
import du produit — un état que la production atteint tous les jours (poste sans
TWS). Et, au passage, la cause des **3 routes « injoignables »** du balayage des
sorties de news, jusqu'ici constatées sans être expliquées.

Le rapport distingue désormais « HTTP 500 », « HTTP 404 » et « pas de réponse » :
les confondre, c'était perdre l'information la plus utile du lot.

---

## 5. Ce qui reste ouvert

1. **Le balayage complet n'est pas dans la suite.** Vingt-cinq passages du
   moteur Skyler prennent des minutes ; la suite tourne en 40 s. Ce sont les
   **barrières** qui sont gardées, pas le balayage — l'outil se lance à la main.
2. **`/api/skyler/memory/import` (POST) reste la porte non balayée** par laquelle
   du texte arbitraire entre dans la mémoire. Hors périmètre : consigne de
   session, et l'invariant READONLY interdit de balayer des POST à l'aveugle.
3. **Un seul jeu d'identités.** Une identité par famille, pas une combinatoire.
4. **Le champ libre du suivi est servi brut** (§2) — anchoré, pas corrigé :
   aucun texte externe ne l'alimente aujourd'hui.
