## Experiment-specific policy

This repository exists to answer one product question, not to accumulate catalog infrastructure.

- The Cycle 1 result is a frozen data prototype and a precommitted decision. Do not build a public UI, production database, continuous crawler, recommendation feed, accounts, submission flow, or branding before the gate.
- Preserve immutable layers in order: permitted raw inputs/coordinates, source-faithful observations, normalized claims, synthesized cards/baselines, audit, then decision. Every producer records input/output hashes, command/version, and manual interventions.
- Score untouched generated outputs before any correction. Corrections occur only on separate copies, remain diffable, and never replace the frozen object being evaluated.
- Keep/Pivot requires an independent human evaluator who did not build or tune the pipeline/data/rubrics and had not seen the card outputs. If that gate fails, do not substitute developer self-review and call it independent.
- A single-catalog comparator must retain all decision-relevant native information. Missing or weakened comparator content cannot create a composite win.
- Every decision-relevant claim identifies original source owner, lineage, direct URL/immutable coordinate, retrieval/test date, subject revision/hash when available, method, and material conditions. An aggregator and the provider whose result it republishes are one lineage, not two independent sources.
- Do not collapse structural review, static security scanning, task execution, adoption, author claims, and experience reports into one score. Adoption-only evidence cannot satisfy independent decision-evidence coverage.
- Label differing results as contradictions only when they address the same proposition under materially comparable conditions; otherwise preserve non-comparability or staleness.
- Freeze cohort, candidate universe, source/search budgets, comparator contract, taxonomy, sampling algorithm, rubrics, thresholds, and invalidity rule before confirmatory output. Use post-freeze public randomness for actual held-out subjects.
- Do not bypass authentication, robots directives, rate limits, terms, licenses, or access controls. Record unavailable evidence with the exact reason; do not treat it as negative evidence.
- Store only third-party material necessary and permitted for verification. Label captures `stored`, `externally_immutable`, or `metadata_only`; do not call metadata-only evidence replayable.
- Any per-card manual intervention is timed and logged. Unlogged work or changing a binding frozen output invalidates the experiment rather than becoming a silent fix.
