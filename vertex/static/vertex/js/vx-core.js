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

  /* ── Échappement HTML (labels de tuiles, texte injecté en innerHTML) ── */
  VX.esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };

  /* ── Tuiles KPI partagées (CMP-02 : source UNIQUE du markup) ──────────
     Émettent le markup CANONIQUE déjà stylé par premium.css / glass.css —
     aucune classe visuelle nouvelle. Un seul argument `tone`
     ('pos'|'neg'|'warn'|'brand'|'') mappé au bon mécanisme selon la forme
     (data-tone pour metric/stat ; classe .vx-pos/.vx-neg pour kpi).
     Valeurs via VX.fmt.nd → absence rendue « — », jamais 0 (règle n°4).
     Les libellés sont échappés ; la valeur est passée telle quelle (déjà
     formatée par l'appelant via VX.fmt). */
  var _toneAttr = function (t) { return (['pos', 'neg', 'warn', 'brand', 'opt'].indexOf(t) >= 0 ? t : ''); };
  var _toneCls = function (t) { return ({ pos: 'vx-pos', neg: 'vx-neg', warn: 'vx-warn' }[t] || ''); };
  VX.tile = {
    /* Métrique riche : label + valeur (+ unité) (+ mini-barre 0-100). */
    metric: function (o) {
      o = o || {};
      var u = o.unit ? '<span class="vx-metric-u">' + VX.esc(o.unit) + '</span>' : '';
      var bar = (o.bar != null && o.v != null)
        ? '<div class="vx-metric-bar"><i style="width:' + Math.max(3, Math.min(100, o.bar)) + '%"></i></div>' : '';
      return '<div class="vx-metric" data-tone="' + (o.v == null ? '' : _toneAttr(o.tone)) + '">'
        + '<span class="vx-metric-k">' + VX.esc(o.k) + '</span>'
        + '<span class="vx-metric-v">' + VX.fmt.nd(o.v) + u + '</span>' + bar + '</div>';
    },
    /* Stat à halo : label + valeur (+ sous-légende) (+ extra, ex. sparkline SVG). */
    stat: function (o) {
      o = o || {};
      var sub = (o.sub != null && o.sub !== '') ? '<div class="vx-stat-sub">' + VX.esc(o.sub) + '</div>' : '';
      return '<div class="vx-stat" data-tone="' + _toneAttr(o.tone) + '">'
        + '<div class="vx-stat-k">' + VX.esc(o.k) + '</div>'
        + '<div class="vx-stat-v">' + VX.fmt.nd(o.v) + '</div>' + sub + (o.extra || '') + '</div>';
    },
    /* KPI dans une carte compacte : label + valeur + delta (ton par classe). */
    kpi: function (o) {
      o = o || {};
      var tc = _toneCls(o.tone);
      var span = o.span ? ' style="grid-column:span ' + (o.span | 0) + '"' : '';
      var delta = (o.delta != null && o.delta !== '')
        ? '<span class="vx-kpi-delta ' + (tc || 'vx-muted') + '">' + o.delta + '</span>' : '';
      return '<div class="vx-card vx-card--compact vx-kpi"' + span + '>'
        + '<span class="vx-kpi-label">' + VX.esc(o.label) + '</span>'
        + '<span class="vx-kpi-value' + (tc ? ' ' + tc : '') + '">' + VX.fmt.nd(o.value) + '</span>' + delta + '</div>';
    },
  };

  /* ── UpdateIndicator (§38) ───────────────────────────────────────── */
  VX.updateIndicator = function (ts, source, mode) {
    const modeLabel = { live: 'Live', delayed: 'Différé', fallback: 'Secours', error: 'Erreur' }[mode] || '';
    const parts = [VX.fmt.ago(ts)];
    if (source) parts.push(source + (modeLabel ? ' ' + modeLabel : ''));
    return `<span class="vx-update" data-mode="${mode || 'unknown'}" title="${VX.fmt.isoFull(ts)}">` +
      `<span class="vx-dot"></span>${parts.join(' · ')}</span>`;
  };

  /* ── États de données (§39) ──────────────────────────────────────── */
  VX.states = {
    loading(rows = 3) {
      let h = '<div class="vx-flex-col" aria-busy="true" data-state="loading">';
      for (let i = 0; i < rows; i++) h += `<div class="vx-skeleton" style="height:${i ? 14 : 22}px;width:${90 - i * 15}%"></div>`;
      return h + '</div>';
    },
    // Mini-visualisation « fantôme » (§44) : silhouette de placeholder, JAMAIS
    // une donnée. Sert à ne plus laisser de rectangle vide (§10). type :
    // 'bars' (défaut) · 'line' · 'ring' · false (aucun).
    ghost(type) {
      if (type === false) return '';
      if (type === 'ring') {
        return '<svg class="vx-state-ghost" viewBox="0 0 44 44" aria-hidden="true">' +
          '<circle cx="22" cy="22" r="17" fill="none" stroke="currentColor" stroke-width="5" opacity=".18"/>' +
          '<circle cx="22" cy="22" r="17" fill="none" stroke="var(--vx-copper-light)" stroke-width="5" ' +
          'stroke-dasharray="60 107" stroke-linecap="round" opacity=".35" transform="rotate(-90 22 22)"/></svg>';
      }
      if (type === 'line') {
        return '<svg class="vx-state-ghost" viewBox="0 0 140 48" aria-hidden="true">' +
          '<line x1="6" y1="42" x2="134" y2="42" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity=".3"/>' +
          '<path d="M6 34 L34 26 L58 30 L82 16 L106 22 L134 12" fill="none" stroke="var(--vx-copper-light)" ' +
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".4"/></svg>';
      }
      let bars = '';
      const hs = [16, 26, 12, 30, 20, 34, 22];
      hs.forEach((h, i) => {
        bars += `<rect x="${8 + i * 19}" y="${42 - h}" width="11" height="${h}" rx="2" ` +
          `fill="${i === 5 ? 'var(--vx-copper-light)' : 'currentColor'}" opacity="${i === 5 ? .38 : .16}"/>`;
      });
      return '<svg class="vx-state-ghost" viewBox="0 0 140 48" aria-hidden="true">' +
        '<line x1="6" y1="42" x2="140" y2="42" stroke="currentColor" stroke-width="1" opacity=".2"/>' + bars + '</svg>';
    },
    empty(reason, action, opts) {
      opts = opts || {};
      const title = opts.title || 'Aucune donnée';
      const g = VX.states.ghost(opts.ghost === undefined ? 'bars' : opts.ghost);
      return `<div class="vx-state" data-state="empty">${g}<b>${title}</b><span>${reason || ''}</span>${action || ''}</div>`;
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
