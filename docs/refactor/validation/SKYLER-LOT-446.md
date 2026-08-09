# SKYLER LOT 446 — « Clôture séance +5 » compte les séances OBSERVÉES, pas les séances de marché : le contraste moteurs/pages du 445 est nuancé, pas confirmé

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-446` (base : lot 445 fusionné,
b28b3be)

Vingt-huitième lot de la veine, **bornage du 445**. Le 445 avait trouvé six
phrases de moteur **toutes exactes** et en avait tiré un contraste : *les phrases
écrites par les moteurs tiennent mieux que celles écrites dans les pages*.
Question de ce lot : **est-ce vrai, ou mon échantillon était-il favorable ?**

Troisième producteur, indépendant des deux premiers : **`decision_memory`**,
16 phrases de `basis`, jamais ouvertes.

**Aucun code, aucun gardien, aucun test.**

## Le banc, avec son témoin positif

`measure(record, closes_after)` est une fonction pure. Le log de séances est
construit par `session_log.record_close()`, **le vrai producteur**, sur dix
séances de marché.

```text
terminal ouvert TOUS les jours
   séances enregistrées : 10 → [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
   phrase rendue        : « clôture séance +5 vs prix à la décision »   valeur 5.0 %
   5ᵉ séance de MARCHÉ  : 105 → 5.0 %
   ACCORD : OUI                                    ← témoin positif

4 jours sans scan
   séances enregistrées :  6 → [101, 103, 105, 106, 108, 110]
   phrase rendue        : « clôture séance +5 vs prix à la décision »   valeur 8.0 %
   5ᵉ séance de MARCHÉ  : 105 → 5.0 %
   ACCORD : NON — la phrase dit « séance +5 », le code mesure la 5ᵉ séance OBSERVÉE
```

**8,0 % annoncé comme le rendement à +5 séances, quand le rendement réel à
+5 séances est 5,0 %.**

## Ce n'est pas un cas de bord : le module le documente lui-même

`session_log.py`, en tête de fichier :

> « aucun jour sans scan n'est comblé : **un trou dans le log reste un trou** »

Le log n'enregistre une clôture **que les jours où un scan tourne**
(`analysis_api.py:199`). Un terminal fermé trois jours laisse trois trous, et
`closes_after_date()` rend une liste **compactée** : l'indice 5 n'est plus la
cinquième séance de marché.

Ce n'est pas non plus une conséquence de données sales — `record_close()` refuse
les entrées invalides, `series.closes()` filtre les valeurs non finies. **Le trou
vient de l'usage, pas de la donnée.**

## Deux conventions dans la même fonction, et une seule est honnête

```python
# branche EN_ATTENTE
basis='%d/%d séance(s) postérieure(s) observée(s)' % (n, sessions)     ← dit « observée(s) »

# branche MESURE
basis='clôture séance +%d vs prix à la décision' % sessions            ← ne le dit pas
```

La première nomme exactement ce qu'elle compte. La seconde, **dix lignes plus
bas**, emploie un vocabulaire de séances de marché pour un compte de séances
observées. C'est la famille du **426** (deux conventions pour un même champ),
appliquée aux **deux branches d'une seule fonction** — et, comme au 434 et au
439, **le contre-exemple est dans la même fonction**.

## Mais la conséquence n'atteint aucun écran — vérifié

```text
lecture de champ (.champ / ['champ']) dans les octets servis
horizons             0 écran
H5 / H20 / H60       0 écran
sessions_observed    0 écran
mfe_pct / mae_pct    0 écran
return_pct           2 écrans … mais PAS celui-ci
```

**Quatrième occurrence du piège « un nom, plusieurs payloads »** — et cette
fois arrêtée avant publication. Les deux lectures de `return_pct` sont :

- `analysis_page.py:885` → `s.return_pct` où `s` vient de `d.scenarios` : c'est la
  **cible d'un scénario**, pas un horizon ;
- `performance_page.py:505` → `r.return_pct` où `r` vient de
  `/api/skyler/calibration` → `outcomes.rows`, avec les colonnes « Prix décision /
  Prix actuel / Rendement » : **une autre forme**, pas les horizons de `measure()`.

**Vingtième résultat faux arrêté avant publication.** Les horizons sont calculés,
sérialisés, persistés — et, sur le périmètre mesuré, **pas affichés**.

## Classement

**Rang 4.** Défaut réel dans le moteur, **sans conséquence à l'écran aujourd'hui**
— la règle que la boucle s'applique depuis le 411 et le 435.

Avec une réserve que je pose noir sur blanc : **si un jour ces horizons sont
affichés**, le défaut devient immédiatement sérieux, et il penche du côté qui
flatte — sur un titre en tendance, mesurer la 5ᵉ séance *observée* au lieu de la
5ᵉ séance *de marché* **allonge la période réelle** et gonfle le rendement
annoncé. Correction pressentie, minuscule et déjà écrite dix lignes plus haut
dans le même fichier : dire « observée » dans les deux branches.

Aucun test du dépôt ne compare la séance annoncée à la séance de marché :
**aucun gardien.**

## La réponse à la question du 445

**Nuancée, pas confirmée.**

Le 445 concluait que les phrases des moteurs sont saines, sur six phrases de deux
producteurs. Un troisième producteur en porte **une qui ne l'est pas**. Le
contraste moteurs/pages tient donc sur les **conséquences affichées** — les
défauts des pages atteignent l'écran, celui-ci non — mais **pas sur la justesse
du vocabulaire**. Mon échantillon du 445 était favorable sur cet axe, et je le
dis.

## Portée

**Une phrase ouverte sur les 16 de `decision_memory`** — les quinze autres
(`classify_error`, `detect_patterns`, `post_mortem`, `ledger_health`) sont
**recensées, non vérifiées**. Sur les 110 phrases concluantes du 444,
**103 restent fermées**.

Le banc construit le log par le **vrai producteur** (`record_close`) sur des
séances **fabriquées** : il établit le comportement du code face à un log troué,
**pas la fréquence des trous dans l'usage réel**. Je n'ai pas lu
`skyler_sessions.json` pour compter les trous existants.

Je n'ai **pas** vérifié que les autres horizons (`H20`, `H60`, `CATALYSEUR`)
souffrent du même écart : la démonstration porte sur `H5`. Le mécanisme est
partagé — c'est la même fonction `measured()` — mais je ne l'ai mesuré qu'une
fois.

**Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `measure()` et `record_close()` sont des fonctions pures
  appelées en mémoire ; aucun fichier de log lu ni écrit ; `persist` redirigé.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quarante-neuvième lot court. Séquence : **443 ✓ · 444 ✗ (correction) · 445 ✗
(famille saine) · 446 ~ (bornage qui nuance)**.

Le 445 avait établi une bonne nouvelle ; celui-ci la borne sans l'annuler. C'est
le geste que la boucle sait faire depuis le 426 : quand un lot conclut, le suivant
va chercher le cas qui ne rentre pas — et cette fois il l'a trouvé au troisième
producteur, dans une fonction dont la branche voisine dit exactement le mot juste.

Comptes séparés : résultats faux **arrêtés avant publication** **20** ; **publiés
puis corrigés** **1**.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
