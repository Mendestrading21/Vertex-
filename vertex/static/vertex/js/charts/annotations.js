/* annotations.js — ré-export des plugins d'annotation (niveaux, événements)
   définis dans chart-core (levelLines, eventMarkers) + création d'alerte
   depuis un niveau réel du graphique. */
(function(){const C=window.VXCharts,VX=window.VX;
C.alertFromLevel=function(sym,level){
  if(level===null||level===undefined||!isFinite(level))return;
  window.VXEntities?.openAddModal(String(sym).toUpperCase(),'alert');
  setTimeout(()=>{const f=document.getElementById('f-level');if(f)f.value=Math.round(level*100)/100;},60);};
})();
