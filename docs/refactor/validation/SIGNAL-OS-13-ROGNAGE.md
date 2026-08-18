# SIGNAL OS · LOT 13 — LE ROGNAGE SILENCIEUX A ENFIN UN INSTRUMENT

Branche : `agent/vertex-signal-os-v1` · SW v219 → **v220** · Suite **3102 passed**

Dette signalée pendant **six lots** : rien ne détectait un texte coupé par un
`overflow:hidden` **sans ellipse ni défilement**. C'est le défaut du lot 209 —
quatre cartes d'indice coupées de 25 à 66 px — trouvé alors *par hasard sur une
capture d'écran*, après que deux instruments de débordement l'eurent déclaré
inexistant : ils mesuraient le débordement du **viewport**, pas celui d'une carte.

L'instrument existe désormais : `tools/mesurer_rognage_silencieux.py`.

---

## 1. Le faux positif qu'il fallait exclure

Premier jet : **21 à 24 signalements, tous sur `.vx-sr-only`**.

Un texte réservé aux lecteurs d'écran est rogné **délibérément** — boîte de
1×1 px, `overflow:hidden` — c'est la technique standard. Sans cette exclusion,
l'instrument accuse précisément l'accessibilité et noie le signal réel.

Après exclusion : **1 défaut à 1440 px, 4 à 390 px.** Signal net.

---

## 2. Trois mécanismes, tous invisibles à la relecture

| site | mécanisme | mesure |
| --- | --- | --- |
| Marchés · cartes macro | `grid-template-columns:1fr auto` + aire figée à 120 px | 5 px à 1440, 20-22 px à 390 |
| Marchés · variante FLAT | rangée **flex** : `min-width:auto` empêche la réduction | 20 px à 390 |
| Portefeuille · Surveillance | `.vx-truncate` dont le `white-space` repasse à `normal` | **37 px verticaux** à 390 |

**Le premier est le lot 209 sur une autre famille de cartes** : une piste `1fr`
ne descend pas sous la largeur *min-content* de son contenu, la carte déborde, et
son `overflow:hidden` coupe sans le dire. `minmax(0,1fr)` + aire en
`min(120px,34%)`.

**Le deuxième montre pourquoi un correctif « sur la famille » ne suffit pas** :
la variante FLAT est en `flex`, donc le `minmax(0,1fr)` de la grille ne la
protège pas. Traitée séparément, sous une bascule déjà recensée (520 px, lot 611
— aucune bande de largeur neuve).

**Le troisième est le plus retors.** `.vx-table-cards td` remet
`white-space:normal` avec une spécificité supérieure à `.vx-truncate` : le texte
passe à la ligne, mais `overflow:hidden` et le `max-width` en ligne restent, et
ce qui dépasse est perdu **verticalement**. *Une troncature à une ligne qui cesse
d'être à une ligne n'est plus une troncature : c'est une perte.*

---

## 3. Un manque du lot 10, trouvé en passant

Au lot 10 j'avais cherché les littéraux **hexadécimaux** du cuivre (`#D28A54`)
et **jamais** leur forme `rgba(210,138,84,…)`.

**Quatorze occurrences** étaient restées cuivre — halos, lisérés et dégradés —
dans `base.css`, `polish.css`, `tokens.css`, `neon-glass.css` et
`options-intel.js`. Converties.

> Chercher une couleur par **une** de ses écritures, c'est n'en trouver qu'une
> partie. Le lot 10 se croyait complet ; il ne l'était pas.

---

## 4. Le gardien m'a repris quatre fois, dont une inédite

| assertion | pourquoi elle restait verte |
| --- | --- |
| `'flex-wrap:wrap' in css` | la déclaration figure des dizaines de fois ailleurs |
| `'.vx-table-cards td.vx-truncate' in css` | la chaîne cherchée est un **préfixe** de `td.vx-truncateX` |
| `'vx-sr-only' in src` | le mot figure aussi dans **la prose** de l'outil |
| `'e.scrollHeight' in code` | figure aussi dans la ligne qui *rapporte* l'écart |
| **`'minmax(0,1fr)' in bloc`** | **mon propre commentaire explicatif contient la chaîne** |

Le dernier est nouveau et mérite d'être retenu : j'avais écrit un commentaire
expliquant *pourquoi* la règle emploie `minmax(0,1fr)`, et ce commentaire suffit
à faire passer le test après suppression de la déclaration. **Un test qui lit sa
propre justification ne lit pas le code.** `_regle()` retire désormais les
commentaires.

C'est la **huitième** fois que la portée d'une assertion me trompe dans cette
refonte.

---

## 5. Mesures — serveur `td-shell-v220` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| rognage silencieux à 1440 px | 1 | **0** |
| rognage silencieux à 390 px | 4 | **0** |
| défilement horizontal de page (1440/768/390) | aucun | **aucun** |

Gardien `tests/test_signal_os_rognage_lot13.py` — 5 tests, **9 mutations sur 9
tuées**.

---

## 6. Ce que je n'ai PAS fait, et pourquoi

**Les 5 modules UI morts ne sont pas supprimés.** Mesure de ce lot :

- **0 consommateur en production** — confirmé, et aucun ne déclare de route ;
- `CLAUDE.md` affirme que `vertex/ui/journal.py` porte « une 4ᵉ copie de
  `DESK_KEYS` » : **c'est périmé**, le symbole n'y existe plus (seuls des noms
  de clés littéraux subsistent dans du JS mort) ;
- mais **4 fichiers de tests les importent**, et deux d'entre eux gardent des
  contrats **vivants** : `test_strategy_os_routes.py` teste 8 routes réelles et
  n'utilise le module mort que dans un seul de ses 9 tests ;
  `test_production.py` s'appuie sur `journal.JS` pour garder le contrat
  `DESK_KEYS`.

Supprimer exige donc de réécrire des gardiens qui protègent du code vivant.
`CLAUDE.md` marque par ailleurs ces modules « en attente de décision ».
Le faire à la hâte en fin de session est exactement la manière dont on expédie
une régression. **Mesure publiée, suppression non faite.**

---

## 7. Dette

- 5 modules UI morts (146 Ko) — mesure faite, suppression à instruire (§6).
- `CLAUDE.md` § DESK_KEYS : la mention de `journal.py` est périmée.
- Rang 3 du Journal (grade / setup / horizon), win/loss par bucket.
- Opportunités, Portefeuille (5 vues sur 6), Options : rangs non audités.
- `chart-theme-obsidian-copper.js` : nom qui ment.
- Étiquetage démo : figé en caractérisation (lot 08).
