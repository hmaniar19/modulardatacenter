#!/usr/bin/env bash
# Freezes the brief, constraints and evaluator. Run once before the loop starts.
set -euo pipefail
cd "$(dirname "$0")"
python3 eval/evaluate.py --selftest
git add brief.md eval autoresearch.sh lock.sh SETUP.md .gitignore
git commit -qm "Lock brief, constraints and evaluator" || true
git tag -f locked-baseline >/dev/null
echo "LOCKED at $(git rev-parse --short HEAD). Loop may start."
