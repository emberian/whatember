# Strand 19 — The Breadstuffs Diaspora: Federation, Multi-Chain Settlement, Blocklace/CapTP, Commons Governance, Polisware, and the Enterprise Verticals

> Primary-source dossier. Compiled 2026-11-02 from the repositories under `/Users/ember/dev/`, their git logs,
> their in-tree goal documents, and the Claude memory stores under `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/`.
> Every commit SHA, Lean 4 / HOL4 / ACL2 theorem signature, Rust struct, and verbatim quotation below was extracted directly
> from the local repositories and memory records, not reconstructed from memory. Where an artifact was parked or a proof
> left uncompleted, the text notes the exact failure mode, missing lemma, or architectural friction.
>
> **Scope boundary.** `/Users/ember/hellas` is strictly third-party historical context (Ember's prior work on workload
> verification, which informed the genesis of Dregg after departure) and is not claimed as open property. All repos
> outside `/Users/ember/dev/whatember/` are treated as strictly read-only.

---

## 0. Executive Map & Architectural Lineage

The monolithic repository `/Users/ember/dev/breadstuffs` was the expansive crucible of Ember's systems engineering.
Between May and August 2026, `breadstuffs` housed simultaneously: a Byzantine fault-tolerant consensus engine over
equivocation-free DAGs (`blocklace`), an object-capability network transport protocol (`captp`), a multi-chain non-custodial
settlement and light-client matrix (`chain`, `cosmos-*`, `solana-*`, `eth-lightclient`, `mina`), an axiomatic democratic
deliberation and collective governance substrate (`collective-choice`, `commons-arbiter`, `metatheory/Polis`), and an
enterprise/database infrastructure tier (`pg-dregg`, `fhir`, `durable-workflow`).

Under the pressure of build times, multi-tenant agent contention, and proving overheads, this monolith fractured into a
specialized diaspora. The table and ASCII lineage below trace where those ideas landed, what succeeded, and what remained parked.

```
                                    ┌────────────────── breadstuffs (monolith) ──────────────────┐
                                    │  consensus: blocklace · captp · dfa-federation · coord     │
                                    │  chains: cosmos-* · solana-* · eth-lightclient · mina      │
                                    │  governance: collective-choice · commons-arbiter · polis   │
                                    │  enterprise: pg-dregg · fhir · durable-workflow            │
                                    └──────────────────────────────┬─────────────────────────────┘
                                                                   │
         ┌─────────────────────┬───────────────────────────┼───────────────────────────┬──────────────────────┐
         ▼                     ▼                           ▼                           ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────────────┐  ┌───────────────────┐  ┌──────────────────┐
│ dragons-clutch   │  │        fn        │  │      svenvs ⋈ Polis         │  │     verekos       │  │ nanodregg/obend  │
│   → dclutch      │  │ BPv7 + NNTP      │  │ Formal non-domination       │  │ Claim/receipt     │  │ Simplex BFT      │
│ Solana SBF       │  │ Store-and-fwd    │  │ "Verify cage, not animal"   │  │ Mathlib-free      │  │ Obend.Consensus  │
│ 8 programs,      │  │ ACL2-verified    │  │ svenvs: HOL4 libertyScript  │  │ Paused 2026-10-19 │  │ Obend.Ledger     │
│ Cohorts 8 → 17   │  │ RFC 9171–9174    │  │ Polis: 66 Lean files        │  │ → minidregg       │  │ Pure Lean / Bend │
└──────────────────┘  └──────────────────┘  └─────────────────────────────┘  └───────────────────┘  └──────────────────┘
```

### High-Level Subsystem Status Summary

| Subsystem | Original `breadstuffs` Path | Diaspora Descendant | Maturity Status | Primary Bottleneck / Park Reason |
|---|---|---|---|---|
| **Consensus / DAG** | `/blocklace`, `/coord` | `nanodregg`, `obend` | **Replaced** | $O(\text{history})$ tau-ordering latency; live-gossip eviction bug. Replaced by Simplex BFT. |
| **Object Capabilities** | `/captp` | `fn`, `obend/lean/Obend/Vault` | **Parked / Absorbed** | ML-DSA PQ test harness aborts (`SIGABRT`); distributed GC cross-federation complexity. |
| **Store & Forward** | `/captp/src/store_forward.rs` | `fn` (`specs/bp-path.md`) | **Graduated (L4)** | Scaled into RFC 9171–9174 Bundle Protocol v7 with formal ACL2 proofs in `fn`. |
| **Multi-Chain Settle** | `/chain`, `/cosmos-*`, `/solana-*` | `dclutch`, `obend` | **L3 (Local / Devnet)** | 25-lane Groth16 verified on EVM, Solana SBF, and CosmWasm; blocked on production MPC setup. |
| **Semantic Lightclients**| `/eth-lightclient`, `/mina` | In-tree `docs/` | **L2 Prototype** | Mina Pasta curve-cycle mismatch; Ethereum sync committee lacked BLS12-381 in-tree. |
| **Cross-Chain Gov** | `/dregg-interchain-gov` | `obend/lean/Obend/Ledger` | **Parked** | Edge tag agreement held only by mirrored constants; lacked proof-of-holding derivation. |
| **Polisware** | `/metatheory/Polis/` | `svenvs` | **L3 (Theoretic Apex)** | 66 Lean files axiom-clean; real LLM agent runtime harness unbuilt; unified framing inflated. |
| **AI Arbitration** | `/commons-arbiter` | `o7vn` (Oracle7) | **Parked** | Lexical prompt-injection filter (`{{` detection); lacked semantic proof of non-domination. |
| **Agent App Store** | `/grain-commons`, `/hosted-*` | `verekos`, `minidregg` | **Parked** | Required Sandstorm `.spk` package pipeline and lived under operated-layer infrastructure debts. |
| **Postgres RLS Engine** | `/pg-dregg` | `minidregg` | **Parked** | `cargo-pgrx` excluded from CI workspace; required managed PG18 runtime; Lean FFI glue churn. |
| **FHE Product DSL** | `/fhir` (`fhIR-0`) | `obend/Hardware` | **L1 Seed** | Six-part admissibility theorem remained in `metatheory/` unproved; FHE matvec size envelopes. |
| **Durable Workflow** | `/durable-workflow` | `hosted-durable` | **L2 Prototype** | C-int ABI mismatch on `setrlimit` (Linux-gnu); duroxide sqlite backend lock contention. |

---

## 1. What Lived in `breadstuffs` (The Monolithic Peak)

### 1.1. Federation, Consensus, and the Blocklace

The federation layer was designed to execute multi-node consensus with verified finality. Its primary documents were
[`GOAL-FEDERATION.md`](file:///Users/ember/dev/breadstuffs/GOAL-FEDERATION.md) and memory file
[`project-federation-payoff.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-federation-payoff.md).

#### The n=4 Federation Payoff (2026-07-07)
On 2026-07-07 (cv session `5d12f365-a748-4e7a-b4ca-99a0291fef49`), Ember achieved the core federation milestone:
a foreign, non-operator client signed its own transfer, submitted via `POST /turns/submit`, and it stream-finalized
cross-node on a verified-executor $n=4$ mesh across two physical machines (`hbox` at `192.168.50.39` and `nextop` at
`192.168.50.130`). The test harness [`node/tests/payoff_client_turn.rs`](file:///Users/ember/dev/breadstuffs/node/tests/payoff_client_turn.rs) verified:
- Dest account funded across all 4 nodes;
- Block heights advanced uniformly: `[1,1,1,1] → [2,2,2,2]`;
- Finalized in ~25 seconds over two clean rounds under `DREGG_TEST_REQUIRE_FINALITY=1`.

#### The $O(\text{history})$ Wall in Verified Finality
The path to this payoff uncovered a severe architectural defect. When running with the verified Lean tau-order finality gate
(`VerifiedFinality::compute_order`, [`node/src/finality_gate.rs:150`](file:///Users/ember/dev/breadstuffs/node/src/finality_gate.rs#L150) calling `dregg_tau_order` FFI into Lean's
`tauOrderFast`), an $n=3$ node mesh would plateau while $n=4$ progressed. The investigation proved this was **not** a
correctness fault, but a catastrophic complexity cliff:
> *"The verified-Lean tau-order finality gate was $O(\text{history})$, recomputed from scratch on EVERY finality poll: the serial
> executor rebuilt the whole wire and Lean rebuilt `PastCache`/`RoundCache` over the full lace on each call, then discarded them.
> As the DAG grew, per-poll cost outpaced block production and the consensus stalled."*
> — [`project-federation-payoff.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-federation-payoff.md)

#### The Blocklace: Cordial Dissemination and Eviction-by-Past
The consensus engine in [`/Users/ember/dev/breadstuffs/blocklace/`](file:///Users/ember/dev/breadstuffs/blocklace/) implemented a Byzantine-repelling Directed
Acyclic Graph (DAG) based on Almeida & Shapiro (2024, arXiv:2402.08068) and Cordial Miners (Shapiro et al., 2022, arXiv:2205.09174).
In cv session `ad7d9679` (sub-agent of `27b28e60`, 2026-08-08, recorded in [`docs/reference/READING-BLOCKLACE-2026-08-08.md`](file:///Users/ember/dev/breadstuffs/docs/reference/READING-BLOCKLACE-2026-08-08.md)),
Ember dispatched a literature review that uncovered a fundamental divergence between theory and implementation:

1. **The Live-Gossip Mutation Defect**:
   The implementation in [`blocklace_sync.rs`](file:///Users/ember/dev/breadstuffs/node/src/blocklace_sync.rs) stated that the tau participant set must be a deterministic function of
   committed state alone. Yet `handle_push` called `constitution.auto_evict(proof)` *on gossip arrival*, mutating the live participant
   set. If Node A saw both halves of an equivocation fork and Node B saw only one, Node A ran at $n-1$ while Node B ran at $n$.
   Consequently, the wave leader formula `wave_leader = participants[wave % n]` selected different leaders on different nodes, creating
   a silent fork. Furthermore, because eviction was not a block in the DAG, a reboot silently reinstated the equivocator.

2. **The Fix (Commits `89238335a` and `0eccd772d`, 2026-08-08/09)**:
   Ember corrected this by moving eviction off gossip-arrival mutation into **exclusion-by-past** (`node(b) ∉ byz(⌊b⌋)`), making eviction
   a structural predicate over a block's causal closure:
   ```rust
   // Commit 89238335ad618998cc74daa77328651add0ddcb8
   // Author: ember arlynx <ember@lunar.town>, Date: Sat Aug 8 17:37:36 2026 -0400
   // "feat(consensus)!: exclusion-by-past — eviction was a live mutation keyed on gossip arrival;
   // both papers make it a predicate over the block's own closure"
   ```
   Followed by commit `0eccd772d1348fb29b79658cf134f3fc18fcfe6d` (Sun Aug 9 05:26:58 2026), adding 2,115 insertions across
   [`blocklace/src/constitution.rs`](file:///Users/ember/dev/breadstuffs/blocklace/src/constitution.rs) and [`blocklace/src/finality.rs`](file:///Users/ember/dev/breadstuffs/blocklace/src/finality.rs) to enforce the Cordial Miners Alg. 1:5 two-tips-per-miner flood cap
   and `CreatorTips::Pair` evidence requirements.

3. **DFA-Federation**:
   To prevent circular dependencies (`cell -> dfa -> federation -> captp -> cell`), [`/Users/ember/dev/breadstuffs/dfa-federation/`](file:///Users/ember/dev/breadstuffs/dfa-federation/)
   isolated route updates. [`FederationQcVerifier`](file:///Users/ember/dev/breadstuffs/dfa-federation/src/lib.rs#L59) verified route transitions using a BLS `ThresholdQC` over
   `old_commitment || new_commitment`:
   ```rust
   pub struct FederationQcVerifier {
       committee: FederationCommittee,
   }

   impl ThresholdVerifier for FederationQcVerifier {
       fn verify_threshold(&self, expected_old: [u8; 32], new_comm: [u8; 32], proof_data: &[u8]) -> Result<(), RouteUpdateError> {
           let qc: ThresholdQC = postcard::from_bytes(proof_data)
               .map_err(|e| RouteUpdateError::ThresholdVerificationFailed(e.to_string()))?;
           let mut msg = [0u8; 64];
           msg[0..32].copy_from_slice(&expected_old);
           msg[32..64].copy_from_slice(&new_comm);
           self.committee.verify(&qc, &msg)
               .map_err(|e| RouteUpdateError::ThresholdVerificationFailed(e.to_string()))
       }
   }
   ```

---

### 1.2. Distributed Object Capabilities: `captp`

The CapTP implementation in [`/Users/ember/dev/breadstuffs/captp/`](file:///Users/ember/dev/breadstuffs/captp/) provided capability transport across federations,
combining the classic Agoric/E CapTP architecture with post-quantum cryptography.

#### Architecture and Invariants
Defined in [`captp/src/lib.rs`](file:///Users/ember/dev/breadstuffs/captp/src/lib.rs#L1-L60):
- **Sturdy References** (`uri::DreggUri`): Portable, durable capability URIs of the form `dregg://<fed-id>/<cell-id>/<swiss-number>`
  that survive transport disconnections.
  ```rust
  #[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
  pub struct DreggUri {
      pub federation_id: [u8; 32],
      pub cell_id: CellId,
      pub swiss_number: [u8; 32],
  }
  ```
- **Swiss Table** (`sturdy::SwissTable`): Maps unguessable bearer secrets (`[u8; 32]`) to live capability descriptors. Possession of the swiss number is itself the authorization.
- **Three-Party Handoffs** (`handoff::HandoffCertificate`): Unforgeable offline capability transfers signed by the introducer,
  verifiable by any third party without contacting the issuer:
  ```rust
  pub struct HandoffCertificate {
      pub introducer_pubkey: [u8; 32],
      pub recipient_pubkey: [u8; 32],
      pub sturdy_ref: DreggUri,
      pub caveat: Pred,
      pub signature: Signature, // Ed25519 or ML-DSA-65
  }
  ```
- **Distributed GC** (`gc`): Cross-federation wire reference counting and drop tracking.
- **Hybrid Post-Quantum Cryptography** (`dregg-pq`): ML-DSA-65 (FIPS 204) hybrid capability-handoff signatures and X25519 + ML-KEM-768
  hybrid transport sessions to resist "Harvest Now, Decrypt Later" (HNDL) attacks.
- **Store-and-Forward Relay** (`store_forward::EncryptedMessage`): Offline delivery using X25519 ECDH $\to$ HKDF-SHA256 $\to$
  ChaCha20-Poly1305 AEAD. Relay operators inspect only ciphertexts; tampering or forging triggers authenticated decryption failure.

#### The PQ Harness Pitfall
A critical test-suite bug plagued `captp`. In commits `d2181916c` and `d78b8512b`, Ember discovered that 130 tests across `captp` and
related crates had never executed because `dregg-pq` aborted the process with `process::abort()` when the Lean-verified ML-DSA-65
cores were missing in test binaries, causing tests to exit prematurely with bare `SIGABRT`s.

---

### 1.3. Multi-Chain Settlement and Semantic Light Clients

The multi-chain vision in `breadstuffs` was defined by Ember's strict doctrine:
> **"You only need wraps/bridges when you lack proofs about the other chain's state transitions — just be a full client of all the chains."**
> — [`project-chain-participation-epoch.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-chain-participation-epoch.md)

#### The 25-Lane Proof Statement
Rather than trusting centralized bridge multisigs, Dregg’s settlement object was an IVC STARK fold compressed into a gnark Groth16 proof
over BN254. The canonical statement was defined as **25 BabyBear field lanes** ($p = 2013265921 = 0x78000001$):
```
Statement = genesis_root[8] ++ final_root[8] ++ num_turns[1] ++ chain_digest[8]
```
With `SEG_ANCHOR_WIDTH = SEG_DIGEST_WIDTH = 8` ([`circuit-prove/src/ivc_turn_chain.rs:284`](file:///Users/ember/dev/breadstuffs/circuit-prove/src/ivc_turn_chain.rs#L284)).

#### Cross-Chain Settlement Parity
The 25-lane BN254 Groth16 proof was verified natively across three disparate runtime architectures:

1. **EVM (`chain/contracts/DreggSettlement.sol`)**:
   Concrete 25-lane contract using Ethereum's `ecPairing` precompile, paired with `DreggGroth16Verifier25.sol`, `DreggVault.sol`,
   and `DreggCredentialGate.sol` (commits `53efc5503`, `b997f9cef`, `ee9f9d887`, `35af20966`).
   ```solidity
   contract DreggSettlement is IDreggSettlement {
       uint256 public constant BABYBEAR_P = 2013265921;
       IGroth16Verifier25 public immutable verifier;

       uint32[8] private _genesisLanes;
       uint32[8] private _provenLanes;
       uint64 private _provenHeight;

       function settle(
           uint32[8] calldata newRootLanes,
           uint64 numTurns,
           uint32[8] calldata chainDigestLanes,
           uint256[8] calldata proof
       ) external override {
           uint256[25] memory publicInputs;
           // pack _provenLanes, newRootLanes, numTurns, chainDigestLanes...
           require(verifier.verifyProof(proof, publicInputs), "invalid settlement proof");
           _provenLanes = newRootLanes;
           _provenHeight += numTurns;
           _provenRoots[keccak256(abi.encodePacked(newRootLanes))] = _provenHeight + 1;
       }
   }
   ```
   *The VK Commitment Flaw Fixed (Flag Day 2026-07-30)*: The original contract stored `bytes32 private immutable _verifyingKeyHash`
   which was never compared against the key used in `ecPairing`. It was corrected so that `verifyingKeyHash()` reads directly from
   `verifier.vkDigest()`, making mismatch structurally impossible.

2. **Cosmos (`cosmos-settlement/src/lib.rs`)**:
   A CosmWasm contract verifying the identical 25-lane proof and Pedersen commitment using `ark-bn254`, without requiring a
   Cosmos-native curve instantiation.

3. **Solana (`solana-settlement/src/lib.rs`)**:
   A native Solana SBF program (no Anchor) verifying the identical proof on-chain using Solana's `alt_bn128` syscalls (`solana_bn254::prelude`).

#### Semantic Light Clients
- **EVM (`eth-lightclient`)**: Verified Ethereum sync-committee attestations, weak-subjectivity checkpoints, and EIP-1186 Merkle
  Patricia Trie (MPT) storage proofs. In commit `0aba72c65788` (2026-07-29), the sync committee rotation was transferred to
  Lean verification after finding that `store::bootstrap_committee` had bypassed the verified gate. Commit `dba55c04b` removed an
  accidental `DREGG_LANE_AA_MUTANT=accept` bypass.
- **Cosmos (`cosmos-lightclient`)**: Verified Tendermint $\ge 2/3$ commit signatures and ICS-23 IAVL Merkle tree membership.
- **Solana (`dregg-bridge/src/solana_holdings.rs`)**: Verified Tower-BFT finalized bank hashes and stake-weighted supermajorities.
- **Mina (`GOAL-MINA-SEMANTIC-LIGHTCLIENTS.md`)**: Reached acceptance of real Mina Devnet block `539508` via a Lean Kimchi/Pickles
  verifier (P0–P6), but the Pasta-vs-BabyBear curve-cycle mismatch prevented full arithmetic deployment.

#### Non-Custodial Cross-Chain Governance: `dregg-interchain-gov`
In [`/Users/ember/dev/breadstuffs/dregg-interchain-gov/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-interchain-gov/src/lib.rs), Ember joined all three foreign light clients into a single
compiled governance seam. Foreign token holders proved their balances on their native chain via read proofs:
- Solana: `ProvenHolding`
- EVM: `ProvenErc20Holding`
- Cosmos: `ProvenCosmosFact`

The holder signed an `owner -> voter` binding (Ed25519 on Solana, EIP-191 on EVM, Cosmos ADR-036). The compile-time pins
`_EVM_TAG_PINNED` and `_COSMOS_TAG_PINNED` locked the tag mapping (`Solana = 0`, `EVM = 1`, `Cosmos = 2`), allowing foreign
balances to flow directly into Dregg's [`CollectiveChoice`] tally without locking, bridging, or wrapping a single token:
```rust
pub fn proven_holding_to_governance(
    proven: &ProvenCosmosFact,
    chain_id: ChainId,
    nullifier_salt: [u8; 32],
) -> Result<ProvenForeignHolding, ForeignFieldsError> {
    let fields = cosmos_lightclient::foreign_holding_fields(proven, nullifier_salt)?;
    ProvenForeignHolding::from_foreign_fields(chain_id, fields)
}
```

---

### 1.4. Democratic Deliberation, Commons Governance, and Polisware

`breadstuffs` contained one of the most mathematically ambitious governance stacks ever designed, spanning game theory,
Ostrom commons management, and formal social choice.

#### Collective Choice (`collective-choice/src/lib.rs`)
Composed four formal mechanisms into a unified `VoteEngine`:
1. **One-Vote-per-Ballot**: Ballot cell with a `WriteOnce(VOTE)` constraint.
2. **Monotone Tally**: Poll cells with `Monotonic` option tallies, preventing replay attacks from lowering counts.
3. **Quorum Gate**: In-cell affine inequality constraint:
   $$\text{AffineLe} \{ M \cdot \text{RESOLVED} - \sum \text{TALLY}_i \le 0 \}$$
4. **Non-Amplifying Delegation (Liquid Democracy)**: Macaroon attenuation via `Mandate::sub_delegate` (`DelegTree::no_amplify`).
5. **One-Vote Nullifiers**: Third layer of defense preventing double voting across the network.

#### The Commons Arbiter (`commons-arbiter/src/lib.rs`)
An "AI authority nobody owns" (`docs/deos/UNCENSORABLE-UTILITY.md`). An autonomous LLM evaluator governed by a community `Rubric`:
- A member submits a `Case` (content + rubric ID).
- An attested LLM session emits a ruling carrying a `ZkOracleAttestation`.
- **Anti-Prompt-Injection Proof**: The attestation proves the ruling is authentic, well-formed JSON, and injection-free (proved
  free of `{{` handlebars delimiters via a verified negative-regex matcher).
- **Quorum Ratification**: A ruling becomes final only when a committee of $n$ independent operators ratifies it ($\lfloor 2n/3 \rfloor + 1$).

#### Grain Commons (`grain-commons/src/lib.rs`)
A decentralized app-store and execution commons for hosted AI agents (Sandstorm grains):
- Signed `.spk` packages where the App ID is the author's Ed25519 public key.
- Committed `Umem` memory heaps with tamper-proof `Pedigree` Merkle trees tracing every code fork.
- `GenesisAgent` minting bounded child sub-agents with attenuated capability ceilings.

#### Polisware: The 66-File Lean Corpus (`metatheory/Polis/`)
Polisware was the formal mathematical constitution for multi-agent coexistence, synthesizing Ember's work on `svenvs` with
computable politics. The spine is defined in [`metatheory/Polis/Polis.lean`](file:///Users/ember/dev/breadstuffs/metatheory/Polis/Polis.lean):

```lean
/-- **`polis_safety` — verify the cage, not the animal.** For a sound policy, a safe
shield, and a safe start, the enveloped system keeps the floor at EVERY step, for EVERY
controller. The controller is universally quantified and never inspected: no psychometric
classification of the inhabitant can be load-bearing for the guarantee. -/
theorem polis_safety
    {step : State → Action → State} {safe : Floor State}
    {pol : Policy State Action} {shield : State → Action} {init : State}
    (sound : SoundPolicy step safe pol)
    (shieldSafe : ∀ s, safe s → safe (step s (shield s)))
    (initSafe : safe init) :
    ∀ (ctrl : State → Action) (n : Nat),
      safe (traj step (envAct pol shield ctrl) init n) := by
  intro ctrl
  have step1 : ∀ s, safe s → safe (step s (envAct pol shield ctrl s)) := by
    intro s hs
    unfold envAct
    by_cases hp : pol s (ctrl s)
    · rw [if_pos hp]; exact sound s (ctrl s) hs hp
    · rw [if_neg hp]; exact shieldSafe s hs
  intro n
  induction n with
  | zero => exact initSafe
  | succ k ih => exact step1 _ ih
```

Key constitutional theorems in `Polis.lean`:
- **Honesty Discrimination via Typing** (lines 213–234):
  ```lean
  inductive ClauseEvidence (c : Clause) : Type where
    | structuralProof (proof : c.claim) : ClauseEvidence c
    | adjudicationCost (clerkCost : Nat) : ClauseEvidence c
    | jurisdictionBoundary (reason : String) : ClauseEvidence c

  theorem structural_requires_proof {c : Clause} (e : ClauseEvidence c)
      (h : e.status = LawStatus.structural) : c.claim := by
    cases e with
    | structuralProof p => exact p
    | adjudicationCost _ => simp only [ClauseEvidence.status] at h; exact absurd h (by decide)
    | jurisdictionBoundary _ => simp only [ClauseEvidence.status] at h; exact absurd h (by decide)
  ```
- **Monotone Amendment and Non-Regression** (lines 279–314):
  ```lean
  theorem regressive_amendment_inert (frozenMin : Agent → Floor State)
      (am : Amendment Agent State) (C : Constitution Agent State)
      (h : ¬ NonRegressive frozenMin am C) :
      guardedApply frozenMin am C = C := by
    unfold guardedApply; rw [if_neg h]

  theorem amendment_stream_nonregression (frozenMin : Agent → Floor State)
      (ams : Nat → Amendment Agent State) {C : Constitution Agent State}
      (hwf : WellFormed frozenMin C) :
      ∀ n, WellFormed frozenMin (amendStream frozenMin ams C n) := by
    intro n
    induction n with
    | zero => exact hwf
    | succ k ih => exact guardedApply_wellFormed frozenMin (ams k) ih
  ```
- **Schism as Empty Meet** (line 335):
  ```lean
  theorem disjoint_floors_no_polis (floors : Agent → Floor State)
      (hempty : ¬ ∃ s, ∀ i, floors i s) : ¬ CanFormPolis floors := by
    rintro ⟨s, hs⟩
    exact hempty ⟨s, hs⟩
  ```
  A polis exists only where exported floors share an inhabitant. If floors are disjoint, there is no common court; this is not
  enforced by censorship or majority vote, but is a structural derivation.

---

### 1.5. Enterprise, Storage, and Durable Database Verticals

#### `pg-dregg`: Verifiable Postgres Extension
In [`/Users/ember/dev/breadstuffs/pg-dregg/`](file:///Users/ember/dev/breadstuffs/pg-dregg/), Ember built a PostgreSQL extension (targeting PostgreSQL 18 via `cargo-pgrx`)
that made Dregg's object-capability model the native Row-Level Security (RLS) engine for relational data:
- `src/authz.rs`: Tier-A capability decoding, verification LRU, and caveat algebra.
- `src/jsonpath.rs`: Compiled Dregg `Pred` predicates directly into SQL `jsonpath` filter expressions:
  ```rust
  // Structural translation table from pg-dregg/src/jsonpath.rs
  // Pred::True                   => "true"
  // Pred::False                  => "false"
  // Pred::AttrEq{key, value}     => "@.key == \"value\""
  // Pred::AttrPrefix{key, pfx}   => "@.key starts with \"pfx\""
  // Pred::NotBefore{at}          => "@.clock >= at"
  // Pred::NotAfter{at}           => "@.clock <= at"
  // Pred::Within{nb, na}         => "@.clock >= nb && @.clock <= na"
  // Pred::AllOf([p...])          => "(f1 && f2 && ...)"
  // Pred::AnyOf([p...])          => "(f1 || f2 || ...)"
  // Pred::Not(p)                 => "!(f)"
  ```
- `src/mirror.rs`: Tier-B/C row types with a `RootChain` anti-substitution mechanism.
- `src/attest.rs`: Tier-C range-attestation proof gate linking SQL queries to zk-circuit receipts.
- `src/workflow.rs`: In-database durable workflow execution.

#### `fhir` (`fhIR-0`): FHE Convex Optimization DSL
Despite its name, [`/Users/ember/dev/breadstuffs/fhir/`](file:///Users/ember/dev/breadstuffs/fhir/) was **not** medical HL7 FHIR; it was **fhIR-0**: Fully Homomorphic Encryption Intermediate Representation:
- Typed DSL for financial orders and products on top of the `fhEgg` / `Cert-F` solver.
- Products carried a convex program shape (LP / QP / aggregation) and a privacy tier: **Dark** (Tier 0, FHE, public matrices only),
  **Shielded** (Tier 1, solver sees private matrices), and **Open** (Tier 2, public).
- `types.rs` defined the visibility and admissibility rule:
  ```rust
  #[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize)]
  pub enum Visibility {
      Public,
      Private,
  }

  pub struct ProgramType {
      pub curvature: Curvature,
      pub matrices: Vec<Visibility>,
      pub cones: Vec<ConeKind>,
      pub dimension: usize,
  }
  ```
- `qp_certificate.rs`: Generated exact SDD $\to$ PSD admission witnesses and strict KKT optimality witnesses.

#### `durable-workflow`, `hosted-durable`, and `hosted-lease`
A deterministic durable execution engine modeled after DBOS and Temporal:
- [`durable-workflow/src/lib.rs`](file:///Users/ember/dev/breadstuffs/durable-workflow/src/lib.rs): Workflows execute deterministic steps checkpointed to a `duroxide` store. Crashes resume
  at the first unfinished step without re-executing completed side effects.
- [`hosted-durable/src/lib.rs`](file:///Users/ember/dev/breadstuffs/hosted-durable/src/lib.rs): Conserving settlement rail charging per-period lease fees via `recTransfer` ($\sum \delta = 0$).
- [`hosted-lease/src/lib.rs`](file:///Users/ember/dev/breadstuffs/hosted-lease/src/lib.rs): Fused meters combining `StandingObligation` with `prepaid_lease` into a single atomic write.

#### `auditable-fund` and `attested-dm`
- [`auditable-fund/src/lib.rs`](file:///Users/ember/dev/breadstuffs/auditable-fund/src/lib.rs): An autonomous trading agent that cannot lie about fills. Every trade lands as a light-client
  verifiable receipt binding a zkOracle price attestation and an attested Hermes decision. A third party auditing the fund requires zero operator trust.
- [`attested-dm/src/lib.rs`](file:///Users/ember/dev/breadstuffs/attested-dm/src/lib.rs): An attested AI Dungeon Master. Prompt integrity is certified via `dregg_zkoracle_prove::render`. Player
  input is strictly slot-confined and checked by a verified negative parser to ensure it cannot escape its data cell into system instructions.

#### `dregg-storage-templates` and `dregg-stream-ingest`
- [`dregg-storage-templates/src/cap_inbox.rs`](file:///Users/ember/dev/breadstuffs/dregg-storage-templates/src/cap_inbox.rs): Standard cell templates for `CapInbox` (deposit accounting + ring root),
  `ProgrammableQueue`, `PubSubTopic`, and `BlindedQueue` (custom ZK verifier).
- [`dregg-stream-ingest/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-stream-ingest/src/lib.rs): Normalized live chat events (YouTube Super Chats, Twitch cheers, TikTok gifts) into paid,
  weighted ballots for collective voting.

---

## 2. The Diaspora: How Ideas and Subsystems Spread Out

When `breadstuffs` was archived, its core components migrated to specialized repositories across `/Users/ember/dev/`.

```
breadstuffs Subsystem                 Descendant Repository                   Key Transformation
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
Solana Bridge & Settlement    ───▶   dragons-clutch ──▶ dclutch             Decomposed monolith into 8 SBF programs,
                                                                             2,646 Lean theorems, Cohort 17 on devnet.
Store-and-Forward CapTP       ───▶   fn                                      Transformed into formal RFC 9171–9174
                                                                             BPv7 bundle protocol with ACL2 proofs.
Claim & Receipt Ledgers       ───▶   verekos ──▶ minidregg                   Paused EKOS half (2026-10-19); carried
                                                                             claim/receipt model into minidregg.
Polisware Non-Domination      ───▶   svenvs                                  Formulated the svenvs key insight:
                                                                             "govern trace-shape, never motive."
Blocklace / Cordial Miners    ───▶   nanodregg ──▶ obend                     Discarded DAG complexity for Simplex BFT
                                                                             (`Obend.Consensus.Simplex`).
```

### 2.1. Solana Settlement: `dragons-clutch` $\to$ `dclutch`
The multi-chain Solana work in `breadstuffs` (`solana-lock`, `solana-settlement`, `dregg-bridge`) moved first into `dragons-clutch`
(gen-1, a 2.15 MB monolith ELF) and was subsequently rewritten into `dclutch` (gen-2). As documented in Strand 12:
- Replaced the monolithic WAVE runtime with **8 discrete SBF programs**;
- Proved 2,646 Lean theorems establishing balance conservation and clearing fairness;
- Deployed Cohorts 8 through 17 on Solana devnet (`clutch.dregg.pro`), culminating in the first retired market on any chain
  on 2026-09-06 (`AvKSizb7...`).

### 2.2. Asynchronous Federation: `fn` (BPv7 & NNTP)
The store-and-forward capability relay from `captp/src/store_forward.rs` and the decentralized news/federation mechanics evolved
into `/Users/ember/dev/fn/` ("formal news"):
- Built as an NNTP news server where **ACL2 makes every decision**;
- Implemented the full **Delay-Tolerant Networking (DTN) Bundle Protocol v7 (BPv7)** per RFC 9171, RFC 9172 (BPSec), RFC 9173, and RFC 9174;
- Namespaces in ACL2:
  - `fn-bpp-`: Primary bundle blocks (CRC-16/CRC-32C, `dtn` and `ipn` endpoint IDs, fragment fields);
  - `fn-bpb-`: Canonical bundle frame codec;
  - `fn-bpn-`: Autonomous BPv7 forwarding node and RFC 6.1.1 status-report engine;
  - `fn-bpf-` & `fn-bpfr-`: Resumable bundle fragmentation and reassembly over overlapping slices;
- Keystones certified in ACL2: `fn-bpp-decode-of-encode`, `fn-bpc-dec-yields-shape`, and `fn-bpp-accepted-input-is-canonical-by-construction`.

### 2.3. Claim/Receipt Ledgers: `verekos` $\to$ `minidregg`
The verifiable audit and receipt tracking pioneered in `auditable-fund` and `pg-dregg` was systematized in `/Users/ember/dev/verekos`:
- Built 190 Lean theorems modeling claim-and-receipt ledgers over an enforced, Mathlib-free `WorldCore` boundary.
- Pinned minidregg theorems: `pinHolds`, `transclusion_pinned`, `toCausalPreimage_injective`, `transclude_uncovered_refused`.
- On 2026-10-19 (commit `89238335a` / `8972945`), Ember paused the EKOS half (`project/CLOSEOUT-2026-10-19.md`) and merged the
  claim/receipt architecture directly into `minidregg`.

### 2.4. Polisware and the `svenvs` Realization
The mathematical link between `metatheory/Polis` and `/Users/ember/dev/svenvs` was captured in
[`project-polis-svenvs-key-insight.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-polis-svenvs-key-insight.md):
> *"svenvs resolves the protected-remainder paradox FOR ENFORCEMENT, not for epistemology. The move: the inhabitant is the
> $\forall$-quantified term the proof never reasons about, so the shadow is real-but-INERT. And the floor is NEGATIVE and
> least-restrictive.*
>
> *The consequence that makes polisware possible: the same $\forall$-blindness that protects the remainder makes the politician
> UNGOVERNABLE-BY-INTERIOR. Therefore govern TRACE-SHAPE, not motive. That is not a compromise — it is the only coherent option,
> and it is exactly why `polis_safety` quantifies over an opaque controller that is never inspected. 'Verify the cage, not the animal.'*
>
> *dregg's two floors ARE svenvs's two theorems. The authority floor corresponds to `safety_preservation`; the human floor
> corresponds to `corrigibility_floor_holds`."*

In HOL4 (`svenvs/liberty/libertyScript.sml`), Ember proved that the cage is not gratuitously restrictive:
- `Theorem maxpol_sound`: The maximal policy permitting actions that preserve safety is sound.
- `Theorem maxpol_is_greatest_sound`: Every sound policy is a subset of `maxpol`.
- `Theorem envelope_is_least_restrictive`: Any policy permitting an action forbidden by `maxpol` is provably unsound for some inhabitant.
- `Theorem envelope_never_overrides_safe_action`: Safe actions pass through untouched.

### 2.5. Consensus Transformation: `nanodregg` $\to$ `obend`
The complexity of the blocklace DAG and the O(history) finality bottlenecks forced a dramatic simplification:
1. `nanodregg` stripped consensus down to its essential state machine, implementing Simplex BFT.
2. In `/Users/ember/dev/obend/lean/Obend/Consensus/Simplex.lean`, Ember unified this consensus lineage:
   - Absorbed `minidregg/Kernel/GenericSimplex.lean`, `GenericSimplexQuorum.lean`, and `GenericSimplexCertificateSafety.lean`;
   - Eliminated DAG traversal in favor of view-based notarization certificates (`NotarizationCert`, `QuorumCert`):
     ```lean
     structure Proposal where
       view : View
       height : Nat
       parent : Block
       turn : Option Obend.Vault.VaultTurn
       deriving BEq

     structure Message where
       sender : NodeId
       view : View
       kind : Kind
       value : Argument
       deriving BEq
     ```
   - Bound block payloads directly to `Option Obend.Vault.VaultTurn`, proving constructive safety and liveness without Mathlib.

---

## 3. What Got Dropped, Parked, or Underelaborated

An archaeological excavation reveals why several brilliant systems in `breadstuffs` were left behind:

```
Dropped / Parked Component        Root Cause of Abandonment / Park
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
pg-dregg                          pgrx cdylib clashed with workspace cargo check; required external PostgreSQL 18
                                  daemon; Lean-FFI bridge was fragile and unmaintained.
fhIR-0 (FHE Order DSL)            Admissibility theorem ("admissible iff it compiles") unproved; FHE public-matrix
                                  envelope too restrictive for general order-book clearing.
Polisware & Commons Arbiter       Real LLM agent runtime harness never deployed; prompt-injection defense relied on
                                  lexical `{{` parsing rather than semantic non-domination.
Auditable Fund / Attested DM      Strictly paper-trading; lacked live broker API integration; prompt integrity was
                                  proven at template-expansion time but output behavior remained unverified.
Blocklace + CapTP                 O(history) finality gate bottleneck; live-gossip eviction bugs; ML-DSA test harness
                                  SIGABRT crashes; multi-round DAG sync complexity.
Cosmos / EVM / Solana Settle      gnark BN254 Groth16 setups relied on single-party dev keys (toxic waste);
                                  lacked on-chain proof-of-holdings derivation to parameterize voting weight.
Mina / Kimchi Light Client        Curve-cycle mismatch (Pasta / Tweedle vs BabyBear); IPA polynomial commitment verifier
                                  exceeded flat gate bounds in production.
```

### Detailed Forensics

1. **`pg-dregg`**:
   The dream of a verifiable Postgres extension with native capability RLS was functionally sound, but operationally marooned.
   Because `cargo-pgrx` manages its own PostgreSQL toolchain, it had to be excluded from the root `Cargo.toml` workspace.
   Whenever core types changed in `breadstuffs/types`, `pg-dregg` was left uncompiled. Furthermore, its Lean link relied on
   an ad-hoc C FFI wrapper (`lean_producer.rs`) rather than a unified compiler.

2. **`fhIR-0`**:
   While the type checker correctly categorized programs into Dark/Shielded/Open tiers, the underlying mathematics required all
   constraint matrices in the Dark tier to be public (due to the limitations of FHE matrix-vector multiplication). This severely
   restricted its usefulness for arbitrary trading products. When the proving lane prioritized Plonky3 recursion, FHE development was paused.

3. **Polisware and the Unification Defect**:
   The meta-review in [`project-polis-unification-correction.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-polis-unification-correction.md) (2026-07-06) found that the celebrated
   "non-domination $\equiv$ light-client-unfoolability" grand unification was a shape identity with zero shared proof content.
   The anti-vacuity checks were checking `accept ≠ True` rather than `∃ c, accept c`, and DECO rung 5 was an empty tautology ($P \to P$).
   The theory was frozen at tag `cut-trace-remainder-0.1` and never wired to live LLM swarms.

4. **Multi-Chain Governance Proof-of-Holdings Gap**:
   As recorded in [`project-chain-participation-epoch.md`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-chain-participation-epoch.md), `dregg-interchain-gov` could verify read proofs from Solana,
   EVM, and Cosmos, but it had **no mechanism to derive voting weight from holdings**. Every voting engine defaulted to a static,
   hardcoded `[u8; 32]` voter set with one-voter-one-vote.

---

## 4. The Grand Revival Roadmap: Unifying with Modern Kernels

Our current formal kernels—**`obend`**, **`minidregg`**, **`svenvs`**, and **`o7vn`**—provide the exact architectural foundation
needed to revive these dropped gems cleanly, eliminating the ad-hoc FFI layers and fragility of the 2026 monolith.

```
Dropped Gem                   Modern Kernel Anchor              Revival Architecture
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
pg-dregg                      minidregg + o7vn                  Implement as a SQL Foreign Data Wrapper (FDW)
(Verifiable Postgres RLS)                                       where row-security policies evaluate against minidregg's
                                                                Mathlib-free WorldCore theorems.
fhIR-0                        obend/Hardware + Leaf             Formulate convex program admissibility as Open Hypergraph
(FHE Convex Product DSL)                                        transformations and Futamura projections in Bend/Lean.
Polisware & Commons Arbiter   svenvs + o7vn                     Ground democratic deliberation in svenvs's HOL4 libertyScript
(Non-Domination Deliberation)                                   theorems; replace regex prompt filters with Oracle7 specialists.
CapTP over Simplex            obend/Consensus + Vault           Embed sturdy capabilities directly into Obend.Vault hyperedges,
(Distributed Capabilities)                                      using Simplex BFT notarizations instead of blocklaces.
Multi-Chain Interchain Gov    obend/Ledger/Seat                 Map cross-chain read proofs (EVM MPT, Tendermint, Solana)
(Non-Custodial Weighting)                                       directly to Obend Ledger Seats with dynamic token-weighting.
Durable Workflow Engine       hosted-durable + minidregg        Express workflow checkpoint replays as deterministic
(Metered Orchestration)                                         minidregg Turn evaluations, eliminating duroxide SQLite locks.
```

### 4.1. Reviving `pg-dregg` via `minidregg` and `o7vn`
In `breadstuffs`, `pg-dregg` suffered from an unmaintained C-FFI link to Lean. In `minidregg`, the entire state transition system
is self-contained, Mathlib-free, and compiles to clean C via `lake build`.
- **Revival Path**: Compile `minidregg/Kernel/World.lean` directly into a PostgreSQL C extension.
- Instead of maintaining complex LRU caches in Rust, PostgreSQL triggers execute `World.step` directly, checking RLS policies as
  pure Lean predicates.
- `o7vn`'s SQL reasoning specialists can synthesize and verify complex JSONPath queries with formal correctness proofs.

### 4.2. Reviving `fhIR-0` via `obend` Open Hypergraphs
`obend` already models categorical computation through [`Obend.Hardware.OpenHypergraph`](file:///Users/ember/dev/obend/lean/Obend/Hardware/OpenHypergraph.lean) and Futamura partial evaluation
in [`Obend.Leaf.Futamura`](file:///Users/ember/dev/obend/lean/Obend/Leaf/Futamura.lean).
- **Revival Path**: Define convex optimization cones as monoidal categories within `OpenHypergraph`.
- The six-part admissibility theorem can be proved by showing that partial evaluation of a Dark-tier product eliminates all private
  matrix parameters, generating a pure public-matvec residual.
- This elevates `fhIR-0` from a speculative type checker to a verified program-extraction compiler for homomorphic clearing.

### 4.3. Reviving Polisware and Commons Arbiter via `svenvs` and `o7vn`
`svenvs` holds the ultimate formal formulation of non-domination in higher-order logic (`libertyScript.sml`).
- **Revival Path**: Port `Metatheory.Polis.polis_safety` directly to the `svenvs` kernel.
- Replace the crude `{{` prompt-injection detection in `commons-arbiter` with semantic evaluation through `o7vn`'s 145 verified
  native specialists.
- When an AI arbiter rules on a dispute, it emits an `o7vn` reasoning certificate proving that its conclusion follows strictly
  from the constitutional rubric without hallucination or premise alteration.

### 4.4. Reviving CapTP over Simplex BFT in `obend`
The fatal flaw of CapTP in `breadstuffs` was its binding to the blocklace DAG, which incurred $O(\text{history})$ tau-ordering costs.
- **Revival Path**: Port CapTP's sturdy references and 3-party handoffs to [`Obend.Consensus.Simplex`](file:///Users/ember/dev/obend/lean/Obend/Consensus/Simplex.lean).
- Instead of reconciling DAG forks, capability handoffs land as linear transactions in [`Obend.Vault.VaultTurn`](file:///Users/ember/dev/obend/lean/Obend/Ledger/Vault.lean).
- Simplex notarization certificates (`NotarizationCert`) provide instant 2-step finality, allowing distributed object capabilities
  to pipeline promises across nodes with zero DAG latency.

### 4.5. Reviving Multi-Chain Non-Custodial Governance in `obend/Ledger`
`dregg-interchain-gov` proved that read proofs could verify cross-chain balances without wrapping tokens, but stalled on the
proof-of-holdings weighting bridge.
- **Revival Path**: Integrate foreign chain read proofs directly into [`Obend.Ledger.Seat`](file:///Users/ember/dev/obend/lean/Obend/Ledger/Seat.lean).
- An incoming EIP-1186 MPT proof (Ethereum) or ICS-23 proof (Cosmos) is verified against the finalized header in a `SeatTurn`.
- The verified balance dynamically parameters the voter's voting power in `Obend.Ledger.Book`, finally realizing the vision of
  true cross-chain non-custodial governance.

---

### Structured Revival Roadmap Table

| Primitive | Original Path in `breadstuffs` | Primary Dropped / Parked Flaw | Modern Host Kernel | Target Architecture & File Seam | Target Assurance Tier |
|---|---|---|---|---|---|
| **`pg-dregg`** | `pg-dregg/` | `pgrx` excluded from workspace; fragile C FFI glue. | `minidregg` + `o7vn` | Lean-compiled Postgres FDW evaluating `World.step` directly. | **Tier 4 (Machine-Checked)** |
| **`fhIR-0`** | `fhir/` | Admissibility theorem unproved; FHE size bounds. | `obend/Hardware` | Monoidal Open Hypergraphs + Futamura partial projection. | **Tier 3 (Sound Semantics)** |
| **`Polisware`** | `metatheory/Polis/` | Anti-vacuity gaps; disconnected from live agents. | `svenvs` | Port `polis_safety` to HOL4; govern traces via `libertyScript`. | **Tier 4 (Machine-Checked)** |
| **`commons-arbiter`** | `commons-arbiter/` | Lexical `{{` injection checks; lacked semantic proof. | `o7vn` | AI rulings emit `o7vn` native reasoning certificates. | **Tier 3 (Certified Reasoning)**|
| **`CapTP`** | `captp/` | Tied to $O(\text{history})$ blocklace DAG; PQ aborts. | `obend/Consensus` | Sturdy refs and 3-party handoffs over Simplex + Vault. | **Tier 4 (Linear Logic QC)** |
| **`interchain-gov`** | `dregg-interchain-gov/` | Lacked dynamic token-weighted balance derivation. | `obend/Ledger` | EIP-1186/ICS-23 read proofs parameterize `Obend.Ledger.Seat`. | **Tier 4 (Proof-Carrying)** |
| **`durable-workflow`** | `durable-workflow/` | SQLite duroxide lock contention; C-int ABI bugs. | `hosted-durable` | Checkpoint replays evaluated as deterministic `Turn`s. | **Tier 3 (State-Machine Safe)**|
| **`grain-commons`** | `grain-commons/` | Operated-layer Sandstorm `.spk` package debts. | `verekos` | Claim/receipt transclusion graphs replace `.spk` files. | **Tier 3 (Receipted Pedigree)** |

---

## 5. Primary Source Index

### Repositories and Git Commits
- `/Users/ember/dev/breadstuffs`:
  - `89238335ad61` (2026-08-08): Exclusion-by-past over blocklace DAG.
  - `0eccd772d134` (2026-08-09): Consensus literature pass (exclusion, catch-up, round gate).
  - `0aba72c65788` (2026-07-29): Ethereum sync committee rotation moved to Lean.
  - `dba55c04b312` (2026-07-29): Removal of accidental `DREGG_LANE_AA_MUTANT` bypass.
  - `53efc5503`, `b997f9cef`, `ee9f9d887`, `35af20966` (2026-07-11): 25-lane EVM settlement contract suite.
  - `d2181916c`, `d78b8512b` (2026-07-24): Fix for `dregg-pq` `SIGABRT` test suite aborts.
- `/Users/ember/dev/verekos`:
  - `89729458b9ad` (2026-10-19): Closeout of EKOS half; migration of claim/receipt model to `minidregg`.
- `/Users/ember/dev/obend`:
  - `5f17752` (2026-10-31): Wave 3 architecture; Simplex consensus and multi-cell vault integration.
- `/Users/ember/dev/fn`:
  - `43e6136d6`, `05c318793`: BPv7 bundle protocol implementation and lock discipline verification.

### Goal and Architecture Documents
- [`/Users/ember/dev/breadstuffs/GOAL-FEDERATION.md`](file:///Users/ember/dev/breadstuffs/GOAL-FEDERATION.md): Living federation execution goal and $n=4$ milestone.
- [`/Users/ember/dev/breadstuffs/GOAL-MULTICHAIN-SETTLEMENT.md`](file:///Users/ember/dev/breadstuffs/GOAL-MULTICHAIN-SETTLEMENT.md): 25-lane multi-chain proof settlement and wrap architecture.
- [`/Users/ember/dev/breadstuffs/GOAL-MINA-SEMANTIC-LIGHTCLIENTS.md`](file:///Users/ember/dev/breadstuffs/GOAL-MINA-SEMANTIC-LIGHTCLIENTS.md): Bidirectional semantic light client requirements.
- [`/Users/ember/dev/breadstuffs/docs/reference/READING-BLOCKLACE-2026-08-08.md`](file:///Users/ember/dev/breadstuffs/docs/reference/READING-BLOCKLACE-2026-08-08.md): Foundational literature review of Cordial Miners.

### Claude Memory Files
- `project-federation-payoff.md`: Detailed root-cause analysis of the $O(\text{history})$ finality gate bug.
- `project-polis-lean-corpus.md`: Complete census of the 66 Polis Lean files.
- `project-polis-svenvs-key-insight.md`: Derivation of trace-shape governance from svenvs $\forall$-blindness.
- `project-polis-unification-correction.md`: Adversarial meta-review of Polis claims and anti-vacuity corrections.
- `project-chain-participation-epoch.md`: Architectural specification of the 25-lane cross-chain settlement format.
- `project-lightclient-stark-true-peers.md`: Analysis of folding verification gates across foreign chains.

### Agent Transcripts (`cv`)
- `5d12f365`: Achieved $n=4$ cross-node stream finality payoff (2026-07-07).
- `a56148a1`: Formalization of the 66 Polis Lean files and svenvs connection (2026-07-04/06).
- `28920d6e`: Launch of the multi-chain participation campaign and 25-lane census (2026-07-11).
- `2ed94bdd`: Mina Kimchi/Pickles Lean verifier development on Devnet block 539508 (2026-07-26/28).
- `ad7d9679`: Sub-agent `reader-blocklace` literature pass on Almeida & Shapiro (2026-08-08).
