/**
 * Rollup verification — the test that matters.
 *
 * Recomputes the earned-value aggregates straight from data/portfolio_data.json and
 * asserts the running page produces identical numbers, then asserts that each level of
 * the hierarchy sums to the organisation total. Double-counting and leakage are silent
 * failures: the screen still looks plausible, the numbers are just wrong.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const EPS = 0.5;
let failures = 0;

function check(name, page, truth, tol = EPS) {
  const ok = Math.abs(page - truth) <= tol;
  if (!ok) failures++;
  const f = n => (Math.abs(n) >= 1e6 ? (n / 1e9).toFixed(4) + 'B' : n.toFixed(4));
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name.padEnd(34)} page=${f(page).padStart(12)}  truth=${f(truth)}`);
}

(async () => {
  const D = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/portfolio_data.json'), 'utf8'));
  const P = D.projects;
  const sum = k => P.reduce((a, b) => a + (+b[k] || 0), 0);
  const bac = sum('BudgetAtCompletion'), ac = sum('ActualCost');
  const ev = sum('EarnedValue'), pv = sum('PlannedValue');

  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + path.join(ROOT, 'index.html'));
  await page.waitForTimeout(700);

  const r = await page.evaluate(() => {
    const o = roll(DATA.projects);
    const lvl = list => ({
      n: list.reduce((a, x) => a + x.projects.length, 0),
      bac: list.reduce((a, x) => a + roll(x.projects).bac, 0)
    });
    return {
      org: { n: o.n, bac: o.bac, ac: o.ac, ev: o.ev, pv: o.pv, spi: o.spi, cpi: o.cpi, eac: o.eac },
      pri: lvl(DATA.priorities), pf: lvl(DATA.portfolios), pg: lvl(DATA.programs),
      problems: PROBLEMS,
      orphans: [
        ...DATA.portfolios.filter(x => !DATA.byPri[x.PriorityID]).map(x => 'portfolio ' + x.PortfolioID),
        ...DATA.programs.filter(x => !DATA.byPf[x.PortfolioID]).map(x => 'program ' + x.ProgramID),
        ...DATA.projects.filter(x => !DATA.byPg[x.ProgramID]).map(x => 'project ' + x.ProjectID)
      ]
    };
  });

  console.log('\nORGANISATION ROLLUP vs independent recomputation');
  check('project count', r.org.n, P.length, 0);
  check('budget at completion', r.org.bac, bac);
  check('actual cost', r.org.ac, ac);
  check('earned value', r.org.ev, ev);
  check('planned value', r.org.pv, pv);
  check('SPI', r.org.spi, ev / pv, 1e-9);
  check('CPI', r.org.cpi, ev / ac, 1e-9);
  check('EAC', r.org.eac, bac / (ev / ac), 1e-5);

  console.log('\nHIERARCHY COMPLETENESS — each level must sum to the organisation total');
  for (const [label, v] of [['priority', r.pri], ['portfolio', r.pf], ['program', r.pg]]) {
    check(`${label} level — count`, v.n, P.length, 0);
    check(`${label} level — budget`, v.bac, bac);
  }

  console.log('\nREFERENTIAL INTEGRITY');
  if (r.orphans.length) { failures++; console.log('  FAIL  orphaned nodes: ' + r.orphans.join(', ')); }
  else console.log('  ok    every node resolves to a valid parent');
  console.log('  ' + (r.problems.length ? 'note  data health flags: ' + r.problems.join(' | ')
                                        : 'ok    data health panel reports no problems'));

  if (errs.length) { failures++; console.log('\n  FAIL  console errors: ' + errs.join(' | ')); }

  await browser.close();
  console.log(failures ? `\n${failures} CHECK(S) FAILED\n` : '\nAll rollup checks passed.\n');
  process.exit(failures ? 1 : 0);
})();
