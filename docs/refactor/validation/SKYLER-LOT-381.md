# SKYLER LOT 381 — Les gardiens des clés de sync gardaient les mauvaises listes

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-381` (base : lot 380 fusionné,
af1b056) · **Ouverture de la tranche 380-389.**

## Piste

Décidée au bilan 380 : auditer **les gardiens eux-mêmes** par mutation. 291
fichiers de test, **2 756 tests** dont personne n'avait vérifié qu'ils voient ce
qu'ils prétendent voir. Cibles choisies : ceux que `CLAUDE.md` nomme comme
protégeant les règles critiques.

Protocole : muter le code protégé, puis lancer **toute la suite** — la question
n'est pas « ce gardien-ci mord-il ? » mais « **un** gardien mord-il ? ». C'est la
seule façon de mesurer une couverture plutôt qu'une intention.

## Résultat

```text
clé renommée dans DESK_KEYS de vx_kit (référence)          MORD
version du service worker rétrogradée                      MORD
vocabulaire des verdicts vidé (window.__VXVOCAB)           MORD
READONLY basculé à False                                   MORD
clé vxAlerts retirée du repli deskKeys() de system_page    AUCUN GARDIEN ⚠
```

**Les invariants lourds sont réellement tenus** — READONLY, service worker,
vocabulaire, source de comparaison des clés. C'est rassurant et ce n'était pas
acquis.

**Un trou, et il est sur la règle critique n°1**, celle dont `CLAUDE.md` dit
« sinon un push l'efface côté serveur » : retirer `vxAlerts` du repli **servi**
de `/system` passe **les 2 754 tests**.

## Ce que l'audit a révélé de plus grave

En cherchant *pourquoi* rien ne mordait, j'ai mesuré quelles listes sont
réellement servies. Le tableau ne correspond pas à la documentation :

| liste | servie ? | gardée ? |
|-------|----------|----------|
| `vertex/static/vertex/js/vx-entities.js` (32 464 o, HTTP 200) | **oui** | oui |
| `system_page.py::deskKeys()` (inline dans `/system`) | **oui** | **NON** |
| `vx_kit.py` DESK_KEYS — dite « source de vérité » | **non — 0/8 pages** | oui |
| `journal.py` | non (page morte) | oui |

`vx_kit.JS` pèse **21 727 octets** et **n'apparaît sur aucune des huit pages** —
mesuré page par page. Or `CLAUDE.md` le décrivait comme « kit global **présent
sur toutes les pages** », et les deux gardiens nommés s'y ancrent comme
référence.

La chaîne fonctionne encore : `vx-entities.js` est comparé à `vx_kit`, donc les
deux restent synchronisés. Mais elle est **ancrée sur un module qui n'atteint
plus le navigateur** — et `vx_kit` figure parmi les candidats de purge. Le jour
où il disparaît, la référence s'en va, tandis que la seule liste servie non
gardée continue de vivre.

**Sur deux listes réellement servies, une seule était protégée.**

## Trois fausses pistes en chemin — l'outil, encore

1. `.replace(…, 1)` a frappé `jget('vxAlerts',…)` ligne 105 au lieu de
   `DESK_KEYS` ligne 259 : « la source de vérité n'est pas gardée » était **faux**.
2. Même erreur sur la mutation d'apostrophe.
3. La mutation d'apostrophe visait de surcroît un bloc de `vx_kit.JS` **servi
   nulle part** — le balayage JS avait raison de ne pas mordre.

Trois fois où j'aurais accusé un gardien sain, dans un lot dont le sujet est
précisément « les gardiens mentent-ils ? ». Le lot 379 l'avait formulé : *un cas
qui ne mord pas accuse d'abord la mutation.* La passe corrigée exige désormais
une **ancre unique** et vérifie que la ligne visée a bien changé.

## Ce que le lot livre

**Un gardien** — `tests/test_desk_keys_servies_lot381.py` (13 tests) — qui garde
les listes **par ce qu'elles servent**, pas par ce que la documentation croit :

- le repli de `/system` porte le contrat complet (17 clés) et **n'en invente
  aucune** — une clé en trop créerait une donnée fantôme dans le blob ;
- `vx-entities.js` vérifié **tel qu'il est servi** (les gardiens existants le
  lisent sur disque) ;
- les 8 pages chargent bien ce fichier — sinon elles retombent sur le repli ;
- **les deux listes servies sont identiques**, quelle que soit celle que le
  navigateur utilise ;
- le fait qui a motivé le lot est **ancré** : si `vx_kit` redevient servi, le
  test le dit et réclame l'extension du périmètre.

**Une correction de documentation** — règle n°1 de `CLAUDE.md`, qui décrivait
trois listes servies dont deux ne le sont pas. Elle nomme désormais les **deux**
listes réellement servies, signale que `vx_kit` sert d'ancre de comparaison sans
atteindre le navigateur, et pointe le nouveau gardien.

### Preuve ROUGE

```text
ROUGE OK  clé retirée du repli servi de /system       | restauration identique
ROUGE OK  clé inventée dans le repli servi            | restauration identique
ROUGE OK  clé retirée du fichier statique servi       | restauration identique
ROUGE OK  les pages cessent de charger vx-entities.js | restauration identique
après restauration : 13 passed
```

Les quatre fautes passaient **toutes** les 2 754 tests avant ce lot. Un cas a
d'abord été **sauté** (espaces après les virgules dans `vx-entities.js`, absents
de mon motif) — signalé puis corrigé.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 380, af1b056) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché.** `CLAUDE.md` est de la documentation, non
  servie : aucun octet servi ne change, pas de preuve MD5 requise, pas de bump.
- Suite : **2754 → 2767 passed / 2 skipped** — verte (+13).
- SW : `td-shell-v187`.

## Portée — ce que ce lot ne prétend pas

Sept mutations sur 2 756 tests : c'est un **sondage**, pas une couverture. Les
gardiens non ciblés restent non vérifiés, et « MORD » signifie « attrape CETTE
faute-là », pas « couvre tout ». Je n'ai pas non plus vérifié si `vx_kit` est
servi ailleurs que sur les 8 pages produit (routes héritées, fragments) — le
gardien ancre le fait sur ces 8 pages seulement.

Note relevée en passant, non traitée : le commentaire en tête de `vx-entities.js`
dit « MIROIR EXACT de `__DESK_KEYS` (terminal.py) », alors que la purge É1 a
retiré toute liste de terminal.py. Référence périmée, sans effet fonctionnel.

## Suite

LOT 382 : poursuivre l'audit des gardiens par mutation — la première passe a
trouvé un trou sur la règle la plus dangereuse en sept sondages. Cibles
suivantes suggérées : sorties XSS assainies (`test_xss_exits_lot177`), chaîne de
sauvegarde desk (`test_desk_backup_lot178`), tokens et littéraux de couleur,
`data_quality` / étiquetage démo. Prochaine échéance périodique : **~lot 390**.
