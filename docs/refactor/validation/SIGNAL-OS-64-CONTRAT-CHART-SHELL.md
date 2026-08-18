# SIGNAL OS · LOT 64 — UNE PORTÉE N'EST PAS UNE SORTIE

Branche : `agent/vertex-signal-os-v1` · SW **v244 → v245** (deux fichiers
`/static` modifiés) · Suite **3 515 passed** (3 507 → +8)

Réserve SIGNAL-OS-63 §6.4, de ma main : *« `opts.freshness` n'est passé par aucun
appelant de `VXCharts.card`. Le badge de fraîcheur canonique du Chart Shell est
donc du code mort. »*

**Je l'avais lu au `grep`. Ce n'est pas une mesure** — un `grep` ne voit ni un
objet construit ailleurs, ni une clé passée depuis une variable. Ce lot mesure.

---

## 1. Les deux directions du contrat, et laquelle compte

`tools/mesurer_contrat_chart_shell.py` compare ce que chaque builder **lit** de
son objet d'options à ce que ses appelants lui **passent**.

| direction | ce que ça veut dire |
| --- | --- |
| **passée, jamais lue** | une page **croit dire quelque chose** et le composant l'ignore en silence |
| **lue, jamais passée** | une capacité que personne ne demande — du code mort |

La première est de loin la plus grave : une page qui passe `source:` en pensant
nommer sa source, et rien ne s'affiche. C'est un défaut **d'honnêteté**, et il
est invisible à la lecture des deux fichiers séparément.

### Le résultat sur cette direction est rassurant, et c'est le principal

```text
=== PASSEES MAIS JAMAIS LUES ===
  aucune.
```

Aucune page ne croit nommer une source, une conclusion, une limite ou une
provenance que le Chart Shell jetterait sans le dire.

### Anti-vacuité : deux témoins, un par direction

Un détecteur qui trouve zéro dans les deux sens et qui est simplement aveugle
rend exactement le même résultat qu'un produit parfait. `--temoin-lu` injecte
`opts.__temoin_jamais_passe` dans `C.card` ; `--temoin-passe` injecte
`__temoin_jamais_lu:1` sur un site d'appel. **Les deux mordent**, sur copie en
mémoire, jamais sur le disque.

---

## 2. La conclusion du lot 581, renversée

`SKYLER-LOT-581` concluait, de `freshnessBadge` :

> Un seul site d'appel — mais il est dans `C.card`, le constructeur de carte
> canonique. **Chaque carte-graphique du produit rend donc ce badge.**

C'est exactement l'inverse, et c'est mesurable **des deux côtés** :

| preuve | résultat |
| --- | --- |
| statique — appelants passant `freshness` | **0** ; la fonction rend `''` sans valeur |
| navigateur — 8 espaces | **4 cartes-graphiques peintes, 0 badge de fraîcheur** |

Le raisonnement sur la **portée** du site d'appel était juste. Il a été appliqué
à un appel **qui ne produit rien**. Et le lot 581 venait justement de corriger
« un compte d'appels n'est pas une surface d'écran » : il a commis aussitôt le
défaut symétrique.

> **Une portée n'est pas une sortie.**

Trois étapes — compter les appels, mesurer leur portée, oublier de regarder
l'écran — et l'erreur s'est déplacée d'un cran à chaque fois sans jamais
atteindre le seul juge qui compte. `SKYLER-LOT-581.md` porte la correction en
place, avec l'énoncé faux laissé visible.

---

## 3. Retiré plutôt que câblé — et pourquoi

L'âge a **déjà un domicile** sur la carte : la provenance en pied,
`VX.updateIndicator(timestamp, source, mode)`, **peinte sur les 4 cartes
mesurées**. Câbler l'en-tête aurait créé un **second domicile pour la même
donnée** — le défaut exact corrigé au lot 63 sur Opportunités, où la qualité des
données portait la pilule de fraîcheur à côté de la vraie puce.

Le retrait supprime en outre l'une des deux grammaires de fraîcheur divergentes
que le lot 581 relevait comme dette (`data-live` ici, `data-state` dans
`VX.freshness`).

**Rendu identique, mesuré avant et après :**

```text
avant : 4 cartes-graphiques · 4 provenances · 0 badge de fraicheur
apres : 4 cartes-graphiques · 4 provenances · 0 badge de fraicheur
```

Un retrait de code inatteignable ne peut rien changer à l'écran — mais l'écrire
sans le vérifier serait exactement le genre de raisonnement que ce lot corrige.

---

## 4. Quatre artefacts de mon propre découpage, arrêtés avant publication

Mon premier passage rendait seize « trouvailles ». **Trois familles étaient
mes fautes**, et une quatrième n'a été révélée que par mutation.

| ce que j'accusais | ce que c'était |
| --- | --- |
| `false` et `true` sont des options | des **valeurs par défaut** de déstructuration prises pour des clés |
| `height` est passée mais jamais lue | lue via `chartHeightStyle(opts)` → `chartHeight(opts)`, un **saut** que je ne suivais pas |
| `coup` est une option de `card` | « se lit **d'un coup d'**œil » — un **commentaire** dont les apostrophes ASCII désynchronisaient mon suivi des chaînes |
| *(rien — le gardien était vert)* | je masquais l'intérieur des **gabarits**, or `${…}` contient du **code réel**, et c'est là que `C.card` compose tout son en-tête |

La quatrième mérite d'être soulignée : elle n'a été trouvée **ni par lecture ni
par la mesure**, mais parce que la mutation M2 (« remettre `opts.freshness` dans
la condition de l'en-tête ») laissait le gardien **vert**. Un masque trop large
rend un détecteur silencieux, et un détecteur silencieux ressemble à s'y
méprendre à un produit sain.

Et l'instrument s'est fait prendre par le mécanisme du gardien creux :
`_lues` lisait le texte brut, où **mon propre commentaire expliquant le retrait**
de `opts.freshness` contenait les mots `opts.freshness`. Masquer d'abord,
analyser ensuite.

*Publier ces quatre-là aurait été accuser le produit de mes fautes.*

---

## 5. Deux tests de la maison, remplacés — et ce n'est pas un assouplissement

Mon retrait a fait tomber `test_freshness_badge_covers_all_states`, et **pas**
`test_chart_shell_contract_complete` — qui exigeait pourtant le jeton
`freshnessBadge`. Le second passait **grâce au commentaire** qui explique le
retrait.

Les deux étaient des recherches de sous-chaînes sur un fichier de mille lignes :
ils affirmaient « le badge canonique couvre tous les états » en vérifiant que six
mots courts existent quelque part — `live` dans `vx-live-dot`, `stale` dans les
états de rendu, `demo` dans `modeLabel`.

- `test_chart_shell_contract_complete` : jeton `freshnessBadge` retiré, avec la
  raison écrite sur place. `updateIndicator` reste gardé — c'est lui qui porte
  réellement l'âge, et il est peint sur les 4 cartes.
- `test_freshness_badge_covers_all_states` : **déplacé là où l'exigence porte** —
  la table `VX.freshness.LABEL` de `vx-core.js`, mesurée peinte aux lots 62–63 —
  et resserré sur la **table** plutôt que sur le fichier. Muté : retirer un état
  de `LABEL` le fait tomber.

Le test est plus fort qu'avant, pas plus faible. Affaiblir un gardien pour faire
passer son propre changement est la faute que ce paragraphe existe pour ne pas
commettre en silence.

---

## 6. Le gardien et ses huit mutations

`tests/test_signal_os_contrat_chart_shell_lot64.py` (8 tests) — il **appelle la
mesure** au lieu d'épingler des chaînes : un gardien qui compare du texte se
contente de la forme, celui-ci vérifie la propriété.

| mutation | résultat |
| --- | --- |
| M1 — `freshnessBadge` remis dans le shell | **tombe** ✅ |
| M2 — `opts.freshness` relu par `card` | **PASSAIT** ❌ → corrigé |
| M3 — masquage des commentaires retiré | **tombe** ✅ |
| M4 — valeurs par défaut reprises pour des clés | **tombe** ✅ |
| M5 — saut par fonction aide retiré | **tombe** ✅ |
| M6 — témoin « lue jamais passée » neutralisé | **tombe** ✅ |
| M7 — sites non analysables tus | **tombe** ✅ |
| M8 — interpolations de gabarit re-masquées | **PASSAIT** ❌ → corrigé |

M2 a révélé la faute d'instrument du §4 ; M8 a révélé qu'**aucun test ne
couvrait ce que M2 venait de montrer**. Après correction, les huit tombent et le
fichier intact passe 8/8.

---

## 7. Ce que la seconde direction a trouvé d'autre — et pourquoi je n'en fais pas des défauts

25 options restent « lues mais jamais passées » : `xTitle`, `yTitle`, `xFmt`,
`crosshair`, `fill`, `glow`, `positiveIsGood`, `valueFmt`, `density`, `xGrid`…

**Ce ne sont pas des défauts.** Ce sont des réglages avec une valeur par défaut
que personne n'a eu besoin de changer — c'est le fonctionnement normal et sain
d'une bibliothèque de composants. Les compter comme des trouvailles gonflerait
le résultat de ce lot d'un facteur six pour rien.

La distinction qui les sépare de `freshness` : `freshness` était une **promesse
d'honnêteté** que le composant affichait dans son contrat et ne tenait jamais.
Un `xTitle` non passé ne promet rien à personne.

Trois méritent tout de même d'être nommées, sans être corrigées ici :
`card.controlsHtml`, `card.size` et `card.stateMessage` — trois branches du
shell qu'aucun appelant n'emprunte.

---

## 8. Réserves

1. **38 sites d'appel ne sont pas analysables** (objet construit ailleurs,
   diffusion `{...base}`). Ils sont **comptés et annoncés**, jamais tus : une
   limite passée sous silence transformerait le silence de l'outil en garantie.
2. **4 cartes-graphiques seulement** étaient peintes dans les conditions de
   mesure (mode démonstration, 1440 px, vues par défaut, disclosures fermées).
   La conclusion « 0 badge » tient parce qu'elle est **doublée par la preuve
   statique** — aucun appelant ne passe la clé — et non par le seul décompte.
3. **`card.controlsHtml`, `card.size`, `card.stateMessage`** : non tranchés.
4. L'outil lit le **texte** des sources ; une clé calculée à l'exécution lui
   échappe par construction.
