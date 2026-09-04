"""vertex/ai/chiffres.py — UN CHIFFRE ABSENT DU PACKET NE SORT PAS.

`CLAUDE.md`, interdit absolu n°1 pour l'IA :

> inventer prix/prime/Greek/probabilité/source

## Le défaut, mesuré le 26 août 2026

Le prompt système interdit à l'IA de **calculer**. `response_validator` interdit
le langage de certitude, les clés d'ordre et les tentatives de recalcul de
score. **Rien** n'empêchait le modèle d'**énoncer** un chiffre qui n'existe pas
dans le packet.

Mesure, sur un packet réel `{price: 309.90, score: 82, plan: {stop: 290.0,
tp1: 330.0}}` et une réponse qui invente tout :

```text
"AAPL cote 412,50 $ et affiche un P/E de 19,4. Objectif 480 $."
"La probabilite de hausse est de 87 %, avec un delta de 0,73."

validate_analysis -> valide ? True     erreurs : AUCUNE
```

Un prix, un P/E, un objectif, une probabilité et un Greek — **cinq chiffres
inventés**, tous acceptés. Une règle que rien n'applique est une intention.

## Ce qui compte comme « chiffre » et ce qui reste de la prose

Exiger que **tout** nombre figure dans le packet rendrait le garde-fou
inutilisable : « les **3** scénarios », « **2** contradictions », « d'ici
**2027** » sont de la prose, pas des données. Un garde-fou qui refuse la prose
est désactivé au premier usage — D-088, payé deux fois.

Un nombre doit donc être **sourcé** quand il se présente comme une donnée :

- il porte une **unité** (`$`, `%`, `€`, `pts`) ; ou
- il a une **partie décimale** (`0,73`, `19,4`) ; ou
- il dépasse 31 — au-delà, ce n'est plus un compte ni un quantième.

Tout le reste est traité comme du texte.

## Ce qui compte comme « présent dans le packet »

Un arrondi d'affichage n'est pas une invention : le packet porte `309.90`,
écrire « 310 $ » est fidèle. Un nombre est donc sourcé s'il correspond à une
valeur du packet **exactement**, **à un arrondi près** (0 à 4 décimales), à
**0,5 % près**, ou **à un facteur 100 près** — parce qu'un même taux s'écrit
`0.0226` dans le packet et « 2,26 % » dans une phrase, et refuser cette lecture
reviendrait à interdire d'exprimer un pourcentage.

## Ce que ce module ne fait pas

Il ne vérifie pas que la phrase est **vraie**, seulement que ses chiffres
viennent du packet. Un modèle peut citer le bon prix dans une phrase fausse ;
cela reste hors de portée d'un contrôle automatique, et le dire évite de faire
passer ce garde-fou pour une garantie de véracité.
"""
from __future__ import annotations

import math
import re

#: Un nombre écrit à la française ou à l'anglaise, avec séparateurs éventuels :
#: `412,50`  `1 234.56`  `19.4`  `87`
_NOMBRE = re.compile(r'(?<![\w.,])(\d{1,3}(?:[   ]\d{3})+|\d+)(?:[.,](\d+))?')

#: Unités qui font d'un nombre une DONNÉE et non de la prose.
_UNITES = ('$', '%', '€', 'usd', 'eur', 'pts', 'pt')

#: Au-delà, un entier n'est plus un compte ni un quantième.
PLAFOND_PROSE = 31

#: Tolérance relative d'arrondi d'affichage.
TOLERANCE = 0.005

#: Années plausibles dans une thèse — jamais des données de marché.
ANNEE_MIN, ANNEE_MAX = 1900, 2100


def _valeur(entier: str, decimale: str | None):
    brut = entier.replace(' ', '').replace(' ', '')
    try:
        return float(brut + ('.' + decimale if decimale else ''))
    except ValueError:
        return None


def _signe(texte: str, debut: int) -> float:
    """`-1.0` si le nombre porte un vrai signe negatif, `1.0` sinon.

    Le signe n'est PAS capte par l'expression reguliere, et c'est delibere :
    dans « 290-330 » le tiret separe deux bornes, il ne rend pas la seconde
    negative. On ne le lit comme un signe que si le caractere qui le precede
    n'est pas un chiffre.

    Sans cette lecture, `-2,23` etait vu comme `2,23` — et **tout theta**, qui
    est toujours negatif, aurait ete accuse d'invention.
    """
    if debut == 0 or texte[debut - 1] != '-':
        return 1.0
    avant = texte[:debut - 1].rstrip()
    if avant and avant[-1].isdigit():
        return 1.0
    return -1.0


def nombres_du_packet(packet) -> set:
    """Toutes les valeurs numériques atteignables dans le packet.

    Le parcours est récursif et **ne se limite pas aux champs connus** : un
    garde-fou qui n'inspecterait que `price` et `score` accuserait le modèle
    d'inventer une valeur qui figure ailleurs dans le dossier.
    """
    vus = set()

    def _voir(o, prof=0):
        if prof > 12:
            return
        if isinstance(o, bool):
            return
        if isinstance(o, (int, float)):
            #  Pas de `try/except pass` : `o` est deja un int ou un float, et
            #  un `except` muet ici serait du bruit defensif que le gardien
            #  `test_pass_et_contexte` compte a juste titre. Ce qu'il
            #  faut ecarter, c'est l'infini et le NaN — un `inf` dans le packet
            #  sourcerait n'importe quel chiffre par la tolerance relative.
            f = float(o)
            if math.isfinite(f):
                vus.add(f)
            return
        if isinstance(o, str):
            for m in _NOMBRE.finditer(o):
                v = _valeur(m.group(1), m.group(2))
                if v is not None:
                    vus.add(v)
            return
        if isinstance(o, dict):
            for cle, val in o.items():
                _voir(cle, prof + 1)
                _voir(val, prof + 1)
            return
        if isinstance(o, (list, tuple, set)):
            for val in o:
                _voir(val, prof + 1)

    _voir(packet)
    return vus


def _est_donnee(texte: str, debut: int, fin: int, valeur: float,
                decimale: str | None) -> bool:
    """Ce nombre se présente-t-il comme une DONNÉE, ou comme de la prose ?"""
    if decimale:
        return True
    if valeur > PLAFOND_PROSE:
        #  Une annee reste de la prose : « d'ici 2027 » n'est pas un prix.
        if float(valeur).is_integer() and ANNEE_MIN <= valeur <= ANNEE_MAX:
            return False
        return True
    apres = texte[fin:fin + 6].lower().lstrip()
    return apres.startswith(_UNITES)


def _est_sourcee(valeur: float, connues: set) -> bool:
    """Cette valeur correspond-elle à une valeur du packet ?"""
    for p in connues:
        if p == valeur:
            return True
        for k in range(0, 5):
            if round(p, k) == valeur:
                return True
        base = max(abs(p), 1e-9)
        if abs(valeur - p) / base <= TOLERANCE:
            return True
        #  `0.0226` dans le packet, « 2,26 % » dans la phrase — et l'inverse.
        for facteur in (100.0, 0.01):
            mis = p * facteur
            if mis == valeur or abs(valeur - mis) / max(abs(mis), 1e-9) <= TOLERANCE:
                return True
            for k in range(0, 5):
                if round(mis, k) == valeur:
                    return True
    return False


def non_sourcees(texte: str, packet, connues: set | None = None) -> list:
    """Les chiffres du texte **absents** du packet, dans l'ordre d'apparition.

    Liste vide = rien d'inventé. Chaque entrée porte la valeur et son extrait,
    pour qu'un rejet soit lisible et non un simple « invalide ».
    """
    texte = str(texte or '')
    connues = nombres_du_packet(packet) if connues is None else connues
    trouves = []
    for m in _NOMBRE.finditer(texte):
        v = _valeur(m.group(1), m.group(2))
        if v is None:
            continue
        v *= _signe(texte, m.start())
        if not _est_donnee(texte, m.start(), m.end(), abs(v), m.group(2)):
            continue
        if _est_sourcee(v, connues):
            continue
        deb = max(0, m.start() - 20)
        trouves.append({'valeur': v,
                        'extrait': texte[deb:m.end() + 12].strip()})
    return trouves
