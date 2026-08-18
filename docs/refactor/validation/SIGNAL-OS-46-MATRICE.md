# SIGNAL OS · LOT 46 — LA MATRICE COMPLÈTE, ET LE TÉMOIN QUI LA REND CRÉDIBLE

Branche : `agent/vertex-signal-os-v1` · SW **v235** (aucun octet servi touché)

Le lot 42 a étendu `mesurer_integrite_pages.py` de deux largeurs à cinq — puis
**ne l'a pas lancé sur les trois nouvelles**. Un instrument étendu mais non
utilisé est une affirmation sans preuve ; ce lot la fournit, et découvre au
passage que le relevé lui-même n'était pas garanti.

---

## 1. Pourquoi cinq largeurs, et pas deux

`VALIDATION.md` demande une matrice à cinq colonnes. L'outil n'en mesurait que
les **extrémités** — 1440 et 320. Or les défauts de grille ne naissent pas aux
extrémités mais aux **bascules** :

| largeur | ce qui bascule |
| --- | --- |
| 1440 | référence, 2–3 colonnes |
| **1024** | sidebar compacte |
| **768** | rail vers navigation mobile |
| **390** | une colonne, graphiques 280–340 px |
| 320 | WCAG 1.4.10, reflow sans défilement horizontal |

Un débordement propre à 768 px passait entre les deux mesures sans que rien ne
le dise.

---

## 2. Le défaut de l'instrument, trouvé en se méfiant de son propre zéro

Premier relevé : **0 défaut sur les cinq largeurs**. Résultat agréable, et
inexploitable tel quel — car rien ne prouvait que le navigateur avait
réellement appliqué le gabarit demandé. Un « 0 débordement à 768 px » mesuré à
1440 est **propre pour la mauvaise raison**.

L'outil vérifie donc désormais, sur la première vue de chaque largeur, que
`window.innerWidth` vaut bien la largeur demandée, et **refuse de continuer**
sinon — code de sortie distinct, pas un vert.

Contre-épreuve : en forçant le gabarit à 1440 tout en demandant 768, l'outil
s'arrête sur
`AVEUGLE — largeur demandee 768 px, largeur rendue 1440 px`.
Le témoin mord.

---

## 3. Le verdict

**35 vues × 5 largeurs = 175 relevés.** À chaque largeur : 0 identifiant
dupliqué · 0 erreur de page · 0 débordement horizontal · 65 liens internes
distincts, 0 cassé.

C'est le critère n°1 du « final release gate » (`VALIDATION.md`) qui passe de
*partiel* à **tenu** : la matrice responsive est mesurée sur toutes ses
colonnes, et le relevé est garanti par un témoin.

---

## 4. Ce que ce lot ne dit pas

1. **Le débordement mesuré est celui du DOCUMENT** (`scrollWidth` vs
   `clientWidth` de `documentElement`). Le rognage d'une carte *à l'intérieur*
   de la page est un autre défaut, et c'est
   `mesurer_rognage_silencieux.py` qui le tient — 0 à 1440 comme à 390.
2. **Une largeur, un rendu.** La matrice ne teste pas le *redimensionnement à
   chaud* : un défaut qui n'apparaîtrait qu'en tirant la fenêtre de 1440 à 768
   sans recharger n'est pas vu.
3. **Les états conditionnels** (tiroir ouvert, bandeau d'erreur, watchlist
   remplie) restent hors du balayage — même réserve qu'au lot 41.
