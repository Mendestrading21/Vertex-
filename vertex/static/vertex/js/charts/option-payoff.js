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
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.mount(cv,{type:'line',
    data:{labels:xs,datasets:[{data:ys,borderColor:C.colors.violet,borderWidth:1.8,pointRadius:0,
      fill:{target:{value:0},above:'#22C77A22',below:'#EF535022'}}]},
    options:{scales:C.axes({yFmt:(v)=>v+' %'}),plugins:{tooltip:{callbacks:{
      label:(ctx)=>`P&L à l'échéance : ${ctx.parsed.y} %`}}}}})}));};
})();
