# SIGNAL OS · LOT 02 — MARCHÉS

Branche : `agent/vertex-signal-os-v1` · SW v208 → **v209** · Suite **3057 passed**

---

## 1. Je m'étais trompé sur l'ampleur

Le lot Shell annonçait « 2 éléments coupés d'environ 40 px » sur `/markets`.
**Mesure de ce lot : quatre, de 25 à 66 px.**

Le premier compte ne retenait que ce qui dépassait le **viewport**. Or
`.vx-mk-idx` porte `overflow:hidden` : deux cartes de la colonne de gauche
débordaient de **leur carte** sans atteindre le bord de l'écran. Invisibles à ce
compte, et tout aussi coupées.

**Un débordement rogné en silence ne dépasse rien : il disparaît.** C'est
précisément ce qu'un instrument qui mesure par rapport au viewport ne peut pas
voir.

---

## 2. Ce que la capture montrait à 390 px

| élément | attendu | rendu |
| --- | --- | --- |
| pastille de plage | `près du haut` | `près du h` |
| pastille de plage | `milieu de plage` | `milie` |
| nom de l'indice | `S&P 500` | deux lignes, comprimé à **25 px** |
| variation | `+1,67 %` | `+1,67` puis `%` seul sur la ligne suivante |
| plage | `plage 5 891–6 500` | coupée |

**Trois symptômes, un mécanisme** : une rangée `flex` en `nowrap` contenant une
pastille en `white-space:nowrap` que rien ne peut réduire. La pastille prend ce
qu'il lui faut, le nom se fait écraser, le reste est rogné — sans ellipse, sans
défilement, sans rien qui signale qu'un mot est tronqué.

---

## 3. Ma première correction en a créé une autre

`white-space:nowrap` sur la variation a bien empêché le `%` de tomber à la ligne.
**Et l'a transformé en débordement.** Mesuré juste après :

| carte | variation | dépassement du padding droit |
| --- | --- | --- |
| S&P 500 | `+1,67 %` | **+18 px** |
| Nasdaq | `+1,03 %` | **+35 px** |
| Dow Jones | `-0,59 %` | **+35 px** |
| Russell 2000 | `+1,33 %` | **+18 px** |

Rogné par le même `overflow:hidden`. J'échangeais un défaut visible contre un
défaut **plus discret** — et je l'aurais publié si je n'avais pas remesuré la
variation elle-même après avoir corrigé la pastille.

**Correction réelle** : la rangée valeur passe elle aussi à la ligne, donc la
variation descend **entière** sous le prix quand les deux ne tiennent pas côte à
côte ; le prix perd 4 px (26 → 22) pour que le cas reste rare.

| carte | après |
| --- | --- |
| les quatre | **−63 px** (dans la carte, avec marge) |

Nom de l'indice : **25-48 px → 72-115 px**. Pastilles : **+25/+42/+63/+66 →
−52/−34/−48/−34**.

---

## 4. Le contre-exemple, tenu par un gardien

`display:none` sur la pastille sous 720 px aurait fait passer **tous** les tests
de débordement, d'un coup. « Près du haut » situe le prix dans sa plage : c'est
une lecture, pas une décoration. La masquer au mobile serait retirer une
information parce qu'elle gêne la mise en page.

`test_la_pastille_de_plage_n_est_pas_masquee_en_mobile` interdit cette sortie.

---

## 5. Bascule : 720 px, déjà mesurée

Choisir 700 ou 640 px aurait créé une bande de largeur que le banc des neuf
bandes du lot 611 n'a jamais exercée. 720 est dans le recensement
`(520, 640, 720, 768, 820, 900, 1024, 1280)`. Un gardien relit cette liste depuis
le fichier du 611 plutôt que d'en recopier la valeur.

---

## 6. Micro-copy : 12 titres écrits à la source

Libellés canoniques de `COPY.md` : `VIX`, `Leadership`, `Risque principal`,
`Top hausses`, `Top baisses`, `Sélection`, `Santé du marché`,
`Qualité des données`, `Au-dessus des moyennes`, `Leaders`, `Régime`,
`Vue globale`.

**15 entrées** retirées de la table de réécriture — il en reste **20**, pour six
pages.

**Les `aria-label` longs sont conservés.** Raccourcir un titre visible ne doit
pas appauvrir le nom accessible : « VIX » seul ne dit pas de quoi parle la
région. Un gardien tient ce point, parce que c'est la simplification qu'on fait
sans y penser.

---

## 7. Mesures

Serveur dont le code servi est **vérifié** (`flex-wrap` mesuré à `wrap` dans le
navigateur, donc la nouvelle règle est bien celle appliquée).

Balayage 8 espaces × 2 largeurs :

| | 768 px | 390 px |
| --- | --- | --- |
| débordements **réels** | **0** | **0** |
| dépassements dans un conteneur défilant (voulus) | 66 | 236 |
| défilement horizontal de page | non | non |

`/markets` passe de 2 (au viewport) / 4 (à la carte) à **0**.

### Portée de ce balayage — ce qu'il ne voit pas

Il compare chaque élément au **viewport**. Le défaut de ce lot, lui, était un
dépassement **de la carte**, rogné par `overflow:hidden` : ce balayage ne l'a
jamais vu et ne le verrait pas ailleurs. Les cartes d'indice ont été mesurées par
une sonde dédiée ; **les autres composants du produit ne l'ont pas été**. Je ne
conclus donc pas « aucun rognage silencieux dans Vertex », seulement « aucun sur
les cartes d'indice de Marchés ».

---

## 8. Gardiens

`tests/test_signal_os_markets.py` — **6 tests**.

**Deux mutations sont d'abord passées au vert**, et c'était mon gardien qui avait
tort : je cherchais des sous-chaînes dans le bloc `@media` entier.
`.vx-mk-idx-topX` **contient** `vx-mk-idx-top`, et `flex-wrap:wrap` cherché dans
tout le bloc était satisfait par la règle voisine `.vx-mk-idx-foot`. Le gardien
lit désormais **la règle**, sélecteur par sélecteur — même famille que 616-B.

| mutation | résultat |
| --- | --- |
| sélecteur renommé | 3 échecs |
| `flex-wrap` retiré de la rangée | 1 échec |
| `min-width` du nom retiré | 1 échec |
| pastille masquée | 1 échec |
| `nowrap` de la variation retiré | 1 échec |
| `aria-label` perdu avec le titre | 1 échec |
| titre non écrit à la source | 1 échec |

---

## 9. Dette

- Table de réécriture : **20 entrées** (6 pages).
- `MutationObserver` : coût **toujours pas mesuré**.
- **Aucun instrument ne détecte le rognage silencieux à l'échelle du produit.**
  C'est la vraie leçon de ce lot et elle n'est pas soldée : il faudrait un
  balayage « enfant plus large que son parent à `overflow:hidden` » sur les huit
  pages. Non fait.
- `/opportunities` à 390 px : 197 dépassements dans des conteneurs défilants —
  **voulus**, mais jamais vérifiés un par un.

---

## 10. Suite

Lot **03 — Opportunités**.
