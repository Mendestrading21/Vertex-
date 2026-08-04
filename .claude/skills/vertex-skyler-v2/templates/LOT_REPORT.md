# SKYLER V2 — LOT XX — TITRE

> Date : YYYY-MM-DD  
> Branche : `agent/skyler-v2-lot-XX-description`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `...`  
> SHA après : `...`  
> PR : `...`

## 1. Constat

Décrire l’état observé avant modification avec fichiers, lignes, sorties, captures ou données reproductibles.

## 2. Problème

Décrire précisément :

- comportement incorrect ou manque ;
- impact utilisateur/financier/technique ;
- sévérité ;
- conditions de reproduction ;
- pourquoi l’existant est insuffisant.

## 3. Périmètre

### Inclus

- ...

### Hors périmètre

- ...

## 4. Décision

Décrire la solution retenue, les alternatives rejetées et la raison.

## 5. Implémentation

### Fichiers modifiés

| Fichier | Rôle | Modification | Risque |
|---|---|---|---|
| `...` | ... | ... | faible/moyen/élevé |

### Contrats et unités

- sources :
- unités :
- périodes :
- fraîcheur :
- conventions :
- versions de schéma/moteur/profil :

### Compatibilité

- API :
- données :
- UI :
- mode démo :
- sans IBKR :
- migration/rollback :

## 6. Tests rouges avant correction

```text
commande
résultat exact
```

Décrire pourquoi le test prouve le défaut.

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex
résultat : ...

python -m pytest tests/ -q
résultat : ...

python -m pytest tests/test_no_orders.py -q
résultat : ...
```

Ajouter les tests ciblés et résultats exacts.

## 8. Validation manuelle et navigateur

| Vue/mode | Taille | Résultat | Capture |
|---|---:|---|---|
| ... | 390×844 | ... | ... |
| ... | 768×1024 | ... | ... |
| ... | 1440×900 | ... | ... |
| ... | 1920×1080 | ... | ... |

- console :
- réseau :
- `/healthz` :
- `/api/client-log` :
- clavier/focus :
- reduced-motion :
- overflow :

## 9. Invariants vérifiés

- [ ] READONLY ;
- [ ] aucun ordre ;
- [ ] aucune donnée inventée ;
- [ ] unités explicites ;
- [ ] fraîcheur réelle ;
- [ ] démo/sans IBKR ;
- [ ] stale/missing/insufficient/offline ;
- [ ] sécurité/XSS/secrets ;
- [ ] tests complets ;
- [ ] responsive/accessibilité si applicable.

## 10. Comparaison avant/après

| Mesure | Avant | Après | Interprétation |
|---|---:|---:|---|
| ... | ... | ... | ... |

## 11. Risques et limites restantes

1. ...
2. ...

Aucune limite ne doit être masquée.

## 12. Rollback

Procédure exacte et données éventuellement affectées.

## 13. Verdict

`GO` / `GO AVEC RÉSERVES` / `NO-GO`

Justification : ...

## 14. Prochaine étape autorisée

Une seule étape : ...

**Arrêt après ce lot — validation humaine requise.**
