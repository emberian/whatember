# whatember — Verifiable Compute, Merkleized Agent Proxies & Formal Silicon Assurance

**Live Site:** [https://emberian.github.io/whatember/](https://emberian.github.io/whatember/)  
**Companion Visual Essays:** [https://emberian.github.io/dregg-microsites/](https://emberian.github.io/dregg-microsites/)

`whatember` is a multi-tab, primary-source technical website and architectural index covering our research and engineering across **Workload Verification & Training-Set Absence Proofs**, **Merkleized Agent Proxies & Capability Gateways**, **Multi-Vendor Hardware Roots of Trust (`tee-verify`, `seL4`, Confidential GPU E2EE)**, **Formal Silicon Synthesis (`obend`)**, and **Five Running Theorem-Proving Substrates** (Lean 4, HOL4/CakeML/Candle, ACL2, Isabelle/HOL, and TLA+/Kani/MIR).

---

## Site Architecture (7 Pages, 27 Interactive Sub-Tabs)

1. **[`index.html` — 01 · Overview & Executive Index](https://emberian.github.io/whatember/index.html)**
   - **1A · Architecture & Thesis**: How hardware attestation, Merkle/MMR history commitments, and algebraic/formal certificates interlock.
   - **1B · Problem → Primitive → Proof Matrix**: Interactive filterable table mapping every verification threat to concrete crates and zero-`sorry` theorems.
   - **1C · Briefing for Quinn & Lucid Computing**: Curated guide to live visual essays (`dregg-microsites`) and reference codebases.
   - **1D · 8 Primary-Source Dossiers**: Direct index of `sources/01..08-*.md` (~619 KB total).
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

---

## Primary-Source Dossiers (`sources/`)

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
