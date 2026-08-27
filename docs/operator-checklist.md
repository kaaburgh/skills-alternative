# Operator checklist

Derived projection of the human actions that are **currently** actionable. [`ROADMAP.md`](../ROADMAP.md)
is authoritative for all planning state — status, dependencies, readiness, sequencing, acceptance. If
this file disagrees with it, the roadmap wins.

Only current, ready human work appears here. Completed, blocked and cloud-executable items do not,
however important they are. Any PR that changes what the operator must do, or how, reconciles this
file in the same change.

## 1. Secure an independent evaluator — `SA-000`

Ready now, and it gates the binding output freeze. An evaluator who turns out not to exist is cheap
to discover today and terminal to discover after the pipeline has run: without one, Keep and Pivot
are both ineligible and Rule 0 fires.

**You cannot be the evaluator.** The contract excludes anyone who built or tuned the pipeline,
schemas, rubrics, source mappings, cards, baselines or thresholds. The task is to find someone else
and keep the handoff clean.

Procedure and the form: [`docs/evaluator-handoff.md`](./evaluator-handoff.md) and
[`experiments/cycle-1/04-audit/evaluator-declaration-template.md`](../experiments/cycle-1/04-audit/evaluator-declaration-template.md).
Disclose the workload as the three audit phases **plus** the post-audit `SA-013` re-derivation
sample. Get the acknowledgement before any output is exposed.

## 2. Capture the ranked input — `SA-001`

Ready now in the sense that only a human can do it: skills.sh authenticates with a Vercel OIDC token
bound to a Vercel team and project, and the provider documents no API key, signup or unauthenticated
tier. The token is an organisational identity no agent sandbox can mint.

Obtaining the token, once, in a Vercel project you control — Settings → OIDC Federation → enable:

```bash
npm i -g vercel && vercel link && vercel env pull   # writes VERCEL_OIDC_TOKEN to .env.local
```

The request itself is the one fixed in the experiment contract:
`GET https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500`, with the token as a bearer
credential, and the capture must preserve the unmodified response bytes, the response headers, the
retrieval time, the request parameters and a SHA-256.

**Do not run the capture by hand yet.** The committed helper and its verifier are not on `main`; they
are still under review in an open pull request. A hand-rolled capture risks producing an artifact
that does not carry the provenance `SA-001` requires, and the input is frozen the moment it is taken.
Wait for that PR to land, then run the helper and its verifier. This entry is updated when it does.
