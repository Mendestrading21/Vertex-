"""vertex.ui.pages.design_system_page — Design System vivant (§50).

Page de RÉFÉRENCE interne : palette, typographie, surfaces, KPI, jauges,
anneaux, barres, badges, boutons, onglets, états, états vides, tableaux —
tous rendus avec les VRAIS tokens (`/static/vertex/css/tokens.css`) et les
VRAIES classes de composants (`components.css`, `buttons.css`, `states.css`).

Strictement visuel : aucune donnée, aucun moteur, aucune connexion. Sert de
source unique de vérité pour l'identité VERTEX BLACK GLASS INSTITUTIONAL.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell


def _load_tokens() -> dict:
    """Valeurs RÉELLES de la cascade (tokens.css, puis glass.css et
    vertex-2-0.css — la couche finale gagne). Les chaînes d'alias var(--x)
    sont résolues jusqu'au hex — la page de référence LIT la vérité au lieu
    de la recopier."""
    import os
    import re
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'static',
                        'vertex', 'css', 'tokens.css')
    try:
        css = open(path, encoding='utf-8').read()
    except OSError:
        return {}
    toks = dict(re.findall(r'(--vx-[a-z0-9-]+)\s*:\s*([^;]+);', css))
    out = {}
    #  Lot 25 : la résolution suit la CASCADE réelle — un alias peut pointer
    #  sur un jeton défini par glass.css ou vertex-2-0.css (couche finale),
    #  et une chaîne d'alias peut faire plusieurs sauts.
    dossier = os.path.dirname(path)
    for feuille in ('glass.css', 'vertex-2-0.css'):
        chemin = os.path.join(dossier, feuille)
        try:
            autre = open(chemin, encoding='utf-8').read()
        except OSError:
            continue
        for m in re.finditer(r'(--vx[a-z0-9-]*)\s*:\s*([^;}]+)[;}]', autre):
            toks[m.group(1)] = m.group(2)
    for k, v in toks.items():
        v = v.strip()
        for _ in range(6):                       # chaînes d'alias bornées
            m = re.fullmatch(r'var\((--vx-[a-z0-9-]+)\)', v)
            if not m:
                break
            v = toks.get(m.group(1), v).strip()
            if v == 'var(%s)' % m.group(1):
                break
        out[k] = v
    return out


_TOKENS = _load_tokens()


def _swatch(var: str, label: str = '') -> str:
    name = label or var
    hexv = _TOKENS.get(var, '')
    meta = f'<span class="ds-hex">{hexv}</span>' if hexv else ''
    return (f'<div class="ds-sw"><span class="ds-chip" style="background:var({var})"></span>'
            f'<code>{name}</code>{meta}</div>')


# ── Groupes de palette (les VALEURS viennent de tokens.css, jamais recopiées) ─
_BG = ['--vx-black', '--vx-obsidian-950', '--vx-obsidian-900', '--vx-obsidian-850',
       '--vx-obsidian-800', '--vx-graphite-900', '--vx-graphite-850',
       '--vx-graphite-800', '--vx-graphite-750', '--vx-graphite-700']
_COPPER = ['--vx-orange-950', '--vx-orange-900', '--vx-orange-850', '--vx-orange-800',
           '--vx-orange-700', '--vx-orange-600', '--vx-orange-500', '--vx-orange-400',
           '--vx-copper-dark', '--vx-copper', '--vx-copper-light']
_SEM = ['--vx-positive', '--vx-negative', '--vx-warning', '--vx-option',
        '--vx-amber', '--vx-beige', '--vx-neutral-chart', '--vx-info']
_TEXT = ['--vx-text-primary', '--vx-text-secondary', '--vx-text-muted',
         '--vx-text-faint']


def _swatches(items):
    return '<div class="ds-sw-grid">' + ''.join(_swatch(v) for v in items) + '</div>'


_DS_CSS = """
<style id="ds-page">
.ds-note{color:var(--vx-text-secondary);font-size:13.5px;line-height:1.6;max-width:74ch;margin:0 0 4px}
.ds-sw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}
.ds-sw{display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--vx-graphite-900);
 border:1px solid var(--vx-border-soft);border-radius:var(--vx-r-sm)}
.ds-chip{width:30px;height:30px;border-radius:8px;flex:0 0 auto;border:1px solid var(--vx-border-strong);box-shadow:var(--vx-shadow-1)}
.ds-sw code{font:600 11px/1.2 var(--vx-font-mono,ui-monospace,monospace);color:var(--vx-text-primary);white-space:nowrap}
.ds-hex{margin-left:auto;font:500 10.5px/1 var(--vx-font-mono,monospace);color:var(--vx-text-muted);font-variant-numeric:tabular-nums}
.ds-type-row{display:flex;align-items:baseline;gap:16px;padding:9px 0;border-bottom:1px dashed var(--vx-border-soft)}
.ds-type-row:last-child{border:none}
.ds-type-row .ds-meta{margin-left:auto;font:500 11px/1 var(--vx-font-mono,monospace);color:var(--vx-text-faint)}
.ds-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.ds-radii{display:flex;gap:16px;flex-wrap:wrap}
.ds-radii>div{width:88px;height:64px;background:var(--vx-graphite-800);border:1px solid var(--vx-border-default);
 display:grid;place-items:end center;padding-bottom:6px;font:500 10px/1 var(--vx-font-mono,monospace);color:var(--vx-text-muted)}
.ds-elev{display:flex;gap:18px;flex-wrap:wrap}
.ds-elev>div{width:150px;height:78px;background:var(--vx-surface-raised);border:1px solid var(--vx-border-soft);
 border-radius:var(--vx-r);display:grid;place-items:center;font:500 11px/1 var(--vx-font-mono,monospace);color:var(--vx-text-muted)}
.ds-ring{--v:72;width:96px;height:96px;border-radius:50%;position:relative;display:grid;place-items:center;
 background:conic-gradient(var(--vx-orange-500) calc(var(--v)*1%),var(--vx-graphite-750) 0)}
.ds-ring::after{content:"";position:absolute;inset:10px;border-radius:50%;background:var(--vx-surface-base)}
.ds-ring b{position:relative;z-index:1;font:650 22px/1 var(--vx-font);color:var(--vx-text-primary);font-variant-numeric:tabular-nums}
.ds-gauge{width:170px;height:90px;overflow:hidden;position:relative}
.ds-gauge .arc{width:170px;height:170px;border-radius:50%;background:conic-gradient(from 270deg,var(--vx-negative) 0 33%,var(--vx-warning) 33% 66%,var(--vx-positive) 66% 100%);
 -webkit-mask:radial-gradient(circle at 50% 100%,transparent 46%,#000 47%);mask:radial-gradient(circle at 50% 100%,transparent 46%,#000 47%)}
.ds-gauge .needle{position:absolute;left:50%;bottom:0;width:2px;height:74px;background:var(--vx-text-primary);transform-origin:bottom center;transform:rotate(38deg);border-radius:2px}
.ds-bar{height:9px;border-radius:99px;background:var(--vx-graphite-750);overflow:hidden;min-width:180px}
.ds-bar>i{display:block;height:100%;border-radius:99px}
.ds-barwrap{display:flex;flex-direction:column;gap:9px;min-width:260px}
.ds-barrow{display:grid;grid-template-columns:70px 1fr 44px;align-items:center;gap:10px;font-size:12px;color:var(--vx-text-secondary)}
.ds-barrow .ds-v{text-align:right;font-variant-numeric:tabular-nums;color:var(--vx-text-muted);font-size:11px}
</style>
"""


# ── Galerie Vertex 2.0 ──────────────────────────────────────────────────────
# Les primitives de `vertex.ui.vx2` rendues avec leur VRAI balisage, pour que
# la refonte ait une surface de contrôle unique (Definition of Done : « démontré
# sur /design-system si réutilisable »). Aucune donnée réelle ici — les valeurs
# sont des exemples de MISE EN FORME, jamais présentées comme des mesures.

def _galerie_2_0() -> str:
    from vertex.ui import vx2

    trace = vx2.decision_trace([
        {'label': 'Donnée', 'valeur': 'Indisponible', 'meta': 'source —',
         'tone': 'missing'},
        {'label': 'Moteur', 'valeur': 'Régime indéterminé', 'meta': 'v4',
         'tone': 'caution'},
        {'label': 'Décision', 'valeur': 'Risque neuf bloqué', 'tone': 'negative'},
        {'label': 'Portefeuille', 'valeur': 'Aucun impact', 'tone': 'neutral'},
    ], emplacement='analyse-hero')

    etats = ''.join([
        vx2.badge_etat(k) for k in
        ('live', 'delayed', 'stale', 'demo', 'offline', 'partial', 'missing',
         'error', 'option')])

    metriques = vx2.metric_strip([
        {'label': 'Positif réel', 'valeur': vx2.valeur('+2,4 %', tone='positive'),
         'meta': 'moteur · exemple'},
        {'label': 'Négatif réel', 'valeur': vx2.valeur('-1,1 %', tone='negative'),
         'meta': 'moteur · exemple'},
        {'label': 'Prudence', 'valeur': vx2.valeur('Différée', tone='caution'),
         'meta': 'fraîcheur'},
        {'label': 'Options', 'valeur': vx2.valeur('0,42', tone='option'),
         'meta': 'delta · exemple'},
        {'label': 'Donnée absente', 'valeur': vx2.valeur(None),
         'meta': 'jamais remplacée par zéro'},
    ])

    tbl = vx2.table(
        colonnes=[{'titre': 'Instrument', 'sticky': True},
                  {'titre': 'Dernier', 'num': True, 'unite': 'USD'},
                  {'titre': 'Variation', 'num': True, 'unite': '%'},
                  {'titre': 'Fraîcheur'}],
        lignes=[
            ['<b>EXEMPLE.A</b>', vx2.valeur('182,40'),
             vx2.valeur('+1,20', tone='positive'), vx2.badge_etat('delayed')],
            ['<b>EXEMPLE.B</b>', vx2.valeur('64,05'),
             vx2.valeur('-0,80', tone='negative'), vx2.badge_etat('stale')],
            ['<b>EXEMPLE.C</b>', vx2.valeur(None), vx2.valeur(None),
             vx2.badge_etat('missing')],
        ],
        libelle='Exemple de table financière du design system',
        cartes_mobile=vx2.rowcard(
            titre='EXEMPLE.A', aparte=vx2.badge_etat('delayed'),
            cellules=[{'label': 'Dernier', 'valeur': vx2.valeur('182,40')},
                      {'label': 'Variation',
                       'valeur': vx2.valeur('+1,20', tone='positive')}]))

    etats_vides = (
        vx2.etat(titre='Aucune donnée de marché',
                 cause='Les sources externes sont injoignables depuis cet '
                       'environnement. Aucune valeur n\'est fabriquée pour '
                       'combler l\'absence.',
                 kind='empty',
                 actions=vx2.bouton('Ouvrir Système', href='/system',
                                    variante='ghost'))
        + '<div style="height:12px"></div>'
        + vx2.capacite_absente(
            quoi='Attribution de performance par facteur',
            pourquoi='Aucun moteur de Vertex ne produit cette décomposition. '
                     'La refonte visuelle ne développe aucun calcul : le '
                     'besoin est consigné plutôt que simulé.')
        + '<div style="height:12px"></div>'
        + vx2.bandeau('Couverture partielle : 3 des 8 dimensions sont '
                      'alimentées.', kind='caution'))

    controles = (
        vx2.bouton('Ouvrir le dossier', variante='primary')
        + ' ' + vx2.bouton('Ajouter au suivi')
        + ' ' + vx2.bouton('Voir la méthode', variante='ghost')
        + '<div style="height:12px"></div>'
        + vx2.chip('Toutes', actif=True) + ' ' + vx2.chip('Actions')
        + ' ' + vx2.chip('ETF') + ' ' + vx2.chip('Options')
        + '<div style="height:12px"></div>'
        + vx2.champ(ident='ds-demo-montant', label='Montant investi',
                    controle='<input class="vx2-input" id="ds-demo-montant" '
                             'inputmode="decimal" placeholder="10 000">',
                    aide='Montant en devise du compte. Distinct d\'une '
                         'quantité de titres.'))

    return (
        _sec2('Decision Trace — la signature',
              'Donnée → Moteur → Décision → Portefeuille · cinq emplacements canoniques',
              trace)
        + _sec2('États de donnée', 'le mot porte le sens, la couleur ne fait que redoubler',
                f'<div style="display:flex;gap:8px;flex-wrap:wrap">{etats}</div>', span='6')
        + _sec2('Provenance', 'source · horodatage · qualité',
                vx2.estampille(source='moteur Vertex', horodatage='—',
                               qualite='exemple'), span='6')
        + _sec2('MetricCard — famille unique', 'remplace vx-kpi / vx-metric / vx-stat / vx-stat-xl',
                metriques)
        + _sec2('Table financière', 'chiffres tabulaires · en-tête collant · colonne clé collante',
                tbl)
        + _sec2('États honnêtes', 'vide · capacité absente · couverture partielle',
                etats_vides, span='6')
        + _sec2('Contrôles', 'boutons, chips, champs', controles, span='6'))


def _sec2(title, sub, body, span='12') -> str:
    subh = (f'<span class="vx2-card-question">{sub}</span>' if sub else '')
    return (f'<section class="vx2-surface vx-col-{span}" aria-label="{title}">'
            f'<div class="vx2-card-head"><h3 class="vx2-card-title">{title}</h3>'
            f'{subh}</div>{body}</section>')


def _content() -> str:
    def sec(title, sub, body, span='12'):
        subh = f'<span class="vx-card-title" style="color:var(--vx-text-muted);font-weight:500">{sub}</span>' if sub else ''
        return (f'<section class="vx-card vx-col-{span}" aria-label="{title}">'
                f'<div class="vx-card-header"><span class="vx-card-title">{title}</span>{subh}</div>'
                f'<div class="vx-card-body">{body}</div></section>')

    # Typographie
    type_rows = ''.join(
        f'<div class="ds-type-row"><span style="font-size:{sz};font-weight:{w};letter-spacing:{ls};color:var(--vx-text-primary)">{lbl}</span><span class="ds-meta">{meta}</span></div>'
        for lbl, sz, w, ls, meta in [
            ('Page title', '34px', '750', '-.02em', 'title / 32–38'),
            ('Hero title', '22px', '700', '-.01em', 'hero / 19–24'),
            ('Card title', '15px', '600', '0', 'card / 13–16'),
            ('KPI principal', 'var(--vx-fs-kpi)', '650', '-.01em', '--vx-fs-kpi / 28'),
            ('Corps éditorial', '14px', '400', '0', 'body / 14–16'),
            ('Metadata 1234.56', '11px', '600', '.02em', 'meta · tabular-nums'),
        ])

    # KPI strip (démonstration, valeurs fictives explicitement neutres)
    kpis = ''.join(
        f'<div class="vx-kpi"><div class="vx-kpi-label">{l}</div><div class="vx-kpi-value">{v}</div>'
        f'<div class="vx-kpi-delta" style="color:var({c})">{d}</div></div>'
        for l, v, d, c in [('Positif', '+2.4 %', '▲ tendance', '--vx-positive'),
                           ('Négatif', '-1.1 %', '▼ risque', '--vx-negative'),
                           ('Accent', '64', 'confiance', '--vx-brand-strong'),
                           ('Neutre', '—', 'donnée absente', '--vx-text-muted')])
    kpi_body = '<div class="vx-grid" style="grid-template-columns:repeat(4,1fr);gap:12px">' + kpis + '</div>'

    # Badges
    badges = (
        '<div class="ds-row">'
        '<span class="vx-badge">Défaut</span>'
        '<span class="vx-badge vx-badge-status" style="color:var(--vx-positive)">LIVE</span>'
        '<span class="vx-badge vx-badge-status" style="color:var(--vx-warning)">DELAYED</span>'
        '<span class="vx-badge vx-badge-status" style="color:var(--vx-negative)">STALE</span>'
        '<span class="vx-badge-demo">DÉMO</span>'
        '<span class="vx-badge vx-badge-decision" style="color:var(--vx-positive)">ACHETER</span>'
        '<span class="vx-badge vx-badge-risk" style="color:var(--vx-negative)">RISQUE</span>'
        '<span class="vx-badge" style="color:var(--vx-option)">OPTIONS</span>'
        '</div>')

    # Boutons — chaque échantillon copie sa classe (délégation data-ds-copy)
    def _b(cls, label, extra=''):
        return f'<button class="{cls}" data-ds-copy="{cls}" {extra}>{label}</button>'
    btns = (
        '<div class="ds-row">'
        + _b('vx-btn vx-btn-primary', 'Primary copper')
        + _b('vx-btn vx-btn-secondary', 'Secondary')
        + _b('vx-btn vx-btn-soft', 'Soft')
        + _b('vx-btn vx-btn-ghost', 'Ghost')
        + _b('vx-btn vx-btn-success', 'Success')
        + _b('vx-btn vx-btn-danger', 'Danger')
        + _b('vx-btn vx-btn-link', 'Link')
        + _b('vx-btn vx-btn-primary', 'Disabled', 'aria-disabled="true"')
        + _b('vx-btn vx-btn-secondary vx-btn-sm', 'Small')
        + '</div><div class="ds-note" style="margin-top:8px">Clic sur un échantillon → copie sa classe.</div>')

    # Onglets / segmented (échantillons — copient leur classe)
    tabs = (
        '<div class="vx-tabs" role="tablist" style="margin-bottom:14px">'
        '<button class="vx-tab vx-active" data-ds-copy="vx-tab vx-active">Vue d’ensemble</button>'
        '<button class="vx-tab" data-ds-copy="vx-tab">Macro</button>'
        '<button class="vx-tab" data-ds-copy="vx-tab">Secteurs <span class="vx-tab-count">7</span></button>'
        '<button class="vx-tab" data-ds-copy="vx-tab">Volatilité</button></div>'
        '<div class="vx-segmented"><button class="vx-active" data-ds-copy="vx-segmented button">Compact</button>'
        '<button data-ds-copy="vx-segmented button">Confort</button>'
        '<button data-ds-copy="vx-segmented button">Dense</button></div>')

    # Jauge + anneaux + barres
    gauge = (
        '<div class="ds-row" style="gap:34px;align-items:flex-end">'
        '<div style="text-align:center"><div class="ds-gauge"><div class="arc"></div><div class="needle"></div></div>'
        '<div class="vx-kpi-label" style="margin-top:6px">Jauge demi-cercle</div></div>'
        '<div style="text-align:center"><div class="ds-ring"><b>72</b></div>'
        '<div class="vx-kpi-label" style="margin-top:6px">Anneau de score</div></div>'
        '<div class="ds-barwrap">'
        '<div class="ds-barrow"><span>Software</span><span class="ds-bar"><i style="width:82%;background:var(--vx-orange-500)"></i></span><span class="ds-v">82</span></div>'
        '<div class="ds-barrow"><span>Énergie</span><span class="ds-bar"><i style="width:61%;background:var(--vx-copper-light)"></i></span><span class="ds-v">61</span></div>'
        '<div class="ds-barrow"><span>Positif</span><span class="ds-bar"><i style="width:48%;background:var(--vx-positive)"></i></span><span class="ds-v">48</span></div>'
        '<div class="ds-barrow"><span>Risque</span><span class="ds-bar"><i style="width:27%;background:var(--vx-negative)"></i></span><span class="ds-v">27</span></div>'
        '</div></div>')

    # États
    states = (
        '<div class="vx-grid" style="grid-template-columns:repeat(2,1fr);gap:14px">'
        '<div><div class="vx-kpi-label" style="margin-bottom:8px">Chargement (skeleton)</div>'
        '<div class="vx-skeleton-line"></div><div class="vx-skeleton-line" style="width:70%;margin-top:8px"></div>'
        '<div class="vx-skeleton-chart" style="margin-top:10px"></div></div>'
        '<div><div class="vx-kpi-label" style="margin-bottom:8px">État vide structuré</div>'
        '<div class="vx-state"><div class="vx-state-icon">—</div>'
        '<div style="font-weight:600;color:var(--vx-text-secondary)">Données de volatilité indisponibles</div>'
        '<div class="ds-note" style="margin:4px 0 8px">La source actuelle ne fournit pas les informations nécessaires à cette visualisation.</div>'
        '<div class="ds-row"><button class="vx-btn vx-btn-secondary vx-btn-sm" data-ds-copy="vx-state-action">Actualiser</button>'
        '<button class="vx-btn vx-btn-ghost vx-btn-sm" data-ds-copy="vx-state-action">Diagnostiquer</button></div></div></div>'
        '</div>'
        '<div style="margin-top:14px" class="vx-stale-banner">Bandeau STALE — données périmées, affichées honnêtement.</div>')

    # Surfaces
    surfaces = (
        '<div class="ds-row" style="gap:16px;align-items:stretch">'
        '<div class="vx-card vx-card--compact" style="flex:1;min-width:180px"><div class="vx-card-body">'
        '<div class="vx-kpi-label">LEVEL 1</div><div style="color:var(--vx-text-secondary);font-size:12.5px;margin-top:4px">Panneau standard · surface graphite, bordure fine.</div></div></div>'
        '<div class="vx-card vx-elevated" style="flex:1;min-width:180px"><div class="vx-card-body">'
        '<div class="vx-kpi-label">LEVEL 2</div><div style="color:var(--vx-text-secondary);font-size:12.5px;margin-top:4px">Carte surélevée · relief, highlight interne.</div></div></div>'
        '<div class="vx-card vx-card--hero" style="flex:1.4;min-width:220px"><div class="vx-card-body">'
        '<div class="vx-kpi-label">LEVEL 3 — HERO</div><div style="color:var(--vx-text-secondary);font-size:12.5px;margin-top:4px">Carte dominante · rayon généreux, profondeur, contrôles intégrés.</div></div></div>'
        '</div>')

    # Rayons & élévation
    radii = ('<div class="ds-radii">'
             '<div style="border-radius:var(--vx-r-sm)">r-sm 8</div>'
             '<div style="border-radius:var(--vx-r)">r 12</div>'
             '<div style="border-radius:var(--vx-r-lg)">r-lg 14</div>'
             '<div style="border-radius:var(--vx-r-modal)">r-modal 16</div>'
             '<div style="border-radius:999px">pill</div></div>'
             '<div class="ds-elev" style="margin-top:16px">'
             '<div style="box-shadow:var(--vx-shadow-1)">shadow-1</div>'
             '<div style="box-shadow:var(--vx-shadow-2)">shadow-2</div>'
             '<div style="box-shadow:var(--vx-shadow-modal)">shadow-modal</div>'
             '<div style="box-shadow:var(--vx-glow-brand)">glow-brand</div></div>')

    intro = ('<section class="vx-card vx-card--hero vx-col-12" aria-label="Design System">'
             '<div class="vx-card-body">'
             '<div class="vx-kpi-label" style="color:var(--vx-brand-strong)">VERTEX BLACK GLASS · DESIGN SYSTEM</div>'
             '<h1 style="font-size:30px;font-weight:750;letter-spacing:-.02em;margin:6px 0 8px;color:var(--vx-text-primary)">Référence visuelle unique</h1>'
             '<p class="ds-note">Tous les éléments ci-dessous sont rendus avec les <b>vrais tokens</b> '
             '(<code>tokens.css</code>) et les <b>vraies classes</b> de composants. Une couleur = une '
             'signification · le bleu n’est jamais une identité · cuivre = marque & action · '
             'vert = positif · corail = risque · violet = options.</p></div></section>')

    return (_DS_CSS + '<div class="vx-grid vx-page-enter">'
            + intro
            + sec('Palette — noirs & graphites', 'fonds obsidienne', _swatches(_BG))
            + sec('Palette — rampe de marque (alias historiques)', 'blanc-gris en verre', _swatches(_COPPER))
            + sec('Palette — sémantiques', 'positif · négatif · warning · options', _swatches(_SEM), span='6')
            + sec('Palette — texte', 'blanc cassé + gris chauds', _swatches(_TEXT), span='6')
            + sec('Typographie', 'hiérarchie', type_rows)
            + sec('Surfaces', 'niveaux 1 → 3', surfaces)
            + sec('KPI', 'bande de métriques', kpi_body, span='6')
            + sec('Badges & statuts', 'pills', badges, span='6')
            + sec('Boutons', 'variantes & états', btns)
            + sec('Onglets & segmented', 'navigation interne', tabs, span='6')
            + sec('Jauges · anneaux · barres', 'visualisations intégrées', gauge, span='6')
            + sec('États', 'chargement · vide · périmé', states)
            + sec('Rayons & élévation', 'formes & profondeur', radii)
            + '<section class="vx-card vx-col-12"><div class="vx-card-header">'
              '<span class="vx-card-title">Vertex 2.0 — Black Glass, Signal Light</span>'
              '<span class="vx-card-title" style="color:var(--vx-text-muted);'
              'font-weight:500">primitives canoniques de la refonte visuelle</span>'
              '</div><div class="vx-card-body"><p class="vx2-question">'
              'Ci-dessous, les primitives de <code>vertex.ui.vx2</code> rendues '
              'avec leur vrai balisage. Les valeurs sont des exemples de mise en '
              'forme : aucune n\u2019est une mesure et aucune n\u2019est pr\u00e9sent\u00e9e '
              'comme r\u00e9elle.</p></div></section>'
            + _galerie_2_0()
            + '</div>')


_DS_JS = """<script>
/* Design System — délégation : clic sur un échantillon [data-ds-copy] copie sa
   classe dans le presse-papiers et affiche un toast. Purement démonstratif. */
document.addEventListener('click', function(e){
  var el = e.target.closest('[data-ds-copy]');
  if(!el) return;
  var cls = el.getAttribute('data-ds-copy') || '';
  try{ if(navigator.clipboard) navigator.clipboard.writeText('.' + cls.split(' ').join('.')); }catch(_){}
  /* Meme defaut qu'au simulateur : le nom global appele n'existe pas, la
     garde le rendait silencieux. Le helper servi est `VX.toast`. */
  if(window.VX && typeof VX.toast === 'function')
    VX.toast('Classe copiée : ' + cls, 'success');
});
</script>"""


def render() -> str:
    return render_shell(
        title='Design System',
        active='system',
        space_label='Design System',
        sub_label='Référence',
        page_label='Design System',
        content=_content(),
        page_js=_DS_JS,
    )
