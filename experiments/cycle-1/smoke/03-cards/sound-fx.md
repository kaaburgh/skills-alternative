# sound-fx — noizai/skills

Provenance-aware composite card. Every sentence below cites the claim it rests on; claims cite
observations; observations cite immutable coordinates and capture hashes. Nothing here is asserted
without a citation, and negative results are stated rather than omitted.

**Canonical identity:** source type `github`, owner/repo `noizai/skills`, skill path `sound-fx`.
Observation version: upstream commit `2a0e09d8cb9056e044c473dd53a136b81ba428e9`.

## What it does

Generates sound effects from a text description by calling the noiz.ai HTTP API [CLM-001]. It
declares `network` and `filesystem` permissions [CLM-004].

## What it costs you to run

It requires a `NOIZ_API_KEY` from the vendor and does not work without one [CLM-002]. The skill's
author and the vendor of the service it calls are the same party, so every description-level claim
about it carries a direct commercial interest [CLM-003].

## Rights

The upstream repository carries no licence, so no reuse or redistribution rights are granted by
default [CLM-005]. This is why this experiment references the upstream content by immutable commit
coordinate instead of storing a copy of it.

## Independent evidence

Three security scanners — Gen Agent Trust Hub, Socket and Snyk — are reported Pass [CLM-006].
**Their version relevance is unresolved:** the listing that republishes them does not state which
revision was scanned, so none of the three can be tied to the observed commit [CLM-006]. Each shares
a lineage with skills.sh as its republisher, though the three scanner owners are distinct from one
another [CLM-006].

Neither mandatory comparator covers this subject: SkillProof's 3,846-entry registry has no match and
Tessl returns 404 on its hierarchical key, with both positive paths proven against known-present
entries the same day [CLM-008]. No qualifying independent experience report was found within the
search budget [CLM-009].

326 installs and 523 stars are recorded [CLM-007]. That is adoption, and under the evidence-class
separation rule it says nothing about whether the skill works [CLM-007].

## Cautions a name-based lookup would miss

A different, unrelated skill shares the display name `sound-fx` — `6m1w/claude-sound-fx` plays themed
terminal notification sounds and does not generate audio [CLM-010]. Two apparently distinct
aggregator sites republish this listing as byte-identical responses, so treating them as two sources
would manufacture false independence [CLM-011].

## Evidence summary

| Class | Present | Independent of author | Version-relevant |
| --- | --- | --- | --- |
| `author_claim` | yes [CLM-001..004] | no | yes |
| `adoption` | yes [CLM-007] | yes | n/a |
| `security` | yes, ×3 owners [CLM-006] | yes | **unresolved** |
| `structural_review` | own observations only [CLM-005, CLM-010] | yes | partly |
| `empirical_efficacy` | **none found** | — | — |
| `experience_report` | **none found** [CLM-009] | — | — |

**Multi-origin decision evidence (E1 shape):** the card has three non-author security lineages under
distinct owners, which satisfies the count — but not the version-relevance requirement, because no
audited revision is stated [CLM-006]. On the rule as written this subject would **not** qualify
until the audited revision can be established. Resolving it needs the authenticated audit endpoint,
which is gated behind `SA-001`.

**Alternatives:** not populated. The frozen candidate universe is defined by the `SA-001` capture,
which does not exist yet, and this item is explicitly barred from pre-empting it. Alternatives are
`SA-009`'s to produce.
