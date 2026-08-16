#!/usr/bin/env python3
"""National AI-economy portfolio dataset -> JSON + Excel template.

Structure follows the segmentation supplied by the user: a single apex priority,
four portfolios, programs beneath each, projects beneath those. Portfolio (a) uses
the user's own examples; (b), (c) and (d) are built out on the same logic that
national AI programmes actually follow: build the physical layer, commercialise the
compute, deploy it sector by sector, then land it in the urban fabric.
"""
import json, random, datetime as dt

random.seed(20260816)
TODAY = dt.date(2026, 8, 16)

DEPTS = ["AI Office", "Digital Infrastructure", "Energy & Utilities", "Foreign Affairs & Trade",
         "Health & Education", "Transport & Municipality", "Finance & Economy", "Interior & Safety"]

PHASES = ["0 - Requested", "1 - Initiating", "2 - Planning",
          "3 - Executing", "4 - Monitoring & Controlling", "5 - Closing"]

PRIORITIES = [
    ("PR-01", "Leading Country to build an AI-Enabled Economy",
     "Establish sovereign AI capability end to end — compute, energy, agreements, "
     "sector deployment and urban infrastructure — and convert it into economic output.",
     "H.E. Council Chair", 1.00),
]

# ---------------------------------------------------------------------------
# portfolio -> program -> [(project name, archetype, budget band)]
# archetype drives duration, milestone set, risk profile and EVM behaviour
#   infra  = heavy capex construction / energy
#   deal   = government-to-government or commercial agreement
#   plat   = platform / model / compute engineering
#   deploy = sector use-case deployment
# ---------------------------------------------------------------------------
STRUCTURE = [
 ("PF-01", "Nationwide Foundation Layers", "Digital Infrastructure", "Dr. A. Al Marri",
  "Sovereign compute, energy and connectivity substrate the whole economy runs on", [

  ("PG-01", "Datacenters", "Digital Infrastructure", "R. Nakamura", [
    ("200MW Tier III Facility — Thor",                 "infra", "xl"),
    ("1GW Liquid-Cooled Facility — IronMan",           "infra", "xxl"),
    ("500MW Tier IV Facility — Valkyrie",              "infra", "xl"),
    ("Modular Edge DC Cluster — Sentinel (12 sites)",  "infra", "l"),
    ("Subsea Cable Landing & DC Interconnect — Poseidon","infra","l"),
    ("Sovereign Cloud Region — Asgard",                "plat",  "l"),
  ]),
  ("PG-02", "G2G Contracts", "Foreign Affairs & Trade", "L. Bergstrom", [
    ("GPU Supply Agreements — USA, India, UK",         "deal", "xxl"),
    ("Cross-Continent Connectivity — EU, NA, India",   "deal", "xl"),
    ("Export Control & Chip Compliance Framework",     "deal", "m"),
    ("Bilateral AI Talent Mobility Accord",            "deal", "s"),
    ("Joint Sovereign AI Research Pact — Korea, Japan","deal", "m"),
    ("Cross-Border Data Adequacy Agreements",          "deal", "s"),
  ]),
  ("PG-03", "National Grids", "Energy & Utilities", "K. Duarte", [
    ("4 Freezone AI Campuses Across Country",          "infra", "xxl"),
    ("Powergrid Upgrade — Site A and Site B",          "infra", "xl"),
    ("3GW Solar + Storage for Compute Load",           "infra", "xxl"),
    ("SMR Feasibility for Compute Baseload",           "infra", "l"),
    ("National Fibre Backbone Ring",                   "infra", "l"),
    ("Grid Interconnect & Substation Programme",       "infra", "l"),
  ]),
 ]),

 ("PF-02", "AI Compute & B2B Agreements", "AI Office", "S. Ramaswamy",
  "Turn installed capacity into a traded, commercially governed national asset", [

  ("PG-04", "Compute Capacity & Allocation", "AI Office", "T. Ivanova", [
    ("National Compute Exchange Platform",             "plat",  "l"),
    ("GPU-as-a-Service Commercial Launch",             "plat",  "m"),
    ("Compute Credits Scheme for SMEs & Startups",     "deploy","m"),
    ("Research Compute Allocation Framework",          "deploy","s"),
    ("Utilisation, Metering & Chargeback System",      "plat",  "m"),
  ]),
  ("PG-05", "Strategic Vendor & OEM Agreements", "Finance & Economy", "H. Lindqvist", [
    ("Multi-Year Accelerator Framework — Tier 1 OEM",  "deal", "xxl"),
    ("Second-Source Accelerator Agreement",            "deal", "xl"),
    ("Networking & Interconnect Supply Agreement",     "deal", "l"),
    ("Liquid Cooling OEM Partnership",                 "deal", "m"),
    ("Semiconductor Assembly & Test Joint Venture",    "infra","xl"),
    ("Hardware Maintenance & Spares Framework",        "deal", "m"),
  ]),
  ("PG-06", "Hyperscaler & Cloud Partnerships", "Digital Infrastructure", "J. Alvarez", [
    ("Hyperscaler Region Landing — Partner A",         "infra","xl"),
    ("Sovereign Cloud Joint Venture",                  "deal", "l"),
    ("Enterprise Migration Incentive Programme",       "deploy","m"),
    ("Cross-Border Compute Reciprocity Agreements",    "deal", "m"),
  ]),
  ("PG-07", "Sovereign Model Programme", "AI Office", "C. Nwosu", [
    ("National Foundation Model — Training Run 1",     "plat", "xl"),
    ("Sovereign Language Multimodal Model",            "plat", "l"),
    ("Model Evaluation & Red-Team Facility",           "plat", "m"),
    ("Open Model Weights Release Programme",           "plat", "s"),
    ("Inference Optimisation & Serving Stack",         "plat", "m"),
  ]),
 ]),

 ("PF-03", "AI Use Case Developments", "AI Office", "P. Mensah",
  "Convert capability into measurable outcomes, sector by sector", [

  ("PG-08", "Government Services AI", "AI Office", "N. Haddad", [
    ("Citizen Services Copilot",                       "deploy","l"),
    ("Automated Permits & Licensing",                  "deploy","m"),
    ("Immigration & Border AI Screening",              "deploy","l"),
    ("Court Case Triage & Legal Research Assistant",   "deploy","m"),
    ("National Document Intelligence Platform",        "plat",  "m"),
    ("Procurement Fraud Detection",                    "deploy","s"),
  ]),
  ("PG-09", "Healthcare AI", "Health & Education", "Dr. F. Rossi", [
    ("Radiology Triage Deployment — 14 Hospitals",     "deploy","m"),
    ("National Genomics AI Platform",                  "plat",  "l"),
    ("Predictive Bed & Capacity Management",           "deploy","s"),
    ("Clinical Documentation Assistant",               "deploy","m"),
    ("Population Health Risk Stratification",          "deploy","s"),
  ]),
  ("PG-10", "Education & Workforce AI", "Health & Education", "G. Tanaka", [
    ("AI Literacy Curriculum — National K-12 Rollout", "deploy","l"),
    ("100k AI Practitioner Reskilling Programme",      "deploy","xl"),
    ("University AI Research Chairs",                  "deploy","m"),
    ("Adaptive Learning Platform Pilot",               "deploy","s"),
    ("National AI Certification Framework",            "deploy","s"),
  ]),
  ("PG-11", "Industry & Energy AI", "Energy & Utilities", "R. Bhatt", [
    ("Predictive Maintenance — National Refineries",   "deploy","m"),
    ("Grid Load Forecasting & Optimisation",           "plat",  "m"),
    ("Port & Logistics Optimisation",                  "deploy","m"),
    ("Water Network Leak Detection",                   "deploy","s"),
    ("Agricultural Yield Optimisation",                "deploy","s"),
  ]),
  ("PG-12", "Financial Services & RegTech AI", "Finance & Economy", "L. Moreau", [
    ("AML Transaction Monitoring Uplift",              "deploy","m"),
    ("Real-Time Payments Fraud Engine",                "plat",  "m"),
    ("Regulatory Reporting Automation",                "deploy","s"),
    ("Credit Decisioning for Thin-File Segments",      "deploy","s"),
  ]),
 ]),

 ("PF-04", "AI Smart City", "Transport & Municipality", "V. Petrova",
  "Land the capability in the physical city — mobility, safety, utilities, identity", [

  ("PG-13", "Urban Digital Twin", "Transport & Municipality", "I. Fernandes", [
    ("City-Scale 3D Digital Twin — Phase 1",           "plat", "l"),
    ("Real-Time Sensor Mesh Deployment",               "infra","m"),
    ("Urban Planning Simulation Engine",               "plat", "m"),
    ("Construction Progress Monitoring AI",            "deploy","s"),
  ]),
  ("PG-14", "Intelligent Mobility", "Transport & Municipality", "M. Osei", [
    ("Adaptive Traffic Signal Network",                "infra","l"),
    ("Autonomous Shuttle Pilot — District 1",          "deploy","m"),
    ("Multimodal Transit Demand Prediction",           "plat", "s"),
    ("Smart Parking & Curb Management",                "deploy","s"),
    ("EV Charging Network Optimisation",               "infra","m"),
  ]),
  ("PG-15", "Public Safety & Emergency AI", "Interior & Safety", "B. Okafor", [
    ("Emergency Response Dispatch AI",                 "deploy","m"),
    ("Flood & Heat Early Warning System",              "plat", "m"),
    ("Crowd Density Monitoring — Major Venues",        "deploy","s"),
    ("Video Analytics Privacy & Governance Framework", "deploy","s"),
  ]),
  ("PG-16", "Smart Utilities & Buildings", "Energy & Utilities", "D. Kaur", [
    ("Smart Metering Rollout — 1.2M Premises",         "infra","xl"),
    ("District Cooling Optimisation",                  "deploy","m"),
    ("Building Energy Management AI",                  "deploy","m"),
    ("Waste Collection Route Optimisation",            "deploy","s"),
  ]),
  ("PG-17", "Citizen Experience & Digital ID", "Interior & Safety", "E. Castellani", [
    ("Unified Digital Identity Wallet",                "plat", "l"),
    ("Single Citizen Portal Consolidation",            "deploy","m"),
    ("Multilingual Citizen Assistant",                 "deploy","m"),
    ("Accessibility & Inclusion Programme",            "deploy","s"),
  ]),
 ]),
]

# archetype -> (duration days range, EVM volatility, risk count range)
ARCH = {
    "infra":  ((520, 1500), 0.17, (2, 6)),
    "deal":   ((180,  760), 0.14, (2, 6)),
    "plat":   ((300,  900), 0.13, (1, 5)),
    "deploy": ((150,  560), 0.11, (0, 4)),
}
# budget bands in USD
BAND = {"s": (3e6, 25e6), "m": (25e6, 140e6), "l": (140e6, 700e6),
        "xl": (700e6, 2.6e9), "xxl": (2.6e9, 9.5e9)}

MILESTONES = {
 "infra": ["Site Selection Approved","Land & Permits Secured","Grid Connection Agreement",
           "Design Authority Approval","Construction Start","Power Energisation",
           "Equipment Installation Complete","Commissioning & Test","Operational Handover"],
 "deal":  ["Mandate Approved","Counterpart Engagement Opened","Term Sheet Agreed",
           "Legal & Compliance Review","Cabinet / Board Approval","Signature",
           "Ratification Complete","First Delivery Received"],
 "plat":  ["Architecture Baselined","Data Access Agreed","Environment Provisioned",
           "Build Complete","Security Accreditation","Evaluation & Red-Team Passed",
           "Production Go-Live","Benefits Review"],
 "deploy":["Business Case Approved","Requirements Baselined","Data Sharing Agreement",
           "Model Development Complete","Pilot Live","Change & Training Complete",
           "Scaled Rollout","Benefits Review"],
}

RISKS = {
 "infra": [("Transformer and switchgear lead times exceed 18 months","Supply Chain"),
           ("Grid connection date slips beyond facility readiness","Energy & Grid"),
           ("Water availability constraint at campus site","Environmental"),
           ("Construction labour availability in peak season","Resource"),
           ("Cooling plant single-sourced with no qualified alternate","Supply Chain"),
           ("Land handover contingent on unresolved zoning approval","Regulatory"),
           ("Commissioning window collides with summer peak load","Schedule"),
           ("Escalation in structural steel and copper pricing","Cost")],
 "deal":  [("Export licence approval slower than programme assumption","Geopolitical"),
           ("Counterpart position may shift after national elections","Geopolitical"),
           ("Chip allocation reduced by vendor under global demand","Supply Chain"),
           ("Data adequacy ruling may require architecture rework","Regulatory"),
           ("Currency exposure on multi-year hardware commitment","Cost"),
           ("Sanctions regime change affects delivery route","Geopolitical"),
           ("Counterpart legal review extends beyond target signature","Schedule"),
           ("Offset and local-content obligations not yet costed","Cost")],
 "plat":  [("Training run may not converge within allocated compute budget","Technical"),
           ("Model evaluation standards not yet defined by regulator","Regulatory"),
           ("Scarce ML platform talent attrition to private sector","Talent"),
           ("Cybersecurity accreditation not complete before go-live","Cyber"),
           ("Inference cost per token above commercial viability","Cost"),
           ("Upstream data quality insufficient for target accuracy","Technical"),
           ("Dependency on a single accelerator generation","Vendor"),
           ("Benchmark performance unverified at production scale","Technical")],
 "deploy":[("Business availability for testing below plan","Resource"),
           ("Frontline adoption capacity constrained by change load","Change Adoption"),
           ("Source system data access agreement unsigned","Regulatory"),
           ("Benefit assumptions untested with end users","Benefits"),
           ("Model bias review may require retraining","Regulatory"),
           ("Integration with legacy case system undocumented","Technical"),
           ("Sector regulator approval outstanding","Regulatory"),
           ("Operating model for post-go-live support undefined","Resource")],
}
RESPONSES = ["Mitigate", "Accept", "Transfer", "Avoid"]

ISSUES = [
 "Vendor delivery slipped against contracted milestone",
 "Interministerial approval overdue from sponsoring department",
 "Environment unavailable since the last platform release",
 "Data sharing agreement rejected by the source authority",
 "Defect backlog above agreed exit criteria",
 "Approved budget not yet released by treasury",
 "Accuracy benchmark not met in evaluation testing",
 "Key technical lead resigned from the delivery squad",
 "Upstream dependency milestone missed by another programme",
 "Security review raised findings blocking accreditation",
 "Scope change requested without an identified funding source",
 "Contractor claim in dispute, blocking milestone certification",
 "Site access delayed pending safety clearance",
 "Counterpart has not confirmed the ratification timetable",
]

LESSONS = [
 ("Grid connection lead time was assumed, not confirmed with the utility",
  "Make a written utility connection date a gate condition before capital release"),
 ("Export licence dependency surfaced only at contract signature",
  "Run an export-control assessment during business case, not after"),
 ("Compute was procured before the workload profile was understood",
  "Baseline the workload mix before committing to accelerator generation"),
 ("Sector regulator was engaged only at pilot stage",
  "Bring the regulator into design review for any citizen-facing model"),
 ("Benefit telemetry was not instrumented at go-live",
  "Make benefit measurement a mandatory acceptance criterion"),
 ("Three departments built overlapping document AI capability",
  "Route all sector use cases through a central capability register first"),
 ("Contingency was consumed before the executing phase began",
  "Hold contingency at portfolio level and release it by exception"),
 ("Change network stood up too late for frontline adoption",
  "Appoint change leads at the same time as the project manager"),
 ("Model evaluation criteria were agreed after training had started",
  "Fix evaluation and red-team criteria before the first training run"),
 ("Bilateral agreement lacked an agreed dispute mechanism",
  "Require a dispute and exit clause in every G2G term sheet"),
]
LESSON_CATS = ["Planning","Stakeholder","Procurement","Quality","Risk","Resource",
               "Communication","Governance"]


def d(base, n): return base + dt.timedelta(days=n)
def iso(x): return x.isoformat() if x else ""


priorities = [dict(PriorityID=a, PriorityName=b, Description=c, ExecutiveSponsor=e,
                   WeightPct=w, FY="FY2026") for a, b, c, e, w in PRIORITIES]
portfolios, programs, projects = [], [], []
milestones, risks, issues, lessons = [], [], [], []
pid = 0

for pf_id, pf_name, pf_dept, pf_owner, pf_desc, progs in STRUCTURE:
    portfolios.append(dict(PortfolioID=pf_id, PortfolioName=pf_name, PriorityID="PR-01",
                           PortfolioOwner=pf_owner, Department=pf_dept))
    for pg_id, pg_name, pg_dept, pg_mgr, projs in progs:
        programs.append(dict(ProgramID=pg_id, ProgramName=pg_name,
                             PortfolioID=pf_id, ProgramManager=pg_mgr))
        for name, arch, band in projs:
            pid += 1
            code = f"PJ-{pid:03d}"
            (dmin, dmax), vol, (rmin, rmax) = ARCH[arch]
            phase = random.choices(PHASES, weights=[13, 14, 16, 28, 17, 12])[0]
            px = PHASES.index(phase)
            dept = pg_dept if random.random() < 0.72 else random.choice(DEPTS)

            dur = random.randint(dmin, dmax)
            # older, bigger things started earlier
            age = random.uniform(0.06, 0.96) if px else random.uniform(0.0, 0.10)
            start = d(TODAY, -int(dur * age) - random.randint(0, 90))
            base_fin = d(start, dur)

            elapsed = max(0.0, min(1.0, (TODAY - start).days / dur))
            planned = elapsed
            if px == 0: planned = 0.0
            elif px == 1: planned = min(planned, 0.10)
            elif px == 2: planned = min(planned, 0.28)
            elif px == 5: planned = max(planned, 0.93)

            spi_t = min(max(random.gauss(0.985, vol), 0.52), 1.20)
            actual = min(max(planned * spi_t, 0.0), 1.0)
            if px == 0: actual = 0.0
            if px == 5: actual = max(actual, 0.90)

            lo, hi = BAND[band]
            bac = round(random.uniform(lo, hi), -5)
            pv = round(bac * planned, 2)
            ev = round(bac * actual, 2)
            cpi_t = min(max(random.gauss(0.995, vol * 0.85), 0.62), 1.22)
            ac = round(ev / cpi_t, 2) if ev > 0 else 0.0
            if px == 0: pv = ev = ac = 0.0

            slip = int(round((1 - min(spi_t, 1.15)) * dur * 0.38))
            fc_fin = d(base_fin, max(slip, 0) + random.randint(-10, 25))

            projects.append(dict(
                ProjectID=code, ProjectName=name, ProgramID=pg_id, ProjectManager=pg_mgr,
                Department=dept, Phase=phase,
                Status="Closed" if (px == 5 and random.random() < .45) else
                       ("On Hold" if random.random() < .04 else "Active"),
                StartDate=iso(start), BaselineFinish=iso(base_fin), ForecastFinish=iso(fc_fin),
                PercentComplete=round(actual, 4), BudgetAtCompletion=bac,
                PlannedValue=pv, EarnedValue=ev, ActualCost=ac, Sponsor=pf_owner,
                BusinessCase=f"{pf_desc}. Delivered under {pg_name}."))

            # milestones, in canonical order
            pool = MILESTONES[arch]
            nms = random.randint(4, min(7, len(pool)))
            for i, mi in enumerate(sorted(random.sample(range(len(pool)), nms))):
                frac = (i + 1) / (nms + 1)
                bd = d(start, int(dur * frac))
                fd = d(bd, random.randint(-6, max(slip, 1) + 16))
                done = fd <= TODAY and random.random() < 0.86
                milestones.append(dict(
                    MilestoneID=f"MS-{len(milestones)+1:04d}", ProjectID=code,
                    MilestoneName=pool[mi], BaselineDate=iso(bd), ForecastDate=iso(fd),
                    ActualDate=iso(fd) if done else "",
                    Status="Complete" if done else ("Overdue" if fd < TODAY else "Planned")))

            # risks
            if px > 0:
                for title, cat in random.sample(RISKS[arch], random.randint(rmin, min(rmax, len(RISKS[arch])))):
                    p_ = random.choices([1,2,3,4,5], weights=[16,31,29,17,7])[0]
                    i_ = random.choices([1,2,3,4,5], weights=[12,27,32,21,8])[0]
                    risks.append(dict(
                        RiskID=f"RK-{len(risks)+1:04d}", ProjectID=code, RiskTitle=title,
                        Category=cat, Probability=p_, Impact=i_,
                        Response=random.choice(RESPONSES), Owner=pg_mgr,
                        Status=random.choices(["Open","Monitoring","Closed"], weights=[5,3,2])[0],
                        DueDate=iso(d(TODAY, random.randint(-90, 300)))))

            # issues
            if px >= 2:
                for t in random.sample(ISSUES, random.randint(0, 5)):
                    raised = d(TODAY, -random.randint(1, 300))
                    issues.append(dict(
                        IssueID=f"IS-{len(issues)+1:04d}", ProjectID=code, IssueTitle=t,
                        Severity=random.choices(["Critical","High","Medium","Low"], weights=[1,3,5,3])[0],
                        Owner=pg_mgr, RaisedDate=iso(raised),
                        TargetDate=iso(d(raised, random.randint(14, 150))),
                        Status=random.choices(["Open","In Progress","Resolved"], weights=[4,3,3])[0]))

            # lessons
            if px >= 4:
                for l, r in random.sample(LESSONS, random.randint(0, 3)):
                    lessons.append(dict(
                        LessonID=f"LL-{len(lessons)+1:04d}", ProjectID=code,
                        Category=random.choice(LESSON_CATS), Lesson=l, Recommendation=r,
                        DateCaptured=iso(d(TODAY, -random.randint(10, 420)))))

CONFIG = [
    ("CPI_Green", 0.95, "Cost Performance Index at or above this = Green"),
    ("CPI_Amber", 0.85, "CPI at or above this (below Green) = Amber; below = Red"),
    ("SPI_Green", 0.95, "Schedule Performance Index at or above this = Green"),
    ("SPI_Amber", 0.85, "SPI at or above this (below Green) = Amber; below = Red"),
    ("Risk_Green", 10, "Highest open risk exposure (Probability x Impact) at or below this = Green"),
    ("Risk_Amber", 16, "Highest open risk exposure at or below this = Amber; above = Red"),
    ("Rollup_RiskRed_Share", 0.20, "Group is Red on risk when this share of its projects are Red on risk"),
    ("Rollup_RiskAmber_Share", 0.08, "Group is Amber on risk at this share"),
    ("Rollup_DeliveryRed_Share", 0.30, "Group is Red when this share of its live projects are Red overall"),
    ("Rollup_DeliveryAmber_Share", 0.15, "Group is Amber at this share"),
    ("Currency", "USD", "Reporting currency for all monetary values"),
    ("ReportingDate", TODAY.isoformat(), "As-at date for elapsed and overdue calculations"),
]

data = dict(
    meta=dict(generated=TODAY.isoformat(), currency="USD",
              source="Synthetic national AI-economy programme - illustrative only"),
    priorities=priorities, portfolios=portfolios, programs=programs, projects=projects,
    milestones=milestones, risks=risks, issues=issues, lessons=lessons,
    config={k: v for k, v, _ in CONFIG})

with open("data/portfolio_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, separators=(",", ":"))

import os
print(f"priorities {len(priorities)} | portfolios {len(portfolios)} | programs {len(programs)} "
      f"| projects {len(projects)} | milestones {len(milestones)} | risks {len(risks)} "
      f"| issues {len(issues)} | lessons {len(lessons)}")
print("BAC total  ${:,.0f}".format(sum(p['BudgetAtCompletion'] for p in projects)))
print("AC total   ${:,.0f}".format(sum(p['ActualCost'] for p in projects)))
for pf in portfolios:
    pgs = [g['ProgramID'] for g in programs if g['PortfolioID'] == pf['PortfolioID']]
    ps = [p for p in projects if p['ProgramID'] in pgs]
    print(f"  {pf['PortfolioID']} {pf['PortfolioName']:<34} {len(pgs)} prog {len(ps):>3} proj  "
          f"${sum(p['BudgetAtCompletion'] for p in ps)/1e9:>6.2f}B")
print("json bytes", os.path.getsize("data/portfolio_data.json"))
