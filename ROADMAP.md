# Roadmap — Cycle 1 evidence-value experiment

## Falsifiable outcome

Cycle 1 tests one narrow proposition:

> For the top 100 canonical, non-duplicate skill entities derived from one frozen skills.sh all-time leaderboard snapshot, an untouched provenance-aware composite card is more useful for an install/avoid/compare decision than every complete individual catalog view available for that subject on at least 15 of 20 post-freeze held-out cards; at the same time, independent evidence and alternatives meet the thresholds below, median human correction is at most five minutes, and the correction-time tail is bounded.

“Top 100” in this repository never means all popular public skills. It means the first 100 accepted canonical entities in the exact frozen skills.sh ranking defined below. Fifteen paired wins in a 20-card audit is deliberately stronger than an observed bare majority: its two-sided 95% Wilson lower bound is above 50%.

The Cycle 1 result is a **data prototype and a decision**, not a site:

1. one frozen ranked input and bounded alternative-candidate universe;
2. 100 canonical entities with identity and source-attempt ledgers;
3. immutable observation, claim, card, baseline, and audit layers;
4. exactly three alternative slots per card;
5. one independently evaluated, post-freeze 20-card paired audit;
6. verified metrics and exactly one Keep/Pivot/Kill outcome.

The cycle excludes a public UI, production database, continuous crawler, submission flow, accounts, personalized recommendations, and original large-scale skill evals. It also does not test demand or business model.

## Fixed experiment contract

### Ranked input, cohort, and candidate universe

The primary input is the authenticated official request:

```text
GET https://skills.sh/api/v1/skills?view=all-time&page=0&per_page=500
```

The committed capture includes the unmodified response bytes, relevant response headers, retrieval time, request parameters, and SHA-256. The only fallback is an operator-provided capture of **that same authenticated endpoint and query**, with the same metadata and schema checks. A rendered page, search-engine result, another catalog, or a hand-built list is not an equivalent fallback. If neither path works, Rule 0 fires.

All 500 ranked rows form the bounded Cycle 1 alternative-candidate universe. The cohort is produced by walking those rows in rank order until 100 canonical non-duplicate entities are accepted. Every encountered row and every group/skip decision remains in the manifest. This walk is the sole definition of the cohort; nothing is skipped for being tuned on. Because `SA-002` now chooses its smoke subject independently of the ranking rather than taking its first row, that subject may land inside the accepted 100, among the remaining ranked rows, or outside the 500 entirely. In every case the rule above is unchanged: it is excluded from confirmatory sampling, never from the cohort. Treating it otherwise would make the cohort something other than the first 100 accepted entities in the frozen ranking, and would single out one tuned entity while the ten calibration entities — selected from this same cohort and tuned on far more heavily — stay in.

Durable identity uses source type, source owner/repository or well-known provider, and actual skill path/slug. Content hash and repository commit identify an **observation version**, not the enduring entity. Display names never join records. Official duplicate flags, identical content, or a verified source move may support grouping; uncertain similarity alone may not. Unresolved identity uncertainty is reported and sensitivity-tested, not silently merged.

### Mandatory comparator set and paired decision task

The prespecified catalog comparators are:

- skills.sh;
- SkillProof;
- Tessl Registry.

skills.sh is mandatory for every audited subject because it defines the cohort. SkillProof and Tessl are mandatory comparators whenever a complete coverage check finds a page/record for that subject. `Not covered` is a valid source result; `coverage unresolved` or `covered but capture incomplete` is not.

For each source, the baseline is an equivalent-format view containing every decision-relevant fact present in the captured native catalog record, with no cross-source synthesis. The native capture/immutable coordinates remain available for completeness review. A pipeline-produced baseline may not omit awkward fields, warnings, setup details, or negative results. Any incomplete required baseline in the held-out sample fires Rule 0 rather than giving the composite a default win.

Baseline completeness is established by a property of the data, never by attestation. `SA-003` freezes, per comparator, a **native field enumeration procedure** — how field keys and their rendered values are extracted from a capture — and a **representation rule** stating what counts as a field being represented in a baseline view. `SA-011` then runs a producer-independent validator that enumerates every native field key in each required comparator capture and lists the ones its baseline view does not represent. `B1` counts a subject complete only when that list is empty for every required comparator. No person certifies completeness and no person's judgement is needed to detect a gap.

This one check is mechanised, where the protocol elsewhere accepts author-performed work, because of the shape of the judgement rather than who makes it. It would fall after the outputs and the twenty drawn subjects are knowable; it moves the primary outcome, since it decides which views the evaluator compares in Phase 1; and an omitted field leaves no trace, because a fact absent from a baseline is not visible in that baseline. Freezing taxonomy, rubrics and thresholds before the data exists neutralises author interest everywhere else in this protocol. Here there was nothing left to freeze at the point of judgement, so the judgement moves back into `SA-003` — onto the calibration captures, before any confirmatory output exists.

Both frozen procedures are validated on the calibration captures, where an omission can be introduced deliberately and the validator must catch it. The evaluator's Phase 2 remains an independent backstop: a completeness defect they find that the validator did not is evidence that the enumeration or representation rule is itself defective, which is a material protocol deviation and fires Rule 0 rather than being corrected into a pass.

The independent evaluator receives the subject identity and a fixed job-to-be-done, then views the untouched composite and all available complete single-catalog views in randomized, label-masked order. For each view the evaluator records:

1. `try`, `avoid`, or `insufficient`;
2. the first skill to try, if any;
3. the most important reason/caveat;
4. decision confidence from 1–5;
5. which one view, if any, is uniquely most useful.

The composite earns a paired win only when it is uniquely most useful against **all** available individual catalog views and contains no critical identity, provenance, or factual error. Ties and losses are not wins. Presentation masking reduces cueing but is not claimed to make visibly different content perfectly blind.

### Evidence and independence

Every observation has both a source owner and a lineage ID for the underlying dataset, scan, test run, or report. Different host pages or owners do not establish independence when they republish the same lineage. Unknown ownership/lineage is treated as non-independent.

Evidence classes stay separate:

- `author_claim` — author-controlled SKILL.md, README, examples, or benchmark;
- `adoption` — installs, stars, forks, or recency; never efficacy;
- `structural_review` — rubric/static quality analysis without task execution;
- `security` — scan or incident with provider, method, and version relevance;
- `empirical_efficacy` — executed task/suite with observable outcome and material model/harness conditions;
- `experience_report` — skill-specific observed use, failure, setup cost, or comparison from an identifiable non-author; copied descriptions and generic listicles do not qualify.

Evidence is version-relevant only when it targets the captured revision or the claim states why it remains applicable. A card satisfies multi-origin decision evidence only when it has at least two independent lineages controlled by different owners and at least one is a version-relevant, non-author `structural_review`, `security`, `empirical_efficacy`, or `experience_report`. Author description plus adoption alone does not pass.

`E1` and `E2` labels are decided by a frozen decision procedure, not by opinion. `SA-003` freezes an ordered, exhaustive set of predicates over frozen observation fields — source owner, lineage ID, evidence class, target revision, and author relationship — such that two people applying them to the same observations must produce the same label, and every emitted label records which predicate decided it. Verification is therefore re-derivation, not review.

Who re-derives is stated rather than assumed. The first pass may be run by whoever built the pipeline, because a frozen predicate set makes the work reproducible rather than discretionary; `SA-013` records that this pass is author-performed and not independent, and the decision memo repeats it wherever `E1` or `E2` is used. Independence comes from a second pass: once the evaluator's audit results are committed and hash-bound, the same eligible evaluator re-derives a deterministic 20-classification sample drawn from the frozen observations. More than two disagreements discards the first pass, and all 200 classifications must be re-derived before any threshold uses `E1` or `E2`; if that cannot be completed, Keep and Pivot are ineligible and Rule 0 fires. Drawing the sub-sample only after the audit is committed keeps the evaluator's paired judgements uncontaminated by evidence classifications.

Differences are labelled contradictions only when they address the same proposition under materially comparable versions, models, harnesses, and tasks. Otherwise the card preserves them as context, stale-version evidence, or non-comparability.

### Immutable artifact layers

Cycle 1 uses these exact layers:

```text
experiments/cycle-1/00-inputs/
experiments/cycle-1/01-observations/
experiments/cycle-1/02-claims/
experiments/cycle-1/03-cards/
experiments/cycle-1/04-audit/
experiments/cycle-1/05-decision/
experiments/cycle-1/manifests/
```

Each producer writes a manifest containing input hashes, output hashes, producer command/version, timestamp, and manual interventions. A source capture is labelled `stored`, `externally_immutable`, or `metadata_only`; only the first two are called replayable. Observations are source-faithful extractions, claims normalize propositions and conditions, and cards synthesize claims. A derived layer consumes only frozen hashes from the preceding layer.

The binding output freeze is the first commit on `main` containing `experiments/cycle-1/manifests/output-freeze.json` whose GitHub Actions workflow named `Cycle 1 output freeze` succeeds. That workflow must run ARK validation plus clean-checkout regeneration and manifest reconciliation. Its GitHub-hosted run ID, URL, `head_sha`, `run_attempt`, `run_started_at`, and server-recorded `completed_at` are preserved in the audit manifest. A run binds only when `run_attempt` is 1. A re-run keeps the same run ID while advancing `completed_at`, so without the attempt number the recorded fields cannot distinguish a first success from a third, and a silent re-run would move the `completed_at` boundary that selects the qualifying NIST pulse and therefore the twenty held-out subjects. A commit whose first attempt failed simply does not qualify; the next freeze commit's own first attempt may bind, and that is not a deviation. Re-running or replacing an already-binding successful freeze, or editing an eligible card/baseline afterward, is a material protocol deviation and fires Rule 0.

### Calibration, held-out sampling, and evaluator independence

The smoke entity and ten calibration entities are excluded from every confirmatory audit. Both remain cohort entities when the frozen ranking places them there; exclusion is from sampling, not from the population. The calibration set is deterministically selected from the frozen cohort using `SHA-256(cohort_snapshot_sha256 || "skills-alternative-cycle-1-calibration-v1")`; its algorithm and exclusions are fixed before any adapter or synthesis tuning.

Only the held-out **algorithm and rank-quartile strata** are precommitted. The actual 20 subjects remain unknowable until after the output-freeze commit. The seed is derived from:

```text
SHA-256(output_freeze_commit_sha || output_freeze_workflow_run_id || nist_beacon_output_value || "skills-alternative-cycle-1-audit-v1")
```

where `nist_beacon_output_value` is the first [NIST Randomness Beacon 2.0](https://csrc.nist.gov/projects/interoperable-randomness-beacons/beacon-20) pulse timestamped at least two minutes after the binding workflow run's GitHub-server-recorded `completed_at`. The algorithm shuffles eligible entities within canonical-rank quartiles and chooses five per quartile. Every exclusion — the smoke subject and the ten calibration entities — is removed from the eligible pool before the shuffle, so the draw cannot land on an ineligible entity and no replacement step exists. Each quartile must hold at least five eligible entities before the draw; if one does not, a required denominator is undefined and Rule 0 fires.

After the draw no subject may be substituted, for any reason. A drawn subject that proves unauditable is not swapped out: it is carried into the audit and resolved by the rule covering its defect, which for an incomplete required comparator capture is `B1` and Rule 0. Substitution is the mechanism by which an inconvenient subject would quietly become a convenient one, so the protocol has none. Rerunning the draw once the pulse is knowable invalidates the experiment.

The evaluator must be a human who did not create or tune the pipeline, schemas, rubrics, source mappings, cards, baselines, or thresholds, and who has not seen the card outputs before receiving the sealed bundle. The evaluator receives the task/rubric but not threshold values. If no such evaluator is available, Keep and Pivot are ineligible and Rule 0 fires.

The audit has three ordered phases:

1. score untouched randomized views and alternatives (candidate names first, generated rationales hidden);
2. start the cleanup timer, reveal provenance, browse captured/native sources, and verify and diagnose every decision-relevant claim, alternative, and baseline-completeness issue;
3. keep the same timer running while editing a separate copy; preserve the verification/diagnosis/edit subtotals, pauses with reasons, patch, and total duration.

T1 includes every human action outside smoke/calibration tuning whose absence would change one or a bounded set of entity/card outputs: identity adjudication; source mapping/joining; source browsing and verification; issue diagnosis; extraction correction; taxonomy assignment/correction; lineage, conflict, or version-relevance classification; candidate replacement/copy checks; baseline completeness/repair; and card edits. Each pre-freeze action records elapsed seconds and all affected entity IDs; shared work is allocated equally across that fixed set before sampling. Generic pipeline development performed only on smoke/calibration data is reported separately and excluded. An audited card's T1 is its allocated pre-freeze time plus the complete post-scoring Phase 2+3 timer; verification, diagnosis, and editing subtotals are reported but the threshold applies to their sum. Only genuine inactivity pauses with timestamped reasons are excluded. An unusable card receives the 15-minute correction cap, not a fast zero. Unlogged, omitted, or reclassified entity-specific work fires Rule 0.

### Metrics

| ID | Metric | Denominator and exact pass value |
| --- | --- | --- |
| E1 | Verified multi-origin decision evidence | 100 cards; count only after all 100 positive/negative classifications are manually verified |
| E2 | Verified independent empirical efficacy evidence | 100 cards; count only after all 100 positive/negative classifications are manually verified |
| C1 | Untouched composite paired wins | 20 held-out cards; Keep requires at least 15 |
| A1 | Correct alternative slots | 60 populated slots; Keep/Pivot eligibility requires at least 48 |
| A2 | Cards with at least two correct alternatives | 20 cards; Keep/Pivot eligibility requires at least 16 |
| T1 | Card-specific human correction time | 20 cards; median at most 5 minutes, at most 2 cards over 10 minutes; unusable = 15 minutes |
| P1 | Cards whose every decision-relevant factual claim is supported by the cited origin/conditions | 20 cards; at least 19, with zero critical identity/provenance errors |
| B1 | Audited subjects whose required comparator baselines represent every native field key | 20 cards; established by the frozen validator rather than by attestation; must be 20 or Rule 0 fires |

Every prototype card must contain three populated, valid candidate edges before output freeze (300 total). Their `target_canonical_id` values must be pairwise distinct, differ from the subject ID, and belong to three distinct canonical identity groups; a copy/fork or another version of the subject cannot fill a slot. Inability to do so is a substantive alternatives-graph Kill, not an empty or duplicated slot. Any invalid emitted target is a critical A1/A2 failure. Recall is explicitly unknown. Alternative slot judgments are clustered by card; report both slot totals and card-level results rather than treating 60 slots as independent observations.

Report raw counts, the initial and corrected identity error rates, publisher/repository/category concentration, one-entity-per-cluster sensitivity, and Wilson intervals for sampled proportions. Thresholds use the integer counts above.

### Decision precedence

Apply the first matching rule:

0. **Kill — experiment invalid, no product inference** if the exact cohort/candidate capture or mandatory comparator capture fails; the held-out subjects become knowable before output freeze; smoke/calibration leaks into an audit; evaluator independence fails; a required denominator is zero/undefined; a held-out quartile holds fewer than five eligible entities; a held-out subject is substituted after the draw; manifests/hashes do not reconcile; a binding output/workflow is replaced or rerun, or binds on a run whose `run_attempt` is not 1; a baseline-completeness defect escapes the frozen validator; the `E1`/`E2` re-derivation cannot be completed; unlogged/reclassified entity-specific work is found; or a material protocol deviation can affect any threshold.
1. **Kill — evidence/alternatives layer not viable** if the prototype cannot populate three canonicalized alternatives on every card, E1 is below 25/100, C1 is at most 4/20 (individual catalogs tie/beat the composite on at least 16/20), P1 is below 19/20, or any critical identity/provenance error exists.
2. **Keep** only if E1 is at least 60/100, E2 at least 30/100, C1 at least 15/20, A1 at least 48/60, A2 at least 16/20, T1 passes both bounds, P1 is at least 19/20 with zero critical errors, and B1 is 20/20.
3. **Run the precommitted category Pivot probe** only if neither prior rule fires, E1 is at least 25/100, A1/A2/T1/P1/B1 pass, and the pre-evidence taxonomy contains at least two primary categories with at least ten cohort entities, at least five still eligible after all exclusions, and verified E1 coverage of at least 60% each. Select the two eligible categories with the highest verified E1 rate (ties: larger category, then category ID), never by composite audit outcome. Use a new post-workflow NIST seed to select five previously unaudited/non-calibration entities per category. **Pivot** only if **each category independently** has at least 4/5 untouched composite wins, 4/5 verified E1 cards, 12/15 correct alternative slots, 4/5 cards with two correct alternatives, median correction at most five minutes with no card over ten, 5/5 provenance passes, and 5/5 complete comparators. Pivot means “fund a confirmatory narrow category-comparison cycle,” not “the category product is validated.”
4. **Kill** otherwise.

Decision thresholds and comparator rules may not change after `SA-003`. A discovered defect is recorded; if material, Rule 0 fires rather than repairing the result into a pass.

### Early-close procedure

Any roadmap item that establishes Rule 0 or another early substantive Kill owns the close; it must not wait for its now-blocked successors or for `SA-015`. In the same change it:

1. writes `05-decision/decision.md` and machine-readable available metrics as `Kill`, naming `experiment invalid` vs substantive evidence/alternatives failure and forbidding unsupported product inference;
2. preserves the triggering evidence and strongest counter-interpretation;
3. marks every other unstarted Cycle 1 item `Dropped` with the same decision artifact as reason—including ready/open siblings, not only downstream items—and honestly reconciles every partially executed item;
4. runs `agentic-repo check` and satisfies the stop condition.

This is the only path that may close Cycle 1 without `SA-015`.

## Executable roadmap

### Execution vocabulary

`Execution` is a closed grammar, not free text. Each value begins with exactly one base term and may carry
one or both qualifiers:

| Term | Meaning |
| --- | --- |
| `CLOUD` | executable end to end by a cloud coding agent |
| `CLOUD RESEARCH` | cloud-executable, but the deliverable is feasibility or access knowledge rather than final artifacts |
| `HUMAN GATED` | the deliverable is a human action; no cloud path completes the item |
| `LOCAL ONLY` | requires a workstation; unused in Cycle 1 and permitted only after a documented feasibility result |
| `+ GATED (<reason>)` | must not start until the named external dependency resolves |
| `+ HUMAN (<bounded role>)` | cloud work containing a bounded human judgment; the parenthetical names the task |

`+ HUMAN (<role>)` names the task, never the person. Who may perform a given role — in particular whether a
role may be performed by whoever built the pipeline — is an evaluator-independence question settled by
`SA-000` and `SA-003`, not by this field.

### SA-000 — Secure an independent human evaluator and sealed handoff

- **Status:** Open
- **Priority:** Critical
- **Execution:** HUMAN GATED
- **Category:** Evaluation governance
- **Depends on:** None
- **Problem / question:** Is an evaluator available who can remain independent of pipeline/rubric construction and unseen outputs until the sealed audit?
- **Next experiment:** Identify one human evaluator, disclose the role and time commitment without showing thresholds or future outputs, record conflicts/relationship, and agree on custody of the phased bundle and ordering key. The disclosed commitment covers the three audit phases and the post-audit `SA-013` re-derivation sample, which begins only after the audit results are committed and hash-bound. The evaluator may withdraw before seeing outputs without invalidating work; replacement must satisfy the same declaration before bundle delivery.
- **Expected information gain:** Removes a predictable late-stage blocker and prevents developer self-review from being relabelled independent after the cards exist.
- **Validation / acceptance:** A signed/acknowledged eligibility and confidentiality-of-thresholds declaration, contact-independent handoff procedure, withdrawal/replacement rule, and expected audit phases including the post-audit re-derivation sample are stored without exposing any card output.
- **Artifacts / docs:** `docs/evaluator-handoff.md`, `experiments/cycle-1/04-audit/evaluator-declaration-template.md`
- **Estimated scope:** Small

### SA-001 — Freeze the official ranked input and candidate universe

- **Status:** Investigation first
- **Priority:** Critical
- **Execution:** CLOUD RESEARCH + GATED (permitted skills.sh authentication, or an operator capture of the same request)
- **Category:** Acquisition gate
- **Depends on:** None
- **Problem / question:** Can Cycle 1 obtain the exact official ranking it claims to study without a hand-picked fallback?
- **Next experiment:** Execute the fixed skills.sh request above through Vercel OIDC. If this environment cannot, attempt one bounded operator handoff for a capture of the same request. Do not inspect subject-specific evidence first.
- **Expected information gain:** Establishes whether the stated population and bounded alternative universe exist as a defensible input.
- **Validation / acceptance:** `00-inputs/skills-sh/` contains the raw 500-row response, request/response metadata, retrieval time, SHA-256, schema validation, rank monotonicity/uniqueness checks, and acquisition-attempt log. Failure records Rule 0 and stops the cycle.
- **Artifacts / docs:** `experiments/cycle-1/00-inputs/skills-sh/`, `docs/source-access.md`
- **Estimated scope:** Small

### SA-002 — Emit one real card and a source-feasibility matrix

- **Status:** Completed and verified
- **Priority:** Critical
- **Execution:** CLOUD RESEARCH
- **Category:** Vertical slice
- **Depends on:** None
- **Problem / question:** Can one skill travel from upstream source through real external evidence into an inspectable card, and which sources are batch-feasible?
- **Why this does not depend on `SA-001`:** The cohort needs the frozen ranked input; this question does not. Whether a more useful card can be assembled at all from GitHub, SkillProof, Tessl and experience reports is answerable on any single public skill, and the answer is the same whichever one it is. Binding the vertical slice to the acquisition gate put the project's only end-to-end output behind a credential held outside the project, which is the state `AGENTS.md` warns about: formalisation stays available while nothing is ever emitted. The smoke subject is excluded from every confirmatory denominator, so choosing it without the ranked input cannot move any threshold.
- **Next experiment:** Name one publicly listed skill as the fixed smoke subject and commit that choice **before inspecting any of its evidence**, recording the date and the reason it was picked. Pick for being ordinarily representative rather than for looking well covered, and state in the record which it is. Then attempt GitHub/upstream, skills.sh details/audits, SkillProof, Tessl, and one bounded external-experience search. Produce the smallest source-faithful observations, claims, baseline views, composite card, and alternatives that can carry the full path. Do not define, touch or pre-empt the cohort or the candidate universe here; the alternatives produced are an ad hoc feasibility probe, not the frozen method, which `SA-009` owns.
- **Expected information gain:** Reveals join keys, authentication, allowed acquisition/storage, rate/search budgets, version relevance, lineage, and genuine missing data before schema work — and does so before the acquisition gate resolves, so a source that cannot be joined at all is discovered while the protocol is still cheap to change.
- **Validation / acceptance:** The subject was committed before its evidence was inspected. The smoke card traces every sentence to an origin; failures are typed. A matrix records for every source: permitted path, auth, stable key, one positive/negative lookup where possible, expected coverage, rate/search limit, storage rights, replay status, and exact batch blocker, and marks which findings are specific to this subject rather than general — a probe run on an unusually well-covered skill overstates feasibility. The smoke subject is permanently ineligible for every confirmatory audit, whether or not the frozen ranking later places it in the cohort.
- **Outcome:** Executed 2026-08-27 on smoke subject `noizai/skills/sound-fx`, drawn deterministically from all 20,000 listed skills and committed before any of its evidence was retrieved. One composite card exists, every sentence citing a claim and every claim an observation with an immutable coordinate. Both mandatory comparators returned `not_covered` with their positive paths separately proven, so this subject is carried by skills.sh alone; that is a coverage floor from a catalogue-wide draw, not an estimate for the ranked-head cohort. The sharpest finding is that skills.sh republishes three non-author security verdicts without stating the revision each scanned, so the shape `E1` wants is present while its version-relevance half fails, and the audited revision appears reachable only through the authenticated endpoint gated by `SA-001`. Storage rights proved to be per-repository rather than per-source: the subject's upstream carries no licence, so its content is referenced by commit coordinate instead of stored. No source-feasibility Kill: every enabled source was reached, keyed and typed.
- **Artifacts / docs:** `experiments/cycle-1/smoke/`, `experiments/cycle-1/smoke/source-feasibility-matrix.md`
- **Estimated scope:** Small

### SA-003 — Freeze protocol, comparators, rubrics, search, taxonomy, and decision rule

- **Status:** Blocked (SA-002)
- **Priority:** Critical
- **Execution:** CLOUD
- **Category:** Experiment protocol
- **Depends on:** SA-001, SA-002
- **Problem / question:** Can the experiment be specified so that later missing sources, categories, and outputs cannot change what counts as success?
- **Next experiment:** Turn the fixed contract above and source-feasibility results into a versioned protocol. Name exact external-search provider/API or disable that source for the entire cohort; freeze locale, aliases, query templates, result depth, exclusion rules, and “first N qualifying results regardless of sentiment.” Freeze a finite primary job-to-be-done taxonomy and assignment rubric before external evidence is processed. Freeze comparator completeness, evaluator eligibility, masking, correction timing, NIST sampling, and Rule 0. Four of these are named separately because a later item would otherwise have to invent them: (a) the per-comparator native field enumeration procedure and representation rule that make baseline completeness machine-decidable; (b) the ordered predicate set that decides every `E1`/`E2` label from frozen observation fields, and the two-pass re-derivation with its 20-classification sample and two-disagreement bound; (c) the binding-freeze field set including `run_attempt`, `run_started_at`, and the attempt-1 requirement; (d) the held-out draw with exclusions removed from the eligible pool before the shuffle, the five-per-quartile precondition, and the prohibition on post-draw substitution.
- **Expected information gain:** Removes cohort, comparator, search, category, and audit degrees of freedom before the final data exists.
- **Validation / acceptance:** `experiment-protocol.md` contains exact integer formulas, no placeholder source or fallback, a deviation log, evaluator declaration, paired task, calibration/held-out/pivot algorithms, and a worked synthetic decision example. Thresholds match this roadmap byte-for-byte. The completeness validator and the `E1`/`E2` predicate set are executable and are demonstrated on the calibration captures: a deliberately omitted native field must be caught, and two independent applications of the predicate set to the same calibration observations must produce identical labels. A procedure that cannot be demonstrated is not frozen.
- **Artifacts / docs:** `docs/experiment-protocol.md`, `experiments/cycle-1/protocol-deviations.md`
- **Estimated scope:** Medium

### SA-004 — Implement artifact schemas, manifests, and adversarial fixtures

- **Status:** Blocked (SA-003)
- **Priority:** High
- **Execution:** CLOUD
- **Category:** Data contract
- **Depends on:** SA-003
- **Problem / question:** Can raw observations, normalized claims, synthesis, baselines, and corrections remain mechanically separate and hash-linked?
- **Next experiment:** Implement the smallest schemas/validators for identities, source attempts, lineage, observations, claims, alternatives, cards, baseline views, manifests, manual interventions, and audits. Use the smoke output as the first real fixture, then add synthetic adversarial cases.
- **Expected information gain:** Tests whether “provenance-aware” survives serialization rather than existing only in prose.
- **Validation / acceptance:** Fixtures cover republished evidence, unknown lineage, stale version, true conflict, non-comparability, missing comparator, fork/copy alternative, unsupported synthesis, and an unlogged edit. Clean-checkout validation proves layer boundaries and manifest hash reconciliation.
- **Artifacts / docs:** `schema/`, `tests/fixtures/`, validation code under one chosen source root
- **Slice budget:** 0/3
- **Remaining slices:** (1) observation/claim/card layer schemas, the manifest schema, and the hash-linking
  validator, using the `SA-002` smoke output as the first real fixture; (2) identity, lineage, source-attempt,
  alternative-edge, and baseline-view schemas with their validators; (3) the adversarial fixture suite covering
  all nine named cases, plus clean-checkout layer-boundary and manifest-reconciliation validation.
- **Estimated scope:** Large

### SA-005 — Resolve and audit the 100-entity cohort

- **Status:** Blocked (SA-004)
- **Priority:** Critical
- **Execution:** CLOUD + HUMAN (bounded identity audit)
- **Category:** Identity / cohort
- **Depends on:** SA-001, SA-004
- **Problem / question:** Can ranked rows be joined to stable skill entities without duplicate inflation or evidence crossing identities?
- **Next experiment:** Freeze the initial canonicalization output before review. Canonicalize all 500 candidate-universe rows, then walk them to 100 accepted cohort entities; preserve all rejected/grouped rows, assign the cohort's primary taxonomy category using upstream author material only, and select the ten calibration entities. Audit every uncertain cohort identity plus a deterministic 20-entity cohort sample and 30-row candidate-universe sample; preserve initial errors and corrections.
- **Expected information gain:** Measures false joins/splits and category/publisher concentration before source evidence can influence membership.
- **Validation / acceptance:** Exactly 500 ranked rows resolve to canonical candidate identities/groups and exactly 100 cohort entities are accepted; every decision has evidence. More than two errors in the 20-entity cohort audit or more than three in the 30-row universe audit requires a full rerun and new pre-evidence freeze; more than five unresolved cohort membership ambiguities fires Rule 0. Report initial/corrected error rates and merge/split sensitivity. Smoke/calibration exclusions are committed.
- **Artifacts / docs:** `00-inputs/cohort/`, `manifests/cohort.json`, `00-inputs/identity-audit.md`
- **Estimated scope:** Medium

### SA-006 — Build source adapters on the excluded calibration set

- **Status:** Blocked (SA-005)
- **Priority:** High
- **Execution:** CLOUD RESEARCH
- **Category:** Source adapters
- **Depends on:** SA-004, SA-005
- **Problem / question:** Do the precommitted access/search rules produce source-faithful observations across ordinary cases, not just the rank-1 smoke subject?
- **Next experiment:** Run every enabled adapter only on the ten calibration entities. Implement typed `covered`, `not_covered`, `ambiguous`, `unavailable`, and `rate_limited` outcomes; preserve original owner and lineage separately from aggregator.
- **Expected information gain:** Establishes batch feasibility and false-join/error shapes without touching audit-eligible content for tuning.
- **Validation / acceptance:** Calibration observations validate; every enabled source has positive/negative fixtures where reality permits; exact request/search budget and caching behavior are enforced; no remote content is executed as instructions.
- **Artifacts / docs:** adapter code/tests, `01-observations/calibration/`
- **Estimated scope:** Medium

### SA-007 — Run one frozen batch acquisition

- **Status:** Blocked (SA-006)
- **Priority:** High
- **Execution:** CLOUD
- **Category:** Evidence acquisition
- **Depends on:** SA-006
- **Problem / question:** What evidence actually exists at cohort scale under the fixed budget, and is the bounded candidate universe sufficient for alternatives?
- **Next experiment:** Run adapters once for all 100 cohort entities and acquire the minimal source/job/compatibility content needed for every canonicalized row in the 500-row candidate universe; capture revision/hash and copy/fork signals. No ad hoc rescue search is allowed.
- **Expected information gain:** Reveals the real E1/E2 ceilings, source dominance, missingness, and candidate-universe quality.
- **Validation / acceptance:** All entities and candidate rows have source-attempt ledgers; stored observations are hash-linked and typed; coverage totals reconcile; all card-specific manual work is timed/logged; a clean-checkout replay from stored inputs yields identical observations.
- **Artifacts / docs:** `01-observations/`, acquisition manifest and coverage report
- **Estimated scope:** Medium

### SA-008 — Freeze claim synthesis and baseline/card rendering on calibration only

- **Status:** Blocked (SA-007)
- **Priority:** High
- **Execution:** CLOUD
- **Category:** Evidence synthesis
- **Depends on:** SA-007
- **Problem / question:** Can heterogeneous observations become bounded claims and fair single-source/composite views without false consensus or straw comparators?
- **Next experiment:** Tune claim typing, comparability, conflict classification, equivalent-format baseline extraction, and composite rendering only on smoke/calibration entities and adversarial fixtures. Baselines must include every decision-relevant native field.
- **Expected information gain:** Tests the central synthesis layer before it sees any confirmatory outcome.
- **Validation / acceptance:** Every generated sentence cites claim/observation IDs; unsupported text fails generation; republished evidence counts once; baseline completeness passes against native calibration captures; no composite quality score is introduced.
- **Artifacts / docs:** synthesis/renderer code/tests, `02-claims/calibration/`, `03-cards/calibration/`
- **Slice budget:** 0/3
- **Remaining slices:** (1) claim typing, comparability, and conflict classification on calibration entities
  and adversarial fixtures; (2) equivalent-format baseline extraction with completeness checked against the
  native calibration captures; (3) composite rendering with generation-time citation enforcement, so
  unsupported text fails generation rather than being reviewed out later.
- **Estimated scope:** Large

### SA-009 — Freeze the alternatives method on calibration only

- **Status:** Blocked (SA-007)
- **Priority:** High
- **Execution:** CLOUD + HUMAN (bounded calibration judgments)
- **Category:** Alternatives graph
- **Depends on:** SA-005, SA-007
- **Problem / question:** Can a bounded, frozen universe yield substitutes for the same job rather than similar names, complements, siblings, or copies?
- **Next experiment:** Compare at least two cheap methods on calibration entities using only frozen candidate data. Freeze one deterministic method/fusion and a job-to-be-done rationale contract. Generated rationales are not shown during initial alternative judgment.
- **Expected information gain:** Determines whether the AlternativeTo graph can be tested without an ontology or changing live search results.
- **Validation / acceptance:** Method emits exactly three populated candidates for every calibration card. Their target canonical IDs are pairwise distinct, not the subject, and from distinct canonical identity groups; every edge is versioned and copy/fork checked. Failure to populate three valid targets is recorded as an alternatives-viability signal, not hidden by a missing or duplicated placeholder. Calibration labels and method choice are frozen and excluded from A1/A2.
- **Artifacts / docs:** alternatives code/tests, `03-cards/calibration/alternatives.jsonl`
- **Estimated scope:** Medium

### SA-010 — Generate all untouched outputs and bind the freeze

- **Status:** Blocked (SA-008)
- **Priority:** Critical
- **Execution:** CLOUD
- **Category:** Data prototype
- **Depends on:** SA-000, SA-008, SA-009
- **Problem / question:** Can the frozen pipeline emit the complete prototype without per-card authorship?
- **Next experiment:** From a clean checkout, generate claims, all available complete single-catalog baselines, 100 composite cards, three populated canonicalized alternative edges each, coverage, and the intervention-allocation log. Do not inspect a future held-out subset. Commit `output-freeze.json` with all hashes and producer versions and add the fixed `Cycle 1 output freeze` workflow. Do not bind the freeze before `SA-000` has secured an eligible evaluator: an absent evaluator makes Keep and Pivot ineligible and fires Rule 0, so freezing first converts a cheap early block into a terminal Kill after the whole acquisition and synthesis cost has been paid.
- **Expected information gain:** Produces the exact untouched objects whose value and maintenance cost will be measured.
- **Validation / acceptance:** Exactly 100 canonical JSON and Markdown composites; required baselines and native coordinates; 300 valid alternative edges, each card having three pairwise-distinct, non-self targets from distinct canonical identity groups; byte-stable regeneration; no unsupported claims; all manual interventions allocated/reconciled. If 300 valid edges cannot be produced, apply the early substantive Kill. Otherwise the first commit whose named GitHub-hosted workflow succeeds on `run_attempt` 1 becomes binding.
- **Artifacts / docs:** `02-claims/`, `03-cards/`, `manifests/output-freeze.json`
- **Estimated scope:** Medium

### SA-011 — Derive and seal the post-freeze audit bundle

- **Status:** Blocked (SA-010)
- **Priority:** Critical
- **Execution:** CLOUD
- **Category:** Audit preparation
- **Depends on:** SA-000, SA-010
- **Problem / question:** Can the audit subjects and view ordering be selected after outputs are immutable, with no missing/straw comparator advantage?
- **Next experiment:** Resolve and persist the binding workflow run ID/URL/head SHA/`run_attempt`/`run_started_at`/server `completed_at`, obtain the specified later NIST pulse, derive five eligible subjects per canonical-rank quartile from a pool the exclusions were removed from, randomize equivalent-format views, and create the phased evaluator bundle. Run the frozen completeness validator over every required comparator capture and its baseline view before sealing; do not repair frozen outputs.
- **Expected information gain:** Removes subject targeting and comparator omission as explanations for a win.
- **Validation / acceptance:** Workflow run and pulse records are preserved, including `run_attempt` 1; sample derivation is independently reproducible; every quartile held at least five eligible entities; no smoke/calibration entity appears and no subject was substituted after the draw; the completeness validator reports no unrepresented native field key, so B1 is 20/20; bundle hashes and sealed ordering key are committed; evaluator declaration is ready. A rerun/replacement or failure fires Rule 0.
- **Artifacts / docs:** `04-audit/bundle/`, `04-audit/sample-manifest.json`, `04-audit/sealed-ordering.json`
- **Estimated scope:** Medium

### SA-012 — Complete the independent human audit

- **Status:** Blocked (SA-011)
- **Priority:** Critical
- **Execution:** HUMAN GATED
- **Category:** Evaluation
- **Depends on:** SA-000, SA-011
- **Problem / question:** Do untouched composites win the fixed decision task, remain accurate, offer credible substitutes, and stay cheap to correct?
- **Next experiment:** An eligible evaluator completes the three audit phases in order. Score untouched views before provenance is unmasked or any cleanup timing begins. Judge all 60 alternatives from identity/job evidence before reading generated rationales. Then start one continuous per-card cleanup timer covering source browsing, verification, diagnosis, and editing of a separate copy.
- **Expected information gain:** Directly measures C1, A1/A2, T1, P1, and B1 without allowing cleanup to improve scored outputs.
- **Validation / acceptance:** Twenty complete paired judgments, 60 slot judgments, card-level alternative results, per-card provenance results, verification/diagnosis/edit subtotals and total cleanup durations, corrections/patches, evaluator declaration, and revealed ordering key. No missing field, omitted active time, or retroactive card change. The evaluator's `SA-013` re-derivation sample must not begin until these results are committed and hash-bound.
- **Artifacts / docs:** `04-audit/results/`
- **Estimated scope:** Medium

### SA-013 — Verify objective evidence metrics across all 100 cards

- **Status:** Blocked (SA-010)
- **Priority:** Critical
- **Execution:** CLOUD + HUMAN (frozen-predicate re-derivation)
- **Category:** Metrics audit
- **Depends on:** SA-010
- **Problem / question:** Are E1/E2 totals real, version-relevant, and lineage-independent rather than uncorrected classifier output, and is the verification itself trustworthy given who performs it?
- **Next experiment:** Re-derive all 100 E1 and all 100 E2 labels from the frozen observations using the `SA-003` predicate set, including explicit negatives, recording for each label the predicate that decided it and any disagreement with the pipeline's initial label. Corrections land in a derived metrics layer without editing frozen cards. Audit the manual-intervention allocation ledger for the enumerated T1 activities and reconcile concentration and identity sensitivity. Then, once `SA-012`'s results are committed and hash-bound, have the same eligible evaluator re-derive the deterministic 20-classification sample.
- **Expected information gain:** Gives 100-card denominators direct verification instead of extrapolating from 20, and measures whether the frozen predicate set actually produces the same labels in two hands.
- **Validation / acceptance:** A reproducible metrics file lists every included/excluded entity and reason; counts reconcile to 100; initial and verified totals remain separate; every label names its deciding predicate; no threshold is calculated from an undefined denominator. The file and the decision memo state that the first pass is author-performed and not independent. The evaluator sample records at most two disagreements; more discards the first pass and requires all 200 to be re-derived before any threshold uses E1 or E2, failing which Keep and Pivot are ineligible and Rule 0 fires.
- **Artifacts / docs:** `05-decision/evidence-metrics.json`, `05-decision/evidence-audit.md`
- **Slice budget:** 0/2
- **Remaining slices:** (1) the author-performed re-derivation of all 200 labels plus the intervention-ledger audit, runnable as soon as `SA-010` lands — an `E1` below the Rule 1 floor here fires the early substantive Kill without spending evaluator time; (2) the evaluator's 20-classification sample, which requires `SA-012` complete and hash-bound, and without which this item is not finished.
- **Estimated scope:** Large

### SA-014 — Run or explicitly skip the precommitted category Pivot probe

- **Status:** Blocked (SA-012)
- **Priority:** High
- **Execution:** CLOUD + HUMAN (paired category audit, only when the probe triggers)
- **Category:** Conditional pivot validation
- **Depends on:** SA-012, SA-013
- **Problem / question:** If broad Keep fails without an early Kill, is value concentrated enough in pre-evidence categories to justify only a narrow confirmatory cycle?
- **Next experiment:** Apply Rules 0–3 mechanically. If the probe is ineligible, commit `not-triggered` with the exact failed predicate. If eligible, select the two categories by the fixed rule, bind a new GitHub-workflow-completion plus later-NIST seed, draw five new entities per category, and repeat the untouched paired/provenance/alternative/correction audit with the same eligible evaluator standard, scoring each category separately.
- **Expected information gain:** Makes Pivot a tested narrow hypothesis rather than post-hoc category mining.
- **Validation / acceptance:** Either a reproducible skip record or ten complete new judgments with all Pivot integer thresholds computed. No category is renamed/reassigned after evidence or broad audit results.
- **Artifacts / docs:** `04-audit/pivot-probe/`
- **Estimated scope:** Medium

### SA-015 — Apply the rule and close Cycle 1

- **Status:** Blocked (SA-014)
- **Priority:** Critical
- **Execution:** CLOUD
- **Category:** Product decision
- **Depends on:** SA-012, SA-013, SA-014
- **Problem / question:** Does the frozen evidence support Keep, a narrow confirmatory Pivot, or Kill?
- **Next experiment:** Recompute every metric from manifests/audits, apply the first matching decision rule, and write the strongest counter-interpretation. Do not change thresholds; material defects invoke Rule 0.
- **Expected information gain:** Converts the prototype into an explicit investment decision without pretending it tested demand.
- **Validation / acceptance:** Machine-readable metrics and `decision.md` agree; the memo states exactly one outcome and rule branch, observed facts vs inference, uncertainty/concentration/sensitivity, source-access limitations, first-draft review changes, and what was deliberately not built. ROADMAP item states are reconciled.
- **Artifacts / docs:** `05-decision/metrics.json`, `05-decision/decision.md`
- **Estimated scope:** Small

## Stop condition

`SA-015` normally closes this roadmap; the Early-close procedure is the only alternative close. A Keep may create a demand-testing roadmap; a Pivot may create only the named confirmatory category-comparison cycle; a Kill archives the evidence and negative results. None authorizes a catalog site inside Cycle 1.
