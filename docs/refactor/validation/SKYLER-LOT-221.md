# SKYLER LOT 221 — Liens internes + boutons : balayage navigateur des 8 pages (constat)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-221` (base : lot 220 fusionné)

## Objet

Piste jamais réalisée EN NAVIGATEUR : vérifier sur le DOM hydraté que
(1) chaque `<a href>` interne des 8 espaces résout en HTTP 200, et
(2) chaque `<button>` porte un câblage détectable. Les gardiens
existants vérifient la source servie ; ici on mesure ce que voit
réellement l'utilisateur après hydratation JS.

## Protocole

Serveur `DEMO=1 NO_IBKR=1` (healthz `ok/demo`) ; Playwright Chromium
1440×900 (domcontentloaded + 4500 ms) sur `/`, `/markets`,
`/opportunities`, `/portfolio`, `/journal`, `/options`, `/system`,
`/tracking`. Extraction du DOM :

- tous les `a[href]` internes (dédupliqués, ancres retirées) → GET
  réel sur chaque cible, statut attendu 200 ;
- tous les `button` → câblage détecté si `onclick` (propriété ou
  attribut), attribut `data-*`, `type="submit"`, ou `aria-controls`.

## Résultat — 0 défaut

| Mesure | Valeur |
|---|---:|
| Liens internes uniques trouvés | **31** |
| Liens en erreur (≠ 200) | **0** |
| Boutons inventoriés (8 pages) | **177** (18+55+39+12+10+20+13+10) |
| Boutons sans câblage détectable | **0** |

Chaque bouton des 8 pages porte au moins un vecteur de câblage
explicite (onclick / data-* pour les délégués globaux / submit /
aria-controls) — cohérent avec l'architecture des délégués clavier et
clic posés aux lots précédents.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : constat pur.

## Preuves

- JSON complet du balayage (31 liens × statut, 177 boutons × page)
  produit par le protocole ci-dessus ; synthèse dans ce rapport.
- Suite complète : **2482 passed / 2 skipped** (référence maintenue).

## Suite

LOT 222 : entretien suivant utile ou directive. Purge terminal.py
toujours EN ATTENTE d'accord humain explicite.
