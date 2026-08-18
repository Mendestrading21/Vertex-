# SIGNAL OS · LOT 65 — CE QUI RESTE, CLASSÉ POUR ÊTRE DÉCIDÉ

Branche : `agent/vertex-signal-os-v1` · SW **v245, inchangé** (aucun octet servi
touché) · Suite **3 520 passed**

57 rapports SIGNAL-OS, **77 réserves ouvertes**, relevées mécaniquement. Une
liste de 77 lignes n'est pas exploitable : personne ne décide sur ça. Ce document
la réduit à ce qui demande vraiment un choix.

**Le résultat principal du classement : ce ne sont pas 77 problèmes.** Une
vingtaine sont *la même* réserve, répétée à chaque lot parce que chaque lot la
redéclare honnêtement.

---

## A. Une seule réserve, répétée ~20 fois — et elle est structurelle

| ce qui revient | dans les lots |
| --- | --- |
| mode **démonstration** (`DEMO=1 NO_IBKR=1`) | 56, 59, 60, 61, 62, 63 |
| une seule largeur (**1440 px**) | 57, 59, 60, 61, 62, 63 |
| un seul titre (**ACN**) | 56, 61, 62, 63 |
| vues secondaires non parcourues | 57, 59 |

**Tout ce qui a été mesuré des lots 41 à 64 l'a été dans le même environnement.**
Ce n'est pas une négligence de lot : c'est le seul environnement dont je dispose.

Ce que cela borne, concrètement : chaque fois qu'un rapport dit « mesuré », il
faut lire « mesuré en démonstration, à 1440 px, sur ACN, vues par défaut ». Les
conclusions **statiques** (une clé n'est passée par personne ; une constante ne
dépend d'aucun âge) ne dépendent pas de l'environnement. Les conclusions
**peintes** (« 4 cartes, 0 badge ») en dépendent.

> **Cette réserve ne peut pas être fermée par un agent.** Elle demande TWS
> connecté, marché ouvert, l'iPhone et le LAN. C'est le vrai trou de propreté du
> projet, et il vaut plus que les 57 autres réserves réunies.

---

## B. Six décisions qui attendent un mot — pas du travail, un arbitrage

1. **`legacy_basket_risk`** (lot 58) — retraite non faite. Supprimer une route
   est un **effet sortant** : ce n'est pas une décision d'agent.
2. **Journal et Système n'affichent aucune étiquette d'âge en premier écran**
   (lot 63). Journal n'en a jamais eu ; **Système a perdu la sienne par mon
   fait** — sa pilule décrivait la connexion sous la classe de la fraîcheur, je
   l'ai reclassée en `vx-badge-status`. À **ratifier ou annuler** : c'est le seul
   endroit de la série où j'ai retiré quelque chose de visible sans mandat
   explicite.
3. **`recommendation` doit-il être peint ?** (lot 58) — le peindre créerait un
   **second domicile** pour une donnée déjà affichée. Mon verdict est une lecture
   de conception, pas une mesure.
4. **`card.controlsHtml`, `card.size`, `card.stateMessage`** (lot 64) — trois
   branches du Chart Shell qu'aucun appelant n'emprunte. Câbler ou retirer.
5. **La troisième disclosure imbriquée d'Analyse** (lot 56) — cinq blocs vivent
   maintenant à deux ou trois replis de profondeur. Question d'ergonomie, pas de
   justesse.
6. **La pilule d'état de Système répète le `<h2>` qui la suit** (lot 63) —
   doublon vu en passant, hors sujet du lot, non corrigé.

---

## C. Limites d'instrument déclarées — à laisser telles quelles

Ce ne sont pas des dettes : ce sont les **bornes** que chaque outil annonce pour
que son silence ne passe pas pour une garantie. Les « fermer » demanderait un
analyseur complet de JavaScript, pas un lot.

- l'AST ne suit pas une variable au-delà d'un saut (lots 57, 58 — **14 moteurs
  restent indéterminés**) ;
- seul `innerText` est lu : un chiffre peint dans un attribut, un `title` ou un
  SVG échappe (lot 61) ;
- une clé calculée à l'exécution échappe ; **38 sites d'appel non analysables**,
  comptés et annoncés (lot 64) ;
- « dérivé » n'est pas distingué de « inventé » — le tri reste humain (lot 61).

**Aucune de ces limites n'est tue.** C'est la règle de la série : une limite
passée sous silence transforme le silence de l'outil en garantie.

---

## D. Ce qui reste réellement mesurable, et que je peux faire

Classé par ce que ça protège, pas par difficulté.

| # | ce qui manque | pourquoi ça compte |
| --- | --- | --- |
| **D1** | **9 familles de coupure sur 16 jamais exercées** (lot 60) | la dégradation n'est prouvée que pour 7 sources sur 16 |
| **D2** | **panne SIMULTANÉE de deux sources** (lot 60) | le cas réel d'un incident réseau ; jamais exercé |
| **D3** | **balayage responsive** — 390 / 768 / 1920 (lots 59, 61, 62, 63) | l'utilisateur consulte sur iPhone ; tout est mesuré à 1440 |
| **D4** | **vues secondaires** de chaque espace (lots 57, 59) | chaque espace a des onglets jamais parcourus par les sondes |
| **D5** | **14 moteurs indéterminés** (lot 58) | on ne sait pas s'ils atteignent l'écran |
| **D6** | **seuils `saved` / `error` / `offline`** de la fraîcheur (lot 62) | trois états du vocabulaire jamais exercés |

**D3 est le plus utile des six** : c'est le seul qui touche un usage réel déclaré
de l'utilisateur (consultation iPhone), et le seul dont un défaut serait visible
tous les jours plutôt que pendant un incident.

---

## E. Ce qui est déjà propre, et qu'il ne faut pas rouvrir

Pour que la liste ci-dessus ne laisse pas croire à un chantier ouvert partout :

- suite **3 520 passed**, arbre de travail propre, tout poussé ;
- **0 erreur console** sur les 8 espaces, `/api/client-log` à `count:0` ;
- **0 étiquette de fraîcheur constante** sur les 8 espaces (lot 63) ;
- **0 option passée-mais-ignorée** par le Chart Shell (lot 64) ;
- **0 chiffre peint sans source** parmi ceux tracés (lot 61) ;
- surface IBKR **entièrement classée en lecture seule**, aucun nom calculé ;
- `CLAUDE.md` **vérifié par un gardien** depuis ce lot — 36 fichiers cités, aucun
  mort, aucun chiffre faux.

---

## F. Réserves de ce lot-ci

1. **Le relevé des 77 est mécanique** : il lit les sections « Réserves » des
   rapports `SIGNAL-OS-*`. Une réserve écrite ailleurs dans un rapport lui
   échappe, et les rapports `SKYLER-*` ne sont pas couverts.
2. **Le classement est un jugement**, pas une mesure. Le rang de D3 est mon avis,
   pas un chiffre.
3. **Les 44 dossiers de `docs/skyler/DECISIONS-EN-ATTENTE.md` ne sont pas
   fusionnés ici** : ils relèvent d'une autre gouvernance, et le fichier reconnaît
   lui-même que son compte contredit celui du lot 527.
