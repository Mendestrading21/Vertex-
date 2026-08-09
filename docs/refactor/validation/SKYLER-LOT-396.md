# SKYLER LOT 396 — Les octets servis n'ont pas bougé

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-396` (base : lot 395 fusionné,
df84870)

**Aucun code. Aucun gardien. Aucun test ajouté.** Deuxième lot court consécutif,
et c'est encore le bon résultat.

## Le point contrôlé — différent de celui du 395

Le lot 395 avait re-mesuré les deux pistes fines restantes. Répéter la même
vérification n'apprendrait rien : ce lot contrôle **la preuve la plus forte de la
boucle**, celle qui n'avait pas été refaite depuis le **lot 390** — le MD5 des
8 pages servies.

```text
page             référence      mesuré         verdict
/                fc15688d1af6   fc15688d1af6   IDENTIQUE
/markets         c0bb91c6971a   c0bb91c6971a   IDENTIQUE
/opportunities   6a22a6abbd03   6a22a6abbd03   IDENTIQUE
/analysis        113827718e99   113827718e99   IDENTIQUE
/portfolio       f1b41b665d4a   f1b41b665d4a   IDENTIQUE
/options         6387210de785   6387210de785   IDENTIQUE
/journal         243699ace2d5   243699ace2d5   IDENTIQUE
/system          73e917c0f2d0   73e917c0f2d0   IDENTIQUE
```

**8/8.** Six lots après le 390 — dont deux qui ont modifié des fichiers de test
et un qui a corrigé une docstring — **pas un octet servi n'a bougé**. La
discipline « aucun fichier de production touché depuis le lot 372 » est vérifiée
par la mesure, pas seulement affirmée.

## Ce que la sonde a reproduit au passage

Lancer le serveur DEMO pour ce contrôle a reproduit **à l'identique** la
trouvaille du lot 391 :

```text
breadth_history — avant 16 points, après 17
   date ajoutée  : ['2026-08-09']
   dernier point : {"d": "2026-08-09", "a50": 50, "a200": 45, "net": -4, "health": 37}
```

Mêmes valeurs que les seize précédentes. Le dossier de rang 1 n'est pas
théorique : **il se reproduit à chaque démarrage en mode démo**, y compris celui
de l'agent. Restauré à l'octet (retour à 16 points), écart runtime final : aucun.

Trois fichiers runtime touchés cette fois (`ai_enrichment`, `breadth_history`,
`daily_prev`) contre huit au lot 390 — l'écart tient à la durée du scan, pas à un
changement de comportement ; je ne l'interprète pas plus loin.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- Arbre propre, **aucun fichier touché** — ni production, ni test.
- Serveur DEMO **arrêté** (port 5002 fermé, aucun processus vivant) ; snapshot
  des 21 fichiers runtime avec contrôle d'apparition ; **écart final aucun**.
- Suite : **2862 passed / 2 skipped**, inchangée. SW : `td-shell-v187`.

## Portée

Le MD5 prouve que **le HTML servi** est identique ; il ne dit rien des fichiers
`/static` (couverts, eux, par l'empreinte du gardien SW, rejouée au lot 394).
Et il vaut pour l'état du dépôt aujourd'hui, pas pour ce qu'un utilisateur a en
cache.

## Où en est la boucle

Deux lots courts d'affilée, avec un point de contrôle différent à chaque fois :
395 → les pistes fines restantes ; 396 → les octets servis. La règle tient :
**un constat se vérifie, il ne se répète pas.**

La matière utile reste **décisionnelle**. Deux dossiers chiffrés et sans risque :

1. **Purge des 7 points MSFT fabriqués** dans `gex_history_cache.json` (388).
2. **Le scan de démo écrivant dans `breadth_history.json`** (391) — reproduit
   ci-dessus, dix-septième point identique.

Prochaine échéance périodique : bilan n°9 **~lot 400**.
