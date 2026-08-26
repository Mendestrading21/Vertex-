/* price-chart.js — graphique principal d'analyse : clôtures fournies par les
   moteurs + niveaux du PLAN moteur (entrée/stop/TP) + marqueurs earnings.
   L'UI ne recalcule AUCUN indicateur : les moyennes mobiles ne sont tracées
   que si le moteur les fournit (limitation documentée sinon). */
(function(){const C=window.VXCharts,VX=window.VX;
C.priceCard=function(host,opts){
  /* opts: labels, closes, plan{entry,stop,tp1,tp2,tp3}, events[{index,label}],
           overlays[{label,values,color}] (fournis par le moteur uniquement) */
  const plan=opts.plan||{};
  const levels=[
    {value:plan.entry,label:'Entrée',kind:'entry'},
    {value:plan.stop,label:'Stop',kind:'stop'},
    {value:plan.tp1,label:'TP1',kind:'tp'},
    {value:plan.tp2,label:'TP2',kind:'tp'},
    {value:plan.tp3,label:'TP3',kind:'tp'},
    {value:plan.resistance,label:'Résistance',kind:'resistance'},
    {value:plan.support,label:'Support',kind:'support'}];
  return C.card(host,Object.assign({},opts,{render:(cv)=>{
    const extra=(opts.overlays||[]).map((o,i)=>({data:o.values,label:o.label,
      borderColor:o.color||C.colors.series[(i+2)%6],borderWidth:1,pointRadius:0,tension:.2,fill:false}));
    const brand=C.colors.brand||'#c9cdd4';
    const chart=C.mount(cv,{type:'line',
      data:{labels:opts.labels,datasets:[{label:'Cours',data:opts.closes,borderColor:brand,
        borderWidth:1.7,pointRadius:0,tension:.15,fill:{target:'origin'},
        backgroundColor:(ctx)=>{const g=ctx.chart.ctx.createLinearGradient(0,0,0,ctx.chart.height||260);
          g.addColorStop(0,brand+'3A');g.addColorStop(1,brand+'00');return g;}},...extra]},
      options:{scales:C.axes({yFmt:(v)=>VX.fmt.price(v)}),interaction:{mode:'index',intersect:false}},
      plugins:[C.levelLines(levels),C.eventMarkers(opts.events||[])]});
    return chart;}}));};
})();
