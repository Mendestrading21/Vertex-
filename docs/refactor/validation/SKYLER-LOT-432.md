# SKYLER LOT 432 — « Aucune décision urgente — laisser courir les thèses intactes », dit la carte, alors que le moteur vient de classer chaque position « Données insuffisantes »

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-432` (base : lot 431 fusionné,
73fab63)

Quinzième lot de la veine. Point de contrôle : la **seconde piste ouverte au 429
et jamais consommée** — la lecture par **table `{…}[champ]`**. La question posée
par la consigne était la bonne : *une table a un repli implicite ; est-il HONNÊTE
ou invente-t-il ?*

**Aucun code, aucun gardien, aucun test.**

## Le pool — 19 lectures par table, appariées, pas devinées

Sur le corpus **servi** (95 objets, 3 829 722 octets), appariement d'accolades
**et** de crochets — pas d'heuristique de proximité (leçon 415) :

```text
lectures par TABLE distinctes (table, clé)   19
   cartes d'échappement HTML ({'<':'&lt;'…})   4   → clé bornée, repli inatteignable
   internes Chart.js (chart.umd.min.js)        2   → hors périmètre
   tables PRODUIT                             13
```

Les treize tables produit, classées par ce que leur repli **fait** :

```text
repli HONNÊTE (avoue l'ignorance)                                   9
   d.bias      → '—'                             options-intel.js
   _ib         → ['IBKR état inconnu', …]        /system
   state       → ['offline', …] / 'muted'        /system · vx-core.js
   mode        → ''                              vx-core.js
   n.impact    → 'vx-dim'                        /system
   t           → 'vx-muted'                      /portfolio
   pr          → 'var(--vx-text-muted)'          /portfolio
   st2.status  → 'frozen'  ·  v.status → 'frozen' /system   (prudent)
repli SANS OBJET (clé bornée par construction)                      3
repli qui RANGE L'INCONNU AVEC LE SAIN                              1   ← celui-ci
```

**Douze sur treize sont honnêtes.** Le treizième mérite le lot.

## La table qui range l'inconnu avec le sain

`/portfolio`, octets servis :

```javascript
function priorityAction(rich){
  const scored = rich.map(t => { const st = thesisState(t);
    const rank = {cassee:3, fragilisee:2, surveiller:0,
                  insuffisant:0, intacte:0, renforcee:0}[st.key] || 0;
    return {t, st, rank}; }).filter(x => x.rank > 0).sort((a,b) => b.rank - a.rank);
  …
  return {sym:null, label:'Aucune décision urgente — laisser courir les thèses intactes', tone:'muted'};
}
```

**Le repli `|| 0` est inatteignable** — `thesisState` produit exactement six clés
et la table les liste toutes six. Mesuré, et c'est important : **le défaut n'est
pas une clé manquante, c'est la VALEUR donnée à `insuffisant`.**

`insuffisant: 0`, puis `.filter(x => x.rank > 0)` : une position dont l'état est
**« Données insuffisantes » n'est pas classée bas — elle est retirée du tri.**

## Mesure — en exécutant les octets servis

`thesisState`, `priorityAction`, `nextAction`, `winnerRule` et
`hasPositiveConfirmation` extraits du marquage servi de `/portfolio` et exécutés
sous Node 22 :

```text
cas                                          états de thèse                    action prioritaire RENDUE
témoin positif — 1 thèse cassée              cassee                            AAA — Réévaluer la sortie —
                                                                               invalidation atteinte
4 positions SANS marque (IBKR hors ligne)    insuffisant ×4                    « Aucune décision urgente —
                                                                                 laisser courir les thèses INTACTES »
3 sans marque + 1 réellement intacte         insuffisant ×3 · intacte          idem
```

Le témoin positif prouve que la carte sait remonter une position en danger. Le
cas mesuré prouve qu'en l'absence de marque, **elle affirme que les thèses sont
intactes alors qu'aucune n'a pu être évaluée.**

## La règle est écrite trois lignes plus haut

`portfolio_page.py:130`, docstring de `thesisState` :

> *« Sans marque → « données insuffisantes » (**jamais un verdict**). »*

La couche d'état **tient** cette règle : elle rend bien `insuffisant`. La couche
d'action **la casse**, et prononce précisément le verdict que le docstring
interdit — en le nommant : *« laisser courir les thèses **intactes** »*.

C'est le motif de la veine, huitième instance : *la règle que le fichier respecte
ailleurs*. Et c'est la parente directe du lot 424 (`INTACT` à confiance 0.0) —
mais cette fois **du côté affiché**.

## Atteignable, et pas au bord

`enrich()` (`portfolio_page.py:93-101`) construit `mark` depuis `quotes[t.id]`,
et le producteur de `quotes` est :

```javascript
try { … await fetch('/api/pos-quotes', …) … } catch(e) { return {}; }
```

**Un échec du fetch rend un objet vide : aucune position n'a de marque.** IBKR
hors ligne, serveur injoignable, réseau coupé — trois chemins ordinaires vers
l'état mesuré. Ce n'est pas un cas construit.

## Prouvé affiché

La carte est rendue dans le marquage servi de `/portfolio` :

```html
<div class="vx-insight vx-col-6" data-tone="action">
  <span class="vx-kpi-label">Action prioritaire</span>
  <div class="…">${act.sym ? '<span class="vx-ticker">'+esc(act.sym)+'</span> — ' : ''}${esc(act.label)}</div>
```

`act.label` est **la chaîne rendue**, sans condition.

## Classement

**Rang 1**, famille des 422/425/428 : aucune valeur n'est inventée — les états de
thèse sont corrects un par un. C'est la **synthèse** qui est fausse, et elle est
fausse dans le sens le plus coûteux pour un trader : elle **rassure** quand elle
devrait dire qu'elle ne sait pas. Un portefeuille dont aucune cotation n'arrive
affiche « aucune décision urgente ».

Correction pressentie, minuscule : compter les `insuffisant` avant le repli et,
s'il y en a, rendre un libellé qui l'avoue (« n positions non évaluables — marques
indisponibles ») au lieu de « thèses intactes ». Le vocabulaire existe déjà dans
le fichier. **Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne mentionne `priorityAction` ni la chaîne « Aucune décision
urgente » : **aucun gardien.**

## Portée

Treize tables produit ouvertes sur les 19 lectures recensées ; les quatre cartes
d'échappement et les deux internes Chart.js sont **écartées par rôle**, pas
vérifiées. Le recensement ne couvre que la forme `{…}[clé]` : un `switch`/`case`
ou une table nommée déclarée ailleurs puis indexée lui échappe toujours.

Je n'ai **pas observé** un portefeuille réel sans cotations : la mesure exécute le
code servi sur des positions fabriquées. Le chemin d'entrée (`catch → {}`) est
établi par lecture, pas constaté en fonctionnement.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396
  (la remesure coûte deux secondes dans la sonde de corpus — reconduite).
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-cinquième lot court. Séquence : **427 ✓ · 428 ✓ · 429 ✗ · 430 bilan ·
431 ~ · 432 ✓**.

Le 431 avait annulé son propre rang 1 parce que l'étiquette fautive était
**conservatrice**. Celui-ci est l'exact inverse : la synthèse penche du côté
**rassurant**, et c'est ce sens-là qui coûte. La même forme — un inconnu rangé
avec un connu — donne un non-défaut dans un cas et un rang 1 dans l'autre. **Le
sens de l'erreur décide du rang.**

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
