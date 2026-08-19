# G2 · #783 — Un push ne peut plus effacer ce qu'il n'envoie pas

Décision : `docs/vertex-1.0/DECISIONS.md` → **D-014**
Code : `vertex/app/routes/desk.py`
Gardien : `tests/test_desk_perte_lot362.py` (11 tests, 7 mutations)

---

## Le défaut n'a pas été découvert ici : il était déjà mesuré, et laissé ouvert

`RELEASE_GATES.md` G2 : *« … et la persistance/sauvegarde est prouvée »*.
`tests/test_desk_perte_lot362.py` avait mesuré trois faits **sans corriger**, et
son en-tête se terminait par une consigne :

> ⚠️ Ce sont des tests de CARACTÉRISATION : ils décrivent le contrat actuel, ils
> ne le bénissent pas. Si le serveur est un jour durci […], ces tests **DOIVENT**
> être mis à jour — c'est précisément leur rôle d'alerte.

Les trois faits :

1. un push `data: {}` était accepté et **remplaçait** le blob — l'écrasement
   redouté n'avait pas besoin d'être « à la main » ;
2. un push **partiel** remplaçait le blob entier : les clés absentes
   disparaissaient côté serveur ;
3. aucun instantané supplémentaire n'était pris à ce moment-là — le point de
   restauration restait l'état d'**avant la première sync du jour**, donc un
   restore faisait perdre tout le travail de la journée.

Ce ne sont pas des risques théoriques. Le client omet toute clé absente de
localStorage (`if (v != null)` dans `vx-entities.js`), et un navigateur dont
l'écriture localStorage échoue en silence — navigation privée, quota — hydrate
sans rien persister, puis pousse `{}`. Les données concernées sont les trades,
le journal, les positions et les alertes de l'utilisateur.

## Le choix : conserver, et le dire

Le serveur **fusionne** au lieu de remplacer. Une clé qu'il détient avec du
contenu et que le push n'envoie pas est conservée, et la réponse le déclare
(`conservees: [...]`) — silencieuse, la protection empêcherait le client de
s'apercevoir qu'il a perdu son stockage.

Le push reste **accepté** (200). Le refuser casserait la synchronisation d'un
navigateur en difficulté, c'est-à-dire précisément au moment où l'on veut
qu'elle continue de fonctionner.

**Pourquoi conserver plutôt que supprimer**, mesuré et non supposé : aucun
chemin du produit n'appelle `removeItem` sur une clé de desk (vérifié sur tout
le dépôt), et vider une liste écrit `'[]'`, qui est bien envoyé. Une absence
n'est donc **jamais** une intention de suppression.

### La contrepartie, et elle a mordu pour de vrai

Si l'omission ne supprime plus, supprimer doit se dire explicitement : envoyer
la clé **vide**. Ce n'est pas resté théorique — la première exécution de la
suite sous le nouveau contrat a laissé le marqueur de
`tests/test_desk_cycle_lot84.py` dans le desk **réel**, parce que son `finally`
remettait l'état d'origine en *omettant* la clé qu'il venait de créer. Corrigé
dans le test, écrit dans D-014, et vérifié par
`test_supprimer_une_cle_se_dit_desormais_EXPLICITEMENT`.

Le contre-exemple qui empêche la garde de tout figer est tenu lui aussi : une
valeur vide (`''`, `[]`, `{}`, `null`) **n'est pas du travail à protéger**.
Sans cela, le serveur empilerait indéfiniment des `'[]'` que plus personne
n'envoie, et `conservees` cesserait de signaler quoi que ce soit.

## Le trou du filet quotidien, comblé

Le filet existant prend son image **avant la première écriture du jour** :
restaurer rendait l'état d'hier. Un instantané
`desk_avantperte_<AAAAMMJJ>-<HHMMSS>.json` est désormais pris **à la seconde**,
au moment précis où des clés sont menacées — et il est listé par
`/api/desk/backups` (`type: 'avant-perte'`) et accepté par `/api/desk/restore`.

« Une portée n'est pas une sortie » : un instantané qu'aucune sortie ne nomme
n'est pas un filet, c'est un fichier. La grammaire du nom reste strictement
validée au restore — élargir à une seconde famille ne devait pas rouvrir une
traversée de chemin, et un test l'éprouve sur sept noms hors grammaire.

Rotations séparées : 7 quotidiens, 20 avant-perte. Le motif est ajouté au
`.gitignore` — ce sont des données personnelles.

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 295 passed        (3 289 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations du gardien           7/7 mordent, plus 2 sur le gardien retargeté
```

Les sept mutations : retour au remplacement total · plus d'instantané ·
protection trop large (les vides protégés) · conservation non annoncée ·
grammaire du restore relâchée · rotation avant-perte non bornée · instantané
non listé. Contrôle vert après restauration de l'arbre.

## Trois gardiens maison ont réagi — tous traités, aucun contourné

| gardien | ce qu'il a vu | traitement |
| --- | --- | --- |
| `test_caches_runtime_lot388` | une 13ᵉ écriture de cache runtime | recensement mis à jour **avec la réponse à la question qu'il pose** : quels tests l'atteignent, redirigent-ils leur stockage |
| `test_desk_cycle_lot84` | ne connaissait qu'une famille d'instantanés | élargi aux deux, en exigeant que chacun **déclare** sa famille |
| `test_desk_ecritures_lot387` | cherchait la chaîne `'data': d0.get('data')` dans le `finally` | réécrit **en AST** : la valeur postée doit descendre de `d0`, littéralement ou via une variable locale. L'intention est mieux tenue qu'avant ; deux mutations le confirment |

## Limites — ce que ce lot ne règle pas

- **Aucune interface ne consomme `/api/desk/backups` ni `/api/desk/restore`.**
  Mesuré : les deux routes ne sont citées que dans la liste d'API de la page
  Système. Restaurer reste donc une opération en ligne de commande. C'est un
  manque réel pour G6 (« sauvegarde/restauration, rollback testé ») et il est
  **hors du périmètre de ce lot** : construire l'écran de restauration est un
  chantier d'interface, pas une conséquence du durcissement.
- Le blob reste un **last-writer-wins** sur les clés envoyées. Deux appareils
  qui modifient la même clé en même temps : le dernier gagne, comme avant. Une
  fusion par clé demanderait un modèle de version que le produit n'a pas.
- La concurrence est protégée par un verrou **de processus** (`desk_lock`).
  Sous plusieurs workers WSGI, deux écritures simultanées resteraient possibles ;
  la production tourne à `--workers 1` (`render.yaml`), ce qui rend le cas
  inatteignable aujourd'hui mais **pas structurellement impossible**.

**G2 non déclaré PASS** : il exige aussi la convergence des doublons
entreprise/data/portfolio et l'uniformité des états de fraîcheur. Ce lot ferme
la troisième moitié — « la persistance/sauvegarde est prouvée » — et rien de
plus.
