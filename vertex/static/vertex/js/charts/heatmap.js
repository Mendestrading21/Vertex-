/* heatmap.js — heatmaps HTML/CSS (secteurs, corrélations, IV, scénarios
   options) : plus lisible et accessible qu'un canvas pour des grilles de
   petite taille.
   LOT 127 — matière VERRE : les anciens rgba verts/rouges hors palette sont
   remplacés par les TOKENS (C.colors.positive/negative convertis en rgb) ;
   chaque cellule est une tuile — dégradé diagonal de sa propre couleur
   (dense en haut-gauche → doux en bas-droit, même grammaire que treemap/
   barres), liseré fin de la couleur, coins arrondis, grille aérée. */
(function(){const C=window.VXCharts=window.VXCharts||{},VX=window.VX;
function rgbOf(hex){
  const m=/^#([0-9A-Fa-f]{6})$/.exec(hex||'');
  if(!m)return null;
  const n=parseInt(m[1],16);
  return ((n>>16)&255)+','+((n>>8)&255)+','+(n&255);}
function cellStyle(v,min,max){
  if(v===null||v===undefined||!isFinite(v))
    return 'background:var(--vx-surface-elevated);border-radius:5px';
  const t=Math.max(-1,Math.min(1,(v-(min+max)/2)/((max-min)/2||1)));
  const rgb=rgbOf(t>=0?C.colors.positive:C.colors.negative)||'128,128,128';
  const a=.12+.42*Math.abs(t);
  return 'background:linear-gradient(135deg,rgba('+rgb+','+(a+.10).toFixed(2)+'),rgba('+rgb+','+(a*.55).toFixed(2)+'));'
    +'box-shadow:inset 0 0 0 1px rgba('+rgb+','+Math.min(.5,a+.15).toFixed(2)+');border-radius:5px';}
C.heatmapCard=function(host,opts){
  /* opts: rows[{label,cells[{value,label?,title?,onclick?}]}], columns[], min,max, fmt */
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return;
  el.classList.add('vx-card','vx-chart-card');
  const fmt=opts.fmt||((v)=>VX.fmt.num(v,1));
  const head=opts.columns?`<tr><th></th>${opts.columns.map(c=>`<th>${c}</th>`).join('')}</tr>`:'';
  const body=(opts.rows||[]).map(r=>`<tr><th style="text-align:left">${r.label}</th>${
    r.cells.map(c=>`<td class="vx-num" title="${c.title||''}" style="${cellStyle(c.value,opts.min??-3,opts.max??3)};cursor:${c.onclick?'pointer':'default'}" ${c.onclick?`data-hm="${c.onclick}"`:''}>${c.label??fmt(c.value)}</td>`).join('')}</tr>`).join('');
  el.innerHTML=`<div class="vx-chart-head"><span class="vx-chart-title">${opts.title||''}</span>
    ${opts.question?`<span class="vx-chart-question">${opts.question}</span>`:''}
    ${opts.conclusion?`<span class="vx-chart-conclusion">${opts.conclusion}</span>`:''}</div>
    <div class="vx-table-wrap" style="border:none"><table class="vx-table" style="border-collapse:separate;border-spacing:3px">${head}${body}</table></div>
    <div class="vx-chart-foot">${VX.updateIndicator(opts.timestamp,opts.source,opts.mode)}
    ${opts.limits?`<span class="vx-meta">${opts.limits}</span>`:''}</div>`;
  el.querySelectorAll('[data-hm]').forEach(td=>td.addEventListener('click',()=>{location.href=td.dataset.hm;}));};
})();
