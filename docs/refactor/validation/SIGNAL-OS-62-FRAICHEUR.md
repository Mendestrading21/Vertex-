# SIGNAL OS · LOT 62 — UN CHIFFRE VRAI HIER, AFFICHÉ SANS LE DIRE

Branche : `agent/vertex-signal-os-v1` · SW **v242 → v243** (octets servis modifiés
sur `/`) · Suite **3 498 passed** (3 492 → +6)

Réserve SIGNAL-OS-61 §6.2, de ma main :

> **La fraîcheur n'est pas jugée.** Un nombre présent dans une réponse **périmée**
> paraît tracé. La moitié « périmée » de la réserve du lot 60 reste donc ouverte —
> seule la moitié « inventée » est traitée.

C'est la moitié la plus sournoise des deux. Un chiffre inventé est faux tout de
suite et le lot 61 sait le dénoncer. Un chiffre **périmé** a été vrai, il reste
plausible, et **rien à l'écran ne le distingue d'un chiffre frais**. *Un chiffre
vrai hier, affiché sans dire qu'il date d'hier, est un mensonge par omission.*

---

## 1. L'expérience : un AVANT/APRÈS, jamais une seule photo

`tools/mesurer_fraicheur_dite.py` charge chaque espace **deux fois** :

1. **nominal** — la réponse passe telle quelle ;
2. **vieilli** — les réponses sont interceptées en vol et leurs champs d'âge
   (`age_s`, `scan_age`, `ts`) réécrits pour placer la donnée à **7 200 s**,
   bien au-delà de tous les seuils.

Une seule photo ne prouverait rien. Voir « Analyse » ne dit pas si l'étiquette
**réagit** ; voir « À actualiser » ne dit pas si elle réagit **à la bonne chose**.
Seul l'écart entre les deux passages est une mesure.

Trois refus de conclure bornent l'instrument : aucune étiquette en nominal, une
page **déjà** `stale` en nominal (l'expérience ne peut plus distinguer un
basculement), et **aucune réponse effectivement vieillie** — « rien ne change »
ne prouve rien si on n'a rien changé.

---

## 2. Le défaut, sur la page où l'on décide le plus vite

`vertex/ui/pages/briefing.py` — Aujourd'hui, la page d'accueil :

```js
const m = b.demo ? 'demo' : 'delayed';
```

**Une constante.** L'étiquette de fraîcheur affichait « Différé » que la donnée
ait trois minutes ou trois jours. Les branches `live` et `stale: ['frozen',
'Périmé']` de `freshBadge` étaient **inatteignables** sur cette page — du code
mort qui donnait l'apparence d'un indicateur vivant.

Ce n'est pas un badge absent : c'est un badge qui **occupe la place** d'un
indicateur de fraîcheur sans porter la moindre information d'âge. L'utilisateur
qui ouvre Aujourd'hui et lit « Différé » croit lire un état mesuré. Il lit une
chaîne littérale.

### Le correctif

L'âge honnête existait déjà : `scan_age` (ancienneté de la **donnée**, pas de
l'entrée de cache), servi par `/api/market/summary` que la page charge par
ailleurs — `VX.fetch` le rend depuis son cache, **sans appel réseau de plus**.

```js
let m=b.demo?'demo':'delayed';
if(!b.demo){
  try{
    const s=await VX.fetch('/api/market/summary',{ttl:60000});
    const ageMs=(typeof s.scan_age==='number')?s.scan_age*1000:null;
    const T=(window.VX&&VX.freshness&&VX.freshness.THRESH)||{live:20000,snapshot:1800000};
    if(ageMs!=null)m=ageMs<T.live?'live':(ageMs<T.snapshot?'delayed':'stale');
  }catch(e){}
}
```

**Les seuils sont empruntés, jamais recopiés.** Deux tables de seuils divergent
au premier ajustement, et l'écran dirait alors « Différé » là où Marchés dit
« À actualiser » — sur la même donnée. Le repli littéral n'existe que pour le cas
où `VX.freshness` n'est pas encore chargé ; il vaut les mêmes valeurs.

### Vérifié au navigateur, branche non-démo forcée

```text
scan_age=10    → {'etat': 'live',    'texte': 'Live'}
scan_age=600   → {'etat': 'delayed', 'texte': 'Différé'}
scan_age=7200  → {'etat': 'frozen',  'texte': 'Périmé'}
```

Les trois états sont désormais atteignables. C'est la mesure qui le dit, pas la
lecture du code.

---

## 3. Ce que mon premier verdict accusait à tort

L'instrument rendait d'abord un verdict **binaire** (DIT / MUET) et accusait
**cinq pages sur huit**. Trois de ces cinq ne mentaient pas. Je me suis corrigé
trois fois, et les trois corrections portent la même leçon.

**3.1 — Le mode démonstration court-circuite l'évaluation.** `if(demo){…DÉMO…}`
sort avant tout calcul de fraîcheur : la page annonce « DÉMO », ce qui est
**honnête**, et le chemin que je mesure n'est simplement pas exercé. Ce n'est pas
un défaut, c'est **non observable** dans cet environnement.

**3.2 — Un mot n'est pas son sens.** Sur Système, un `data-state="live"` porte la
classe `vx-freshness` et le texte « **Système opérationnel** ». Il décrit l'état
de la **connexion**, pas l'âge de la donnée. L'accuser de mentir sur la fraîcheur
aurait été confondre un mot avec son sens.

**3.3 — Il existe DEUX grammaires de fraîcheur, pas une.** Mesuré, pas supposé :

| grammaire | émise par | vocabulaire |
| --- | --- | --- |
| `.vx-fresh-chip[data-state]` | `VX.freshness.chip()` | `live` · `snapshot` · `stale` · `saved` · `error` · `offline` |
| `.vx-freshness[data-live]` | `freshBadge()` | `live` · `delayed` · **`frozen`** (« Périmé ») · `demo` · `fallback` |

N'en connaître qu'une faisait rendre « sans vocabulaire » sur une page qui en a
bien un. L'outil connaît maintenant l'équivalence `frozen` = `stale`.

Le verdict est donc à **quatre** valeurs — **DIT** / **MUET** / *non observable
(démo)* / *sans vocabulaire* — et seul `MUET` remonte comme un défaut :

```python
pire = max(pire, code if code == 1 else 0)
```

*Confondre un mot avec son sens aurait accusé des pages honnêtes.* C'est la
troisième fois de la série qu'un instrument accuse le produit d'une faute qui
était la mienne (lot 53, lot 60, lot 62) — et la troisième fois que la correction
vaut plus que la trouvaille.

---

## 4. Le gardien et ses quatre mutations

`tests/test_signal_os_fraicheur_lot62.py` (6 tests).

| mutation | attendu | résultat |
| --- | --- | --- |
| **M1** — la constante `const m = b.demo ? 'demo' : 'delayed'` restaurée | tombe | **tombe** ✅ |
| **M2** — l'emprunt à `VX.freshness.THRESH` remplacé par des seuils recopiés | tombe | **PASSAIT** ❌ → corrigé |
| **M3** — la seconde grammaire (`.vx-freshness[data-live]`) oubliée dans l'outil | tombe | **tombe** ✅ |
| **M4** — la visite nominale supprimée (il ne reste qu'une photo) | tombe | **tombe** ✅ |

**M2 était creux — sixième gardien creux de la série, toujours le même
mécanisme : une sous-chaîne qui existe ailleurs.** Ma première version cherchait
`VX.freshness.THRESH` ; cette chaîne apparaît **aussi dans le commentaire que
j'avais écrit juste au-dessus du code**. Supprimer l'emprunt réel laissait donc
le test vert. Retargeté sur l'expression exacte
`(window.VX&&VX.freshness&&VX.freshness.THRESH)||`, la mutation rejouée échoue
correctement et le fichier intact passe 6/6.

La liste des six, pour mémoire : `'available'inc` (voisin), le double
`querySelector`, `'loadCredibilite()'` (sous-chaîne de sa propre définition), un
emoji lu d'une charge vide, `+contextes(d)` (présence vs site d'appel), et
celui-ci. **Un gardien qui n'a pas été muté n'est pas un gardien.**

---

## 5. Service worker

`v242 → v243` : les octets servis sur `/` ont changé. Les cinq épinglages de
version dans les tests et `_SW_VERSION` de
`tests/test_sw_cache_scope_lot361.py` suivent. `_EMPREINTE` **inchangée** —
aucun fichier sous `/static` n'a été touché.

---

## 6. Réserves

1. **Options n'a aucun vocabulaire de fraîcheur.** Verdict *sans vocabulaire* :
   ce n'est pas un mensonge, c'est une absence — mais rien ne dit à
   l'utilisateur de quand datent des primes d'options, qui vieillissent vite.
   C'est la réserve la plus intéressante que ce lot ouvre.
2. **Le mode démonstration masque le chemin sur plusieurs espaces.** Ce que je
   mesure, je le mesure hors démo ou pas du tout. La validation en conditions
   réelles (IBKR, marché ouvert) reste à faire par l'utilisateur.
3. **Trois champs d'âge seulement** (`age_s`, `scan_age`, `ts`). Une réponse qui
   daterait sa donnée autrement échapperait au vieillissement.
4. **Le seuil `saved` / `error` / `offline` n'est pas exercé** : l'expérience ne
   couvre que l'axe de l'âge, pas celui de la panne (traité aux lots 59–60).
5. **Un seul titre (`ACN`), une seule largeur.**
