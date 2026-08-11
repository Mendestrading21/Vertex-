# SKYLER — LOT 603 · LES SILENCES DES AUTRES PAGES, TRAITÉS

Le rapport 602 nommait la suite : « les silences équivalents ailleurs sont
**nommés, pas traités** — ils viennent ensuite ». C'est ce lot.

## Le résultat en un chiffre : 92 → 20 → 4

Trois instruments successifs sur les 8 pages servies, chacun corrigeant le
précédent :

| instrument | critère | compte | verdict |
| --- | --- | --- | --- |
| 1ᵉʳ banc | « le corps du `catch` écrit-il une zone ? » | **52** silences | **faux** |
| 2ᵉ banc | « le `catch` contient-il `return` ? » ∧ « quelque chose suit-il ? » | **48** candidats | **faux** |
| 3ᵉ banc | les deux croisés | **20** muets | juste, mais brut |
| **lecture** | rôle réel de chacun des 20 | **4 défauts** | **le résultat** |

**Le compte brut ment d'un facteur treize.** C'est `596-B` — un compte sans rôle
ne prouve rien — payé deux fois dans le même lot.

## Les quatre défauts, corrigés

| page | fonction | API | avant | après |
| --- | --- | --- | --- | --- |
| `/markets?view=macro` | `loadMacroRegime` | `/api/market/summary` | `catch(e){return;}` → **zone vide et muette** | `VX.states.error('Appétit pour le risque indisponible')` |
| `/portfolio?view=risk` | `renderHiddenDeps` | `/api/skyler/graph` | `catch(e){return;}` → **section absente** | la section existe et dit son état |
| `/portfolio?view=risk` | `renderStress` | `/api/portfolio/stress` | `catch(e){return;}` → **section absente** | idem |
| `/portfolio?view=risk` | `renderDiscipline` | `/api/portfolio/context` | `catch(e){return;}` → **section absente** | idem |

Les trois sections de Portefeuille portaient **déjà** un état honnête pour
`d.empty` / `d.available===false` — le moteur savait dire « je n'ai pas la
donnée ». **Seul le chemin réseau restait muet.** Le défaut n'était pas
l'absence d'une idée d'honnêteté : c'était un trou dans son application.

## La preuve, en vrai Chromium, avec l'échec injecté

Six passes, viewport 1440×900, service worker bloqué (**602-B**) :

| passe | erreurs console | texte rendu | zone |
| --- | --- | --- | --- |
| **0. `/markets?view=macro` nominal** | **0** | 2 840 car. | « APPÉTIT POUR LE RISQUE · RISK-OFF · écart −11 » |
| **1. `summary` → 500** | 2 *(injectés)* | **2 636** car. | `⚠ Appétit pour le risque indisponible · Réessayer · Ouvrir Système` |
| **2. `/portfolio?view=risk` nominal** | **0** | 4 746 car. | « DÉPENDANCES CACHÉES (KNOWLEDGE GRAPH) » |
| **3. `skyler/graph` → 500** | 2 *(injectés)* | **3 569** car. | `⚠ Dépendances cachées indisponibles` |
| **4. `portfolio/stress` → 500** | 2 *(injectés)* | **4 115** car. | `⚠ Stress-scénarios indisponibles` |
| **5. `portfolio/context` → 500** | 2 *(injectés)* | **4 463** car. | `⚠ Discipline du portefeuille indisponible` |

**Chaque passe en échec rend une taille différente du nominal** — c'est
**602-A**, la règle née hier, qui exige cette comparaison. Les erreurs console
des passes 1 et 3-5 sont les 500 que j'injecte moi-même.

## L'arrêt du lot — mon harnais a passé à vide, DEUXIÈME fois

Premier jet : **les six passes rendaient une taille identique** (2 775 pour
`/markets`, 1 590 pour `/portfolio`) et **les zones étaient ABSENTES même en
nominal**. Cause : je chargeais `/markets` et `/portfolio` **sur leur vue par
défaut** (`overview`, `team`) alors que les quatre fonctions ne sont appelées
que sur `view=macro` et `view=risk`.

Ce qui a sauvé le lot est **602-A appliquée à la lettre** : le contrôle vérifie
le **texte attendu**, pas la non-vacuité, donc il a dit **NON** au lieu de dire
OUI sur une page qui n'avait jamais exécuté le code corrigé. **La règle écrite
hier a arrêté l'erreur d'aujourd'hui, le lendemain.**

**Arrêtés avant publication : 233 → 234 (+1).**

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « `/opportunities` était l'exception : moins de 5 silences sur les 7 autres pages » | **CONFIRMÉ — 4** |
| **(b)** | « chaque site trouvé est un vrai défaut produit » | **RÉFUTÉ — 16 des 20 sont bénins** |
| **(c)** | « le défaut se concentre sur les pages les plus récentes » | **NON MESURABLE** — 4 cas sur 2 pages, effectif trop petit (595-C) |
| **global** | | **MIXTE** |

**(a) n'aurait pas survécu à un compte brut.** Le premier banc disait 52, le
troisième 20 : les deux réfutaient (a). **C'est la lecture qui l'a confirmé.**
Un piège peut être sauvé par la lecture après avoir été enterré par la mesure.

## Les seize bénins, et pourquoi

| motif | sites | pourquoi ce n'est pas un défaut |
| --- | --- | --- |
| écriture `localStorage` de confort | 2 | rien à l'écran ; l'échec (quota) ne ment sur rien |
| aide pure à valeur de repli (`return null` / `{}` / `[]`) | 4 | **l'appelant décide** — le silence est délégué, pas perdu |
| sonde `session/manifest` | 4 | boucle de veille re-jouée toutes les 60 s (« on ré-essaiera », en commentaire) |
| boucle « au mieux » (désinscription SW, purge de caches, import de clés) | 3 | l'échec d'un élément ne doit pas casser la boucle |
| graphique optionnel dans une carte **déjà rendue** | 2 | la carte parle ; seul le canvas manque |
| enrichissement non bloquant (`loadAnalyst`) | 1 | conçu pour ne pas bloquer le dossier principal |

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure `vertex/ui/pages/*.py`. Le cas exclu : les **fichiers JS
statiques** sous `vertex/static/vertex/js/`, chargés par les mêmes pages.

**88 `catch` · 9 PARLE · 37 REPLI · 42 MUET.** Le compte brut y est **deux fois
plus élevé que sur les pages** (42 contre 20) — et **le nombre de défauts de
zone y est zéro**. Ces fichiers sont de l'infrastructure : magasin, routeur,
coquille, noyau de graphiques, boucles de veille. Le seul cas discutable,
`vx-shell.js::watchSession`, est **une boucle ré-enregistrée toutes les 60 s**
qui porte le commentaire « scan pas encore publié → on ré-essaiera ».

**Le second contrôle inverse le classement du premier**, et c'est sa valeur : là
où le compte est le plus gros, le défaut est nul.

## Ce que le lot n'établit pas

- **Que ce soient les derniers silences du produit.** Je n'ai mesuré qu'**une
  forme** — le bloc `catch`. Les `if(!d)return;` **hors** `catch`, les
  `.catch(()=>{})` en fin de chaîne de promesse et les erreurs avalées par un
  `Promise.allSettled` **ne sont pas dans mon périmètre**.
- Que les 16 bénins le resteront : ce sont des **lectures**, datées d'aujourd'hui.
- Que les vues autres que `macro` et `risk` soient exemptes : j'ai exercé la
  voie d'échec **des quatre corrigées**, pas de toutes les zones des deux pages.

## Règles neuves

- **603-A — UN COMPTE BRUT DE SILENCES MENT D'UN FACTEUR DIX.** 52, puis 20,
  puis **4 après lecture**. Trois instruments, trois nombres, un seul vrai.
  Corollaire opérationnel de `596-B`.
- **603-B — UNE VOIE D'ÉCHEC NE S'EXERCE QUE SUR LA VUE QUI L'APPELLE.** Charger
  la vue par défaut d'une page à onglets ne prouve rien sur le code d'un autre
  onglet — la zone est absente pour une raison qui n'est pas celle qu'on teste.
- **603-C — UN PIÈGE ENTERRÉ PAR LA MESURE PEUT ÊTRE SAUVÉ PAR LA LECTURE.**
  Le volet (a) était réfuté par les deux comptes bruts et **confirmé** par la
  lecture des rôles. L'ordre compte : mesurer, puis lire, puis conclure.

## Ce que le dépôt fait bien

- **Les trois sections de Portefeuille savaient déjà dire « donnée absente »**
  (`d.empty`, `d.available===false`) avec le motif du moteur. Le trou était
  étroit et précis : le seul chemin réseau.
- **37 `catch` sur 92 écrivent déjà un état honnête** — la discipline majoritaire
  du produit est la bonne ; les muets sont l'exception, pas la règle.
- **Aucun des 42 muets du JS statique n'est un défaut de zone.** La séparation
  infrastructure / rendu tient.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **2 fichiers de production modifiés, 5 gardiens de version mis à jour**, bump
  SW `td-shell-v188` → **`td-shell-v189`**.
- MD5 des 8 pages : **6 / 8 identiques** — `/markets` = **`cadcddec50df`**
  (était `c0bb91c6971a`), `/portfolio` = **`61c9516ad3e3`** (était
  `f1b41b665d4a`). Les six autres identiques à l'octet.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**
  (20 fichiers ; 7 modifiés par la session navigateur, restaurés).
- Suite : **2864 passed / 0 skipped**. Aucun test ajouté, aucun retiré.
- Navigateur : **6 passes, 0 erreur console sur les 2 nominales**, les 4 voies
  d'échec exercées et prouvées par le texte attendu.
- **READONLY intact** : aucun ordre, aucun chemin d'écriture touché.

## Comptes

- Arrêtés avant publication : **234 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
- **Dossiers produit corrigés : 2** *(531-A fermé au 602 pour `/opportunities`,
  étendu ici aux 4 silences de `/markets` et `/portfolio`)*
