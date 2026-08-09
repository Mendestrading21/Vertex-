# SKYLER LOT 397 — Le registre confronté à lui-même

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-397` (base : lot 396 fusionné,
1a41c94)

Troisième lot court. **Aucun code, aucun gardien, aucun test.** Une seule ligne
corrigée, dans un rapport.

## Le point contrôlé — jamais fait en 25 lots

395 avait re-mesuré les pistes fines, 396 les octets servis. Ce lot contrôle **la
mémoire de la boucle elle-même** : chaque lot 372→396 a-t-il son rapport, sa
ligne d'index et son bloc STATUS — et les **chiffres** concordent-ils ?

C'est la seule omission qui serait **invisible autrement** : rien ne vérifie le
registre, et c'est lui qu'on relit pour décider.

## Présence — 25 sur 25

```text
lots vérifiés (372 → 396)                    25
   rapport + ligne d'index + bloc STATUS     25
   incomplets                                 0
```

**Mon premier détecteur en signalait deux** — les lots 380 et 390. Faux : ce sont
les lots de **bilan**, dont le bloc STATUS prend la forme `## BILAN — veille
active, lots N → M` et non `**Lot N — livré**`. Le détecteur ne connaissait
qu'une seule forme. *Encore l'instrument avant le document.*

## Exactitude — un écart réel

La présence ne dit rien de la justesse. Chaque ligne d'index porte quatre
chiffres (version du cœur, SW, suite, verdict) ; j'ai confronté deux d'entre eux
au rapport correspondant.

```text
suite : 25/25 concordants   2645 → 2672 → 2693 → 2703 → 2712 → 2721 → 2730 →
                            2754 → 2754 → 2767 → 2779 → 2793 → 2793 → 2806 →
                            2817 → 2826 → 2831 → 2835 → 2835 → 2842 → 2856 →
                            2862 → 2862 → 2862 → 2862
SW    : 24/25 concordants   1 écart
```

**Lot 394 : l'index affirme `v187`, le rapport ne l'écrit nulle part.** Les 24
autres rapports enregistrent la version du service worker dans leurs
« Vérifications du cycle » ; celui-là ne la mentionne que comme nom de règle.
L'assertion du registre n'était **adossée à rien** — vraie par ailleurs, puisque
le lot n'a touché aucun octet servi, mais invérifiable depuis le rapport.

Cette fois, ce n'était **pas** le détecteur : la ligne manquait réellement.

**Corrigé** — la ligne SW est ajoutée au rapport 394, avec la mention de son
origine. Après correction : **0 écart sur 25**.

## Ce que ce contrôle vaut

La chaîne des 25 comptes de suite est **strictement monotone et exacte**, du
2645 du lot 372 au 2862 d'aujourd'hui : aucune erreur de transcription en
25 lots de tenue de registre. C'est la première fois que c'est vérifié plutôt que
supposé.

Et l'écart trouvé est du genre le plus discret qui soit : **un chiffre affirmé
dans le registre sans source dans le rapport**. Rien ne l'aurait révélé — ni la
suite, ni les gardiens, ni une relecture, puisque la valeur était juste.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché**, aucun test — la seule modification est
  une ligne dans `SKYLER-LOT-394.md`. Pas de preuve MD5 requise, pas de bump.
- Snapshot des 21 fichiers runtime avec contrôle d'apparition ; écart final
  **aucun**.
- Suite : **2862 passed / 2 skipped**, inchangée. SW : `td-shell-v187`.

## Portée

Deux des quatre colonnes du registre ont été confrontées (suite, SW). La version
du cœur et le verdict GO ne l'ont pas été — la première est constante à 0.9.0, le
second est déclaratif. Et le contrôle porte sur la **concordance interne** du
registre : il ne dit pas que les chiffres décrivent fidèlement ce qui s'est passé,
seulement que les deux documents disent la même chose.

## Où en est la boucle

Trois lots courts, trois points de contrôle distincts : pistes fines (395),
octets servis (396), registre (397). Chacun a apporté quelque chose de mesuré ;
aucun n'a nécessité de code.

La matière utile reste **décisionnelle** — purge des 7 points MSFT (388) et scan
de démo dans `breadth_history` (391, reproduit au 396).

Prochaine échéance : **bilan n°9 au lot 400**.
