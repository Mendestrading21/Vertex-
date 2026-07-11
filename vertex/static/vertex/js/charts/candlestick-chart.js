/* candlestick-chart.js — chandeliers OHLC. Rendu UNIQUEMENT si des barres
   OHLC complètes sont fournies par les moteurs — jamais reconstituées côté
   UI (donnée absente = repli honnête sur price-chart, limitation affichée). */
(function(){const C=window.VXCharts;
C.candlestickCard=function(host,opts){
  const bars=opts.bars||[];
  const ok=bars.length>=2&&bars.every(b=>[b.o,b.h,b.l,b.c].every(x=>x!==null&&x!==undefined));
  if(!ok){
    return C.priceCard(host,Object.assign({},opts,{
      closes:bars.map(b=>b.c).filter(x=>x!=null).length?bars.map(b=>b.c):(opts.closes||[]),
      limits:(opts.limits?opts.limits+' · ':'')+'OHLC indisponible — tracé en clôtures (aucune bougie inventée)'}));
  }
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.mount(cv,{
    type:'bar',
    data:{labels:opts.labels,datasets:[
      {/* mèches */ data:bars.map(b=>[b.l,b.h]),backgroundColor:bars.map(b=>b.c>=b.o?'#22C77A88':'#EF535088'),maxBarThickness:1.5,grouped:false},
      {/* corps  */ data:bars.map(b=>[Math.min(b.o,b.c),Math.max(b.o,b.c)]),
        backgroundColor:bars.map(b=>b.c>=b.o?C.colors.positive:C.colors.negative),maxBarThickness:7,grouped:false}]},
    options:{scales:C.axes({}),plugins:{tooltip:{callbacks:{label:(ctx)=>{const b=bars[ctx.dataIndex];
      return `O ${b.o} · H ${b.h} · L ${b.l} · C ${b.c}`;}}}}},
    plugins:[C.levelLines((opts.levels)||[]),C.eventMarkers(opts.events||[])]})}));};
})();
