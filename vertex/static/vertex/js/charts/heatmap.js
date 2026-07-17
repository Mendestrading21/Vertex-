/* heatmap.js — heatmaps HTML/CSS (secteurs, corrélations, IV) : plus lisible
   et accessible qu'un canvas pour des grilles de petite taille. */
(function(){const C=window.VXCharts,VX=window.VX;
function cellColor(v,min,max){
  if(v===null||v===undefined||!isFinite(v))return'var(--vx-surface-elevated)';
  const t=Math.max(-1,Math.min(1,(v-(min+max)/2)/((max-min)/2||1)));
  /* Couleurs dérivées du thème (émeraude gains / corail pertes) — aucune divergence hors-thème. */
  const pos=(C.rgba&&C.rgba(C.colors.positive,.10+.4*t))||`rgba(54,200,137,${.10+.4*t})`;
  const neg=(C.rgba&&C.rgba(C.colors.negative,.10+.4*(-t)))||`rgba(237,101,92,${.10+.4*(-t)})`;
  return t>=0?pos:neg;}
C.heatmapCard=function(host,opts){
  /* opts: rows[{label,cells[{value,label?,title?,onclick?}]}], columns[], min,max, fmt */
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return;
  el.classList.add('vx-card','vx-chart-card');
  const fmt=opts.fmt||((v)=>VX.fmt.num(v,1));
  const head=opts.columns?`<tr><th></th>${opts.columns.map(c=>`<th>${c}</th>`).join('')}</tr>`:'';
  const body=(opts.rows||[]).map(r=>`<tr><th style="text-align:left">${r.label}</th>${
    r.cells.map(c=>`<td class="vx-num" title="${c.title||''}" style="background:${cellColor(c.value,opts.min??-3,opts.max??3)};cursor:${c.onclick?'pointer':'default'}" ${c.onclick?`data-hm="${c.onclick}"`:''}>${c.label??fmt(c.value)}</td>`).join('')}</tr>`).join('');
  el.innerHTML=`<div class="vx-chart-head"><span class="vx-chart-title">${opts.title||''}</span>
    ${opts.question?`<span class="vx-chart-question">${opts.question}</span>`:''}
    ${opts.conclusion?`<span class="vx-chart-conclusion">${opts.conclusion}</span>`:''}</div>
    <div class="vx-table-wrap" style="border:none"><table class="vx-table">${head}${body}</table></div>
    <div class="vx-chart-foot">${VX.updateIndicator(opts.timestamp,opts.source,opts.mode)}
    ${opts.limits?`<span class="vx-meta">${opts.limits}</span>`:''}</div>`;
  el.querySelectorAll('[data-hm]').forEach(td=>td.addEventListener('click',()=>{location.href=td.dataset.hm;}));};
})();
