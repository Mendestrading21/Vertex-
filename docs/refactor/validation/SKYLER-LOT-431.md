# SKYLER LOT 431 — `modeOf` ne peut jamais rendre « Live » : le jeton `ibkr` n'existe nulle part dans le vocabulaire qu'il interroge (et j'annule mon propre rang 1)

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-431` (base : lot 430 fusionné,
e62fecb)

Quatorzième lot de la veine, premier après le bilan n°12. Point de contrôle : la
**piste ouverte au 429 et jamais consommée** — les vocabulaires en **minuscules**,
que le balayage précédent avait comptés (44 couples) sans en confronter un seul à
son producteur.

**Aucun code, aucun gardien, aucun test.**

## Le pool, trié par RÔLE et non par forme

Sur le corpus **servi** (95 objets, 3 829 722 octets) :

```text
porteurs comparés à un jeton MINUSCULE       53
couples distincts                           119

  VOCABULAIRES (≥ 2 jetons)                  22 porteurs
  jeton UNIQUE (drapeau, pas un vocabulaire) 31 porteurs
```

Le tri par rôle (leçon 419) sépare d'emblée les 31 drapeaux — `data === 'object'`,
`fn === 'function'`, `net === 'offline'` — des 22 vrais vocabulaires. Parmi ces
22, seuls quelques-uns viennent d'un **producteur serveur** ; les autres sont des
états d'interface fabriqués et consommés dans le même fichier.

## L'alerte la plus prometteuse — et la chaîne l'a levée

`bias` est comparé à **`haussier`**, **`baissier`** *et* **`bearish`** : trois
jetons, deux langues, sur ce qui ressemble au même champ. C'est exactement la
forme du 428.

La remontée dit autre chose. Ce sont **deux champs distincts** :

```text
options-gex.js:139        r.bias === 'haussier'   ← gex_scan.py:45  → haussier|baissier|neutre
options-structure.js:109  d.bias === 'bearish'    ← multileg_lab.py:421 → bullish|bearish|neutral
```

Chaque consommateur interroge le vocabulaire de **son** producteur. **Alerte
levée** — troisième fois que ce motif se présente (426 sur l'IV, 429 sur
`spy_regime`, ici sur `bias`).

*(Au passage : `options_lab_api.py:46-48`, qui dérive ce `bias`, accepte les deux
vocabulaires de `verdict` — `('ACHETER','RENFORCER','BUY')` et
`('ÉVITER','EVITER','ALLÉGER','ALLEGER','AVOID')`. Le dépôt sait le faire.)*

## Ce que j'ai trouvé — et qu'il faut énoncer exactement

`/markets`, dans les octets servis :

```javascript
function modeOf(scan){
  return scan && scan.data_source==='demo' ? 'fallback'
       : (scan && scan.source==='ibkr' ? 'live' : 'delayed');
}
```

Le vocabulaire réellement produit pour ce champ, source de vérité :

```python
# terminal.py:352
scan_state['source'] = ('yfinance' if stooq_n == 0 else
                        'stooq' if yahoo_n == 0 else 'yfinance+stooq')
# terminal.py:373
scan_state['source'] = 'demo'
```

**Quatre valeurs : `yfinance`, `stooq`, `yfinance+stooq`, `demo`. `ibkr` n'en
fait pas partie.** `/healthz` sert le même champ (`system.py:33`,
`'data_source': scan_state.get('source')`), et `/scan` aussi.

### Mesure, en exécutant les octets servis

```text
source produite            mode rendu    pied de carte
'yfinance'                 delayed       « yfinance Différé »
'stooq'                    delayed       « stooq Différé »
'yfinance+stooq'           delayed       « yfinance+stooq Différé »
'demo'                     fallback      « demo Secours »

TÉMOIN POSITIF
'ibkr'  (jamais produit)   live          ← la branche EXISTE et fonctionne
```

Le libellé vient de `vx-core.js`, servi :
`{live:'Live', delayed:'Différé', fallback:'Secours'}[mode]`.

**`modeOf` a trois issues ; une seule est inatteignable, et c'est « Live ».**
`markets_page.py` passe `mode: modeOf(scan)` à **16 cartes**.

## Périmètre : deux autres sites portent la même comparaison, et ils NE SONT PAS SERVIS

C'est le contrôle qui empêche de surestimer :

```text
gnavFresh — badge « 🟢 LIVE IBKR »      (terminal.py:2574, :4100)   AUCUN OCTET SERVI
_srcb     — « 🟢 IBKR live »            (terminal.py:3132)          AUCUN OCTET SERVI
modeOf    — 16 cartes                   (/markets)                  SERVI
```

Les deux premiers vivent dans les constantes `PAGE_*` mortes du dossier 374.
**Un seul site sert réellement.**

## J'annule mon propre rang 1

Ma première lecture était : « 16 cartes ne peuvent jamais dire Live ». C'est
exact. Mais la question qui décide du rang est : **le libellé rendu est-il
FAUX ?**

Non. `scan_state['source']` décrit la provenance des **séries de cours** du scan,
et celles-ci viennent réellement de yfinance ou de stooq. Écrire « yfinance
Différé » est **honnête et correct**.

Il reste deux choses, plus petites que ce que je croyais :

**(a) Une branche morte.** `scan.source === 'ibkr'` ne peut jamais être vraie :
une des trois issues de `modeOf` est inatteignable. **Rang 4** — piège latent,
aucune conséquence à l'écran aujourd'hui.

**(b) Une sous-estimation, pas un mensonge.** Quand IBKR est connecté,
`_apply_ibkr_indices()` (`terminal.py:2241-2249`) **écrase en place** les prix des
indices de `scan_state['indices']` par les valeurs temps réel et marque chaque
entrée `src = 'ibkr'`. Le bandeau d'indices et le graphique comparé de `/markets`
lisent ces entrées — donc des valeurs **temps réel** — pendant que le pied de
carte annonce « Différé ». L'étiquette est **conservatrice** : elle annonce moins
frais que la réalité. Ce n'est pas une violation de l'invariant d'honnêteté, qui
interdit d'annoncer mieux que ce qu'on a.

**Et c'est un recoupement**, pas une trouvaille neuve : le lot 386 avait déjà
mesuré que le marqueur `src = 'ibkr'` n'atteint aucune surface servie. Mécanisme
différent — 386 : un champ jamais lu ; ici : un champ lu, comparé au mauvais
niveau (`scan.source` au lieu de `scan.indices_live.source`, écrit juste à côté
en `terminal.py:2257`). **Même dossier, deuxième porte.**

## Verdict du lot

**Négatif au sens du produit.** Une comparaison qui ne peut jamais être vraie,
sur un site servi, mais dont l'effet est un libellé **conservateur** et non
mensonger. **Rang 4**, versant recoupement du dossier 386 (rang 1, déjà ouvert).

Aucun gardien ne mentionne `modeOf`. **Aucun GO, rien n'est engagé.**

## Portée

Un seul porteur ouvert sur les 22 vocabulaires minuscules recensés ; **21 restent
non confrontés**, dont `s` (5 jetons d'état de veille), `key`, `ib`, `status`,
`dest`, `state`. Les 15 porteurs lus par **table `{…}[champ]`** — la seconde
piste du 429 — ne sont **toujours pas** ouverts.

Je n'ai **pas observé** IBKR connecté : le scan est vide au démarrage et aucun
payload persisté ne porte d'`indices`. La sous-estimation du point (b) est établie
**par la lecture de la chaîne** (l'overlay écrase les prix en place, les cartes
lisent ces entrées), **pas constatée à l'écran**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **MD5 des 8 pages REMESURÉS** — l'inférence devient une mesure :
  `/` fc15688d1af6 · `/markets` c0bb91c6971a · `/opportunities` 6a22a6abbd03 ·
  `/analysis` 113827718e99 · `/portfolio` f1b41b665d4a · `/options` 6387210de785 ·
  `/journal` 243699ace2d5 · `/system` 73e917c0f2d0 → **8/8 identiques aux
  références des lots 390/396**. Ce n'est plus une inférence.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-quatrième lot court. Séquence : **425 ✓ · 426 ✗ · 427 ✓ · 428 ✓ · 429 ✗ ·
430 bilan · 431 ~**.

Ce lot est la contrepartie exacte du 428 : même forme — un jeton comparé à un
vocabulaire qui ne le contient pas —, mais **la conséquence ne franchit pas la
barre de l'écran**. Le 428 rendait un calcul faux et l'affichait avec sa clé de
lecture ; le 431 rend une étiquette **trop prudente**. La forme ne suffit pas à
faire un défaut : c'est la conséquence affichée qui décide, et il faut savoir
descendre son propre diagnostic quand elle ne suit pas.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
