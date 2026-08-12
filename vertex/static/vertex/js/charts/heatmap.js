/* heatmap.js — matrice HTML accessible pour secteurs, corrélations, IV et
   scénarios. Les valeurs restent du texte réel ; le scroll est contenu dans
   la carte et la couleur ne remplace jamais le libellé chiffré. */
(function(){
'use strict';
const C=window.VXCharts=window.VXCharts||{},VX=window.VX;
let heatmapUid=0;

function esc(value){
  return String(value==null?'':value).replace(/[&<>"']/g,c=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function rgbOf(hex){
  const m=/^#([0-9A-Fa-f]{6})$/.exec(hex||'');
  if(!m)return null;
  const n=parseInt(m[1],16);
  return ((n>>16)&255)+','+((n>>8)&255)+','+(n&255);
}
function tOf(v,min,max){
  if(v===null||v===undefined||(typeof v!=='number'&&typeof v!=='string')
      ||(typeof v==='string'&&!v.trim()))return null;
  const numeric=Number(v);
  if(!Number.isFinite(numeric))return null;
  return Math.max(-1,Math.min(1,(numeric-(min+max)/2)/((max-min)/2||1)));
}
/* L'intensité reste contenue : fond mat, liseré sémantique, encre stable. */
function cellStyle(v,min,max,dominant,negative,positive){
  const t=tOf(v,min,max);
  if(t===null)
    return 'background:var(--vx-surface-elevated);color:var(--vx-text-muted);border-radius:5px';
  const rgb=rgbOf(t>=0?positive:negative)||'128,128,128';
  const a=.06+.18*Math.abs(t);
  return 'background:rgba('+rgb+','+a.toFixed(2)+');'
    +'box-shadow:inset 0 0 0 '+(dominant?'1.5px':'1px')+' rgba('+rgb+','+(dominant?'.72':Math.min(.44,a+.14).toFixed(2))+');'
    +'color:var(--vx-text-primary);font-weight:'+(dominant?'800':'650')+';border-radius:5px';
}

C.heatmapCard=function(host,opts){
  /* opts: rows[{label,cells[{value,label?,title?,onclick?}]}], columns[],
     min,max,fmt,negativeColor?,positiveColor?,source,timestamp,mode,limits */
  opts=opts||{};
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return null;
  el.classList.add('vx-card','vx-chart-card');
  const fmt=opts.fmt||((v)=>VX.fmt.num(v,1));
  const mn=opts.min??-3,mx=opts.max??3;
  const negative=opts.negativeColor||C.colors.negative;
  const positive=opts.positiveColor||C.colors.positive;
  const rows=Array.isArray(opts.rows)?opts.rows:[];
  const columns=Array.isArray(opts.columns)?opts.columns:[];
  const id='vxhm-'+(++heatmapUid);

  /* Cellule dominante = |t| max de la grille, uniquement parmi les valeurs
     réellement numériques. Une absence ne peut donc jamais gagner le focus. */
  let domT=0,domRow=-1,domCol=-1;
  rows.forEach((r,ri)=>(Array.isArray(r.cells)?r.cells:[]).forEach((c,ci)=>{
    const t=tOf(c&&c.value,mn,mx);
    if(t!==null&&Math.abs(t)>Math.abs(domT)){domT=t;domRow=ri;domCol=ci;}
  }));

  const head=columns.length?`<thead><tr><th scope="col"></th>${columns.map(c=>`<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>`:'';
  const body=rows.map((r,ri)=>{
    const cells=Array.isArray(r.cells)?r.cells:[];
    return `<tr><th scope="row">${esc(r.label)}</th>${cells.map((c,ci)=>{
      c=c||{};
      const available=tOf(c.value,mn,mx)!==null;
      const display=c.label!=null?c.label:(available?fmt(Number(c.value)):'n/d');
      const column=columns[ci]!=null?columns[ci]:('colonne '+(ci+1));
      const aria=`${r.label||'Ligne'}, ${column} : ${display}`;
      const interactive=!!c.onclick;
      return `<td class="vx-num vx-heatmap-cell" title="${esc(c.title||aria)}" aria-label="${esc(aria)}" style="${cellStyle(c.value,mn,mx,ri===domRow&&ci===domCol,negative,positive)}"${interactive?` data-hm="${esc(c.onclick)}" role="link" tabindex="0"`:''}>${esc(display)}</td>`;
    }).join('')}</tr>`;
  }).join('');

  let scaleBody;
  if(mn<0&&mx>0){
    scaleBody=`<span>${esc(fmt(mn))}</span><i aria-hidden="true"></i><span>${esc(fmt(0))}</span><i aria-hidden="true"></i><span>${esc(fmt(mx))}</span>`;
  }else if(mx<=0){
    scaleBody=`<span>${esc(fmt(mn))}</span><i class="vx-heatmap-scale-negative" aria-hidden="true"></i><span>${esc(fmt(mx))}</span>`;
  }else{
    scaleBody=`<span>${esc(fmt(mn))}</span><i class="vx-heatmap-scale-positive" aria-hidden="true"></i><span>${esc(fmt(mx))}</span>`;
  }
  const scale=`<div class="vx-heatmap-scale" role="img" aria-label="Échelle de couleur, de ${esc(fmt(mn))} à ${esc(fmt(mx))}">${scaleBody}</div>`;
  const question=opts.question||'';
  const conclusion=opts.conclusion||'';
  const summary=opts.summary||conclusion||question||opts.title||'Matrice de données';
  const provenance=(opts.source||opts.timestamp)?VX.updateIndicator(opts.timestamp,opts.source,opts.mode):'';
  const foot=(provenance||opts.limits)?`<div class="vx-chart-foot">
    ${provenance?`<span class="vx-chart-provenance">${provenance}</span>`:''}
    ${opts.limits?`<span class="vx-meta">${esc(opts.limits)}</span>`:''}</div>`:'';
  const content=rows.length?`<div class="vx-heatmap-scroll" role="region" tabindex="0" aria-label="${esc(opts.title||'Heatmap')} — tableau défilant horizontalement">
      <table class="vx-heatmap-table"><caption class="vx-sr-only">${esc(summary)}</caption>${head}<tbody>${body}</tbody></table></div>${scale}`
    :`<div class="vx-state" data-state="empty" role="status"><div class="vx-state-icon">—</div><div><b>Donnée indisponible</b><br>${esc(opts.stateMessage||question||'Aucune cellule à afficher.')}</div></div>`;

  el.innerHTML=`<div class="vx-chart-head"><h3 class="vx-chart-title" id="${id}-title">${esc(opts.title||'')}</h3>
    ${(opts.timeframe||opts.unit||opts.freshness)?`<span class="vx-chart-meta">
      ${opts.timeframe?`<span class="vx-badge">${esc(opts.timeframe)}</span>`:''}
      ${opts.unit?`<span class="vx-badge vx-badge-unit">${esc(opts.unit)}</span>`:''}
      ${C.freshnessBadge?C.freshnessBadge(opts.freshness):''}</span>`:''}
    ${question&&!conclusion?`<span class="vx-chart-question">${esc(question)}</span>`:
      (question?`<span class="vx-sr-only">${esc(question)}</span>`:'')}
    ${conclusion?`<span class="vx-chart-conclusion">${esc(conclusion)}</span>`:''}</div>
    ${content}${foot}`;
  el.querySelectorAll('[data-hm]').forEach(td=>{
    const open=()=>{location.href=td.dataset.hm;};
    td.addEventListener('click',open);
    td.addEventListener('keydown',event=>{
      if(event.key==='Enter'||event.key===' '){event.preventDefault();open();}
    });
  });
  return el;
};
})();
