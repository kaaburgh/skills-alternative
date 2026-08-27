# Cycle 1 source access

This document records acquisition procedure and environment-specific blockers. `ROADMAP.md` remains authoritative for planning state and acceptance criteria.

## skills.sh ranked input (SA-001)

Cycle 1 is bound to exactly this authenticated request:

```text
GET https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500
```

No rendered leaderboard, search result, other catalog, or hand-built list is an equivalent fallback.

### Authentication and provider-contract facts

The skills.sh API reference documents Vercel project OIDC as the authentication mechanism for `/api/v1/skills`. The bearer token is project-scoped, short-lived, and must not be committed. The documented local-development path is an authenticated Vercel CLI linked to a project; Vercel also exposes a short-lived development OIDC token through current CLI/SDK tooling.

The same API reference documents `view=all-time`, zero-indexed `page`, and `per_page` from 1 through 500. Therefore the Cycle 1 request uses the documented all-time view, page 0, and the documented maximum page size rather than an arbitrary row cap. The example response also makes clear that page 0 can be a slice of a larger leaderboard.

skills.sh's current terms describe the API as public, rate-limited programmatic access and explicitly permit reasonable caching on the caller's own infrastructure. That supports storing this bounded leaderboard response as the Cycle 1 raw input. Those terms also say skill content remains governed by the licenses in the source repositories; this capture helper stores only the ranked-list response and does not infer rights over downstream skill bodies.

A 2026-08-27 acquisition handoff on PR #7 also records that `robots.txt` contains `Disallow: /api/`. This repository does not use that as permission to crawl or to bypass authentication. The bounded SA-001 action is one authenticated request to the exact endpoint that the same provider expressly documents for programmatic use, subject to its published authentication and rate-limit rules. If the provider's API documentation, terms, or robots policy changes before capture, stop and reconcile the access decision rather than proceeding on stale assumptions.

References:

- https://www.skills.sh/docs/api
- https://www.skills.sh/terms
- https://github.com/vercel/vercel-py#readme
- https://www.skills.sh/vercel-labs/agent-browser/protected-vercel-deployments

The unattended GitHub runtime currently has neither a Vercel project identity nor Vercel credentials, so it cannot mint that token itself. The generic execution sandbox also currently fails outbound DNS. These are environment-specific acquisition blockers, not evidence that skills.sh is unavailable and not a Rule 0 result.

### Operator capture helper

`scripts/capture_skills_sh.py` performs only the fixed request above. It reads `VERCEL_OIDC_TOKEN` from the process environment, never accepts the token as a command-line argument, never writes it, and refuses to overwrite a successful capture.

On a machine already authenticated to Vercel, first verify the intended account/project. The skills.sh-documented local path is `vercel link` followed by `vercel env pull`; current Vercel SDK documentation also exposes `vc project token <project-name>` as a way to obtain a short-lived development OIDC token. Make the token available to the helper as `VERCEL_OIDC_TOKEN` using a secret-safe local mechanism, then run:

```bash
python3 scripts/capture_skills_sh.py
```

Do not paste the token into a command argument, commit `.env.local`, or print the token into logs. If using `vc project token`, use Vercel CLI 53.3.0 or newer before capturing its stdout: Vercel-maintained guidance records that CLI 50.25.0 through 53.2.x could emit this credential on stderr. Upgrade instead of trying to recover a token from stderr.

A successful run writes:

- `experiments/cycle-1/00-inputs/skills-sh/response.json` — unmodified response bytes;
- `request-response-metadata.json` — exact request parameters, UTC retrieval time, HTTP status, a bounded set of provenance/cache/rate-limit response headers, response byte count, and SHA-256; authentication is recorded only as `Vercel OIDC bearer (token omitted)`;
- `validation.json` — the documented row-shape check, exact 500-row count, unique skill IDs, derived rank range/uniqueness, non-increasing all-time install counts, and the same response SHA-256.

The helper validates the public API's documented `V1Skill` fields (`id`, `slug`, `name`, `source`, `installs`, `sourceType`, `installUrl`, `url`). Because the API defines this endpoint as the all-time leaderboard rather than exposing a separate `rank` field, rank is the response position; the helper checks positions 1–500 are complete and unique and that `installs` is non-increasing, allowing ties.

If the request returns an HTTP error, the helper stores a token-free timestamped acquisition-failure record. If an HTTP-success response fails schema/count/order validation, it preserves the exact failed response bytes plus token-free metadata and the validation error under timestamped `validation-failure-*` files. A failed capture is evidence to inspect; it is not silently replaced with another population.

### Frozen-capture integrity

File-existence checks prevent an ordinary second capture from overwriting files in the same checkout, but they do not by themselves detect a hand edit or a replacement performed after removing/restoring the files. For that reason, validating an existing response also checks git state:

```bash
python3 scripts/capture_skills_sh.py \
  --validate-body experiments/cycle-1/00-inputs/skills-sh/response.json
```

For the canonical response path, the validator distinguishes the expected first-capture state (`untracked_first_capture`) from a committed unchanged capture (`tracked_unchanged_from_head`). If the response is already tracked and its bytes differ from `HEAD`, validation fails rather than accepting a newer internally self-consistent population. Run this check after the initial capture and again after committing the frozen input. A deliberate replacement must therefore appear as an explicit reviewable repository change instead of being silently normalized by fresh metadata and hashes.

This git check complements, rather than replaces, the SHA-256 and payload checks. Synthetic fixtures or files outside the repository are reported as such and remain useful for parser tests, but they do not establish frozen-input integrity.

### Current handoff

Issue #4 is the bounded operator handoff for SA-001. Until a permitted authenticated capture exists, downstream subject-specific work remains blocked and the public rendered leaderboard must not be used as a substitute.
