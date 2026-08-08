# SKYLER LOT 382 — L'invariant couleur annoncé était plus large que ce qu'on garde

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-382` (base : lot 381 fusionné,
946b81b)

## Piste

Seconde passe d'audit des gardiens par mutation. Le lot 381 avait trouvé un trou
sur la règle critique n°1 en sept sondages ; le rendement justifiait de
continuer. Protocole **durci** après les trois mutations fautives du 381 : ancre
unique obligatoire, mutation vérifiée effective, code muté vérifié **servi**, et
suite complète à chaque cas.

## Résultat de la passe

```text
sanitize_news retiré de /news-feed (sortie servie)         MORD
sanitize_news retiré de la construction des événements     MORD
profondeur de rotation des sauvegardes ramenée à 0         MORD
fichier vertex/static modifié SANS bump d'empreinte        MORD
littéral de couleur #ff00ff dans le shell servi            AUCUN GARDIEN ⚠
[témoin] commentaire anodin                                 ne mord pas — correct
```

J'ai ajouté un **témoin négatif** : une modification anodine qui ne doit *pas*
faire tomber la suite. Il se comporte comme attendu, ce qui donne du poids aux
quatre « MORD » — une suite qui tombe sur n'importe quoi ne prouverait rien.

Les protections lourdes tiennent : les deux sorties news assainies, la chaîne de
sauvegarde desk, et l'empreinte SW ↔ actifs (modifier `tokens.css` sans bumper
échoue bien).

## Le trou n'est PAS une myopie — c'est un écart doc / gardien

Tentation immédiate : accuser `test_no_blue_in_ui_pages` de ne pas couvrir le
shell. Vérification par mutation ciblée, avant d'accuser :

```text
#1e6fd9 (bleu non-marque)   MORD
#ff00ff (magenta)           AUCUN
#c0392b (rouge brique)      AUCUN
```

Le gardien balaie bien `vertex/ui/**/*.py`, shell compris, et fait **exactement
ce que son nom annonce** : aucun bleu non-marque. Ce n'est pas lui qui ment.

C'est `CLAUDE.md` qui annonçait « tokens/VXChartTheme uniquement (**aucun
littéral couleur**) » — un invariant bien plus large que ce que quoi que ce soit
n'a jamais imposé.

## La mesure qui tranche

```text
littéraux #RRGGBB distincts dans vertex/ui/**       : 265
dont réellement présents dans une page SERVIE       :  53
```

Répartis sur une dizaine de modules (`options_intel_page` 10, `analysis_page` 9,
`system_page` 8, `opportunities_page` 7, `portfolio_page` 5…). « Aucun littéral
couleur » est donc **faux depuis longtemps** : il y en a 53 dans les octets
servis aujourd'hui. Exiger zéro casserait la suite sans rien améliorer.

**Verdict : le code respecte la règle réelle. C'est l'énoncé qui était faux, et
le contrat qui n'était verrouillé nulle part.**

## Ce que le lot livre

**Un gardien** — `tests/test_litteraux_couleur_servis_lot382.py` (12 tests) :

- **anti-vide** : les 8 pages doivent être rendues, et ≥ 20 littéraux détectés —
  si ce nombre tombe à zéro, ce n'est pas que tout va bien, c'est que le
  détecteur est cassé ;
- **borne de dérive fixée À la mesure** (55 pour 53 mesurés) : on n'exige pas
  zéro, on interdit la **croissance silencieuse** ;
- **la règle réelle vérifiée sur les OCTETS SERVIS** : aucun bleu non-marque dans
  ce que le navigateur reçoit — le gardien historique, lui, lit les sources, donc
  un bleu venu du shell, d'un statique ou d'un moteur lui échapperait ;
- **anti-péremption** : si le périmètre de `test_no_blue_in_ui_pages` cessait
  d'inclure le shell, le test le dit.

**Une correction de `CLAUDE.md`** : section « Couleurs — la règle réellement
tenue », avec les chiffres mesurés et la distinction entre la règle imposée
(aucun bleu non-marque) et la préférence pour les nouveaux travaux (tokens).

### Preuve ROUGE

```text
ROUGE OK  3 littéraux de couleur ajoutés au shell servi   | restauration identique
ROUGE OK  bleu non-marque servi depuis le shell           | restauration identique
ROUGE OK  borne de dérive franchie                        | restauration identique
ROUGE OK  périmètre du gardien historique restreint       | restauration identique
après restauration : 12 passed
```

Les quatre fautes passaient **toutes** les 2 767 tests avant ce lot.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 381, 946b81b) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché.** `CLAUDE.md` est de la documentation,
  non servie : aucun octet servi ne change, pas de preuve MD5 requise, pas de
  bump.
- Suite : **2767 → 2779 passed / 2 skipped** — verte (+12).
- SW : `td-shell-v187`.

## Portée — ce que ce lot ne prétend pas

Six mutations de plus, soit treize en deux lots sur 2 779 tests : toujours un
**sondage**. Le comptage des littéraux servis se fonde sur la présence textuelle
du `#RRGGBB` dans la page ; un littéral construit dynamiquement (concaténation,
interpolation) ne serait pas vu — la borne le sous-estime donc peut-être. Enfin,
je n'ai pas jugé la **légitimité** des 53 littéraux servis : certains sont
sûrement volontaires, la borne gèle l'existant sans le valider.

## Suite

LOT 383 : poursuivre. Deux lots, deux écarts **doc vs réalité** trouvés au même
endroit — les invariants de `CLAUDE.md`. Piste naturelle : **vérifier
systématiquement chaque règle critique annoncée contre ce qu'un gardien impose
réellement** (il en reste : apostrophes françaises échappées, `scan_state` jamais
réassigné, données réelles / étiquetage démo, `desk_data.json` jamais écrasé).
Prochaine échéance périodique : **~lot 390**.
