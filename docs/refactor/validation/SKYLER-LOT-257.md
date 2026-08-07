# SKYLER LOT 257 — README ↔ réalité : 4 défauts corrigés (dont 1 de sécurité)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-257` (base : lot 256 fusionné)

## Objet

Le README (vitrine du dépôt) n'avait jamais été audité contre la
réalité mesurée — contrairement à CLAUDE.md (lots 214-218) et aux docs
de validation (lot 238). Audit ligne par ligne contre les faits
établis par la campagne.

## Défauts trouvés et corrigés (4)

1. **SÉCURITÉ — affirmation fausse** : « Le serveur écoute déjà sur
   tout le réseau local (`host='0.0.0.0'`) ». La réalité (durcie et
   gardée par `test_network_binding_lot218`) : **écoute 127.0.0.1 par
   défaut**, `0.0.0.0` seulement si `VERTEX_CODE` (verrou) ou
   `VERTEX_LAN=1`. Un lecteur suivant le README aurait cru son desk
   exposé (ou s'y serait attendu) à tort. → Section réécrite avec la
   vraie procédure.
2. **Pages obsolètes** : liste pré-refonte (`/titre`, `/entreprises`,
   `/watchlist`…) → remplacée par les 8 espaces canoniques mesurés
   (lot 251 : 8 × HTTP 200) + note de redirection des anciennes routes.
3. **Univers faux** : « 57 leaders US » → S&P 500 ∪ Nasdaq 100 ∪ Dow
   (~500 titres — `vertex/data/universe.py`, healthz : 517).
4. **Structure périmée** : ne mentionnait ni `vertex/app/routes/` ni
   `vertex/ui/pages/` ni les moteurs actuels (decision_stack,
   recommendation…) → mise à niveau.

## Vérifications AVANT correction (calibrage)

- `ib_reader.py` : existe ET branché (`terminal.py` L2099
  `from ib_reader import IBKRReader`, readonly forcé) — la ligne du
  README le concernant était CORRECTE, conservée.
- `DEMARRER_ICI.md`, `Lancer_VERTEX.command/.bat`, `.env.example` :
  tous existants — pointeurs conservés.
- Aucun test n'épingle le contenu du README (grep tests/ : 0).

## Décision SW

**Pas de bump** (`td-shell-v173`) : README seulement, aucun octet
servi ne change.

## Preuves

- Diff limité à README.md (4 blocs).
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 258 : entretien espacé ou directive. La purge attend « GO purge
étape 1 ».
