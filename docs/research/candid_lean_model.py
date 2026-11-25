"""Startup cost and break-even model for a standalone Candid-style owner's-engineering department.

Run: python3 docs/research/candid_lean_model.py
Inputs are tagged (cited) or (estimate); sources are in candid-intelligence-lean-replica.md.
"""

SETUP = {
    "Separate LLC formation, optional liability wall (estimate, verify with TX SOS)": 300,
    "TBPELS firm registration, >1 employee (cited)": 150,
    "Legal: MSA/NDA templates, PE liability terms, info-barrier policy (estimate)": 6_000,
    "Brand, site, sample deliverable pack (estimate)": 3_000,
    "Workstations x2 (estimate)": 6_000,
    "Backtest dataset: public plant records, vendor spec sheets (estimate)": 5_000,
}

MONTHLY = {
    "Part-time W-2 Texas PE in responsible charge, 40 h/mo @ $125 (estimate)": 40 * 125,
    "Professional liability $1M/$1M, $10k/yr, midpoint of cited $2.5k-$20k": 10_000 / 12,
    "General liability + cyber (estimate)": 250,
    "LLM APIs, cloud, Workspace, CAD/PDF tools (estimate)": 1_200,
    "Sales: conferences, travel, amortized (estimate)": 1_500,
    "Accounting, payroll, misc (estimate)": 500,
}
FOUNDER_DRAW = 2 * 4_000  # decision: two founders on a survival draw

DEFERRED = {
    "SOC 2 Type I first year (cited ~$20k all-in)": 20_000,
    "Thermoflow licence (price unpublished; placeholder until quoted)": 30_000,
}

# (price, PE review hours, direct non-PE cost, delivery load in pre-FEED equivalents)
OFFERS = {
    "Site screen (FEL1, 1 week)": (12_000, 6, 300, 0.25),
    "Pre-FEED pack (FEL2, 4 weeks)": (55_000, 30, 1_500, 1.0),
    "Owner's-engineer retainer (monthly)": (15_000, 12, 500, 0.5),
}
PE_RATE = 125            # USD/h beyond the 40 included hours (estimate)
FOUNDER_CAPACITY = 2.0   # pre-FEED equivalents per month the two founders can deliver (estimate)
HIRE_CAPACITY = 1.5      # per added senior engineer (estimate)
HIRE_COST = 175_000 * 1.3 / 12  # Candid's posted $100k-$250k band midpoint, 1.3x load

# Monthly counts of (screens, pre-FEED packs, active retainers)
SCENARIOS = {
    "base": [
        (0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (2, 1, 0), (2, 1, 1),
        (2, 1, 1), (2, 2, 1), (2, 2, 1), (2, 2, 2), (3, 2, 2), (3, 2, 2),
    ],
    "downside": [
        (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 1, 0),
        (1, 0, 0), (1, 1, 0), (2, 1, 0), (1, 1, 1), (2, 1, 1), (2, 1, 1),
    ],
}


def run(name: str, ramp: list[tuple[int, int, int]]) -> None:
    offers = list(OFFERS.values())
    fixed_base = sum(MONTHLY.values()) + FOUNDER_DRAW
    cash = low = -sum(SETUP.values())
    hires, breakeven, year_revenue = 0, None, 0
    print(f"\n[{name}] month  revenue   direct   fixed   hires  net       cumulative")
    for m, counts in enumerate(ramp, 1):
        revenue = sum(c * o[0] for c, o in zip(counts, offers))
        pe_hours = sum(c * o[1] for c, o in zip(counts, offers))
        load = sum(c * o[3] for c, o in zip(counts, offers))
        while load > FOUNDER_CAPACITY + hires * HIRE_CAPACITY:
            hires += 1
        direct = max(0, pe_hours - 40) * PE_RATE + sum(c * o[2] for c, o in zip(counts, offers))
        fixed = fixed_base + hires * HIRE_COST
        net = revenue - direct - fixed
        cash += net
        low = min(low, cash)
        year_revenue += revenue
        if breakeven is None and net > 0:
            breakeven = m
        print(f"{m:>12}  {revenue:>8,.0f} {direct:>8,.0f} {fixed:>8,.0f} {hires:>5}  {net:>8,.0f} {cash:>12,.0f}")
    print(f"  first cash-positive month: {breakeven}; peak cash need: ${-low:,.0f}; "
          f"with deferred items: ${-low + sum(DEFERRED.values()):,.0f}; "
          f"year-1 revenue: ${year_revenue:,.0f}; year-end cash: ${cash:,.0f}")


def main() -> None:
    print(f"One-time setup: ${sum(SETUP.values()):,.0f}")
    print(f"Monthly fixed before hires: ${sum(MONTHLY.values()) + FOUNDER_DRAW:,.0f}")
    print(f"Deferred until a buyer requires them: ${sum(DEFERRED.values()):,.0f}")
    for name, (price, hours, direct, _) in OFFERS.items():
        cost = hours * PE_RATE + direct
        print(f"{name}: ${price:,}, direct ${cost:,}, gross margin {1 - cost / price:.0%} (excl. founder time)")
    for name, ramp in SCENARIOS.items():
        run(name, ramp)
    # PitchBook lists 7 employees; Ashby lists 7 open roles. Inference, not a reported figure.
    print(f"\nCandid-style payroll burn, 14 heads x $175k x 1.3: ${14 * 175_000 * 1.3:,.0f}/yr")


if __name__ == "__main__":
    main()
