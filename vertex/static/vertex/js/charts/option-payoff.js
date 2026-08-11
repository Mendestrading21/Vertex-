/* option-payoff.js — payoff à l'échéance depuis strike/prime FOURNIS.
   P&L par prix du sous-jacent = arithmétique du contrat (pas un modèle).
   LOT 124 — finition « ultra propre » : le BREAKEVEN (le chiffre éducatif
   d'un payoff) et le SPOT sont enfin TRACÉS (lignes verticales nommées),
   zones gain/perte sur tokens, trait fin + halo doux.
   LOT 192 (tournée TV) — zones gain/perte HACHURÉES (équivalent canvas du
   tvHatch SVG : le payoff à l'échéance est une ESTIMATION, pas un réel)
   + libellés de zones GAIN/PERTE de part et d'autre du breakeven. */
(function(){const C=window.VXCharts=window.VXCharts||{},VX=window.VX;
/* hachures 45° dans la grammaire tvHatch (teinte faible + rayures fines) */
function _hatch(color){
  const t=document.createElement('canvas');t.width=8;t.height=8;
  const g=t.getContext('2d');
  g.globalAlpha=.08;g.fillStyle=color;g.fillRect(0,0,8,8);
  g.globalAlpha=.38;g.strokeStyle=color;g.lineWidth=1.4;
  g.beginPath();
  g.moveTo(-2,10);g.lineTo(10,-2);
  g.moveTo(-2,2);g.lineTo(2,-2);
  g.moveTo(6,10);g.lineTo(10,6);
  g.stroke();
  return g.createPattern(t,'repeat');}
C.payoffCard=function(host,opts){
  /* opts: spot, strike, premium, right('C'|'P'), breakeven */
  const s0=opts.spot,K=opts.strike,prem=opts.premium,right=opts.right||'C';
  if([s0,K,prem].some(v=>v===null||v===undefined)){
    const el=typeof host==='string'?document.getElementById(host):host;
    if(el)el.innerHTML=VX.states.empty('Contrat incomplet — payoff non tracé (aucune donnée inventée).');
    return null;}
  const xs=[],ys=[];
  for(let i=0;i<=40;i++){const s=s0*(0.7+0.6*i/40);xs.push(VX.fmt.price(s));
    const intr=right==='C'?Math.max(0,s-K):Math.max(0,K-s);
    ys.push(Math.round(((intr-prem)/prem)*1000)/10);}
  const be=opts.breakeven??(right==='C'?K+prem:K-prem);
  /* index (fraction continue) d'un prix sur l'axe 0.7·s0 → 1.3·s0 */
  const idxOf=(p)=>Math.max(0,Math.min(40,((p/s0)-0.7)/0.6*40));
  const marks={id:'vxPayoffMarks',afterDatasetsDraw(chart){
    const a=chart.chartArea,sx=chart.scales.x,g=chart.ctx;
    const mark=(idx,label,col,dy)=>{const x=sx.getPixelForValue(idx);
      if(!isFinite(x)||x<a.left||x>a.right)return;
      g.save();g.strokeStyle=col;g.setLineDash([3,3]);g.lineWidth=1;
      g.beginPath();g.moveTo(x,a.top);g.lineTo(x,a.bottom);g.stroke();g.setLineDash([]);
      g.fillStyle=col;g.font='700 9px sans-serif';g.textAlign='center';
      g.fillText(label,x,a.top+dy);g.restore();};
    mark(idxOf(s0),'spot',C.colors.info,10);
    mark(idxOf(be),'BE '+VX.fmt.price(be),C.colors.warning,22);
    /* libellés de zones TV : GAIN du côté profitable du BE, PERTE de l'autre */
    const xb=Math.max(a.left,Math.min(a.right,sx.getPixelForValue(idxOf(be))));
    const gainRight=right==='C';
    const zone=(x,label,col)=>{g.save();g.fillStyle=col;g.globalAlpha=.85;
      g.font='800 8.5px sans-serif';g.textAlign='center';
      g.fillText(label,x,a.bottom-6);g.restore();};
    if(xb-a.left>34)zone((a.left+xb)/2,gainRight?'PERTE':'GAIN',gainRight?C.colors.negative:C.colors.positive);
    if(a.right-xb>34)zone((xb+a.right)/2,gainRight?'GAIN':'PERTE',gainRight?C.colors.positive:C.colors.negative);
  }};
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.mount(cv,{type:'line',
    data:{labels:xs,datasets:[{data:ys,borderColor:C.colors.violet,borderWidth:1.6,pointRadius:0,
      fill:{target:{value:0},above:_hatch(C.colors.positive),below:_hatch(C.colors.negative)}}]},
    options:{scales:C.axes({yFmt:(v)=>v+' %'}),plugins:{tooltip:{callbacks:{
      label:(ctx)=>`P&L à l'échéance : ${ctx.parsed.y} %`}}}},
    plugins:[C.softGlowPlugin(),marks]})}));};
})();
