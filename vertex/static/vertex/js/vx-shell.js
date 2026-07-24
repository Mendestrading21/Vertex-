/* Vertex Shell — interactions du squelette : sidebar, topbar, palette,
   drawers, modals, notifications, connexions, horloge, retour contextuel. */
(function () {
  'use strict';
  const VX = window.VX;
  const $ = (id) => document.getElementById(id);
  const app = $('vx-app');

  /* ── Sidebar (état persistant vxSidebarState) ────────────────────── */
  try {
    const saved = localStorage.getItem('vxSidebarState');
    if (saved === 'collapsed') app.dataset.sidebar = 'collapsed';
  } catch (e) {}
  $('vx-collapse-btn')?.addEventListener('click', () => {
    const next = app.dataset.sidebar === 'collapsed' ? 'expanded' : 'collapsed';
    app.dataset.sidebar = next;
    try { localStorage.setItem('vxSidebarState', next); } catch (e) {}
  });
  /* Mobile drawer nav */
  const mobileNavBtn = $('vx-mobile-nav-btn');
  if (window.matchMedia('(max-width:640px)').matches && mobileNavBtn) mobileNavBtn.style.display = 'inline-flex';
  mobileNavBtn?.addEventListener('click', () => {
    app.dataset.mobileNav = app.dataset.mobileNav === 'open' ? 'closed' : 'open';
    overlay(app.dataset.mobileNav === 'open');
  });
  $('vx-mobile-more')?.addEventListener('click', () => {
    /* Espaces hors barre mobile (5 prioritaires) : Options, Journal, Système. */
    VX.shell.openDrawer('Navigation', ['options', 'journal', 'system'].map(id => {
      const it = { options: ['Options', '/options'], journal: ['Journal', '/journal'], system: ['Système', '/system'] }[id];
      return `<a class="vx-nav-item" href="${it[1]}">${it[0]}</a>`;
    }).join(''));
  });

  /* ── Overlay / drawer / modal ────────────────────────────────────── */
  let lastFocus = null;
  function overlay(open) { $('vx-overlay').dataset.open = open ? '1' : '0'; }
  function trapFocus(container) {
    const focusables = container.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
    if (focusables.length) focusables[0].focus();
  }
  const shell = VX.shell = {
    openDrawer(title, html) {
      lastFocus = document.activeElement;
      $('vx-drawer-title').textContent = title;
      $('vx-drawer-body').innerHTML = html;
      $('vx-drawer').dataset.open = '1'; overlay(true);
      trapFocus($('vx-drawer'));
    },
    closeDrawer() { $('vx-drawer').dataset.open = '0'; overlay(false); lastFocus?.focus?.(); },
    openModal(title, bodyHtml, footerHtml) {
      lastFocus = document.activeElement;
      $('vx-modal-title').textContent = title;
      $('vx-modal-body').innerHTML = bodyHtml;
      $('vx-modal-footer').innerHTML = footerHtml || '';
      $('vx-modal').dataset.open = '1';
      trapFocus($('vx-modal'));
    },
    closeModal() { $('vx-modal').dataset.open = '0'; lastFocus?.focus?.(); },
    closeAll() {
      shell.closeDrawer(); shell.closeModal();
      $('vx-palette').dataset.open = '0';
      $('vx-context-menu').dataset.open = '0';
      app.dataset.mobileNav = 'closed'; overlay(false);
    },
  };
  document.querySelectorAll('[data-close-drawer]').forEach(b => b.addEventListener('click', shell.closeDrawer));
  document.querySelectorAll('[data-close-modal]').forEach(b => b.addEventListener('click', shell.closeModal));
  $('vx-overlay').addEventListener('click', shell.closeAll);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') shell.closeAll(); });

  /* ── Retour contextuel (§15) ─────────────────────────────────────── */
  const backBtn = $('vx-back-btn');
  const ctx = VX.context.get();
  const SPACE_LABELS = { '/': 'au briefing', '/markets': 'aux marchés', '/opportunities': 'aux opportunités', '/portfolio': 'au portefeuille', '/analysis': 'à l’analyse', '/performance': 'à la performance', '/intelligence': 'à l’intelligence', '/system': 'au système' };
  if (ctx && ctx.from && ctx.from !== location.pathname && backBtn) {
    const label = ctx.view === 'watchlist' ? 'Retour à la watchlist' : ('Retour ' + (SPACE_LABELS[ctx.from] || 'à ' + (ctx.label || ctx.from)));
    backBtn.querySelector('span').textContent = label;
    backBtn.dataset.visible = '1';
    backBtn.addEventListener('click', () => {
      const url = new URL(ctx.from, location.origin);
      if (ctx.view) url.searchParams.set('view', ctx.view);
      location.href = url.pathname + url.search;
    });
  }
  VX.context.restoreIfReturning();

  /* ── Horloge & session marché (heure New York) ───────────────────── */
  function tickClock() {
    const el = $('vx-session'); if (!el) return;
    try {
      const ny = new Date().toLocaleTimeString('fr-FR', { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit' });
      const nyDate = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/New_York' }));
      const day = nyDate.getDay(), mins = nyDate.getHours() * 60 + nyDate.getMinutes();
      const open = day >= 1 && day <= 5 && mins >= 570 && mins < 960;
      const pre = day >= 1 && day <= 5 && mins >= 240 && mins < 570;
      const label = open ? 'Marché ouvert' : (pre ? 'Pré-marché' : 'Marché fermé');
      const dotCol = open ? 'var(--vx-positive)' : (pre ? 'var(--vx-warning)' : 'var(--vx-text-faint)');
      el.innerHTML = `<b><span class="vx-live-dot" style="display:inline-block;margin-right:5px;background:${dotCol}"></span>${label}</b><br><span class="vx-muted">New York ${ny}</span>`;
    } catch (e) { /* fuseaux non dispo */ }
  }
  tickClock(); setInterval(tickClock, 30000);

  /* ── État global (sidebar footer) + connexions ───────────────────── */
  async function loadStatus() {
    try {
      const st = await VX.fetch('/api/live/status', { ttl: 60000 });
      const el = $('vx-global-status'); if (!el) return;
      const demo = !!st.demo;
      const dot = el.querySelector('.vx-dot'); const label = el.querySelector('.vx-status-label');
      dot.style.background = demo ? 'var(--vx-warning)' : 'var(--vx-positive)';
      label.textContent = demo ? 'Mode démo' : 'Données actives';
      window.__vxStatus = st;
      VX.bus.emit('vx:connection-changed', st);
    } catch (e) { /* silencieux : bandeau par page */ }
  }
  loadStatus(); VX.refresh.register(loadStatus, 90000, 'status');

  $('vx-connections-btn')?.addEventListener('click', async () => {
    let st = window.__vxStatus, diag = null;
    try { diag = await VX.fetch('/api/system/diagnostics', { ttl: 30000 }); } catch (e) {}
    const ib = st && !st.demo ? (st.domains?.quotes?.fresh ? 'live' : 'delayed') : 'offline';
    const rows = [
      ['IBKR', ib === 'live' ? 'Live' : (ib === 'delayed' ? 'Différé' : 'Hors ligne'), ib],
      ['TradingView', diag?.tradingview ? `${diag.tradingview.stored} signaux stockés` : 'non configuré', diag?.tradingview?.stored ? 'live' : 'fallback'],
      ['Claude', diag?.ai ? `${diag.ai.ok}/${diag.ai.total} analyses OK` : 'non configuré', diag?.ai?.total ? 'live' : 'fallback'],
      ['Synchronisation', 'desk /api/desk (last-writer-wins)', 'live'],
      ['Qualité des données', st?.demo ? 'DÉMO (synthétique, jamais réel)' : 'voir Système / Données', st?.demo ? 'fallback' : 'live'],
    ].map(([name, detail, mode]) =>
      `<div class="vx-kv"><span class="k">${name}</span><span class="v"><span class="vx-badge vx-badge-status" data-status="${mode}"><span class="vx-dot"></span>${detail}</span></span></div>`
    ).join('');
    VX.shell.openDrawer('Connexions', rows +
      '<div class="vx-mt4"><a class="vx-btn" href="/system?view=connections">Ouvrir Système / Connexions</a></div>');
  });

  /* ── Notifications (§42) ─────────────────────────────────────────── */
  const notifs = VX.notifications = {
    _items: [],
    push(item) {
      this._items.unshift(Object.assign({ ts: Date.now(), status: 'unread', priority: 'normal' }, item));
      this._items = this._items.slice(0, 60); this._render();
    },
    markAllRead() { this._items.forEach(i => i.status = 'read'); this._render(); },
    _render() {
      const unread = this._items.filter(i => i.status === 'unread').length;
      const badge = $('vx-notif-badge');
      if (badge) { badge.hidden = !unread; badge.textContent = unread; }
    },
  };
  $('vx-notifs-btn')?.addEventListener('click', async () => {
    try {
      const a = await VX.fetch('/api/alerts/active', { ttl: 20000 });
      (a.active || []).forEach(al => {
        if (!notifs._items.some(n => n.key === al.symbol + al.level)) {
          notifs.push({ key: al.symbol + al.level, category: 'Alerte', title: `${al.symbol} · ${al.level}`, message: al.reason, ticker: al.symbol, priority: al.level === 'ACTIONABLE' ? 'high' : 'normal' });
        }
      });
    } catch (e) {}
    const html = notifs._items.length ? notifs._items.map(n =>
      `<div class="vx-notif-item" data-priority="${n.priority}"><div class="vx-notif-body">
        <div class="vx-flex vx-between"><b>${n.title}</b><span class="vx-meta">${VX.fmt.ago(n.ts)}</span></div>
        <div class="vx-dim">${n.message || ''}</div>
        <div class="vx-meta">${n.category || ''}</div></div>
        ${n.ticker ? `<button class="vx-btn vx-btn-sm" onclick="VX.openAnalysis('${n.ticker}')">Analyse</button>` : ''}</div>`
    ).join('') : VX.states.empty('Aucune notification pour le moment.', '');
    VX.shell.openDrawer('Notifications', html);
    notifs.markAllRead();
  });

  /* ── Actualiser ──────────────────────────────────────────────────── */
  $('vx-refresh-btn')?.addEventListener('click', function () { VX.refresh.runAll(this); });

  /* ── Command palette (§14) ───────────────────────────────────────── */
  /* 8 espaces canoniques (PR n°2) + approfondissements joignables. */
  const PAGES = [
    ["Aujourd'hui", '/'], ['Marchés', '/markets'], ['Marchés · Secteurs', '/markets?view=sectors'],
    ['Marchés · Volatilité', '/markets?view=volatility'], ['Marchés · Breadth', '/markets?view=breadth'],
    ['Opportunités', '/opportunities'], ['Opportunités · Options', '/opportunities?view=options'],
    ['Opportunités · Anomalies', '/opportunities?view=anomalies'], ['Opportunités · Calendrier', '/opportunities?view=calendar'],
    ['Analyse', '/analysis'],
    ['Portefeuille', '/portfolio'], ['Portefeuille · Watchlist', '/portfolio?view=watchlist'],
    ['Portefeuille · Risque', '/portfolio?view=risk'],
    ['Options', '/options'], ['Options · Volatilité', '/options?view=volatility'],
    ['Journal', '/journal'], ['Journal · Décisions', '/journal?view=journal'],
    ['Journal · Track Record', '/journal?view=track-record'], ['Journal · Suivis', '/tracking'],
    ['Analyse · Comité', '/intelligence?view=committee'],
    ['Système', '/system'], ['Système · Connexions', '/system?view=connections'],
    ['Système · Archive', '/system?view=archive'], ['Système · Design System', '/design-system'],
  ];
  const palette = $('vx-palette'), pInput = $('vx-palette-input'), pList = $('vx-palette-list');
  let pItems = [], pSel = 0, namesCache = null;
  function openPalette() {
    lastFocus = document.activeElement;
    palette.dataset.open = '1'; pInput.value = ''; renderPalette(''); pInput.focus();
  }
  async function tickerMatches(q) {
    if (!q || q.length < 1) return VX.recentTickers.get().slice(0, 5).map(s => ({ sym: s, name: 'récent' }));
    try {
      if (!namesCache) namesCache = (await VX.fetch('/api/names', { ttl: 600000 })) || {};
      const names = namesCache.names || namesCache;
      const qq = q.toUpperCase();
      return Object.entries(names)
        .filter(([sym, name]) => sym.startsWith(qq) || String(name).toUpperCase().includes(qq))
        .slice(0, 6).map(([sym, name]) => ({ sym, name }));
    } catch (e) {
      return /^[A-Za-z.]{1,6}$/.test(q) ? [{ sym: q.toUpperCase(), name: 'ouvrir l’analyse' }] : [];
    }
  }
  async function renderPalette(q) {
    const groups = [];
    const tickers = await tickerMatches(q);
    const ent = window.VXEntities;
    if (tickers.length) groups.push(['Titres', tickers.map(t => ({ label: t.name, mono: t.sym, run: () => VX.openAnalysis(t.sym) }))]);
    if (ent) {
      const qq = q.toUpperCase();
      const pos = ent.positions().filter(p => !qq || p.sym.includes(qq)).slice(0, 4);
      if (pos.length) groups.push(['Positions', pos.map(p => ({ label: `position · ${VX.fmt.nd(p.qty)} @ ${VX.fmt.nd(p.entry)}`, mono: p.sym, run: () => VX.openAnalysis(p.sym) }))]);
      const watch = ent.watchlist().filter(w => !qq || w.sym.includes(qq)).slice(0, 4);
      if (watch.length) groups.push(['Watchlist', watch.map(w => ({ label: w.thesis || 'surveillance', mono: w.sym, run: () => VX.openAnalysis(w.sym) }))]);
      const alerts = ent.alerts().filter(a => !qq || String(a.sym || '').includes(qq)).slice(0, 3);
      if (alerts.length) groups.push(['Alertes', alerts.map(a => ({ label: a.note || a.cond || 'alerte', mono: a.sym, run: () => VX.openAnalysis(a.sym) }))]);
    }
    const ql = q.toLowerCase();
    const pages = PAGES.filter(([label]) => !ql || label.toLowerCase().includes(ql)).slice(0, 7);
    if (pages.length) groups.push(['Pages', pages.map(([label, href]) => ({ label, mono: '→', run: () => location.href = href }))]);
    groups.push(['Actions', [
      { label: 'Ajouter (favori, watchlist, suivi, position, alerte, thèse)', mono: '+', run: () => { shell.closeAll(); window.VXEntities?.openAddModal(q.toUpperCase()); } },
      { label: 'Actualiser les données', mono: '↻', run: () => VX.refresh.runAll($('vx-refresh-btn')) },
    ].filter(a => !ql || a.label.toLowerCase().includes(ql))]);

    pItems = []; pSel = 0;
    pList.innerHTML = groups.filter(([, items]) => items.length).map(([g, items]) =>
      `<div class="vx-palette-group">${g}</div>` + items.map(it => {
        const idx = pItems.push(it) - 1;
        return `<div class="vx-palette-item" role="option" data-idx="${idx}" aria-selected="${idx === 0}">
          <span class="vx-mono">${it.mono || ''}</span><span class="vx-truncate">${it.label}</span></div>`;
      }).join('')).join('');
    pList.querySelectorAll('.vx-palette-item').forEach(el => {
      el.addEventListener('click', () => { pItems[+el.dataset.idx]?.run(); palette.dataset.open = '0'; });
      el.addEventListener('mousemove', () => selectPalette(+el.dataset.idx));
    });
  }
  function selectPalette(i) {
    pSel = Math.max(0, Math.min(pItems.length - 1, i));
    pList.querySelectorAll('.vx-palette-item').forEach(el =>
      el.setAttribute('aria-selected', String(+el.dataset.idx === pSel)));
    pList.querySelector(`[data-idx="${pSel}"]`)?.scrollIntoView({ block: 'nearest' });
  }
  pInput?.addEventListener('input', () => renderPalette(pInput.value.trim()));
  pInput?.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); selectPalette(pSel + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); selectPalette(pSel - 1); }
    else if (e.key === 'Enter') { e.preventDefault(); pItems[pSel]?.run(); palette.dataset.open = '0'; }
  });
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openPalette(); }
  });
  $('vx-global-search')?.addEventListener('focus', (e) => { e.target.blur(); openPalette(); });
  $('vx-global-search')?.addEventListener('click', openPalette);

  /* ── + Ajouter (§19) ─────────────────────────────────────────────── */
  $('vx-add-btn')?.addEventListener('click', () => window.VXEntities?.openAddModal());

  /* ── Sauvegarde du contexte avant de quitter la page ─────────────── */
  window.addEventListener('pagehide', () => {
    if (!location.pathname.startsWith('/analysis/')) VX.context.save();
  });
})();
