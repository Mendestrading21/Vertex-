"""
LOT 358 — Gardien du SECOND point de sortie de news : le cerveau Claude+web.

La règle critique n°5 du projet (« tout texte externe passe par
`sanitize_news()` avant d'être servi — rendu en innerHTML côté client »)
décrit UNE famille de sorties : `/news-feed`, `/api/events/<sym>`,
`/api/skyler/<sym>` — celles que le gardien du lot 177 couvre.

Il en existe une SECONDE, non couverte jusqu'ici : `/api/ai/enrichment`
(`vertex/ai/enrichment.py::parse_news`), qui sert des titres d'actualité
issus d'une recherche web relayée par Claude. Ce chemin n'appelle PAS
`sanitize_news` et ne le doit pas : son unique rendu
(`vertex/ui/pages/system_page.py::loadBrain`) échappe déjà au point
d'affichage via `esc()`. Y ajouter un assainissement serveur
double-échapperait les titres légitimes (« record » → `&quot;record&quot;`
affiché tel quel).

Sa sûreté repose donc sur trois propriétés — que ce fichier fige, car
aucune n'était gardée :
  1. le serveur ne garde que des citations http(s) (`provenance._safe_url`) ;
  2. le serveur borne la forme servie (4 champs, longueurs plafonnées,
     `impact` dans un ensemble fermé) ;
  3. le seul rendu de ces titres passe par `esc()`, défini dans la même
     source servie.

Retirer l'une des trois rouvrirait un vecteur XSS. Ce gardien le dit.
"""
import os
import re

from vertex.ai import enrichment as E
from vertex.ai import provenance as P


_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SYSTEM_PAGE = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'system_page.py')

# Charge utile hostile : schémas de lien exécutables + balises dans les textes.
_MAL_CITATIONS = [
    {'title': 'js', 'url': 'javascript:alert(1)'},
    {'title': 'data', 'url': 'data:text/html,<script>alert(1)</script>'},
    {'title': 'vbs', 'url': 'vbscript:msgbox(1)'},
    {'title': 'relatif', 'url': '/interne'},
    {'title': 'non-texte', 'url': 42},
    {'title': 'vrai', 'url': 'https://n.ews/a'},
]


class _MalProvider:
    """Provider simulé qui renvoie du texte et des liens hostiles."""

    model = 'claude-test'

    def available(self):
        return True

    def research_json(self, system, user):
        if 'actualité' in user or 'items' in user:
            return {'data': {'items': [
                {'headline': '<script>alert(1)</script>' + 'T' * 500,
                 'impact': '<img src=x onerror=alert(2)>', 'why': 'W' * 500,
                 'date': 'D' * 200, 'extra': '<script>alert(3)</script>'},
            ]}, 'citations': list(_MAL_CITATIONS), 'searches': 1}
        return {'data': {'price': 10.0}, 'citations': list(_MAL_CITATIONS),
                'searches': 1, 'text': 'cours 10'}


# ── 1. Seuls les liens web réels survivent ───────────────────────────────────

def test_seules_les_citations_http_s_sont_servies():
    env = P.wrap(1, source=P.SRC_CLAUDE_WEB, citations=list(_MAL_CITATIONS))
    urls = [c['url'] for c in env['citations']]
    assert urls == ['https://n.ews/a']          # tout le reste est jeté
    blob = repr(env)
    assert 'javascript:' not in blob and 'data:text/html' not in blob


def test_enrichissement_de_bout_en_bout_ne_sert_aucun_schema_executable():
    snap = E.run(['TSTQ'], provider=_MalProvider(), persist_store=False)
    import json
    blob = json.dumps(snap, ensure_ascii=False)
    assert 'javascript:' not in blob
    assert 'vbscript:' not in blob
    assert 'data:text/html' not in blob


# ── 2. La forme servie reste bornée et fermée ────────────────────────────────

def test_la_forme_des_actualites_ia_reste_bornee_et_fermee():
    snap = E.run(['TSTQ'], provider=_MalProvider(), persist_store=False)
    item = snap['surfaces']['news']['TSTQ']['value'][0]
    # Aucun champ libre ne traverse : la forme est reconstruite, pas recopiée.
    assert set(item) == {'headline', 'impact', 'why', 'date'}
    assert len(item['headline']) <= 200 and len(item['why']) <= 280
    assert len(item['date']) <= 40
    # `impact` pilote une classe CSS côté client → ensemble fermé obligatoire.
    assert item['impact'] in ('HAUSSIER', 'BAISSIER', 'NEUTRE')


# ── 3. Le seul rendu passe par esc() ─────────────────────────────────────────

def _appels_englobants(src, pos):
    """Identifiants des appels qui englobent `pos`, du plus proche au plus large.

    On remonte le texte en comptant les parenthèses : chaque `(` non refermée
    ouvre un niveau, et le mot qui la précède est le nom de l'appel (vide pour
    un simple groupement). S'arrête à la fin de l'instruction précédente.
    """
    noms, i, profondeur = [], pos - 1, 0
    while i >= 0 and pos - i < 400:
        c = src[i]
        if c == ')':
            profondeur += 1
        elif c == '(':
            if profondeur:
                profondeur -= 1
            else:                       # parenthèse ouverte non refermée : un niveau
                j = i - 1
                while j >= 0 and (src[j].isalnum() or src[j] in '_$.'):
                    j -= 1
                noms.append(src[j + 1:i])
        elif c in ';\n' and not profondeur:
            break
        i -= 1
    return noms


def _rendus_sans_esc(src, motif):
    """Occurrences de `motif` qui ne sont enveloppées par aucun appel esc()."""
    return [src[max(0, m.start() - 60):m.end() + 20]
            for m in re.finditer(re.escape(motif), src)
            if 'esc' not in _appels_englobants(src, m.start())]


def test_le_titre_ia_n_est_rendu_que_via_esc():
    src = open(_SYSTEM_PAGE, encoding='utf-8').read()
    assert 'function esc(' in src, 'esc() doit être défini dans la source servie'
    assert '.headline' in src, 'le rendu du titre IA a disparu — gardien à revoir'
    assert not _rendus_sans_esc(src, '.headline'), \
        'un titre d\'actualité IA est injecté en innerHTML sans esc()'


def test_les_citations_ia_sont_echappees_dans_le_lien_et_le_libelle():
    src = open(_SYSTEM_PAGE, encoding='utf-8').read()
    assert not _rendus_sans_esc(src, 'c.url'), \
        'une URL de citation est injectée sans esc()'
    assert 'rel="noopener noreferrer"' in src        # pas d'accès à window.opener
