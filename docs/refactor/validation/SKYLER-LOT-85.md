# SKYLER V2 — LOT 85 : boucle continue — alertes + flux live bout-en-bout

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-85-alertes`
(base : `integration/vertex-skyler-v2` @ `462462a`, fraîchement fetchée).

## 1. Cycle alerte (navigateur, 4/4)

```text
1 création VXEntities.addAlert('ACN', above, 999.5) →
  persistée localStorage (0→1), hasAlert vrai                 OK
2 sync desk : le serveur porte l'alerte (push réel 17 clés)   OK
3 UI branchée (la fiche parle des alertes)                    OK
4 suppression propre + serveur nettoyé (re-push)              OK
```

## 2. Flux live SSE — SAIN (2 faux positifs de MES sondes, dits)

- sonde curl piped : 0 octet en 30 s → **buffering du pipe**, pas du
  serveur (vérifié au SOCKET BRUT : réponse instantanée — retry: 4000 +
  replay `id:1 event:system data:{json}`) ;
- sonde EventSource `onmessage` : silencieuse car les événements sont
  NOMMÉS — re-prouvé avec `addEventListener('system')` : événement JSON
  reçu en navigateur ;
- le consommateur produit `live-updates.js` fait exactement ça :
  abonnement par canal + reconnexion lastEventId + fermeture pagehide.

## 3. Verdict : SAIN — lot documentaire, 3 gardiens (nés verts, dits)

`tests/test_alerts_live_lot85.py` : la route SSE garde
retry/replay/heartbeat · le consommateur garde canaux nommés/lastEventId/
pagehide · l'API client alertes reste complète.

## 4. Preuves

```text
python -m pytest tests/ -q → 1725 passed, 2 skipped   (1722 + 3)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 5. MINI-BILAN de tournée 81-85 (écrit dans STATUS)

Polices auto-hébergées (0 requête externe) · offline RÉEL corrigé
(défaut majeur : le shell n'enregistrait jamais le SW) · 26 contrôles
interactifs 0 inerte · cycle desk 6/6 sans perte possible · alertes+SSE
4/4 sains. Suite 1714 → 1725, SW v125 → v127.

## 6. Suite

Lot 86 : angle suivant le plus porteur de la tournée perpétuelle.
