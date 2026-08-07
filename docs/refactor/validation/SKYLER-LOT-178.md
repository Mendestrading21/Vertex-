# SKYLER V2 — LOT 178 : filet de sécurité du desk (backup + restore)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-178`
(base : `integration/vertex-skyler-v2` @ `9e07880`, lot 177 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey : `auth.py` (candidat prévu) est déjà TRÈS couvert
(test_auth_routes, 15 tests — force-brute, open-redirect, échappement).
Repli sur la vraie lacune : la chaîne de SAUVEGARDE de `desk.py` —
le round-trip push/pull est couvert (desk_routes, cycle lot 84), mais
le snapshot quotidien (`_backup_desk`, filet contre le
last-writer-wins — règle critique n°6), la rotation à 7 jours et la
validation du restore (le nom vient du client — surface de sécurité)
étaient à zéro test.

## 2. Ce qui est figé (`tests/test_desk_backup_lot178.py`, 8 tests)

```text
Snapshot quotidien — créé au PREMIER écrasement du jour (le contenu
  sauvegardé est celui d'AVANT le push) ; jamais réécrit par les
  pushs suivants (le snapshot du matin protège toute la journée) ;
  rotation : 8 anciens + celui du jour → 7 conservés (BACKUP_KEEP),
  les plus vieux purgés
/api/desk/restore — noms hors motif STRICT refusés 400 (« nom
  invalide ») : ../../etc/passwd, date incomplète, suffixe .bak,
  autre.json, vide — le path traversal est impossible ; introuvable
  → 404 ; backup illisible (nom valide, contenu mort) → 500 SANS
  toucher le desk courant ; restore réussi → données du snapshot +
  ts DE MAINTENANT (dans le modèle last-writer-wins, tous les
  appareils re-tirent la version restaurée)
/api/desk/backups — listés du plus récent au plus ancien, keep 7
```

## 3. Preuves

```text
python -m pytest tests/test_desk_backup_lot178.py -q → 8 passed
python -m pytest tests/ -q → 2397 passed, 2 skipped (2389 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 179 : dernières surfaces de sécurité à sonder — webhook
TradingView (secret hmac, anti-replay — vérifier la couverture des
12 tests existants), en-têtes de réponse (headers lot 77 ?), ou
retour au survey général. MINI-BILAN 176-180 au lot 180.
