# SKYLER LOT 218 — Derniers invariants CLAUDE.md : desk backup (gardé) + écoute réseau (gardien neuf)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-218` (base : lot 217 fusionné)

## Objet

Fin de l'audit d'invariants CLAUDE.md (lots 214, 216, 217) : les deux
derniers non audités — « desk_data.json : ne jamais l'écraser à la
main ; backups desk_backup_* + /api/desk/restore » et « sans code
d'accès, le serveur n'écoute que 127.0.0.1 ».

## Constat 1 — Filet desk_data.json : TENU et déjà gardé (8 tests)

`tests/test_desk_backup_lot178.py` couvre la chaîne entière :
snapshot quotidien créé AVANT le premier écrasement du jour (filet
contre le last-writer-wins), snapshot du matin jamais réécrit par les
pushs suivants, rotation à 7 jours, validation STRICTE du nom au
restore (surface de sécurité : le nom vient du client). Rien à ajouter.

## Constat 2 — Écoute réseau : TENUE… mais gardée par AUCUN test

La règle vit dans `terminal.py` (_start_app L10728-10729) :

```python
lan_ok = AUTH_ON or os.environ.get('VERTEX_LAN') == '1' or 'PORT' in os.environ
host = '0.0.0.0' if lan_ok else '127.0.0.1'
```

Lacune mesurée : `grep lan_ok|0.0.0.0|VERTEX_LAN tests/` →
**0 occurrence**. On pouvait passer l'écoute par défaut à 0.0.0.0 —
desk lisible par tout le Wi-Fi sans code — sans casser la suite.

## Livré — gardien `tests/test_network_binding_lot218.py` (3 tests)

1. les DEUX lignes de la décision épinglées à la source (le bloc
   __main__ ne s'exécute pas sous pytest — inspection de source,
   comme les gardiens readonly) ;
2. table de vérité re-déroulée sur la même expression : défaut →
   127.0.0.1 ; verrou actif / VERTEX_LAN=1 / cloud ($PORT) → 0.0.0.0 ;
   VERTEX_LAN=0 ≠ opt-in ;
3. le message de config_validation reste honnête
   (« 127.0.0.1 uniquement »).

## Bilan de l'audit d'invariants (lots 214 → 218)

| Invariant CLAUDE.md | Verdict | Gardien |
|---|---|---|
| n° 1 desk sync 4 listes | TENU | existant (vert, 17 clés vérifiées) |
| n° 2 JS généré valide | TENU | existant (lot 182, node --check) |
| n° 5 sanitize_news | TENU | existant (lot 177) + faux positif écarté |
| n° 6 desk_data backups | TENU | existant (lot 178, 8 tests) |
| IBKR readonly | TENU | 3 existants |
| IBKR RequestTimeout=45 | TENU | **neuf** (lot 216) |
| scan_state jamais réassigné | TENU | **neuf** (lot 217) |
| écoute 127.0.0.1 sans code | TENU | **neuf** (lot 218) |

**8 invariants vérifiés par constat, 3 lacunes de garde réelles
trouvées et comblées, 0 violation.**

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : tests seulement.

## Preuves

- Nouveau gardien : **3/3 passed**.
- Suite complète : **2482 passed / 2 skipped** (2479 + 3).

## Suite

LOT 219 : entretien suivant ou directive. Mini-bilan 216-220 attendu
au lot 220. Purge terminal.py toujours EN ATTENTE d'accord humain.
