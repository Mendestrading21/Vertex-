# SKYLER LOT 368 — Une vraie faille XSS : le titre du post-mortem n'était pas échappé

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-368` (base : lot 367 fusionné,
0e1ddad)

## Piste calibrée

Jumelle du lot 367 (`?view=`), mais sur les **segments de chemin** —
`/analysis/<sym>`, `/titre/<sym>`, `/memory/<decision_id>`… Un segment est du
texte libre : **plus exposé** qu'un paramètre de requête.

## Correction de méthode, d'abord

Ma première sonde envoyait des charges contenant `/`. Werkzeug refuse `%2F`
dans un segment et rend son **404 par défaut (701 octets)** : la charge
n'atteignait jamais le moteur de rendu, et la sonde **ne prouvait rien** —
28 lignes de « non » rassurants et vides. Toutes les charges retenues sont
**sans barre oblique** ; 18 requêtes sur 42 rendent alors une vraie page.

## 1. Le symbole : sain, et doublement protégé

```text
/analysis/"><img src=x onerror=alert(1)>   →  200, 75 216 octets
                                              const SYM="IMGS"
                                              &lt; ×1  &quot; ×2  &gt; ×1
```

Les caractères non alphanumériques sont **retirés** avant l'injection JS, et le
texte affiché est **échappé**. Les redirections `/titre/` et `/company/`
restent **relatives** (`/analysis/HTTPS:%5C%5CEVIL.TEST`) — pas de redirection
ouverte — et une charge CRLF est refusée par Werkzeug. **0 fuite sur 6 charges
× 7 gabarits.**

## 2. La mémoire décisionnelle : une faille réelle

`/memory/<decision_id>` sert bien une page (200, 19 371 octets, 1 bloc inline
qui parse, 35 `id` sans doublon) — celle que le lot 359 avait signalée comme
non couverte. Sa docstring promet :

> « TOUT contenu de la mémoire est ÉCHAPPÉ (XSS) »

**C'était faux pour le titre.** Le corps utilise bien `markupsafe.escape` pour
chaque ligne, mais l'argument `title=` de `render_shell` l'avait oublié :

```python
title='Post-mortem %s' % rec.get('symbol')      # ← sans échappement
```

Mesure d'exploitabilité — un symbole contenant `</title>` **sort de la balise** :

```text
symbole = '</title><script>alert(1)</script>'
title   = 'Post-mortem '
après </title> : <script>alert(1)</script> · Vertex</title> <link rel="icon" …
```

Un `<script>` **actif injecté dans le `<head>`**. Avec `</title><img src=x
onerror=…>`, même résultat : balise active hors du titre.

### Portée réelle — dite franchement

Le `symbol` d'un record vient du moteur de décision de Vertex (univers de
symboles contrôlé), **pas d'une saisie utilisateur**. L'exploitation suppose
d'écrire dans `skyler_memory.json`, un fichier local. Ce n'est donc **pas
exploitable à distance aujourd'hui** : c'est un défaut de défense en profondeur
— et surtout une **promesse fausse dans la documentation du code lui-même**.

## Correctif

Une ligne, qui restaure l'invariant déjà revendiqué :

```python
# `title` va dans <title> SANS échappement par le shell : un symbole
# contenant `</title>` sortirait de la balise et injecterait du HTML actif
# (constaté au lot 368 — le corps était échappé, pas le titre).
title='Post-mortem %s' % _e(rec.get('symbol'))
```

Ce n'est pas « implémenter une fonctionnalité manquante » (règle du lot 365) :
c'est faire tenir au code une promesse qu'il affichait déjà.

## Gardien

`tests/test_segments_url_lot368.py` (12 tests) : 5 charges hostiles sur
`/analysis/<sym>`, `const SYM` reste alphanumérique, redirections relatives,
anti-vide (un symbole légitime doit produire une vraie page), et pour la
mémoire — record hostile injecté dans une mémoire **temporaire** (le vrai
`skyler_memory.json` n'est jamais touché, méthode du lot 362) — contenu
échappé, sortie de `<title>` impossible, 404 lisible sans réflexion.

**Une assertion de ce gardien était elle-même trop stricte** : elle refusait la
sous-chaîne `onerror=alert` même **échappée**, donc inerte. Corrigée pour ne
viser que la forme **exécutable** (`<img` non échappé).

### Preuve ROUGE

```text
ROUGE OK     correctif retiré : le titre du post-mortem n'est plus échappé | restauration identique
             2 failed, 10 passed
après restauration : 12 passed
VERDICT : gardien mordant sur la faute réelle
```

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 367, 0e1ddad) ; arbre propre.
- Un fichier de **production** a changé → preuve exigée : serveur DEMO
  (`/scan` 20 lignes, `source=demo`), **MD5 des 8 pages : 0 écart / 8**.
  Normal — `/memory/` n'est pas l'une des 8, et le correctif est confiné.
- Suite complète : **2566 → 2578 passed / 2 skipped** — verte (+12).

## Décision SW

**Pas de bump** (`td-shell-v187`) : les 8 MD5 le prouvent, `/static` inchangé.

## Portée — ce que ce lot ne prétend pas

Une seule faille trouvée, non exploitable à distance, corrigée en une ligne.
Les charges testées sont cinq classiques : ce n'est pas un audit de sécurité
exhaustif. Les autres appels à `render_shell(title=…)` n'ont pas été audités un
par un — piste ouverte : **un `title=` recevant une donnée non filtrée ailleurs
aurait le même défaut**. Le durcissement de fond (échapper le titre dans
`render_shell` lui-même) toucherait toutes les pages servies : **en attente de
GO**.

## Suite

LOT 369 : veille active. Piste prioritaire — auditer tous les `render_shell(
title=…)` (même classe que la faille de ce lot). **LOT 370 : checkpoint
périodique complet + bilan de la tranche 360-369.**
