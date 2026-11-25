"""AI Block scenario sweep: 3 sizes x 2 prime movers x 2 cooling modes = 12 scenarios.

Run: python3 docs/modular-dc/ai_block_model.py [--json]
Each input names an evidence id from docs/modular-dc/evidence.json or research/evidence.json,
or is marked ASSUMPTION. Capex excludes IT: tenants own the GPUs.
"""
import json
import math
import sys

HOURS = 8760

# Block sizes: IT design load in kW. One GB200/GB300 NVL72 scalable unit (8 racks) needs 1.2 MW
# (ai-cmp-gb200-su-mw); half and four units bracket it.
SIZES = {"Half SU 0.6 MW": 600, "One SU 1.2 MW": 1200, "Four SU 4.8 MW": 4800}

# Cooling: peak and annual facility overhead as a fraction of IT (PUE - 1).
# Dry-only: CDU ~2% (ai-cmp-vertiv-cdu-power), dry-cooler fans ~3% (wtr-cryptocooling-1mw),
# 10% air-side heat (ai-cmp-gb300-split) on DX at ~0.3 kW/kW = 3%, electrical losses 2%,
# misc 1% -> 1.11 annual, 1.15 peak (ASSUMPTION built from the cited parts).
# Dry + trim chiller: same, plus trim chiller on the 115 afternoons above 90 F
# (wtr-midland-climate) -> 1.13 annual, 1.30 peak (ASSUMPTION; Schneider RD109 reaches
# 1.15 annual in Dallas with adiabatic assist, ai-cmp-se-rd109-pue).
COOLING = {
    "Dry-only, 45 C loop": {"peak": 0.15, "annual": 0.11, "capex_per_kw_it": 0},
    "Dry + trim chiller": {"peak": 0.30, "annual": 0.13, "capex_per_kw_it": 120},  # ASSUMPTION
}
# Dry-only cannot hold a 45 C rack inlet above ~37 C ambient (8 K approach, ASSUMPTION):
# Midland passes 37.8 C on 24 afternoons (wtr-midland-climate). Tenants accept GPU throttling
# on those afternoons, or the Block runs the trim-chiller variant.
DRY_ONLY_HOT_AFTERNOONS = 24

# Prime movers: unit nameplate kW, derate for rich field gas and summer heat, heat rate.
PRIME_MOVERS = {
    "Recip fast-response": {
        # Cat G3516 Fast Response 1,500 ekW continuous, 100% block load, 9,771 Btu/ekWh
        # (ai-pwr-g3516fr-block, ai-pwr-g3516fr-hr). Derate 20% for rich gas (gas-pioneer-derate
        # 15-30%, ai-pwr-apg-mn).
        "units": [(1500, 0.80)],
        "heat_rate": 9771,
        "capex_curve": [(500, 3150), (1000, 2800), (2000, 2550), (4500, 2000)],  # ai-site-doe-recip-size
        "om_per_mwh": 19,  # ai-site-doe-maint-1p9c
    },
    "Gas turbine": {
        # Capstone C1000S 1,000 kW for small Blocks (pwr-capstone-c1000), Solar Taurus 60
        # 5,670 kW for 4.8 MW (ai-pwr-taurus60); 20% loss at 100 F (ai-pwr-taurus70-derate).
        "units": [(1000, 0.80), (5670, 0.80)],
        "heat_rate": 10830,  # ai-pwr-taurus60; C1000S is 10,300 LHV (pwr-capstone-c1000)
        "capex_curve": [(2000, 5200), (5000, 3400), (10000, 2500)],  # ai-site-doe-gt-size
        "om_per_mwh": 15,  # ASSUMPTION
    },
}
PART_LOAD_PENALTY = 0.14  # +14% fuel per kWh at ~50% load (ai-site-partload-14pct), applied pro rata
GAS_BTU_PER_SCF = 1067    # gas-tetrasoft-tx-btu
GAS_USD_PER_MCF = 1.60    # ASSUMPTION: firm residue gas near Waha (ai-site-waha-basis-2027)

BESS_HOURS = 1.0          # ASSUMPTION: covers one unit trip, swings and checkpoint dips
BESS_USD_PER_KWH = 254    # ai-pwr-megapack-tx
BESS_INSTALL = 0.15       # ASSUMPTION
BESS_OM_PER_KWH_YR = 8830 / 3900  # ai-pwr-megapack-tx maintenance per kWh

# IT enclosure, CDU, dry coolers, 480/415 V distribution, controls, fire: modular AI hall
# ~US$4.4M/MW excl. IT on a site with existing infrastructure (cmp-modular-cost).
HALL_USD_PER_KW_IT = 4400
SITE_WORK_USD = {600: 400_000, 1200: 600_000, 4800: 1_500_000}  # ASSUMPTION: pad, gas tap, fence, permits
SWITCHGEAR_USD_PER_UNIT = 25_000  # pwr-turnkey-switchgear $25-50k for two sets

# Network: 100G wave $2.5-6k/mo, off-net tail $1-3k, 1+1 protection doubles
# (ai-site-wave-longhaul, ai-site-wave-offnet-protect) -> ~$14k/mo protected (ASSUMPTION midpoint).
NETWORK_USD_PER_MONTH = 14_000
STAFF_USD_PER_YEAR = {600: 450_000, 1200: 450_000, 4800: 750_000}  # ASSUMPTION: 24/7 techs, 5-8 FTE
INSURANCE_RATE = 0.025  # rsk-hotaling-premium 1.5-4% of insured value

# Revenue: rent per kW of IT per month plus energy at cost. JLL: $210 + E for 250 kW-1 MW,
# $178 + E for 1-5 MW (ai-cmp-jll-rent-1mw). Remote islanded site discount 20% (ASSUMPTION).
def rent_per_kw_month(it_kw: int) -> float:
    return (210 if it_kw <= 1000 else 178) * 0.80


UTILIZATION = 0.90  # ASSUMPTION: share of IT capacity leased on average


def interp(curve, x):
    if x <= curve[0][0]:
        return curve[0][1]
    for (x0, y0), (x1, y1) in zip(curve, curve[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return curve[-1][1]


def scenario(size_name, it_kw, pm_name, cool_name, hall=HALL_USD_PER_KW_IT, util=UTILIZATION, rent_kw_month=None):
    pm, cool = PRIME_MOVERS[pm_name], COOLING[cool_name]
    peak_kw = it_kw * (1 + cool["peak"])
    avg_kw = it_kw * util * (1 + cool["annual"])
    unit_kw, derate = min(
        PRIME_MOVERS[pm_name]["units"],
        key=lambda u: (math.ceil(peak_kw / (u[0] * u[1])) + 1) * u[0],
    )
    usable = unit_kw * derate
    running = math.ceil(peak_kw / usable)
    units = running + 1  # N+1
    nameplate = units * unit_kw
    load_factor = avg_kw / (running * usable)
    heat_rate = pm["heat_rate"] * (1 + PART_LOAD_PENALTY * max(0.0, 1 - load_factor) / 0.5)
    mwh = avg_kw * HOURS / 1000
    mcfd = avg_kw * 24 * heat_rate / GAS_BTU_PER_SCF / 1000

    bess_kw = usable
    bess_kwh = bess_kw * BESS_HOURS
    capex = {
        "power": nameplate * interp(pm["capex_curve"], nameplate) + units * SWITCHGEAR_USD_PER_UNIT,
        "bess": bess_kwh * BESS_USD_PER_KWH * (1 + BESS_INSTALL),
        "hall_cooling_electrical": it_kw * (hall + cool["capex_per_kw_it"]),
        "site": SITE_WORK_USD[it_kw],
    }
    total_capex = sum(capex.values())
    energy_cost = mwh * pm["om_per_mwh"] + mcfd * 365 * GAS_USD_PER_MCF
    fixed_opex = (
        NETWORK_USD_PER_MONTH * 12
        + STAFF_USD_PER_YEAR[it_kw]
        + INSURANCE_RATE * total_capex
        + bess_kwh * BESS_OM_PER_KWH_YR
    )
    rent = (rent_kw_month or rent_per_kw_month(it_kw)) * it_kw * util * 12
    cash = rent - fixed_opex  # energy is billed to tenants at cost
    return {
        "size": size_name, "prime_mover": pm_name, "cooling": cool_name,
        "it_kw": it_kw, "peak_kw": round(peak_kw), "units": f"{units} x {unit_kw} kW",
        "nameplate_kw": nameplate, "load_factor": round(load_factor, 2),
        "bess": f"{round(bess_kw)} kW / {round(bess_kwh)} kWh",
        "gas_mcfd": round(mcfd), "energy_usd_per_mwh": round(energy_cost / mwh, 1),
        "capex": {k: round(v) for k, v in capex.items()}, "capex_total": round(total_capex),
        "capex_per_kw_it": round(total_capex / it_kw),
        "rent_usd_yr": round(rent), "fixed_opex_usd_yr": round(fixed_opex),
        "cash_usd_yr": round(cash),
        "payback_years": round(total_capex / cash, 1) if cash > 0 else None,
    }


def main():
    rows = [scenario(s, kw, pm, c) for s, kw in SIZES.items() for pm in PRIME_MOVERS for c in COOLING]
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
        return
    print(f"{'#':>2} {'size':<15}{'prime mover':<20}{'cooling':<20}{'gensets':<14}{'gas mcf/d':>9}"
          f"{'$/MWh':>7}{'capex $M':>9}{'$/kW IT':>8}{'cash $k/yr':>11}{'payback':>8}")
    for i, r in enumerate(rows, 1):
        pb = f"{r['payback_years']} y" if r["payback_years"] else "never"
        print(f"{i:>2} {r['size']:<15}{r['prime_mover']:<20}{r['cooling']:<20}{r['units']:<14}"
              f"{r['gas_mcfd']:>9}{r['energy_usd_per_mwh']:>7}{r['capex_total'] / 1e6:>9.2f}"
              f"{r['capex_per_kw_it']:>8}{r['cash_usd_yr'] / 1e3:>11.0f}{pb:>8}")
    print(f"\nDry-only scenarios throttle GPUs on ~{DRY_ONLY_HOT_AFTERNOONS} hot afternoons a year.")
    chosen = ("Four SU 4.8 MW", 4800, "Recip fast-response", "Dry-only, 45 C loop")
    print(f"\nSensitivity, chosen design (base payback {scenario(*chosen)['payback_years']} y):")
    for label, overrides in [
        ("Hall $2,500/kW IT", {"hall": 2500}),
        ("Hall $6,000/kW IT", {"hall": 6000}),
        ("Utilization 70%", {"util": 0.70}),
        ("Rent $178/kW-month, no remote discount", {"rent_kw_month": 178}),
        ("Rent $110/kW-month", {"rent_kw_month": 110}),
    ]:
        r = scenario(*chosen, **overrides)
        print(f"  {label:<40} capex ${r['capex_total'] / 1e6:5.1f}M  payback {r['payback_years']} y")


if __name__ == "__main__":
    main()
