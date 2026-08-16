# Portfolio Drill-Down

An executive dashboard for a national AI-economy programme. Drills **Vision → Portfolio → Program → Project**, computes PMI/PMBOK earned-value metrics, and reads its data from an Excel workbook.

No server. No database. No dependencies at runtime. `index.html` is the entire application — double-click it.

---

## Quick start

**Just want to look at it?** Open `index.html`. It ships with a synthetic dataset: 1 vision, 4 portfolios, 17 programs, 84 projects, $57.8B.

**Want to load your own data?** Open `data/Portfolio_Reporting_Template.xlsx`, replace the sample rows, then drag the file onto the dashboard. Nothing to rebuild.

**Want to change the app?**

```bash
npm install          # playwright, for tests only
npm run all          # regenerate data + rebuild index.html
npm test             # regression + rollup verification
npm run serve        # http://localhost:8000
```

Requires Python 3 with `openpyxl` (`pip install openpyxl`) and Node 18+.

**Windows:** works as-is. The npm scripts go through `scripts/py.js`, which finds `py -3`, `python` or `python3` automatically. Installing [Git for Windows](https://git-scm.com/downloads/win) is recommended so Claude Code can use Bash rather than PowerShell.

If `npm install` fails with `UNABLE_TO_VERIFY_LEAF_SIGNATURE`, or `pip install` with
`CERTIFICATE_VERIFY_FAILED`, that is this machine's antivirus TLS interception, not the project.
`~/.npmrc` pins `cafile` to the Norton root, which replaces the default CA bundle rather than
adding to it, so anything *not* being intercepted then fails to verify. Workarounds that do not
touch global config:

```bash
npm install --userconfig /dev/null
pip install --use-feature=truststore openpyxl
```

The Playwright browser download (`npx playwright install`, needed once before `npm test`)
fails the same way — `unable to verify the first certificate`. Neither workaround above fixes
it; make Node read the OS trust store instead, where the Norton CA is registered (Node 22+):

```bash
NODE_OPTIONS=--use-system-ca npx playwright install chromium-headless-shell
```

Once the browser is installed, `npm test` itself needs no flag — it launches a local browser
against a local file. None of this affects hosted CI, which downloads over public CAs normally.

Nothing above is needed just to *use* the dashboard — only to rebuild it.

---

## How it fits together

```
scripts/gen_data.py   ──►  data/portfolio_data.json  ──┐
                                                        ├──►  scripts/build.py  ──►  index.html
src/app.html  ─────────────────────────────────────────┘
                      └►  scripts/build_xlsx.py  ──►  data/Portfolio_Reporting_Template.xlsx
```

`src/app.html` is the source. `index.html` is generated — **never edit it directly.**

---

## The four columns that matter

Every metric on every screen derives from four columns on the `Projects` sheet:

| Column | Meaning |
|---|---|
| `BudgetAtCompletion` | Total approved budget |
| `PlannedValue` | Budgeted cost of work **scheduled** to date |
| `EarnedValue` | Budgeted cost of work **completed** to date |
| `ActualCost` | Spent to date |

From these the dashboard computes schedule and cost variance, SPI, CPI, forecast at completion, variance at completion, and every RAG status. If your PMs maintain only four columns reliably, make it these.

RAG thresholds live on the `Config` sheet — change them there, never in code.

---

## Navigating

A persistent hierarchy navigator sits above every screen, in three modes:

- **Cascade** — column browser. Click across levels, jump sideways without going back.
- **Map** — the whole programme as one proportional strip, width = budget, colour = RAG. Zooms as you drill.
- **Matrix** — Portfolio × Phase (or × Department). Click a cell to open that portfolio filtered to that slice.

Filters apply once and persist across every level. Breadcrumbs and browser Back both work.

---

## Deploying

Push to GitHub, import into Vercel, done — it's a static site with `index.html` at the root. No configuration, no environment variables, free tier.

---

## Working on this with Claude Code

Read `CLAUDE.md` first. It records the data model, the exact formulas, the RAG rules, and — importantly — the decisions that look like bugs but aren't, such as why rollup risk uses concentration rather than the worst single risk.
