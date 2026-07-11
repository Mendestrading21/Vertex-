/* Vertex Core — event bus, contexte de navigation, refresh manager,
   fraîcheur, toasts. Aucune logique financière ici : l'UI consomme les
   moteurs, elle ne recalcule rien. */
(function () {
  'use strict';
  const VX = window.VX = window.VX || {};

  /* ── Télémétrie d'erreurs (objectif 0-erreur : /api/client-log) ──── */
  function reportError(msg, src, line) {
    try {
      fetch('/api/client-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: location.pathname, msg: String(msg || '').slice(0, 300), src: String(src || '').slice(0, 160), line: line | 0 }),
      }).catch(() => {});
    } catch (e) {}
  }
  window.addEventListener('error', (e) => reportError(e.message, e.filename, e.lineno));
  window.addEventListener('unhandledrejection', (e) => {
    const r = e && e.reason;
    reportError('unhandledrejection: ' + ((r && r.message) ? r.message : String(r)).slice(0, 260), '', 0);
  });

  /* ── Event bus (§41) ─────────────────────────────────────────────── */
  const bus = new EventTarget();
  VX.bus = {
    on(name, fn) { bus.addEventListener(name, fn); return () => bus.removeEventListener(name, fn); },
    emit(name, detail) { bus.dispatchEvent(new CustomEvent(name, { detail })); },
  };
  VX.EVENTS = ['vx:favorites-changed', 'vx:watchlist-changed', 'vx:follow-changed',
    'vx:position-changed', 'vx:alert-changed', 'vx:thesis-changed',
    'vx:decision-updated', 'vx:data-refreshed', 'vx:connection-changed'];

  /* ── Formatage ───────────────────────────────────────────────────── */
  VX.fmt = {
    nd(v) { return (v === null || v === undefined || v === '' || (typeof v === 'number' && !isFinite(v))) ? '—' : v; },
    num(v, dec = 2) {
      if (v === null || v === undefined || !isFinite(v)) return '—';
      return Number(v).toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    },
    pct(v, dec = 2, signed = true) {
      if (v === null || v === undefined || !isFinite(v)) return '—';
      const s = signed && v > 0 ? '+' : '';
      return s + Number(v).toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + ' %';
    },
    price(v) { return VX.fmt.num(v, Math.abs(v) >= 1000 ? 0 : 2); },
    /* §38 : « À l'instant », « Il y a 8 min », « Aujourd'hui à 15:42 »… */
    ago(ts) {
      if (!ts) return '—';
      const d = (ts instanceof Date) ? ts : new Date(typeof ts === 'number' && ts < 1e12 ? ts * 1000 : ts);
      if (isNaN(d)) return '—';
      const s = Math.max(0, (Date.now() - d.getTime()) / 1000);
      if (s < 10) return 'À l’instant';
      if (s < 90) return `Il y a ${Math.round(s)} s`;
      if (s < 3600) return `Il y a ${Math.round(s / 60)} min`;
      const today = new Date(); const opts = { hour: '2-digit', minute: '2-digit' };
      if (d.toDateString() === today.toDateString()) return 'Aujourd’hui à ' + d.toLocaleTimeString('fr-FR', opts);
      const yest = new Date(Date.now() - 864e5);
      if (d.toDateString() === yest.toDateString()) return 'Hier à ' + d.toLocaleTimeString('fr-FR', opts);
      return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
    },
    isoFull(ts) {
      const d = (ts instanceof Date) ? ts : new Date(typeof ts === 'number' && ts < 1e12 ? ts * 1000 : ts);
      return isNaN(d) ? '' : d.toLocaleString('fr-FR');
    },
  };

  /* ── UpdateIndicator (§38) ───────────────────────────────────────── */
  VX.updateIndicator = function (ts, source, mode) {
    const modeLabel = { live: 'Live', delayed: 'Différé', fallback: 'Secours', error: 'Erreur' }[mode] || '';
    const parts = [VX.fmt.ago(ts)];
    if (source) parts.push(source + (modeLabel ? ' ' + modeLabel : ''));
    return `<span class="vx-update" data-mode="${mode || 'fallback'}" title="${VX.fmt.isoFull(ts)}">` +
      `<span class="vx-dot"></span>${parts.join(' · ')}</span>`;
  };

  /* ── États de données (§39) ──────────────────────────────────────── */
  VX.states = {
    loading(rows = 3) {
      let h = '<div class="vx-flex-col" aria-busy="true" data-state="loading">';
      for (let i = 0; i < rows; i++) h += `<div class="vx-skeleton" style="height:${i ? 14 : 22}px;width:${90 - i * 15}%"></div>`;
      return h + '</div>';
    },
    empty(reason, action) {
      return `<div class="vx-state" data-state="empty"><b>Aucune donnée</b><span>${reason || ''}</span>${action || ''}</div>`;
    },
    stale(ageText, source, impact) {
      return `<div class="vx-stale-banner" data-state="stale">⏳ Donnée rassise (${ageText}${source ? ' · ' + source : ''})` +
        `${impact ? ' — ' + impact : ' — décision ACTIONABLE bloquée'}</div>`;
    },
    error(cause, retryFn) {
      return `<div class="vx-error-banner" data-state="error">⚠ ${cause || 'Erreur de chargement'}` +
        `<button class="vx-btn vx-btn-sm" onclick="${retryFn || 'location.reload()'}">Réessayer</button>` +
        `<a class="vx-btn vx-btn-sm vx-btn-ghost" href="/system?view=data">Ouvrir Système</a></div>`;
    },
  };

  /* ── Toasts (§42 — jamais alert/confirm/prompt) ──────────────────── */
  VX.toast = function (message, tone = 'info', ms = 3200) {
    let host = document.querySelector('.vx-toasts');
    if (!host) { host = document.createElement('div'); host.className = 'vx-toasts'; host.setAttribute('role', 'status'); document.body.appendChild(host); }
    const t = document.createElement('div');
    t.className = 'vx-toast'; t.dataset.tone = tone; t.textContent = message;
    host.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity .3s'; setTimeout(() => t.remove(), 350); }, ms);
  };

  /* ── VXContext (§15) : conservation page/vue/filtres/scroll ─────── */
  const CTX_KEY = 'vxNavigationContext';
  VX.context = {
    _read() { try { return JSON.parse(sessionStorage.getItem(CTX_KEY) || 'null'); } catch (e) { return null; } },
    save(extra) {
      const url = new URL(location.href);
      const ctx = Object.assign({
        from: url.pathname, view: url.searchParams.get('view') || null,
        filters: VX.context._collectFilters(), scrollY: window.scrollY,
        label: document.querySelector('[data-page-label]')?.dataset.pageLabel || document.title,
        ts: Date.now(),
      }, extra || {});
      try { sessionStorage.setItem(CTX_KEY, JSON.stringify(ctx)); } catch (e) { /* quota */ }
      window.VXContext = ctx;
      return ctx;
    },
    get() { return window.VXContext || VX.context._read(); },
    clear() { try { sessionStorage.removeItem(CTX_KEY); } catch (e) {} window.VXContext = null; },
    _collectFilters() {
      const out = {};
      document.querySelectorAll('[data-filter-key]').forEach(el => {
        const k = el.dataset.filterKey;
        if (el.matches('.vx-chip')) { if (el.getAttribute('aria-pressed') === 'true') out[k] = el.dataset.filterValue || '1'; }
        else if (el.value) out[k] = el.value;
      });
      return out;
    },
    /* Restaure filtres + scroll si on revient sur la page d'origine. */
    restoreIfReturning() {
      const ctx = VX.context._read();
      if (!ctx || ctx.from !== location.pathname) return null;
      const view = new URL(location.href).searchParams.get('view') || null;
      if (ctx.view && view && ctx.view !== view) return null;
      Object.entries(ctx.filters || {}).forEach(([k, v]) => {
        document.querySelectorAll(`[data-filter-key="${k}"]`).forEach(el => {
          if (el.matches('.vx-chip')) { if ((el.dataset.filterValue || '1') === v) el.setAttribute('aria-pressed', 'true'); }
          else el.value = v;
        });
      });
      if (ctx.scrollY) requestAnimationFrame(() => window.scrollTo(0, ctx.scrollY));
      return ctx;
    },
  };
  /* Ouvre l'analyse en conservant le contexte — utilisé PARTOUT. */
  VX.openAnalysis = function (symbol, extra) {
    VX.context.save(Object.assign({ selectedSymbol: symbol }, extra || {}));
    VX.recentTickers.push(symbol);
    location.href = '/analysis/' + encodeURIComponent(symbol.toUpperCase());
  };

  /* ── Tickers récents ─────────────────────────────────────────────── */
  VX.recentTickers = {
    get() { try { return JSON.parse(localStorage.getItem('vxRecentTickers') || '[]'); } catch (e) { return []; } },
    push(sym) {
      sym = String(sym || '').toUpperCase(); if (!sym) return;
      const list = VX.recentTickers.get().filter(s => s !== sym); list.unshift(sym);
      try { localStorage.setItem('vxRecentTickers', JSON.stringify(list.slice(0, 12))); } catch (e) {}
    },
  };

  /* ── Refresh Manager (§40) ───────────────────────────────────────── */
  const cache = new Map();     // url -> {ts, data}
  const inflight = new Map();  // url -> Promise
  VX.fetch = function (url, { ttl = 30000, priority = 'normal', signal } = {}) {
    const hit = cache.get(url);
    if (hit && Date.now() - hit.ts < ttl) return Promise.resolve(hit.data);
    if (inflight.has(url)) return inflight.get(url);
    const ctl = new AbortController();
    if (signal) signal.addEventListener('abort', () => ctl.abort());
    const p = (async () => {
      let lastErr;
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          const r = await fetch(url, { signal: ctl.signal });
          if (!r.ok) throw new Error('HTTP ' + r.status);
          const data = await r.json();
          cache.set(url, { ts: Date.now(), data });
          if (cache.size > 80) cache.delete(cache.keys().next().value);
          return data;
        } catch (e) {
          lastErr = e;
          if (e.name === 'AbortError') throw e;
          await new Promise(res => setTimeout(res, 600 * (attempt + 1)));
        }
      }
      throw lastErr;
    })().finally(() => inflight.delete(url));
    inflight.set(url, p);
    return p;
  };
  VX.refresh = {
    _tasks: [], _suspended: false,
    register(fn, intervalMs, label) {
      const task = { fn, intervalMs, label, id: null };
      const run = () => { if (!document.hidden) { try { fn(); } catch (e) { console.error('[vx-refresh]', label, e); } } };
      task.id = setInterval(run, intervalMs);
      this._tasks.push(task);
      return task;
    },
    async runAll(btn) {
      if (btn) { btn.dataset.state = 'refreshing'; btn.disabled = true; }
      cache.clear();
      try {
        await Promise.allSettled(this._tasks.map(t => t.fn()));
        VX.bus.emit('vx:data-refreshed', {});
        if (btn) { btn.dataset.state = 'success'; VX.toast('Données actualisées', 'success'); }
      } catch (e) { if (btn) btn.dataset.state = 'error'; }
      if (btn) setTimeout(() => { btn.dataset.state = 'ready'; btn.disabled = false; }, 900);
    },
  };
  /* Suspendre en arrière-plan, rafraîchir au retour. */
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) VX.bus.emit('vx:data-refreshed', { reason: 'visibility' });
  });
})();
