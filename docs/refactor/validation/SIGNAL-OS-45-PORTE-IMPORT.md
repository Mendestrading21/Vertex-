# SIGNAL OS · LOT 45 — LA PORTE PAR LAQUELLE DU TEXTE ARBITRAIRE ENTRE

Branche : `agent/vertex-signal-os-v1` · SW **v235** (aucun octet servi touché)

Réserve nommée deux fois — `SIGNAL-OS-40` §5 et `SIGNAL-OS-42` §4.3 :
`POST /api/skyler/memory/import` est **le seul chemin** par lequel un texte que
le produit n'a pas calculé entre dans la mémoire décisionnelle. Le balayage des
sorties est GET seul — l'invariant READONLY interdit de tirer des POST à
l'aveugle — donc cette porte n'était pas mesurée.

---

## 1. Ce que l'empreinte protège, et ce qu'elle ne protège pas

Le gestionnaire vérifie un `content_sha256` **avant** toute écriture : une
archive altérée est refusée, rien n'est touché. C'est de l'**intégrité**, pas de
la **provenance** — qui fabrique le bundle calcule aussi son empreinte.

Le contenu reste donc arbitraire par construction, et **c'est normal** : un
import est une restauration, pas un canal de confiance. La question utile n'est
pas « peut-on stocker du balisage ? » — on le peut, et l'interdire casserait la
restauration. Elle est : **que font les sorties de ce qui a été stocké ?**

---

## 2. Comment ce lot entre, sans tirer un POST

Par la porte du moteur : `decision_memory.merge_memory`, l'appel exact que le
gestionnaire fait une fois l'empreinte validée. Même discipline qu'au lot 40 —
on emprunte la porte du produit, on n'écrit pas un magasin à la main avec une
forme devinée, et l'invariant READONLY n'est pas frôlé.

Un record est déposé avec un champ libre piégé (`thesis`), puis les deux sorties
sont interrogées.

---

## 3. Le verdict, deux sorties, deux contrats

| sortie | ce qu'elle fait du texte importé | verdict |
| --- | --- | --- |
| `/memory/<decision_id>` (HTML) | **échappe** — `&lt;script&gt;` | sûr |
| `/api/skyler/memory/<decision_id>` (JSON) | rend le champ **tel quel** | acceptable **aujourd'hui** |

Le second n'est pas une fuite : **aucun consommateur d'interface ne le peint** —
mesuré en cherchant l'appel dans tout `vertex/ui/**`, et non supposé. Le seul
usage voisin est `/api/skyler/memory/export`, un téléchargement.

Le gardien ancre les deux faits ensemble. Le jour où un rendu de cette API
apparaîtra, le test tombera et il faudra **choisir un domicile** pour
l'échappement — au lieu d'en découvrir deux, comme le lot 33 l'a mesuré pour le
double échappement des news.

---

## 4. Le gardien

`tests/test_signal_os_porte_import_lot45.py` — 3 tests.

Le premier n'est pas décoratif : il vérifie que le record est **bien stocké**.
Sans lui, les deux suivants pourraient passer parce que rien n'est entré — un
vert qui ne prouve rien.

Vérifié par mutation : retirer l'échappement de la valeur dans `_row` de la vue
post-mortem fait tomber le test du rendu HTML.

---

## 5. Ce qui reste ouvert

1. **Le POST lui-même n'est toujours pas tiré.** Ce lot mesure ce que la porte
   dépose et ce que les sorties en font ; il ne mesure pas la validation
   d'empreinte en conditions réelles de requête.
2. **Les autres magasins du bundle** — séances (`session_log`) et journal de
   calibration (`skyler_journal`) — sont fusionnés par le même gestionnaire et
   ne sont pas couverts ici. Leur cas est le même *en raisonnement*, pas encore
   *en mesure*.
