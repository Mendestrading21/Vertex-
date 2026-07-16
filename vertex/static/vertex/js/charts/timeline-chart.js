/* timeline-chart.js — chronologie d'événements (HTML sémantique). */
(function(){const VX=window.VX;
window.VXCharts.timelineCard=function(host,opts){
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return;
  el.classList.add('vx-card');
  const items=(opts.items||[]).map(it=>`<div class="vx-flex" style="align-items:flex-start;padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
    <span class="vx-mono vx-meta" style="min-width:84px">${it.when||'—'}</span>
    <span class="vx-badge" style="flex:none">${it.kind||''}</span>
    <span class="vx-grow" style="font-size:12.5px">${it.label}</span>
    ${it.sym?`<button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${it.sym}">${it.sym}</button>`:''}</div>`).join('');
  el.innerHTML=`<div class="vx-chart-head"><span class="vx-chart-title">${opts.title||''}</span>
    ${opts.controlsHtml?`<span class="vx-chart-controls">${opts.controlsHtml}</span>`:''}
    ${opts.question?`<span class="vx-chart-question">${opts.question}</span>`:''}</div>
    ${items||VX.states.empty(opts.emptyText||'Aucun événement à venir.')}
    <div class="vx-chart-foot">${VX.updateIndicator(opts.timestamp,opts.source,opts.mode)}</div>`;};
})();
