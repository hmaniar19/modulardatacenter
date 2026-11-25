# Stranded gas: where the AI Block gets the best feasibility and project cost

Date: 2026-11-25. Feeds: siting decision for the AI Block (`docs/modular-dc/basis-of-design.md`)
before PR #2 merges. Evidence ids refer to `docs/modular-dc/evidence.json` (270 sources;
`sg-*` = stranded-gas research fetched 2026-11-25) or `research/evidence.json`. Numbers come from
`python3 docs/modular-dc/ai_block_model.py` (site sweep at the bottom of its output).
**ASSUMPTION** marks our own inputs.

## Answer

Stop chasing the cheapest molecule. Across eight basin and source combinations, gas price moves
payback least. Buying shut-in Appalachian gas at $1.50 instead of $2.92/MMBtu saves 0.2 years.

What moves it, in order:
1. The grid price the tenant would otherwise pay at the nearest hub.
2. The rent that hub supports.
3. Gas quality, through engine derate and genset count.
4. Permit and power-sale risk.

On that basis, **Appalachia (SW Pennsylvania / northern West Virginia) ranks first at 5.5 years**:
- Dry Marcellus gas at the M-2 hub index plus a fee.
- Under 10 ms from Northern Virginia.
- Industrial power in Virginia costs 9.86¢/kWh against our ~5¢.
- A cool climate, so the dry-only cooling never throttles.

**The Permian is the fallback at 6.5–7.1 years.** It has the fastest permit and the clearest law
for selling power to tenants, but cheaper grid power, 24 hot days and a recent permit pause.

The lead survives removing both of our Appalachia assumptions (lean-gas derate and smaller remote
discount): 6.8 years against 7.1. It does not survive losing the grid-price gap (8.2 years).

## What "stranded gas" means here, and what it costs

| Source type | Delivered cost | Firmness | Volume and decline | Contract form | Evidence |
|---|---|---|---|---|---|
| Price-stranded Permian (Waha) | Negative 90 days in a row in 2026 (avg −$2.19 Jan–mid-June); back near $1.9–2.0 by Nov; forward basis −$1.15 to −$2.41 | Low: cheap only while pipes are full; congestion returns early 2028 | Associated gas, >50% first-year decline | Waha 2-month avg + $0.55 (Sterling Digital, 5 y + 2×1 y) | [sg-sup-waha-90days] [ai-site-waha-basis-2027] [ai-site-waha-2028-risk] [sg-sup-sterling-price] [gas-jpt-decline] |
| Price-stranded Appalachia (M-2) | M-2 cash $1.12 vs Henry Hub $3.05 (Oct 1–20, 2026); producers shut in at ≤$1.25 | Seasonal: spring and autumn cuts expected until mid-2028 | Shale −75.5% from peak over ~7 years | Firm deals priced "M-2 plus" (EQT) | [sg-sup-m2-cash-oct] [sg-sup-antero-shutin-125] [sg-sup-app-recur-2028] [sg-sup-eqt-m2plus] |
| Stripper and legacy wells | Hub less gathering (undisclosed) | High per well, slow decline | 78% of US wells ≤90 Mcf/d; Appalachia declines ~4.9%/yr | Aggregator at a compressor station (Diversified) | [sg-sup-eia-78pct-marginal] [sg-sup-terminal-decline] |
| Gathering or plant tailgate | Index + ~$0.55 | Medium to high; gathering has outages | 1–25 MW per pad | 5–20 year gas purchase agreements | [sg-sup-sterling-price] [ai-site-epa-gathering-interrupt] |
| Flare gas (Bakken, Permian) | Not priced | Low | Steep decline | Onsite-use tax relief (ND, TX HB 591) | [sg-sup-nd-flare-155] [gas-forvis-hb591] |

The AI Block needs about 1.1 MMcf/d for years. That is too small for a major producer's
attention, too large for one stripper well, and too steady for one flaring well. The workable
form is a firm gathering or tailgate contract at index plus a fee. Seasonal cheap gas is upside,
not the base case.

## Site ranking (4.8 MW, fast-response recips, dry-only cooling)

| Rank | Site | Gas $/MMBtu | Gensets | Rent $/kW-mo | Energy margin $k/yr | Capex $M | Payback | Air permit (days) | Moratorium risk | Selling power to tenants |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Appalachia N WV, M-2 gathering | 3.07 | 5 × 1,500 | 160 | 1,014 | 40.88 | 5.5 y | 120 | low | PSC exemption only at 90 MW+ or in a microgrid district |
| 1 | Appalachia SW PA, M-2 gathering | 2.92 | 5 × 1,500 | 160 | 1,046 | 40.88 | 5.5 y | ~180 (no clock) | medium | Unclear: "the public" test; self-supply exemption only |
| 1 | Appalachia E OH, M-2 gathering | 2.94 | 5 × 1,500 | 160 | 1,042 | 40.88 | 5.5 y | 240 | high | Allowed (HB 15) |
| 4 | Haynesville NW LA, dry gas | 3.10 | 5 × 1,500 | 144 | 405 | 38.16 | 6.4 y | ~30 | low | Unclear: LPSC docket R-37905 |
| 5 | San Juan NM, ~5,400 ft | 3.11 | 6 × 1,500 | 156 | 603 | 43.37 | 6.5 y | 120 | medium | Allowed (HB 93) |
| 6 | Permian TX, Waha gathering | 2.41 | 6 × 1,500 | 138 | 547 | 41.12 | 7.1 y | 9 | high | Allowed as an incident of tenancy |
| 7 | Anadarko OK, gathering | 3.26 | 6 × 1,500 | 138 | 354 | 41.14 | 7.4 y | 180 | medium | Allowed (SB 480) |
| 8 | Bakken ND, associated gas | 2.90 | 6 × 1,500 | 125 | 1,081 | 43.38 | 7.8 y | 120 | low | Unknown |

How each input was set:
- **Gas:** Henry Hub $3.05 [sg-sup-m2-cash-oct], plus the local forward basis (average of the two
  cited strips: [ai-site-waha-basis-2027] [sg-sup-m2-basis-strip] [sg-sup-haynesville-basis]
  [sg-sup-midcon-basis] [sg-sup-rockies-basis]; San Juan at $2.3 spot [sg-sup-sanjuan-price]), plus
  $0.55 transport and service [sg-sup-sterling-price], plus state production tax: TX 7.5%
  [sg-sup-tx-sev-75], WV 5%, OH 2.5¢/Mcf [sg-sup-oh-sev], OK 7% [sg-sup-ok-gpt], ND 6.55¢/Mcf
  [sg-sup-nd-gpt], NM ~8.97% [sg-sup-nm-combined], LA 15.14¢/Mcf [sg-sup-la-sev], PA none.
  The contract can make the buyer pay it [sg-sup-tx-sev-payer].
- **Derate:** rich associated gas 20% [gas-pioneer-derate] [ai-pwr-apg-mn]; lean dry gas 5%
  (ASSUMPTION); San Juan another 10% for altitude (ASSUMPTION).
- **Rent:** hub band midpoint [sg-mkt-rent-dfw-phx] [sg-mkt-rent-secondary], or JLL's 1–5 MW $178
  [ai-cmp-jll-rent-1mw] where no hub rent exists. Less a remote discount of 10% under 10 ms to the
  hub, 20% at 10–20 ms, 30% beyond that or with no hub rent (ASSUMPTION, direction from
  [sg-mkt-secondary-discount]). Appalachia is 5.5 ms from Washington [sg-mkt-rtt-pit-was].
- **Energy margin:** tenants pay our cost plus half the gap to the hub state's industrial price.
  EIA Electric Power Monthly table 5.6.A, Sept 2026: VA 9.86, TX 6.99, AZ 7.95, CO 10.04 ¢/kWh.
  Energy is bundled into the lease, not sold metered (see the legal section).
- **Build cost index:** Dallas 1.00, Columbus 1.12, Phoenix 1.10 [sg-mkt-cost-cw-markets];
  Bakken 1.10 (ASSUMPTION).

**Robustness of the Appalachia lead (SW PA):**

| Case | Gensets | Payback |
|---|---|---|
| Base | 5 | 5.5 y |
| Rich-gas derate 20% instead of 5% | 6 | 6.0 y |
| Remote discount 20% instead of 10% | 5 | 6.3 y |
| Both | 6 | 6.8 y |
| Both, and no energy margin | 6 | 8.2 y |
| Seasonal shut-in gas at $1.50/MMBtu | 5 | 5.3 y |
| *Permian with lean tailgate gas (derate 5%)* | 5 | *6.5 y* |

## Why each basin lands where it does

- **Appalachia.**
  - Dry gas, cool climate (Pittsburgh mean max 92.6 °F, 9.5 days ≥90 °F
    [sg-reg-clim-pittsburgh-meanmax]) and the expensive Northern Virginia grid as the comparison.
    The region already absorbs AI load: Homer City 4.5 GW [sg-mkt-prec-homer] and the Shippingport
    campus [sg-mkt-prec-shippingport].
  - Cost: building is 12% dearer than Dallas, and labour is tight [sg-mkt-labor-columbus].
  - Between the three states:
    - Ohio has the clearest power-sale law (HB 15) [sg-reg-oh-hb15], but 138 local moratoria upheld
      by its Supreme Court [sg-reg-oh-moratoria] and a 240-day permit [sg-reg-oh-pti-180d].
    - West Virginia has the lowest permit risk (Rule 13, 90 + 30 days) [sg-reg-wv-r13-90d], but its
      PSC exemption needs 90 MW+ or a certified microgrid district [sg-reg-wv-hb2014-psc]
      [sg-reg-wv-microgrid-psc].
    - Pennsylvania has no severance tax [sg-sup-pa-impactfee]. Its executive order on data center
      permits applies only above 25 MW [sg-reg-pa-eo-2026-05], but its utility test is unclear for
      selling power to tenants [sg-reg-pa-public-utility].
- **Haynesville.**
  - Lean gas and a fast notification permit [sg-reg-la-311-gen], but a hot, humid climate
    (91 days >90 °F) [sg-reg-clim-shreveport-meanmax].
  - Louisiana's permit excludes "facility byproducts" as fuel [sg-reg-la-311-fuel].
  - Third-party power sales sit in an open docket.
- **Permian.**
  - Cheapest gas, cheapest build, 9-day permits [ai-pwr-tceq-days-2024], and a clear tenancy
    exemption [sg-reg-tx-tenant-exempt].
  - Held back by Texas's cheap grid power (less margin), rich gathering gas (one more genset),
    24 throttle days, and a permit pause that could recur [ai-pwr-tceq-pause-directive].
  - Buying processing-plant tailgate gas instead of raw gathering gas recovers 0.6 years.
- **San Juan.** Good rent against Phoenix, but gas is no longer cheap and altitude costs a genset.
- **Anadarko.** The most expensive gas plus city moratoria [sg-reg-ok-local].
- **Bakken.**
  - Best grid margin against Denver, and the closest precedent: an off-grid recip, dry-cooled
    campus near Williston [sg-mkt-prec-wdi] [sg-mkt-prec-wdi-recip].
  - But no hub rent nearby, so the rent assumption is weakest there.

## Selling power to tenants without becoming a utility

- **Texas.** Furnishing electricity to tenants "as an incident of tenancy" is excluded from the
  utility definition [sg-reg-tx-tenant-exempt]. Selling metered kWh would make us a retail
  provider, and those cannot own generation [sg-reg-tx-rep]. Price one all-in lease per kW-month.
- **Ohio, Oklahoma, New Mexico** allow data centers to self-supply: [sg-reg-oh-hb15]
  [sg-reg-ok-sb480] [sg-reg-nm-hb93].
- **Pennsylvania and West Virginia** need counsel before a site is optioned. One structure to test
  (ASSUMPTION, not legal advice): the tenant leases the whole Block, power island included, so the
  generation counts as self-supply.

## Recommendation

1. **Lead the site search in northern West Virginia and SW Pennsylvania.** Target dry Marcellus gas
   on gathering at an "M-2 plus" price [sg-sup-eqt-m2plus]. Pool low-decline conventional wells
   through an aggregator's compressor station where available [sg-sup-diversified-ky] [sg-sup-diversified-lowdecline].
2. **Keep the Permian as the fast parallel track.** Buy processing-plant tailgate gas, not raw
   gathering gas. Use the 9-day permit, and file before any new pause.
3. **Hold Haynesville** until Louisiana's fuel-byproduct and third-party-sale questions are answered.
4. **Drop Anadarko and Bakken** unless a specific site brings a tenant or a gas price well below index.

## Not settled

- **Basin rents.** No published rent exists for any basin, and none for Pittsburgh. The 10/20/30%
  remote discount is ours. Next check: broker quotes for a 5 MW powered shell near Pittsburgh and Dallas.
- **Lean-gas derate.** Run a chromatograph on the candidate gathering or tailgate gas.
- **Power-sale structure in PA and WV.** Needs legal counsel.
- **Basin round-trip latency.** No ping node exists inside any basin; carrier test pings would settle it.
- **Small-buyer gas terms outside the one disclosed Sterling contract.**
- **Permit times outside Texas.** Only statutory clocks were found.
