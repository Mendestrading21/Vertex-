# G3 · #783 — Le moteur ne se notait pas

Instrument : `tools/vertex_1_0/mesurer_track_record.py`
Gardien : `tests/test_vertex_1_0_track_record.py` (10 tests, 6 mutations)
Mesure figée : `docs/vertex-1.0/inventory/track_record.json`

---

## Le défaut

`RELEASE_GATES.md` G3 demande que *« la mémoire des résultats soit exploitable
sans look-ahead »*. La seconde moitié n'a de sens que si la première tient :
encore faut-il que la mémoire produise **quelque chose**.

`track_record._fwd` cherchait un libellé `'%m-%d'` dans `series['dates']`, qui
contient des dates **ISO**. `'05-15' in ['2026-05-15', …]` est toujours faux :
`.index()` levait `ValueError` sur **chaque** entrée, et `evaluate()` rendait
`resolved: 0` quoi qu'il arrive.

```text
avant : 8 entrées, +1 / +5 / +20 tous échus  ->  0 résolue
après : 8 entrées, mêmes horizons            ->  8 résolues
```

`vertex/engines/analysis.py` fournit **les deux** formats — `dates` en ISO et
`date_labels` en `%m-%d` — avec un commentaire qui dit pourquoi : « afin de ne
jamais réinterpréter les années ». La fonction lisait le mauvais champ, et son
propre commentaire (« dernière occurrence — bord d'année ») décrivait une
contorsion rendue nécessaire par ce mauvais choix.

## Pourquoi il a survécu : un test vert au-dessus

`tests/test_track_record_lot89.py` fournissait `dates = ['08-01', …]`. Ce format
n'est **produit nulle part**. Le test validait un chemin qui n'existe pas en
production, et il passait — ce qui rendait le défaut invisible à la suite
entière, y compris à tous les audits qui l'ont traversée.

C'est la leçon la plus transférable de ce lot : **une fixture qui ne ressemble
pas à la production ne teste pas la production**, et un test vert au-dessus d'un
défaut est pire que pas de test — il en interdit la découverte.

## Ce que l'écran disait pendant ce temps

> « Pas encore assez de verdicts résolus … **Le registre se remplit à chaque
> scan.** »

C'est-à-dire : *patience*. Pour une condition qui ne pouvait **jamais** se
résoudre. L'écran n'inventait pas de chiffre — il donnait une explication
rassurante à un vide dont il ignorait la cause.

`evaluate()` ventile désormais les entrées non notées en trois causes
distinctes : `horizon_non_echu`, `sans_serie`, `date_absente`. L'écran les sert.
`resolved: 0` ne peut plus passer pour un manque d'historique.

## La restriction aux survivants, maintenant dite

Une entrée n'est notée que si son titre est **encore dans le scan du jour** —
c'est de là que viennent les séries de prix. Un verdict sur un titre sorti de
l'univers n'est jamais compté : la fiabilité affichée porte donc sur les
**survivants**.

Ce n'est pas corrigeable sans historique de prix pour les titres sortis, que le
produit ne conserve pas. Mais c'est **disable**, et c'est désormais dans la note
servie. Un biais nommé n'est plus un biais caché.

## Le look-ahead, vérifié horizon par horizon

La garde existait déjà et elle est correcte : `j >= len(closes)` refuse un
horizon non échu. Ce lot la teste **séparément par horizon**, ce qui est la
formulation exacte de la propriété : à trois séances de la fin, `+1` doit être
calculé et `+5` / `+20` refusés. Un test « en bloc » aurait laissé passer une
implémentation qui rend `+20` dès que `+1` est disponible.

## Un témoin qui « passait » pour la mauvaise raison

Le témoin négatif de l'instrument — « une entrée non échue ne doit jamais être
résolue » — était vert **pendant tout le temps où la jointure était cassée** :
rien ne se résolvait, donc rien ne pouvait se résoudre à tort. Il n'a commencé à
dire quelque chose qu'une fois la mesure vivante, et il a alors immédiatement
signalé que ma borne était fausse (`SEANCES - 2` laisse `+1` échu).

Un témoin négatif vert sur un détecteur aveugle ne prouve rien.

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 340 passed        (3 330 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations                      6/6 mordent, contrôle vert
```

Les six : retour à la jointure `%m-%d` · look-ahead autorisé · ventilation des
causes supprimée · la note n'avoue plus les survivants · l'écran réinvite à
patienter · la fixture revient au format court.

> Une septième tentative de mutation a « passé » : elle remplaçait `survivants`
> par `SURVIVANTS_RETIRE`, dont le `.lower()` contient encore le mot cherché.
> C'était **ma mutation** qui était mauvaise, pas le test — refaite correctement,
> elle mord.

Serveur réel, `DEMO=1 NO_IBKR=1` :

```text
huit espaces                    200 · 0 débordement · 0 erreur console
/api/client-log                 count: 0
/api/track-record               ignores servi, note avec la mention « survivants »
/journal?view=track-record      « 0 verdict(s) enregistré(s), 0 résolu(s) —
                                  il en faut 5 par verdict pour publier une
                                  fiabilité. »
```

Bump du cache de shell `td-shell-v207 → v208`.

## Limites

- **Le registre réel n'a pas été mesuré** : `edge_ledger.jsonl` est gitignoré et
  absent du conteneur. Toutes les mesures portent sur un état fabriqué au format
  exact du produit. Sur la machine du trader, le premier `/api/track-record`
  après ce correctif dira enfin quelque chose — c'est là, et seulement là, que
  la fiabilité réelle du moteur apparaîtra.
- **La restriction aux survivants n'est pas levée**, seulement dite.
- `tp1_rate` reste approximé sur clôtures, sans intraday — inchangé, et toujours
  étiqueté comme tel.

**G3 non déclaré PASS** : il exige aussi un packet décisionnel
reproductible/versionné, l'ingestion WMB avec provenance, et des scénarios
étiquetés/calibrés. Ce lot ferme « la mémoire des résultats est exploitable »,
et rien de plus.
