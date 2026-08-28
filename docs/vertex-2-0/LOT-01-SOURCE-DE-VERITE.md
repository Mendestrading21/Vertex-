# Lot 1 — Source de vérité visuelle

## Ce qui change

Une **couche de vérité unique** est posée au-dessus des quinze feuilles existantes
plutôt qu'à leur place : `vertex/static/vertex/css/vertex-2-0.css`, chargée en
dernier, après `glass.css`.

Elle redéfinit les jetons `--vx-*` que les pages consomment **déjà**. Résultat :
l'identité change sans qu'une seule page ne modifie son balisage, et les alias
historiques restent valides tant que leurs consommateurs n'ont pas migré —
exactement ce que le lot 1 demande.

### Jetons de rôle 2.0

`--vx-night` `--vx-shell` `--vx-graphite` · verre `subtle`/`card`/`raised` ·
`--vx-ink` `--vx-silver` `--vx-mist` `--vx-smoke` · sémantique `--vx-positive`
`--vx-negative` `--vx-caution` `--vx-options` `--vx-analysis-light`.

`--vx-info`, `--vx-blue` et `--vx-cyan` retombent sur l'argent : **aucun bleu
identitaire ne peut plus apparaître**, même si une page ancienne les invoque.
La marque est l'argent ; le vert ne porte jamais l'identité, seulement le positif réel.

### Typographie

Geist (interface) et Geist Mono (prix, tickers, pourcentages, mesures), variables,
**auto-hébergées** — aucune requête externe, le produit reste utilisable hors ligne.
General Sans et JetBrains Mono restent chargées comme repli.

`font-variant-numeric: tabular-nums` est appliqué à toute valeur dynamique et à
toutes les cellules de tableau : les colonnes de chiffres ne « sautent » plus
quand une valeur change.

### Decision Trace — la signature

`Donnée → Moteur → Décision → Portefeuille`, reliés par une hairline argent.
La couleur n'apparaît **qu'au nœud qui porte réellement ce sens** ; un nœud neutre
reste argent.

La contrainte des cinq emplacements canoniques n'est pas une consigne écrite dans
un document : elle est **imposée par le code**. `vx2.decision_trace()` lève une
`ValueError` si l'emplacement demandé n'appartient pas à `TRACE_EMPLACEMENTS`.
Une sixième surface décorative est donc impossible à livrer par inadvertance.

## Primitives — `vertex/ui/vx2.py`

Propriétaire visuel unique de la refonte. Une classe `.vx2-*` n'est écrite que là,
jamais dans une page.

`valeur` `badge_etat` `estampille` `decision_trace` · `page_header` `context_bar`
`section` `surface` · `metric` `metric_strip` · `etat` `bandeau` `capacite_absente`
· `table` `rowcard` `chart_card` · `bouton` `chip` `tabs` `champ`.

**Le module ne calcule rien.** Il met en forme des valeurs déjà produites par les
moteurs. `valeur(None)` rend `—` en gris : jamais `0`, jamais une couleur
directionnelle, jamais complétée. `capacite_absente()` existe précisément pour
qu'une maquette réclamant un calcul inexistant produise un aveu plutôt qu'un
chiffre fabriqué dans un template.

`badge_etat()` écrit **toujours le mot** (« Temps réel », « Différée », « Périmée »,
« Démo », « Hors ligne », « Partielle », « Indisponible », « Erreur ») : la pastille
de couleur ne fait que redoubler une information déjà lisible, jamais la porter
seule.

## Deux défauts corrigés après lecture de la capture

Le premier rendu de la galerie a montré ce qu'aucune relecture de CSS n'aurait donné :

1. **Les nœuds de la Decision Trace se collaient** — « DONNÉEIndisponiblesource — ».
   Les trois `span` du corps étaient en ligne ; `.vx2-trace-body` manquait sa
   règle `flex-direction:column`. Corrigé, puis recapturé.
2. **La colonne clé collante laissait une couture** — le conteneur de table était
   en verre translucide ; une colonne collante doit masquer ce qui défile dessous.
   Le fond de table est passé en **opaque** (`--vx-surface-base`), ce qui sert
   aussi la lisibilité d'une table financière dense.

## Service worker

`td-shell-v219` → **`td-shell-v220`**. La coque servie charge une feuille et deux
polices nouvelles ; sans bump, un visiteur déjà en v219 garderait l'ancienne
identité en cache. `vertex-2-0.css` et les deux `.woff2` Geist sont ajoutés au
précache (contrôle 146).

Les six gardiens qui épinglent la version ont été mis à jour dans le même commit,
empreinte `/static` comprise — c'est ce que `test_sw_cache_scope_lot361` exige,
et il le dit lui-même dans son message d'échec.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4246 passés**, 154 ignorés, 1 échec environnemental connu |
| Console navigateur | 0 erreur sur `/`, `/options`, `/portfolio`, `/design-system` |
| Débordement horizontal | 0 px, desktop **et** mobile, sur les 4 routes |
| Captures | `docs/vertex-2-0/preuves/lot-01-apres/` |

Galerie complète des primitives : `/design-system` → section « Vertex 2.0 —
Black Glass, Signal Light » (capture `design-system-galerie-2-0.png`).

## Limites

- Geist est chargée en **variable** : les graisses 100–900 viennent d'un seul
  fichier par famille. Aucune face italique n'est embarquée — le produit n'en
  utilise pas.
- Les quatre familles de tuiles historiques (`vx-kpi`, `vx-metric`, `vx-stat`,
  `vx-stat-xl`) sont **visuellement** unifiées par le remappage des jetons mais
  leurs classes existent encore. Leur retrait appartient au lot 14, après
  migration du dernier consommateur.

## Rollback

Retirer la ligne `vertex-2-0.css` de la coque suffit à revenir à l'identité
précédente : la couche est purement additive et ne supprime aucun jeton.
