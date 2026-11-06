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
| 8 | Audit theorem instantiated over FlashProve proofs | NEW | zkml-research, minidregg | L1 | Rust auditor whose alarm routes through AuditSampling; ε_chk from their theorem; beacon leg; injected corruptions measured vs 1/q on real proofs | GROUNDING.md | opened 2026-11-06 |
| 9 | Attested transport + receipts (MPC-TLS call-tree certificates) | NEW | breadstuffs | L2 | one real HTTPS call tree certified end to end with a verifiable receipt per hop | GROUNDING.md | opened 2026-11-06 |
| 10 | Third-party verification of a real Claude Code session (R0-R3) | NEW | breadstuffs, cv | L2 | a stranger verifies a cv-exported session through R3 with no host trust; microsite | GROUNDING.md | opened 2026-11-06 |
| 11 | Streaming certificates (prefix receipts over a live log, Büchi/ω) | NEW | breadstuffs | L0 | per-window receipts with MMR non-omission; a policy holds "so far" on a live transcript stream | GROUNDING.md | opened 2026-11-06 |
| 12 | Tree automata over JSON/CBOR transcripts | NEW | breadstuffs | L0 | structural claims over committed structured records, Lean statement, counts, demo over real transcripts | GROUNDING.md | opened 2026-11-06 |
| 13 | Eval-provenance / model-identity receipt (FlashProve commitment + registry v2 + signed eval) | NEW | zkml-research | L1 | one receipt binding commitment ID, per-expert roots, eval record; verifier CLI; which-model microsite updated | GROUNDING.md | opened 2026-11-06 |
| 14 | Hardware: tensor-core field experiment + holography accumulation read (F3, F4) | NEW | zkml-research, obend notes | L0 | counts-exact MMA model validated on a GPU if one is granted; accumulation verdict with recursion-verifier sizes | GROUNDING.md | opened 2026-11-06 |
| 15 | ArkLib upstream: RBR-to-Fiat-Shamir/BCS compiler contribution | NEW | minidregg, fork of ArkLib | L1 | PR-ready branch on a fork, their conventions, their CI green; ember opens the PR | GROUNDING.md | opened 2026-11-06 |
| 16 | Unlearning / forgetting certificates (C18-C20) | NEW | zkml-research | L0 | exact-deletion certificate in the harness with attacks refused and counts; Lean statement | GROUNDING.md | opened 2026-11-06 |

Decisions waiting on ember (also tracked here so they are not lost): transcript.json on public GitHub (initiative 1);
ledger policy A/B and the three vacuous ProofProducing demos (5); 3 vs 5 custodians (3); chokepoint home in minidregg
(4); keep/move/delete the Mac shared mathlib cache (7); whether a GPU may be used for 14 (vast is not ours to use
without ember's word); whether to open the ArkLib PR (15).
