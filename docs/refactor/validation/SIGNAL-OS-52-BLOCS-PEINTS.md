# SIGNAL OS · LOT 52 — LE PIXEL, ET UN INVENTAIRE FAUX DE QUINZE SUR VINGT

Branche : `agent/vertex-signal-os-v1` · SW **v238, inchangé** (aucun octet servi
touché : ce lot n'ajoute qu'un instrument, un gardien et deux documents) ·
Suite **3 432 passed** (3 413 → +19)

Ce lot ne livre pas une fonctionnalité. Il paie une réserve que j'avais écrite
moi-même au lot 49, et il corrige un chiffre que j'avais publié faux.

---

## 1. La réserve, et pourquoi elle n'était pas une formalité

SIGNAL-OS-49 §5.2, de ma main :

> Le rendu n'est pas vérifié au navigateur dans ce lot : le gardien prouve que
> le câblage existe et que la donnée arrive, **pas que le pixel s'affiche**.

Les gardiens des lots 49-51 lisent les **octets servis**. Ils voient le site
d'appel `+contextes(d)` et la clé dans la réponse de l'API. Ni l'un ni l'autre
ne prouve qu'un humain voit quelque chose. Trois défauts très ordinaires passent
dessous : un bloc dont toutes les gardes `if` retombent et qui rend une chaîne
vide ; un conteneur de hauteur nulle ; une exception plus haut dans `loadSkyler`.

`tools/mesurer_blocs_peints.py` mesure la seule chose qui compte : **le texte
que la page affiche**.

---

## 2. Le verdict, et le fait que seul le navigateur pouvait donner

```text
temoin API : 6 moteurs · 21 contextes sur ACN
temoin ecran : « Objection » peint
  disclosure Analyse approfondie      ouverte au clic
  disclosure Contextes du dossier     ouverte au clic
#an-skyler : 2465 caracteres ecrits · 2541 montres · 136 elements de hauteur non nulle

contextes (lot 49)             PEINT  lignes 3/3 dans le bloc
fiabilité (lot 50)             PEINT  lignes 3/3 dans le bloc
contextes du dossier (lot 51)  PEINT  lignes 3/3 dans le bloc
```

Neuf lignes sur neuf, zéro erreur JS. **Et le chemin nominal est atteint** : sur
`ACN`, `regime_break` répond `available: true` — la réserve §5.3 du lot 49
(« ce sont leurs états honnêtes qui s'affichent, pas le chemin nominal ») tombe
elle aussi. Les deux autres montrent leur état honnête, ce qui met les deux
chemins sur le même écran.

### Le fait que les gardiens d'octets ne pouvaient pas voir

Premier relevé : `#an-skyler` portait **2 426 caractères de `textContent` pour
ZÉRO de `innerText`**, dans une chaîne d'ancêtres tous `display:block` et
`visibility:visible`. Rien n'était masqué. La cause : un
`<details id="an-deep-analysis">` **fermé** — 86 px de haut pour un contenu de
1 529 px. Les trois blocs vivent **deux disclosures en profondeur**.

C'est un choix assumé, écrit dans la source : *« Expertise à la demande : les
moteurs continuent tous de charger, mais leurs sorties secondaires ne
concurrencent plus le verdict canonique. »* Je ne le change pas — mais c'était
invisible depuis les octets, et tout le chemin de peinture en dépend. Un test
le fige désormais, y compris le fait que la disclosure **n'est pas ouverte
d'office** : ce serait un autre produit.

Corollaire d'outillage : `innerText` est ici le bon instrument **parce qu'il**
exclut le contenu d'un `<details>` fermé. `textContent` aurait déclaré « peint »
un contenu que personne ne voit.

---

## 3. L'inventaire du §4 était faux de quinze sur vingt

SIGNAL-OS-49 §4 nommait **vingt** moteurs « n'atteignant aucune réponse
servie ». Mesuré sur les **162 routes GET servies**, témoin à l'appui : **cinq**.

**Douze** sortaient déjà dans `packet.contexts`, sous des clés plus courtes que
leur nom de module — et sont peints depuis le lot 51 par le bloc générique :

| moteur (nom du §4) | clé réellement publiée |
| --- | --- |
| `relative_volume_context` | `contexts.relative_volume` |
| `relative_strength_context` | `contexts.relative_strength` |
| `iv_skew_context` | `contexts.iv_skew` |
| `iv_term_structure` | `contexts.iv_term_structure` |
| `open_interest_concentration` | `contexts.open_interest_concentration` |
| `earnings_proximity` | `contexts.earnings_proximity` |
| `gap_risk_context` | `contexts.gap_risk` |
| `drawdown_context` | `contexts.drawdown` |
| `downside_volatility` | `contexts.downside_volatility` |
| `fundamental_context` | `contexts.fundamentals` |
| `anomaly_context` | `contexts.anomalies` |
| `call_put_structure` | `contexts.call_put_structure` |

**Trois** autres (`multi_asset_guard`, `opportunity_attribution`,
`opportunity_reliability`) sortent dans `decision` et sont peints depuis le
lot 50.

> ⚠ **CORRIGÉ AU LOT 54 — « restent cinq » est faux : il n'en reste AUCUN
> d'enfermé.** Le tableau ci-dessous est exact sur les emplacements et faux sur
> le verdict. Ma sonde cherchait le **nom du module** dans les corps de réponse ;
> or `decision_readiness` publie sous `decision.readiness`,
> `walk_forward_validation` et `option_cohort` servent des corps entiers qui ne
> se nomment jamais, `historical_stress` sort en `stress_test`, et
> `decision_evidence` alimente `contexts.data_quality`. Les cinq atteignent une
> route servie. **Cinquième fois** qu'une hypothèse de nommage me trompe dans
> cette série, et cette fois elle était dans la *méthode* de la sonde, pas dans
> une liste. Inventaire corrigé et figé : `SIGNAL-OS-54-PREPARATION.md` §1.

**Restent cinq**, et leur emplacement dit pourquoi :

| moteur | fichier | ce que l'emplacement implique |
| --- | --- | --- |
| `decision_evidence` | `vertex/engines/` | exposable sur la fiche |
| `decision_readiness` | `vertex/engines/` | exposable sur la fiche |
| `walk_forward_validation` | `vertex/engines/` | exposable sur la fiche |
| `historical_stress` | `vertex/portfolio/` | **pas un moteur par titre** — demande une route de portefeuille |
| `option_cohort` | `vertex/tracking/` | **pas un moteur par titre** — demande une route de suivi |

Ce dernier point n'est pas un détail de rangement : deux des cinq n'ont rien à
faire sur `/api/skyler/<sym>`, et les chercher là serait la cinquième version de
la même erreur.

Le chiffre honnête (5) vaut mieux que le chiffre confortable (20) : il annonçait
un chantier quatre fois plus gros qu'il n'est.

---

## 4. Ce que la contre-épreuve a corrigé — dans l'instrument, puis dans le gardien

Quatre fautes, trouvées en essayant de faire échouer mon propre travail.

**4.1 Un témoin supposé au lieu d'être lu.** J'avais pris « Score Skyler »
comme témoin d'écran. Ce libellé n'existe pas. Et le titre statique
« Diagnostic moteurs » n'aurait pas convenu non plus : il est dans le HTML
servi et resterait affiché même si `loadSkyler` échouait — *un témoin qui
survit à la panne qu'il doit détecter ne témoigne de rien.* Le bon est
« Objection : », dernière chose que `loadSkyler` écrit avant les trois blocs.

**4.2 La sonde comptait des occurrences voisines.** Bloc 51 supprimé, elle
annonçait quand même « lignes 3/3 ». « Technique », « Catalyseurs » et
« Marché » sont des mots courants : ils vivent aussi dans les cartes de
dimensions et dans le détail du score. Je mesurais la page, pas le bloc. Chaque
ligne est désormais cherchée **dans le sous-arbre de son bloc**. C'est
exactement le piège qui m'avait déjà eu deux fois en écrivant le gardien du
lot 51 — et il a suffi de changer d'organe de mesure pour qu'il revienne.

**4.3 Le conteneur n'est pas l'ancre.** Première version du découpage : « le
plus petit élément portant l'ancre ». Elle rendait 0/3 sur un bloc intact,
parce que l'ancre est un libellé qui est le **frère** des lignes, pas leur
parent. Un pas vers le parent, borné, jamais au-dessus de `#an-skyler` — et non
« remonter jusqu'à trouver ce que je cherche », qui finirait toujours par
réussir et ne prouverait rien.

**4.4 Des préfixes de module inventés.** Le gardien cherchait les cinq moteurs
enfermés sous une liste de préfixes de mon cru ; il en manquait deux. C'est
cette erreur qui a révélé que `historical_stress` et `option_cohort` ne sont pas
des moteurs par titre (§3). Le test fige maintenant le **chemin mesuré**.

### La contre-épreuve, dans les deux sens

Site d'appel muté (`+contextes(d)` et `+contextesDossier(r)` retirés), serveur
relancé, sonde rejouée :

```text
contextes (lot 49)             ABSENT  ancre=NON · lignes 0/3 dans le bloc
fiabilité (lot 50)             PEINT   ancre=oui · lignes 3/3 dans le bloc
contextes du dossier (lot 51)  ABSENT  ancre=NON · lignes 0/3 dans le bloc
EXIT=1
```

La sonde **discrimine** : elle accuse les deux blocs retirés et laisse intact
celui qu'on n'a pas touché. Une sonde qui serait tombée en bloc n'aurait rien
prouvé.

Le gardien pytest a subi trois mutations, chacune attrapée par **un seul** test :
clé de packet renommée (`drawdown` → `drawdown_renomme`), disclosure ouverte
d'office (`open`), moteur enfermé déplacé.

---

## 5. Pourquoi le renommage d'une clé méritait un test à lui seul

Le bloc du lot 51 est **générique** : il lit `packet.contexts` en entier. C'est
sa qualité — il accueillera le vingt-deuxième contexte sans une ligne de code.
C'est aussi son angle mort : renommer une clé n'y casse rien de visible, la
ligne disparaît **en silence**. Nommer les douze correspondances, c'est rendre
cette disparition bruyante.

---

## 6. Réserves

1. **Un seul titre, un seul viewport.** `ACN` à 1440 px. Les instruments des
   lots 42/46 balaient cinq largeurs ; ils n'ont pas été rejoués ici.
2. **Le mode démonstration, pas le marché.** Aucune donnée de marché n'est
   joignable depuis ce conteneur ; les valeurs peintes sont celles du jeu de
   démonstration, étiqueté comme tel à l'écran. Ce lot prouve le **chemin de
   peinture**, pas la justesse d'un chiffre de marché.
3. **Cinq moteurs restent enfermés** (§3). Trois sont exposables sur la fiche ;
   deux demandent une route de portefeuille ou de suivi — travail de nature
   différente, à ne pas confondre.
4. ~~**La sonde ne mesure que trois blocs.**~~ — **PAYÉE au lot 53.**
   `tools/mesurer_hotes_resolus.py` mesure les **quinze** hôtes de la fiche, en
   nominal **et sous coupure totale des données**. Verdict : tous aboutissent
   dans les deux modes, et sous coupure chacun nomme sa panne. Aucun défaut
   produit — mais trois fautes d'instrument, dont la plus instructive est un
   verdict « trois hôtes bloqués » qui n'était qu'une attente trop courte. Voir
   `SIGNAL-OS-53-HOTES-RESOLUS.md`.
