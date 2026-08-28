# Lots 17-20 — Analyse, Options/Simulateur, Portefeuille/Suivi/Performance, Vertex IA/Système : VÉRIFICATION (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Protocole

8 pages restantes vérifiées au navigateur réel (1600 px, pleine page,
console, jetons anglais, langage d'ordre) + dossier `/analysis/NVDA`
(position déclarée). Captures dans ce dossier.

## Conformités mesurées (aucun défaut)

- **Simulateur** : hypothèses visibles, « Vertex ne transmet aucun ordre »,
  table de prise en charge par classe (Options/Actions complètes, ETF
  partielle — look-through non simulé DIT, Forex déclarée absente).
- **Performance** : populations séparées (5 cartes avec source chacune,
  « un indicateur ne mélange jamais deux de ces lignes »), échelle de
  déblocage du track record (0/5 trades), « calcul non disponible dans
  Vertex » nommés.
- **Suivi** : nature du rendement « Hypothétique — jamais encaissé »,
  renvois aux propriétaires canoniques sans recopie.
- **Options** : chaîne grisée sans donnée, aucune Greek estimée en
  l'absence de contrat.
- **Analyse (dossier NVDA)** : refus structuré « Vertex ne tranche pas »,
  DecisionTrace, fondamentaux en `—`.

## Défauts trouvés et corrigés (4)

1. **[object Object] à l'écran** (Analyse) : « Médiane sectorielle P/E »
   rendait l'objet entier quand `sector_median` était un dict vide
   (`median_pe ?? t.sector_median`). → valeur numérique seule, sinon n/d.
   `tests/test_mediane_sectorielle_lot17.py`.
2. **Badge de santé sur-affirmant** (Système) : « Opérationnel ·
   8 moteurs » (vert) pendant que la jauge disait 0/8 — le badge lisait
   /healthz (sonde de VIE, status='ok' par conception) et comptait des
   moteurs DÉCLARÉS. → il lit `/readyz` (vérifications réelles) : « Prêt ·
   4/4 vérifications » mesuré en direct. `tests/test_badge_sante_lot20.py`.
3. **Légende de treemap mensongère** (Portefeuille) : pavé NVDA rouge
   (repli concentration 100 % — sain) sous une légende « couleur = P&L
   latent … gris sans marque ». → la légende déclare les deux encodages.
   `tests/test_legende_treemap_lot19.py`.
4. **Violet hors options** (Vertex IA) : l'encart `data-tone="ai"` portait
   `--vx-option` via glass.css. → la couche finale (vertex-2-0.css) le
   ramène à l'argent structurel ; mesuré rendu : rgb(201,206,216).
   `tests/test_ton_ia_palette_lot20.py`.

Service worker **v267** ; gardien d'empreinte /static remis à jour dans le
même commit (`test_sw_cache_scope_lot361`). Les 4 correctifs vérifiés EN
DIRECT au navigateur après redémarrage, console vide.

## Preuves

- 4 bancs nés rouges → verts ; suite complète : **4373 passés · 153
  ignorés · 0 échec**.
- Captures : 9 PNG pleine page.

## Limites consignées

- Environnement sans réseau sortant : pages vérifiées en mode dégradé
  (données absentes honnêtes) ; les vues peuplées restent à re-vérifier
  sur scan réel à l'acceptation (contrôle 150).
- Lot 21 (responsive complet 390→1600, clavier, zoom 200 %, reduced
  motion, Lighthouse) : à exécuter comme lot dédié.

## Rollback

`git revert` du commit du lot.
