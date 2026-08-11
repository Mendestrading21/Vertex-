# SKYLER LOT 399 — Qui, dans la suite, sort sur Internet ?

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-399` (base : lot 398 fusionné,
ad9d23b)

Le lot 398 avait neutralisé **deux** sorties réseau au passage, sans savoir s'il
en restait. Ce lot mesure la question au lieu de la supposer.

## L'instrument — et sa validation avant emploi

Un plugin pytest à **deux capteurs** :

1. un **faux proxy local** : `HTTPS_PROXY`/`HTTP_PROXY` pointent dessus pendant
   toute la session, donc **tout** `CONNECT` y atterrit — y compris ceux de
   libcurl/`curl_cffi` (le transport de yfinance), qu'un simple patch de
   `socket` **ne verrait pas** ;
2. un patch de `socket.socket.connect` pour les connexions directes sans proxy.

Aucun blocage : le faux proxy répond `502` et ferme — la sortie échoue comme elle
échouerait hors ligne, le verdict des tests n'est pas modifié.

**Témoin positif obligatoire avant de conclure quoi que ce soit** — trois tests
jetables :

```text
test_positif_yfinance    → CONNECT fc.yahoo.com:443    CAPTÉ (curl_cffi)
test_positif_requests    → CONNECT example.com:443     CAPTÉ (requests)
test_negatif_aucun_reseau→ (rien)                      muet — correct
```

L'instrument voit les deux transports et attribue au bon test. *Sans ce contrôle,
un « 0 sortie » n'aurait rien valu.*

## La mesure — 3 sorties sur 2 864 tests

```text
sortie                              attribuée à
en.wikipedia.org:443   HTTP/1.0     <session>  ← à l'IMPORT, avant le 1er test
fc.yahoo.com:443       HTTP/1.1     test_obsidian_theme.py::test_company_twin_never_invents
fc.yahoo.com:443       HTTP/1.1     test_refus_variable_lot392.py::…description_inventee
```

Dispersion des durées : le test le plus lent de la suite est à **1,52 s**, aucun
au-delà. Aucune attente réseau longue **dans cet environnement** — mais c'est
précisément parce que le proxy échoue vite ; sur une machine connectée, ces trois
sorties aboutissent.

## Ce que chacune coûte réellement

### 1. Wikipedia, à l'import — comportement de PRODUIT

`vertex/data/universe.py` L16 appelle `get_index_members()` **au niveau module** ;
sans cache frais, `vertex/data/constituents.py` va chercher les trois listes
d'indices sur Wikipedia (`_TIMEOUT = 15` s **par requête**) puis écrit
`constituents_cache.json` à la racine.

C'est **voulu et documenté** pour l'application (« le demarrage n'est JAMAIS
bloque », repli sur snapshot statique). Mais cela s'applique aussi à `pytest` :
sur une machine connectée, **chaque lancement de la suite** fait ces requêtes,
avec jusqu'à 45 s d'attente si Wikipedia traîne, et crée un **23ᵉ fichier
runtime**. Vérifié : `constituents_cache.json` est bien couvert par `*_cache.json`
dans `.gitignore` — **aucun risque de commit**. Je ne touche pas à la production
de ma propre initiative : **classé en dossier** (rang 4).

### 2. `test_company_twin_never_invents` — sortie inutile, retirée

`company_twin()` appelle `_company._fetch_profile()`, qui interroge yfinance. Or
le profil **n'entre dans aucune des assertions** du test (elles portent sur
`fundamentals`, `scan` et `missing`). La sortie ne rendait le test que lent et
dépendant de la connexion. Neutralisée par `monkeypatch` — hors ligne le fetch
échouait déjà, le verdict est **identique**. Aucune écriture disque en jeu.

### 3. `/desc` — le test écrivait dans le dépôt de l'utilisateur

C'est la vraie trouvaille, et elle vient d'un test que **j'ai écrit moi-même au
lot 392**.

`terminal.py` L1983 : quand le fetch yfinance **réussit**, `/desc/<sym>` écrit
`desc_cache.json` **à la racine du dépôt**. Le test
`test_un_symbole_inconnu_ne_recoit_pas_une_description_inventee` appelle cette
route à chaque exécution de la suite.

Le défaut était **doublement invisible** :

- ici, le réseau échoue → aucune écriture, rien à voir ;
- au **recensement du lot 389** (« quels tests écrivent des données runtime ? »),
  parce que l'écriture est **conditionnée à la réussite du fetch** — un
  recensement statique des sites d'écriture ne pouvait pas la relier à ce test.

*Une écriture conditionnelle au réseau échappe à un recensement fait hors ligne.*

**Preuve directe, sans réseau** — `yf.Ticker` remplacé par un faux qui réussit :

```text
desc_cache.json à la racine AVANT           : False
(1) sans isolation → écriture à la racine   : True   ← créé par la sonde, supprimé ensuite
(2) avec l'isolation du lot 399 → dans tmp  : True   | racine touchée : False
```

**Corrigé** : `_DESC_PATH` et `_desc_cache` sont isolés par `monkeypatch` dans ce
seul test. **La route reste la vraie** — seule sa destination change. La sortie
réseau, elle, est **conservée délibérément** : ce test existe pour vérifier qu'une
réponse yfinance réelle sur un symbole inexistant ne remplit aucun champ ; la
supprimer réduirait le test à sa branche hors ligne.

## Après correction

```text
sorties réseau     3 → 2
écritures dans le dépôt depuis la suite    1 → 0
```

Il reste : Wikipedia à l'import (produit, dossier) et le `/desc` du lot 392
(volontaire, sans effet disque).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — deux fichiers de test modifiés. Pas de
  preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition. La passe
  ré-horodate `desk_data.json` / `ai_enrichment.json` / `weekly_snapshot.json`
  (contenu identique) ; restaurés. Le `desc_cache.json` créé par la sonde a été
  supprimé par la sonde elle-même. Écart final **aucun**, aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**, inchangée — aucun test ajouté, et c'est
  délibéré.

## Portée

Le détecteur voit ce qui **tente de sortir pendant la suite**. Il ne dit rien des
sorties qu'un chemin non couvert par un test ferait en production, ni de ce
qu'une machine connectée déclencherait en aval d'une réponse réussie. Et « 3 »
n'est un chiffre honnête que parce que le témoin positif a prouvé que
l'instrument voit — sans lui, ce serait un zéro décoratif.

## Où en est la boucle

Cinq lots courts, cinq points de contrôle distincts : pistes fines (395), octets
servis (396), registre (397), tests inertes (398), sorties réseau (399). Les deux
derniers ont trouvé du code, pas de la documentation périmée.

La matière utile reste **décisionnelle** — purge des 7 points MSFT (388) et scan
de démo dans `breadth_history` (391).

Prochaine échéance : **bilan n°9 au lot 400**.
