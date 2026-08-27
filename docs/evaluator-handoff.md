# Cycle 1 evaluator handoff

This document is the repository-side procedure for `SA-000`. It prepares an independent human evaluator for the later sealed audit without claiming that an evaluator has been secured. `ROADMAP.md` remains authoritative for experiment state, eligibility, audit phases, and decision rules.

## Goal

Secure one human evaluator before any audit output is exposed. The evaluator must be independent of construction and tuning of the experiment and must not know the Cycle 1 decision thresholds while performing the audit.

The operator may explain the project goal, the evaluator role, expected workload, the fixed decision task, and the ordered audit phases. Do not provide future card outputs, held-out identities, ordering material, or threshold values during recruitment.

## Eligibility before output exposure

Before receiving any card, baseline, held-out subject, sealed ordering material, or generated rationale, the evaluator must acknowledge the declaration template at `experiments/cycle-1/04-audit/evaluator-declaration-template.md`.

The acknowledgement must establish that the evaluator:

- is a human;
- did not create or tune the pipeline, schemas, rubrics, source mappings, cards, baselines, or decision thresholds;
- has not seen Cycle 1 card outputs;
- records any relationship or conflict that could reasonably affect independence;
- has not inspected the decision thresholds and agrees not to seek them until the audit work is complete;
- understands the three ordered audit phases and the custody rules below.

A project contributor who fails any of these conditions is not made independent by signing the form.

## Recruitment and acknowledgement

1. Give the candidate only the role description, expected workload, fixed decision task, and phase description needed for informed consent.
2. Ask the candidate to disclose relevant relationship/conflict information and whether they have contributed to any prohibited construction/tuning work.
3. Keep the threshold values and all future outputs out of the recruitment packet.
4. Obtain a dated signed or otherwise durable acknowledgement of the declaration before bundle delivery.
5. Record a stable evaluator identifier and the acknowledgement artifact/coordinate. Avoid unnecessary personal data in the repository; contact details may remain outside it when the acknowledgement can still be audited.

`SA-000` is not complete merely because this procedure and template exist. Completion requires a real eligible evaluator and acknowledgement.

## Custody and phased delivery

The bundle must be delivered so later-phase information cannot leak into an earlier phase.

### Before phase 1

- Keep the ordering key, provenance reveal, correction material, and any later-phase files outside the evaluator's phase-1 package.
- Verify the evaluator acknowledgement is already recorded.
- Record the exact bundle artifact or immutable coordinate delivered and its hash when the later protocol supplies the bundle format.

### Phase 1 — untouched scoring

Deliver only the material allowed for untouched scoring by the frozen protocol. The evaluator records the fixed decision-task answers before provenance is revealed and before any cleanup/editing begins.

Generated alternative rationales remain hidden during initial alternative judgment, as required by the roadmap.

### Phase 2 — provenance and verification

Only after phase-1 results are durably recorded, reveal the provenance/native-source material permitted by the frozen protocol. Start and preserve the required cleanup timing at the protocol-defined boundary. Verification and diagnosis are part of the timed work; they are not free pre-edit inspection.

### Phase 3 — correction copy

Keep timing running as required while the evaluator edits a separate copy. Never replace or mutate the untouched object that was scored. Preserve the resulting patch/correction artifact and the timing breakdown required by the frozen protocol.

The ordering key is revealed only at the point prescribed by the later sealed-bundle protocol, after it can no longer influence earlier judgments.

## Withdrawal and replacement

If the evaluator withdraws **before seeing any audit output**, record the withdrawal without exposing outputs and recruit a replacement. The replacement must satisfy and acknowledge the same eligibility declaration before bundle delivery; the withdrawal alone does not invalidate prior pipeline work.

If withdrawal, accidental exposure, threshold exposure, or an eligibility conflict is discovered **after output exposure**, do not improvise a replacement rule or silently restart the audit. Preserve what was exposed and when, and resolve the event under the frozen protocol and Rule 0/deviation handling then in force.

## Handoff record

When an evaluator is secured, the repository record for `SA-000` should contain or reference:

- stable evaluator identifier;
- dated eligibility/threshold-confidentiality acknowledgement;
- disclosed relationship/conflict information sufficient to judge independence;
- acknowledgement that the ordered phases and custody boundary are understood;
- the contact-independent method by which the evaluator will receive phase artifacts and return results;
- any pre-output withdrawal/replacement event.

Do not store secrets, access tokens, private contact details that are unnecessary for auditability, or future card outputs in the declaration itself.

## Completion boundary

This document is procedure, not evidence that the human gate passed. `SA-000` can advance to its accepted state only after an actual evaluator satisfies the roadmap's eligibility conditions and the acknowledgement/handoff record exists. Until then, downstream work that depends on `SA-000` remains gated.