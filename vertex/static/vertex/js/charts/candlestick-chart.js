/* candlestick-chart.js — chandeliers OHLC + overlays de moyennes mobiles (§12).
   Bougies rendues UNIQUEMENT si des barres OHLC complètes sont fournies par les
   moteurs — jamais reconstituées côté UI (donnée absente = repli honnête sur
   price-chart, limitation affichée). Les overlays (MM20/MM50/MM200…) sont des
   séries RÉELLES calculées côté serveur, superposées en lignes interactives.
   Tooltip index + crosshair Chart.js, niveaux du plan et marqueurs d'événements
   conservés. */
(function () {
  const C = window.VXCharts, VX = window.VX;

  function shownOverlays(overlays) {
    return (overlays || []).filter(function (o) {
      return o && o.data && o.data.some(function (x) { return x != null; });
    });
  }
  function overlayLegend(overlays) {
    return shownOverlays(overlays).map(function (o) { return { label: o.label, color: o.color }; });
  }
  function overlayLineDatasets(overlays) {
    return shownOverlays(overlays).map(function (o) {
      return { type: 'line', label: o.label, data: o.data, borderColor: o.color,
        borderWidth: o.width || 1.3, pointRadius: 0, pointHoverRadius: 0, tension: .12,
        fill: false, spanGaps: true, borderDash: o.dash || [], order: 0 };
    });
  }

  C.candlestickCard = function (host, opts) {
    const bars = opts.bars || [];
    const ok = bars.length >= 2 && bars.every(function (b) {
      return [b.o, b.h, b.l, b.c].every(function (x) { return x !== null && x !== undefined; });
    });
    const overlays = opts.overlays || [];

    if (!ok) {
      /* Repli honnête : clôtures + mêmes overlays (priceCard attend `values`). */
      return C.priceCard(host, Object.assign({}, opts, {
        closes: bars.map(function (b) { return b.c; }).filter(function (x) { return x != null; }).length
          ? bars.map(function (b) { return b.c; }) : (opts.closes || []),
        overlays: shownOverlays(overlays).map(function (o) {
          return { label: o.label, values: o.data, color: o.color }; }),
        limits: (opts.limits ? opts.limits + ' · ' : '') + 'OHLC indisponible — tracé en clôtures (aucune bougie inventée)',
      }));
    }

    const legend = (opts.legend || []).concat(overlayLegend(overlays));
    return C.card(host, Object.assign({}, opts, { legend: legend, render: function (cv) {
      return C.mount(cv, {
        type: 'bar',
        data: { labels: opts.labels, datasets: [
          { label: 'wick', data: bars.map(function (b) { return [b.l, b.h]; }),
            backgroundColor: bars.map(function (b) { return (b.c >= b.o ? C.colors.positive : C.colors.negative) + '99'; }),
            maxBarThickness: 1.5, grouped: false, order: 3 },
          { label: 'candle', data: bars.map(function (b) { return [Math.min(b.o, b.c), Math.max(b.o, b.c)]; }),
            backgroundColor: bars.map(function (b) { return b.c >= b.o ? C.colors.positive : C.colors.negative; }),
            maxBarThickness: 7, grouped: false, order: 2 },
        ].concat(overlayLineDatasets(overlays)) },
        options: { interaction: { mode: 'index', intersect: false }, scales: C.axes({}),
          plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (ctx) {
            if (ctx.dataset.type === 'line') return ctx.dataset.label + ' : ' + (ctx.parsed.y == null ? '—' : VX.fmt.price(ctx.parsed.y));
            if (ctx.dataset.label === 'wick') return null;
            const b = bars[ctx.dataIndex];
            return 'O ' + b.o + ' · H ' + b.h + ' · L ' + b.l + ' · C ' + b.c;
          } } } } },
        plugins: [C.levelLines(opts.levels || []), C.eventMarkers(opts.events || [])],
      });
    } }));
  };
})();
