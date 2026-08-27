# SA-002 source-feasibility matrix

What each source permits, how it is keyed, and what would block it at cohort scale. All lookups
2026-08-27 against smoke subject `noizai/skills/sound-fx`.

Recorded here rather than in `docs/source-access.md`, which `SA-001` work is concurrently writing;
`SA-002`'s declared artifacts include `experiments/cycle-1/smoke/`, and splitting avoids two open
branches editing one file.

**Read the last column first.** *General* findings are properties of the source and carry to the
cohort. *Subject-specific* findings do not: the smoke subject was drawn uniformly from all 20,000
listed skills, so coverage seen here is a **floor** for the ranked-head cohort, not an estimate.

| Source | Permitted path | Auth | Stable key | Lookup result | Rate / budget | Storage rights | Replay status | Batch blocker | Kind |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| skills.sh listing (rendered) | `Allow: /` — the page, unlike `/api/`, is not disallowed | none | `/{owner}/{repo}/{skill}` | **positive**, 200 | not stated for pages | caching "encouraged and not restricted" **for skills.sh's own material only** — it does not own or relicense skill content | extracted fields `stored`; **the page itself `metadata_only`, not replayable** | **the page cannot be archived** — it embeds the author's SKILL.md body, so capture must extract fields at fetch time; plus unknown politeness budget at 100× | general |
| skills.sh API | `Disallow: /api/`, but the provider documents these endpoints and issues credentials, so authenticated use is sanctioned | **Vercel OIDC bearer** | `/api/v1/skills/...` | not attempted — no token | 600 req/min per (team, project) | as above | `stored` | **credential held outside the project** (`SA-001`) | general |
| GitHub upstream — content | anonymous git read via the session proxy | none | `{owner}/{repo}@{commit}:{path}` | **positive**, clone at `2a0e09d8` | not hit | **depends on the repo's licence** | `externally_immutable` | none technically; per-repo licence must be checked before storing | general |
| GitHub upstream — REST API | blocked in this session | session repo scope | `/repos/{owner}/{repo}` | **403** — "GitHub access to this repository is not enabled for this session" | 60/h unauthenticated in general | n/a | n/a | **API metadata unavailable for third-party repos without attaching each one**; content path is unaffected | general |
| SkillProof | `Allow: /` | none | flattened slug, e.g. `davila7-3d-web-experience` | **negative**, 404 on two constructed keys; positive path proven 200 | one lookup timed out at 30 s, succeeded at 60 s | not examined | `metadata_only` for a miss | **key is lossy** — owner/repo/skill flattened with hyphens, so joining from a skills.sh id is ambiguous and needs its 3,846-entry sitemap as an index | general |
| Tessl Registry | `Disallow:` empty — all allowed | none | `/registry/skills/{host}/{owner}/{repo}/{skill}` | **negative**, 404; positive path proven 200 on `anthropics/skills/docx` | not hit | not examined | `metadata_only` for a miss | none — the key maps directly onto the skills.sh id | general |
| External experience search | search API | n/a | none | **no qualifying report** | one query, this budget | n/a | `metadata_only` | provider and query budget must be frozen in `SA-003` or the source disabled cohort-wide | general |

## Findings that change how later items should be built

**The audit-revision gap is the sharpest one.** skills.sh republishes Gen Agent Trust Hub, Socket and
Snyk verdicts on the rendered page but does not say which revision each scanned. Three non-author
security lineages under distinct owners is exactly the shape `E1` wants, and it still fails the
version-relevance half of the rule. The audited revision appears to be reachable only through
`/api/v1/skills/audit/{source}/{skill}` — behind the same Vercel OIDC credential as `SA-001`. So the
metric most likely to carry the cohort is gated on the acquisition credential even though the
listing itself is not.

**A listing page cannot be archived just because the catalogue permits caching.** skills.sh renders
the author's SKILL.md body inside its own page, and its terms say plainly that it does not own, host
or relicense skill content. Its permission to cache therefore covers its own metadata — counts,
dates, audit verdicts — and stops at the embedded body. The consequence for `SA-006`/`SA-007` is
structural: the adapter must **extract fields at fetch time** rather than archive responses, and the
page itself can only ever be `metadata_only`, which the contract says is not replayable. So the
provenance chain for this comparator rests on extracted fields plus a response hash, not on a
replayable capture.

It also constrains the baseline. A comparator view may not omit awkward content, and none was
omitted — but for an unlicensed upstream, "complete" can only mean field-complete **by reference**,
not verbatim reproduction. `SA-003` has to decide whether the comparator-completeness contract, and
`B1` with it, is satisfied by reference, because otherwise no unlicensed subject can ever produce a
complete baseline.

**Storage rights are per-repository, not per-source.** The subject's upstream has no licence at all,
so its content could not be stored and had to be referenced by commit coordinate. A batch run cannot
assume a single storage policy for "GitHub"; every entity needs its own licence check before its
content is written down, and some fraction will be reference-only.

**Two comparator keys, two difficulty classes.** Tessl's hierarchical key joins directly from the
skills.sh id. SkillProof's flattened slug does not: `{owner}-{repo}-{skill}` collapsed with hyphens
is ambiguous when any part contains a hyphen, so its adapter needs the registry sitemap as an index
rather than key construction. That is adapter work `SA-006` should budget for.

**Republisher detection is cheap and necessary.** Two aggregator domains returned byte-identical
responses — same SHA-256, same 245,351 bytes. Hashing responses catches this class outright, before
any lineage reasoning is needed.

**Display-name collision is real, not hypothetical.** An unrelated `sound-fx` exists under a
different owner. The durable-identity rule earns its keep on the first subject drawn at random.

## What this probe does not establish

Coverage. One subject, drawn from the whole catalogue rather than the ranked head, produced
`not_covered` at both mandatory comparators. That is a floor, and the honest reading is that
comparator coverage for the actual cohort is **unknown** and must be measured on the calibration set
in `SA-006`. It would be wrong to conclude from this that comparators are usually empty; it would be
equally wrong to assume the ranked head is well covered.

It also does not establish anything about the paired decision task. No baseline comparison was
scored here and none should be: scoring belongs to the audit, on held-out subjects, after freeze.
