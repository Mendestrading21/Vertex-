# SKYLER LOT 392 — Les refus construits en variable : l'angle mort du 377, mesuré

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-392` (base : lot 391 fusionné,
9f013b3)

## Piste

Le lot 377 avait prouvé « **39 refus, 39 motivés, 0 muet** » — mais son détecteur
déballe `jsonify(...)` puis exige un dict **littéral**. Une réponse assemblée
dans une variable (`out = {}` … `out['ok'] = False` … `return jsonify(out), 400`)
lui est invisible. Il le déclarait ; ce lot le mesure.

## Le dénominateur, resserré par la mesure

```text
retours déballés donnant un dict LITTÉRAL (périmètre du 377)   417
retours déballés donnant une VARIABLE  (angle mort)            393
   dont dans une fonction de ROUTE                              34
   dont enveloppés (jsonify/tuple) → réellement SERVIS           31
   soit                                                          30 routes distinctes
```

Le volume brut de l'angle mort (393) est du même ordre que le périmètre couvert
(417) — le premier chiffre impressionne, mais **359 de ces retours sont des aides
internes**, pas des réponses d'API. La surface qui compte est de **30 routes**.
Un dénominateur non trié aurait fait croire à un trou deux fois plus grand qu'il
n'est.

## Le verdict, prouvé à l'exécution

Les 30 routes ont été sollicitées avec des entrées que le serveur doit refuser —
symbole inexistant, corps vide, identifiant inconnu. On ne raisonne pas sur le
code : on lit **la réponse réellement servie**.

```text
12 refus identifiés · 12 motivés · 0 MUET
```

Les motifs prennent plusieurs formes, toutes honnêtes : `reason`, `error`,
`available: false`, `empty` + `generator`, ou l'`audit_trail` qui énumère ce qui
manquait — forme déjà relevée au 377.

Trois réponses ne portent aucune clé de motif mais **ne sont pas des refus**, et
n'inventent rien :

```text
/desc/ZZZZINEXISTANT    {"summary":"", "industry":"", "employees":null, …}
/api/positions/state    zéros + delta_global:null + note « jamais estimés en agrégat »
/api/desk               {}
```

Une absence rendue comme une absence : exactement l'invariant n°4.

**L'angle mort du 377 est propre.** Ce n'est pas une absence de résultat : c'est
un résultat.

## Deux fois l'instrument en cause — dont une qui a sali un cache

**Fausse alerte.** Ma sonde signalait `run_startup_sequence` comme un refus MUET.
Il ne l'est pas : c'est un rapport de démarrage dont **le motif vit entièrement
dans `steps`**, chaque étape portant son statut et son message
(`'DEGRADED', 'SSE indisponible — polling seul'`). Ma liste de clés de motif ne
contenait pas `steps`. **Neuvième fois de la tranche que l'outil est en cause
avant le code.**

**Trois mutations fautives, dont une salissante.** Sur la preuve ROUGE :
`greeks_note` n'est pas dans `positions_api.py` mais dans `recalculator.py` · la
clé `reason` ne vient pas d'`analysis_api` · et surtout, pour `/desc`, j'avais
muté une branche **non atteinte** dans cet environnement — sans réseau, le bloc
`yf.Ticker` échoue et le chemin servi est **l'initialisation** du dict.

Corrigée, cette mutation a mordu — mais elle a aussi **écrit une description
inventée dans `desc_cache.json`**, que le code restauré relisait ensuite : la
suite restait rouge après restauration. Le fichier a été supprimé (il n'existait
pas avant la sonde), écart runtime final : **aucun**.

Deux enseignements : *une mutation qui ne mord pas accuse d'abord la mutation* a
encore payé trois fois de suite ; et **restaurer le code ne suffit pas quand la
mutation a écrit sur disque** — il faut vérifier l'état runtime, pas seulement
l'arbre git.

## Un 22ᵉ fichier runtime, découvert par cet incident

`desc_cache.json` n'apparaît que lorsqu'une description est récupérée avec
succès : il était absent des 21 fichiers inventoriés depuis le lot 388. Le
gardien livré ne l'écrit pas — avec le code sain, `summary` reste vide et le
cache n'est jamais alimenté (vérifié après exécution). **Versé aux dossiers** :
l'inventaire runtime est à ouvrir de 21 à 22.

## Gardien

`tests/test_refus_variable_lot392.py` (14 tests). Le 377 **ne peut pas** couvrir
ces routes : son détecteur est statique et exige un littéral. Ici la propriété
est vérifiée **à l'exécution, sur la réponse servie**, stockage redirigé vers un
dossier temporaire (ces routes journalisent — leçon des lots 387-389).

- **dénominateur** : ≥ 25 routes servant une réponse construite en variable
  (30 mesurées) — sinon le gardien serait vide de sens ;
- **anti-double-emploi** : si le détecteur du 377 se mettait à déballer les
  variables, les deux gardiens se recouvriraient — le test le signale ;
- **LA propriété** : sur 10 routes prouvées refuser, la réponse doit porter un
  motif. La liste de clés acceptées est large : figer UNE clé ferait échouer un
  simple renommage, donc du code sain (leçon du 383) ;
- **rien n'est inventé** : `/desc` rend des chaînes vides pour un symbole
  inconnu ; la note « Greeks jamais estimés en agrégat » reste servie.

### Preuve ROUGE

```text
le détecteur du 377 se met à voir les variables (double emploi)   ROUGE OK
note « jamais estimés » retirée (site réel)                       ROUGE OK
la note ne dit plus « jamais estimés »                            ROUGE OK
description INVENTÉE pour un symbole inconnu (site SERVI)         ROUGE OK
après restauration : 14 passed
```

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Copies de sûreté des 21 fichiers runtime avant toute sonde ; `desc_cache.json`
  créé par la preuve ROUGE puis **supprimé** ; écart runtime final : aucun.
- Suite : **2842 → 2856 passed / 2 skipped** (+14). SW : `td-shell-v187`.

## Portée

Les 10 routes testées à l'exécution sont celles **prouvées refuser aujourd'hui** ;
les 20 autres routes à réponse variable ne sont couvertes que par le compte du
dénominateur. Et le verdict « 0 muet » porte sur les entrées invalides que j'ai
choisies : un chemin de refus déclenché par une autre condition — panne réseau,
IBKR absent — n'a pas été sollicité.

## Suite

Restent, à l'occasion : formes imbriquées des promesses de retour (375) · trois
sites de concaténation à constantes (374) · commentaire périmé de
`vx-entities.js`. Aucune ne porte de question d'honnêteté non tranchée ; le
prochain lot pourra être court si rien ne mérite mieux.

Prochaine échéance périodique : bilan n°9 **~lot 400**.
