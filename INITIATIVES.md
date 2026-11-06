# Initiatives register

The one place every initiative is listed, so none is forgotten and none quietly shrinks below the sophistication
it was opened for. The root updates rows from lane reports; lanes include their row in every report. Rungs: L0 idea,
L1 audited Lean statement, L2 construction whose accept decision routes through the statement, L3 end to end on a
real artifact and re-runnable by a stranger, L4 composed with an external stack and adversarially audited in public.
A row's "bar" is the sophistication it must reach before it counts as done; "toy" means it stopped short.

Rule for every lane: **ground first**. Before building, scout what /Users/ember/dev/breadstuffs, minidregg,
zkml-research, degg-research, DreggNet, drorb and the whatember dossiers already have for the problem, write
GROUNDING.md (what exists, what is reused, what is replaced and why), then build on it. Never re-invent what is
there; never keep what is there only because it is there.

| # | Initiative | Owner lane | Repo | Rung | Bar | Next gate | Last report |
|---|---|---|---|---|---|---|---|
| 1 | Parser/language excellence (policy language, demos, perf, Lean-first AIR generator, build) | parser deputy + 4 sub-lanes | breadstuffs | L2-L3 | policy language elab+compile proved; two public demos; generator kills hand-written AIR; `make check-fast` < 2 min | demo (a) corpus receipt; policyc | 2026-11-06 |
| 2 | Tower256 certificate leaf prover | Tower256 gen 5 | minidregg | L2-L3 | native 9104 kernel; ContentCert gaps closed; m≥2 receipts compiled; umbrella green | 32G umbrella, merge, kernel | 2026-11-06 |
| 3 | Dark learning (MPC custody, HE helpers, collaborative ZK proof, handover) | dark-learning gen 3 (+ Astra scholar done) | zkml-research | L2 | ZK proof leaves custody; untrusted-input verifier; fork decided on a built ZKPoPK; privacy bound at 2^-40 over 10^6 steps | ZK layers 2-3; verifier; lattice ZKPoPK | 2026-11-06 |
| 4 | Governance device + attestation (seL4 chokepoint, NVIDIA/Blackwell, Chutes) | governance successor | degg-research, breadstuffs | L3 | IRQ exposure fixed; virtio TX; runtime halt falsifier; Blackwell verified live; narrator gate on | CAKEML-ROUTE.md, Blackwell | 2026-11-06 |
| 5 | HOL4-Lean bridge (panSem export, row contracts, install) | bridge follow-on (done) | DreggNet, breadstuffs, degg-research | L3 | 64 contracts; Mac install 60 s; ladder on exported evaluate | ember: ledger policy A/B; vacuous demos | 2026-11-06 |
| 6 | Mina/Pickles emitter rescue | rescue lane | breadstuffs | L0 | every module < 4 GB / 60 s or retired with census | census + diagnosis | opened 2026-11-06 |
| 7 | Iteration speed (profiles, olean cache, Mac setup, check-fast) | iteration lane | minidregg, breadstuffs, redregg | L0 | umbrella < 10 min on bb2; no non-Mina module > 4 GB; lane loop < 2 min on Mac | ranked table | opened 2026-11-06 |
| 8 | Audit theorem over our own bit-exact recompute of gpt-oss-20b (MXFP4), cross-silicon (TPU v5e / T4 via Kaggle); FlashProve demoted to a comparison point | init-8 lane | zkml-research, breadstuffs | L1 | bit-exact recompute reproducing a pinned backend; a steered output a tolerance checker accepts and exact recompute refuses, on real weights; tuned on Mac/Kaggle before any paid H100 | first bit-exact match | 2026-11-06 repointed |
| 9 | Attested transport + receipts (MPC-TLS call-tree certificates) | NEW | breadstuffs | L2 | one real HTTPS call tree certified end to end with a verifiable receipt per hop | GROUNDING.md | opened 2026-11-06 |
| 10 | Third-party verification of a real Claude Code session (R0-R3) | NEW | breadstuffs, cv | L2 | a stranger verifies a cv-exported session through R3 with no host trust; microsite | GROUNDING.md | opened 2026-11-06 |
| 11 | Streaming certificates (prefix receipts over a live log, Büchi/ω) | NEW | breadstuffs | L0 | per-window receipts with MMR non-omission; a policy holds "so far" on a live transcript stream | GROUNDING.md | opened 2026-11-06 |
| 12 | Tree automata over JSON/CBOR transcripts | NEW | breadstuffs | L0 | structural claims over committed structured records, Lean statement, counts, demo over real transcripts | GROUNDING.md | opened 2026-11-06 |
| 13 | Eval-provenance / model-identity receipt | init-13 lane | zkml-research, dregg-microsites | L3 (strict mode waits on H100 recompute of E3) | receipt over real Llama 4 Maverick: own §11 conversion reproduces FlashProve wsums digest over 232 GB; per-expert cSHAKE roots; Lean identity_sound/hollow_refused; which-model page live | ember: who signs a real eval (H100 recompute of FlashProve dropped by ember) | 2026-11-06 `45f11ea9` |
| 14 | Hardware: tensor-core exactness model (F3) + holography accumulation (F4) | init-14 lane (done to L1) | zkml-research, minidregg lane/mma-exact, degg-research, redregg | L1 | F3 counts model + checked Lean exactness per accumulator + GPU protocol ready; F4 verdict "adapt" (no cheaper hash-based accumulation; keep commitment-free structure accumulation for later) | ember: one hour on a B300/B200 (+H100) | 2026-11-06 `b21d99d6` |
| 15 | ArkLib: Selvage keystone derived from ArkLib's merged state-restoration theorem (finite alphabets); review draft finds no adaptive-adversary test in ArkLib's SR suite | init-15 lane (done) | minidregg lane/arklib-sr-bridge, zkml-research | L1 | bridge green (4,082 jobs, no sorry); coupling lemma proved; two codex checks; retirement list (recommend keep as cross-check) | ember: infinite-alphabet closure; post review; adaptive-test PR to ArkLib; blueprint (c) | 2026-11-06 `f00e39c75` |
| 16 | Unlearning / forgetting certificates (C18-C20) | init-16 lane | zkml-research, minidregg lane/unlearning-certs | L2 | exact deletion for C18/C19 on UCI optdigits, 22/22 attacks refused, SGD as a bound, custody on Pedersen commitments, Lean statements green | umbrella + merge; ember: transcript leak, custody release, PQ commitment | 2026-11-06 `2c7013d5` |
| 17 | Accelerator readiness: dark-learning BFV kernels, Tower256 GPU prover, tensor-core probe; emulate locally, tune on Kaggle T4/TPU, one-hour runbooks for paid boxes | accel-readiness lane | zkml-research, degg-research | L0 | each workload passes a Kaggle dry run; RUNBOOK with box spec and cost; no paid hardware until ready | GROUNDING.md | opened 2026-11-06 |
| 18 | TPU first-principles performance: bound per kernel, static HLO/Pallas checks on the Mac, Kaggle profiles as %-of-bound; MXFP4 recompute, BFV NTT, sumcheck-as-matmul at ≥95% | tpu-perf lane | zkml-research | L0 | rerunnable bound + static check + measured %-of-bound per kernel; ≥95% or named gap; project TPU style guide | bound calculator + HLO inspector on Mac | opened 2026-11-06 |

Decisions waiting on ember (also tracked here so they are not lost): transcript.json on public GitHub (initiative 1);
ledger policy A/B and the three vacuous ProofProducing demos (5); 3 vs 5 custodians (3); chokepoint home in minidregg
(4); keep/move/delete the Mac shared mathlib cache (7); whether to apply for an H100 on the VCF cluster (8); whether a GPU may be used for 14 (vast is not ours to use
without ember's word); whether we contribute the Merkle-adapter/BCS blueprint upstream (15c).
