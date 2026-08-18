# SIGNAL OS · LOT 49 — TRENTE-QUATRE MOTEURS, ZÉRO PEINT

Branche : `agent/vertex-signal-os-v1` · SW **v235 → v236** · Suite **3402 passed**

La fusion du lot précédent a fait entrer 171 commits de `main` — **34 moteurs
neufs, +8 056 lignes**. La question qui décide de leur valeur n'est pas
« compilent-ils ? » mais **« l'écran en montre-t-il quelque chose ? »**.

---

## 1. La mesure : vingt-trois clés, vingt-trois fois zéro

Pour chaque sortie des moteurs neufs, recherche de la clé dans `vertex/ui/**` et
dans le JS servi :

```text
regime_break … sector_coherence … historical_stress … decision_evidence …
walk_forward_validation … option_cohort … open_interest_concentration …
                                                    interface : 0
```

**Aucune** n'est lue. Vérification côté Python d'abord, pour ne pas accuser à
tort : les 34 modules sont tous importés au moins une fois — ils ne sont pas
morts. Ils sont **muets**.

Trois d'entre eux atteignaient déjà la réponse servie de `/api/skyler/<sym>`,
sous `decision.regime_break`, `.sector_coherence` et `.instrument_profile` —
mesuré sur la réponse réelle, pas déduit du code.

C'est le motif du dossier **454**, en toutes lettres : *une conséquence
CALCULÉE, SÉRIALISÉE et ENVOYÉE n'est toujours pas AFFICHÉE.*

---

## 2. Ce que ce lot branche

Les trois sont peints sur la fiche Analyse, **sans un appel de plus** : la
donnée était déjà sur le fil dans `loadSkyler`, il suffisait de la lire.

| moteur | ce qu'il répond |
| --- | --- |
| `regime_break` | le régime a-t-il rompu ? volatilité ×N, décalage en σ, séances observées |
| `sector_coherence` | le secteur confirme-t-il ? écart au secteur, rang, membres |
| `instrument_profile` | à quoi ai-je affaire ? classification, classe d'actif |

**Rendus tels qu'ils se disent.** Les trois portent leur propre état honnête
(`available: false` + `reason`, `classification: 'UNCLASSIFIED'`) : la page
montre la valeur quand elle existe et **la raison du moteur** quand elle
n'existe pas. Jamais un tiret muet, jamais un chiffre de remplissage.

**Annoncés descriptifs.** Les moteurs portent eux-mêmes
`does_not_change_decision: true` et « ne modifie ni le score ni le verdict ».
La page le dit : trois lignes chiffrées posées sous un verdict se liraient
sinon comme un second verdict.

---

## 3. Le gardien a failli être creux, et c'est la partie utile

Première version : elle vérifiait que la chaîne `regime_break` est **servie**.
Elle l'est — dans le **corps** de la fonction `contextes()`, servie qu'elle soit
appelée ou non.

Contre-épreuve : j'ai retiré `+contextes(d)` du rendu, c'est-à-dire le câblage
lui-même. **Les huit tests sont restés verts.**

Le gardien mesurait la présence d'un texte, pas l'existence d'un appel —
exactement la faute que cette série corrige depuis le lot 35, et je ne l'aurais
pas vue sans passer la mutation. Un neuvième test exige désormais le **site
d'appel** ; la même mutation le fait tomber.

Les autres tests tiennent les deux moitiés du contrat : la donnée **arrive**
(clé présente dans la réponse servie) et elle est **lue** (clé présente dans la
page). Sans la première, la seconde passerait sur trois lignes vides.

---

## 4. Ce qui reste à brancher — la liste

> ⚠ **CORRIGÉ AU LOT 52 — ce §4 est faux de quinze sur vingt.** Mesuré sur les
> **162 routes GET servies**, témoin à l'appui : **cinq** moteurs sont
> réellement enfermés, pas vingt. Douze de cette liste sortent dans
> `packet.contexts` sous des clés plus courtes (`drawdown_context` publie
> `contexts.drawdown`) et sont peints depuis le lot 51 ; trois autres sortent
> dans `decision` et sont peints depuis le lot 50. Le chiffre exact et la
> correspondance module → clé sont dans `SIGNAL-OS-52-BLOCS-PEINTS.md` §3, et
> figés par `tests/test_signal_os_blocs_peints_lot52.py`.
>
> La liste ci-dessous est conservée telle qu'elle a été écrite : c'est la
> quatrième fois de la série qu'une hypothèse de nommage me trompe, et l'effacer
> ferait disparaître la seule chose qu'elle enseigne encore.

Vingt des moteurs neufs n'atteignent **aucune** réponse servie mesurée à ce
jour : `decision_evidence`, `decision_readiness`, `relative_volume_context`,
`relative_strength_context`, `iv_term_structure`, `iv_skew_context`,
`open_interest_concentration`, `earnings_proximity`, `gap_risk_context`,
`drawdown_context`, `downside_volatility`, `fundamental_context`,
`anomaly_context`, `multi_asset_guard`, `call_put_structure`,
`opportunity_attribution`, `opportunity_reliability`, `historical_stress`,
`walk_forward_validation`, `option_cohort`.

Chacun demande deux gestes : l'exposer dans une réponse, puis le peindre. Ce lot
en fait trois ; les vingt autres sont un travail de même nature, à faire un par
un — et **c'est de loin le plus gros gisement de valeur non délivrée du produit**.

---

## 4 bis. Suite immédiate (lot 50) — trois de plus, et une leçon

Le §4 annonçait vingt moteurs « n'atteignant aucune réponse servie ». **C'était
faux pour trois d'entre eux**, et la cause est ma mesure, pas le produit : mon
sondage utilisait un titre au dossier pauvre — clôtures parfaitement plates,
aucune date, aucun secteur. Refait avec un historique réaliste (200 clôtures
bruitées, dates, secteur), trois ressortent :

| moteur | ce qu'il rend |
| --- | --- |
| `opportunity_reliability` | **six contrôles** de fiabilité des preuves : données exploitables, portes évaluables, aucune porte déclenchée, réconciliation, score complet, seuil de revue |
| `opportunity_attribution` | **ce qui manque au score** — blocs insuffisants et contextes absents |
| `multi_asset_guard` | anomalies de classe d'actif, avec sévérité |

Ces trois-là valent mieux que les trois du lot 49. `opportunity_attribution`
surtout : c'est le bloc qui transforme un « 12/40 » opaque en quelque chose
d'actionnable — on ne subit plus le score, on voit ce qui lui manque.

Peints avec la même discipline, et leur clause descriptive respectée
(`does_not_change_verdict`, « sans ajustement de score ») : **ils expliquent le
verdict, ils ne le remplacent pas.**

Le sondage mesurait la pauvreté de mon jeu d'essai, pas le produit. C'est la
faute du lot 38, une fois de plus : *un instrument doit reproduire l'état que le
produit peut réellement atteindre.* **Reste donc dix-sept moteurs**, pas vingt —
et ce chiffre-là est à re-mesurer avant d'être cru.

---

## 5. Réserves

1. **Six sur trente-quatre.** Le reste est listé au §4, pas traité.
2. ~~**Le rendu n'est pas vérifié au navigateur dans ce lot**~~ — **PAYÉE au
   lot 52.** Vérifié dans Chromium sur `/analysis/ACN` : les trois blocs
   peignent leurs neuf lignes, contre-épreuve à l'appui. Et la mesure a trouvé
   ce qu'aucun gardien d'octets ne pouvait voir — ils vivent **deux
   `<details>` en profondeur**. Voir `SIGNAL-OS-52-BLOCS-PEINTS.md`.
3. ~~**Le jeu de démonstration ne remplit pas les trois**~~ — **caduque au
   lot 52.** Sur `ACN`, `regime_break` est `available: true` : le chemin
   **nominal** est peint, pas seulement le chemin d'indisponibilité. Les deux
   autres montrent bien leur état honnête (`sector_coherence` sans proxy
   sectoriel, `instrument_profile` non classé), ce qui donne les deux chemins
   sur le même écran.
