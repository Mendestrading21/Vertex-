# SIGNAL OS · LOT 33 — L'ÉNUMÉRATION DES SORTIES N'EST PLUS MANUELLE

Branche : `agent/vertex-signal-os-v1` · SW **v233 inchangé** (aucun octet servi
modifié) · Suite **3168 → 3171 passed**

Réserve n°1 du lot 32, écrite en toutes lettres : « l'énumération reste
manuelle ». Le gardien du lot 177 nomme trois sorties de news ; le lot 32 en a
trouvé une quatrième — **par accident**, en cherchant pourquoi une mutation ne
mordait pas. Un gardien qui liste des noms ne verra jamais la sortie qu'on
ajoutera demain.

Ce lot renverse la charge de la preuve : on empoisonne les états partagés et on
interroge **toutes** les routes GET. Plus rien à tenir à jour.

---

## 1. Le résultat

| | |
| --- | --- |
| routes GET interrogées | **155** |
| routes servies (réponse obtenue) | **≥ 100** (plancher du gardien ; 160 à la mesure hors exclusions) |
| routes servant du balisage externe vivant | **0** |
| durée dans la suite | **3,85 s** |

Aucune cinquième sortie. Ce n'est pas « rien » : c'est la première fois que la
règle n°5 est vérifiée **par énumération** et non par confiance dans une liste.

---

## 2. Trois défauts de mon instrument, tous mesurés en le cassant

### 2.1 La coupure réseau ne coupait pas — et des requêtes sont sorties

Première version : `socket.socket` remplacé. Le balayage a lancé de vraies
requêtes vers Yahoo (refusées 403 par le proxy, donc aucune donnée récupérée).
`yfinance` passe par `curl_cffi`, donc par libcurl, qui ouvre ses sockets **en
C** : aucun patch Python ne l'arrête.

Coupure corrigée sur deux étages — `socket.socket.connect` (la MÉTHODE : `ssl`
dérive de la classe, remplacer le symbole casse l'import de `yfinance`) et les
variables de proxy pointées sur un port mort local. Surtout : elle est
**prouvée** par un vrai client HTTP avant tout balayage, et l'outil **refuse de
tourner** si la preuve échoue.

> Un garde-fou qu'on n'a pas éprouvé n'est pas un garde-fou. C'est la leçon du
> lot 31, appliquée cette fois à mon propre outil.

### 2.2 J'ai appelé les points interdits

Le balayage énumère tout — il a donc appelé `/api/ticker/<sym>`, `/desc/…`,
`/api/analyst/…`. Le réseau était coupé et prouvé, donc rien n'est sorti ; mais
la consigne ne portait pas sur le réseau, elle portait sur **l'appel**. Ces
préfixes sont désormais exclus par nom (`HORS_LIMITES`), *en plus* de la
coupure. Leur cas est raisonné à la lecture du code, pas mesuré — et c'est dit.

### 2.3 Une route « résistait à l'interruption » — mauvaise hypothèse

J'ai d'abord conclu à un `except:` nu quelque part dans le produit. Faux.
`/api/live/events` est un **flux SSE** : sa réponse ne se termine jamais par
conception, et un `client.get()` ordinaire la consomme indéfiniment. La lecture
est maintenant **bornée** (`buffered=False` + plafond d'octets), ce qui permet
d'inspecter ce qu'un flux sert sans attendre sa fin.

Et un dernier, de ma main : le gardien armait le minuteur **sans installer le
gestionnaire** — l'action par défaut de `SIGALRM` termine le processus. La suite
sortait en 142 (128+14), et un `| tail` dans mon shell masquait le code derrière
un exit 0 trompeur.

---

## 3. Ce que le balayage a d'abord accusé, et pourquoi c'était faux

`/scan` et `/api/ticker/<sym>` ressortaient la charge brute. Vérifié **avant
d'accuser** : ces deux routes servent `scan_state['detail'][sym]['news']`, un
store qui a **un seul écrivain** en production — la boucle de scan de
`terminal.py` — et qui assainit AVANT de déposer. L'état que mon sondage
fabriquait (news brutes dans `detail`) n'existe pas.

**Mais la vérification a trouvé autre chose.** Puisque `detail['news']` est déjà
assaini, `/api/events/<sym>` et `/api/skyler/<sym>`, qui rassainissent à la
sortie, servent un texte **doublement échappé** :

```
titre réel      AT&T relève : Barron's y croit
après ingestion AT&amp;T relève : Barron&#39;s y croit
servi par /api/events  AT&amp;amp;T … Barron&amp;#39;s
```

Aucun consommateur ne rend ces titres aujourd'hui — je ne qualifierai donc
**pas** cela de défaut visible, et je n'ai rien changé au comportement : retirer
la seconde passe réduirait la protection sans bénéfice observable. Le fait est
**ancré par un test** dont le message d'échec dit quoi faire le jour où un rendu
apparaît : choisir un domicile, au lieu d'en découvrir deux.

---

## 4. Ce que le lot livre

| fichier | rôle |
| --- | --- |
| `tools/mesurer_sorties_news.py` | l'instrument : coupure prouvée, worker IBKR neutralisé par identité d'objet, lecture bornée, journal reprenable |
| `tests/test_signal_os_enumeration_sorties_lot33.py` | le gardien : témoin, ancre, balayage |

Le worker IBKR est neutralisé **par identité d'objet**, pas par liste de
modules — sinon je reproduirais exactement le défaut que ce lot corrige. Mesuré :
une seule liaison est atteignable ainsi, `desk.py` recevant `opt_job` en
**paramètre de fabrique** (variable de fermeture, hors de portée).

Aucun moteur, aucune règle métier, aucun octet servi touché — **pas de bump SW**.

---

## 5. L'anti-vacuité

Un balayage qui n'atteint rien passe tout. Deux garde-fous :

1. **Un témoin** — `/news-feed` doit montrer la charge **neutralisée**
   (`alert(1)` présent, `<script>` absent). S'il ne la montre pas, le poison
   n'est pas arrivé et le balayage ne prouve rien.
2. **Un plancher** — au moins 100 routes réellement servies. Une route
   injoignable est comptée à part, jamais comme propre.

---

## 6. Réserves honnêtes

1. Les six préfixes hors limites ne sont pas mesurés. `/api/ticker/<sym>` sert
   le même store que `/scan` par le même chemin ; c'est un raisonnement de
   lecture, pas une mesure.
2. Les routes à **plusieurs** paramètres sont écartées : on ne sait pas les
   remplir honnêtement, et deviner produirait des 404 qui ne prouvent rien.
3. Le balayage est **GET seul**. Une sortie POST qui renverrait du texte externe
   ne serait pas vue — écarté délibérément, l'invariant READONLY interdit de
   balayer des POST à l'aveugle.
4. Les marqueurs sont quatre motifs distinctifs. Une sortie qui transformerait
   la charge en un balisage *différent* mais toujours actif passerait.
