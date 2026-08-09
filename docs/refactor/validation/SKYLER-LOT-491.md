# SKYLER LOT 491 — Les 7 barèmes non tracés : la liste du 486 confondait TROIS échelles homonymes — et la confiance plafonnée à 50/100 que j'ai mesurée n'est affichée NULLE PART

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-491` (base : lot 490 fusionné,
`a8d60c0c`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le bilan n°17 a conclu que la boucle « a atteint la limite de ce qu'elle peut
apporter seule ». La réponse n'est pas un onzième lot d'introspection : retour au
produit, sur les **7 barèmes nommés mais jamais tracés** du 486.

## Calibration, écrite dans le code du banc

Deux réponses connues, sortie programmée si l'une manque :

```text
score40 du paquet parfait = 29   attendu 29 (485)   OK
facteur calibration       = 0.5  attendu 0,50 (docstring)   OK
```

## Ce que le banc mesure — `confidence()` est bel et bien plafonnée

`skyler_core.confidence()` est un produit de quatre facteurs. Sur le paquet
**parfait** (score technique 100, R:R 99, régime TREND_UP, aucune contradiction,
option qualité 100) :

```text
data_quality   1.0     bloc data_quality 4/4 du score
agreement      1.0     0 contradiction(s) tracée(s)
robustness     0.875   1 bloc insuffisant sur 8 — proxy   ← fundamentals_quality, toujours (485)
calibration    0.5     « aucun historique — facteur plafonné à 0,50, jamais supposé calibré »
─────────────────────────────────────────────────────────
VALEUR 0,438  →  « confiance 44/100 »
```

**Et le plafond n'est PAS structurel** : sur 81 combinaisons, le maximum atteint
est **1,0 → 100/100**, mais **seulement si une calibration réelle est fournie**.

### Est-elle fournie ? Mesuré — non, et pour une raison chiffrée

`/analysis` passe bien `calibration=calib` (`analysis_api.py:164`), tiré de
`decision_memory.calibration_factor_for(...)`. Lu sur le fichier réel :

```text
skyler_memory.json : 29 décisions enregistrées · 0 résultat MESURÉ
calibration_factor_for(level=A|B|REFUS_WATCH|None) → value 0.5
   basis : « échantillon insuffisant (0/20 mesure(s) pour le moteur 0.9.0)
            — facteur plafonné à 0,50, jamais inventé »
```

**Le seuil est 20 mesures. Il y en a 0.** Le facteur vaut donc 0,50 pour tous les
niveaux, et la confiance de Skyler est **aujourd'hui bornée à 50/100**.

Et le **balayage `/opportunities`** ne passe **aucune** calibration
(`skyler_sweep.py:50-51`) — pour lui le facteur est 0,50 **par construction**.

## Le retournement — ce chiffre n'est affiché nulle part

J'allais classer un défaut. **Vérifié dans les octets servis** de
`/analysis/AAPL` : le champ `confidence` de `skyler_core` **n'atteint aucune
surface servie**. Sur les 15 occurrences de `confidence` dans `vertex/ui/` et
`vertex/static/`, **aucune** ne lit celle-là :

```text
briefing.py:209/295   reg.confidence  → confiance du RÉGIME
briefing.py:402       d.confidence    → « Confiance données »
markets_page.py:254/877  r.confidence → confiance d'une ligne de scan
analysis_page.py:752  dec.confidence  → confiance du DECISION_STACK
intelligence_page.py:356  moyenne d'un autre champ
widget_lab.py (×5)    laboratoire de design, non servi
```

Et le balayage `/opportunities` **n'expose même pas** de champ `confidence`
(mesuré sur les 16 champs de ligne de `skyler_sweep`).

**Classification honnête** : un estimateur documenté, plafonné, explicitement
« jamais 100 % », calculé à chaque appel de `/api/skyler/<sym>` — **et jamais
peint**. C'est la famille du 486 : **exact, produit, jamais affiché**. Je le
**nomme, je ne le classe pas** (règle 486 sur les défauts latents), parce qu'un
chiffre non affiché ne peut tromper personne.

## Le vrai résultat : la liste du 486 confondait trois échelles

Le 486 avait rangé sous un même toit « `confiance conf/100` » et
« `accord agreement/100` ». Mesuré, ce sont **trois producteurs différents** :

```text
skyler_core.py:100    'agreement'  facteur de confiance dans [0,1]   ← NON servi
decision_stack.py:251 'agreement'  round(agreement * 100)            ← c'est CELUI-CI qui s'affiche
decision_stack.py:286 'confidence' int(max(0, min(100, …)))          ← c'est CELUI-CI qui s'affiche
skyler_core.py:74     confidence() produit de 4 facteurs             ← NON servi
```

**Dix-neuvième récurrence du piège de l'homonyme**, et la plus coûteuse : j'ai
benché pendant tout un lot un objet **qui n'est pas celui qu'on voit à l'écran**.
Le 484 avait déjà signalé la même chose sur le S+/S de `/opportunities` — la
leçon existait, elle ne m'a pas protégé parce que **je ne l'ai pas appliquée
AVANT de choisir ma cible**.

**Les deux barèmes réellement affichés (`decision_stack`) ne sont PAS mesurés par
ce lot** : `confidence` y est bornée à [0,100] par un `min/max` explicite, donc
son maximum est atteignable **par construction du clamp** — mais je n'ai pas
établi qu'une entrée réelle l'atteint. **Nommés, non tracés. Ils restent dus.**

## Le second contrôle — un cas que le recensement EXCLUT

Le réveil demandait de distinguer un `/100` **barème** d'un `/100`
**pourcentage** : le 486 ne les avait pas séparés. Cas trouvé :
`briefing.py:402` — « Confiance données `d.confidence` % ». Ce n'est **pas** un
barème sur 100 mais un **pourcentage de fraîcheur**, avec un seuil à 70. Le
recensement du 486 l'aurait compté comme un huitième barème. **L'exclusion est
justifiée, et elle montre que la liste des « 7 » n'était pas une population
propre.**

## Deux faux résultats arrêtés avant publication

1. **Ma sonde était mal étiquetée.** Elle annonçait tester « plafonné à 0,50 » et
   ne cherchait que `plafonn` — elle a rendu **PRÉSENT**, ce qui m'aurait fait
   écrire que la page affiche le plafond. Vérifié : l'unique `plafonn` servi est
   `capped_by_gate` (déjà établi au 484), et **« 0,50 » comme « 0.50 » sont
   ABSENTS des octets servis**. *Matcher un motif approximatif n'est pas matcher
   la chose* — pour la troisième fois, et pour la deuxième fois **contre moi**.
2. **J'allais attribuer le plafond de 0,50 au chiffre affiché.** `conf` vient de
   `dec.confidence` (`analysis_page.py:752`), c'est-à-dire du **decision_stack**.
   Sans la trace, je publiais un rang 1 sur un objet qui n'est pas celui-là.

**Arrêtés avant publication : 55 → 57.**

## Portée

- **Aucun rang posé.** Ce lot ne fait grossir la feuille d'aucun dossier — il
  **nettoie une population** et **empêche une fausse publication**.
- `decision_stack.confidence` et `decision_stack.agreement`, **les deux barèmes
  réellement à l'écran**, restent **non tracés** : c'est la dette de ce lot, et
  je la nomme.
- `best.score /100`, `edge /100`, `r.score /100` (`/opportunities`),
  `count + ' / 10 max'` et `rating_mean/5` : **non tracés non plus**. Le lot en a
  traité **deux** des sept, et a montré que **deux autres étaient mal identifiés**.
- Le compte « 0/20 mesures » est lu sur **le fichier runtime réel**, en lecture
  seule. Il changera si des résultats sont mesurés — **le plafond de 0,50 est un
  état, pas une propriété permanente**.
- **Aucun navigateur ouvert** : la non-présence de `confidence` est établie sur
  les **octets servis** et sur le recensement des lectures dans `vertex/ui/`.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié**. `score40()`, `confidence()`,
  `calibration_factor_for()` appelés en mémoire — **`skyler_core` ne contient
  aucune écriture (485)**, `decision_memory` lu en **lecture seule**. **Aucune
  route réseau sortante.**
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime : 21 fichiers, aucun apparu, aucun disparu, écart **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le bilan n°17 demandait du produit. Ce lot en a fait — et le produit lui a
répondu que **ma liste de cibles était sale**. Deux des sept « barèmes » du 486
désignaient des objets non affichés ; un huitième candidat était un pourcentage.

Ce n'est pas le lot que j'espérais. C'est celui qui empêche le suivant de se
tromper : **la prochaine mesure partira des DEUX barèmes réellement peints**
(`decision_stack`), pas d'un moteur qui calcule dans le vide.

Comptes séparés : résultats faux **arrêtés avant publication 57 (+2)** ; publiés
puis corrigés **10** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
