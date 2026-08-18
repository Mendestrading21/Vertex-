# SIGNAL OS · LOT 60 — LA PANNE PARTIELLE, ET UNE MATRICE QUI DISAIT « OK » SANS RIEN PROUVER

Branche : `agent/vertex-signal-os-v1` · SW **v242, inchangé** (aucun octet servi
touché) · Suite **3 486 passed** (3 481 → +5)

Réserve SIGNAL-OS-59 §5.2, de ma main : *« Coupure totale seulement. Une panne
partielle — une source sur cinq en échec — reste le cas le plus fréquent en
vrai, et n'est pas mesurée. »*

Une coupure totale est presque confortable : tout échoue, tout le monde le voit.
La panne partielle est plus traître — la page reçoit quatre réponses sur cinq,
elle a de quoi remplir la plupart de ses cases, et **rien ne la force à signaler
celle qui manque**.

---

## 1. Le résultat, et la seule façon honnête de le compter

`--couper-une <famille>` coupe une seule famille de routes. Familles **relevées**
du trafic réel des huit espaces, pas supposées.

| famille coupée | espaces réellement mesurés | verdict |
| --- | --- | --- |
| `market` | 8 | sain |
| `desk` (sync des données perso) | 8 | sain |
| `live` | 8 | sain |
| `session` | 8 | sain |
| `skyler` | 4 | sain |
| `options` | 2 | sain |
| `scan` | 2 | sain |

**40 cellules réellement mesurées, toutes saines.** Les autres sont « hors
portée » — la page n'appelle pas cette famille — et ce mot compte : sans lui,
j'aurais annoncé « 56/56 OK » dont seize cellules ne prouvaient rien.

Exemple de ce que le mode voit quand il mord : sous panne `market`, `/markets`
affiche « **Régime indisponible · Réessayer · Ouvrir Système** » sur l'hôte
concerné, pendant que les deux autres se remplissent normalement. C'est
exactement le comportement voulu — la panne est **localisée et nommée**.

---

## 2. Trois fautes, et la deuxième rendait la mesure entièrement creuse

**2.1 La coupure sortait du périmètre des données.** `**/*market*` attrapait
aussi l'URL de la page `/markets` : le document recevait un 500, rien ne se
chargeait, et le témoin rendait « AVEUGLE ». Il avait raison — je mesurais un
navigateur privé de page, pas un produit qui dégrade.

**2.2 Trois familles sur six ne coupaient RIEN — et rendaient « 8/8 OK ».**
`portfolio`, `tracking`, `news` : aucune requête interceptée sur aucun des huit
espaces. Quarante-huit cellules vertes dont vingt-quatre ne prouvaient
strictement rien. Et l'en-tête de l'outil affirmait déjà que les familles sont
« tirées des routes réellement servies » — **elle mentait** : je les passais à la
main. `--familles` les relève désormais du trafic réel.

C'est la faute qui revient sous tous les visages depuis le lot 35 : *j'ai écrit
ce que je croyais, là où il fallait mesurer.*

**2.3 « Hors portée » n'existait pas.** Une page qui n'appelle pas une famille
n'est ni saine ni aveugle. Les confondre trompe dans les deux sens : un « OK »
qui ne prouve rien, ou une alarme sur une page qui n'a rien à voir. Le verdict
existe maintenant, et il n'empoisonne pas le résultat d'ensemble.

---

## 3. Ce que ce mode ne peut PAS voir — et pourquoi je l'écris ici

L'outil détecte les hôtes qui **n'aboutissent pas**. Il ne sait pas reconnaître
un hôte qui aboutit avec une valeur **inventée** ou **périmée** à la place de la
donnée manquante. Un chiffre plausible affiché sans source lui paraîtra sain.

C'est une limite de méthode, pas un réglage — et c'est précisément le défaut que
la panne partielle rend le **plus probable**, puisque la page a de quoi remplir
presque toutes ses cases. Un « 40/40 » qui tairait cela se lirait comme une
garantie qu'il n'est pas. Un test tient cette phrase dans l'en-tête de l'outil,
là où on lit le résultat.

---

## 4. Le gardien, et ses quatre mutations

| mutation | test qui tombe |
| --- | --- |
| la coupure ressort du périmètre (le bug d'origine) | le périmètre |
| le témoin du mode partiel retiré | l'anti-vacuité |
| « hors portée » compte de nouveau comme un défaut | les trois verdicts |
| la limite de méthode effacée de l'en-tête | l'aveu écrit |

La quatrième est inhabituelle et assumée : elle garde une **phrase**, pas un
comportement. Ce que l'outil avoue ignorer fait partie de ce qu'il mesure.

---

## 5. Réserves

1. **Sept familles sur seize.** Le relevé en propose seize ; les neuf autres
   (`events`, `status`, `summary`, `digest`, `manifest`, `regime`, `pos-quotes`,
   `cal-feed`, `tradingview`) ne sont pas balayées. Chacune est un passage de
   plus, pas un travail d'une autre nature.
2. **Une seule famille à la fois.** Deux sources simultanément en panne
   pourraient produire un état qu'aucune coupure isolée n'atteint.
3. **La valeur inventée reste hors de portée** (§3). La détecter demanderait de
   comparer chaque chiffre affiché à sa source — un instrument d'une autre
   nature, et de loin le plus utile qui manque encore.
4. **Une seule largeur** (1440 px) et le mode démonstration.
