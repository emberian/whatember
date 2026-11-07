# Directives dig, 2026-11-07: what ember asked for, and what became of it

Trigger (ember, 2026-11-07, `cc:78fef112-a52f-425f-8503-f3fa24ff087c`):

> "it seems you're hooked on empirical GPU runs, which i do respect and understand, but i just suspect that maybe our
> system could be improved so much more from the synthetic/analytic perspective ;) and maybe exploring higher
> algorithms and compositions ... maybe you should use `cv` or dig around one of our history directories to find
> other directives from me.."

**Method.** I took ember's typed prompts from every Claude Code `history.jsonl` root (`~/claude`, `~/medium-old-claude`,
`~/claude-bup-2-16`, `~/.claude-elide`, `~/claude-mid-pyana`, `~/.claude-2026-06-26`, `~/.claude-2026-08-04`,
`~/.claude-10-03`, live `~/.claude`, and the persvati mirror in `aidev/raw/persvati`) plus `~/.codex/history.jsonl`.
I kept the dregg-family project directories (breadstuffs, minidregg, DreggNet, zkml-research, degg-research,
redregg, whatember, drorb, dregg-microsites), and also prompts from `~`, aidev, obend and dragons-clutch that hit
proof-system or governance keywords. Then I deduplicated the set and filtered it to substantive prompts. That left
716 prompts from 2026-05-19 to 2026-11-07: I read 391 from July to November in full, and a sub-agent read the 325
from May and June. Only ember's own words are quoted; pasted agent text is excluded. Status was judged by grepping
the seven repos, `INITIATIVES.md`, `SWARM-2026-11-05-SYNTHESIS.md` and the zkml-research docs. Every status claim
names its evidence.

This dig builds on three earlier recoveries and does not replace them:
- `zkml-research/forcodex/01-STEERS.md` and `01b-STEERS-RECOVERED.md` (August, about 40 steers from the zkML campaign);
- `redregg/archive/2026-10-03/INTENT-{MAY-JUNE,JULY-AUGUST,SEPTEMBER-OCTOBER}-20261003.txt` (intent models);
- `whatember/sources/strands/15-metamanagement-open-cycles-revival-triage.md` (cycles C1-C15 and the revival list).

Session ids are `cc:` for Claude Code and `codex:` for Codex. Dates are local.

---

## 1. The ranked directives

Rank reflects how often ember came back to a directive, how much of the program depends on it, and how far it
has drifted from view.

### 1. Analytic and synthetic work over empirical runs
- **Quotes.** "We've also become WAY too empirical/measurement-driven, over measurements that don't actually make much
  sense with regards to the ultimate composed system overhead&performance" (2026-10-27, minidregg,
  `cc:d0d33f7b-1304-4ad3-96f2-1735fa3775b2`). "I'm not sure I want to *measure* the way you suggest because naive
  measurements often become folly ... you'd set up some kinda empirical harness and you'd draw wild inferences from it"
  (2026-10-29, obend, `cc:33ee7e81-25a8-4000-aaf3-942ad7ef028b`). "the one-day refutable experiment, i am not a fan of.
  i would prefer we be more ambitious ... you propose an experiment and then the rest of the system never gets built"
  (2026-10-31, obend, `cc:01a18fe9-771b-71b2-b01f-da7ed6517d48`). Today's trigger, quoted above.
- **What it asks for.** Derive designs from cost models, theorems and first principles. Measure only to calibrate.
  An experiment is not a foundation to build on.
- **Status: partly done, and slipping.** The rule exists on paper: "Counts over clocks" in `PROGRAM-2026-11-05` §1, and
  the 08-14 retraction in `zkml-research/docs/COST-MODEL.md`, prompted by ember: "THE CLOCK DATA IS NOT SOUND". But
  the next gates in `INITIATIVES.md` are mostly runs: row 14 wants "one hour on a B300/B200", row 17 wants a Kaggle
  dry run for each workload, and row 3 is waiting on a run of record. The three experiments that
  `SWARM-2026-11-05-SYNTHESIS.md` asks for first are all hbox runs. No row in the register is an analytic
  construction. §2 below lists the ones ember asked for.

### 2. Exactly one circuit, derived from Lean, and never a hand-written AIR
- **Quotes.** "the only AIR circuits ever should be the ones derived from lean ... it really does need to only have one
  circuit/algebraic statement that they all share" (2026-06-08, breadstuffs/metatheory,
  `cc:3b829648-9d41-4dad-bd2e-1a3eb7f618ab`). "(we already have a Lean->AIR compiler setup don't we...??? ... there
  was no need to handwrite anything in rust..?)" (2026-07-14, `cc:1d7ab035-f693-4560-9781-3d5a570220fe`). The /goal
  "Retire every first-party Rust-authored circuit by emitting it from Lean ... Never hand-author a constraint to close
  a gap; if an emitter is missing, name it" (2026-07-15, DreggNet, `cc:8f4c1176-9612-4902-98b4-84f9e1467f21`). "we
  need to be writing a *compiler/translator tool that helps us do this completely automatically, we use Lean so that
  we can metaprogram systems exactly like that*" (2026-07-28, `cc:ffb42026-536a-43c0-a17e-d232b6a299c7`). "IN the new
  system we will never ever be handwriting any AIR ... at most 10% of the total lines of code" (2026-08-06, minidregg,
  `cc:b54b6026-1b53-47dc-9148-5d041555810c`).
- **What it asks for.** A Lean metaprogram that emits the AIR and the Rust call surface together, so the law holds by
  construction and does not depend on lanes remembering it.
- **Status: partly done.** minidregg tracks no `air.rs` or `builder.rs`. The breadstuffs v1 effect-VM hand AIR is
  retired (`circuit/src/effect_vm/air.rs` header), and a law-1 enforcement test exists
  (`circuit-prove/tests/law1_enforcement_gate.rs`, `7b1f3657c`, today). Still open: `breadstuffs/fhegg-solver/src/air.rs`
  is a Rust-authored constraint system; strand 15 revival #7, the "Lean AIR generator", is at L0 ("the law's
  most-repeated violation"); and the next gate of register row 1 is still the cutover of the direct-logic compiler to
  the Lean IR2 compiler. The generator itself does not exist. A test that catches violations is not one.

### 3. A proof-producing translator: verify the generator, not each output
- **Quotes.** "GENERATING CODE FROM MODELS ~ if we also verify the generator. and the generator can be a PROOF PRODUCING
  TRANSLATOR and it does **not** have to fully automatically discharge all of its obligations" (2026-06-30, DreggNet,
  `cc:e6761437-a2c9-4cae-868d-85e8d4f589da`). "proof-producing translations of Lean and other dependently typed
  constructs to algebraic and other proof systems" (2026-07-24, `cc:ccb26860-7dc6-47d3-96fb-62df550eb2e1`). "maybe
  even designing a (proven sound in lean) sorta "compilation to zkcircuit" type pipeline...? ... imagining also/separately
  a sorta proof-producing templater" (2026-07-16, `cc:3e00cf4f-418c-4725-861d-79a681805f78`). "a lot of circuits are
  like weakest preconditiony shaped things over the executor semantics, right?" (2026-06-08, `cc:3b829648-…`).
- **What it asks for.** A translator from Lean semantics to constraints that emits its correctness proof, or the
  obligations it could not discharge, with each output.
- **Status: partly done.** The policy language's elaborate-and-compile path is proved, and the union compile's fast
  paths are proved equal to the slow ones (`f45ef0ba5`, register row 1). The AIR emitters are byte-pinned
  (descriptors plus goldens), not proof-producing. No wp-style derivation of circuits from executor semantics exists
  in any repo.

### 4. Proof repair and refactoring tooling
- **Quotes.** "improving our datalog and predicate and caveat languages ... (this will involve proof repair work i
  bet..)" (2026-06-07, `cc:3b829648-…`). "let's do all the work needed to refute everything, HOPEFULLY also **figure out
  how to repair the theorems etc**" (2026-07-16, `cc:b41a7fca-7bb1-485b-8918-553f4977c89b`). "what will it take to finish
  mechanizing the metatheory? and also exploring some proof repair and other techniques" (2026-10-29, obend,
  `cc:33ee7e81-…`). "we allowed simple generation mistakes early on in development to propagate and now we don't have
  good enough tools for doing a refactoring like "widen 1->8 felts" even though it's actually quite mechanical as a proof
  repair task" (2026-11-06, `cc:78fef112-…`).
- **What it asks for.** Tools that carry proofs across a change of representation or a protocol edit, so a
  refactoring costs one mechanical pass and not a swarm.
- **Status: not started.** `rg -i 'proof.repair'` finds the phrase only in redregg notes. Nothing in breadstuffs,
  minidregg or zkml-research implements it. "Refute-then-repair" is a lane rule in `PROGRAM-2026-11-05` §1, but no tool
  supports it.

### 5. A proven 100-120-bit configuration, with the decoding regime in the statement
- **Quotes.** "if our system only has 61 bits of security, how good is that, what is each "bit" measuring the grinding
  of, and what would we do to have a genuine, proven 120-bit configuration of our system..? i'm not afraid of doing
  novel formalized cryptanalytic research together with you guys" (2026-07-16, `cc:b41a7fca-…`). "unique-decoding
  regime (Johnson/list-decoding is named research); the deployed-ZK adaptive bound reduced to one RO-programming lemma;
  the additive-FRI transform for the binary-tower substrate ? i would like to keep working on the actual Loom/etc
  floor/etc ;) to completion ideally" (2026-08-08, minidregg, `cc:37e4ed4c-387f-4d95-b314-d9e2a6a5d182`).
  The other side of the same directive: "sigh. here we are again cargo-culting the FRI/STARK soundness floor. actually
  look at that fucking floor instead of talking about" (2026-08-02, `cc:e0d13eed-1b60-40b1-b2f0-36dee4ba14b1`), and
  "the "FRI floor" is never a cost, that's just literally the assumptions made for FRI STARKs, so what is the actual
  cost?" (2026-08-06, `cc:a39c8058-8569-4568-9601-f8b9f553a151`).
- **What it asks for.** Proven bits from a proven regime, landed as parameters, and no ceremony about the floor.
- **Status: partly done.** The statements exist. `minidregg/Assurance/TwoRegimeQueryBudget.lean` puts the regime in
  the type (CBR withdrawn). `Selvage/OracleLogProgram.lean` found the one-lemma RO residual refutable and repaired it.
  `zkml-research/docs/BINARY-POSITION.md` landed BaseFold on the additive tower and ring switching. The parameters
  have not landed. Deployed proofs carry 34 unique-decoding bits, and Johnson 73 rests on an unproved hypothesis
  (`SWARM-2026-11-05-SYNTHESIS.md` §5). F2, the `num_queries` pin, is "NOT landed" (`PROOF-SYSTEM-SPACE.md` §6),
  and `plonky3-recursion` is still pinned at `fc3c6df`. BinarySpartan (2026/1656) and Magnetar (2026/2423) prove
  100-120 bits in unique decoding in public.

### 6. Sound, post-quantum aggregation over graphs of interactions
- **Quotes.** "We have never once had an actually sound, correct implementation of a useful aggregation scheme that lets
  us compress graphs of interactions down to single proofs ... the STARK is important for its post-quantum nature"
  (2026-05-31, `cc:5a0f6a2e-08ba-4cfc-aab1-f894f047703a`). "graph-transition folding is a goal" (2026-05-28, same
  session). "our proof tree is too deep also;) and lacks some of the important properties of the mina setup tht i had
  designed in 2018" (2026-06-29, `cc:12518a7b-eb1f-4a97-821e-a60b7539bff3`). "doing this as a recursive fold as
  opposed to factoring deeper into a more efficient stark that gets folded/tree-agg'd up is going to be.... unwise"
  (2026-07-16, `cc:3e00cf4f-…`). The 08-07 /goal: "finish the formalization of Loom (zk and etc) with accumulation, full
  recursion" (`cc:6977f98e-e709-4fa7-82b1-101860c76372`).
- **What it asks for.** PCD over DAGs (tree and scan-state shapes) with a knowledge-soundness theorem, not a linear
  chain.
- **Status: partly done.** `RecursiveAggregation.lean` (a chain anchored at genesis) is at L2, and the shifted-BCS
  accumulation verifier was refuted and repaired in `OracleLogProgram.lean`. F4 holography accumulation got the verdict
  "adapt" (register row 14). No DAG or graph PCD statement exists anywhere.

### 7. Own the proof system: recompose the literature, and build many systems from shared primitives
- **Quotes.** "we learned that we're OK at implementing entire proof systems and that we *could* own our own proof system
  from the literature ... it does need to be capable of supporting recursion tho" and "you are superintelligent, i'm
  sure you can dig into what all the best schemes offer and figure out the mathematics behind them and recompose it into
  something novel/frontier/SOTA" (2026-08-06, minidregg, `cc:b54b6026-…`). "what's the deal with the fold etc being
  *identical to plonky3*, didn't we find research of different systems we were going to explore....????" (2026-08-08,
  `cc:37e4ed4c-…`). "we're trying to *flesh out models and implementations of many of these proof systems (by
  implementing the primitives in composable ways etc)* ... lean is a bag of formal composable ingredients that we build
  as we chart them out ... parts of the design you've ben tacitly treating as fixed, are in fact mutable" (2026-08-14,
  `cc:e68bba8f-b812-4a28-a632-f8756454a9e8`). "We CAN be implementing MULTIPLE proof systems for evaluations btw..."
  (2026-08-14, `cc:5ba0dbe2-1a24-4f66-a9e1-faf47e4b18bd`).
- **Status: partly done.** Selvage exists (152 files). `BINARY-POSITION.md` reports "13 of 18 keystones transfer with
  NO new mathematics" and Spartan as three compositions. `PROOF-SYSTEM-SPACE.md` §4 lists ten unoccupied design points
  (U1-U10), enumerated by `notes/construction-search/space.py`. None of U1-U10 has been built. The program's stance
  since 11-05, "compose with FlashProve, do not re-prove", leaves this directive in the register with no lane.

### 8. Compositions of automata and certificates: tiny automata as fast polynomial proofs, substring at position, properties on the form
- **Quotes.** The /goal "improving the performance, assurance, algorithms, capabilities ... of the proof composing
  template enginge / automata arithmetization ... please experiment with ways of composing tiny automata that are
  megafast to run as polynomial proofs" (2026-07-25, `cc:ccb26860-…`). "we do need to figure out some way to compose
  these things with the regex/dfa type stuff so that we can have a maximally flexible & also extremely efficient setup"
  (2026-07-16, `cc:3e00cf4f-…`). "ways of composing eg proof systems / certificates that a substring matches at a
  particular location, properties on the form" (2026-11-05, `cc:78fef112-…`). "I'm especially hoping we can make
  progress on verified arithmetization of various automata and compositions of automata and explore points int he
  design space of ifferent ways of composing proofs and automata" (2026-11-05, same). "tree automata and streaming
  certificates and everything else, absolutely VITAL!!!!!!!" (2026-11-06, same).
- **Status: the most-built directive, still partly done.** Tree automata (row 12) and Büchi streaming certificates
  (row 11) are at L3 locally. `AttestedAutomatonWeld8` runs 4M tokens in 40 ms. Open: the weld binds lane 0 only
  (`SWARM-2026-11-05-SYNTHESIS.md` §2). `SubstringAt`, `OccursIn` and `Absent` exist only as statement schemas, in
  `zkml-research/notes/astra/certificates/StatementSchemas.lean` and `docs/CERTIFICATES.md`, not as theorems in
  minidregg or breadstuffs. F6 (substring-at-position independent of the proof system) is unbuilt.

### 9. A deductive calculus for how certificates compose
- **Quote.** "we have NO formal model of the proof statements of all the proofs ... Ideally we would have this as a
  symbolic deductive system so we can demonstrate that chaining together all our proof system actually does result in a
  property being carried along" (2026-05-23, `cc:70642dc2-d9f1-434b-8209-c2c96787bd92`). Echoed on 07-08: "new
  compositions SHOULD come with new proofs!" (DreggNet, `cc:ca49a136-b817-4644-8a86-092e07ec5c2e`).
- **Status: partly done, in prose.** There is an algebra in `docs/CERTIFICATES.md` and a receipt judgment in
  `degg-research/research/GOVERNANCE-CLAIM-LATTICE.md`. All three 11-05 lanes found the same gap: binding is assumed
  (`Selvage/Commitment.lean:113`), and "co-location is not conjunction". No Lean calculus exists, and no ε or binding
  term is threaded through one.

### 10. Datalog and SMT-style semantic richness inside certificates
- **Quotes.** "we can't just do some quick-zip proof on the satisfiability of the datalog formula against some
  merkelized fact universe?" (2026-05-20, `cc:e75ed07b-4ce4-4f00-a0b8-3abab4a2f20f`). "getting as much semantic richness
  out of our system as we can (can we express full datalog or hellasymbolic smt style things too..?)" (2026-11-05,
  `cc:78fef112-…`).
- **Status: not started as a certificate.** Datalog appears only as authorization logic
  (`breadstuffs/metatheory/Polis/PolisAuthDatalog.lean`). No derivation or absence certificate for Datalog exists in
  zkml-research, minidregg or the register.

### 11. A verified circuit optimizer, and re-deriving the old circuits without losing performance
- **Quotes.** "i wonder if somehow we can also turn this into an optimizer/etc of the modeled circuit...? so that we can
  write nice things that are also extremely efficient (and the optimizer/etc would be verified)" (2026-07-12,
  `cc:e307afc5-…`). "what we could be doing to explore re-deriving our handmaintained circuits, automatically 👀 and
  hopefully measure along the way that we're not massively regressing performance ... and honestly i wonder if we can
  improve the arithmetiziation framework(s) themselves too...." (2026-07-23, `cc:ccb26860-…`). "a monthlong project ...
  just improving the arithmetizer/compiler/stuff so that we could rewrite/refactor all the old circuits without losing
  perf (or even gaining perf and simplicity) or assurance" (2026-07-25, `cc:aca16966-b955-46b9-a10a-d16f632bb306`).
- **Status: partly done.** The only proved rewrites are the proved-equal fast paths in the policy compiler. There is no
  rewrite set over constraint IR that preserves the satisfying set. The "monthlong" arithmetizer project never ran as
  one.

### 12. Light-client unfoolability, stated through circuit semantics
- **Quotes.** "we need to figure out how to *phrase the formal property needed* that the lightclient is *proven
  unfoolable* **thrugh the semantics of the circuits**" (2026-06-16, `cc:3b829648-…`). "the algebraic statement needs to
  be strong enough that it like refines or bisimulates or whatever the protocol" (2026-06-08, same). "We need to 1.
  implement all the checks in-circuit, 2. prove them sound, 3. prove them complete" (2026-06-16, same).
- **Status: partly done.** The R0-R3 unfoolability ladder (`grain-verify`, `turn-prover`, register row 10) is at L2.
  It is stated over receipts, not over the circuit's algebraic statement.

### 13. Foreign proof systems, both ways: witness them directly, or re-interpret the semantics
- **Quotes.** "what i had in mind was modeling solana in lean and having a verified light client circuit that we can fold
  into dregg proofs ... i do'nt just want a circuit i wanna know that the circuit is right" (2026-07-15,
  `cc:2348b20c-…`). "i'd like to explore both approaches because they do different things. One directly witnesses a
  foreign proof system ..., the other is a semantic re-interpretation across to a different proof system" (2026-07-30,
  `cc:0bea043f-…`). "that "cost wall" is fake bullshit ... our plonky3 system supports full plonky3-recursion so it is
  WELL CAAPBLE of being able to actually compute a verifier gadget for pickles/kimchi" (2026-08-07,
  `cc:95d178d1-…`). "Do we have a STARK that can verify a pickles proof?" (2026-05-22, `cc:70642dc2-…`).
- **Status: partly done.** `breadstuffs/metatheory/EmitInAirPickles.lean` exists, and `docs/MINA-PICKLES-RESCUE.md`
  sits at L0 in register row 6, because single modules need more than 12 GB to elaborate. Nothing models Solana in
  Lean.

### 14. Decompilation into logic
- **Quotes.** "we need to be majorly rethinking how we implement and verify these circuits, so that we can have more
  tactics and automation and maybe some DSLs, for helping with all sorts of analysis and remapping and proof producing
  translation and decompilation into logic" (2026-07-11, `cc:9517ebc7-…`). "would we be able to do a kinda
  decompilation-into-logic to translate a fixed EVM contract ... into an as-efficient-as-possible set of circuits and
  aggreagtor/folds......?" (2026-07-26, `cc:2ed94bdd-…`).
- **Status: partly done, on paper.** `zkml-research/notes/evm-decompilation.md` §9 ("one fragment end-to-end") and
  `VERDICTS.md` §3d ("real, unclaimed at the right granularity, staged"). No code.

### 15. Hypergraph rewriting over theories as a production zkVM
- **Quote.** "a hypergraph rewriting framework that we should revisit and see if we can turn into an actual production
  zkvm, because it's an extremely powerful paradigm (hypergraph rewriting over theories/logics)" (2026-07-24,
  `cc:ccb26860-…`). Also "hyperedge as primitive might be interesting" (2026-08-06, `cc:b54b6026-…`).
- **Status: not started.** The only trace is a 10-03 replay note in `redregg/replays/`.

### 16. Analytic lower bounds as a weapon against bad speed claims
- **Quote.** "We would like to prove their claims about "100x speedup" fraudulent by demonstrating a solid lower bound of
  a polynomial proof of a defi relevant thing, using our arithmetizer (which implements Gabbay's framework)" (2026-07-26,
  `cc:8853efaf-…`).
- **Status: partly done.** `breadstuffs/tools/direct-logic-bench` and `papers/direct-logic-arithmetization` provide
  conformance plus microbenchmarks ("an unsound relation has no benchmark speedup"). There is no lower-bound
  statement. The analytic half of the request is missing.

### 17. Performance from first principles: within 5% of the hardware, synthetically
- **Quote.** "i really would love a way to get *excellent* performance on TPU, like, from first principles ... ensuring
  synthetically that we're writing good code that will execute to within 5% of what the hardware is capable of"
  (2026-11-06, `cc:78fef112-…`). Earlier: "isn't things going to get expensive at actual-realistic market sizes..?"
  (2026-07-17, DreggNet, `cc:c18f4027-…`) and "what if the data was already primarily resident on the GPU?" (07-18,
  same).
- **Status: partly done.** Register row 18 is at L0→L1, with deviceless TPU compiles on hbox and a bound calculator.
  The "synthetic" part of the request, a static check that proves a kernel sits at its bound, is the next gate and has
  not been built.

### 18. Verifiable dark continual learning, with virtualization tricks for training
- **Quote.** "are there other clever "virtualization" or other gigabrain techniques we can think about ... towards
  verifiable inference or (especially) training. because we are going to want verifiable dark continual-learnning at
  some point, and if the weights aren't fully encrypted truly terrible things may befall the mind within" (2026-08-13,
  `cc:1b80977b-…`). Also "is there no way to do it over a single untrusted provider?" (2026-11-06, `cc:78fef112-…`).
- **Status: partly done (L2).** Register row 3 has three custodians, 2^-101 per step, and a run of record ending around
  Nov 10. `DARK-LEARNING-PROGRAM.md` lists C1-C23; Rank1GradientCheck is at L1. The single-provider question is
  answered negatively in the lane files: FHE custody cannot gate execution, so MPC custody is forced (SWARM §3). That
  answer has not been put to ember as a theorem, and it should be.

### 19. Open, public verifiability of inference, floating point included
- **Quote.** "it is a top-priority goal for me to replicate attestable's results with public algorithms and public
  software" and "let's set our sights on understanding how we can make something BETTER and OPEN ... (**everyone**
  deserves verifiability) ... we can do actual floating point stuff i reckon.... we WILL need to be somewhat
  mathematically clever" (2026-08-12, `cc:3e64269c-…`).
- **Status: largely done to L3.** In register row 8, gptoss-int is bit-identical on Mac, x86, T4 and TPU v5e, and the
  exact recompute refuses steered transcripts. Row 13 is the eval-provenance receipt over Maverick. catgrad
  integration has not moved past `minidregg/Theory/ZkmlTensorOps.lean`.

### 20. STARK-in-FHE and FHE-in-STARK
- **Quote.** "doesn't it make sense to have both stark-in-fhe and fhe-in-stark the way you described it above, since they
  actually achieve very different contructional outcomes?" (2026-08-13, `cc:ca67a4c1-…`).
- **Status: partly done (L0).** `zkml-research/notes/two-ladder-composition.md` (08-13). vFHE G1-G6 are open, and the
  program parks vFHE beyond G1.

### 21. Fields, hashes and commitments are mutable
- **Quotes.** "like we're only using babybear because plonky3 already was" (2026-08-13, `cc:ca67a4c1-…`). "why *are we
  using poseidon2* are we stuck with it?" (2026-08-14, `cc:e68bba8f-…`). "the idea was to have a multi-commitment scheme
  where inside circuits we often want/need poseidon/poseidon2 but outside often want blake3 ... those tensions may not
  have resulted in a coherent design" (2026-07-31, `cc:0709475d-…`). "why are we folding bytes32 to bb? that sounds
  fake?" (2026-06-30, `cc:12518a7b-…`).
- **Status: mostly done as decisions.** `VERDICTS.md` §1 records the field and hash verdicts (KoalaBear refuted).
  `minidregg/board/RULINGS.md` sets cSHAKE256 roots and MPC-in-the-head over Keccak for ZK openings. The coherent
  multi-commitment design is U2 in `PROOF-SYSTEM-SPACE.md` (hybrid prime/binary over one byte-level content
  commitment), and it is unbuilt.

### 22. Re-found the kernel by its categorical laws; revisit SetField and single-felt values
- **Quotes.** "think really hard about recompositions/factorings/categorical constructions that we need to witness the
  broken symmetries of.... ... important values being a single babybear felt rather than a limbed bignum" (2026-07-26,
  `cc:d527daf6-…`). "a new/more abstract/purer/less rigid/more-"formally necessary by the laws of category to solve any
  problem like this"" (2026-08-07, minidregg, `cc:b54b6026-…`). "we would like to be able to derive the abstract spec
  from kinda cateogorical first principles" (2026-05-30, `cc:5a0f6a2e-…`).
- **Status: not done.** The 11-06 complaint about widening values from 1 felt to 8 shows the single-felt shape still
  spreading. Strand 15's C8 ruling on the canonical kernel is still pending.

### 23. Lazy, symbolic and retroactive proving modes
- **Quotes.** "the proofs need to be something that can **be performed *retroactively* on the accumulated local
  state/things** in some modes" (2026-05-29, `cc:5a0f6a2e-…`). "most of the system dynamics can proceed somewhat
  "symbolically/lazily" and we only need to actually collapse into a witness when demanded" (2026-06-22,
  `cc:2f7d6b31-…`). "what about modalities of operation that don't involve producing a full STARK all the time?"
  (2026-06-11, `cc:3b829648-…`).
- **Status: not started in the current program.** It appears only in breadstuffs reference docs. It has no register
  row.

### 24. Retained-mode, incremental global computation instead of re-execution
- **Quote.** "it seems fundamentally this current generation of code generation models keeps writing re-execution. if
  you imagine the global computation graph required to keep a mini system going, the whole thing would be incremental
  and efficient and held "retained-mode," ykwim?" (2026-10-31, minidregg, `cc:01a18fa5-51c4-7992-906c-97cb89814dae`).
- **Status: partly done.** RULINGS: "Snapshots, never genesis replays". Nothing makes proving or checking incremental.

### 25. A verified STARK verifier fully out of the TCB, and a verified autostark pipeline
- **Quotes.** "we need to expand the verified stark verifier? that needs to be like, fully out-of-the-TCB" (2026-06-26,
  `cc:960f30af-…`). "btw is our STARK actually sound? the one we use in minidregg? do we have a sound framework that
  takes our definitions from the logic and "autostarks" them..??? (is that itself verified..?)" (2026-09-30,
  `cc:0c315aee-…`).
- **Status: partly done.** `breadstuffs/metatheory/docs/SOUNDNESS-RESIDUAL-CENSUS.md` exists, and the ArkLib bridge
  (row 15) derives the Selvage keystone. The perfect-binding assumption at `Selvage/Commitment.lean:113` is still the
  seam. No one has given ember the yes or no that 09-30 asked for.

### 26. Research questions put to agents and never answered
- **Quotes.** "i also heard from chris allen that STARKs don't work for pow/pouw ... can you use kagi to maybe research
  what acceptably high performance and generality (recursion/folding/aggregation/pcd/whatever)systems we could/should be
  using in mini instead of / alongside the hash based iops" (2026-10-01, `cc:0c315aee-…`). The "zkvm swimlanes" file
  from Chris, with "crossreference everything they have been doing, against everything *we* have been doing"
  (2026-09-28, `~/dev`, `cc:181be9a9-8e84-419d-9321-a62d00be4970`). "a system that's built out of constantrate
  channels and does some kinda layered nonsense with broadcast domains that simultaneously also comes to consensus on an
  order" (2026-10-01, same session as the first).
- **Status: not visible.** None of them appears in the register or in the zkml-research docs. (The minidregg "swimlane"
  hits are the wekan app, not Chris's file.)

### 27. Method rules that keep getting lost

None of these is a construction. Each one is a reason later work went wrong when it was forgotten.

- "We **cannot** be having circuits in our TCB that don't have functional correctness and invariant
  preservation/correctness/commuting squares/refinement triangles -- otherwise our system is just a fancy LARP"
  (2026-06-08, `cc:3b829648-…`).
- "the only risk, is if you start compromising on either the runtime performance, or the assurance level" (2026-06-30,
  `cc:e6761437-…`). On 11-05 (obend, `cc:01a1a8fd-…`) ember traced this to Heiser: "security does not come at the
  expense of performance".
- "every time we get deep into these proof engineering projects ... you want to give up and start using testing which
  is the antithesis of formal verification" (2026-07-03, DreggNet, `cc:36b05823-…`). The counterweight: "testing is
  about validation, not verification" (2026-07-16, `cc:ec6d3a9c-…`).
- "Oh my god we keep *naming our residuals* ... We need to STOP GIVING UP" (2026-08-05, `cc:cde9cf30-…`).
- "we DO trust the lean system ... later on when assurance is more important than iteration time, THEN someone can go
  ahead and rerun the entire proof process on a *verified lean kernel*" (2026-11-06, `cc:78fef112-…`).
- "don't ask me "how do you want" type questions... "what do our constraints admit" and "what do the laws of computer
  science allow" are what guide us" (2026-06-23, `cc:f1ce2c45-…`).
- "we need to stop having astra do vacuity attacks lmao, and invite it to be a more equal peer collaborator not just
  attacking but also synthesizing" (2026-10-28, minidregg, `cc:01a1839d-…`).

---

## 2. Analytic and synthetic opportunities ember asked for that we never pursued

For each item, the next construction is the smallest one that turns the directive into a Lean object with an
executable consumer. None of them needs a GPU.

1. **Wp-derived constraint generation** (directives 2, 3, 14). Define `deriveConstraints : (Step : S → S → Prop) →
   Descriptor` by computing the weakest precondition of `post = step pre` over the Lean executor's IR, then prove one
   theorem for the generator: `sat (deriveConstraints step) (pre, post, w) ↔ step pre post`. Do this once, not per
   circuit. First target: the non-revocation circuit from the 07-15 /goal, compared byte-for-byte against its current
   emitter. This is C9 made real, and the law-1 test becomes a regression check, not the mechanism.

2. **A proof-repair transport for representation changes** (directive 4). For "widen 1 felt to 8": a Lean
   metaprogram, given an embedding/projection pair `e : F → F^8`, `p : F^8 → F` with `p ∘ e = id`, rewrites the
   affected definitions, re-elaborates each dependent declaration, and emits a census of goals it closed by
   `simp [p_e]` or `congr`, with the residue left as named goals. The gate is how many declarations break before and
   after. This also covers the "would editing the SPEC ... reliably turn the *proofs about the circuit* red" ask
   (06-20, `cc:01fdcbfa-…`).

3. **The cost model as a Lean function, with a provable Pareto front** (directives 1, 5, 17). Lift
   `COST-MODEL.md`'s counts (field multiplications, hash permutations, queries, opening sizes) into a total function of
   `(field, extension, blowup, queries, grinding, regime)`, with security drawn from `TwoRegimeQueryBudget`. Then prove
   that the chosen parameters are Pareto-minimal over a finite grid. Checking the grid with `#guard` or a compiled exe
   is fine (memory: compiled checks over the kernel). This replaces the hbox `recursion_tower_profile` sweep as the
   thing that decides F2. The run becomes a single calibration.

4. **A lower bound for a DeFi relation** (directive 16). State and prove, for a given arithmetization class (degree d,
   width w, lookups allowed or not), a lower bound on the rows or constraints needed for a 64-bit range-checked
   constant-product swap over BabyBear⁴. Then show the BitLogic or ModulusZK "20-100x" figure sits below it. This is
   the analytic half of direct-logic-bench.

5. **A certificate composition calculus in Lean** (directives 8, 9). A judgment `⊢ c : R @ (ε, A)` with rules for
   conjunction over a shared commitment (which carries the computational-binding term the 11-05 lanes found missing),
   sequencing, sampled audit (AuditSampling), recursion (adding ε), and deferral (directive 23). Instantiate it with
   Weld8 (and fix lane 0), `SubstringAt` from openings, MMR non-omission, and the Büchi window. This is the object
   ember asked for on 05-23, and it gives "properties on the form" one home.

6. **Datalog derivation and absence certificates** (directive 10). Positive facts: a derivation tree whose leaves are
   openings against the committed EDB root and whose internal nodes are rule instances, so it is checkable by an AIR
   that is a lookup into the rule table. Stratified negation: gap proofs over a sorted commitment, which MMR gap
   exclusion already supplies. Lean statement: `accepts cert ↔ (P, EDB(c)) ⊨ q`. This is ember's 05-20 "satisfiability
   ... against some merkelized fact universe", not evaluation inside the STARK.

7. **DAG PCD with a knowledge-soundness statement** (directive 6). Generalize `RecursiveAggregation` from chains to
   DAGs of bounded depth, with each node accumulating its predecessors' accumulators. Prove knowledge soundness by the
   same game-slot method `Selvage/Depth.lean` uses. Price tree against chain against scan-state with item 3's
   function, not with a run.

8. **Hypergraph rewriting as one AIR** (directive 15). Arithmetize a double-pushout rewrite step as a multiset (LogUp)
   balance over a hyperedge table plus a rule-table lookup. Then one descriptor serves every rewrite system, with the
   theorem `trace accepted ↔ valid rewrite sequence`. Automata, Datalog (item 6) and the effect VM become instances,
   which is the compression the 10%-of-the-lines goal for minidregg needs.

9. **A verified constraint-IR optimizer** (directive 11). Rewrite rules on the IR (CSE, degree reduction by
   intermediate columns, folding range checks into lookups), each proved to preserve the projection of the satisfying
   set onto public columns, with item 3's cost function as the objective. Combined with item 1, this is ember's
   "monthlong arithmetizer project".

10. **Assemble a proof system from shared parts** (directive 7). Pick one unoccupied point, U2 or U8 from
    `PROOF-SYSTEM-SPACE.md`. Instantiate it entirely from Selvage and ArkLib-aligned parts (PCS, IOR, FS/BCS
    compiler), so that the prover and verifier come from the composition and are not hand-written. The deliverable is
    the composition theorem plus the counts from item 3. This turns "lean is a bag of formal composable ingredients"
    into a demonstrated generator.

11. **The single-provider dark-learning impossibility, stated** (directive 18). A Lean statement that no protocol in
    which one party holds `Enc(W)` and can evaluate on chosen `x` can prevent an unsanctioned run. Then ember's 11-06
    question gets a theorem, and the MPC-custody decision has a reason in writing.

12. **A static roofline certificate** (directive 17). For each TPU kernel, derive FLOPs and bytes moved from the HLO,
    and require `achieved ≥ 0.95 × min(peak_flops, bw × intensity)` as a check computed from the compiler output. A
    Kaggle profile then confirms the number and does not discover it.

---

## 3. What ember keeps coming back to

1. **The proofs must mean something.** From May to November: "still bullshit?" (05-20), "a fancy LARP" (06-08),
   "we really DO NOT have a correct, safe, proven-secure circuit **at all**" (06-16), the 07-09 /goal "build real
   doors, not painted ones", "we keep *naming our residuals*" (08-05), and "WE NEED TO ACTUALLY FIGURE OUT HOW TO START
   USING THE MORE SOPHISTICATED VERSION OF THE THEORY" (10-27, `cc:01a17d0c-…`). The other half of the same theme: vacuity checking is "tacit behavior, not a contribution"
   (01-STEERS §2), and on 10-28, "stop having astra do vacuity attacks".
2. **Lean first, then generate everything else.** 05-31 (extract circuits from the real Lean), 06-08, 07-14, 07-15,
   07-28, 08-06, and 11-06 (the 1-to-8 felt repair). This is the most-repeated directive in the corpus and the
   least-built one. Strand 15 calls it "the law's most-repeated violation".
3. **Recursion and aggregation carry the load, in the Mina lineage.** "recursive proofs ARE the bomb" (05-20); "the
   mina setup tht i had designed in 2018" (06-29); 07-11 (a recursive fold for the light client); 08-03 ("our
   recursive stark-in-stark verification"); 08-05 ("We have recursive STARK verification. ALL over the place dude");
   10-01 ("thought about these problems a LOT at mina").
4. **Ambition: no downscoping, no minimal slices.** "It's genuinely NOT a multi year research project" (07-03);
   "Let's not pull back or flinch just because we have a big gap" (07-09); "you keep thinking ... downscope downscope
   downscope" (07-24); "I'm not trying to build a "minimal demo" ... pillars and layers" (08-17, dragons-clutch,
   `cc:c37f7ac1-…`); "oct13 isn't a deadline" (10-03); "we've let week-1 become a hobgoblin of our minds" (10-26);
   "starting with "one or two" is just absolutely never going to make any progress on this before we die" (11-06).
5. **First principles and categorical derivation.** Missing duals (05-24), the spec from categorical first principles
   (05-30), "gigabrained algorithms/decompositions/factorings/categorical-methods" for fhEgg (07-13,
   `cc:77a94632-…`), broken symmetries (07-26), the laws of category (08-07), universal constructions and colimits
   (10-28, for fn2), and natural transformations and "where structure survives transportation" (11-06, codex). The
   program has many measurements and few derivations.
6. **Against naive empiricism.** The 08-14 clock retraction, 10-27, 10-29, 10-31 and today. Ember respects
   measurement ("perf numbers on `hbox`", 07-14), but wants it to calibrate a model, not stand in for one.
7. **Frontier research, then our own synthesis.** "we don't want to merely fart out something any grad student could
   have done" (08-06); "implementing good ideas that just never have been combined yet (either because nobody thought
   of it or because it was too hard before AI)" (08-13, `cc:ca67a4c1-…`); "have we learned anything about advancing
   the pareto frontier of any construction at all" (08-17, `cc:c820add0-…`); "so that we're not just building whatever
   default bullshit your latent space has" (11-06, codex).
8. **Composition across the stack, not islands.** "does everything actually compose correctly from the dsl level all
   the way into the cell/turn model" (05-23); "we implement these mechanics individually excellently, but that they
   then also excellently compose" (07-13); "when we can start braiding these leafs into fully-composed orb software" (07-08); "new
   compositions SHOULD come with new proofs!" (07-08).
9. **Initiatives forgotten by the project-management layer.** "what else is wide-open or unprogressed" (08-13);
   "whether we've acquired myopia" (10-10, `cc:905fe751-…`); "we often fail to do a sufficient amount of project
   management to keep them all moving forward ;) and end up forgetting some initiatives" (11-06). Directives 4, 10,
   15, 22, 23 and 26 above are the current casualties.
10. **The open / shielded / dark spectrum, and openness as a public good.** Tiers of dark DreggFi (07-14), "we seriously
    do want to support multiple points on the spectrum" (08-06), "**everyone** deserves verifiability" (08-12), and
    "the ./orb and datacake ... is just a plain Public Good" (07-15).

**Reading across all three sections:** nearly every built directive was built empirically, as a run, a census or a
measured L3 demo. Nearly every unbuilt one is a generator, a calculus, a transport, or a bound. Ember has named that
asymmetry three times in eleven days.
