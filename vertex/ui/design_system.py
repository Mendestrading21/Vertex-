"""
vertex/ui/design_system.py — COUCHE DESIGN SYSTEM GLOBALE (polish premium).

Injectée sur TOUTES les pages, en amont du vx_kit. Uniquement du COSMÉTIQUE
universel et à faible spécificité : rien qui touche la logique, les données, ni
la mise en page des composants existants (pas de width/display/grid/padding
imposés). Elle harmonise ce qui, aujourd'hui, diffère d'une page à l'autre :
barres de défilement, focus clavier, sélection, tooltips, numéraux tabulaires,
transitions douces, respect de prefers-reduced-motion.

⛔ N'écrase aucun style de composant : les pages gardent la main (spécificité
supérieure). C'est une base, pas une refonte.
"""

CSS = r"""
/* ── Tokens Vertex canoniques (référence ; les composants VX les consomment) ── */
:root{
 --vx-accent:#ff7a18;--vx-accent2:#ff9a3d;--vx-good:#22c55e;--vx-good2:#16d17a;
 --vx-bad:#ef4444;--vx-info:#b9683d;--vx-warn:#f5b45b;--vx-neutral:#8794ab;
 --vx-ink:#eef2f8;--vx-ink2:#c9d2e0;--vx-mut:#8794ab;--vx-faint:#5c6577;
 --vx-hair:rgba(255,255,255,.08);--vx-hair2:rgba(255,255,255,.14);
 --vx-r-sm:8px;--vx-r:12px;--vx-r-lg:18px;--vx-r-pill:999px;
 --vx-s-1:4px;--vx-s-2:8px;--vx-s-3:12px;--vx-s-4:16px;--vx-s-5:24px;--vx-s-6:32px;
 --vx-ease:cubic-bezier(.4,0,.2,1);
}

/* ── Barres de défilement premium (uniformise les pages qui n'en ont pas) ── */
*{scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.18) transparent}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.14);border-radius:99px;border:2px solid transparent;background-clip:content-box}
::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,.28);background-clip:content-box}

/* ── Sélection & focus clavier accessibles ── */
::selection{background:rgba(255,122,24,.30);color:#fff}
:focus-visible{outline:2px solid var(--vx-accent);outline-offset:2px;border-radius:4px}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid var(--vx-accent);outline-offset:2px}

/* ── Numéraux tabulaires : alignement parfait des chiffres partout ── */
.num,.mono,[data-num],table td,table th{font-variant-numeric:tabular-nums lining-nums}

/* ── Transitions douces (base ; les composants restent maîtres) ── */
a,button{transition:color .15s var(--vx-ease),background-color .15s var(--vx-ease),border-color .15s var(--vx-ease),transform .12s var(--vx-ease),box-shadow .15s var(--vx-ease)}
button{cursor:pointer}
img{max-width:100%}
::placeholder{color:rgba(135,148,171,.6)}

/* ── Tooltip universel opt-in : ajoute data-tip="…" sur n'importe quel élément ── */
[data-tip]{position:relative}
[data-tip]:hover::after,[data-tip]:focus-visible::after{
 content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%);
 background:#12151c;color:#eef2f8;border:1px solid rgba(255,255,255,.16);border-radius:9px;
 padding:7px 11px;font:600 11.5px/1.4 ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;
 white-space:normal;width:max-content;max-width:260px;z-index:100000;pointer-events:none;
 box-shadow:0 10px 30px rgba(0,0,0,.45);animation:vxtipin .14s var(--vx-ease)}
[data-tip]:hover::before,[data-tip]:focus-visible::before{
 content:"";position:absolute;left:50%;bottom:calc(100% + 2px);transform:translateX(-50%);
 border:6px solid transparent;border-top-color:#12151c;z-index:100000;pointer-events:none}
@keyframes vxtipin{from{opacity:0;transform:translateX(-50%) translateY(3px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}

/* ── Accessibilité : respect du réglage « moins d'animations » ── */
@media(prefers-reduced-motion:reduce){
 *,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}
}
"""

__all__ = ['CSS']
