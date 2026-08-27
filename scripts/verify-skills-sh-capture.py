#!/usr/bin/env python3
"""SA-001 - verify the skills.sh capture carries the provenance the roadmap requires.

Every check recomputes a property from the bytes on disk. Nothing is accepted because the
capture declares it: the recorded SHA-256 is checked by re-hashing the file, the row count by
counting rows, the request by string-comparing it to the contract URL. A capture cannot pass
this by asserting that it is valid.

Exit 0 = every required property holds. Exit 1 = at least one does not; each failure names the
property that is missing rather than only that something is wrong.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTRACT_URL = "https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500"
EXPECTED_ROWS = 500
REQUIRED_ROW_FIELDS = ("id", "slug", "name", "source", "installs", "sourceType", "url")

results: list[tuple[bool, str, str]] = []


def check(ok: bool, name: str, detail: str = "") -> bool:
    results.append((ok, name, detail))
    return ok


def main() -> int:
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, check=True).stdout.strip())
    d = root / "experiments/cycle-1/00-inputs/skills-sh"

    body_p, headers_p, req_p = d / "response.json", d / "response-headers.txt", d / "request.json"
    for p in (body_p, headers_p, req_p):
        if not check(p.is_file(), f"present: {p.relative_to(root)}"):
            return report()

    raw = body_p.read_bytes()
    meta = json.loads(req_p.read_text(encoding="utf-8"))

    # --- provenance recomputed from the bytes, not read off the manifest -------------------
    actual_sha = hashlib.sha256(raw).hexdigest()
    check(meta.get("response_sha256") == actual_sha,
          "recorded SHA-256 matches the actual response bytes",
          f"recorded={meta.get('response_sha256')} actual={actual_sha}")
    check(meta.get("response_bytes") == len(raw),
          "recorded byte length matches the actual file", f"file is {len(raw)} bytes")
    check(meta.get("url") == CONTRACT_URL,
          "request URL is byte-identical to the contract URL",
          f"recorded={meta.get('url')!r}")
    check(meta.get("http_status") == 200, "response status was 200",
          f"recorded={meta.get('http_status')}")
    check(meta.get("redirects_followed") is False,
          "no redirect was followed (a cross-host redirect strips Authorization)")
    check(meta.get("capture_label") == "stored",
          "capture is labelled 'stored', which the provider's terms permit")

    for field in ("requested_at_utc", "completed_at_utc"):
        val = meta.get(field)
        ok = False
        if isinstance(val, str):
            try:
                ts = datetime.strptime(val, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                ok = ts <= datetime.now(timezone.utc)
            except ValueError:
                ok = False
        check(ok, f"{field} is a UTC timestamp that is not in the future", f"value={val!r}")

    # --- no credential anywhere in the committed capture -----------------------------------
    header_text = headers_p.read_text(encoding="utf-8", errors="replace")
    check(not re.search(r"(?i)authorization:|x-vercel-oidc-token:", header_text),
          "no credential header was stored")
    check("<redacted>" in json.dumps(meta.get("request_headers_sent", [])),
          "the recorded request headers keep the token redacted")

    # --- the payload is the population the contract claims to study ------------------------
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        check(False, "response body is valid JSON", str(e))
        return report()
    check(True, "response body is valid JSON")

    rows = doc.get("data")
    if not check(isinstance(rows, list), "response has a 'data' array"):
        return report()
    check(len(rows) == EXPECTED_ROWS, f"'data' holds exactly {EXPECTED_ROWS} ranked rows",
          f"found {len(rows)}")

    pag = doc.get("pagination", {})
    check(pag.get("page") == 0, "pagination echoes page 0", f"got {pag.get('page')}")
    check(pag.get("perPage") == EXPECTED_ROWS, f"pagination echoes perPage {EXPECTED_ROWS}",
          f"got {pag.get('perPage')}")

    missing = {f for r in rows if isinstance(r, dict) for f in REQUIRED_ROW_FIELDS if f not in r}
    check(not missing, "every row carries the documented identity fields",
          f"missing across rows: {sorted(missing)}" if missing else "")

    ids = [r.get("id") for r in rows if isinstance(r, dict)]
    check(all(isinstance(i, str) and i for i in ids), "every row has a non-empty string id")
    dupes = {i for i in ids if ids.count(i) > 1}
    check(not dupes, "row ids are unique across the capture",
          f"{len(dupes)} duplicated id(s), e.g. {sorted(dupes)[:3]}" if dupes else "")

    installs = [r.get("installs") for r in rows if isinstance(r, dict)]
    check(all(isinstance(v, int) for v in installs), "every row has an integer install count")
    if all(isinstance(v, int) for v in installs):
        breaks = [i for i in range(1, len(installs)) if installs[i] > installs[i - 1]]
        check(not breaks,
              "install counts are non-increasing, i.e. rank order is monotonic",
              f"{len(breaks)} inversion(s), first at row {breaks[0]}" if breaks else "")

    return report()


def report() -> int:
    failed = [r for r in results if not r[0]]
    for ok, name, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"\n          {detail}" if detail and not ok else ""))
    print()
    if failed:
        print(f"{len(failed)} of {len(results)} checks FAILED. "
              "The capture does not yet carry the provenance SA-001 requires.")
        return 1
    print(f"All {len(results)} checks passed. The capture carries the provenance SA-001 requires.")
    print("Note: this verifies the capture's internal properties. It cannot attest that the bytes "
          "came from skills.sh - that rests on the operator having run the capture script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
