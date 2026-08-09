# SKYLER LOT 445 — J'ouvre les phrases que le serveur écrit, et elles sont justes : 15 accords sur 16, le seizième sur un état inatteignable

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-445` (base : lot 444 fusionné,
bc7f37d)

Vingt-septième lot de la veine. Le 444 avait livré **la carte** — 110 phrases
composées au serveur, mesurables, **aucune vérifiée**. Ce lot en ouvre les
premières : les **28 phrases de `basis`**, le plus gros porteur, rendu en
infobulle sur trois écrans.

**Aucun code, aucun gardien, aucun test.**

## Le banc : la phrase annonce-t-elle le chiffre que le code calcule ?

`confidence()` de `skyler_core` appelée sur des paquets fabriqués, chaque
`basis` confronté à la valeur que le même appel produit.

```text
entrée              phrase rendue                                          valeur   accord
dq_pts = 0          bloc data_quality 0/4 du score                            0.0    OUI
dq_pts = 1          bloc data_quality 1/4 du score                           0.25    OUI
dq_pts = 2          bloc data_quality 2/4 du score                            0.5    OUI
dq_pts = 3          bloc data_quality 3/4 du score                           0.75    OUI
dq_pts = 4          bloc data_quality 4/4 du score                            1.0    OUI

n_contra = 0        0 contradiction(s) tracée(s) — −0,20 chacune              1.0    OUI
n_contra = 1        1 contradiction(s) …                                      0.8    OUI
n_contra = 2        2 contradiction(s) …                                      0.6    OUI
n_contra = 3        3 contradiction(s) …                                      0.4    OUI
n_contra = 4        4 contradiction(s) …                                      0.2    OUI
n_contra = 5        5 contradiction(s) …                                      0.0    OUI
n_contra = 6        6 contradiction(s) — −0,20 chacune                        0.0    NON  ← coût marginal 0,00

n_insuf = 0         0 bloc(s) insuffisant(s) sur 8 …                          1.0    OUI
n_insuf = 2         2 bloc(s) insuffisant(s) sur 8 …                         0.75    OUI
n_insuf = 4         4 bloc(s) insuffisant(s) sur 8 …                          0.5    OUI
n_insuf = 8         8 bloc(s) insuffisant(s) sur 8 …                          0.0    OUI

                                                    accord phrase/valeur : 15 / 16
```

**Témoin positif intégré** : les valeurs varient à chaque marche (0 → 0,25 → 0,5
→ 0,75 → 1,0), donc le banc et le moteur réagissent bien.

### Les dénominateurs annoncés sont exacts

- **« sur 8 »** : `block(...)` est appelé sous **8 noms distincts** —
  `asymmetry_scenarios`, `catalysts`, `data_quality`, `fundamentals_quality`,
  `institutions_flow_anomalies`, `market_regime_sector`, `options_quality`,
  `technical_timing`. **Exact.**
- **« /4 »** : le maximum vient du profil (`prof.raw['skyler_score']['blocks']`),
  et `vertex/strategy/profiles/vertex_strategy_v2.json` donne
  `"data_quality": 4`. **Exact pour le profil servi.** Le `4` est **écrit en dur**
  dans la phrase et dans le calcul (`dq_pts / 4.0`) alors que le bloc lui-même lit
  `cfg.get('data_quality', 4)` vingt lignes plus bas — **latence**, pas défaut :
  aujourd'hui les deux coïncident.

## Le seizième cas, et pourquoi je ne le publie pas comme un défaut

À `n_contra = 6`, la valeur est écrasée par `max(0.0, …)` : la sixième
contradiction coûte **0,00**, pas 0,20. La phrase « −0,20 chacune » serait alors
fausse.

**J'ai failli le publier.** Le producteur, `skyler_core.py:197`, est une
**boucle** :

```python
for c in ((market or {}).get('conflicts') or []):
    contradictions.append({'kind': 'sources_conflict', …})
```

Une boucle : donc un nombre non borné, donc l'état est atteignable. **Faux.** En
remontant au producteur des conflits, `market_context.py:107-114` :

```python
conflicts = []
if vix_a is not None and vix_b is not None and abs(vix_a - vix_b) > 1.0:
    conflicts.append({'dimension': 'vix', …})
```

**Un seul `if`, une seule dimension.** La liste contient **au plus un** élément.
Total maximal de contradictions : `verdict_vs_regime` + `verdict_vs_extreme` +
`sources_conflict` + `skyler_vs_canonical` = **4**. L'écrêtage à 5 **n'est jamais
atteint**.

*Une boucle n'est pas une preuve de multiplicité — il faut remonter à ce qu'elle
parcourt.* **Dix-neuvième résultat faux arrêté avant publication.**

## `knowledge_graph` : deux phrases pour deux méthodes, et le repli est étiqueté

```python
method = 'residual_vs_SPY' if residual_mode else 'raw'
'basis': ('corrélation des résidus de marché %s/%s = %.2f sur %d points (seuil %.2f)
           — régression sur SPY, part expliquée retirée' …) if residual_mode else
         ('corrélation brute (méthode raw) des rendements log %s/%s = %.2f sur %d points
           (seuil %.2f) — SPY absent, marché non contrôlé' …)
```

Trois choses vérifiées :

- **La méthode est nommée dans la phrase ET dans un champ** (`method`) : le repli
  ne se déguise pas en mesure contrôlée. C'est exactement ce qui manquait au
  dossier **422** (repli muet de l'expected-move).
- **Le nombre de points est `L - 1`**, ce qui est le compte exact de rendements
  log tirés de `L` clôtures. Pas d'inflation du `n`.
- **Le seuil est affiché** (`CORR_STRONG`), donc la sélection est lisible.

Les trois autres `basis` du même fichier nomment leur provenance sans
l'embellir : « déclaré dans le secteur %s **par la watchlist du code** » (avec
`source: 'vertex/market/sectors.py (watchlist statique)'`), « **date déclarée** du
calendrier », « **position réelle déclarée** sur %s ». Chaque arête porte un
`evidence_level` (F1/F2), et le fichier ajoute de lui-même :
« aucune source fournisseurs/clients/concurrents branchée — relations jamais
inventées ».

## Classement

**Aucun défaut.** Et c'est le résultat.

Sur les six phrases ouvertes — quatre de `skyler_core`, deux de
`knowledge_graph` — **six sont exactes**. Les chiffres annoncés sont ceux que le
code calcule ; les dénominateurs sont les vrais ; les replis sont étiquetés ; les
provenances sont nommées.

C'est la **première famille d'affirmations que la boucle mesure et trouve
saine**. Elle contraste avec ce que les lots 427 à 443 ont trouvé côté interface
— une légende sur liste fixe, un entonnoir plat par construction, un R:R
tautologique, une carte toujours fraîche. **Les phrases écrites par les moteurs
tiennent mieux que les phrases écrites dans les pages.**

Un seul point à surveiller, **rang 4** : le `4` en dur du dénominateur
`data_quality`, dans la phrase **et** dans le calcul, alors que le bloc lui-même
lit la valeur du profil. Aucun écart aujourd'hui ; un changement de profil en
créerait un, silencieusement, **des deux côtés à la fois**.

## Portée

**Six phrases sur 28 ouvertes.** Les 22 autres — 16 de `decision_memory`, une de
`red_team`, le reste de `skyler_core` et `knowledge_graph` — sont **recensées,
non vérifiées**. Et `basis` n'est qu'un champ sur les 13 qui atteignent un écran :
**104 des 110 phrases concluantes du 444 restent fermées**.

Le banc appelle le **moteur réel** sur des paquets **fabriqués** : il établit que
la phrase et le calcul s'accordent **pour toute entrée que j'ai pu produire**, pas
que ces entrées reflètent l'usage réel.

Je n'ai **pas** vérifié que `_pearson` calcule bien une corrélation de Pearson ni
que `_residual_vs_market` régresse correctement : j'ai vérifié que **la phrase dit
ce que le code fait**, pas que le code fait ce qu'il faut. Ce sont deux questions
différentes, et je n'ouvre que la première.

**Aucun navigateur ouvert** — les infobulles ne sont pas observées au survol.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `confidence()` appelée en mémoire, sans écriture ; aucun
  appel réseau.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quarante-huitième lot court. Séquence : **442 ✓ · 443 ✓ · 444 ✗ (correction) ·
445 ✗ (bornage sain)**.

Deux lots de suite sans défaut de produit. Celui-ci ne trouve rien **parce qu'il
n'y a rien à trouver là** — et c'est une information : la classe la plus neuve du
recensement, celle qui porte des chiffres écrits par le serveur, résiste à
l'ouverture. Le vivier reste ouvert à 104 phrases ; ce lot dit seulement que les
six premières tiennent.

Les deux comptes restent séparés : résultats faux **arrêtés avant publication**
**19** ; **publiés puis corrigés** **1**.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
