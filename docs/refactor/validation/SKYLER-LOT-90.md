# SKYLER V2 — LOT 90 : boucle continue — persist + connections figés + bilan 86-90

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-90-services`
(base : `integration/vertex-skyler-v2` @ `b91baf2`, fraîchement fetchée).
**Services INTACTS — diff = tests + docs uniquement.**

## 1. Les 10 comportements figés (nés verts, dits)

`vertex/services/persist.py` (49 l. — la persistance dont dépendent
desk_data et la mémoire souveraine) et `connections.py` (132 l. — l'état
honnête des intégrations). Tests redirigés vers un répertoire temporaire :
**aucun fichier runtime touché**.

```text
persist : fichier absent → défaut · JSON corrompu → défaut jamais
  crash · aller-retour fidèle (accents/n-d) · échec d'écriture
  silencieux par contrat (cache best-effort) · cache_path = racine     OK
connections : IBKR désactivé → OFFLINE + action TWS · activé sans
  session → OFFLINE (« configuré ≠ connecté — jamais LIVE sans
  preuve ») · connected → DELAYED · live → LIVE avec « lecture
  seule » TOUJOURS dit · tous les statuts ∈ canoniques + readonly
  True · demo_mode → CHAQUE connexion étiquetée demo                   OK
```

## 2. MINI-BILAN 86-90 : le programme « moteurs blindés » est complet

5 lots, **46 caractérisations nées vertes**, suite 1725 → **1771**,
**0 ligne de logique modifiée**, fichiers runtime jamais touchés :

- 86 · decision_stack (10) — bornes 56/66/80, None honnête, CHOP,
  distribution, démo étiquetée ;
- 87 · recommendation + __VXVOCAB (10) — vocabulaire sans trou,
  discipline -20/-25 exacte, thêta ;
- 88 · evidence + reasoning (10) — clamp 0-100, fondamental 0 = absent,
  contradictions Loi 14, jamais un % inventé ;
- 89 · track_record (6) — n<5 jamais publié, division par zéro
  impossible, TP1 non résolu honnête ;
- 90 · persist + connections (10) — tolérance totale, honnêteté des
  états.

**Toute la chaîne « données → preuves → décision → affichage →
auto-notation » est désormais figée par la suite : un changement de
sémantique n'importe où la cassera.**

## 3. Preuves

```text
python -m pytest tests/ -q → 1771 passed, 2 skipped   (1761 + 10)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 91 : angle suivant le plus porteur — la tournée continue.
