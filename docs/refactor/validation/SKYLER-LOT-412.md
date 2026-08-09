# SKYLER LOT 412 — Le gardien de la règle n°3 détecte le changement d'asset, mais n'impose pas le bump

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-412` (base : lot 411 fusionné,
858704b)

La règle critique n°3 protège le **repli hors-ligne** : si un octet de `/static`
change sans bump du service worker, un visiteur déjà venu et hors ligne garde
l'ancienne copie. Le gardien du lot 361 est censé l'imposer. **Personne n'avait
vérifié qu'il l'impose vraiment.**

**Aucun code, aucun gardien, aucun test.**

## D'abord la concordance : les trois sources s'accordent

```text
version SERVIE      (vertex/app/routes/system.py)         v187
version ENREGISTRÉE (tests/test_sw_cache_scope_lot361.py) v187
empreinte ENREGISTRÉE                                     f83645b51509e515c016e581…
empreinte RECALCULÉE sur les 54 fichiers de /static       f83645b51509e515c016e581…   IDENTIQUE
```

Rien à redire : le contrat enregistré décrit bien l'état servi.

## La question que personne n'avait posée

Le message d'aide du gardien est explicite :

> *« À faire dans le MÊME commit : 1. bumper `const CACHE='td-shell-vN'` … ;
> 2. remettre à jour `_EMPREINTE` et `_SW_VERSION` dans ce fichier. »*

**Le point 1 est-il une obligation ou une demande ?**

## L'expérience — le scénario du développeur pressé

Simulé exactement : un octet ajouté à `vertex/static/vertex/css/tokens.css`,
puis `_EMPREINTE` mise à jour **comme le gardien le demande**, et
`const CACHE='td-shell-v187'` **laissé tel quel**.

```text
asset modifié · empreinte mise à jour · CACHE inchangé (v187)
suite complète →  2864 passed
```

**Verte.** Un fichier servi a changé, le repli hors-ligne n'a pas été purgé, et
rien dans les 2 864 tests ne le signale.

Pourquoi : `test_les_assets_servis_correspondent_a_la_version_enregistree`
compare l'empreinte — satisfaite dès qu'on la réécrit. Et
`test_la_version_enregistree_n_est_jamais_en_avance_sur_le_service_worker`
n'exige que `_SW_VERSION <= _version()`, soit `187 <= 187`. **Aucun test
n'exige que la version AUGMENTE quand l'empreinte change.**

## Ce qui atténue — et qu'il faut dire

Le trou n'est **pas silencieux**. Avant d'en arriver là, le développeur voit
échouer le gardien, avec l'instruction en toutes lettres :

```text
E   1. bumper `const CACHE='td-shell-vN'` dans vertex/app/routes/system.py …
E   Empreinte mesurée : 765c3c5cc0833e05…
```

Il faut donc **obéir à la moitié de l'instruction** pour produire le défaut, pas
simplement l'oublier. C'est une différence réelle : le gardien informe, il
n'automatise pas.

## Pourquoi je ne le corrige pas

La correction évidente — « exiger que `_SW_VERSION` augmente quand `_EMPREINTE`
change » — **n'est pas implémentable dans le fichier lui-même** : les deux
constantes sont éditées par le commit qu'on veut contrôler, donc l'ancienne
valeur a déjà disparu au moment où le test s'exécute. Un registre append-only
(`{187: 'f83645…'}`) déplace le problème sans le fermer : une entrée reste
éditable sur place.

**La seule vérification robuste lit l'historique git** — comparer les valeurs du
commit précédent. C'est un instrument d'un autre ordre que ceux de la suite
actuelle (aucun test ne lit git aujourd'hui), et c'est une décision de
conception, pas une réparation d'agent. **Classé rang 3** : le défaut est réel
mais son exploitation demande d'ignorer une consigne affichée.

*Un contrat écrit dans le fichier qu'il contrôle ne peut pas s'imposer à qui
édite ce fichier.*

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché à l'arrivée.** La sonde a modifié `tokens.css` et le
  gardien 361, tous deux **restaurés à l'octet** (`git status` vide, empreinte
  recalculée de nouveau égale à l'enregistrée, v187 = v187). Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels ré-horodatés par les passes de suite, restaurés. Écart
  final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Ce lot teste **une** faille précise : mettre à jour l'empreinte sans bumper. Il
ne dit pas que le gardien soit faible ailleurs — le lot 394 avait rejoué la
règle n°3 avec une faute réelle (fichier `/static` modifié sans rien toucher
d'autre) et **elle mordait**. Les deux résultats se complètent : le gardien
**détecte** le changement d'asset ; il **n'impose pas** la conséquence.

## Où en est la boucle

Seizième lot court. Le point contrôlé change encore de famille : après les
provenances (411), le contrat de cache. Le défaut trouvé est **structurel et
borné** — il vit dans la façon dont un gardien peut se garantir lui-même.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
