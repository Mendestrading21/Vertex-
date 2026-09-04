# 11 — Audit sécurité

## Ce qui est bien fait
- **Verrou d'accès** : `VERTEX_CODE` (`.env`) → toute l'app protégée par code d'entrée
  (`terminal.py:127-141`, blueprint `auth`). Sans `VERTEX_CODE` : démo ouverte **mais** liaison réseau restreinte.
- **Secret** : `VERTEX_SECRET` indépendant, sinon dérivé/persisté (`.vertex_secret`), gitignoré.
- **Lecture seule** : `READONLY=True`, workers IBKR `readonly=True`, 17 outils d'ordre interdits — surface d'écriture
  côté broker **nulle** (voir `09`).
- **Runtime gitignoré** : `.env`, `.vertex_secret`, `desk_data.json`, `desk_backup_*`, caches — non commités.

## Findings
- **SEC-01 (P1) — Surface XSS via `innerHTML`.** ~**649** usages d'`innerHTML` (pages + terminal.py) contre **5**
  appels `sanitize_news`. Tout contenu **externe** (news, textes tiers) rendu en `innerHTML` doit passer par
  `news_plus.sanitize_news()` (règle produit n°5). **Action** : recenser les injections `innerHTML` alimentées par
  des sources externes vs. par des chaînes internes de confiance ; garantir la sanitisation des premières + test.
- **SEC-02 (P2) — Liaison réseau.** Sans code d'accès, n'écouter que `127.0.0.1` ; LAN/iPhone → `VERTEX_CODE`
  (ou `VERTEX_LAN=1` en connaissance de cause). Vérifier que le binding par défaut reste local. `IBKR_HOST` par
  défaut `127.0.0.1` (`terminal.py:803`).
- **SEC-03 (P2) — Secrets hors de l'audit.** Cet audit et toute capture doivent **masquer** les identifiants de
  compte et ne jamais contenir `.env`/`VERTEX_SECRET`/clés API. Gardien humain à chaque commit de docs.
- **SEC-04 (P3) — En-têtes de sécurité.** Évaluer CSP / `X-Content-Type-Options` / `Referrer-Policy` sur les
  réponses HTML (defense-in-depth vis-à-vis de SEC-01), sans casser les CDN de graphes si utilisés en local.

## Principe
Vertex est mono-utilisateur, local par défaut, lecture seule. La priorité sécurité n°1 est **l'intégrité des
données affichées** (ne pas mentir) autant que la confidentialité. Détail : `.claude/rules/vertex-safe-editing-rules.md`.
