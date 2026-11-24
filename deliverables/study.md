# Flare-gas modular data center: phased study (Texas, Nov 2026)

## Decision in one paragraph

A drop-and-go Block is buildable under $500k, and it is mobile, gathering-line-free, Starlink-connected and nearly water-free, as the owner hoped. Its infrastructure is a new continuous-rated field-gas engine in the Cat G3412 class (423 ekW continuous), 12 immersion tanks with dry coolers sized for West Texas heat, a gas train, a trailer and Starlink, for $406,400. It carries 248 kW of miners, and four Blocks fit a 300 mcf/d well behind one leased gas-conditioning skid. Latency and water are not the binding constraints. The binding constraints are hashprice, well decline and engine cost. Wells lose 55% of their gas in year one [E:gas-jpt-decline], so the Blocks must keep moving: 9 moves and 5 new sites in 5 years in our month-by-month simulation. With every cost loaded, a hashing MWh at a wellsite costs about $184: $131 for the site and $52 for the miners. Revenue at the Nov 16, 2026 hashprice of $30.45/PH/day [E:cmp-hri-hashprice] is $94. We found no evidence that Texas operators pay anyone to take flare gas; miners pay about $1/mcf [E:com-braiins-paidtotake]. Hosting other people's miners does not close the gap either. The site alone needs about $0.131/kWh, against published hosting rates of $0.0725 median [E:com-lm-hosting-median] to $0.085 for flare sites [E:com-ez-hosting-packages]. The 2028 halving follows cuts in hashprice of 54-59% at the last two [E:com-ez-2020-halving][E:com-hri-2024-q1]. **Recommendation: do not deploy capital at today's prices.** Spend Phase 0 (about $50k) securing gas options, engine quotes and tenants. Build the pilot Block when one trigger fires: hashprice at or above $60/PH/day for 30 days, a tenant signing take-or-pay hosting at $0.13/kWh or more, or an operator buying Blocks under a flat operating fee. The GO IF and KILL IF lines are at the end.

Data shape used throughout: a **Site** is one lease with one gas delivery point (a tee on the separator gas outlet upstream of the flare). A **Block** is the unit of capital and the unit of mobility: one genset, its own electrical island, one compute skid, one network kit. A site holds as many Blocks as its gas supports, and Blocks leave one at a time as the well declines.

## 1. Modular data center design

**What precedent says the module should be.** The flare-gas industry already converged on container-scale modules. Crusoe's fleet, sold to NYDIG in March 2025, was 425+ modular data centers totaling 250+ MW [E:gas-crusoe-nydig], about 0.6 MW per module. Crusoe required at least 300 mcf/d per module [E:gas-coloradosun-300mcf] and designed for mobility because "sites have a decline curve" [E:gas-crusoe-decline]. EZ Blockchain targets sites flaring at least 350 mcf/d with 2.5 MW mobile units [E:gas-ez-350]. Upstream Data sells much smaller skids, 48 to 325 kW, burning 12 to 91 mcf/d [E:gas-upstream-hashgen][E:gas-upstream-fuel]. Giga Energy started with 40-ft containers at drilling sites [E:gas-tamu-giga].

**Compute enclosure options, priced.**

| Enclosure | Capacity | Price | Cooling |
|---|---|---|---|
| Bitmain Antbox N5 20HQ | 658 kW | $45,000 | air [E:cmp-antbox-n5] |
| Bitmain Antspace HK3 | 1 MW, 210 hydro miners | $90,000 | hydro, PUE 1.034 [E:cmp-antspace-hk3-price][E:cmp-hk3-pue] |
| Antspace HD5 | 1.5 MW | $75,999 | hydro + dry tower [E:wtr-cmb-hd5-price] |
| Fog C6 tank | 24 kW, 4-6 miners | $4,450 incl. dry cooler, PDU, coolant | immersion [E:cmp-fog-c6][E:cmp-fog-c6-price] |
| Giga Box Air | 600-1,430 kW | quote only | air [E:cmp-gigabox] |
| Crusoe Spark Liquid | up to 3.5 MW | quote only | closed-loop DLC [E:cmp-crusoe-spark-liquid] |

**Chosen design: the Block.** One Block is a trailer or skid pair:
- Power: one new continuous-rated natural-gas genset, Cat G3412 non-emergency class: 423 ekW continuous, field gas approved [E:eng-g3412-cont], 0.5 g/bhp-hr NOx without aftertreatment [E:eng-g3412-nox], 480 V output, plus an oxidation catalyst for CO and VOC. A standby-rated set is not allowed to run 24/7 [E:eng-iso-esp], so no standby units.
- Gas handling: per Block, a two-phase scrubber, regulator and meter on the line from the site header. Per site, an H2S scavenger vessel and, only if the gas analysis calls for it, a leased mechanical-refrigeration dew-point skid. Refrigeration, not JT, because a JT skid needs a pressure drop that low-pressure separator gas cannot give without a compressor. Liquids knocked out go back to the operator's tank battery under the gas agreement, since they are the operator's hydrocarbons and the operator's royalty obligation.
- Compute bay: 12 Fog C6 immersion tanks with dry coolers, 68 slots for S21 XP-class miners at 3,645 W each [E:cmp-s21xp-spec], 248 kW of IT. Miners belong to hosting tenants in the hosting structure.
- Electrical: generator output at 480 V feeding a low-voltage panel directly. No transformer, no medium-voltage gear.
- Network: one Starlink Business kit [E:cmp-starlink-hw].

**Why 248 kW and not 1 MW.** Three reasons. First, money at risk: a 1 MW enclosure is cheap, but the 1 MW of miners inside it costs about $940k [E:cmp-s21xp-price]. Second, decline: a well that starts at 300 mcf/d can be under 150 mcf/d within a year [E:gas-jpt-decline], so a quarter-site Block (73 mcf/d) lets us remove capacity in steps instead of running one big genset at half load. Third, it avoids paralleling. Each Block is its own island, so the $25,000 to $100,000 paralleling switchgear [E:pwr-turnkey-switchgear] and the $3,000 to $8,000 per-genset control upgrades [E:pwr-turnkey-controls] are not needed. ASIC load can be shed in 3.6 kW steps, so an island does not need a second genset for stability.

**How Blocks combine like Lego.** Blocks share only two things: a gas header from the separator tee, and a fence. Electrically they never touch. Adding a Block means adding a tee on the header and setting a trailer down. Removing one means closing a valve. If a later AI customer needs N+1 power, Generac-class gensets can parallel and load-share without communication lines [E:pwr-generac-noloadshare], but that belongs in a different product (section 5).

## 2. Flared and stranded gas supply

**The rules that make this a market.** Texas Statewide Rule 32 allows flaring while drilling and for 10 days after completion [E:gas-rrc-flare-faq]. After that, RRC staff grant exceptions 45 days at a time up to 180 days, and anything longer needs a Commission Final Order [E:gas-rrc-flare-180]. The bigger driver is federal. EPA's OOOOb associated-gas standard phases out routine flaring at new oil wells after May 7, 2026 [E:gas-cfr-5377b-may2026]. The same rule lists recovering gas "from the separator" and using it "as an onsite fuel source" as a compliant option, equal to a sales line [E:gas-cfr-5377b-onsite]. If gas fails fuel spec, flaring is allowed up to 72 hours per incident [E:gas-cfr-5377b-72h]. EPA's April 30, 2026 guidance allows limited flaring past the deadline [E:gas-epa-flare-memo-2026], and the Nov 25, 2025 final rule kept 18-month extensions [E:gas-epa-oooob-final-ext]. The federal Waste Emissions Charge is dead, disapproved under the CRA on March 14, 2025 [E:gas-epa-wec-cra]. The stick is the flaring ban, not a fee.

**Texas tax carrot.** HB 591, effective Sept 1, 2023, exempts from severance tax gas that would have been flared and is consumed within 1,000 ft of the well [E:gas-forvis-hb591][E:gas-forvis-1000ft]. The well needs RRC authorization to flare for at least 30 days in the prior year [E:gas-forvis-30day]. A Block parked on the pad is inside 1,000 ft by construction. This saves the operator 7.5% of the gas value and is a negotiating chip.

**Who regulates what.** The RRC regulates flaring as waste. TCEQ regulates air quality, including engine authorizations [E:gas-rrc-tceq-air]. On the RRC production report, code 1 is lease or field fuel use "for field operations" and code 4 is vented or flared [E:gas-rrc-lease-use]. A third-party data center is not a field operation, so the operator should report our gas as a sale (inference). That matters because gas sold to a miner is a sale and royalty attaches [E:gas-mcfarland-royalty].

**How the tie-in works physically.** Miners buy the gas from the operator at the wellsite and pipe it to their own generators [E:gas-mfp-pipes]. Crusoe used 1-5 year gas purchase agreements with change of custody, at a price "not comparable" to pipeline sales [E:gas-crusoe-gpa]. Deployments typically lasted 1 to 3 years [E:gas-coloradosun-demob]. No gathering line is involved. The delivery point is a tee on the separator gas outlet upstream of the flare.

**How much gas there is.** Global flaring was 167 bcm in 2025, and US flaring fell 7%, helped by the Matterhorn Express pipeline [E:gas-wb-ggfr-2025]. Permian flared volume rose about 1% in 2024 while intensity fell 5% [E:gas-mrt-permian-2024]. Texas and Permian intensity are down 50% and 62% since 2019 (industry source) [E:gas-tipro-intensity]. The pool of flaring sites is shrinking as pipes arrive. That is a threat to the business and an argument for mobility.

**Gas price context.** The Waha hub traded negative on 42% of 2024 trading days [E:gas-eia-waha-2024], and on 107 flow days in 2025 against a record 158 in 2024 [E:gas-ngi-waha-2025], with trades as low as -$11.00 [E:gas-ngi-waha-low]. Where a sales line exists, the gas is often worth less than nothing. Where none exists, Texas operators have mostly been able to keep flaring under exceptions [E:com-tribune-rrc-nodenial], so the gas has little value to them but they have little pressure to pay for its removal. Section 9 sets the price we pay at about $1/mcf.

**Gas quality, the engineering risk.** A representative raw Permian associated gas is about 60% methane with 40% heavier hydrocarbons [E:gas-pioneer-composition], roughly 1,500 Btu/scf by our calculation. Raw rich gas can derate a generator 15 to 30% (vendor claim) [E:gas-pioneer-derate], because heavier hydrocarbons lower the methane number and force retarded timing [E:pwr-secondwatt-mn]. USGS-era Texas samples have a median of 1,067 Btu/scf with a 5th-95th range of 779 to 1,273 [E:gas-tetrasoft-tx-btu]. We model 1,067 usable Btu/scf, and a gas chromatograph sample is the first field task. JT conditioning skids remove 100 to 250 Btu/ft3 [E:pwr-scon-jt], but Croft's start at 1 to 10 MMcf/d [E:gas-croft-jt], far too big for a Block. H2S matters too. TCEQ treats gas as sour at about 24 ppm [E:gas-tceq-sour], and engine limits run 100 to 500 ppm depending on the engine (vendor) [E:gas-pioneer-h2s].

**Decline.** Unconventional wells decline more than 50% in year one and about 30% in year two [E:gas-jpt-decline]. Gas from all pre-2024 Lower 48 wells fell 23% in one year [E:gas-eia-base-decline]. A 300 mcf/d well is a two-Block well within about a year unless several wells feed one header.

**Alternatives for gas with no line.** The World Bank lists small modular power, truck-mounted mini-LNG, CNG and mini gas-to-liquids [E:gas-wb-alternatives], and calls small-scale capture economically challenging [E:gas-wb-alt-econ]. Onsite power has the lowest capital per mcf because the product, electricity turned into hashrate, leaves by satellite and not by truck.

## 3. SWOT

**Strengths**
- Cheap fuel: miners typically pay about $1/mcf for flare gas [E:com-braiins-paidtotake], about $12 per MWh of compute.
- Proven model. Crusoe built 250+ MW of it before selling [E:gas-crusoe-nydig].
- Regulatory fit. Onsite fuel use is an explicit OOOOb compliance path [E:gas-cfr-5377b-onsite], and HB 591 removes severance tax on the gas [E:gas-forvis-hb591].
- No grid interconnect, so none of the 120-week transformer queue [E:pwr-woodmac-2024], and Texas SB 6's 75 MW large-load curtailment rules do not reach a 1 MW off-grid site [E:rsk-sb6-75mw].
- Zero operating water with closed-loop dry cooling [E:wtr-gasilov-liquid-dry].
- Low bandwidth need. ASIC Stratum traffic is a few kbps per miner [E:cmp-asic-bandwidth].

**Weaknesses**
- Revenue is one commodity. Hashprice at $30.45/PH/day puts many miners at or below breakeven [E:cmp-hri-breakeven].
- ASICs lose about 90% of their value in one generation [E:rsk-ing-new-s21]. Resale depends on efficiency, not age [E:rsk-ing-efficiency].
- A hashing MWh costs about $184 at a wellsite with every layer loaded, against $94 of revenue today (section 9).
- Small high-speed gensets have major overhauls every 30,000 to 36,000 hours [E:pwr-secondwatt-overhaul-1800], so every 3.5 to 4 years at 24/7 duty.
- Single genset per Block means no redundancy, which rules out SLA compute.

**Opportunities**
- Mandatory capture. New Mexico requires 98% capture by Dec 31, 2026 [E:com-nm-98pct], and OOOOb ends routine flaring at new wells after May 7, 2026 [E:gas-cfr-5377b-may2026]. Operators under real pressure may buy Blocks and pay a flat operating fee, a model EZ Blockchain has proposed [E:com-ngi-ez-flatfee].
- Hosting demand. Flare-gas sites already host third-party miners [E:com-musk-flarehost], at published rates up to $0.085/kWh all-in [E:com-ez-hosting-packages].
- Newer miners raise revenue per MWh. The S23 runs at 11 J/TH [E:cmp-s23-spec] against 13.5 for the S21 XP.
- Hybrid compute later. H100 time rents for $2.50 to $4.90 per GPU-hour at specialist clouds [E:cmp-h100-rates], 20 to 30 times bitcoin revenue per MWh, if a site gets fiber or microwave.
- Crusoe exited bitcoin flare mining and moved to AI [E:gas-cnbc-crusoe-sale], which leaves room for small operators.
- Used and rental gensets sidestep the new-equipment backlog [E:pwr-crusader-used][E:pwr-frio-rental].

**Threats**
- Halving in 2028 cuts the block subsidy from 3.125 to 1.5625 BTC [E:rsk-halving-2028]. The last two halvings cut hashprice 54% and 59% [E:com-ez-2020-halving][E:com-hri-2024-q1].
- Difficulty doubled between the last two hashprice bottoms [E:rsk-hashprice-difficulty].
- Pipelines arrive. US flaring fell 7% in 2025 as Matterhorn came online [E:gas-wb-ggfr-2025].
- Theft. A Winkler County sheriff gets calls about oilfield theft at least three times a week [E:rsk-tribune-theft], and 730 S21 XP miners were stolen in a single Fort Worth cargo theft in Nov 2026 [E:rsk-stolen911-s21].
- Insurance at 5 to 10 times data-center rates, specialty markets only [E:rsk-hotaling-premium], because underwriters see remote sites as fire risks [E:rsk-founder-fire].

## 4. First-principles build and retrofit plan

**Start from the physics.** One mcf of 1,067 Btu gas carries 1.067 MMBtu. At 10,060 Btu/kWh, a small genset turns it into 106 kWh. Crusoe's fleet averaged about 125 kWh/mcf on 10.4 Bcf [E:gas-fortuda-crusoe-bcf], and Upstream Data's skids run at about 3.6 kW per mcf/d [E:cmp-upstream-fuel]. The physical limit per site is therefore fixed by the gas, not by money: 300 mcf/d is 1.1 to 1.5 MW of electricity. Everything else is a question of what that MW costs to convert and what it earns.

**Where the money goes per Block ($406,400 infrastructure, 248 kW IT).**

| Item | Cost | $/kW IT | Share |
|---|---|---|---|
| Continuous-rated G3412-class genset, commissioning, oxidation catalyst | $275,000 | 1,109 | 68% |
| 12 immersion tanks, dry coolers, 35% extra dry-cooler capacity | $66,400 | 268 | 16% |
| Block gas train: scrubber, regulator, meter | $25,000 | 101 | 6% |
| 480 V, trailer, network | $40,000 | 161 | 10% |
| Optional: 68 owned S21 XP | $232,560 | 938 | (Block becomes $638,960) |

The power plant, not the enclosure, is the expensive part of the infrastructure. That is why the engine choice matters more than any other choice in the Block. Cat does not publish a G3412 price, so we estimate $250,000 against the $172,000 to $259,000 new price of a comparable 500 kW-class gaseous set [E:eng-generac-price]. Chinese 250-400 kW gas sets list at $50,000 to $75,000 [E:eng-gensetplus-cn] and would cut the Block to about $223k, but their rating class and field-gas capability are not shown and their EPA certification must be proven (section 9). The silicon is the other big number, and it loses about 90% of its value in a generation [E:rsk-ing-new-s21], while the power and cooling hardware lasts a decade. The SpaceX lesson applied here: own the long-lived infrastructure, and treat the miners as a consumable that someone buys only when the hashprice pays them back fast. Used S19 machines sell for $1.68/TH against $17.14/TH new [E:rsk-ing-used-s19][E:rsk-ing-new-s21], but they fail on physics, not price. At about 30 J/TH they earn $42/MWh, below the $74/MWh of site operations plus gas (section 9). Cheap old silicon cannot pay for the genset's fuel and upkeep.

**Delete parts before optimizing them.**
- Delete the transformer. Generate at 480 V and feed the compute bus directly (inference from the vendor 480 V ratings [E:pwr-imp-g3508]). Average transformer lead time went from about 50 weeks in 2021 to 120 weeks in 2024 [E:pwr-woodmac-2024], padmount units take about 75 weeks [E:pwr-woodmac-padmount], and prices are up 60 to 80% since 2020 [E:pwr-powermag-prices].
- Delete medium-voltage switchgear. It costs $15,000 to $85,000 per section before a 1.6 to 2.2 times install multiplier [E:pwr-htyel-mv].
- Delete paralleling (section 1).
- Delete chillers and towers (section 7).
- Delete the fiber (section 6).

**Retrofit and repurpose.**
- Compressor engines. Waukesha rebuilt a 1990 VHP compressor drive with 120,000+ hours and repurposed it for power generation [E:pwr-innio-compressor-reuse]. Idle compressor packages are common in the oilfield, and their engines are already rated for field gas.
- Used gensets, with care. A used Cat G3412C 500 kW natural gas set is listed at $169,900 [E:pwr-depco-g3412], but it is a 120/208 V standby unit, and the emergency G3412 is specified for pipeline gas at methane number 70-100 [E:eng-khl-g3412-mn]. Standby units are not built for 24/7 duty [E:eng-iso-esp]. A used Waukesha F2895GSIU 400 kW set sold as-is for $12,500 [E:eng-tnt-waukesha], which shows how cheap a rebuild candidate can be when its rating and hours check out. Used gas sets carry a 30 to 60% premium over diesel in 2026 [E:pwr-nextler-used-premium], but are available now.
- Rentals. Permian rental fleets offer 400 kW prime field-gas units that are parallel-ready with onboard gas conditioning [E:pwr-bigd-400][E:pwr-bigd-parallel], 50 to 400 kW wellhead-gas units in the Eagle Ford [E:pwr-frio-rental], and month-to-month leases with maintenance included [E:pwr-wgl-lease]. Aggreko alone serves 180+ flare operators [E:pwr-aggreko-flare]. List prices give the scale: Warren CAT rents a 455 kW prime unit for $10,500 a month, fuel type not stated [E:com-warrencat-455], and a 1,475 kW natural-gas unit for $45,000 a month [E:com-warrencat-ng1475]. A generic US table puts 150-500 kW units at $4,000 to $10,000 a month [E:com-haifeng-rental-range]. At about $10,000 a month, renting costs $120k a year against about $275k to buy a continuous-rated engine, so renting fits a 90-day pilot and buying fits a fleet.

**Backlog plan, practical.** New large gensets ordered now from Cummins ship in the second half of 2028 [E:pwr-nextler-cummins]. Caterpillar's order backlog is $72 billion [E:pwr-nextler-cat-backlog]. Recip engines quote 12 to 18 months [E:pwr-sourcerock-recip] to 12 to 24 months to first power [E:pwr-gr1d-recip-lead]. Small gas turbines take 18 to 36 months [E:pwr-utilitydive-smallgt]. The order of preference: a rented prime-rated field-gas set for a pilot (weeks); continuous-rated engines ordered in Phase 0 so they arrive when a trigger fires; used Cat or Waukesha units only when the nameplate shows a continuous or prime rating and a load test passes; converted compressor engines (one to three months of shop work); and a new import set only with EPA certification papers in hand. Immersion tanks ship from stock. The only long-lead item in a Block is the genset, and Phase 0 is when it gets ordered.

## 5. Requirements: power, prime mover, latency

**Power from 300 mcf/d.** 300 mcf/d is 12,500 scf/h. At 1,000 to 1,300 Btu/scf that is 12.5 to 16.25 MMBtu/h [E:pwr-eia-heat-content]. Electricity is fuel energy divided by heat rate [E:pwr-eia-kwh-formula].

| Prime mover | Heat rate or efficiency | MW from 300 mcf/d at 1,067 Btu |
|---|---|---|
| Recip engine, EIA 2025 fleet | 8,853 Btu/kWh HHV [E:pwr-eia-heatrates] | 1.51 |
| Jenbacher J420 | 42.6% LHV [E:pwr-jenbacher-j420] | ~1.52 |
| Cat G3406 class, catalogue peak | 37.3% LHV, ~10,060 HHV [E:pwr-cat-g3406-eff] | 1.33 |
| Simple-cycle gas turbine, EIA fleet | 10,975 Btu/kWh [E:pwr-eia-heatrates] | 1.22 |
| Capstone C1000S microturbine | 10,300 Btu/kWh LHV [E:pwr-capstone-c1000] | ~1.13 |
| Rental 350 kW field-gas set (our fuel basis) | ~12,100 Btu/kWh [E:pwr-sage-350] | 1.10 |

The base case uses the measured rental-set figure, 12,100 Btu/kWh, because a 423 kW engine carrying 269 kW, about 64% load, on conditioned field gas will not reach a new engine's catalogue peak. After 8% parasitic load the fuel supports 1.01 MW net, and four Blocks load 0.99 MW of miners. Gas use per Block is 73 mcf/d, so four Blocks fit a 300 mcf/d well with 2% to spare. At a catalogue 10,060 Btu/kWh each Block would burn 61 mcf/d.

**Rich gas limits the engine, not the fuel.** Rich associated gas carries more energy per scf, not less: the representative Permian mix is about 1,500 Btu/scf [E:gas-pioneer-composition]. The problem is knock. Heavier hydrocarbons lower the methane number and force retarded timing [E:pwr-secondwatt-mn]. Most industrial gas gensets need a methane number of 55-80 or more [E:eng-pioneer-mn], while raw associated gas runs 30-50 [E:eng-pioneer-raw], and vendors put the resulting derate at 15 to 30% [E:gas-pioneer-derate]. The design handles knock with capacity first and treatment second. Each Block needs only 269 kW gross from a 423 ekW continuous engine [E:eng-g3412-cont], 36% headroom, which covers a 30% derate without shedding miners. If Cat or Waukesha rating tools, run on the site's gas analysis, show a deeper derate, a refrigeration dew-point skid is added at the site.

**Gas mass balance with conditioning.** Conditioning removes 100 to 250 Btu per cubic foot of heavy ends [E:pwr-scon-jt], and the removed liquids take volume with them. Take raw gas at 1,500 Btu/scf: 300 mcf/d carries 450 MMBtu/d. Assume conditioning strips 250 Btu/scf and shrinks volume 8% (our assumption; no shrink figure was found). That leaves about 276 mcf/d at 1,250 Btu/scf, or 345 MMBtu/d of engine fuel. The model needs 4 x 73 mcf/d x 1,067 Btu/scf, or 312 MMBtu/d. Conditioned rich gas still covers the fleet with 10% to spare, because the model's 1,067 Btu fuel basis was set below rich-gas energy on purpose. With lean gas near the 1,067 median, no conditioning is needed and no shrink applies.

**Prime mover recommendation: continuous-rated reciprocating gas engine, 400 to 500 kW class.**
- Recip engines tolerate field gas. Waukesha VHP gensets run on "nearly any gaseous fuel without treatment" [E:pwr-waukesha-vhp], Waukesha VGF engines accept 400 to 2,300 Btu fuel [E:eng-kts-vgf], and Crusoe ran VHP9504GSI sets directly on wellhead gas [E:pwr-innio-crusoe]. Jenbacher lists associated petroleum gas as a fuel [E:pwr-jenbacher-apg].
- Continuous rating, because the miners are a flat 24/7 load. A lean-burn engine that meets NSPS JJJJ NOx in-cylinder, such as the G3412 at 0.5 g/bhp-hr [E:eng-g3412-nox], needs only an oxidation catalyst. Rich-burn Waukesha VHP engines are the alternative for the hottest, richest gas, with a three-way catalyst [E:eng-wpi-vhp].
- Not a large engine. The Cat G3520 is 3,120 ekW standby [E:pwr-cat-g3520-rating], more than twice what the site can feed.
- Not a gas turbine. Small turbines take 18 to 36 months and prices rose from about $2,000 to $3,000/kW [E:pwr-utilitydive-gtprice].
- Microturbine only for sour gas. The C1000S accepts raw sour associated gas [E:pwr-capstone-sour] but burns about 15 to 25% more fuel per kWh than a recip engine.
- Not fuel cells. Bloom's measured heat rate is excellent at 7,057 Btu/kWh [E:pwr-gr1d-bloom-measured], but it costs $3,000 to $8,300/kW and its efficiency falls from 65% to 53% over life [E:pwr-gr1d-bloom-eff]. We found no source on its tolerance for raw rich gas.

**Latency and bandwidth requirements by workload.**

| Workload | Bandwidth | Latency tolerance | Uptime | Fits a Block on Starlink? |
|---|---|---|---|---|
| Bitcoin mining | a few kbps per miner [E:cmp-asic-bandwidth], under 1 Mbps for the site | seconds | interruptible | Yes |
| Batch GPU inference or rendering | tens of Mbps sustained | seconds to minutes | 99% is enough | Marginal: Starlink uploads 12-35 Mbps [E:cmp-starlink-priority-spec] |
| Interactive inference | tens to hundreds of Mbps | 150-250 ms already tolerated [E:cmp-inference-geo] | N+1 power, redundant WAN | No on one genset |
| Training | PB-scale data: 1 PB takes ~10 days at 10 Gbps [E:cmp-pb-transfer] | low | high; checkpoints handle 6.5 node failures per 1,000 node-days [E:cmp-training-failures] | No |

Latency is not the issue for any workload a Block can run. Throughput and power redundancy are. Tier III corresponds to 99.982% [E:cmp-tier3], and these tier percentages are legacy estimates [E:cmp-tier-caveat]. A single genset Block will not reach them.

**GPU arithmetic at Block scale.** An 8-GPU DGX B200 draws 14.3 kW [E:cmp-dgxb200-power] and an 8-GPU Blackwell server costs $360,000 to $470,000 [E:cmp-b200-server]. $500k buys one server, which uses 1% of the gas. Frontier racks draw 227 kW each [E:cmp-rack-density], and IT for 1 MW of B300s costs about $39M [E:cmp-b300-it-cost]. The first-principles point is that power is a small slice of GPU cost. One B200 server uses about 125 MWh a year, about $10,600 at $85/MWh, against about $131,000 a year to recover a $415,000 server over 4 years at 10% (our arithmetic). Stranded gas saves a GPU owner a few percent of total cost and costs them bandwidth and uptime. Cheap power matters to bitcoin, where power is most of the cost, not to GPUs. GPU compute at a wellsite is a phase-3 option for a multi-well pad with a microwave link, not the pilot.

## 6. Connectivity and the modular trailer retrofit

**Yes, a trailer can retrofit a stranded well, and Starlink is enough for mining.** Starlink Local Priority costs $55 a month for 50 GB up to $530 a month for 2 TB [E:cmp-starlink-price], hardware starts at $349 [E:cmp-starlink-hw], and Business plans carry a 99.9% uptime SLA [E:cmp-starlink-sla]. The Texas median in H1 2026 was 108.1 Mbps down, 18.5 Mbps up, and 38 ms [E:cmp-ookla-tx]. A 272-miner site at a few kbps each needs about 1 Mbps. Even the throttled speed after the data allowance, 1 Mbps down and 0.5 Mbps up [E:cmp-starlink-throttle], keeps a Block mining. Plan one terminal per Block plus a cellular backup where coverage exists. Each Block keeps its own uplink so it can move alone.

**When bandwidth grows (GPU phase).**
- Starlink Performance Kit: 400+ Mbps download [E:cmp-starlink-perfkit], with no published upload figure.
- Licensed microwave: a Part 101 link costs mid-to-upper five figures [E:cmp-mw-cost], licensing adds 6 to 12 weeks [E:cmp-mw-licensing], and 6 to 11 GHz paths of 20 to 30+ miles are practical [E:cmp-mw-range]. One hop from a pad to a fiber-fed tower is usually the cheapest real-bandwidth path.
- Fiber: medians are $16.25/ft underground (about $86k a mile) and $6.49/ft aerial (about $34k a mile) [E:cmp-fiber-median], within a range of $11 to $24/ft underground [E:cmp-fiber-perfoot]. A five-mile lateral costs as much as a Block. It only pays on a multi-well pad expected to produce for years.

**The retrofit sequence on a stranded well.**
1. Gas sample and flow test. Gas chromatograph for Btu and C2+, a stain tube for H2S, 30 days of meter data from the operator.
2. Gas purchase agreement and site access agreement (section 9 terms).
3. Pad. Gravel, berm, fence, 50 ft setback from the separator and flare.
4. Tie-in. Tee and valve on the separator gas outlet upstream of the flare, scrubber, regulator, meter run [E:gas-cfr-5377b-onsite].
5. Set the genset trailer, then the compute skid, cable at 480 V, fill the cooling loop, power up, point miners at the pool.
6. File the PI-7 within 10 days of construction start if the engine is treated as stationary [E:rsk-tceq-512-10day].

## 7. Cooling: closed-loop economics

**Options compared for a 248 kW Block in Midland heat.**

| Option | Water use | Capex | Notes |
|---|---|---|---|
| Evaporative tower | ~2.2 L/kWh [E:wtr-gasilov-wue]; 6.75M gal/yr per MW [E:wtr-uptime-1mw-tower] | low | 2.6 to 3.4 truckloads a day per MW; dead on arrival |
| Dry cooler with adiabatic assist | ~0.2 L/kWh [E:wtr-gasilov-adiabatic] | medium | water only on the hottest days |
| Liquid (immersion or hydro) + dry cooler | 0.00 L/kWh, PUE 1.09 [E:wtr-gasilov-liquid-dry] | $100-167/kW for dry coolers [E:wtr-bullminers-capex] | chosen |
| Air-cooled container | zero | lowest | rated only to +100F [E:wtr-ez-air-range] |
| Engine-heat absorption chiller | adds a tower | $0.65-1.7M per MW of heat (our arithmetic) | COP 0.7-1.4 vs 6-6.5 electric [E:wtr-absorption-cop] |

**Why closed-loop immersion wins on both capex and opex.**
- Capex. A Fog C6 tank with dry cooler, PDU and coolant costs $4,450 for 24 kW [E:cmp-fog-c6-price]. Twelve tanks plus 35% extra dry-cooler capacity come to $66,400 for a 248 kW Block, about $268/kW. Conventional data-center air cooling is $200 to $500/kW and CDU liquid is $500 to $1,200+/kW [E:wtr-gd-cooling-capex].
- Opex. Dry-cooler fans draw about 3.2% of load on a 1 MW unit [E:wtr-cryptocooling-1mw]. Immersion fluid is about 800 L per 100 kW tank and is not water [E:wtr-bullminers-fluid].
- Heat tolerance. Midland exceeds 100F on 24 days a year and set a 116F record [E:wtr-midland-climate][E:wtr-midland-record]. Air containers stop at +100F, while immersion containers are rated to +120F [E:wtr-ez-imm-range]. A dry cooler loses capacity in heat; one 120 kW unit falls from 140 kW at 25C to 120 kW at 35C [E:wtr-amg-dcx120]. The Block carries 35% more dry-cooler capacity than nameplate (in the BOM) and accepts a small throttle on the hottest afternoons.
- Freeze. Midland reaches freezing on 58 mornings a year [E:wtr-midland-freeze], so the outdoor loop carries about 40% propylene glycol, good to about -8F [E:wtr-pg-freeze].

**The "looping cycle" question answered.** A closed loop that is never drained is the right cycle. Crusoe's hyperscale closed-loop sites fill once and the loop is "never entirely drained or refilled" [E:wtr-crusoe-closedloop]. Using engine exhaust heat to drive an absorption chiller does not pay at this scale. Absorption chillers run on 100-180C by-product heat [E:wtr-trigeneration] but deliver a COP of only 0.7 to 1.4 against 6 to 6.5 for electric chillers [E:wtr-absorption-cop]. A DOE fact sheet (a PDF our checker could not verify) puts installed cost at $1,800 to $6,000 per ton and says absorption needs a larger cooling tower. On those figures it costs more than the whole Block and brings back the water problem. Miners in immersion run happily on warm fluid. No chilled water is needed anywhere.

## 8. Water: DAF, SWD, trucking, and permits

**Water need of the chosen design.** One-time fill plus glycol, then leak top-up only. An Antspace HD5 dry tower for 1.5 MW holds 2.1 m3 of coolant, about 555 gallons [E:wtr-millionminer-hd5]. A Block loop is smaller. One 130-bbl vacuum truck carries 5,460 gallons [E:wtr-ev-130bbl], about ten such fills. Water is a logistics line item, not a constraint. The owner's worry is right only for evaporative cooling, where hauling alone at $1.50 to $4.00 per barrel [E:wtr-pph-hauling] would cost $0.18 to $0.64M a year per MW.

**Can DAF units turn produced water into cooling water?** No. Dissolved air flotation removes suspended oil and solids, not dissolved salts [E:wtr-daf-wiki]. Produced-water TDS is usually too high for reuse [E:wtr-pw-wiki]. In the Permian it is about 110,000 to 170,000 mg/L [E:wtr-beg-tds], three to five times seawater [E:wtr-seawater]. Evaporation concentrates salts and forces blowdown [E:wtr-tower-coc], so post-DAF produced water would scale any wet cooling system within weeks. A true conversion requires desalination. Texas pilots reached 317 mg/L from about 120,000 [E:wtr-beg-desal], at a projected cost under $2/bbl [E:wtr-beg-disposal-cost]. That is a water-treatment business, not a data-center input. There is no DAF "conversion kit" that makes potable or cooling-grade water.

**Should we route anything to SWD plants?** We produce no wastewater. Disposal averages about $0.70 per barrel and rises above $1 with distance [E:wtr-beg-disposal-cost]. The operator already handles its produced water under RRC Rule 9 [E:wtr-rrc-swd-rule9], with stricter Permian disposal permitting since June 1, 2025 [E:wtr-rrc-permian-swd]. Taking on produced-water handling would only add RRC permits to our business.

**Is TCEQ a nightmare?** Not for this design.
- Closed-loop systems need no TCEQ wastewater authorization [E:wtr-tceq-closedloop].
- A public water system starts at 15 connections or 25 people for 60 days a year [E:wtr-tceq-pws]. An unstaffed Block site is far below that.
- Groundwater is controlled by local groundwater districts, not TCEQ or RRC [E:wtr-tceq-gw]. Buying trucked water avoids a well.
- Temporary surface-water rights are available for up to 3 years [E:wtr-tceq-tempwr] if a site ever needs them.
- Produced-water surface discharge and land application moved to TCEQ under HB 2771 and SB 1145 [E:wtr-beg-tceq-transfer]. Avoid both.
- Hauling oil and gas waste for hire needs a $250/yr RRC permit [E:wtr-rrc-hauler]. We haul none.

**Temporary use.** Yes, simpler. A dry closed loop on trucked-in fresh water, with no discharge and no staff living on site, needs neither a wastewater authorization nor a water-system registration (inference from the two rules above; confirm with counsel). Buy water from a licensed bulk tanker service; Midland has potable, RO and DI tanker vendors [E:wtr-waterrunner].

**Opex ideas from industrial practice.**
- Fill all four loops from one truck at mobilization, and store premix glycol in a tote on the trailer.
- Do not take custody of produced water. The operator keeps it under RRC recycling rules, which allow some recycling without a permit [E:wtr-rrc-recycling-rule8] and 60-day minor permits [E:wtr-rrc-minor-permit].
- HB 49 now limits tort liability for treated produced water [E:wtr-hb49-liab]. That helps the operator's own reuse programs, not a Block.

## 9. Hypothesis test: the sub-$500k Lego module

**Owner hypothesis.** A mobile module under $500k, deployed in multiples and combined like Lego, not tied to a gathering line, gives a quicker ROI on stranded gas, and the only open challenges are latency and water.

**Verdict by claim.**

| Claim | Holds? | Evidence |
|---|---|---|
| A module can be built under $500k | Holds for the infrastructure: $406,400 with a new continuous-rated US engine, about $223k with an import engine if it proves out. With 68 owned miners it is $638,960 or about $455k | BOM below |
| Multiples combine like Lego | Holds, as independent islands on a shared gas header | section 1 |
| Not tied to a gathering line | Holds: separator tie-in is an OOOOb-compliant onsite fuel use [E:gas-cfr-5377b-onsite] | section 2 |
| Latency is a challenge | False for mining; only bandwidth limits GPU work | section 5 |
| Water is a challenge | False with closed-loop dry cooling | sections 7-8 |
| Quicker ROI | Breaks at today's prices under every structure we modeled | below |
| These are the only challenges | Breaks: hashprice, decline, engine cost, gas terms, air permits, heat, theft, insurance, tax | below |

**Infrastructure Block BOM ($406,400).**
- New continuous-rated Cat G3412-class field-gas genset, 423 ekW continuous [E:eng-g3412-cont]: $250,000 (estimate within [E:eng-generac-price]). Freight and commissioning: $15,000. Oxidation catalyst for CO and VOC [E:eng-colo-oxcat]: $10,000 (estimates).
- 12 Fog C6 tanks at $4,450 each, including dry cooler, PDU and coolant [E:cmp-fog-c6-price]: $53,400. Extra 35% dry-cooler capacity for 45C days at $100-167/kW [E:wtr-bullminers-capex]: $13,000.
- Block gas train: two-phase scrubber, regulator, meter: $25,000 (estimate). The site's leased conditioning skid and H2S scavenger are operating costs, about $75,000 a year across the fleet.
- 480 V panel and cables $20,000. Trailer or skid $15,000. Starlink, switch, cameras $5,000 (estimates).
- Optional owned miners: 68 S21 XP at $3,420 [E:cmp-s21xp-price], $232,560.

**Decline, simulated month by month.** Wells lose 55% in year one, 30% in year two, then 20% and 16.7% [E:gas-jpt-decline][E:gas-jpt-yr5]. A 300 mcf/d well falls to 201 mcf/d at month 6, 135 at month 12, 95 at month 24 and 63 at month 48. Each Block burns 73 mcf/d. In research/fleet_model.py, four Blocks start on one well, and whenever a site can no longer feed its Blocks, the extra Blocks move to the newest site with spare gas or open a new 300 mcf/d site. Over 5 years that produces 9 moves and 5 new sites, at months 1, 5, 11, 12, 22, 39, 40 and two at 50. Each move costs $30,000 and 3 idle weeks. Each new site costs $40,000 to develop. Fleet availability averages 0.896. The fourth Block leaves in month 1, so the business is a fleet that must have its next sites signed before it needs them, never a single well.

**What a hashing MWh costs at a wellsite (four-Block fleet, 7,783 MWh a year).**

| Cost layer | $/year | $/MWh |
|---|---|---|
| Infrastructure capital, 10% over 5 years | 444,657 | 57.1 |
| Site operations: genset O&M $169k, leased conditioning skids and H2S scavenger $75k, field tech, insurance, tax, moves, new sites, security | 481,422 | 61.9 |
| Gas at $1/mcf [E:com-braiins-paidtotake] | 95,933 | 12.3 |
| Site subtotal | 1,022,012 | 131.3 |
| Miner capital, 10% over 3 years | 374,063 | 48.1 |
| Miner repair and pool fee | 33,236 | 4.3 |
| Total, owning the miners | 1,429,311 | 183.7 |

Revenue at $30.45/PH/day and 13.5 J/TH is $94/MWh. Owning new miners at a wellsite breaks even at about $60/PH/day. The site alone, before miners, needs $0.131/kWh. The hashprice record low this month is $26.20 [E:cmp-dcf-recordlow].

**Who pays whom for the gas.** The evidence points one way. Crusoe sold its service to producers as cost-free [E:com-crusoe-costfree] and paid them a de minimis price for the gas [E:com-crusoe-deminimis]. EZ Blockchain offers no upfront cost to producers [E:com-ez-zeroupfront]. Permian trade press describes producers selling flare gas to miners [E:com-pbog-sell]. An off-grid miner reports miners now typically pay about $1/Mcf [E:com-braiins-paidtotake]. We found no case of a Texas operator paying a fee to have flare gas taken. The Texas RRC had not denied a flaring exception in years as of 2019 [E:com-tribune-rrc-nodenial], so Texas operators feel little forced-shut-in pressure. The exceptions are narrow. During negative Waha pricing, producers paid buyers to take gas [E:com-ngi-waha-pay] and shut in wells [E:com-eastdaley-shutin]. New Mexico requires 98% gas capture by Dec 31, 2026 [E:com-nm-98pct]. EZ Blockchain has also proposed a model where the producer buys the data center and pays EZ a flat fee to operate it [E:com-ngi-ez-flatfee]. The base case therefore pays $1/mcf for gas and assumes no fee.

**Five-year fleet results (research/fleet_model.py, gas $1/mcf, 12,100 Btu/kWh unless noted).**

| Structure and price path | Capex | Year 1 cash | Years 3-5 cash per year | Paid back in 5 years? |
|---|---|---|---|---|
| Host at the $0.0725 US median [E:com-lm-hosting-median] | $1.69M | -$94k | -$20k to $89k | No, cumulative cash -$65k |
| Host at $0.085, the flare-site rate [E:com-ez-hosting-packages] | $1.69M | $1k | $77k-189k | No, $421k back |
| Host at $0.085, gas free | $1.69M | $95k | $173k-287k | No, $901k back |
| Host at $0.085, import engine at 10,060 Btu/kWh | $0.95M | $125k | $125k-237k | No, $772k back |
| Own miners, $30.45, halving cuts hashprice 59% as in 2024 [E:com-hri-2024-q1][E:com-hri-2024-halving] | $2.62M | -$3k | -$247k to -$348k | No, cumulative cash -$1.12M |
| Own miners, $30.45, halving cuts 54% as in 2020 [E:com-ez-2020-halving] | $2.62M | -$3k | -$211k to -$312k | No, cumulative cash -$991k |
| Own miners, $30.45, BTC price fully offsets halving | $2.62M | -$3k | $74k-187k | No, $404k back |
| Own miners, $40, fully offset | $2.62M | $218k | $298k-418k | No, $1.53M back |
| Own miners, $60, fully offset | $2.62M | $680k | $767k-901k | Yes, 3.5 years |
| Own miners, $80, halving cuts 54% | $2.62M | $1.14M | $223k-340k | No, $2.57M back |

Hosting moves the hashprice risk to the tenant but does not remove it. A tenant running S21 XPs earns $94/MWh today and would pay us $72.50 to $85, a thin margin that vanishes at the halving, so take-or-pay terms are hard to get and hard to enforce. Flare-gas hosting does exist in West Texas [E:com-musk-flarehost], and EZ also sells a profit-share tier at $0.055/kWh [E:com-ez-hosting-packages], which is a hashprice bet in different clothes.

**Crediting resale value.** The engines, tanks and trailers last about a decade, so writing them off over 5 years understates the fleet. Credit half the infrastructure back as resale at year 5 (our assumption) and compute the 5-year return:

| Case | Capex | 5-year cash | Resale at year 5 | 5-year IRR |
|---|---|---|---|---|
| Host at $0.0725 | $1.69M | -$65k | $813k | -14% |
| Host at $0.085 | $1.69M | $421k | $813k | -7% |
| Host at $0.085, import engine at 10,060 Btu/kWh | $0.95M | $772k | $445k | 7% |
| Own miners, $30.45, halving cuts 54% | $2.62M | -$991k | $813k | -40% |
| Own miners, $60, fully offset | $2.62M | $3.88M | $813k | 20% |

Resale does not change the verdict. The best hosting case, with a cheap engine that still has to prove its rating and certification, earns 7% a year, below the cost of capital for equipment parked on someone else's lease. Only a $60 hashprice makes the Block a good investment.

**Why not fewer, bigger engines, or rented ones?** Four 423 ekW engines put about 1.7 MW of nameplate on gas that supports about 1.1 MW. That is the price of the Lego design, and it buys two things. The first is derate headroom against 30-50 methane-number gas. The second is mobility in steps. A single 1.2 MW engine would cost less per kW, but the well delivers only 45% of its initial gas at month 12 and 32% at month 24 (the decline curve above), so that engine would run at under half load within a year, at a worse heat rate, and the whole capital would have to move at once. Renting right-sized 400 kW prime field-gas sets instead of buying cuts fleet capex to $0.59M, but at about $10,000 a month each, maintenance included [E:com-haifeng-rental-range][E:pwr-wgl-lease], the rent alone is $480k a year. Hosting at $0.085 then loses $70k to $265k every year in research/fleet_model.py. Renting fits a 90-day pilot, not a fleet. The bigger-engine trade is real and should be priced in Phase 0. Quote one 1 MW-class engine against four 400 kW-class engines, and model both on the measured decline of the first site. If the first site is a manifold of several wells with a flatter combined decline, the bigger engine may win.

**The constraints the hypothesis missed, and the way around each.**
1. Hashprice and the halving. The binding constraint. Way around: commit no capital until a trigger fires (GO IF below). Then own the long-lived infrastructure, and buy miners only at $60/PH/day or more.
2. Engine cost and rating. The genset is 68% of the infrastructure, and it must be continuous-rated: standby ratings cover outages only, up to 200 hours a year [E:eng-iso-esp], and prime ratings cap average load at 70% [E:eng-iso-prp]. Continuous runs 76-85% of the standby figure [E:eng-cummins-ratio][E:eng-g3412-cont]. The engine's cooling package is rated to 43C ambient [E:eng-g3412-ambient], below Midland's 47C record, so summer derate is a dealer question before purchase. The $250,000 engine price is our estimate, because Cat does not publish one. The verdict does not hinge on it. At $172,000 (the low end of the comparable new range [E:eng-generac-price]) hosting at $0.085 returns $488k of $1.37M in 5 years; at $259,000 it returns $413k of $1.72M; with a $66,270 import engine it returns $772k of $0.95M. Owning miners at $60/PH/day pays back in 3.5 years at $250,000 and 2.9 years at $172,000. Way around: get firm quotes from Cat, Waukesha and purpose-built prime-rated wellhead set makers [E:eng-taylor-wellhead] in Phase 0, and buy an import only with EPA stationary certification and a continuous rating on paper.
3. Gas terms and royalty. Gas sold to a miner carries royalty [E:gas-mcfarland-royalty], and Crusoe priced gas off-market [E:gas-crusoe-gpa]. Way around: 1-3 year gas options at no more than $1/mcf with a right to remove Blocks as flow falls, signed now while no capital is at risk. Use the HB 591 severance-tax saving [E:gas-forvis-hb591] to win the operator's yes. Where capture is mandatory, as in New Mexico, offer the operator-owned flat-fee model.
4. Air permit. Engines over 240 hp must register under PBR 106.512 [E:rsk-tceq-512-240hp], and at 500 hp and up a rich-burn engine must hold 2.0 g/hp-hr NOx [E:rsk-tceq-512-nox]. The wellsite rule 106.352 covers only 450 hp sweet gas per site [E:rsk-tceq-352-450hp], and four Block engines total about 1,450 hp at load. NSPS JJJJ limits non-emergency 100-500 hp gas engines to NOx 1.0, CO 2.0 and VOC 0.7 g/hp-hr [E:eng-jjjj-100-500]. Way around: the G3412-class engine meets 0.5 g NOx in the engine [E:eng-g3412-nox], and the oxidation catalyst in the BOM handles CO and VOC [E:eng-colo-oxcat]. A rich-burn alternative would need a three-way catalyst and air/fuel controller, about $25,000 on a 500 hp engine plus $6,000 a year [E:eng-colo-nscr-cost][E:eng-colo-nscr-om]. Every Block is registered as stationary with a PI-7 filed within 10 days of setting [E:rsk-tceq-512-10day]. Nonroad treatment for stays under 12 months [E:rsk-cfr-nonroad-12mo] and the PBR 106.511 portable path [E:rsk-tceq-511-noreg] are a bonus, not something the plan depends on.
5. Heat. The S21 XP immersion model is listed for 0 to 45C [E:com-s21xpimm-45], Bitmain's dry-cooler rack for 40C [E:com-bitmain-ec2dt], and only Fog claims field operation to 50C [E:com-fog-50c]. Midland has reached 47C [E:wtr-midland-record]. Immersion practice alarms at 55C fluid and shuts down at 60C [E:com-dcentral-throttle]. Way around: the 35% extra dry-cooler capacity in the BOM, plus planned throttling on the hottest afternoons. The C6 tank's own ambient rating is not published, so the pilot logs fluid temperature against ambient before Block 2 is bought.
6. Gas quality. Most industrial gas gensets need a methane number of 55-80 or more [E:eng-pioneer-mn], while raw associated gas runs 30-50 [E:eng-pioneer-raw]. Field-gas engines derate to avoid detonation as methane number falls [E:eng-heavyparts-derate], and sour gas above engine limits [E:gas-pioneer-h2s] needs a scavenger. Way around: 36% engine headroom first; then, if the gas analysis requires it, a small refrigeration dew-point skid, which comes as small as 100 Mcfd [E:eng-petrogas-r100] and needs no pressure drop. No small-skid lease price was found; the model carries $2,000 a month per active site, the figure for a larger leased JT skid [E:eng-croft-jt-lease], as a placeholder that Phase 0 quotes replace. Sample before signing, and walk away from wells above 100 ppm H2S.
7. Theft and security. Oilfield theft is routine [E:rsk-tribune-theft], with one producer losing $1.1M in two years [E:rsk-tribune-1m]. Texas funded oilfield-theft task forces in 2025 [E:rsk-tribune-taskforce]. Way around: miners inside locked tanks on a locked trailer, cameras on Starlink, GPS trackers, serial registration, and tenants insuring their own miners.
8. Insurance and tax. Premiums run 1.5 to 4% of insured value [E:rsk-hotaling-premium], and insurers want fire suppression and security described up front [E:rsk-relm-suppress]. Business property above the first $125,000 per location is taxed [E:rsk-bpp-125k], with renditions due April 15 [E:rsk-comptroller-rendition]. Both are in the opex above.

**Bottom line.** The owner is right about the machine and early on the timing. The Lego Block is real: under $500k, trailer-mobile, no gathering line, kbps of bandwidth, one truckload of water. Its weak point is money. At 1 MW scale, with wells that force a move every few months, a wellsite MWh costs more than bitcoin pays today, and nobody in Texas is paying to have the gas taken. The right move now is to buy options, not equipment.

## Phased plan

- **Phase 0, now, about $50k, no equipment.** Sign gas option letters with three operators at no more than $1/mcf (Texas flaring wells, plus New Mexico wells facing the 98% capture deadline). Collect gas chromatograph, H2S and 30-day meter data, and run them through Cat and Waukesha rating tools for methane-number derate. Get firm quotes on continuous-rated field-gas engines, a small conditioning skid lease, and one import engine with certification papers. Collect hosting letters of intent. Pitch the operator-owned flat-fee model to the New Mexico operators.
- **Phase 1, pilot Block, when a trigger fires.** One infrastructure Block on one well, with a rented prime-rated field-gas genset for the first 90 days. Measure kWh per mcf, fluid temperature against ambient, uptime, and site cost per MWh against this model.
- **Phase 2, four Blocks and three optioned next sites.** Only if the pilot's measured site cost is under $131/MWh all-in.
- **Phase 3, hybrid.** On a multi-well pad with a microwave link, add redundant gensets and a GPU batch tenant. Miners act as the flexible load that absorbs gas swings.

GO IF: hashprice holds at or above $60/PH/day for 30 consecutive days, or a tenant signs 12-month take-or-pay hosting for at least 200 kW at $0.13/kWh or more, or an operator signs to buy Blocks under a flat operating fee; and in every case the gas costs no more than $1.00/mcf, tests below 100 ppm H2S, and the first site shows at least 300 mcf/d of measured flow over 30 days (the owner's minimum), from one well or a manifold of nearby wells.

KILL IF: no trigger fires by Dec 31, 2027, four months before the expected 2028 halving, or the pilot's measured site cost exceeds $131/MWh over 90 days, or fewer than 3 next sites with at least 73 mcf/d each are under option by month 6 of the pilot.
