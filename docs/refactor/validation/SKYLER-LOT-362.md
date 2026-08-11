# SKYLER LOT 362 — Règle n°6 : ce que « en cas de doute, les backups » promet vraiment

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-362` (base : lot 361 fusionné,
be5666f)

## Piste calibrée

Quatrième passage de la question qui a donné les lots 358, 359 et 361 — « la
règle écrite décrit-elle vraiment le code servi ? » — appliquée à la **règle
n°6**, celle qui protège les **données réelles de l'utilisateur** :
« `desk_data.json` : ne jamais l'écraser à la main ; en cas de doute, backups
`desk_backup_*.json` + `/api/desk/restore` ».

## Ce qui est SAIN — et mieux que la règle ne le dit

- **Chaîne de sauvegarde** (`vertex/app/routes/desk.py`) : snapshot quotidien
  avant écrasement, rotation à 7, restore au nom **strictement** validé
  (`re.fullmatch(r'desk_backup_\d{8}\.json')` → traversée refusée), `ts` neuf
  au restore pour que tous les appareils re-tirent la version restaurée. Déjà
  gardée par `tests/test_desk_backup_lot178.py`.
- **Le client se protège bien** (`vertex/ui/vx_kit.py`) : `pushServer()` ne part
  qu'après hydratation réussie (`_bootDone`) ; si `bootSync` échoue, il ne
  pousse **pas** (« blob potentiellement incomplet ») ; `bootSync` re-remplit
  toute clé absente en local avant tout push.

## Ce que la règle ne dit pas — trois faits mesurés

Sonde isolée (`persist.cache_path` redirigé vers un dossier temporaire — le
vrai `desk_data.json` n'a jamais été touché) :

```text
— 2. travail de la journée (2e sync) → snapshot quotidien créé AVANT
   contenu du snapshot : [{"note":"thèse"}]
— 3. un client pousse un desk VIDE ({}) — accepté ?
   HTTP 200 {'ok': True, 'ts': 3000}
   serveur après : {}
   snapshots après : ['desk_backup_20260808.json'] (inchangé = True )
— 4. un client pousse un desk PARTIEL (1 clé sur 3) — accepté ?
   serveur après : ['myFavs']
— 5. restore : à quel instant remonte-t-on ?
   → on récupère l'état d'AVANT la 1re sync du jour : True
   → le travail du jour (« ajout du jour ») est PERDU : True
```

1. **Un push `data: {}` est accepté** et remplace le blob. La validation porte
   sur le **type** (`isinstance(body['data'], dict)`) — `{}` est un dict.
   L'écrasement redouté n'a donc pas besoin d'être « à la main ».
2. **Le last-writer-wins est total, pas clé par clé** : un push partiel efface
   les clés absentes côté serveur.
3. **Aucun snapshot supplémentaire n'est pris à ce moment-là.** Le point de
   restauration reste l'état d'**avant la première sync du jour** — un restore
   fait donc **perdre tout le travail de la journée**, avec au plus **7 jours**
   de profondeur.

**Scénario résiduel réaliste** : un navigateur dont l'écriture localStorage
échoue en silence (navigation privée, quota) — `bootSync` hydrate mais rien ne
persiste, et le push suivant envoie `{}`. Le serveur est le seul endroit où ce
cas pourrait être arrêté ; il ne l'arrête pas.

## Ce que le lot livre

1. **Gardien neuf** `tests/test_desk_perte_lot362.py` (5 tests de
   **caractérisation**) : push vide accepté, validation de type seule, push
   partiel qui efface, point de restauration inchangé après la perte,
   profondeur bornée à 7. Les messages d'échec disent explicitement « mettre à
   jour ce gardien » — ces tests décrivent le contrat, ils ne le bénissent pas.
2. **Règle n°6 de `CLAUDE.md` corrigée** : ce que le filet couvre vraiment
   (point de restauration, profondeur 7 jours, last-writer-wins total, push
   vide accepté), ce que le client garantit déjà, et les deux gardiens.

### Preuve que le gardien ALERTE

Pour des tests de caractérisation, la bonne preuve n'est pas « retirer une
défense » mais **simuler le durcissement proposé** et vérifier que le gardien
vire au rouge — c'est-à-dire qu'il réclame sa mise à jour :

```text
durcissement simulé (refus du push vide) → ROUGE OK — le gardien réclame sa mise à jour
   1 failed, 2 passed in 2.06s
restauration : identique
après restauration : 5 passed in 1.98s
```

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 361, be5666f) ; arbre propre.
- Suite complète : **2511 → 2516 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : le lot ne touche que `tests/`, `CLAUDE.md`
et `docs/` — aucun octet servi, `/static` inchangé.

## Ce que ce lot NE fait pas — décision à prendre

Aucune perte réelle n'a été observée et **je n'ai rien durci** : refuser un push
qui vide un desk non vide changerait le contrat de synchronisation
(last-writer-wins est le modèle documenté et assumé), et pourrait bloquer un
« je vide tout volontairement » légitime. Trois options, par coût croissant, en
attente d'un **GO humain** :

- **A — snapshot supplémentaire avant perte** : prendre un `desk_backup_` de
  plus quand le push entrant vide ou réduit fortement le desk. Purement
  additif, ne bloque jamais la sync, supprime le « on perd la journée » dans le
  cas qui compte.
- **B — refus 409 d'un push vide sur un desk non vide**, avec un en-tête
  explicite pour forcer si l'utilisateur le veut vraiment.
- **C — fusion par clé au lieu du remplacement total** : change le modèle de
  sync, le plus intrusif, à ne faire que si le last-writer-wins gêne
  réellement.

Ma recommandation : **A**, additive et sans effet de bord — mais c'est votre
décision, rien n'est engagé.

## Suite

LOT 363 : veille active. Reste à passer à la question : règle n°1 (clés de sync
desk — déjà auditée aux lots 323/327 et gardée par 2 tests) et règle n°4
(données RÉELLES uniquement). Prochaine échéance périodique : ~lot 370.
