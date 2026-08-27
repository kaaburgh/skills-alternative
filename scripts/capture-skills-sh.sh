#!/usr/bin/env bash
# SA-001 — capture the frozen skills.sh ranked input with full provenance.
#
# Requires VERCEL_OIDC_TOKEN in the environment (see docs/source-access.md).
# Writes experiments/cycle-1/00-inputs/skills-sh/. Never writes the token anywhere.
#
# Redirects are deliberately NOT followed: curl strips the Authorization header on a
# cross-host redirect, which would silently yield a 401 body captured as if it were data.
# A redirect is reported so the operator can decide, rather than papered over.

set -euo pipefail

URL='https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500'
OUT_DIR="$(git rev-parse --show-toplevel)/experiments/cycle-1/00-inputs/skills-sh"

if [[ -z "${VERCEL_OIDC_TOKEN:-}" ]]; then
  echo "VERCEL_OIDC_TOKEN is not set. See docs/source-access.md for how to obtain one." >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
cd "$OUT_DIR"

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
  echo "No capture written." >&2
  rm -f response.json
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

echo "Captured $byte_len bytes, sha256 $sha256"
echo "Wrote: $OUT_DIR/{response.json,response-headers.txt,request.json}"
echo "Now run: python3 scripts/verify-skills-sh-capture.py"
