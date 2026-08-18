# SIGNAL OS · LOT 25 — CIBLES TACTILES, ANIMATIONS RÉDUITES, TITRES DE PAGE

Branche : `agent/vertex-signal-os-v1` · SW v230 → **v231** · Suite **3137 passed**

Trois contrôles jamais mesurés. **Deux rendent vide**, un trouve un défaut.

---

## 1. Les deux résultats vides

### Animations réduites — 0 sur 35 vues

La préférence système `prefers-reduced-motion: reduce` est **émulée** dans le
navigateur, puis chaque élément visible est interrogé sur son `animationName` et
sa durée effective. **Aucune animation ne persiste.**

Le produit respecte le choix de l'utilisateur. Ce résultat ne vaut que parce que
l'instrument aurait vu une animation résiduelle : il lit le style **calculé**,
pas la présence d'un bloc `@media` dans les sources.

### Titres de page — 9 sur 9 uniques

```
/               « Aujourd'hui · Vertex »
/markets        « Marchés · Vertex »
/opportunities  « Opportunités · Radar · Vertex »
/analysis       « Analyse · Vertex »
/analysis/ACN   « ACN · Analyse · Vertex »
/portfolio      « Portefeuille · Synthèse · Vertex »
/options        « Options · Vertex »
/journal        « Journal · Vertex »
/system         « Système · Vertex »
```

Aucun doublon, et la sous-vue apparaît quand elle existe.

---

## 2. Le défaut : six familles de cibles sous 24×24 à 390 px

| cible | taille | voisin le plus proche |
| --- | --- | --- |
| `.vx-ticker` (AFL) | 93×17 | 121 px |
| `.vx-ticker` (AOS) | 32×17 | 49 px |
| `.vx-ticker` (MMM) | 53×17 | — |
| lien secteur « Semiconducteurs » | 98×15 | 40 px |
| lien secteur « Software » | 50×15 | 40 px |
| lien secteur « Big Tech » | 49×15 | 40 px |

### La précision qui compte : ce n'est PAS une violation

WCAG 2.5.8 exempte les cibles suffisamment **espacées**. Les voisins sont à
**40 à 121 px** : l'exception s'applique, le produit est **conforme**.

C'est un défaut de **confort sur téléphone** — 15 à 17 px de haut sous le
pouce — et l'utilisateur consulte Vertex sur iPhone. Le corriger relève du
produit, pas de la norme. Le présenter comme une non-conformité aurait invoqué
une autorité qu'on n'a pas.

---

## 3. La cause, et c'est la troisième fois

La politique de taille tactile mobile est définie **par classe** :

```css
.vx-btn,.vx-tab,.vx-chip{min-height:40px}
```

Donc tout contrôle qui ne porte pas la classe y échappe. Le lot 294 avait déjà
dû rattraper les contrôles segmentés, et son commentaire dit la cause mot pour
mot : « hors de la règle ci-dessus car sans classe vx-btn ».

> Une règle qui s'applique par nom de classe ne protège que ce qu'on a pensé à
> nommer. Trois rattrapages font un motif, pas une série d'oublis.

### Le correctif

Une règle qui vise le **comportement** plutôt que la classe —
`role="button"`, `data-open-analysis`, `a[onclick]` — donc les contrôles à venir
sont couverts sans nouveau rattrapage.

Deux choix explicites :

- **Seuil 32 px**, qui est celui que le produit s'est déjà donné pour les
  actions secondaires (`.vx-btn-sm`). En inventer un autre aurait créé une
  troisième échelle dans un système qui en a déjà deux.
- **`:not(.vx-btn):not(.vx-chip):not(.vx-tab)`**, sans quoi la nouvelle règle
  **rabaisserait** les boutons de 40 à 32. Corriger une famille ne doit pas
  dégrader celle d'à côté.

`display:inline-flex` est indispensable : `min-height` ne fait **rien** sur un
élément inline. Sans lui, la règle existerait et ne changerait rien — le pire
des deux mondes, parce qu'elle *aurait l'air* d'une correction.

---

## 4. Mesures — serveur vérifié avant lecture

| relevé (390 px) | avant | après |
| --- | --- | --- |
| cibles sous 24×24 | **6 familles** | **0** |
| non textuel sous 3:1 (non-régression lot 24) | 0 | **0** |
| texte sous AA (non-régression lot 22) | 0 | **0** |

Les deux non-régressions comptent : la règle change le `display` de trois
familles d'éléments, ce qui pouvait déplacer la mise en page.

---

## 5. Gardien — `tests/test_signal_os_tactile_lot25.py` (4 tests, 6 mutations sur 6 tuées)

| mutation | résultat |
| --- | --- |
| `inline-flex` retiré (règle rendue inerte) | 1 échec |
| famille des tickers retirée | 1 échec |
| famille des liens retirée | 1 échec |
| exclusion des boutons retirée | **3 échecs** |
| politique historique cassée | 1 échec |
| seuil secondaire désaccordé | 1 échec |

La première mutation est la plus utile : elle laisse la règle **en place** et
sans effet. C'est le genre de régression qu'une relecture approuve.

---

## 6. Réserve honnête

Le seuil retenu est **32 px**, pas les 44 pt recommandés par Apple ni les 48 dp
de Google. C'est un compromis assumé avec la densité du produit, aligné sur son
échelle existante — et le commentaire du lot 612 avait déjà tranché que passer
les actions secondaires de 32 à 40 relevait d'une décision de design, pas d'un
correctif. Cette décision-là reste ouverte.
