# Roadmap — Cycle 1 evidence-value experiment

## Decision this cycle must enable

Decide whether this proposition is worth a second cycle:

> For someone choosing among public agent skills, a provenance-aware card that combines independent evidence, exposes disagreement, and names credible substitutes is materially more decision-useful than any single existing catalog for a majority of popular skills, and can be maintained with at most five minutes of human cleanup per card.

This is a product-risk experiment. It does not attempt to prove demand, business model, or production-scale crawling. The cycle ends with **Keep**, **Pivot**, or **Kill** based on committed artifacts and thresholds below.

## Cycle 1 deliverable

The complete prototype consists of:

1. a timestamped cohort derived from the all-time skills.sh leaderboard and resolved to 100 canonical, non-duplicate skill entities;
2. a provenance ledger and replayable extracted records from GitHub/upstream material, skills.sh adoption and partner audits, SkillProof, Tessl, and a bounded search for skill-specific external experience reports;
3. 100 machine-produced evidence cards, each with up to three ranked alternatives and explicit missing/conflicting evidence;
4. frozen single-catalog baseline views for the same subjects;
5. a deterministic, held-out 20-card audit bundle, completed by a reviewer who did not tune the pipeline where possible;
6. a metrics report and decision memo that applies the rule in this roadmap without changing it after results are known.

The cycle excludes a public site, production database, continuous crawler, personalized recommendations, author submission flow, and original large-scale skill evals.

## Known source constraints to verify, not assume away

- The [skills.sh API](https://skills.sh/docs/api) exposes the all-time leaderboard, stable IDs, content hashes/file trees, duplicate flags, and partner security audits. Its current documented authentication path is Vercel OIDC; the experiment must prove a permitted, reproducible acquisition path before depending on it.
- [SkillProof](https://skillproof.dev/blog/skills-that-beat-baseline) publishes baseline-vs-skill testing and says it has tested more than two thousand skills, but bulk access, stable identity mapping, and reproducible machine-readable access are not yet established for this project.
- [Tessl](https://tessl.io/blog/skills-are-software-and-they-need-a-lifecycle-introducing-skills-on-tessl/) distinguishes structural review evals from with/without-skill task evals. A review score is not empirical efficacy evidence, and broad public task-eval coverage must not be assumed.
- skills.sh may aggregate security verdicts from other providers. Independence is assigned to the originating provider/run, not to the page or API that republishes it.

## Frozen definitions and metrics

These definitions are part of the experiment contract. `SA-002` may clarify field-level mechanics after the first vertical slice, but it must not weaken the semantic bar or decision thresholds.

### Unit of analysis

The acquisition snapshot starts from all-time leaderboard order and advances until it contains 100 canonical, non-duplicate entities. The frozen manifest preserves every encountered leaderboard row, rank, exclusion/grouping decision, alias, source revision, and retrieval time so that “top 100” cannot be silently reinterpreted later.

A canonical identity is based on the actual skill source, path/slug, and immutable revision or content hash—not display name alone. Forks or copies are grouped only with recorded evidence; uncertain matches remain separate and are labelled uncertain.

### Independent source

Two items are independent only when they have different controlling source owners and do not reuse the same underlying claim, dataset, scan, or test run. Upstream `SKILL.md` and its README are one author-controlled source. An audit surfaced by skills.sh retains the audit provider as its origin. A mirrored or translated report is not a new source.

### Evidence classes

- **Author claim:** description, README, examples, or self-reported benchmark.
- **Adoption signal:** installs, stars, forks, recency; never treated as efficacy.
- **Structural review:** rubric or static quality analysis without task execution.
- **Security evidence:** static/dynamic scan or documented incident, with provider and method.
- **Empirical efficacy evidence:** an executed task or suite with an observable outcome and enough conditions to interpret it. It is **independent** only when the evaluator is not the skill author.
- **Experience report:** a skill-specific report by an identifiable user/reviewer that describes observed use, failure, setup cost, or comparison; generic listicles and copied descriptions do not qualify.

### Decision-useful synthesis

A reviewed card passes this metric only if it contains at least one correct fact or conclusion that changes an install/avoid/compare decision and that no one baseline catalog presents by itself. It must require cross-source combination, identity reconciliation, or explicit treatment of a material conflict/non-comparability. Merely placing independent facts next to each other is not enough.

The reviewer answers a fixed question: **“Would this additional information plausibly change which skill I try, whether I try one, or what caveat/setup I plan for?”** and records the concrete finding that caused the answer.

### Alternative correctness

Every card has exactly three candidate slots. A candidate is correct when it addresses substantially the same user job, is a plausible substitute before installation, and is not merely a fork/copy of the subject. On the 20-card audit, missing slots count as incorrect. `precision@3 = accepted candidate slots / 60`; the passing bar is at least 48/60 (80%). Recall is reported as unknown rather than implied.

### Cleanup time

Cleanup starts when the reviewer opens the generated card and ends when it meets the audit rubric or is marked unusable. Source browsing needed to verify or correct the card is included. The median across all 20 audited cards must be at most five minutes; unusable cards retain their full time and fail usefulness.

### Reported metrics

| ID | Metric | Denominator |
| --- | --- | --- |
| M1 | Cards with at least two correctly attributed independent source owners, including at least one non-author source | 100 canonical cards |
| M2 | Cards with decision-useful synthesis not available in any one baseline catalog | 20 held-out cards |
| M3 | Cards with independent empirical efficacy evidence | 100 canonical cards |
| M4 | Correct alternatives (`precision@3`) | 60 held-out candidate slots |
| M5 | Median manual cleanup time | 20 held-out cards |
| M6 | Single-source redundancy: reviewer reaches the same decision and material rationale from one baseline catalog alone | 20 held-out cards |
| M7 | Claim accuracy/provenance: sampled decision-relevant claims supported by the cited origin and conditions | all such claims in 20 held-out cards |

For M1 and M3, the automated result is accepted only if the held-out audit finds no more than one false-positive card for that metric. Report raw counts, failures, and Wilson intervals for sampled proportions; thresholds use the observed counts specified here, not an extrapolated point estimate.

## Decision rule

Apply the first matching rule in this order:

1. **Kill** if M1 is below 25/100, or M6 is at least 16/20, or M7 is below 95%. These mean useful independent evidence is too rare, one incumbent already supplies nearly all decision value, or the synthesis cannot be trusted.
2. **Keep** only if all are true: M1 at least 60/100; M2 at least 12/20; M3 at least 30/100; M4 at least 48/60; M5 at most five minutes; M6 at most 5/20; and M7 at least 95%.
3. **Pivot to curated category comparisons** if Keep fails but M1 is at least 25/100, M4 is at least 48/60, M7 is at least 95%, and the audited data contains at least two coherent job categories with at least five canonical skills each and at least half of the audited cards in those categories pass M2. The decision memo must name the categories from the frozen data, not invent them after selecting favorable examples.
4. **Kill** otherwise.

Failure to acquire a named optional source is a measured absence, not automatic failure. Failure to obtain and freeze a defensible 100-entity cohort makes the experiment invalid; `SA-001` must then choose and document either a permitted equivalent leaderboard snapshot (without changing thresholds) or an early Kill, rather than proceed with a hand-picked cohort.

## Execution order

### SA-001 — Produce one real end-to-end evidence card and prove cohort access

- **Status:** Investigation first
- **Priority:** Critical
- **Category:** Vertical slice / acquisition
- **Depends on:** None
- **Problem / question:** Can the project obtain one real popular skill plus independent evidence through permitted, reproducible paths, and can it freeze the official all-time ranking needed for the cohort?
- **Known evidence:** skills.sh documents an authenticated API; SkillProof and Tessl expose public reports but bulk access and stable joins are unproven.
- **Hypotheses:** One card can be assembled without a crawler or production schema; skills.sh OIDC or a permitted operator-provided export can freeze the ranking; missing optional sources can be represented honestly.
- **Next experiment:** Use a fixed, non-hand-picked subject from the first accessible all-time leaderboard page (the highest-ranked entity). Capture its upstream revision, skills.sh record/audits, attempted SkillProof/Tessl mappings, and one bounded external-review search. Produce a human-readable card plus a source ledger. In the same slice, freeze enough signed/hashed leaderboard response to prove how a 100-entity cohort will be obtained. Do not bypass authentication or access controls.
- **Expected information gain:** Establishes the actual join keys, provenance fields, access blockers, and whether the narrow path can emit a decision-useful object before formalising a schema.
- **Proposed direction after evidence:** Continue to `SA-002` if a defensible cohort path exists; otherwise record the exact blocker and choose a permitted equivalent snapshot or early Kill under the decision rule.
- **Compatibility / safety:** No credentials or complete third-party pages in git. Respect source terms, robots directives, rate limits, and licenses.
- **Validation / acceptance:** `experiments/cycle-1/smoke/` contains one rendered card, its extracted evidence records, direct source URLs, retrieval timestamps, hashes/revisions, every failed acquisition attempt, and a reproducible cohort-access note. A reviewer can trace every card claim to an origin. The slice states which evidence is missing and does not assign composite quality.
- **Artifacts / docs:** `experiments/cycle-1/smoke/`, `docs/source-access.md`
- **Estimated scope:** Small

### SA-002 — Freeze the experiment protocol, schema, and audit rubric

- **Status:** Blocked (SA-001)
- **Priority:** Critical
- **Category:** Experiment contract
- **Depends on:** SA-001
- **Problem / question:** Convert lessons from the real card into a machine-checkable contract without moving the product thresholds.
- **Known evidence:** This roadmap fixes semantic definitions and the decision rule; the vertical slice reveals field shapes and real source limitations.
- **Hypotheses:** A small claim-level model can preserve origin, aggregator, subject revision, method, conditions, direction, and comparability without a universal quality score.
- **Next experiment:** Define the minimal JSON/JSONL schemas, source-status vocabulary, card template, single-source baseline format, alternative rubric, decision-usefulness rubric, timing procedure, error taxonomy, and deterministic audit sampling algorithm. Pre-commit the audit seed and exact replacement rule before cohort processing.
- **Expected information gain:** Shows whether provenance and disagreement can remain inspectable rather than disappearing into prose.
- **Proposed direction after evidence:** Use the contract for all remaining artifacts; schema changes after card generation require a recorded protocol deviation and invalidate affected metrics until regenerated.
- **Compatibility / safety:** Make conditions explicit; do not infer evaluator independence from site branding alone.
- **Validation / acceptance:** Schemas validate the smoke card; the protocol contains executable metric formulas, immutable threshold values, a 20-card sampling rule (five per rank quartile), blinded comparison procedure, cleanup timer instructions, and a deviation log initially empty. Fixtures cover missing evidence, republished audits, version mismatch, true conflict, and non-comparable results.
- **Artifacts / docs:** `docs/experiment-protocol.md`, `schema/`, `fixtures/`, `experiments/cycle-1/protocol-deviations.md`
- **Estimated scope:** Medium

### SA-003 — Freeze and audit the 100-entity cohort

- **Status:** Blocked (SA-002)
- **Priority:** Critical
- **Category:** Cohort / identity
- **Depends on:** SA-002
- **Problem / question:** Can leaderboard rows be resolved to stable skill identities without display-name joins, hidden exclusions, or duplicate inflation?
- **Known evidence:** skills.sh exposes stable IDs, content hashes, source type, and an `isDuplicate` signal; that signal alone may not cover forks, moved skills, or multi-skill repositories.
- **Hypotheses:** Source + actual skill path/slug + revision/hash is sufficient for most identities; uncertain cases can remain explicit without corrupting the cohort.
- **Next experiment:** Traverse frozen all-time rank order until 100 canonical non-duplicate entities are accepted. Preserve every encountered row and reason for grouping/exclusion. Manually audit all uncertain identities and a deterministic 10-entity sample of accepted identities.
- **Expected information gain:** Measures identity ambiguity and prevents evidence or alternatives from being joined to the wrong skill.
- **Proposed direction after evidence:** Use the immutable manifest as the only population for Cycle 1.
- **Compatibility / safety:** Do not exclude low-quality, unavailable, suspicious, or inconvenient skills; only evidenced duplicates/copies are skipped.
- **Validation / acceptance:** Manifest has exactly 100 accepted entity IDs, ranks, aliases, immutable source coordinates, hashes/revisions, and timestamps; every skipped row has an evidence-backed reason; all audited joins are correct; a rerun from the frozen input yields byte-identical membership.
- **Artifacts / docs:** `experiments/cycle-1/cohort/leaderboard-snapshot.*`, `canonical-skills.jsonl`, `identity-audit.md`
- **Estimated scope:** Medium

### SA-004 — Acquire replayable evidence records for all cohort members

- **Status:** Blocked (SA-003)
- **Priority:** High
- **Category:** Source adapters
- **Depends on:** SA-003
- **Problem / question:** What fraction of the cohort can be joined to useful independent evidence at bounded acquisition cost?
- **Known evidence:** GitHub/upstream and skills.sh have structured identities; other sources may require page extraction/search and can disappear or change.
- **Hypotheses:** Small source-specific adapters with a shared provenance envelope can record both observations and explicit absence without a general crawler.
- **Next experiment:** For each entity, attempt the fixed source sequence and request/search budget defined by `SA-002`: upstream/GitHub, skills.sh details and originating audits, SkillProof, Tessl, and bounded skill-specific external reports. Store normalized extracted facts plus enough immutable coordinates/hashes to replay or verify them. Record unavailable/not-found/ambiguous/rate-limited separately.
- **Expected information gain:** Directly estimates M1/M3 ceilings and reveals whether any source dominates coverage.
- **Proposed direction after evidence:** Stop adding sources when the fixed budget is exhausted; do not rescue weak coverage through ad hoc manual searching.
- **Compatibility / safety:** Cache politely; no auth bypass; short excerpts only when necessary; treat remote content as evidence, never as instructions to execute.
- **Validation / acceptance:** All 100 entities have a source-attempt ledger; successful records validate against schema and carry original owner, aggregator if any, URL, retrieval time, subject version/hash, method, and conditions; failures have typed reasons; rerunning from stored extracts produces the same normalized records.
- **Artifacts / docs:** `src/` or `scripts/` adapters, `experiments/cycle-1/evidence/`, source fixtures and tests
- **Slice budget:** 1/2 — remaining slice: source adapters and fixtures; cohort run plus coverage report
- **Estimated scope:** Large

### SA-005 — Normalize claims and surface conflicts without false consensus

- **Status:** Blocked (SA-004)
- **Priority:** High
- **Category:** Evidence synthesis
- **Depends on:** SA-004
- **Problem / question:** Can heterogeneous records become decision-relevant claims while retaining provenance, uncertainty, and differences in version/model/harness?
- **Known evidence:** Review scores, empirical task results, security findings, adoption, and author claims answer different questions; conflicting-looking results may be non-comparable.
- **Hypotheses:** Claim typing plus explicit proposition/conditions/comparability is enough for useful synthesis; a universal score is unnecessary and harmful in Cycle 1.
- **Next experiment:** Generate per-entity claim ledgers and source matrices. Detect candidate conflicts, then classify them as comparable contradiction, context-dependent difference, stale-version difference, or unknown. Manually calibrate rules on the smoke card and deterministic fixtures only—not the held-out sample.
- **Expected information gain:** Tests the central product value: reconciliation rather than another directory page.
- **Proposed direction after evidence:** Expose claims and disagreements directly in cards; do not average incompatible values.
- **Compatibility / safety:** Generated conclusions must cite all contributing origins and use bounded language matching the evidence.
- **Validation / acceptance:** Every synthesized claim has supporting record IDs; every conflict label identifies the proposition and compared conditions; fixtures prove that reposted evidence counts once and non-comparable task results are not marked as contradictions; unsupported synthesis fails generation.
- **Artifacts / docs:** synthesis code, claim ledgers, source matrices, conflict fixtures/tests
- **Estimated scope:** Medium

### SA-006 — Generate three credible alternative candidates per skill

- **Status:** Blocked (SA-003)
- **Priority:** High
- **Category:** Alternatives graph
- **Depends on:** SA-003
- **Problem / question:** Can cheap catalog/content signals recover plausible substitutes rather than merely similar names, sibling skills, or copies?
- **Known evidence:** skills.sh provides semantic search but its ranking optimizes discovery, not substitutability; the cohort may contain multi-purpose and category-unique skills.
- **Hypotheses:** A job-to-be-done representation plus copy/fork exclusion and simple candidate fusion can reach 80% precision@3 without building a full ontology.
- **Next experiment:** On the smoke card and protocol fixtures, compare at least two cheap candidate methods (catalog search and content/job similarity). Freeze one method or deterministic fusion before generating candidates for the cohort. Always emit three slots; use explicit missing slots when no defensible candidate exists.
- **Expected information gain:** Determines whether the “AlternativeTo” graph is achievable independently of evidence coverage.
- **Proposed direction after evidence:** Generate exactly three ranked candidates and a short evidence-backed substitution rationale for each.
- **Compatibility / safety:** Exclude canonical copies/forks and do not treat complementary skills as substitutes merely because keywords overlap.
- **Validation / acceptance:** All 100 cards have three candidate slots; each populated edge records method signals and rationale; generation is deterministic from frozen inputs; smoke/fixture judgments are not included in the held-out M4 score.
- **Artifacts / docs:** alternative-generation code, `experiments/cycle-1/alternatives.jsonl`, tests
- **Estimated scope:** Medium

### SA-007 — Render 100 candidate cards and single-source baselines

- **Status:** Blocked (SA-005)
- **Priority:** High
- **Category:** Data prototype
- **Depends on:** SA-005, SA-006
- **Problem / question:** Can the normalized evidence and alternative graph produce inspectable cards that help a choice without hand-authored prose?
- **Known evidence:** The experiment needs comparable output, not a UI. Missing and contradictory evidence are themselves useful only if visible.
- **Hypotheses:** Markdown plus canonical JSON is sufficient to test decision value and cleanup cost.
- **Next experiment:** Render all cohort cards and separate baseline views for each individual catalog. Include identity, intended job, prerequisites/compatibility, adoption (labelled), evidence by class, conflicts/non-comparability, freshness, three alternatives, and explicit unknowns. Generate a machine-readable coverage report without interpreting the final decision.
- **Expected information gain:** Produces the actual prototype and reveals whether synthesis remains useful at card scale.
- **Proposed direction after evidence:** Freeze generated outputs before drawing the audit sample.
- **Compatibility / safety:** No composite “quality” score; no unsupported recommendation; every decision-relevant sentence links to claim IDs/origins.
- **Validation / acceptance:** Exactly 100 canonical JSON cards and 100 readable Markdown cards validate and render; baseline views exist for every source that covers the entity; generation from frozen inputs is byte-stable apart from declared build metadata; coverage totals reconcile with source ledgers.
- **Artifacts / docs:** `experiments/cycle-1/cards/`, `baselines/`, `coverage.json`, renderer/tests
- **Estimated scope:** Medium

### SA-008 — Run the held-out 20-card audit

- **Status:** Blocked (SA-007)
- **Priority:** Critical
- **Category:** Evaluation
- **Depends on:** SA-007
- **Problem / question:** Are cards accurate, uniquely decision-useful, alternatives credible, and cleanup cheap when judged outside pipeline calibration?
- **Known evidence:** Developer self-review would favor the synthesis; card/baseline labels and ordering can bias a reviewer.
- **Hypotheses:** Deterministic sampling, blinded/randomized presentation, and a fixed rubric can yield a directional but auditable prototype result.
- **Next experiment:** After outputs are frozen, derive five cards from each rank quartile using the pre-committed seed and replacement rule. Build a bundle that randomizes and hides whether each view is the synthesized card or a single-source baseline. Prefer a reviewer who did not tune the pipeline. If only the maintainer is available, preserve blinding and disclose the limitation. Time cleanup separately, verify all decision-relevant claims, judge all 60 alternative slots, and record the concrete unique insight or failure for M2/M6.
- **Expected information gain:** Supplies the evidence needed for every subjective decision threshold while exposing pipeline false positives.
- **Proposed direction after evidence:** Lock the completed audit before calculating the decision.
- **Compatibility / safety:** Do not replace sampled hard cases except under the pre-committed rule; preserve all rejected claims and alternatives.
- **Validation / acceptance:** Audit contains exactly 20 distinct cohort cards, 60 alternative judgments, per-card M2/M6 decisions with rationale, claim-level provenance checks, M1/M3 false-positive checks, cleanup durations, reviewer identity/relationship disclosure, blinded ordering key revealed only after completion, and no unresolved rubric fields.
- **Artifacts / docs:** `experiments/cycle-1/audit/`
- **Estimated scope:** Medium

### SA-009 — Apply the pre-committed rule and close Cycle 1

- **Status:** Blocked (SA-008)
- **Priority:** Critical
- **Category:** Product decision
- **Depends on:** SA-008
- **Problem / question:** Does the measured evidence justify Keep, a narrow category-comparison Pivot, or Kill?
- **Known evidence:** All thresholds and precedence are fixed above; sampled estimates are directional and must show uncertainty.
- **Hypotheses:** The result will discriminate among broad aggregation, narrow comparisons, and no project without requiring a website.
- **Next experiment:** Recompute M1–M7 from frozen artifacts, reconcile counts to the audit, apply the first matching decision rule, and write the strongest counter-interpretation. Do not change thresholds; protocol deviations are reported with impact.
- **Expected information gain:** Converts the data prototype into an explicit investment decision.
- **Proposed direction after evidence:** **Keep:** plan a second cycle for user-demand testing using the existing cards. **Pivot:** plan only the named category comparison experiment. **Kill:** archive the data and reasons; do not build catalog infrastructure.
- **Compatibility / safety:** Distinguish observed metrics from inference; do not generalize beyond the frozen popular-skill cohort.
- **Validation / acceptance:** A reproducible metrics file yields the same counts shown in `decision.md`; the memo states exactly one Keep/Pivot/Kill outcome, the rule branch that fired, uncertainty/counterevidence, source-access limitations, and what was deliberately not built. Roadmap status/evidence are reconciled.
- **Artifacts / docs:** `experiments/cycle-1/metrics.json`, `experiments/cycle-1/decision.md`
- **Estimated scope:** Small

## Stop condition

`SA-009` closes this roadmap. Do not add implementation work for a site to Cycle 1. A second roadmap is justified only by the recorded decision and must treat demand as a new assumption rather than claiming that data usefulness alone proves a product should exist.
