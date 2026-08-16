# Scope v2: Executive Portfolio Drill-Down
### Zero-cost architecture, PMP-aligned data model, and the build plan for Claude Code

**Prepared for:** bijoy
**Date:** 16 August 2026
**Supersedes:** the Teams4PM teardown scope of the same date
**Status:** working prototype delivered and verified

---

## 1. What changed, and why it is better

The first scope assumed you were rebuilding Teams4PM: connectors, a sync engine, a database, multi-tenant auth. Your revised direction removes all of it. What remains is the part that actually produces executive value.

| Dropped | Kept |
|---|---|
| Microsoft Graph / Jira / Monday connectors | A canonical project data model |
| Sync scheduler, job queue, delta tokens | Earned-value and RAG computation |
| Postgres, multi-tenancy, row-level security | The five-level drill-down |
| Entra ID SSO, RBAC | The visual reporting layer |
| Power BI licensing | Excel as the input surface |

**Effect on effort:** the original MVP was 9–11 weeks. This one is built. The remaining work is refinement, not construction.

**Effect on cost:** $0, permanently. Section 4 itemises it.

The trade you are making is real and worth stating plainly: data entry becomes manual. That is the correct trade at this stage — it lets you prove the reporting concept with executives before spending a single week on integration. If the drill-down does not change how your leadership team makes decisions, no connector would have saved it.

---

## 2. The concept

Five levels, each rolling up into the one above, each drillable down and navigable back:

```
Organisation          all priorities, portfolio-wide KPIs, the funnel, where work sits
    └─ Priority       strategic objective — portfolios beneath it
        └─ Portfolio  programs beneath it
            └─ Program    projects beneath it
                └─ Project    full PMP dashboard: EVM, milestones, risks, issues, lessons
```

Every level answers the same four executive questions in the same visual language, so the reader learns the interface once:

1. **How much is committed, and how much is spent?**
2. **Are we on schedule and on budget?** (SPI / CPI)
3. **What is off track, and what is driving it?** (RAG, with the driver named)
4. **What sits underneath this?** (drill down)

---

## 3. What has been built

A single self-contained HTML file — no install, no build step, no server. Double-click to open. Delivered as both a standalone file and a structured repository ready for Claude Code (Section 11).

**The hierarchy navigator** — persistent above every screen, in three synchronised modes:

- **Cascade** — a four-column browser (Vision │ Portfolios │ Programs │ Projects). Each column shows the children of the selection to its left, so you can move down *and sideways* without going back. Every row carries RAG, project count and budget. This is the primary navigation surface.
- **Map** — an icicle chart of the entire programme: band width is share of approved budget, colour is RAG. It **zooms** — the deepest selected node fills the width and only its subtree is drawn, with the projects row appearing once you are inside a portfolio. Minimum band widths are enforced by proportional redistribution so no project is ever too small to click.
- **Matrix** — Portfolio × Phase, switchable to Portfolio × Department, with row and column totals. Clicking a cell opens that portfolio filtered to that slice.

The navigator auto-collapses to a compact path strip at project level so the detail screen has room, and can be collapsed or expanded manually at any level.

**Why there is no Venn diagram.** You asked for one and it is the wrong instrument: a Venn encodes *overlapping* sets, but this hierarchy is strictly nested — a project belongs to exactly one program, one portfolio, one vision. Drawing it as a Venn would imply intersections that cannot exist and would misrepresent the data. The dimensions that genuinely cut across portfolios are **department** and **phase**, and that is exactly what the Matrix mode crosses. It gives you the "where does work overlap" answer a Venn was reaching for, without asserting something false.

**Organisation level**

- Eight KPI tiles: projects in scope with a RAG strip, approved budget, actual cost, forecast at completion with over/underrun, SPI, CPI, open risks, open issues
- Projects by phase (PMBOK process groups, ordinal ramp)
- Approved budget by priority
- Data health panel — referential integrity checked on load
- **Where the work sits** — a Sankey flowing department into delivery phase (the Teams4PM signature visual, rebuilt)
- Needs attention — amber and red by budget, each naming the dimension driving it
- **Schedule vs cost quadrant** — every project plotted SPI against CPI, bubble sized by budget, quadrants labelled, clickable
- Open risk exposure — 5×5 probability/impact heatmap
- Priority cards and the full sortable project register

**Priority / Portfolio / Program levels** — the same KPI tiles and charts scoped to that node, plus budget by child entity and drill cards for the level below.

**Project level** — overall status, % complete, budget, EAC/VAC, SPI, CPI, risks, issues; project facts; earned-value analysis; milestone schedule showing baseline against forecast with slip in days; risk matrix; full risk register sorted by exposure; issue log sorted by severity; lessons learned.

**Throughout** — filters (department, phase, RAG, free-text search) applied once above everything and persisted across drill levels; breadcrumbs plus working browser back; every chart has a table view for accessibility; light and dark mode; drag-and-drop workbook loading.

---

## 4. Cost

| Component | Choice | Cost |
|---|---|---|
| Application | Single HTML file, hand-written SVG charts | $0 — no library, no licence |
| Spreadsheet reader | SheetJS Community Edition (Apache 2.0) via free CDN | $0 |
| Data entry | Excel, or LibreOffice / Google Sheets | $0 |
| Source control | GitHub free tier | $0 |
| Hosting | Vercel Hobby | $0 |
| Runtime | None — the file is the application | $0 |
| **Total** | | **$0** |

No database, no server, no API keys, no per-seat licence, nothing that can invoice you later. The single external dependency is SheetJS, loaded only when a workbook is dropped — the dashboard runs fully offline on its embedded data without it.

---

## 5. Data model

Ten sheets. Four columns do the heavy lifting.

| Sheet | Purpose | Links via |
|---|---|---|
| `Priorities` | Organisational objectives | — |
| `Portfolios` | Grouped investment | `PriorityID` |
| `Programs` | Related projects | `PortfolioID` |
| `Projects` | **The main sheet** | `ProgramID` |
| `Milestones` | Baseline vs forecast dates | `ProjectID` |
| `Risks` | Register with P × I scoring | `ProjectID` |
| `Issues` | Issue log with severity | `ProjectID` |
| `LessonsLearned` | Captured lessons | `ProjectID` |
| `Config` | RAG thresholds, currency, reporting date | — |
| `README` | Legend and formula reference | — |

**The four columns that drive everything:**

| Column | PMI term | Meaning |
|---|---|---|
| `BudgetAtCompletion` | BAC | Total approved budget |
| `PlannedValue` | PV | Budgeted cost of work *scheduled* to date |
| `EarnedValue` | EV | Budgeted cost of work *completed* to date |
| `ActualCost` | AC | Spent to date |

Everything else — variances, indices, forecasts, all RAG statuses — is derived. If your PMs only ever maintain four columns reliably, make it these four.

---

## 6. Formulas and RAG rules

All PMI/PMBOK standard, computed identically in the workbook and the dashboard:

| Measure | Formula | Reading |
|---|---|---|
| Schedule variance | `SV = EV − PV` | Negative = behind schedule |
| Cost variance | `CV = EV − AC` | Negative = over budget |
| Schedule performance index | `SPI = EV ÷ PV` | Below 1.0 = behind |
| Cost performance index | `CPI = EV ÷ AC` | Below 1.0 = over |
| Estimate at completion | `EAC = BAC ÷ CPI` | Forecast total at current efficiency |
| Variance at completion | `VAC = BAC − EAC` | Negative = forecast overrun |
| Risk exposure | `P × I` | 1–25 |

**Project RAG** — thresholds live on the `Config` sheet, never in code:

- Cost: CPI ≥ 0.95 green · ≥ 0.85 amber · below red
- Schedule: SPI ≥ 0.95 green · ≥ 0.85 amber · below red
- Risk: highest open exposure ≤ 8 green · ≤ 14 amber · above red
- Overall: the worst of the three

**Rollup RAG — two decisions worth understanding.** A portfolio's status is the worst of four inputs, not three. Cost and schedule aggregate their earned-value inputs, which is standard practice. The other two are concentration measures, and both exist to fix a specific failure:

| Input | Rule | The failure it prevents |
|---|---|---|
| Cost | Aggregate CPI vs thresholds | — |
| Schedule | Aggregate SPI vs thresholds | — |
| **Risk concentration** | Share of projects red on risk (≥30% red, ≥15% amber) | One severe risk anywhere turning a fifty-project portfolio red. The first build did this and every portfolio went red, so the indicator carried no information. |
| **Delivery concentration** | Share of live projects red overall (≥30% red, ≥15% amber) | *Aggregate masking* — a portfolio whose totals look healthy while a quarter of its projects are individually failing. In the current data, AI Smart City has SPI 1.02 and CPI 1.06 but 44% of its projects red. Without this rule it would report green. |

All four sets of thresholds live on the `Config` sheet, not in code.

---

## 7. Verification performed

| Check | Result |
|---|---|
| Workbook formulas recalculated (LibreOffice) | 729 formulas, **0 errors** |
| SPI, CPI, EAC, SV, CV spot-checked against independent Python | **Exact match** |
| Dashboard rollups vs independent Python sums (BAC, AC, EV, PV, SPI, CPI, EAC) | **Exact match** |
| Priority, portfolio and program totals each sum to the org total | **Exact match** — no leakage, no double-counting |
| Referential integrity across all five levels | **No broken links** |
| Drill-down, breadcrumbs, browser back, filters, sorting, table views, dark mode | **All pass** |
| Browser console errors | **None** |
| Chart palette — CVD separation, contrast, ordinal spacing, light and dark | **Validated** |

---

## 8. Build plan from here

**Phase 1 — Load your own data (days, not weeks).** Replace the sample rows with two or three real programs. Do not convert everything; prove the shape first. Expect the `Config` thresholds to need tuning against how your PMO already defines green.

**Phase 2 — Show it to one executive.** Everything after this should be driven by what they ask for in that meeting, not by this document.

**Phase 3 — Port to Vercel.** Create a repo, put the file at `index.html`, connect the repo to Vercel. It deploys as a static site with no configuration. Add the workbook as a committed `data.json` if you want it to load without a drop.

**Phase 4 — Refinements likely to surface.** Trend over time (needs periodic snapshots — see the warning below); benefits tracking; resource and capacity view; scheduled PDF or email export; per-user landing level.

**Phase 5 — AI, once the base is mature.** The highest-return additions are narrative status summaries grounded in the computed metrics, and natural-language query over the project set ("which projects slipped this quarter?"). Both are thin layers over data you already have. Predictive forecasting is not buildable until Phase 4 snapshots have accumulated several months of history.

**Working with Claude Code:** keep the data model, the formula table, and the RAG rules from Sections 5 and 6 in a `CLAUDE.md` at the repo root. Ambiguity in those three areas is the main thing that produces inconsistent generated code across a build like this.

---

## 9. The one thing to decide early

**Start capturing periodic snapshots as soon as you load real data.** Every trend, velocity, and predictive feature depends on having history, and history cannot be reconstructed later. The cheapest possible version is committing a dated copy of the workbook to the repo each month. It costs nothing now and is expensive to retrofit — this was the same warning in the first scope, and it is the only one that survives the change in direction unchanged.

---

## 10. Deliberate exclusions

Not built, and not oversights: no authentication (the file is as private as wherever you put it), no write-back to Excel (the dashboard reads, it does not edit), no live integration, no per-user permissions, no server-side anything. Each is addable later. None is needed to prove whether executives will use this.

---

## 11. Handing this to Claude Code

The dashboard is now a proper repository rather than a loose file:

```
portfolio-dashboard/
  CLAUDE.md          the spec Claude Code works from — read this first
  README.md          how to run, build and deploy
  index.html         BUILD OUTPUT — never hand-edit
  src/app.html       the source
  data/              dataset + Excel template
  scripts/           gen_data.py · build_xlsx.py · build.py
  tests/             regression.spec.js · verify_rollups.js
  package.json       npm run all · npm test · npm run serve
```

**`CLAUDE.md` is the important file.** It carries the data model, the exact PMI formulas, the RAG rules, the charting constraints, and — most usefully — the decisions that *look* like bugs but are not. Without it, a future session will "fix" rollup risk back to worst-single-risk and turn every portfolio red again. It also records the hard constraints: no dependencies, one output file, no browser storage, thresholds in data rather than code.

**Two tests, and one of them matters more.** `regression.spec.js` walks every drill path, all three navigator modes, filters, sorting and dark mode, failing on any console error. `verify_rollups.js` independently recomputes the earned-value aggregates and asserts the page matches, then asserts each hierarchy level sums to the organisation total. Run the second one after any change to `roll()` or `normalize()` — double-counting and leakage are silent failures that still look plausible on screen.

**First commands:**

```bash
cd portfolio-dashboard
npm install && npm test      # confirm the baseline is green
npm run serve                # http://localhost:8000
```

---

## Files delivered

| File | What it is |
|---|---|
| `portfolio-dashboard.html` | The application. Self-contained, opens by double-click, ships with sample data |
| `Portfolio_Reporting_Template.xlsx` | The data template — ten sheets, formulas, dropdowns, README legend, sample rows |
| `scope-v2-portfolio-drilldown.md` | This document |

All sample data is synthetic. No figure in it comes from a real organisation.

---

## Appendix — the sample portfolio structure

One apex priority, four portfolios, 17 programs, 84 projects, **$57.76B** approved. Portfolio (a) uses your examples verbatim; (b), (c) and (d) follow the sequence national AI programmes actually run in — **build the physical layer, commercialise the compute, deploy it sector by sector, then land it in the city.**

The budget shape is deliberate and matches how these programmes really spend: foundation and compute absorb 89% of capital, while use cases and smart city — where the economic return is claimed — are comparatively cheap.

```
Leading Country to build an AI-Enabled Economy                    $57.76B

├── a) Nationwide Foundation Layers                    18 proj    $36.33B  (63%)
│   ├── Datacenters              200MW Tier III — Thor · 1GW Liquid-Cooled — IronMan
│   │                            500MW Tier IV — Valkyrie · Modular Edge Cluster — Sentinel
│   │                            Subsea Landing & Interconnect — Poseidon · Sovereign Cloud — Asgard
│   ├── G2G Contracts            GPU Supply (USA, India, UK) · Cross-Continent Connectivity (EU, NA, India)
│   │                            Export Control & Chip Compliance · Bilateral AI Talent Mobility
│   │                            Joint Sovereign AI Research Pact · Cross-Border Data Adequacy
│   └── National Grids           4 Freezone AI Campuses · Powergrid Upgrade Site A/B
│                                3GW Solar + Storage · SMR Feasibility for Baseload
│                                National Fibre Backbone Ring · Grid Interconnect & Substations
│
├── b) AI Compute & B2B Agreements                     20 proj    $15.02B  (26%)
│   ├── Compute Capacity &       National Compute Exchange · GPU-as-a-Service Launch
│   │   Allocation               Compute Credits for SMEs · Research Allocation Framework
│   │                            Utilisation, Metering & Chargeback
│   ├── Strategic Vendor & OEM   Multi-Year Accelerator Framework (Tier 1) · Second-Source Agreement
│   │                            Networking & Interconnect Supply · Liquid Cooling OEM Partnership
│   │                            Semiconductor Assembly & Test JV · Maintenance & Spares Framework
│   ├── Hyperscaler & Cloud      Hyperscaler Region Landing · Sovereign Cloud JV
│   │                            Enterprise Migration Incentives · Cross-Border Compute Reciprocity
│   └── Sovereign Model          Foundation Model Training Run 1 · Sovereign Language Multimodal
│                                Model Evaluation & Red-Team Facility · Open Weights Release
│                                Inference Optimisation & Serving Stack
│
├── c) AI Use Case Developments                        25 proj     $3.56B  (6%)
│   ├── Government Services      Citizen Copilot · Automated Permits · Border AI Screening
│   │                            Court Case Triage · Document Intelligence · Procurement Fraud
│   ├── Healthcare               Radiology Triage (14 hospitals) · National Genomics Platform
│   │                            Predictive Bed Management · Clinical Documentation · Risk Stratification
│   ├── Education & Workforce    K-12 AI Literacy Curriculum · 100k Practitioner Reskilling
│   │                            University AI Chairs · Adaptive Learning Pilot · Certification Framework
│   ├── Industry & Energy        Refinery Predictive Maintenance · Grid Load Forecasting
│   │                            Port & Logistics Optimisation · Water Leak Detection · Agri Yield
│   └── Financial & RegTech      AML Monitoring Uplift · Real-Time Payments Fraud
│                                Regulatory Reporting Automation · Thin-File Credit Decisioning
│
└── d) AI Smart City                                   21 proj     $2.86B  (5%)
    ├── Urban Digital Twin       City-Scale 3D Twin Ph1 · Sensor Mesh · Planning Simulation
    │                            Construction Progress Monitoring
    ├── Intelligent Mobility     Adaptive Traffic Signals · Autonomous Shuttle Pilot
    │                            Transit Demand Prediction · Smart Parking · EV Charging Optimisation
    ├── Public Safety            Emergency Dispatch AI · Flood & Heat Early Warning
    │                            Crowd Density Monitoring · Video Analytics Privacy Framework
    ├── Smart Utilities          Smart Metering (1.2M premises) · District Cooling Optimisation
    │                            Building Energy Management · Waste Route Optimisation
    └── Citizen Experience       Unified Digital Identity Wallet · Single Citizen Portal
                                 Multilingual Citizen Assistant · Accessibility & Inclusion
```

**Modelling detail that makes the numbers behave realistically.** Each project carries an archetype — `infra`, `deal`, `plat` or `deploy` — which drives its duration, budget band, milestone set, risk register and earned-value volatility. Infrastructure runs long with grid and supply-chain risks; agreements carry geopolitical and export-control risks; platform work carries technical and talent risks; deployments carry adoption and regulator risks. Milestone sets differ accordingly — a datacenter passes *Grid Connection Agreement* and *Power Energisation*, a G2G contract passes *Term Sheet Agreed* and *Ratification Complete*.

**One thing to change when you make this yours.** The eight departments are generic national-government functions — AI Office, Digital Infrastructure, Energy & Utilities, Foreign Affairs & Trade, Health & Education, Transport & Municipality, Finance & Economy, Interior & Safety. Swap them for your actual entity names on the `Projects` sheet. Keep the count at eight or fewer: the Sankey assigns a distinct, colourblind-validated hue per department and folds any ninth into "Other".
