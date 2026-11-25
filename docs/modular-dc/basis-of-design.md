# AI Block: basis of design (pre-FEED, rev A)

Date: 2026-11-25. Prepared by the think tank as its first package, in the format of the Candid-style
pre-FEED pack (`docs/research/candid-intelligence-lean-replica.md`). Evidence: `[id]` refers to
`docs/modular-dc/evidence.json` (`ai-*` ids, 123 sources fetched 2026-11-25) or
`research/evidence.json` (other ids). Numbers come from `python3 docs/modular-dc/ai_block_model.py`.
**ASSUMPTION** marks our own inputs.

## Decision

Build the AI Block as a **4.8 MW IT module**: four NVIDIA NVL72 scalable units. It is powered by
**six 1,500 ekW fast-response gas recips (5 running + 1 spare)** on a split 480 V bus with a
1.2 MW battery. It uses **dry coolers only on a 45 °C liquid loop**, and burns **about 1.1 MMcf/d of
firm gas**. Capex excluding GPUs is **$41.1M ($8,567/kW IT)**, and payback is **7.6 years** at a
remote-site rent of $142/kW-month. The 0.6 MW and 1.2 MW Blocks do not pay back in a useful time
(18 to 111 years), because 24/7 staff, protected fiber and the N+1 spare do not shrink with the
Block.

Two consequences:
- **The AI Block does not run on flare wells.** A 300 mcf/d well supports only a 1.2 MW Block,
  which takes 18 years to pay back. A 300 mcf/d well also falls below 150 mcf/d within a year
  [gas-jpt-decline]. AI tenants expect Tier III [ai-cmp-gb200-tier3], so the fuel must be firm gas
  from a processing-plant tailgate or a gathering header under a firm contract
  [ai-site-eia-firm-def]. 1.1 MMcf/d is under 0.5% of one 275 MMcf/d plant [ai-site-et-mustang-draw].
- **The flare-gas mining Block (`deliverables/study.md`) stays a separate product.** The study's
  "phase 3 hybrid" is replaced by this product on firm gas.

## Data shape

- **Site:** one firm gas delivery point, one A/B fiber path, one fence.
- **AI Block:** the unit of capital. It has four parts:
  - a power island (N+1 gensets, two 480 V buses with a tie, BESS on each bus);
  - a cooling plant (CDUs N+1, dry coolers N+1, air-side DX for the 10% air heat);
  - four IT halls, one scalable unit (SU) each;
  - a network hut.
- **SU (scalable unit):** 8 NVL72 racks, 1.2 MW [ai-cmp-gb200-su-mw]. It is the tenant's unit of lease.
- **Tenant:** owns GPUs and pays rent per kW per month plus energy at cost. The same powered-shell
  model Energy Vault uses with Crusoe in Snyder, TX [ai-site-snyder-leaseback].

## Design criteria

| Criterion | Value | Basis |
|---|---|---|
| IT load per SU | 1.2 MW (8 racks; GB300 rack 135 kW design power, 155 kW peak) | [ai-cmp-gb200-su-mw] [ai-cmp-gb300-135tdp] |
| Rack supply | 415 V AC from 480 V; plan for 800 V DC from 2027 | [ai-cmp-se-rd109-132kw] [ai-cmp-800v-2027] |
| Heat split | 90% liquid, 10% air | [ai-cmp-gb300-split] |
| Coolant to rack | up to 45 °C; 177 LPM per rack at 45 °C | [ai-cmp-gb300-45c] [ai-cmp-gb300-flow] |
| Site climate | Midland: >90 °F on 115 afternoons, >100 °F on 24, record 116 °F | [wtr-midland-climate] |
| Load transients | 30 → 100% in milliseconds; energy at 0.2–3 Hz; checkpoint dips of minutes | [ai-cmp-swing-30pct] [ai-pwr-msft-fft] [ai-pwr-checkpoint] |
| Availability target | Tier III, 99.982% | [cmp-tier3] [ai-cmp-gb200-tier3] |
| Field-gas derate | 20% (cited range 15–30%; methane number 25–95) | [gas-pioneer-derate] [ai-pwr-apg-mn] |
| Air permit | TCEQ EGU Standard Permit; West Texas NOx 3.11 lb/MWh | [ai-pwr-pbr512-noegu] [ai-pwr-egusp-nox] |
| Bus voltage | 480 V; one bus tops out at about 8 MW of generation, so two buses | [ai-pwr-lv-8mw-limit] |

## Scenario sweep (12)

| # | Size | Prime mover | Cooling | Gensets | Gas mcf/d | Capex $M | $/kW IT | Payback |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.6 MW | Recip FR | Dry-only | 2 × 1,500 | 150 | 10.43 | 17,384 | 50.4 y |
| 2 | 0.6 MW | Recip FR | Dry + trim | 2 × 1,500 | 153 | 10.50 | 17,504 | 51.1 y |
| 3 | 0.6 MW | Turbine | Dry-only | 2 × 1,000 | 156 | 13.72 | 22,873 | 109.1 y |
| 4 | 0.6 MW | Turbine | Dry + trim | 2 × 1,000 | 159 | 13.80 | 22,993 | 111.3 y |
| 5 | 1.2 MW | Recip FR | Dry-only | 3 × 1,500 | 300 | 15.31 | 12,755 | 18.2 y |
| 6 | 1.2 MW | Recip FR | Dry + trim | 3 × 1,500 | 305 | 15.45 | 12,875 | 18.4 y |
| 7 | 1.2 MW | Turbine | Dry-only | 3 × 1,000 | 313 | 19.99 | 16,657 | 27.5 y |
| 8 | 1.2 MW | Turbine | Dry + trim | 3 × 1,000 | 317 | 20.13 | 16,777 | 27.9 y |
| **9** | **4.8 MW** | **Recip FR** | **Dry-only** | **6 × 1,500** | **1,113** | **41.12** | **8,567** | **7.6 y** |
| 10 | 4.8 MW | Recip FR | Dry + trim | 7 × 1,500 | 1,170 | 44.72 | 9,317 | 8.4 y |
| 11 | 4.8 MW | Turbine | Dry-only | 8 × 1,000 | 1,215 | 45.93 | 9,570 | 8.6 y |
| 12 | 4.8 MW | Turbine | Dry + trim | 9 × 1,000 | 1,268 | 47.77 | 9,953 | 9.1 y |

Why recips over turbines: small turbines cost $5,200/kW at 2 MW against $2,550/kW for recips
[ai-site-doe-gt-size] [ai-site-doe-recip-size], and they lose about 20% of output at 100 °F
[ai-pwr-taurus70-derate]. Why fast-response recips: the G3516 Fast Response takes 100% block load in
one step [ai-pwr-g3516fr-block], while a typical lean-burn 2 MW set takes 30% [ai-pwr-hsk78g-step].

Why dry-only: one fewer genset (6 vs 7), $3.6M less, zero operating water. The cost is GPU
throttling on about 24 afternoons a year above 100 °F, when a 45 °C rack inlet cannot be held with
an 8 K dry-cooler approach (ASSUMPTION; [wtr-midland-climate]). NVIDIA's reference design is
dry-cooler based and needs chillers "maybe 1% of the year" in some climates [ai-cmp-nv-1pct-chiller].
Scenario 10 is the fallback if a tenant refuses summer throttling.

**Sensitivity of scenario 9:**

| Input change | Capex | Payback |
|---|---|---|
| Base | $41.1M | 7.6 y |
| Hall $2,500/kW IT | $32.0M | 5.7 y |
| Hall $6,000/kW IT | $48.8M | 9.3 y |
| Utilization 70% | $41.1M | 10.8 y |
| Rent $178/kW-month, no remote discount | $41.1M | 5.6 y |
| Rent $110/kW-month | $41.1M | 11.0 y |

## Chosen configuration

**Power island.**
- 6 × Cat G3516 Fast Response class, 1,500 ekW continuous at 9,771 Btu/ekWh
  [ai-pwr-g3516fr-hr]. They are derated to 1,200 kW on field gas. Peak load is 5.52 MW, so 5 run
  and 1 is spare.
- A NOx-selectable build reaches 0.5 g/bhp-hr without aftertreatment [ai-pwr-g3516-nox05]. That is
  under the NSPS JJJJ 1.0 limit [ai-pwr-jjjj-table1] and the West Texas EGU limit.
- Two 480 V buses (G1–G3 on A, G4–G6 on B) with a normally closed tie. Each bus stays under the
  ~8 MW low-voltage limit [ai-pwr-lv-8mw-limit].
- BESS 2 × 600 kW / 600 kWh, one per bus. Each covers a unit trip, sub-second swings and
  checkpoint dips. NVIDIA's reference design puts a BESS in front of onsite generators
  [ai-pwr-nv-bess-gen]. GB300 power shelves hold only 65 J per GPU [ai-pwr-gb300-65j].
- BESS sizing is contested: Williams pairs 46% BESS with gas [ai-site-sty-bess], while VoltaGrid
  claims none is needed [ai-site-voltagrid-nobess]. We carry 1 h at one unit's rating (ASSUMPTION)
  until a transient study is done.

**Cooling.**
- 3 × 2.3 MW CDUs, 2 duty + 1 standby [ai-cmp-vertiv-cdu2300]. Each draws about 2% of its rated
  load [ai-cmp-vertiv-cdu-power].
- 3 × 3 MW dry coolers, 2 duty + 1 standby, rated to 55 °C ambient [ai-cmp-vertiv-trimcooler].
- Packaged DX units for the 480 kW of air-side heat.
- Annual PUE 1.11, peak 1.15 (ASSUMPTION built from cited parts; see the model header).

**IT.**
- Four halls, one SU each: 8 racks plus networking. The benchmark is Vertiv's 1.3 MW MegaMod in an
  801 sq ft hall [ai-cmp-vertiv-megamod-1p3].
- Rack 600 × 2,294 × 1,068 mm, up to 3,300 lb loaded [ai-cmp-gb300-rack-dims]
  [ai-cmp-nvl72-weight-gb300].
- Halls 1–2 hang on Bus A and halls 3–4 on Bus B. The closed tie lets the spare genset and either
  BESS serve both buses. A full A/B dual feed to every hall, which Tier III's "no single point of
  failure" implies [ai-cmp-gb200-tier3], is a FEED-stage option to price.

**Network.**
- A/B fiber laterals to an I-20 carrier route [ai-site-motran-i20].
- A protected 100G wave: $2,500–6,000/month unprotected, protection doubles it, plus an off-net
  tail [ai-site-wave-longhaul] [ai-site-wave-offnet-protect].
- Latency costs about 1.6 ms round trip per 100 route-miles [ai-site-fiber-latency-mile], against a
  2 s time-to-first-token budget [ai-site-mlperf-ttft].

**Plot plan.**
- A 92 × 56 m fence, about 1.3 acres. Compare 0.12 acre for one 1.77 MW Armada unit alone
  [ai-site-armada-leviathan-dims].
- Gensets in 12.2 × 3.0 m enclosures [ai-site-j420-container], with at least 5 ft to openings
  (NFPA 37) [ai-site-nfpa37-5ft].
- BESS ≥10 ft from everything [ai-site-ifc-ess-10ft].
- Noise is about 50 dB(A) at 90 m, against the Texas 85 dB nuisance yardstick [ai-site-genset-72dba]
  [ai-site-tx-noise-85db].
- Drawing: `docs/presentation/ai-block-design.html`, slide 6.

## Capex (scenario 9, screening level)

| Line | $M | Basis |
|---|---|---|
| Power: 9 MW nameplate at $2,000/kW + 6 paralleling sections | 18.15 | [ai-site-doe-recip-size] [pwr-turnkey-switchgear] |
| BESS 1.2 MWh at $254/kWh + 15% install | 0.35 | [ai-pwr-megapack-tx]; ASSUMPTION install |
| IT halls, CDUs, dry coolers, 480/415 V distribution | 21.12 | $4.4M/MW modular hall [cmp-modular-cost] |
| Site: pad, gas tap, fence, permits | 1.50 | ASSUMPTION |
| **Total excl. GPUs** | **41.12** | $8,567/kW IT, vs $17.6M/MW all-in greenfield [ai-site-cw-17p6m] |

Tenant GPUs are separate: about $39M per MW for B300 [cmp-b300-it-cost], so roughly $187M for 4.8 MW.

**Operating cost:**
- Fixed opex is $1.95M a year: 24/7 staff (ASSUMPTION), protected fiber, insurance at 2.5% of
  capex [rsk-hotaling-premium], and BESS maintenance.
- Energy is billed at cost, about $34.5/MWh: gas at $1.60/mcf (ASSUMPTION, near Waha
  [ai-site-waha-basis-2027]) plus $19/MWh O&M [ai-site-doe-maint-1p9c].
- Rent is $178/kW-month (JLL, 1–5 MW [ai-cmp-jll-rent-1mw]) less a 20% remote-site discount
  (ASSUMPTION), at 90% utilization (ASSUMPTION).

## Schedule and long leads

| Item | Lead time | Basis |
|---|---|---|
| 1–3 MW gas gensets | 54–78 weeks | [ai-pwr-terrapin-gasgen] |
| Large gensets (Cummins) | ship 2H 2028 | [pwr-nextler-cummins] |
| Switchgear | 44 weeks (WoodMac); MV 52–80 weeks | [ai-pwr-woodmac-q2-2025] [ai-pwr-terrapin-mv] |
| BESS | 1–2 quarters | [ai-pwr-megapack-lead] |
| Modular IT hall | 12 weeks to 3 months | [ai-site-armada-leviathan] [cmp-crusoe-spark-3mo] |
| EGU Standard Permit | 9 days average in 2024 | [ai-pwr-tceq-days-2024] |

The critical path is the gensets, at about 15–18 months from order. Mitigation: order gensets at
FID, and keep 480 V (no MV gear, no transformer queue).

**Permit risk.** On Sept 21, 2026 the governor directed TCEQ to halt all permits sought by data
centers [ai-pwr-tceq-pause-directive]. TCEQ applied it to all air and water authorizations for
infrastructure directly supporting data centers, with no size threshold [ai-pwr-tceq-pause-scope].
It was lifted Nov 13 [ai-pwr-tceq-pause-lifted], and review resumed Nov 17 [ai-pwr-tceq-resumed].
The pause was not codified, so it can recur. File early, and keep the permit in the gas
operator's or power company's name where counsel agrees (ASSUMPTION, needs legal review).

Location: stay west of I-35/I-37. Eagle Ford counties east of I-37 fall in the East Texas NOx
region (0.14 lb/MWh), which in practice requires SCR [ai-pwr-egusp-region] [ai-pwr-egusp-nox].

## Research backlog (next checks, in order of effect on the decision)

1. **Hall cost.** The $4.4M/MW comes from one source and swings payback 5.7–9.3 years. Get budget
   quotes: Vertiv MegaMod, Armada, Crusoe Spark, Giga.
2. **Tenant and rent.** Who leases 4.8 MW islanded, at what rent and SLA? Crusoe's islanded
   microgrid reached 99.2% [ai-site-crusoe-redwood-avail], below Tier III. Talk to 5 GPU clouds
   and enterprise users; JLL says 500 kW–3 MW users struggle to find capacity [ai-cmp-jll-enterprise].
3. **Firm gas.** Terms and price for 1.1 MMcf/d at a processing-plant tailgate or gathering header
   (no public figure found). Waha congestion may return in 2028 [ai-site-waha-2028-risk].
4. **Transient study.** Can lean-burn or fast-response recips follow 0.2–3 Hz swings in island
   mode? That sets the BESS size. Get Cat and INNIO data.
5. **Gas analysis and derate.** A chromatograph on the candidate supply, and the G3516 FR derate at
   the measured methane number.
6. **Dry-only summer.** Dry-cooler approach at 40–47 °C ambient, and hours of throttling.
7. **Fiber.** Quotes on Permian routes (FiberLight, Segra) for laterals and a protected 100G wave.
8. **Permits.** Confirm the EGU Standard Permit text (the PDF is unquoted) and track pause recurrence.
9. **Staffing.** Can remote monitoring plus on-call replace 24/7 onsite staff? That is the lever
   that could make a 1.2 MW Block viable.
10. **800 V DC.** Design the halls to retrofit 800 V DC power for 2027+ racks.
