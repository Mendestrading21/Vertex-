# SIGNAL OS · LOT 54 — « QUOI FAIRE », ET AUCUN MOTEUR N'ÉTAIT ENFERMÉ

Branche : `agent/vertex-signal-os-v1` · SW **v238 → v239** · Suite **3 442 passed**
(3 437 → +5)

---

## 1. L'inventaire, corrigé pour la cinquième fois — et cette fois c'était la méthode

SIGNAL-OS-52 §3 annonçait **cinq moteurs enfermés** : ne sortant d'aucune route
servie. Re-mesuré moteur par moteur, par son **appelant** et par sa **clé de
sortie** plutôt que par son nom :

| moteur | sortie réelle | route servie | lu par l'UI avant ce lot |
| --- | --- | --- | --- |
| `decision_evidence` | `contexts.data_quality` · `contexts.reconciliation` | `/api/skyler/<sym>` | **oui** — peint au lot 51 |
| `decision_readiness` | `decision.readiness` | `/api/skyler/<sym>` | non → **ce lot** |
| `walk_forward_validation` | le corps entier | `/api/skyler/validation` | non |
| `historical_stress` | `stress_test` | `/api/portfolio/context` | non |
| `option_cohort` | le corps entier | `/api/tracking/options/cohort` | non |

**Aucun des cinq n'est enfermé.** Tous atteignent une route servie ; quatre
étaient seulement **muets**.

La cause de l'erreur mérite d'être nommée précisément, parce qu'elle n'est plus
du même ordre que les quatre précédentes. Celles-là étaient des listes fausses ;
celle-ci était **la méthode de la sonde**. `tools/mesurer_moteurs_muets.py`
cherche `"nom_du_module"` dans le corps des réponses. Cela ne marche que si un
moteur publie sous une clé qui porte son nom de fichier. Or :

- `decision_readiness` publie sous `readiness` ;
- `walk_forward_validation` et `option_cohort` **servent le corps entier** d'une
  route dédiée, qui ne se nomme donc jamais lui-même ;
- `historical_stress` sort sous `stress_test` ;
- `decision_evidence` alimente deux contextes aux noms sans rapport.

*Une sonde qui cherche des noms de fichiers dans du JSON mesure ma convention de
nommage, pas le produit.* Le seul relevé fiable passe par l'**appelant** —
`grep` du module dans les routes — puis par la **clé** qu'il écrit.

**Conséquence pratique, et elle est bonne :** le travail restant est de
**peindre**, pas d'**exposer**. Aucune route à créer. C'est bien moins de travail
que les rapports 49 et 52 ne l'annonçaient.

---

## 2. Ce que ce lot peint : `decision.readiness`

C'est le complément exact du lot 50. `opportunity_attribution` dit **ce qui
manque** au score ; `readiness` dit **quoi faire, dans quel ordre**, pour que le
dossier devienne décidable — et pourquoi il ne l'est pas encore.

| statut du moteur | libellé à l'écran |
| --- | --- |
| `BLOCKED_BY_GATE` | bloqué par une règle |
| `EVIDENCE_REQUIRED` | preuves à collecter |
| `SCORE_INCOMPLETE` | score incomplet |
| `ANALYTICAL_REVIEW_READY` | prêt pour **revue analytique** |

Le quatrième libellé est pesé : « prêt » tout court se lirait comme un feu vert
d'achat. Le moteur parle de préparation **analytique**, et la page dit exactement
cela.

Sous le statut, la liste des points à traiter, chacun avec sa raison telle que le
moteur la donne : « Collecter régime de marché — contexte indisponible »,
« Résoudre la gate RR_BELOW_2 — … ». Liste **bornée à cinq**, et le total
annoncé : une troncature silencieuse ferait croire le dossier plus proche d'être
complet qu'il n'est.

### READONLY — le mot « actions » ne doit pas pouvoir se lire comme un ordre

Le moteur nomme `actions` une liste d'actes **analytiques** : collecter un
contexte, évaluer une règle. Il porte lui-même `read_only: true` et « ne
constitue jamais une instruction d'exécution ». Dans un produit dont l'invariant
absolu est de ne jamais passer d'ordre, laisser planer le doute serait un défaut
grave. Le bloc s'intitule donc « **Préparation — diagnostic analytique, jamais
une instruction d'exécution** », et un gardien tient cette phrase à l'écran ainsi
que l'absence de tout verbe d'ordre sur la fiche.

---

## 3. Vérifié au pixel, pas seulement à l'octet

`tools/mesurer_blocs_peints.py` (lot 52) couvre désormais quatre blocs :

```text
contextes (lot 49)             PEINT  lignes 3/3 dans le bloc
fiabilité (lot 50)             PEINT  lignes 3/3 dans le bloc
contextes du dossier (lot 51)  PEINT  lignes 3/3 dans le bloc
préparation (lot 54)           PEINT  lignes 2/2 dans le bloc
#an-skyler : 3 013 caracteres ecrits · 3 103 montres
```

`#an-skyler` passe de 2 465 à 3 013 caractères. `tools/mesurer_hotes_resolus.py`
confirme que les quinze hôtes aboutissent toujours.

---

## 4. Le gardien, et ses quatre mutations

`tests/test_signal_os_preparation_lot54.py` — chaque mutation est attrapée par
**un seul** test :

| mutation | test qui tombe |
| --- | --- |
| `+preparation(d)` retiré du rendu | le site d'appel (leçon du lot 49) |
| clause « jamais une instruction d'exécution » retirée | la garde READONLY |
| un statut du moteur privé de libellé | la table de traduction |
| « · 5 affichés » retiré | la troncature annoncée |

Le test des statuts mérite un mot : il **lit les statuts dans le moteur**
(`vertex/engines/decision_readiness.py`) au lieu de les recopier. Une liste
recopiée diverge dès le premier ajout, et l'écran afficherait alors un jeton en
majuscules — laid et incompréhensible. Ce test-là attrape un défaut qui n'existe
pas encore.

---

## 5. Réserves

1. **Trois moteurs muets restent** : `walk_forward_validation` (route
   `/api/skyler/validation`), `historical_stress` (`stress_test` dans
   `/api/portfolio/context`), `option_cohort` (`/api/tracking/options/cohort`).
   Aucun n'a sa place sur la fiche Analyse — ils appartiennent respectivement à
   Système, Portefeuille et Journal/suivi. Les peindre est un travail de même
   nature, sur trois pages différentes.
2. **`tools/mesurer_moteurs_muets.py` porte encore la méthode fautive** du §1.
   Il n'a pas été corrigé dans ce lot ; s'y fier de nouveau reproduirait
   l'erreur. Le corriger demande de partir des **appelants**, ce qui est un autre
   instrument, pas un correctif d'une ligne.
3. **Un seul titre, une seule largeur** pour la vérification au pixel : `ACN` à
   1440 px, en mode démonstration.
4. **L'état `ANALYTICAL_REVIEW_READY` n'a pas été observé à l'écran** — le jeu de
   démonstration ne le produit pas. Le libellé existe et le gardien le vérifie
   dans les octets ; son rendu réel reste non mesuré.
