#!/usr/bin/env python3
"""Capture and validate the fixed Cycle 1 skills.sh leaderboard request."""

from __future__ import annotations

import argparse
import datetime as dt
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500"
TOOL_VERSION = "sa001-capture-v1"
REQUIRED_FIELDS = (
    "id",
    "slug",
    "name",
    "source",
    "installs",
    "sourceType",
    "installUrl",
    "url",
)
RELEVANT_RESPONSE_HEADERS = {
    "age",
    "cache-control",
    "content-length",
    "content-type",
    "date",
    "etag",
    "last-modified",
    "retry-after",
    "x-ratelimit-limit",
    "x-ratelimit-remaining",
    "x-ratelimit-reset",
    "x-vercel-cache",
    "x-vercel-id",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relevant_headers(headers: object) -> dict[str, str]:
    pairs = getattr(headers, "items")()
    return {
        str(key).lower(): str(value)
        for key, value in pairs
        if str(key).lower() in RELEVANT_RESPONSE_HEADERS
    }


def validate_payload(body: bytes) -> dict[str, object]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"response is not UTF-8 JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("top-level response must be a JSON object")
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise ValueError("top-level 'data' must be a JSON array")
    if len(rows) != 500:
        raise ValueError(f"expected exactly 500 ranked rows, got {len(rows)}")

    ids: list[str] = []
    installs: list[int] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"row {index} is not a JSON object")
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            raise ValueError(f"row {index} missing documented field(s): {', '.join(missing)}")

        row_id = row["id"]
        if not isinstance(row_id, str) or not row_id.strip():
            raise ValueError(f"row {index} has invalid id")
        install_count = row["installs"]
        if isinstance(install_count, bool) or not isinstance(install_count, int) or install_count < 0:
            raise ValueError(f"row {index} has invalid installs value")

        for field in ("slug", "name", "source", "sourceType", "installUrl", "url"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise ValueError(f"row {index} has invalid {field}")

        ids.append(row_id)
        installs.append(install_count)

    duplicate_ids = sorted(row_id for row_id, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        preview = ", ".join(duplicate_ids[:5])
        raise ValueError(f"duplicate skill id(s): {preview}")

    descending = all(a >= b for a, b in zip(installs, installs[1:]))
    if not descending:
        for pos, (a, b) in enumerate(zip(installs, installs[1:]), start=1):
            if a < b:
                raise ValueError(
                    f"all-time leaderboard is not monotonic by installs at positions {pos}/{pos + 1}: {a} < {b}"
                )

    return {
        "schema": "documented-v1-skill-fields",
        "row_count": len(rows),
        "unique_skill_ids": len(set(ids)),
        "derived_rank_first": 1,
        "derived_rank_last": len(rows),
        "derived_rank_unique": True,
        "installs_non_increasing": True,
        "required_fields": list(REQUIRED_FIELDS),
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ensure_absent(paths: list[Path]) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise RuntimeError("refusing to overwrite immutable capture file(s): " + ", ".join(existing))


def capture(output_dir: Path) -> int:
    token = os.environ.get("VERCEL_OIDC_TOKEN")
    if not token:
        raise RuntimeError("VERCEL_OIDC_TOKEN is not set; obtain a permitted Vercel project OIDC token first")

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "response.json"
    metadata_path = output_dir / "request-response-metadata.json"
    validation_path = output_dir / "validation.json"
    ensure_absent([raw_path, metadata_path, validation_path])

    request = urllib.request.Request(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "skills-alternative-cycle-1/sa-001",
        },
        method="GET",
    )
    started_at = utc_now()

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            status = response.status
            response_headers = relevant_headers(response.headers)
    except urllib.error.HTTPError as exc:
        failure = {
            "tool_version": TOOL_VERSION,
            "request_url": ENDPOINT,
            "request_parameters": dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(ENDPOINT).query)),
            "auth_method": "Vercel OIDC bearer (token omitted)",
            "started_at_utc": started_at,
            "completed_at_utc": utc_now(),
            "http_status": exc.code,
            "response_headers": relevant_headers(exc.headers),
            "result": "http_error",
        }
        write_json(output_dir / f"acquisition-failure-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json", failure)
        raise RuntimeError(f"skills.sh request failed with HTTP {exc.code}; bearer token was not logged") from exc

    completed_at = utc_now()
    body_sha256 = sha256_bytes(body)
    try:
        validation = validate_payload(body)
    except ValueError as exc:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        failed_body = output_dir / f"validation-failure-{stamp}.bin"
        failed_meta = output_dir / f"validation-failure-{stamp}.json"
        failed_body.write_bytes(body)
        write_json(
            failed_meta,
            {
                "tool_version": TOOL_VERSION,
                "request_url": ENDPOINT,
                "request_parameters": dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(ENDPOINT).query)),
                "auth_method": "Vercel OIDC bearer (token omitted)",
                "started_at_utc": started_at,
                "retrieved_at_utc": completed_at,
                "http_status": status,
                "response_headers": response_headers,
                "response_body_bytes": len(body),
                "response_body_sha256": body_sha256,
                "result": "validation_error",
                "validation_error": str(exc),
                "failed_response_path": failed_body.name,
            },
        )
        raise RuntimeError(
            f"skills.sh returned a response that failed SA-001 validation; preserved {failed_body.name}: {exc}"
        ) from exc

    metadata = {
        "tool_version": TOOL_VERSION,
        "request_url": ENDPOINT,
        "request_parameters": dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(ENDPOINT).query)),
        "auth_method": "Vercel OIDC bearer (token omitted)",
        "started_at_utc": started_at,
        "retrieved_at_utc": completed_at,
        "http_status": status,
        "response_headers": response_headers,
        "response_body_bytes": len(body),
        "response_body_sha256": body_sha256,
    }

    raw_path.write_bytes(body)
    write_json(metadata_path, metadata)
    write_json(validation_path, validation | {"response_body_sha256": body_sha256})
    print(json.dumps({"output_dir": str(output_dir), "sha256": body_sha256, **validation}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/cycle-1/00-inputs/skills-sh"),
        help="directory for the immutable successful capture",
    )
    parser.add_argument(
        "--validate-body",
        type=Path,
        help="validate existing raw response bytes without performing a network request",
    )
    args = parser.parse_args()

    try:
        if args.validate_body:
            body = args.validate_body.read_bytes()
            print(json.dumps(validate_payload(body) | {"response_body_sha256": sha256_bytes(body)}, sort_keys=True))
            return 0
        return capture(args.output_dir)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
