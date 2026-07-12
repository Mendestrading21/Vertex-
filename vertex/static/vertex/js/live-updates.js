/* Vertex Live Updates — client SSE (§26).
   EventSource → VX.bus (vx:live:<canal>) avec : reconnexion automatique
   (Last-Event-ID géré par le navigateur), déduplication par id, repli
   polling adaptatif si SSE échoue, ralentissement onglet masqué,
   statut publié sur VX.bus ('vx:live-status'). Aucune exécution :
   les événements ne font que DÉCRIRE l'état serveur. */
(function () {
  'use strict';
  const VX = window.VX; if (!VX) return;
  let es = null, lastId = 0, failures = 0, pollTimer = null;
  let status = 'OFFLINE';

  function setStatus(s) {
    if (s === status) return;
    status = s;
    VX.bus.emit('vx:live-status', { status: s });
  }
  VX.liveStatus = () => status;

  function dispatch(ev) {
    if (!ev || typeof ev.id !== 'number' || ev.id <= lastId) return; /* dédup */
    lastId = ev.id;
    VX.bus.emit('vx:live:' + ev.channel, ev.data);
    VX.bus.emit('vx:data-refreshed', { channel: ev.channel, live: true });
  }

  function connect() {
    if (es || document.hidden) return;
    try {
      es = new EventSource('/api/live/events' + (lastId ? '?lastEventId=' + lastId : ''));
    } catch (e) { fallbackPolling(); return; }
    es.onopen = () => { failures = 0; setStatus('LIVE'); stopPolling(); };
    es.onerror = () => {
      es && es.close(); es = null;
      failures += 1;
      setStatus(failures > 3 ? 'FALLBACK' : 'DELAYED');
      if (failures > 3) fallbackPolling();
      else setTimeout(connect, Math.min(30000, 2000 * failures));
    };
    ['market', 'positions', 'options', 'portfolio', 'decisions',
     'alerts', 'connections', 'jobs', 'system'].forEach(ch => {
      es.addEventListener(ch, (m) => {
        try { dispatch(JSON.parse(m.data)); } catch (e) {}
      });
    });
  }

  /* Repli : polling adaptatif du statut live (le refresh manager par page
     continue de rafraîchir les données elles-mêmes). */
  function fallbackPolling() {
    if (pollTimer) return;
    const tick = async () => {
      try {
        await VX.fetch('/api/live/status', { ttl: 0 });
        setStatus('FALLBACK');
      } catch (e) { setStatus('OFFLINE'); }
    };
    tick();
    pollTimer = setInterval(() => { if (!document.hidden) tick(); }, 60000);
  }
  function stopPolling() { if (pollTimer) { clearInterval(pollTimer); pollTimer = null; } }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { es && es.close(); es = null; setStatus('DELAYED'); }
    else connect();
  });
  window.addEventListener('pagehide', () => { es && es.close(); es = null; });

  connect();
})();
