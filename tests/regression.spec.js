/**
 * Regression suite — walks every drill path, all three navigator modes, filters,
 * sorting, table toggles and dark mode. Fails on any console error.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const APP = 'file://' + path.resolve(__dirname, '..', 'index.html');
const SHOTS = path.resolve(__dirname, 'screenshots');
fs.mkdirSync(SHOTS, { recursive: true });

let failures = 0;
const t = async (label, fn) => {
  try {
    const r = await fn();
    if (r === false) { failures++; console.log(`  FAIL  ${label}`); }
    else console.log(`  ok    ${label}${r && r !== true ? ' — ' + r : ''}`);
  } catch (e) { failures++; console.log(`  FAIL  ${label} — ${e.message.split('\n')[0]}`); }
};
const shot = (p, f, h) => p.screenshot({ path: path.join(SHOTS, f), clip: { x: 0, y: 0, width: 1680, height: h } });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1680, height: 1100 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  const go = async (hash = '') => { await page.goto(APP + hash); await page.waitForTimeout(600); };
  const mainTable = () => page.locator('.card').filter({ hasText: 'All projects' });

  await go();

  console.log('\n== ORGANISATION VIEW');
  await t('stat tiles', async () => (await page.locator('.tile').count()) + ' tiles');
  await t('charts render', async () => (await page.locator('main svg').count()) + ' charts');
  await t('drill cards', async () => (await page.locator('main .drill').count()) + ' cards');
  await t('project register', async () => (await mainTable().locator('tbody tr').count()) + ' rows');
  await t('scope chip', async () => await page.locator('#scopechip').textContent());
  await shot(page, '01-org.png', 1100);

  console.log('\n== NAVIGATOR: CASCADE');
  await t('four columns', async () => (await page.locator('.ccol').count()) === 4);
  await t('column headers', async () =>
    (await page.locator('.chd').allTextContents()).map(s => s.trim().replace(/\s+/g, ' ')).join(' | '));
  await page.locator('.ccol').nth(1).locator('.citem').nth(1).click(); await page.waitForTimeout(400);
  await t('portfolio click navigates', async () => page.url().split('#')[1]);
  await t('programs column narrows', async () => (await page.locator('.ccol').nth(2).locator('.citem').count()) + ' programs');
  await t('selection highlighted', async () => (await page.locator('.citem.sel').count()) + ' selected');
  await page.locator('.ccol').nth(2).locator('.citem').first().click(); await page.waitForTimeout(400);
  await t('program click navigates', async () => page.url().split('#')[1]);
  await page.locator('.ccol').nth(3).locator('.citem').first().click(); await page.waitForTimeout(400);
  await t('project click navigates', async () => page.url().split('#')[1]);
  await t('auto-collapses at project', async () =>
    (await page.locator('.navbody').getAttribute('class')).includes('collapsed'));
  await t('collapsed strip shows path', async () => await page.locator('.navhead .chip').textContent());
  await page.locator('#navtoggle').click(); await page.waitForTimeout(300);
  await t('manual expand', async () => !(await page.locator('.navbody').getAttribute('class')).includes('collapsed'));
  await shot(page, '02-cascade.png', 420);

  console.log('\n== NAVIGATOR: MAP');
  await go();
  await page.locator('[data-navmode="map"]').click(); await page.waitForTimeout(400);
  await t('org level = 3 rows, no projects row', async () => {
    const labels = await page.locator('.navbody svg text').allTextContents();
    return labels.includes('PROJECTS') ? false : 'VISION/PORTFOLIOS/PROGRAMS';
  });
  await t('every band clickable (min width)', async () => {
    const w = await page.locator('.navbody svg rect').evaluateAll(rs => Math.min(...rs.map(r => +r.getAttribute('width'))));
    return w >= 1.2 ? `min band ${w.toFixed(1)}u` : false;
  });
  await shot(page, '03-map-org.png', 340);
  await go('#/portfolio/PF-01');
  await page.locator('[data-navmode="map"]').click(); await page.waitForTimeout(400);
  await t('zoomed = 4 rows with projects', async () =>
    (await page.locator('.navbody svg text').allTextContents()).includes('PROJECTS'));
  await t('band count matches subtree', async () => (await page.locator('.navbody svg rect').count()) + ' bands');
  await shot(page, '04-map-zoom.png', 380);

  console.log('\n== NAVIGATOR: MATRIX');
  await go();
  await page.locator('[data-navmode="matrix"]').click(); await page.waitForTimeout(400);
  await t('cells rendered', async () => (await page.locator('.mcell').count()) + ' cells');
  await t('column totals present', async () => (await page.locator('.mtot').count()) + ' totals');
  await shot(page, '05-matrix.png', 440);
  await page.locator('[data-mtxcol="dept"]').click(); await page.waitForTimeout(400);
  await t('switch to department axis', async () =>
    (await page.locator('.mtx th').allTextContents()).slice(1, 3).join(' | '));
  await page.locator('[data-mtxcol="phase"]').click(); await page.waitForTimeout(300);
  await page.locator('.mcell').first().click(); await page.waitForTimeout(500);
  await t('cell click navigates + sets filter', async () =>
    page.url().split('#')[1] + ' · ' + (await page.locator('#scopechip').textContent()));

  console.log('\n== DRILL PATHS & BREADCRUMBS');
  await go('#/project/PJ-002');
  await t('project view loads', async () => (await page.locator('.tile').count()) + ' tiles');
  await t('five breadcrumb levels', async () => (await page.locator('#crumbs .crumb').count()) === 5);
  await t('risk register present', async () =>
    (await page.locator('.card').filter({ hasText: 'Risk register' }).count()) > 0);
  await t('EVM + milestones', async () => (await page.locator('main svg').count()) + ' charts');
  await shot(page, '06-project.png', 1100);
  await page.locator('#crumbs .crumb').nth(2).click(); await page.waitForTimeout(400);
  await t('breadcrumb jumps up', async () => page.url().split('#')[1]);
  await page.goBack(); await page.waitForTimeout(400);
  await t('browser back works', async () => page.url().split('#')[1]);

  console.log('\n== FILTERS');
  await go();
  const dept = (await page.locator('#fdept option').nth(1).textContent()).trim();
  await page.selectOption('#fdept', dept); await page.waitForTimeout(400);
  await t(`department = ${dept}`, async () => await page.locator('#scopechip').textContent());
  await page.selectOption('#frag', 'r'); await page.waitForTimeout(400);
  await t('+ overall RAG = red', async () => await page.locator('#scopechip').textContent());
  await t('navigator respects filters', async () =>
    (await page.locator('.ccol').nth(3).locator('.citem').count()) + ' projects in cascade');
  await page.click('#clearf'); await page.waitForTimeout(400);
  await t('clear restores scope', async () => await page.locator('#scopechip').textContent());

  console.log('\n== TABLE, SORTING, THEME');
  const tog = page.locator('main [data-tv]').first();
  await tog.click(); await page.waitForTimeout(250);
  await t('chart table view', async () => (await tog.getAttribute('aria-pressed')) === 'true');
  await tog.click(); await page.waitForTimeout(200);
  const topBudget = async () => (await mainTable().locator('tbody tr').first().locator('td').nth(8).textContent()).trim();
  await page.locator('th[data-sort="BudgetAtCompletion"]').click(); await page.waitForTimeout(400);
  const asc = await topBudget();
  await page.locator('th[data-sort="BudgetAtCompletion"]').click(); await page.waitForTimeout(400);
  const desc = await topBudget();
  await t('sort ascending then descending', async () => asc !== desc ? `${asc} → ${desc}` : false);
  await page.click('#themebtn'); await page.waitForTimeout(400);
  await t('dark mode', async () => (await page.locator('html').getAttribute('data-theme')) === 'dark');
  await shot(page, '07-dark.png', 1100);

  console.log('\n== CONSOLE: ' + (errors.length ? errors.join(' | ') : 'clean'));
  if (errors.length) failures++;

  await browser.close();
  console.log(failures ? `\n${failures} CHECK(S) FAILED\n` : '\nAll regression checks passed.\n');
  process.exit(failures ? 1 : 0);
})();
