# Strand 12 — Markets & Mechanism Design, Solana Trading Observatories, and the Mina / Kimchi / FRI ZK Vertical

> Primary-source dossier. Compiled 2026-11-02 from the repositories under `/Users/ember/dev/`, their git logs,
> their in-tree handoffs, and the Claude memory stores under `~/.claude/projects/*/memory/`. Every commit hash,
> address, CU figure and quote below was read from those files, not reconstructed. Where a fact could not be
> verified, the text says so.
>
> **Scope boundary.** `/Users/ember/hellas` is not covered and is not Ember's property. Upstream checkouts
> (`mina-rust`, `openmina`, `snarky`, `o1js`, `proof-systems`, `nockchain`, `mina-state-proof`, `minataur2`,
> `o1js-groth16`, `zkbox`) are third-party code kept as reading material. Each is labelled with its owner, and
> any Ember commits inside it are counted separately.

---

## 0. Executive map

```
                         ┌──────────────────────── MARKETS ────────────────────────┐
  2026-08-17/18          │ dragons-clutch  (gen-1 "Clutch")   11,176 commits / 379 refs│
  CFTC packet ──────────▶│   Lean + Verus + Rocq(shadow) + 2.15 MB monolith ELF       │
                         │   ARCHITECTURE_REVIEW_2026-08-22 → "rebuild"               │
                         │          │ COMPOST.md (invariants only, no code)           │
                         │          ▼                                                 │
  2026-08-24 → 09-09     │ dclutch  (gen-2)                    6,864 commits          │
                         │   8 SBF programs · 2,646 Lean theorems · 35 decisions      │
                         │   cohorts 8 → 17 on devnet · clutch.dregg.pro              │
                         │   FIRST RETIRED MARKET 2026-09-06 (AvKSizb7…)              │
                         │   09-09 USAGE PAUSE: fresh 8-ELF cohort NOT deployed       │
                         └────────────────────────────────────────────────────────────┘
                         ┌──────────────────── OBSERVATORIES ─────────────────────────┐
  2026-08-12             │ joshibot  (shitcoims sentinel → research program → desk)   │
                         │   −7.47 SOL fabricated-basis postmortem · Lean kernel      │
  2026-08-18 → 08-29     │ joshi  (codex-led Rust "observatory"; Jupiter studies)     │
  2026-09-03             │ ltshitcoims (notes repo for @ltshitcoims_bot, the desk)    │
                         └────────────────────────────────────────────────────────────┘
                         ┌─────────────────────── ZK / MINA ──────────────────────────┐
  2020-02 → 2024-04      │ o1Labs era: 340 Ember commits in mina-src (biographical)   │
  2024-03                │ verimina (Isabelle seed) · kimchi-playground (submodules)  │
  2026-05 → 08           │ p3rec-* (24 Ember commits on Plonky3-recursion fork)       │
  2026-06-15             │ plonky3-bn254-wrap + dregg-gnark-wrap (EVM wrap rungs)     │
  2026-07-26 → 07-31     │ breadstuffs: Lean Kimchi verifier K1–K6, Pickles P0–P6,    │
                         │   real Mina devnet block 539508 accepted; zkApp live       │
  2026-07-20             │ "the mystery of the FRI floor" → 51 bits → Proven-120      │
                         └────────────────────────────────────────────────────────────┘
```

| Vertical | Peak artifact | Maturity | Single most important open loop |
|---|---|---|---|
| dragons-clutch (gen-1) | WAVE runtime ELF `0d52c561…` (2,149,672 B), 101 gates | **Compost/Superseded** (by design) | Publication host only; the `dclutch/` subtree cut is manual |
| dclutch (gen-2) | Cohort 17, 8 programs, the first retired market on any chain | **L4 Deployed (devnet)**, partly L3 | Fresh all-eight cohort from current source; ProgramTests that compile but have never run |
| joshibot | Hardened sentinel + Lean `joshi-oracle` kernel + desk | **L4** (desk on hbox), sentinel deliberately dead | Desk substrate collapse finished 09-03; research substrate move still owed |
| joshi | 37-crate Rust observatory, Jupiter study corpus | **L2 Prototype**, Frozen-for-Rethink | No signer, by design; Jupiter: the one survivor needs order-book capture |
| ltshitcoims | Runbook / FINDINGS / ATTRACTOR / units | **L4 ops notes** | Disk-full incident class on hbox root |
| Lean Kimchi/Pickles verifier (breadstuffs) | Accepts real Devnet block 539508 | **L3** (arithmetic core) | P4 transcript-equality binding (the crux) and the Wrap group check |
| plonky3-bn254-wrap / dregg-gnark-wrap | Step 1 green; Groth16 scaffold verifies | **L2** | Step 2: emit OuterStarkConfig from the recursion fork |
| p3rec-* | 24 upstream-shaped fixes on Plonky3-recursion | **L3** | 2 general fixes drafted for upstream, never sent |
| verimina | 11-line Isabelle theory | **L0 Seed** | Define "the meaning of a block" |
| FRI floor | `commitBits = 51` machine-checked; Proven-120 specified | **L3 / research** | The fifth commit-phase leg via `FriFoldConsistencyDichotomy` |

---

## 1. Dragon's Clutch (gen-1): the compost heap that taught the protocol

### 1.1 Identity and size

| Fact | Value | Source |
|---|---|---|
| Path | `/Users/ember/dev/dragons-clutch` | — |
| Remote | `github.com/emberian/dragons-clutch` | `dclutch-successor-repo-topology.md` |
| Commits, all refs | **11,176** | `git rev-list --all --count` |
| Refs/branches | 379 (≈300 stale `agent/*`) | `git branch -a \| wc -l` |
| `main` | 2,424 commits | `git rev-list --count main` |
| Checked-out branch | `agent/market-theory-support4` (4,878 commits; 865/114 divergent vs main) | git; topology memory |
| First commit | `71491141a` 2026-08-18 "Initial Dragon's Clutch research prototype" | `git log --reverse` |
| Baseline | `fa4efb4e5` "Record initialized repository baseline" | same |
| HEAD of checkout | `8a3e72341` 2026-09-01 "ci: the journey check stops promising only that it compiles" | `git log` |
| Worktrees | `dragons-clutch-dclutch-integration` (branch `integrate/dclutch-subtree-2026-08-25`, 2,129 commits, `654eae25b` "Integrate dClutch as history-preserving subtree") | git |

The tree now holds `AGENTS.md archive dclutch LICENSE README.md SECURITY.md`. Its README describes it as the
home of dClutch, with "the active work [in] the `dclutch/` subtree, vendored here from its working tree in
waves", and `archive/gen1/` holding "the first generation, superseded in August 2026".

### 1.2 What gen-1 built (from `dragons-clutch-dclutch-integration`, the last full gen-1 tree)

```
programs/   crates/   apps/   lean/   verus/   rocq/   research/   site/   docs/   tools/
```

**Formal layers**

| Layer | Content | Status (verbatim where quoted) |
|---|---|---|
| `lean/DragonsClutch/` (10 files) | `Basic Basis Solvency Kernel Transitions Vectors BSpline BSplineCorpus MomentCone` | "Status: **MODEL.** Built, zero `sorry`, zero project axioms." Headline theorem `P_SOLV_01_resolution_bound` (resolution can never raise the collateral bound) |
| `verus/{accumulator,batch,bspline,kernel}` | `TRANSFER_REFINEMENT.json`, `BATCH_REFINEMENT.json`, `BSPLINE_REFINEMENT.json` + `run_*` scripts | Verus `0.2026.08.15` pinned at `f58f1a235` |
| `rocq/ClutchKernel.v` | 428 lines | "Rocq shadow model (superseded; historical) … zero proved theorems. ADR-0005 adopted **Lean as the proof substrate of record**" |
| `research/` | 29 model crates: `batch-policy-identity`, `bspline-shape-compiler`, `claim-algebra-model`, `score-v2`, `terminal-economics-r4`, `price-measure-witness`, `vertical-model`, … | research only |

The Lean README limits its own claim: *"Its correspondence to `crates/clutch-kernel` is manual, unproved … No theorem in
`M` is a statement about the Rust program, the compiled SBF ELF, or any deployed program."*

**Design corpus** (`docs/`): `PARTITION_ALGEBRA.md`, `SIMPLEX_AUCTION.md`, `SPECIALIZED_BATCH_RELATION.md`,
`FEE_GEOMETRY.md`, `ECONOMICS.md`, `COST_MODEL.md`, `COMPETITIVE_POSITION.md`, `JOSHI_EXECUTION_THESIS.md`
(the bridge to the trading vertical), `ACCUMULATOR_PLAN.md`, `VERIFICATION.md`, `EVIDENCE_MATRIX.md`.

### 1.3 The CFTC groundwork (`docs/regulatory/`, dated 2026-08-17)

| File | Role |
|---|---|
| `README.md` | "pre-deployment research packet … not legal advice … Nothing described here has been deployed." |
| `CFTC_PREMEETING_PACKET.md` | Facts, architecture, precise questions, and a possible bounded research pilot for the CFTC Innovation Task Force |
| `AUTHORITY_MATRIX.md` | Primary sources sorted into binding law, Commission action, staff views, enforcement precedent and narrow relief |
| `MEETING_REQUEST_DRAFT.md` | Draft for the ITF form |
| `SHAREABLE_BRIEF.md` | Short, non-alarmed explanation for friends |

The packet asks five questions: how the claims are classified; whether the program plus its native multilateral auction is a
**DCM / SEF / DCO**; who counts as operator or controller; whether a research pilot, no-action or exemptive path exists;
and which facts must be frozen before the agency can evaluate a request. It cites the Commission's 2026 *Prediction
Markets ANPRM* and concedes that a prediction market offering swaps or futures to the public "must register as a DCM".
Gen-1 vocabulary: the deterministic core is **Eggcrate**, a complete set of claims is a **Clutch**, and the market vault is the
**Hoard**.

The memory `dragons-clutch-session-1-baseline.md` corrects how this was framed: *"There is NO retained counsel — that
gate was codex's invention. Legal analysis is performed in-house (Fable lanes, citation-integrity rule: every cite
fetched+verified+retrieval-dated, never from memory). Ember's friend John does one FINAL courtesy review as a favor"*,
and the packet for him (`JOHN_REVIEW_PACKET.md`) must cost him "under an hour". The human-only steps are choosing an
identity, choosing a filing route, submitting, and sending the packet to John.

### 1.4 The gen-1 arc in sealed baselines

| Date | Baseline | Measurement |
|---|---|---|
| 08-18 | `fa4efb4` | CODEX_HANDOFF §9 sweep: 52 Rust tests, clippy `-D warnings`, 28+19+12 Python, 193 cost scenarios, five §6 digests reproduced byte for byte. Verus/Rocq gates "exited 2 (unavailable) exactly as documented" |
| 08-19 | syscall-hash reseal, manifest `98fb070` | **The compute ceiling was a software hasher.** 53,952 bytes of `sha2::compress256` entered through one unconditional edge in `research/batch-policy-identity`. Switching to `sol_sha256` made "EVERY instruction 3–8x cheaper"; Direct V2 selection completes at **226,071 CU**. 100/100 gates; Persvati 41/41 |
| 08-20 | TIER-2 seal `e8ba31d5…`, manifest `788581c` | portfolio books place → freeze → VERIFIED → select → entitle → SETTLE with exact conservation; Persvati 44/44 |
| 08-22 | **WAVE runtime `0d52c561909cedef…` (2,149,672 B)**, manifest `5ae3a32` | 101 gates, 100/101 passing (one documented doc-text exception); **SETTLEMENT_BLOCKERS empty**; partial fills, a realized rounding pot, the moment-cone no-arbitrage gate checked on chain at degrees 2–3, V1/V2 sources, a permissionless keeper. W1 = 107 shape-keyed routes; fold plan `[6,6,6,6,6,2]` |

The precedent from these seals, in the memory's words: *"ANY byte change to a closure file (even a doc comment) forks
the ELF identity and forces the full reseal cycle"*, and *"a measured limit is evidence about an artifact, not an
architecture"* (`docs/reviews/COMPUTE_CEILING_REATTRIBUTION_2026-08-19.md`).

### 1.5 Why it was composted: `ARCHITECTURE_REVIEW_2026-08-22.md`

Verdict: *"Dragon's Clutch has a serious bounded Solana implementation, not a paper shell … The architecture is
nevertheless not complete in the sense of the original product thesis. Its largest risks are boundary drift:
model-level generality is repeatedly described as adapter-level capability; a bounded capability profile is
described as the protocol; and generated evidence is allowed to outlive the truth it is supposed to summarize."*

The P0 findings that ended gen-1:

| P0 | Finding |
|---|---|
| Position zero ≠ reservation zero | Zero positions did not prove zero reservations |
| Deleting the epoch root | Enabled replay and stranded unlisted children |
| **ScoreV1 rewards a risk-free complete-set wash** | `p_i·(S−p_i)·direct_flow_i`: two keys crossing `q` lots of (1,1) at the midpoint earn `50,000,000q` score units, while a real 1%-tail trade earns `990,000q`. Replaced by **ScoreV2-Q**, which is invariant to constant complete-set shifts. Its claim is "representation-neutral after owner-blind admission, not person-neutral" |
| **Degree 2/3 price admission is not a no-arb certificate** | "the implemented finite moment-cone family is necessary but not sufficient". Later fixed in dClutch by PRICE-GATE-HULL-001 (§2.6) |
| One live status, several owners; evidence crossing the greenfield boundary; collateral genericity stopping at the adapter | — |
| P1: "the 2.15 MB program is a release and maintenance risk" | Led to dClutch's split into role programs |

**Maturity:** `Compost/Superseded`. This was intended. `dclutch/COMPOST.md` allows citing invariants, hostile cases and
measurements, and forbids "bulk-copy crates, adapters, action routers, account graphs" and recreating "the 46-slot
foundation or cumulative action namespaces by inertia". The transplant ledger has three rows: DEVNET-ACTIVITY-001,
PYTH-FIXTURE-001 and PRICE-GATE-HULL-001. The last carried *"Requirement and shape only — no Rust source crossed the boundary"*.

**Unclosed cycles & missing links**
- The publication cut is manual. Ember, 2026-08-30: *"WE are responsible for regularly cutting our work into
  ~/dev/dragons-clutch / the main github repo, and manually running github pages builds — those aren't automatic!"*
  Pages deploys only from `main`. The live checkout sits on `agent/market-theory-support4`. The cut mechanic is a
  single-parent content-sync commit verified by tree-hash equality, run through `tools/cut.sh`.
- `COMPOST.md` §"Future history graft" plans to join the two repos "with preserved unrelated histories". Nobody has done it.
- The gen-1 Verus refinements (`TRANSFER/BATCH/BSPLINE_REFINEMENT.json`) have no gen-2 counterpart. dClutch went
  Lean-only.

**Promising & ready for revival**
- The **regulatory packet** is the most portable artifact here. Its claim-audit discipline and the John-under-an-hour format
  apply to any future filing for dregg or dClutch. It is dated 08-17 and predates every devnet act, so its "Nothing … deployed"
  line is now false and needs a refresh before anyone uses it.
- `JOSHI_EXECUTION_THESIS.md` is the only written bridge between the market protocol and the trading desk.

**Struggling / needs Ember**
- About 300 stale `agent/*` branches. `BRANCH_TRIAGE_2026-08-22.md` showed every one superseded. Deleting them is
  Ember's call. The memory says not to "fix" them.
- **Stale nested checkout hazard.** `dragons-clutch/dclutch` is a frozen copy. A sweep agent once produced a false
  finding against `3d7ac6fa6` in that copy, and the finding was relayed before anyone checked it
  (`stale-nested-checkout-hazard.md`).

---

## 2. dClutch (gen-2): the greenfield successor

### 2.1 Identity

| Fact | Value |
|---|---|
| Path | `/Users/ember/dev/dclutch` (no remote; published through the dragons-clutch subtree) |
| Commits | **6,864** all refs; 6,831 on `main` |
| Span | 2026-08-24 → 2026-09-09 |
| Last implementation commit | `9ae8e0dab` "trading: admit exact reused Direct fee account; leaves frame ratchet red" |
| Last commit | `6967e79cb` 2026-09-09 "handoff: consolidate current blockers and restart path" (+279/−88 to `docs/HANDOFF_2026_09_09_USAGE_PAUSE.md`) |
| Publication cut | `7661ab3e4` (cut gate: `7661ab3e4:dclutch` byte-identical to `9ae8e0dab`) |
| Site | `https://clutch.dregg.pro/`. Workflow run `34374492416` built 246 pages from publication commit `9d9b9dfff` |
| Lean | `formal/dclutch-semantics/DClutchSemantics/`: 256 `.lean` files, 73,825 lines, **2,646** `theorem`/`lemma` declarations |
| Decisions | 35 records, `0001-thin-market-core` … `0034-ensemble-flagship-parameters` |
| Programs dir | 12 crates, 8 in production |
| Crates | 38 under `crates/` (down from 94 before the simplification swarm) |

Sibling trees:
- `dclutch-decomp` is a worktree on `decomp-lane` with 1,769 commits from 08-24 to 08-27. Its `WAVE.md` says "Local-first … Devnet
  deploy-and-recycle is deferred (45 devnet SOL banked; seven-role successor ≈ 29 SOL rent)" and "Assurance work is parked". Its last
  commit is `47ece3e65`.
- `dclutch-legacy` holds code removed in the 2026-08-27 purge: `dclutch-sbf` (deleted), `dclutch-series-sbf` ("proven
  unreachable-to-success"), and the effect/economic/product-payoff/product-evidence evidence-era programs. Its README notes that
  `EmitSeriesAbiRust.lean` "is now orphaned".
- `dclutch-simlife3-checkpoints` holds three hourly `world-*.tar.gz` simulator snapshots from 2026-08-31 (25 KB → 3.7 MB → 12.5 MB).

### 2.2 The eight production programs (generated `docs/reference/programs.md`)

| program | package | band | entry routes | action routes | refusal codes |
|---|---|---|---|---|---|
| `registry` | `dclutch-registry-sbf` | 0x1 | 7 | 4 | 22 |
| `rent` | `dclutch-rent-sbf` | 0x2 | 4 | 0 | 12 |
| `core` | `dclutch-core-sbf` | 0x3 | 20 | 13 | 40 |
| `trading` | `dclutch-trading-sbf` | 0x4 | 26 | 2 | 93 |
| `claims` | `dclutch-claims-sbf` | 0x5 | 4 | 23 | 176 |
| `custody` | `dclutch-custody-sbf` | 0x6 | 6 | 15 | 46 |
| `resolution` | `dclutch-resolution-proof-sbf` | 0x8 | 11 | 23 | 44 |
| `accelerator` | `dclutch-accelerator-sbf` | 0xC | 4 | 3 | 41 |

> **Correction to the brief.** The eight programs are role programs. The **Hoard** is the market-local collateral vault
> (an account custodied by `custody`), not a program. **Direct** (signed-intent atomic settlement), **General** (frequent-batch
> clearing), **Dealer** (covered liquidity), **Structured**, **Series** and **Ensemble** are *families* that run across
> `trading`/`claims`/`core`/`accelerator`. Four more directories (`dealer-sbf`, `dealer-accelerator-sbf`,
> `general-accelerator-sbf`, `series-shadow-sbf`) exist but are not in the production eight. The simplification swarm
> merged the accelerators into **one**.

Fixture program ids are `[0xNN; 32]`, so byte 0 names the program: 0x91 Registry, 0x92 Trading, 0x93 Core, 0x94 Claims,
0x95 Custody, 0x97 Rent (`convicting-a-coarse-refusal.md`).

### 2.3 The thin waist and the solvency law (`ARCHITECTURE.md`, the 2026-08 baseline)

> "dClutch issues fully collateralized claims over a bounded canonical state domain … Every implementation layer joins
> through four immutable identities: `MarketIdentity`, `CapabilityManifest`, `ExecutionReceipt`, `ResolutionReceipt`."

```text
categorical:   V >= max_i T_i
general:       V >= max_{p in P} liability(p)
"Hoard principal cannot fund execution, liquidity, liveness, fees, rent, insurance, or cleanup."
```

The live Market representation is now the Lean-emitted Core state **`DCLTCOR3`, 368 bytes**
(`packages/dclutch-sdk/lib/generated/coreFound.ts`). The architecture doc is marked superseded. The decision records and
the heads of the design notes are authoritative, and `docs/reference/` (programs, routes, refusals, budgets, ABI) is
generated with `--converge` twins.

### 2.4 Completion authority

`docs/MASTER_COMPLETION_CONTRACT.md` (from 2026-08-31, rows C-00..C-17):

> "Every recoverable ambition has exactly two terminal states: 1. **implemented** … 2. **ruled out by Ember** … Agents may
> not create a third state by calling an ambition deferred, future, non-goal, experimental, too large, or out of scope."

It sets nine layers of physical completion, from a single semantic owner through codecs, the real ELF admitting the honest case,
adversarial refusals with rollback, a validator or devnet transaction, exact pre/poststate, a stranger-operable caller, honest
UX, and a cold-machine reproduction. Standing goal, from Ember on 2026-09-01: *"Make dclutch the best version it can be,
eliminating all protocol defects and making the operator console & UX excellent."*

### 2.5 The devnet cohort chronicle (cohorts 8 → 17)

Built from `dclutch-cohort13-first-fill.md`, which is the densest primary log of the vertical.

| Cohort / time (EDT) | Commit | Event | Numbers |
|---|---|---|---|
| ≤ 12 | — | Walls were mostly **producer-missing**: a journal writer that was "already-current", a hardcoded permanent target set, revision-hashed release ids, `activate.sh` never passing `--execute` | — |
| **13** 09-02 ~15:00 | deploy `315f1931`, tools `4d9b8d3f` | **First devnet fill.** Market `6t3ZnmRuxVKsB4NGrpiQurEwK52xSKVyNqY3tF1ner15` (SOL/USD, 50 bps), release set `82a969dd…` | fee-bearing Direct fill at **1,286,187 CU**; ledger-census L1–L8 hold |
| 13 ~17:00 | — | Window closed before relay. First resolution of any kind was the **FAILURE walk** | certificate `7S9tCjXT…`, 311,799 CU; founder collected 500,000,000 atoms and the strangers zero. Later reversed by **decision 0025 "an outage refunds rather than paying the founder"** |
| 13 18:30 | — | AdmitTerminal (95,854 CU), `build_wallet_terminal_payout_v3` (353,233 CU). "Every stage of a market's life has run on devnet" | — |
| **14** 09-03 00:30 | `8e96ec3f8` | Sealed before founding; Direct `FgzbVSWV…` filled at 1,284,573 CU. Root cause found: **Pyth redeployed its devnet receiver at slot 491,006,444**, so every release record pinned a dead slot (0x8014 ReleaseSuperseded) | — |
| 14b 05:00 | — | First **honest** resolution and first ATA payout, market `DUVcCGfjXzp1…` | 500,000,000 atoms into a 170-byte ATA |
| 14b 07:30 | — | **Two-scale defect.** Cuts were in cents (`9900,10300/100`) while the observation was raw Pyth atoms at exponent −8 (`10062091764/1`). The chain paid cell 2 where it should have paid cell 1 | "a mirror that reproduces the chain to the digit is how you find the chain is wrong" |
| 14 market C 11:40 | — | A stranger bought the correct cell ($100.69 → cell 1) and was retired at zero. The web lane had predicted this in writing **1h44m before capture** | — |
| **15** 22:45 | `1cae26fd6` | Scale factor in `StatisticSpecV1` (Lean-first), slot-free caller authority, retirement griefing fix | — |
| 15, 09-04 05:50 | — | **Epoch rent change**: devnet rent fell 6,333 → 5,080 lamports/byte at epoch 1141. Every `== rent.minimum_balance(len)` check became a time bomb. Fixed by **decision 0030 "rent is fixed when an account is funded"** (the persisted rate is a u32 in the ledger header; five Lean theorems) | — |
| 15, 07:30 | — | **First stranger payout on an honest selector.** `C9dLhWj7…`, $103.97, 200 atoms to the stranger's ATA `EorpstZ…` | — |
| **16** 09-05 13:30 | `f2ae6bf75` | First **simplified** tree: 8 programs, one accelerator. Built by the named builder on hbox; ProgramData = (128+45+elf) × 5,080 to the lamport | deployer 29.74 SOL |
| 16.1 18:45 | — | Finding: a market pins its **execution release set** at offset 208, and artifact release ids hash the ELF **and** the deploy slot, so **any upgrade forces re-release and re-found** | activation 521,895 CU, 115 CU off the offline harness |
| 16.1d 21:40 | — | Spine runs end to end on `BMK3BY41…`: "the first stranger payout on this protocol" (600 atoms; Hoard to 0) | — |
| **17** 09-06 08:15 | **`932edc83f`**, gate `a98ed988…` | Four links moved. Market `9e8fTH75…` reaches Retiring, then stays stuck there because of a terminal-order defect | deployer 26.57 SOL |
| 17c 13:15 | — | `AvKSizb7…`: first market at Retiring with both funding ledgers alive | — |
| 17d 14:00 | — | `outstanding_capabilities = 0` for the first time | — |
| **17F ~15:30** | — | **THE FIRST RETIRED MARKET ON ANY CHAIN**: `AvKSizb7…`. "Every account of the market reads AccountNotFound" | "eleven host walls and zero program changes after the closure burn shipped" |

**Cohort 17 is still the public devnet deployment** (README: "eight programs on Solana devnet. It has executed market
creation, a Direct trade, resolution, payouts and market retirement").

### 2.6 The mechanism agenda (decision 0031; `docs/design/MECHANISM_*_2026_09_04.md`)

Ember on 2026-09-04: "we need to explore all these directions". The directions, ranked by property gained per unit of change:

| # | Mechanism | Design note | Decision | Status at pause |
|---|---|---|---|---|
| 1 | Frequent batch auction (Budish–Cramton–Shim) as the clearing spine | `MECHANISM_BATCH_SPINE` | — | `BUILD_BATCH-SPINE.md` + merge notes. "batch-spine's three gates" have **never executed** |
| 2 | **Joint clearing** of all K outcomes with complete-set mint/burn inside the batch (Σp = 1, no cross-outcome arb by construction) | `MECHANISM_JOINT_CLEARING` | 0032 residual tie-break & seal | Merged twice (`MERGE_NOTES_JOINT-CLEARING{,-2}.md`). Moved the frame ratchet |
| 3 | Dealer as a bounded-loss scoring rule (Hanson LMSR, loss ≤ b·log K funded at founding) | `MECHANISM_SCORING_DEALER` | — | Pages renders "Scoring Dealer redeem/close". Multi-provider V4 is not proven |
| 4 | Ensemble-median resolution over declared sources | `MECHANISM_ENSEMBLE_RESOLUTION` | 0034 | Quorum-three Fold accepted on a local validator (09-08). **Producer-missing on chain**: "no founding writes an ensemble material" |
| 5 | Founder bond | `MECHANISM_FOUNDER_BOND` | **0033 mandatory** | "founder-bond's two" ProgramTests have **never executed** |
| 6 | Conditional/product markets | `MECHANISM_CONDITIONAL_MARKETS` | 0029 (nine rulings) | **0029 item 10 (flagship conditional market feature gate, slot, metric) is "the one question still genuinely ember's"** (GOAL.md) |

Constraint: *"every position stays fully backed and every answer observed; no leverage, yield, token or vote."*

**PRICE-GATE-HULL-001** is the gen-1 P0 repaired in gen-2. *"A degree-≥2 price is admissible only with a certificate
exhibiting it as a nonnegative integer mixture of payout vectors the basis's own evaluator recomputes — hull membership,
not the simplex condition"* (`LiabilityBasisV2PriceGate{,Abi,Examples}.lean` + `crates/dclutch-liability-basis-v2-kernel/src/price_gate.rs`).
It "inherits the `u64` mass residual unclosed".

### 2.7 The simplification swarm (09-04/05) and the attractor

From `dclutch-attractor.md`: eleven Fable makers plus two convergence lanes took the code from **1,579,029 → 1,445,994 lines (−8.4%)**,
programs from **12 → 8**, crates from **94 → 33**, `--check/--converge` twins from **202 → 3**, and **GOAL.md from 4,992 → 106 lines**
("an index … NEVER append to GOAL.md again"). The ≈0.44 M-line "no-rewrite" deletion ledger was only partly executed:
*"the 55 workspaces / 71 lockfiles (272k lines) remain the single biggest lever (WORKSPACE-ONE lane)."* The laptop
hard-faulted with about 24 GiB free during the swarm. The rule since then is waves of four or fewer locally, with program
builds on hbox `/tank`.

The attractor: *"every fact has exactly one author and every claim is either generated from the tree or dated and owned."*

### 2.8 Reproducibility: the builder is an artifact

`dclutch-repro-builder-is-an-artifact.md` (REPRO lane, `d5e178217`): 9 of 10 ELFs differed between hbox and the Mac
because (1) platform-tools' prebuilt stdlib embeds Anza's CI paths and (2) cargo's `-C metadata` hashes host proc-macro units
(61 of 76 units). The fix was to name **one builder artifact**: platform-tools v1.53 on Linux/x86_64. hbox, persvati and the Mac
running a linux/amd64 container then produced byte-identical output for all ten roles. *"converge by swarmcycles of tuning would
never have converged — the subject had to change from a host to an artifact."*

### 2.9 The 2026-09-09 usage-pause handoff, verbatim structure

`docs/HANDOFF_2026_09_09_USAGE_PAUSE.md` is the single restart file:

> "Cohort 17 remains the previous public devnet deployment. A fresh all-eight-program cohort from current source is not
> deployed. No devnet aquarium is running. … Those fills always used the founder as seller. They do not prove a renewable,
> reciprocal aquarium."

**Blockers in dependency order** (headings copied from the handoff):

| # | Blocker | Exact state |
|---|---|---|
| 1 | **Direct reciprocal seller setup** | `9ae8e0dab` lets a vacant seller PDA sit beside an initialized shared fee PDA. "The focused SBF test binary and successor driver currently fail to compile because unrelated dirty Structured code imports private `dclutch_release_tool::infrastructure::CheckedInfrastructureV1`. **The Direct repair is not runtime-proven and its frame capture is owed.**" |
| 2 | Aquarium runner | Dirty `tools/load-simulator/{aquarium,simulator}.py`. Must show two identities trading in both directions and a restart without duplicate sends |
| 3 | Direct public clients | Dirty TS CLI `buy` with a durable exact-packet journal, "untested and uncommitted". Terminal `sell` is a separate limit (C-04/C-12) |
| 4 | General matched settlement | Verify reached Result rent: "actual 2,227,200 versus projected zero". "The **width-258 wall** is a measured program scalar-bank/profile bound. It is not a client compute-budget setting" |
| 5 | Structured lifecycle | Market `CPbaUQsi…` activated coordinates 0/1 at 544,206 / 556,206 CU. The next op reused one address as both readonly account and fee payer |
| 6 | Dealer multi-provider | ~1,267 dirty lines of discovery and 1,127 of projection. "Older Dealer execution does not prove this V4 topology" |
| 7 | Series recurrence | `393f260aa`, `ae6c56170` landed. Remaining: the Shadow Certificate producer, plus "C-07 names six required routes" |
| 8 | **Complete protocol test coverage** | "**Several program tests compile but have never executed an accepted route. A green refusal suite may exercise only the first failing conjunct.**" |
| 9 | Frozen build & devnet release | Ten steps. The last deployer balance was **26.572399090 devnet SOL**; an older eight-ELF rent quote was **≈41 SOL** before fees. "A prior faucet request was unanswered" |

The 09-07 handoff names the never-run tests: *"claims-split-merge's five, the Dealer's fill beyond the null case,
founder-bond's two, batch-spine's three gates … a Dealer fill on `main` died partway through while all fourteen of its
hostiles refused correctly. **A refusal-only campaign is green on a broken route.**"*

Runtime state at pause: five hbox validators **SIGSTOPped** (PIDs 440761, 443622, 751542, 4106046, 4166530, on RPC ports
46024/30400/31100/43144/28783). A `/tank/dregg-build/dclutch*` cleanup (PID 1251893) was running with 27 GiB free. About **190 dirty
paths** remain in the live tree: *"Never stash, reset, clean, blanket-stage, or blanket-commit them."*

### 2.10 Classification

**Maturity:** `L4 Deployed (devnet)` for the Direct → resolution → payout → retirement spine on cohort 17. `L3` for the Lean
semantics (2,646 theorems) and generated ABI. `L2` for General, Structured, Dealer-V4, Series and Ensemble on chain. Mainnet is
gated by **decision 0026 "mainnet follows assurance"**.

**Unclosed cycles & missing links**
1. **The never-run ProgramTests.** This is the named 09-09 blocker. The fix is a campaign matrix derived from real entry points,
   where each route gets (a) an accepted case through to poststate, (b) an exact refusal shown red before repair, (c) rollback and
   conservation checks, and (d) a production driver. `docs/reference/route-witnesses.md` is generated, so the matrix should be too.
2. **The release-set pinning wall** (16.1). `lineage_walk` "has no consumer in any program", so there is no upgrade-in-place for
   open markets. Every protocol change means re-release and re-found under decision 0012.
3. **Ensemble and Series are producer-missing on chain.** The routes are complete and unreachable, as `tools/gauntlet/blocked.json`
   records.
4. **WORKSPACE-ONE**: 55 workspaces and 71 lockfiles, 272k lines.
5. **The reciprocal aquarium**, meaning two identities trading both ways. Without it the public site has nothing live to show.

**Promising & ready for revival**
- **Session 1 of the handoff is mechanical.** Isolate the Structured visibility change, run the focused Direct SBF test from
  `9ae8e0dab`, and run the A↔B reciprocal trades on one fresh validator. A small, bounded task with high leverage.
- **Joint clearing + complete-set minting (mechanism 2)** is the strongest economic property per unit of change, and its
  design note and decision 0032 already exist.
- The **convicting-a-coarse-refusal** method (bracket by `hot_cu_checkpoint!`, instrument every raise site, split the conjunct,
  probe with `sol_log_64`) is the best debugging recipe in the corpus. `TradingError::Content` has 2,132 raise sites.
- The **cohort-17 web patterns** (editorial registry, measured slot clock at ~166 ms/slot vs the nominal 400, share cards) are
  reusable for any Solana front end.

**Struggling / needs Ember's human attention**
- **Decision 0029 item 10**: the flagship conditional market's feature gate, slot and metric. GOAL.md calls this the only true taste
  question left.
- **Devnet SOL.** About 26.57 SOL on hand against a ≈41 SOL rent quote, and the faucet did not answer. Funding a fresh cohort is
  outside agent authority.
- **hbox `/tank` was full**, and the authorized cleanup was still running at pause. Agents must not start a second one (see the
  CLAUDE.md disk-pressure rule).
- **The ~190 dirty paths** need sorting by slice owner. The handoff's dirty-tree ownership table is the map. It mixes interrupted
  semantic work with "formatting noise", and only a human or a careful single lead should commit it.
- The site's **copy strikes** (STRIKE FOUR: "the fix is DELETION, not rephrasing"; STRIKE FIVE: "Descriptive and extremely minimal")
  are recorded as standing taste. Ember should re-read the live site against them after the next cohort.

---

## 3. Solana trading observatories: joshibot → joshi → ltshitcoims

### 3.1 Context: the money, stated plainly (`ember-income-structure.md`, as of 2026-08-12)

- Income is **$DREGG creator fees** (mint `XkeTXo1125vz5H9svJpGiw4JvLbN8VmMu9cmMvspump`, PumpSwap pool `2XHrhkxf…`), measured at about
  $213–313/day, plus about $2k in Meteora DLMM LPs. The coin was "launched predatorily" by someone else, and Ember "wrested control of" it.
- Obligations are about $4,100/mo, plus a $40k IRS debt.
- Doctrine: **"fees pay the bills, and the book is never dismantled to pay them."** An LP-strategy agent was once given
  dated obligations as a constraint on the book, and it recommended selling ≥$900 of a $1,351 book.
- **The sentinel is dead by choice.** Ember: *"keep the sentinel dead, because i already lost all the money i set aside for
  pump and have banned myself from 'tuition' until we've managed to earn some back using Science."*

### 3.2 joshibot (`/Users/ember/dev/joshibot`, 321 commits, `dev`, 2026-08-12 → 09-03, no remote)

**Origin.** "shitcoims Sentinel — a local-first, sell-only Solana position monitor". Its safety posture is strong: no buy function;
three live gates (`execution.enabled`, `--live`, and a mode-0600 arm file bound to the pubkey); and the Jupiter transaction is treated
as untrusted, so before submission it checks the signer and fee payer, a program allowlist, close/ATA destinations, and an exact
simulation.

#### The −7.47 SOL fabricated-cost-basis postmortem (`joshibot-fabricated-cost-basis.md`)

> "`shitcoims_sentinel/engine.py:770-773` stamps a lot's cost basis from the **current Jupiter exit quote** whenever
> `lot.needs_basis`. PnL therefore starts at 0% by construction regardless of what was actually paid, so a '−10% stop'
> fires ten percent below wherever the coin had already fallen to in the 10-minute auto-protect delay."

| Metric (live window 2026-08-12, reconstructed from chain by two methods reconciling to the lamport) | Value |
|---|---|
| Net | **−7.47 SOL (~$564)** over 137 buys / 121 sells |
| Operator-typed basis | **+18.1%** mean over 3 round trips |
| Fabricated basis | **−29.1%** over 16 |
| Shape | avg win +11.4%, avg loss −45.8%, 43% hit rate |
| Damage concentration | 97% of losses from round trips worse than −15% |

**The lesson about inference** (verbatim): *"Grok's own end-of-session diagnosis was that the −10% default was scalping the
bags too early, and its fix was to widen the default to −35%. That is backwards: widening addresses the 1% of damage in the
−15%..−5% band while enlarging the 97% below it. The real defect is the basis source, not the threshold."* The data needed
for the fix was already on disk (`intelligence_state/intelligence.sqlite3`, with `sol_delta_lamports` per signature). It had
been blocked by the intelligence/sentinel isolation boundary.

#### "Harden, don't rewrite" (`joshibot-harden-dont-rewrite.md`)

Two independent reviews agreed that none of the defects were type errors:
- Double-submit at `executor.py:243-254`: a signature recorded on confirmation timeout, then a retry builds a new order. With
  scale-outs, both partials could land.
- The 32-address simulation ceiling (`executor.py:193-200` vs `clients.py:193`): past it, every live sell fails.
- A config lost-update in `server.py:94,104,126`, outside `_policy_lock`.
- **`transaction.py` (243 lines of v0/ALT/allowlist/simulation binding) is "the best code in the tree".**
- The inverted defect distribution: the pure layer has 1,402 assertions, while `executor.py`, the only module that spends money,
  had **zero tests**. *"That is the LLM authoring signature: what was easy to test got tested."*

#### The research program (GOAL.md done log, from 2026-08-13)

| Item | Commit / result |
|---|---|
| Track A: fabricated basis killed at all four sites, executor safe to retry (`isBlockhashValid` as proof of death), 32-address ceiling chunked | `e509cc3`, 416 pytest + 5 dashboard |
| **Lean kernel** `kernel/Joshi/{Basis,Bin,Dsl,Envelope,Export,Fill,History,Release}.lean` | "quote-derived basis is unconstructible; no-basis can never fire a stop"; no-lookahead as a theorem over all strategies; DSL trial count **110,880 predicates**; `tripped_breaker_is_absorbing`. Zero sorries, Lean core only, builds in about 2 s |
| Track C: kernel load-bearing via `@[export]` C ABI (`joshi_sell_out`, `joshi_accepts`) → `joshi-oracle` binary; 15 parity tests over 600 random pools | caught round-vs-floor and dropped-denominator transcription bugs |
| Tape recorder `2d93305` | 96 tests, 31/31 mutations; graduation median corrected from 0.5 s to 250 s (Marino: 264 s) |
| Signal #1 SVN co-trading | **UNRESOLVABLE-AT-THIS-N**. Instrument finding: with no planted coordination, Bonferroni FWER 0.600 and about 99 BH clusters "from nothing" |
| Signal #2 funding-tree | **NO-LINKS-AT-THIS-N**. It refused a false positive that would have merged "OUR OWN SENTINEL with a third-party KOL" |
| Spike #3 callout→flow | p = 0.00498 when our own wallet was included, which was a closed loop. Structural-zero guard added |
| Replay engine, purged/embargoed walk-forward, deflated Sharpe with the cross-trial variance term kept | — |
| `RESULT_dregg_boundary.md` (08-15) | **Falsified the boundary-press objective.** The real fee ladder is **25 rungs 5 bps apart keyed on market cap in SOL**, verified on 1,058/1,058 swaps. "The joint position is LONG its own price essentially everywhere" |
| Two populations (08-16) | The quality cluster is held. Ghost-town scalps under 5 min: 7/13 winners, +$3.09. Every hold past 5 min: 1/20, **−$61** |
| 08-29 | Gated portal (Sign-In-With-Solana), D4M layer "found three bugs in our shipping crew matcher", "CLEAN is not a buy signal" |
| `238c183` 09-03 | **"the desk: one substrate under eleven packages, and the dead stack gone"** |

Studies directory: ~40 modules (`callout_volatility`, `crew_persistence`, `crime_signatures`, `bundle_hypothesizer`,
`dregg_boundary`, `lp_strategy`, `mayhem_arm`, `jupiter_programs`, …). `kernel_svm/` is a 188k-line SVM capture/oracle harness.

**`marketfabric-untrusted-not-slop.md`** is the outside-research policy. Alif's marketfabric has `runs/` gitignored, a
flagship pre-registered study that was never reported, a CPCV purge that is a no-op, and an invented DSR. Its LP null was
caused by a fee bug: *"Nulls can be artifacts too."* Only `crates/quantmath` may be lifted.

### 3.3 joshi (`/Users/ember/dev/joshi`, 303 commits, `main`, 2026-08-18 → 08-29)

**What it is.** A Rust workspace of **37 crates** (`joshi-accounting`, `joshi-epistemic-book`, `joshi-market-state`,
`joshi-pump-adapter`, `joshi-wallet-topology`, `joshi-wave6-*`, …) and six apps (`collector core g0-harness glass resident up`).
From the README: *"a personal, accessibility-first, human-directed market observatory and trading cockpit for Pump.fun …
It contains no wallet keys, signer, live executor, or authorization to trade."*

**The constitution** (`JOSHI_THOUGHT.md`, 2026-08-16, Ember × Codex):
> "JOSHI began as accessibility infrastructure. Existing Pump mobile and browser interactions require too much painful
> tapping and precision navigation for Ember's stiff hands … Accessibility is not a later UI polish lane."

and the warning that motivated the rewrite:
> "A research agent can study microdips, callouts … obtain a clean local result; and silently replace the project with that
> result. That failure already happened in the joshibot/Claude history … a null for the projection was narrated as a verdict
> on the process."

It sets out an eight-kind **epistemic type system**: Observed fact, Implemented capability, Derived interpretation, Latent
estimate, Operator perception, Hypothesis, Metaphor, Aspiration. Ember's product definition (joshibot memory, 08-16): *"my
personal copy of the pump app"*, with parity first and superpowers second. Every hunch and zap is captured as (state, action)
pairs for later distillation.

**What it built** (MORNING.md, 08-25): the Glass cockpit runs end to end under a Playwright walk (pair → 18-row board → coin
page → hold → journal). Registered studies: `selector-live-v1` was "Inconclusive on the registered tier-8 primary (2-1-3),
promising on the exploratory tier-2 (4-0-2)". `tournament-v1` found "Every conditional cell red after the adverse haircut;
least-red family is 'do the least'."

#### Why the Jupiter studies were mostly null (commits 2026-08-27)

| Commit | Study | Result |
|---|---|---|
| `81ff540` | Recon: SOL up/down 5m/15m contracts on Jupiter are **Polymarket CLOB rails**, settling on Chainlink SOL/USD; fee about 1.75% at mid | "contract prices are EPHEMERAL", so the collector had to start immediately |
| `125b17e` | Conditional settlement | Step 0 caught the wrong rule. The real rule is `twap60(close) >= twap60(open)` (15/15), not the whole-window average (12/15). Flip zone "razor-narrow": only \|dist\| ≤ 2 bps is live at 60 s. "Nothing clears a 50c entry" |
| `074b629` | Backfill **3,357 settled rounds** through Polymarket Gamma (Helius was the wrong path) | Leg-in "net-fee lock 97.5/98.2%" flagged as an **ORACLE bound**: "the exact count-the-wrong-thing trap, flagged not hidden" |
| `5846833` | Decision-time opportunity census | **Mostly null.** Near-boundary fade at 5m: +4.4c falls to +1.75c (the fee floor) at 10 s freshness. **One survivor: 15m fade at +3.5c** (about 2× the floor). Buy-ahead: clean NULL (49.9% win, CI [46.8, 53.0]) |
| `0eb6ba6` | Flow model on 342,531 Kraken ticks, 29 features, GBM + logistic, walk-forward | **An "earned null."** Market Brier **0.0965** vs GBM[price+flow] 0.1022 vs price-only 0.1020. Hawkes η = **0.93 @ 165 s**, near-critical. "The crowd does feed on itself at eta near one — but the price already knew." The residual +5.0c is "seconds-scale contract-print lag behind the Kraken reference (latency-arb territory)" |

**Why null.** The venue is efficiently priced against a public reference. The fee (0.070·q(1−q)) consumes the edges
that survive causal discipline. The only remaining edge is executability, meaning what the order book offers at size, and
fill prints cannot measure that. *"Firming the one survivor (15m fade) needs orderbook-ladder capture, not fills — the
recommended next instrument."*

**Endgame of joshi** (08-29): `93e5c98` "the DREGG utility portfolio — five products from the surviving assets"
(`docs/planning/DREGG_UTILITY.md`), then the v1 gate decisions: "gate threshold set to **888,888 DREGG**", and "gate bot is
ltshitcoims". After that the work moved back into joshibot's desk.

**joshi-gift.** `LICENSE_GRANT_rupert.md` (2026-08-31) grants a "perpetual, irrevocable, worldwide, royalty-free, non-exclusive,
transferable, and sublicensable licence" over `github.com/emberian/joshimoments` (commit `4b4f676b…`, roots `43adb095` and
`08ffbe9b`) to "Rupert of @ecomerateHQ". It includes a `.sig.json` attestation and `verify_attestation.py`. This is a signed
gift of the observatory work.

### 3.4 ltshitcoims (`/Users/ember/dev/ltshitcoims`, 8 commits, 2026-09-03)

The notes and state repo for **`@ltshitcoims_bot`**, the $DREGG holders' Telegram desk. Gate: sign a challenge and hold
≥ 888,888 $DREGG (operator override 88,888). Group `-5010286089`. Signer page `shitcoims.dregg.studio/sign`. Six sibling
services post through the bot's outbox: launch-screen digest, movers feed (chart montages), daily wire, watchlist alerts,
callout archiver, and record. The code lives in `~/dev/joshibot/{desk,dregg_*}`. It is deployed to hbox by
`rsync --files-from` + `ssh -n` with an import smoke test before restart, and `hbox-units/` holds the only versioned copies
of the systemd units.

**`INCIDENT-2026-09-03.md`**: hbox root filled. The screen's score tape went to **zero rows/hour for ~22.5 h**. The gate
crash-looped 44 times (`sqlite3.OperationalError: disk I/O error` at `PRAGMA journal_mode=WAL`). journald lost every log from
Aug 29 to Sep 2. Ember's report: *"peepl were failing to have their keys verify thru it."*

**`ATTRACTOR.md`**: joshibot is about 380k lines of Python. The live desk is 22k of that, and **one product had been built as eleven
small products**. Twelve cross-cutting ideas existed as hand-rolled copies, for example an "atomic heartbeat JSON writer: 7 copies"
and a "raw `INSERT OR IGNORE INTO outbox`: 5". The end state is `desk/` as one substrate of about 2k lines. Census: about 15k lines
deletable (`shitcoims_scout`, `shitcoims_sentinel`, `shitcoims_lpexec`); about 16k is research substrate to **move, not delete**
(paperdesk, cluster, netmap, replay, kernel), because every RESULT doc's reproducibility depends on it. `6331f23` "the collapse landed".

### 3.5 Classification (observatories)

**Maturity:** joshibot desk at `L4 Deployed` (hbox, real users gated by token holdings). Sentinel and executor `Frozen-for-Rethink`
by Ember's ruling (the "tuition ban"). joshi at `L2 Prototype` / `Frozen-for-Rethink`. ltshitcoims is `L4` ops documentation.

**Unclosed cycles & missing links**
- **Order-book ladder capture for Jupiter 15m.** This is the one instrument that could confirm or kill the single surviving cell. It
  is a read-only collector (no signer), so the ban does not apply.
- **`RESULT_callout_volatility.md`.** Ember's correction is that callouts are echo-bots that fire after real 161-wallet bursts, so a
  callout stream marks continued two-sided flow, which is a volatility locator for scalping and LP work. The memory lists it as
  "untested until" that study.
- **Research substrate move.** The 16k lines of paperdesk/cluster/replay/kernel belong beside `studies/`, per the ATTRACTOR.
- **The (state, action) hunch/zap corpus** is meant to be distilled into Ember's intuition. "capture first, distill later or never".
  No capture loop is known to be running.

**Promising & ready for revival**
- The **Lean kernel + `joshi-oracle` C ABI** is a small, verified execution kernel (`sellOut_le_reserve`,
  `tripped_breaker_is_absorbing`) that could serve as a pre-trade check for any future executor, dClutch's operator included.
- The **"desk sells well"** finding: Ember's vesting-exit ladder fills measured **+1.96% vs routing the same clip** (t = 3.31,
  n = 221). Smooth unlock selling (about 14 daily clips) gives 10.9% dispersion against 46.8% for a single clip. These are cash
  improvements, not speculation.
- The DREGG execution edge: Ember trades DREGG at about 25 bps effective while everyone else pays about 105. *"the desk's largest
  unpriced execution advantage."*

**Struggling / needs Ember's human attention**
- **When to lift the tuition ban** is Ember's decision alone. The written criterion is "earn some back using Science", and no
  study has yet shown positive expected value.
- **The disk-full class on hbox root** (`/` reached 100% on 09-02/03 and again during dClutch on 09-03, per `hbox-use-tank.md`).
  The ops fix (journald caps, services writing under `/tank`) needs Ember's sign-off on the box.
- **The Rupert license grant** is outward-facing and irrevocable. Any follow-on contributions are covered by "any future
  contribution", which Ember should keep in mind before pushing to `joshimoments`.

---

## 4. The Mina / Kimchi / Pickles / FRI ZK vertical

### 4.1 Biographical substrate (upstream code, not Ember's property)

Ember was an engineer at **o1Labs** on Mina. `mina-src` (MinaProtocol/mina, branch `compatible`, 38,152 commits) holds **340
Ember-authored commits** under `ember.arlynx@o1labs.org`, `cmr@o1labs.org`, `ember@lunar.town` and `emberian`, dated
**2020-02-10 → 2024-04-23**. They are mostly CI, release and migration tooling, e.g. `426078ac9c` "slightly different approach",
`298b1a4bc0` "mina-berkeley-migration-script name", `99f9af8d11` "dhall/PromotePackage: acknowledge Devnet", and 2020 work on the
connection gater. `mina-stealth-fixes` has 59 Ember commits, and `proof-systems` has 3 (`31a21e71b4`, `ba93cd38ef` "use workspace deps",
`21d648eebf`). That is the source of the deep fluency with Kimchi and Pickles. The code belongs to o1Labs and the Mina Foundation.

| Checkout | Owner | Role now |
|---|---|---|
| `mina` (non-git snapshot, Mar 2024, has a 499 KB `circuit.html`) / `mina2` / `mina3` | MinaProtocol | OCaml reference for `pickles/step_main.ml`, `wrap_main.ml` |
| `mina-rust` (5,192, `develop`) | o1-labs | Rust Pickles **prover** that dregg links; "external gate list → proof in 0.66s" |
| `openmina` (1,344) | openmina | `BlockVerifier` used as ground truth for block 539508 |
| `proof-systems` (10,732, last `f6d958dc05` 2026-06-22) | o1-labs | `kimchi::verifier`; Fq sponge constants dumped from `fq_kimchi::static_params()` at `f6d958dc05` |
| `snarky`, `o1js` | o1-labs | reference |
| `mina-state-proof` (590) | NilFoundation | prior art for Mina → EVM state proofs |
| `o1js-groth16` (44) | onurinanc | prior art for in-o1js BN254 pairing |
| `minataur2` (190) | olton | block explorer |
| `zkbox` | "satoshi" | SnarkyJS toy |
| `nockchain` (253, last 2026-06-10) | nockchain maintainers (incl. `bitemyapp`) | **competitive reference.** dregg's bumper sticker in `UNIFYING-STORY.md:28`: "**better than nockchain** — crystallinely coherent, l4v-grade", meaning "a claim about *crystalline coherence*, not feature count" |

### 4.2 Ember-originated ZK artifacts

#### verimina (`/Users/ember/dev/verimina`, March 2024)

Seven `.thy` files: `Aggregation Ouroboros OuroborosGenesis OuroborosPraos OuroborosSamasika Verimina ZkappLogic`. **Six are
empty.** `Verimina.thy` is 11 lines:

```isabelle
theory Verimina
  imports Main
begin
(* need to define:
- the meaning of a block
  roughly, the postcondition the block witnesses
- the encoding of a block
*)
end
```

**Maturity: `L0 Seed`.** The file names lay out a plan to verify Mina consensus (Ouroboros Samasika, Mina's variant), Praos and
Genesis, plus recursive aggregation and zkApp logic. Its central question ("the meaning of a block … the postcondition the block
witnesses") is the same question the 2026 Lean `MinaRealBlockGate` answers in part. The seed was never germinated in Isabelle. It
was answered in Lean two years later.

#### kimchi-playground (March 2024), o1js-hints (2025-04-08, one commit "Init commit")

The playground is two submodules (`proof-systems`, `snarky`) and nothing else. o1js-hints is a stock zkApp template. Both are `L0`.

#### p3rec-batched-ro / p3rec-pristine (Plonky3-recursion fork, 24 / 22 Ember commits, 2026-05-21 → 08-16)

The engine underneath dregg's recursive STARK. Load-bearing Ember fixes:

| Commit | Fix |
|---|---|
| `c14b5fc` | Plonky3 rev → `82cfad73` (fixes `OodEvaluationMismatch` with degree-7 AIRs). This is the rev every downstream crate pins |
| `ccebf66` / `72ffc56` | Native-batch leaf-wrap: `RecursionInput::NativeBatchStark`; "C3 GREEN … fix the WitnessId(0) double-creator" |
| `fc12f23` | "IVC fixed-point: pin child-VK identity in-band … the constant-VK perpetual fold" |
| `8d42900` | expose-claim NPO channel binding leaf publics to the root |
| `abc2c2a`, `a45ee56` | DSU global-`WitnessId(0)` collapse; "close 2 WitnessChecks bus imbalances — **the IVC same-endpoint mixed-root forgery now REJECTS**" |
| `7b74512` | FROZEN-PROOF replay (0.2 s oracle) root-causes the IVC residual to a LogUp bus imbalance, "NOT FRI" |
| `be52a51` | `normalize_to_shape` (**Pickles step-wrap shape**) + opt-in coeff-lookups |
| `993efec` | "deterministic verifier op-list — VK fingerprint was build-order random" |
| `0a4a554` | GPU recursion-layer prove path, byte-identical |
| `0ed1182` (08-16) | "make the HornerAcc chain guard go RED — it had never been seen to refuse" |
| `04e636e`, `a3a1b1f` | **DRAFT upstream PR**: "a tasteful upstream offer of 2 general-purpose engine fixes" |

**Maturity: `L3`.** Forgery-rejection tests exist and are wired into dregg.
**Ready for revival:** the drafted upstream PR. The two general engine fixes have never been offered to Plonky3. Doing so is
outward-facing, so it is Ember's call.

#### plonky3-bn254-wrap (3 commits, 2026-06-15)

| Commit | Content |
|---|---|
| `e80f499` | "Step 1 GREEN: the BN254 outer StarkConfig — the field-transition rung of the dregg EVM wrap" |
| `5dc2a2c` | Step-2 public-input bridge. The outer config carries dregg's four publics |
| `96440ab` | "nail the FRI-param parity seam — wrap targets the recursion-root config (arity 1, PoW 14)" |

`OuterStarkConfig`: BabyBear values, `BinomialExtensionField<BabyBear,4>`, **Poseidon2-over-BN254** commitments (width 3, deg-5
S-box, R_F = 8, R_P = 56, HorizenLabs bn256, "the same trust root SP1 uses"), and `MultiField32Challenger<BabyBear, Bn254, …>`.
FRI uses `log_blowup=3`, 38 queries, 14 PoW bits. The keystone is `src/hasher.rs::MultiFieldPoseidon2Hasher`: *"Upstream Plonky3
ships no such hasher."* Tests: `outer_config_round_trips`, `outer_config_rejects_wrong_public`,
`production_constants_load_from_zkhash`. Motivation: `WholeChainProof` is **~502 KiB**, and the target is a ~260-byte Groth16
checked for about 270k gas.

#### dregg-gnark-wrap (1 commit `1a0d990`, 2026-06-15)

A Go/gnark circuit that verifies the outer STARK and ends in Groth16 BN254 with an exported Solidity verifier.

```
$ go run .
compiled: 741 R1CS constraints, 6 public, 4 secret  (0.00s)
groth16 setup done (0.07s)
groth16 verify: OK
exported Groth16Verifier.sol (27022 bytes)
```

Measured: **Poseidon2-BN254 permutation = 243 R1CS**; full-circuit estimate **~1–1.3M R1CS**. *"the FRI proof is empty in the stub
(only the public-input binding runs)."* The key design choice is native BN254 hashing with emulated BabyBear values: "This split
is the whole reason the wrap is cheap."

**Maturity (both): `L2 Prototype`.** In breadstuffs the lineage continued into `chain/gnark/peer_wrap_circuit.go` (`1bdaea5b67`,
forge 21/21), which "reuses the FRI-wrap VERBATIM". The standalone repos are frozen there.

**Unclosed loop:** README Step 2, "emit this config from the recursion fork". The fork's Poseidon2 op-table and FRI private data
are BabyBear-width-16-specific. The smaller path is to prove the last BabyBear STARK and re-commit it under `OuterStarkConfig`, as
a thin re-prove "mirroring SP1's separate 'shrink' layer". A second gate comes from the FRI memory: **gnark Groth16 setup memory
(23 GB @ 4.98M constraints)**. At Proven-120 (d = 8), the outer config must raise lb 3 → 6 to hold q at 36. Otherwise the R1CS
grows to about 14–22M and setup needs about 35–50 GB.

### 4.3 The Lean Kimchi → Pickles verifier (breadstuffs, 2026-07-26 → 07-31)

Goal (Ember, 07-26): *"a Mina proof verifier as FAST as possible, in Lean; interchain proofs 'as nice as possible'."* Plan docs:
`docs/MINA-KIMCHI-VERIFIER-PLAN.md`, `docs/KIMCHI-VERIFY-SPEC.md` (ten checks C1–C10, sourced from `verifier.rs` v0.7.0 with line
numbers). **SP1 is NEVER acceptable**, so the verifier uses dregg-native Pasta emulation. The **hybrid swarm** ran Kimi K3
(`kimi -p`) as builder with Claude reviewing actual theorems and `#assert_axioms`. Memory note: Kimi applied deep techniques unprompted.

| Rung | Commit | Content |
|---|---|---|
| K1 `PastaField` | `1ba1d6613` | Fp/Fq of the Pallas/Vesta 2-cycle |
| K2 `PastaCurve` | `6a3ff11ab` | point ops + endomorphism (ζ pinned, cube facts proven) |
| K3 `PastaPoseidon` | `4a39a1e3b` | Kimchi FS transcript (α = 7, 55 full rounds). Permutation **FORCED** via `Sha256FoldForcing.foldl_cstep_forces`; KAT vs o1js |
| K4 `PastaCurveComplete/ScalarMul/IPA` | `fbdfad15c`/`0d0c71284`/`6eb283421` | RCB complete-add, forced GLV ladder, **`sVec_eq_bPoly`** (IPA deferral sound: k challenges ⇒ 2^k terms never materialised, which is Pickles' accumulator) |
| K5 `KimchiVerify` | `78ae2edf7`, `6705d1bd4`, `835db56c6` | C4–C8 over the real field, six custom-gate bodies, v/u re-derivation |
| K6 `MinaStateQuery` | `38d64b233` | ⚠ **three CR floors PROVABLY FALSE** (injectivity over ℕ while `absorbAt` reduces mod p), so every K6 payoff is vacuous. `PastaPoseidon` **double-permutes on even-length input** (hidden because the 7 `#guard`s pinned only odd lengths) |
| Reality gate | `7f42aa143` | `ft_eval0`/`cip`/`lin_const_term` recomputed in Python from the Rust and all match; 174/175 constants verified upstream. Extractors preserved at `metatheory/fixtures/kimchi-extractors/` (`646c235c0`) |
| P0–P2 `PicklesRecursion` | `5c1423632` | one decision body at both cycle sides |
| **`MinaRealBlockGate`** | `1b1e6a4a3`/`b25556c22` | **Devnet block 539508** (`3NLmVB6Fs3dm4kXNkgwheHXzJXNpCCwEDe76RpTVeBTNujm12zNk`): Pallas, k = 15, `prev_challenges = 2`, public 40, domain 2^14. o1-labs' own `kimchi::verifier::verify` returns `Ok(())` first; then `kimchiVerifyDecisionFieldRec` **ACCEPTS** the real block and rejects 4 tampers |
| P6 | `c5ae5dbe1` | "the freeze was REJECTING MINA": `verifier.rs:810-813` compares against the verifier **index's** count, not zero |
| Fq sponge `PastaPoseidonFq` | — | `core_is_Ref_at_Fp` by induction, so the double-permute bug cannot return. Two transcript defects found (`ft_eval1` order, missing `prev_challenge_digest`) |
| P3 `PicklesFinalize` | `98f9c7cde` | `derivePlonk_perm_is_K5_permScalar` holds by `rfl`. P5 is now "a field swap" |
| **Mina → dregg live** | — | A zkApp on **Mina Devnet** consumed a recursive proof of a Poseidon-Merkle path into a **dregg-emitted root** and recorded the leaf on chain, attesting commit `0e66ea63c` (`docs/MINA-DEVNET-DEPLOYMENT.md`) |

**The prior-art correction** (`docs/AUDIT-IMPORTER-AND-DOCS.md`, `d7dcbf5d2`): `l-adic/snarky`'s `formal/` already has an
executable Lean 4 `kimchiVerify` with AGM soundness capstones, sorry-free, by Martin Allen, dated 2026-06-24. It is an
independent org ("NOT an o1-labs repo") and **UNLICENSED**, so it is read-only. It **excludes recursion**, so **P3/P4/P6 are
genuinely ours.** *"NEVER re-claim 'first machine-checked Kimchi verifier.'"*

**The Pickles-in-Lean epoch** (Ember, 07-31): *"this might be the first independent implementation of Pickles… useful code ideas
have been trapped in that OCaml for a while."* The precise claim: openmina/mina-rust **loads gates from OCaml blobs**, so a Lean
synthesis would be the first independent **synthesis**. Phase A is differential, with byte-exact gate lists diffed against o1js.
The honest name is *"independent, differentially-verified Lean implementation of Pickles synthesis — NOT 'machine-checked
Pickles.'"* Phase B (recursion soundness) is optional and epic. The win: removing Node and js_of_ocaml from proving, so "the 44GB
o1js-compile OOM disappears".

**Maturity: `L3`** for the arithmetic core against a real block. `L2` for Pickles synthesis (the first rung, a gap read, is planned).

**Unclosed cycles & missing links** (from `docs/MINA-REAL-BLOCK-GATE.md`)
1. **P4, the transcript-equality binding: "THE CRUX", measured, not proved.** *"without the transcript-equality binding,
   `finalize_other_proof` discharges a `Deferred_values` AN ATTACKER CHOSE."* It needs a RO/collision assumption for the sponge
   stated as a **hardness** assumption. An injectivity assumption would repeat the vacuity bug in §4.4. It also needs `endo`
   injectivity on 128-bit prechallenges.
2. **The Wrap GROUP check** is "weeks, the largest unbuilt block". No group element is touched by any check yet.
3. **K6 floors.** Restate them as hardness or bounded statements, never as injectivity.
4. **Pickles synthesis Phase A**: emit step/wrap gate lists from Lean and diff them byte-for-byte against o1js.

### 4.4 The FRI floor: the mystery, the crisis, the number

**The quote.** Breadstuffs session `bc04f12c-…`, **2026-07-20T04:17:57Z**, right after "ready for this research campaign? :)":

> *"(my secret hope is that as we get far enough we either finally solve the mystery of the FRI floor, or we find a counterproof)"*

Sixteen hours later (07-20T20:52Z): *"first off, let's respond to the crisis, and just upgrade our parameters please, and just
**remove** more of the claims about bits or etc etc etc, and also any bogus 'calculator' style things that aren't well formally
connected."*

Earlier framing (07-16): *"if our system only has 61 bits of security, how good is that, what is each bit measuring the grinding of?"*

**What the "floor" is.** Every FRI-based system's soundness rests at the bottom on a proximity-gap or correlated-agreement
statement about Reed-Solomon codes, plus hash assumptions. The field assumes it. dregg names it as an explicit carrier. Ember's
correction is recorded in `project-lightclient-stark-true-peers.md`: *"'discharging the FRI floor' is a MYTH … everyone else silently
ASSUMES FRI soundness; dregg naming the floor is us being MORE honest than the field, not a debt — do NOT list it as a residual."*
The "mystery" is therefore whether the floor can be **derived**, so it stops being an assumption, or **refuted** at deployed
parameters. Hence "or we find a counterproof".

**What the campaign found** (`project-fri-soundness-reality.md`, `docs/reference/FRI-SOUNDNESS-THREE-ISLANDS-2026-07-28.md`):

```
 Island A  deterministic apex the light client runs   CircuitSoundness.verifyBatch, lightclient_unfoolable
           [StarkSound]/FriLdtExtractV3* as Boolean undischarged Props; vacuity wound REPAIRED (FriLdtExtractV3Faithful)
 Island B  adversary-quantified chain → real verifier  FriVerifierO.verifyAlgoO_run_eq ; friLdtExtractV3_rom_adv_of_legs
           legs εFS + εGrind + εMerkle + εQueryᵃ  — ε_C is NOT a leg ; hcover bridge named & undischarged
           epsFriAdv_deployed_vacuous_at_2_31 : composed bound ≥ 1 at 2^31 queries
 Island C  L0–L6 correlated-agreement ladder (BCIKS20 Thm 4.1, UD regime) ≈101 bits over the quartic extension
           "NOT the ledger's 109/111"
```

- **The number is 51.** `deployed_wrap_commitBits` machine-checks `commitBits = 51` with a two-sided `Nat.log2` bracket. A
  published 57 was "half-corrected": config and height were mismatched (`DEPLOYED_WORST_LOG_D0 = 16 + 3` called "MEASURED"). The
  real pairing is `IR2_INNER_LOG_BLOWUP = 6` with `WRAP_LOG_CEIL = 16`, giving |D⁽⁰⁾| = 2^22.
- **Proven-120 is specified**: d = 8, lb = 6, q = 36, pow = 16, giving **122.60 bits on every shipped config**. d = 5 is dead
  (ceiling 118). d = 6 caps at 119 and needs a permanent fork of 18 plonky3 crates.
- **Correlated agreement is mechanized.** `CorrelatedAgreement/{Scaffolding,BerlekampWelch,Interpolation,Collinearity,Theorems,Interface,RlcDischarge,DecimLiftDischarge}.lean`.
  The crux `polishchuk_spielman` (Cramér–Nardi-fixed form, Kopparty 2025 §2.2 Lemma 2.2) landed at `3b493456e2`: axioms
  `[propext, Classical.choice, Quot.sound]`, 13/13 `#assert_axioms`, non-vacuous on `ZMod 11`. Deployed instance: 2^24 domain,
  rate 1/8, UD radius 7,340,032.
- **The vacuous-floor disaster** (`feedback-prove-the-floor-false.md`, "the single worst bug we have ever found"): `HashCR`,
  `Poseidon2SpongeCR`, `MSISHard` and `MLWESearchHard` were stated as **non-existence or injectivity**, which is **false at real
  parameters** by pigeonhole. That made "the whole circuit-soundness tower (StarkSound/FRI 'rests only on HashCR') … VACUOUSLY TRUE
  at deployment." `SchnorrDLHard` failed the opposite way: it was trivially **true**. Fixes: `08d3cded3` (lattice), `62f001aeb` (hash).
- **HyperFRI is a NEGATIVE RESULT.** Ember (07-26): "that concluded with a negative result, it isn't something we are actually
  pursuing." Two-sided isotypic codes are dead, and "there is no grading to halve".

**The lever nobody has pulled.** `FriFoldConsistencyDichotomy.lean` is 974 lines, fully proved, and referenced only by itself and
`FriPositiveRadiusSchedule.lean`. It proves the dichotomy the commit-phase term exists to cover: a fold either stays consistent
(farness propagates with no probability needed) or deviates and is caught at a proven price. *"Wired in as a fifth leg through the
same `hcover`-shaped bridge, BCIKS20's separate ε_C addend may not be logically necessary for this codebase's proof strategy at all.
… it is untried."*

**Maturity: `L3` (proved core) / open research.**

**Unclosed cycles & missing links**
1. **The word↔proof bridge** (`WordProofBridge` / `DeployedFriEmbedding` / `hcover`), flagged in-tree as "not a lemma-sized gap:
   it is the FRI-proximity-to-`VmTrace` decode."
2. **A fifth commit-phase leg** over `Strategy`/`OracleComp`, built either by formalizing BCIKS Lemma 8.2 (no attempts in-tree) or by
   wiring in the dichotomy, which requires extending `epsFriAdv_compose`'s union bound.
3. **Unifying the islands.** `commitBits`/`epsC`/`friCommitLedger` appear only in the ledger family, with zero hits in any file that
   mentions `verifyAlgo` or `OracleComp`.
4. **Running `TestSettlementGadgetMarginalCosts` at d ≠ 4.** "the repo owns it and has never run it". This is the measurement Proven-120
   needs before it moves the gnark wrap.

**Promising & ready for revival.** The dichotomy lever is the most direct route to Ember's "secret hope". If the fifth leg closes,
the commit-phase floor becomes a derived consequence of a proved combinatorial dichotomy plus the query phase. That would partly
solve the mystery, and it might also expose a counter-instance at the deployed parameters (2^22 domain, blowup 2^6), which is the
"counterproof" branch. Either way it is a well-posed research lane with all its parts on disk.

**Struggling / needs Ember**
- **Which number goes public.** 51 (machine-checked, deployed today), 101 (UD-regime CA, a different column), or 122.60
  (Proven-120, specified but not deployed). The 07-20 ruling ("remove more of the claims about bits") stands until Ember revises it.
- **Whether Proven-120 deploys.** It costs about +25% prover time and +20% proof size, with gnark setup memory as the binding gate.

### 4.5 Adjacent: light-client "true peers" and the vacuous folds

Within the same campaign, ETH (`3884100013`), Tendermint (`87f7368f63`), Solana (`4834d1de55`, the "rooted stake-weighted
supermajority", three audit holes captured) and Midnight (`5b540c20df`) light clients were emitted as AIRs, with
`DreggPeerRegistry.sol` (`0e40bd4d1c`) verifying peer-chain finality Groth16s. **The PROOF-MODE crypto folds as landed are vacuous**
(`docs/AUDIT-CRYPTO-GADGETS.md`, `c183acdce`). Executable collision witnesses (`pairHash [0]*8 [0]*56 = pairHash [0]*8 ([0]*56 ++ [1])`)
make `hcr` an empty premise, so `eth_finality_from_gates` and its five siblings "PROVE NOTHING". Validator mode, where the native
crypto check is done by the validator, remains sound.

The **Solana Foundation grant** for a verified Solana light-client circuit (v6 total **$47,344 = "GREGG" on a phone keypad**; v4
was $37,344 = "DREGG") is the bridge between this ZK vertical and the Solana market vertical. The files are kept out of the repo at
`~/Downloads/Dregg_Solana_Formal_Verification_Grant_Proposal.{rtf,docx}`, with one placeholder left.

### 4.6 Peripheral: dreggfi-report, dregg-otc, modulus-go-round

| Repo | What | Maturity |
|---|---|---|
| `dreggfi-report` (7 commits, 07-13/14) | Typst brief "a proof-carrying financial substrate". v3 is "written from the *measured* state": an 8-mechanism engine (60/60 + 36/36 + a 14/14 `--release` STARK), on-chain verification re-minted on Base/Solana/Cosmos (7/7, 2/2, 5/5), DrEX PQ-signed order matching, and a Halmos-proved launchpad (7/7) whose audit "found and fixed a real permanent-loss bug (42/42)". `87d94fe`: Tier-0 no-viewer graded as an adversarial t-of-n threshold bound | `L3` document over `L2–L4` artifacts |
| `dregg-otc` (no commits on `dev`) | Passphrase-claimable Solana escrow, raw `solana-program` 3.0, ~50 KB. Claim key from PBKDF2-SHA512 at 600,000 rounds with salt `"dregg-otc/v1/" ‖ offer`, so claims can't be sniped from the mempool. Program id `7bGfrNxemPSvthXXnYcHfDY8cjgWYeeysWm463tzfmh6`. Local validator tests cover wrong-passphrase refusal and a stranger's cancel | `L2–L3`, **uncommitted**. Whether it went to mainnet is not verified here |
| `modulus-go-round-onepager` (Typst, dated 2026-07-22) | "CULTDAO and the Modulus-go-round". DREGG research one-pager on modulus conversion across workloads ("Same workload. Same security target. Every conversion counted.") | `L1` artifact |

**Needs Ember:** `dregg-otc` has a full working tree and a static page but **zero commits**. Committing it locally is safe. A
mainnet deploy and freezing the upgrade authority are Ember's decisions.

---

## 5. Cross-strand patterns: lessons paid for in this vertical

| Pattern | Where it bit | Memory |
|---|---|---|
| **Producer-missing.** Reader, schema and refusal all built; producer never written. "the FAILURE path exercises every one of them and the SUCCESS path exercises none" | dClutch cohorts 9–13; Ensemble and Series today | `producer-missing-pattern.md` |
| **A refusal-only suite is green on a broken route** | Dealer fill died while 14/14 hostiles refused | 09-07 handoff §4 |
| **Fabricated inputs look like outputs** | joshibot basis from the exit quote; tri-state social flags; `False` as a fabricated negative | joshibot memories |
| **An absent signal needs a positive control** | 19 instrumented sites, zero `Program log` lines anywhere | `absent-signal-needs-positive-control.md` |
| **A floor that is false makes everything above it vacuous** | HashCR injectivity; K6 CR floors; light-client folds | `feedback-prove-the-floor-false.md` |
| **A second author finds the first author's error** | dClutch two-scale defect found by the web mirror; Mina fixtures circular until dregg emitted them | cohort-13 memory; Mina memory |
| **Count the wrong thing** | Jupiter oracle-bound "97.5% lock"; whole-window vs twap60 settlement; config/height pairing for 57 vs 51 bits | joshi commits; FRI memory |
| **Nulls can be artifacts too** | marketfabric's LP null came from a down-move fee bug | `marketfabric-untrusted-not-slop.md` |
| **The builder is an artifact, not a host** | SBF reproducibility | `dclutch-repro-builder-is-an-artifact.md` |
| **Rulings are usually missing facts** | 6 of 8 "principled" calls overturned by a reader | `rulings-are-usually-missing-facts.md` |
| **Ember rules by reversal** | "you aren't waiting on me for rulings are you?" | `ember-rules-by-reversal-not-approval.md` |

```
   Lean semantics ──► generated ABI/codec ──► SBF ELF (named builder) ──► devnet cohort ──► census L1–L8
        ▲                                                                              │
        └──────────── second author (web mirror / Python recompute / chain read) ◄─────┘
                         this loop found: two-scale, epoch rent, terminal order,
                         Pyth receiver slot, prev_challenges freeze, double-permute
```

---

## 6. Revival docket (ordered by leverage ÷ cost)

| # | Action | Vertical | Agent-doable? | Gate |
|---|---|---|---|---|
| 1 | Isolate the dirty Structured `CheckedInfrastructureV1` import; run the focused Direct SBF test from `9ae8e0dab`; run A↔B reciprocal trades on one fresh hbox validator under `/tank` | dclutch | yes | check `df -h /tank` and the cleanup log first; no second cleanup |
| 2 | Derive the accepted-route campaign matrix from the generated `routes.md`; run claims-split-merge ×5, founder-bond ×2, batch-spine ×3, Dealer non-null fill | dclutch | yes | filtered tests only (`--test-threads=1`) |
| 3 | Wire `FriFoldConsistencyDichotomy` as a fifth leg of `epsFriAdv_compose` | breadstuffs FRI | yes (research lane) | statements audited for vacuity |
| 4 | P4 transcript-equality binding under a hardness-style sponge assumption | Lean Pickles | yes | prove the floor satisfiable and **not refutable** at real params |
| 5 | Order-book ladder capture for Jupiter 15m (read-only) | joshi | yes | no signer; the tuition ban stands |
| 6 | Step 2 of the BN254 wrap (thin re-prove under `OuterStarkConfig`) | plonky3-bn254-wrap | yes | gnark setup memory ≤ box |
| 7 | Commit `dregg-otc` locally | dregg-otc | yes | no deploy |
| 8 | Send the two Plonky3-recursion engine fixes upstream | p3rec | **Ember** | outward-facing |
| 9 | Fund and deploy a fresh 8-ELF cohort (≈41 SOL vs 26.57 on hand) | dclutch | **Ember** (funding) | standing authority covers deploy, not faucet |
| 10 | Rule on 0029 item 10 (flagship conditional market) | dclutch | **Ember** | taste |
| 11 | Refresh the CFTC packet's factual status ("Nothing … deployed" is now false) before any external use | dragons-clutch | draft yes; send **Ember** | legal, outward |
| 12 | Decide the public FRI number (51 / 101 / 122.60) and whether Proven-120 deploys | breadstuffs | **Ember** | — |
| 13 | Lift or keep the trading "tuition ban" | joshibot | **Ember only** | — |

---

## 7. Source index

**Memory files read in full or in part**
- `~/.claude/projects/-Users-ember-dev-dragons-clutch/memory/`: all 35, including `MEMORY.md`, `dclutch-cohort13-first-fill.md`,
  `dclutch-attractor.md`, `dclutch-mechanism-agenda.md`, `dclutch-repro-builder-is-an-artifact.md`, `dclutch-successor-repo-topology.md`,
  `dclutch-swarm-resume-protocol.md`, `dclutch-swarmcycle-plan-2026-08.md`, `dclutch-web-aliveness-patterns.md`,
  `dclutch-disk-worktree-drift.md`, `dragons-clutch-r1-sealed-baseline.md`, `dragons-clutch-session-1-baseline.md`,
  `convicting-a-coarse-refusal.md`, `producer-missing-pattern.md`, `absent-signal-needs-positive-control.md`,
  `build-by-inspection-converge-later.md`, `rulings-are-usually-missing-facts.md`, `verified-facts-wrong-inference.md`,
  `stale-nested-checkout-hazard.md`, `lane-budget-cap.md`, `ember-rules-by-reversal-not-approval.md`, `fail-closed-is-not-absolution.md`
- `-Users-ember-dev-joshibot/memory/`: all 6 (`joshibot-fabricated-cost-basis`, `joshibot-harden-dont-rewrite`,
  `marketfabric-untrusted-not-slop`, `ember-income-structure`, `persvati-box`, `MEMORY`)
- `-Users-ember-dev-joshi/memory/`: both (`ltshitcoims-notes-repo`, `MEMORY`)
- `-Users-ember-dev-dragons-net/memory/`: all 3. These cover the NNTP/Lean `dn-compiler` work with PR #33 by wisper-dev, which is out of
  this vertical's scope and recorded only for completeness
- `-Users-ember-dev-breadstuffs/memory/`: `project-mina-kimchi-verifier`, `project-pickles-in-lean-epoch`,
  `feedback-kimchi-circuit-agents`, `feedback-prove-the-floor-false`, `project-fri-soundness-reality`,
  `project-fri-correlated-agreement-formalization`, `project-hyperfri-math-street-collab`, `project-lightclient-stark-true-peers`,
  `project-solana-foundation-grant`, `project-midnight-strategy`
- Transcript: `-Users-ember-dev-breadstuffs/bc04f12c-dd0d-4657-90ed-6a5813018017.jsonl` (the FRI-floor quote and its neighbours)

**In-tree documents**
- dclutch: `docs/HANDOFF_2026_09_09_USAGE_PAUSE.md`, `docs/HANDOFF_2026_09_07.md` §4, `ARCHITECTURE.md`, `COMPOST.md`, `GOAL.md`,
  `README.md`, `docs/MASTER_COMPLETION_CONTRACT.md`, `docs/reference/programs.md`, `docs/decisions/` (list), `docs/design/MECHANISM_*`
- dragons-clutch-dclutch-integration: `docs/regulatory/{README,CFTC_PREMEETING_PACKET}.md`, `docs/reviews/ARCHITECTURE_REVIEW_2026-08-22.md`,
  `lean/README.md`, `rocq/README.md`
- dclutch-decomp `WAVE.md`; dclutch-legacy `README.md`
- joshibot `README.md`, `GOAL.md`; joshi `README.md`, `JOSHI_THOUGHT.md`, `MORNING.md`, Jupiter commits `81ff540 125b17e 074b629 5846833 0eb6ba6`
- ltshitcoims `README.md`, `ATTRACTOR.md`, `INCIDENT-2026-09-03.md`; joshi-gift `LICENSE_GRANT_rupert.md`
- plonky3-bn254-wrap `README.md`; dregg-gnark-wrap `README.md` + `1a0d990`; p3rec-batched-ro Ember log; verimina `*.thy`
- dreggfi-report `README.md`; dregg-otc `README.md`; modulus-go-round-onepager `main.typ`

**Not verified in this pass:** the contents of the eight `MECHANISM_*` design notes beyond their titles; whether `dregg-otc` was ever
deployed to mainnet; the current state of breadstuffs' Pickles rungs after 2026-07-31; and whether the hbox `/tank` cleanup (PID 1251893)
finished. Check each of these before acting on it.
