# SIGNAL OS · LOT 53 — QUINZE HÔTES, AUCUN DÉFAUT, TROIS FAUTES D'INSTRUMENT

Branche : `agent/vertex-signal-os-v1` · SW **v238, inchangé** (aucun octet servi
touché) · Suite **3 437 passed** (3 432 → +5)

Ce lot paie la réserve SIGNAL-OS-52 §6.4. Le produit en sort **indemne**. Ce qui
en sort corrigé, c'est ma façon de le mesurer — trois fois.

---

## 1. Le verdict

`tools/mesurer_hotes_resolus.py` conduit la fiche Analyse dans ses deux régimes
et relève ses **quinze** hôtes `%%LOADING%%`.

| mode | résultat |
| --- | --- |
| nominal | 15/15 aboutissent · résolution complète en **~2 s** |
| **données coupées** (500 sur toutes les routes de données) | 15/15 aboutissent · résolution complète en **~9,5 s** |

Les deux durées varient d'une exécution à l'autre — c'est pourquoi l'outil rend
le temps mesuré au lieu de le supposer, et pourquoi il attend une condition
plutôt qu'un délai (§3).

Sous coupure totale, chaque hôte **nomme sa panne** : « Skyler injoignable :
HTTP 500 », « ⚠ Décision indisponible · Réessayer · Ouvrir Système », « ⚠ Bureau
non synchronisé ». Aucun squelette perpétuel, aucun chiffre inventé, aucun vide
muet. C'est exactement la règle produit — *donnée absente → état honnête* — et
elle tient sous panne totale, ce qu'aucun gardien d'octets ne pouvait établir.

---

## 2. Ce que « hôte » veut dire, et pourquoi ma première réponse était fausse

Premier jet : « tout `[id^="an-"]` ou `[data-body]` sans texte est un hôte qui
n'aboutit pas ». Cinq accusations. **Quatre étaient corrects**, chacun pour une
raison différente :

| élément | pourquoi il est vide | ce que j'avais manqué |
| --- | --- | --- |
| `#an-catalyst-strip` | porte `hidden`, `display:none` | je ne testais que les `<details>` fermés |
| `#an-fav` | `<button>` à icône SVG, `aria-label` posé | un contrôle n'est pas un hôte |
| `#an-order-ticket` | rempli **au clic** sur « Calculer le dimensionnement » | vide au repos par construction |
| `#an-fresh` | il affichait « DÉMO » — je l'avais lu trop tôt | voir §3 |

C'est la faute du lot 51 sous un nouveau visage : **j'ai pris l'absence de
contenu pour un défaut sans demander si le produit l'avait voulue.** Absence de
contenu n'est pas promesse rompue.

La bonne définition était dans le titre de l'outil, et je ne l'avais pas suivie :
**un hôte est un élément qui a porté un squelette.** Lui seul a promis du
contenu ; lui seul peut manquer à sa promesse.

Deuxième correction de la même définition : marquer les hôtes depuis le test,
après `domcontentloaded`, en attrapait **12 sur 15**. Les trois manquants sont
les plus **rapides** — résolus avant que la sonde n'ouvre l'œil. Une sonde qui
perd les hôtes rapides mesure la lenteur du produit, pas ses promesses. Le
marquage est désormais un script d'initialisation exécuté à `DOMContentLoaded`.

### Au passage : `#an-order-ticket` en lecture seule

Le nom appelait une vérification. C'est un **calculateur de dimensionnement**,
titré « Dimensionnement indicatif — aucune exécution », dont la seule sortie est
un presse-papiers avec le message « Ticket d'analyse copié — aucune
transmission ». Aucun chemin d'ordre. L'invariant READONLY est intact.

---

## 3. La faute la plus instructive : j'ai accusé le produit d'un défaut qui était mon chronomètre

Premier verdict du mode `--couper` : « **trois hôtes restent squelettes pour
toujours** » — Compatibilité portefeuille, Historique et suivis, Options
associées. J'ai instrumenté `loadDossier` avec des marqueurs d'étape pour
trouver où elle mourait. Le point d'arrêt **se déplaçait d'une exécution à
l'autre** : `(aucune)`, puis `06-avant-hero`, puis `avant-11-options`.

Un point d'arrêt qui bouge n'est pas une panne. C'était **moi qui lisais en
cours de route**. Mesuré en suivant l'état dans le temps :

```text
t= 5s  squelettes=11    options=SQ  portefeuille=SQ  historique=SQ
t=10s  squelettes= 3    options=SQ  portefeuille=SQ  historique=SQ
t=15s  squelettes= 0    options=ok  portefeuille=ok  historique=ok
```

Sous coupure totale, la fiche dégrade **entièrement**, en une quinzaine de
secondes : chaque `fetch` en échec coûte ~1,8 s et ils s'enchaînent en série.
Lent — et ce n'est pas un défaut.

C'est la leçon du lot 48 — *une attente fixe transforme une course en tirage au
sort* — commise par moi **dans le lot même qui la cite**. L'outil attend
désormais une **condition** (plus aucun squelette), jusqu'à un plafond franc, et
rend le temps qu'il a fallu.

J'ai failli « corriger » un produit sain. Trois hypothèses successives — un
`VX.fetch` qui pend, une garde anti-course qui abandonne, un `catch` manquant —
étaient toutes fausses, et chacune aurait produit un correctif inutile dans du
code qui marche.

---

## 4. Le gardien tient peu, et c'est délibéré

J'ai voulu un gardien statique : « chaque `async function load*` contient un
`catch` qui peint ». Mesuré sur les six loaders, ma détection en donnait
**quatre sur six** : `loadDecisionStack` était compté comme ne peignant pas,
alors que le navigateur le voit afficher « ⚠ Décision indisponible » sous
coupure. La cause est banale — une expression régulière `[^}]*` ne traverse pas
des accolades imbriquées. **Comparer par le texte ce qui doit l'être par la
structure**, encore.

Livrer ce gardien, c'était livrer un test faux pour deux loaders sur six. Le
comportement se prouve au navigateur ; `tests/test_signal_os_hotes_lot53.py` ne
tient donc que des faits **structurels** — mais il les tient vraiment :

1. la fiche sert bien ses **quinze** squelettes (sans eux l'instrument devient
   aveugle, car le squelette *définit* l'hôte) ;
2. les **trois** libellés de disclosure que l'outil clique existent toujours
   (`Analyse approfondie`, `Évidence historique`, `Contextes du dossier`) ;
3. le peintre `body(id, html)` cible toujours `#id [data-body]`.

### Le troisième test était creux, et la mutation l'a dit

Première version du test 3 : je cherchais la sous-chaîne
`querySelector('#'+id+' [data-body]')`. Elle apparaît **deux fois** — dans
`body()` et dans le `$b` de `loadAnalyst`. Contre-épreuve : j'ai cassé la cible
du **vrai** peintre, et le test est resté vert, satisfait par l'occurrence
voisine. Il vise maintenant la définition entière. Troisième fois de la série
qu'une occurrence voisine me donne un gardien creux.

Les trois mutations sont attrapées, chacune par un seul test.

---

## 5. Réserves

1. **Une seule page.** La fiche Analyse. Les sept autres espaces ont leurs
   propres hôtes et ne sont pas balayés — l'instrument est générique, seule la
   liste des disclosures à ouvrir est propre à cette page.
2. **Un seul titre, une seule largeur.** `ACN` à 1440 px.
3. **Deux régimes, pas tous.** Nominal et coupure **totale**. Une panne
   *partielle* — une source sur cinq en échec — n'est pas mesurée, et c'est le
   cas le plus fréquent en vrai.
4. **Le plafond est à 45 s.** Au-delà, l'outil accuse. Ce seuil est un choix, pas
   une mesure : si le produit ralentit légitimement, il faudra le rehausser
   sciemment plutôt que subir un faux positif — et se souvenir du §3 avant de
   conclure à un défaut.
