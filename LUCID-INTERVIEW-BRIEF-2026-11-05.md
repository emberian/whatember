# Lucid Computing interview brief (2026-11-05)

Compiled from lucidcomputing.ai (index, overview, experimentation-cluster, validation-cluster, notes, careers),
their Substack (From Assertions to Evidence, 07-28; Building an adversarial testbed, 07-29; Traffic Shaping
for Workload Classification, 08-04, now 404), their Ashby job board, github.com/Lucid-Computing (10 repos,
six cloned to scratchpad), ai-2040.com Plan A verification supplement, Amodo's SitRep, Kagi, Scry, and
whatember dossiers 01/03/04 plus zkml-research notes. Nothing here is from Hellas.

---

## 1. Who they are

- **Lucid Computing Inc.**, San Francisco, founded early 2025. CEO **Kristian Rönn** (ex-Normative.io, author of
  *The Darwinian Trap*; the "darwinian demons / AI arms race" podcast guy). CTO **Gregory Kollmer** (Columbia).
  Europe-based Director "Connor" (connor@lucidcomputing.ai). Engineers visible in git: Jonathan Ng, Teddy
  Chang, Caleb Parikh, "jon", "milos-product-maker", Alex (logger/proxy), Andriy (tailnet).
- **Quinn Dougherty** (Forall R&D, quinn@for-all.dev) is a *contractor* there, not staff. Quinn's note to you:
  "one of the products im helping them on is this proxy server with merkleization for agents."
- Tagline: "Provable trust infrastructure for frontier AI. Verifiable AI. Proven in hardware."
- Three business lines: (a) **NeoCloud** confidential GPU inference (H100/H200 NVIDIA CC, B200/B300 TEE-I/O,
  Intel TDX hosts) with "AI Passports" (signed receipt per inference: auditor results + policy compliance +
  model identity), data-residency, private fine-tuning; (b) **Lucid Labs** research: a multi-silicon
  Verifiable Studio cluster (H100/H200/B300/MI355X, DPUs/FPGAs/SmartNICs in-path, passive TAPs) operated for
  the **Verifiable Compute Foundation** (CA nonprofit, filed 2026-05-18, ED Samuel Härgestam, Stockholm; free
  access via Research Access Program; Tuesday 10-11am PT office hours; cluster "opening in November");
  (c) **Adversarial testbed with RISE** (Research Institutes of Sweden): 16x H100 retrofit, 18-month program,
  RISE's cyber team red-teams, results published either way. Standards work: Sovereignty Certificates
  (sovcert.org, RATS RFC 9334 + ping-based RTT location), IETF/CCC/OCP/SL5.
- Ecosystem: they are the "builder" arm of **Plan A** (ai-2040.com, AI Futures Project): inference-only
  datacenter retrofits for a US-China pacing agreement. Amodo Design's SitRep grades the 17 workstreams;
  only 4 are active. Rönn wrote one of Plan A's open-problems overviews. Tristan Harris boosts them.
- Hiring (Ashby, live now): MTS Network Engineer, MTS (applied crypto / attestation protocols / proof
  systems / "evidence formats that make a claim about compute independently checkable"; GPU kernel static
  analysis; distributed evidence platform), Data Center Security Architect, **VP of Research**, Head of US
  Policy, policy associate, ops, commercial partnerships. Remote/London allowed on the general req.

## 2. Their "workload verification" problem, decomposed

They frame everything as **four questions a cluster must answer with signed receipts** (validation-cluster page):

| Q | Claim | Their mechanism | Status (their words) |
|---|---|---|---|
| Where | compute is in licensed jurisdiction, not diverted | GPU-TEE-keyed RTT ping to in-facility landmark; sovcert spec; silicon throttling as key-transplant countermeasure | sovcert published; transplant defense "research primitive" |
| How | no undeclared training past threshold | signed **Verifiable Job Manifest** reconciled against shunt-power metering (DC-SCM/BMC), GPU utilization counters, passive optical TAP hashing flow headers into an append-only commitment; **traffic shaping** (bandwidth-capped pod uplinks + randomized inference routing) to make covert training uneconomic | accept target: <=10% error on power-to-compute vs H100 benchmarks |
| What | the model that ran is the evaluated one, weights not swapped | model hashed at load inside GPU TEE; **unpredictable sample of requests recomputed on reference hardware** outside the TEE; bind deployed hash to lab-signed eval record; "model/eval provenance graphs rather than single weight hashes" | bit-exact recompute "being hardened for production"; recompute red-teaming "not started" (Amodo) |
| Who | no misuse (jailbreak, distillation, dangerous requests) | identity + scoped agent mandates + in-path monitoring; **AIAB** (Auditor-in-a-Box) | "in development" |

Plus an **Assurance Node**: collects RFC 9334 evidence from auditors in CVMs, evaluates a formal policy
language (`policy.forbid(...)`, Python `ClaimsAuditor` SDK, "evaluator formally verified upstream, integration
in development"), emits hash-chained signed receipts with heartbeat, revocation, freshness, SPDM at treaty tier.
Explicitly unproven: nation-state resistance, camera binding, unenrolled hardware, recompute hardening.

Their design philosophy (From Assertions to Evidence): verification is a **claim-design problem**. Narrow
decision-relevant claim; minimal disclosure; capture on-site, evaluate off-site via signed receipts;
tier claim strength honestly (assertion / cryptographic / probabilistic). Structured transparency (Trask).

## 3. What their code actually is (github.com/Lucid-Computing)

- **aiab-introspection** (219 files, Python, active daily): "Auditor-in-a-Box". Lab and auditor jointly sign
  an audit **plan** (now a 5-block graph IR: input_logs / classifier / run_python / run_llm / final_report);
  a Tinfoil AMD SEV-SNP CPU CVM ingests **signed agent-transcript logs** from a proxy, runs a restricted
  Python AST plan against `gpt-oss-safeguard-120b` in a separately attested Tinfoil inference enclave,
  returns a schema-bounded signed report (e.g. one bit: `flagged`). Demo target was a GDM demo (Oct 13
  proposal by Caleb); example plan: "are there destructive commands" across agent sessions. Reproducible
  OCI image builds; release pinned by Tinfoil `tinfoil.hash`.
- **The "Merkle logger / WORM"** feeding AIAB is Alex's proxy pushing ~1MB signed segments to `tag:worm`
  receivers. As of 2026-10-23 the real logger evidence format "changes until end of week"; the box still
  uses a stand-in signed-export key. THIS is Quinn's "proxy server with merkleization for agents."
- Their own gap lists (REQUIREMENTS_COMPLIANCE.md, DEFERRED.md, THREAT_MODEL.md) are candid:
  - no completeness: "A malicious authorized logger could omit events before signing"; "Completeness is the
    Logger's job; AIAB verifies integrity only"; no coverage claim; bypass demonstrated in demo.
  - sampling: "Monitor mode uses **unverifiable Bernoulli request sampling**"; deferred: "verifiable random
    sampling from an auditor-committed seed (HMAC or VRF). Sample by token, not request."
  - no transparency log, no durable fork/rollback protection beyond an optional auditor checkpoint; per-boot
    Ed25519 report key.
  - model identity: "The requested model identifier is **not an immutable weight digest**"; `artifact_digest`
    is a blocker ("the current Tinfoil classifier alias is not a weight commitment").
  - egress: one boolean is "not a proven bandwidth limit"; no DP, no fixed-length reports.
  - "No persistence is not proof of memory erasure." Hardware/lifecycle issue "code alone cannot close."
  - policy language: restricted Python AST interpreter, "exactly one classification call".
- **ai-vault**: local-first MCP proxy/firewall with policy control (Mar 2026, dormant).
- **sovereignty-certificate-specification** v0.1.0 draft (Oct 2025): RATS roles, HRoT+TEE ephemeral key
  binding, Location Measurement Agent, anchor fleet, Verifiable Attestation Result.
- enclave config repos (t3-enclave, aiab-*-enclave): Tinfoil measured-image configs. They lean on Tinfoil
  for the whole CVM/attestation layer.

## 4. Overlap map: their mechanism vs what you have built

Everything on the right is open, yours, Lean-checked where stated. Paths are absolute.

| Lucid need | Your artifact | The sharper statement you can make |
|---|---|---|
| Merkleized agent-transcript logger whose completeness they admit they cannot verify | `breadstuffs/dregg-query` (Blake3 MMR, attested slices, paged windows, Count=0 aggregation), `metatheory/Dregg2/Lightclient/MMR.lean` (`server_cannot_omit_position`, `light_client_position_non_omission`), `AttestedQuery.lean` (`server_cannot_omit`, gap witnesses), `degg-research/experiments/inclusion-availability` (zero-dep MMR proxy with `equivocation.rs` split-view detection), `audit/` (`BudgetProof`, `CountProof`) | "Your WORM gives integrity. An MMR with dense range certificates gives **non-omission**: the auditor's window query cannot silently drop a record, and the proof is Lean-checked. Equivocation detection catches a forked history between two auditors." Their deferred item "stronger fork protection" is exactly this. |
| "Unverifiable Bernoulli request sampling" / deferred "VRF from auditor-committed seed, sample by token" | `minidregg/Selvage/AuditSampling.lean` (1,173 lines, 0 sorry): `q = p(1-ε_chk) - ε_bind - ε_beacon`, predictability enforced by type (`corrupt : List Ω → Bool` never sees the coin), `E[C_τ] ≤ 1/q`, `E[Λ] ≤ b/q`, `failOpen_no_legs`; `dregg-pq/pqvrf` (Lean-verified PQ VRF); `notes/audit-sampling-prior-art.md` | Their recompute-a-sample plan IS commit-then-audit. The folklore bound 1-(1-p)^k assumes ε_bind=ε_chk=ε_beacon=0 and non-adaptive corruption. You have the machine-checked composed bound, AND the fail-open refutation: if a recompute timeout is treated as "no alarm", an adversary aborts whenever audited and q collapses. Do NOT claim the statement is novel (Rinberg et al. 2511.02620, eprint 2026/541, covert security). Claim: the three-leg composition + adaptive stopping-time + fail-closed, machine-checked. |
| "Model identifier is not an immutable weight digest"; "provenance graphs rather than single weight hashes"; hollow-LLM | `zkml-research/registry/` (8 frontier checkpoints committed, streaming range-request SHA-256, up to 1.56 TB Kimi-K3; v2 design: per-expert Poseidon2 Merkle roots `R_{ℓ,e}`, 477 KB for all 58 DeepSeek-V3.1 MoE layers); `notes/moe-router-binding.md` (0.72% overhead top-k gate binding); microsite "Which model?" | "A flat SHA-256 over safetensors is the right *registry* commitment but is unopenable by any proof system. Commit per-expert in the prover's own field so a sampled recompute (or a proof) can open only the 3.5% of experts that fired." Hollow-LLM (2607.28884) is the attack their AI Passport must answer. |
| Bit-exact recompute "being hardened for production"; reproducibility workstreams (Amodo #5-#9 mostly not started) | `zkml-research/docs/mx-formats.md`, `phase0/` (exhaustive BF16 census; OCP MXFP4 block-32 E2M1 dot products are exact ≤13-bit integers; 1,382,400 gpt-oss-20b rows fit); `docs/the-position.md` (Zamir Thm 1: ε-approximate float checks admit undetectable backdoors; Spain OSDI'26 exploitable at published params) | "Recompute-and-compare on floats has a tolerance; any tolerance is a backdoor channel (Zamir). MXFP4-native checkpoints make the dot product an integer so 'bit-exact' is a theorem, not a hope." This is directly their "inference reproducibility" and "frontier recomputation algorithms" gaps. |
| Assurance Node policy language, "evaluator formally verified upstream, integration in development"; AIAB restricted-Python plan interpreter | `metatheory/Dregg2/Crypto/{Deriv/*,Cfg,HandlebarsGuarded,SlotConfinement,ZkOracle}.lean` (Brzozowski complement DFAs, `tableDfa_faithful`, parsing certificates `compact_sound`, slot confinement), `breadstuffs/dfa` (3.8k Rust), `AttestedAutomatonWeld8.lean` (4M tokens / 40 ms welded STARK guard), `sdk::tool_gateway` + `@[export dregg_deleg_admit]` Lean admission | "`policy.forbid(pattern)` over transcripts needs *complement* and *structure* or it is bypassable by splitting a token across JSON fields. We have verified regex-complement + CFG parse certificates welded to one content commitment, so 'no record matches P' is a proof, not a classifier score." Also: absence proofs over whole corpora with Count=0 (dossier 01 §5 protocol). |
| Intel TDX / SEV-SNP / Nitro attestation, Tinfoil dependence, "two TEE vendors, compare reports" (deferred) | `breadstuffs/tee-verify` (5.5k Rust, offline quote verification for Nitro, SEV-SNP Milan/Genoa/Turin, TDX DCAP v4/v5), `tee-produce`, `dregg-chutes-e2ee` (confidential GPU TDX attest + ML-KEM-768 envelope), `docs/TEE-VERIFY-AUDIT-2026-07-25.md` | Vendor-independent verifier they could run instead of Tinfoil's SDK path (THREAT_MODEL: "Tinfoil hosts the hardware and remains a party to these assumptions"). |
| "TEE residual trust" / why attestation alone is not evidence | `degg-research/experiments/shielded-baseline/tests/residual_trust.rs`: 377/1,125 forged outcomes pass every local check without a validity proof; 0 with one | Concrete, executable argument for "attested execution + proof", matching their own line "attestation is not proof of source correctness". |
| Transparency log / durable auditor collection / per-boot keys | `grain-verify` R0-R3 unfoolability ladder (renter-pinned genesis, countersigned checkpoints, anti-truncation `receipts.len() >= num_turns`, anti-rewrite, R3 recursive STARK aggregate through Lean `r3VerifyCore`); `turn-prover` (7.7k Rust) | A third party can verify an agent session without trusting the host, which is the AIAB auditor's actual position. |
| Verified in-path devices (FlexNIC, traffic shaper, Assurance Node receipts) | `breadstuffs/orb` 312-module Lean HTTP proxy lowered to a verified 1,868-byte x86-64 loop (`ServeExportServes.lean`), `drorb` QUIC, `obend` silicon elaborator (FPGA RTL / CDNA3 / FP4 tensor-core 6-stage equivalence, Sky130 DRC) | Their job req: "assume every component around you may be hostile" and in-path device assurance is "the hardest unsolved problem". A verified dataplane and a Lean-elaborated FPGA path are the long-horizon answer. |
| Hardware-rooted FLOP counting "the operator can't reset"; power-to-compute estimator | nothing direct; nearest is `obend` silicon work and `fhegg-rtl` | Honest gap on your side. Their side-channel / power work is real physics you have not done. |
| Sovereignty certificates / RTT location | nothing direct | Gap. You can critique (key transplant, relay attacks) but have not built it. |

## 5. Where your skills land in their org

1. **The merkleized agent proxy / logger is unfinished and Quinn is on it.** Alex's signed-segment format was
   still churning two weeks ago; the box has no completeness or fork story. You have shipped exactly this
   three different ways (degg-research zero-dep MMR, dregg-query attested windows, grain-turn Wasm roots) with
   Lean non-omission theorems. Offer: a logger evidence format = MMR root + range certificate + equivocation
   check, drop-in behind their `InputVerifier.verify(text, evidence, scope) -> commitment` interface.
2. **Recomputation soundness.** Amodo grades recompute red-teaming "not started" and recompute server
   security "not on track". The audit theorem + fail-closed result + beacon/VRF leg + MXFP4 exactness is a
   complete research program they are hiring a VP of Research to define. You have the Lean.
3. **Model identity that a proof can open.** AI Passport "model identity" today is a Tinfoil alias. Per-expert
   Poseidon2 roots + router binding is the design that survives hollow-LLM.
4. **Policy evaluator with semantics.** Their `policy.forbid(...)` and restricted-AST plan runner are where a
   verified complement-DFA + CFG certificate engine belongs; it also turns "classifier says flagged" into a
   second, exact evidence tier alongside the probabilistic one, matching their own evidence tiering.
5. **Red-team posture.** Your refute-then-repair discipline, anti-vacuity gates, and the 377/1,125 forgery
   experiment are the house style they say they want ("publish negative results", "breakers never builders").
6. **Formal methods bridge.** Quinn's remit is "guiding AI safety orgs through the formal methods explosion";
   you are the person who has already done the Lean for the primitives he is about to need. Co-authoring
   the claim table / receipt schema / manifest schema (their stated deliverables) as Lean structures with
   theorems is a natural joint output.

## 6. Questions to ask them

- Who chooses the recompute sample and when is the seed fixed? (Same question you raised for Attestable: if
  the operator picks the seed after seeing the request, grinding is free.) Is the beacon drand/Roughtime as
  listed, and is it absorbed before or after the commitment?
- What happens on recompute timeout or non-bit-exact mismatch below tolerance: alarm, or warning? (fail-open)
- What is "model identity" in an AI Passport today: Tinfoil release digest, or a weight commitment? How will
  the "provenance graph" be committed so a sampled recompute can open it?
- Logger completeness: how will the auditor know a segment was dropped before signing? Any plan for a
  dense index / MMR / transparency log, or is it still "logger's job"?
- Policy language: what is the semantics of `policy.forbid`? Regex? Over tokens or bytes? Who proves the
  evaluator correct "upstream"?
- Traffic-shaping post was pulled from Substack (404 today). Why?
- Testbed: what is RISE's red-team scope on the Assurance Node itself (the device that signs receipts)?
- VCF cluster: can an external researcher get bare-metal H100/B300 CC time to test welded STARK guards or
  MXFP4 exact recompute at frontier batch sizes? (Yes per their page; Tuesday office hours.)
- For Quinn specifically: which interface is the proxy exposing to the box, and is the evidence format
  frozen yet?

## 7. Cautions

- Hellas: say "I worked on workload verification at Hellas before; the project became Dregg" and stop. No
  Hellas code or design detail. Everything you point them to is in emberian/* on GitHub.
- Do not claim the sampling theorem statement is a first (see prior-art note). Claim the composition,
  the adaptive schedule, the fail-closed refutation, and that it is machine-checked.
- Their stack is Tinfoil-shaped; be gentle about it. Pitch tee-verify as "a second verifier", not a
  replacement.
- whatember's 1C tab already has the six-codebase table for Quinn; share
  https://emberian.github.io/whatember/ rather than re-explaining.
- Attestable / Hellas / Lucid are "collaborators in the worldsystem", your own words. Keep that register.
