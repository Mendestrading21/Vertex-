"""vertex/data/descriptions_fr.py — DESCRIPTIONS MÉTIER EN FRANÇAIS.

Table de secours : une phrase d'activité, un secteur et un pays pour les titres
les plus consultés. Elle sert dans deux cas, et c'est ce qui justifie qu'elle
soit **écrite à la main** plutôt que traduite à la volée :

1. **mode démonstration** — aucun appel réseau ne doit partir, et un écran vide
   ferait passer la vitrine pour une panne ;
2. **secours** — yfinance limite les appels `info` bien plus vite que les
   cotations ; sans table, une fiche ouverte un jour de throttle n'afficherait
   rien du tout.

Ce ne sont **pas des données de marché** : aucun prix, aucun chiffre, rien qui
puisse périmer en séance. Une activité d'entreprise change à l'échelle de
l'année, et le texte est daté par le dépôt lui-même.

Forme : `{ticker: (résumé, secteur, pays)}`.
"""
from __future__ import annotations

DESCRIPTIONS = {
    'AAPL': ("Apple conçoit, fabrique et vend des smartphones (iPhone), ordinateurs (Mac), tablettes (iPad) et objets connectés (Apple Watch, AirPods), ainsi qu'un large écosystème de services (App Store, iCloud, Apple Music, paiements). Son intégration matériel-logiciel et sa marque premium en font l'une des plus grosses capitalisations mondiales.", 'Électronique grand public', 'États-Unis'),
    'NVDA': ("Nvidia conçoit des processeurs graphiques (GPU) et des puces d'accélération devenus le standard de l'intelligence artificielle et des centres de données. Ses cartes équipent le jeu vidéo, la 3D professionnelle, l'automobile autonome et l'entraînement des grands modèles d'IA.", 'Semi-conducteurs', 'États-Unis'),
    'MSFT': ("Microsoft édite Windows, la suite Office/Microsoft 365 et la plateforme cloud Azure. Le groupe est aussi présent dans le jeu vidéo (Xbox), les réseaux professionnels (LinkedIn) et investit massivement dans l'IA (partenariat OpenAI, Copilot).", 'Logiciels & Cloud', 'États-Unis'),
    'META': ("Meta exploite Facebook, Instagram, WhatsApp et Messenger, réunissant des milliards d'utilisateurs. L'essentiel de ses revenus vient de la publicité ciblée ; le groupe investit aussi dans la réalité virtuelle/augmentée (Reality Labs) et l'IA.", 'Réseaux sociaux & Publicité', 'États-Unis'),
    'GOOGL': ("Alphabet, maison mère de Google, tire l'essentiel de ses revenus de la publicité (Recherche, YouTube, réseau display). Le groupe possède aussi Android, le cloud Google Cloud, et des paris technologiques (Waymo, IA DeepMind/Gemini).", 'Internet & Publicité', 'États-Unis'),
    'AMZN': ("Amazon est le leader mondial du commerce en ligne et, via AWS, le numéro un du cloud d'entreprise — sa principale source de profits. Le groupe est aussi présent dans la logistique, la publicité, le streaming (Prime) et les objets connectés (Alexa).", 'E-commerce & Cloud', 'États-Unis'),
    'AVGO': ("Broadcom conçoit des semi-conducteurs (réseau, connectivité, stockage) et des logiciels d'infrastructure d'entreprise. Ses puces équipent centres de données, smartphones et équipements réseau ; le groupe croît par acquisitions.", 'Semi-conducteurs', 'États-Unis'),
    'TSLA': ("Tesla conçoit et produit des véhicules électriques, des batteries et des solutions de stockage/énergie solaire. Le groupe mise sur la conduite autonome, la robotique et l'intégration verticale de sa production.", 'Automobile & Énergie', 'États-Unis'),
    'NFLX': ("Netflix est la plateforme mondiale de streaming vidéo par abonnement, produisant et diffusant films et séries dans le monde entier. Le groupe développe la publicité et le jeu vidéo pour diversifier ses revenus.", 'Streaming & Médias', 'États-Unis'),
    'AMD': ("AMD conçoit des processeurs (CPU Ryzen/EPYC) et cartes graphiques (Radeon) pour PC, serveurs et centres de données. Le groupe est un concurrent direct d'Intel et de Nvidia et monte en puissance sur l'IA.", 'Semi-conducteurs', 'États-Unis'),
    'CRM': ("Salesforce est le leader mondial des logiciels de gestion de la relation client (CRM) en mode cloud : ventes, service client, marketing et analytique de données, avec une forte intégration d'IA (Einstein).", "Logiciels d'entreprise", 'États-Unis'),
    'COST': ("Costco exploite un réseau mondial d'entrepôts en libre-service réservés aux adhérents. Son modèle repose sur des marges faibles, de gros volumes et des revenus d'abonnement récurrents très fidélisants.", 'Distribution', 'États-Unis'),
    'LLY': ("Eli Lilly est un laboratoire pharmaceutique majeur, notamment dans le diabète et l'obésité (agonistes GLP-1), l'oncologie, l'immunologie et les neurosciences. Ses traitements récents connaissent une très forte demande.", 'Pharmacie', 'États-Unis'),
    'JPM': ("JPMorgan Chase est la plus grande banque américaine : banque de détail, banque d'investissement, gestion d'actifs et de fortune. Diversifiée et solide, elle sert de baromètre au secteur financier.", 'Banque', 'États-Unis'),
    'V': ("Visa exploite le plus grand réseau mondial de paiement par carte, percevant une commission sur chaque transaction sans porter le risque de crédit. Un modèle très rentable qui profite de la baisse du cash.", 'Paiements', 'États-Unis'),
    'MA': ("Mastercard exploite un réseau mondial de paiement électronique, se rémunérant sur les transactions traitées. Comme Visa, elle bénéficie de la digitalisation des paiements sans supporter le risque de crédit.", 'Paiements', 'États-Unis'),
    'HD': ("The Home Depot est le leader américain de la distribution de bricolage, matériaux et équipements pour la maison, servant particuliers comme professionnels du bâtiment.", 'Distribution spécialisée', 'États-Unis'),
    'UNH': ("UnitedHealth Group est un géant américain de la santé : assurance santé (UnitedHealthcare) et services de soins/données (Optum). Un acteur clé et défensif du système de santé américain.", 'Assurance santé', 'États-Unis'),
    'XOM': ("ExxonMobil est une major pétrolière et gazière intégrée : exploration, production, raffinage et chimie. Ses résultats suivent les cours du pétrole et du gaz ; le groupe investit aussi dans la capture de carbone.", 'Pétrole & Gaz', 'États-Unis'),
    'WMT': ("Walmart est le premier distributeur mondial par le chiffre d'affaires, avec un réseau massif d'hypermarchés et une activité e-commerce en forte croissance. Positionné sur les prix bas, il est défensif en période d'incertitude.", 'Distribution', 'États-Unis'),
}


#: Ancien nom, conservé pour les appelants historiques.
_FR_DESC = DESCRIPTIONS

__all__ = ['DESCRIPTIONS']
