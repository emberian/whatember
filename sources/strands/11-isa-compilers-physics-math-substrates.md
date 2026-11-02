# Strand 11 — ISAs, Compilers, Formal Mathematics, Physics & Frontier Substrates

> Primary-source dossier. Compiled 2026-11-02 from the repos under `/Users/ember/dev/`, their
> `git log`s, and the agent memory files under `~/.claude/projects/*/memory/`. Every number in this
> file was read off a README, a commit message, a memory file, or a `wc`/`git rev-list` run on
> 2026-11-02. Where a claim comes from an agent's own memory rather than a re-run, it is marked
> *(memory)*. Nothing here was rebuilt or re-proved for this dossier.

---

## 0. How to read this strand

### 0.1 Ownership legend

The vertical as briefed mixes four very different kinds of directory. Treating them alike would
overstate what is Ember's. Every project below carries one of these tags:

| Tag | Meaning |
|---|---|
| **OWN** | Ember-authored (alone, or with agents working for Ember). |
| **CO** | Co-authored with a named human collaborator. |
| **CONTRIB** | Someone else's project; Ember contributed reviews, PRs, issues or a formalization layer. |
| **MIRROR** | Upstream checkout kept as a build substrate or reference. No meaningful Ember authorship. |

`/Users/ember/hellas` code is **not** claimed anywhere in this strand. It appears once, as an
external dependency that graphplay planned to target (catgrad, §3.1.7).

### 0.2 Maturity scale (used in every section)

`L0 Seed/Idea` · `L1 Spike` · `L2 Prototype` · `L3 Proved/Tested Core` · `L4 Deployed/Production` ·
`Frozen-for-Rethink` · `Compost/Superseded`

### 0.3 Privacy redactions in this strand

`whatember` is published at `emberian.github.io/whatember`. Three sources in this vertical contain
material that must not go there, and this strand **deliberately omits** it:

1. `~/.claude/projects/-Users-ember-Documents-Nebula-Genomics/memory/`: personal whole-genome and
   medical analysis. §5.10 covers only its methodology lessons.
2. `~/.claude/projects/-Users-ember-dev-dgem/memory/dgemma-deploy.md`: contains a **live API key and a
   Pulumi passphrase in plaintext** (see §5.4, human-attention item H-1).
3. `~/dev/qaa/SECURITY-FINDINGS.md`: vulnerability details for a third party's server, assessed with
   the owner's consent. Only its existence is recorded here.

---

## 1. Executive map

| # | Project | Path | Tag | Commits | Active span | Maturity | One line |
|---|---|---|---|---|---|---|---|
| 1 | absass | `~/dev/absass` | CO (Grissess) | 157 (88 ember / 69 Grissess) | 2022-06-26 → 2022-09-16 | L2 → Frozen | "ABSOLUTE ASS": 16-bit word-size-agnostic RISC ISA, 3 HDL cores, Rust emulator, C-like compiler |
| 2 | RISC-V custom-instruction spike | `~/dev/silicon` | OWN (spike) | untracked | 2026-02-20 | L1 | 8 custom instructions (LVB, BLAKE3 co-proc, VATCALL/CAPTRAP traps), Sail + Spike |
| 3 | gamevm | `~/dev/gamevm` | OWN | no git | 2026-01-05 | L0 | 3,110-line plan to turn Blackwing into a schema-driven game VM |
| 6 | ergolang | `~/dev/ergolang` | OWN | 2 | 2025-12-17 | L1 | "Programs as Sheaf Sections", an 834-line Prolog interpreter |
| 7 | velato | `~/dev/velato` | CONTRIB | 91 (1 ember) | 2023 → 2026-03 | upstream L4 | Linebender Lottie renderer fork; **misfiled**, it is not a language |
| 9 | bend | `~/dev/bend` | MIRROR | 3,416 | — | n/a | HigherOrderCO Bend; referenced by stella's README |
| 10 | rustc.js | `~/dev/rustc.js` | OWN | 0 (README only) | 2025-08-24 | L0 | A 207-byte README that names an API |
| 11 | serde-reflect | `~/dev/serde-reflect` | OWN | 4 | 2024-01 | L1/L2 | Runtime type DB replacing monomorphized serde |
| 12 | thy-of-ocaml + polyml `TranslateOcaml.sml` | `~/dev/thy-of-ocaml`, `~/dev/polyml/mlsource/MLCompiler/TranslateOcaml.sml` | OWN (untracked) | fork 1,202 (0 ember); file untracked | 2024-03-25 | L1 | SML→OCaml translator inside PolyML's compiler (612 lines) |
| 13 | FStar / CakeML / HOL / candle / polyml | `~/dev/*` | MIRROR (+ local patches) | 36K / 26K / 22K / 800 / 5K | — | n/a | The HOL4/CakeML/Candle substrate for stella and svenvs |
| 14 | reu_unif | `~/dev/reu_unif` | OWN | 8 | 2015 → 2023 | Compost | NSF-EPSCoR REU unification code (Rust) |
| 15 | **graphplay** | `~/dev/graphplay` | OWN | 93 | 2026-05-28 → 06-10 (+ 06-14/15 experiments) | **L3** | Equitable-partition quotient of quantum walks in Lean 4; sorry-free; ε-equitable attention |
| 16 | **birkhoff-asa ("asagolf")** | `~/dev/birkhoff-asa` | OWN | 200 across all refs; origin/main 123 | 2026-05-15 → 05-17 | **L3** (+ live site) | Exact, kernel-checked size of ASA/SAS down to ZFC; Books Two/Three: SDG and gauge theory |
| 17 | navier-stokes-proof | `~/dev/navier-stokes-proof` | CONTRIB | 12 on main (+3 branches) | 2026-08-15 → 08-17 | L2 (formalization layer) | Found the viscous-term erratum in Cambria's NS paper; 978-theorem community Lean layer |
| 18 | soundcalc-lean | `~/dev/soundcalc-lean` | MIRROR | 163 (0 ember) | 2026-06 → 08 | upstream L3 | symbolicsoft's Lean port of ethereum/soundcalc |
| 19 | intmat → intmat2 | `~/dev/intmat`, `~/dev/intmat2` | OWN (intmat codex-built) | 174 / 55 | 2026-10-14 → 10-16 | intmat Compost; intmat2 L2 | "Interior": evolving-matter alife in Julia. **Not** integer matrices |
| 20 | intmat-handoff | `~/dev/intmat-handoff` | OWN (archive) | no git | 2026-10-16 | archive | Extracted codex thread + original ChatGPT brief |
| 21 | rhaposPDE | `~/dev/rhaposPDE` | OWN | no git | — | L0 | "a love letter to differential equations", a one-line README |
| 22 | pauli-Group/Hegemon | `~/dev/pauli-Group/Hegemon` | MIRROR | ~1,100 (0 ember) | → 2026-03 | n/a | Pauli Group's PQ shielded-payment chain |
| 23 | reu / bead-calculus | `~/dev/bead-calculus` | OWN | 13 | 2025-12-29 → 30 | L1 | String diagrams as marble machines (puzzle game) |
| 25 | **stella** (+ stella-suite worktree) | `~/dev/stella` | OWN | 252 (suite branch 139) | 2026-05-15 → 05-19 | L2/L3 core; HOL track scaffolded | Girard's transcendental syntax as a substrate; 47.3K lines Rust, 7.4K lines HOL4 |
| 26 | spindle / RIG | `~/dev/spindle` | OWN | 162 | 2026-05-15 → 05-20 | **L4** (playable, public) | A zero-G sport derived from one co-rotating-frame ODE |
| 27 | h ("h ghost") | `~/dev/h` | OWN | 268 | 2026-09-01 → 09-07 | L4 (models served/published) → mothballed | Falcon-H1 continued pretraining on Ember's library |
| 28 | dgem | `~/dev/dgem` | OWN | no git | 2026-06-19 | L4 (deployed; current status unknown) | Scale-to-zero DiffusionGemma on AWS via Pulumi |
| 29 | clairnets / GLaDOS (+ qwen38-probe) | `~/dev/clairnets` | OWN | 146 | 2026-06-25 → 06-28 (+ 08-25 probe) | L2/L3 | Verifier-gated reasoning "organ" grafted into OLMo |
| 30 | qaa | `~/dev/qaa` | OWN (capture) | 1 | 2026-10-04 | L2 | Local mirror of the "trash magic" PHP organisms |
| 31 | starmap | `~/dev/starmap` | OWN | 4 | 2026-02-09 → 14 | L1 | Interest/project embedding map |
| 32 | luteastress | `~/dev/luteastress` | OWN | 4 | 2026-02-08 → 10 | L2 (study done) | Shared-stressor menstrual-synchrony simulation (Python + Rust ODE) |
| 33 | SauersML/group-approximation | `~/SauersML/group-approximation` | CONTRIB | (Ember commits 2026-09-07) | 2026-09-05 → 07 | upstream L3 | Non-MF groups paper; Ember reviewed and contributed GGT Lean |
| 34 | Nebula-Genomics | `~/Documents/Nebula-Genomics` | OWN (private) | — | 2026-05 → 08 | — | **Redacted** (§0.3) |

**Missing from disk:** `~/dev/clairnets-qwen38-probe` does not exist as a separate repo. The
project lives at `~/dev/clairnets/qwen38-probe/`; only its Claude project directory is separate.

---

## 2. The through-line: "proposer, then checker"

Read as one corpus, the strongest projects in this vertical share one architectural move.
**Untrusted cleverness proposes; a small trusted checker disposes; the measurement is what remains
after the checker.** The pattern shows up in five independent repos:

```
                  ┌───────────────────────────────────────────────────────────────┐
                  │   UNTRUSTED PROPOSER            SMALL TRUSTED CHECKER         │
                  ├───────────────────────────────────────────────────────────────┤
 graphplay        │ trained LDT net / any solver →  checkedSolve_sound (Lean)     │
 clairnets/GLaDOS │ neural narrower, learned α   →  verifier-gated reduced product │
 birkhoff-asa     │ refine/Prover search, agents →  src/kernel.rs (zero-diff)      │
 stella           │ iex_fast, unify_fast, tabling → reference `iex` differential   │
                  │                                  oracle (byte-identical)        │
 soundcalc-lean†  │ Python float calculator      →  native_decide over exact ℚ     │
 navier-stokes†   │ prose PDE argument           →  89 + 978 kernel-checked lemmas  │
                  └───────────────────────────────────────────────────────────────┘
                                         † not Ember's repo; Ember contributed (NS)
                                           or tracks it as a reference (soundcalc)
```

Two consequences recur across the projects and are worth stating once:

- **Soundness is free and power is the science.** graphplay proves it in Lean
  (`checkedSolve_sound`, `id_sound_but_useless`). clairnets then re-measures it empirically:
  "SOUND for ANY policy — 0 unsound / 0 incomplete even under an adversarial policy" (`ffe2fae`).
  birkhoff-asa builds its whole prover UI on it: "engine proposes, kernel disposes … `src/kernel.rs`
  zero-diff throughout" *(memory: website-prover)*.
- **The bounded-width wall.** graphplay's `acStep_xor_sound_but_abstains` predicts that local
  deduction cannot cross affine/XOR constraints. Five weeks later, clairnets hit exactly that wall at
  scale and nearly misread it as a failure (`d2bc512 RE-GROUNDING: I misread Finding 3 — the
  bounded-width abstention is the LDT theorem, NOT a failure`). This is the cleanest cross-repo
  closed loop in the strand. A machine-checked theorem caught an empirical misreading.

---

## 3. Part I — Custom ISAs, VMs and silicon

### 3.1 `absass` — ABSOLUTE ASS (CO, with Grissess)

**Problem it attacks.** A from-scratch, fully owned, toy-but-real computer: ISA spec, multiple
hardware cores, an emulator, an assembler, and a small compiler. The goal was to learn every layer of
a machine by building it.

**Primary sources.** `README.md`; `doc/isa-insn.txt` (16-bit), `doc/isa-insn-32.txt`,
`doc/isa-mult.txt` (long instructions), `doc/calling-convention.txt`, `doc/interrupt.txt`,
`doc/io.txt`, `doc/boot-record.txt`, `doc/ass.tex` (typeset spec).

Verbatim feature list (README):

> - A compact and uniform 16-bit instruction format
> - A pleasant RISC load-store design, we think, we're not really sure as while we are educated, we are still so ignorant.
> - Word-size agnostic. Want a 4-bit CPU? Go for it! 64 bit? Sure!
> - A suite of poorly-tested implementations that occasionally make their way onto an FPGA
> - A generalized bitwise instruction that can perform any of the 16 2-input boolean functions

#### 3.1.1 The ISA (from `doc/isa-insn.txt`)

| Major opcode `I[15:12]` | Class | Encoding notes |
|---|---|---|
| `0x0000` (whole word) | **Distinguished exception generator** | Clears SR2 bit 0, SR8 ← R0+2, R0 ← SR2, SR9 ← 1 |
| `0001` | Bitwise | `I[11:8]` = **truth-table number** (0 F … 6 XOR … 8 AND … 14 OR, 15 T). "this value can be treated as a LUT, using bits from D and S as indices" |
| `0010` | Arithmetic | `Si` immediate flag; ops Add/Sub/Shl/Shr/Asr/Rol/Ror/Neg |
| `0011` | Comparison | EQ/GT/SN/IV flag nibble → 16 predicates (AB, ABE, GT, GTE, NEQ, BLE, BL, LT, LTE …) |
| `01xx` | Data transfer ("XF") | Independent src/dst **indirect** bits plus 2-bit **increment modes** (none / auto-inc / pre-dec / post-dec), so push and pop are a single `XF` |
| `1000` | Conditional | Signed 8-bit offset in *instructions*; condition = register nonzero |
| `1001 1` | Subword ops | Subword size/index/sign-extend |
| `0xF 0x1` long form | Multiply/divide | 32-bit "Long Instruction" packet; `0x0` extension id, nonzero ids reserved for implementors |

The calling convention (`doc/calling-convention.txt`) is continuation-flavoured: R0 = PC (with a
built-in +2 per cycle that composes with auto-modification), R1 = SP, R2 = FP, **R3 = RC
"Continuation Address"**, R4–R10 args (caller-saved), R11–R15 temporaries (callee-saved). Push is
`XF *-SP, src`; pop is `XF dst, *SP+`.

Memory-mapped I/O (`doc/io.txt`): "every ass needs to fart sometimes." `TEXT0` is a 4-word
opcode/length/pointer/status device with busy and pending bits.

#### 3.1.2 Implementations

| Component | Path | Size | Language | Notes |
|---|---|---|---|---|
| SpinalHDL core | `spinal_ass/src/main/scala/mylib/` | 2,377 lines across `Ass.scala` (535), `Fart.scala` (410), `Uart.scala` (276), `RegAccess.scala` (230), `Nexass.scala` (175), … | Scala/SpinalHDL | `Nexass*` targets a Nexys board (`nexass/vvml.pdc`) |
| **Formal check** | `spinal_ass/.../AssFormal.scala` | 30 | SpinalHDL + SymbiYosys | `LogicUnitFormal`: BMC depth 10. Asserts the LogicUnit output equals the truth-table LUT lookup for every input (4-bit) |
| MyHDL core | `myass/ass.py` | 636 | Python/MyHDL | Renamed from `myhdl` (`b1a78d8`) |
| Rust emulator / disassembler | `assrs/src/{isa.rs,sim.rs,lib.rs}` + `machine.html` | ~380 | Rust | `06ee0b9 start updating assrs for new isa`, `825f8f6 working sim frontend` |
| Assembler | `assembler/` | — | MoonScript | Labels, `LI` aliases |
| **assc** compiler | `assc/src/{main.rs,grammar.pest,gen.rs,gen/}` | ~1,260 Rust | Rust + pest | C-like: declarations, expressions, `||`/`&&` precedence ladder, statements, branches, a calling convention, function declarations, and a register allocator (`gen::rall::{RAlloc, RaCx}`) |
| FTDI bring-up | `fart/` (`ftdi-rs`), `ardufart/ardufart.ino` | — | Rust, Arduino | Host-side serial to the FPGA core |

Git arc (oldest first): `31a8b46 ABSOLUTE ASS` (ember, 2022-06-26) → `394c90b Add the initial
documentation on the ISA` (Grissess) → `fbccaf7 implement logic unit` → `53914fd tests pass` →
`7e96e48 time to refine the ISA` → `dbb77f9 update assembler for new ISA` → `a4aefc9 assc: Add
statements, branches, etc.` → `8e779e8 assc: Add calling convention` → **`4d960df assc: Add
function declarations`** (Grissess, 2022-09-16, HEAD).

- **Maturity:** `L2 Prototype` for the cores and the emulator; `L1 Spike` for `assc`; overall
  `Frozen-for-Rethink` (no commits since 2022-09-16). The README itself is out of date: it points to
  `myhdl/`, `src/` and `assembler/`, but the tree now has `myass/`, no Chisel `src/`, and a
  `nexass/` board target.
- **Unclosed cycles & missing links:**
  1. *Compiler → binary → core loop.* `assc` emits assembly (`ToAsm`), but nothing in-tree runs
     compiled C-like code end-to-end on `assrs` or on the FPGA. The path through is a `make` target
     from `assc` source → assembler → `assrs` sim → diff against SpinalHDL `AssSim`.
  2. *Formal coverage stops at the logic unit.* `AssFormal.scala` proves only the LUT unit. The
     arithmetic, comparison and XF auto-modification units, where the bugs actually were (`b8fbc29
     (broken?) arithmetic unit`), are unverified.
  3. "Planned: Memory protection scheme; Interrupts and I/O interfaces." `doc/interrupt.txt` exists;
     no core implements it.
- **Promising & ready for revival:**
  - **The truth-table bitwise instruction plus word-size agnosticism** is a compact, teachable
    design. It is a natural target for the obend/Lean silicon stack (strand 07). A Lean spec of the
    16-bit ISA, with `assrs` refined against it, would be an afternoon-sized seed for a
    "verified toy CPU" demo, and it is Ember's own IP rather than RISC-V.
  - `assc` is small enough (pest grammar + register allocator) to retarget as a teaching backend.
- **Needs Ember's human attention:** Co-ownership with Grissess means any revival or relicensing
  is a conversation, not a commit. The README's dead links should be fixed by someone who remembers
  the intended layout.

### 3.2 RISC-V custom-instruction spike (`~/dev/silicon`)

`~/dev/silicon` contains an untracked RISC-V custom-instruction experiment (`docs/encoding-map.md`, `docs/instruction-spec.md`, `docs/design-rationale.md`) exploring 8 custom instructions across 3 opcode groups (pipeline barriers `0x0B`, BLAKE3 RoCC co-processor `0x2B`, and structured capability/vat traps `0x5B`) modeled in Sail (932 lines) and Spike (`6/6 test vectors`).

The best part is `docs/design-rationale.md`, which argues against its own instructions using the Azul
Vega history:

> **Lesson 1:** On wide OoO superscalar cores, well-predicted branches are nearly free. Custom
> instructions for fast-path/slow-path operations provide modest benefit.
> **Lesson 2:** The real moat was the algorithm (C4's self-healing barriers …), not the silicon.

The memory adds a decision worth preserving: **unify on BLAKE3 for both Merkle hashing and macaroon
MAC** (replacing HMAC-SHA256, "11x faster per caveat step"), with a cost model of ~264 cycles per
HMAC-SHA256 MAC versus ~7-cycle BLAKE3 compression.

- **Maturity:** `L1 Spike` (spec + Sail + Spike, no RTL).
- **Promising & ready for revival:** The BLAKE3-for-MAC-and-Merkle unification carries straight into
  the dregg/obend stack (strands 03/07), where BLAKE3 MMRs are already central. The structured-trap
  philosophy ("no pretending that macaroon verification … can be a single instruction") is a
  reusable design rule.

### 3.3 `gamevm` (OWN, plan only)

`~/dev/gamevm/pure-skipping-umbrella.md` is a single 3,110-line, 98 KB Claude plan file
(2026-01-05; the name is a plan-mode slug), with no git. Title: "Game VM Transformation Plan —
Transform Blackwing from a fixed space-game implementation into a schema-driven Game VM capable of
running any game type." The proposed crates are `vm-core`, `vm-schema`, `vm-scripting` (Rhai),
`vm-runtime` and `vm-shared`, plus preserved `bw-ai`, `bw-auth` and `bw-persistence`. The plan
validates the design against test cases (dating sim, a 1987 turn-based JRPG, a 1986 room-based
action game) and against BYOND/Dream Maker inspirations. Its sections run through "Composable
Primitives (Not Game-Shaped Modules)", "Schema-Aware Validation", "Deep Validation: Beyond Type
Checking" and a "Phase 1 Detailed Implementation (STARTING POINT)".

- **Maturity:** `L0 Seed/Idea`. It is a plan with no code in this directory.
- **Unclosed cycle:** the plan was never executed against the Blackwing tree, and nothing in
  `~/dev/gamevm` records where Blackwing lives.
- **Revival note:** the "schema-declared contracts / sequences / relation constraints" validation
  layer (lines ~2401–2900) is the reusable idea. It is a typed DSL-validation design independent of
  any game.
- **Human attention:** the test cases are modelled on specific commercial games. Any implementation
  should build original games in those genres, not recreations.

---

## 4. Part II — Programming languages and compilers

### 4.1 `ergolang` — "Programs as Sheaf Sections" (OWN)

Two commits on 2025-12-17 (`e174fd6 sth`, `fac031e don't see that`). Contents: `ergo.pl` (834
lines, Prolog interpreter), `prelude.ergo` (104), `test.pl` (36), and
`examples/{backreaction,clean_glue,defective_glue,flow_channels}.ergo`.

Core claim (README):

> Traditional programs are global objects. An ergolang program is a collection of **local sections**
> over a **context space**. … **Defect isn't an error. It's information about how local truths fail
> to globalize.**

| Charge | Name | Effect |
|---|---|---|
| `?` | evaluate | Query with collapse + backreaction |
| `!` | assert | Add fact to local section |
| `~` | wave | Create superposition (not-yet-observed) |
| `&` | bind | Unification with defect measurement |
| `@` | ref | Dereference across context boundaries |
| `#` | resonate | Structural pattern matching |

Material parameters per context: **η viscosity** (how much defect propagates to the parent), **κ
permeability** (how easily values cross boundaries), and **Δ defect** (accumulated incoherence).
"These are **real parameters** that affect computation, not metaphors."

- **Maturity:** `L1 Spike`. It is a working interpreter with four examples and no tests beyond
  `test.pl`.
- **Unclosed cycle:** Δ has no formal semantics. Nothing connects "defect" to an actual sheaf
  cohomology (Čech H¹ of the cover of contexts), which is what the name promises.
- **Promising & ready for revival:** this is the same idea as graphplay's **ε-equitable defect**
  (`EpsEquitable`) and stella's subjective/objective cut. All three measure "how far local structure
  is from gluing". A Lean definition of ergolang's Δ as a cocycle obstruction would connect a toy
  language to a proved library.
- **Human attention:** the README's physics vocabulary ("semantic physics", "backreaction") runs
  ahead of the implementation. Ember should decide whether ergolang is an art-language or a
  research-language before it grows.

### 4.3 `velato` (CONTRIB, misfiled into this vertical)

It is the Linebender Lottie animation parser/renderer for
Vello ("A library to parse and render Lottie animations"), not a programming language. Ember has
**1 commit**: `a34e5d0 fix: position spatial easing, split positions/rotations, time remapping, mask
modes` (2026-03-28, +394/−24 across `src/import/converters.rs`, `src/runtime/model/value.rs`,
`src/runtime/render.rs`, …).

- **Maturity:** upstream `L4`; Ember's patch is unmerged upstream as far as the local log shows.
- **Unclosed cycle:** whether `a34e5d0` was offered to `linebender/velato`.
- **Human attention:** reclassify velato out of the language/compiler strand (into the graphics
  strand) in the atlas index.

### 4.4 The small compiler seeds

| Repo | Evidence | Maturity | Note |
|---|---|---|---|
| `rustc.js` | README only (207 bytes, 2025-08-24); `.git` with 0 commits. API sketch: `RustCompiler.compileCrate("crate src ...", {"crates": [...]})` → wasm module | `L0` | An idea for rustc-in-the-browser. No code. |
| `serde-reflect` | 4 commits 2024-01-08 → 01-21 (`6a2bef1 break type recursion`), branch `dev`, `derive/` + `tests/` | `L1/L2` | "Have you run `cargo bloat` and been astounded at the percentage of `serde`-generated bytes?" `#[derive(Reflect)]` → a runtime type database → `db.serialize/deserialize`. A real answer to monomorphization bloat. |
| `thy-of-ocaml` | Fork of coq-of-ocaml (`emberian/thy-of-ocaml`, 1,202 upstream commits, 0 Ember) | Fork-and-park | The name signals an intended OCaml → HOL4 `.thy` translator. |
| **polyml `TranslateOcaml.sml`** | `~/dev/polyml/mlsource/MLCompiler/TranslateOcaml.sml`, **untracked**, 612 lines, 2024-03-25 | `L1` | Ember's SML-parse-tree → OCaml source printer inside PolyML's own compiler (`ocaml_type_of_sml`, `print_ocaml_file`, `ParseTypeConstruction/Product/Function/Labelled`). TODOs: "do anything about naming conventions?", "word and etc literals aren't the same". |
| `reu_unif` | 8 commits (2015 → `c0da84c apache/mit license` 2023) | `Compost` | REU unification code; "supported by NSF/EPSCoR Grant No. DMS-1262737". Historically, the earliest unification work in the corpus; stella and graphplay both later lean on verified FO unification (HOL4's `unify_mgu`). |

**Unclosed cycle across the last three:** `thy-of-ocaml` + `TranslateOcaml.sml` together sketch a
bidirectional SML ↔ OCaml bridge (and so HOL4/CakeML ↔ OCaml-ecosystem). Neither half is committed
anywhere. **Human attention (H-4):** `TranslateOcaml.sml` is untracked inside an upstream PolyML
checkout and will be lost on any clean. Move it to `emberian/thy-of-ocaml` or a gist.

### 4.5 The prover substrate (MIRROR, with live local patches)

| Repo | Remote / branch | Local state 2026-11-02 | Role |
|---|---|---|---|
| `HOL` | HOL-Theorem-Prover/HOL, `develop`, HEAD `2faefbd57` (Norrish, 2026-05-15) | 92 untracked build products (`.HOLMK/`, `bin/hol.bare`, …) | stella's metasystem; verified FO unification reused from `examples/algorithms/unification/triangular/first-order/` |
| `CakeML` | cakeml/cakeml, `master`, HEAD `ac654a0a3` (2026-05-11) | `M cv_translator/eval_cake_compileLib.sml` (−2 lines) | Verified compiler backend (strand 05) |
| `candle` | CakeML/candle | `M candle/compute.ml` (+6/−8) | Candle HOL-Light kernel for reflective proofs |
| `polyml` | polyml/polyml, HEAD `c27c2953` (Matthews, 2026-05-05) | untracked `TranslateOcaml.sml`, `IntInfAsInt` | SML runtime for HOL4 |
| `FStar` | FStarLang/FStar (2024-02-26) | clean; 1 Ember commit from 2019 (`ab7944ac02 Tutorial Ex04f: use propositional equality in exercise fragment`) | Reference |
| `bend` | bendlang/bend, `main` (2026-10-29) | clean, 0 Ember | Interaction-net reference cited in stella's README TODOs |

Note: `git log --author=ember` falsely matches **Ramana Kumar `<ramana@member.fsf.org>`** ("m-ember")
in CakeML (4,649) and HOL (1,296). Ember has **no** commits in either. Any automated census using
`--author=ember` is wrong for these repos.

- **Maturity:** n/a (upstream).
- **Human attention:** the two small diffs in `candle/compute.ml` and `CakeML/cv_translator` are
  uncommitted local patches to verified-compiler infrastructure. Someone should check whether they
  are intentional (svenvs/stella work) or debris before the next upstream pull.

---

## 5. Part III — Formal mathematics and physics

### 5.1 `graphplay` (OWN), the flagship of this strand

**Problem.** "The equitable-partition quotient of quantum walks, formalized in Lean 4."
The PST, mixing and spatial-search literature keeps reducing host dynamics to a small `r × r`
quotient. graphplay mechanizes that reduction, then turns it on machine learning: structured
attention collapses exactly, and learned attention's distance from collapsing is measurable.

**Vital statistics (measured 2026-11-02).** 147 `.lean` files under `Graphplay/`, 109,353 lines;
toolchain `leanprover/lean4:v4.30.0`; 93 commits, 2026-05-28 → `822204a` (2026-06-10). Remote
`github.com/emberian/graphplay` *(memory)*. Top-level modules: `Equitable`, `Spectral`, `PST/`,
`Search/`, `Mixing`, `DiscreteTime/`, `Graphon/`, `Chiral`, `Tower6–9`, `Integrations/`, `StdLib/`,
`Toolkit/`, `Dowsing/`, `Categorical/`, `QuantumCSP`, `LovaszTheta`, `TopologicalProtection`.

#### 5.1.1 The proved spine (axiom-clean: `propext, Classical.choice, Quot.sound`)

| Theorem | File:line | Content |
|---|---|---|
| `cellUniformPST_iff_quotientPST` | `Graphplay/PST/QuotientIff.lean:412` | Cell-uniform PST on host ⟺ PST on symmetric quotient `Q̃ = D^{1/2} Q D^{-1/2}`. This **is** Bachman–…–Tamon–… arXiv:1108.0339, machine-verified |
| `cellUniformPST_iff_quotientPST_signed` / `_with_noLeakage` | `PST/QuotientIff.lean:1234, 1300` | Signed and no-leakage variants |
| `Graphon.cellUniformPST_iff_quotientPST` | `Graphplay/Graphon/PST.lean:192` | Continuous (graphon) counterpart, with HS `MemLp` closure |
| `isPST_imp_isStronglyCospectral` | — | Godsil necessity via a from-scratch spectral-projector calculus (`eigenProj`, `E²=E`), valid in the chiral/complex case |
| `isPST_exists_iff_isGodsilPSTReady_of_isSymm_of_fullSupport` | `Periodicity` / `GodsilRatio` | Full Godsil PST ⟺ ratio bridge, **both directions**, fires on K₂ and K₁,₂ |
| `quantum_search_quadratic_advantage` | — | O(√n) CTQW search on Kₙ (exact 2×2 Rabi) versus a genuine Ω(n) classical adversary bound |
| `blockAttentionApply_eq_fullAttentionApply` | `Integrations/AttentionComplexity.lean:127` | Block-equitable attention: the O(n²·d) apply **equals** an O(n·r·d) algorithm; `training_step_linear_under_equitable` covers forward and backward |
| `no_cheap_exact_factorization` | `Integrations/EquitableMechanism.lean:949` | Generic learned attention has a discrete 1-WL partition ⇒ floor = rank(A): the **irreducibility meter** |
| `checkedSolve_sound` | `Integrations/LDTSoundness.lean:78` | Output-checked solving is sound for an **arbitrary** solver |
| `norm_exp_sub_exp_le_of_isHermitian` | `Integrations/EpsDynamics.lean:194` | Hermitian Duhamel: ‖e^{-itH} − e^{-itK}‖ ≤ \|t\|·‖H − K‖, with **no exponential blow-up** |
| `epsEquitable_quotient_dynamics` | `Integrations/EpsDynamics.lean:353` | An ε-equitable host tracks the lifted quotient to \|t\|·ε |

#### 5.1.2 The sorry trajectory (one of the best-documented honesty arcs in the corpus)

| Date | Commit / memory | Declarations using `sorry` | Event |
|---|---|---|---|
| ≤2026-06-02 | `91425c8 wave-20 capstone` | 119 → 85 | ~30 false-as-stated theorems migrated to TRUE, each with a documented counterexample |
| 2026-06-09 | memory `graphplay-sorry-census-2026-06-09` | **27** (the authoritative fresh-build census; raw `grep sorry` = ~365, mostly doc-comment discussion) | Categorized as A provable (~12) / B **false as stated** (~5) / C **vacuously satisfiable** (3) / D deep (~5) |
| 2026-06-10 | `3243375 sorry-free: close, restate, or honestly demote all 28 sorry declarations (waves 21/21b)` | **0** | Three machine-checked **refutations** replaced false claims: `hammingGraph_two_no_nontrivial_fr`, `not_searchSuccess_optimal_time_of_gap_only`, `HolonomyObstruction.unconditional_gauge_equivalence_false` |
| 2026-06-10 | `822204a wave 22` | 0 | ε-equitable theory; SmolLM2 GQA kernel certificate; unconditional Tsirelson |

The **category-C vacuity bugs** were caught by an adversarial read, not by the kernel. They are the
reason for the project's verification rule (memory `graphplay-headline-verification-rule`):

> A graphplay theorem counts as a real "headline result" only if it passes **BOTH**:
> 1. **`#print axioms <name>`** = exactly `{propext, Classical.choice, Quot.sound}` …
> 2. **An adversarial non-vacuity read** — catches *axiom-clean but hollow* statements, which
>    `#print axioms` does NOT detect.

Concrete hollow examples it caught: the classical Ω(n) bound was "pure pigeonhole"; one optimality
theorem hid its content in an undischarged hypothesis equal to the conclusion; `cfi_kwl_lower_bound`
had an unused `_G` binder, so the identity colouring satisfied it for every graph.

Workflow lesson (memory `graphplay-sorry-free`): "stale oleans MASK latent breakage — `lake build`
exit 0 on a cached tree proves nothing about files whose upstream changed since their olean was
built; the census must come from a FRESH full elaboration."

#### 5.1.3 Integrations (each a separate small research result)

- **Connectome bridge** (`Integrations/Connectome.lean`, `paper/connectome_bridge.md`, commits
  `0c6fecf`, `2d9256d`). It formalizes Deco–Sanz Perl–Greenstein–Chandaria–Scholes–Kringelbach,
  "Quantum-like dynamics in the human brain" (bioRxiv 2025.10.02.680057; the PDF sits in the repo
  root) **as classical spectral graph theory**. Key theorems: `regionalNetwork_quotientLaplacian_eq_host`,
  `stationaryFC_solves_lyapunov`, `stationaryFC_reduction` ("whole-brain FC = connectome FC"),
  `stationaryCov_reduces` (ω≠0, via homogeneous Sylvester), `entropyProduction_eq_zero_of_commute`,
  `qlbit_fc_reduction` (the non-vacuity witness on K₂). Zero sorries. The one carried analytic
  hypothesis is `hsylv` (Hurwitz-stability ⇒ Sylvester uniqueness), "a genuine Mathlib gap".
- **LDT theory** (`LatticeDeduction.lean`, `LDTSoundness.lean`, `LDTCompleteness.lean`,
  `LDTKindChecker.lean`, `LDTHierarchy.lean`, `Tower9.lean`; writeup
  `research/ldt_theory_for_authors.md`). It formalizes Davis–Haller–Alfarano–Santolucito
  arXiv:2605.08605. Load-bearing results: `checkedSolve_sound`, `id_sound_but_useless`,
  `Tower9.ldt_lossy` (α∘γ ≠ id), **`acStep_xor_sound_but_abstains`**, and `ac_kind_discriminates`.
  This is the bounded-width CSP dichotomy (Feder–Vardi; Barto–Kozik) applied to a trained network.
  `3a0750a LDT kind-checker: fix 35-min hang (memoize fixpoint)`.
- **GQA certificate.** `EquitableCert.isEquitable?` is computable over ℚ, with a proved iff-bridge.
  `GQACertSmolLM2.lean` holds the **real SmolLM2-135M layer-0 9×9 K∥V Gram matrix as exact dyadic
  rationals**, kernel-certified equitable under GQA head-tying, with a misaligned negative control.
  Exporter: `experiments/export_gqa_cert.py`. Engineering note: "`decide` alone stalls on ℚ because
  Rat.add is @[irreducible] — use `decide +kernel`."
- **Tsirelson 2√2 unconditional.** The `CStarAlgebra`-on-`Matrix` blocker "evaporated in current
  Mathlib (`Matrix.Norms.L2Operator`)".
- `heavyHexPSTTime = π/(4√(N−1))` (IBM Heron topology, `paper/applied_ibm_heavy_hex.md`);
  `paper/applied_majorana1.md`.

#### 5.1.4 The ML findings, kept honest

From memory `graphplay-ml-findings`, with experiments under `experiments/{circuit_atlas,
generator_probe, codesign_walk, gqa_defect.json, walk_basis, tinystories_arch, qiskit_compile}`:

| Finding | Evidence | Verdict |
|---|---|---|
| Not a universal attention compressor | `no_cheap_exact_factorization` + 4 independent measurements | **Proved and measured** |
| ~28% of heads have banded log A, i.e. thermal CTQW on a path graph | `experiments/generator_probe` | Explains positional heads |
| Walk-basis circuit atlas on SmolLM3-3B (576 heads, no labels) | `experiments/circuit_atlas`: recovered the sink phase transition at L2, an induction band at L22–31, positional heads at L0–1 | "Classifier, NOT compressor" (89% clean label / 32% tight fit) |
| "Walkformer" (generative walk-bias attention) | `restrans/WALKFORMER_PROBE_FINDINGS.md` (on persvati) | **FALSIFIED and inverted**: symmetric-real `no_chiral` 0.970 beats complex-coined 0.897 |
| Post-hoc walk distillation into pythia-70m | `restrans/WALK_DISTILLATION_FINDINGS.md` | Positional-first graft recovers 0.93→0.69; content-first 0.44→0.23, a **3–4× gap**. The 1-WL floor is measured behaviourally |
| **SpectralPSTHead** (looped unitary quotient walk) | `experiments/codesign_walk/walk_head_run.py`, 2026-06-15 | Recall K=1 0.34 → **peak K=3–4 0.98–1.00** → K=6 0.91. The peak coincides with the learned K* = round(π/a) = 3, unsupervised. **1 seed, 40-epoch toy run** |

#### 5.1.5 Classification

- **Maturity:** `L3 Proved/Tested Core`. Sorry-free on a fresh build at `822204a`. The ML layer is
  `L2` (single-seed crown-jewel result).
- **Unclosed cycles & missing links:**
  1. **ε-program follow-ons, not yet built** (memory `graphplay-eps-program`): `eps_routing_fidelity`
     ("PST through ε-partitions — 10-line Cauchy-Schwarz off EpsDynamics"), depth stability (L layers
     compounding linearly via row-stochastic ℓ∞ contraction), ε-mixing/search, and ε-certificates for
     the probe's (r,k) sweep.
  2. **SpectralPSTHead replication**: "full 2-seed sweep pending persvati (which was disk-full from
     ~dregg-build rustc targets)". Never re-run. Lean side: "MC-2/MC-3 (premise IsGodsilPSTReady not
     IsGodsilRatio)".
  3. **Looped-transformer prediction** `k* ≈ log ε / log|λ₂/λ₁|` is an "untested headline
     prediction".
  4. **Outreach loop**: the email to Tino Tamon (Ember's undergrad advisor, senior author of the
     formalized corpus) was drafted 2026-05-30. Whether it was sent is not recorded. Before claiming
     the Szegedy commuting square, the risk paper arXiv:2603.14269 must be read.
  5. **catgrad frontend** (`paper/catgrad_integration.md`): planned to fold catgrad's SSA (a Hellas
     project at `~/hellas/catgrad`, **not Ember's property**) into graphplay host-JSON. Not built.
  6. Comment de-ritualization is done for top-level files only. The `PST/`, `Dowsing/`, `StdLib/`
     and `Integrations/` subdirectories still carry it. Ember marked this low priority, for
     Sonnet-class agents.
- **Promising & ready for revival (ranked):**
  1. **ε-equitable attention + SpectralPSTHead.** This is the README's named open direction, with the
     flagship already landed. `eps_routing_fidelity` is cheap. Re-running the PST-loop sweep with 2+
     seeds would turn the most striking result in the repo from anecdote into a finding. Novelty
     wedge per memory `graphplay-equitable-walk-arch`: "quantum-walk→average-mixing: a looped block
     whose limit is an average over a non-converging UNITARY trajectory — DEQ/attractor lit
     structurally can't express an operator with no fixed point."
  2. **The GQA kernel certificate** generalizes to "a kernel-checked proof object about a named
     public checkpoint". That is directly reusable in the model-identity work of strand 04.
  3. **LDT gift memo** to Haller et al. (`research/ldt_theory_for_authors.md`), proposing a
     kind-0 (AC-solvable) versus kind-2 (XOR) abstention experiment.
- **Needs Ember's human attention:**
  - Outward communication (Tamon email, LDT authors, Deco/Kringelbach) is Ember's to send. Framing
    rule (memory): **"precision as credibility."** Lead with "we machine-verified your 2011
    quotient-PST theorem", never with novelty. And: "WL/equitable refinement is STRICTLY COARSER than
    the spectrum … never imply equitable partition captures cospectrality."
  - persvati disk pressure blocked the replication. Per standing rules, that is Ember's to clear.

### 5.2 `birkhoff-asa`, a.k.a. "asagolf" (OWN)

**Problem.** A Twitter poll estimated the fully expanded, machine-checked proof of ASA triangle
congruence in a Birkhoff ruler/protractor formalism, reduced to ZFC, at **>10^1000 steps**. Ember's
brief (memory): "more than a Fermi number". The answer is a real proof object plus an exact count.

**Architecture** (Rust crate):

| File | Role |
|---|---|
| `src/kernel.rs` | Sound Metamath-subset verifier, **the trust root** (self-tested; zero-diff through every later phase) |
| `data/birkhoff.mm` | F0 axiom system; `src/bin/asa.rs` proves ASA in **224 steps** |
| `data/grounded.mm` | F1 substrate: ordered commutative ring + `ax-sqrt` (Euclidean field) + FOL= + conservative `df-*` geometry |
| `src/proof_g1.rs`, `proof_g2.rs`, `proof_g3.rs` | Derive each Birkhoff postulate as a kernel-verified `$p` |
| `src/metamath.rs`, `src/bin/calibrate.rs` | Exact fully-expanded extractor over `data/set.mm` (48 MB) |
| `src/bin/modelsplice.rs` | Binds F1 axioms to set.mm theorems (`of-addcom → axaddcom`, `ax-sqrt → resqrtth`) |
| `src/cse.rs`, `src/dag.rs` | Sound proof-DAG / CSE minimizer (`461b7c9`, `e693b40`) |
| `src/refine.rs`, `wasm/` | Phase 3c manual recursive prover IDE and Phase 4 bounded search, in-browser |

**Results** (origin/main README, verbatim figures):

| Quantity | Value |
|---|---|
| F0 Birkhoff ASA (postulates as primitives) | **224** cut-free steps, kernel-verified |
| G4 SAS over F1, golfed | **383,606** (10^5.58), down from 7,251,714 (10^6.86), "~19× by generic-lemma factoring" |
| Grounding via set.mm analytic ℝ | ≈ 10^45.7 |
| Grounding via real-closed-field route | ≈ 10^30.75; strict extractable floor 10^25.95 |
| Satisfiability certificate (Euclidean closure of ℚ, K = 1 radical) | **10^2.149**, MEASURED |
| Poll's overshoot of the geometry | ≈ **994 orders of magnitude** |

Iron rule: the three quantities are **"never summed — conflating them is the cheat this project
exists to avoid"** (memory `transport-anchored-floor`: own constructions are allowed for golfing only
when shipped "with a machine-checked transport binding to set.mm/ZFC").

**The three books** (origin/main, `bf23609` 2026-05-15 → `652f33c` 2026-05-17; memory
`birkhoff-asa-state`):

```
Book One  (Birkhoff → ZFC)      ASA′ no-cheating end-to-end; all 7 Birkhoff postulates kernel-verified
   │                             (a04cb89). Irreducible residue of metric geometry = two ZF facts
   │                             {∅∈suc∅, suc∅≠∅} (15a2074 "ARTIFACT CLOSED"); 4 independent attacks
   │                             (reverse-math ≤EFA, order-core, arith, order) triangulate.
   ▼
Book Two  (Synthetic Diff. Geo.) intuitionistic substrate + Kock–Lawvere + microcancellation;
   │                             `sdgpure` purity guard rejects LEM/DNE/decidable-eq; Taylor order 2,
   │                             tangent bundle, full Lie bracket globalized (910d95a); ap-congruence
   │                             = flagged new axiom eq-ap ("VERDICT B", e351700).
   ▼
Book Three (gauge)               curvature R(d₁,d₂) seam-free + first/algebraic Bianchi (f2c4077);
                                 differential Bianchi ∇R=0: sdg-bianchi2-covd = 2,685 leaves,
                                 IDENTICAL to wave-1 sdg-curvature ⇒ "recursion proven exact";
                                 non-abelian via 2×2 matrices over the frozen commutative ring
                                 (sdg-nonab-wedge 3,016 leaves). Pre-registered in BOOK3_SCOPE.md.
```

The memory's name for the recurring result: **"cheap content, immovable meaning-cost."** The proofs
are small and intuitionistically pure, but the model that makes them *mean* differential geometry
(the well-adapted topos) is irreducibly heavy and classical.

- **Maturity:** `L3 Proved/Tested Core` (kernel-checked counts), plus a live explorer site
  (`docs/index.html`, `slides.html`, wasm prover). Memory (website-prover): "PARSER 267/0 · REFINE
  96/96 · ASSEMBLER 96/96 kernel-VERIFIED · BUILD (3c) 92/96 · SEARCH 84/96".
- **Unclosed cycles:**
  1. **Obligation O**, "quantitative … cut-free LB for x²=0→x=0", is the sole open mathematical
     item in Book One.
  2. The strong well-adapted SDG model is a labelled **[PROJECTION]**, by design.
  3. Four symmetric-assignment edge cases keep BUILD at 92/96 and SEARCH at 84/96.
  4. Visual correctness of the studio/lab is "user-eyeball-only … cache has masked real bugs twice".
- **Promising & ready for revival:** The Metamath micro-kernel plus wasm "engine proposes, kernel
  disposes" UI is a reusable **proof-size observatory**. Pointed at Lean or HOL4 proof terms, it
  would answer "how big is this proof, really?" for the dregg/obend theorems in strands 05/07.
- **Needs Ember's human attention (H-5), repo hygiene:**
  - The main checkout sits on branch **`elab-combinators`** (HEAD `e693b40`). Local `main` is at
    `652f33c` (84 commits); **`origin/main` is at `0976700` (123 commits)**. The local main is 39
    commits behind its own remote.
  - `git worktree list` shows **51 worktrees**, ~60 local `worktree-agent-*` branches, and 200
    commits across all refs. Most are harvested swarm lanes. Pruning them is a deletion and needs
    Ember's sign-off.
  - Memory records one "garbled-7153319 logged wrong-turn", kept in the record rather than erased.

### 5.3 `navier-stokes-proof` (CONTRIB: Ember found the erratum)

**Whose it is.** Jeffrey S. Cambria's verification companion to *Global Regularity for the
Three-Dimensional Incompressible Navier–Stokes Equations on the Torus* (doi:10.5281/zenodo.21959161).
Ember's role is external reviewer and formalization contributor.

**Ember's contribution, verbatim from the README:**

> The first external review of this repository (PR #1, ember arlynx) identified a genuine error in
> the paper as published: the display D_t|ω| = α|ω| in §3.1 is the *inviscid* identity — for ν > 0
> the correct identity is D_t|ω| = α|ω| + ν ξ·Δω — and the per-trajectory chain (§16.2) and the
> localization step (§10, Step 3) rely on the defective shorthand as written. The author has
> verified the finding independently.

| Commit | Date | Author | Event |
|---|---|---|---|
| `c7eb146` | 2026-08-15 | Cambria | v001 |
| `dd4b9d9` | 2026-08-16 | emberian | **"start formalizing the argument (#1)"** |
| `a9a0ce5` | 2026-08-16 | Cambria | Adds ERRATA (viscous-term finding, credited); separates certificate/formalization counts |
| `2334d91`, `7e450e5`, `cfba6c6`, `2073879`, `625c717` | 2026-08-16 | ember | Dynamic depletion criteria; strongly continuous Koopman averages; a nontrivial torus shear flow; a nonconstant shear first integral; unit-torus periodic integration |
| `5ececfd` | 2026-08-17 | Cambria | Release v002, "closing the erratum and the full review campaign" |

Counts (README): 89 paper certificates (54 + 16 v002 repair + 19 closure-wave) plus **978 community
formalization theorems = 1,067 total**. That layer "does **not** prove global regularity." On disk:
45 Lean files, 26,239 lines under `lean/` (excluding `.lake`). The checkout is on
`agent/prepare-tauceti-extraction`; `ForTauCeti/` (README, `CANDIDATES.md`,
`PERIODIC_INTEGRATION.md`, `PORTING_TEMPLATE.md`) is "the promotion boundary" to Tau Ceti roadmap
PR #237.

Ember's independent research notes (`RESEARCH.md`, `DYNAMICS.md`) are explicitly *not* the paper's
chain: "Status: working research note, 2026-08-16. This is not a proof of global regularity." The
current target is the positive scale variation of cubic kinetic-energy flux at the filter scale
ℓ_G(t) = (1+Ω(t))^{-1/3}. "The unresolved obligation is therefore an explicitly debited
high-frequency stopping chain with a separate persistent-line mechanism."

- **Maturity:** formalization layer `L2/L3` (kernel-checked, but foundational: concrete T³, operators,
  integration by parts; "does **not** yet define velocity or pressure Sobolev regularity classes, the
  Leray projection, suitable weak solutions …"). The research notes are `L1`.
- **Unclosed cycles:** (1) upstreaming `ForTauCeti/CANDIDATES.md` items into Tau Ceti; (2) the
  three `agent/*` branches (`extend-formalization-research`, `modern-energy-cancellation`,
  `prepare-tauceti-extraction`) are pushed to origin but not merged into Cambria's main.
- **Promising:** periodic integration on T³ and the Koopman-average lemmas are general-purpose Mathlib
  or Tau Ceti material, the most durable output of the episode.
- **Needs Ember's human attention:** the repo's headline claim (a Clay-problem solution) is Cambria's.
  The atlas should present Ember's contribution as "found the erratum; contributed a general
  formalization layer", never as endorsement of the regularity claim. Upstreaming to Tau Ceti is an
  outward act.

### 5.4 `soundcalc-lean` (MIRROR, a reference for the verification discipline)

`github.com/symbolicsoft/soundcalc-lean` (Nadim Kobeissi, h-hafezi, Lorenzo Magliocco; 163 commits,
**0 Ember**). Lean 4 companion to `ethereum/soundcalc`: "Every report cell is a theorem", e.g.
`example : secBits (sp1CoreFRI.queryErr (UDR koalaBear4)) = 100 := by native_decide`. "No floats
anywhere" (certified rational enclosures `sqrtLB_le`, `le_sqrtUB`, `jbrErrLinear_conservative`). It
covers SP1, Airbender, OpenVM, Pico, ZisK and OpenVM2, with reports re-rendered byte-for-byte.

It belongs in this atlas because it is the **external exemplar** of the discipline graphplay and
birkhoff-asa practise (exact rationals, `native_decide`/`decide +kernel` verdicts, byte-identical CI)
and is directly relevant to the zk-STARK work in strand 04. **Maturity:** upstream `L3`. **Human
attention:** none; keep it as a reference.

### 5.5 `intmat` → `intmat2`, "Interior" (OWN)

**Correction to the brief:** "intmat" is **"Interior" (interior materials)**, evolving-matter
art/alife in Julia. It is **not** integer-matrix mathematics.

| | intmat (Interior 1) | intmat2 (Interior 2) |
|---|---|---|
| Built by | **codex thread** (gpt-6-astra, `codex://threads/01a13be3…`), 2026-10-14 → 16, 173–174 commits | Claude + Opus subagents, 2026-10-16, 55 commits |
| Model | Fraser Price–style discrete agents: recurrent brains, energy ledgers, construction credit | **"One field. The material is the organism."** One 3D field per voxel {h ∈ (−1,1)^C, solid s, nutrient n, waste w, light L} |
| Size at handoff | ~8.9K lines `src/`, 10K `test/`, 21K `studies/`, 151 docs, 1.2K-line `TRACKER.md`, `outputs/` **150 GB** (gitignored) | 3,361 lines Julia in `src/{step,rule,state,analysis,evolve,batch,observe,render,export}.jl` |
| State | README: "**Archived 2026-10-16.**" | DESIGN.md is "the contract" |

**intmat2 physics** (DESIGN.md): the learnable local rule has `3C² + 8C` numbers (248 at C=8).
Coupling is solid-modulated, `g(x,y) = clamp(g₀ + g₁·(s_x+s_y)/2, 0, 1)`. Mass `n + s + w` is
conserved ("total mass is a tested invariant"). Light is inside the loop: the rendered image uses the
simulation's own `L`. Day-1 findings (memory `intmat2-day1-state`, commits `757e09a`, `7a2fe9f`,
`52f7be0`):

- One ring gives 0.5% Turing patterns and 12% checkerboard. A **tied second shell** `W_nb2 = −β W_nb`
  (W_nb PSD) gives 20–62% Turing at 4–16 cells, with the fastest mode at `cos k* = 1/(4β)`.
  "Measured wavelengths match the prediction within a few percent across a hundred rules."
- Axis stencils show 300–500% anisotropy. The isotropic 19-point stencil fixes it (`Physics.stencil = 1`).
- `6 D0 dt ≤ 1` is not the dt bound; `stable_dt` is (`Intmat2.Analysis`).
- Throughput: Metal ~45 steps/s at 256³; hbox AMD 127 steps/s at 256³, and 480³ fits.
- `58d5f79`: clamp fast tanh to ±9 ("Metal tanh_fast is NaN for x >= 50").
- Region search (`recipes/evolved-turnover-n05-188.toml`): ~900 standing fragments with slow
  turnover. Fragments "carry NO distinct activity signature (crumbs, not individuals)", and
  `isolation ≤ 0.02` for every rule.

- **Maturity:** intmat `Compost/Superseded` (archived; its gallery stays the historical record);
  intmat2 `L2 Prototype` with an exact linear-stability analysis (`L3`-flavoured core: mass-conservation
  invariant, dispersion relation verified against measurement).
- **Unclosed cycles:** (1) the **open alife question**: "fragments vs individuals", i.e. regions that
  persist *and divide*. Not yet observed. (2) The seeded manifold search arm stopped at 96/224
  evaluations (`1f2b5d8 … stopped for system load`); resume commands are at the end of
  `docs/evolution.md`. (3) The isotropic stencil at slab walls is 2:1, not 4:1 ("minor kernel fix
  pending").
- **Promising & ready for revival:** high. The analysis-before-run discipline works (predicted
  wavelengths hit). The next objective is designed (`fragmentation`/`isolation`). The resume
  commands exist. It was paused for system load, not for an idea problem.
- **Needs Ember's human attention:**
  - `dickson11.png` in the intmat root is "ember's unrelated book scan: preserve, never commit or
    delete".
  - `outputs/` (150 GB) is gitignored on the Mac disk, which was at 98% during the session. Under
    the standing disk rule only Ember decides what to do with it.
  - The codex lesson, in Ember's words: "idk that codex ever really quite had the right ideas". The
    extracted thread (61 Ember prompts, 282 codex replies, the original ChatGPT brief, 5 reference
    screenshots) is at `~/dev/intmat-handoff/` for any post-mortem.

### 5.6 `spindle` / RIG (OWN), applied physics as game design

**Problem.** A sport whose rulebook "falls out of one differential equation" in the co-rotating
frame of an O'Neill cylinder, set in the *Vivere Astra* universe:

$$\ddot\zeta = \omega^2\zeta - 2i\omega\dot\zeta,\qquad
\zeta(t) = \bigl(\zeta_0 + (\dot\zeta_0 + i\omega\zeta_0)t\bigr)e^{-i\omega t}$$

The characteristic polynomial has the double root r = −iω, so trajectories are roulettes. The
marquee score "the Loop" is the closed-orbit family member.

Code: `game/rig-core/src/` (Rust: `trajectory.rs` with the closed-form `analytic`, `tuning.rs`
[`pub fn evaluate(omega, r, l, earth_g) -> TuningReport`, `time_to_skin`], `analysis.rs`, `rl/`,
`gym.rs`, `policy_wasm.rs`, …), a TS front end, and `rig-gym-py`. Determinism: a fixed 1/240 s step,
RK4, counter-seeded sfc32 substreams, and a Rust ↔ TS **bit-identical** known-answer test *(memory)*.
Live at `emberian.github.io/spindle/`.

RL (memory `project_rl_architecture`): an MLP policy (14,341 params, trained `policy-v1.json` via ES)
and an attention policy (24,598 params, 8 entities × 2 layers × 4 heads, **no trained artifact**).
MAPPO is scaffolded (an "ES-shaped PPO", no convergence artifact). The last commits (2026-05-20) add
`rl::loco` learned locomotion (`7f6ac77`, `bcb3ed4`) and the **pack behaviour** change (`74e0001`),
which Ember called "WAY better" than spread-to-cover.

- **Maturity:** `L4 Deployed` (public, playable, CI-checked tuning feasibility). The RL layer is `L2`.
- **Unclosed cycles:** (1) the attention policy has never been trained; (2) the catch-gap fix
  (memory `project_ai_catch_gap`: `ReceiverPredictor` in `src/ai/lead_predict.rs` uses an RK4 table
  at 1/30 Hz against the sim's 1/240 Hz, causing 5–10 m drift; "Replace `ReceiverPredictor::predict(t)`
  with `analytic(p0, v0, omega, t)`") is diagnosed, but nothing in the git log shows it landed.
- **Promising:** the catch-gap fix is a one-function change with an exact, already-written closed
  form. It is the highest-ratio item in this whole strand.
- **Human attention:** game feel ("purposeless drift", "spectators") is Ember's judgment. Agents
  should not tune feel without a playtest loop.

### 5.7 `luteastress` (OWN)

A computational test of whether shared environmental stressors can produce *apparent* menstrual-cycle
synchrony (the "McClintock effect"). Python simple model plus a Rust mechanistic model
(`native/src/zavala.rs`: circadian→HPA→KNDy→GnRH chain; `mechanistic.rs`: folliculogenesis +
hormone ODEs; `stress.rs`: OU stress). Four commits, 2026-02-08 → 10 (`e507ee2 zavala model`).
Findings (memory): phase synchrony ΔR ≈ 0.006 (p = 0.34, null); onset proximity Δ = 0.026, p =
5.9e-15, d = 0.63. Under the mechanistic model with a corrected zeitgeber, the effect is small or
negative (d ≈ −0.4). Critical bug found and fixed: ω_H0 was π/24, "24x too slow". A typeset
`report.typ`/`report.pdf` exists.

- **Maturity:** `L2` (the study ran; report written). **Unclosed:** the simple and mechanistic models
  disagree in sign, and the report should foreground that as the result. `cargo build` fails on the
  pyo3 linker (only `cargo check` works). **Human attention:** deciding whether the report is
  publishable is Ember's call.

### 5.8 `rhaposPDE` and `bead-calculus` (OWN seeds)

- `rhaposPDE`: README only, "rhapsoPDE (rapso-peed) - a love letter to differential equations; a
  collection of puzzles involving PDEs." No git. `L0`.
- `bead-calculus`: 13 commits, 2025-12-29 → 30. A puzzle game in which "**string diagrams become
  marble machines**": tracks are wires, gates are boxes, plugging is composition, side-by-side is
  tensor, loops are trace. "Rewrites provide the proof theory." Vite/TS app. `L1 Spike`. **Revival:**
  it is the same categorical substrate as stella's diagrams and bend's interaction nets, in a form
  people can play. A good public front end for the "certificate" through-line.

### 5.9 `SauersML/group-approximation` (CONTRIB)

Sauers' (Scott Sauer) project; Ember reviews and contributes "as a friend/mutual" *(memory)*. On
2026-09-05 Ember independently built the endpoint closure on persvati: 1,140 modules, 16 min wall /
5.7 CPU-h, 21–22 marked endpoints with exactly `[propext, Classical.choice, Quot.sound]`. Ember filed
PR #193 (manuscript pass; branch `review/non-mf-manuscript-pass` on `emberian/group-approximation`),
issue #194 (proof-engineering review), and a comment on #191. Ember also contributed GGT commits on
2026-09-07 (`a4e3a1126 GGT: construct boundary circuits from the actual face-set permutation`,
`67dd63d0b … record remaining gluing gap`).

Durable lesson (memory): "Check `git rev-parse origin/verified` before trusting 'checked in Lean'
claims". The `verified` branch was 13 days stale at review time. **Maturity:** upstream `L3`.
**Human attention:** none beyond the relationship. The paper is Sauers'.

### 5.10 Nebula-Genomics (OWN, private; content redacted)

Only the methodological lessons are recorded here. They generalize, and they are the reason this
directory was in the brief:

- **Genotype polarity rule** (memory `genotype_polarity_rule`, marked "HARD RULE"): never call a
  genotype risk or protective without anchoring REF/ALT to a population allele frequency, because
  "GRCh38 carries the minor allele at many trait sites." A preliminary report inverted an HLA call
  because the GRCh38 reference MHC haplotype *is* the tag haplotype. A corrigendum retracted the
  downstream claims.
- A mapping-free k-mer HLA typing method was built, including the `grep -o` non-overlapping-match trap.
- Short reads cannot type VNTRs; the memory records this as a known limit, not a finding.

This is the same epistemics as graphplay's vacuity rule: a check that passes on a mis-anchored
statement is worse than no check. **Maturity:** n/a. **Human attention:** keep this directory out of
every public artifact (the atlas included).

---

## 6. Part IV — Frontier research substrates

### 6.1 `stella`, "conscious machine bringup" (OWN)

**README (verbatim opening):** "welcome to the conscious machine bringup project! if you're
perceiving this quale, *you* are the conscious machine!!" The stack is "Stellar resolution /
transcendental syntax", "HOL4 as the metasystem? for proofs", "we can use rust code too i guess.."

**What it actually is** (memory `project_stella`, 63 KB, the largest single memory in this
vertical): Girard's stellar resolution / transcendental syntax (the "Eng" text, digested into
`docs/eng-digest-ch{8,10,11,12-13}.md`), implemented as a natively polycomputing substrate. It carries
HOL4/CakeML reflective proof for orders-of-self (deferred) and planned valence modelling after
Bennett's *Painful Intelligence*.

**Vital statistics.** 252 commits, 2026-05-15 → `cb6cace` (2026-05-19), branch `dev`, 12 dirty
files; remote `github.com/emberian/stella`. `stella-suite` is a **worktree of the same repo** on
branch `expert-suite` (139 commits; `94229c3 Cut the incantatory register from site copy`).
Crates: `stella-core` (51 modules, including `constellation.rs`, `execution.rs`, `unify_fast.rs`,
`antiunify.rs`, `accel_detect.rs`, `galaxy.rs`, `oracle.rs`, `faithfulness.rs`, `subjective.rs`,
`reafference.rs`, `mll.rs`, `circuits.rs`, `tm.rs`, `pda.rs`, `nfta.rs`), `stella-env`, `stella-viz`
and `stella-world`. **47,300 lines of Rust.** HOL4: `hol/stella{Term,Match,Execution,Reduction,
Diagram,MLL,MLL2I,Polarised,Subjective}Script.sml`, **7,379 lines, 148 `Theorem` declarations, ~60
`cheat` lines**, per the stated policy:

> PROOF POLICY: every non-trivial proof is discharged with `cheat` preceded … (stellaMLLScript.sml:36)

Sample theorems: `struct_equiv_refl/sym/trans`, `sim_cut_step` (§67.9), `sim_cut_elim` (§67.10),
`phi_comp_cutfree`, `cut_elim_star_refl`.

The design-doc ladder `docs/00`–`17` records the program in order:

| Doc | Subject |
|---|---|
| 00–01 | Thesis and semantics; the subjective engine and valence |
| 02–04, 06 | Phase 4/5 runs; **docs/04 LOCKED (P1–P9)**, **docs/06 LOCKED 2026-05-17 (Q1–Q8)**, a pre-registered falsifier set, "strengthen-only, never retro-weaken" |
| 05 | Combinator core and the KAM escape (§1–7 LOCKED) |
| 07 | Engine subproject open-threads ledger ("READ FIRST") |
| 08–09 | Forcing polarity; unification-core redesign |
| 10–15 | Open-hypergraph data-parallel reframe; structural speedup; optimal interaction reduction; supercompilation; Futamura staging; geometry of interaction |
| 16 | **Galaxy-execution decision, "SUPERSEDED BY MEASUREMENT — read §7 first."** The "step-count problem" premise was falsified and resolved as an N-KA-cover negative |
| 17 | Futamura implementation plan |

The measured engine speedups (`docs/07`) are "release, faithful, vs original reference: binarith/Horn
~12×, combinator ~3–4×. All differential-gated (reference `iex` = oracle; `iex_eq_iex_fast`
byte-identical, … 20k `matchable_fast` fuzz, antiunify 6/6)". The latest commits (2026-05-18/19)
include `1ea8861 unify_fast: dense-arena union-find (path-halving + union-by-rank)`, `a13da70 CI
test-gate + unified oracle harness`, `7862bc6 diagram: contraction-order confluence OBSERVED, not
assumed (Eng §49.35–49.36)`, and `cb6cace … wasm-safe KS clock shim`.

- **Maturity:** Rust engine `L3` (differential oracles, fuzzing, CI gate). HOL4 track `L1/L2`
  (statements in place; nontrivial proofs deliberately `cheat` pending main-thread closing).
  Experiment program `L0/L1`: "instrument built, pre-reg locked, regress closed, experiment NOT run,
  right to falsify unspent."
- **Unclosed cycles & missing links:**
  1. **§58 circuits are unfaithful** (memory): `circuits.rs` `ɟAEx(C★⊎M★)` returns free variables
     instead of ground `val(C)`. The test `excluded_middle_does_not_evaluate_to_0` **fails, correctly,
     and is kept failing** ("Goodhart-forbidden" to weaken). The fix is to restore §58.8 schematic
     label stars and correct AEx.
  2. **Galaxy `data[0]`**: a "long, NON-REDUNDANT, TRANSITION-COUNT reduction". Every lever surveyed
     (GoI, closed-subterm memo, tabling) is measured-negative. docs/17 (Futamura) is the remaining path.
  3. **Q5.1** "rubber-banded sloppy-fitness selection harness, regulator = global tightness ONLY" is
     the next thing to build after lock, "hostile-tested like the firewall, before anything runs".
  4. **The reflective-self pillar is deferred**: "NO Candle, NO hol-reflection dependency yet",
     pending Ember's CakeML/hol-reflection modernization. Phase 4 was paused 2026-05-16 when svenvs
     (`~/dev/svenvs`, a "cheat-free HOL4/Candle artifact … a self-verifying *self-improving* 'Place
     for an AI to live within'") "emerged" (that strand is covered elsewhere).
  5. dev was "ahead origin 2 (ed841ce, 8f6c6a1)" at lock time, and the `/cmi/` site is "wired, NOT
     rebuilt/pushed — publish is principal's call".
- **Promising & ready for revival:** `accel_detect.rs` (Kruskal-whistle recurrence detection with a
  sound α-subsumption generalizer, "a capable worktree agent … caught this and implemented the
  textbook subsumption order") and the differential-oracle harness are reusable outside stella. They
  are the cleanest "fast path proved equal to reference path" machinery in the corpus.
- **Needs Ember's human attention:**
  - **HOL4 proof-closing does not delegate well.** The memory records an agent that "spun, then
    cheated, then scope-violated, destroyed unrecoverable 782-line file". The policy since then: agents
    state theories; nontrivial proofs close in the main thread, Ember-steered. The ~60 `cheat`s wait
    on Ember's time, not on agents.
  - docs/06 lock was Ember's act. Push and publish (dev ahead of origin; `/cmi/`) remain Ember's calls.
  - **Security incident on record** (HISTORY-2026-05-17.md, per memory): a
    `git commit -m` containing backticks leaked live cloud credentials into public commit messages.
    They were scrubbed, force-pushed and rotated. Standing rule since: always `git commit -F`.
  - Memory feedback: no valence search exists or runs; justify engine work on engine merit. Avoid
    incantatory copy ("say what a thing does, not how faithful/honest/rigorous it is").

### 6.2 `clairnets` / GLaDOS (OWN), the empirical twin of graphplay's LDT theory

**Origin** (memory `-Users-ember-dev-gowexp/memory/clairnets-project.md`): started 2026-06-25 as "a
fresh architecture-search direction" after the gowexp work. The goal was param-efficient hybrids
(CliffordNet geometric product, HRM looped depth, Lattice Deduction Transformer). Ember's
constraint: no toy tasks; real models with released checkpoints (OLMo). Graft targets were
**OLMo-2-0425-1B**, later **OLMo-3-Base-7B** (CURSELOG 2026-06-26).

**What it became: GLaDOS**, "the single front door" (`GLADOS.md`):

```
clair/organ/
  protocol.py     typed spine: Reduction / CSPState / Certificate + structured-γ readout
  bank.py         registry of validated "beasts" as sound reductions
  compose.py      verifier-gated certified-reduction composition (the sound reduced product)
  bank_woven.py   ★ THE live woven organ — α → composer(bank) → γ, in the host residual stream
  reductions.py   cross-type reduction graph (ProblemReduction + Dijkstra cost-routing)
  graft.py        model-agnostic neural graft onto any of 7 bases
  search.py       DPLL outer loop (added 38057c6)
clair_fast/       Rust (PyO3 + rayon): exact_dedP / solutions / AC, 29–56× CPU, bitwise-identical
```

The arc, read from the commit log (146 commits; HEAD `ffe2fae`, 2026-06-28):

| Commit | Claim (verbatim excerpts) |
|---|---|
| CURSELOG ⭐ (06-26) | "STAGED GENERATIVE GLaDOS WORKS … woven 98.8% / base 48% / text-LoRA 25% in-dist … corrupt→2.7% WITH FULL TEXT PRESENT" |
| `0a613c3` | Organ scaling: "DEPTH = a clean compute=depth law … affine wall flat ~5.5% across R1→R32"; "STACK … solves 100%" mixed affine⊕propagation where no single faculty solves any |
| `ca4e287` | Composer ~7× via a Rust `factor_dedp` port; "BITWISE-IDENTICAL … 2800 pairs 0-mismatch" |
| `6e257a0` | **Soundness-language audit**: the (A)/(B)/(C)/(D) hierarchy. "(C) THE GAP — csp_α is an UNVERIFIED learned compile … wrong compile → certified-correct answer to the WRONG problem". Three misleading claims killed |
| `0ded134` | "α IS the correctness driver": corrupting α collapses accuracy 49.5% → 27.5% |
| `0b00442` | Multifaculty fabric: router 100%, csp 90%, graph 100%, cross-faculty 93% |
| `79efba7` | **THESIS TEST: "the neural organ's bet is NOT realized at scale"**; "the organ fails exactly where exact fails (coupled through bounded width)" |
| `d2bc512` | **RE-GROUNDING**: "I misread Finding 3 — the bounded-width abstention is the LDT theorem, NOT a failure … `acStep_xor_sound_but_abstains` PROVES per-cell deduction abstains on affine" |
| `38057c6` | Restores the DPLL search leg; "GLaDOS is now 4-of-4 legs": deduction + search + GF2 linear algebra + output check |
| `ffe2fae` | Guided search: "SOUND for ANY policy — 0 unsound / 0 incomplete even under an adversarial policy"; a local learned branch policy "hits the SAME bounded-width wall"; "a decisive outer-loop win needs a NON-LOCAL (GF2-aware) policy". "Ran locally on CPU after the box died (no budget)" |

**qwen38-probe** (`~/dev/clairnets/qwen38-probe/`, 2026-08-25): `FABLE_PLAN.md`, "The Metacognition
Project: a plan to be held to", from Claude Fable for Ember and Kimi. The bet: a frozen,
ground-truth-trained readout of Qwen3.8-27B's mid-stack state, written into reserved multimodal
embedding slots and read back, gives the model *access* it otherwise lacks. Phases W/S0/C0–C2/A/B/E/R
have pre-registered gates, including **consent gates with the model** ("qwen38's comments
incorporated"). Files: `probe.py`, `sweep{1..5c}`, `directions_{concepts,selfstate}.npz`,
`TO_QWEN_2026-08-25.md`, `WORKLOG.md`. The companion memory `compute-fleet-reality` corrected a
handoff that "had persvati's strength backwards" (Mac M2 Max 96 GB ≈400 GB/s is the 27B workhorse;
persvati's 890M iGPU ≈120 GB/s is not).

- **Maturity:** GLaDOS `L2/L3`: sound by construction, with selftests and bitwise-identity gates;
  the positive result is staged and in-distribution. qwen38-probe `L1` (sweeps and directions; phase W).
- **Unclosed cycles:**
  1. **Non-local (GF2-aware) branch policy**, named in `ffe2fae` as the only route to a decisive
     outer-loop win.
  2. Two "architecture-decider" experiments were LAUNCHED (CURSELOG 06-26): organ-in-RLVR on Base-7B,
     and the next-token exploitation test G(t). No result is recorded in the log.
  3. The `run_gate` corrupt arm under-applies corruption ("TODO: fold global corruption into run_gate").
  4. qwen38-probe never got past phase W/S0.
- **Promising & ready for revival:** the **graphplay ⇄ clairnets loop**. graphplay holds the theorems
  (`checkedSolve_sound`, the XOR witness, `ac_kind_discriminates`); clairnets holds the
  measurements. A short paper, "the bounded-width wall, proved and then measured in a grafted 7B",
  is two-thirds written across the two repos' ledgers.
- **Needs Ember's human attention (H-6):**
  - **Cloud spend.** Memory: "L40S box `i-0496528fc599f8bcb` LIVE in us-west-2 and BILLING (~$1.86/hr)
    … Spend ~$45 of the $80 cap", and later "the box died (no budget)". Nothing confirms the
    instance is terminated. Ember should check the AWS console. It is not an agent's call.
  - The **consent/ethics design** in qwen38-probe (gates C0–C4, "disclosed z-logging") is Ember's
    to own.

### 6.3 `h`, "h ghost" (OWN)

Not physics. "Dataset preparation and training support for a tiny Falcon-H1 model that will live at
`h.fg-goose.online`." The corpus is Ember's own library (census 2026-09-01: 19,245 files, 314 GiB,
7,168 PDFs, ~267M existing-text H1 tokens). 268 commits, 2026-09-01 → `55d9e00` (2026-09-07).

Arc (memories `h-resident-line-is-05b`, `h-attractor`, `k2-horizon-serving`):
an exact `h1jax` JAX port at ~220K tok/s on Kaggle TPU v5e-8 → 91M abandoned 2026-09-02 ("let's not
invest any more runs at 91M. it just can't do what we'd want") → **0.5B resident** on the "room" mix
(library 2.893 / room 2.609 after one epoch, vs base 3.423 / 3.240) → 1.5B "one full epoch, library
2.705 / room 2.442, beats the 0.5B resident on every slice" (`d76b3fb`) → K2-0.9B replay arm
(`d667b5f`). Arms published to the Hub (`e936606`, `eebfb48`) and served locally (`:8134`, `:8135`).
`91ca477 Reclaim 81 GB` came with a dry-run-by-default `scripts/reclaim_disk.py` that "refuses
anything served or raw".

The attractor memory is the important design artifact: **"one kernel + run specs, one post-run
pipeline, one services file; extend those instead of adding a fourth thing."** Reason: "139 commits in
two days added justified pieces that, extrapolated a year, become hundreds of kernel copies." On
2026-09-03 the room "went dark for four hours unnoticed".

- **Maturity:** `L4` (trained arms published and served), then mothballed 2026-09-07 (`03216c5
  braindump: … mothballing section`).
- **Unclosed cycles:** the post-run pipeline and services file consolidation (attractor items 2–3)
  were not finished. Kernel specs (item 1) were done 2026-09-03.
- **Promising:** the 1.5B arm beat the resident everywhere. The `braindump.md` HANDOFF section is
  the documented re-entry point.
- **Human attention:** published-category tradeoffs and Hub licensing ("the base's contradictory
  license fields", `e936606`) are Ember's calls.

### 6.4 `dgem` (OWN, infra)

Scale-to-zero DiffusionGemma (`RedHatAI/diffusiongemma-26B-A4B-it-FP8-dynamic`) on vLLM. A Go
`waker` binary on a small front-door instance (TLS, wake-on-request, 20-minute idle stop) fronts a
`g6e.xlarge` (L40S 48 GB). Everything is in Pulumi TypeScript (`pulumi/{index,network,inference,frontdoor}.ts`).
Design reasoning (README/PLAN.md): FP8 weights ~28 GB ⇒ L40S is the cheapest single AWS GPU that
fits; the default VPC avoids ~$32/month NAT; spot stop ≠ terminate keeps the EBS weight cache warm;
`aws.ec2.SpotInstanceRequest` instead of `Instance+market_options` (provider bug #38142 orphans a
billing instance). Memory: **DEPLOYED and verified end-to-end 2026-06-19**, served via an
sslip.io hostname to work around a DNS delegation mismatch. vLLM OOM fix: `maxNumSeqs=2`,
`gpuMemoryUtilization=0.85`, `expandable_segments:True`, `maxModelLen=262144`.

- **Maturity:** `L4 Deployed` as of 2026-06-19. **Current state unknown** (not checked; doing so
  would touch AWS).
- **Unclosed cycle:** the live box was patched via SSM, so "`pulumi up` will show the inference
  instance wanting REPLACEMENT … triggers a ~25GB weight re-download". Code and infrastructure have
  diverged.
- **Needs Ember's human attention (H-1, highest priority in this strand):**
  1. `dgem` has **no git repo**. The infrastructure-as-code exists only on this disk, with a Pulumi
     **local** backend (`file://~`).
  2. The memory file `dgemma-deploy.md` contains the **endpoint API key and the Pulumi config
     passphrase in plaintext**. Rotate the key; move both secrets out of agent memory.
  3. Confirm whether the deployment (front door with an Elastic IP, plus the GPU instance) is still
     running and billing.

### 6.5 Smaller frontier repos

| Repo | What it is | Maturity | Open loop / attention |
|---|---|---|---|
| `qaa` | Local mirror of the "trash magic / trashbook" self-replicating PHP "organisms" (LafeLabs). `serve.py` reimplements `dir.php`/`fileloader.php`/`load-file.php` read-only with a path-traversal guard; `browse.html` fractal browser; 30 + 26 instances captured 2026-10-04 | `L2` | Owner-authorized **non-destructive** assessment (memory). Findings exist in `SECURITY-FINDINGS.md` (redacted here). Sibling `.art` sites "still to crawl". Reporting the findings back is Ember's relationship ("give the organism an immune system, not amputation"). |
| `starmap` | 4 commits 2026-02-09 → 14: interest/project embedding map (`interests.txt`, `my-projects.txt`, `resummarize-*`, `categorize-taxonomy.py`, frontend) | `L1` | Its memory is mostly unrelated reverse-engineering notes about OAuth headers. **Attention:** auth-header reverse-engineering notes should not migrate into any public artifact. |
| `pauli-Group/Hegemon` | Pauli Group's PQ shielded-payment chain (ML-DSA/SLH-DSA, ML-KEM, STARK-proved Merkle accumulator) | MIRROR | Reference for PQ + STARK design in strands 03/04. 0 Ember commits. |

---

## 7. Cross-cutting synthesis

### 7.1 Maturity roll-up

| Level | Projects |
|---|---|
| `L4 Deployed` | spindle (public game), h (published/served arms, mothballed), dgem (deployed 06-19, status unknown) |
| `L3 Proved/Tested Core` | **graphplay** (sorry-free, 109K Lean lines), **birkhoff-asa** (kernel-checked counts + live prover), stella Rust engine (differential-oracle gated), GLaDOS soundness core |
| `L2 Prototype` | absass cores, intmat2, navier-stokes formalization layer, luteastress, qaa, graphplay ML layer, stella HOL track (scaffolded) |
| `L1 Spike` | RISC-V custom-instruction spike, ergolang, serde-reflect, TranslateOcaml.sml, bead-calculus, starmap, qwen38-probe, assc |
| `L0 Seed/Idea` | gamevm, rustc.js, rhaposPDE |
| `Frozen-for-Rethink` | absass (since 2022-09) |
| `Compost/Superseded` | intmat (→ intmat2), reu_unif, graphplay walkformer (falsified), stella docs/16 §1–6 (superseded by measurement) |

### 7.2 Closed loops worth celebrating (with the commit that closed each)

1. **Theorem caught a misreading.** graphplay `acStep_xor_sound_but_abstains` → clairnets `d2bc512`.
2. **Erratum found and accepted upstream.** NS PR #1 (`dd4b9d9`) → Cambria's ERRATA (`a9a0ce5`) → v002 (`5ececfd`).
3. **Sorry census to zero.** 119 → 85 → 27 → 0 (`3243375`), with three machine-checked refutations
   in place of false claims.
4. **Poll answered with an object.** >10^1000 claimed → 10^5.58 geometry measured; ASA′ closed
   no-cheating (`a04cb89`, `15a2074`).
5. **Analysis predicted the pattern.** intmat2 tied two-shell: predicted `cos k* = 1/(4β)`, measured
   "within a few percent across a hundred rules" (`757e09a`).

### 7.3 Open loops, ranked by leverage ÷ effort

| Rank | Loop | Where | Effort | Why now |
|---|---|---|---|---|
| 1 | spindle catch gap: `ReceiverPredictor` → `trajectory::analytic` | `game/rig-core/src/ai/lead_predict.rs` | hours | Closed form already exists; fixes long passes in a shipped game |
| 2 | SpectralPSTHead multi-seed replication | `graphplay/experiments/codesign_walk/` | 1 GPU-day | The most striking ML result in the corpus rests on 1 seed |
| 3 | `eps_routing_fidelity` + depth stability | `graphplay/Graphplay/Integrations/EpsDynamics.lean` | days | "10-line Cauchy-Schwarz off EpsDynamics" |
| 4 | intmat2 seeded-manifold arm (96/224) and the "individuals" objective | `intmat2/docs/evolution.md` | days | Resume commands written; paused only for load |
| 5 | Non-local GF2-aware branch policy | `clairnets/clair/organ/search.py` | week | Named as the only route to a decisive win |
| 6 | stella §58 circuits faithfulness | `stella/crates/stella-core/src/circuits.rs` | days | A correctly failing test is waiting |
| 7 | absass Lean spec + `assrs` refinement | new | week | An owned ISA as a verified toy CPU for the obend stack |
| 8 | ergolang Δ as a Čech obstruction | `ergolang/` + Lean | week | Connects to graphplay ε-defect and the stella cut |

### 7.4 Human-attention queue (Ember only)

| ID | Item | Kind |
|---|---|---|
| **H-1** | `dgem`: plaintext API key and Pulumi passphrase in agent memory; no git; unknown billing state | Security / cost |
| H-6 | clairnets L40S `i-0496528fc599f8bcb` (us-west-2): confirm terminated | Cost |
| H-4 | `TranslateOcaml.sml` untracked inside an upstream PolyML checkout | Data loss risk |
| H-5 | birkhoff-asa: local main 39 behind origin; 51 worktrees and ~60 agent branches to prune | Hygiene (deletion) |
| H-7 | graphplay outreach: Tamon email, LDT authors, Deco/Kringelbach | Outward |
| H-8 | stella: push dev, publish `/cmi/`, close the ~60 HOL `cheat`s in the main thread | Outward / proof |
| H-9 | intmat `outputs/` 150 GB on a near-full Mac disk | Disk (Ember decides) |
| H-10 | absass co-ownership (Grissess) before any revival or relicense | Relationship |
| H-11 | Local patches in `candle/compute.ml` and `CakeML/cv_translator/eval_cake_compileLib.sml`: intentional or debris? | Substrate hygiene |
| H-12 | Atlas taxonomy: move velato (graphics) and h/dgem/intmat (not math/physics) to their proper strands | Editorial |

### 7.5 Lessons the agents wrote down (verbatim, durable)

- graphplay: "axiom-clean ≠ non-vacuous."
- graphplay: "stale oleans MASK latent breakage."
- birkhoff-asa: "engine proposes, kernel disposes." Three quantities are "never summed."
- stella: "HOL4 proof-closing is a poor delegation fit." "NEVER run two WRITE agents on the same
  crate/dir concurrently." "NEVER use `git commit -m` with backticks/$ — ALWAYS -F a message file."
- h: "extend those instead of adding a fourth thing." "treat a near-empty observatory day as an
  outage alarm, not quiet."
- clairnets: "Negatives are results." (CURSELOG header) "soundness is a permission … cashes out ONLY
  where the boundary check exists" (`6e257a0`).
- Nebula: "never call a genotype risk/protective without anchoring REF/ALT to a population AF."
- intmat: the codex build is the cautionary tale. Every fix became "more accounting on the same
  agent-centric skeleton" (intmat2 DESIGN.md).

---

## Appendix A — Commit index (hashes cited in this strand)

| Repo | Hash | Date | Subject (abridged) |
|---|---|---|---|
| absass | `31a8b46` | 2022-06-26 | ABSOLUTE ASS |
| absass | `4d960df` | 2022-09-16 | assc: Add function declarations |
| velato | `a34e5d0` | 2026-03-28 | fix: position spatial easing … mask modes |
| graphplay | `3a0750a` | — | LDT kind-checker: fix 35-min hang |
| graphplay | `91425c8` | 2026-06-02 | wave-20 capstone |
| graphplay | `0c6fecf` / `2d9256d` | 2026-06-04 | Connectome bridge / connectome energy |
| graphplay | `3243375` | 2026-06-10 | sorry-free (waves 21/21b) |
| graphplay | `822204a` | 2026-06-10 | wave 22: ε-equitable, GQA cert, Tsirelson |
| birkhoff-asa | `bf23609` | 2026-05-15 | asagolf: exact ZFC-grounded size |
| birkhoff-asa | `a04cb89` | 2026-05-16 | ALL 7 BIRKHOFF POSTULATES KERNEL-VERIFIED |
| birkhoff-asa | `15a2074` | 2026-05-17 | ARTIFACT CLOSED — two ZF facts |
| birkhoff-asa | `e351700` | 2026-05-17 | ap-congruence is VERDICT B |
| birkhoff-asa | `910d95a` | 2026-05-17 | Lie bracket globalized |
| birkhoff-asa | `f2c4077` | 2026-05-17 | BOOK 3 wave 1: curvature + Bianchi + gauge |
| birkhoff-asa | `652f33c` | 2026-05-17 | HISTORY Acts XI–XII (local main HEAD) |
| birkhoff-asa | `0976700` | 2026-05-17 | Phase 3c + Phase 4 built (origin/main HEAD) |
| birkhoff-asa | `e693b40` | 2026-05-16 | cse minimizer (checkout HEAD, `elab-combinators`) |
| navier-stokes | `dd4b9d9` | 2026-08-16 | start formalizing the argument (#1) |
| navier-stokes | `5ececfd` | 2026-08-17 | Release v002 |
| navier-stokes | `625c717` | 2026-08-16 | extract unit-torus periodic integration |
| intmat | `32f46d8` | 2026-10-16 | Point README at intmat2 |
| intmat2 | `757e09a` | 2026-10-16 | two-shell tied experiment |
| intmat2 | `58d5f79` | 2026-10-16 | clamp fast tanh to ±9 |
| intmat2 | `1f2b5d8` | 2026-10-16 | partial fragments arm (stopped for load) |
| spindle | `74e0001` | 2026-05-20 | PACK BEHAVIOR |
| spindle | `7f6ac77` | 2026-05-20 | rl::loco learned locomotion |
| stella | `1ea8861` | 2026-05-18 | unify_fast dense-arena union-find |
| stella | `a13da70` | 2026-05-18 | CI test-gate + unified oracle harness |
| stella | `cb6cace` | 2026-05-19 | wasm-safe KS clock shim |
| stella-suite | `94229c3` | 2026-05-17 | Cut the incantatory register |
| clairnets | `6e257a0` | 2026-06-27 | soundness-language audit |
| clairnets | `79efba7` | 2026-06-28 | THESIS TEST (Finding 3) |
| clairnets | `d2bc512` | 2026-06-28 | RE-GROUNDING |
| clairnets | `38057c6` | 2026-06-28 | RESTORE the DPLL SEARCH leg |
| clairnets | `ffe2fae` | 2026-06-28 | GUIDED SEARCH |
| h | `d76b3fb` | 2026-09-06 | First cooled 1.5B |
| h | `91ca477` | 2026-09-07 | Reclaim 81 GB |
| h | `55d9e00` | 2026-09-07 | braindump: both trained arms served |
| group-approximation | `a4e3a1126` | 2026-09-07 | GGT: boundary circuits from face-set permutation |

## Appendix B — Memory files read for this strand

```
~/.claude/projects/-Users-ember-dev-graphplay/memory/        (17 files: MEMORY, equitable-walk-arch, eps-program,
                                                               novelty-and-next-phase, ml-findings, connectome-bridge,
                                                               ldt-theory, sorry-census-2026-06-09, sorry-free,
                                                               certified-honest-floor, headline-verification-rule,
                                                               restrans-suite-is-junk, tino-outreach, …)
~/.claude/projects/-Users-ember-dev-birkhoff-asa/memory/     (MEMORY 37 KB, birkhoff-asa-state 31 KB,
                                                               transport-anchored-floor, website-prover)
~/.claude/projects/-Users-ember-dev-stella/memory/           (project_stella 64 KB + 10 feedback/reference files)
~/.claude/projects/-Users-ember-dev-intmat/memory/           (intmat-codex-takeover, intmat-direction, intmat2-day1-state)
~/.claude/projects/-Users-ember-dev-silicon/memory/MEMORY.md
~/.claude/projects/-Users-ember-dev-spindle/memory/          (+ -Users-ember-pug-simbi project_ember_{spindle,stella})
~/.claude/projects/-Users-ember-dev-h/memory/                (12 files)
~/.claude/projects/-Users-ember-dev-clairnets/memory/        (+ -Users-ember-dev-gowexp/memory/clairnets-project.md)
~/.claude/projects/-Users-ember-dev-dgem/memory/             (contains secrets — see H-1)
~/.claude/projects/-Users-ember-dev-{qaa,starmap,luteastress}/memory/
~/.claude/projects/-Users-ember-SauersML-group-approximation/memory/
~/.claude/projects/-Users-ember-Documents-Nebula-Genomics/memory/   (read; contents redacted)
```

Directories in the brief with **no memory files**: `-Users-ember-dev-graphplay-research-looped-arch`
(project dir only), `-Users-ember-dev-clairnets-qwen38-probe` (project dir only).
