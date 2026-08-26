# Second-pass review of the Cycle 1 roadmap

This document records a second independent review of [`ROADMAP.md`](../ROADMAP.md), performed after the
first-pass revisions recorded in [`docs/roadmap-review.md`](./roadmap-review.md). Like that document, it is
an audit note, not a second source of planning state; `ROADMAP.md` remains authoritative.

No roadmap item was executed and no planning state was changed by the change that added this note. Applying
any finding below is a separate bounded decision, because several of them move thresholds, dependencies, or
sequencing.

## Review boundary

Reviewed state: commit `603a554` (`Record final roadmap review verdict`) on branch `claude/roadmap-review-wmpevu`,
covering `ROADMAP.md`, `AGENTS.md`, `docs/roadmap-authoring.md`, `docs/agent-playbook.md`,
`docs/agent-policy.local.md`, `docs/roadmap-review.md`, `.agentic-repo.toml`, and `.github/`.

The review asked two questions:

1. **Contract conformance** — does the roadmap satisfy the repository's own authoring and evidence rules?
2. **Gameability and reachability** — can Cycle 1 still reach Keep, Pivot, or Kill in a way that is not
   supported by the evidence it collected, or become unreachable for an avoidable reason?

Verification performed: manual reading of every section and item; independent recomputation of the roadmap
dependency graph (uniqueness, resolvability, acyclicity, ready ratio, chokepoint share); independent
recomputation of the Wilson interval claim.

`agentic-repo check` could not be executed in the review environment (the pinned kit artifact
`agentic-repo-kit-0.1.16.pyz` was downloaded and its SHA-256 matched `.agentic-repo.lock.json`, but sandbox
policy denied the invocation), so the graph numbers were recomputed by hand first. The pinned check then ran
in CI on the commit that added this note — the roadmap itself is unchanged from the reviewed state — and
returned `agentic repository contract is consistent` with `ready = 2/16 outstanding (12.5%)` and
`chokepoint: SA-001 gates 14/16 outstanding (87.5%)`, matching the independent recomputation exactly
([run 33008012122](https://github.com/kaaburgh/skills-alternative/actions/runs/33008012122)). The graph
numbers below are therefore tool-confirmed; the Wilson interval numbers remain this reviewer's own
computation, since no tool in this repository checks them.

## What holds up

These are stated so a later reader does not re-litigate them:

- **Graph invariants hold.** Sixteen unique IDs, every `Depends on` value resolves, the graph is acyclic, and
  every `Status` value is inside the vocabulary that `enforce_status_vocabulary = true` makes binding. The
  pinned `agentic-repo check` confirms this mechanically, along with generated-file integrity and links.
- **The Wilson claim is arithmetically correct.** At 15/20 the two-sided 95% Wilson interval is
  [0.531, 0.888]; at 14/20 it is [0.481, 0.855]. Fifteen really is the smallest integer whose lower bound
  clears 0.5, so the C1 threshold is derived rather than chosen.
- **Vertical-slice ordering is right.** `SA-002` emits one real end-to-end card before `SA-003` (protocol) and
  `SA-004` (schemas), which is the order `AGENTS.md` demands and the order projects usually get wrong.
- **The freeze/holdout construction is sound.** Binding on a named GitHub-hosted workflow completion plus a
  later NIST Beacon pulse removes the agent's control over both the sampling boundary and the draw.
- **The early-close procedure is genuinely designed.** Requiring the item that trips Rule 0 to write the
  decision artifact and drop unstarted siblings closes the usual failure where an invalidated experiment
  cannot reach the item that records its own death.
- **Ready ratio is acceptable.** Two of sixteen outstanding items (12.5%) are ready, above the configured
  `ready_floor = 1` and `ready_floor_fraction = 0.1`.

## Blocking findings

### BF-1 — Comparator completeness is self-certified, and the certifier is ambiguous

`SA-011` carries `Execution: CLOUD plus human comparator-completeness check` and must establish `B1 = 20/20`
before sealing. Nothing names who performs that check.

Both readings are defective. If the pipeline author performs it, the guarantee that comparators are not straw
comparators — the entire load-bearing fix from first-pass finding 1 — rests on a self-check by the party whose
composite must beat those comparators. If the independent evaluator performs it, they see twenty subjects'
baseline views before the sealed phased bundle, which is the exposure `SA-000` and the masking design exist
to prevent.

That first horn is stated too strongly, and on its own it proves too much. The same author picks the taxonomy,
the rubrics and the thresholds, and those are sound. A solo experimenter is an interested party at every layer
of this project; if interest alone disqualified a judgement, nothing here would survive, and this review's own
BF-6 deliberately accepts an author-performed pass. What singles this check out is the shape of the judgement,
not the person making it:

1. it falls **after** the outputs and the twenty drawn subjects are knowable, so precommitment is not
   protecting it the way it protects the taxonomy and the thresholds;
2. it **moves the primary outcome**, because it decides which views the evaluator compares when scoring C1;
3. it **leaves no trace**, because a fact absent from a baseline is not visible in that baseline.

The evaluator's Phase 2 is a real backstop but a late one: the audit phases are ordered, scoring is Phase 1 and
baseline-completeness diagnosis is Phase 2, so an omission has already done its work on C1 by the time anyone
could catch it. Those three properties together are what the rest of the protocol removes by freezing
judgements before the data exists, and what this check had nothing left to freeze against.

The metric with the harshest consequence in the document (`B1` below 20 fires Rule 0) is therefore the one
whose execution is least specified.

Suggested resolution: make completeness mechanical wherever possible — a field-level diff between the native
capture and the generated baseline view, with unmatched native fields enumerated rather than attested — and
name explicitly who adjudicates the residue that a diff cannot judge.

### BF-2 — `SA-000` is not sequenced before the expensive path

`SA-000` (secure an independent human evaluator) is `Open`, `Critical`, and depends on nothing, but only
`SA-011` and `SA-012` depend on it. Every other item can complete without it.

The reachable worst case is: execute `SA-001` through `SA-010` including the frozen batch acquisition and the
binding output freeze, then discover no eligible evaluator exists. The contract's own rule then applies —
"If no such evaluator is available, Keep and Pivot are ineligible and Rule 0 fires" — and the entire cycle is
invalid after all of its cost has been paid. Nothing in the roadmap prevents that ordering; `SA-000` being
listed first is presentation, not sequencing.

Suggested resolution: add `SA-000` to the `Depends on` of `SA-010` (or `SA-003`), so the binding freeze cannot
occur before the evaluator is secured. This converts a terminal late Rule 0 into an early cheap block, and it
costs nothing else — `SA-000` is ready today.

### BF-3 — The `deterministic replacement rule` is referenced but never defined

The held-out sampling paragraph states that "the smoke/calibration exclusions and deterministic replacement
rule are applied before selection". No replacement rule is defined anywhere in `ROADMAP.md`. The adjacent
sentence about "a replacement/rerun after seeing the pulse" concerns the freeze, not subject substitution.

This is an open degree of freedom sitting inside the one paragraph whose entire purpose is to close them, at
the exact point where the twenty confirmatory subjects are drawn. Whoever runs `SA-011` will have to invent
it, after the pulse is knowable.

Suggested resolution: define the rule in `SA-003` (which freezes the sampling algorithm) — what makes a drawn
entity ineligible, and the deterministic successor function that replaces it — or delete the phrase and state
that exclusions are applied to the eligible pool before the shuffle so replacement never arises.

### BF-4 — The binding freeze does not pin `run_attempt`

The binding freeze preserves the workflow run's ID, URL, `head_sha`, and server-recorded `completed_at`, and
Rule 0 fires if the binding workflow is "replaced or rerun".

A GitHub Actions re-run of the same run keeps the same run ID and increments `run_attempt`, and
`completed_at` advances. So the recorded field set cannot distinguish attempt 1 from attempt 3, and a re-run —
including an accidental "re-run failed jobs" — silently moves the `completed_at` boundary that determines
which NIST pulse qualifies, which determines the twenty subjects. The rule is stated as enforced but is not
decidable from the data the roadmap requires to be stored.

Suggested resolution: persist `run_attempt` and `run_started_at` alongside the existing fields, and require
`run_attempt == 1` for a binding freeze.

### BF-5 — No item declares a `Slice budget`

`docs/roadmap-authoring.md` requires `Slice budget: k/N` on any item that plainly will not fit in one PR, and
`agentic-repo check` warns on `Partially implemented` items without one. Zero of sixteen items declare a
budget, and every item is scoped `Small` or `Medium` — none is `Large`, which the authoring doc defines as
"requires a slice budget".

At least two items are visibly multi-PR at their stated content. `SA-004` implements schemas and validators
for identities, source attempts, lineage, observations, claims, alternatives, cards, baseline views,
manifests, manual interventions and audits, plus nine classes of adversarial fixture. `SA-008` tunes claim
typing, comparability, conflict classification, baseline extraction and composite rendering, plus
generation-time citation enforcement. `SA-003` and `SA-007` are plausible candidates too.

This is precisely the state the field exists to make visible: each slice will be individually correct and
bounded, and nothing will record that one is the sixth. The cost of fixing it is one line per item today, and
it is unrecoverable later.

### BF-6 — `SA-013`'s verifier is unspecified, and E1 drives both Kill and Keep

`SA-013` requires manual verification of all 100 E1 and all 100 E2 classifications. E1 fires the Rule 1 Kill
below 25/100, gates Rule 3 Pivot eligibility at 25/100, and gates Rule 2 Keep at 60/100. It is the single most
decision-loaded metric in the document after C1.

The item says `CLOUD plus bounded human verification` and names no independence requirement. The `SA-000`
independence gate is written for the *evaluator*, and the audit phases in the protocol section describe only
the evaluator's work, so on the current text the pipeline author may verify their own pipeline's E1/E2
classifications — including the judgment calls that "version-relevant" and "non-author" require.

Suggested resolution: either state explicitly that E1/E2 verification is objective enough to be author-performed
and say why, with an independently reproducible rule per classification, or route a deterministic sample of
the 200 classifications through a second party.

## Substantive findings

### SF-1 — C1's difficulty is not held constant across subjects

The composite wins a pair only by being uniquely most useful against **all** available individual catalog
views. skills.sh is present for every subject because it defines the cohort; SkillProof and Tessl are required
only "whenever a complete coverage check finds a page/record for that subject".

A subject covered by one catalog therefore requires the composite to beat one view; a subject covered by three
requires it to beat three. The 15/20 threshold is precommitted as if per-card difficulty were fixed, and
`B1 = 20/20` is satisfied equally by twenty single-comparator subjects and twenty three-comparator subjects.
Nothing precommits the expected comparator-count distribution, stratifies C1 by it, or requires it to be
reported.

This does not make a win fake, but it makes the same C1 number mean materially different things, and the
difference is only knowable after the cohort is frozen. Suggested resolution: precommit that the
comparator-count distribution of the twenty held-out subjects is reported with C1, and state whether a
distribution dominated by single-comparator subjects weakens the Keep claim in the memo.

### SF-2 — P1 turns one judgment call into the Keep/Kill boundary

`P1` requires 19 of 20 cards to have every decision-relevant factual claim supported, with zero critical
identity or provenance errors. Below 19 the Rule 1 Kill fires; there is no middle band. One evaluator's
strictness on one borderline claim on one card is the difference between "Keep" and "evidence layer not
viable", and the roadmap offers no adjudication path — correctly, it forbids repairing the result, but it also
does not require the disagreement to be recorded or its effect measured.

Suggested resolution: precommit that disputed P1 findings are enumerated in the decision memo with a
sensitivity line at P1 ± 1. This changes no threshold and adds no repair path; it only stops a
one-judgment flip from being invisible.

### SF-3 — T1's integrity is honour-system but is presented as enforced

Rule 0 fires on "unlogged/reclassified entity-specific work". No property of the data can detect work that was
never logged. `AGENTS.md` is explicit about this class: "Where a rule can only be judged by a person, say so
where the rule is written and wherever a validator would otherwise appear to cover it."

The T1 paragraph is unusually careful about *what* must be logged and how shared work is allocated, which
makes the omission more consequential — it reads as mechanically enforced to every later agent. Suggested
resolution: state at the T1 definition and in Rule 0 that this condition is attested, not verified, and that
its assurance comes from the contemporaneous timing discipline rather than from a check.

### SF-4 — Capture labels are producer-declared but drive the replayability claim

A capture is labelled `stored`, `externally_immutable`, or `metadata_only`, and "only the first two are called
replayable". The label is written by the producer. `stored` is checkable against a property of the data
(bytes present, hash reconciles) and `externally_immutable` is partially checkable (the coordinate resolves to
an immutable form such as a commit SHA), but the roadmap requires neither check — it requires only the label.

This is the pattern `AGENTS.md` names directly: comparing a self-declared label reports conformance that was
never checked. Suggested resolution: require `stored` to be validated by presence and hash reconciliation, and
`externally_immutable` by the coordinate matching a precommitted immutable-form pattern, in `SA-004`'s
validators.

### SF-5 — E2 has no role in the Pivot branch

Rule 2 Keep requires `E2 >= 30/100`. Rule 1 has no E2 floor, and Rule 3 does not mention E2 at all — Pivot
eligibility checks E1, A1, A2, T1, P1, B1, and the category probe checks category-level E1 but not E2.

A Pivot is therefore reachable with `E2 = 0/100`: the branch that keeps the project funded on weaker evidence
is the one that never checks whether independent empirical efficacy evidence exists anywhere in the cohort.
That may be deliberate — Pivot funds a confirmatory cycle rather than validating a product — but the
falsifiable outcome sentence promises that "independent evidence and alternatives meet the thresholds below",
and a reader will not find the exemption without diffing the three rules.

Suggested resolution: either add an explicit E2 floor to Rule 3, or state in Rule 3 that Pivot deliberately
ignores E2 and why.

### SF-6 — `SA-005`'s cohort-audit rerun is unbounded

More than two errors in the 20-entity cohort audit, or more than three in the 30-row universe audit, "requires
a full rerun and new pre-evidence freeze". No maximum number of reruns is set.

Each rerun is a fresh draw against the same integer bar, so repeated reruns converge on passing by chance
rather than by improved canonicalization, and the passing attempt is the one that becomes the frozen cohort.
This is the same class of loophole the first-pass review closed for held-out subjects, left open one layer
lower.

Suggested resolution: precommit a maximum (two reruns is a natural choice), after which the failure is a
substantive identity-layer Kill, and require every attempt's error counts to be preserved.

### SF-7 — Phase 1 alternative judgment may lack the evidence it requires

`SA-012` requires the evaluator to judge all 60 alternative slots "from identity/job evidence before reading
generated rationales", untimed, in Phase 1. `SA-011`'s bundle contents are specified as randomized
equivalent-format views of the twenty subjects plus the sealed ordering key. Nothing states that the bundle
carries target-side job evidence for the 60 alternative candidates.

Without it, Phase 1 slot judgment degrades to name recognition, and A1/A2 measure the evaluator's prior
familiarity rather than the alternatives method. With it, the bundle contains sixty additional entity
summaries whose completeness and neutrality are unspecified — and those summaries are pipeline output too.

Suggested resolution: specify in `SA-011` exactly what target-side material accompanies each slot, and hold it
to the same completeness contract as baseline views.

### SF-8 — `SA-013` may precede `SA-012`, with no stated safeguard

`SA-013` depends only on `SA-010`, so all 100 E1/E2 verifications may complete before the human audit begins.
The author would then know whether Keep remains reachable while preparing and sealing the bundle in `SA-011`.

Outputs are frozen and the ordering is sealed, so the leverage is limited, and running `SA-013` first has a
real benefit: an E1 below 25/100 kills the cycle before an evaluator's time is spent. The gap is that the
roadmap neither permits nor forbids the ordering, and does not say which safeguard makes it acceptable.

Suggested resolution: state the intended ordering and, if `SA-013` may run first, note that `SA-011`'s outputs
are hash-bound before `SA-013` begins.

## Hygiene findings

- **HF-1 — `SA-011` is scoped `Small`.** It resolves workflow and pulse metadata, derives the sample, randomizes
  views, builds the phased bundle, and performs up to sixty native-to-baseline completeness verifications by
  hand. That is not `Small`, and scope calibration is the thing `Estimated scope` exists to provide.
- **HF-2 — `Execution` values drift outside the documented vocabulary.** `docs/roadmap-authoring.md` defines
  `CLOUD`, `CLOUD RESEARCH`, `GATED`, `LOCAL ONLY`. The roadmap also uses `HUMAN GATED`, `CLOUD plus bounded
  human identity audit`, `CLOUD plus bounded calibration judgments`, `CLOUD plus human comparator-completeness
  check`, `CLOUD plus bounded human verification`, and `CLOUD + HUMAN GATED when triggered`. Only `Status` is
  check-enforced, so nothing fails — but this is the exact drift `AGENTS.md` warns about for statuses, and the
  human-gated portion of an item is decision-relevant enough to deserve a closed value.
- **HF-3 — `Blocked (<ID>)` names only one of several blockers, and cannot name more.** `SA-010` is
  `Blocked (SA-008)` but also depends on `SA-009`; `SA-014` is `Blocked (SA-012)` but also depends on
  `SA-013`. This was first written up as an authoring defect. It is not one: reading the pinned kit artifact
  shows the status is matched by `^blocked\s*\(\s*(<ID>)\s*\)$`, which accepts exactly one ID, and with
  `enforce_status_vocabulary = true` a two-ID value would fail the check rather than warn. A multi-blocker
  item therefore cannot express both blockers in its status field, and choosing between two co-equal blockers
  would only move which one is hidden. `Depends on` remains the complete answer. Recorded here as a kit
  expressiveness limit so it is not rediscovered as a roadmap defect; no roadmap change is warranted.
- **HF-4 — The freeze workflow's trigger is unspecified.** The binding freeze is "the first commit on `main`"
  whose named workflow succeeds, but `SA-010` does not state the workflow's trigger. The existing
  `agentic-repo-check.yml` runs on `push` (all refs) and `pull_request`, so a branch run would also succeed on
  a commit that later reaches `main` by merge or squash under a different SHA. `SA-010` should pin
  `push: branches: [main]`.
- **HF-5 — NIST pulse fields to persist are not enumerated.** `SA-011` requires "pulse records are preserved".
  Naming the fields — chain and pulse index, `timeStamp`, `outputValue`, and the signature — makes the draw
  independently replayable instead of merely recorded.
- **HF-6 — No operator-facing projection exists.** The contract makes it optional, so this is not a violation.
  But two human actions are ready right now — `SA-000` in full, and the bounded operator capture path inside
  `SA-001` — and both are currently discoverable only by reading a 385-line planning document.

## Structural observations

Reported by the pinned `agentic-repo check` in CI, and independently recomputed to the same values:

```
ready = 2/16 outstanding (12.5%)   -> SA-000, SA-001
chokepoint: SA-001 gates 14/16 outstanding (87.5%)
```

`SA-001` gating 87.5% of outstanding work is the honest shape of this experiment rather than a defect: the
cohort is defined by one authenticated skills.sh request, and there is deliberately no hand-built fallback.
Two consequences are worth stating where they will be read.

First, the fallback is narrow by design — only an operator capture of the same authenticated endpoint and
query qualifies — so the operator handoff inside `SA-001` is not an optional cross-check but the project's
only alternative route, and it should be prepared before it is needed rather than after `SA-001` fails.

Second, `SA-001` failing produces "Kill — experiment invalid, no product inference", which is the correct
label: an acquisition blocker is not evidence about the product question. The roadmap should not acquire a
second cohort source to reduce this risk, because that would change the population under study. The residual
risk is real and correctly priced; it is recorded here so that a later agent does not read the chokepoint
warning as an invitation to invent a fallback the contract forbids.

## Reviewer's verdict

The roadmap is in good condition and its decision rule is materially harder to game than the first draft. The
findings above are concentrated in one place: **the parts of the protocol that require a human, but do not say
which human.** BF-1, BF-6, and SF-2 are all instances of it, and BF-1 is the one that can manufacture the primary
result.

Recommended order if the findings are applied: BF-2 and BF-5 first (both are one-line edits with no threshold
consequence), then BF-1, BF-3, BF-4, and BF-6 folded into `SA-003`, which is where the protocol freezes and after
which "decision thresholds and comparator rules may not change". Everything in the substantive list must land
before `SA-003` or not at all.
