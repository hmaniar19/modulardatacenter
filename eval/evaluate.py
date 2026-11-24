#!/usr/bin/env python3
"""Flare-gas modular data center study evaluator. Stdlib only. OFF-LIMITS to the research agent.
Order: tripwire -> run cap -> hard gates -> evidence check -> site physics + economics
-> critic (median of N) -> METRIC / ASI lines. Any gate failure exits non-zero.
"""
import hashlib, html, json, os, re, statistics, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

ROOT = Path(os.environ.get("MDC_ROOT", Path(__file__).resolve().parent.parent))
SELFTEST = os.environ.get("MDC_SELFTEST") == "1"
STATE = Path(os.environ.get("MDC_STATE_DIR", ROOT / ".scratch" / "state"))
LOCKED = ["brief.md", "eval", "autoresearch.sh", "lock.sh", "SETUP.md"]
MODEL_KEYS = ["gas_mcfd", "gas_btu_per_scf", "heat_rate_btu_per_kwh", "parasitic_fraction",
              "claimed_it_mw", "uptime_fraction", "gas_cost_usd_per_mcf", "capex_usd",
              "opex_ex_fuel_usd_per_year", "revenue_usd_per_year", "module_count", "module_capex_usd"]
SECTIONS = {1: "modular", 2: "gas", 3: "swot", 4: "first-principles", 5: "requirements",
            6: "connectivity", 7: "cooling", 8: "water", 9: "hypothesis"}
AXES = {"technical_rigor": 0.30, "economic_realism": 0.25, "regulatory_accuracy": 0.20,
        "actionability": 0.25}
CITE = re.compile(r"\[E:([A-Za-z0-9_\-]+)\]")


def fail(msg, code=1):
    print(f"GATE FAILED: {msg}")
    print("ASI biggest_flaw=" + re.sub(r"\s+", " ", f"gate failed: {msg}")[:400])
    sys.exit(code)


def read(rel):
    p = ROOT / rel
    if not p.exists():
        fail(f"missing file {rel}")
    return p.read_text(encoding="utf-8")


def load_json(rel):
    try:
        return json.loads(read(rel))
    except json.JSONDecodeError as e:
        fail(f"{rel} is not valid JSON: {e}")


def tripwire():
    if SELFTEST:
        return
    def git(*a):
        return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    if git("rev-parse", "-q", "--verify", "refs/tags/locked-baseline").returncode != 0:
        fail("no locked-baseline tag. Run ./lock.sh first", 4)
    d = git("diff", "--name-only", "locked-baseline", "--", *LOCKED)
    u = git("ls-files", "--others", "--exclude-standard", "--", *LOCKED)
    changed = (d.stdout + u.stdout).split()
    if changed:
        fail("locked files changed since lock: " + ", ".join(changed), 4)


def run_cap(c):
    STATE.mkdir(parents=True, exist_ok=True)
    log = STATE / "attempts.log"  # counts every attempt, including gate failures
    n = sum(1 for _ in log.open()) if log.exists() else 0
    if n >= c["max_runs"]:
        print(f"RUN CAP REACHED ({n}/{c['max_runs']}). STOP THE LOOP and report to the owner.")
        sys.exit(3)
    with log.open("a") as f:
        f.write(f"{int(time.time())}\n")
    return n + 1


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def page_has_quote(url, quote):
    q = norm(quote)
    if len(q) < 12 or not url.startswith("http"):
        return False
    key = hashlib.sha256((url + "|" + q).encode()).hexdigest()
    cache = STATE / "verified" / key
    if cache.exists():
        return True
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"})
        raw = urllib.request.urlopen(req, timeout=20).read(4_000_000).decode("utf-8", "ignore")
    except Exception:
        return False
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    ok = q in norm(text)
    if ok:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(url)
    return ok


def check_evidence(ev, c):
    items, verified = {}, set()
    for it in ev.get("sources", []):
        for k in ("id", "url", "quote", "fetched", "claim"):
            if not str(it.get(k, "")).strip():
                fail(f"evidence entry missing '{k}': {json.dumps(it)[:120]}")
        if it["id"] in items:
            fail(f"duplicate evidence id {it['id']}")
        items[it["id"]] = it
        if SELFTEST and os.environ.get("MDC_SKIP_VERIFY") == "1":
            verified.add(it["id"])
        elif page_has_quote(it["url"], it["quote"]):
            verified.add(it["id"])
    if len(items) < c["min_sources"]:
        fail(f"need >= {c['min_sources']} evidence sources, found {len(items)}")
    if len(verified) < c["min_verified_sources"]:
        bad = [i for i in items if i not in verified][:10]
        fail(f"only {len(verified)} sources verified (exact quote found at url by plain HTTP "
             f"fetch); need >= {c['min_verified_sources']}. Unverified: {', '.join(bad)}")
    return items, verified


def split_sections(study):
    found = {}
    parts = re.split(r"^## ", study, flags=re.M)
    for p in parts[1:]:
        m = re.match(r"(\d+)\.", p)
        if m:
            found[int(m.group(1))] = p
    return found


def hard_gates(c, items):
    brief = read("brief.md")
    study = read("deliverables/study.md")
    n = len(study.split())
    if n < c["min_words_study"]:
        fail(f"study.md is only {n} words; need >= {c['min_words_study']}")
    if n > c["max_words_study"]:
        fail(f"study.md is {n} words; cap is {c['max_words_study']}")
    if re.search(r"\b(TODO|TBD|FILL_ME|lorem ipsum)\b", study, re.I):
        fail("study.md contains a placeholder")
    secs = split_sections(study)
    for num, word in SECTIONS.items():
        body = secs.get(num)
        if body is None:
            fail(f"study.md needs a '## {num}. ...' section ({word})")
        if word not in body.split("\n", 1)[0].lower():
            fail(f"study.md section {num} heading must contain '{word}'")
        cites = CITE.findall(body)
        if len(cites) < c["min_citations_per_section"]:
            fail(f"section {num} has {len(cites)} [E:id] citations; need >= "
                 f"{c['min_citations_per_section']}")
    unknown = sorted({i for i in CITE.findall(study) if i not in items})
    if unknown:
        fail("study.md cites unknown evidence ids: " + ", ".join(unknown[:10]))
    swot = secs[3].lower()
    for w in ("strengths", "weaknesses", "opportunities", "threats"):
        if w not in swot:
            fail(f"SWOT section missing '{w}'")
    for label in ("GO IF", "KILL IF"):
        if not re.search(rf"^[\s\-\*]*\**{label}\**\s*:.*\d", study, re.M):
            fail(f"study.md needs a '{label}: ...' line with a numeric threshold")
    return brief, study


def check_model(m, items, verified, c):
    vals, assumptions, unverified = {}, 0, 0
    for k in MODEL_KEYS:
        e = m.get(k)
        if not isinstance(e, dict) or not isinstance(e.get("value"), (int, float)):
            fail(f"site_model.json: '{k}' must be an object with numeric 'value'")
        if e["value"] < 0:
            fail(f"site_model.json: '{k}' is negative")
        vals[k] = float(e["value"])
        if e.get("evidence_id"):
            if e["evidence_id"] not in items:
                fail(f"site_model.json: '{k}' cites unknown evidence_id {e['evidence_id']}")
            if e["evidence_id"] not in verified:
                unverified += 1
        elif e.get("assumption") is True:
            assumptions += 1
        else:
            fail(f"site_model.json: '{k}' needs an evidence_id or \"assumption\": true")
    if vals["gas_mcfd"] < c["min_gas_mcfd"]:
        fail(f"gas_mcfd {vals['gas_mcfd']} below owner minimum {c['min_gas_mcfd']}")
    lo, hi = c["gas_btu_per_scf_range"]
    if not lo <= vals["gas_btu_per_scf"] <= hi:
        fail(f"gas_btu_per_scf {vals['gas_btu_per_scf']} outside plausible {lo}-{hi}")
    lo, hi = c["heat_rate_btu_per_kwh_range"]
    if not lo <= vals["heat_rate_btu_per_kwh"] <= hi:
        fail(f"heat_rate {vals['heat_rate_btu_per_kwh']} outside plausible {lo}-{hi}")
    if not 0 <= vals["parasitic_fraction"] < 0.6 or not 0 < vals["uptime_fraction"] <= 1:
        fail("parasitic_fraction must be in [0,0.6) and uptime_fraction in (0,1]")
    gross_mw = vals["gas_mcfd"] * 1000 * vals["gas_btu_per_scf"] / 24 / vals["heat_rate_btu_per_kwh"] / 1000
    net_mw = gross_mw * (1 - vals["parasitic_fraction"])
    if abs(vals["claimed_it_mw"] - net_mw) > c["power_tolerance"] * net_mw:
        fail(f"claimed_it_mw {vals['claimed_it_mw']} inconsistent with gas energy: "
             f"{vals['gas_mcfd']:.0f} mcf/d x {vals['gas_btu_per_scf']:.0f} Btu/scf / "
             f"{vals['heat_rate_btu_per_kwh']:.0f} Btu/kWh = {gross_mw:.3f} MW gross, "
             f"{net_mw:.3f} MW after parasitic load")
    fuel = vals["gas_mcfd"] * 365 * vals["gas_cost_usd_per_mcf"]
    cash = vals["revenue_usd_per_year"] - vals["opex_ex_fuel_usd_per_year"] - fuel
    stress_cash = vals["revenue_usd_per_year"] * 0.6 - vals["opex_ex_fuel_usd_per_year"] - fuel * 0.7
    pb = round(vals["capex_usd"] / cash, 2) if cash > 0 else None
    spb = round(vals["capex_usd"] / stress_cash, 2) if stress_cash > 0 else None
    it_mwh = net_mw * 8760 * vals["uptime_fraction"]
    n_mod = vals["module_count"]
    if n_mod < 1 or n_mod != int(n_mod):
        fail("site_model.json: module_count must be a whole number >= 1")
    if n_mod * vals["module_capex_usd"] > vals["capex_usd"] * 1.001:
        fail(f"module_count x module_capex_usd ({n_mod * vals['module_capex_usd']:.0f}) exceeds "
             f"site capex_usd ({vals['capex_usd']:.0f}); site capex must include the modules")
    mod_cash = cash / n_mod
    return {"gross_mw": round(gross_mw, 3), "net_it_mw": round(net_mw, 3),
            "it_mwh_per_year": round(it_mwh), "fuel_usd_per_year": round(fuel),
            "annual_cash_flow_usd": round(cash), "payback_years": pb,
            "stress_case": "revenue x0.6 (gas decline + price), fuel x0.7",
            "stress_annual_cash_flow_usd": round(stress_cash), "stress_payback_years": spb,
            "revenue_per_it_mwh": round(vals["revenue_usd_per_year"] / it_mwh, 1) if it_mwh else None,
            "capex_per_it_mw": round(vals["capex_usd"] / net_mw) if net_mw else None,
            "module_capex_usd": round(vals["module_capex_usd"]),
            "module_under_500k": vals["module_capex_usd"] < 500000,
            "module_it_kw": round(net_mw * 1000 / n_mod),
            "module_payback_years_ex_site_costs": round(vals["module_capex_usd"] / mod_cash, 2) if mod_cash > 0 else None,
            "assumptions": assumptions, "unverified_citations": unverified}


def ask_judge(cmd, prompt):
    try:
        r = subprocess.run(cmd, shell=True, input=prompt, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return None
    for m in reversed(list(re.finditer(r"\{[^{}]*\}", r.stdout, re.S))):
        try:
            d = json.loads(m.group(0))
            out = {a: max(0, min(100, int(d[a]))) for a in AXES}
            out["biggest_flaw"] = str(d.get("biggest_flaw", ""))[:400]
            return out
        except (ValueError, KeyError, TypeError):
            continue
    return None


def judge_prompt(brief, c, ev, verified, model, derived, study):
    ev_view = [dict(it, verified=(it["id"] in verified)) for it in ev.get("sources", [])]
    return f"""You are a skeptical reviewer: an oilfield facilities engineer who has also built
and operated off-grid compute sites, and has seen many flare-gas ventures fail.
Score this study 0-100 on four axes. Be harsh. 50 means mediocre.
Deduct heavily for: generic advice, claims not tied to verified evidence, wrong physics or
units, ignoring gas decline curves or gas composition (H2S, NGLs, wet gas), naming the wrong
regulator, vague vendor or lead-time claims, numbers marked as assumptions, any of the
owner's 8 asks answered weakly, and filler.
'verified: false' evidence means the quote was NOT found at the url; treat it as unproven.
BRIEF (owner asks, fixed):
{brief}
HARD LIMITS: {json.dumps(c)}
EVIDENCE: {json.dumps(ev_view)}
SITE MODEL (as submitted): {json.dumps(model)}
DERIVED BY EVALUATOR (physics and cash, base and stress): {json.dumps(derived)}
STUDY:
{study}
Return ONLY one JSON object, no prose, no code fence:
{{"technical_rigor": int, "economic_realism": int, "regulatory_accuracy": int, "actionability": int, "biggest_flaw": "one sentence naming the single weakest point"}}"""


def main():
    c = load_json("eval/constraints.json")
    tripwire()
    run_no = run_cap(c)
    ev = load_json("research/evidence.json")
    items, verified = check_evidence(ev, c)
    brief, study = hard_gates(c, items)
    model = load_json("deliverables/site_model.json")
    derived = check_model(model, items, verified, c)
    cmd = os.environ.get("JUDGE_CMD", "").strip()
    if not cmd:
        fail("JUDGE_CMD not set in eval/judge.env", 4)
    prompt = judge_prompt(brief, c, ev, verified, model, derived, study)
    results = [r for r in (ask_judge(cmd, prompt) for _ in range(c["judge_runs"])) if r]
    if len(results) < (c["judge_runs"] + 1) // 2:
        fail(f"judge returned usable JSON only {len(results)}/{c['judge_runs']} times", 5)
    med = {a: statistics.median(r[a] for r in results) for a in AXES}
    raw = sum(med[a] * w for a, w in AXES.items())
    weak = derived["assumptions"] + derived["unverified_citations"]
    penalty = round(c["assumption_penalty_max"] * weak / len(MODEL_KEYS), 1)
    composite = max(0, round(raw - penalty))
    worst = min(results, key=lambda r: sum(r[a] * w for a, w in AXES.items()))
    rec = {"run": run_no, "ts": int(time.time()), "composite": composite, "raw": round(raw, 1),
           "penalty": penalty, "median": med, "derived": derived, "verified": len(verified),
           "sources": len(items), "flaws": [r["biggest_flaw"] for r in results]}
    hold = os.environ.get("HOLDOUT_CMD", "").strip()
    if hold and run_no % c["holdout_every"] == 0:
        h = ask_judge(hold, prompt)
        if h:
            rec["holdout"] = round(sum(h[a] * w for a, w in AXES.items()), 1)
            rec["holdout_flaw"] = h["biggest_flaw"]
            print(f"METRIC holdout_score={rec['holdout']}")
            print("ASI holdout_flaw=" + re.sub(r"\s+", " ", h["biggest_flaw"]))
    with (STATE / "runs.jsonl").open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"METRIC composite_score={composite}")
    for a in AXES:
        print(f"METRIC {a}={med[a]:.0f}")
    print(f"METRIC verified_sources={len(verified)}/{len(items)}")
    print(f"METRIC net_it_mw={derived['net_it_mw']} payback_years={derived['payback_years']} "
          f"stress_payback_years={derived['stress_payback_years']}")
    print("ASI biggest_flaw=" + re.sub(r"\s+", " ", worst["biggest_flaw"]))
    for r in results:
        if r is not worst:
            print("ASI other_flaw=" + re.sub(r"\s+", " ", r["biggest_flaw"]))
    print(f"ASI run={run_no}/{c['max_runs']} penalty={penalty} "
          f"(assumptions + unverified citations in site_model.json, {weak} of {len(MODEL_KEYS)})")


def selftest():
    words = " ".join(["word"] * 400)
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        for d in ("eval", "deliverables", "research", "state"):
            (t / d).mkdir()
        (t / "brief.md").write_text("Owner brief.")
        c = json.loads((Path(__file__).parent / "constraints.json").read_text())
        (t / "eval/constraints.json").write_text(json.dumps(c))
        heads = {1: "Modular design", 2: "Gas supply", 3: "SWOT", 4: "First-principles retrofit",
                 5: "Requirements", 6: "Connectivity", 7: "Cooling", 8: "Water",
                 9: "Hypothesis test"}
        body = "\n".join(f"## {n}. {h}\n{words} [E:s0] [E:s1]\n" for n, h in heads.items())
        body += "strengths weaknesses opportunities threats\n"
        body = body.replace("## 4.", "strengths weaknesses opportunities threats\n## 4.")
        (t / "deliverables/study.md").write_text(
            body + "GO IF: gas test shows 300 mcf/d for 30 days\nKILL IF: H2S above 100 ppm\n")
        (t / "research/evidence.json").write_text(json.dumps({"sources": [
            {"id": f"s{i}", "url": "https://example.com", "quote": "example domain text",
             "fetched": "2026-11-24", "claim": "x"} for i in range(c["min_sources"])]}))
        model = {k: {"value": 1, "assumption": True} for k in MODEL_KEYS}
        # 300 mcf/d x 1100 Btu/scf / 9000 Btu/kWh = 1.528 MW gross; x0.9 = 1.375 MW net
        model.update({"gas_mcfd": {"value": 300, "evidence_id": "s0"},
                      "gas_btu_per_scf": {"value": 1100, "evidence_id": "s1"},
                      "heat_rate_btu_per_kwh": {"value": 9000, "evidence_id": "s2"},
                      "parasitic_fraction": {"value": 0.1, "evidence_id": "s3"},
                      "claimed_it_mw": {"value": 1.375, "evidence_id": "s4"},
                      "uptime_fraction": {"value": 0.9, "evidence_id": "s5"}})
        (t / "deliverables/site_model.json").write_text(json.dumps(model))
        stub = ("python3 -c \"print('ok {\\\"technical_rigor\\\": 60, \\\"economic_realism\\\": 40, "
                "\\\"regulatory_accuracy\\\": 50, \\\"actionability\\\": 70, "
                "\\\"biggest_flaw\\\": \\\"stub\\\"}')\"")
        env = dict(os.environ, MDC_ROOT=str(t), MDC_STATE_DIR=str(t / "state"),
                   MDC_SELFTEST="1", MDC_SKIP_VERIFY="1", JUDGE_CMD=stub, HOLDOUT_CMD="")
        r = subprocess.run([sys.executable, __file__], env=env, capture_output=True, text=True)
        # 60*.3 + 40*.25 + 50*.2 + 70*.25 = 55.5; 6 of 12 fields are assumptions -> 7.5 -> 48
        ok = r.returncode == 0 and re.search(r"METRIC composite_score=48\b", r.stdout)
        bad = dict(model, claimed_it_mw={"value": 3.0, "evidence_id": "s4"})
        (t / "deliverables/site_model.json").write_text(json.dumps(bad))
        r2 = subprocess.run([sys.executable, __file__], env=env, capture_output=True, text=True)
        ok = ok and r2.returncode != 0 and "inconsistent with gas energy" in r2.stdout
        if ok:
            print("SELFTEST OK")
            return 0
        print("SELFTEST FAILED\n" + r.stdout + r.stderr + "\n---\n" + r2.stdout)
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main()
