# Independent review of the Cycle 1 roadmap

This document records why the first roadmap was revised. It is an audit note, not a second source of planning state; [`ROADMAP.md`](../ROADMAP.md) remains authoritative.

## Review boundary

The first draft is preserved in GitHub commit [`d4182bb`](https://github.com/kaaburgh/skills-alternative/commit/d4182bb0eedc734d4e2862660e38bd6209d379d1) (`Bootstrap ARK and add first experiment roadmap`). A context-isolated reviewer was given that repository state, the original product brief, and ARK 0.1.16 guidance, but not the drafting rationale. The reviewer was another agent, not a human or institution; “independent” here means independent drafting context and an adversarial assignment.

The review goal was narrow: find ways the roadmap could formally reach Keep/Pivot without producing a trustworthy answer about the prototype.

## Blocking findings and applied changes

1. **No real paired outcome.** The first draft counted “plausibly decision-changing” information and compared pipeline-created baselines. That could reward a straw comparator. The revision names skills.sh, SkillProof, and Tessl; requires complete equivalent-format views checked against native captures; and makes an untouched paired win the primary outcome. Keep now requires 15/20 wins, enough for the 95% Wilson lower bound to exceed 50%.
2. **Held-out subjects were predictable.** The first draft committed the seed before pipeline work and did not exclude all tuned examples. The revision precommits only the algorithm, excludes smoke/calibration entities, binds all outputs first, and derives subjects from a future NIST Randomness Beacon pulse.
3. **Cleanup could improve scored output.** The revision scores untouched views first, then verifies provenance, then times corrections on copies. All earlier card-specific work is logged and added to correction time; unusable cards receive a time cap rather than a quick zero.
4. **Invalid experiments could still pass.** Rule 0 now stops on cohort/comparator failure, compromised holdout, non-independent evaluation, undefined denominators, unreconciled hashes, binding-output changes, unlogged work, or material protocol deviation.
5. **Pivot allowed post-hoc category mining.** Taxonomy and assignments now freeze before external evidence; category selection is objective; and Pivot requires a separate ten-card post-freeze probe. Otherwise category findings are exploratory and cannot fire the branch.
6. **Cohort and fallback were underspecified.** The revision fixes the exact skills.sh endpoint/query, preserves the 500-row candidate universe, permits only a capture of the same authenticated response as fallback, and treats revision/hash as observation version rather than durable identity.
7. **Alternatives could come from a changing/unverified universe.** The candidate universe is frozen with the cohort; every emitted candidate is canonicalized, versioned, and copy/fork checked; exactly three slots are scored, with missing slots incorrect.
8. **Low-value “independence” could pass.** Multi-origin evidence now requires lineage separation and a version-relevant non-author decision observation. README plus installs does not qualify.
9. **“Replayable” was stronger than the artifacts.** Exact input → observation → claim → card/baseline → audit → decision layers now carry hash manifests and explicit replay-status labels.
10. **One successful page did not establish batch feasibility.** The vertical slice now produces a source matrix covering access, joins, budgets, storage, and replay; adapters are tested on ten excluded calibration entities before the 100-entity run.
11. **Items were too broad.** The final graph separates acquisition, vertical slice, protocol, schemas, identity, adapters, batch data, synthesis, alternatives, freeze, audit bundle, human audit, objective metrics, Pivot probe, and decision into bounded reviewable items.

## Closure review

Two closure checks reviewed the revised roadmap only for ways its decision could still be gamed or become unreachable. They found eight additional blockers, all incorporated before publication:

1. **An early failure could block the item that writes the decision.** Every item that triggers Rule 0 or an early substantive Kill now owns an explicit early-close procedure: write the Kill artifact and available metrics, preserve the evidence and counter-interpretation, drop blocked successors with reasons, and leave the ARK graph consistent.
2. **A commit timestamp was not a trustworthy sampling boundary.** The binding freeze now requires a successful named GitHub-hosted workflow. Sampling uses its server-recorded completion time, immutable run identity and commit SHA, plus the first qualifying later NIST Beacon pulse. Re-running or replacing the successful freeze invalidates the experiment.
3. **Three alternatives were scored but not guaranteed.** All 500 ranked rows are canonicalized as the bounded candidate universe, the frozen prototype must contain exactly 300 populated candidate edges, and inability to produce them is a substantive Kill rather than missing data hidden from the denominator.
4. **A Pivot could average one strong category with one weak category.** Both precommitted categories must now pass every category-level integer threshold independently.
5. **Manual work could escape the time metric.** T1 now enumerates all entity-specific intervention classes, requires elapsed time plus affected IDs, allocates shared work equally over that fixed set, separates calibration-only pipeline development, and treats missing or reclassified work as invalidating.
6. **Post-score diagnosis could escape T1.** The per-card cleanup timer now starts before provenance/source verification and runs through diagnosis and editing; subtotals remain visible, but the threshold applies to the complete Phase 2+3 sum.
7. **Three slots did not guarantee three alternatives.** Every card now requires pairwise-distinct, non-self target canonical IDs from distinct canonical identity groups; duplicated versions, copies, and forks cannot fill the 300-edge contract.
8. **An early close could leave a sibling item runnable.** The early-close procedure now drops every other unstarted Cycle 1 item, including ready/open siblings, and reconciles every partially executed item.

## Residual limitations accepted for Cycle 1

- Twenty paired cards remain a small directional audit even with the stronger 15/20 bar.
- One independent human evaluator is still subjective; this is a prototype gate, not a generalizable user study.
- Catalog coverage, access rules, and pages can change after the frozen snapshot.
- External experience search is only as reproducible as the provider and fixed query budget allow.
- The all-time skills.sh ranking may be clustered, manipulated, or unrepresentative; results cannot be generalized to all public skills.
- Passing Cycle 1 would establish evidence-card usefulness for this cohort, not product demand, willingness to pay, or production economics.
