# SKYLER V2 — LOT 177 : gardien XSS de bout en bout (règle critique n°5)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-177`
(base : `integration/vertex-skyler-v2` @ `497ba01`, lot 176 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible — NOUVELLE DIRECTION : surfaces de sécurité

Survey : les pages UI ont leurs gardiens, `news_plus` a le lot 102 —
mais le lot 102 fige la FONCTION `sanitize_news`, pas les ROUTES. La
règle critique n°5 du projet (« tout texte externe passe par
sanitize_news avant d'être servi — rendus en innerHTML côté
client ») n'avait AUCUN test d'injection de bout en bout : rien ne
prouvait que chaque point de sortie HTTP applique réellement
l'assainissement.

## 2. Ce qui est figé (`tests/test_xss_exits_lot177.py`, 6 tests)

Payload injecté dans les états partagés : `<script>alert(1)</script>`
dans le titre, `<img src=x onerror=alert(2)>` dans la traduction,
lien `javascript:alert(3)`, et un lien https avec quotes/chevrons.

```text
/news-feed — titre servi SANS balise avec quotes échappées
  (« alert(1)Résultats &quot;record&quot; »), fr entièrement vidé,
  publisher sans balise ; lien javascript: → None, lien https
  conservé mais %-encodé (%22/%3C — sûr en href ET window.open) ;
  le filtre serveur ?sym= ne contourne PAS l'assainissement
/api/events/<sym> — le JSON complet ne contient JAMAIS <script>,
  javascript:alert ni onerror= ; le texte survit neutralisé
/api/skyler/<sym> — même garantie sur tout le SkylerPacket (les
  news traversent evidence/events sans jamais ressortir brutes)
Gardien statique — compte des sites d'appel sanitize_news( en
  production ≥ 6 (content, analysis_api ×2, skyler_sweep,
  terminal ×2) : retirer un assainissement fait échouer la suite
```

## 3. Preuves

```text
python -m pytest tests/test_xss_exits_lot177.py -q → 6 passed
python -m pytest tests/ -q → 2389 passed, 2 skipped (2383 + 6)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 178 : poursuivre les surfaces de sécurité — candidats : verrou
d'accès VERTEX_CODE (auth.py, 149 l — cookies/redirections), en-têtes
de réponse, /api/desk (écriture du blob : LWW + backup), ou retour
au survey général. MINI-BILAN au lot 180.
