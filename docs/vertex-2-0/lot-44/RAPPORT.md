# Lot 44 — La taille des graphiques est gérée, plus improvisée (RAPPORT)

Date : 2026-08-28 · Demande utilisateur : « gère la taille des graphiques
widgets ».

## Constat

Chaque page inventait ses pixels (recensés : 140, 150, 220, 230, 240, 260,
320, 360…) et le corps de graphique portait un `height` inline que la
feuille ne pouvait pas moduler. En mobile, une carte « hero » de 360 px
occupait la quasi-totalité du viewport d'un téléphone.

## Livré

1. **Échelle nommée** — `C.TAILLES = {xs:120, s:160, m:200, l:240, xl:300,
   hero:360}` et `C.card` accepte `size:` ; `height:` numérique reste
   accepté (compat totale — prouvé au navigateur : ancien inline et
   nouvelle forme rendent un calcul IDENTIQUE au pixel près).
2. **La feuille reprend la main** — le corps émet `--vx-chart-h` et lit sa
   hauteur de la variable (C.card + le corps posé à la main
   d'options-intel).
3. **Borne mobile** (≤ 640 px) — `max-height:min(var(--vx-chart-h),58vw)`,
   scopée `[style*="--vx-chart-h"]` :
   - `max-height`, pas `height` : dans une carte flex, seul un min/max
     borne la taille servie par l'algorithme flex — un height, même
     `!important`, ne plafonne pas un item qui grandit (mesuré au
     navigateur pendant ce lot) ;
   - scopée aux corps OPTÉS : les hauteurs épinglées par id (`#an-chart`,
     260 px, lot 620) gardent leur contrat ;
   - le plein écran survit — son `min-height:62vh` bat un max-height
     inférieur (règle CSS min > max).

Service worker **v281**, épingles + empreinte /static suivies (outil
`vertex_2_0_bump_sw.py`).

## Preuves

- `tests/test_tailles_graphiques_lot44.py` — 6 gardiens (échelle déclarée,
  résolveur, variable émise des deux côtés, borne max-height scopée, plein
  écran préservé). Rouge d'abord.
- Navigateur, 375 px : carte `size:'hero'` → `--vx-chart-h:360px`,
  `max-height` calculé **217,75 px** = min(360, 58vw). Desktop : calcul
  identique à l'ancienne forme (aucun changement visuel).
- Suite complète : **4443 passés · 173 ignorés · 0 échec**.

## Dette résiduelle (dite)

Les pages continuent de passer des pixels historiques (`height: 240`) ;
l'échelle `size:` est disponible pour les prochains graphiques mais la
migration des ~20 sites d'appel vers les gabarits nommés n'a pas été forcée
ici — elle changerait des hauteurs mesurées par les bancs visuels et mérite
son propre passage avec captures avant/après.
