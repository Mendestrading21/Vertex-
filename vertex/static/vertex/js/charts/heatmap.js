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
function tOf(v,min,max){
  if(v===null||v===undefined||!isFinite(v))return null;
  return Math.max(-1,Math.min(1,(v-(min+max)/2)/((max-min)/2||1)));}
/* GRAMMAIRE TV (lot 194) : le texte de chaque cellule porte la COULEUR de son
   intensité (fondu avec |t|, comme les cartes secteurs TV), et la cellule
   DOMINANTE de la grille (|t| max) est en pleine intensité — liseré appuyé +
   gras 800 — pendant que les autres restent adoucies. */
function cellStyle(v,min,max,dominant){
  const t=tOf(v,min,max);
  if(t===null)
    return 'background:var(--vx-surface-elevated);border-radius:5px';
  const rgb=rgbOf(t>=0?C.colors.positive:C.colors.negative)||'128,128,128';
  const a=.12+.42*Math.abs(t);
  const txt=(.45+.55*Math.abs(t)).toFixed(2);
  return 'background:linear-gradient(135deg,rgba('+rgb+','+(a+.10).toFixed(2)+'),rgba('+rgb+','+(a*.55).toFixed(2)+'));'
    +'box-shadow:inset 0 0 0 '+(dominant?'1.6px':'1px')+' rgba('+rgb+','+(dominant?'.75':Math.min(.5,a+.15).toFixed(2))+');'
    +'color:rgba('+rgb+','+txt+');font-weight:'+(dominant?'800':'700')+';border-radius:5px';}
C.heatmapCard=function(host,opts){
  /* opts: rows[{label,cells[{value,label?,title?,onclick?}]}], columns[], min,max, fmt */
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return;
  el.classList.add('vx-card','vx-chart-card');
  const fmt=opts.fmt||((v)=>VX.fmt.num(v,1));
  const mn=opts.min??-3,mx=opts.max??3;
  /* cellule dominante = |t| max de TOUTE la grille (comptes réels, 1 seule) */
  let domT=0,domRow=-1,domCol=-1;
  (opts.rows||[]).forEach((r,ri)=>r.cells.forEach((c,ci)=>{
    const t=tOf(c.value,mn,mx);
    if(t!==null&&Math.abs(t)>Math.abs(domT)){domT=t;domRow=ri;domCol=ci;}}));
  const head=opts.columns?`<tr><th></th>${opts.columns.map(c=>`<th>${c}</th>`).join('')}</tr>`:'';
  const body=(opts.rows||[]).map((r,ri)=>`<tr><th style="text-align:left">${r.label}</th>${
    r.cells.map((c,ci)=>`<td class="vx-num" title="${c.title||''}" style="${cellStyle(c.value,mn,mx,ri===domRow&&ci===domCol)};cursor:${c.onclick?'pointer':'default'}" ${c.onclick?`data-hm="${c.onclick}"`:''}>${c.label??fmt(c.value)}</td>`).join('')}</tr>`).join('');
  el.innerHTML=`<div class="vx-chart-head"><span class="vx-chart-title">${opts.title||''}</span>
    ${opts.question?`<span class="vx-chart-question">${opts.question}</span>`:''}
    ${opts.conclusion?`<span class="vx-chart-conclusion">${opts.conclusion}</span>`:''}</div>
    <div class="vx-table-wrap" style="border:none"><table class="vx-table" style="border-collapse:separate;border-spacing:3px">${head}${body}</table></div>
    <div class="vx-chart-foot">${VX.updateIndicator(opts.timestamp,opts.source,opts.mode)}
    ${opts.limits?`<span class="vx-meta">${opts.limits}</span>`:''}</div>`;
  el.querySelectorAll('[data-hm]').forEach(td=>td.addEventListener('click',()=>{location.href=td.dataset.hm;}));};
})();
