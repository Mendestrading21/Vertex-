# SKYLER V2 — LOT 55 : connexions entre pages (fil d'Ariane cliquable + retour complet)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-55-connections`
(base : `integration/vertex-skyler-v2` @ `f182464`, fraîchement fetchée) ·
Mode : développement, arc « jusqu'au lot 60 » (2/7) — directive utilisateur
« simplifier les connexions entre les pages ».

## 1. Audit préalable (honnête) — l'infrastructure était déjà bonne

Avant de toucher quoi que ce soit, audit réel des connexions existantes :
`VX.openAnalysis` (contexte sauvegardé + tickers récents) est utilisé
PARTOUT via la délégation globale `[data-open-analysis]` ; les tuiles KPI
du briefing sont déjà des liens vers leur domicile (`/markets`,
`/markets?view=breadth`, `/markets?view=volatility`, meilleure opp. →
fiche) ; les leaders sectoriels de Marchés, les dossiers d'Opportunités,
les lignes du Portefeuille ouvrent la fiche d'un clic ; les badges de
calibration de la carte Mémoire → vues cellule (lots 39-40). Deux trous
RÉELS restaient — fermés centralement.

## 2. Trou n°1 : fil d'Ariane MORT (fermé)

« Vertex / Analyse / AAPL » : « Vertex » et « Analyse » étaient des
`<span>`/`<b>` non cliquables — depuis une fiche, le chemin naturel de
remontée n'existait pas. Corrigé aux DEUX niveaux de rendu :

- **serveur** (`vertex/ui/shell/__init__.py`) : `_topbar` rend
  `<a class="vx-crumb-root" href="/">Vertex</a>` et le segment d'espace
  en `<a href="{racine de l'espace}">` — le href vient de `PRIMARY_NAV`
  par l'id actif (`_space_href`, source unique) ;
- **client SPA** (`vx-router.js` `updateCrumb`) : le crumb reconstruit à
  chaque navigation porte les mêmes liens — le href d'espace est dérivé
  du menu latéral RENDU (`[data-nav-id]`), zéro duplication du registre ;
- CSS (`layout.css`) : liens en couleur héritée, soulignement au survol.

## 3. Trou n°2 : retour contextuel incomplet (fermé)

`SPACE_LABELS` (vx-shell.js §15) référençait les anciennes routes
`/performance` et `/intelligence` mais PAS `/options` ni `/journal` : un
retour depuis ces espaces affichait le chemin brut (« Retour /options »).
Complété — les 8 espaces canoniques couverts, les 2 anciennes routes
encore joignables conservées.

## 4. Tests (rouges d'abord — 5 nouveaux)

`tests/test_connections_lot55.py` (rouge 5/5 confirmé) : racine du crumb
= lien serveur · segment d'espace = lien serveur (`/markets` prouvé) ·
`updateCrumb` client construit des liens depuis `data-nav-id` ·
`SPACE_LABELS` couvre les 8 espaces · SW ≥ v112 et v111 absent.

## 5. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_connections_lot55.py -q → 5 passed
python -m pytest tests/ -q → 1655 passed, 2 skipped   (1650 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v112 servi,
  cycle souverain inclus)
Preuve navigateur (parcours RÉEL) :
  /analysis/AAPL (chargement dur) → crumb « Vertex / Analyse / AAPL »
    avec root href="/" et espace href="/analysis" ;
  CLIC réel sur « Analyse » → atterrit sur /analysis ;
  navigation SPA VX.openAnalysis('MSFT') → crumb reconstruit garde les
    deux liens (root "/", espace "/analysis"). 0 erreur console.
```

SW `td-shell-v111` → `td-shell-v112` + 4 gardiens.

## 6. Invariants

READONLY intact · aucun moteur touché (navigation pure) · `main` intacte ·
fichiers runtime non commités · source unique respectée aux deux niveaux
(PRIMARY_NAV côté serveur, menu rendu côté client).

## 7. Suite (arc)

Lot 56 : polish détaillé Aujourd'hui + Marchés. Puis 57-59, et 60 = RC
finale + bilan consolidé n°4 + ARRÊT.

**Arrêt après ce lot — validation humaine requise.**
