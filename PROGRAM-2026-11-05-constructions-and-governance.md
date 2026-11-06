# Program proposal: every idea as a mature construction, aimed at technical governance of training and inference (2026-11-05)

Status: proposal for ember, written after the Lucid brief and a Kagi/arXiv/ePrint sweep. Nothing launched.
Companion: `LUCID-INTERVIEW-BRIEF-2026-11-05.md`, `zkml-research/docs/{AGENDA,VERDICTS,FRONTIER-QUEUE,COMPOSITIONS}.md`,
`whatember/sources/strands/15-...` (cycles C1-C15, revival list, H1-H15).

---

## 0. What changed in the world since the August campaign

Our notes have zero mentions of the first three. They change where effort is worth spending.

1. **FlashProve (Anthropic Frontier Red Team, 2026-11-02, Apache 2.0, github.com/anthropics/FlashProve, v0.16.0,
   "not maintained, not accepting contributions").** Hash-based IOP (code proximity + linear constraints + lookups),
   Llama 4 Maverick 400B MoE on a 4-bit public conversion, one H100: 110 tok/s prefill at batch 24, 18.78 MB per
   1,024-token request, 17 s CPU verify, ~70-95x over vLLM, 39 min offline commitment good for ~16M requests.
   Lean 4 top-level theorems for completeness, soundness (`q/2^124 + 2^-101`), zero knowledge in the ROM, backed
   by an executable Lean verifier; the fast C++ verifier is unverified. Greedy decoding only, integer arithmetic,
   architecture not hidden, 1,024-token context, side channels out of scope. Authors: Rinberg, Allain, Chiesa,
   Christ, Dalal, Fenzi, Mayer, Weissenberg. Rinberg is the exfiltration-security author in our prior-art note.
   **AGENDA's "the open position is vacant" is now false for the inference prover.** It is still vacant for
   everything around the prover, which is where our portfolio actually lives.
2. **SASH (Singapore AI Safety Hub, Sep 2026)** open prototype on Stwo (Circle STARK, M31, Blake2s, LogUp, Freivalds
   for weight matmuls): Llama-3.1 8B greedy, 4,096+512 tokens in 1.0 h on one H100, 79.0M committed cells per
   position, $3-5 per request, 18.5 GiB proof, 100 bits under the FRI conjecture. Their cost model is "positions/s
   = R / c" with R = 99M cells/s loop-bound and 2.1B cells/s commit-bound. 42% of GPU time is lookup-column
   generation. Projects 1T dense at 32-48 h per request. Not ZK, not audited.
3. **Peigné, Nguyen, Wang, "Proposals and challenges for zero-knowledge verification of frontier AI training"
   (arXiv 2606.05433, v3 2026-10-21, 71 pp).** Pre-committed spec + inter-node traffic observation + live Merkle
   commitments to intermediate computation + genesis proofs + beacon-selected step proofs with bit-exact BF16/FP32
   semantics + ex-ante attestations as running invariants; zkVM with BF16/FP32 precompiles as reference. This is our
   DARK-TRAINING + AuditSampling design, published by a third party. Our notes cite 2606.05433 nine times; check
   whether they cite v1 or v3 and whether our rank-1/low-rank/Freivalds-backprop virtualization is in it.
4. **DiFR (2511.20621, vLLM integration)** and **TOPLOC** are what Amodo/Plan A grade as the "recomputation
   algorithms" workstream (active). Both are tolerance-based (AUC, LSH). Zamir's theorem says every tolerance is a
   steering channel. Nobody in that workstream has said so in print.
5. **Gargiulo & Kulp, "Workload Identification with Physical Side Channels" (2609.00309)**: external 10 MHz power
   traces on H200, 97% train/infer/non-AI, hardened against four evasions, diluted LoRA at 48-88% before a rescue
   rule. Dataset released. This is Lucid's "How" claim and we have nothing here.
6. **Plan A / Amodo SitRep**: of 17 inference-only-retrofit workstreams, 4 active, 7 not on track, 5 not started.
   "Not started": new TAP types, reproducible inference stack, network reproducibility, frontier recomputation
   algorithms, recomputation red-teaming. "Not on track": recompute server security, verification reporting,
   TAP installation assurance, physical audits, side-channel mitigation and wardens.
7. **ArkLib (Verified-zkEVM, EF, Lean 4 over Mathlib + VCV-io)** now covers IOR, sumcheck, PCS, FRI/STIR/WHIR,
   Fiat-Shamir, BCS. Our notes have 167 mentions; AGENDA calls out an unaudited premise. FlashProve's Lean does not
   appear to use it. Two independent Lean formalizations of the same protocol family now exist beside Selvage.
8. Proof-system frontier: holography accumulation (2026/538, stateless PCD for lincheck/checkable-subspace
   SNARKs), ProtogaLattice (2026/1317) and LatticeFold+, TensorZKP (2026/1250: sumcheck + Spielman code on tensor
   cores, 2^25 gates in 215 ms, HyperPlonk/Brakedown), Chimera (2026/1388 GPU sumcheck for Spartan), zkDuel
   (Triton sumcheck kernels), DATE'26 binary-tower sumcheck on GPU. ZK-regex at PoPETs 2026 (2026/1284, ZK Email,
   Circom, DFA-based). zkVM SoK 2026/525 and contract-validated benchmarking 2026/1729.
9. Lucid's AIAB and logger stack (see brief): no completeness, unverifiable sampling, model identity not a weight
   digest, `policy.forbid` evaluator "formally verified upstream, integration in development."

Implication in one line: **the prover race is being run by people with H100 fleets and we should compose with
them, not against them. Our comparative advantage is the surround: audit theorems, absence and policy
certificates, model identity, training governance, agent-proxy accountability, verified translations end to
end, and the refusal to grant tolerance.**

## 1. The maturity ladder (what "maturely demonstrating" means, so it can be a gate)

Every idea gets a rung. The program is "move each construction up one rung, in dependency order, never down."

| Rung | Name | Gate (all of it, checked by a different agent than the builder) |
|---|---|---|
| L0 | idea | a note in `notes/` with a falsifier stated |
| L1 | statement | Lean statement, `#assert_axioms`-clean, passed the anti-vacuity gate (`forensics`, CarrierCensus-style carrier census, no `P -> P`, hypotheses inhabited by a witness) |
| L2 | construction | executable (Rust/Lean-extracted) whose accept decision routes through the L1 statement; byte-identity between emitted object and proved object (no twin); counts-based cost model, not wall clock |
| L3 | demonstration | runs end to end on a real artifact (a shipped checkpoint, a real transcript corpus, a real TEE quote, a real FlashProve proof) with a public microsite that shows the receipt and lets a stranger re-verify |
| L4 | composed and attacked | composed with at least one external stack (FlashProve, Stwo, ArkLib, Lucid AIAB, tee-verify against a live quote) and survived a written adversarial audit whose negative findings are published with the construction |

Rules that make the ladder real (they are the lessons already paid for, now as gates):
- **Statement audits are a standing gate, not a campaign** (C12). Every L1 landing runs `forensics`; every lane
  brief forbids vacuous and tautological statements by name.
- **Lean-first is a generator, not a law** (C9). One metaprogram emits AIR + Rust call surface; CI fails on any
  hand-written `air.rs`/`builder.rs` constraint. Build this before widening any circuit lane, or every lane
  re-violates the law.
- **No mirrors, no twins.** A Rust reimplementation that is "equivalent" to the Lean is a mirror unless the
  equivalence is a theorem or a byte-identity receipt.
- **Refute-then-repair.** A refutation lane must land the repaired statement in place.
- **Counts over clocks.** Field-op counters are the cost model; hbox wall clock is a calibration.
- **Narrow tests.** `-E 'test(...)'`, never bare `-p`.

## 2. The portfolio, placed on the ladder, grouped by governance claim

Rungs below are my reading of the dossiers plus today's repo checks; the first task of each lane is to confirm
or correct its own rung with a witness.

### G-A. "This model, these weights, this output" (inference provision)

| Construction | Where | Rung now | Next rung gate |
|---|---|---|---|
| Commit-then-audit theorem (three legs, adaptive, fail-closed) | `minidregg/Selvage/AuditSampling.lean` | L1 (0 sorry) | L2: instantiate the abstract checker with FlashProve's `cp_verify` as the audited proof (ε_chk from their theorem), a drand/pqvrf beacon as the ε_beacon leg, and a Blake3 MMR of request commitments as the ε_bind leg; emit a Rust auditor whose alarm routes through the Lean predicate. L3: run it over 10k Maverick requests on hbox/VCF cluster with injected corruptions; publish `E[C_τ]` vs 1/q. |
| Native-format exactness (MXFP4 13-bit block dots, E8M0 spread) | `zkml-research/phase0`, `docs/mx-formats.md` | L1/L2 (measured, census) | L2: a Lean statement that an MXFP4 block dot in the prover field equals the OCP reference, order-independent; L3: FlashProve proves a *4-bit conversion*; show the delta between their integer model and the shipped MXFP4 gpt-oss checkpoint as a concrete Zamir-style steering budget, or show it is zero. |
| Model identity registry v2 (per-expert Poseidon2 roots, router binding) | `zkml-research/registry`, `notes/moe-router-binding.md` | L1 design, v1 tool L3 | L2: implement v2 commitment for gpt-oss-20b in the prover field; prove `R_{ℓ,e}` opening binds the active expert; L3: cross-check against FlashProve's published Maverick commitment ID (can one registry entry name both?). |
| Boundary-not-interior matmul (sumcheck virtualization, 78-308x) | `Assurance/ZkmlMatmulSumcheck.lean`, `boundary_exchange_rate.py` | L1 + counts | L2 via COMPOSITIONS C1 (Dumas-Kaltofen-Villard certificates + proved FS compiler): Freivalds/rank certificates as the audited object. SASH already uses Freivalds for weights; ours is the proved transform. |
| Hollow-LLM microsite "Which model?" | `~/src/dregg-microsites/which-model` | L3 | L4: extend to "which model answered THIS FlashProve proof" using their commitment ID + our registry. |
| Verifiable dark continual learning (rank-1 Freivalds backprop, low-rank boundary) | `docs/DARK-TRAINING.md`, `Rank1GradientCheck.lean`, `ZkmlLowRankUpdate.lean` | L1 | L2: one LoRA step on a real adapter, proved at the boundary; compare against Peigné et al. step-proof costs. |
| vFHE p61 / joint modulus | `CyclotomicInertia.lean`, G1-G6 in FRONTIER-QUEUE | L1 + measured | unchanged; G1 single-prime afternoon experiment is still the cheapest unblock. Lower priority than G-A above for governance. |

### G-B. "Nothing in this corpus/log matches P, and the log is complete" (absence and policy)

| Construction | Where | Rung now | Next rung gate |
|---|---|---|---|
| Regex complement DFAs, `tableDfa_faithful`, finiteness | `Dregg2/Crypto/Deriv/*`, `breadstuffs/dfa` | L2 | L3: run the dossier-01 §5 protocol on a real corpus (e.g. 1M FineWeb docs) for a benchmark-canary pattern and publish the Count=0 receipt + verify time. Compare to ZK Email 2026/1284 (Circom DFA, no complement, no CFG). |
| Parsing certificates + slot confinement + 8-lane weld | `Cfg.lean`, `CfgCompact`, `HandlebarsGuarded`, `AttestedAutomatonWeld8` | L2 (4M tok / 40 ms) | L3: a "substring matches at position i" certificate as a first-class object: (content commitment, i, pattern, proof) with a Lean statement `substringAt c i P`, position-binding theorem, and a JSON receipt a stranger verifies. This is the primitive ember named; it is also exactly Lucid's `policy.forbid` evaluator. |
| MMR non-omission, gap exclusion, zero-count aggregation | `MMR.lean`, `AttestedQuery.lean`, `dregg-query`, `audit` | L2 | L3: ship as a logger evidence format (`mmr-evidence/v1`) that satisfies AIAB's `InputVerifier.verify(text, evidence, scope) -> commitment`; equivocation test between two auditors. L4: hand it to Quinn. |
| Recursive aggregation anchored at genesis | `RecursiveAggregation.lean`, `turn-prover` | L2 | L3: fold the corpus run above into one proof; publish verify-time vs N. |
| Properties on the form (CFG membership, JSON schema, chat-turn framing) | `Cfg.lean`, `DyckStackEmit` | L2 | L3: the same receipt shape as substring-at-position, for "record i is well-formed under grammar G". |

### G-C. "Where it ran, on what, under what root of trust" (hardware)

| Construction | Where | Rung now | Next rung gate |
|---|---|---|---|
| Multi-vendor quote verifier | `tee-verify` (Nitro, SNP, TDX) | L2 (audited 07-25) | L3: verify a live Tinfoil/Lucid TDX quote and an NVIDIA CC GPU attestation report (H100 CC mode) offline; publish the parsed evidence. L4: VCF cluster, bare metal, B300 TEE-I/O. |
| Residual trust forgery experiment | `degg-research/.../residual_trust.rs` | L3 | L4: same construction over AIAB's one-bit report (what can an honest-looking enclave forge if the logger omits?). |
| Verified HTTP dataplane / in-path device | `orb`, `ServeExportServes.lean`, `drorb` | L2 (1,868-byte verified loop) | L3: an in-path "receipt NIC" that commits flow-header hashes to an MMR (Lucid's TAP evidence plane) running the verified loop. Long horizon; name it, do not start it before G-A/G-B L3s. |
| Side-channel workload identification | none | L0 | Decide: ignore (their physics, not ours) or reproduce 2609.00309 on hbox GPUs with their released dataset as an L0->L1 scouting note. I recommend ignore until a VCF slot exists. |

### G-D. "Every agent action was admitted, metered and receipted" (agent provision)

| Construction | Where | Rung now | Next rung gate |
|---|---|---|---|
| Unfoolability ladder R0-R3 | `grain-verify`, `turn-prover` | L2/L3 | L4: third-party verification of a real Claude Code session transcript (cv export) with renter-pinned genesis; this is also the aidev provenance story. |
| Capability forests, tool gateway, Lean admission | `FullForestAuth.lean`, `sdk::tool_gateway`, `dregg_deleg_admit` | L2 | L3: the Lucid "scoped agent mandate" receipt: mandate + MMR + admission proof, verified offline. |
| Keyless BYOK / ACP proxy | `mini-keys`, `deos-hermes` | L2 | L3 only if a demo needs it. |

## 3. Foundational research tracks (the "highest speed STARKs and compositions" ask)

These are questions, each with the cheapest experiment, in the FRONTIER-QUEUE style. None should be started
without a construction above that consumes the answer.

- **F1. Who do we compose with?** Three candidate substrates now exist for the audited proof: FlashProve
  (hash-based IOP, Lean soundness, unmaintained), Stwo (M31, production, SASH's path), Selvage (ours, Lean-specified,
  Rust executed, 152 files). Experiment: take one Maverick request; produce a FlashProve proof; write the Selvage
  `checker` instance that accepts it; count the felts a native Selvage recursion of `cp_verify` would cost. The
  answer decides whether Selvage is a verifier-side composition layer or a prover.
- **F2. Blowup drop and the stale commit bound** (VERDICTS §1b, priced not landed): prover ÷15.2, verifier ×2.28.
  Land it with the `num_queries` pin. This is our single largest unlanded prover lever.
- **F3. Tensor-core sumcheck.** TensorZKP maps sumcheck + Spielman codes to tensor cores (36x over SIMT). Our
  Ozaki base-13 FP4 tensor-core equivalence work in `obend/SiliconKernel.lean` is the verified version of that
  trick. Experiment: BabyBear sumcheck round as an INT8 MMA on an H100, counts vs their 215 ms.
- **F4. Stateless recursion.** Holography accumulation (2026/538) vs our AccRbrFold/shifted BCS: which gives a
  smaller recursion verifier for the audit aggregate? Read-and-compare note first (one lane, one day).
- **F5. Lattice folding** (ProtogaLattice, LatticeFold+): relevant only if vFHE G1-G6 advance. Park.
- **F6. The substring-at-position certificate as a proof-system-independent object.** Define it once in Lean
  (commitment scheme abstract), instantiate for Poseidon2-8 (ours), Blake2s Merkle (Stwo), and FlashProve's
  commitment if its format permits. The point is that a governance receipt should not name a prover.
- **F7. Tolerance is a channel, stated for recompute.** Write the two-page note that applies Zamir to DiFR/TOPLOC
  thresholds, with the numbers, and send it to Amodo/Lucid. Cheapest high-value thing on this list.
- **F8. Binary towers on GPU** (DATE'26) vs our `CharTwoWall`/`AdditiveBaseFold`: we proved the folding; they
  built the kernel. Note only.

## 4. Decisions that are yours before any of this launches

- **H1/C8: which kernel is canonical (Mini vs nano).** Every L2 gate above says "routes the accept decision
  through the Lean"; that is a kernel question. A one-paragraph ruling in `minidregg/board/RULINGS.md` unblocks
  C9 (the generator), which unblocks every circuit lane.
- **Compose with FlashProve, or stay prover-independent?** F1 answers it empirically, but the stance (we
  are the surround, not the prover) is a taste call.
- **Demo order.** My recommendation: (1) audit theorem instantiated on FlashProve proofs, (2) substring-at-position
  + Count=0 corpus receipt, (3) MMR logger evidence for AIAB, (4) tee-verify on a live NVIDIA CC quote. Each is
  2-4 weeks for a small swarm, each lands an L3 microsite, and together they cover Lucid's What/Who/Where.
- **Lane width** (H15): one rule. I would run at most four lanes, one per demo, each a doer that owns its rung gate.

## 5. First two weeks (if you say go)

1. Root reads FlashProve `docs/protocol.md`, `lean/THEOREM.md`, `paper/paper.pdf` and writes `notes/flashprove-read.md`
   with the checker interface the audit theorem needs. One day.
2. Lane A: AuditSampling checker instantiation + Rust auditor + beacon leg. Gate: L2 with injected-corruption
   counts matching `1/q` within sampling error.
3. Lane B: substring-at-position certificate (Lean statement + Rust receipt + verifier CLI) over `AttestedAutomatonWeld8`.
   Gate: L2, then the 1M-document Count=0 run on hbox under `swarm-build`.
4. Lane C: `mmr-evidence/v1` behind AIAB's `InputVerifier` interface, with the equivocation test. Gate: L2;
   hand to Quinn as a PR against a fork.
5. Root: F7 note (tolerance is a channel, for recompute), and the C8 ruling draft for you to sign.
6. Standing: `forensics` on every landing; no lane touches `air.rs` by hand (C9 generator first if any lane needs a
   new constraint).

Not in this program on purpose: side-channel physics, RTT location, vFHE beyond G1, anything that re-runs the
August prover-engineering lanes. Those are either other people's strengths or already priced.
