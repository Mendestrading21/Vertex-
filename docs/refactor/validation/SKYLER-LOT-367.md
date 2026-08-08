# SKYLER LOT 367 — `?view=` : pas le trou qu'on croyait, mais un chemin d'injection non gardé

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-367` (base : lot 366 fusionné,
8b5a1ef)

## Piste calibrée

Les gardiens JS (lots 182/186) ne balayent que les routes **nues**. Les
variantes `?view=…` — vers lesquelles pointent les 40 redirections legacy —
servent-elles du JavaScript jamais parsé ? Le lot 359 avait trouvé exactement
cela sur `/analysis`.

## Mesure — et la piste s'effondre

**Découverte** : 37 variantes trouvées en lisant les onglets `?view=` dans le
HTML servi. *Ma liste tirée d'un grep du code n'en voyait que 25* — le grep
manquait `?view=learnings`, `?view=progression`, `?view=events`,
`?view=positioning`, `?view=impacts`, `?view=macro`… Première correction de
méthode : **découvrir depuis le servi, pas depuis la source**.

Ces variantes servent **16 blocs `<script>` inline absents des routes nues** —
un trou quatre fois plus grand que celui du lot 359. Sauf que.

**Vérification avant de conclure.** Diff entre le bloc d'une route nue et celui
de sa variante :

```text
=== /portfolio vs /portfolio?view=risk : 2 ligne(s) de diff, |a|=65915 |b|=65915
     -const VIEW="team";
     +const VIEW="risk";
=== /markets vs /markets?view=sectors : 2 ligne(s) de diff
     -const VIEW='overview';
     +const VIEW='sectors';
=== /journal vs /journal?view=learnings : 2 ligne(s) de diff
     -const VIEW='overview';
     +const VIEW='learnings';
```

**Le JavaScript est identique au nom de la vue près.** Une faute de syntaxe s'y
verrait sur la route nue, déjà balayée par le lot 182. **Il n'y a pas de trou.**
Un gardien qui reparse 16 quasi-doublons aurait coûté du temps d'exécution pour
n'attraper rien de neuf.

Trois pages (`/intelligence`, `/system`, `/options`) servent d'ailleurs des
blocs **strictement identiques** entre toutes leurs vues.

## Ce qui, en revanche, n'était gardé par rien

Le constat utile est ailleurs : **ce paramètre d'URL atteint les octets
servis** — une constante `const VIEW=…` dans le JS de 4 pages, un attribut
`data-view` sur 2 autres. Sa sûreté ne tient qu'à une **liste blanche** côté
serveur (`view = view if view in dict(_VIEWS) else 'team'`).

Sondé avec des charges hostiles sur les 8 pages qui lisent `view=` :

```text
/markets         VIEW='overview'    payload dans le JS : non
/opportunities   VIEW="radar"       payload dans le JS : non
/portfolio       VIEW="team"        payload dans le JS : non
/journal         VIEW='overview'    payload dans le JS : non
/system          VIEW=(ROOT&&ROOT.dataset.view)||'…   payload : non
/intelligence    VIEW=(ROOT&&ROOT.dataset.view)||'…   payload : non
/options, /analysis : pas de constante VIEW servie
```

Et avec une charge d'attribut (`"><img src=x onerror=…`) : `data-view` reste
`connections` / `analyst`, **aucune trace de la charge dans la page**. La liste
blanche tient partout — mais **aucun test ne le vérifiait**.

## Ce que le lot livre

**Gardien neuf** `tests/test_vues_parametre_lot367.py` (33 tests) :

- 3 charges hostiles × 8 routes : la valeur de `?view=` ne doit **jamais**
  ressortir telle quelle dans la page, ni sous forme exécutable ;
- une vue inconnue retombe sur la vue par défaut, et toute constante `VIEW`
  servie reste un identifiant simple (`[a-z_]+`) ;
- anti-vide : une vue **légitime** doit bien changer la page — sinon le
  paramètre serait ignoré et les tests ne prouveraient rien.

### Preuve ROUGE

```text
ROUGE OK     liste blanche retirée sur Portefeuille (const VIEW JS) | restauration identique
après restauration : 33 passed
VERDICT : gardien mordant
```

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 366, 8b5a1ef) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2533 → 2566 passed / 2 skipped** — verte (+33).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Aucune vulnérabilité n'a été trouvée : la liste blanche tient sur les 8 pages.
Le lot **ferme une fenêtre de non-détection sur un chemin d'injection**, il ne
répare rien. Les charges testées sont trois classiques (sortie de chaîne JS,
sortie d'attribut, fermeture de `<script>`) — ce n'est pas un audit de sécurité
exhaustif.

Et la conclusion la plus utile est négative : **le trou soupçonné n'existait
pas**. Sans le diff, ce lot aurait posé un gardien inutile et écrit un rapport
annonçant une faille imaginaire.

## Suite

LOT 368 : veille active. Pistes ouvertes — `/memory/<id>` et
`/memory/cell/<g>/<k>` (HTML servi, exigent un identifiant réel) ; promesses de
docstrings en un seul mot majuscule et docstrings de fonctions (hors périmètre
du lot 366). Prochaine échéance périodique : ~lot 370.
