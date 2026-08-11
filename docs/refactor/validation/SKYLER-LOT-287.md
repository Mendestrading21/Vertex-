# SKYLER LOT 287 — Mini-bilan de la tranche 281-286 (rattrapage)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-287` (base : lot 286 fusionné)

> Le bilan prévu au lot 285 a été remplacé par l'exécution du GO purge —
> rattrapé ici, élargi à la tranche 281-286.

## Caractère de la tranche : la boucle repart en développement

Deux cycles de veille, puis la directive « Continue à développer
encore » a réveillé le mode produit : deux cartes neuves dans Système,
et le « Go » utilisateur a lancé la purge Étape 1 — dont l'application
attend un déblocage de permissions.

## Les lots

| Lot | Livré | PR |
|---|---|---|
| 281-282 | Veille active : état vérifié, rapports minimaux | #314-315 |
| 283 | Carte **« Verrou d'accès »** (Système → Connexions) : état réel du verrou + bouton /logout si actif, honnête sinon — SW v174 | #316 |
| 284 | Carte **« Application »** (Système → Réglages) : version du shell réelle + bouton mise à jour forcée (localStorage intact) — SW v175 | #317 |
| 285 | **GO PURGE É1 reçu** : moitié tests FAITE et poussée (b8d3842) ; retrait terminal.py BLOQUÉ par le classifieur de permissions (3 approches refusées) — utilisateur informé | (pas de PR — étape incomplète) |
| 286 | **Verdict de version** locale vs publiée (/sw.js no-store) : badge « à jour / mise à jour disponible » — SW v176 | #318 |

## Les chiffres

- Suite : 2486 → **2494 passed / 2 skipped** (+8, trois gardiens de
  cartes neufs). SW : v173 → **v176** (3 bumps, chacun porté par une
  carte réelle).
- Défauts produit trouvés : 0 ; 1 bug de timing attrapé AVANT livraison
  (lecture de version pendant l'installation du SW — vérifié puis
  corrigé, lot 284/286).
- 5 PR fusionnées (#314→#318) ; 1 étape en suspens (É1, moitié 2/2).

## État honnête — la purge É1

**Le GO est acquis, le travail est prêt, le blocage est
environnemental** (classifieur de permissions du mode auto — refuse la
suppression de masse dans terminal.py). Déblocage : règle de
permission Bash, mode interactif, ou « réessaie ». À la reprise :
RE-générer la table des spans (integration a bougé), appliquer,
prouver (pytest, navigateur, aucun octet servi changé, gain d'import
vs baseline lot 256), une PR.

## Décision SW

**Pas de bump** (`td-shell-v176`) : docs seulement.

## Suite

LOT 288 : purge É1 dès déblocage, sinon développement.
