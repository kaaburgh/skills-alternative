# Cycle 1 independent evaluator declaration — SA-000 record

**Status: PENDING OPERATOR COMPLETION AND EVALUATOR ACKNOWLEDGEMENT**

This is the concrete `SA-000` evaluator record derived from `evaluator-declaration-template.md`. Complete every `[TODO]`, resolve every unchecked statement, and obtain durable evaluator acknowledgement of the completed record **before** this pull request is merged or any Cycle 1 audit output is exposed.

A prior agreement to help with the project may be recorded below, but it substitutes for acknowledgement of this declaration only if the referenced message explicitly covers the eligibility, confidentiality, custody, and post-audit commitment stated here.

## Recruitment record

- Evaluator identifier: `[TODO: stable identifier; avoid unnecessary personal data]`
- Role / expected contribution description provided on (UTC): `[TODO]`
- Candidate agreement to take the role received on (UTC): `[TODO]`
- Durable reference to that agreement: `[TODO: message/export/other coordinate, or explain how it is retained outside the repository]`
- Contact-independent handoff method for phase artifacts and returned results: `[TODO]`

## Eligibility declaration

By acknowledging this completed record, the evaluator states that:

- [ ] I am a human evaluator.
- [ ] I did not create or tune the Cycle 1 pipeline.
- [ ] I did not create or tune its schemas.
- [ ] I did not create or tune its evaluation rubrics.
- [ ] I did not create or tune its source mappings.
- [ ] I did not create or tune its cards or baseline views.
- [ ] I did not choose or tune its decision thresholds.
- [ ] I have not seen Cycle 1 card outputs before this acknowledgement.
- [ ] I have not inspected the Cycle 1 decision thresholds and will not seek them until my required evaluator work is complete.

Any uncertainty or exception must be recorded below before output exposure.

## Relationship and conflict disclosure

Describe any relationship to the project, repository owner, skill authors/providers, catalogs, or other circumstance that could reasonably affect independence. Write `none known` only when that is accurate.

Disclosure: `[TODO]`

## Audit and custody acknowledgement

The evaluator understands that the audit is intentionally phased and that later-phase information must not influence earlier judgments.

- [ ] I will complete and durably record the untouched scoring phase before receiving the provenance/native-source reveal permitted for the next phase.
- [ ] I understand that cleanup timing begins at the protocol-defined reveal boundary and includes the verification and diagnosis work required by the protocol.
- [ ] I will edit only a separate correction copy and will not replace or mutate the untouched object that was scored.
- [ ] I will not use generated alternative rationales during the initial alternative judgment when the protocol keeps them hidden.
- [ ] I will preserve required results, timing records, corrections, and other audit artifacts through the agreed handoff path.
- [ ] I understand that sealed ordering material is handled according to the later frozen audit protocol rather than revealed early.

## Post-audit SA-013 commitment

After the three audit phases are complete and their results are committed and hash-bound, the same evaluator is used for the independent `SA-013` evidence-classification check.

- [ ] I agree to complete the required post-audit `SA-013` re-derivation sample when it is released to me.
- [ ] I understand that the frozen protocol may require an expanded re-derivation, potentially covering all 200 E1/E2 classifications, if the sample does not validate the first pass; I agree to complete that required expansion or to report inability/withdrawal rather than silently substituting another procedure.
- [ ] I will not inspect or seek Cycle 1 decision thresholds while this post-audit evaluator work remains incomplete.

## Withdrawal and exposure

- [ ] I understand that I may withdraw before seeing audit outputs; a replacement must independently satisfy the same declaration before receiving them.
- [ ] If I accidentally see withheld output, threshold information, ordering material, or another later-phase artifact early, I will record what I saw and when rather than continuing silently.

## Durable acknowledgement

- Name or stable evaluator identifier: `[TODO]`
- Acknowledged on (UTC): `[TODO]`
- Signature / durable acknowledgement reference: `[TODO]`
- Operator verification that acknowledgement was obtained before output exposure: `[TODO: date/reference]`

## SA-000 completion note

Do not convert this record from `PENDING` or mark `SA-000` complete merely because the candidate agreed to help. Before merge, confirm that the completed record establishes evaluator eligibility, threshold confidentiality, phased custody, the post-audit `SA-013` commitment, and a durable acknowledgement without exposing card outputs.

`ROADMAP.md` is authoritative. `docs/evaluator-handoff.md` defines the repository-side handoff procedure.