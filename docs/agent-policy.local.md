## Experiment-specific policy

This repository exists to answer one product question, not to accumulate catalog infrastructure.

- The Cycle 1 result is a frozen data prototype and a pre-committed Keep/Pivot/Kill decision. Do not build a public UI, production database, continuous crawler, recommendation feed, accounts, or branding before that gate.
- Preserve raw observations separately from normalized claims and synthesized conclusions. Every decision-relevant claim must identify its original source owner, direct URL, retrieval or test date, subject version/hash when available, evidence method, and material conditions such as model or harness.
- An aggregator and the provider whose result it republishes are not independent sources. Reposts, mirrors, forks, and claims derived from the same underlying run count once.
- Do not collapse structural review, static security scanning, task execution, adoption counts, author claims, and user reports into one “quality” score. Keep the evidence type and limitations visible.
- Label differing results as contradictions only when they address the same proposition under materially comparable conditions. Otherwise preserve the difference as context or non-comparability.
- Do not bypass authentication, robots directives, rate limits, or access controls. Record unavailable evidence as unavailable with the exact reason; do not silently treat it as negative evidence.
- Freeze the cohort, audit sampling rule, rubrics, and decision thresholds before generating the final cards. Do not tune them after seeing the final audit result.
- Store only the third-party material necessary to verify the experiment and permitted by the source. Prefer URLs, immutable revisions, hashes, structured facts, and short attributed excerpts over republishing whole pages.
