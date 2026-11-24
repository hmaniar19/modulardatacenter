#!/usr/bin/env bash
# Frozen benchmark entrypoint. OFF-LIMITS to the research agent.
set -euo pipefail
cd "$(dirname "$0")"
unset MDC_SELFTEST MDC_SKIP_VERIFY MDC_ROOT MDC_STATE_DIR ANTHROPIC_API_KEY OPENAI_API_KEY CODEX_API_KEY
set -a; source eval/judge.env; set +a
exec python3 eval/evaluate.py
