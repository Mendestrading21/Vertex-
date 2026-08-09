# SKYLER LOT 417 — « Rendement +20 séances » : le N affiché n'est pas le N du calcul

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-417` (base : lot 416 fusionné,
a4bb4aa)

Deuxième lot dans la veine des moteurs. Cible :
`vertex/engines/track_record.py` — **le moteur qui note Vertex lui-même**. Son
docstring annonce la couleur : *« Aucune promesse, que du mesuré. »* C'est
précisément ce qui rend la question intéressante : **le mesuré est-il présenté
avec son échantillon ?**

**Aucun code, aucun gardien, aucun test.**

## Le mécanisme

`evaluate()` ne publie un paquet que si `b['n'] >= 5`. Mais `n` compte les
entrées **résolues à au moins un horizon**, tandis que chaque statistique
d'horizon se calcule sur sa propre liste :

```python
b['n'] += 1
if f1  is not None: b['f1'].append(f1)
if f5  is not None: b['f5'].append(f5)
if f20 is not None: b['f20'].append(f20)   # ne se remplit que si +20 séances existent
```

Un verdict émis il y a 6 séances alimente `n` et `f5`, **pas** `f20`. Le filtre
protège donc le paquet, **pas chaque nombre publié**.

## Mesuré, pas déduit — moteur exécuté en mémoire

Ledger fabriqué dans le scratchpad (`persist._BASE_DIR` redirigé), série de prix
fabriquée, mémo réinitialisé.

```text
TÉMOIN −   4 entrées                          AUCUN PAQUET (filtre n≥5)        ✔
TÉMOIN +   5 entrées toutes anciennes         n=5  win_1j=100  win_5j=100  win_20j=100  avg_20j=15.73
CAS        1 ancienne + 4 à horizon court     n=5  win_1j=20   win_5j=20   win_20j=100  avg_20j=20.0
```

Troisième ligne : le terminal annonce **`N = 5`**, **20 % de gagnants à 1 et 5
séances**, et dans la même ligne **100 % de gagnants et +20,0 % de rendement
moyen à 20 séances** — **assis sur une seule observation**. Les quatre autres
verdicts n'ont pas encore atteint l'horizon ; rien ne le dit.

## Ce n'est pas un cas de bord : c'est l'état normal du registre

Un registre qui tourne contient toujours des verdicts trop récents pour +20.
Mesuré sur un cas réaliste — un verdict par séance sur les 40 dernières :

```text
N annoncé                                        39
observations réelles derrière « +1 séance »      39   (100 % de N)
observations réelles derrière « +5 séances »     35   ( 90 % de N)
observations réelles derrière « +20 séances »    20   ( 51 % de N)
```

La colonne « +20 séances » repose **structurellement** sur un sous-ensemble
strict de `N`, et cette proportion n'est **jamais** affichée. Le cas à une seule
observation est l'extrême ; le biais, lui, est permanent.

## Où ça s'affiche — et la phrase qui promet ce que le chiffre n'a pas

`vertex/ui/pages/performance_page.py:443` construit la ligne du tableau :

```text
Verdict │ N │ Rdt +5 s │ Rdt +20 s │ % gagnants +5 s │ TP1 avant stop
        │ 5 │   …      │  +20,0 %  │      20 %       │   — % (0)
```

Deux choses dans cette seule ligne :

1. **`TP1 avant stop` affiche son dénominateur entre parenthèses**
   (`s.tp1_rate + ' % (' + s.tp1_resolved + ')'`). Le moteur expose bien
   `tp1_resolved` — **la bonne pratique existe déjà, appliquée à une seule
   métrique sur quatre.**
2. **`Rdt +20 s` n'expose rien**, et se lit sous le `N` de la même ligne.

Et la légende du graphique qui en fait son sujet — *« Rendement moyen +20
séances par verdict »*, `performance_page.py:459` — déclare :

> *« moyenne réelle des verdicts résolus **(n≥5)** — mesure, pas une promesse »*

**C'est faux pour ce chiffre-là** : `n≥5` filtre le paquet, pas l'échantillon de
la moyenne à 20 séances. La phrase promet exactement la garantie qui manque.

## Le gardien

`tests/test_track_record_lot89.py:58`,
`test_evaluate_min_sample_and_no_division_by_zero`, vérifie que `WATCH` (1
entrée) est tué et que `BUY` (6 entrées) est publié — donc le minimum **du
paquet**. Sa fixture ne contient que **7 cours**, si bien que `f5` et `f20` sont
`None` partout : le cas où un horizon a moins d'observations que `n` **n'est
jamais exercé**. Le gardien tient ce qu'il teste ; il ne teste pas ce que le nom
« min_sample » laisse entendre pour chaque statistique publiée.

À son crédit, il assert `tp1_resolved == 0` — encore une fois, le dénominateur
est surveillé **là où il est exposé**.

## Classement, sans le gonfler

**Rang 1** — mais il faut dire en quoi c'est différent du 407. Ici **le nombre
n'est pas faux** : c'est une moyenne réelle d'observations réelles. Ce qui est
faux, c'est **l'échantillon suggéré** (le `N` de la ligne) et **la légende** qui
affirme `n≥5`. C'est un défaut d'**honnêteté de présentation** sur la page dont
le sujet est précisément la confiance qu'on peut accorder au moteur — pas une
erreur d'arithmétique.

Correction pressentie, et elle est petite : publier le compte par horizon comme
le moteur le fait **déjà** pour TP1 (`len(b['f20'])` à côté de `avg_20j`),
l'afficher entre parenthèses comme le fait **déjà** la colonne TP1, et corriger
la légende. **Aucun GO, rien n'est engagé.**

## Portée

Un seul moteur, une seule fonction (`evaluate`). Le registre réel de
l'utilisateur (`edge_ledger.jsonl`) **n'existe pas sur ce poste** : je ne peux
donc rien dire de l'ampleur sur ses données à lui — les proportions ci-dessus
viennent d'un registre fabriqué, réaliste mais fabriqué. `record()`,
`_hit_tp1()` et la mémoïsation n'ont pas été rouverts (couverts au lot 89).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde vit
  dans le scratchpad et redirige `persist._BASE_DIR` dans un dossier temporaire.
  Pas de preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-et-unième lot court, deuxième dans la veine des moteurs — et **deux
trouvailles en deux lots**, contre trois bornages consécutifs juste avant. La
veine tient.

Un motif se dessine sur ces deux lots : dans les deux cas, **le code contenait
déjà la bonne pratique à côté du défaut** — au 416 la neutralité honnête
(`pos = 50.0` quand `hi == lo`, trois lignes plus bas), ici le dénominateur
exposé (`tp1_resolved`, dans le même dictionnaire). Le défaut n'est pas
l'ignorance de la règle : c'est son application incomplète.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
