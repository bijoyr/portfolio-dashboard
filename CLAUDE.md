# CLAUDE.md — Portfolio Drill-Down

Read this before changing anything. It records the decisions that are easy to break by accident.

---

## What this is

A single-file executive dashboard for a national AI-economy programme. Five levels, each rolling up into the one above:

```
Vision → Portfolio → Program → Project → (project dashboard)
```

Data comes from an Excel workbook. There is no database, no server, no API, no auth. The whole application is `index.html`.

## Repository layout

```
src/app.html        THE SOURCE. Edit this, never index.html.
data/portfolio_data.json    Dataset injected at build time
data/Portfolio_Reporting_Template.xlsx    The input template
scripts/gen_data.py         Generates the synthetic sample dataset
scripts/build_xlsx.py       Builds the Excel template from the dataset
scripts/build.py            Injects data into the template → index.html
index.html          BUILD OUTPUT — never hand-edit, it is overwritten
tests/              Playwright regression + rollup verification
```

**`index.html` is generated.** Editing it directly is the single most likely mistake. Edit `src/app.html`, then run `npm run build`.

## Commands

```bash
npm run data     # regenerate sample data + Excel template
npm run build    # src/app.html + data → index.html
npm run all      # both
npm test         # regression suite + rollup verification
npm run serve    # http://localhost:8000
```

Python deps: `openpyxl` (Excel). Node deps: `playwright` (tests only). Neither is needed to *run* the dashboard.

## Build reproducibility

The build is deterministic: `gen_data.py` is seeded (`random.seed(20260816)`) with a fixed
`TODAY`, so `npm run all` reproduces `index.html` and the workbook **byte for byte**. After a
rebuild with no source change, `git status` must be clean. If it isn't, something has
introduced nondeterminism — find it rather than committing the diff.

Three things keep it that way. Do not undo them:

1. **Every Python file read/write passes `encoding="utf-8"`.** Windows defaults to cp1252 and
   `src/app.html` contains the RAG glyphs, so the default breaks the build outright and would
   silently corrupt non-ASCII data on the way into the JSON.
2. **`build.py` writes with `newline="\n"`,** and `.gitattributes` pins `eol=lf`. Without both,
   Windows rewrites all 1,528 line endings and every build reads as a full-file diff.
3. **`build_xlsx.py` freezes the workbook timestamps** (`freeze_timestamps`). An xlsx is a zip;
   openpyxl stamps every entry with "now", making each rebuild a 72 KB binary diff with an
   identical payload. That noise is what buries real changes in the snapshot history.

## Snapshots

`snapshots/YYYY-MM-DD.xlsx` — dated copies of the workbook, committed periodically. This is the
one thing that cannot be retrofitted: every trend, velocity and forecasting feature needs
history, and history not captured is gone. Add a new dated copy whenever the data changes
materially; never overwrite an existing one.

---

## Hard constraints

These are not preferences. Breaking them breaks the product.

1. **Zero cost, zero runtime dependencies.** No React, no chart library, no CSS framework, no build toolchain, no paid service. Every chart is hand-written SVG. The only external resource is SheetJS from cdnjs, loaded lazily *only* when a user drops a workbook — the dashboard must remain fully functional offline without it.
2. **One file output.** `index.html` must stay self-contained. No separate `.css` or `.js` files, no `import`, no `fetch` of local assets. It has to work from `file://` by double-click.
3. **No browser storage.** No `localStorage`, no `sessionStorage`, no cookies. State lives in memory and in the URL hash.
4. **Thresholds live in data, not code.** Every RAG threshold is read from the workbook's `Config` sheet. Never hard-code a threshold in `src/app.html`.
5. **Colours come from CSS custom properties.** SVG uses `fill="var(--cat-1)"` etc. so light/dark swap without re-rendering. Never write a hex literal into chart code.

---

## Data model

Ten sheets. Parent links are by ID and must resolve — orphans are reported in the Data Health panel and excluded from rollups.

| Sheet | Links to parent via |
|---|---|
| `Priorities` | — |
| `Portfolios` | `PriorityID` |
| `Programs` | `PortfolioID` |
| `Projects` | `ProgramID` |
| `Milestones` / `Risks` / `Issues` / `LessonsLearned` | `ProjectID` |
| `Config` | — (thresholds, currency, reporting date) |

**Four columns drive everything.** All derived metrics come from these:

| Column | PMI term | Meaning |
|---|---|---|
| `BudgetAtCompletion` | BAC | Total approved budget |
| `PlannedValue` | PV | Budgeted cost of work **scheduled** to date |
| `EarnedValue` | EV | Budgeted cost of work **completed** to date |
| `ActualCost` | AC | Spent to date |

Everything else — SV, CV, SPI, CPI, EAC, VAC, every RAG status — is computed. Do not add a column that duplicates a derived value; compute it in `normalize()` instead.

---

## Formulas (PMI / PMBOK — do not invent variants)

```
SV  = EV − PV          negative = behind schedule
CV  = EV − AC          negative = over budget
SPI = EV ÷ PV          below 1.0 = behind schedule
CPI = EV ÷ AC          below 1.0 = over budget
EAC = BAC ÷ CPI        forecast total at current efficiency
VAC = BAC − EAC        negative = forecast overrun
risk exposure = Probability × Impact   (1–5 each, so 1–25)
```

These are implemented identically in two places — `scripts/build_xlsx.py` (as Excel formulas) and `src/app.html` (in `normalize()`). **If you change one, change both**, and re-run `npm test`.

## RAG rules

**Project level** — thresholds from `Config`:

| Dimension | Rule |
|---|---|
| Cost | CPI ≥ `CPI_Green` → green; ≥ `CPI_Amber` → amber; else red |
| Schedule | SPI ≥ `SPI_Green` → green; ≥ `SPI_Amber` → amber; else red |
| Risk | highest open exposure ≤ `Risk_Green` → green; ≤ `Risk_Amber` → amber; else red |
| Overall | worst of the three |

Projects in phase `0 - Requested` are `na`, not green — they have no performance to measure.

**Rollup level (program / portfolio / vision)** — the worst of **four** inputs:

| Input | Rule | Why it exists |
|---|---|---|
| Cost | aggregate CPI (Σ EV ÷ Σ AC) | standard |
| Schedule | aggregate SPI (Σ EV ÷ Σ PV) | standard |
| Risk concentration | share of projects red on risk vs `Rollup_RiskRed_Share` / `_Amber_` | **Do not replace with "worst single risk".** That was the original implementation and it turned every portfolio red — one severe risk anywhere dominated a fifty-project group and the indicator carried no information. |
| Delivery concentration | share of live projects red overall vs `Rollup_DeliveryRed_Share` / `_Amber_` | Prevents **aggregate masking** — a group whose totals look healthy while a quarter of its projects are individually failing. AI Smart City has SPI 1.02 / CPI 1.06 but 44% red projects; without this rule it reports green. |

`na` projects are excluded from the delivery-concentration denominator.

---

## Architecture of `src/app.html`

Sections are numbered in the file:

| § | Contents |
|---|---|
| 1 | Constants — phases, colour slot names |
| 2 | Helpers — formatting (`money`, `moneyC`, `pct`, `idx`), RAG functions |
| 3 | `normalize()` — builds indexes, computes every derived value, checks referential integrity into `PROBLEMS[]`. **`roll()` lives here** — the rollup function |
| 4 | State + filters (`state`, `passes()`, `filtered()`) |
| 5 | Chart primitives — all hand-written SVG |
| 6 | Shared blocks — `tiles()`, `drillCards()`, `projectTable()`, `attentionCard()`, `healthCard()` |
| 7 | Views — `viewOrg`, `viewLevel`, `viewProject` |
| 7b | **Navigator** — `navCascade`, `navMap`, `navMatrix`, `renderNav` |
| 8 | Routing — hash-based, `parseRoute`, `crumbsFor`, `render` |
| 9 | Wiring — delegated events, theme, tooltip, workbook loading |

### The navigator (§7b)

Three synchronised modes above every screen:

- **Cascade** — Miller columns (Vision │ Portfolios │ Programs │ Projects). Each column shows children of the selection to its left, or everything at that level if nothing is selected. This is the primary navigation surface and the one to keep fastest.
- **Map** — icicle chart, band width = budget share, colour = RAG. **It zooms**: the deepest selected node fills the width and only its subtree is drawn. The projects row only appears once inside a portfolio or program — at vision level 84 projects would be sub-pixel. Minimum band width is enforced with proportional redistribution (`MINW`) so no node is unclickable.
- **Matrix** — Portfolio × Phase (or × Department). This is the cross-cutting view.

**Why there is no Venn diagram.** It was requested and it is the wrong form: a Venn encodes *overlapping* sets, but this hierarchy is strictly nested — a project belongs to exactly one program. A Venn would imply intersections that cannot exist. The genuine cross-cutting dimensions are department and phase, which cut across portfolios, and that is what the Matrix mode shows. If someone asks for a Venn again, show them the Matrix.

---

## Charting rules

Follow these or the output stops being coherent:

- **Categorical**: fixed slot order `--cat-1` … `--cat-8`, assigned by entity, never by rank. A 9th category folds into "Other" — never generate a hue.
- **Sequential** (magnitude, heatmaps): `--seq-1` … `--seq-7`, one hue, light→dark.
- **Ordinal** (phases): `--ord-0` … `--ord-5`. `--ord-0` is neutral grey for "Requested" (pipeline, not yet approved).
- **Status** (RAG): `--st-good` / `--st-warn` / `--st-crit` / `--st-na`. Reserved for status **only** — never reuse as a series colour.
- **Never a dual-axis chart.** Two measures of different scale → two charts.
- **RAG is never colour alone.** Every chip carries a glyph (`✓ ! ✕ –`) and an accessible label.
- **Every chart has a table view.** The `chartCard()` wrapper provides the toggle — use it.
- Thin marks, hairline grid, no dashed gridlines, no number on every data point.

The palette was validated for colour-blind separation and contrast in both light and dark mode. If you change a colour, re-validate it — don't eyeball it.

---

## Testing

```bash
npm test
```

`tests/regression.spec.js` walks every drill path, all three navigator modes, filters, sorting, table toggles and dark mode, and fails on any console error.

`tests/verify_rollups.js` recomputes BAC, AC, EV, PV, SPI, CPI and EAC independently and asserts the page matches, and asserts that priority, portfolio and program totals each sum to the organisation total. **This is the test that matters** — it catches double-counting and leakage in the hierarchy, which are silent failures that look plausible on screen.

When you change `roll()` or `normalize()`, run this before anything else.

---

## Deploying

Static. Push the repo, point Vercel at it, no configuration needed — `index.html` at the root is served directly. No environment variables, no build command (or set it to `python3 scripts/build.py` if you want Vercel to rebuild from source).

---

## Known limitations (deliberate, not bugs)

- No authentication — the file is as private as wherever you put it
- Read-only — the dashboard never writes back to Excel
- No history/trending — needs periodic snapshots, which nothing captures yet
- No live integration with any PM tool
- Department count should stay ≤ 8; a 9th folds into "Other" in the Sankey

## The one thing to do early

**Start capturing dated snapshots of the workbook as soon as real data is loaded.** Every trend, velocity and forecasting feature depends on history, and history cannot be reconstructed later. The cheapest version is committing a dated copy of the workbook monthly.
