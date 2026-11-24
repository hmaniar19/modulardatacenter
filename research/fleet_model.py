#!/usr/bin/env python3
"""Month-by-month fleet simulation for the flare-gas Block study (study.md section 9).

Four Blocks start on one 300 mcf/d well. Each well declines (year-1 55%, year-2 30%,
year-3 20%, then 16.7%/yr, per gas-jpt-decline). When a site's gas can no longer feed
all its Blocks, the excess Blocks move to the newest site with spare gas, or open a new
300 mcf/d site. A move costs cash and idle weeks. Hashprice can halve at the 2028 halving.

Run: python3 research/fleet_model.py            (prints all scenarios)
"""
import math

MONTHS = 60
MINERS, MINER_KW, MINER_PRICE = 68, 3.645, 3420       # cmp-s21xp-spec, cmp-s21xp-price; 4 Blocks fit 300 mcf/d at 12,100 Btu/kWh
PARASITIC = 0.08
BTU_SCF = 1067                                          # gas-tetrasoft-tx-btu
MOVE_COST, MOVE_IDLE_WEEKS = 30000, 3                   # lowboy, crane, re-tie-in, pad, re-registration
SITE_GAS0 = 300                                         # owner minimum, mcf/d
ANNUAL_DECLINE = [0.55, 0.30, 0.20, 0.167, 0.167]       # gas-jpt-decline, gas-jpt-yr5
BLOCK_INFRA = 250000 + 15000 + 10000 + 12 * 4450 + 13000 + 20000 + 25000 + 15000 + 5000
# new continuous-rated field-gas engine, Cat G3412 non-emergency class, 423 ekW continuous
# (eng-g3412-cont; price estimated within eng-generac-price SG500 range), freight/commissioning,
# oxidation catalyst for CO/VOC (eng-colo-oxcat), 12 Fog C6 tanks (cmp-fog-c6-price), +35% dry-cooler
# capacity, 480 V, Block gas train (scrubber, regulator, meter), trailer, network
NEW_SITE_COST = 40000                                   # gas test, agreement, legal, header
MECH_AVAIL = 0.92
FIXED_OPEX = 60000 + 12000 + 1000 + 60000 + 15000        # field tech, security, Starlink, leased conditioning skids (~2.5 sites x $2k/mo, eng-croft-jt-lease), H2S scavenger
GENSET_OM_PER_MWH = 20
INSURANCE_RATE, PROPERTY_TAX_RATE = 0.025, 0.018         # rsk-hotaling-premium; on value above rsk-bpp-125k
POOL_FEE, MINER_REPAIR_RATE = 0.02, 0.02
HALVING_MONTH = 17                                      # ~Apr 2028 from Dec 2026 start


def block_it_kw():
    return MINERS * MINER_KW


def block_gas_mcfd(heat_rate):
    gross_kw = block_it_kw() / (1 - PARASITIC)
    return gross_kw * heat_rate * 24 / BTU_SCF / 1000


def well_rate(age_months):
    q = SITE_GAS0
    for m in range(age_months):
        d = ANNUAL_DECLINE[min(m // 12, len(ANNUAL_DECLINE) - 1)]
        q *= (1 - d) ** (1 / 12)
    return q

def simulate(hashprice=30.45, jt=13.5, gas_price=1.0, heat_rate=12100, halving_cut=0.46,
             own_miners=False, hosting_usd_kwh=0.0725, months=MONTHS, n_blocks=4,
             block_infra=BLOCK_INFRA, rent_genset_usd_month=0):
    if rent_genset_usd_month:
        block_infra -= 275000  # engine, commissioning and catalyst come with the rental
    capex = n_blocks * (block_infra + (MINERS * MINER_PRICE if own_miners else 0)) + 60000
    need = block_gas_mcfd(heat_rate)
    sites = [{"age": 0, "blocks": n_blocks}]
    cash_by_year, cum, payback, moves, opened = [0.0] * math.ceil(months / 12), -capex, None, 0, 1
    for m in range(months):
        idle_block_weeks = 0.0
        month_moves = 0
        for s in sites:
            cap = int(well_rate(s["age"]) // need)
            if s["blocks"] > cap:
                excess = s["blocks"] - cap
                s["blocks"] = cap
                month_moves += excess
        for _ in range(month_moves):
            newest = sites[-1]
            if newest["blocks"] < int(well_rate(newest["age"]) // need) and newest["age"] < 6:
                newest["blocks"] += 1
            else:
                sites.append({"age": 0, "blocks": 1})
                opened += 1
        moves += month_moves
        idle_block_weeks = month_moves * MOVE_IDLE_WEEKS
        block_months = n_blocks - idle_block_weeks / 4.345
        mwh = block_months * block_it_kw() / 1000 * 730 * MECH_AVAIL
        hp = hashprice * (halving_cut if m >= HALVING_MONTH else 1.0)
        if own_miners:
            rev = hp / (jt * 24 / 1000) * mwh
            var = POOL_FEE * rev + MINER_REPAIR_RATE * n_blocks * MINERS * MINER_PRICE / 12
        else:
            rev = hosting_usd_kwh * 1000 * mwh
            var = 0.0
        gas_mcf = mwh / (1 - PARASITIC) * 1000 * heat_rate / BTU_SCF / 1000
        genset_om = 0 if rent_genset_usd_month else GENSET_OM_PER_MWH * mwh / (1 - PARASITIC)
        opex = (genset_om + n_blocks * rent_genset_usd_month + FIXED_OPEX / 12
                + INSURANCE_RATE * capex / 12 + PROPERTY_TAX_RATE * max(capex - 125000, 0) / 12 + var
                + month_moves * MOVE_COST)
        new_sites = sum(1 for s in sites if s["age"] == 0) - (1 if m == 0 else 0)
        opex += max(new_sites, 0) * NEW_SITE_COST
        cash = rev - opex - gas_mcf * gas_price
        cash_by_year[m // 12] += cash
        cum += cash
        if payback is None and cum >= 0:
            payback = round((m + 1) / 12, 1)
        for s in sites:
            s["age"] += 1
        sites = [s for s in sites if s["blocks"] > 0 or s is sites[-1]]
    return {"capex": round(capex), "block_gas_mcfd": round(need, 1), "moves_5y": moves,
            "sites_opened_5y": opened, "cash_by_year": [round(c) for c in cash_by_year],
            "cum_5y": round(cum + capex), "payback_years": payback}


IMPORT_GENSET_INFRA = BLOCK_INFRA - 250000 + 66270      # cmp-genset-400 / eng-gensetplus-cn class instead of new G3412
RENT = 10000  # $/month per 400 kW prime field-gas set, maintenance included (com-haifeng-rental-range, pwr-wgl-lease)

SCENARIOS = {
    "BASE host at $0.0725/kWh US median (com-lm-hosting-median), gas $1/mcf": {},
    "host at $0.085/kWh flare-site rate (com-ez-hosting-packages)": {"hosting_usd_kwh": 0.085},
    "host at $0.085/kWh, gas free": {"hosting_usd_kwh": 0.085, "gas_price": 0.0},
    "host at $0.085/kWh, import genset, 10,060 Btu/kWh": {"hosting_usd_kwh": 0.085, "heat_rate": 10060, "block_infra": IMPORT_GENSET_INFRA},
    "host at $0.085/kWh, rented 400 kW prime gensets at $10k/month": {"hosting_usd_kwh": 0.085, "rent_genset_usd_month": RENT},
    "own miners, $30.45, halving x0.41 (2024 repeat, com-hri-2024-q1)": {"own_miners": True, "halving_cut": 0.41},
    "own miners, $30.45, halving x0.46 (2020 repeat, com-ez-2020-halving)": {"own_miners": True},
    "own miners, $30.45, BTC price fully offsets halving": {"own_miners": True, "halving_cut": 1.0},
    "own miners, $40, fully offset": {"own_miners": True, "hashprice": 40, "halving_cut": 1.0},
    "own miners, $60, fully offset": {"own_miners": True, "hashprice": 60, "halving_cut": 1.0},
    "own miners, $80, halving x0.46": {"own_miners": True, "hashprice": 80},
    "own miners, S23 11 J/TH at same price, $30.45, fully offset": {"own_miners": True, "jt": 11, "halving_cut": 1.0},
}


if __name__ == "__main__":
    print(f"Block IT {block_it_kw():.0f} kW, gas per Block {block_gas_mcfd(10060):.1f} mcf/d "
          f"(10,060 Btu/kWh), {block_gas_mcfd(12100):.1f} mcf/d (12,100)")
    print("well rate mcf/d by month:", {m: round(well_rate(m)) for m in (0, 6, 12, 18, 24, 36, 48)})
    for name, kw in SCENARIOS.items():
        print(name, simulate(**kw))
