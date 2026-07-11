/* option-theta.js — décomposition temps depuis la simulation moteur. */
(function(){const C=window.VXCharts,VX=window.VX;
C.thetaCard=function(host,sim,opts){
  const td=(sim&&sim.time_decay)||[];
  if(!td.length){const el=typeof host==='string'?document.getElementById(host):host;
    if(el)el.innerHTML=VX.states.empty('Décomposition temps indisponible.');return null;}
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,
    td.map(t=>'J+'+t.days),td.map(t=>t.value),{color:C.colors.warning,yFmt:(v)=>VX.fmt.num(v,1)})}));};
})();
