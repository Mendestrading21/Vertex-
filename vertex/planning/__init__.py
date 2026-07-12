"""vertex.planning — préparation d'ordre & gestion de position (§4/§11/§32).

⛔ READONLY ABSOLU : ce paquet PRÉPARE un ordre (dimensionnement, ticket à
copier manuellement dans IBKR) mais n'en TRANSMET jamais aucun. Aucune fonction
ici n'appelle un courtier. « Préparer » ≠ « exécuter ».
"""
from .order_ticket import size_position, build_ticket, SIDES

__all__ = ['size_position', 'build_ticket', 'SIDES']
