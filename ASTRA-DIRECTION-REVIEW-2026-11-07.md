| Question | Judgment | Direction I would defend |
|---|---|---|
| Validation-seeking myopia | [INFERRED] Yes. The recurring failure is substituting an easier object for the intended one, then validating that substitute. | Make existing execution and receiving paths determine the theorem and the gate. Rows 5 and 10 give concrete examples. |
| Five analytic lanes | [INFERRED] Right capabilities, but several gates still prescribe their answers or permit disconnected consumers. | Keep all five; change their completion criteria and share their interfaces. Generator and transport have the greatest immediate compounding value. |
| Dark learning | [INFERRED] One bounded custody/handover/release run is justified. A 2,000-step replay is not the next investment. | Finish the integration evidence already being assembled; redirect expansion to composed security and preprocessing accounting. |
| What stops | [INFERRED] Stop reconstructed-session milestones, vacuous demo claims, repeated corpus/line-count victories, and independent emitter proliferation. | Retain useful regression artifacts; retire their inflated claims and standing lane allocations. |
| Next six hours | [INFERRED] Spend the window connecting and simplifying existing work. | Prioritize actual-ledger R3, the shared generator, precondition repair, one consumed certificate calculus, and one executable security/resource ledger. |

# Astra direction review — 2026-11-07

This is a direction review, not a certification of the code. **[READ]** means I or a read-only review subagent inspected the cited text or source; reported tests remain reported tests. **[RAN]** means a command executed during this review, with its limited result stated. **[INFERRED]** marks my conclusions and recommendations. No prover, build, benchmark, cloud operation or process-control action was run. Only this review is being changed and committed.

[READ] Sources include `DIRECTIVES-DIG-2026-11-07.md`, all 19 rows and the decision tail of `INITIATIVES.md`, `zkml-research/notes/analytic/COMMON.md`, all five roster briefs through `cv show <id> | head -150`, and the requested parser, dark-learning and initiative-10 transcript tails. Source paths below are relative to their named repository; working-lane paths are identified explicitly. The register inspected at whatember `51f12a6` had no rows after 19. These are active lanes, so unmerged working files are observations of work in progress, not final lane claims.

Terminology: an **AIR** is the algebraic constraint system a proof checks over an execution trace. **R3** is this program's strongest session-verification rung. **PCD**, proof-carrying data, attaches composable proofs to a graph of computations. A **refinement** connects an implementation's behavior to its specification. **Binding** prevents one commitment from being used for incompatible contents. **Fiat–Shamir** replaces interactive verifier challenges with hashes; its security accounting must include an adversary's hash queries. A **Pareto frontier** contains choices that cannot improve one objective without worsening another, within the stated search space. **L3** here means the register's real-artifact, stranger-rerunnable milestone, not a universal assurance level.

## 1. Where the program seeks validation instead of new capability

[INFERRED] The program's problem is not that it measures things. It repeatedly closes a locally convenient proposition while leaving the user's proposition at a seam between components. “The model we reconstructed verifies,” “the receipt faithfully records our checker,” and “the example inhabits our abstraction” can all be true while the intended system remains unavailable. The detailed notes often admit this. The register then compresses the qualification away, and the next assignment optimizes the compressed claim.

### Row 10: a gate that verifies its own reconstruction

[READ] In `breadstuffs/grain-turn/src/finalize.rs:89–101`, a continued session replaces the real pre-cell's nonce and balance with carried model values. The explanation at `:328–355` is unusually clear: this chain attests an EffectVM model head, not the ledger head; executor fee debits and the per-turn nonce tick are absent; record adjacency is not checked there. `grain-turn/tests/r3_threaded_session.rs:62–85` explicitly asserts that the model equals the proved head **and the real head does not**. Later the test verifies R3 against that model.

[INFERRED] This is an excellent diagnostic regression and a terrible completion gate for third-party verification of an actual session. A larger replay cannot repair this discrepancy. Stop giving the reconstructed path progress credit toward executor-faithful R3.

[READ] The replacement is already correctly directed. The `i10-single-tick-grain-descriptor` branch, inspected at `fb28753c6`, ties `grainTurn_row_agrees_executor` to actual executor definitions: multiple field writes, one nonce tick and one fee debit per turn. Its `grain-session/SINGLE-TICK-DESCRIPTOR.md` still names three obligations: O1 obtains row hypotheses from deployed rotated `Satisfied2`; O2 connects the final row to the published after-state; O3 binds all eight limbs of the 32-byte values. `Dregg2/Grain/R3Verify.lean:268–285`, `r3_unfoolable`, assumes `EngineSound` and head-denotation coherence. It does not discharge those obligations.

[INFERRED] Protect the replacement work. Do not promote its row theorem to a completed session theorem before those connections exist. Likewise, eight-limb iroot widening fixes receipt-root truncation; it does not independently fix fees, nonce semantics or full-width field-value provenance.

### Row 5: known vacuity treated as a preference question

[READ] `breadstuffs/orb-compiler/Pancake/ProofProducing.lean:286–303` gives the redirect certificates the premise `∀ s : PancakeState σ, s.locals "code" = some (codeVal s)`. The state space includes states with no such local. `httpStamp_cert` and `crlfStamp_cert` at `:562–567` and `:600–605` similarly assume a bound buffer in every state. `LadderPanSem.lean:468–474` already proves `wf_reading_local_uninhabited`. Its comment directs these clients to the precondition-bearing `RefinesClk` / `RefinesClkPan` interface. The closed-leaf `closedDemo` is unaffected.

[READ] Nevertheless, `degg-research/research/BRIDGE-KNOT.md:518–522` puts whether to move the three demos to precondition form under “Decisions only ember can make.” The register repeats the deferral. The finding is not new: `research/BRIDGE-CODEX.md:66` attributes it to `e5081531c`; the inspected LadderPanSem source includes it at `27ad92ee3`.

[INFERRED] This is the clearest thing to retire immediately: the three certificate claims in their current form, and the fake permission barrier around repairing them. The reusable repair is to propagate a meaningful initial-state precondition through translation and composition. Another vacuity report would add nothing.

### Rows 8 and 13: real artifacts, narrower propositions than the headline

[READ] Row 8's `zkml-research/docs/EXACT-RECOMPUTE.md` reports layer-0 integer agreement across four kinds of hardware, all-layer CPU execution, and 301/302 held-out argmax agreement with float64. It explicitly audits **gptoss-int v0**, an integer derivative, rather than the floating-point model. The same note exhibits a forged recompute report that passes offline receipt checking; rerunning the computation catches it.

[READ] In `minidregg` commit `c9717142f`, `Selvage/AuditExact.lean` defines `Transport` to require that a successful opened recompute report equal the specification's output. `no_chkBad` and `exact_bound` then eliminate the checker-error term under that premise. `lying_badAt` and `lying_not_transport` show why it matters. This is a valid conditional audit theorem. It is not a proof of the numerical implementation. The live tests are useful evidence about that implementation, with much narrower coverage than the universal premise.

[INFERRED] Keep the exact backend and audit construction. Stop treating nine receipt decisions as independent confirmation of numerical correctness, or the 302 positions as a fidelity guarantee. The tolerance demonstration also uses a logit-level abstraction, not TOPLOC or DiFR themselves; its large threshold admits the integer derivative. It cannot establish that a deployed floating-point checker is exploitable to the same degree. Further comparison work must hold the intended model and acceptance relation fixed.

[READ] Row 13's `research/model_identity_receipt_2026_11_06/GROUNDING.md`, §§6–8, records useful independent conversion over the real 232 GB checkpoint. It also says strict mode transfers trust to authenticated recomputers; the current E3 commitment edge is published rather than recomputed by this lane; the example evaluation signer is a demonstration key. `identity_sound_strict` depends on recomputer honesty, and `FpSoundUpTo` remains an unquantified external premise.

[INFERRED] That supports a useful provenance-receipt implementation. It does not supply an independent evaluation or a trust-free proof of deployed model identity. More checkpoint bytes do not remove those premises. The next leverage is connecting these typed edges to the shared certificate calculus, not another model-name demo.

### Rows 9, 11 and 12: L3 must name the relation

[READ] Row 9's `breadstuffs/metatheory/Dregg2/Lightclient/CallTreeDeploy.lean:173–208` connects authenticated body substrings across hops. `calltree/GROUNDING.md:114–121` records the demoted host-asserted grain anchor, missing typed call-ID edges, recorder assignment trust, and missing freshness challenge. The real four-hop recording and stranger replay support that narrower relation.

[INFERRED] They do not yet certify the causal tool execution of an agent. More hops or another recording would mostly reconfirm the existing relation. The useful next edge is authenticated call identity tied to the renter's session and source.

[READ] Row 11's `demo/stream-receipts/README.md` includes a good control: removing a line before regenerating every receipt passes chain validation but fails against an external source anchor. It also correctly refuses to certify infinite-run liveness from a finite prefix. Row 12's `demo/tree-absence/README.md:32–48` documents patterns with 13, seven and zero matches; the zero-match pattern deliberately misses backtick substitution and other shell forms. At `:112–115`, the publicly recheckable artifact is one record, while the corpus counts are local measurements. B/C pattern-to-policy correspondence is tested, not generally proved (`:56–61`).

[INFERRED] Keep both components. Stop growing line counts, and retire any interpretation of the zero-match result as “no dangerous process command occurred.” The source documentation is more careful than the register. A global L3 label should never make a local fixture or a producer-selected projection look like complete execution evidence.

### The analytic pivot can reproduce the same problem

[READ] The transport brief's gate is the before/after count of broken declarations. In the new `/Users/ember/dev/lean-transport/Transport/Worker.lean:116–149`, repair candidates include replacing a failed literal expectation, a `#guard_msgs` expected message, or a closed theorem's literal right-hand side with what the changed program now computes. `Transport/Census.lean:15–23` correctly distinguishes these `retyped` statements from `repaired` proofs whose statements did not change.

[INFERRED] Preserve that distinction in the success gate. A lower broken count is not proof repair if the propositions changed. Layout pins can legitimately regenerate; semantic invariants and axiom-footprint expectations need a separately justified change. Otherwise the program has automated changing the answer key. I did not observe a particular iroot security theorem being weakened by this tool; this is a concrete risk in its mechanism and metric.

[READ] The costmodel brief asks to prove the chosen deployed parameters Pareto-minimal. The directives dig §2.4 asks to derive a lower bound and “Then show” a rival's speedup lies below it. Its roofline proposal asks compiler output to certify achieved throughput of at least 95% of an ideal limit.

[INFERRED] These are analytic versions of validation-seeking. A frontier search must be allowed to reject the deployed point. A lower bound must be allowed not to refute a competitor, especially one using a different proof class or baseline. Operation and compulsory-byte counts establish resource lower bounds; they cannot alone establish achieved speed. A static guarantee needs a schedule, latency and overlap assumptions, actual traffic, and a hardware model. Calling a prediction a certificate does not close that gap.

### Evidence against a blanket indictment

[READ] Row 1's proved-equal compiler speedup (`f45ef0ba5`) and direct-logic cutover (`520727fb2`, `3501b00f9`) improve a reusable, consumed path. Row 19's `degg-research` commits `248f1cf` and `ed3ee50` connect an adversarial crash/recovery model to a byte implementation: `AriadneStep.non_omission` quantifies over reachable adversarial runs, and `CommitBytes.stepBytes_sound` identifies accepted bytes with the modeled transition. The host still must perform persistence and forwarding in order, as its README says. These are meaningful constructions with a remaining deployment seam, not vacuous proofs.

[READ] The dig is stale about part of the commitment repair. Current `minidregg/Selvage/Commitment.lean` proves `BindingCommitment.isEmpty_of_card_lt`: perfect binding cannot describe a compressing root over a larger message space. Commit `7b3468acf` adds `AuthMapCommitment.lean`, including `opened_word_or_collision` and `lightClientKnowledgeSound_authMap`. Its collision is exhibited by the actual opening transcript, not the automatically true statement that some collision exists somewhere. Current main `c4ecabe0f` also implements retained served state and suffix binding in `Compiler/DurableServed.lean`; “nothing incremental exists” would be false. Incremental proof production is a further question.

[RAN] `git merge-base --is-ancestor c9717142f HEAD` in the inspected minidregg checkout returned 1, and `git show` identifies that SHA as a merge **into the lane branch**. The local main lacked `Selvage/AuditExact.lean`, although the commit object contained it. This does not establish current remote state; no fetch was performed. It does mean the register's “merged to main c9717142f” was not verified by its cited SHA and this checkout. Integration claims need the receiving-main commit, not another successful lane build.

[INFERRED] These corrections matter. An audit that repeats old holes after their repairs is itself a validation exercise. The useful program-wide question is now: which production consumers use the repaired abstraction?

## 2. Are the five analytic lanes aimed right?

[INFERRED] Keep all five. They cover the most repeatedly neglected capabilities. But their completion target must be the elimination of a recurring class of work, not five new islands of Lean. A milestone can be small; the assignment and consumer must remain ambitious.

| Lane | Evidence from current work | Ambitious target and needed correction |
|---|---|---|
| Transport | [READ] A general elaboration worker exists, and the actual iroot migration was handed over at `02cc02301`, with Lean work `5734d3aac`. Its transcript explicitly left Rust checks, collision control, schema/VK changes and umbrella integration outstanding. | [INFERRED] Make a declared representation change propagate through definitions, proofs, emitted layouts and receiving code. Separate preserved statements from changed statements. For iroot, bind the existing full digest: an embedding of the old single felt into eight felts preserves its collisions. Finish this migration and demonstrate reuse on the next real change. |
| Generator | [READ] `breadstuffs-lanes/generator/.../Derive/WpGenerator.lean:588–595` proves `derive_sat_iff_exec` with existential witnesses and public projections. `WpDescriptor.lean:293–297` connects it to real `Satisfied2`, explicitly with empty memory/map operations. | [INFERRED] This is substantive. But the lane introduced a fresh `Prog` executor. Connect the existing application semantics to it, emit a descriptor actually used by the prover, and retire the equivalent authored constraints. The general translator should produce unresolved obligations where necessary; it need not solve arbitrary Lean predicates. |
| Costmodel | [READ] `notes/analytic/costmodel.md` publishes counts, recursion costs and separate calibration constants. It retains `[BUDGET-compose]` as an assumption. | [INFERRED] Search a declared feasible design space, including field/extension validity, implementation support and full-run error. Return a frontier or infeasibility, not proof that today's choice wins. Connect the chosen configuration to `num_queries` admission and actual emitted objects. Distinguish ideal lower bound, calibrated prediction and proved schedule bound. |
| Calculus | [READ] `breadstuffs-lanes/calculus/.../CertCalculus/Core.lean` defines a probabilistic `Valid`, explicit binding obligations and named assumptions. Its header calls `Deriv.census`, which prints the derivation tree, its executable consumer. | [INFERRED] Printing a derivation is insufficient. A real verifier must accept composed certificates through this interface. Connect shared content, positions, windows and source identity; make mismatched subjects fail. Keep Datalog and rewriting on the same interfaces rather than producing independent AIRs. |
| PCD/system | [READ] `minidregg-lanes/pcdsystem/Selvage/DagPcd.lean:45–54` explicitly leaves recursive-verifier flattening unproved. Its `linScheme` at `:511–527` publishes the full word, uses `Unit` as accumulator witness, and extracts local witnesses from the round message. | [INFERRED] The generic graph theorem is useful; the concrete example is not a succinct private graph proof system. Connect generated recursive-verifier circuits to the shared-oracle protocol, instantiate computational commitments, and consume the cost/error interfaces. More tiny DAG examples do not close that seam. |

[READ] The generator and parser have already negotiated a boundary, but it is the wrong long-term one. The parser transcript records the generator declining zkOracle and custom-leaf lowering because its first milestone has no hash-site semantics. The parser consequently started another zkOracle generator lane.

[INFERRED] Do not halt these useful cutovers. Make them extensions and clients of one semantic IR. The generator owns arithmetic, public projections, carries, hash-site obligations and emitted constraints. Parser owns source-language lowering into that interface. A hash primitive may carry an explicit collision reduction; it must not become a silent “trusted leaf.” Byte identity is a good transition check for unchanged layouts, not the permanent correctness definition: two equivalent optimized encodings may differ in bytes.

[INFERRED] Calculus owns the meaning of composed claims, their subjects, assumptions and error events. PCD owns extraction and recursive aggregation against that contract. Costmodel prices their actual structures. Transport migrates them without quietly changing the intended property. This is the overlap to exploit. Building a separate epsilon language, cost representation or constraint language in every lane would defeat the simplification objective.

[INFERRED] The calculus brief also needs two semantic corrections. Completeness for a query should say that a suitable certificate exists when the query holds; an arbitrary malformed certificate need not be accepted. A gap opening establishes absence from a committed base-fact table. Absence from recursively derived Datalog facts requires closure/fixpoint evidence. The brief names existing `FixpointCert` and `StratifiedCert`; reuse their semantics. Similarly, multiset balance alone is not all the conditions of graph rewriting: preserve incidence and the conditions governing legal deletion and identification of nodes. An algebraic encoding of a weaker rewrite relation would be another substitute success.

[INFERRED] The single-provider impossibility belongs beside the dark-learning capability model, with PCD helping formalize it, rather than as a distracting third completion criterion for graph aggregation. Distinguish computing another ciphertext, learning an unauthorized output, advancing accepted state and cloning a usable model. Public homomorphic evaluation permits the first; it does not by itself give the others. A theorem whose premise grants exactly the forbidden capability cannot justify the entire MPC architecture.

[READ/INFERRED] The five briefs still leave these directives without a concrete owned deliverable: categorical kernel/SetField redesign (22); operational deferred and retroactive proving (23); incremental proving/checking over retained computation (24); both STARK-in-FHE and FHE-in-STARK (20); the semantic reinterpretation side of foreign verification, including Solana (13); and the unanswered research/consensus questions in 26. EVM decompilation (14) is only adjacent to a generic generator, not assigned as an actual frontend. A logical `defer` rule does not implement a retained witness store or discharge scheduler. Record these as backlog with dependencies and owners; do not claim broad lane names cover them. The current retained-state commit is a foundation to reuse, not a reason to restart that work.

## 3. Dark learning: keep one integration run, redirect expansion

[INFERRED] I would defend finishing the bounded eight-step custody, handover and release exercise. I would not defend starting a 2,000-step encrypted replay now. The rented third machine is an integration instrument, not the research thesis. Its value is whether it tests a distinct operational boundary; geographical separation and another machine do not establish independent administrative custody.

[READ] Deployment already found serious defects: `zkml-research/docs/DARK-LEARNING-SCHEME-DECISION.md:1897–1904` records public HE mask seeds that let a custodian recover the model, and accepted out-of-range truncations before range checks were added. Those are good reasons to exercise the composed implementation. The latest lead transcript also reports exact truncation and its integration in `2c11f069`, `bd1ebdfb`, `1b3d9178`, `b1a485f8` and `991b29fd`. The construction changes accepted truncations from an approximation to the intended integer result, with a retry on the wrap zone. That is precisely the analytic progress the program needs.

[READ] The statistical and cryptographic claims must remain separate. `notes/dark-learning-gen6/proof.md:788–807` gives approximately 2^-101.3 per step and 2^-90.3 over 2,000 steps plus release for the listed algebraic tests. It explicitly excludes Merkle binding and Fiat–Shamir grinding; hash-query count multiplies the round terms. `xtrunc.md:144–155` separately estimates whole-run privacy distance: approximately 2^-30.3 for the small LowGear record and 2^-23.8 for 2,000 steps. That table admits it has not rescaled drowning for the extra preprocessing batches.

[INFERRED] The privacy figures are upper bounds, not demonstrated probabilities of revealing the model. But they cannot support an unqualified cryptographic-strength whole-run privacy claim. Nor can the algebraic 101-bit figure be promoted to the complete noninteractive guarantee. Better composition and accounting are more valuable now than accumulating more training steps under those unresolved bounds.

[READ] The accounting already demonstrates why. `research/dark_learning_2026_11_06/privacy_budget.py:94–134` hardcodes pre-exact-truncation object counts and gives `gen6()` no XT parameter. Updated arithmetic lives in a scratch `budget_xt.py`, referenced by the note. `xtrunc.md:168–172` prices LowGear extras at 37.8 kbit per triple-equivalent; `prep.md:593–597` explicitly corrects the generated-triple price to 82.9 kbit at N=16,384, explaining that 37.8k used nominal triples. The old estimate still appears in the lead's report.

[INFERRED] Do not replace that with another hand-calculated authoritative number. Batch rounding, randoms and openings have different prices. Generate the actual preprocessing plan and its security terms from the pinned program, then price that plan once. This removes a recurring error source.

[READ] `train.md:53–104` already reports roughly 330 plaintext runs and learning curves over five orders; `:136–153` describes a release over the first 52 test images, chosen to fit memory. `prep.md:673–682` prices the record at about 573 GB per party, including 225 GB setup and 219 GB release, versus eight steps at 15.5 GB each.

[INFERRED] Much of the record is therefore custody setup and release engineering. Name it that way. A long MPC replay primarily adds endurance evidence if semantic equivalence holds. State the reliability question requiring that duration before paying for it with more lane attention. It does not discover a new learning method.

[READ] `handover.md:83–145` checks cooperative memory, files and restart behavior. [INFERRED] A successful guest-memory scan or keyring invalidation cannot prove that a malicious cloud host kept no snapshot. Treat erasure and non-collusion as explicit deployment assumptions. Do not let a green keyring smoke test stand in for the custody threat model.

[INFERRED] Cut further MNIST sweeps, hbox-specific throughput tuning for the superseded placement, and expansion of the record's duration. Keep one owner for the bounded run and its real failures. Redirect the remaining work to the shared budget, generated verifier linkage, and the exact meaning of unauthorized execution. These are recommendations only; this audit has not stopped or changed any running work.

## 4. What should stop or be retired

[INFERRED] Retire claims and redundant work paths; preserve useful artifacts and regression tests. Nothing here calls for deleting another lane's files or killing its processes.

| Stop or retire | Preserve or replace it with |
|---|---|
| Row 10 model-head R3 as a session-verification milestone. | Keep the diagnostic that exposes the mismatch. Replace the served path with actual-ledger single-tick composition and full-width binding. |
| Row 5's three local-reading certificates under impossible universal premises, and the “Ember decision” to repair them. | One precondition-bearing translator and inhabited clients. Keep the valid closed-leaf example as a regression. |
| Row 3's planned long replay and more plaintext tuning as the default next research step. | One bounded integration record; a generated privacy, soundness and preprocessing ledger. |
| Row 1's law-1 census as evidence that a generator exists; independent one-off emitters as the terminal design. | Keep the cheap regression ratchet. Make actual emitters clients of one verified generation interface. |
| More row-9 recordings, row-11 line-count milestones and row-12 zero-match safety stories. | Typed causal edges, authenticated source binding, and composed acceptance of existing tree/stream certificates. |
| Row 6's “every module under 4 GB / 60 s or retired with census” as the research objective. | Optimize shared elaboration problems that unblock the foreign-verifier consumer. Retire redundant wrappers, not the requested Pickles capability because it is expensive to compile. This judgment concerns the register's gate, not an audited rescue implementation. |
| Rows 14/17/18 hardware tours without a decision tied to a count model. | Use existing measurements for calibration. Schedule another device run only to distinguish competing designs or resolve a named schedule/precision uncertainty. |
| Repeated “done-lane” ceremonies and microsites for rows 2, 9, 11–15. | Keep their components; give remaining integrations to the receiving owner. A finished local construction need not retain a permanent lane to rediscover its residuals. |
| Aspirational status promotion based on green build totals. | Name the relation, assumptions, real consumer and receiving commit. Building 10,428 jobs is integration evidence, not a stronger theorem. |

[INFERRED] Do not stop the analytic lanes, exact truncation, the consumed policy compiler improvements, AuthMap repair, retained-state work, or Ariadne continuity. They are examples of the program becoming more capable. The distinction is whether the work removes a recurring limitation for other work.

## 5. The top five moves for the next approximately six hours

[INFERRED] Concentrate the existing owners on these five moves. They are ordered by leverage; the completion conditions are real acceptance conditions, not a promise that every unfinished theorem fits six hours. Finish and integrate the closest useful construction before opening replacement lanes. If a condition remains unproved, report that exact unfinished connection; do not substitute a green miniature. Each move includes cleanup of the old path or backlog claim.

### 1. Complete the actual-ledger R3 connection and iroot migration

[INFERRED] **Repo and files:** breadstuffs, using the existing single-tick and transport worktrees. Work in `metatheory/Dregg2/Circuit/Emit/EffectVmEmitGrainTurn*.lean`, the rotated layout/emitter modules, `grain-turn/src/finalize.rs`, `turn/src/rotation_witness.rs`, `cell/src/commitment.rs`, and `grain-turn/tests/{ledger_head_delta,r3_threaded_session}.rs`. Transport's `Worker.lean` / `Census.lean` should expose statement changes separately from preserved-statement repairs.

[INFERRED] **Done means:** the admitted descriptor entails the actual multi-turn ledger head, including fee debits, nonce ticks and full values; the path no longer substitutes model nonce/balance; the original receipt-root collision separates at the anchor while its deliberately truncated control still collides. O1/O2/O3, schema/VK changes and receiving integration are accounted for. A preserved semantic target, not updated expected output, determines success. This closes several old gaps together and gives the transport tool a real customer.

### 2. Make the generator replace an existing emitter

[INFERRED] **Repo and files:** breadstuffs, `metatheory/Dregg2/Circuit/Derive/{WpGenerator,WpDescriptor}.lean`, `metatheory/Dregg2/Circuit/Emit/AccumulatorNonRevocation{Emit,Refine,Complete}.lean`, and `circuit-prove/src/{zkoracle_leaf_adapter,custom_leaf_adapter}.rs`. Publish the shared primitive interface in `zkml-research/notes/analytic/generator.md` rather than letting separate emitters define incompatible ones.

[INFERRED] **Done means:** one real existing transition refines `Prog`; its descriptor passes through the normal emitted/proving consumer; the old equivalent authored constraint construction is removed from that path. Hash, carry and public-input primitives have one owner, with explicit obligations for unsupported operations. A second distinct client exercises that same interface as it becomes available. Do not spend this window proving more properties of a fresh executor while the first production client remains disconnected.

### 3. Repair the bridge precondition abstraction and close its false backlog barrier

[INFERRED] **Repos and files:** breadstuffs `orb-compiler/Pancake/{EmitCorrectCompose,EmitCorrectClock,ProofProducing,LadderPanSem}.lean`; degg-research `research/{BRIDGE-KNOT,BRIDGE-CODEX}.md`. Use the existing precondition-bearing refinement machinery.

[INFERRED] **Done means:** all three local-reading clients have satisfiable initial-state conditions carried through translation and composition; each has a nontrivial initialized execution; no all-states-bound-local premise remains in those certificate claims. Retire the old wrappers and remove the repair from “only Ember can decide.” Keep any genuinely different ledger-policy choice separate. This is a finite, known cleanup with a reusable result, not another audit campaign.

### 4. Give the calculus a receiving verifier, and give PCD that same contract

[INFERRED] **Repos and files:** breadstuffs `metatheory/Dregg2/CertCalculus/Core.lean`, `Dregg2/Lightclient/CallTreeDeploy.lean`, and the existing tree/stream certificate modules; minidregg `Selvage/{AuthMapCommitment,DagPcd}.lean` on their appropriate branches; degg-research `research/GOVERNANCE-CLAIM-LATTICE.md` and `experiments/chokepoint-step/{AriadneStep,CommitBytes}.lean` as the already-built continuity source.

[INFERRED] **Done means:** a real composed acceptance path consumes the calculus judgment, with one named subject, source commitment, window and binding event; two individually valid certificates about different subjects fail composition. Instantiate an existing tree/window claim, not a new toy leaf. The continuity adapter must expose the host persist-before-forward obligation. PCD consumes the same claim/error contract and explicitly tracks its remaining recursive-verifier flattening connection. `Deriv.census` may explain the result; it is not the receiving verifier. This gives rows 4/9/11/12/19 a shared way to become a system.

### 5. Unify security and resource accounting; reconcile the register from its outputs

[INFERRED] **Repos and files:** zkml-research `research/dark_learning_2026_11_06/{privacy_budget,cosnark_soundness}.py`, its pinned genesis and native darkprep planning interface, `notes/dark-learning-gen6/{xtrunc,prep,proof,cloud}.md`, and `notes/analytic/costmodel.md`; minidregg `Assurance/{CostModel,TwoRegimeQueryBudget}.lean`. Follow through into whatember `INITIATIVES.md` after the work, not during this read-only audit.

[INFERRED] **Done means:** one read-only command derives preprocessing counts and lifetime budgets from the actual pinned configuration, including XT retries/batches, backend, release size, field and query settings. It reports algebraic soundness, binding/Fiat–Shamir assumptions and privacy distance separately. It uses generated rather than nominal triple counts. The cost search can report that no supported point reaches the requested composed security target; if it finds one, its concrete `num_queries` pin is handed to or landed by the receiving owner. This is not a claim that a FRI cost function directly prices the distinct dark-learning proof system: share the accounting schema and configuration provenance, with backend-specific derivations.

[INFERRED] Update the existing register once from these integrated results: add the five analytic owners, mark the long dark run deferred, remove resolved or false permission barriers, qualify the narrow L3 relations, cite receiving commits, and assign the uncovered directives listed in §2. Do not create another permanent status ledger. The purpose of the six-hour window is to reduce the number of independently maintained stories the program must keep consistent.
