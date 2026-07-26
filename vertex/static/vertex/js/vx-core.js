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
  let _pageBus = [];                    // abonnements de PAGE (purgés à la navigation)
  VX.bus = {
    /* opts.persistent : abonnement de SHELL, survit aux navigations client.
       Défaut = abonnement de page → retiré au teardown (évite les doublons). */
    on(name, fn, opts) {
      bus.addEventListener(name, fn);
      if (!(opts && opts.persistent)) _pageBus.push({ name, fn });
      return () => bus.removeEventListener(name, fn);
    },
    emit(name, detail) { bus.dispatchEvent(new CustomEvent(name, { detail })); },
    _clearPage() { _pageBus.forEach((h) => bus.removeEventListener(h.name, h.fn)); _pageBus = []; },
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
    var href = '/analysis/' + encodeURIComponent(symbol.toUpperCase());
    if (VX.router && VX.router.go) VX.router.go(href);   // navigation ticker fluide (SPA)
    else location.href = href;                            // repli dur (routeur absent)
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

  /* ── Couche de données : cache persistant + SWR + dédup (§40, LOT 3) ──
     Le cache survit désormais au reload (sessionStorage) → revenir sur une page
     ne relance pas un chargement lourd. Déduplication in-flight, invalidation
     ciblée, stale-while-revalidate (VX.swr), annulation propre. Lecture seule. */
  const cache = new Map();     // url -> {ts, data}
  const inflight = new Map();  // url -> {p, ctl}
  const PERSIST_KEY = 'vxDataCache';
  const PERSIST_MAX_ENTRY = 200000;   // n'archive pas les gros payloads (ex. /scan ~8Mo)
  const PERSIST_MAX = 60;             // nb d'entrées persistées

  /* Hydrate le cache depuis la session au démarrage (revisite instantanée). */
  (function hydrate() {
    try {
      const raw = sessionStorage.getItem(PERSIST_KEY);
      if (!raw) return;
      const obj = JSON.parse(raw);
      Object.keys(obj).forEach((u) => { cache.set(u, obj[u]); });
    } catch (e) {}
  })();
  let _persistTimer = null;
  function schedulePersist() {
    if (_persistTimer) return;
    _persistTimer = setTimeout(() => {
      _persistTimer = null;
      try {
        const out = {}; let n = 0;
        // les plus récents d'abord, bornés en taille et en nombre
        const entries = Array.from(cache.entries()).sort((a, b) => b[1].ts - a[1].ts);
        for (const [u, v] of entries) {
          if (n >= PERSIST_MAX) break;
          let s; try { s = JSON.stringify(v); } catch (e) { continue; }
          if (s.length > PERSIST_MAX_ENTRY) continue;   // trop gros → non persisté
          out[u] = v; n++;
        }
        sessionStorage.setItem(PERSIST_KEY, JSON.stringify(out));
      } catch (e) {}
    }, 400);
  }

  function _store(url, data) {
    cache.set(url, { ts: Date.now(), data });
    if (cache.size > 120) cache.delete(cache.keys().next().value);
    schedulePersist();
  }

  VX.fetch = function (url, { ttl = 30000, priority = 'normal', signal } = {}) {
    const hit = cache.get(url);
    if (hit && Date.now() - hit.ts < ttl) return Promise.resolve(hit.data);
    if (inflight.has(url)) return inflight.get(url).p;
    const ctl = new AbortController();
    if (signal) signal.addEventListener('abort', () => ctl.abort());
    const p = (async () => {
      let lastErr;
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          const r = await fetch(url, { signal: ctl.signal });
          if (!r.ok) throw new Error('HTTP ' + r.status);
          const data = await r.json();
          _store(url, data);
          return data;
        } catch (e) {
          lastErr = e;
          if (e.name === 'AbortError') throw e;
          await new Promise(res => setTimeout(res, 600 * (attempt + 1)));
        }
      }
      throw lastErr;
    })().finally(() => inflight.delete(url));
    inflight.set(url, { p, ctl });
    return p;
  };

  /* Lecture synchrone du cache (sans réseau) : donnée + fraîcheur, ou null. */
  VX.fetch.peek = function (url) {
    const hit = cache.get(url);
    return hit ? { data: hit.data, age: Date.now() - hit.ts, ts: hit.ts } : null;
  };
  /* Invalidation CIBLÉE (clé exacte, préfixe, ou prédicat) — plus de cache.clear() aveugle. */
  VX.fetch.invalidate = function (target) {
    let pred;
    if (typeof target === 'function') pred = target;
    else if (typeof target === 'string') pred = (u) => u === target || u.indexOf(target) === 0;
    else { cache.clear(); schedulePersist(); return; }
    Array.from(cache.keys()).forEach((u) => { if (pred(u)) cache.delete(u); });
    schedulePersist();
  };

  /* stale-while-revalidate : rend le cache TOUT DE SUITE (même périmé), puis
     revalide en fond et rappelle onData si la donnée a changé. Ne vide JAMAIS
     l'écran, ne remplace jamais du valide par du vide (erreur → garde l'ancien).
     Retourne un annulateur : à appeler au changement de page/ticker (anti-hors-ordre). */
  VX.swr = function (url, onData, opts) {
    opts = opts || {};
    const ttl = opts.ttl == null ? 30000 : opts.ttl;
    let alive = true;
    const hit = cache.get(url);
    let servedStr = null;
    if (hit) { servedStr = safeStr(hit.data); try { onData(hit.data, { stale: Date.now() - hit.ts >= ttl, cached: true }); } catch (e) {} }
    const fresh = hit && Date.now() - hit.ts < ttl;
    if (!fresh) {
      VX.fetch(url, { ttl: 0 }).then((data) => {
        if (!alive) return;                       // navigation/ticker changé → ignore (hors-ordre)
        const s = safeStr(data);
        if (s !== servedStr) { try { onData(data, { stale: false, cached: false }); } catch (e) {} }
      }).catch(() => { /* garde l'ancien contenu, jamais de vide */ });
    }
    return function cancel() { alive = false; };
  };
  function safeStr(o) { try { return JSON.stringify(o); } catch (e) { return null; } }
  VX.refresh = {
    _tasks: [], _suspended: false,
    /* opts.persistent : tâche de SHELL (statut global…), survit aux navigations.
       Défaut = tâche de page → intervalle arrêté au teardown (évite les doublons
       de loaders et les fetch fantômes après changement de page). */
    register(fn, intervalMs, label, opts) {
      const task = { fn, intervalMs, label, id: null, persistent: !!(opts && opts.persistent) };
      const run = () => { if (!document.hidden) { try { fn(); } catch (e) { console.error('[vx-refresh]', label, e); } } };
      task.id = setInterval(run, intervalMs);
      this._tasks.push(task);
      return task;
    },
    _clearPage() {
      const keep = [];
      this._tasks.forEach((t) => { if (t.persistent) { keep.push(t); } else { clearInterval(t.id); } });
      this._tasks = keep;
    },
    async runAll(btn) {
      if (btn) { btn.dataset.state = 'refreshing'; btn.disabled = true; }
      VX.fetch.invalidate();      // vide cache mémoire + persistance (rafraîchissement explicite)
      try {
        await Promise.allSettled(this._tasks.map(t => t.fn()));
        VX.bus.emit('vx:data-refreshed', {});
        if (btn) { btn.dataset.state = 'success'; VX.toast('Données actualisées', 'success'); }
      } catch (e) { if (btn) btn.dataset.state = 'error'; }
      if (btn) setTimeout(() => { btn.dataset.state = 'ready'; btn.disabled = false; }, 900);
    },
  };

  /* ── Cycle de vie de PAGE (navigation client persistante, LOT 2) ──────
     Le routeur (vx-router.js) appelle VX.page._teardown() AVANT de remplacer
     #vx-content : on arrête les tâches/abonnements de la page sortante et on
     exécute ses nettoyages (onLeave). Le shell (statut, live-updates, entités)
     est marqué persistant et n'est jamais touché. */
  VX.page = {
    _gen: 0,
    _leave: [],
    onLeave(fn) { if (typeof fn === 'function') this._leave.push(fn); },
    _teardown() {
      this._leave.forEach((fn) => { try { fn(); } catch (e) {} });
      this._leave = [];
      try { VX.refresh._clearPage(); } catch (e) {}
      try { VX.bus._clearPage(); } catch (e) {}
      this._gen++;
    },
  };

  /* ── Store global minimal (LOT 2 — fondation ; SWR/dédup enrichis au LOT 3) ──
     Vérité partagée du contexte applicatif : session active, ticker courant,
     historique de navigation, prix live (source centrale à venir). Lecture seule
     côté métier — aucun ordre, aucune donnée inventée. */
  VX.store = {
    _s: {
      active_session_id: null, previous_session_id: null, session_status: null,
      active_ticker: null, selected_timeframe: null,
      nav_history: [], live_prices: {}, freshness_map: {},
    },
    get(k) { return this._s[k]; },
    set(k, v) { this._s[k] = v; VX.bus.emit('vx:store-changed', { key: k, value: v }); return v; },
    snapshot() { return Object.assign({}, this._s); },
    pushNav(href) {
      const h = this._s.nav_history;
      if (h[h.length - 1] !== href) h.push(href);
      if (h.length > 30) h.shift();
    },
  };
  /* Suspendre en arrière-plan, rafraîchir au retour. */
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) VX.bus.emit('vx:data-refreshed', { reason: 'visibility' });
  });

  /* ── PRÉCHAUFFAGE : au chargement du shell, on réchauffe les endpoints légers
     (digest de session + résumé marché) dès que le navigateur est au repos, pour
     que la première navigation vers Aujourd'hui / Marchés soit quasi instantanée.
     Uniquement des GET de lecture, cache client partagé (VX.fetch). Aucun ordre. */
  const _warm = () => {
    ['/api/session/digest', '/api/market/summary'].forEach(u => {
      try { VX.fetch(u, { ttl: 30000, priority: 'low' }).catch(() => {}); } catch (e) {}
    });
  };
  const _schedule = () => (window.requestIdleCallback
    ? requestIdleCallback(_warm, { timeout: 2500 }) : setTimeout(_warm, 900));
  if (document.readyState === 'complete') _schedule();
  else window.addEventListener('load', _schedule, { once: true });
})();
