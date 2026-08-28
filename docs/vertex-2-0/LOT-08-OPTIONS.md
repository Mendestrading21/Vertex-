# Lot 8 — Options

## Le dossier par sous-jacent était inaccessible

`CLAUDE.md` documente une collision de route connue :

> **Collision de route connue** : `/options/<sym>` est déclaré 2× (JSON `opt_ep`
> terminal.py + page `redesign.py`). Toute intervention options doit dédupliquer,
> pas aggraver.

Ce que la documentation ne disait pas, c'est **qui gagne**. Mesuré :

```
GET /options/AAPL  →  200, 575 octets, Content-Type JSON
{"beta":null,"call_wall":null,"contracts":[],"error":"TypeError: …
```

C'est le JSON qui gagne. La page du dossier options — celle qui porte la
**chaîne CALL / strike / PUT**, que le contrat appelle « la table spécialisée
principale » — n'a donc **jamais été servie**.

### Neuf liens internes déversaient du JSON brut

| Fichier | Contexte |
|---|---|
| `briefing.py` | tuile « Dossier options » d'Aujourd'hui |
| `analysis_page.py` × 3 | bascule Action/Options du dossier, « Dossier options complet », « Ouvrir le dossier options » |
| `opportunities_page.py` × 4 | quatre boutons « Options » du screener et de Positions × moteur |
| `inspector-drawer.js` | bouton « Options » du drawer d'entité |

Chacun de ces neuf liens ouvrait une page de JSON brut. Ce n'est pas un défaut
visuel mineur : c'est un cul-de-sac au milieu du parcours d'analyse.

### La correction, et sa limite

Supprimer l'endpoint JSON serait une modification de **backend**, hors du
périmètre de cette refonte. La page reçoit donc une URL qui lui appartient —
`/options/dossier/<sym>` — et les neuf liens la suivent. `/options/<sym>` reste
servi **à l'identique** pour ses éventuels consommateurs.

**Besoin hors périmètre consigné :** dédupliquer la route côté backend et rendre
`/options/<sym>` à la page. Le JSON est déjà servi sous `/api/options/chain/<sym>`
et `/api/options/chain-grid/<sym>` — l'endpoint historique fait doublon.

## La chaîne est enfin joignable depuis l'espace Options

Le contrat fait de la chaîne la table principale des Options. Elle existait, dans
le dossier par sous-jacent, mais **rien dans l'espace Options n'y menait**.

Un bouton la rend joignable depuis le sélecteur de sous-jacent, et **suit le
symbole actif** :

- sans symbole → « Choisir un sous-jacent pour ouvrir sa chaîne », **désactivé**,
  sans `href`. Un lien qui mènerait à une 404 est pire qu'un lien absent ;
- avec symbole → « Ouvrir la chaîne de AAPL → » vers `/options/dossier/AAPL`.

Vérifié en pilotant le navigateur : saisie du symbole → clic → la page HTML du
dossier s'ouvre, `0` erreur.

## Trois états malhonnêtes, corrigés au lot précédent

Rappel, car ils appartiennent à cette page : la vue Structure portait un
**squelette perpétuel** (`#vx-os-verdict`, jamais rempli faute de sous-jacent),
un **« — » nu** pour les sensibilités, et un raccourci « Depuis le tableau : »
suivi de **rien** quand la chaîne n'est pas alimentée. Les trois portent
désormais leur cause.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4266 passés**, 154 ignorés, 1 échec environnemental connu |
| `/options/dossier/AAPL` | page HTML, 23 614 octets, grille de chaîne câblée |
| Lien de chaîne | vérifié au navigateur, bout en bout |
| Balisage servi | **0 anomalie** sur 17 routes |
| Blocs vides | 0 |
| Console | 0 erreur page |

Service worker `v228` → **`v229`**.

## Limites

- La chaîne ne rend aucun contrat ici : les sources de marché sont injoignables,
  et `/options/dossier/<sym>` affiche donc ses états honnêtes. Le rendu de la
  grille CALL/strike/PUT alimentée reste à vérifier sur une machine connectée.
- Les sous-vues **Vue d'ensemble**, **Radar contrats** et **Scénarios** restent
  servies mais hors barre d'onglets (`_LEGACY_VIEWS`), absorbées par Structure.
  Ce choix précède la refonte et n'a pas été rouvert.
- Term structure, smile/skew, OI/GEX et le drawer contrat (contrôles 079 à 081)
  ne sont pas refondus.

## Un flake pré-existant, observé

`test_scan_cache::test_scan_response_cache_gzip_etag_304` a échoué une fois dans
la suite complète, puis passé isolément **et** à la relance complète suivante.
Dépendance d'ordre sur l'état de cache partagé, indépendante de ce lot. Noté, non
corrigé — ce n'est pas le périmètre visuel.
