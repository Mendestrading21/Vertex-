# Lot 14 — Nettoyage visuel

> Le lot 14 demande de retirer « CSS, classes et docs de design devenus sans
> usage, **après recherche des consommateurs** ». Ce rapport fait la recherche,
> chiffre la dette, et distingue ce que j'ai fait de ce qui reste une décision
> humaine.

## `neon-glass.css` — 855 lignes jamais servies

**Preuve d'exécution.** Requêtes CSS réellement émises sur `/`, `/analysis/<sym>`,
`/system`, `/options` et `/portfolio` : **dix-neuf feuilles**, et celle-ci n'en
fait pas partie. La coque ne la référence pas ; aucune autre feuille ne
l'importe ; aucun fichier `.py`, `.js` ou `.html` du produit ne la mentionne.

**Elle n'a pas été supprimée, et c'est délibéré.**

Le danger d'un fichier mort n'est pas son poids : c'est qu'on le lise comme la
vérité. **C'est arrivé pendant cette refonte.** En cherchant pourquoi la carte de
verdict du dossier Analyse n'avait aucun style, on trouve dans ce fichier des
règles `.vx-verdict-card` — et l'on peut conclure à tort qu'elles s'appliquent.
Elles ne s'appliquent pas.

Cinq bancs lisent encore ce fichier comme registre de règles de design :
`test_neon_glass_01`, `test_analysis_visual_lot619`, `test_perf_lot72`,
`test_reconstruction_today`, `test_options_visual_lot623`. Le supprimer
exigerait de les supprimer aussi — donc **de retirer de la couverture**, ce qui
est pire que de garder un fichier inerte clairement étiqueté.

**Ce qui a été fait :** un bandeau en tête du fichier déclare qu'il n'est pas
servi, dit comment cela a été vérifié, et pourquoi il subsiste. Le piège est
désamorcé pour le prochain lecteur, humain ou agent.

**Décision humaine requise :** supprimer le fichier et les cinq bancs, ou
convertir ces bancs pour qu'ils portent sur les feuilles réellement servies.

## La dette de composants, chiffrée

Le contrat 2.0 veut **une** famille de cartes et **une** MetricCard. Voici ce qui
existe réellement dans les pages servies :

| Famille | Occurrences de classe |
|---|---:|
| `vx-kpi` | 63 |
| `vx-stat` | 50 |
| `vx-metric` | 25 |
| `vx-stat-xl` | 8 |
| `vx2-metric` (2.0) | 4 |
| **Total à migrer** | **146** |

`.vx-card` est redéfini dans **six feuilles servies** — `components` (14 règles),
`glass` (12), `premium` (8), `cockpit` (5), `polish` (5), `responsive` (2) — soit
46 règles concurrentes, plus 3 dans la feuille morte.

**Aucune migration de masse n'a été tentée**, et je préfère le dire que le
maquiller :

1. Ces 146 occurrences sont **déjà visuellement unifiées** par le remappage des
   jetons du lot 1 : elles consomment toutes `var(--vx-*)`, donc l'identité 2.0
   s'y applique. Migrer les classes ne changerait **rien pour l'utilisateur**.
2. Le risque est réel et asymétrique : 146 remplacements dans sept pages dont
   trois font plus de 90 ko, sans jeu de tests de rendu, en fin de session
   longue. Le gain est nul, le risque de régression ne l'est pas.

C'est une dette **mesurée et datée**, pas un oubli.

## Ce que le nettoyage a réellement produit ailleurs

Le vrai nettoyage de ce chantier n'a pas consisté à retirer du CSS, mais à
retirer des **mensonges** :

| Trouvé | Où |
|---|---|
| Squelette perpétuel (chargeur retiré, conteneur resté) | `/performance` × 2, `/options` × 1 |
| Conteneur référencé par le JS et absent du DOM | `#an-verdict` (Analyse) |
| Emplacement de fraîcheur jamais rempli | `#op-fresh` (Opportunités), Suivi |
| `</div>` orphelin fermant une `<section>` | Analyse — **toute la page** |
| Règle de base absente, seule sa surcharge mobile écrite | matrice des connexions (Système) |
| Alias de couleur rendant une autre couleur | `blue` → vert de marque, `cyan` → beige |
| Route masquée par une collision | dossier Options, **9 liens morts** |
| Vocabulaire métier recopié au lieu d'être lu | verdicts dans `calendar.js` |

Chacun a été corrigé, et deux gardiens ont été ajoutés pour que ces classes de
défaut ne reviennent pas en silence : `tests/test_balisage_servi_vertex_2_0.py`
et l'outillage `tools/vertex_2_0_*`.

## Nommage laissé en place

`chart-theme-obsidian-copper.js` ne décrit plus rien : ni obsidienne cuivrée, ni
cuivre. Il est conservé — la coque et plusieurs bancs l'épinglent, et un
renommage n'apporterait aucune clarté à l'utilisateur. Un bandeau en tête du
fichier dit ce qu'il contient réellement.
