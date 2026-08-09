# SKYLER LOT 439 — Les trois pages jamais ouvertes : `/journal` est exemplaire, `/options` cache ses affirmations dans son JS, `/analysis` n'en a aucune — et six instruments ont été jetés pour l'établir

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-439` (base : lot 438 fusionné,
9532c39)

Vingt-deuxième lot de la veine, **dernier de la tranche**. Le 438 avait refermé
la veine des contrats de champ ; le vivier désignait une lacune plus large :
**`/journal`, `/analysis` et `/options` n'ont jamais été ouvertes** par la méthode
« partir de l'écran ».

**Aucun code, aucun gardien, aucun test.**

## Ce que les trois pages disent quand elles n'ont rien à dire

Phrases rassurantes littérales, mesurées sur les octets servis :

```text
/journal    7 phrases   TOUTES honnêtes — chacune NOMME l'entrée manquante
            « Aucun trade réel déclaré avec résultat — le journal est la seule source de cette section. »
            « Aucune erreur déclarée — renseigne le champ « erreur » à chaque sortie perdante. »
            « Aucune leçon consignée — renseigne le champ « leçon » à chaque sortie de trade. »
            « Aucune hypothèse journalisée — chaque décision est une thèse à vérifier. »
            …
/analysis   1 phrase
/options    0 phrase
```

**`/journal` est le meilleur exemple du dépôt sur ce point.** Aucune de ses sept
phrases ne prétend qu'une mesure a eu lieu ; chacune dit **quelle donnée
utilisateur manque et comment la fournir**. C'est exactement la garde qui manquait
à `/portfolio` (432, 433) et à `renderAnomalies` (434). Le contre-exemple n'est
plus seulement sur `/system` — il est ici, et il est meilleur.

## Les affirmations rendues, page par page

```text
                    HTML de page    JS de page (/static)    TOTAL
/journal                       8            —                   8   dont 2 porteuses d'un chiffre
/analysis                      0            0                   0
/options                       0           35                  35
```

Deux faits mesurés :

**`/options` ne cache rien — mes premiers comptages, si.** Ses 35 affirmations
(`question`, `limits`, `conclusion`, `confirm`, `invalidate`) vivent dans
`options-intel.js`, `options-gex.js`, `options-structure.js` et
`options-scanner.js`, pas dans le HTML de la page. Un compteur qui ne regarde que
le marquage rend « 0 » et se trompe.

**`/analysis` n'a aucune affirmation, nulle part.** Ni dans son HTML, ni dans un
JS de page — **elle n'en charge aucun**. Mesuré : **22 248 octets** servis (la
plus petite des huit, contre 39 673 à 844 315 pour les autres), **0 `<canvas>`,
0 mention de `VXCharts`, 0 vue `?view=`**, 17 coques `vx-card`, 5 411 octets de
script inline, un seul appel réseau cité — `/api/names`.

Je **ne conclus pas** qu'elle n'affiche jamais de graphique : elle est
manifestement pilotée à la demande (un titre s'ouvre depuis
`data-open-analysis`). Ce qui est mesuré, c'est qu'**au chargement elle ne porte
ni moteur de graphique ni contrat d'explication**, là où les sept autres pages en
portent.

## Une confirmation, pas une trouvaille

L'une des deux affirmations chiffrées de `/journal` est
« **moyenne réelle des verdicts résolus (n≥5)** — mesure, pas une promesse ».
C'est le **dossier 417**, dont la légende « (n≥5) » avait été mesurée fausse. Le
417 est donc **confirmé servi sur `/journal`**. Je le note comme recoupement ; le
point de contrôle est consommé et je ne le rejoue pas.

## Six instruments, six contrôles — et une mesure abandonnée

Je voulais aussi mesurer, page par page, si le **contrat de carte** (question /
limites / source) est tenu. Je n'y suis pas arrivé, et le chemin vaut d'être
écrit :

```text
v1  compteur `VXCharts.card(` + plafond `len(opts)>6000`   → /opportunities : 0 carte
      CONTRÔLE : le comptage LITTÉRAL en trouve 7. Le plafond écartait
      silencieusement les cartes à `render:` long.
v2  plafond levé                                            → /options : 0 carte
      CONTRÔLE : le JS de page servi depuis /static n'était pas rattaché à la page.
v3  scripts rattachés                                       → /options : toujours 0
      CONTRÔLE : `options-intel.js` appelle `VC.card(...)` — un ALIAS local.
      « Compter les appels sans les ENVELOPPES rate l'usage » : 4ᵉ récidive (409, 413, 414).
v4  alias détectés (C, VC, cc, cc2, G)                      → / et /analysis : 1 carte à 0 %
      CONTRÔLE : cette carte est rendue PAR UN BUILDER (`catalystRunway`), qui reçoit
      `question:` de son APPELANT — le contrat est à un autre niveau que le compteur.
```

**La métrique elle-même est mal définie** : une carte rendue à travers un builder
porte son contrat au point d'appel du builder, pas dans les options de
`VXCharts.card`. Je n'ai pas de compteur qui sache attribuer les deux, et je
**n'annonce donc aucun taux de couverture**.

C'est le quatrième contrôle « invraisemblance » de la boucle (414, 437, 438, ici),
et il a mordu quatre fois sur quatre.

## Classement

**Aucun défaut nouveau.** Le lot rend trois faits mesurés — `/journal`
exemplaire, `/options` documenté dans son JS, `/analysis` sans contrat au
chargement — et **un aveu** : la couverture du contrat de carte n'est pas
mesurable avec les instruments dont je dispose.

Le seul point qui mériterait un examen ultérieur est `/analysis`, **et il est
trop peu établi pour entrer dans les dossiers**. Je le laisse comme piste, pas
comme constat.

## Portée

Le recensement ne couvre que les **littéraux entre guillemets simples**, de 10 à
200 caractères, dans huit familles de champs — les phrases construites
dynamiquement lui échappent toujours, et c'est la même zone d'ombre que depuis le
427.

Je n'ai **ouvert aucune affirmation** de `/options` : les 35 sont **recensées, non
vérifiées**. Sur `/journal`, une des deux affirmations chiffrées est déjà un
dossier connu, l'autre (« Masse des pertes concentrée entre 0 et −10 % ») est une
**consigne de lecture**, pas un compte vérifiable.

`/analysis` n'a pas été ouverte avec un symbole : la mesure porte sur la page
**au chargement**, pas sur un titre analysé.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad — l'incident du 435 s'est reproduit
  une fois et a été corrigé sur-le-champ.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Quarante-deuxième lot court, **dernier de la tranche 430-439**.

La tranche se termine sur un lot qui ne trouve rien et qui **dit pourquoi**. Le
compte des instruments fautifs atteint **quatorze en six lots** (430, 434 ×2,
435, 437 ×3, 438 ×3, 439 ×4). Tous arrêtés avant publication, par les mêmes trois
contrôles — témoin positif, invraisemblance, lecture de la sortie brute.

C'est la statistique la plus utile de la tranche, et le bilan n°13 devra la
regarder en face : **la boucle passe désormais plus d'effort à vérifier ses
instruments qu'à mesurer le produit.**

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
