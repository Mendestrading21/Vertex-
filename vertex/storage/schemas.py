"""vertex.storage.schemas — VERSION ET MIGRATION DU REGISTRE.

Un registre append-only survit à ses lecteurs : ce qui est écrit aujourd'hui
sera relu par du code qui n'existe pas encore. Deux règles en découlent, et
elles sont toutes les deux des refus.

**Une version future est refusée.** Lire un format qu'on ne comprend pas ne
produit pas une erreur : cela produit une donnée *fausse présentée comme sûre*,
ce qui est strictement pire. Vertex préfère s'arrêter.

**Chaque migration est réversible.** Le programme l'exige, et la raison est
pratique : un lot qu'on ne peut pas annuler n'a pas de rollback, donc pas le
droit d'être publié. Une migration montante sans descendante est une porte à
sens unique dans un dépôt qui promet des retours en arrière.

## Comment ajouter une version

1. incrémenter `VERSION_COURANTE` ;
2. écrire le couple `(monter, descendre)` dans `MIGRATIONS[VERSION_COURANTE]` ;
3. le test `test_migrer_puis_retrograder_rend_l_enregistrement_d_origine`
   éprouve l'aller-retour — il n'y a rien à déclarer de plus.
"""
from __future__ import annotations

#: Version du format d'observation. Toute observation écrite la porte.
VERSION_COURANTE = 1

#: `version -> (monter_depuis_la_precedente, redescendre_vers_la_precedente)`.
#:
#: Vide à la version 1 : il n'existe aucun format antérieur. Ce n'est pas un
#: oubli, et le test le dit — un registre neuf n'a rien à migrer.
MIGRATIONS: dict = {}


def migrer(enregistrement: dict) -> dict:
    """Amène un enregistrement à `VERSION_COURANTE`, ou refuse.

    Refuse dans les deux sens : une version future ne peut pas être devinée, et
    une version passée sans migration déclarée ne peut pas être inventée.
    """
    v = enregistrement.get("schema_version")
    if not isinstance(v, int):
        raise ValueError(
            "enregistrement sans version de schéma — impossible de savoir "
            "comment le lire, et le supposer produirait une donnée fausse")
    if v > VERSION_COURANTE:
        raise ValueError(
            "version de schéma %d, lecteur en version %d — lire un format non "
            "compris rendrait une donnée fausse présentée comme sûre"
            % (v, VERSION_COURANTE))
    out = dict(enregistrement)
    while out["schema_version"] < VERSION_COURANTE:
        cible = out["schema_version"] + 1
        couple = MIGRATIONS.get(cible)
        if not couple:
            raise ValueError(
                "aucune migration déclarée vers la version %d — un saut de "
                "format ne s'improvise pas à la lecture" % cible)
        out = couple[0](out)
        out["schema_version"] = cible
    return out


__all__ = ["VERSION_COURANTE", "MIGRATIONS", "migrer"]
