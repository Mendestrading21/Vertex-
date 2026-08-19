# G1 · #779 — La fabrique Flask quitte le monolithe (dernière des quatre)

Module : `vertex/app/factory.py::create_app`
Gardien : `tests/test_vertex_1_0_factory_parity.py` (10 tests, 7 mutations)
Gardien de sécurité retargeté : `tests/test_safe_api_errors_lot648.py`

---

## Ce qui a bougé

Sept blocs de plomberie Flask vivaient dans `terminal.py`, dispersés entre les
lignes 88 et 1865 : `Flask(__name__)`, la configuration de session, le
fournisseur JSON sûr, la mesure de latence, le verrou d'accès, les en-têtes de
sécurité, les pages d'erreur 404/500 et la compression gzip.

**Aucun ne dépendait de l'état du monolithe** — c'est ce qui a rendu le
déplacement possible, et c'est ce qui a été mesuré avant de le tenter.

```text
lignes de terminal.py     7 245 → 7 174
règles d'URL servies      194   → 194   (diff exact : aucune)
blueprints du monolithe   7     → 6     (`auth` n'en était pas un)
```

## Le piège, mesuré avant d'écrire une ligne

`terminal.py` faisait `Flask(__name__)` **depuis la racine du dépôt** :

```text
root_path     = /…/Vertex-
static_folder = /…/Vertex-/static
```

Ce dossier contient deux fichiers, et les deux sont **réellement référencés par
les pages servies** : `chart.umd.min.js` et `icon-180.png`.

Écrire `Flask(__name__)` dans `vertex/app/factory.py` aurait fait dériver
`root_path` vers `vertex/app/`, donc `static_folder` vers un chemin qui n'existe
pas. Les deux fichiers seraient partis en **404 sans la moindre erreur au
démarrage** — et le service worker, qui met tout `/static` en cache, aurait
conservé ces 404.

D'où `Flask('terminal', root_path=…)` explicite. Le gardien compare les chemins
**résolus** et fait deux requêtes réelles ; la mutation « root_path implicite »
le fait tomber.

`import_name` reste `'terminal'`, ce qui préserve `app.name`. Le monolithe le
produisait déjà dans les deux modes : `__name__` vaut `'terminal'` à l'import, et
`'__main__'` en lancement direct — cas où Flask renvoie de toute façon le nom du
fichier.

## `auth` n'était pas un blueprint à injection

Il figurait dans `A_INJECTION` avec la raison « code d'accès (VERTEX_CODE) ».
Vérifié : `VERTEX_CODE` vient de `vertex/app/config.py`, **pas** du monolithe.
Il est donc enregistré par `create_app()`, **en premier**, parce que son
`before_request` doit pouvoir refuser une requête destinée à n'importe quel
blueprint. `A_INJECTION` passe de 7 à 6 entrées, et le test suit.

## Un test à moi qui ne pouvait pas échouer

La première version de `test_le_verrou_d_acces_est_pose_avant_tout_le_reste`
affirmait garder la place du verrou *à l'intérieur* de `create_app()`. Mutation
M5 : verrou déplacé en fin de fabrique → **le test passait**.

Il avait raison de passer : `create_app()` n'enregistre que lui, donc il est
premier où qu'on le mette dans la fonction. Le comportement ne change pas. Le
test, lui, annonçait protéger quelque chose qu'il ne pouvait pas voir.

Remplacé par `test_l_ordre_d_enregistrement_servi_est_celui_qui_est_declare`,
qui contrôle l'ordre **servi** au complet. Mutations de contrôle : verrou
supprimé → échoue ; les 15 blueprints avancés avant lui → l'application ne se
construit plus du tout.

## Le neuvième piège de sous-chaîne — le premier que j'ai posé moi-même

`test_le_monolithe_ne_construit_plus_l_application` cherchait `Flask(__name__)`
dans `terminal.py`. Il échouait sur un fichier parfaitement correct : la chaîne
vit désormais dans **le commentaire qui explique pourquoi elle a disparu**.
Retargeté sur l'affectation (`^\s*app\s*=\s*Flask\(`).

## Ce que trois gardiens maison ont arrêté

1. `test_terminal_imports_lot324` — quatre imports devenus orphelins
   (`Flask`, `redirect`, `request`, `_auth`). Retirés.
2. `test_safe_api_errors_lot648` — appelait `terminal._err_500` directement.
   **Retargeté et renforcé** : le handler est maintenant éprouvé de bout en bout
   (route qui lève → requête réelle → réponse servie), plus un second test qui
   vérifie qu'il est bien **enregistré sur l'application servie**. L'ancienne
   forme vérifiait la fonction ; celle-ci vérifie qu'elle sert.
3. `test_pass_terminal_lot386` — recensement gelé à 38 `except: pass`, devenu 36.
   Les deux partis sont nommés dans le fichier, avec une note explicite : la
   première baisse est **certaine** (le `try` entourait un import), la seconde
   est **raisonnée** — le lot 386 n'avait pas consigné la famille de chaque
   ligne. Le `pass` de `_gzip_response` est devenu un `return resp` explicite.

Aucun n'a été contourné, et **aucune borne n'a été relevée**.

## Preuves

```text
compileall                       exit 0
pytest tests/ -q                 3 289 passed
diff des règles avant/après      PARITÉ EXACTE (194 = 194, aucune ligne)
mutations du gardien fabrique    6/6 mordent après correction du test creux
```

Serveur réel, `DEMO=1 NO_IBKR=1` — chaque morceau déplacé vérifié par son
**effet**, en HTTP, pas par sa présence dans le fichier :

```text
huit espaces                     200 · 0 débordement · 0 erreur console
/api/client-log                  count: 0
X-Content-Type-Options           nosniff
X-Frame-Options                  SAMEORIGIN
Referrer-Policy                  strict-origin-when-cross-origin
Permissions-Policy               camera=(), microphone=(), geolocation=()
/api/desk                        Cache-Control: no-store
/scan (Accept-Encoding: gzip)    Content-Encoding: gzip · Vary · 148 531 o
/static/chart.umd.min.js         200
/static/icon-180.png             200
/api/route-absente               404 {"error":"not_found","path":…}
JSON NaN                         {"x": null}
```

## Constat relevé, non corrigé

La page 404 est peinte en `#FF7A18` / `#FF9A3D` — l'**ancienne identité orange**,
alors que `CLAUDE.md` fixe le violet `#9B7BFF`. Constaté au déplacement, laissé
tel quel et **écrit dans le module** : repeindre une page au passage d'une
extraction mêlerait deux changements dans un même diff, et la couleur d'une page
d'erreur est une décision de design, pas une conséquence de refactorisation.

## État de G1

| responsabilité (RELEASE_GATES G1) | propriétaire |
| --- | --- |
| factory Flask | **`vertex/app/factory.py::create_app`** |
| routes | `vertex/app/factory.py::BLUEPRINTS` |
| lifecycle / workers | `vertex/app/lifecycle.py` |
| scheduler | `vertex/scheduler/registry.py` (corrigé) |

Les quatre ont un propriétaire modulaire, avec parité prouvée et sans double
démarrage. **Ce qui reste avant de déclarer G1 PASS** : 11 routes LEGACY vivent
encore dans `terminal.py` (2 à 5 dépendances chacune, patron `make_blueprint`
requis) et 6 blueprints y sont encore enregistrés parce que l'état qu'ils
consomment y vit. La phrase de G1 « `terminal.py` n'est plus le centre de
nouvelles responsabilités » est tenue ; « n'en a plus aucune » ne l'est pas.

**Verdict : G1 tenu sur les quatre propriétaires nommés, non déclaré PASS.**
La décision revient à l'humain.
