# Cycle 1 source access

This document records acquisition procedure and environment-specific blockers. `ROADMAP.md` remains authoritative for planning state and acceptance criteria.

## skills.sh ranked input (SA-001)

Cycle 1 is bound to exactly this authenticated request:

```text
GET https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500
```

No rendered leaderboard, search result, other catalog, or hand-built list is an equivalent fallback.

### Authentication facts

The skills.sh API reference documents Vercel project OIDC as the authentication mechanism for `/api/v1/skills`. The bearer token is project-scoped, short-lived, and must not be committed. The documented local-development path is an authenticated Vercel CLI linked to a project; Vercel also exposes a short-lived development OIDC token through current CLI/SDK tooling.

References:

- https://www.skills.sh/docs/api
- https://github.com/vercel/vercel-py#readme

The unattended GitHub runtime currently has neither a Vercel project identity nor Vercel credentials, so it cannot mint that token itself. The generic execution sandbox also currently fails outbound DNS. These are environment-specific acquisition blockers, not evidence that skills.sh is unavailable and not a Rule 0 result.

### Operator capture helper

`scripts/capture_skills_sh.py` performs only the fixed request above. It reads `VERCEL_OIDC_TOKEN` from the process environment, never accepts the token as a command-line argument, never writes it, and refuses to overwrite a successful capture.

On a machine already authenticated to Vercel, first verify the intended account/project and use a current Vercel CLI. Current Vercel tooling supports obtaining a short-lived development token with `vc project token <project-name>`. With CLI 53.3.0 or newer, a bounded invocation is:

```bash
vc whoami
vc --version
VERCEL_OIDC_TOKEN="$(vc project token <project-name>)" \
  python3 scripts/capture_skills_sh.py
```

If `vc project token` is unavailable in the installed CLI, use the skills.sh-documented `vercel link` + `vercel env pull` path instead, taking care not to commit `.env.local` or any other pulled environment value.

A successful run writes:

- `experiments/cycle-1/00-inputs/skills-sh/response.json` — unmodified response bytes;
- `request-response-metadata.json` — exact request parameters, UTC retrieval time, HTTP status, a bounded set of provenance/cache/rate-limit response headers, response byte count, and SHA-256; authentication is recorded only as `Vercel OIDC bearer (token omitted)`;
- `validation.json` — the documented row-shape check, exact 500-row count, unique skill IDs, derived rank range/uniqueness, non-increasing all-time install counts, and the same response SHA-256.

The helper validates the public API's documented `V1Skill` fields (`id`, `slug`, `name`, `source`, `installs`, `sourceType`, `installUrl`, `url`). Because the API defines this endpoint as the all-time leaderboard rather than exposing a separate `rank` field, rank is the response position; the helper checks positions 1–500 are complete and unique and that `installs` is non-increasing, allowing ties.

If the request returns an HTTP error, the helper stores a token-free timestamped acquisition-failure record. If an HTTP-success response fails schema/count/order validation, it preserves the exact failed response bytes plus token-free metadata and the validation error under timestamped `validation-failure-*` files. A failed capture is evidence to inspect; it is not silently replaced with another population.

### Current handoff

Issue #4 is the bounded operator handoff for SA-001. Until a permitted authenticated capture exists, downstream subject-specific work remains blocked and the public rendered leaderboard must not be used as a substitute.
