"""LOT 620 — contrats du nouveau shell analytique institutionnel.

Ces gardiens verrouillent les primitives partagées par les huit espaces. Ils ne
figent pas un pixel précis : ils empêchent le retour des layouts locaux, des
tables compactées à l'excès et d'un drawer qui déborde ou perd le focus.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'vertex/static/vertex/css/layout.css'
COMPONENTS = ROOT / 'vertex/static/vertex/css/components.css'
RESPONSIVE = ROOT / 'vertex/static/vertex/css/responsive.css'
TABLES = ROOT / 'vertex/static/vertex/css/tables.css'
SHELL_JS = ROOT / 'vertex/static/vertex/js/vx-shell.js'
SHELL_PY = ROOT / 'vertex/ui/shell/__init__.py'
REFERENCES = ROOT / 'docs/refactor/VISUAL_REFERENCE_MAP.md'


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def test_page_composition_primitives_are_shared_and_not_page_scoped():
    layout = _read(LAYOUT)
    components = _read(COMPONENTS)
    for selector in ('.vx-section-stack', '.vx-hero-grid', '.vx-insight-rail'):
        assert selector in layout
    for selector in ('.vx-page-lead', '.vx-kpi-strip', '.vx-toolbar',
                     '.vx-disclosure', '.vx-data-ledger', '.vx-readonly-shield'):
        assert selector in components
    assert 'grid-template-columns:minmax(0,2fr) minmax(260px,1fr)' in layout


def test_four_kpis_become_two_columns_and_hero_stacks_on_tablet():
    responsive = _read(RESPONSIVE)
    tablet = responsive[responsive.index('@media (max-width:1024px)'):]
    assert '.vx-hero-grid,.vx-hero-grid--wide' in tablet
    assert 'grid-template-columns:minmax(0,1fr)' in tablet
    assert '.vx-kpi-strip,.vx-kpi-strip[data-count="3"]' in responsive
    assert 'grid-template-columns:repeat(2,minmax(0,1fr))' in responsive


def test_drawer_supports_context_variants_footer_and_focus_loop():
    markup = _read(SHELL_PY)
    js = _read(SHELL_JS)
    css = _read(COMPONENTS)
    for node_id in ('vx-drawer-tabs', 'vx-drawer-body', 'vx-drawer-footer'):
        assert f'id="{node_id}"' in markup
    assert 'openDrawer(title, html, options)' in js
    assert "opts.variant === 'summary'" in js
    assert "opts.variant === 'detail'" in js
    assert "e.key !== 'Tab'" in js
    assert 'document.activeElement === first' in js
    assert 'document.activeElement === last' in js
    assert 'width:min(520px,40vw)' in css
    assert 'width:100vw;min-width:0;max-width:none' in _read(RESPONSIVE)


def test_financial_table_has_sticky_header_readable_rows_and_visible_affordance():
    css = _read(TABLES)
    assert 'height:40px' in css
    assert 'height:48px' in css
    assert '.vx-table-primary' in css
    assert '.vx-row-open' in css
    assert 'opacity:.58' in css
    assert 'font-family:var(--vx-font-mono)' in css
    assert 'font-size:10.5px' in css  # labels des cartes mobiles, plus 9.5 px


def test_reference_map_records_unique_corpus_and_rejects_visual_anti_patterns():
    doc = _read(REFERENCES)
    assert 'Dix-sept sont uniques' in doc
    assert 'E1654E95-662F-45DF-B385-565FA015E530.jpeg' in doc
    assert 'E95FBE06-D504-46C8-932A-B8ABAE021B01.jpeg' in doc
    assert '8CB3C7B2-9007-4B73-B5C4-44A461C244AB.jpeg' in doc
    assert 'Doublons confirmés par SHA-256' in doc
    assert 'glow permanent' in doc
    assert 'Buy/Sell' in doc
    assert '`n/d` ne devient jamais zéro' in ' '.join(doc.split())
