# Prompt Architect v0.4.0-rc.2

First reproducible release candidate of Prompt Architect V0.4.

## Status

- Architecture: FROZEN
- D01–D12: CLOSED
- Release baseline: VERIFIED
- Clean-checkout reproducibility: PASS
- Immutable rollback tags: AVAILABLE
- Real-model runtime validation: PENDING

## Verification

- V0.3 protected baseline: MATCH 24 / DIFF 0
- V0.4 release baseline: MATCH 21 / DIFF 0
- README reverse references: 28 / 28
- Clean checkout from this tag: PASS

## Important

This release candidate does **not yet claim real-model runtime validation**.

Promotion to `v0.4.0` Stable requires SHIP-02 runtime smoke tests:

- A — Authorization ≠ value acceptance
- B — Notification timing
- C — Priority / fairness / notification ownership

## Release history

- `v0.4.0-rc.1` is retained as an immutable historical tag.
- `v0.4.0-rc.2` fixes clean-checkout reproducibility caused by line-ending normalization.

## Promotion

If SHIP-02 A/B/C all pass:

1. Commit the runtime evidence record.
2. Re-run FRG-01 / FRG-02 / FRG-07.
3. Tag the evidence-containing commit as `v0.4.0`.
4. Publish `v0.4.0` as the Stable release.
