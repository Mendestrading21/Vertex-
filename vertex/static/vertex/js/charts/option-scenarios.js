/* option-scenarios.js — matrice scénarios (Stop/Flat/TP1-3 × temps) depuis
   la SIMULATION MOTEUR (scenario_pricer) — l'UI ne price rien. */
(function(){const C=window.VXCharts,VX=window.VX;
C.scenarioMatrix=function(host,sim,opts){
  const el=typeof host==='string'?document.getElementById(host):host;
  if(!el)return;
  const scen=sim&&sim.scenarios;
  if(!scen){el.innerHTML=VX.states.empty('Simulation moteur indisponible pour ce contrat.');return;}
  const order=['STOP','BEAR','FLAT','BASE','TP1','TP2','TP3'];
  const rows=order.filter(k=>scen[k]).map(k=>{
    const by=scen[k].by_time_days||{};
    return{label:`${k} (${VX.fmt.price(scen[k].spot)})`,
      cells:Object.entries(by).map(([d,v])=>({value:v.pnl_pct,label:VX.fmt.pct(v.pnl_pct,0),
        title:`J+${d} · valeur ${v.value}`}))};});
  const cols=Object.keys((scen.FLAT||scen.BASE||{}).by_time_days||{}).map(d=>'J+'+d);
  C.heatmapCard(el,Object.assign({rows,columns:cols,min:-60,max:60,
    limits:(sim.model_source||'')+' — estimation modèle, pas une promesse'},opts||{}));};
})();
