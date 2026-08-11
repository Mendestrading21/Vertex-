# SKYLER V2 — LOT 04 — NEWS, CATALYSEURS ET ANOMALIES

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-04-events-ohlcv`
> Base : `agent/skyler-v2-lot-03-market-context`
> Périmètre : série canonique + dédup news + timeline normalisée — aucun calcul financier modifié

## 1. Constat (audit OHLCV — risque n°7 du STATUS)

Vérifié de bout en bout : **la chaîne OHLCV décisionnelle est déjà honnête**.
Le scan produit des O/H/L/V RÉELS (`analysis.py:281-296`, None si colonnes absentes,
jamais fabriqués) ; la page Analyse ne construit des bougies QUE si O/H/L réels et
alignés (`analysis_page.py:371-372`), sinon repli ligne étiqueté (« clôtures
quotidiennes ») ; le builder LWC valide chaque bougie et se replie honnêtement.
Aucune reconstruction artificielle à supprimer dans les chemins décisionnels.

Défauts réels trouvés :
1. **Formes de série non canoniques admises** : `/api/anomalies` et
   `/api/options/volatility` acceptaient `detail['closes']` / `detail['history']`
   — formes qu'AUCUN producteur n'écrit (code mort ouvrant la porte à des séries
   ambiguës) ; `/api/options/volatility` ne lisait même PAS la série canonique
   (closes toujours None → vol réalisée jamais calculée).
2. **Aucune déduplication de news** (mêmes titres re-servis).
3. **Aucune timeline normalisée** : news/earnings/macro/anomalies éclatés, sans
   distinction fait/interprétation ni impact tracé.

## 2. Décision

- `vertex/data/series.py` (nouveau) : accesseur CANONIQUE `closes(detail)` →
  `(clôtures_valides, 'scan.series.close')` — seule forme admise, points invalides
  écartés (jamais transformés), `([], None)` honnête. Branché dans
  `/api/anomalies/<sym>` (+ champ `series_source`) et `/api/options/volatility/<sym>`
  (la vol réalisée reçoit enfin la vraie série).
- `news_plus.dedupe_news(items)` : titre normalisé (casse/ponctuation/espaces) ou
  lien identique → premier conservé, jamais réécrit.
- `vertex/engines/events.py` (nouveau, pur) : timeline normalisée
  `{kind, label, date, dte, category: fact|interpretation, source, impact_hint,
  impact_derivation, importance, confidence}` :
  publication de news = FAIT mais impact suggéré UNIQUEMENT par mots-clés
  déterministes transparents (`impact_derivation: 'keywords'`, sinon None) ;
  earnings/macro = faits DECLARED du calendrier réel ; anomalies = INTERPRÉTATIONS
  (EXACT_STATISTICAL) ; datés triés par DTE croissant ; révisions d'analystes =
  `{available: false}` honnête (aucune source branchée — jamais estimé).
- Route additive `GET /api/events/<sym>` : assemble détail news (assainies
  **au point de sortie**), earnings du `cal_state`, macro réelle
  (`macro_calendar.events`), anomalies sur série canonique.

## 3. Fichiers modifiés

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/data/series.py` | nouveau — accesseur canonique | faible |
| `vertex/engines/events.py` | nouveau — timeline pure | faible |
| `vertex/services/news_plus.py` | + `dedupe_news` (additif) | faible |
| `vertex/app/routes/analysis_api.py` | anomalies → série canonique + `/api/events/<sym>` | faible |
| `vertex/app/routes/options_intel_api.py` | volatilité → série canonique | faible |
| `tests/test_events_timeline.py` | nouveau — 14 tests | faible |

## 4. Tests

```text
rouge : collection error (modules inexistants)
vert  : python -m pytest tests/test_events_timeline.py -q → 14 passed
suite : python -m pytest tests/ -q → 1214 passed, 2 skipped · compileall exit 0
```

Couverture : canonicité (formes legacy refusées), filtrage sans invention, dédup
(normalisation + lien, jamais de réécriture), forme normalisée, fait vs
interprétation, impact par mots-clés seulement, tri DTE, révisions absentes
honnêtes, build vide, dédup dans la timeline, route + XSS (`<script>` neutralisé).

## 5. Validation runtime (DEMO=1 NO_IBKR=1)

- `/api/anomalies/GOOGL` → `series_source: scan.series.close`, 120 points réels, 4 spikes ;
- `/api/events/GOOGL` → 7 événements : NFP (dte 3, fait), Résultats GOOGL (dte 9,
  fait DECLARED), CPI (dte 9), anomalies z=−2.5/+2.0 en interprétations —
  datés d'abord ; `revisions.available: false` ; `demo: true` ;
- `/api/client-log` = 0.

## 6. Invariants vérifiés

- [x] aucun OHLCV artificiel (audit documenté) ; une seule série canonique ;
- [x] fait ≠ interprétation ; impact jamais inventé ; catalyseur ≠ simple date ;
- [x] news assainies au point de sortie (XSS), déduplication sans réécriture ;
- [x] révisions = absence honnête ; moteurs financiers non modifiés ; READONLY.

## 7. Risques restants

1. Révisions d'analystes : dimension prévue, source à brancher (lot futur).
2. Anomalies de volume/options/fondamentales : le package `vertex/anomalies`
   existant les couvre au scan ; leur normalisation dans la timeline viendra
   avec le SkylerPacket (lot 5).
3. La timeline n'est pas encore affichée dans l'UI (l'API est prête) — lot 8.

## 8. Verdict

**GO** — 14 tests rouges → verts, chaîne OHLCV auditée honnête, série canonique
unique, timeline normalisée servie en runtime, suite 1214 verte.

## 9. Prochaine étape autorisée

`/vertex-skyler-v2 lot-5` (Skyler Core — contrats typés, score /40, hard gates,
scénarios, décision canonique).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**
