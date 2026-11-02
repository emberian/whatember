# whatember — Verifiable Compute, Merkleized Agent Proxies & Formal Silicon Assurance

**Live Site:** [https://emberian.github.io/whatember/](https://emberian.github.io/whatember/)  
**Companion Visual Essays:** [https://emberian.github.io/dregg-microsites/](https://emberian.github.io/dregg-microsites/)

`whatember` is a multi-tab, primary-source technical website and architectural index covering our research and engineering across **Workload Verification & Training-Set Absence Proofs**, **Merkleized Agent Proxies & Capability Gateways**, **Multi-Vendor Hardware Roots of Trust (`tee-verify`, `seL4`, Confidential GPU E2EE)**, **Formal Silicon Synthesis (`obend`)**, and **Five Running Theorem-Proving Substrates** (Lean 4, HOL4/CakeML/Candle, ACL2, Isabelle/HOL, and TLA+/Kani/MIR).

---

## Site Architecture (`open-strands` Branch: 10 Pages, 41 Interactive Sub-Tabs, 2.29 MB Rendered HTML)

1. **[`index.html` — 01 · Overview & Executive Index](https://emberian.github.io/whatember/index.html)**
   - **1A · Architecture & Thesis**: How hardware attestation, Merkle/MMR history commitments, and algebraic/formal certificates interlock.
   - **1B · Problem → Primitive → Proof Matrix**: Interactive filterable table mapping every verification threat to concrete crates and zero-`sorry` theorems.
   - **1C · Briefing for Quinn & Lucid Computing**: Curated guide to live visual essays (`dregg-microsites`) and reference codebases.
   - **1D · Primary-Source Dossiers**: Direct index of all primary-source dossiers (`sources/01..08-*.md` & `sources/strands/09..19-*.md`, ~1.39 MB total).
2. **[`workload.html` — 02 · Workload Verification, Absence Proofs, zkML & vFHE](https://emberian.github.io/whatember/workload.html)**
   - **2A · Proving Training-Set & Corpus Absence**: 6-phase protocol combining `Blake3Mmr`/`DocTree` commitments, `RangeCertificate` non-omission proofs (`MMR.lean:server_cannot_omit_position`), certified BPE tokenization (`tokenizer`), 3,522-line Lean 4 Brzozowski regex-complement DFAs (`Dregg2/Crypto/Deriv/*`), 4M-token/40ms welded parsing certificates (`AttestedAutomatonWeld8.lean`), zero-budget STARKs (`audit`), and `DARK-TRAINING.md`.
   - **2B · Selvage & Commit-Then-Audit (`AuditSampling.lean`)**: Zero-`sorry` Lean 4 supermartingale bounds ($\mathbb{E}[C_\tau] \le 1/q$), `failOpen_no_legs`, and **78×–308×** boundary exchange cost reduction.
   - **2C · Model Identity, Native `MXFP4` & MoE Router Binding**: 1.56 TB model weight registry (`Kimi-K3`), exact $\le 13$-bit integer dot products for block-32 `MXFP4 (E2M1)` weights, `gpt-oss-20b` 124.4M scale-byte census, and **0.72%-overhead** top-$k$ MoE router gate binding.
   - **2D · Verifiable FHE ($p_{61}$) & Continual Learning**: `CyclotomicInertia.lean` ($p_{61} = 2^{61} - 2^{26} + 1$, algebraic degree 64, 10–40% FHE speedup) and 3,200+ continual-learning STARK proofs.
3. **[`proxies.html` — 03 · Merkleized Agent Proxies, Capabilities & Verified Dataplanes](https://emberian.github.io/whatember/proxies.html)**
   - **3A · The 4 Merkleization Engines**: Zero-dep BLAKE3 MMR proxy (`degg-research/experiments/inclusion-availability`), Wasm `grain-turn` `HISTORY_ROOT_SLOT=3` & `HEAP_ROOT_SLOT=6` ($O(1)$ `grain-fork` & `confined-swarm`), and depth-16 4-ary Sparse Merkle `FactSet` + 120-felt capability forests (`FullForestAuth.lean`).
   - **3B · Tool-Call, ACP & Keyless BYOK Proxies**: `sdk::tool_gateway` (`@[export dregg_deleg_admit]`), `deos-hermes` ACP gateway, and `mini-keys` `SO_PEERCRED` keyless BYOK proxy (`NoKeyMaterialInGrainMemory`).
   - **3C · `zkoracle-live` Outbound HTTPS Proxy**: 2-PC TLSNotary MPC-TLS welded to Dyck JSON & DFA STARKs (`AttestedAutomatonWeld8.lean`).
   - **3D · Verified HTTP Dataplane (`Orb`)**: 312-module Lean 4 HTTP proxy lowered via HOL4/CakeML/Pancake to a verified **1,868-byte x86-64 machine loop** (`ServeExportServes.lean`).
4. **[`hardware.html` — 04 · Hardware Roots of Trust, Multi-Vendor TEEs, `seL4` & `obend` Silicon](https://emberian.github.io/whatember/hardware.html)**
   - **4A · `obend` Silicon Elaborator, FPGA & 6-Stage Equivalence**: 452 Lean 4 modules (`0 sorryAx`), 64-bit hardware CAM (`ExprCAM.lean`), 3-phase glitch-free `ICAP` DPR (**17.89× Verilator speedup**), 5-layer Sky130 PDK DRC proof (`HardwareVerify.lean`), and **6-stage equivalence** across FPGA RTL, AMD `CDNA3` GPU Wavefront ISA, and Ozaki Base-13 `FP4 (E2M1)` Tensor Cores (`SiliconKernel.lean`).
   - **4B · Multi-Vendor TEE Verification & Confidential GPU E2EE**: Pure-Rust `tee-verify` for AWS Nitro, AMD SEV-SNP (Milan/Genoa/Turin), and Intel TDX DCAP v4/v5, plus FIPS 203 `ML-KEM-768` GPU E2EE (`dregg-chutes-e2ee`).
   - **4C · TEE Residual Trust Proof & Bare-Metal `seL4` Microkit**: Empirical 377/1,125 forgery proof (`residual_trust.rs`) and `seL4` Protection Domain 3 BabyBear STARK verifier.
   - **4D · Post-Quantum Capabilities & Proving Physics**: `dregg-pq` (`ML-DSA-65`, `ML-KEM-768`, `X-Wing`, `pqvrf`), Blackwell B200 `clmad`, TPU v6e `CROSS`/`MORPH`, and Zama HPU 409.6 GB/s `ntt_acc_modsw` RTL tap.
5. **[`assurance.html` — 05 · Formal Assurance Kernels, Anti-Vacuity Gates & Red-Teaming](https://emberian.github.io/whatember/assurance.html)**
   - **5A · Five Running Formal Substrates**: Lean 4, HOL4/CakeML/Candle (`svenvs` reflective self-upgrading 1.19 GB x64 compiler discharging Löb’s obstruction + `verifereum` EVM proofs), ACL2 (`fn` 647K LOC + `fn2` 2,705 ACL2 functions in Lean 4), Isabelle/HOL (`o7vn` 0.1 ms MLton binaries), and TLA+/Kani/MIR.
   - **5B · Kernel Evolution**: `breadstuffs` → `minidregg` (Farkas `SysCert` `lawSat_never_unknown`) → `nanodregg` (Clairvoyant call-by-need, `Simplex` BFT) → `obend`.
   - **5C · Anti-Vacuity & Adversarial Red-Teaming**: `CarrierCensus.lean`, `ApexPremiseVacuity.lean`, `forensics`, and the `plonky3-recursion` (`52e1fab`) query-dedup soundness fix (`TwoRegimeQueryBudget.lean`).
   - **5D · Computable Law & Operatorless Agents**: `OPERATORLESS_AGENTS.md`, `leakage-lab`, and 5 CFTC/SEC regulatory comment filings.
6. **[`vision.html` — 06 · The Vision, Decade Lineage (2013–2026) & Swarm Engineering](https://emberian.github.io/whatember/vision.html)**
7. **[`atlas.html` — 07 · Searchable Master Atlas: 38+ Repos, 19 Microsites, 65+ Posters & Papers](https://emberian.github.io/whatember/atlas.html)**
8. **[`deos.html` — 08 · DeOS, MiniDregg, NanoDregg, DelveTalk & The `breadstuffs` Diaspora](deos.html)**
   - **8A · DeOS, MiniDregg, NanoDregg, DelveTalk & Spween**: Complete operating system and live-programming stack (`DelveTalk` 18-opcode bytecode + Smalltalk-80 environment, `Spween` scene graph, `Preoscript`, and `OBend` hardware unification).
   - **8B · `breadstuffs` Diaspora I (Kernels, Circuits & Crypto)**: How `bread-kernel`, `bread-circuit`, `bread-stark`, and `bread-Poseidon2` split into `minidregg`, `nanodregg`, and `obend`.
   - **8C · `breadstuffs` Diaspora II (DeOS Surfaces & `starbridge`)**: `deos-ui`, `spween`, `preoscript`, `delvetalk`, `starbridge` MCP/WebSocket bridge, and how to take back up the declarative visual desktop surface.
   - **8D · `breadstuffs` Diaspora III (`dreggnet`, Worlds & PoA)**: P2P gossip, Proof-of-Agency (`poa`), interactive worlds (`mud`, `don`), and deterministic world-tick verification.
   - **8E · `breadstuffs` Diaspora IV (Federation, Chains & Polisware)**: Cross-chain bridges (Mina/Solana/Ethereum), Polisware civic governance, and `commons` resource accounting.
9. **[`verticals.html` — 09 · All Verticals: Cognitive Learning, ISAs/Math, Markets, Residents & Interiority](verticals.html)**
   - **9A · Cognitive Learning (`abcdeez`, `factshift`, `EKOS`/`verekos`, `teach`)**: Non-stationary bandit spaced repetition, 4-axis competence vector, and formal skill graphs.
   - **9B · Custom RISC ISAs (`absass`), RNS Math (`intmat`/`intmat2`) & Physics (`eshkol`, `torchship`)**: Absolute Ass RISC ISA, exact integer RNS matrices, `graphplay`, and relativistic spacecraft telemetry.
   - **9C · Prediction Markets (`dclutch`, `joshi`, `pbot1`) & Mina ZK**: Combinatorial LMSR + Bregman projection in Lean 4/Rust, autonomous market-making engines, and Mina/Kimchi/Pickles recursive ZK.
   - **9D · Resident Minds (`allgame`, `tulip`, `fn`/`fn2`), Games (`don`, `automatafl`) & `audec`**: Persistent autonomous minds, 322-tool `fn` with 5-tier context compression, GPU evolution worlds, and verified neural audio codecs.
   - **9E · Machine Interiority (`comp-theo`), The Bridge, Interpretability (`negstab`, `formal-organisms`) & Social Choice**: Phenomenology of artificial minds, model organisms of negotiated stabilization, and formal social choice (`socchoice`, `law`).
10. **[`triage.html` — 10 · Metamanagement, Unclosed Cycles (`C1`–`C15`), Revival Candidates & Human Triage (`H1`–`H15`)](triage.html)**
    - **10A · Swarm Metamanagement & `cv distill`**: Quantitative continuity architecture (`21.5 / 24` recall vs `0.5 / 24` handoff notes), `CLAUDE.md` stratigraphy, and `mission-control`/`helm`.
    - **10B · Portfolio Maturity Matrix (`L0`–`L4`) & 15 Unclosed Engineering Cycles (`C1`–`C15`)**: Concrete closure pathways across all 374 `~/dev` directories.
    - **10C · Top 15 Revival Candidates ("Take Back Up")**: High-leverage dormant gems now unlocked by `minidregg`/`nanodregg`/`obend`/`svenvs`.
    - **10D · 15 Struggling Areas Needing Human Attention (`H1`–`H15`)**: Architectural forks, multi-worktree divergences, and taste judgments that only Ember can resolve.

---

## Primary-Source Dossiers (`sources/` & `sources/strands/`)

| # | Dossier File | Size | Topic |
|---|---|---|---|
| 01 | [`sources/01-parsing-query-aggregation-absence.md`](sources/01-parsing-query-aggregation-absence.md) | 74 KB | Parsing Certificates, Attested MMR Queries, Regex-Complement DFAs & Training-Set Absence Proofs |
| 02 | [`sources/02-merkle-agent-proxies-and-dataplanes.md`](sources/02-merkle-agent-proxies-and-dataplanes.md) | 82 KB | Merkleized Agent Proxies, Capabilities, `grain-turn` MMR/Heap Roots, `zkoracle-live` & Verified `Orb` Dataplane |
| 03 | [`sources/03-hardware-tee-sel4-and-capabilities.md`](sources/03-hardware-tee-sel4-and-capabilities.md) | 77 KB | Multi-Vendor TEE Verification (`tee-verify`), Confidential GPU E2EE, TEE Residual Trust, `seL4` & Post-Quantum Crypto |
| 04 | [`sources/04-workload-verification-zkml-vfhe-selvage.md`](sources/04-workload-verification-zkml-vfhe-selvage.md) | 70 KB | Workload Verification, Selvage Commit-Then-Audit (`AuditSampling.lean`), Native `MXFP4`, MoE Router Binding & $p_{61}$ vFHE |
| 05 | [`sources/05-formal-assurance-kernels-and-redteaming.md`](sources/05-formal-assurance-kernels-and-redteaming.md) | 77 KB | Formal Assurance Substrates, Farkas `SysCert`, Anti-Vacuity Gates (`CarrierCensus.lean`), Red-Teaming & Computable Law |
| 06 | [`sources/06-vision-origins-and-complete-project-atlas.md`](sources/06-vision-origins-and-complete-project-atlas.md) | 89 KB | The Vision, Decade Lineage (2013–2026), Swarm Engineering (`redregg` & `cv`) & Complete Project Atlas |
| 07 | [`sources/07-obend-silicon-fpga-and-latest-dregg.md`](sources/07-obend-silicon-fpga-and-latest-dregg.md) | 78 KB | `obend` Silicon Elaborator (`ExprCAM`, Futamura, 3-Phase `ICAP` DPR), Sky130 PDK DRC & 6-Stage FPGA/CDNA3/FP4 Equivalence |
| 08 | [`sources/08-october-november-2026-stratum.md`](sources/08-october-november-2026-stratum.md) | 72 KB | Late Oct–Nov 2026 Stratum: `svenvs` & `hol-reflection`, `verekos`, `o7vn`, `fn2`, `negstab` & `forensics` |
| 09 | [`sources/strands/09-deos-minidregg-nanodregg-delvetalk-deep-dive.md`](sources/strands/09-deos-minidregg-nanodregg-delvetalk-deep-dive.md) | 64 KB | Deep Dive: `DeOS`, `MiniDregg`, `NanoDregg`, `DelveTalk`, `Spween`, `Preoscript` & `OBend` Hardware Unification |
| 10 | [`sources/strands/10-cognitive-learning-abcdeez-factshift-ekos.md`](sources/strands/10-cognitive-learning-abcdeez-factshift-ekos.md) | 80 KB | Cognitive Learning & Adaptive Memory: `abcdeez`, `factshift`, `EKOS`/`verekos`, `teach`/`sensei` & `notecard` |
| 11 | [`sources/strands/11-isa-compilers-physics-math-substrates.md`](sources/strands/11-isa-compilers-physics-math-substrates.md) | 89 KB | Custom RISC ISA (`absass`), `dhttp`, `intmat`/`intmat2` RNS Matrices, `graphplay`, `eshkol` & `torchship` |
| 12 | [`sources/strands/12-markets-dclutch-solana-joshi-mina-zk.md`](sources/strands/12-markets-dclutch-solana-joshi-mina-zk.md) | 77 KB | Combinatorial Prediction Markets (`dclutch`), `joshi`/`pbot1`/`polymarket-arb` & Mina/Kimchi/Pickles Recursive ZK |
| 13 | [`sources/strands/13-residents-bots-games-worlds-audec.md`](sources/strands/13-residents-bots-games-worlds-audec.md) | 85 KB | Resident Minds (`allgame`, `tulip`, `fn`/`fn2`), Games (`don`, `automatafl`, `c6-4x`, `mud`) & `audec` Audio Codecs |
| 14 | [`sources/strands/14-interiority-bridge-interpretability-organisms.md`](sources/strands/14-interiority-bridge-interpretability-organisms.md) | 87 KB | Machine Interiority (`comp-theo`), The Bridge, Interpretability (`gowexp`, `negneg`, `negstab`, `formal-organisms`) & Social Choice |
| 15 | [`sources/strands/15-metamanagement-open-cycles-revival-triage.md`](sources/strands/15-metamanagement-open-cycles-revival-triage.md) | 87 KB | Metamanagement, Unclosed Cycles (`C1`–`C15`), Top 15 Revival Candidates & Human Triage (`H1`–`H15`) |
| 16 | [`sources/strands/16-breadstuffs-kernel-circuits-crypto-diaspora.md`](sources/strands/16-breadstuffs-kernel-circuits-crypto-diaspora.md) | 42 KB | `breadstuffs` Diaspora I: Kernel (`bread-kernel`), Plonky3 STARK Circuits & Cryptographic Primitives |
| 17 | [`sources/strands/17-breadstuffs-deos-surfaces-starbridge-diaspora.md`](sources/strands/17-breadstuffs-deos-surfaces-starbridge-diaspora.md) | 46 KB | `breadstuffs` Diaspora II: `deos-ui`, `spween`, `preoscript`, `delvetalk`, `starbridge` & `deos-hermes` |
| 18 | [`sources/strands/18-breadstuffs-dreggnet-games-worlds-diaspora.md`](sources/strands/18-breadstuffs-dreggnet-games-worlds-diaspora.md) | 72 KB | `breadstuffs` Diaspora III: `dreggnet` P2P Gossip, Proof-of-Agency (`poa`) & Interactive Worlds (`mud`, `don`) |
| 19 | [`sources/strands/19-breadstuffs-federation-chains-commons-diaspora.md`](sources/strands/19-breadstuffs-federation-chains-commons-diaspora.md) | 50 KB | `breadstuffs` Diaspora IV: Federation, Cross-Chain Bridges, Polisware Civic Governance & `commons` |
