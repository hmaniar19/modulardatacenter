# Candid Intelligence: what they do, and a lean think tank built on the same formula

Date: 2026-11-24. Feeds: decision to stand up our own AI-leveraged engineering think tank as a
separate department, with its own charter, procedures, P&L and client-data wall. It is not part of
the flare-gas data center operating procedures (`deliverables/study.md`).

Evidence tags: **(cited)** a source passage read on 2026-11-24; **(inferred)** reasoning from cited
facts; **(estimate)** our number, rerun in `candid_lean_model.py`.

## Answer

Candid Intelligence (Candid, candid.engineering) began in 2025 as an AI agent platform for EPC bidding
and pre-construction. By late 2026 it presents itself as an AI-powered owner's engineering firm for
gas-fired power. It delivers PE-stamped concept-to-FID packages: pre-FEED in 4 weeks, FEED in 12, and
±15% backtested cost accuracy. It raised about $6M seed from Quiet Capital, Liquid 2, SE Ventures
(Schneider Electric), Presight-Shorooq and others, with about 7 staff. Its formula is software doing
the drafting, calculating, cross-checking and repricing, with a licensed engineer bench signing every
sheet, sold on speed, guarantees and blind backtests. A lean copy for our think tank needs about
**$20k setup and $17k/month fixed**. Peak cash need is **about $43k (base) to $83k (downside)**, plus
about $50k of buyer-triggered items (SOC 2, Thermoflow). Burn with zero sales is about $228k for
year 1. All of it hinges on one untested assumption, the sales ramp.

## 1. What Candid is (OSINT)

| Fact | Value | Source |
|---|---|---|
| Legal name, HQ | Candid Intelligence, Inc.; Houston TX and San Francisco CA; mail drop 2261 Market St STE 85789, SF | privacy policy on candid.engineering/work-with-candid.html (cited); PitchBook (cited) |
| Founded | 2025 | Greentown Labs member page; PitchBook (cited) |
| Founders | Talha Faiz (process plant design at Chiyoda, AI at Meta); Hassan Azmat (CEO, repeat founder, CMU autonomous racing) | SE Ventures post, Jan 12 2026 (cited) |
| Headcount | 7 employees (PitchBook); LinkedIn shows 5 | PitchBook; LinkedIn company page (cited) |
| Funding | $5.5M seed Sep 2025 (Quiet Capital lead, Liquid 2), per Indexed; $6M seed 24 Feb 2026, 10 investors incl. E14, Flexcap, Presight, per PitchBook; $6M per Presight-Shorooq release | indexed.vc; PitchBook; Zawya release Feb 24 2026 (cited). Likely one round reported twice (inferred) |
| Strategic backers | SE Ventures (Schneider Electric), with an AVEVA synergy thesis; Presight-Shorooq Fund I (G42); Yann LeCun as angel | SE Ventures post; Zawya; candid.engineering (cited) |
| Valuation | Dealroom shows "Enterprise value $22—33m" | search snippet only; page returned 403, unverified |
| Accelerator | Greentown Labs Houston member; accelerator entry 15 Dec 2025 | Greentown; PitchBook (cited) |
| Security posture | SOC 2 Type I, ISO 27001 aligned, NDA on every engagement | candid.engineering FAQ (cited) |

**The pivot (cited, dated):**
- **2025 to early 2026: a software product.** "Agentic AI platform purpose-built for industrial
  project pre-construction." It ingests past bids, P&IDs, specs, line lists and vendor sheets, then
  runs agents for requirements extraction, RFI drafts, cross-discipline reconciliation, cost and risk,
  and bid assembly (SE Ventures). Pitch claims: bidding costs $1M and 12 weeks per project; Candid
  cuts that 10x and tightens error from ±25% to ±10% (Zawya). Customers were EPCs.
- **Late 2026: a tech-enabled services firm.** "We are an owner's engineering firm for gas-fired
  power." "You work with engineers, not a software tool." Customers are owners and developers before
  final investment decision (candid.engineering FAQ). LinkedIn: "A new kind of engineering firm for
  energy infrastructure." Indexed.vc names "owner-operators and EPCs building data centers and energy
  infrastructure."
- **Hiring confirms the services turn.** All 7 open roles are engineering delivery or sales: Director
  of Engineering Delivery, VP Projects, Senior Process, Piping, Mechanical and Electrical Engineers
  (all "Power Generation / Gas-to-Power", $100K–$250K posted), and a Houston Sales Engineer. There
  are no ML roles (Ashby posting API, `includeCompensation=true`, cited).

The pivot is the lesson. Selling AI software to EPCs faces long procurement cycles and IT security
reviews. Selling stamped deliverables to owners is a familiar purchase that the software makes cheaper
to produce (inferred).

## 2. How they consult

Source for this section: candid.engineering home page and FAQ (cited).

**Scope, concept to FID:** site and configuration studies, interconnection and permitting support,
pre-FEED, FEED, long-lead equipment. "We don't build." The EPC handoff uses the EPC's own file formats.

**Deliverables:** plot plan, heat and material balance, single-line diagram, PFD to P&ID, cost
estimate, schedule, scope gaps and long-lead risks. Every sheet is reviewed and stamped by a PE
licensed in the project's state, delivered in the client's templates.

**The 4-step delivery engine:**
1. Intake. One basis of design and three candidate sites. Gaps are filled "from satellite imagery,
   public records and nearby plants", and assumptions are marked.
2. Scenario sweep. Software evaluates 12 scenarios across sites and seasons, using industry-standard
   tools so engineers can check every number. It draws on "350+ GW of power-generation engineering".
3. Live pricing. Rolling vendor quotes and channel partners. Client quotes are used under NDA.
4. PE review and stamp. The output is a full gate pack or single deliverables.

**Trust devices (the real sales engine):**
- Backtest to ±15% against built plants rebuilt from public records.
- Free blind revalidation: "Hand us a plant you already built."
- Guarantees: a late package is free, and rework when the project changes is warranted at no charge.
- Sample deliverables before commitment, and a 30-minute live demo with founders.

**Go-to-market:** founder-led demos with a reply "from a founder's inbox within one business day".
RB2B visitor de-anonymization on the website (privacy policy). Panel at the EPC Show, Houston.
Greentown Houston membership. Strategic investors as channels (Schneider, AVEVA).

**Pricing:** not published anywhere found. Unknown.

## 3. The formula, reduced to levers

| # | Lever | What Candid does | Copy? |
|---|---|---|---|
| 1 | Narrow vertical | Gas-fired power, pre-FID only | Yes, narrower (see §4) |
| 2 | Sell outcomes, not software | Stamped gate packs | Yes |
| 3 | AI does the toil | Drafting, calc, cross-check, change propagation, repricing | Yes, with off-the-shelf models |
| 4 | Licensed bench signs | "Standby bench" of PEs | Yes, part-time W-2 PE first |
| 5 | Proprietary calibration data | Backtest on 350+ GW of built plants | Yes, start small and public-records based |
| 6 | Live vendor pricing | Rolling quotes and channel partners | Yes, it is our moat in small gas gensets |
| 7 | Risk reversal | Late means free, rework warranted, blind backtest | Yes, cap the warranty in the MSA |
| 8 | Enterprise trust | SOC 2 Type I, NDA, encryption | NDA now; SOC 2 only when a buyer asks |
| 9 | VC-scale team | ~14 heads planned, ML researchers | No |

## 4. Our think tank: charter

**Separate department.** Own name, procedures, P&L and data room. Its engineering, permitting and
cost work follows its own QA and stamping procedure, not the data center business's. Decision: form a
separate LLC so engineering liability stays outside the data center operation. Cost is $300
(estimate), and it is reversible.

**Information barrier.** Outside clients will share sites, gas positions and costs. If the parent
develops data centers too, the think tank must wall that data off from the parent, the way Candid
promises "Your project stays yours." Internal work for the parent goes through the same intake,
contract and pricing as an outside client.

**Wedge (decision):** 1–100 MW behind-the-meter gas power for data centers and modular compute:
recip engines, aeroderivatives, small simple-cycle units, and stranded or flare-gas sites. Candid's
public example is a 2×GT combined cycle priced at $108M installed. We go smaller and faster, where
our own flare-gas study already holds verified engine, gas, water and permitting evidence.

**Full scope (mirrors Candid, every gate):**
1. Site screening and go/no-go (FEL1): gas supply, interconnection or islanded, land, water, air
   permit class, fiber.
2. Configuration studies (FEL2): prime mover selection, N+x redundancy, heat balance, cooling, scenario sweep.
3. Engineering deliverables: plot plan, PFD, P&ID, single-line, heat and material balance, equipment
   list, MTO.
4. Cost and schedule: Class 4/3 estimate, long-lead tracker, vendor quote book.
5. Permitting and interconnection support: air (TCEQ standard permit or PBR in Texas), water,
   local land use, and ERCOT large-load or islanded study inputs.
6. Owner's-engineer retainer through FID: lender independent-engineer responses, bid evaluation of
   EPC offers.
7. EPC handoff in native formats.
8. AI layer: document ingestion, spec and requirement extraction, cross-discipline reconciliation,
   change propagation, and backtest library.

**Offer ladder (prices are estimates; Candid publishes none):**

| Offer | Duration | Price | Direct cost | Gross margin excl. founder time |
|---|---|---|---|---|
| Free blind backtest | 1 week | $0 (lead magnet) | founder time | n/a |
| Site screen (FEL1) | 1 week | $12,000 | $1,050 | 91% |
| Pre-FEED pack (FEL2) | 4 weeks | $55,000 | $5,250 | 90% |
| Owner's-engineer retainer | monthly | $15,000 | $2,000 | 87% |

Price sanity check: SE Ventures cites FEED at about $30M on a $1B project, roughly 3% (cited). A
$55k pre-FEED on a $30–60M BTM plant is about 0.1–0.2% of capex, well below conventional FEED budgets
(inferred). The price is still untested with any buyer.

## 5. Startup costs

From `python3 docs/research/candid_lean_model.py` (run 2026-11-24).

**One-time setup: $20,450**

| Item | Cost | Basis |
|---|---|---|
| Separate LLC formation | $300 | estimate, verify with TX SOS |
| TBPELS firm registration (>1 employee) | $150 | cited, pels.texas.gov/firm_faq.htm |
| Legal: MSA, NDA, PE liability terms, info-barrier policy | $6,000 | estimate |
| Brand, site, sample deliverable pack | $3,000 | estimate |
| Workstations ×2 | $6,000 | estimate |
| Backtest dataset build | $5,000 | estimate |

**Monthly fixed: $17,283**

| Item | $/mo | Basis |
|---|---|---|
| Part-time W-2 Texas PE in responsible charge, 40 h @ $125 | 5,000 | estimate. Texas requires the firm to list its licensed PE *employees*, and a PE may hold a secondary part-time association (cited, TBPELS FAQ). A 1099 stamp-for-hire does not fit that rule |
| Professional liability $1M/$1M | 833 | $2.5k–$20k/yr small-firm range, midpoint (cited, morrowinsure.com) |
| General liability + cyber | 250 | estimate |
| LLM APIs, cloud, Workspace, CAD/PDF tools | 1,200 | estimate |
| Conferences and travel | 1,500 | estimate |
| Accounting, payroll, misc | 500 | estimate |
| Founder draw, 2 × $4,000 | 8,000 | decision |

**Deferred until a buyer requires them: about $50,000.** SOC 2 Type I, first year, about $20k all-in
(cited, vanta.com). Thermoflow licence, price unpublished, so the $30k placeholder needs a quote
(thermoflow.com/licensing.html confirms one-year and long-term licences only).

**Hiring trigger:** add a senior engineer at $175k × 1.3 load (Candid's posted band midpoint) when
delivery load exceeds founder capacity. Capacity assumptions: 2 pre-FEED equivalents per month for
the founders, and 1.5 for each hire (estimates).

| Scenario | First cash-positive month | Peak cash need | + deferred items | Year-1 revenue | Hires by M12 |
|---|---|---|---|---|---|
| Base | 3 | $43,317 | $93,317 | $1,184,000 | 2 |
| Downside (sales start M4, about half) | 6 | $83,467 | $133,467 | $519,000 | 0 |
| No sales for 12 months | never | $227,850 | $277,850 | $0 | 0 |

**Comparison:** a Candid-style team of 14 at the same band burns about $3.2M/yr in payroll alone
(inferred from 7 staff plus 7 open roles). The lean version is about 15x cheaper to run until demand
is proven.

## 6. Launch sequence (first 90 days)

1. Weeks 0–2: form the LLC, sign the part-time PE, file TBPELS registration (5–6 week issuance,
   cited), bind professional liability, write the MSA with capped warranty and late-delivery terms.
2. Weeks 2–6: build the backtest library. Rebuild 5–10 public BTM or small gas plants (permits, EIA
   filings, vendor spec sheets) and record estimate vs actual. Publish one sample pack.
3. Weeks 4–12: offer 3 free blind backtests to developers. Convert to paid site screens. Founder-led
   demos. Attend one Houston power or data center event.
4. Trigger SOC 2 and Thermoflow only on a signed or requiring client.

## Not settled

- **Demand and price.** No buyer has been asked. The ramp and prices are estimates. The next check is
  10 developer calls and 3 free backtests, then measure paid conversion.
- **Candid's prices, revenue and customers.** None published. PitchBook marks them "Generating
  Revenue" with no figure.
- **Valuation.** The $22–33M Dealroom figure is a search snippet; the page returned 403.
- **Funding reconciliation.** $5.5M Sep 2025 (Indexed) vs $6M Feb 2026 (PitchBook, Zawya). Probably
  the same round at close.
- **Market size for BTM data center power.** An Enverus headline says data centers drive 88% of
  forecast industrial BTM demand (search snippet only; page returned 403).
- **Founder capacity per month with AI tooling.** Untested. It sets the first-hire date.
- **Insurance.** A quote may exceed the midpoint once power-plant design exposure is disclosed.

## Sources (read 2026-11-24)

- https://candid.engineering/ (home, FAQ) and https://candid.engineering/work-with-candid.html (privacy policy)
- https://www.linkedin.com/pulse/our-investment-candid-intelligence-agentic-ai-unleash-productivity-7d5gc/ (SE Ventures, Jan 12 2026)
- https://www.zawya.com/en/press-release/companies-news/presightshorooq-100m-ai-fund-deploys-capital-in-five-companies-in-its-first-quarter-359067 (Feb 24 2026)
- https://greentownlabs.com/members/candid-intelligence
- https://indexed.vc/companies/candid-intelligence
- https://pitchbook.com/profiles/company/932530-06
- https://api.ashbyhq.com/posting-api/job-board/candidintelligence?includeCompensation=true
- https://pels.texas.gov/firm_faq.htm
- https://morrowinsure.com/industries/engineers-insurance
- https://www.vanta.com/collection/soc-2/soc-2-for-startups
- https://thermoflow.com/licensing.html
