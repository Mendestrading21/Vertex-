# SKYLER V2 — LOT 189 : TOURNÉE GRAPHIQUE TV — fondation + jauge

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-189`
(base : `integration/vertex-skyler-v2` @ `2f9eef4`, lot 188 fusionné).
Lot UI (directive utilisateur : « tout Vertex doit ressembler à ça —
fluide, beau, parfait », captures TradingView à l'appui, confirmée en
cours de lot). Moteurs INTACTS, READONLY intact.

## 1. Livré

```text
INVENTAIRE — docs/refactor/validation/TV-CHARTS-INVENTORY.md : tous
  les graphiques vivants par page, ordonnés par visibilité, avec
  statuts ☐/◐/✔ et le plan des prochains lots.
GRAMMAIRE TV (chart-core.js) :
  · C.gauge REFAIT style TradingView — l'arc ENTIER est un dégradé
    CONTINU construit sur les couleurs des bandes (rouge→jaune→vert,
    fondues aux frontières), pointeur BLANC court posé sur l'arc
    (jamais sur le texte central — ajusté après 1re capture), halo de
    zone, libellés de bandes au fil de l'arc, grand chiffre blanc +
    unité, ÉTAT coloré en évidence sous l'arc (« Volatilité
    comprimée… » en vert, comme le « Strong Buy » TV). API 100 %
    compatible : les 6 appelants (Marchés ×3, Portefeuille, Système,
    Intelligence, options-intel) héritent sans changement.
  · C.tvHatch(id,color) — pattern SVG hachuré « estimation » (les
    zones prévisionnelles des prochains lots).
  · C.tvEdgeChip(x,y,text,color) — chip d'étiquette de bord
    (Max/Moy/Min/Actuel du cône de prix cible à venir).
SW v152 → v153 + 4 gardiens de version (+ lot187 ajusté).
```

## 2. Accros rencontrés (dits)

Les gardiens couleur (lots 51-53/61/62) ont refusé mes fallbacks
successifs `#080808` puis `#0c0c0e` (hors inventaire figé) →
remplacés par `var(--vx-graphite-850,#121214)`, autorisé partout.
Le gardien a fait exactement son travail.

## 3. Preuves

```text
node --check chart-core.js → OK
Serveur DEMO port 5002 · captures Playwright 1440/390 :
  Marchés/Breadth (jauge 50 % « Participation moyenne » jaune),
  Marchés/Volatilité (VIX 12.7 pointeur en zone verte, état
  « Volatilité comprimée — primes bon marché » en vert), 0 erreur
  console — captures ENVOYÉES à l'utilisateur.
python -m pytest tests/ -q → 2461 passed, 2 skipped (gardiens
  couleur + SW v153 inclus)
```

## 4. Suite

LOT 190 : cône de projection du plan de trade (Analyse) — l'éventail
min/moy/max style prix cible TV, nourri par les niveaux RÉELS du
moteur (entrée/stop/TP1-3), avec tvEdgeChip — + zones hachurées
d'estimation + MINI-BILAN 186-190.
