# SA-002 smoke subject

**Subject:** `noizai/skills/sound-fx` — <https://www.skills.sh/noizai/skills/sound-fx>

**Committed:** 2026-08-27, before any evidence about this subject was retrieved. This file and
`selection.json` are the precommitment `SA-002` requires; nothing subject-specific had been fetched
when they were written.

## Why this subject

Nobody chose it. `SA-002` asks for a subject picked for ordinary representativeness rather than for
looking well covered, so the selection removes the author's discretion entirely: a fixed seed indexes
into the full public catalogue.

```text
index = int(SHA-256("skills-alternative-cycle-1-smoke-subject-v1"), 16) mod len(pool)
pool  = sorted(unique <loc> across both public skill sitemaps)
```

`selection.json` records the seed, both sitemap URLs and their SHA-256 digests, the pool size, the
index, and the resulting URL, so the draw replays exactly. The sitemaps are advertised in
`robots.txt` and are not subject-specific evidence; reading them to build the pool is not inspecting
the subject.

## What this subject is and is not representative of

The pool is the **whole catalogue** — 20,000 unique listed skills, uniformly drawn. So the subject is
catalogue-representative, **not** cohort-representative: the Cycle 1 cohort is the ranked head, the
first 100 accepted entities in the frozen skills.sh ranking, and a uniform draw over 20,000 almost
certainly lands outside it.

That matters for how the results read. Path properties this probe establishes — join keys,
authentication, permitted access, rate and search budgets, storage rights, replay status, batch
blockers — are properties of the sources and carry over. **Coverage** findings do not: whatever share
of comparators cover this subject is a floor for the cohort, not an estimate of it, because ranked-head
entities are more likely to be covered everywhere. The source-feasibility matrix marks which findings
are which.

The alternative — picking a popular skill so comparators would be well populated — is exactly the
selection-for-coverage the item forbids, and it would have made feasibility look better than it is.

## Standing exclusion

This subject is permanently ineligible for every confirmatory audit, whether or not the frozen
ranking later places it in the cohort. Any tuning done against it is smoke/calibration work and is
excluded from `T1` accordingly.
