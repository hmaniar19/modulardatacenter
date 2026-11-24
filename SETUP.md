# Autoresearch setup: flare-gas modular data center

Rules for the whole job:
- Research is read-only web browsing. Do not contact anyone, sign up, or spend money.
- Never edit brief.md, eval/, autoresearch.sh, lock.sh or SETUP.md after locking.
- Local git repo only. Do not create a GitHub repo or push.

1. `python3 eval/evaluate.py --selftest` must print `SELFTEST OK`.
2. `./lock.sh` must print `LOCKED`.
3. Start `/autoresearch` (or loop by hand) with:
- Intent: Deep, phased, evidence-backed study answering all 8 owner asks in brief.md for a
  drop-and-go modular data center on stranded or flared gas, ending in a GO/KILL decision.
- Benchmark command: `bash autoresearch.sh`
- Primary metric: `composite_score`, points, higher is better
- Files in scope: `deliverables/`, `research/`
- Off-limits: `brief.md`, `eval/`, `autoresearch.sh`, `lock.sh`, `SETUP.md`
- Max iterations: 30 (the evaluator enforces the run cap)
- Constraints: every claim in deliverables/study.md cites `[E:id]` from research/evidence.json;
  every evidence quote is exact text from its url (plain HTTP fetch must find it); every number
  in deliverables/site_model.json cites an evidence id or is marked `"assumption": true`.
  Each iteration, fix the `ASI biggest_flaw` from the last run.
4. Stop on `RUN CAP REACHED`, the iteration cap, or 5 runs without improvement.

Run history: `.scratch/state/runs.jsonl`.
