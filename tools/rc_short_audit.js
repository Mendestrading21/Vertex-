/**
 * tools/rc_short_audit.js — RC COURTE périodique (SKYLER LOT 32).
 *
 * Audit léger navigateur des 8 espaces canoniques :
 *   - 0 erreur console au repos (erreurs réseau in-flight d'une navigation
 *     abandonnée et polices externes injoignables en sandbox exclues,
 *     comme documenté au lot 27) ;
 *   - 0 pageerror (exception JS non rattrapée) ;
 *   - HTTP 200 par page ; /healthz ok ; /api/client-log à 0 ;
 *   - service worker courant servi (td-shell-vNNN affiché pour preuve).
 *
 * Usage : serveur démo lancé (DEMO=1 NO_IBKR=1 START_ON_IMPORT=1), puis
 *   NODE_PATH=/opt/node22/lib/node_modules node tools/rc_short_audit.js
 * Sortie : rapport texte + code retour 0 (GO) / 1 (défauts à investiguer).
 */
const { chromium } = require('playwright');

const BASE = process.env.VERTEX_BASE || 'http://127.0.0.1:5002';
const PAGES = ['/', '/markets', '/opportunities', '/analysis',
               '/portfolio', '/options', '/journal', '/system'];
// Bruit d'environnement documenté (lot 27) — jamais des défauts produit :
const NOISE = [/net::ERR_ABORTED/, /fonts\.googleapis\.com/, /fonts\.gstatic\.com/,
               /Failed to load resource/];

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium',
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const defects = [];

  for (const path of PAGES) {
    const consoleErrors = [];
    const pageErrors = [];
    const onConsole = (m) => {
      if (m.type() === 'error' && !NOISE.some((r) => r.test(m.text()))) {
        consoleErrors.push(m.text());
      }
    };
    const onPageError = (e) => pageErrors.push(String(e));
    page.on('console', onConsole);
    page.on('pageerror', onPageError);

    const resp = await page.goto(BASE + path, {
      waitUntil: 'domcontentloaded', timeout: 20000,
    });
    await page.waitForTimeout(2500);            // hydratation + premier poll

    const status = resp ? resp.status() : 0;
    if (status !== 200) defects.push(`${path} → HTTP ${status}`);
    for (const e of consoleErrors) defects.push(`${path} → console: ${e}`);
    for (const e of pageErrors) defects.push(`${path} → pageerror: ${e}`);
    console.log(`${path.padEnd(15)} HTTP ${status}  console_err=${consoleErrors.length}  pageerror=${pageErrors.length}`);

    page.off('console', onConsole);
    page.off('pageerror', onPageError);
  }

  const health = await page.evaluate(async (base) => {
    const r = await fetch(base + '/healthz');
    return { status: r.status, body: await r.text() };
  }, BASE);
  console.log(`/healthz        HTTP ${health.status}  ${health.body.slice(0, 60)}`);
  if (health.status !== 200) defects.push(`/healthz → HTTP ${health.status}`);

  const clientLog = await page.evaluate(async (base) => {
    const r = await fetch(base + '/api/client-log');
    return await r.json();
  }, BASE);
  const n = Array.isArray(clientLog) ? clientLog.length
    : (clientLog.count ?? (clientLog.errors || []).length);
  console.log(`/api/client-log n=${n}`);
  if (n !== 0) defects.push(`/api/client-log → ${n} erreur(s) client`);

  const sw = await page.evaluate(async (base) => {
    const r = await fetch(base + '/sw.js');
    const t = await r.text();
    const m = t.match(/td-shell-v(\d+)/);
    return m ? m[0] : null;
  }, BASE);
  console.log(`sw.js           ${sw}`);
  if (!sw) defects.push('/sw.js → aucun td-shell-vNNN trouvé');

  await browser.close();
  if (defects.length) {
    console.log('\nDÉFAUTS :');
    for (const d of defects) console.log('  - ' + d);
    process.exit(1);
  }
  console.log('\nRC COURTE : GO — 0 défaut.');
  process.exit(0);
})().catch((e) => { console.error('AUDIT ÉCHOUÉ :', e); process.exit(1); });
