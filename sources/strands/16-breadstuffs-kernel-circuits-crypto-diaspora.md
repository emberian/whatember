# Strand 16 — Breadstuffs Kernel, Circuits, FHE (`fhegg-*`), and Cryptography Diaspora

Primary-source technical archaeology dossier, written 2026-11-02 from the repositories, git histories,
agent session transcripts, per-project memory records, and verified mathematical corpora across
`/Users/ember/dev/breadstuffs`, `/Users/ember/dev/minidregg`, `/Users/ember/dev/nanodregg`,
`/Users/ember/dev/obend`, `/Users/ember/dev/zkml-research`, `/Users/ember/dev/plonky3-recursion`, and
`/Users/ember/dev/o7vn`. Hellas is not part of this strand's ownership property; where the record mentions
it, it appears strictly as biographical context (Ember worked at Hellas on workload verification, and
the architecture Ember was creating evolved into Dregg after leaving; Hellas handled reproducible-numeric
workloads, while Dregg centered on capability-secure distributed systems).

Every number, commit SHA, file path, line citation, and theorem statement below was inspected on
2026-11-02 from the primary source trees.

---

## 0. Executive Ledger & Corpus Grounding

### 0.1 Primary Source Ledger

| System / Subsystem | Repository / Memory Path | Primary Artifacts & Grounding Records |
|---|---|---|
| **Core Kernel & State** | `/Users/ember/dev/breadstuffs/{cell, cell-crypto, turn, turn-prover, exec-lean, dregg-lean-ffi}` | `CORE-AUDIT.md` (2026-07-03, workflow `wf_68020930-db3`), `memory/project-dregg2-architecture.md`, `memory/project-dregg2-three-projections.md` |
| **Circuit Emission & Law #1** | `/Users/ember/dev/breadstuffs/{circuit, circuit-prove, metatheory, constraint-lowering}` | `docs/CIRCUITS-FROM-PROOFS.md`, `GOAL-STARK-KILL.md`, `circuit-prove/tests/law1_enforcement_gate.rs` (commit `19439d261`), `memory/project-lean-authored-air-law.md` |
| **Verified Rotated Layout** | `/Users/ember/dev/breadstuffs/metatheory/Dregg2/Circuit/Emit/` & `turn/src/rotation_witness.rs` | `EffectVmEmitRotationV3.lean` (`rotated178`), commit `94217ed3c` (2026-07-18), `memory/project-rotated-layout-single-source.md` |
| **Plonky3 Recursion & IVC** | `/Users/ember/dev/plonky3-recursion` & `/Users/ember/dev/breadstuffs/recursion-verify` | Commit `af3f6cc` (2026-06-26, `ExposeClaim`, `pin_preprocessed_commit`, `NativeBatchStark`), `52e1fab` (FRI query configuration), `memory/project-universal-fold-buff-lightclient.md` |
| **FHE Accelerator (`fhegg-*`)** | `/Users/ember/dev/breadstuffs/{fhegg-core, fhegg-fhe, fhegg-rtl, fhegg-solver}` | `fhegg-rtl/` (commit `217062e2d`), `fhegg-core/src/bfv_lean.rs`, `fhegg-solver/src/pdhg.rs`, `HBOX-24CORE-ENVELOPE.md`, `GOAL-FRI-PRODUCT.md` |
| **Experimental Cryptography** | `/Users/ember/dev/breadstuffs/{crypto-hermine, crypto-tanuki, crypto-traccoon, crypto-xmvrf, crypto-hashrand}` | Commits `62741cc2e` (Tanuki), `67395c5fb` (workspace fold), `e91d88b84` (`CratesOutsideCI`), `metatheory/Dregg2/Crypto/{HermineThreshold, VRF, RandomnessBeacon}.lean` |
| **Isabelle / CryptHOL** | `/Users/ember/dev/breadstuffs/uc-crypthol/` | Commit `e17b9da35` (2026-06-07), `Dregg2_FCom.thy`, `Dregg2_Carriers.thy`, `Dregg2_FDregg.thy`, `memory/reference-uc-crypthol-isabelle.md` |
| **Diaspora: Mini Admission** | `/Users/ember/dev/minidregg` | `memory/project-no-proof-system-in-mini-admission.md`, `Pred/Satisfiable.lean` (Farkas `SysCert`), `Compiler/PredCompile.lean` (`Pred.witnessed` $\to$ `false`), `Kernel/Run.lean` (`checkRun_sound`, `no_accepted_of_output_mismatch`) |
| **Diaspora: Silicon Compiler** | `/Users/ember/dev/obend` | `AMBITION.md`, `SILICON-ELABORATOR.md`, `Obend/Hardware/ReductionMachine.lean`, `Obend/Lower/Proofs/Hardware.lean` |
| **Diaspora: $p_{61}$ vFHE** | `/Users/ember/dev/zkml-research` | `notes/fold-as-opening.md`, `Theory/CyclotomicInertia.lean` (`p61_prime`, $p = 127 \cdot 2^{54} + 1$), `research/vfhe_2026_09_08/` |
| **Diaspora: Isabelle / MLton** | `/Users/ember/dev/o7vn` | `src/isabelle/Veri7vn_Inspection.thy`, `Fold_Cascade.thy`, `tools/fusion/` |

---

### 0.2 Three Necessary Corrections to the Narrative

1. **Law #1 was not an aspirational stylistic preference; it was an AST-level CI ratchet.**
   The tenet "Circuits are emitted from Lean; zero Rust-authored constraints or AIRs, ever" was
   enforced by an AST scanner in `circuit-prove/tests/law1_enforcement_gate.rs`. When
   it broke on 2026-07-30 (commit `81ee5492d`), Ember spent 25 hours hunting the attribution failure,
   landing commit `19439d261` on 2026-07-31 to distinguish `Construct` (hand-authoring algebra) from
   `Pattern` (destructuring emitted IR), adding line-attributed compiler diagnostic reporting so no
   engineer could ignore a gate failure.
2. **Mini did not drop proof systems because proving was "too slow"; it dropped them because the back-half STARK soundness was unproven while re-execution was sound and immediate.**
   On 2026-10-01 (`project-no-proof-system-in-mini-admission.md`), Ember observed that while the front-half
   compiler (logic to constraints) was verified in `Compiler/Air.lean`, the back-half PCS was empty
   (`Tower256MerkleCardinalityCore`), the conjectured 130-bit STARK yielded only 51–73 bits proven, and
   `Pred.witnessed vk` literally compiled to `false` in `Compiler/PredCompile.lean`. Mini chose level-3
   re-execution (`Kernel/Run.lean`, `checkRun_sound`) because deterministic re-execution, access control,
   and value conservation covered 100% of user properties without carrying an unsound cryptographic dependency.
3. **The experimental crypto crates (`crypto-*`) were not abandoned due to cryptographic breaks; they were clean reference implementations parked because they were synchronous islands in an asynchronous world.**
   `crypto-hermine`, `crypto-tanuki`, `crypto-traccoon`, `crypto-xmvrf`, and `crypto-hashrand` were
   fully functional, passing 55 tests (`67395c5fb`). They implemented synchronous cores with trusted dealers
   or round barriers, whereas Dregg required fully asynchronous Byzantine fault tolerance with distributed
   key generation (DKG) and weak-VSS. They were parked pending an asynchronous network substrate that could
   host them faithfully.

---

## 1. What Lived in `breadstuffs` (The Monolithic Engine)

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │               BREADSTUFFS MONOREPO                     │
                                    │          (346 crates, ~1.2M lines Rust/Lean)           │
                                    └───────────────────────────┬────────────────────────────┘
                                                                │
         ┌───────────────────────┬──────────────────────────────┼──────────────────────────────┬─────────────────────────┐
         │                       │                              │                              │                         │
         ▼                       ▼                              ▼                              ▼                         ▼
┌──────────────────┐   ┌───────────────────┐        ┌───────────────────────┐      ┌───────────────────────┐   ┌───────────────────┐
│   CORE KERNEL    │   │   CIRCUIT-EMIT    │        │      FHEGG STACK      │      │  EXPERIMENTAL CRYPTO  │   │    UC-CRYPTHOL    │
│  & EXEC-LEAN FFI │   │     (LAW #1)      │        │    (FHE & ACCEL)      │      │    (POST-QUANTUM)     │   │ (ISABELLE PROOFS) │
├──────────────────┤   ├───────────────────┤        ├───────────────────────┤      ├───────────────────────┤   ├───────────────────┤
│ • dregg-cell     │   │ • EffectVmDesc2   │        │ • fhegg-core (BFV)    │      │ • crypto-hermine      │   │ • Dregg2_FCom.thy │
│ • dregg-turn     │   │ • rotated178      │        │ • fhegg-fhe (WGPU/PBS)│      │ • crypto-tanuki       │   │ • Dregg2_FDregg   │
│ • dregg-exec-lean│   │ • p3-recursion    │        │ • fhegg-solver (PDHG) │      │ • crypto-traccoon     │   │ • Dregg2_Carriers │
│ • libdregg_lean.a│   │ • 8 folded leafs  │        │ • fhegg-rtl (Lean-HDL)│      │ • crypto-xmvrf        │   │ • AFP matched pair│
│ • CORE-AUDIT     │   │ • AST CI Ratchet  │        │ • fold-opening        │      │ • crypto-hashrand     │   │ • FComDischarge   │
└──────────────────┘   └───────────────────┘        └───────────────────────┘      └───────────────────────┘   └───────────────────┘
```

### 1.1 The Core Kernel & State Transition Engine

The core operational kernel of `breadstuffs` lived across three tightly coupled layers:
- **`cell` (`dregg-cell`)**: The capability-secure agent cell model. Cells are isolated execution contexts
  possessing typed memory slots, capability tables, and authority bounds. Key source files:
  - `cell/src/cell.rs`: Core `Cell` struct, capability attenuation, and facet dispatch.
  - `cell/src/ledger.rs`: Multi-cell ledger mapping cell addresses to states.
  - `cell/src/nullifier_set.rs` & `commitment_set.rs`: Accumulator tracking state evolution without linkability.
  - `cell/src/prepaid_lease.rs`: Gas-metering and execution lifespan management.
- **`turn` (`dregg-turn`)**: The atomic transactional turn execution framework. Turns are structured as
  call forests with rollback semantics. Key source files:
  - `turn/src/action.rs`: Transactional action variants (transfers, capability mints, contract calls).
  - `turn/src/rotation_witness.rs`: Witness generation mapping execution states into layout columns.
  - `turn/src/collapse.rs`: Turning a multi-agent call tree into an atomic ledger delta.
- **`exec-lean` (`dregg-exec-lean`) & `dregg-lean-ffi`**: The boundary where Rust yields authority to Lean.
  - `exec-lean/src/lean_shadow.rs` & `lean_apply.rs`: Differential execution harness linking `libdregg_lean.a`.
    Every state transition executed by Rust was shadowed in Lean; any discrepancy triggered a strict veto.
  - `dregg-lean-ffi/src/lean_direct.rs`: Zero-copy C-ABI boundary transporting Lean runtime objects.

#### The 2026-07-03 Soundness Reckoning: `CORE-AUDIT.md`
On 2026-07-03, workflow `wf_68020930-db3` subjected `starbridge-v2` and `turn` to an adversarial audit.
Out of 21 findings, 19 survived ruthless skeptical refutation. Five structural findings exposed deep fault lines:
1. **Finding #1/#3 (Durable overlay incomplete change-set — SOUNDNESS)**:
   In `starbridge-v2/src/world/world.rs:1574-1602`, `collect_touched` matched only ~13 of 30+ `Effect` variants.
   Operations like `Effect::Burn` (crediting the token well), `Effect::Mint`, `CreateCell`, and
   `ExerciseViaCapability` mutated cells that were never recorded in `touched`. When `dual_write` committed
   to disk, `ledger_root` held the true post-root, but the overlay held only partial state. On crash and restart,
   `persist.recover()` computed `checkpoint ⊕ overlay`, observed `canonical_ledger_root(reconstructed) != recovered_ledger_root()`,
   failed with `OpenError::Divergent`, and either refused to boot or silently truncated committed turns.
   *The Fix:* The executor exposed its exact journal write-set (`LedgerJournal::touched_cells` $\to$
   `TurnExecutor::last_write_set`); `world.rs` `dual_write` recorded `touched ∪ executor.last_write_set()`.
2. **Finding #2 (Unrolled commit rejection desync — SOUNDNESS)**:
   In `commit_turn` (`world.rs:1109-1268`), the state transition applied in-RAM *before* writing to disk:
   `engine.execute_turn` mutated the ledger, `history.record_commit` recorded the step, and `self.height += 1` ran.
   If disk I/O failed in `p.dual_write`, the code returned `CommitOutcome::Rejected` *without rolling back*
   the engine, height, or chain head. Control never reached `self.receipts.push`, leaving receipts desynced
   from height (`receipts.len() == height - 1`), while subsequent submissions suffered confusing double-spend rejections.
3. **Finding #4 (deploy_factory executor-bypass — SOUNDNESS)**:
   The factory-birth path bypassed the executor entirely (like genesis), emitting neither a `CommitRecord` nor a
   journal write-set. Durable overlay replication had to remain opt-in until factory births were enclosed in journals.
4. **Finding #6 (Dynamics forest-depth truncation — CORRECTNESS)**:
   Dynamics derivation walked only top-level nodes, dropping nested cell creations. Fixed via `CallTree::iter_dfs`.
5. **Finding #7 (Engine-twin AddToSlot overflow — CORRECTNESS)**:
   Checked math was missing on `AddToSlot`, causing panic on saturating balance arithmetic; fixed to match `SubFromSlot`.

---

### 1.2 Circuit-Emit, Architectural Law #1, and Rotated Layout Single-Source

#### Architectural Law #1: Zero Rust-Authored Constraints
As documented in `metatheory/README.md:15` and `docs/CIRCUITS-FROM-PROOFS.md`:
> *"Circuits are emitted from Lean (architectural law #1: zero Rust-authored constraints or AIRs, ever).
> Every constraint set the prover enforces is a byte-pinned artifact emitted from a proved Lean module
> (the Argus IR and the descriptor JSONs); Rust only interprets those artifacts. A coverage gap is closed
> by emitting from a new proved module, never by hand-authoring a constraint."*

The soundness boundary is absolute: a STARK verifier accepts exactly what the polynomial constraint system admits.
A bug in a Rust witness generator causes a proof generation failure (a liveness bug). But a bug or omission in
a constraint causes the verifier to accept invalid transitions (a catastrophic soundness break).
This was proven painfully when `predicate-arith.json` was briefly hand-edited on disk, inadvertently omitting
both Poseidon2 weld legs.

#### The Dual-Rung Verification Ladder
Every circuit family in `metatheory/Dregg2/Circuit/Emit/` was required to climb two rungs:
- **Rung 1 (Functional Refinement)**: The descriptor row semantics equal the intended specification.
- **Rung 2 (Semantic No-Forgery Teeth)**: Proof that invalid transitions are rejected.

In `metatheory/Dregg2/Circuit/Emit/EffectVmEmitTurnChainBinding.lean`:
```lean
/-- Rung 1: The canonical lookup is EXACTLY the genuine per-row hash equation. -/
theorem perRowHash_canonical_iff (hash : List ℤ → ℤ) (env : VmRowEnv)
    (isFirst isLast : Bool) :
    perRowHash hash env isFirst isLast ↔
      (isFirst = false ∧ isLast = false →
        env.loc Chain.ACC_OUT = hash [env.loc Chain.ACC_IN, env.loc Chain.OLD_ROOT,
                                      env.loc Chain.NEW_ROOT, env.loc Chain.IDX])

/-- Rung 2: Adversarial tooth — broken continuity is rejected by the window constraints. -/
theorem turnChain_rejects_broken_continuity
    (hash : List ℤ → ℤ) (tf : TraceFamily) (env : VmRowEnv) (isFirst : Bool)
    (hnew : 0 ≤ env.loc Chain.NEW_ROOT ∧ env.loc Chain.NEW_ROOT < 2013265921)
    (hold : 0 ≤ env.nxt Chain.OLD_ROOT ∧ env.nxt Chain.OLD_ROOT < 2013265921)
    (hbad : env.loc Chain.NEW_ROOT ≠ env.nxt Chain.OLD_ROOT) :
    ¬ turnChainWindowHolds hash tf env isFirst false

/-- Rung 2: Adversarial tooth — non-unit step increments are rejected. -/
theorem turnChain_rejects_bad_idx_step
    (hash : List ℤ → ℤ) (tf : TraceFamily) (env : VmRowEnv) (isFirst : Bool)
    (hidx : env.nxt Chain.IDX ≠ env.loc Chain.IDX + 1) :
    ¬ turnChainWindowHolds hash tf env isFirst false

/-- Rung 2: Adversarial tooth — corrupted real-turn counts are rejected. -/
theorem turnChain_rejects_bad_real_count
    (hash : List ℤ → ℤ) (tf : TraceFamily) (env : VmRowEnv) (isFirst : Bool)
    (hbad : env.nxt Chain.REAL_COUNT ≠ env.loc Chain.REAL_COUNT + env.nxt Chain.IS_REAL) :
    ¬ turnChainWindowHolds hash tf env isFirst false
```

#### The AST Enforcement Ratchet: Commit `19439d261`
On 2026-07-31, Ember landed commit `19439d261` (`law #1 has been RED for a day, and the reason nobody owned
it is that the message was a number`). The gate in `circuit-prove/tests/law1_enforcement_gate.rs`
parsed the AST of the entire Rust workspace, tracking five distinct dialects of constraint authoring:
1. **Plonky3 symbolic**: `x.assert_zero(..)` on any receiver, plus `.when_transition(..)` in `AirBuilder` files.
2. **Closures**: `eval: Box::new(|row, _, pi| ..)` bypassing symbolic builders.
3. **`ConstraintExpr` literals**: Direct constructions of the AST enum.
4. **Descriptor gate trees**: Hand-assembled `LeanExpr`, `VmConstraint`, or `VmConstraint2` nodes (the exact
   trick used by `shielded_ring_clearing_air.rs` before it was deleted).
5. **`air_accepts` predicates**: Rust functions deciding row validity.

The commit made the AST counter differentiate between *authored* algebra (`Site::Construct`) and *destructuring*
lowering (`Site::Pattern`):
```rust
// circuit-prove/tests/law1_enforcement_gate.rs:
// For dialects (3) and (4) the same text `ConstraintExpr::Binary { col }` is either
// construction (algebra originates here — authoring) or destructuring (algebra arrived
// from somewhere else and is being read — lowering / interpreting).
// classify_site decides it syntactically:
//   * a `..` rest inside the braces is pattern-only,
//   * a following `=>` or `|` is a match arm,
//   * `matches!`, `if let`, `while let`, `let .. =` are patterns,
//   * anything else constructs.
```

#### The `rotated178` Single-Source Breakthrough
Before July 2026, column layout indices were maintained in two places: hand-typed arrays in Rust (`cell/src/commitment.rs`
and `turn/src/rotation_witness.rs`) and column assignments in Lean. Inevitable off-by-one shifts caused silent
verification failures.
On 2026-07-18, commit `94217ed3c` (`circuit: finish single-source verified rotated layout`) closed this:
- `metatheory/Dregg2/Circuit/Emit/EffectVmEmitRotationV3.lean` defined `rotated178`, proving that 178 occupied
  columns formed a complete tiling under `Legal`.
- All seven deployed emit group-columns (capabilities, heap, fields, nullifiers, commitments, revocations, cells)
  were defined as literal projections `rotated178.groupCol`.
- Rust producers (`write_lanes` and `rotation_witness.rs`) imported the generated constants directly.
- `check-descriptor-drift.sh` enforced zero byte drift across all 105 descriptor JSONs and 67 field constants.

---

### 1.3 The STARK-Kill and Plonky3 Recursion Engine

As documented in `GOAL-STARK-KILL.md`, Breadstuffs launched a campaign to completely annihilate
`circuit/src/stark.rs` (an $O(n^2)$ legacy hand-rolled STARK prover) and ~45 hand-authored AIRs, migrating
to Plonky3 IR2 (`p3_batch_stark::BatchProof` returned by `prove_vm_descriptor2`).

#### The Plonky3-Recursion Fork (`/Users/ember/dev/plonky3-recursion`)
Plonky3 out-of-the-box lacked IVC (Incrementally Verifiable Computation) primitives. In commit `af3f6cc`
(2026-06-26), Ember added the missing IVC scaffolding:
1. **`expose_as_public_output` / `ExposeClaim`**: A verified channel allowing child circuits to pass state
   to parents via public inputs.
2. **`pin_preprocessed_commit`**: In-circuit verification key identity binding, preventing an attacker from
   swapping the circuit being recursed upon.
3. **`verify_p3_native_batch_proof_circuit` (`RecursionInput::NativeBatchStark`)**: Recursive verification
   of batch STARK proofs inside BabyBear.
4. **`52e1fab` (FRI Query Configuration)**: Ensuring query counts in FRI verification are fixed by the verified
   verifier configuration rather than read off the untrusted proof header.

#### Universal Fold Buff Lightclient
Documented in `memory/project-universal-fold-buff-lightclient.md`, Ember collapsed the dual-artifact split
(per-turn effect-vm VK vs whole-chain recursion tree). All 8 sub-proof carriers were turned into recursive
IR-v2 leaves:
- `Bridge`, `Custom`, `Deco`, `Dsl`, `Factory`, `Hatchery`, `Membership`, `Sovereign`.
- Each carrier implemented `prove_*_binding_node_segmented`, allowing a pure light client to witness every
  transition that a full validator re-executes.

---

### 1.4 The FHE Subsystem (`fhegg-*`)

The `fhegg` subsystem was designed as a zero-leakage, confidential dark pool and encrypted state engine:
- **`fhegg-core`**: Core BFV (Brakerski-Fan-Vercauteren) and TFHE primitives.
  - `fhegg-core/src/bfv_lean.rs`: Ciphertext representation over RNS (Residue Number System) limbs.
    Implemented `fold_add(a, b, t)`—coefficient-wise modular addition with wrap guards preventing plain-bound overflow:
```rust
pub fn fold_add(
    a: &LeanCiphertext,
    b: &LeanCiphertext,
    plaintext_modulus: u64,
) -> Result<LeanCiphertext> {
    check_compatible(a, b)?;
    let bound_sum = u128::from(a.plain_bound) + u128::from(b.plain_bound);
    if bound_sum >= u128::from(plaintext_modulus) {
        return Err(BfvLeanError::WrapRefused { bound_sum, plaintext_modulus });
    }
    Ok(rns_add_raw(a, b, bound_sum as u64))
}
```
- **`fhegg-fhe`**: High-performance cryptographic execution.
  - WGPU-accelerated blind rotations (`tfhe_blind_rotation_wgpu.rs`), CMUX gates, and NTT crossover algorithms.
  - Exact private order books (`private_book_bfv_exact.rs`) and distributed MPC MAC checks.
  - Measured envelopes (`HBOX-24CORE-ENVELOPE.md`) benchmarking NTT performance on 24-core hardware.
- **`fhegg-solver`**: Fast untrusted Stage-1 clearing solver.
  - `fhegg-solver/src/pdhg.rs`: Primal-Dual Hybrid Gradient flow-LP for uniform-price auction clearing.
  - Emits `Cert-F` primal-dual certificates. The untrusted Rust solver solves the LP; the Lean-verified
    checker validates optimality and clearing bounds in milliseconds.
- **`fhegg-rtl` (`fhegg-rtl/`)**: Hardware acceleration spine (Commit `217062e2d`, 2026-07-14).
  - Built a compiling Lean 4 netlist DSL $\to$ Verilog emitter (`lean/Fhegg/Rtl/Netlist.lean`).
  - Proved `fullAdder_realizes` (`Examples/FullAdder.lean`):
```lean
def fullAdder : Netlist where
  nInputs := 3
  gates :=
    [ .xor (.inp 0) (.inp 1)      -- w0 = a ⊕ b
    , .xor (.gate 0) (.inp 2)     -- w1 = w0 ⊕ cin      (sum)
    , .and (.inp 0) (.inp 1)      -- w2 = a · b
    , .and (.gate 0) (.inp 2)     -- w3 = w0 · cin
    , .or  (.gate 2) (.gate 3) ]  -- w4 = w2 ∨ w3       (carry)
  outputs := [ .gate 1, .gate 4 ]

def fullAdderSpec (ins : List Bool) : List Bool :=
  let a := ins.getD 0 false
  let b := ins.getD 1 false
  let c := ins.getD 2 false
  [ xor (xor a b) c, (a && b) || (xor a b && c) ]

theorem fullAdder_realizes : RealizesSpec fullAdder fullAdderSpec := by
  intro ins
  simp only [evalNetlist, fullAdder, evalGates, List.foldl, evalGate, evalRef, List.map, fullAdderSpec]
  cases ins.getD 0 false <;> cases ins.getD 1 false <;> cases ins.getD 2 false <;> rfl
```
  - Provided golden models for the NTT butterfly (`Golden/Butterfly.lean`) and mint-safe accumulator
    (`Golden/Accumulator.lean`) to co-simulate against SpinalHDL FPGA designs.

---

### 1.5 The Experimental Cryptography Frontier (`crypto-*`)

Breadstuffs incubated five advanced post-quantum and lattice cryptographic reference implementations:

#### 1. `crypto-hermine` (Hermine Lattice Threshold Signature)
- **Specification:** Pinned to IACR ePrint 2026/419 and Lean files `metatheory/Dregg2/Crypto/HermineThreshold.lean`
  and `HermineExtractor.lean`.
- **Algebra:** $n = 256$, Dilithium prime $q = 8380417$. Verification equation:
  $$A \cdot z = w + c \cdot t \pmod q$$
  where $s = \sum \lambda_i s_i$, $z_i = y_i + c \cdot (\lambda_i s_i)$, $w = A \sum y_i$, $t = A \cdot s$.
- **Noise Flooding:** Implemented in `metatheory/Dregg2/Crypto/Smudging.lean`. Uses a discrete Gaussian CDT
  sampler to achieve statistical zero-knowledge hiding of individual key shares (statistical distance $\le B/M$).
- **Extraction:** Proved `hermine_special_soundness_extracts_relation`—two transcripts with identical $w$
  and differing challenges $c, c'$ extract the secret preimage $(c - c')^{-1} (z - z')$.

#### 2. `crypto-tanuki` (Tanuki 2-Round Lattice Threshold Signature)
- **Specification:** Pinned to NIST MPTS 2026, EKT24 (CRYPTO 2024), and Ringtail (Oakland 2025).
- **Architecture:** Two-round (1 offline, 1 online) threshold signature over $R_q = \mathbb{Z}_q[X]/(X^n + 1)$.
- **Commit `62741cc2e`:** Provided a reference implementation with rounded MLWE keys $t \leftarrow \lfloor A s + e \rceil$,
  pairwise zero-sum PRF masking seeds, and Shamir secret sharing over polynomial rings.

#### 3. `crypto-traccoon` (Threshold Raccoon / TRaccoon)
- **Specification:** Pinned to Eurocrypt 2024 (del Pino, Espitau, Katsumata, Maller, Mouhartem, Prest, Saarinen, Takemure).
- **Architecture:** 3-round lattice threshold signature (`commit` $\to$ `reveal` $\to$ `masked-respond`) with
  one-time additive row/column masks. Served as the cited-proven baseline against which Hermine was measured.

#### 4. `crypto-xmvrf` (Key-Updatable Post-Quantum VRF)
- **Specification:** Pinned to IACR ePrint 2026/052 ("Key Updatable Hash Based VRF") and `metatheory/Dregg2/Crypto/VRF.lean`.
- **The Pitfall Fixed:** Bodaghi et al. (FC24, "Breaking X-VRF") proved that naive WOTS+ hash chains lack
  collision resistance under adversarial public keys, allowing validators to forge multiple VRF outputs.
  `crypto-xmvrf` forces a collision-resistant Merkle commitment to each epoch's output, restoring strict uniqueness.

#### 5. `crypto-hashrand` (Post-Quantum Randomness Beacon)
- **Specification:** Pinned to Bandarupalli et al. (ACM CCS 2024 / IACR ePrint 2023/1755) and
  `metatheory/Dregg2/Crypto/RandomnessBeacon.lean`.
- **Property:** Eliminates BLS pairings, DKG, and group public keys. Proves *unbiasability* and *unpredictability*
  strictly reduced to hash collision resistance (`HashCR`) under a random oracle model. Implemented the synchronous
  commit-then-reveal safety core.

---

### 1.6 Isabelle / CryptHOL Universal Composability (`uc-crypthol`)

In `uc-crypthol/` (Commit `e17b9da35`, 2026-06-07), Ember bridged Lean 4 with Isabelle2025-2 and AFP 2025-2:
- **`Dregg2_FCom.thy`**: Mechanized the ideal commitment functionality $\mathcal{F}_{\text{com}}$ using
  CryptHOL's `Sigma_Commit_Crypto.Pedersen`:
  - `dregg2_commit_hom`: Additive homomorphism verified from group axioms.
  - `dregg2_F_com_hiding`: Perfect, unconditional hiding (adversary advantage $= 0$).
  - `dregg2_F_com_binding`: Computational binding strictly reduced to Discrete Logarithm hardness.
  - `dregg2_F_com_realizes`: Formal proof that the deployed Pedersen commitment realizes $\mathcal{F}_{\text{com}}$.
- **`metatheory/Dregg2/Crypto/UCBridge.lean`**: The Lean carrier `FComDischarge` bundled these CryptHOL guarantees
  into Lean `Prop` fields, proving entailment to `CryptoPrimitives.binding` and `CryptoPrimitives.unlinkable`.

---

### 1.7 Underelaborated Gadgets: `fold-opening`, `sumcheck-toy`, `constraint-lowering`

- **`fold-opening` (Commit `33456ea05`, 2026-08-13)**:
  Demonstrated that BFV ciphertext addition `fold_add` is linear, and its multilinear extension (MLE) is linear:
  $$c_{\text{out}} = \sum_{k} a_k c_k \implies \hat{c}_{\text{out}} = \sum_{k} a_k \hat{c}_k$$
  Therefore, one evaluation of the MLEs at a random point $r$ certifies the entire fold across all additions
  with **zero sumcheck rounds and zero per-addition constraints**. This reduced proof overhead from
  $\Theta(B \cdot N \cdot L)$ in an AIR to $\Theta(N \cdot L)$ in the opening route.
  *The Stub:* It lacked a polynomial commitment scheme (PCS). The prover asserted $\hat{c}(r)$ without
  opening a cryptographic commitment, making it vulnerable to the Dusk/OtterSec evaluation forge.
- **`sumcheck-toy` (Commit `bc2e9f4b9`, 2026-08-13)**:
  Wired `p3-sumcheck` at revision `82cfad73` to prove a product-of-multilinears:
  $$S = \sum_{x \in \{0,1\}^n} f(x) g(x)$$
  over BabyBear field extensions, reducing claims through $n$ quadratic sumcheck rounds.
- **`constraint-lowering`**:
  Lowered ordering constraints (`FieldGte`, `FieldLte`, `Monotonic`) into BabyBear polynomial constraints.
  Since BabyBear has characteristic $p \approx 2^{31}$, checking $a \ge b$ was done by verifying that
  $d = a - b$ has a small bit-decomposition ($d \in [0, 2^{\text{bits}})$). Multi-limb values ($u64$) were
  lowered via a cascading borrow chain (`emit_ge_multilimb`).

---

## 2. The Diaspora: How Ideas Spread Across the Repositories

When `breadstuffs` was drained and frozen in October 2026, its intellectual capital radiated into six specialized
sister repositories. Each fork was driven by hard empirical lessons.

```
                              ┌─────────────────────────────────────┐
                              │        BREADSTUFFS DIASPORA         │
                              └──────────────────┬──────────────────┘
                                                 │
         ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
         │                   │                   │                   │                   │
         ▼                   ▼                   ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    MINIDREGG    │ │    NANODREGG    │ │      OBEND      │ │  ZKML-RESEARCH  │ │      O7VN       │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • Level-3       │ │ • Extreme       │ │ • Silicon       │ │ • p61 field     │ │ • Isabelle/MLton│
│   re-execution  │ │   footprint     │ │   Elaborator    │ │   vFHE          │ │   industrial    │
│ • Dropped STARK │ │   reduction     │ │ • Hardware      │ │ • fold-as-      │ │   pipeline      │
│   from admission│ │ • In-memory     │ │   Reduction     │ │   opening       │ │ • Native code   │
│ • Farkas        │ │   evaluation    │ │   Machine       │ │ • Multilinear   │ │   synthesis     │
│   SysCert       │ │ • Strip host    │ │ • Glitch-free   │ │   PCS           │ │ • Gate export   │
│ • Selvage split │ │   overheads     │ │   ICAP DPR      │ │ • Matmul sumchk │ │   rel-census    │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 2.1 Why Handwritten Rust AIRs Were Banned (Law #1)
The ban on handwritten Rust constraints was born from a fundamental asymmetry:
- **Witness generators are allowed to be buggy in Rust.** A faulty witness generator produces inputs that
  fail to satisfy the verifier's polynomials. The proof fails to verify; the system halts or retries. This is a
  **liveness defect**.
- **Constraint systems must never be written in Rust.** A missing or broken constraint changes the relation
  the verifier accepts. An adversary can forge invalid transitions that pass verification. This is a
  **catastrophic soundness collapse**.
By forcing constraints to be emitted as data from Lean 4 (`EffectVmDescriptor2`), every accepted transition
was anchored to a Lean refinement proof (`turnChain_descriptor_refines_rust_air`).

### 2.2 Why Mini Dropped Proof Systems From Synchronous Admission
On 2026-10-01 (`project-no-proof-system-in-mini-admission.md`), Ember interrogated Mini's proving infrastructure:
> *"is our STARK actually sound? ... do we have a sound framework that takes our definitions from the logic
> and 'autostarks' them? ... is that something we WANT to build into mini? ... our proof system research was
> immature and im not sure really completed..."*

The investigation revealed that:
1. `Pred.witnessed vk` compiled to `false` in `Compiler/PredCompile.lean`. No proof-gated law had ever passed!
2. The back-half STARK soundness was compromised: while the FRI query protocol conjectured 130 bits,
   formal extraction bounds proved only 51–73 bits, and the PCS was empty (`Tower256MerkleCardinalityCore`).
3. The compiler's `Selvage/` and `Assurance/` modules accounted for 280 of 814 modules (~35% of build time),
   imposing an enormous compilation tax.
4. **The Verdict:** Mini banished proof systems from synchronous admission. Admission was gated purely by
   deterministic **Level-3 re-execution** in Lean (`Kernel/Run.lean`):
```lean
/-- checkRun_sound: an accepted claim names the kernel's own sample;
    the writes are EXACTLY the writes the program's product names. -/
theorem checkRun_sound {E : Evaluator} {program : Program} {libraries : List Program}
    {sample : E.Input} {claim : RunClaim} {writes : List FieldWrite} {verdict : Verdict E.Output}
    (accepted : checkRun E.toMachine program libraries sample claim writes = .ok verdict) :
    ∃ t, runOf E.toMachine program libraries sample = some t ∧
      E.Spec t verdict.output ∧
      E.writesOf program.abi verdict.output = some verdict.writes ∧
      (∀ w, w ∈ writes ↔ w ∈ verdict.writes) ∧
      claim.sampleJam = E.encodeInput sample ∧
      claim.outputJam = E.encodeOutput verdict.output ∧
      verdict.steps = claim.steps ∧ claim.steps ≤ program.abi.fuel ∧
      E.run claim.steps t = .ok verdict.output ∧
      E.steps claim.steps t = verdict.steps

/-- no_accepted_of_output_mismatch: a successful evaluation authorizes nothing by itself.
    If the command's writes differ from the writes the program's actual product names,
    no claim is accepted. -/
theorem no_accepted_of_output_mismatch {E : Evaluator} {program : Program}
    {libraries : List Program} {sample : E.Input} {writes : List FieldWrite} {t : E.Term}
    {out : E.Output} {decoded : List FieldWrite}
    (run : runOf E.toMachine program libraries sample = some t) (derives : E.Spec t out)
    (names : E.writesOf program.abi out = some decoded)
    (differ : ∃ w, ¬ (w ∈ writes ↔ w ∈ decoded)) (claim : RunClaim) (verdict : Verdict E.Output) :
    checkRun E.toMachine program libraries sample claim writes ≠ .ok verdict
```
Proofs were relegated to an optional, asynchronous carrier slot to be consumed only when backed by external,
audited verifiers.

### 2.3 The Twin Deletion Campaign
Throughout Breadstuffs, developers suffered from "Twin Maintenance": writing a type in Lean, rewriting an
identical struct in Rust, and writing a manual serializer between them. Inevitably, one side evolved and the
other drifted, creating phantom bugs.
- The `project-twin-deletion-campaign.md` decreed that **one language must own each structure**.
- For column layout, Lean owned `rotated178`, and Rust imported the generated column indices.
- For execution state, Lean owned the semantics, exported via `@[export dregg_trustline_step]`, and Rust called
  the compiled C archive (`libdregg_lean.a`).
- Whenever a twin was detected, the Rust mirror was deleted.

### 2.4 Evaluator Generalization (Moving Beyond Nock)
On 2026-10-01, Ember liberated Mini from an exclusive reliance on Nock:
> *"we DEFINITELY do not need to be stuck with nock, i'm not even a particularly big fan of it"*

Nock was demoted from the core architecture to Evaluator #1 in a pluggable registry. The kernel required only
that an evaluator provide a deterministic Lean semantics, canonical encoding, step metering, and a `run_sound`
theorem. This opened the path for SKI combinators, pure lambda calculus with sharing, and typed interaction nets.

---

## 3. What Got Dropped, Parked, or Underelaborated

An archaeological excavation reveals several brilliant mechanisms that were parked during the October 2026 freeze:

| Component / Subsystem | Exact Location in `breadstuffs` | What Was Finished | What Was Left Incomplete / Parked |
|---|---|---|---|
| **`crypto-hermine`** | `crypto-hermine/src/` & `metatheory/Dregg2/Crypto/Hermine*.lean` | Full 2-round signing, Gaussian CDT sampler, Lean extraction theorem, $n=256$. | Distributed Key Generation (DKG) was a trusted dealer; network ceremony had no asynchronous consensus. |
| **`crypto-tanuki`** | `crypto-tanuki/src/` | 2-round NIST MPTS scheme, Shamir over $R_q$, rounded MLWE. | Relied on cited-proven security; proofs were not formalized in Lean. |
| **`crypto-traccoon`** | `crypto-traccoon/src/` | 3-round Eurocrypt 2024 scheme with additive row/col masks. | Benchmarking baseline only; lacked production integration. |
| **`crypto-xmvrf`** | `crypto-xmvrf/src/` & `Dregg2/Crypto/VRF.lean` | Collision-resistant output tree fixing FC24 X-VRF uniqueness break. | Pre-audit; parameter sets and tree depths were unoptimized. |
| **`crypto-hashrand`** | `crypto-hashrand/src/` & `Dregg2/Crypto/RandomnessBeacon.lean` | Synchronous commit-then-reveal safety core, `HashCR` reduction in Lean. | Asynchronous weak-VSS, Gather, and Approximate Agreement were flagged as stubs. |
| **`fhegg-rtl`** | `fhegg-rtl/` (Lean + hardware) | Netlist DSL $\to$ Verilog emitter, adder proofs, butterfly golden models. | Full NTT/PBS accelerator remained SpinalHDL stubs; no end-to-end bitstream synthesis. |
| **`fhegg-solver`** | `fhegg-solver/src/` | Fast PDHG LP solver, Cert-F primal-dual certificates. | Market metatheory audit revealed MPC reveal modeled as argmax vs balance-threshold. |
| **`uc-crypthol`** | `uc-crypthol/` | Full Isabelle2025-2 machine-checked proofs of $\mathcal{F}_{\text{com}}$ realization. | Semantic transport from Isabelle to Lean statements relied on manual structural matching (`FComDischarge`). |
| **`fold-opening`** | `fold-opening/src/` | BFV linear fold certified via single MLE point opening. | Missing multilinear polynomial commitment scheme (BaseFold/WHIR); evaluation unbacked. |
| **`sumcheck-toy`** | `sumcheck-toy/src/` | Multilinear sumcheck over BabyBear using `p3-sumcheck`. | Unwired to state commitments; verified evaluation in isolation. |
| **Resource Camera** | `metatheory/Dregg2/Camera/` | Iris-style CAMERA resource algebra unifying conservation and authority. | Confined to abstract metatheory; never hooked into the deployed transaction pipeline. |

---

## 4. How Modern Foundations Supercharge Taking Them Back Up

The diaspora was not an abandonment; it was a purification. Today, our newer foundations provide the exact
missing puzzle pieces needed to resurrect Breadstuffs' parked masterpieces.

### 4.1 `obend` Silicon Elaborator $\to$ Resurrects `fhegg-rtl`
`fhegg-rtl` stalled because in July 2026 there was no mature hardware synthesis toolchain in Lean 4.
Today, `obend` has built that exact bridge:
- **`Obend/Lower/Fragment.lean`**: Lowers Lean 4 kernel terms directly into `Core4` (`lower_sound`).
- **`Obend/Hardware/ReductionMachine.lean`**: Compiles `Leaf.Book` supercombinators into a spatial grid of
  hardware `AutomatonTile`s connected by a credit-controlled NoC (`automaton_simulates_book`).
- **3-Phase Glitch-Free ICAP DPR Controller**: Dynamically reconfigures FPGA tiles based on slot-guarded
  specialization (`dpr_preserves_neighbor_tiles_and_packets`).
*The Revival:* Instead of handwriting SpinalHDL stubs for NTT butterflies, `obend`'s Silicon Elaborator can
synthesize the entire FHE NTT/PBS datapath directly from Lean specifications down to Verilog and FPGA bitstreams!

### 4.2 `minidregg` Farkas `SysCert` $\to$ Replaces Bulky STARK Predicates
In Breadstuffs, authorization constraints required heavy STARK circuits. In `minidregg`, Ember introduced
the Farkas negative-cycle certificate engine in `Pred/Satisfiable.lean`:
```lean
inductive SysCert where
  | clash (v : Node)
  | cycle (cs : List Con)
deriving Repr, DecidableEq

def SysCert.check (s : Sys) : SysCert → Bool
  | .clash v => s.present.contains v && s.absent.contains v
  | .cycle cs =>
      cs.all (fun c => s.cons.contains c) && (cs.map Con.x).isPerm (cs.map Con.y) &&
        decide ((cs.map Con.k).sum < 0)

theorem SysCert.check_sound {s : Sys} {c : SysCert} (h : c.check s = true) (o n : State) :
    ¬ s.satisfied o n
```
*The Revival:* Difference logic and capacity constraints do not need zero-knowledge proofs. A Bellman-Ford
solver produces an exact negative cycle certificate `SysCert.cycle` that checks in $O(|V|)$ operations.
The heavy STARK is replaced with linear-time Farkas certificate checking.

### 4.3 `zkml-research` $p_{61}$ vFHE $\to$ Solves the `fold-opening` PCS Gap
`fold-opening` proved that BFV ciphertext additions can be certified with one common-point MLE opening,
but lacked a compatible field and multilinear PCS.
`zkml-research` discovered the miraculous $p_{61}$ prime:
$$p_{61} = 127 \cdot 2^{54} + 1 = 2287828610704211969 = 2^{61} - 2^{54} + 1$$
- **Proved in Lean:** `Theory/CyclotomicInertia.lean` proves `p61_prime` via kernel-checked Lucas certificates.
- **2-Adicity:** Exactly 54. Supports negacyclic NTT up to $N = 2^{53}$.
- **Fold Congruence:** $2^{61} \equiv 2^{54} - 1 \pmod p$, enabling Goldilocks-style reduction with 3 lazy bits.
*The Revival:* By instantiating BFV ciphertexts directly over $p_{61}$, the ciphertext coefficients live in the
native proving field! The multilinear PCS (BaseFold over $p_{61}$) binds the ciphertexts directly, closing the
$60M Dusk/OtterSec evaluation hole without costly field emulation.

### 4.4 `o7vn` Isabelle/MLton Pipeline $\to$ Mechanizes `uc-crypthol`
`uc-crypthol` suffered from the semantic transport gap between Isabelle2025-2 and Lean 4.
`o7vn` has perfected an industrial Isabelle $\to$ SML $\to$ MLton pipeline:
- Code generation from Isabelle theories (`src/isabelle/`) directly compiles via MLton into standalone,
  ultra-high-performance native binaries.
*The Revival:* Instead of hand-bridging CryptHOL theorems into Lean `Prop` fields, we can use `o7vn`'s pipeline
to compile CryptHOL-verified cryptographic algorithms directly into native shared libraries that are linked
into the node.

### 4.5 Plonky3-Recursion & Degree-3 Sumcheck
In `minidregg/Assurance/AirSumcheckCubic.lean`, the degree-3 sumcheck engine unifies GKR fraction-tree layers
and Hadamard elementwise zerochecks:
$$\text{cubicForm } E\ A\ B\ C\ D = \hat{E} \cdot (\hat{A}\hat{B} + \hat{C}\hat{D})$$
With soundness error $m \cdot 3 / |F|$. This connects directly to `ZkmlMatmulSuccinctChecker.lean`, which verifies
matrix multiplication contractions at $(\mu + \nu)/|F| + \kappa \cdot 3 / |F|$ without reading dense tables.

---

## 5. The Revival Roadmap

The table below outlines the precise engineering blueprint for taking back up Breadstuffs' parked subsystems
using our modern foundational toolchains:

| # | Subsystem | Parked Asset in `breadstuffs` | Modern Foundation Enabler | Target Architecture & Revival Action | Priority |
|---|---|---|---|---|---|
| **R1** | **FHE NTT/PBS Hardware** | `fhegg-rtl/` (Lean netlist DSL, Golden butterfly/accumulator) | `obend/` Silicon Elaborator (`Obend/Hardware/ReductionMachine.lean`) | Lower Lean FHE butterfly specs through `Core4` $\to$ `Leaf.Book` $\to$ `AutomatonTile` grid on eFPGA. Completely bypass handwritten SpinalHDL. | **P1 (High)** |
| **R2** | **vFHE Common-Point Fold** | `fold-opening/` (MLE common point opening, zero sumcheck) | `zkml-research/` $p_{61}$ field (`p61_prime`, $127 \cdot 2^{54}+1$) | Re-base BFV ciphertexts onto $p_{61}$. Disclose evaluations against a BaseFold PCS over $p_{61}$. Eliminate $\Theta(B \cdot N \cdot L)$ AIR constraints. | **P1 (High)** |
| **R3** | **Post-Quantum Threshold Signatures** | `crypto-hermine/` & `crypto-tanuki/` | `minidregg/` access control & `o7vn/` verified relations | Implement an asynchronous network ceremony with weak-VSS to replace the trusted dealer. Deploy Hermine as the threshold validator signature. | **P2 (Med)** |
| **R4** | **Post-Quantum Randomness Beacon** | `crypto-hashrand/` (Synchronous safety core, `HashCR` proof) | `minidregg/` consensus & commit-reveal engine | Complete the asynchronous Gather and Approximate Agreement layer. Replace classical BLS beacons with HashRand across the cluster. | **P2 (Med)** |
| **R5** | **CryptHOL UC Verification** | `uc-crypthol/` (`Dregg2_FCom.thy`, Isabelle2025-2) | `o7vn/` Isabelle $\to$ SML $\to$ MLton compiler pipeline | Compile CryptHOL-verified cryptographic primitives directly to native code via MLton, eliminating the unmechanized Lean bridge caveat. | **P3 (Deep)** |
| **R6** | **Lightweight Constraint Checking** | `constraint-lowering/` (BabyBear borrow chain) | `minidregg/` Farkas `SysCert` (`Pred/Satisfiable.lean`) | Replace complex range-check polynomial gadgets with $O(\|V\|)$ Farkas negative-cycle certificates checkable in kernel admission. | **P1 (High)** |
| **R7** | **Confidential Clearing Core** | `fhegg-solver/` (PDHG solver, Cert-F certificates) | `metatheory/Market/` audit & `zkml-research` | Fix the MPC reveal specification split (reconcile argmax vs balance-threshold) and bind Cert-F checking to the deployed DEX clearing loop. | **P2 (Med)** |

---

## 6. Primary Source Verification & Hash Manifest

All statements and paths in this strand are grounded in the following immutable artifacts:

1. **Breadstuffs Law #1 Enforcement:**
   - Commit: `19439d261d9622f6a08a39df9a02e0bbcc267054` (2026-07-31)
   - Gate: `/Users/ember/dev/breadstuffs/circuit-prove/tests/law1_enforcement_gate.rs`
   - Canonical Doc: `/Users/ember/dev/breadstuffs/docs/CIRCUITS-FROM-PROOFS.md`
2. **Breadstuffs Core Audit:**
   - Document: `/Users/ember/dev/breadstuffs/CORE-AUDIT.md` (Workflow `wf_68020930-db3`, 2026-07-03)
   - Fixed in: `starbridge-v2/src/world/world.rs` (`LedgerJournal::touched_cells`)
3. **Verified Rotated Layout:**
   - Commit: `94217ed3c` (2026-07-18)
   - Source: `/Users/ember/dev/breadstuffs/metatheory/Dregg2/Circuit/Emit/EffectVmEmitRotationV3.lean`
4. **Isabelle / CryptHOL UC Grounding:**
   - Commit: `e17b9da35` (2026-06-07)
   - Sources: `/Users/ember/dev/breadstuffs/uc-crypthol/{Dregg2_FCom.thy, ROOT}`
   - Environment: Isabelle2025-2 + AFP 2025-2
5. **Plonky3 IVC Fork:**
   - Commit: `af3f6cc269810d2e3a73baceabb47edb83333578` (2026-06-26)
   - Source: `/Users/ember/dev/plonky3-recursion/README.md`
6. **Mini Admission & Farkas Solver:**
   - Memory: `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-no-proof-system-in-mini-admission.md`
   - Theorem: `/Users/ember/dev/minidregg/Pred/Satisfiable.lean:486` (`SysCert.check_sound`)
   - Re-execution: `/Users/ember/dev/minidregg/Kernel/Run.lean:316,383` (`checkRun_sound`, `no_accepted_of_output_mismatch`)
7. **$p_{61}$ Field Discovery:**
   - Theorem: `/Users/ember/dev/minidregg/Theory/CyclotomicInertia.lean` (`p61_prime`, commit `641ceeb`)
   - Spec: `/Users/ember/dev/zkml-research/notes/fold-as-opening.md`
8. **Silicon Elaborator:**
   - Spec: `/Users/ember/dev/obend/SILICON-ELABORATOR.md`
   - Machine: `/Users/ember/dev/obend/Obend/Hardware/ReductionMachine.lean`
