# SKYLER LOT 377 — Le gardien du lot 376 n'en voyait qu'un tiers

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-377` (base : lot 376 fusionné,
2900973)

## Piste calibrée

Prolongement direct du lot 376, qui verrouillait le contrat de refus honnête sur
`return {…'available': False…}` **littéral** — 13 cas, tous motivés. Un refus
signalé autrement échappait à tout. Consigne : **mesurer chaque convention avant
de décider laquelle est décidable.**

## Mesure — volume par convention (1321 fonctions)

```text
return None                242     ← absence de valeur ordinaire, PAS un refus
return []                   28     ← « rien trouvé » sur une liste : honnête
return {}                   13
return {available: False}   13     ← seuls cas vus par le lot 376
return {ok: False}           4
```

`return None` domine très largement, mais ce n'est **pas** une convention de
refus : c'est le retour normal d'un utilitaire sans valeur à donner. La question
n'y est pas décidable, et je ne prétends pas la trancher.

## Le vrai défaut : le PÉRIMÈTRE du gardien précédent

Mon premier détecteur ne regardait que `return <Dict>`. Or la majorité des refus
d'API sont **enveloppés** : `return jsonify({...})`, souvent
`return jsonify({...}), 400`. Le nœud est alors un `Call` ou un `Tuple`, jamais
un `Dict` — ils étaient **tous** invisibles.

```text
refus vus par le détecteur naïf (lot 376) : 13
refus réels, enveloppes déballées         : 39
                                            → couverture du lot 376 : 33 %
```

Les 26 manquants sont précisément **les plus exposés** : les refus servis en JSON
au navigateur, ceux que l'interface montre à l'utilisateur. **12ᵉ fois de la
boucle que le périmètre de l'outil ment**, et la première où c'est un gardien
**déjà fusionné** qui se révèle myope.

C'est un défaut d'un genre particulier : le code était sain, le gardien passait
au vert, et le vert ne voulait pas dire ce qu'on croyait. **Un gardien myope est
plus dangereux qu'une absence de gardien, puisqu'il rassure.**

## Le résultat, périmètre corrigé

**39 refus, 39 motivés, 0 muet.** Vérifié sur les réponses réellement servies :

```text
/api/copilot/ask   HTTP 200  {'ok': False}  error='question vide'
/api/desk/restore  HTTP 400  {'ok': False}  err='nom invalide'
```

Note honnête sur un cas voisin : `/api/skyler/<sym>` répond 200 **sans clé
d'état** pour un symbole inconnu. Vérification faite avant de crier : il sert une
décision complète avec un `audit_trail` énumérant ce qui manquait (`anomaly:
false`, `fundamentals: false`…). C'est la forme honnête sous un autre habillage —
**la traçabilité est le motif**. Pas un refus muet.

## La discipline des contrats à deux visages, mesurée

Une fonction qui renvoie un dict riche dans une branche et un `{}` ou `None` nu
dans une autre offre à l'appelant un refus muet **déguisé en valeur** :
`r.get('reason')` rend `None` sans dire pourquoi.

```text
fonctions à dict riche seul   : 190
fonctions à retour nu seul    : 134
fonctions MIXTES              :  37
  dont l'une porte une clé d'état :  0
```

Le dénominateur est réel — 37 fonctions mixtes existent — donc le zéro l'est
aussi. Quand une fonction s'engage sur un contrat d'état, elle ne retombe jamais
sur un retour nu.

**Verdict : sain, rien touché.** Ce que ce lot corrige, c'est la **couverture**.

## Gardien

`tests/test_refus_api_lot377.py` (9 tests) :

- **périmètre** nommément vérifié (`desk.py`, `analysis_api.py`, `copilot.py`) ;
- **anti-vide** : ≥ 30 refus trouvés ;
- **la leçon verrouillée** : le déballage doit voir **strictement plus** que le
  détecteur naïf, avec un écart d'au moins 10 — si l'écart tombe, c'est que le
  gardien est redevenu myope, pas que le code a changé ;
- **la propriété** : aucun refus muet, message d'échec expliquant *pourquoi*
  c'est grave ;
- **sur réponses servies** : 2 refus réels, motif d'au moins 8 caractères ;
- **contrats à deux visages**, avec son propre dénominateur (≥ 10 fonctions
  mixtes à examiner) ;
- **pas trop strict** : ≥ 3 familles de motifs employées, sinon la tolérance est
  sans objet et doit être resserrée.

### Preuve ROUGE

```text
ROUGE OK  refus d'API rendu MUET                               | restauration identique
ROUGE OK  motif du refus servi vidé en chaîne vide             | restauration identique
ROUGE OK  déballage jsonify retiré (myopie du lot 376 rejouée) | restauration identique
ROUGE OK  contrat à deux visages introduit                     | restauration identique
ROUGE OK  refus servi qui cesse de refuser                     | restauration identique
après restauration : 9 passed
VERDICT : gardien mordant sur les 5 cas
```

Le troisième cas est le plus significatif : il rejoue **la myopie elle-même** en
retirant le déballage du gardien. Sans lui, rien n'empêcherait quelqu'un de
« simplifier » `_deballe` et de retomber à 33 % de couverture, au vert.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 376, 2900973) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2712 → 2721 passed / 2 skipped** — verte (+9).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Le déballage suit `jsonify(...)`, `dict(...)` et les tuples `(charge, code)`. Un
refus construit dans une variable puis renvoyé, ou passé par un helper maison,
reste invisible — je n'ai pas mesuré combien il en existe. Les 242 `return None`
ne sont **pas** tranchés : la mesure dit qu'ils ne sont pas décidables comme
refus, pas qu'ils sont tous honnêtes. Les exceptions comme convention de refus
n'ont pas été examinées du tout. Enfin, comme au lot 376 : un motif présent n'est
pas un motif **exact** — ce lot vérifie qu'on parle, pas qu'on dit vrai.

## Suite

LOT 378 : veille active. Pistes ouvertes — (a) **les exceptions comme convention
de refus**, jamais examinées ; (b) les refus construits en variable puis renvoyés
(angle mort déclaré ci-dessus) ; (c) les trois sites de concaténation à
constantes du lot 374 ; (d) les formes imbriquées des promesses de retour
(lot 375). Prochaine échéance périodique : **~lot 380** (bilan de la tranche
370-379, désormais tout proche).
