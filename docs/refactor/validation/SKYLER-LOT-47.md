# SKYLER V2 — LOT 47 : bouton Importer + empreinte stable au round-trip JS

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-47-import-button`
(base : `integration/vertex-skyler-v2` @ `e9db87a`, fraîchement fetchée —
leçon du lot 46 appliquée) · Mode : développement continu.

## 1. Choix du lot — justification

La restauration souveraine (lots 45/46) existait en API seulement — le
trader devait utiliser curl pour restaurer sa sauvegarde. Le bouton
« Importer » ferme le cycle côté produit : Exporter et Importer côte à
côte dans la carte Mémoire.

## 2. Périmètre livré

### 2.1 UI — carte Mémoire

- bouton fantôme « Importer ← » à côté d'« Exporter → » (label + input
  file caché, `accept=.json`) ; sous-titre mis à jour (« l'import
  restaure par rejeu — la donnée locale gagne toujours ») ;
- câblage JS (`wireMemoryImport`, garde anti-double-wiring) : FileReader
  → `JSON.parse` (fichier illisible → message négatif honnête) → POST
  `/api/skyler/memory/import` → **affichage honnête des DEUX chemins** :
  succès = stats exactes par magasin (« X ajoutée(s), Y déjà
  présente(s) (la donnée locale gagne) … entrées corrompues ignorées :
  N — ledger : SAIN ») + rechargement de la carte ; échec = l'erreur
  structurée du serveur affichée TELLE QUELLE (jamais maquillée) ;
- XSS : tout contenu serveur affiché passe par `esc()` ; aucune
  apostrophe française brute dans la chaîne JS (entités HTML).

### 2.2 DÉFAUT RÉEL attrapé par la preuve navigateur — et corrigé

Premier essai réel (upload du bundle INTACT via le bouton) : **« Import
refusé — empreinte_invalide »**. Cause : `JSON.stringify` replie les
flottants entiers (`100.0` → `100`) — l'empreinte canonique Python ne
matchait plus après le round-trip navigateur. Les tests Python (lots
42/45/46) ne pouvaient pas le voir : le client de test Flask préserve
`100.0`.

Correctif : **`_canonical_bundle_json`** (source unique export + import)
normalise les flottants entiers en entiers avant l'empreinte ; la `note`
du bundle documente la recette (« 100.0 ≡ 100 ») ; les tests de
vérification hors ligne du lot 42 sont alignés sur la recette ; test
rouge dédié `test_import_survives_js_number_roundtrip` (simulation du
round-trip JS) — rouge confirmé puis vert.

### 2.3 Service worker

Shell visible → **SW v106 → v107** + 4 gardiens.

## 3. Méthode — rouge d'abord

`tests/test_import_button_lot47.py` (5 tests) : 4 rouges initiaux
(bouton, câblage, deux chemins de résultat, SW) + 1 rouge du défaut JS
attrapé en preuve navigateur. Tous verts après ; les 22 tests
export/import des lots 42/45/46 restent verts (27 au total).

## 4. Preuves

```text
python -m pytest tests/test_import_button_lot47.py tests/test_export_integrity_lot42.py \
  tests/test_sovereign_import_lot45.py tests/test_import_full_lot46.py -q → 27 passed
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1627 passed, 2 skipped (baseline 1622 → +5)

Navigateur (serveur DEMO, VRAI fichier d'export uploadé via le bouton) :
  avant correctif : « Import refusé — empreinte_invalide »  ← DÉFAUT RÉEL
  après correctif : « Restauration terminée — décisions : 0 ajoutée(s),
    3 déjà présente(s) (la donnée locale gagne) · séances : 0 · journal :
    0 — ledger : SAIN » · console_err=0

tools/rc_short_audit.js : 8 pages · client-log 0 · sw.js td-shell-v107
  RC COURTE : GO — 0 défaut.
```

Moteur 0.9.0 inchangé.

## 5. Invariants tenus

- résultat honnête dans les deux sens (stats exactes / erreur serveur
  telle quelle) ; la donnée locale gagne (visible dans le message) ;
- empreinte STABLE au round-trip JS, recette documentée dans le bundle
  même ; source unique de canonicalisation (export + import) ;
- XSS échappé ; apostrophes en entités ; SW v107 + 4 gardiens ; preuve
  navigateur exécutée ET décisive (défaut réel attrapé avant livraison) ;
- READONLY absolu ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog (candidats lot 48)

1. Toute amélioration constatée pendant le travail ;
2. RC périodiques espacées si le backlog code s'épuise à nouveau.

**Arrêt après ce lot — validation humaine requise.**
