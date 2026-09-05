# Adoption des méthodes ECC — test Python, E2E et QA navigateur

Trois skills du catalogue *Everything Claude Code* (ECC) sont retenus comme
**sources de méthode** pour les lots de qualité Vertex : `python-testing`,
`e2e-testing` et `browser-qa`.

Aucun n'est installé, exécuté ni recopié. Ils n'ajoutent ni skill actif, ni
agent, ni hook, ni dépendance, ni commande. Le skill maître `vertex-2-0` reste
la seule autorité ; ce document en est une référence, jamais un concurrent.

## Pourquoi ces trois-là, et pas le catalogue

ECC publie 286 skills. La quantité installée n'est pas un objectif : une
méthode entre ici seulement si elle améliore un contrôle Vertex précis.

Les 283 autres sont écartés pour trois motifs mesurables :

- **stack absente** — `backend-patterns` vise Node/Express/Next.js ;
  `database-migrations`, `postgres-patterns` et `prisma-patterns` supposent un
  SGBD que Vertex n'a pas (persistance fichier via `vertex/services/persist.py`) ;
- **autorité concurrente** — `safety-guard`, `delivery-gate` et `gateguard` sont
  des hooks bloquants (stop hook, blocage Edit/Write/Bash). Les activer
  placerait une seconde grille de gates en travers des hard gates Vertex, ce
  que l'invariant d'autorité unique interdit ;
- **hors périmètre** — Kotlin, Swift, Laravel, Django, Kubernetes, DeFi,
  healthcare et le reste du catalogue ne touchent aucun contrôle Vertex.

## Audit supply-chain préalable

Exigé par `methodology-sources.md` avant toute adoption externe.

| Critère | Constat | Preuve |
|---|---|---|
| Source | `github.com/affaan-m/ECC` | dépôt attaché à la session |
| Version | `2.2.1` | `VERSION` |
| SHA audité | `847e7f6494900ef9b9ea0569269f7e2db6d38071` | `git rev-parse HEAD`, 2026-09-04 |
| Licence | MIT | `LICENSE` — copie autorisée avec attribution ; la méthode est malgré tout reformulée, pas recopiée |
| Permissions | aucune | les trois `SKILL.md` sont du Markdown pur |
| Hooks | aucun | `ls skills/<nom>/` → `SKILL.md` seul, aucun script |
| Dépendances ajoutées | aucune | `playwright` et `pytest` sont déjà déclarés dans `requirements-dev.txt` |
| Adéquation Flask | partielle | détaillée par skill ci-dessous |
| Plan de retrait | supprimer ce fichier et son lien dans `SKILL.md` | aucun consommateur runtime, aucun import, aucun test |

## Constat mesuré qui motive l'adoption

Quatre instruments navigateur existent déjà et **ne mesurent rien** :

- `requirements-dev.txt` déclare `playwright>=1.40` et documente que les gates
  G4 « n'ont jamais tourné, ni en CI ni en local » ;
- `.github/workflows/ci.yml` n'installe pas Chromium — `grep -n "playwright\|chromium"`
  sur le workflow ne renvoie aucune ligne ;
- `tests/test_vertex_1_0_aveu_navigateur.py` documente les quatre instruments
  qui sortaient en code 1 faute de navigateur, confondant « jamais mesuré » et
  « le produit a planté ».

Un gate qui ne s'exécute nulle part ne garde rien. C'est le défaut que ces
méthodes visent — pas une amélioration cosmétique de la suite.

## `python-testing` — méthodes retenues

Adéquation forte : Vertex est un dépôt pytest avec un `conftest.py` central et
plusieurs centaines de `tests/test_*_lotNNN.py`.

- **Cycle rouge → vert → refactor** : le défaut est prouvé par un test qui
  échoue *avant* la correction. Cohérent avec « tests rouges si défaut » du
  protocole d'exécution.
- **Portée des fixtures** (`function`, `module`, `session`) choisie
  explicitement : une fixture `session` qui porte un snapshot de marché ne doit
  pas fuiter entre tests et fabriquer une fraîcheur que le runtime n'a pas.
- **Paramétrisation avec `ids` lisibles** : un cas financier hostile doit être
  nommé dans le rapport d'échec, pas réduit à `case3`.
- **`autospec` sur les mocks** : un mock non contraint d'un client de données
  peut survivre à un changement de signature et verdir un test qui ne teste
  plus rien.
- **Marqueurs déclarés dans `pytest.ini`** avant usage, pour que
  `-m "not slow"` reste une sélection et non un oubli silencieux.
- **`tmp_path` plutôt que des chemins réels** pour les tests de persistance.

Rejeté : la section base de données (Vertex n'en a pas) et le seuil de
couverture chiffré, qui n'est pas un contrôle Vertex — la preuve exigée est le
défaut reproduit, pas un pourcentage.

## `e2e-testing` — méthodes retenues

Adéquation partielle : le skill est écrit en TypeScript pour le runner
Playwright JS. Vertex utilise le binding **Python**. Les corps de code ne sont
pas transposables ; les méthodes le sont.

- **Page Object Model** : les sélecteurs d'une page vivent à un seul endroit.
  Applicable aux douze pages cibles, et cohérent avec la règle du propriétaire
  canonique unique.
- **Artefacts d'échec** — capture, trace, vidéo attachées à l'échec plutôt que
  reconstituées après coup.
- **Identification d'un test instable par répétition** (`--repeat-each`) avant
  toute conclusion : mesurer l'instabilité, ne pas la supposer.
- **Installation explicite du navigateur dans le job CI** : c'est le point qui
  débloque directement les gates G4 aujourd'hui muets.

**Rejeté, et c'est important :**

- **La quarantaine** (`test.fixme`, `test.skip` sur un test instable). Vertex
  interdit qu'un test masque une perte réelle — c'est la préoccupation
  `audit-integrity` déjà nommée dans `methodology-sources.md` à propos de
  `tests/_supersede.py`. Un test instable est un défaut à corriger ou une
  abstention explicitement rapportée, jamais un test désactivé en silence.
- **La section « Financial / Critical Flow Testing »**, qui pilote une
  exécution d'ordre et une confirmation blockchain. Interdite par
  `READONLY=True` / `ANALYSIS_ONLY=True` : Vertex n'a aucun chemin d'exécution
  à tester, et n'a pas à en acquérir un pour satisfaire une méthode externe.

## `browser-qa` — méthodes retenues

- **Rayon d'action en lecture seule par défaut**, jamais de parcours mutant, et
  **rédaction des captures** avant enregistrement. Vertex durcit ce point : une
  capture ne doit contenir ni identifiant, ni solde, ni position déclarée, ni
  clé — l'invariant s'applique aussi aux preuves de livraison.
- **Le bruit console est trié, pas ignoré** : une erreur tierce et une erreur
  produit ne se rangent pas ensemble.
- **`INCONCLUSIVE` quand la référence visuelle manque** — jamais un succès
  silencieux. C'est exactement la distinction « mesuré » / « jamais mesuré »
  que `test_vertex_1_0_aveu_navigateur.py` impose déjà.
- **axe-core est nécessaire mais non suffisant** : environ 30–40 % des règles
  WCAG sont automatisables. Clavier, ordre de focus, zoom et lecteur d'écran
  restent manuels. Ne jamais conclure « accessible » depuis une passe
  automatique.
- **Verdict explicite** en fin de rapport, sans moyenne ni score composite.

**Adapté :** le skill propose 375 / 768 / 1440 px. Vertex impose **390 / 1024 /
1600 px**. Les points de rupture Vertex l'emportent.

**Rejeté :** la dépendance à un MCP navigateur (`claude-in-chrome`,
`browserbase`). Vertex pilote Playwright Python en local, sans serveur externe
ni permission supplémentaire.

## Matrice besoin → contrôle Vertex

| Besoin | Méthode retenue | Preuve exigée |
|---|---|---|
| Défaut prouvé avant correction | `python-testing` — rouge/vert | test rouge daté, puis vert après correctif minimal |
| Mock qui ne dérive pas | `python-testing` — `autospec` | signature vérifiée, test rouge si la source change |
| Gates G4 réellement exécutés | `e2e-testing` — navigateur installé en CI | job CI installant Chromium, sortie 0 = mesuré / 2 = témoin muet |
| Sélecteurs de page maintenables | `e2e-testing` — POM | un propriétaire par page, aucun sélecteur dupliqué |
| Preuve visuelle par page | `browser-qa` — captures | 1600 / 1024 / 390 px, avant/après, console et `/api/client-log` contrôlés |
| Accessibilité | `browser-qa` + revue manuelle | axe-core **et** clavier, focus, zoom, contraste |
| Absence de fuite dans les preuves | `browser-qa` — rédaction | aucune donnée de compte ni secret dans une capture commitée |

## Subordination

En cas de contradiction entre une méthode ECC et le skill maître, les
invariants Vertex ou une référence de ce dossier, **le document Vertex
l'emporte sans discussion**. Ces méthodes guident un lot ; elles n'autorisent
jamais une permission, une dépendance, un skill actif supplémentaire ou une
modification métier implicite.
