# SKYLER LOT 402 — Les 300 fichiers rejoués seuls : la suite ne dépend pas de son ordre

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-402` (base : lot 401 fusionné,
a996c81)

Le lot 401 a prouvé qu'**une** dépendance d'ordre existait, et l'a corrigée. Il
n'a pas dit s'il y en avait d'autres. Ce lot balaie le périmètre entier :
**chaque fichier de test rejoué seul**, dans un interpréteur neuf.

**Aucun code, aucun gardien, aucun test.** Le résultat est négatif — et il est
mesuré.

## Le résultat

```text
fichiers de test rejoués SEULS                 300 / 300
   échecs                                        0
   skips                                         0
   tests exécutés, somme des passes isolées   2 864
   tests de la suite complète                 2 864   ← identique
```

L'égalité des deux totaux est le contrôle qui compte : elle prouve qu'aucun test
n'a été **perdu** en chemin (fichier non collecté, erreur d'import silencieuse).
Chaque test a tourné dans les deux régimes, et le verdict est le même.

**Après le correctif du lot 401, la suite ne dépend plus de son ordre
d'exécution** — dans la direction mesurée ici.

## L'instrument a échoué une fois, et je l'ai vu avant de conclure

Le premier balayage a été lancé en tâche de fond avec `nohup … &` ; le processus
n'est **pas mort** quand j'ai cru l'avoir arrêté, et un second balayage a été
lancé sur le **même fichier de sortie**. Résultat :

```text
lignes écrites                339
fichiers distincts couverts   195      ← sur 300 attendus
```

Un rapport écrit à ce moment-là aurait annoncé « 0 échec » sur un périmètre
**incomplet de 35 %**, en le présentant comme complet.

Ce qui l'a révélé n'est pas une intuition : c'est un **contrôle de cohérence
interne** — comparer le nombre de lignes, le nombre de fichiers distincts, et le
dénominateur attendu. Les trois devaient coïncider ; ils ne coïncidaient pas.

*Un « 0 » n'a de valeur que si le dénominateur est vérifié, pas supposé.*

**Un bénéfice secondaire de l'incident** : les 202 fichiers passés deux fois
donnent une mesure gratuite de reproductibilité — **202 verdicts identiques sur
202**, aucun test instable parmi eux.

Le balayage a été complété sur les 98 fichiers manquants, puis consolidé :
300/300.

Le harnais lui-même a été validé avant emploi par un **témoin positif** — un
fichier de test délibérément faux, correctement rapporté `1 failed`.

## Ce que ce balayage ne dit pas

Il teste **une** direction : *un fichier a-t-il besoin des autres pour passer ?*
Il ne teste pas la direction inverse — *un fichier casse-t-il les suivants ?* —
qui est celle du lot 401, trouvée par un autre chemin (empreinte d'état global,
puis rejeu d'une queue de 66 fichiers).

Il ne teste pas non plus les ordres **intermédiaires** : 300 fichiers admettent
un nombre d'ordonnancements qu'aucun lot ne balaiera. Ce qui est établi est
exactement ceci : **isolation complète → vert partout**, et **ordre nominal →
vert**.

## Un chiffre trouvé en chemin — le dossier du 401, quantifié

Les 300 exécutions isolées tournent avec un `persist._BASE_DIR` **réel** — la
redirection accidentelle de la fixture du lot 392 ne s'applique pas hors de son
module. Effet mesuré sur l'état runtime :

```text
skyler_decisions.json    11 entrées → 18      (+7 écrites par les tests)
skyler_memory.json        3 clés    →  3      (contenu réécrit, taille stable)
```

Le lot 401 avait établi que la queue de 66 fichiers écrivait dans ces deux
fichiers ; on sait maintenant **combien** : **7 décisions journalisées dans le
journal réel de l'utilisateur** pour une passe isolée complète. Ce n'est pas une
piste nouvelle, c'est le **même dossier de rang 2**, désormais chiffré. Restauré
à l'octet, comme le reste.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — ni production, ni test, ni gardien. Pas de preuve
  MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition. Le balayage a
  modifié `ai_enrichment`, `desk_data`, `skyler_decisions`, `skyler_memory` ; la
  suite complète a ensuite ré-horodaté `ai_enrichment`, `desk_data`,
  `weekly_snapshot`. **Tous restaurés** ; écart final **aucun**, aucun fichier
  apparu.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Septième lot court, septième point de contrôle distinct. Celui-ci confirme par la
mesure ce que le 401 laissait espérer, et il ferme la question : **la dépendance
d'ordre trouvée au 401 était la seule détectable par isolation.**

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388, tous les dossiers de rang 1 à l'arrêt.
