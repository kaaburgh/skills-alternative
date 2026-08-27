#!/usr/bin/env bash
# SA-001 — capture the frozen skills.sh ranked input with full provenance.
#
# Requires VERCEL_OIDC_TOKEN in the environment (see docs/source-access.md).
# Writes experiments/cycle-1/00-inputs/skills-sh/. Never writes the token anywhere.
#
# The capture is a frozen input: once taken, it defines the population Cycle 1 studies.
# So this script refuses to run at all when a capture already exists, before spending a
# request, and captures into a staging directory that is promoted only on success. A second
# run must never replace a frozen leaderboard with a newer snapshot: the replacement would be
# internally consistent and would pass verification, while silently changing the population
# every later measurement is taken against.
#
# Redirects are deliberately NOT followed: curl strips the Authorization header on a
# cross-host redirect, which would silently yield a 401 body captured as if it were data.
# A redirect is reported so the operator can decide, rather than papered over.

set -euo pipefail

URL='https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500'
OUT_DIR="$(git rev-parse --show-toplevel)/experiments/cycle-1/00-inputs/skills-sh"

# Fail closed before spending a request: never overwrite a frozen capture.
existing=()
for f in response.json response-headers.txt request.json; do
  [[ -e "$OUT_DIR/$f" ]] && existing+=("$f")
done
if (( ${#existing[@]} > 0 )); then
  {
    echo "A capture already exists at:"
    echo "  $OUT_DIR"
    echo "Present: ${existing[*]}"
    if [[ -f "$OUT_DIR/request.json" ]]; then
      echo "Existing capture:"
      python3 - "$OUT_DIR/request.json" <<'PYEOF' || true
import json,sys
m=json.load(open(sys.argv[1]))
print(f"  retrieved  {m.get('requested_at_utc')}")
print(f"  sha256     {m.get('response_sha256')}")
print(f"  bytes      {m.get('response_bytes')}")
PYEOF
    fi
    echo
    echo "This input is frozen once captured: it defines the population Cycle 1 measures."
    echo "Re-capturing would produce a newer snapshot that is internally consistent and passes"
    echo "verification, while silently changing that population. Refusing."
    echo
    echo "To replace it deliberately, remove those files in their own reviewable commit first,"
    echo "so the replacement is visible in history rather than appearing as an edit in place."
  } >&2
  exit 4
fi

if [[ -z "${VERCEL_OIDC_TOKEN:-}" ]]; then
  echo "VERCEL_OIDC_TOKEN is not set. See docs/source-access.md for how to obtain one." >&2
  exit 2
fi

# Capture into staging so a failed or partial run never leaves anything at the canonical path.
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT
cd "$STAGING"

requested_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
http_code="$(
  curl -sS --max-time 120 \
    --proto '=https' --tlsv1.2 \
    -H "Authorization: Bearer ${VERCEL_OIDC_TOKEN}" \
    -H 'Accept: application/json' \
    -D response-headers.txt \
    -o response.json \
    -w '%{http_code}' \
    "$URL"
)"
completed_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# The token can only ever appear in a request header, which curl does not write to -D output.
# Belt and braces: refuse to keep a headers file that contains anything token-shaped.
if grep -qiE 'authorization:|x-vercel-oidc-token:' response-headers.txt; then
  echo "response-headers.txt unexpectedly contains a credential header; removing capture." >&2
  rm -f response.json response-headers.txt
  exit 3
fi

if [[ "$http_code" != "200" ]]; then
  echo "Request returned HTTP $http_code (expected 200)." >&2
  echo "--- response headers ---" >&2; cat response-headers.txt >&2
  echo "--- body (first 500 bytes) ---" >&2; head -c 500 response.json >&2; echo >&2
  case "$http_code" in
    401) echo "401 = missing/invalid/expired Vercel OIDC token. Re-run 'vercel env pull'." >&2 ;;
    30*) echo "Redirect: Authorization is not forwarded across hosts. Do NOT use --location-trusted; report this." >&2 ;;
    429) echo "429 = rate limited; honour the Retry-After header above." >&2 ;;
  esac
  echo "No capture written; the canonical path was not touched." >&2
  exit 1
fi

sha256="$(sha256sum response.json | cut -d' ' -f1)"
byte_len="$(wc -c < response.json | tr -d ' ')"

cat > request.json <<JSON
{
  "url": "$URL",
  "method": "GET",
  "query_parameters": { "view": "all-time", "page": "0", "per_page": "500" },
  "request_headers_sent": ["Authorization: Bearer <redacted>", "Accept: application/json"],
  "redirects_followed": false,
  "requested_at_utc": "$requested_at",
  "completed_at_utc": "$completed_at",
  "http_status": $http_code,
  "response_sha256": "$sha256",
  "response_bytes": $byte_len,
  "capture_label": "stored",
  "capture_tool": "scripts/capture-skills-sh.sh",
  "curl_version": "$(curl --version | head -1)"
}
JSON

# Promote atomically-ish: the guard above proved the canonical path was empty, and nothing
# below this line can fail in a way that leaves a partial capture there.
mkdir -p "$OUT_DIR"
mv response.json response-headers.txt request.json "$OUT_DIR/"

echo "Captured $byte_len bytes, sha256 $sha256"
echo "Wrote: $OUT_DIR/{response.json,response-headers.txt,request.json}"
echo "Now run: python3 scripts/verify-skills-sh-capture.py"
echo "Then commit the capture: it is frozen from that point on."
