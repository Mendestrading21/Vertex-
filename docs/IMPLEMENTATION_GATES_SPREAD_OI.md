# Vertex — implémentation exacte de `SPREAD_EXCESSIVE` et `OI_INSUFFICIENT`

## Emplacements de code

| Responsabilité | Fichier | Fonction ou bloc |
|---|---|---|
| Seuils par défaut `SWING_3_6M` | `vertex/options/horizon_scanners.py` | `_FALLBACK_SWING_3_6M` |
| Contrôle d’un maximum | `vertex/options/horizon_scanners.py` | `_maximum_ok()` |
| Contrôle d’un minimum | `vertex/options/horizon_scanners.py` | `_minimum_ok()` |
| Qualification de mandat | `vertex/options/horizon_scanners.py` | `_swing_3_6m_mandate()` |
| Choix du contrat évalué | `vertex/options/horizon_scanners.py` | `scan()` puis `options_context()` |
| Gate de décision | `vertex/engines/skyler_core.py` | `hard_gates()` |
| Plafonnement du verdict | `vertex/engines/skyler_core.py` | `_decision_label()` |

## 1. Entrée contractuelle attendue

Le board options fournit un dictionnaire par contrat. Les deux gates n’inventent ni bid/ask ni open interest : elles lisent uniquement `spread_pct` et `oi` déjà présents dans ce dictionnaire.

```python
raw_contract = {
    "sym": "XYZ",
    "type": "CALL",
    "exp": "2026-09-18",
    "dte": 135,
    "delta": 0.42,
    "oi": 650,
    "volume": 87,
    "spread_pct": 3.5,
    "quote_age_seconds": 120,
}
```

Pour le mandat `SWING_3_6M`, les fallback déclarés sont les suivants :

```python
_FALLBACK_SWING_3_6M = {
    "preferred_dte": [90, 180],
    "target_dte": 135,
    "holding_plan_sessions": [5, 10, 15],
    "delta_abs_min": 0.30,
    "delta_abs_max": 0.60,
    "open_interest_min": 500,
    "volume_min": 50,
    "spread_pct_max": 8.0,
    "max_quote_age_seconds": 900,
}
```

Si le profil V3 fournit `options_profile.swing_3_6m`, ses valeurs remplacent ces fallbacks. Le code ne disperse donc pas le seuil de 500 OI ou 8,0 % de spread dans le moteur de décision.

## 2. Qualification du contrat au scanner

### Fonctions atomiques

Le scanner retourne trois états possibles : `True`, `False` ou `None`. `None` désigne une donnée absente, invalide ou non convertible — jamais une conformité présumée.

```python
def _minimum_ok(value, minimum):
    if value is None:
        return None
    try:
        return bool(float(value) >= float(minimum))
    except (TypeError, ValueError):
        return None


def _maximum_ok(value, maximum):
    if value is None:
        return None
    try:
        return bool(float(value) <= float(maximum))
    except (TypeError, ValueError):
        return None
```

### Mandat `SWING_3_6M`

`_swing_3_6m_mandate()` produit le dictionnaire source des deux gates :

```python
def _swing_3_6m_mandate(contract, config):
    age = _quote_age(contract)
    return {
        "delta_ok": _value_in_range(
            contract.get("delta"),
            config["delta_abs_min"],
            config["delta_abs_max"],
        ),
        "oi_ok": _minimum_ok(
            contract.get("oi"),
            config["open_interest_min"],
        ),
        "volume_ok": _minimum_ok(
            contract.get("volume"),
            config["volume_min"],
        ),
        "spread_ok": _maximum_ok(
            contract.get("spread_pct"),
            config["spread_pct_max"],
        ),
        "quote_fresh_ok": _maximum_ok(
            age,
            config["max_quote_age_seconds"],
        ),
        "bounds": {
            "oi_min": config["open_interest_min"],
            "spread_pct_max": config["spread_pct_max"],
            "holding_plan_sessions": list(config["holding_plan_sessions"]),
        },
    }
```

La règle de statut est ensuite uniforme :

```python
def _mandate_status(mandate):
    checks = [value for key, value in mandate.items() if key.endswith("_ok")]
    if any(value is False for value in checks):
        return "OUT_OF_MANDATE"
    if any(value is None for value in checks):
        return "PARTIAL_MANDATE"
    return "IN_MANDATE"
```

| Valeur de `spread_ok` ou `oi_ok` | Effet sur le statut du contrat | Effet ultérieur sur la gate correspondante |
|---|---|---|
| `True` | Conformité possible, si les autres contrôles sont aussi vrais | `triggered=False` |
| `False` | `OUT_OF_MANDATE` | `triggered=True` |
| `None` | `PARTIAL_MANDATE`, si aucun autre contrôle n’est faux | `triggered=None` |

Un contrat hors DTE n’entre pas dans le scanner `SWING_3_6M`. Parmi les contrats admissibles, le tri privilégie d’abord `IN_MANDATE`, puis `PARTIAL_MANDATE`, enfin `OUT_OF_MANDATE`. Le premier contrat devient `options_context.best` : ce choix unique empêche les gates de lire un contrat différent de celui exposé par le contexte Skyler.

## 3. Code exact des gates Skyler

Dans `hard_gates(packet, score)`, les deux gates partagent le même contexte :

```python
elif gid in ("SPREAD_EXCESSIVE", "OI_INSUFFICIENT", "DTE_OUT_OF_MANDATE"):
    octx = packet["contexts"]["options"] or {}
    best = octx.get("best") or {}
    mandate = best.get("mandate") or {}
    if not octx.get("available") or not best:
        gate(gid, None, "candidat options non fourni — gate non évaluable")
        continue
```

Ce préambule est essentiel. En l’absence de `OptionsContext` ou de candidat sélectionné, le résultat est `None` et non `False`. Autrement dit, Vertex ne dit pas « spread conforme » ou « OI suffisant » lorsqu’il ne dispose pas du contrat à vérifier.

### `SPREAD_EXCESSIVE`

```python
if gid == "SPREAD_EXCESSIVE":
    ok = mandate.get("spread_ok")
    gate(
        gid,
        None if ok is None else not bool(ok),
        (
            "spread non fourni — jamais supposé conforme"
            if ok is None
            else "spread %.2f %% %s le mandat" % (
                best.get("spread_pct") or 0,
                "respecte" if ok else "dépasse",
            )
        ),
    )
```

Le booléen est inversé volontairement : `spread_ok=True` devient `triggered=False`, alors que `spread_ok=False` devient `triggered=True`. Une donnée de spread absente laisse `ok=None`, donc `triggered=None`.

Pour le fallback `SWING_3_6M` à 8,0 %, le comportement est :

| `spread_pct` | `spread_ok` | Sortie `SPREAD_EXCESSIVE` |
|---:|---|---|
| `3.50` | `True` | `triggered=False` |
| `8.00` | `True` | `triggered=False` car la borne est inclusive |
| `8.01` | `False` | `triggered=True` |
| `None`, texte invalide ou objet invalide | `None` | `triggered=None` |

### `OI_INSUFFICIENT`

```python
elif gid == "OI_INSUFFICIENT":
    ok = mandate.get("oi_ok")
    gate(
        gid,
        None if ok is None else not bool(ok),
        (
            "open interest non fourni — jamais supposé conforme"
            if ok is None
            else "open interest %s %s le mandat" % (
                best.get("oi"),
                "respecte" if ok else "ne respecte pas",
            )
        ),
    )
```

Le comportement est symétrique, mais le seuil est un minimum. Avec le fallback `open_interest_min=500` :

| `oi` | `oi_ok` | Sortie `OI_INSUFFICIENT` |
|---:|---|---|
| `650` | `True` | `triggered=False` |
| `500` | `True` | `triggered=False` car le minimum est inclusif |
| `499` | `False` | `triggered=True` |
| `None`, texte invalide ou objet invalide | `None` | `triggered=None` |

## 4. Effet exact sur le verdict

Les gates sont évaluées dans l’ordre du profil. La liste `triggered` ne conserve que les gates dont `triggered is True`; les états `None` sont exposés dans `unknowns`, mais ne deviennent pas silencieusement des gates déclenchées.

```python
def _decision_label(packet, score, gates, detail):
    triggered = [g for g in gates if g["triggered"] is True]
    if triggered:
        return (
            "REFUSER" if score["total"] < 24 else "ATTENDRE",
            triggered[0],
            False,
        )
    if score["total"] >= 28:
        decision = "ACHETER"
    elif score["total"] >= 24:
        decision = "ATTENDRE"
    else:
        decision = "REFUSER"
    return decision, None, False
```

Donc un spread supérieur à la limite ou un OI sous le minimum ne produit pas d’exception et ne supprime pas le contrat de l’audit. Il est visible, la gate est `True`, et un score autrement fort est **plafonné à `ATTENDRE`**. Si le score est inférieur à 24/40, le verdict devient `REFUSER`.

## 5. Limites intentionnelles

Ces deux gates contrôlent le contrat sélectionné, pas l’intégralité de la chaîne. Elles ne remplacent pas les contrôles `volume_ok`, `quote_fresh_ok` et `delta_ok`, qui alimentent aujourd’hui le statut de mandat et le score `options_quality`, sans gates autonomes. Elles ne vérifient pas non plus le P&L d’options, le slippage réellement exécuté ou la profondeur de carnet : ces données ne sont pas encore stockées dans le ledger.

La garantie de sécurité essentielle est donc la suivante : **les données absentes deviennent explicites (`None`, `PARTIAL_MANDATE`, `unknowns`) ; elles ne deviennent jamais `False` au sens de « gate sûre » ni `True` au sens de « conformité prouvée ».**

## Références de code

La version correspondante est incluse dans la demande de fusion active. Les fichiers de référence sont `vertex/options/horizon_scanners.py` et `vertex/engines/skyler_core.py`.
