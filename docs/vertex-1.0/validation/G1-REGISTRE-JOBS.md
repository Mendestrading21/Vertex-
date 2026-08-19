# G1 · #779 — Le registre de jobs déclarait 27 automatisations dont 18 n'existaient pas

Instrument : `tools/vertex_1_0/mesurer_registre_jobs.py`
Gardien : `tests/test_vertex_1_0_registre_jobs.py` (9 tests, 8 mutations passées)
Mesure figée : `docs/vertex-1.0/inventory/registre_jobs.json`

---

## Pourquoi ce lot existe

`RELEASE_GATES.md` G1 demande *« … et scheduler ont un propriétaire modulaire »*.
Le scheduler en avait déjà un : `vertex/scheduler/registry.py`, servi par
`/api/system/automations`. **C'est exactement ce qui rendait le défaut
invisible : la case était cochée.**

La question qu'il fallait poser n'était pas « qui possède le scheduler ? » mais
**« ces jobs existent-ils ? »**.

## La mesure

Le registre ne reçoit d'information que par `registry.beat('NOM')`. Un nom
déclaré qu'aucun `beat` ne porte ne peut pas tourner — jamais. L'instrument
énumère à l'AST tous les appels `.beat(` du monolithe et du paquet `vertex`
(les tests sont exclus : un `beat` de test ne fait pas tourner un job).

```text
avant : 27 déclarés ·  7 émetteurs · 20 sans exécutant
après : 27 déclarés ·  9 émetteurs · 18 marqués `implemente: False`
```

Témoins (l'outil sort en 2 s'ils ne mordent pas) : un nom fabriqué qu'aucun
`beat` n'émet doit ressortir `SANS_EMETTEUR` ; au moins un job réel doit
ressortir `ACTIF`. Mutation vérifiée : neutraliser la détection AST
(`n.func.attr == 'beat'` → un autre nom) fait bien sortir l'outil en 2.

## Ce que l'écran disait

Trois affirmations fausses, toutes servies ensemble sur la vue
Système › Automatisations :

1. **« jamais exécuté »** pour les 27 lignes sans `last_run` — le même mot pour
   un job en panne et pour un job qu'aucun code n'exécute. Deux causes
   opposées, une seule étiquette.
2. **« les jobs "jamais exécuté" dépendent d'intégrations absentes dans cet
   environnement »** — un *diagnostic*, en pied de page, faux pour 18 lignes
   sur 27 : elles ne dépendent de rien, elles n'ont pas d'exécutant.
   `NEWS_REFRESH`, lui, tournait toutes les 60 s depuis toujours et se
   déclarait à 900 s : sa boucle n'émettait simplement aucun battement.
3. **« sur événement »** dans la colonne « Prochaine (est.) » — une *promesse*
   de déclenchement pour sept jobs que rien ne déclenchera jamais.

Plus une quatrième, dans le panneau Démarrage : **« scheduler READY · 27 jobs
enregistrés »** — un inventaire flatteur présenté comme un état de santé.

C'est la règle 4 de `CLAUDE.md` (donnée absente → aveu honnête, jamais une
valeur inventée) appliquée à un **état** plutôt qu'à un chiffre.

### Les deux dernières n'ont pas été trouvées par l'API

`/api/system/automations` sert un JSON qui ne contient ni la colonne
« Prochaine » ni le bilan du panneau Démarrage. Le statut corrigé et l'API
vérifiée, **la capture d'écran montrait encore « sur événement » sur sept
lignes** et « 27 jobs enregistrés » en dessous. La même invention, deux
surfaces plus loin. Un test d'API vert ne dit rien de ce que la page affirme.

## Ce qui a été fait

| Correction | Fichier |
| --- | --- |
| 4ᵉ colonne `implemente` au registre canonique, `NON_IMPLEMENTES` exporté | `vertex/scheduler/registry.py` |
| `etat` servi : `NON_IMPLEMENTE` / `EN_ATTENTE` / `ACTIF` / `ERREUR` | `vertex/scheduler/registry.py` |
| `NEWS_REFRESH` émet enfin (boucle de nouvelles), cadence 900 → **60 s** réels | `terminal.py` |
| `POSITION_REFRESH` émet enfin (`/api/pos-quotes`), cadence 45 s → **None** (à la demande) | `vertex/app/routes/desk.py` |
| L'écran distingue les quatre états ; pied de page réécrit | `vertex/ui/pages/system_page.py` |
| Colonne « Prochaine » : `—` pour un job sans exécutant | `vertex/ui/pages/system_page.py` |
| Bilan : « 9 jobs exécutables … · 18 déclarés sans exécutant » | `vertex/services/connections.py` |
| Bump du cache de shell `td-shell-v206 → v207` (octets servis modifiés) | `vertex/app/routes/system.py` |

Un `try/except Exception: pass` a été **retiré** au passage plutôt qu'ajouté :
l'import du registre est remonté en tête de `desk.py`, où un import cassé
éclate au démarrage au lieu de se taire à chaque sauvegarde. Le gardien
`tests/test_pass_et_contexte_lot379.py` avait détecté les deux nouveaux
avaleurs silencieux — sa borne n'a **pas** été relevée.

## Le drapeau est confronté à la mesure, dans les deux sens

`implemente` n'aurait aucune valeur s'il n'était qu'une annotation : il
dériverait au premier ajout. Le test central le compare à ce que l'AST trouve
**dans les deux directions** :

- marquer un job implémenté sans émetteur → échec (l'écran l'afficherait
  « en attente » pour toujours, ce qui se lit comme une panne) ;
- poser un émetteur sans lever le drapeau → échec (l'écran nierait un travail
  qui a bien lieu).

## Preuves

```text
compileall                      exit 0
pytest tests/ -q                3284 passed          (3275 avant le lot)
mutations du gardien            8/8 mordent          (M1..M8, contrôle vert)
```

Navigateur 1440 px, `DEMO=1 NO_IBKR=1`, service workers bloqués :

```text
/system?view=automations   27 lignes rendues
libellés                   OK 5 · « non implémenté » 18 · « en attente » 4
lignes non implémentées promettant un déclenchement   0
débordement horizontal     non
erreurs console            0
/api/system/connections    Scheduler READY | 9 jobs exécutables, 5 avec au
                           moins une exécution · 18 déclarés sans exécutant.
```

Effet vérifié par l'usage, pas par la chaîne : un POST sur `/api/pos-quotes`
fait passer `POSITION_REFRESH` de `EN_ATTENTE` à `ACTIF` avec `runs=1`.

## Ce que ce lot ne fait pas

Il **n'implémente pas** les 18 jobs déclarés sans exécutant, et ne les supprime
pas non plus. Les supprimer effacerait une intention produit (brief pré-marché,
audit d'intégrité des positions, moteur de suivi) ; les implémenter serait du
code métier nouveau, hors du périmètre de G1. Ils sont désormais **nommés pour
ce qu'ils sont** — et le jour où l'un d'eux reçoit un exécutant, le gardien
exige que le drapeau suive.

G1 reste **non franchi** : `Flask(__name__)` et les hooks de latence vivent
encore dans `terminal.py`. Ce lot ferme la quatrième des quatre responsabilités
citées par G1 (factory · routes · lifecycle/workers · **scheduler**), après le
registre de routes (`vertex/app/factory.py`) et la garde de double démarrage
(`vertex/app/lifecycle.py`).
