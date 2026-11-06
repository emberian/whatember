# Swarm synthesis, 2026-11-05: three Opus research lanes, cross-lane picture

The lanes' own files are the record; this page is only the join. Read them, not this.

| Lane | Files (committed, pushed) |
|---|---|
| Dark learning | zkml-research `9443850d`, `439da79c`: `docs/DARK-LEARNING-PROGRAM.md` (23 constructions C1-C23), `notes/dark-learning-foundations-critique.md` (F1-F15), `notes/dark-learning-tradeoff-space.md`, `notes/dark-learning-codex-synthesis.md`, `notes/dark-learning-scripts/` (784 constructions enumerated, 112 pass gates; bf16 backward-table census) |
| Proof-system space | zkml-research `7c75bd58`: `docs/PROOF-SYSTEM-SPACE.md`, `docs/CERTIFICATES.md`, `docs/VERDICTS.md` §9, `notes/construction-search/space.py`, `notes/selvage-foundations-critique-2026-11-05.md`, `notes/proof-system-codex-synthesis.md` |
| Silicon-to-semantics / governance | degg-research `15db978`: `research/GOVERNANCE-CLAIM-LATTICE.md`, `research/governance-foundations-critique.md`, `research/governance-codex-synthesis.md`, `research/governance-literature-notes-2026-11-05.md`, `experiments/mma-field-mapping/`, `experiments/air-census/`; redregg-notes `d1540c5c1`: `designs/SILICON-TO-SEMANTICS-ALIGNMENT-2026-11-05.md` |

Each lane ran two Codex (gpt-6-astra) rounds; each records what it adopted and refuted. Across the three, Codex
found or corrected roughly a dozen defects in our foundations and in the lanes' own first drafts.

## Where the lanes converge without having talked to each other

1. **Binding is assumed, not bought.** Proof lane: `Selvage/Commitment.lean:113` assumes perfect binding, which no
   hash-based commitment satisfies. Governance lane: receipts must carry an explicit ε and a binding leg
   (ε₁+ε₂+ε_b); "co-location is not conjunction". Dark-learning lane: the audit theorem's ε_bind leg is the one
   that carries the displacement bound 2B/q. Same seam, three directions. Repair: one computational-binding
   advantage term threaded through Selvage, CERTIFICATES.md's algebra, and the claim lattice's receipt judgment.
2. **The weld binds at lane 0 only.** Proof lane: `AttestedAutomatonWeld8` checks one lane of its 8-lane digest and
   is not routed (about 2^15.5 at the weld). Governance lane: "the policy weld forces lane 0 only." Every absence
   and policy claim in dossier 01 §5 rests on this until it is fixed.
3. **Non-omission is the hard claim, and we do not have it where it matters.** Governance lane: grain-verify
   admits a host can make calls that never get a receipt; "completeness is not non-omission." Proof lane: the DFA
   soundness statement never mentions the input word. Dark-learning lane: FHE custody cannot gate execution at all
   (Enc(W)·x for chosen x is cheap), so "no unsanctioned run of the mind" needs MPC custody. The construction that
   answers all three is the governance lane's commit-before-forward at an attested choke point, plus the
   dark-learning lane's C21 (one-time step encodings; the model never leaves the custodians).
4. **Statement shape and auditing do the work; hardware and format are second-order.** Proof lane's counts: the
   tensor-core + Lean-emitted + commit-then-audit + native-MXFP4 point is 11.7x under SASH per request and ~675x
   when audited at 1%, but tensor cores alone buy 1.49x and MXFP4 1.06x. Governance lane's counts: FP4 beats INT8
   for proving only above ~5x throughput ratio. Dark-learning lane: at p = 0.01 the every-step displacement cap is
   71% of cost, so sampling stops paying below that. All three say: spend on the statement and the audit game.
5. **Our security numbers are stale in our favor.** Deployed proofs carry 34 provable bits (unique decoding); the
   Johnson 73 rests on an unproved hypothesis in our own Lean. The FHE confidentiality proof at deployed parameters
   fails at 10^6 steps (2^-14.2 against 2^-40) and a 61-bit single prime cannot fit the smudge; N = 8192 is forced.
   FRONTIER-QUEUE G1 "single prime dissolves both holes" is stale: it fixes one.

## What the world looks like after today's reads

- FlashProve (Anthropic, 11-02) is the inference prover; compose, do not re-prove. Our audit theorem is the thing
  only we have; instantiate it over FlashProve's soundness statement.
- ArkLib is at 4 live sorries, same toolchain and Mathlib pin as minidregg: import correlated agreement and ring
  switching, mirror FRI and sumcheck, keep our RBR-to-FS/BCS compiler, state restoration and accumulation depth.
- BinarySpartan (2026/1656) and Magnetar (2026/2423) are public and prove 100-120 bits in unique decoding.
- Prior art the notes must now cite: PRISM 2026/1956 (cross-limb binding), Reef 2023/1886 (ZK regex absence over
  committed documents), ZkAudit 2404.04500 (served = evaluated, eval absence), Peigné v3 (sampled step audits,
  but not our rank-1 / low-rank / derived-backward-table ideas; and the derived backward table is refuted by
  census anyway: sigmoid 148, tanh 190, GELU 412, SiLU 751 bf16 codes).

## The constructions the lanes rate highest (their IDs)

- Governance (b)+(g) commit-before-forward at an attested choke point; (c) quote and proof opening one typed
  statement; (d)+(h) one Lean function emitting AIR and RTL with ZK-CEC netlist equivalence; (i)+(l) receipts
  carrying their own ε and assumptions.
- Dark learning C21 (no reusable model leaves the custodians), C2 (sampled step audits + every-step displacement
  cap, with the Lean statement Codex wrote), C8 (decrypt only on proof; restricted IND-CPA-D), C23 (contractive
  learner bounds lasting damage), C22 (expiring custody keys).
- Proof space U1 (the audited tensor-core/Lean/MXFP4 point), U3 (policy automaton fused into inference output),
  U8 (blowup drop as a per-descriptor knob, global form refuted), U6 (proof-carrying prefix/KV reuse), U9
  (binary-field hash-native wrap of FlashProve proofs).

## The three hbox experiments the lanes want first (all counts-based, all under swarm-build, all filtered)

1. `recursion_tower_profile` at (6,19,16), (6,86,16), (2,57,16), (2,148,0) plus a 2^16-row zkML child: prices the
   34 to 100-bit fix in the wrap and decides the blowup drop per descriptor.
2. One ct×ct with its integer rescale certificate three ways (native p61, PRISM-style RNS-202@8192, row-interleaved;
   predicted 159,744 / ~1.06M felts) plus the wire cost of one fused activation/derivative crossing at N = 8192:
   decides the FHE-versus-MPC fork for dark learning.
3. Lower `commitFrame` (MMR append over Blake3) through the existing Pancake emitter, prove `commit_before_forward`
   for one step, serve behind the demo flag. Cheap in parallel: the two new residual_trust arms; parse a public
   NVIDIA CC attestation sample with tee-verify (it has no NVIDIA support today).

## Decisions that are ember's

- FHE custody vs MPC custody for the mind (dark-learning F11 and C21): the welfare argument now points at MPC.
- The flag day: landing the `num_queries` pin and the binding-term repair rotates VKs and re-emits 132 goldens.
- Whether Selvage imports ArkLib (same pin) or keeps mirroring.
- Which of the three hbox experiments runs first; they are independent and could run as three lanes.

## Lieutenant handoff

The three lanes hold the context. Resume them (SendMessage) rather than briefing successors; each already has its
first experiment designed. If they must be succeeded, `cv distill` them, do not re-brief from this page.
