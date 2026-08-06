# SKYLER V2 — LOT 71 : PROGRAMME 100 % (ouverture) — hygiène des références

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-71-hygiene-doc`
(base : `integration/vertex-skyler-v2` @ `ed8f00f`, fraîchement fetchée).

## 0. Nouvelle directive utilisateur

« Continue à tout développer et quand t'as tout à 100 tu me dis. »
→ Sortie de la surveillance espacée, ouverture du **PROGRAMME 100 %**
(lots 71 → 75) : fermer TOUT ce qui reste d'améliorable et de prouvable,
puis déclarer le 100 % à l'utilisateur avec un bilan consolidé n°6.
Cadence resserrée (~2 min entre lots).

## 1. Défaut réel corrigé (hérité, dit au lot 68)

La docstring de `vertex/data_sources/ibkr_gateway.py` citait un gardien
INEXISTANT (`tests/test_readonly_gateway.py`) — la doc mentait sur qui
garde le READONLY. Corrigé PAR la source : elle cite désormais les trois
vrais gardiens (`test_no_orders.py`, `test_ibkr_honesty.py`,
`test_order_ticket.py`).

## 2. Classe de défauts fermée (gardien prospectif)

Balayage complet du dépôt : tout chemin de fichier cité dans le code et
absent du disque. Résultat : les dizaines de « manquants » apparents sont
des chemins d'URL `/static/vertex/...` (fichiers réels sous
`vertex/static/` — faux positifs) ; UNE seule vraie divergence (le
gateway, ci-dessus) ; une référence auto-gardée par `os.path.exists`
(saine). `tests/test_hygiene_lot71.py` (2 tests, rouges d'abord) impose
désormais : toute référence `tests/test_*.py` dans vertex/ doit exister.

## 3. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1696 passed, 2 skipped   (1694 + 2)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v123 servi,
  cycle souverain inclus)
Responsive 8 pages × 3 viewports → 0 débordement, 0 erreur
```

Pas de bump SW : aucun changement de shell visible (docstring serveur).

## 4. Suite

Lot 72 : audit PERFORMANCE (poids des pages, scripts servis, temps de
chargement mesurés en navigateur) — chaque lot du programme ferme un
angle, le lot 75 sera la RC finale + BILAN n°6 (déclaration 100 %).
