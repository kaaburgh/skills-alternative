# Source access — skills.sh ranked input (`SA-001`)

Durable record of how the Cycle 1 ranked input is obtained, what the provider permits, and what
has actually been attempted. `ROADMAP.md` remains authoritative for experiment state.

Status of the acquisition itself: **not yet captured.** The investigation is complete and the exact
path is known; executing it requires a credential this repository's agent environment cannot hold.
See *Acquisition attempt log* and *Operator handoff*.

## The request under contract

```text
GET https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500
```

Verified against the provider's published API reference (`https://www.skills.sh/docs/api`,
retrieved 2026-08-27):

| Contract element | Documented | Verdict |
| --- | --- | --- |
| Base URL `https://skills.sh` | "Base URL https://skills.sh … All endpoints are under `/api/v1/`" | valid |
| `view=all-time` | `"all-time"` (default), `"trending"`, or `"hot"` | valid |
| `page=0` | "Page number, 0-indexed. Default: 0." | valid |
| `per_page=500` | "Results per page, **1-500**. Default: 100." | valid, at the documented maximum |

The contract's request is a well-formed, documented call. Nothing in it needs to change.

Documented response shape: `{"data": [ … ], "pagination": {"page", "perPage", "total", "hasMore"}}`.
Each row carries `id` ("Stable unique identifier. Format: `{source}/{slug}`"), `slug`, `name`,
`source`, `installs`, `sourceType`, `installUrl`, `url`. The single-skill endpoint additionally
returns `hash` (SHA-256 of the skill), which is what the roadmap treats as an *observation version*
rather than durable identity.

## What the provider permits

**robots.txt** (`https://www.skills.sh/robots.txt`, retrieved 2026-08-27):

```text
User-Agent: *
Allow: /
Disallow: /internal/
Disallow: /debug-security/
Disallow: /search
Disallow: /api/
```

`Disallow: /api/` covers the contract endpoint. Read alone it would forbid the request outright.
It does not, because the same site publishes an API reference at `/docs/api` that documents these
endpoints as "the public API", specifies how to authenticate, and states per-credential rate
limits. The directive is the ordinary anti-indexing use of robots.txt — keep crawlers out of JSON
responses — not a prohibition on the programmatic access the provider itself documents and issues
credentials for. Authenticated use through the documented path is sanctioned access. Unauthenticated
or crawling access to `/api/` is not, and this repository does not perform it.

**Terms of use** (`https://www.skills.sh/terms`, retrieved 2026-08-27), verbatim on the two points
the experiment depends on:

- *"Use of the public API is rate-limited per IP. Programmatic abuse, scraping that bypasses the
  rate limit, or use that materially degrades service for others may result in IP-level blocks.
  Reasonable use, including caching results on your own infrastructure, is encouraged and not
  restricted."* — storing the capture is permitted, so the ranked input qualifies for the
  `stored` capture label rather than `metadata_only`.
- *"Skills shown in the directory are the property of their authors and distributed under the
  licenses present in the source repositories. We do not own, host, or relicense skill content."*
  — relevant later to `SA-007`: skills.sh conveys no rights over skill bodies, so any stored skill
  content is governed by its own upstream licence, not by skills.sh's terms.

**Rate limit**: 600 requests/minute per (team, project), reported in `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, `X-RateLimit-Reset`; `429` carries `Retry-After`. One request is required
for this input, so the limit is not a constraint for `SA-001`.

## Authentication: why the agent cannot execute this

The documented and only authentication mechanism is a **Vercel OIDC token**:

- it is minted by Vercel for a specific **team and project** with OIDC Federation enabled;
- it is short-lived (rotated roughly every 12 hours) and request-scoped;
- it is presented as `Authorization: Bearer <token>` or `x-vercel-oidc-token: <token>`;
- skills.sh verifies it against `oidc.vercel.com` and logs `owner_id`, `project_id` and
  `environment` per request.

This is an organisational identity tied to a Vercel account. It is not a key that can be requested
or generated from inside this repository's execution environment, and no substitute exists: the
provider documents no API key, no signup flow, and no unauthenticated tier for these endpoints.

Per `AGENTS.md`, this is an environment-specific acquisition failure escalated as a bounded operator
handoff — **not** a finding that the capability is unavailable to the project. It plainly is
available to the project: the holder of a Vercel account can obtain the token in minutes.

## Acquisition attempt log

All times UTC, 2026-08-27. Every request below is to a robots-permitted path.

| # | Action | Result |
| --- | --- | --- |
| 1 | Inspect execution environment for a Vercel OIDC token, skills.sh credential, or Vercel CLI | None present. `VERCEL_OIDC_TOKEN` unset; no `vercel` binary. The environment's other credentials (AWS, GitHub, session tokens) are unrelated to skills.sh and using them would be credential misuse, so they were not tried. |
| 2 | `GET https://skills.sh/robots.txt` (07:07Z) | `308` → `https://www.skills.sh/robots.txt` → `200`. Disallows `/api/`; see above. |
| 3 | `GET https://www.skills.sh/sitemap.xml` → `sitemap-misc.xml` | `200`. Located `/docs/api` and `/terms`, both robots-permitted. |
| 4 | `GET https://www.skills.sh/docs/api` | `200`. Established the documented request grammar, the Vercel OIDC requirement, rate limits, and error semantics. |
| 5 | `GET https://www.skills.sh/terms` | `200`. Established storage rights and skill-content ownership. |
| 6 | Issue the contract request itself | **Not attempted, deliberately.** Without a token the call cannot succeed — the provider documents `401` for "Missing, invalid, or expired Vercel OIDC token" — so an unauthenticated request would add no information the documentation does not already state, while being exactly the disallowed, unsanctioned use of `/api/`. A `401` was not manufactured to prove a blocker the docs already specify. |

No attempt was made to bypass authentication, the robots directive, rate limits, or the terms.

## Operator handoff

**Blocked line.** `SA-001` acceptance: the raw 500-row response and its provenance.

**Required capability.** A Vercel OIDC token for a Vercel project with OIDC Federation enabled.

**Operator ask.** Run `scripts/capture-skills-sh.sh` (below) once, with that token in the
environment, and commit what it writes.

```bash
# one time, in a Vercel project you control:
#   Vercel dashboard → Project → Settings → OIDC Federation → enable
npm i -g vercel
vercel link                 # link a local directory to that project
vercel env pull             # writes VERCEL_OIDC_TOKEN into .env.local (~12h validity)

# then, from the root of this repository:
set -a; . /path/to/.env.local; set +a
./scripts/capture-skills-sh.sh
```

The script writes `experiments/cycle-1/00-inputs/skills-sh/` and never stores the token or any
request header carrying it.

**The capture is frozen once taken.** It defines the population every later Cycle 1 measurement is
made against, so the script refuses to run when a capture already exists — before spending a
request — and prints the existing capture's retrieval time and hash instead. It captures into a
staging directory and promotes only on success, so a failed or partial run leaves the canonical
path untouched. A second run would otherwise produce a newer snapshot that is internally consistent
and passes every verification below, while silently changing that population. Replacing a capture
deliberately means removing it in its own reviewable commit first, so the replacement appears in
history rather than as an edit in place.

**Verification.** `scripts/verify-skills-sh-capture.py` checks the capture against the acceptance
criteria by recomputing them from the bytes on disk — hash, row count, pagination echo, identifier
uniqueness, install-count ordering, exact request URL — rather than trusting anything the capture
declares about itself. One property is invisible inside a single capture: whether a frozen capture
was later replaced. A re-capture is internally consistent and would pass every other check. So the
verifier also reads git, which does record it — a committed capture must still match what was
committed — and reports an uncommitted capture as the ordinary first-capture state rather than
failing it. A capture that passes has the provenance `SA-001` requires; one that fails
names the missing property. Run it after the capture, and again in review:

```bash
python3 scripts/verify-skills-sh-capture.py
```

**Independent progress.** Everything in this document, plus both scripts, was completed without the
credential. The blocked line is the capture alone.

## Open questions for later items

- The leaderboard row shape documented at `/docs/api` carries no duplicate/alias flag. The roadmap's
  identity rules mention "official duplicate flags" as a permitted grouping signal; whether such a
  signal exists in the actual payload is unresolved and must be settled from the real capture, not
  assumed. `SA-005` owns it.
- `total` in the documented example is 8420, so the 500-row capture is page 0 of a much larger
  leaderboard. That is what the contract intends — the candidate universe is deliberately bounded at
  500 — but it means "top 100" is emphatically a slice of one catalog's ranking, as the roadmap's
  falsifiable-outcome section already states.
