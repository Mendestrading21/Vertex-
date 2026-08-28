# Lots 15 à 17 — Portefeuille, Performance, Marchés

Les trois pages que la première livraison avait laissées en l'état : elles
héritaient de l'identité 2.0 et passaient tous les contrôles transverses, mais
leur hiérarchie d'information n'avait pas été retravaillée.

Toutes trois ont livré la même surprise que les lots 7 à 14 : le travail n'a
presque pas consisté à décorer, mais à **découvrir que des blocs entiers ne
fonctionnaient pas**, sans qu'aucun contrôle existant puisse le dire.

---

## Lot 15 — Portefeuille

### Deux sous-vues du contrat n'existaient pas

`portfolio-center.md` réclame Synthèse, Positions, **Allocation**, Options,
Risque, **Thèses**. La page servait Synthèse, Positions, Performance, Risque,
Options, Watchlist.

**Allocation.** `/api/portfolio/context` calculait déjà, et depuis longtemps,
les poids par titre, le HHI, le mix par type d'actif, le mix sectoriel avec sa
couverture, le budget de risque au stop et les expositions factorielles. **Un
seul** de ces chiffres était affiché — au fond d'un `<details>` de la vue
Risque. La sous-vue les montre tous, et n'en recalcule aucun.

**Thèses.** `thesisState()` classait chaque position en six états honnêtes —
« Cassée — invalidation atteinte », « Fragilisée », « Renforcée par les
faits »… — et ne servait qu'à colorer une pastille dans un tableau. Le texte de
la thèse ne se lisait qu'au survol d'un attribut `title`. La sous-vue ouvre
thèse, invalidation, distance à l'invalidation, objectif, catalyseur et
prochaine action analytique.

`?view=watchlist` reste une URL valable : elle mène à Thèses.

### Quatre axes déclarés absents

Le contrat réclame six axes d'exposition. Vertex en calcule deux. Devise, pays,
thème et look-through ETF sont **déclarés absents**, jamais simulés.

### Défauts vus en pilotant, pas en relisant

| Défaut | Ce que l'utilisateur voyait |
|---|---|
| `VX.freshness.assess({ageMs:null})` rend l'état `unknown`, dont le libellé **est** « — » | Un tiret nu à côté d'un bouton, ne nommant ni sa grandeur ni son absence |
| `allocBars` suffixait « % » en dur | Le budget de risque, en dollars, s'affichait **« 3280,0 % »** |
| Une part de 0,03 % s'arrondissait à « 0,0 % » | Un zéro de façade pour une ligne qui existe — désormais « < 0,1 % » |
| Le treemap laisse tomber les tuiles trop petites | Troncature muette, lue comme « tout le portefeuille est ici ». Elle est nommée sous le graphique |
| `data-variante="primaire"` ne désigne aucune règle CSS | Le bouton principal n'était pas distingué (la classe réelle est `vx2-btn--primary`) |
| `.vx2-rowcard` vit dans `.vx2-rowcards`, en `display:none` au-dessus de 760 px | La carte de thèse **aurait disparu sur desktop**. Piège évité avant la première capture |
| Deux jetons inventés en écrivant la CSS (`--vx-hairline`, `--vx-fs-sm`) | Ne sont définis nulle part — remplacés par les jetons réels |

### Le desk n'a pas été écrit

Le garde-fou du dépôt refuse d'écraser `desk_data.json` — à raison. Les vues
peuplées sont pilotées autrement : la sortie **réelle** de `portfolio_context`,
calculée hors ligne sur un portefeuille fictif, est servie au navigateur, et les
positions sont posées dans le `localStorage`. Aucune valeur n'est écrite à la
main ; `desk_data.json` est resté à ses 48 octets.

---

## Lot 16 — Performance

### Trois chargeurs définis, zéro appel

`loadKpis`, `loadEquity` et `loadMonthlyAndDist` étaient orphelins depuis le
retrait de `loadDiscipline()` de l'orchestration.

- `#vx-pf-kpis` gardait son squelette **indéfiniment** — un cinquième squelette
  perpétuel, après les quatre du lot 14.
- `vx-pf-equity`, `vx-pf-drawdown` et `vx-pf-monthly` n'existaient dans le DOM
  d'**aucune** vue : les chargeurs écrivaient dans le vide.
- `heatmap.js`, `equity-chart.js` et `drawdown-chart.js` n'étaient pas servis
  sur cette page. `VXCharts.heatmapCard` restait `undefined`.

### Une fonction qui levait, sans que personne le sache

Le corps de `loadDiscipline()` avait été collé **dans** `loadMonthlyAndDist`,
après son retour anticipé. Avec trois clôtures ou plus, elle levait
`b is not defined` — `b`, `hero` et `next` n'étaient déclarés dans aucune
portée — et n'avait de toute façon plus **une seule ligne** dessinant la
heatmap qu'elle était censée produire.

Invisible, parce que personne ne l'appelait. L'erreur n'est apparue qu'après
avoir rebranché la fonction **et** peuplé la page.

### Une garde muette

```js
window.addEventListener('load', fn, {once:true})
```

Après que `load` a déjà tiré — ce qui est le cas de tout rendu différé — ce
rappel n'est **jamais** rejoué. Deux blocs s'y fiaient pour attendre un script
`defer` : ils attendaient pour toujours, sans rien dire. La garde sonde
désormais, puis **avoue** si la bibliothèque n'arrive pas.

### Les cinq populations

Le contrat interdit de fusionner cinq populations dans un même indicateur.
Elles sont nommées côte à côte, chacune avec sa nature de résultat, sa source
et son propriétaire :

| Population | Nature | Mesurée |
|---|---|---|
| Trades réels déclarés | Réalisé — encaissé | **ici** |
| Positions IBKR | Latent — non encaissé | Portefeuille |
| Signaux théoriques moteurs | Théorique — aucun capital engagé | **ici** (Historique) |
| Idées suivies | Hypothétique — jamais encaissé | Suivi |
| Simulations options | Scénario — hypothèses explicites | **non conservée** |

La ContextBar dit laquelle les indicateurs de la page mesurent, et avec quel
échantillon : un taux de réussite sans son `n` ne dit pas s'il vaut quelque
chose.

### La heatmap mensuelle est déclarée absente

Son code de rendu n'existe plus. La réécrire supposerait d'agréger des
rendements par mois **dans l'UI**, ce que `performance-center.md` interdit
explicitement. Elle est avouée, pas fabriquée.

---

## Lot 17 — Marchés

### La feuille morte a enfin causé un dégât visible

`neon-glass.css` — 855 lignes jamais servies, étiquetées au lot 14 comme dette
sans conséquence — portait les **seules** règles de la pastille de régime.
Sans elles, la Synthèse affichait :

> Régime non qualifié Lecture du marché en cours — moins de 3 dimensions…

Une phrase incohérente, produite par un style absent. La règle est rapatriée
dans la couche canonique. C'est le premier dommage **mesuré** de cette feuille ;
jusqu'ici, elle n'avait qu'induit en erreur pendant la refonte elle-même.

### Un troisième tiret nu, corrigé à la racine

`VX.updateIndicator(null, …)` rendait « ● — · Moteur de régimes Différé » :
`VX.fmt.ago(null)` renvoie « — », et ce tiret, posé à l'emplacement d'un âge,
**se lit comme un âge**. Impossible de savoir si la donnée est fraîche, vieille,
ou jamais horodatée.

Corrigé dans le helper partagé — « Âge inconnu » — après l'avoir corrigé deux
fois localement aux lots 15 et 16. Les douze pages ont été revérifiées après ce
changement global.

### Libellés et sous-vue canoniques

`Breadth` était le seul mot anglais de la barre d'onglets, alors que le corps de
la page écrivait déjà « Participation → » pour désigner la **même** sous-vue.
`Vue d'ensemble` devient `Synthèse`.

`Indices & cross-asset`, que le contrat réclame, existait déjà : ses trois blocs
vivaient repliés dans un `<details>` de la Synthèse. Ils ont leur sous-vue et
leur URL partageable ; la Synthèse **dit où ils sont partis** — un déménagement
muet est une perte.

---

## Bancs mis à jour, pas écartés

Cinq bancs décrivaient le balisage modifié. Aucun n'a été ajouté au registre
`_supersede` : leur intention reste valable, seul le balisage a changé.

| Banc | Ce qui change | Ce qui est garanti |
|---|---|---|
| `test_journal_routes_200` | `<h1>` porte la classe `vx2-title` | La page porte bien son titre |
| `..._lot624` · discipline | Nouveau conteneur `vx-pf-discipline` | Les mesures de discipline **n'écrasent plus** la bande des résultats déclarés — deux populations au même emplacement |
| `..._lot624` · chronologie | Libellé `Journal` (canonique) | Même sous-vue, même URL |
| `..._lot621` · Marchés Synthèse | Blocs déplacés vers `indices` | **Plus fort qu'avant** : le banc vérifie qu'ils ne sont ni restés, ni perdus, et que la Synthèse pointe vers eux |
| `..._lot621` · Marchés Volatilité | En-tête `vx2.page_header` | La page porte un en-tête canonique et sa question métier |

---

## Preuves

```
0 anomalie de balisage        Portefeuille ×3, Performance ×5, Marchés ×6
0 bloc vide                   13 routes
0 défaut d'accessibilité      12 pages × 2 viewports
0 débordement horizontal      8 largeurs, zoom 200 % inclus
0 erreur console              12 pages, vides ET peuplées
```

Suite complète : **4266 passés**, 154 ignorés, 1 échec **environnemental**
(`test_la_classification_est_discriminante` exige > 100 références git ; ce
clone en porte 3 — il passe sur la CI, qui dispose du dépôt complet).

Service worker `v232` → `v235`.

## Périmètre respecté

Aucun moteur, formule, score, gate, verdict, modèle de données, store, API,
endpoint, provider, worker, job ni connexion n'a été touché. `READONLY` et
`ANALYSIS_ONLY` restent `True`. `desk_data.json` n'a pas été écrit.
