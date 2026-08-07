# SKYLER LOT 259 — SECURITE.md ↔ réalité : 3 corrections (1 bouton fantôme)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-259` (base : lot 258 fusionné)

## Objet

Dernière porte d'entrée racine jamais auditée après README (257) et
DEMARRER_ICI (258) : `SECURITE.md` — le document qui explique le verrou
d'accès. Audité affirmation par affirmation contre le code.

## Ce qui est VRAI (vérifié dans la source, conservé)

- Cookie signé httponly + SameSite=Lax, **30 jours** (terminal.py
  L133-134 : `PERMANENT_SESSION_LIFETIME=timedelta(days=30)`).
- Comparaison à **temps constant** (auth.py L127 :
  `hmac.compare_digest`).
- **Anti-force-brute** : verrou progressif après 5 essais,
  `min(300, 15×(n-4))` s — « jusqu'à 5 min » exact (auth.py L133).
- Procédures Render / local / `.gitignore` : conformes.

## Les 3 corrections

1. **Bouton fantôme** : « Bouton “Se déconnecter & verrouiller” dans
   *Paramètres* » — ce bouton n'existe QUE dans `PAGE_SETTINGS`
   (terminal.py L7477), page héritée **orpheline** (0 routée, preuve
   lot 248) : aucun utilisateur ne peut l'atteindre. La route
   `/logout` fonctionne, elle → doc corrigée (« visiter /logout »).
2. **Désactivation incomplète** : « L'app redevient ouverte » omettait
   le durcissement (lot 218) : sans code, le serveur n'écoute plus que
   127.0.0.1 → précisé (cohérent avec README lot 257).
3. **Liste des pages publiques incomplète** : la vraie
   `PUBLIC_PATHS` (auth.py L28-30) inclut aussi `/logout`,
   `/api/healthz` et le webhook TradingView (authentifié par secret
   signé) → complétée.

## Constat pour l'humain (pas d'action prise)

Le bouton de verrouillage n'a jamais été recâblé dans la nouvelle UI
(l'ancienne page Paramètres est orpheline). `/logout` couvre le besoin,
mais si tu veux un bouton visible (ex. dans Système), c'est un petit
lot produit à part — dis-le.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs seulement.

## Preuves

- Chaque affirmation tracée vers sa ligne de code (citées ci-dessus).
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 260 : mini-bilan 256-260 attendu. La purge attend « GO purge
étape 1 ».
