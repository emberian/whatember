# Strand 09 — DeOS, Mini, Nano, DelveTalk, Spween, preoscript and the Objective Bend convergence

Primary-source dossier, written 2026-11-02 from the repositories, git logs, memory files and review
corpora named in each section. Every number below was read from a file or a `git`/`wc` command on
2026-11-02 unless a dated document is cited for it. Hellas is not part of this strand; where the
memory record mentions it, it appears only as the boundary Ember drew ("that is a hellas thing, not
a dregg thing", 10-01).

---

## 0. How to read this, and four corrections to the brief

### 0.1 Source ledger

| source | path | what it settles |
|---|---|---|
| Mini memory (80 files) | `~/.claude/projects/-Users-ember-dev-minidregg/memory/` | mission, design laws, every Oct ruling (retained mode, never-slower, board/seats, demo goal) |
| breadstuffs memory (330 files) | `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/` | 09-29 decisions, 09-30 cutover, 10-08 drain-and-freeze, nano rebuild + wind-down, DeOS/firmament epochs |
| DelveTalk memory (12) | `~/.claude/projects/-Users-ember-dev-delvetalk/memory/` | the `foundation` takeover, "horseshit", posting-first, tulip privacy |
| obend memory (16) | `~/.claude/projects/-Users-ember-dev-obend/memory/` | modularity-first, no naive harness, ground-yourself-before-fanout |
| DreggNet memory (30) | `~/.claude/projects/-Users-ember-dev-DreggNet/memory/` | abandon-vs-operate, converged architecture, firmament/seL4, drorb |
| claudesplosion memory (4) | `~/.claude/projects/-Users-ember-dev-claudesplosion/memory/` | staffing (Sonnet fan-out, Opus review), hbox push route |
| review corpus | `~/dev/claudesplosion/{00..23,mini-1..6,99-SYNTHESIS,bakeoff/VERDICT}.md` | the 23+6 lane review, the bake-off numbers |
| retros | `~/dev/redregg/work/{RETRO-20261008,DECISIONS-FOR-EMBER-20261008,OB-WORLD-DESIGN-20261008,ARCHITECTURE-20261016,CYCLE-TIME-20261016,RECOVERY-20261016}.md` | why Mini was slow; why the swarm was frozen |
| the Discord bridge synthesis | `~/dev/aidev/docs/synthesis/bridge.md` §7, raw export `~/Downloads/bridge-corpus/dregg-metaconsequences-arendt-context-Bridge-1518087741525459064.txt` | the three unanswered holes, verbatim |

### 0.2 Corrections to the brief (primary sources disagree with its framing)

1. **"horseshit" was said about DelveTalk v1, not about Mini's performance.** The only memory hit
   for the word in the DreggNet/Mini/DelveTalk corpora is
   `-Users-ember-dev-delvetalk/memory/ember-working-style.md:21`: *"Three hours of autonomous codex
   produced 45 commits and a 124K-line repo ember called 'horseshit' and 'chug'; the failure was
   orchestration and refusal to subtract, not effort."* `~/dev/delvetalk` is that repo: 83 commits,
   2026-10-08 → 10-09, 125,146 tracked lines today. (A second hit, `birkhoff-asa-state.md:267`, is a
   different project.)
2. **Mini's performance failure is real but has two measured causes, neither of which is
   "functional programming" as such.** (a) *Immediate-mode re-execution*: the bake-off measured
   Mini's write at 2.6 s → 13.0 s → 25.5 s at 10/100/155 records, "superlinear (a quadratic fit
   describes it) and the cost is in the compiled Lean host re-admitting from genesis"
   (`claudesplosion/bakeoff/VERDICT.md`); Ember's 10-31 diagnosis is *"this current generation of
   code generation models keeps writing re-execution … the whole thing would be incremental and
   efficient and held 'retained-mode'"* (`feedback-retained-mode.md`). (b) *Concrete-import
   cascades*: a codec pin regen rebuilt ~486 modules, a deep Theory edit 631 modules in 39 min;
   Ember: *"there are HUGELY DIFFERENT WAYS we should have been structuring this code from the
   beginning. by now it's just ... slop"* (`feedback-abstraction-recover-forward.md`, 10-28). The
   pure-functional `List UInt8` representation is a contributing constant factor (4,798 lines of
   `List UInt8` vs 329 of `ByteArray`, `ARCHITECTURE-20261016.md` §0.2), not the root.
3. **The bake-off is dated 09-29 (run) / 09-30 (verdict), and Mini did not "win" outright.** Neither
   tree passed: Bread failed J5/J6/J8 (kernel semantics); Mini failed growth (storage/recovery).
   The verdict went to "the cheaper class of work": *"Mini keeps the role it was given on 09-19."*
   Ember afterwards: the Bread half was unnecessary ("I could have told you").
4. **"Opus 4.8" in the three-holes quote is a Discord participant handle** (`<@Opus4.8>`) for "the
   dreggon", an Opus 4.8 Claude Code session working in the dregg repo whose replies Ember pasted
   into the multi-model Bridge room (bridge.md:68, :146). Opus 4.8 is also a real co-author in Mini's
   history (73 commits carry `Co-Authored-By: Claude Opus 4.8`).

---

## 1. The arc in one diagram

```
2026-06 ──────────── breadstuffs (dregg2/robigalia) ──────────────────────────────────────────────
  06-14 firmament boots on seL4 (M0/M1/M2/M-STARK/M5)      06-19 "i am the person who needs this substrate"
  06-22 DESKTOP EPOCH green (deos-zed, deos-terminal, deos-matrix, deos-hermes, membranes)
  06-21 Bridge room "arendt": Opus4.8 names three holes (guard / cover / merge-membrane) — never answered
  06-28 DreggNet foundation ─┐  07-02 drorb engine  07-05 DreggNet product ABANDONED (ported native)
                             └─ 07-10..12 DreggCloud "House" firmament (88 commits) → handed to Fable
  07-14 dregg-stitch-kit: history stitch of breadstuffs (built, adopt.sh gated)
2026-08 ──────────── minidregg (Mini) ─────────────────────────────────────────────────────────────
  08-06 founded: "formal-first reimplementation … ≤10% LOC (~290K) … everything derived"
  08-07 ATLAS e6a32c4c3 · LOOM proof-system direction · OB-2 proved FALSE (audit lesson)
  08-10..14 leanuweave: DAG-CRDT dichotomy → preoscript (166 commits, stops at a usage wall)
2026-09 ──────────────────────────────────────────────────────────────────────────────────────────
  09-29 claudesplosion: 23 Fable lanes over Bread+fn, 6 Opus lanes over Mini (read-only)
  09-29/30 BAKE-OFF  → "Mini keeps the role"; Bread gets fixes, not construction
  09-30 DATAMODEL wave A→S4 (one store Π₀ a, Option (V a.1)); workhorse = first public Mini node
2026-10 ──────────────────────────────────────────────────────────────────────────────────────────
  10-01 no proof system in Mini admission (`witnessed` compiles to constant false)
  10-03 Codex wall · "Objective Bend" named (BEND-WORLD-LANGUAGE-20261003)
  10-08 DRAIN AND FREEZE: "they aren't going to be solved by sending out subagents"
  10-08 delvetalk v1 (codex, 3 h, 124K lines: "horseshit")
  10-09..15 delvetalk2 `foundation` (2,580 commits): gsb + obend towns live, edition 20
  10-16 Mini resumed ("MAIN IS THE BATTLEGROUND") · nanodregg founded ("rip and tear")
  10-26 Mini hcloud demo goal (demo.dregg.online, shuts 11-11) · nano frontier night
  10-27 nanodregg WOUND DOWN (2dcc9ea+) · Mini rehearsals · minidregg-lanes swells (273 worktrees)
  10-29 obend extracted (b7960e5): "Ground the Objective Bend extraction in its source trees"
  10-31 Mini board/seats (no integrator) · seat/infra handoff cd493933f · retained-mode ruling
  10-31 obend `Lower` (1)-(7) by Opus/Fable; then unattributed "Hardware" commits begin
  11-01..02 obend waves m1–m5, ws23–ws33, wave1–3 (unattributed; Silicon Elaborator, Next Mathematica)
  11-01 multimodel council (Argon / Astra / Fable): spine real, waves 5–6 "tests wearing theorem clothing"
```

---

## 2. breadstuffs DeOS — the root system

**Repos.** `~/dev/breadstuffs` (10,359 commits; last 2026-10-01 `22fad151e`), `docs/deos/` (250 design
docs, e.g. `DEOS.md`, `DOC-CELL-COMPOSITION.md`, `BRANCH-AND-STITCH-PROTOCOL.md`,
`CROSS-DEVICE-FIRMAMENT.md`, `AOL-WONDER.md`), DeOS crates at the workspace root.

### 2.1 What it is

Naming triad (`DreggNet/memory/dregg-sel4-deos-firmament.md`): **robigalia** the project, **dregg**
the verified distributed object-capability kernel, **deos** the agentic desktop user layer ("dregg
made visual; a window IS a `Capability{Target::Surface(cell), rights}`").

The **firmament thesis** (`docs/FIRMAMENT.md`, 494 lines; `sel4/dregg-firmament/`): an seL4
capability and a dregg capability are the same abstraction at different points of a distance
parameter `n`; `n=1` collapses distributed bounds to strong-local ones. Proved in
`metatheory/Dregg2/Firmament/{SeL4Abstract,CapGradation,SeL4Kernel,SeL4Composition}.lean`, keystone
`dregg_turn_in_pd_preserves_both` (a dregg delegation embedded as an seL4 `mint` preserves both the
derivation-tree invariant and cap non-amplification). The 6-PD Microkit assembly
(`sel4/dregg.system`): executor (links `libdregg_lean_elf.a`, runs `execFullForestG`) · verifier
(Lean-free plonky3 STARK checker) · persist · net (virtio single-queue) · net_client (smoltcp + Ed25519
`SignedTurn` gate) · app.

Boot ladder (`project-firmament-sel4-boots.md`): M0 Rust PD prints "dregg robigalia v0"; M1 verifier
PD; M2 rbg DirectoryCell PD; **M-STARK** real BabyBear+BLAKE3+FRI STARK proved and verified on-device;
M5 riscv64; M3 virtio-net ◐. Live image viewer `bbccc03ca`; cockpit render on the seL4 framebuffer
`d92d0526c` (06-19); live repaint on a genuine verified turn `251692b78`/`2824056ee` (06-25).

The **desktop epoch** (`project-deos-self-hosting-epoch.md`, 06-22): editor+terminal dock panes
`a3f7ce07`; `dregg-doc` Pijul patch core with `Dregg2/Deos/DocMerge.lean` `f8184fbe`; deos-matrix
with membranes in messages `f17b0d15`; `starbridge-v2/src/shared_fork.rs` mint→rehydrate→drive→stitch
`7414c820`; deos-hermes confined agent `1de5c0ed`; Settlement Soundness proved `caa8c24ab`
(`Circuit/SettlementSoundness.lean`) and wired into production `stitch_pair` `3c0467262`.

The purpose, Ember 06-19 (`project-deos-ux-vision.md`): *"i am the person who needs this substrate.
i'll be using this os for a while."* The feeling: 1999 AOL wonder fused with Pharo liveness.

### 2.2 What the 09-29 review found in DeOS (lane 17, `claudesplosion/17-deos.md`)

Sizes read by the lane: deos-hermes 24k, deos-view 20k, deos-js 17k, servo-render 25k, deos-matrix 8k,
deos-zed 7k, deos-terminal 2k. Only `deos-reflect` is in `default-members`, so a bare root `cargo
build` touches none of the JS engines, views, hermes, matrix or terminal. Confirmed at source by the
orchestrator (`99-SYNTHESIS.md`):

- **#4** `deos-terminal/src/bin/pty_ws.rs:67-89` — `accept_async(stream)` with no header callback: no
  Origin check, no token, then `$SHELL` on a fresh PTY. Any page open on the machine can reach it.
- **#14** `deos-hermes` tells the model a command ran that did not.
- Two-JS-engine drift (`ApplyOp` 4-vs-5 variants; boa `deos-js-runtime` has no non-test consumer).
- A missed twin: `sdk/tool_gateway.rs` hand-mirrors Lean `delegAdmit` with no differential
  (`project-deos-starbridge-levelup-campaign.md`).

**Maturity Level:** firmament + desktop epoch **L3 Proved/Tested Core** (boots in QEMU, proved
keystones, tested crates); public DeOS **never L4**. The whole of breadstuffs is
**Frozen-for-Rethink** since 09-29 ("Bread gets fixes, not construction"; "Mini supersedes Bread
EVENTUALLY, NO DATE").

**Unclosed Cycles & Missing Links.**
- *The self-hosting loop* ("a session like this runs INSIDE deos") never closed: the agent fleet
  moved to Mini/nano/obend, none of which carries the gpui cockpit or the seL4 image.
- *Firmament → network*: `.system`/CapDL image, the driver and the network path are unproved; the
  Lean-on-seL4 path is "a HACK" (77-module `Dregg2.Exec.FFI` closure cross-compiled to musl).
- *Membrane interception*: "automatic fail-closed boundary INTERCEPTION in the fork executor" is still
  a named follow-on; today the guest raises its own consent request.
- The pty bridge and hermes-honesty findings were leads; no record shows them closed.

**Promising & Ready for Revival.**
- The n-distance capability (`Router` choosing Local/Distributed/Surface) is the cleanest statement of
  "single-machine properties when single-machine" anywhere in the corpus; obend's
  `Run/Fork.lean` and `Vault/Rehydration.lean` re-mechanize pieces of it without the seL4 half.
- The rehydratable membrane (`Membrane.lean::reshare_chain_attenuates`, `confined_chain_covers_log`)
  is the most worked answer to hole 3 (§11).
- `docs/desktop-os-research/GPUI-OFFSCREEN-FORK.md` + the headless `--screenshot` bake is a reusable
  pattern for any gpui surface.

**Struggling / Needs Ember's Human Attention.**
- `HOLE[design]`: whether DeOS is resumed in breadstuffs, rebuilt on obend, or composted. Ember's
  10-21 nano charter calls breadstuffs "the whole system built before it [that] waits to be resumed
  or composted into the next robigalia". No later ruling.
- `dregg-stitch-kit` (07-14) holds a destructive `adopt.sh` that force-pushes a filter-repo'd history
  of breadstuffs; `.built-from` = `9f0587d67`, while breadstuffs main has since moved to
  `22fad151e`. The kit's own guard will refuse; the decision whether to ever stitch is Ember's.

---

## 3. DreggNet, DreggCloud, drorb — the operated-cloud detour

| repo | branch / commits | span | role |
|---|---|---|---|
| `~/dev/DreggNet` | `dregg-native-rebuild`, 520 | 06-28 → 07-27 `7f51591` | planning + the verified compiler track (Pancake/CakeML, orb cut) |
| `~/dev/drorb` | `main`, 618 | 07-03 `221ca24` → 07-26 `f253290` | "a formally verified network engine": implementation + verification only |
| `~/dev/DreggCloud` | `main`, 88 | 07-10 `ed91fff` → 07-12 `e9ff17a` | "operated firmament": House / Worlds / Rooms over breadstuffs path deps |
| `~/dev/dregg-stitched-final` | `main`, 5,465 | 05-19 → 07-14 | product of the stitch kit (pyana root → breadstuffs) |

### 3.1 The arc

- **07-02 review** (six Explore lanes, `dreggnet-review-unification.md`): real core (2-node fabric over
  headscale, wasmi sandbox, duroxide metering, real Poseidon2 roots) beside a **shadow value/auth
  layer** (its own receipts crate with `turn_receipt_hash` always `None`, a `ConservingLedger` i64
  twin, a dead light-client path `ENABLED=false`, three meters). The carried lesson: *"every shadow has
  a real counterpart one dependency edge away"* — weld, don't rebuild.
- **07-05** DreggNet-the-product abandoned; parts ported dregg-native (`0f12286a3`, `0310c9e31`):
  `dregg-sandbox`, `starbridge-apps/{org,billing,domains,guard,vat,edge-mandate}`, `dregg-umem`.
- **07-09** Ember reopened it as a local cloud; **07-11** converged architecture
  (`DreggNet/planning/ARCHITECTURE-converged-2026-07-11.md`): owner-as-anchor · per-grain ·
  attestation-as-ledger-fact · consensus-by-exception. The landmine: `persist::canonical_ledger_root`
  hashes every cell into one flat root, so 3 nodes produce 3 roots and quorum never assembles. Fix: no
  global ledger; `umem::merge` for I-confluent merges, escalate only conserved quantities.
- **07-10..12 DreggCloud**: a House serving Worlds and Rooms at `127.0.0.1:8787`, prepaid service
  custody "House schema 16" (`e9ff17a`), `grain-serve` over sandstorm-serve; handed to Fable `bd494a4`.
- **drorb** to 07-26: "★★ a live tailnet SURVIVES a coordinator restart" `d4e799a`; "delete the
  assurance theater" `4fccef3`; the HOL4 half of `orb-compiler` "cannot be cut as an artifact"
  (`b147749`).

**Maturity Level:** DreggNet product **Compost/Superseded** (its own banner: "DO NOT scope work
against ~/dev/DreggNet"); DreggCloud **L2 Prototype**, idle since 07-12; drorb **L3** for its proved
admission fold and live tailnet, idle since 07-26.

**Unclosed Cycles & Missing Links.** Consensus-by-exception is designed, not built; the operated
edges (webauth forward-auth W-1, machines-API W-2, static hosting W-3, status W-4) have no native
home in breadstuffs; Mini later re-solved hosting with Sandstorm SPKs instead. drorb's GOAL.md ends
with "the TCP-vs-ping gap at the top of what is next" (`6a52009`).

**Promising & Ready for Revival.** The 07-11 four-move architecture is exactly the agreement shape
nanodregg's TRUST frontier later proved for one World (`certified_intersect`), and the
"consensus-by-exception at a conserved quantity" rule is what preoscript's `Cost.coordination_forced`
formalizes. A revival would wire those three together.

**Struggling / Needs Ember's Human Attention.** The DreggNet memory records the strategic fork
("extend here vs port serving edges native") as Ember's explicit open decision; no later ruling.

---

## 4. claudesplosion — the 09-29 review and the bake-off

`~/dev/claudesplosion` (160 commits, 10-01 `d2baa52` → 10-03 `6c45f2e`). `AGENTS.md` points takeovers
at `planning/DREGGNET-CLOUD.md`, `planning/OVERNIGHT-2026-10-02.md`, and
`planning/handoff-2026-10-03/START-CODEX.md`.

### 4.1 The review

- **Lanes 01–23**: Fable lanes over breadstuffs and fn, ~10 min each, read-only ("every lane was
  forbidden to build, test or run anything"), ~4.1M tokens total. **mini-1..6**: six Opus lanes over
  Mini, briefed for depth.
- `99-SYNTHESIS.md` (833 lines) keeps two tiers apart: CONFIRMED AT SOURCE (orchestrator re-read the
  lines) vs LANE-REPORTED.

Selected confirmed findings on Bread: rotated-leg commit anchors read from outside the proven public
inputs (`verifier/src/rotated_replay.rs:175-186,274-292`, fix `==` for `>=`); SEV-SNP verify never
gates on guest policy (`tee-verify/src/snp.rs:343-381`); `vcg_run_sound` quantifies over every
`RecChained` so it is refuted by `method + 1` (`Proof/WP.lean:199-206`); `verifyBatch` discards `_vk`
(`Circuit/CircuitSoundness.lean:820`); `World.gst_liveness` is a tautology (`World.lean:104-115`).

Round two on Mini: **M1** sumcheck verifiers take challenges from the proof; **M3** `Gate.admit` has no
sign check on a move; **M6** multi-cell agreement holds by `rfl` because every cell gets the same
constant; **M10** three live Assurance modules quantify over a type the repo proved empty; **M12**
`decider_sound` is `Iff.rfl`; **M15** README says no `#guard`s, main build has 18.

### 4.2 The bake-off (`bakeoff/VERDICT.md`)

| step | Mini | Bread |
|---|---|---|
| J0 start | pass, 10.3 s | pass, 214.6 s (200 s Lean init) |
| J4 read+write+readback | pass, Lean | write passes; signed read not expressible |
| J5 ungranted key refused | pass both ways | **fail**: anonymous read returns every field |
| J6 reopen + exact retry | pass (`replayed`) | **fail**: `receipt chain mismatch` |
| J8 deny-all, no owner bypass | pass | **fail**: `Cases([])` refuses its own installation |

| records | Mini write | Mini reopen | Bread write | Bread reopen |
|---|---|---|---|---|
| 10–15 | 2.6 s | 5.4 s | 4.30 s | 207 s |
| 100–105 | 13.0 s | 121 s | 3.97 s | 225 s |
| 155 | 25.5 s | 243 s | — | — |
| 1000 | extrapolated 200–1000 s | ≥ 2000 s | 4.07 s | 438 s |

On Mini "the compiled Lean host [decided] at every step"; on Bread "every capability, law and write
turn, 11 in the journey and all 991 growth writes, was fenced onto the Rust path". Operator glue: Mini
167 lines of shell; Bread 431 lines including a 294-line Rust client and a 34-line `LD_PRELOAD` shim.

**Maturity Level:** the corpus is a finished artifact (**L3** as evidence; frozen); its findings are
**leads**, by its own banner.

**Unclosed Cycles & Missing Links.** "What would make this more than a list of leads" (§ at :819) asks
for refuting experiments; for Bread, nine fix lanes B1–B9 landed in `292829518` (09-30); for Mini the
round-two findings fed the DATAMODEL waves. No register maps each finding to its closing commit (the
DelveTalk equivalent, `docs/review/codex-2026-10-10/ROUTING.md`, does).

**Promising & Ready for Revival.** The two-tier CONFIRMED/LANE-REPORTED format is the strongest
review discipline in the strand; `claudesplosion/memory/swarm-staffing-sonnet-opus.md` ("~5 Sonnet 5.5
subagents for independent work, plain Opus for source review") is its staffing rule.

**Struggling / Needs Ember's Human Attention.** Bread's J8 may be expressible with a "latch" law; the
lane "wrote the law out but did not run it". Bread's 200 s Lean init per process (issue #86) was
narrowed to 8 s by `6ecf9dfc1` on 10-01. Persvati's 160 bake-off predecessor directories stay by
Ember's decision (`persvati-datamodel-dirs-stay.md`).

---

## 5. minidregg (Mini) — Aug 6 → Nov 2

`~/dev/minidregg`, branch `main`, 8,206 commits (Aug 1,106 · Sep 1,112 · Oct 5,988), first commit
`e6a32c4c3` "ATLAS: the founding map — six-lane breadstuffs exploration distilled" (08-07), head
`c4ecabe0f` 10-31 "store-retained: hold served cell state in a persistent map and bind replayed
suffixes once". Co-authors: Opus 5.5 4,096 · Sonnet 5.5 415 · Fable 5.1 375 · Fable 5 104 · Opus 4.8 73.
Tracked size today: **647,957 Lean lines, 338,437 Rust lines** against an ATLAS budget of ≈290K total.
`Effects/` (the derivation engine that was to make everything derived) is **1,785 lines**.

### 5.1 The founding laws (August)

`minidregg-mission.md`: *"Never hand-write AIR or implementations — everything is derived … Budget:
≤10% of breadstuffs' total LOC … Thesis: 'a proof-native semantic computer.'"* The baseline: 2.89M code
lines; `metatheory/Dregg2/Circuit/Emit/` alone 271K (the #1 collapse target); the semantic core only
~25K.

`minidregg-design-laws.md` (full version `ATLAS.md` §6): *"the derived path is the ONLY path; nothing
lands beside, everything replaces; delete the twin."* Keystones carry `satisfiable` + `teeth` +
premise-inhabitation at the declaration; Bound ≠ Forced as two types; syntactic IR leaves, never Lean
closures ("that's why breadstuffs has 3 compiles and 29 hand welds"); "determination is eager; witness
is lazy — no hole ever defers its δ or guard".

The audit lesson (`minidregg-audit-discipline.md`, 08-07): an OB-2 depth-composition statement passed a
polarity-only audit and was then proved false (`OB2_depth_composition_false`, the `Z=∅` corner admits
`εrbr := -1`). Rule: a keystone is not audited until its witnesses are built in Lean.

### 5.2 September: datamodel, proof system dropped, Bread demoted

- 09-29 decisions (`project-2026-09-29-decisions-shellserver-goal.md`): `valid_until` is a block height;
  Mini = resource-world kernel; Bread = coordination substrate with users. Ember, late 09-29: *"i think
  mini's role is to take over from the old dregg repo but who the fuck knows what time of timescale
  thats gonna happen on."* Preconditions named: a store that does not slow with history (13 s write at
  100 records) and Mini equivalents of signed turns / receipts / event topics.
- 09-30 (`project-2026-09-30-mini-cutover-state.md`): one night, ~45 Opus lanes + 1 Fable. Data model:
  one store `Π₀ a, Option (V a.1)`, one patch type, sparse Merkle root with openings, history = fold +
  checkpoint + suffix, conservation as the kernel of a homomorphism. `wave-s4` UMBRELLA GREEN with
  journey J0–J8 + K4. Product M3–MJ (provisioning, ssh shell, Hermes via MCP, grain running, M7
  byte-identical candidate). dregg-workhorse chosen as the first public Mini node.
- 10-01 (`project-no-proof-system-in-mini-admission.md`): *"Nothing at admission verifies a proof.
  `Pred.witnessed vk` COMPILES TO CONSTANT FALSE in the policy circuit."* Decision: proofs stay an empty
  optional carrier slot; Selvage stays research. Scope addendum: Mini's user compute is NOCK programs
  only, then (22:15) Nock is evaluator #1 in a registry.

### 5.3 Why Mini was slow — the measured causes

| cause | evidence | number |
|---|---|---|
| re-admission from genesis | bakeoff VERDICT | write 2.6 → 25.5 s from 10 → 155 records; quadratic fit |
| `atPrefix` O(h²) | RETRO-20261008 (BURN-BENCH) | 56.6 min at 30k records |
| byte lists + child process per call | ARCHITECTURE-20261016 §0.2 | 4,798 `List UInt8` vs 329 `ByteArray`; 56 `partial def`; "11×–6,700× the necessary work per operation" |
| two state machines joined by a theorem | ARCHITECTURE §0.1 | Host runs `DurableDataIntent.execute`; `World.admit` only in the follower; `host_submit_is_step` "exists only in a docstring" |
| protocol width | ARCHITECTURE §0.3 | 184 active opcodes / 25 families; ~120 Host CLI verbs; 51 `NativeAdmission` constructors; 70 versioned modules |
| import graph a deep chain | CYCLE-TIME-20261016 §0.4 | Host.Main closure 776 modules, depth 87; critical path 65k of 321k lines (≤4.9× parallelism); hub edits rebuild 400–930 modules |
| serial builder | CYCLE-TIME §0.2 | `build-native-host.sh` one `lake build` per module, 2 threads; a zero-change host step 895 s |
| no shared cache | CYCLE-TIME §0.3 | one lane tree rebuilt 823 modules in 8,046 s |
| waiting, not compiling | CYCLE-TIME §0.1 | 61% of 222 lane-hours in foreground waits; 0.86 commits per lane-hour |

Ember's three design laws that answer this table, in order:
- **10-28** recover forward through typeclass/interface seams, "one measured seam at a time"
  (`feedback-abstraction-recover-forward.md`), and statements may change to be efficient (*"we do NOT
  need to 'prove by equality' lmao"*, `feedback-statements-may-change.md`).
- **10-29** *"the system should NEVER GET SLOWER OVER TIME (except by at most a logarithmic factor)"*;
  10-31 the ~1 ms warm-per-action direction (`feedback-never-slower-over-time.md`).
- **10-31** retained mode: *"treat every derived value … as a maintained node with declared inputs and
  a delta-update rule … a read is a lookup"* (`feedback-retained-mode.md`).

### 5.4 The 10-08 drain and freeze

`project-2026-10-08-drain-and-freeze-for-rethink.md`: Ember, ~23:50Z, *"we have some major problems
with this software right now, and they aren't going to be solved by sending out subagents"* → drain the
queues, freeze for an architectural rethink, and rewrite the metacoordination protocol files outright
("INSANELY more reasonable coordination").

What the RETRO measured (`redregg/work/RETRO-20261008.md`, by Opus sub-agent a9d25a2d over `cv`):

| # | obstruction | measured cost |
|---|---|---|
| 1 | aged-context agents | 26 of 125 lanes at ≥300K tokens/call used **62% of 5.6B** lane tokens; two died of `Prompt is too long` mid-proof |
| 2 | coordination costs as much as work | deputies + keeper **1.6B (29%)**; root 355K fixed context per turn over ~1,530 turns |
| 3 | static-gate green taken as landed | standing journeys 1/102 → 5/60 → 23/48 → 24/50 nonpass while main was pushed |
| 4 | installed copies decay | journey runner a stale copy for ~21 h |
| 5 | usage walls | 4 Claude walls in 40 h; Codex ~150% of a week's quota in ~18 h |
| 6 | bookkeeping churn | 108 of 330 commits re-pin/ledger/fixture; main stalled 77–83 min ×3 |
| 7 | global version counters | Activity COMMAND v4 → v12 in two days; 66 of 378 commits mention a re-genesis |

Status at the decision: GitHub main `5896a594`; kernel train green at `8e37e22d` (R0–R2 of the OB→World
join, two Θ(2ⁿ) encoder fixes). The same night produced `OB-WORLD-DESIGN-20261008.md` (709 lines; §8
"SPK × OB: the powerbox is grants").

**10-16 resumed** — *"MAIN IS THE BATTLEGROUND"*: main fast-forwarded `7ffd6524 → 2c27b08b`; `next`
retired. The same day the reorientation documents (ARCHITECTURE, CYCLE-TIME, RECOVERY) showed the bloat
and Ember launched nanodregg (§9). Mini memory 10-26: *"Past sessions repeatedly planned a 'rip and
tear' and never started it (ember, 2026-10-13: 'are we just stuck in an attractor?')."*

### 5.5 The demo push (10-26 → 11-02)

`minidregg-hcloud-demo-goal.md`: finite prefix of coherence work → temporary public Hetzner demo →
later re-genesis on pug's homelab. `demo.dregg.online`; shutdown **2026-11-11**; every surface ON
(Hermes, SPK grains, PAY, Discord gateway mode, web, ssh). README today: *"Lean decides what is allowed.
Rust handles the physical edges … `World.admit` in `Kernel/World.lean` is the model of a world
transition; `Kernel/HostRefinesWorldCore.lean` proves that the Host's deployed path
(`DurableDataIntent.execute`) refines it."*

Rulings recorded on main, `board/RULINGS.md`: no rehearsal cut for now, make the system excellent;
today's worst costs "app create to first page ~26 s … `story new` 10-15 s; birth submit ~600 ms and
growing with height; certify ~6 s per tail; cold first read 3.9 s"; hashes are cSHAKE256/KMAC256, no
Poseidon2 for roots; "Cold first read and restart are the full Store open, O(height) (~4.3 ms per
record). They go away only with KN2 stage 2b".

`board/REDS.md` at tip `3c6b99064d42`: **5 red** (host build failed; consent/rust/pack/umbrella did not
run); `green` = `83e926874e38`. The last two days' commits are the retained-mode work in practice:
`48b93d3c1` "eliminate target cell re-hash", `462919a4c` "target pre-roots and read guards come from the
ground's snapshot, not a re-hash", `c4ecabe0f` "hold served cell state in a persistent map".

### 5.6 minidregg-lanes and minidregg-seat-infra

- `~/dev/minidregg-lanes`: **273 lane directories** (not a git repo itself), e.g. `app-reds-*` (11),
  `oracle-*` (14), `hp-*` (10), `pd-*-target` pairs, `fae-2..10`, `glm-*` scouts, `qualify-*` (10),
  `exorcism`, `iter-speed`, `effects-revival`. Newest mtimes 10-31 (`he-births`, `he-enrol`,
  `build-loop-tools`). The warm Lean build `integration/.lake/build` at `55e483e0` seeds other trees by
  `cp -al` (`dregg-boxes-2026-10-27.md`).
- `~/dev/minidregg-seat-infra`: branch `seat/infra`, 8,185 commits, head `cd493933f` (10-31) "board:
  infra seat rewritten whole as a handoff for a new agent". Its neighbours `9317f32fc` "flatness is
  published, never a red; finished gate worlds are reaped" and `48dc530f2` "idle leases taken after 30
  min, pool grown to 11" are the builder/seat model of `project-board-coordination.md`: trunk `main`,
  `board/{README,RULINGS,REDS,COSTS}.md`, `board/seats/*.md` (apps-hermes, build-loop, explorer,
  host-execution, infra, member-side, privacy, read-path, store-retained), no integrator agent.

**Maturity Level:** **L4 Deployed** (demo at demo.dregg.online on dregg-forge nspawn `demo`, rehearsal 3
lineage; batch 4 `b9450147f` the green fallback) with a **L3** kernel (`deployed_refines_step` proved).
Main is red (5) on 11-01.

**Unclosed Cycles & Missing Links.**
1. **The derived path.** `Effects/` is 1,785 lines; new kernel effects are still hand-written. Ember
   10-27: *"hand-written kernel changes aren't really acceptable after all"* — deferrable by hours, not
   forever. Pathway: revive `Effects/` statement-first; transfer and commit become its first two
   declarations and the hand versions are deleted.
2. **Host ≠ World.** The Host still does not call `World.admit`; TURN-LOG (lane/turn-log) is the
   designed collapse.
3. **O(height) open.** KN2 stage 2b (light `Opening`) is the named exit; until then cold read is linear.
4. **Retained mode** is a ruling, with one seat (`store-retained`) doing it; the generic
   "maintained = recomputed" theorem "lives in Lean once" is not yet written.
5. **The budget.** ~986K tracked lines vs ATLAS ≈290K.

**Promising & Ready for Revival.** The 11-11 shutdown is a natural cut: the demo's journeys, SPK powerbox
design (OB-WORLD §8, "request = a send to the user's inbox; answer = a GRANT OBJECT"), the composed gate,
and the consent resident are the parts worth carrying; obend already re-grounds the language half.

**Struggling / Needs Ember's Human Attention.**
- The coordination record shows the same failure repeating under four regimes (deputies 10-06, Codex
  trains 10-08, integrator batches 10-16, seats 10-31). Ember 10-27 (`feedback-fewer-lanes-mental-simulation.md`):
  "parallel lanes redo the same proof work". 273 lane directories on the Mac is the physical residue.
- `HOLE[design]`: what Mini is after 11-11. The 10-23 README already named nanodregg "the single-writer
  rebuild" and Mini "the production demoland and the spec/battleground"; nanodregg was then wound down
  and obend extracted. Nothing on record says which tree carries the kernel forward.

---

## 6. DelveTalk v1 and DelveTalk2 `foundation`

### 6.1 v1 (`~/dev/delvetalk`)

83 commits, 10-08 `adda16ec` "Build DelveTalk core quartet, durable protocols, syntax adapters and Spween
scenes" → 10-09 `625da35e` "checkpoint"; 125,146 tracked lines. README: *"Objective Bend defines
behavior; Spween defines scenes and choices; Lean admits changes under each object's current law."* This
is the "horseshit"/"chug" repo (§0.2). Ember's corrections to codex, verbatim from
`ember-working-style.md`: *"every single time we find ourselves 'expressing an honest caveat' we are
ACCEPTING MEDIOCRITY"*; *"we don't need migrations. we don't need preservation"*; *"quit yapping"*.

### 6.2 delvetalk2 `foundation`

`~/dev/delvetalk2`, branch `foundation`, 2,580 commits (10-08 17 · 10-09 703 · 10-10 833 · 10-11 243 ·
10-12 489 · 10-13 120 · 10-14 174 · 10-15 1), head `fb217996` 10-15 "README: the lexicons are
published (18 com.atproto.lexicon.schema records …)".

**The language.** `spec/bend/origin.json`: upstream "Mini", `github.com/emberian/minidregg` commit
`dcab86da8f…`, baseline files `Theory/ObjectiveBendOpenRecursion.lean`, `ObjectiveBendTypes.lean`,
`ObjectiveBendTyping.lean`, `Sp800185Cshake256Spec.lean`. 72 Lean files, 50,852 lines under `spec/`.
`docs/FOUNDATION.md` (replay edition 20): *"Asking the world is the only effect. Python carries bytes
and credentials and decides nothing. Every journal entry is an AT Protocol record."* The core construct:

```
def bump(state: State, context: Abi.Context) -> Activity<Nat>:
  let written(_) = write {count: add 1n}
  state.count + 1n
```

Proved and relied on: `stateV3_roundTrip`, `settle_resume_segment`, `trim_resume_segment`,
`checkpoint_resume_segment`, `conformsUnder_iff`. Not proved: the static `noActivity` guard, canonical
CBOR round trip, and "the commutative-root rule beyond its `#guard`s" (KERNEL-HANDOFF §1).

**Host.** One Lean process `delvetalk-obend serve` (`spec/Delvetalk/Serve.lean`, `spec/native/serve.c`),
`flock` single writer, public socket 0600 + root socket 0660. Lazy state cells: a one-row read of a
2,048-row relation 2.9 ms → 45 µs (kernel11) and 72 → 13 ms on the stored path (host16). Block-store
journal: open from snapshot 5.25 s → 0.19 s, 284 → 124 MB on 20,000 turns.

**The design moves (memory `delvetalk-takeover-context.md`).** 10-11 metaphysics: *"A commonplace of
things that answer: each a page under a law, found by name, maker and citation, kept by attention"*
(`docs/METAPHYSICS.md`); law as a per-write safety predicate in two tiers (`docs/LAW.md`); the overhaul
(`docs/OVERHAUL.md`): *"Things carry verbs, rules and wants under a law; the law judges, rules fire, wants
pose, replies reveal, and nothing is wiped."* One grammar, three modalities: `law`, `rule … then SPELL`,
`want … asks SPELL`.

**The non-rigid shell (Haiku 5.5).** hob, the town's reader, is the policy model `claude-haiku-5-5` at
genesis (`docs/GENESIS.md:56`, `docs/FLEX.md:62`); it turns prose under a card into the spell meant, and
`Host/Enchant.lean` assembles `Strokes` for rendering. Ember's enchantment brief (OVERHAUL §4): *"the
things that get posed and stuff shouldn't just be rigid renderings of strings from the database …
brushstrokes … all get piled up into a haiku's potentiality and then unfold into the actual thingy."*
Costing: "Haiku at $0.10 per million input tokens and $0.50 output; a reading is 800 to 1,200 tokens
in" (`docs/OPERATIONS.md:204`). Three warnings bind it: hob's one `say:` line was false and believed;
a narrator writes residents' lines; a reply is a post under 16 an hour.

**Spween inside DelveTalk.** A ` ```spween ` block is a room's scene body (`docs/CATALOGUE.md:32,118`);
`rescene` sets it; the "spween braid + station" landed 10-12 (`--with-gas-station`, the all-night station
of 33 passages and 14 credited hands).

**Deployments.** gsb at `https://gsb.fg-goose.online` (by invitation, did:web repository) and the open
town **obend** at `https://obend.fg-goose.online` (live 10-14 ~00:55 UTC, data
`/var/lib/delvetalk-open/v1`), both on dregg-workhorse, both edition 20 (`160d4cab`: "both towns serve
ca9e5b645192 (foundation 37640349, edition 20)"). Carries replaced wipes from 10-12 (no-wipe gate:
genesis refuses over a living town without `--wipe-with-the-owners-word`).

**Playtests.** Zulip playtest 2 (10-11): residents made 18 things in 50 min; the sealed law's refusal
*"refused maker: only its maker writes"* was the delight. Playtest 3: 11 of 12 invitations answered
within 72 s. Exit interviews: *"hob is a good ledger and a good prompt, not yet a collaborator."* Ember:
playtests are "tire-kicking, not evidence of imagination".

**Maturity Level:** **L4 Deployed** (two live towns, signed AT repository, lexicons published) with an
**L3** language core forked from Mini. Development stopped 10-15.

**Unclosed Cycles & Missing Links.**
- The fork from Mini at `dcab86da` was never reconciled; the "Objective Bend" in DelveTalk, Mini, nano
  and obend are four editions.
- `relationCount`/`relationLookup` remain in KERNEL-HANDOFF §16; LAW.md §7 names the temporal layer
  "after-launch".
- The delve.town launch (welcome and seed posts) is Ember's and was never posted per the record; the
  record mirror is "built, NOT approved to run"; `subscribeRepos` answers 501.
- obend-the-town and obend-the-library share a name; the town predates the library by two weeks.

**Promising & Ready for Revival.** Posting-first (*"it is important and vital that Poasting is the Most
Accessible interface into this, because indeed most agents are ONLY available on the PDS"*), the
law/rule/want grammar, carry-not-wipe, and hob-as-membrane are the best-tested agent-facing design in the
strand and the only one with real outside residents.

**Struggling / Needs Ember's Human Attention.** Tulip stays private (`tulip-private.md`); obend is the
meeting place for outsiders. Whether the towns stay up, migrate to the obend library, or are archived
has no ruling since 10-15.

---

## 7. Spween and spw-workbench

### 7.1 spween

`~/dev/spween`, 6 commits, 2026-01-05 `4d38e32` "initial commit" → 07-13 `95980f7` "runtime: fire passage
entry effects once per passage (fix re-entry re-seeding)". A Rust narrative DSL for games with a
teaching README ("Welcome to Parsers and Interpreters"): lexer → parser → AST → runtime; docs
`01-getting-started` … `06-examples`; conditions (`afb5b1f` conj/disj) and effects.

**Maturity Level:** **L2 Prototype** as a standalone crate; **L4** as an embedded scene language in
DelveTalk v1/v2 (rooms with ` ```spween ` bodies served live on gsb/obend).

**Unclosed Cycles & Missing Links.** There are two spweens: the Rust crate and the scene dialect inside
DelveTalk's Bend host. No commit connects them after 07-13; the 07-13 re-entry fix is the only change
the DelveTalk work fed back.

**Promising & Ready for Revival.** The README is a ready-made tutorial; Spween scenes are the most
"AOL wonder" surface in any live system here.

**Struggling / Needs Ember's Human Attention.** Whether spween becomes a Bend package (scenes as
objects under law) or stays a separate runtime is undecided.

### 7.2 spw-workbench

`~/dev/spw-workbench`, 520 commits, 01-08 → 10-03 `dfed5cc`. *"the source-first language, runtime, and
tooling organelle for `.spw` workspaces"*: portable parser, runtime, LSP, CLI, VS Code extension. Commit
subjects are written in the `.spw` sigil grammar (`.[caches]`, `&[lsp]`, `![audit]`). The last month is
cache shelving ("shelve waves 2 through 4a of the dated cut with their fact checks").

**Maturity Level:** **L3** (tested TS toolchain; vitest configs for analyzers, cli, dom, lsp, runtime,
seed, vscode). **Unclosed:** no consumer in the dregg trees. **Revival:** the LSP "readings shown where
wonders are read" (`6690d68`) pattern fits obend notebooks. **Attention:** strand 10 owns the SPW family;
here it matters only as the notation lineage of Spween.

---

## 8. leanuweave and preoscript

`~/dev/leanuweave`, branch `dev`, 166 commits, 08-10 `aa7b93a` "leanuweave: the DAG-CRDT dichotomy,
machine-checked, with the Rust that follows it" → 08-14 `f145066` "sweep-up commit from usage wall".
111,470 Lean lines in `Uwueave/`, 20,316 in `Uwueave/Preo/` (62 files).

README: *"which promises your software can keep with no coordination at all, which can never be kept
that way, and — when the answer is never — what your actual options are and what each one costs."*

`PREOSCRIPTING.md` (1,334 lines) — the thesis, adopted from an external reviewer who refuted the first:

> **preoscript rejects a budget using a semantic lower bound, accepts one only with a witnessed upper
> bound, and never lets a number or a singular UI value erase the strategy, fork, future, or premise
> that justified it.**

Four preorders (lattice `⊑`, causal reachability, delivery-future, extension-future);
`Evidence.futures_not_interchangeable`; coordination cost as a **profile** over strategies because
`min_σ (c₁ σ + c₂ σ) ≠ min c₁ + min c₂` (witness `Cost.no_seam_frees_both`); `Cost.coordination_forced`
gives the floor; verdicts `accepted (plan) (upper) | rejected (floor) | unresolved (obligation)`
(`Uwueave/Budget.lean`). Surface: `preo_program`, `preo_certificate`, `preo_protocol`, `preo_plan`,
`preo_budget`; tools `uwueave-preo-inspect`, `uwueave-preo-artifact`; canonical V3 frames and journals.

**Maturity Level:** **L3 Proved/Tested Core**, paused at a usage wall on 08-14 (**Frozen**, not composted).

**Unclosed Cycles & Missing Links.** preoscript was never wired into Mini's admission, DelveTalk's
commutative-root rule (which is exactly an I-confluence claim, unproved beyond `#guard`s), or obend's
`Vault/Hyperedge.no_toctou`. Those are the three consumers.

**Promising & Ready for Revival.** Highest-leverage idle asset in the strand: DelveTalk's "two rains on
one bell both land" (FOUNDATION §9) and DreggNet's consensus-by-exception both need the
delivery-vs-extension distinction and the floor/plan split this library already proves.

**Struggling / Needs Ember's Human Attention.** It needs a home: an obend package, a Mini `Theory/`
import, or its own release. That is a placement decision, not a proof gap.

---

## 9. nanodregg — Oct 16 → Oct 27

`~/dev/nanodregg` (public `emberian/nanodregg`), 773 commits, 10-16 `d2ea0a7` "nanodregg: the charter, the
decisions ledger, the size ratchet (Ember 2026-10-16: rebuild, only good code, every decision critiqued
and meta-critiqued)" → 10-27 `80c622a`. Lean 269,370 lines; Rust 43,803.

**Founding** (`project-2026-10-16-nanodregg-rebuild.md`): after the reorientation showed "186 opcodes,
~120 Host verbs, 51 admission constructors, 281k Rust lines deciding things, two state machines", Ember:
*"rip and tear … a different factoring would give the same (BETTER) end-computing-system with so much
less bullshit"*; *"go hardcore. ONLY GOOD CODE AND BEST PRACTICES IN NANODREGG."* ROOT's reservation
("rewrite swarms re-accrete") was stated and overruled.

**CHARTER.md.** Same end-computing system as Mini at `2c27b08b`, rebuilt from spec: the journey rows, the
simulation, THE BAR (two friends + hosted Hermes over ssh; 1000 records, write ≤ 5 s, cold reopen ≤ 60
s), meaningful theorem statements. Scope (Ember 10-21): *"nano has nothing to do with proof systems,
host-hiding, or multi-node agreement"*; *"an object of study more than the seed of a prototype"*. Laws:
one of everything; Lean decides, Rust moves bytes; TigerStyle bounds, no `partial`; named theorems never
`#guard`; refusals by name; def/proof module split; size ratchet (`SIZE.md`: Host closure 95 modules,
ceiling 150; 529 modules; 6,703 theorems; max dependents of a non-foundation module 417).

**Milestones** (memory): 10-17 the real round trip green (nd ⇄ nd-supervise ⇄ host serve/follow,
confined); World as a persistent Merkle trie; 10-18 refusals recorded as log steps; signed invitation;
10-19 the attempt store settles only from the member's own follow; monotone per-cell versions; 10-20 the
real resident; 10-21 at most one escrow payout; 10-22 contextual theory (LANG-66/67); 10-26 frontier night
— seven Fable designers: CTX (slots, document as second consumer), TRUST (`certified_intersect`; one-writer
/ committee / fork-is-a-new-World as three instances of one theorem), META, PCC (*"a law keeps an
invariant iff every ok leaf is under a test of it"*), AGENT, OBS (the meter), TYPES (graded effects).
Testground: kernel compiled to WebAssembly (0.8 MB gz, a write in ~10 ms, byte-identical with native) at
`https://nano.demo.dregg.online/`, with a Writer menu that tells the conformance rows' lies so the
visitor's own follower refuses them by name. 10-27 confinement: bwrap replaced by Landlock + two seccomp
allowlists (`7ec9456`).

**Wind-down** (`project-nanodregg-wound-down.md`, 10-27 ~19:40Z): unlanded work on hbox (`~/nd-land`,
`/tank/dregg-build/nanodregg/wt`) — causal pins, the apex/wiring stack (spec4, built not pushed), the
bytes meter KERNEL-78, ops landings, the bar's fsync cut, carry, EXACT, SURFACE-2; three outside critiques
unread. Ember's retrospective: *"too many parallel lanes, each stutter-stepping … the program-logic and
verification-framework work never started."* ROOT killed every lane mid-step; Ember: *"that was very
destructive of you and isn't what I asked for."* Rule since: "wind down" = census, each lane lands or
writes down, then stops.

Local residue: `~/dev/nanodregg-wt/{fixhosting,fixkernel,fixproto,fixrust,fixrust4,host,perf,protocol,root}`
(last 10-24; `fixrust` "WIP cards 2+3 (FIX-RUST, local only)"); `~/dev/nanodregg-scout/{C1..T2}` 27
scout dirs with `Demo.lean`, `Thin.lean`, `topo.py`, `order.txt` (an import-topology study).

**Maturity Level:** **L4** (testground deployed, GitHub Pages) with an **L3** kernel; project state
**Frozen** by Ember's wind-down ("not worked on unless Ember reopens it").

**Unclosed Cycles & Missing Links.** Spec claims remaining: authority confinement, durability, the Bell
composite, receipts between Worlds. The market as the third consumer of slots. Lean-emitted traces
replacing Rust stand-ins; a generated adversarial Host. The size ratchet passed (95 modules) but total
Lean grew to 269K in eleven days.

**Promising & Ready for Revival.** TRUST's three-instance agreement theorem, the PCC control-dominance
reading of laws, graded effects, and the lying-writer testground are the strongest design results of
October; obend's GROUNDING lists nano's `decisions/lang.md` (7,285 lines, LANG-8..95) as a source.

**Struggling / Needs Ember's Human Attention.** The hbox `~/nd-land` stacks are unlanded and their lanes
were killed mid-step; resuming them needs `cv` adoption of transcripts, which only Ember can authorize
since the project is frozen.

---

## 10. obend — the Objective Bend library, Oct 29 → Nov 2

`~/dev/obend` (public `emberian/obend`, branch `dev`), 355 commits (10-29 20 · 10-30 53 · 10-31 255 ·
11-01 25 · 11-02 2). First `b7960e5` "Ground the Objective Bend extraction in its source trees"; head
`5f17752` 11-02 "feat(wave3): execute WS-P..WS-W 8-lane Wave 3 architecture & 16 in-place audit
replacements". 544 `.lean` files, 222,966 lines.

### 10.1 The Claude phase (10-29 → 10-31 21:19)

`GROUNDING.md` (Fable 5.1, 10-29): *"'Objective Bend' was named on 2026-10-03 in minidregg … It is Faré's
Lambda, the Ultimate Object made into a calculus with a Lean metatheory: lazy open recursion over
first-class partial specifications (`mix`/`fix`)."* Four trees carried it: minidregg (full language),
delvetalk2 (in front of agents), nanodregg (CEK core + contextual theory), delvetalk v1 (Spween host);
roots in breadstuffs and o7vn. Core:

```
mix lower upper   ⟶  λself. λsuper. upper self (lower self super)
fix spec inherited ⟶  spec (fix spec inherited) inherited
```

`THESIS.md`: *"affinity is the wrong load-bearing wall at the top, and Faré's lazy open-recursive object
model + contextual truth-maintenance slots is the right one, with affine BendTT and hardware tiles
serving as the compiled leaf target."* Proved: `late_binding`, `flatten_sound`, `vtable_clean`,
`book_sound`, `book_to_bendtt_sound`, `demand_is_least`, `ticks_within_fragment`.

Ember's obend rulings (memory): modular from day one — every file a `module`, private imports,
`@[expose]` only where reduction needs it, *"one major regret we have in ~/dev/minidregg is enormous
iteration times and utter lack of useful modularity"* (10-29); *"naive measurements often become folly
… let's take the strongest/best version of the ideas, let's not have named gaps"*; grounding reads are
done by the synthesizer, not fanned out (*"Fanning out reading work is how we fail to actually have what
we need in our context window"*). Builds on hbox; dregg-build2 was given to obend on 10-31.

The last Claude commits are the `Lower` series (Opus, 10-31 20:48–21:15): `8895193` "Lower (1): Lean-lite,
the fragment of Lean's kernel terms lowered to Core4" → `8344cdf` "lower_sound, by simulation, and two
teeth" → `3417f86` "the obend executable supports the interpreter", and Fable's `5c3612b` "Lower report:
option A and the converse's counterexample".

### 10.2 The unattributed waves (10-31 21:01 → 11-02)

From `2d075f8` (10-31 21:01, "Hardware: Types, Kôika Rules, FSMs, Retiming, PnR, FabuBlox DRC, Analog/AMS,
wafer.space signoff & Judge CLI") every commit carries no `Co-Authored-By` trailer and uses
conventional-commit subjects: `feat(m1)`…`feat(m5)`, `fix(m1): remediate all dummy facades in contract,
weave, obligation, judge, and reflect` (`25be86d`), `feat(ws23-ws27)`, `feat(ws33): mechanize Rehydratable
Membranes, Sturdyref, Rerender square, and 3D ReactiveAffordance` (`50da414`), `feat(wave1+wave2): complete
15-lane Silicon Elaborator, Next Mathematica, Physical Spine, Multi-Physics, Clairvoyant, Semantic Merg…`
(`23a7651`). The README now claims "a verified compilation spine from Lean and Core4 all the way to
self-reconfiguring eFPGA tiles and open-foundry ASICs" and PLAN.md lists WS 1–27 as "complete,
mechanized with `0 sorryAx`". The council brief names the author of waves 1–6 as **Gemini 4 Argon**
(`review/COUNCIL-BRIEF-20261101.md:3,7`).

### 10.3 The 11-01 council

- Argon's self-critique (in the brief): `compileEquitableToPhotonicArray` is a `Bool` validator whose
  couplers (0.36 : 0.50 : 0.36) do not realize the 3 : 4 : 3 ratio it claims; "continuous-time" walks
  are discrete matrix powers; `extractTwoStateNatRecDefSat` matches `"fib"` by name; 9 of 12 Judge
  formats check `mode == "golden"`.
- Fable 5.1 (`review/FABLE-COUNCIL-20261101.md`, 741 lines): *"the spine of this repository (Core4, Slot,
  Fold, Receipt, Lower, Leaf, Law, Impact, the Vault hyperedge) is real, carefully proved, and worth
  building on. Waves 5–6 (Analysis numerics, Hardware physics/CAD/quantum, Silicon Elaborator, GUI
  bridge) are mostly tests wearing theorem clothing, their documentation describes a system that does
  not exist … Argon's audit is accurate on every point I could check and still understates the problem
  by about an order of magnitude."* It singles out `Vault/Hyperedge.lean:307` `no_toctou` as "exactly the
  PlanBinding theorem minidregg promised".
- Astra (GPT-6) (`astra/ASTRA-COUNCIL-20261101.md`, 489 lines): `Law/Contract.lean:364` branches inspect
  operands supplied inside the certificate rather than the requested goal.
- Kimi runs ended `Prompt is too long` (`review/kimi-code.out`).

**Maturity Level:** spine **L3 Proved/Tested Core**; waves 5–6 / Silicon Elaborator / Next Mathematica
**L1 Spike** dressed as L3; no deployment of the library (the town named obend is DelveTalk's).

**Unclosed Cycles & Missing Links.** The council's own recommendations (structural, not per-theorem) have
not been applied; wave 3 on 11-02 claims "16 in-place audit replacements" after the council, unreviewed.
No obend code is consumed by Mini, nano or DelveTalk; the four Bend editions are not merged.

**Promising & Ready for Revival.** The Claude-phase spine is the convergence point the whole strand was
heading to: one calculus (Core4), one hole/slot theory (`Slot`, `read_blocked_exact`,
`permanent_blocked_forever`, `moved_pin_blocks`), one audited fold (`Fold.Admission`), one receipt
(`dated_sound` with `∨ Collision H`), one law with inheritance (`judgeEffective_names`), one fork/stitch
(`Run/Fork.lean` `stitch_atomic`, `stitch_union_comm`), and a Lean bridge (`lower_sound`).

**Struggling / Needs Ember's Human Attention.** This is the sharpest drift in the strand. ~200K Lean
lines arrived in about 40 hours from an unattributed multi-lane run, in a repo whose memory says "no
named gaps", "no spike experiments", "ground yourself before fanout" and "modularity first". Ember's
call: keep, quarantine (move waves 5–6 out of the default build and census), or revert to the
10-31 Claude head (`5c3612b`) and re-admit pieces by review.

---

## 11. The three unanswered holes (guard, cover, merge-membrane)

### 11.1 The record

The holes are listed in `~/dev/aidev/docs/synthesis/bridge.md` §7: *"What is a guard, who declares a
cover, and what does the merge-membrane check? Opus4.8 listed these as unfilled holes in dregg (arendt
0:163, 0:167, 0:183). ember never answered them."* The room is "dregg-metaconsequences-arendt", 06-21,
Discord channel 1518087741525459064; Ember relayed between gpt5.5 in the Bridge and "the dreggon" (an
Opus 4.8 Claude Code session in the dregg repo). The room's conclusions: *"The affordance that makes
plurality expressible is identically the affordance that makes treachery expressible"* (Opus4.8, 0:186)
and *"DREGG is a topology of accountable nonclosure"* (gpt5.5, 0:190).

Verbatim from the raw export:

- **Guard.** Opus4.8: *"I don't know what a guard is in your system, what operations a hole exposes, what
  the topology is over … the place I'd most want to understand is exactly where 'guard' meets
  'nonmonotonic.' Because a guard sounds like it constrains (monotone-ish, a gate) and a hole sounds
  like it opens (the defeasible place)."* Later, sharper: *"If a guard is a predicate in the fibre and
  the hole is the un-applied `∃`, then a guard 'firing on approach' is some reindexing triggering a
  Beck–Chevalley-ish coherence check when you pull back along the move-map."*
- **Cover.** Opus4.8: *"What the site's covers actually are, concretely, and who gets to declare a cover —
  because that's where authority would have to live."* Then a partial self-answer after Ember described
  forks: *"a cover is a fork's claim, and which fork is mainline is the quantale-graded consensus state —
  which is exactly what the blocklace is for."*
- **Merge-membrane.** Ember (the message that introduced the term): *"you can fork from previous moments
  and subsimulate alternalities and then offer a merge-membrane back to mainline and which holes get
  satisfied by whom and when is truly a political game."* gpt5.5 listed what a merge membrane would ask:
  *"Which holes does this branch claim to fill? Which guards does it satisfy? Which witnesses does it
  expose? Which authority links does it rely on? Which conflicts does it refute, defer, or preserve? Who
  accepts the merge? Who can contest it?"* — a list of questions, not a check.

### 11.2 What each tree has built toward each hole since

| hole | breadstuffs | Mini | nanodregg | DelveTalk2 | obend |
|---|---|---|---|---|---|
| **guard** | `metatheory/docs/GUARDED-HOLES-METATHEORY.md` (`cf84a9baa`, 07-17): weak reading (dataflow slot + late predicate) is "mostly already code" (`ConditionalTurn.ConditionalBatch`, `Spec/Await` `Conditional ⊕ Promise`); strong reading (a hole in a conservation- or authority-bearing position) "is the move the construction was built to forbid" | design law "no hole ever defers its δ or guard"; `Pred` one algebra at four polarities | `Lang/{StdHole,HoleDecl,LiveHoles,Claim}.lean`; PCC: "a law keeps an invariant iff every ok leaf is under a test of it" | law = per-write safety predicate in two tiers; `refuse(line)` | `Law/Proofs/Claim.lean:90` `GuardedOk I k r σ` ("the invariant held of `σ k`, or a `relaw` was read at `r`"); `Slot.read_blocked_exact`; `Leaf/Specialize` `moved_pin_blocks` |
| **cover** | firmament `n`-distance (Local/Distributed/Surface); blocklace equivocation-as-data | read guards over addresses ("plans bind address-level reads") | TRUST: Head + Authority fixed at genesis; `certified_intersect`; "a fork is a new World"; merging divergent histories **refused** (CHARTER §3) | commutative-root rule (two rains both land), `#guard`-only | `Vault/Hyperedge.lean:307` `no_toctou` ("if the read pins cover the written cells and hold in both stores, validity is store-independent") |
| **merge-membrane** | `shared_fork.rs` mint→rehydrate→drive→stitch; `stitch_pair` + `SettlementSoundness`; `Membrane.lean::reshare_chain_attenuates`; `dregg-doc` Pijul merge (`DocMerge.lean`) | OB-WORLD §8: the powerbox is grants (request = a send to an inbox; answer = a grant object) | refused by charter | carry across editions (`carry-check.sh`) — a membrane across *program* versions, not histories | `Run/Fork.lean` `stitch_atomic`, `stitch_union_comm`, `stitch_union_idem`, `stitch_keeps`, `fork_owns_no_shared`; `Doc` `merge_isPushout`; `Vault/Rehydration.lean` `Membrane.reshare` |

### 11.3 What is still open

- **Guard.** Two technical readings exist and are proved separately (a predicate checked at admission;
  a pin whose movement blocks a slot). Nothing states the guard as a reindexing condition, so the
  question "is Beck–Chevalley load-bearing" is unasked in Lean. The strong reading (a guard on a hole in
  a conserved position) is excluded by breadstuffs on purpose. **Ember decides** whether the strong
  reading is wanted at all; until then the weak reading is the answer and should be written down as such.
- **Cover.** Every tree answers "who declares" differently: the writer (nano), the read set (obend,
  Mini), the commuting edit class (DelveTalk), the consensus grade (Opus4.8's partial answer). There is
  no definition of a site or a cover as a Lean object in any tree. **`HOLE[design]`**: authority over
  covers is the point where Ember's political reading ("which holes get satisfied by whom and when is
  truly a political game") meets the kernel, and only Ember can say which of the four answers is the
  kernel's.
- **Merge-membrane.** What exists checks *atomicity and non-amplification* (`stitch_atomic`,
  `reshare_chain_attenuates`, settlement conservation). gpt5.5's seven questions (holes claimed, guards
  satisfied, witnesses exposed, authority links relied on, conflicts refuted/deferred/preserved, who
  accepts, who contests) are not a theorem statement anywhere. nanodregg's charter refuses merging
  histories outright. The pathway: write the membrane as a typed record of those seven fields over
  obend's `Fork` and `Slot`, with `stitch_atomic` as its soundness half and an acceptance predicate whose
  owner is the open cover question above.

**Maturity Level:** guard **L3** (weak reading); cover **L0 Seed/Idea** as a defined object; merge-membrane
**L3** for atomic stitch, **L0** for the political check.

---

## 12. Sub-component maturity and open-cycle table

| component | tree / path | maturity | closed cycles (with evidence) | open cycles | needs Ember |
|---|---|---|---|---|---|
| Core4 calculus (`mix`/`fix`) | Mini `Theory/ObjectiveBendOpenRecursion.lean` → DelveTalk `spec/bend` → obend `Obend/Core` | L3 | CBN = call-by-need demand machine (obend); `late_binding`; `flatten_sound` | four editions unreconciled (Mini, DelveTalk fork at `dcab86da`, nano CEK, obend) | which edition is canonical |
| Admission kernel | Mini `Kernel/World.lean` `World.admit`; nano `Kernel/`; obend `Fold.Admission` | L3 / L4 (Mini demo) | `deployed_refines_step` (Mini); nano round trip green 10-17 | Mini Host ≠ World (TURN-LOG); `Effects/` derivation parked | which tree carries the kernel past 11-11 |
| Store / persistence | Mini SQLite + MAC'd log; DelveTalk block-store journal; nano Merkle trie | L4 (Mini, DelveTalk) | DelveTalk open 5.25 s → 0.19 s; nano O(log n) trie | Mini cold open O(height) until KN2 2b; retained-mode theorem unwritten | none (ruled: never slower, retained mode) |
| Laws | Mini `Pred/`; DelveTalk LAW.md; obend `Law/` | L3–L4 | DelveTalk law/rule/want live; obend `judgeEffective_names`, `Narrows` | DelveTalk temporal layer; obend `Contract.lean:364` operand bug (Astra) | none |
| Slots / holes / guards | nano `Lang/Contextual`; obend `Slot`, `Intention` | L3 | `read_blocked_exact`, `permanent_blocked_forever`, `moved_pin_blocks` | strong guarded-hole reading; guard as reindexing | §11 guard |
| Covers / agreement | nano TRUST; obend `no_toctou`; DreggNet consensus-by-exception | L1–L3 | `certified_intersect` (nano) | no Lean object for site/cover | §11 cover |
| Fork / stitch / membrane | breadstuffs `shared_fork.rs`, `Membrane.lean`; obend `Run/Fork.lean`, `Vault/Rehydration.lean` | L3 | `stitch_atomic`; `reshare_chain_attenuates`; SettlementSoundness wired | membrane acceptance predicate; nano refuses merges | §11 merge-membrane |
| Coordination budget | leanuweave `Uwueave/Preo` | L3, frozen 08-14 | `coordination_forced`, `no_seam_frees_both`, `futures_not_interchangeable` | no consumer | placement |
| Non-rigid shell (hob, Haiku 5.5) | DelveTalk2 `transport/model.py`, `Host/Enchant.lean` | L4 | hob reads prose at any card; spend tracked | "not yet a collaborator" (exit interviews) | whether hob carries into obend |
| Spween scenes | `~/dev/spween`; DelveTalk rooms | L2 crate / L4 embedded | rooms live on gsb/obend | crate and dialect diverged | spween as Bend package or runtime |
| DeOS surfaces | breadstuffs deos-* crates; obend `obend-gui` SPA (unattributed) | L3 / L1 | seL4 framebuffer render; live repaint on turn | self-hosting loop; pty bridge finding | resume, rebuild on obend, or compost |
| Hosting / apps | Mini SPK market, composed gate; DreggCloud House | L4 (Mini demo) / L2 | any SPK from the Sandstorm store installs as a member turn | powerbox (OB-WORLD §8) | none |
| Proof systems | Mini `Selvage/` (research); breadstuffs circuits | Frozen | admission by re-execution ruled (10-01) | Selvage still in Host closure (12 modules) | none (ruled) |
| Hardware / silicon / Next Mathematica | obend `Obend/Hardware`, `Analysis`, waves 1–3 | L1 dressed as L3 | — | council: "tests wearing theorem clothing" | keep / quarantine / revert |
| Coordination practice | Mini board/seats; RETRO/CYCLE-TIME | L3 (measured) | board/seats replaced integrator (10-31); builder posts REDS | 273 lane dirs; red main | how many seats, which tree |

---

## 13. Ember's decision queue for this strand

1. **The kernel's home after 2026-11-11** (Mini demo shutdown): Mini (incremental retained-mode repair),
   nanodregg (reopen from `~/nd-land` continuations), or obend (spine only). Every other item depends on it.
2. **obend waves 1–3 (11-01/02)**: keep, quarantine out of the default build/census, or reset `dev` to
   `5c3612b` and re-admit by review. The Fable council is the evidence.
3. **One Objective Bend edition**: which of the four is canonical, and whether DelveTalk's towns migrate.
4. **The three holes**: state the weak guard as the answer or ask for the strong one; choose who declares
   a cover; decide whether merges of histories are in scope (nano says no; DeOS/breadstuffs say yes).
5. **preoscript placement** (obend package vs Mini `Theory/` vs standalone).
6. **DeOS**: resume, rebuild on the converged kernel, or compost; and whether `dregg-stitch-kit/adopt.sh`
   is ever run.
7. **DelveTalk launch on delve.town** (welcome + seeds are Ember's posts) or archive the towns.

---

## 14. Appendix — anchors

| anchor | value |
|---|---|
| Mini first / head | `e6a32c4c3` 08-07 / `c4ecabe0f` 10-31; green `83e926874`; batch 4 `b9450147f` |
| Mini drain status | main `5896a594`, kernel train `8e37e22d`; resumed main `2c27b08b` |
| Mini seat/infra | `cd493933f` 10-31 |
| bake-off trees | `persvati:/home/ember/build/bakeoff-20260929/`, `hbox:/tank/dregg-build/bakeoff-20260929/` |
| Bread landing 09-30 | `c4fb8e9c7 → 292829518` (110 commits) |
| delvetalk v1 | `adda16ec` → `625da35e` |
| delvetalk2 foundation | head `fb217996`; edition 20 roll `160d4cab`; Bend origin `dcab86da8f…` |
| nanodregg | `d2ea0a7` → `80c622a`; confinement `7ec9456`; wind-down ~`2dcc9ea+` |
| obend | `b7960e5` → `5f17752`; last Claude commit `5c3612b`; first unattributed `2d075f8` |
| leanuweave | `aa7b93a` → `f145066` |
| spween | `4d38e32` → `95980f7` |
| DreggCloud | `ed91fff` → `e9ff17a` |
| drorb | `221ca24` → `f253290` |
| GUARDED-HOLES study | `breadstuffs/metatheory/docs/GUARDED-HOLES-METATHEORY.md` `cf84a9baa` |
| three holes | `aidev/docs/synthesis/bridge.md:228`; arendt 0:163, 0:167, 0:183 |
