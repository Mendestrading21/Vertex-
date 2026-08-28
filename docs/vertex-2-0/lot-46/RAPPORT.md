# Lot 46 — Fraîcheur honnête : l'âge affiché vient du serveur, jamais du clic

## Problème (besoin consigné depuis la campagne visuelle)

1. `/cal-feed` ne portait aucun champ `ts` : `cal_state` n'écrivait qu'un
   libellé humain (`updated` = « 19:54 28/08 ») — la page Calendrier
   affichait un libellé figé, jamais un âge vivant, et les anciennes pages
   affichaient l'heure du NAVIGATEUR comme fraîcheur (toujours verte, fausse).
2. `options-symbol.js` passait `timestamp: Date.now()` sur **7 cartes**
   (structure par terme, cône, OI, smile, scénarios, décote, sensibilité IV)
   — l'heure du CLIC affichée sous « source : scan ».
3. Les payloads `/api/options/vol-charts` et `/api/options/scenarios` ne
   portaient aucune époque exploitable (`as_of` = libellé humain,
   inanalysable par `VX.freshness._ms`).

## Correctif

- `terminal.py` : les deux écrivains de `cal_state['updated']` posent aussi
  `cal_state['ts'] = time.time()` → `/cal-feed` le sert (`**cal_state`).
- `options_intel_api.py` : `_ts_epoch()` (options_as_of d'abord, repli
  scan_ts) ; `vol-charts` et le payload succès de `scenarios` portent `ts`.
- `options-symbol.js` : les 7 `timestamp: Date.now()` → `timestamp: d.ts` —
  ts absent → « Âge inconnu » (le mot honnête d'updateIndicator), jamais
  maintenant.
- `calendar.js` : la fraîcheur préfère `cal.ts` (âge VIVANT, re-tické) avec
  le libellé de construction en suffixe ; replis inchangés.
- SW **v281 → v282** (outil `vertex_2_0_bump_sw.py`, empreinte 78 fichiers).
- `docs/vertex-2-0/RECAPITULATIF.md` : en-tête de mise à jour — le document
  historique affirmait encore « PR en brouillon, rien n'a été fusionné » et
  listait comme ouverts des besoins soldés.

## Preuves

- Serveur démo : `/cal-feed` → `ts: 1787946871.02` à côté de
  `updated: "19:54 28/08"` ; `/api/options/vol-charts/NVDA` → `ts` epoch.
- Navigateur : Calendrier affiche « À l'instant · lot construit à 19:54
  28/08 · Différé » — un âge serveur re-tické, plus un libellé figé.
  Console vide.
- `tests/test_fraicheur_honnete_lot46.py` — 4 bancs nés rouges (époque sur
  /cal-feed, les 2 écrivains posent ts, vol-charts/scenarios portent ts,
  plus aucun `timestamp: Date.now()` dans options-symbol.js).
- Suite complète : **4471 passés · 152 ignorés · 0 échec**.

## Rollback

git revert du commit unique.
