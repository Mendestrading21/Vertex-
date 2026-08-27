"""vertex.ui.vx2 — primitives de présentation Vertex 2.0 (« Black Glass, Signal Light »).

Propriétaire visuel UNIQUE des composants de la refonte 2.0. Chaque primitive
rend le balisage attendu par `static/vertex/css/vertex-2-0.css` : une classe
`.vx2-*` n'est écrite qu'ici, jamais dans une page.

CE MODULE NE CALCULE RIEN.
Il met en forme des valeurs déjà produites par les moteurs. Il ne dérive aucun
prix, aucune Greek, aucun score, aucun verdict, aucun pourcentage. Les seules
opérations arithmétiques admises sont des mises en forme d'affichage
(séparateurs de milliers, signe, décimales) sur une valeur reçue telle quelle.

Règle d'honnêteté : une valeur absente rend `—`. Elle ne devient jamais `0`,
ne prend jamais une couleur directionnelle, et ne se voit jamais complétée.
"""
from __future__ import annotations

from html import escape as _e
from typing import Iterable, Mapping, Sequence

# Valeur affichée quand la donnée n'existe pas. Distincte d'un vrai zéro.
ABSENT = '—'

#: Tons sémantiques autorisés. Toute autre valeur retombe sur le neutre argent.
TONES = ('positive', 'negative', 'caution', 'option', 'missing', 'neutral')

#: Libellés français des états de donnée, pour que la couleur ne porte jamais
#: seule le sens (contrôle 127).
ETATS = {
    'live': 'Temps réel',
    'delayed': 'Différée',
    'stale': 'Périmée',
    'demo': 'Démo',
    'offline': 'Hors ligne',
    'partial': 'Partielle',
    'missing': 'Indisponible',
    'error': 'Erreur',
    'option': 'Options',
}


def _tone(value: str | None) -> str:
    """Normalise un ton ; tout ton inconnu devient neutre plutôt que coloré."""
    return value if value in TONES else 'neutral'


def _attr(name: str, value) -> str:
    return f' {name}="{_e(str(value), quote=True)}"' if value not in (None, '') else ''


# ══════════════════════════════════════════════════════════════════════════
# Valeurs et provenance
# ══════════════════════════════════════════════════════════════════════════

def valeur(v, *, unite: str = '', tone: str | None = None, mono: bool = True) -> str:
    """Rend une valeur déjà calculée. `None` rend `—` en gris, jamais `0`.

    `tone` doit venir d'une lecture du moteur (« cette valeur EST négative »),
    jamais d'une comparaison faite ici : ce module ne juge pas une donnée.
    """
    cls = 'vx2-mono' if mono else ''
    if v is None or v == '':
        return f'<span class="{cls} vx2-absent" title="Donnée indisponible">{ABSENT}</span>'
    txt = _e(str(v)) + (f'<span class="vx2-unit"> {_e(unite)}</span>' if unite else '')
    t = _tone(tone)
    tcls = {'positive': ' vx2-pos', 'negative': ' vx2-neg',
            'caution': ' vx2-cau', 'option': ' vx2-opt'}.get(t, '')
    return f'<span class="{cls}{tcls}">{txt}</span>'


def badge_etat(etat: str, *, texte: str | None = None) -> str:
    """Badge d'état de donnée. Le mot est TOUJOURS écrit — la pastille de
    couleur ne fait que redoubler une information déjà lisible."""
    key = (etat or 'missing').lower()
    label = texte or ETATS.get(key, etat or 'Indisponible')
    return (f'<span class="vx2-badge" data-state="{_e(key, quote=True)}">'
            f'{_e(label)}</span>')


def estampille(*, source: str | None = None, horodatage: str | None = None,
               qualite: str | None = None, note: str | None = None) -> str:
    """Source · heure · qualité. La provenance doit survivre à toute
    recomposition visuelle (contrôle 010) : si elle manque, on l'avoue."""
    parts = []
    parts.append(f'<span>Source <b>{_e(source)}</b></span>' if source
                 else f'<span>Source <b>{ABSENT}</b></span>')
    if horodatage:
        parts.append(f'<time>{_e(horodatage)}</time>')
    else:
        parts.append(f'<span>Horodatage {ABSENT}</span>')
    if qualite:
        parts.append(f'<span>{_e(qualite)}</span>')
    if note:
        parts.append(f'<span>{_e(note)}</span>')
    return '<div class="vx2-stamp">' + '<span aria-hidden="true">·</span>'.join(parts) + '</div>'


# ══════════════════════════════════════════════════════════════════════════
# Decision Trace — la signature
# ══════════════════════════════════════════════════════════════════════════

#: Les CINQ emplacements canoniques, et eux seuls (contrôle 117).
TRACE_EMPLACEMENTS = (
    'aujourdhui-hero',
    'opportunite-drawer',
    'analyse-hero',
    'ia-audit-decision',
    'portefeuille-impact',
)


def decision_trace(noeuds: Sequence[Mapping], *, emplacement: str) -> str:
    """Donnée → Moteur → Décision → Portefeuille.

    `emplacement` doit appartenir à `TRACE_EMPLACEMENTS` : la signature perd
    tout sens si elle décore une sixième surface. L'appel est refusé plutôt
    que silencieusement rendu ailleurs.

    Chaque nœud : `{'label', 'valeur', 'meta', 'tone'}`. Un nœud sans ton
    reste argent — c'est le défaut, pas une anomalie.
    """
    if emplacement not in TRACE_EMPLACEMENTS:
        raise ValueError(
            f'Decision Trace hors emplacement canonique : {emplacement!r}. '
            f'Autorisés : {", ".join(TRACE_EMPLACEMENTS)}')
    out = []
    for n in noeuds:
        t = _tone(n.get('tone'))
        val = n.get('valeur')
        val_html = _e(str(val)) if val not in (None, '') else ABSENT
        meta = n.get('meta')
        out.append(
            f'<li class="vx2-trace-node" data-tone="{t}">'
            f'<span class="vx2-trace-dot" aria-hidden="true"></span>'
            f'<span class="vx2-trace-body">'
            f'<span class="vx2-trace-label">{_e(str(n.get("label", "")))}</span>'
            f'<span class="vx2-trace-value">{val_html}</span>'
            + (f'<span class="vx2-trace-meta">{_e(str(meta))}</span>' if meta else '')
            + '</span></li>')
    return (f'<ol class="vx2-trace" data-trace="{_e(emplacement, quote=True)}" '
            f'aria-label="Trace de décision : donnée, moteur, décision, portefeuille">'
            + ''.join(out) + '</ol>')


# ══════════════════════════════════════════════════════════════════════════
# Structure de page
# ══════════════════════════════════════════════════════════════════════════

def page_header(*, titre: str, question: str, surtitre: str = '',
                actions: str = '', fraicheur: str = '') -> str:
    """En-tête canonique : la QUESTION métier est obligatoire (contrôle 031).
    Une page qui ne sait pas dire à quoi elle sert n'est pas prête."""
    return (
        '<header class="vx2-header">'
        '<div class="vx2-header-top"><div>'
        + (f'<p class="vx2-eyebrow">{_e(surtitre)}</p>' if surtitre else '')
        + f'<h1 class="vx2-title">{_e(titre)}</h1>'
        f'<p class="vx2-question">{_e(question)}</p>'
        '</div>'
        + (f'<div class="vx2-header-actions">{actions}</div>' if actions else '')
        + '</div>'
        + (fraicheur or '')
        + '</header>')


def context_bar(groupes: Sequence[Mapping]) -> str:
    """Période · univers · filtres · source. Chaque groupe : `{'label', 'contenu'}`."""
    cells = []
    for g in groupes:
        cells.append(
            '<div class="vx2-context-group">'
            f'<span class="vx2-context-label">{_e(str(g.get("label", "")))}</span>'
            f'{g.get("contenu", "")}</div>')
    sep = '<span class="vx2-context-sep" aria-hidden="true"></span>'
    return ('<div class="vx2-contextbar" role="group" aria-label="Contexte de la page">'
            + sep.join(cells) + '</div>')


def section(*, titre: str, corps: str, note: str = '', actions: str = '',
            niveau: int = 2) -> str:
    h = max(2, min(4, niveau))
    head = (f'<div class="vx2-section-head">'
            f'<h{h} class="vx2-section-title">{_e(titre)}</h{h}>'
            + (f'<span class="vx2-section-note">{_e(note)}</span>' if note else '')
            + (actions or '') + '</div>')
    return f'<section class="vx2-section">{head}{corps}</section>'


def surface(corps: str, *, titre: str = '', question: str = '', pied: str = '',
            compact: bool = False, hero: bool = False, span: int | None = None,
            actions: str = '') -> str:
    """Carte unique de la refonte. `hero` = surface élevée (verre plus dense
    + reflet de matière). Aucune variante ad hoc ne doit être créée ailleurs."""
    cls = 'vx2-hero' if hero else 'vx2-surface'
    if compact and not hero:
        cls += ' vx2-surface--compact'
    if span:
        cls += f' vx2-col-{span}'
    head = ''
    if titre or question or actions:
        head = ('<div class="vx2-card-head"><div>'
                + (f'<h3 class="vx2-card-title">{_e(titre)}</h3>' if titre else '')
                + (f'<p class="vx2-card-question">{_e(question)}</p>' if question else '')
                + '</div>' + (actions or '') + '</div>')
    return f'<div class="{cls}">{head}{corps}{pied}</div>'


# ══════════════════════════════════════════════════════════════════════════
# Métriques
# ══════════════════════════════════════════════════════════════════════════

def metric(*, label: str, valeur_html: str, meta: str = '', tone: str | None = None,
           grand: bool = False) -> str:
    cls = 'vx2-metric vx2-metric--lg' if grand else 'vx2-metric'
    t = _tone(tone)
    return (f'<div class="{cls}">'
            f'<span class="vx2-metric-label">{_e(label)}</span>'
            f'<span class="vx2-metric-value" data-tone="{t}">{valeur_html}</span>'
            + (f'<span class="vx2-metric-meta">{_e(meta)}</span>' if meta else '')
            + '</div>')


def metric_strip(items: Iterable[Mapping]) -> str:
    """Bande compacte de métriques. Volontairement SANS hiérarchie interne :
    si une valeur doit dominer, elle appartient à la DecisionZone, pas ici
    (contrôle 035)."""
    return ('<div class="vx2-strip">'
            + ''.join(metric(label=i.get('label', ''),
                             valeur_html=i.get('valeur', valeur(None)),
                             meta=i.get('meta', ''),
                             tone=i.get('tone'),
                             grand=bool(i.get('grand')))
                      for i in items)
            + '</div>')


# ══════════════════════════════════════════════════════════════════════════
# États — jamais un rectangle vide
# ══════════════════════════════════════════════════════════════════════════

def etat(*, titre: str, cause: str, kind: str = 'empty', actions: str = '',
         fantome: bool = True) -> str:
    """État honnête. `cause` est obligatoire : dire « aucune donnée » sans dire
    POURQUOI oblige l'utilisateur à deviner si la source est absente, en panne
    ou simplement vide (contrôle 044)."""
    ghost = ('<span class="vx2-state-ghost" aria-hidden="true">'
             '<i></i><i></i><i></i><i></i></span>') if fantome else ''
    return (f'<div class="vx2-state" data-kind="{_e(kind, quote=True)}" role="status">'
            f'{ghost}'
            f'<p class="vx2-state-title">{_e(titre)}</p>'
            f'<p class="vx2-state-cause">{_e(cause)}</p>'
            + (f'<div class="vx2-state-actions">{actions}</div>' if actions else '')
            + '</div>')


def bandeau(texte: str, *, kind: str = 'neutre') -> str:
    """Bandeau posé sur une carte qui porte DÉJÀ de la donnée (retard,
    couverture partielle, avertissement). Ne remplace jamais un état vide."""
    return (f'<div class="vx2-banner" data-kind="{_e(kind, quote=True)}" role="status">'
            f'<span>{_e(texte)}</span></div>')


def capacite_absente(*, quoi: str, pourquoi: str) -> str:
    """Capacité que Vertex ne fournit pas.

    La refonte 2.0 est visuelle : elle ne développe aucun moteur. Quand une
    maquette réclame un calcul inexistant, on l'AVOUE ici plutôt que de le
    fabriquer dans un template.
    """
    return etat(titre=f'{quoi} — calcul non disponible dans Vertex',
                cause=pourquoi, kind='missing', fantome=True)


# ══════════════════════════════════════════════════════════════════════════
# Tables
# ══════════════════════════════════════════════════════════════════════════

def table(*, colonnes: Sequence[Mapping], lignes: Sequence[Sequence[str]],
          libelle: str, cartes_mobile: str = '', vide: str = '') -> str:
    """Table financière dense.

    `colonnes` : `{'titre', 'num': bool, 'sticky': bool, 'unite': str}`.
    L'unité vit dans l'EN-TÊTE, pas répétée dans chaque cellule (contrôle 051).
    `cartes_mobile` porte la même donnée en cartes-lignes : sous 760 px la
    table est masquée, jamais compressée jusqu'à l'illisible (contrôle 134).
    """
    if not lignes:
        return vide or etat(titre='Aucune ligne à afficher',
                            cause='Le tableau est vide pour les filtres actuels.',
                            kind='empty')
    ths = []
    for c in colonnes:
        cls = ' class="' + ' '.join(
            filter(None, ['vx2-num' if c.get('num') else '',
                          'vx2-sticky-col' if c.get('sticky') else ''])) + '"'
        if cls == ' class=""':
            cls = ''
        unite = (f' <span class="vx2-th-unit">({_e(c["unite"])})</span>'
                 if c.get('unite') else '')
        ths.append(f'<th scope="col"{cls}>{_e(str(c.get("titre", "")))}{unite}</th>')
    trs = []
    for row in lignes:
        tds = []
        for c, cell in zip(colonnes, row):
            cls = ' class="' + ' '.join(
                filter(None, ['vx2-num' if c.get('num') else '',
                              'vx2-sticky-col' if c.get('sticky') else ''])) + '"'
            if cls == ' class=""':
                cls = ''
            tds.append(f'<td{cls}>{cell}</td>')
        trs.append('<tr>' + ''.join(tds) + '</tr>')
    mob = f'<div class="vx2-rowcards">{cartes_mobile}</div>' if cartes_mobile else ''
    wrap_attr = ' data-mobile="cards"' if cartes_mobile else ''
    return (f'<div class="vx2-table-wrap"{wrap_attr} tabindex="0" role="region" '
            f'aria-label="{_e(libelle, quote=True)}">'
            f'<table class="vx2-table"><caption class="vx2-sr-only">{_e(libelle)}</caption>'
            f'<thead><tr>{"".join(ths)}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>{mob}')


def rowcard(*, titre: str, aparte: str = '', cellules: Sequence[Mapping]) -> str:
    """Une ligne de table rendue en carte, pour le mobile."""
    cells = ''.join(
        f'<div class="vx2-rowcard-cell"><dt>{_e(str(c.get("label", "")))}</dt>'
        f'<dd>{c.get("valeur", ABSENT)}</dd></div>' for c in cellules)
    return (f'<article class="vx2-rowcard">'
            f'<div class="vx2-rowcard-head"><strong>{_e(titre)}</strong>'
            f'{aparte}</div>'
            f'<dl class="vx2-rowcard-grid">{cells}</dl></article>')


# ══════════════════════════════════════════════════════════════════════════
# Graphiques — le conteneur, jamais la donnée
# ══════════════════════════════════════════════════════════════════════════

def chart_card(*, titre: str, question: str, dom_id: str, conclusion: str = '',
               source: str = '', horodatage: str = '', unite: str = '',
               periode: str = '', legende: str = '', table_equivalente: str = '',
               resume_accessible: str = '', hauteur: int = 240,
               limites: str = '', span: int | None = None) -> str:
    """Conteneur de graphique conforme au contrat.

    Le rendu de la série reste la propriété du moteur graphique existant : ce
    conteneur RÉSERVE la hauteur (pas de saut de mise en page), porte la
    question, la conclusion, la provenance, l'unité, la période, les limites,
    un résumé accessible et la table équivalente. Il ne touche à aucune valeur.
    """
    pied_bits = []
    if unite:
        pied_bits.append(f'<span>Unité : {_e(unite)}</span>')
    if periode:
        pied_bits.append(f'<span>Période : {_e(periode)}</span>')
    if limites:
        pied_bits.append(f'<span>Limites : {_e(limites)}</span>')
    pied = ('<div class="vx2-chart-foot">'
            + (f'<div class="vx2-legend">{legende}</div>' if legende else '<div></div>')
            + (f'<div>{"".join(pied_bits)}</div>' if pied_bits else '')
            + '</div>')
    stamp = estampille(source=source or None, horodatage=horodatage or None)
    resume = (f'<p class="vx2-sr-only">{_e(resume_accessible)}</p>'
              if resume_accessible else '')
    concl = (f'<p class="vx2-chart-conclusion">{_e(conclusion)}</p>'
             if conclusion else '')
    tbl = (f'<details class="vx2-chart-table"><summary>Voir les valeurs sous forme '
           f'de tableau</summary>{table_equivalente}</details>'
           if table_equivalente else '')
    corps = (f'{concl}'
             f'<div class="vx2-chart" id="{_e(dom_id, quote=True)}" '
             f'style="--vx2-chart-h:{int(hauteur)}px" role="img" '
             f'aria-label="{_e(question, quote=True)}">{resume}</div>'
             f'{pied}{stamp}{tbl}')
    return surface(corps, titre=titre, question=question, span=span)


# ══════════════════════════════════════════════════════════════════════════
# Contrôles
# ══════════════════════════════════════════════════════════════════════════

def bouton(libelle: str, *, href: str = '', variante: str = '', ident: str = '',
           attrs: str = '') -> str:
    """Le libellé annonce le RÉSULTAT (« Ouvrir le dossier »), jamais l'action
    technique. Aucun libellé d'ordre n'est admis dans ce produit."""
    cls = 'vx2-btn' + (f' vx2-btn--{variante}' if variante else '')
    if href:
        return (f'<a class="{cls}" href="{_e(href, quote=True)}"'
                f'{_attr("id", ident)}{attrs}>{_e(libelle)}</a>')
    return (f'<button type="button" class="{cls}"{_attr("id", ident)}{attrs}>'
            f'{_e(libelle)}</button>')


def chip(libelle: str, *, actif: bool = False, href: str = '', attrs: str = '') -> str:
    etat_attr = ' aria-pressed="true"' if actif else ' aria-pressed="false"'
    if href:
        etat_attr = ' aria-current="true"' if actif else ''
        return (f'<a class="vx2-chip" href="{_e(href, quote=True)}"'
                f'{etat_attr}{attrs}>{_e(libelle)}</a>')
    return f'<button type="button" class="vx2-chip"{etat_attr}{attrs}>{_e(libelle)}</button>'


def tabs(items: Sequence[Mapping], *, libelle: str) -> str:
    """Onglets de sous-vues. `{'label', 'href', 'actif'}` — de vrais liens :
    chaque sous-vue garde une URL partageable et un retour prévisible."""
    out = []
    for it in items:
        cur = ' aria-current="page"' if it.get('actif') else ''
        out.append(f'<a class="vx2-tab" href="{_e(str(it.get("href", "#")), quote=True)}"'
                   f'{cur}>{_e(str(it.get("label", "")))}</a>')
    return (f'<nav class="vx2-tabs" aria-label="{_e(libelle, quote=True)}">'
            + ''.join(out) + '</nav>')


def champ(*, ident: str, label: str, controle: str, aide: str = '',
          erreur: str = '') -> str:
    """Label VISIBLE, aide proche, erreur reliée au champ (contrôle 126)."""
    invalide = ' data-invalid="true"' if erreur else ''
    decrit = []
    if aide:
        decrit.append(f'{ident}-aide')
    if erreur:
        decrit.append(f'{ident}-err')
    return (f'<div class="vx2-field"{invalide}>'
            f'<label for="{_e(ident, quote=True)}">{_e(label)}</label>'
            f'{controle}'
            + (f'<p class="vx2-help" id="{_e(ident, quote=True)}-aide">{_e(aide)}</p>'
               if aide else '')
            + (f'<p class="vx2-field-error" id="{_e(ident, quote=True)}-err" '
               f'role="alert">{_e(erreur)}</p>' if erreur else '')
            + '</div>')


__all__ = [
    'ABSENT', 'TONES', 'ETATS', 'TRACE_EMPLACEMENTS',
    'valeur', 'badge_etat', 'estampille', 'decision_trace',
    'page_header', 'context_bar', 'section', 'surface',
    'metric', 'metric_strip', 'etat', 'bandeau', 'capacite_absente',
    'table', 'rowcard', 'chart_card', 'bouton', 'chip', 'tabs', 'champ',
]
