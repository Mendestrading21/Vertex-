/* option-iv-sensitivity.js — sensibilité IV depuis la simulation moteur. */
(function(){const C=window.VXCharts,VX=window.VX;
C.ivSensitivityCard=function(host,sim,opts){
  const iv=(sim&&sim.iv_sensitivity)||[];
  if(!iv.length){const el=typeof host==='string'?document.getElementById(host):host;
    if(el)el.innerHTML=VX.states.empty('Sensibilité IV indisponible.');return null;}
  return C.barCard(host,Object.assign({},opts,{
    labels:iv.map(x=>(x.iv_shift_pct>0?'+':'')+x.iv_shift_pct+' %'),
    values:iv.map(x=>x.pnl_pct),yFmt:(v)=>v+' %'}));};
})();
