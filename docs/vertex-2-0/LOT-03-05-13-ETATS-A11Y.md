# Lots 3, 5 et 13 — Point focal, états honnêtes, accessibilité

## Lot 5 — Aujourd'hui a un point focal

La page ouvrait sur **douze tuiles d'indices de poids rigoureusement égal**. Douze
choses également importantes, c'est zéro hiérarchie : rien ne dit par où commencer.
Le titre disait `Dashboard`, dans un produit intégralement francophone.

Le premier écran porte désormais une **DecisionTrace** —
`Donnée → Moteur → Décision → Portefeuille` — et la page s'appelle **Aujourd'hui**.

Elle ne calcule rien : chaque nœud lit `scan_state`, déjà produit par les moteurs.
Dans l'état dégradé de cet environnement elle rend, honnêtement :

| Nœud | Valeur | Ton |
|---|---|---|
| Donnée | Aucune source — *aucun scan servi* | rouge |
| Moteur | Régime indéterminé — *aucun signal de marché* | ambre |
| Décision | Comité sans verdict — *aucun dossier évalué* | gris |
| Portefeuille | Aucune position — *rien à exposer* | gris |

Le nœud Portefeuille est complété **côté client** : le serveur ne connaît pas les
positions déclarées à cet endroit, il ne suppose donc rien.

### Un bug attrapé sur la capture

La première version injectait l'identifiant du nœud Portefeuille par un
**remplacement de chaîne** visant « le premier nœud sans donnée ». Quand Décision et
Portefeuille étaient tous deux sans donnée, l'identifiant atterrissait sur le
mauvais nœud — et le client écrivait le compte des positions **dans la case
Décision**. Visible sur la capture, invisible à la relecture.

Corrigé à la racine : `vx2.decision_trace()` accepte désormais un `ident` **par
nœud**. La classe entière de ce défaut disparaît.

## Lot 3 — Aucun rectangle vide

Un outil mesure ce que la doctrine interdit : `tools/vertex_2_0_etats_vides.py`.
Il cherche, dans l'application réelle, les conteneurs visibles de taille non
négligeable sans texte, sans graphique et sans contrôle.

Deux faux positifs ont dû être écartés — et c'est ce qui rend l'outil utilisable :

- le contenu d'un `<details>` **replié** garde une boîte de mise en page dans
  Chromium alors que `innerText` rend `''`. Ce n'est pas un bloc vide, c'est un bloc
  fermé. Sept blocs de `/system` étaient signalés à tort ;
- un conteneur **transparent sans bordure** ne se voit pas : c'est de l'espace, pas
  un rectangle.

### Le vrai défaut trouvé

`/performance` portait **deux squelettes perpétuels**. `loadDiscipline()` avait été
retirée — elle était appelée et définie nulle part, et faisait échouer toute la vue
— mais ses deux conteneurs sont restés avec leur squelette. La page promettait donc
une donnée qui n'arriverait **jamais**. Un chargement qui ne se résout pas est un
mensonge tranquille.

Remplacés par un état honnête : « Verdict de discipline — calcul non disponible dans
Vertex », avec sa cause, et « Prochain axe de travail — non produit ».

**Résultat : 0 bloc vide sur 13 routes.**

## Lot 13 — Accessibilité et responsive, mesurés

`tools/vertex_2_0_a11y.py` mesure sur l'application réelle : débordement horizontal
à 8 largeurs, boutons sans nom accessible, images sans alternative, champs sans
étiquette reliée, lien d'évitement, et **contraste du texte réellement rendu**.

Le calcul de contraste résout le fond en **remontant les ancêtres** jusqu'à une
couche opaque, en composant les alphas. Sur des surfaces en verre, lire
`backgroundColor` sur l'élément lui-même rendrait « transparent » et la mesure
serait fausse — c'est-à-dire toujours verte.

### Ce que la mesure a trouvé

**Deux jetons de texte échouaient à AA.** Sur la surface la plus claire du produit
(`#20252f`), qui est le cas le pire :

| Jeton | Avant | Ratio avant | Après | Ratio après |
|---|---|---:|---|---:|
| `--vx-smoke` | `#7a828f` | **3,96:1** | `#9aa1ad` | 5,91:1 |
| `--vx-text-faint` | `#5f6672` | **2,66:1** | `#8f96a2` | 5,16:1 |

Les méta-textes de 10,5 px étaient lisibles pour qui a une bonne vue, et illisibles
pour les autres. La hiérarchie ne repose donc plus sur la seule luminosité : elle
vient aussi du poids et de la taille, comme la doctrine le demande.

**Un bouton sans nom accessible.** `vx-add-btn` porte son libellé « Ajouter » dans
un `<span class="vx-hide-mobile">` : sous 430 px, un lecteur d'écran annonçait
« bouton », rien de plus. `aria-label` ajouté.

**Trois faux positifs sur `/system`** venaient de la même cause que les blocs vides :
des boutons libellés vivant dans un `<details>` fermé. Corrigé **dans la mesure**,
pas dans la page — le défaut était dans l'outil.

### Résultat

```
Débordement horizontal   390 · 430 · 768 · 1024 · 1280 · 1440 · 1600 · 1920   →  0 px partout
Audit 1440×1000          12 pages  →  0 défaut
Audit  390×844           12 pages  →  0 défaut
```

## Un piège d'outillage, noté pour la suite

Le gardien d'empreinte `/static` a échoué alors que la valeur enregistrée était
correcte : un `.pyc` périmé dans `tests/__pycache__` servait l'ancienne constante.
`find tests -name __pycache__ -exec rm -rf {} +` avant de conclure qu'un gardien
d'empreinte ment.

Ce même gardien avait auparavant attrapé une **vraie** erreur : le commit du lot 2
portait une empreinte périmée, parce que j'avais édité `simulator.js` après l'avoir
enregistrée. Il fait exactement son travail.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4246 passés**, 154 ignorés, 1 échec environnemental connu |
| Blocs vides | **0** sur 13 routes — `preuves/etats-vides.json` |
| Accessibilité | **0 défaut** sur 12 pages × 2 viewports — `preuves/a11y.json` |
| Débordement horizontal | **0 px** sur 8 largeurs × 12 pages |
| Console navigateur | 0 erreur page sur les 12 routes |
| Captures | `preuves/lot-05-apres/`, `preuves/lot-13-apres/` |

Service worker `v221` → **`v222`** (coque servie + jetons de contraste), six
gardiens de version et empreinte `/static` mis à jour dans le même commit.

## Limites déclarées

- Le contraste est mesuré sur le texte **réellement rendu à ce moment**. Un texte
  qui n'apparaît qu'après une interaction (drawer, modale, ligne survolée) n'est pas
  couvert par cette passe.
- Le piégeage du focus dans les drawers n'est pas encore mesuré automatiquement :
  l'outil prévoit l'emplacement, la vérification reste manuelle à ce stade.
