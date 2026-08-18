# SIGNAL OS · LOT 59 — LES HUIT ESPACES SOUS PANNE, ET UN QUI MENTAIT PAR SILENCE

Branche : `agent/vertex-signal-os-v1` · SW **v241 → v242** · Suite **3 481 passed**
(3 476 → +5)

Réserve SIGNAL-OS-53 §5.1, de ma main : *« Une seule page. Les sept autres
espaces ont leurs propres hôtes et ne sont pas balayés. »* Ce lot la paie — et
elle valait d'être payée.

---

## 1. Seize passages, deux défauts

`tools/mesurer_hotes_resolus.py --tous` balaie les **huit espaces**, en nominal
**et** sous coupure totale des données. Seize passages.

| espace | nominal | coupure |
| --- | --- | --- |
| Aujourd'hui, Marchés, Opportunités, Analyse, Portefeuille, Système | OK | OK |
| **Journal** | *défaut* → corrigé | OK |
| **Options** | OK | *défaut* → corrigé |

L'instrument était générique dès l'origine ; seule la **liste des disclosures à
ouvrir** était propre à la fiche Analyse. Elle est désormais **découverte** —
l'outil ouvre tout `<details>` fermé, en plusieurs passes, car ouvrir une
disclosure en révèle d'autres. Nommer la liste à la main aurait reproduit la
faute du lot 56, où un troisième bloc replié non prévu avait fait rendre
« jamais peint » sur un produit correct.

---

## 2. Le défaut d'Options : l'état honnête existait, le produit n'y arrivait jamais

Sous coupure, `/options` gardait `#vx-os-verdict` à l'état de **squelette
au-delà de 45 secondes** — le plafond de l'instrument — quand la fiche Analyse
dégrade entièrement en 5 s.

Et voici ce qui rend ce défaut intéressant : **`loadStructure()` porte un
`.catch` parfaitement honnête**, qui peint « Analyse indisponible : … ». Il
n'était jamais atteint.

La vue amorce son symbole depuis le tableau d'options. Quand `/api/options`
échoue, `board()` avale l'erreur et rend `[]` ; aucun symbole n'est choisi ; la
garde `if (!input.value && (pre || syms.length))` reste fausse. **`loadStructure`
n'est donc jamais appelé**, et le squelette du HTML initial reste à l'écran pour
toujours.

*On ne trouve pas cela en lisant le code* — le `catch` est là, bien visible —
*ni dans les octets servis*. Il faut couper les données et regarder l'écran.

### Le correctif, et ce qu'il refuse d'inventer

Un `else` : quand aucun symbole ne peut être choisi, la page **le dit**. Et
`board()` retient désormais la **cause**, que son `catch → []` confondait :

| cause | ce que la page affiche |
| --- | --- |
| tableau injoignable | « Tableau d'options injoignable — aucun titre à analyser » |
| tableau vide | « Aucun titre à options dans le tableau courant » |

Les deux nomment le recours qui reste ouvert : saisir un symbole à la main. Un
état honnête qui laisse l'utilisateur sans issue n'est honnête qu'à moitié.

**Mesuré après correctif : 45 s de squelette → erreur nommée en 0,5 s.**

---

## 3. Le défaut du Journal : rien à voir à l'écran, et pourtant faux

`#vx-pf-kpis` ressortait vide. Diagnostic honnête, et il tempère l'alarme : le
hero juste au-dessus dit déjà « Aucune décision journalisée pour l'instant »,
les KPI sont donc retirés **à bon droit** — quatre « n/d » n'ajouteraient que du
bruit. Hauteur mesurée du conteneur : **0 px**. Il n'y avait *rien à voir*.

Ce qui mentait, c'est l'**arbre d'accessibilité** : un
`aria-label="Quatre indicateurs de discipline"` sur un conteneur sans aucun
enfant — annoncé au lecteur d'écran, introuvable à l'exploration. Un attribut
`hidden` le retire.

Et son symétrique le remet dès qu'une décision est journalisée : sans cela, le
correctif d'accessibilité aurait créé un défaut pire — des KPI calculés et
invisibles, le motif exact que cette série traque depuis le lot 49.

Je le dis sans le grossir : **ce n'était pas un défaut visible**, et le rapport
ne prétendra pas le contraire.

---

## 4. Le gardien, et ses trois mutations

`tests/test_signal_os_degradation_huit_lot59.py` — chaque mutation tombe sur un
seul test :

| mutation | test qui tombe |
| --- | --- |
| la branche « aucun symbole » retirée | le défaut revient |
| la cause de l'absence n'est plus retenue | « vide » ≠ « injoignable » |
| le `.catch` de `loadStructure` retiré | le filet du chargement démarré |

La troisième dit une chose utile : les deux chemins sont **nécessaires**. Le
`catch` couvre le cas où le chargement démarre et échoue ; la nouvelle branche
celui où il ne démarre jamais. Retirer l'un ou l'autre rouvre un trou.

Un cinquième test tient le fait que l'outil lit les huit espaces **du registre**
`PRIMARY_NAV` au lieu de les recopier.

---

## 5. Réserves

1. **Une seule largeur** — 1440 px. Le balayage responsive est un autre
   instrument (lots 42/46), non rejoué ici.
2. **Coupure totale seulement.** Une panne *partielle* — une source sur cinq en
   échec — reste le cas le plus fréquent en vrai, et n'est pas mesurée.
3. **Les vues secondaires ne sont pas parcourues.** Chaque espace a des vues
   (`?view=…`) ; le balayage prend la vue par défaut. Sur Système, huit hôtes
   sont restés « non demandés » pour cette raison.
4. **Le mode démonstration.** Les états nominaux sont ceux du jeu de
   démonstration, étiqueté comme tel.
