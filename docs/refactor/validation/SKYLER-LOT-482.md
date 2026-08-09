# SKYLER LOT 482 — Retour au produit : QUATRE des dix « dossiers en attente » ne sont pas des dossiers — deux bornages et deux recoupements, tous de la cause 406/407 déjà classée et chiffrée. La liste tombe de dix à six.

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-482` (base : lot 481 fusionné,
`268eecd`)

Le 481 a fixé lui-même la consigne : *« la boucle a passé trois lots à se mesurer
elle-même. Le prochain doit revenir au produit. »* **Ce lot revient au produit** —
il mesure l'inventaire réel des défauts de Vertex, pas la forme de mes rapports.

**Il ne corrige rien.** Aucun fichier de production touché.

## Les DEUX contrôles — et le second corrige le réveil

Le 481 a posé une règle neuve : *un contrôle choisi parmi les cas que l'instrument
voit ne teste jamais ce qu'il ne voit pas.* Elle impose **deux** contrôles quand
l'instrument pose une restriction.

```text
CONTRÔLE 1 — cas connu, DANS le périmètre
   attendu (mesuré au 478)   vx-entities.js:236  equity() { return get('myTradesEquity', []); }
   mesuré                    :236  equity() { return get('myTradesEquity', []); }
   verdict                   PASSÉ

CONTRÔLE 2 — cas que la restriction du réveil EXCLURAIT
   le réveil affirme         « 426 (drawdown) vit dans performance_page.py / /journal »
   mesuré                    grep drawdownCard → vertex/ui/pages/portfolio_page.py:614
                             AUCUNE occurrence dans performance_page.py
   verdict                   LE RÉVEIL EST FAUX — et une restriction à
                             performance_page.py n'aurait RIEN trouvé
```

**La règle du 481 a payé dès son premier emploi.** Sans le second contrôle,
j'aurais cherché le drawdown dans le mauvais fichier et conclu à un dossier
inatteignable.

**Compte : arrêté avant publication, 46 → 47.**

---

# LA MESURE — quatre entrées de la liste ne sont pas des dossiers

Le réveil proposait de « vérifier si 408 + 409 + 411 partagent une cause » et si
le 426 est « un troisième symptôme ». **La mesure va plus loin que la question :
ce ne sont pas des dossiers du tout.** Chaque rapport le dit lui-même.

## 408 — un BORNAGE, et il se déclare comme tel

```text
titre    « Le || 0 du lot 407 est ISOLÉ, pas une famille »
verdict  « Le défaut du 407 est isolé. Le dossier de rang 1 reste ce qu'il était :
           un site, une page, une décision — pas une famille à traiter. »
         « Sur le chemin qui compte — les charges utiles envoyées aux moteurs —
           le défaut du 407 est UNIQUE. 25 POST examinés, 1 seul fautif. »
         « celui-ci BORNE ce qu'ils ont trouvé — un résultat négatif utile »
```

**Le 408 ne trouve rien : il mesure que le 407 ne s'étend pas.** C'est un
résultat, et c'est un résultat sur le **407**, pas un dossier neuf.

## 409 — un BORNAGE, et il se déclare comme tel

```text
titre    « Les 8 pages balayées : UNE SEULE consigne impossible, celle du 406 »
verdict  « Une seule consigne est impossible : celle du lot 406. Aucun site
           n'écrit myTradesEquity — vérifié une nouvelle fois, 0. »
         « Le défaut du 406 est UNIQUE sur les 8 pages servies. »
         « Comme le 408 l'a fait pour le || 0 du 407, ce lot BORNE le dossier
           plutôt que de l'élargir »
```

**Même forme : le 409 borne le 406.**

## 411 — un RECOUPEMENT

```text
titre    « Les 59 provenances déclarées : 2 nomment une origine sans producteur,
           et elles ne s'affichent jamais »
verdict  « 25 sur 27 sont exactes. Les deux seules qui nomment une origine sans
           producteur sont celles DU DOSSIER 406/407. »
         « Le préjudice du 406/407 est donc bien le graphique absent et la
           consigne impossible — PAS une provenance mensongère à l'écran. »
```

**Le 411 ne trouve pas un défaut : il PRÉCISE le 406/407** — et sa précision est
une **atténuation mesurée**, pas une aggravation. Il dit lui-même : « C'est une
précision, pas une atténuation : le HHI faux du 407, lui, **est** affiché. »

## 426 — un RECOUPEMENT, déclaré mot pour mot

```text
« Ce n'est PAS un défaut nouveau — c'est le dossier 406/411, retrouvé par un
  autre chemin. Je le note comme RECOUPEMENT, pas comme trouvaille. »
```

**Le 426 se retire lui-même de la liste des dossiers, cinquante-six lots avant
que je ne le lui demande.**

---

# CE QUE LA MESURE ÉTABLIT

```text
406  ┐
407  ├─ UNE cause : deux clés de DESK_KEYS lues, écrites par personne
408  │   BORNAGE du 407  — « isolé, pas une famille », 25 POST examinés
409  │   BORNAGE du 406  — « unique sur les 8 pages servies »
411  │   RECOUPEMENT     — les 2 provenances sans producteur sont les siennes
426  ┘   RECOUPEMENT     — déclaré tel quel par son propre rapport

CLASSÉ ET CHIFFRÉ AU 478 : rang 2 · 4 lignes · 1 fichier · régression FAIBLE
```

**Six numéros de rapport, un seul dossier.** Le 478 en avait fusionné deux ; la
mesure d'aujourd'hui en rattache **quatre de plus**.

```text
DOSSIERS EN ATTENTE DE CLASSEMENT :  10  →  6
   restants : 388 · 391/396 · 379 · 363 · 386 · 456+459 (volet symbols_usable)
```

## Une précision de produit, mesurée, et elle applique la leçon 477

Le 411 et le 426 disent que les étiquettes « ne s'affichent jamais ». Vérifié
par exécution — **et la formulation est exacte pour une raison qui mérite d'être
dite** :

```text
GET /portfolio → « clôtures déclarées (myTradesEquity) » PRÉSENT dans les octets servis
portfolio_page.py:604   if(eq.length>=2 && …)   ← la carte n'est CONSTRUITE que là
portfolio_page.py:617   source:'clôtures déclarées (myTradesEquity)'  ← à l'intérieur
```

**Le littéral est SERVI mais jamais PEINT.** C'est exactement la distinction du
477 (*un commentaire est servi mais pas affiché*), appliquée ici à une chaîne
enfermée dans une branche morte. **Un détecteur qui cherche dans les octets
servis le trouve ; l'utilisateur ne le voit jamais.**

Et la garde de la ligne 604 est **honnête** : sans série, la page rend un
`emptyCard` avec un motif et un bouton. **Le produit ne ment pas ici** — il se
tait correctement. C'est le témoin positif que le 478 avait déjà relevé, et il
tient.

## Classement — AUCUN, et c'est le résultat

**Il n'y a rien à classer.** Les quatre entrées ne portent aucun défaut propre :
deux mesurent l'absence d'extension d'un défaut connu, deux le décrivent
autrement. **Aucune ne survit au critère absolu du 480** — pour la raison la plus
simple : *aucune ne prétend à un défaut*.

**La feuille de décision est inchangée.** Le 406/407 y figure déjà (lot C,
rang 2, 4 lignes), et les quatre rattachements **n'ajoutent pas une ligne de
correction**.

## Mutualisation — c'est le lot entier

Contrairement aux 477 (« isolé ») et 479 (« absente »), **ici la mutualisation
n'est pas un bonus : c'est le résultat**. Les quatre entrées se réduisent parce
qu'elles pointent toutes le même code, déjà chiffré.

---

# CE QUE LE LOT NE PRÉTEND PAS

- **Je n'ai pas rejoué les mesures des 408, 409, 411 et 426.** Leurs chiffres —
  25 POST examinés, 8 pages balayées, 27 littéraux confrontés, 17 affirmations
  recensées — sont **les leurs**, cités comme tels. Ce que **ce lot** établit,
  c'est **ce que chacun DIT être** : un bornage ou un recoupement, dans ses
  propres mots.
- **Je ne les retire pas de l'historique.** Ils restent des lots livrés et leurs
  mesures gardent leur valeur — un bornage qui empêche une campagne inutile est
  un résultat. **Je les retire de la liste des dossiers EN ATTENTE DE
  CLASSEMENT**, ce qui est autre chose.
- **Je n'ai pas rouvert le 406/407 lui-même.** Son rang 2 et son chiffrage à
  4 lignes datent du 478 et ne sont pas re-mesurés ici.
- Le volet **456+459** reste dans les six restants : le 456 est déjà au plan
  (rang 2, devisé au 472), mais le volet `symbols_usable` en est **distinct** et
  je ne le tranche pas dans ce lot.
- **Aucun navigateur.** La présence dans les octets servis est établie par `GET`
  via `test_client` ; la non-peinture est établie **par lecture de la garde**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `persist` redirigé vers un `mkdtemp` **et la redirection
  vérifiée par `cache_path()`** ; **aucun moteur appelé, aucun écrivain appelé** ;
  **`/api/portfolio/team`, `/options/<sym>`, `/api/analyst/`,
  `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## LA FEUILLE DE DÉCISION — INCHANGÉE

**20 dossiers · 55 à 63 lignes · 20 gardiens · douze rang 1 · sept rang 2 · un
rang 3.** Les dix lots A à J sont **inchangés**.

```text
dossiers en attente de classement   10 → 6   (388 · 391/396 · 379 · 363 · 386 · 456+459)
rattachés au 406/407                 +4      (408 bornage · 409 bornage · 411 · 426 recoupements)
```

**Dettes ouvertes, inchangées** : huit rangs relatifs non re-vérifiés ; deux
dossiers rangés non chiffrés (422 rang 1, 431 rang 4) ; trois dossiers de
DÉCISION (469, 468, 466/467) ; le candidat « champ capital » (478).

## Où en est la boucle

Quatre-vingt-quatrième lot court, **retour au produit comme le 481 l'exigeait**.

Le lot ne trouve aucun défaut neuf, et **c'est ce qu'il devait faire** : la liste
des dossiers en attente contenait **quatre entrées qui n'en étaient pas**, et
elles y figuraient depuis soixante-dix lots. Quatre rapports sur six d'une même
veine ne cherchaient pas un défaut — **deux le bornaient, deux le reformulaient**
— et tous les quatre le disaient dans leur propre titre.

Le fait de méthode est court et il vaut pour la suite :

**UNE LISTE DE DOSSIERS EN ATTENTE N'EST PAS UNE LISTE DE DÉFAUTS. Elle
accumule des NUMÉROS DE LOT, et un lot peut n'avoir rien trouvé.** Le 408 et le
409 sont d'excellents lots — ils ont empêché de transformer une correction d'un
site en campagne sur soixante. **Les compter comme des dossiers à classer, c'était
confondre le travail et son objet.**

Et une observation qui prolonge celle du 481 sans la répéter : **la règle des deux
contrôles a servi dès son premier emploi**, et elle a servi contre le réveil, pas
contre le produit. Une règle de méthode posée pour se protéger d'une erreur
d'instrument vient d'attraper une erreur de brief. **Je le note sans en tirer de
loi : un seul cas.**

Comptes séparés : résultats faux **arrêtés avant publication** **47** (+1, le
« 426 vit dans `performance_page.py` » du réveil) ; **publiés puis corrigés**
**8** ; **interprétations retirées** **3** ; re-localisation **0** ; incohérences
de rang **0** ; rangs sans justification **0** ; **rangs relatifs non
re-vérifiés 8**.

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre vingt
dossiers, douze de rang 1, pour 55 à 63 lignes, et il est INCHANGÉ.**
