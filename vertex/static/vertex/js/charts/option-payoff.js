/* option-payoff.js — payoff à l'échéance depuis strike/prime FOURNIS.
   P&L par prix du sous-jacent = arithmétique du contrat (pas un modèle). */
(function(){const C=window.VXCharts,VX=window.VX;
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
  /* Repères RÉELS optionnels : bande ± mouvement attendu (em_pct) et objectif (tgt).
     Dessinés en pixels sur l'axe x (indices de la grille xs). */
  const emPct=(typeof opts.expectedMovePct==='number')?opts.expectedMovePct:null;
  const tgt=(typeof opts.target==='number')?opts.target:null;
  const sToIdx=(s)=>{const f=(s/s0-0.7)/0.6*40;return Math.max(0,Math.min(40,f));};
  const marks={id:'vxPayoffMarks',beforeDatasetsDraw(chart){
    const a=chart.chartArea,sx=chart.scales.x,g=chart.ctx;if(!sx)return;g.save();
    if(emPct!=null){const lo=sx.getPixelForValue(sToIdx(s0*(1-emPct/100))),hi=sx.getPixelForValue(sToIdx(s0*(1+emPct/100)));
      g.fillStyle='rgba(192,183,159,.10)';g.fillRect(Math.min(lo,hi),a.top,Math.abs(hi-lo),a.bottom-a.top);
      g.fillStyle='rgba(192,183,159,.55)';g.font='9px sans-serif';g.fillText('mouvement attendu ±'+emPct.toFixed(1)+' %',Math.min(lo,hi)+4,a.top+11);}
    const vline=(s,col,lbl)=>{const x=sx.getPixelForValue(sToIdx(s));if(x<a.left||x>a.right)return;
      g.strokeStyle=col;g.setLineDash([4,3]);g.beginPath();g.moveTo(x,a.top);g.lineTo(x,a.bottom);g.stroke();g.setLineDash([]);
      g.fillStyle=col;g.font='9px sans-serif';g.fillText(lbl,x+3,a.bottom-4);};
    vline(be,'rgba(255,255,255,.35)','breakeven');
    if(tgt!=null)vline(tgt,'rgba(54,200,137,.6)','objectif');
    g.restore();}};
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.mount(cv,{type:'line',
    data:{labels:xs,datasets:[{data:ys,borderColor:C.colors.violet,borderWidth:1.8,pointRadius:0,
      fill:{target:{value:0},above:'#36c88922',below:'#ed655c22'}}]},
    options:{scales:C.axes({yFmt:(v)=>v+' %'}),plugins:{tooltip:{callbacks:{
      label:(ctx)=>`P&L à l'échéance : ${ctx.parsed.y} %`}}}},
    plugins:[marks]})}));};
})();
