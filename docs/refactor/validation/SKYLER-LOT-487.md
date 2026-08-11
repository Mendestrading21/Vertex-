# SKYLER LOT 487 — La dette du 486 soldée AU NAVIGATEUR : le défaut est CONFIRMÉ à l'écran, le mécanisme fonctionne dès qu'on remplit le champ — et l'atténuation qui maintenait le rang 2 est RÉFUTÉE : l'alerte et la barre ne sont JAMAIS sur la même vue

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-487` (base : lot 486 fusionné,
`ee6563ef`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 486 avait nommé sa dette : « aucune exécution de moteur ce lot … c'est du JS
client … **un rendu navigateur la solderait** ». Le 485 avait prouvé que payer
une dette nommée trouve autre chose. **C'est encore vrai — et cette fois contre
mon propre classement.**

## Le banc

Serveur DEMO, **Chromium préinstallé** lancé par `executable_path`
(`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`) — les navigateurs sur
disque sont en **1194** et Playwright réclamait **1228** ; `playwright install`
**n'a pas été lancé**, conformément à la consigne d'environnement.

**Toute la synchronisation desk coupée au niveau réseau** : `route('**/api/desk**')`
→ `abort()`, en **lecture comme en écriture**. Ni le serveur ni `desk_data.json`
ne sont touchés. Positions semées en `localStorage` **avant hydratation** :
`AAA 4 000 · BBB 3 000 · CCC 3 000` → poids attendus **40 / 30 / 30 %**.

### Deux calibrations, et la première a ÉCHOUÉ

**Premier essai : bloqué le POST seul.** Résultat : l'alerte affichait
« **ACN = 65 %** » — un symbole que je n'avais **pas** semé. La page s'était
hydratée depuis le desk **serveur**, qui avait écrasé ma graine : **le banc ne
mesurait pas mes données.** Je n'ai lu aucun résultat de ce passage.

**Corrigé** en coupant aussi le GET : l'alerte affiche alors
« **AAA = 40 %** », exactement le poids semé. **Calibration passée.**

**Seconde calibration, dans le banc final** : les trois symboles semés doivent
apparaître dans le tableau. `['AAA','BBB','CCC']` — **passée**.

Et une découverte de structure au passage : le tableau des poids **n'est pas sur
la vue par défaut**. `/portfolio` ouvre sur **Synthèse** (0 cellule `Poids`) ; le
tableau vit sur l'onglet **Positions**. Sans ce clic, le banc mesurait une page
qui ne contient tout simplement pas l'objet étudié.

## Ce que l'écran montre — 486-A CONFIRMÉ par exécution

**Onglet Positions, état RÉEL du produit (aucun `entrySnap.score`)** :

```text
titre   poids affiché   couleur de barre   tick 60 %   suffixe « / cap % »   classe warn   Conviction
AAA     40,0 %          positive (verte)   absent      absent                 false         —
BBB     30,0 %          positive (verte)   absent      absent                 false         —
CCC     30,0 %          positive (verte)   absent      absent                 false         —
```

**Une position à 40 % du portefeuille affiche une barre VERTE.** Tout ce que le
486 avait déduit du recensement des octets est vrai à l'écran : pas de tick, pas
de suffixe, pas de classe `vx-warn`. **Le rang passe de « par recensement » à
« par exécution ».**

La colonne Conviction rend « **—** » : c'est le repli **honnête** de `convOf`,
et il tient. Le produit ne ment pas là — il se tait.

## Le second contrôle — un cas que le PRODUIT n'exerce jamais

Même banc, **`entrySnap.score = 30` injecté** (un score qu'aucun site servi
n'écrit) :

```text
AAA     40,0 % / 5 %    negative (rouge)   PRÉSENT     PRÉSENT               true          A · 30
BBB     30,0 % / 5 %    negative (rouge)   PRÉSENT     PRÉSENT               true          A · 30
CCC     30,0 % / 5 %    negative (rouge)   PRÉSENT     PRÉSENT               true          A · 30
```

**Le mécanisme fonctionne parfaitement.** Tick, plafond « / 5 % », rouge, classe
`vx-warn`, palier « A · 30 » : tout s'allume dès que le champ est rempli.

C'est le contrôle qui **discrimine** : il ne confirme pas seulement le symptôme,
il confirme **la cause**. Le code n'est pas cassé — **il attend une donnée que
personne n'écrit**. Si la barre était restée verte ici, mon diagnostic du 486
aurait été faux.

## Ce que le navigateur RÉFUTE — mon propre classement

Le 486 a maintenu 486-A au **rang 2** pour une seule raison, écrite noir sur
blanc : « **une information co-visible existe** — l'alerte de concentration
Top1 > 25 % ». Mesuré :

```text
vue Synthèse (vue par défaut)   alerte « Concentration élevée : AAA = 40 % »  PRÉSENTE
                                cellules « Poids »                            0
vue Positions                   3 barres de poids, toutes vertes
                                « Concentration élevée » dans le texte         ABSENTE
```

**Les deux ne sont jamais à l'écran en même temps.** L'alerte vit sur Synthèse,
la barre sur Positions ; changer d'onglet **remplace** la vue.

Ma « co-visibilité » était une inférence tirée des **octets servis de la page**,
pas du **rendu de la vue**. C'est exactement la leçon que le 486 a lui-même
publiée — *un chemin peut être servi et jamais pris* — **et je l'ai appliquée au
défaut sans l'appliquer à mon atténuation.**

### Le contrepoids, que je donne aussi

L'alerte est sur la **vue par défaut** : un utilisateur qui ouvre `/portfolio`
la voit d'abord. L'information existe dans la session, elle n'est pas absente du
produit. **Cela ne restaure pas le rang 2** : la vue Positions est celle dont le
métier est d'exposer le risque **ligne par ligne**, et sur cette vue, rien —
aucune couleur, aucun plafond, aucun avertissement — ne le signale. Le critère
du 456 parle d'une information **co-visible** ; ici elle ne l'est pas.

**486-A : rang 2 → RANG 1.** Critères absolus : (a) servi et **rendu**, vérifié
au navigateur ; (b) un affichage de risque qui ne peut pas exprimer le risque ;
(c) **aucune information co-visible sur la vue concernée**. Aucune comparaison à
un autre dossier n'entre dans ce rang.

**Publiés puis corrigés : 9 → 10.**

## Le fait de méthode

Le 485 avait posé : *un test appliqué à un objet de l'enquête doit l'être à tous
les objets de même genre*. Ce lot en donne la forme la plus gênante :

**LE TEST D'ACCESSIBILITÉ DOIT ÊTRE APPLIQUÉ À L'ATTÉNUATION AUTANT QU'AU
DÉFAUT.** J'ai vérifié que le défaut était atteignable, et j'ai cru mon
atténuation sur parole parce qu'elle m'arrangeait — elle faisait descendre un
rang. Les 477 et 478 disaient déjà que les atténuations sont ce que la boucle
publie de plus fragile ; il manquait la parade, et c'est la même que pour le
reste : **l'exécuter.**

## Portée

- **L'exclusivité des deux onglets est établie sur DEUX passages** (Synthèse :
  alerte présente, 0 barre · Positions : 3 barres, alerte absente), **pas sur une
  seule session**. Deux tentatives de bascule en une session ont échoué —
  l'une n'a pas changé la vue (0 barre : **mesure écartée, non lue**), l'autre a
  expiré sur le sélecteur. **Je le dis plutôt que de présenter une preuve plus
  propre que ce que j'ai obtenu.**
- Les poids sont **semés**, non réels : le banc établit le **comportement du
  rendu**, pas l'état du portefeuille de l'utilisateur.
- **Un seul viewport (1440 × 1200)**, un seul thème. Pas de mobile.
- **`/api/client-log` : `{"count":0,"errors":[]}`** — zéro erreur client
  côté serveur. La seule erreur console (`net::ERR_FAILED`) est **mon propre
  blocage de `/api/desk`**, pas un défaut du produit ; je ne la compte pas.
- Le défaut **latent** du 486 (`tierOf` lisant un score /100 comme un /40) reste
  latent : le banc l'a contourné en injectant un score **déjà sur /40**. Non
  exercé, non classé.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Serveur DEMO **arrêté** — `pgrep terminal.py` vide, port 5002 en refus de
  connexion, vérifié.
- **Synchronisation desk coupée en lecture ET en écriture** : `desk_data.json`
  n'a pas été sollicité.
- Snapshot runtime **avec copie du contenu** : le contrôle d'**apparition** a
  attrapé **ma propre pollution** — `l487_res.json` écrit à la racine du dépôt
  par un script du banc (`os.chdir` puis chemin relatif). **Supprimé**, puis
  restauration revérifiée : **21 fichiers, aucun apparu, aucun disparu, écart
  final AUCUN.** Le serveur DEMO avait touché `breadth_history.json` et
  `daily_prev.json` — reproduction connue du 391 — **restaurés à l'octet**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quatre lots de suite ont payé une dette nommée par le lot précédent, et **les
quatre ont trouvé autre chose que ce qu'ils venaient chercher** : le 484 dans une
catégorie écartée d'une phrase, le 485 dans un bloc qui marquait « quelque
chose », le 486 dans une jauge sans dénominateur, le 487 **dans sa propre
atténuation**.

Ce dernier est le plus inconfortable, parce qu'il ne corrige pas un instrument :
il corrige un **classement**, c'est-à-dire ce que la boucle propose à l'humain.
Un rang 2 dit « moins urgent » ; il était faux.

Comptes séparés : résultats faux **arrêtés avant publication 52 (+1 — la
première calibration ratée, dont je n'ai lu aucun résultat)** ; **publiés puis
corrigés 10 (+1)** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
