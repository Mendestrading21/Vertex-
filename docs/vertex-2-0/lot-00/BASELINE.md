# Baseline Vertex 2.0 — lot 0

Mesurée le 28 août 2026 sur `agent/vertex-2-0-integration-20260828` @ `cb33d90`,
en `DEMO=1 NO_IBKR=1`. **Rien n'est déduit d'un nom de fichier, d'une doc ou
d'un drapeau de configuration : tout ce qui suit est mesuré au runtime.**

Artefacts reproductibles dans ce dossier :
`inventaire-depot.json`, `audit-runtime.json`, `frontiere-ibkr.txt`,
`surface-claude.txt`, `captures-avant/`.

---

## 1. Ce que la consolidation a changé, mesuré

`audit_runtime.py` compare la branche fusionnée à la baseline que PR #838
décrit — laquelle est celle de `main`.

| Élément | Baseline #838 (`main`) | Mesuré ici | |
|---|---|---|---|
| Navigation principale | 7 entrées | **12 entrées** | ✅ |
| `/calendar` | redirige vers Opportunités | **200** | ✅ |
| `/markets` | redirige vers le Dashboard | **200** | ✅ |
| `/simulator` | **404** | **200** | ✅ |
| `/follow-up` | **404** | **200** | ✅ |
| `/performance` | redirige vers Journal | **200** | ✅ |
| Collision `GET /options/<sym>` | le JSON gagne sur la page | **résolue** | ✅ |
| Règles / endpoints / blueprints | 204 / 199 / 29 | **206 / 199 / 29** | |
| Feuilles CSS sur la coque | 18 | **19** | |
| Scripts sur la coque | 17 | **17** | |
| Routeur persistant du shell | non chargé | **non chargé** | ❌ |
| Polices | General Sans / JetBrains Mono | **Geist / Geist Mono** | ✅ |

**Aucune redirection ni 404 n'est comptée comme une page livrée** : les douze
routes cibles rendent 200 et une page HTML, vérifié au navigateur avec captures.

## 2. Matrice vérité → cible des douze pages

| Page | Route | HTTP | Payload | Latence médiane | Transition déclarée |
|---|---|---:|---:|---:|---|
| Aujourd'hui | `/` | 200 | 147,3 ko | 2 ms | `conserver_renommer` |
| Calendrier | `/calendar` | 200 | 27,3 ko | 2 ms | `extraire` |
| Marchés | `/markets` | 200 | 75,1 ko | 2 ms | `restaurer` |
| Opportunités | `/opportunities` | 200 | 123,9 ko | 2 ms | `conserver` |
| Analyse | `/analysis` | 200 | 25,1 ko | 2 ms | `conserver` |
| Options | `/options` | 200 | 25,5 ko | 2 ms | `conserver` |
| Simulateur | `/simulator` | 200 | 28,9 ko | 2 ms | `creer_apres_moteur` |
| Portefeuille | `/portfolio` | 200 | 131,1 ko | 2 ms | `conserver` |
| Suivi | `/follow-up` | 200 | 25,2 ko | 2 ms | `migrer_tracking` |
| Performance | `/performance` | 200 | 78,1 ko | 2 ms | `separer_du_journal` |
| Vertex IA | `/intelligence` | 200 | 70,5 ko | 2 ms | `promouvoir` |
| Système | `/system` | 200 | 103,1 ko | 2 ms | `conserver` |

**Lecture honnête de la latence :** 2 ms est le temps de rendu du **HTML** en
mode démo, sans worker ni fournisseur. Ce n'est **pas** un temps de page perçu :
les données arrivent ensuite par `fetch`. Une mesure de latence perçue exige un
poste connecté — hors de portée ici, et déclarée telle.

## 3. Inventaire du dépôt

| Élément | Nombre |
|---|---:|
| Fichiers suivis | 3 356 |
| Fichiers Python | 907 |
| Fichiers de test | 475 · **4 011 fonctions de test** |
| Décorateurs de route (approx.) | 175 |
| `except Exception` (approx.) | 382 dont **174 silencieux** |
| Moteurs (`vertex/engines/`) | 60 modules |
| Sources de données (`vertex/data_sources/`) | 33 modules |
| Feuilles CSS | 20 (19 servies, 1 non servie) |
| Scripts JS | 49 |
| Documents Markdown | 1 022 |

Les **174 `except` silencieux** sont un chiffre de baseline, pas un verdict :
cette refonte a déjà montré deux fois qu'une garde défensive transforme un bug
en silence d'apparence honnête (la carte Alertes d'Aujourd'hui, le helper de
notification du Simulateur). → à instruire au lot d'observabilité.

## 4. Autorité Claude

`audit_claude_surface.py` : **1 skill Vertex, 6 auditeurs, références résolues,
audit 001–150 continu.** Le skill maître de #838 est l'unique autorité ; mes
ajouts aux références ont été abandonnés au profit des siens, sans mélange.

## 5. Ce qui reste ouvert — aucun n'est masqué

### Collision de route restante

`GET /api/anomalies/<sym>` a **deux propriétaires** :
`analysis_api.api_anomalies` et `strategy_os.anomalies_for`. → lot 9.

### Routeur persistant du shell

Documenté et testé, **toujours pas chargé**. → lot d'architecture.

### Dette de confidentialité IBKR — 13 appels sensibles

```
terminal.py                            accountSummary, positions ×2, managedAccounts
vertex/data_sources/ibkr_compte.py     accountSummary, portfolio ×2, reqPnL, managedAccounts ×2
vertex/data_sources/ibkr_positions.py  positions
vertex/data_sources/ibkr_replay.py     positions
tools/vertex_1_0/mesurer_g5_live.py    positions
```

**Dette P0 du lot 2, jamais une capacité autorisée.** À classifier puis
supprimer derrière un `MarketDataGateway`. Le mode `--enforce` du scanner
devient obligatoire à la fin de ce lot.

## 6. Captures avant

12 pages × 3 largeurs — **1600 / 1024 / 390** — dans `captures-avant/`,
avec `rapport.json`.

```
0 erreur console        12 pages × 3 largeurs
0 débordement horizontal 12 pages × 3 largeurs
```

C'est l'état **avant** les lots de convergence, pas un certificat : le mode
démo sert des collections vides, et cette refonte a déjà montré que des pans
entiers de code ne s'exécutent que sur une page peuplée.

## 7. Tests

```
python -m compileall -q terminal.py vertex     OK
python -m pytest -q                            4 310 passés · 154 ignorés
                                               1 échec environnemental
```

L'échec est `test_la_classification_est_discriminante` : il exige plus de 100
références git, ce clone en porte 4. Relevé **avant** toute modification. Il
passe sur la CI, qui dispose du dépôt complet.

## 8. Ce que le lot 0 ne dit pas

- **Aucune donnée de marché réelle.** L'egress vers les fournisseurs est
  bloqué : les modes `live` et `delayed` ne sont pas observables, et aucun
  graphique ne trace de série réelle.
- **Aucune mesure de latence perçue.** Voir §2.
- **Aucun jugement de composition.** La conformité de chaque page au blueprint
  du skill relève des `PAGE_CONTRACT`, pas de cette baseline.
