#!/usr/bin/env bash
# Watchdog for Gengar's own automations.
# Prints a short alert only when something is wrong; prints NO_REPLY when healthy.
# Exit 0 = healthy (silent), exit 1 = problem (message delivered).

set -uo pipefail

JOBS=(
  "ac9e7ada-134e-4b83-8161-6ec18ca312b9|English reminder"
  "88810bfe-4ecc-4a99-99e6-541ba5d2cc1e|BBC News drill"
)

PROBLEMS=()

for entry in "${JOBS[@]}"; do
  id="${entry%%|*}"
  name="${entry##*|}"

  raw="$(openclaw automations get "$id" 2>/dev/null)" || {
    PROBLEMS+=("$name: could not read job state (id $id)")
    continue
  }

  state="$(printf '%s' "$raw" | python3 -c '
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("PARSE_ERROR"); raise SystemExit
s=d.get("state") or {}
print("|".join([
    "enabled="+str(d.get("enabled")),
    "status="+str(s.get("lastRunStatus")),
    "delivery="+str(s.get("lastDeliveryStatus")),
    "errors="+str(s.get("consecutiveErrors")),
    "autoDisabled="+str((s.get("autoDisabled") or {}).get("reason","none")),
    "lastRunAtMs="+str(s.get("lastRunAtMs")),
    "lastError="+((s.get("lastError") or "none")[:120]),
]))
' 2>/dev/null)" || state=""

  if [[ "$state" == "PARSE_ERROR" || -z "$state" ]]; then
    PROBLEMS+=("$name: unparseable state")
    continue
  fi

  get_field() { printf '%s' "$state" | cut -d'|' -f"$1"; }

  f1="$(get_field 1)"; f2="$(get_field 2)"; f3="$(get_field 3)"
  f4="$(get_field 4)"; f5="$(get_field 5)"; f7="$(get_field 7)"

  enabled="${f1#enabled=}"
  status="${f2#status=}"
  delivery="${f3#delivery=}"
  errors="${f4#errors=}"
  autoDisabled="${f5#autoDisabled=}"
  last_error="${f7#lastError=}"

  if [[ "$enabled" != "True" ]]; then
    PROBLEMS+=("$name: DISABLED (reason=${autoDisabled}, consecutiveErrors=${errors})")
  fi
  if [[ "$errors" != "0" && "$errors" != "None" ]]; then
    PROBLEMS+=("$name: ${errors} consecutive failures (lastStatus=${status}, delivery=${delivery})")
  fi
  if [[ "$status" == "error" ]]; then
    PROBLEMS+=("$name: last run failed — ${last_error}")
  fi
  if [[ "$delivery" == "not-delivered" && "$status" == "ok" ]]; then
    PROBLEMS+=("$name: run ok but delivery not-delivered")
  fi
done

if [[ ${#PROBLEMS[@]} -eq 0 ]]; then
  echo "NO_REPLY"
  exit 0
fi

echo "⚠️ Gengar automation health check"
for p in "${PROBLEMS[@]}"; do
  echo "• $p"
done
echo ""
echo "Inspect: openclaw automations list --all"
echo "Recover: openclaw automations enable <jobId>"
exit 1
