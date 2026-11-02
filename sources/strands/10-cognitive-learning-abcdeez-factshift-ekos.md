# Strand 10 — Cognitive Learning, Knowledge Ecosystems, SPW Symbolic Interfaces & Enterprise Knowledge Compilers

> `abcdeez` · `abcdeez2` · `abcdeez-spec` · the three `-live-*-abcdeez` environments · `curricularizedbooks` (BookLevel) ·
> `factshift-redux` · `app.factshift.com` · `spweebo'ard` · `spween` · `spw-workbench` · `spwsft` ·
> `EKOS` · `verekos` · `lunar-logseq` · `ticklogseq` · `lunar.town` · `annas-mcp` · `semantic-scholar-fastmcp-mcp-server`

Compiled 2026-11-02 from primary sources: every repository's README / design / plan files, `git log` (counts,
authors, dates and hashes quoted below are from `git -C <repo> log`), the per-project Claude memory directories
`~/.claude/projects/-Users-ember-dev-EKOS/memory/`,
`~/.claude/projects/-Users-ember-dev-breadstuffs--spw--workbench/memory/`, and the cross-project histories
`~/dev/aidev/docs/projects.md` and `~/dev/aidev/docs/ledger.md` (both generated 2026-10-10). The repositories were
only read. No builds were run in them, because a build writes into a tree outside `whatember`. Wherever this dossier
says "verified", the evidence is a line count, a grep, or a quoted file, and the method is given.

---

## 0. Reading guide and two corrections to the brief

The brief that commissioned this strand made two assumptions that the primary sources contradict. Anyone reading
this strand should take these in first.

| # | Brief's assumption | What the sources show | Evidence |
|---|---|---|---|
| C1 | EKOS is ember's Enterprise Knowledge Compiler | **EKOS is alexeyban's project.** `emberian/EKOS` is a fork that matches upstream. ember has **0 commits** in it (508 from alexeyban, 1 from ekaterina safrygina). Ember's own work is **VerEKOS** (`~/dev/verekos`, 198 commits, all by ember arlynx, all on 2026-10-19). | `git log --author=ember` is empty in `~/dev/EKOS`; the memory `verekos-sibling-project.md` says: "ember is a fan of EKOS, not its author" |
| C2 | EKOS turns informal knowledge into "a 190-theorem Lean 4 proof spine over minidregg" | That proof spine belongs to **VerEKOS's `world/`**, not to EKOS. EKOS is 176 k lines of Rust with no proofs. The count checks out: **193 `theorem`/`lemma` declarations** across 19 files in `verekos/world/World/` (the closeout says "190-odd"), no `sorry`/`axiom`, Lean `v4.30.0`, with minidregg as a dependency pinned at `dcab86da`. VerEKOS was **started and closed out on the same day** (2026-10-19). | `grep -rhoE '^\s*(theorem\|lemma) ' World … \| wc -l` → 193; `project/CLOSEOUT-2026-10-19.md` |

There is also an **authorship map** that the brief did not draw. Several repositories in this vertical belong to
**spwashi (Sam Washington)**, ember's collaborator, who owns the meaning of SPW. ember worked as an implementer
("codemonk") or reviewer on them:

| Repo | Primary author(s) | ember's role | Remote |
|---|---|---|---|
| `app.factshift.com` | Sam Washington / spwashi (281 commits, 2023-11-02 → 2024-10-30) | none in git; later re-imported into factshift-redux | `factshift/app.factshift.com` |
| `spw-workbench` | spwashi (518 commits, 2026-01-08 → 2026-10-03) | 2 commits (`f424cf4`, `93ff88e`, 2026-07-23: CLI path checks, Neovim LSP mount following) | `spwashi/spw-workbench` |
| `spweebo'ard` | ember arlynx (13 commits, 2026-01-05..06) | sole implementer of spwashi's semantics | `spwplace/spweeboard` |
| `spween` | ember arlynx (6 commits) | author | `spwplace/spween` |
| `curricularizedbooks` | ember arlynx (3 commits, 2026-04-30, kimi session) | author | `spwplace/curricularizedbooks` |
| `factshift-redux` | ember arlynx (16 commits, 2025-10-10..11) | author (domain model, AI-generated) | `emberian/factshift-redux` |
| `EKOS` | alexeyban (508) | fan, upstream critic (11 issues filed) | `alexeyban/EKOS` |
| `verekos` | ember arlynx (198) | author / root orchestrator | `emberian/verekos` |
| `abcdeez`, `abcdeez2` | ember arlynx (77 / 48) | author | `emberian/abcdeez` |
| `annas-mcp` | iosifache (23) | 3 commits (DOI, SciDB, download fixes) | `emberian/annas-mcp` fork |
| `semantic-scholar-fastmcp-mcp-server` | yuzongmin et al. | 3 commits (2026-02-09) | `emberian/…` fork |
| `lunar-logseq`, `ticklogseq` | ember arlynx (236 / 94, logseq-plugin-git autocommits) | author | local bare repos in `~/shitheap/` |

`~/dev/aidev/docs/projects.md:55` sorts most of this into one bucket: "Work done for or with other people: … spwashi's SPW
notation (spweebo'ard keyboard, factshift) … These end when the engagement ends. None has a successor in ember's own
tree."

Hellas does not appear anywhere in this vertical, and nothing here is attributed to it.

---

## 1. The vertical at a glance

```
                         ┌──────────────────────── COGNITIVE LEARNING ─────────────────────────┐
                         │                                                                     │
   PAPER.md (theory) ──► abcdeez2 (44 kLoC research monolith, 2025-08-08..10)                   │
                         │        │  "contract ; reorganize"  b6e4310 / 6ce24be                 │
                         │        ▼                                                            │
                         │  abcdeez  v0.0.17 (1.4 kLoC core + Xilem app, iOS/web/desktop,       │
                         │           2025-08-11..15)   ◄── OLD_FUNCTIONALITY_NEEDED.md (648 L)  │
                         │        │                                                            │
                         │        ├── -live-dev-env(-2)-abcdeez   (TinyEMU→CheerpX Alpine VM IDE)│
                         │        └── -live-web-editor-abcdeez    (Monaco + cargo→WASM hot reload)│
                         │                                                                     │
                         │  curricularizedbooks / BookLevel (2026-04-30)  — no shared code     │
                         └─────────────────────────────────────────────────────────────────────┘

   ┌──────────── SPW NOTATION FAMILY (spwashi's semantics) ─────────────┐
   │ app.factshift.com (d3 force canvas + "spw" command mode, 2023–24)  │
   │      └─► factshift-redux (Rust domain model + chumsky spw_parser)  │
   │ spweebo'ard (Android IME: SPW → llama.cpp → prose, 2026-01-05..06) │
   │ spwsft (Unsloth LoRA on GLM-4.7-Flash for SPW pairs, 2026-01-20)   │
   │ spw-workbench (spwashi: parser/runtime/LSP/CLI, 520 commits)       │
   │      └─► breadstuffs ".spw hypersemantic tree" (2026-07-23)        │
   │ spween (narrative DSL + parsers tutorial; used by delvetalk)       │
   └────────────────────────────────────────────────────────────────────┘

   ┌────────────── ENTERPRISE KNOWLEDGE COMPILATION ─────────────────────┐
   │ EKOS (alexeyban; 35 crates, 176 kLoC Rust, 211 RFCs, 282 devlogs)   │
   │      ▲ 11 upstream issues (#10–#20)        │ fixtures as scoreboard │
   │      │                                     ▼                        │
   │ verekos (ember, one day): world/ Lean model, 193 theorems           │
   │      over minidregg @ dcab86da ; map/ ; check/ ; slice1/ ; reader/  │
   │      └─► CLOSEOUT: claim/receipt model carries over to minidregg    │
   └─────────────────────────────────────────────────────────────────────┘

   ┌──────── PERSONAL / COLLECTIVE KNOWLEDGE SUBSTRATE (2023) ──────────┐
   │ lunar-logseq (lunar.town collective graph), ticklogseq, lunar.town │
   └────────────────────────────────────────────────────────────────────┘
   ┌──────── RESEARCH-RETRIEVAL TOOLING (2026-02-08..09) ───────────────┐
   │ annas-mcp (fork, +DOI/SciDB), semantic-scholar-fastmcp (fork, +2 tools) │
   └────────────────────────────────────────────────────────────────────┘
```

**Summary matrix**

| Project | Dates (git) | Commits | Size | Maturity |
|---|---|---|---|---|
| abcdeez2 | 2025-08-08 → 08-10 | 48 | core 44,404 L Rust | **Compost/Superseded** (mined by abcdeez) |
| abcdeez | 2025-08-08 → 08-15 | 77 | core 1,427 L; xilem-app 8,833 L | **L2 Prototype** (ships on 4 targets; the model is a heuristic) |
| abcdeez-spec | ~2025-08-10 (no git) | — | 18,574 L of spec text | L0/L1 (AI-generated reverse spec) |
| -live-dev-env(-2), -live-web-editor | 2025-08-11 (no git) | — | JS + VM scripts | **L1 Spike**, frozen |
| curricularizedbooks | 2026-04-30 | 3 | 2,383 L TS app + 10 book JSONs | **L2 Prototype** (static site; no scheduler) |
| app.factshift.com | 2023-11-02 → 2024-10-30 | 281 | 5,412 L JS | L2 (spwashi's; deployed as a site) |
| factshift-redux | 2025-10-10 → 10-11 | 16 | domain 3,387 L; spw_parser 1,228 L | **L1 Spike** / Frozen-for-Rethink |
| spweebo'ard | 2026-01-05 → 01-06 | 13 | core 6,688 L Rust + Kotlin | **L1→L2**, abandoned (Android crashed, iOS never started) |
| spwsft | 2026-01-20 | 1 | 2 scripts | L0/L1 |
| spween | 2026-01-05 → 07-13 | 6 | 3,076 L Rust + 6 docs | **L2** (library; tutorial; used by delvetalk) |
| spw-workbench | 2026-01-08 → 10-03 | 520 | packages + 3 editor extensions | L3/L4 (spwashi's; mounted in breadstuffs) |
| EKOS (upstream) | 2026-07-11 → 10-19 | 509 | 176,172 L Rust | L4 (alexeyban's; installers, Docker, ekos.dev) |
| verekos | 2026-10-19 (one day) | 198 | world/ 5,358 L Lean, 193 thms | **L3 Proved core → Frozen-for-Rethink** (paused by closeout) |
| lunar-logseq / ticklogseq | 2023-03-13 → 04-05 | 236 / 94 | 40 + 1 pages | Compost (historical) |
| annas-mcp / semantic-scholar | 2026-02-08..09 | +3 / +3 | forks | L4 (in daily use as MCP tools) |

---

## 2. abcdeez: adaptive training for graph-coded mental models

### 2.1 The theory: `abcdeez/PAPER.md` (226 lines)

The whole family descends from one paper draft, *"Adaptive Training for Flexible Skill Acquisition: Building Navigable
Mental Models of Graph-Structured Tasks"*. The paper is **not** about spaced repetition of isolated items. Its
thesis, verbatim:

> "**mastery of structured knowledge should imply flexible, bidirectional access and adaptive traversal, not just a
> parroted sequence.**"

> "Traditional training often inadvertently **linearizes** this rich structure … Human studies show that without
> explicit training, people tend to impose a total order even when presented with partial orders."

Its five contributions (§1): a unified probabilistic learner model over graph structure, a coverage-optimal task
battery, an EIG scheduler, behavioural metrics, and a pre-registered study design.

**Domain.** The paper writes the domain as a graph `G = (V, E, R)`, where `R` holds semantic relations such as `is_vowel`.

**Latent learner state (§3.2):**

| Symbol | Meaning | Topology |
|---|---|---|
| `z_v ∈ ℝ` / `[0,2π)` / `ℝ^D` | latent node position | linear / cyclic / DAG (soft inequalities, optionally hyperbolic) |
| `θ_o` | operation proficiency (successor, predecessor, k-jump, shortest-path) | IRT-like ability |
| `s_v(t)` | memory strength with decay | this is where spaced repetition lives |
| `K_ij` | confusability kernel, e.g. `w₁ exp(−‖z_i−z_j‖²/ρ²)` | "locality of errors" |
| `B` | latent chunk boundaries | add RT and error cost when crossed |

**Response model (§3.3):**
- Pairwise order: `p(u ≺ v) = σ(β_op (z_v − z_u) + K_uv)` (Luce/Bradley-Terry).
- Operation accuracy: `σ(α_o(η(q) − b_o − δ_boundary·1[boundary] − span_cost(m) − λ s_v(t)))`.
- RT: Ex-Gaussian `ExG(μ, σ, τ)` with `μ = λ₀ + λ₁·distance + λ₂·1[reverse] + λ₃·1[boundary] − λ₄ s_v(t) + u_subj + u_o`.
  The paper also allows a strategy mixture `π·ExG_serial_scan + (1−π)·ExG_direct_index`.

**Selection (§3.4):** `q* = argmax_q E[KL(p(θ|D_t) ‖ p(θ|D_t, response to q))]`, filtered to a 70–80% success zone, with
ε-greedy exploration.

**Task battery (§4).** Ordered sequences: pairwise order, successor/predecessor, k-jump, forward and reverse segment
recital (a "reverse-N treadmill"), boundary bridging, missing-item completion, and index mapping. Cycles: wraparound
comparison and shortest cyclic distance. DAGs: comparability, ancestor queries, linear extension, minimal and maximal
elements, insertion. General graphs: shortest path, next step, landmarks, macros. Transfer tasks: filtering,
projection switching, isomorphic transfer.

**Metrics (§5).** Bidirectionality index `ΔRT_rev−fwd → 0`; symbolic-distance slope `→ 0`; wrap penalty; poset
fidelity (entropy over the linear extensions a learner generates); locality of errors; strategy-shift index `π_t`;
transfer index.

**Study (§6).** A synthetic 26-glyph alphabet or a 7-node DAG. Conditions are Adaptive-GCM versus a non-adaptive
linear group (a "mere practice" control) versus a further control. Hypotheses: H1 representational shift (`λ₁ → 0`),
H2 seam smoothing (`δ_boundary` falls), H4 transfer to an isomorphic graph.

This is the most intellectually serious artefact in the vertical. It takes a precise position: spaced repetition
optimises item forgetting curves, while this system optimises **information about the learner's internal graph**.
The paper's own words (§2.3): "Instead of merely optimizing the recall probability of individual *items*, our
scheduler prioritizes queries that maximize **expected information gain** about the underlying *graph structure*
itself."

### 2.2 abcdeez2: the research monolith (`~/dev/abcdeez2`, 48 commits, 2025-08-08 → 08-10)

**Maturity: Compost/Superseded.** It is kept as a mine for parts. The current app's
`OLD_FUNCTIONALITY_NEEDED.md` points back to `../abcdeez2/xilem-app/src`.

History: `c4cb956 claude-code: first draft` (08-08). Then a long run of `claude-code: iter`, `hurtling forward`, `wow`,
`4b7dc1a gpt-5: please fix errors`, `b6e4310 contract ; reorganize`, `6ce24be contraction`, `f9e8ce0 tests... pass?`,
`a28bc0d claude: create core book`, and finally `c235c3f claude-code: iter web-backend` (08-10).

In two days the core grew to **44,404 lines** of Rust. The largest modules (`wc -l`):

| Module | Lines | What it is |
|---|---|---|
| `core/src/data/export.rs` | 2,372 | research data export |
| `core/src/ui/research_dashboard.rs` | 2,195 | experiment dashboard |
| `core/src/compliance/irb.rs` | 1,769 | IRB application and consent-form generation |
| `core/src/statistics/core.rs` | 1,626 | Ex-Gaussian, quartiles, Shapiro-Wilk |
| `core/src/bin/research_backend.rs` | 1,562 | — |
| `core/src/protocol/version_control.rs` | 1,547 | protocol versioning |
| `core/src/learning/bayesian.rs` | 1,415 | **the real EIG engine** |
| `core/src/compliance/citation_manager.rs` | 1,293 | — |
| `core/src/experiments/ab_testing.rs` | 1,162 | — |
| `core/src/data/sensor_integration.rs` | 1,145 | EEG / GSR / eye tracker |
| `core/src/data/audio_recording.rs` | 1,074 | think-aloud protocol |
| `core/src/statistics/mixed_effects.rs` | 1,055 | — |
| `core/src/learning/hierarchical_bayes.rs` | 946 | partial pooling |
| `core/src/learning/strategy_mixture.rs` | 834 | serial scan vs direct index |

The parts actually worth reviving are in `learning/` and `core/topology.rs`:

- `core/src/learning/bayesian.rs`: `BayesianLearnerModel`; `PosteriorDistribution { entropy(), update(obs, var),
  kl_divergence(&other) }` (Gaussian conjugate updates); `ChunkBoundaryPosterior`; `calculate_eig`,
  **`monte_carlo_eig(task, n_samples)`**, **`adaptive_monte_carlo_eig(task) -> (f64, usize)`**, `rank_tasks_by_eig`,
  `total_entropy`; `struct MonteCarloEIG`.
- `core/src/core/topology.rs`: a general `Topology` with `new_linear`, `new_cyclic`, `alphabet()`, `days_of_week()`,
  `new_dag`, `new_graph(…, f64 weights)`, `example_dag`, `get_k_jump`, `is_before`, `has_path`, `are_comparable`,
  `get_topological_sort`, `shortest_path`, `get_segment`. **This is the part of the paper that is actually built**:
  linear, cyclic, DAG and general graphs. The current abcdeez dropped it.
- `learning/macro_learning.rs`, `learning/transfer_learning.rs`, `tasks/music.rs`, `tasks/navigation.rs`,
  `tasks/boundaries.rs`.

The repository also reviews itself. `abcdeez2/CORE_REVIEW_NOTES.md` (314 lines, dated 2025-08-11, "Reviewer: Claude
Code Analysis") is a frank account of what went wrong:

> "**CRITICAL**: The Ex-Gaussian PDF implementation has a fundamental mathematical error"
> (`statistics/core.rs:157-178`)

> "**HIGH**: The entire mixed-effects implementation is severely oversimplified … E-step and M-step are not
> implementing actual EM algorithm … Results would be statistically meaningless for hierarchical data analysis"

> Quartiles by `sorted[len/4]` with no interpolation; Shapiro-Wilk with "crude approximations"; "50+ instances of
> `.unwrap()`"; nodes identified by `String` instead of a `NodeId` newtype.

`abcdeez2/STATUS.md` (240 lines) records a crate-name split-brain: `core/src/main.rs` imports `graph_learning_core`
while the crate is named `abcdeez_core`, and `xilem-app/main.rs` calls `graph_learning_app::run()`. In the same
breath it praises "Research-Grade Implementation", "Production-Ready Backend … OAuth (Apple, GitHub) … automatic
Let's Encrypt". `REORGANIZATION.md` (351 lines) proposes reorganising "42+ files in flat src/".

**Diagnosis.** Agents built the *institution* around the study: IRB forms, federation across sites, GDPR/HIPAA
settings, sensor drivers, Bayesian factors, power analysis. They did this before any learner had used the core loop,
and the statistics under it were wrong. The `contract ; reorganize` commits are ember noticing and cutting.

### 2.3 abcdeez: the shipped contraction (`~/dev/abcdeez`, v0.0.17, 77 commits)

**Maturity: L2 Prototype.** It builds and runs on iOS, web/PWA and desktop, and has a server. The learner model is
heuristic, not Bayesian.

Timeline (from `git log`): `c4cb956 claude-code: first draft` (08-08, shared ancestry with abcdeez2) → `bc4d8f8 all
builds...` → `6163e83 builds and runs on ios` → `d0ed7af PWA` → `0a74177 runs everywhere!!!` (08-11) → `a9afab5 old
functionality ported forward` → `92aec05 more old functionality` → versions `v0.0.11` … `ba53d6b 0.0.17` (08-12) →
`2909c95 save some files before we delete them lol` (08-15, last commit).

Workspace (`Cargo.toml`): members `core`, `web-backend`, `xilem-app`; `version = "0.0.17"`; `description = "Alphabet
mastery tool"`; `homepage = "https://abcdeez.fg-goose.online"`; `[profile.dist]` with `lto = "thin"` (cargo-dist).
`CLAUDE.md` contains only the check commands (`RUSTFLAGS=-Awarnings cargo check -p abcdeez-core` / `web-backend` /
`abcdeez-app` / `abcdeez-web`, then `./build-all.sh --desktop --web`). CI lives in `.github/workflows/`:
`deploy-live-env.yml`, `deploy-pwa.yml`, `mobile-web-builds.yml`, `release.yml`.

**Core data model** (`core/src`, 1,427 lines):

```rust
// alphabet.rs
pub struct Letter(u8);                         // next/prev/forward_jump/backward_jump/distance_to/is_vowel
fn chunk_id(&self) -> u8                       // ABC-DEF-GHI-JKL-MNO-PQR-STU-VWX-YZ
fn is_chunk_boundary(&self) -> bool            // matches!(self.0, 3|6|9|12|15|18|21|24)
AlphabetDomain::confusability_score(a, b)

// task.rs
pub enum TaskType {
    WhatComesAfter{letter}, WhatComesBefore{letter},
    IsBeforeAfter{first, second, is_before},
    ForwardJump{start, distance}, BackwardJump{start, distance},
    ReciteForward{start, length}, ReciteBackward{start, length},
    WhatIsAtPosition{position}, WhatPositionIs{letter},
    HowFarBetween{first, second},
}

// learner.rs
pub struct LearnerState {
    forward_proficiency, backward_proficiency, position_proficiency, jump_proficiency: f64,
    letter_strengths: HashMap<Letter, f64>,
    confusion_matrix: HashMap<(Letter, Letter), f64>,
    response_history: Vec<Response>,
    avg_response_time: Duration, response_time_by_distance: HashMap<i8, Duration>,
    chunk_boundary_penalty: f64,          // init 1.5, floored at 1.0
    sessions_completed: u32, total_tasks_completed: u32,
}

// stats.rs
pub struct MasteryMetrics {
    bidirectionality_index,   // RT(backward) - RT(forward)
    symbolic_distance_slope,  // slope of RT vs distance
    chunk_boundary_penalty, uses_direct_retrieval: bool, position_accuracy,
    mastery_score, forward_fluency, backward_fluency, random_access_ability,
    structural_understanding,
}
```

**What the shipped algorithm actually does.** This is verified by reading `learner.rs:64-170` and `task.rs:247-343`.

- `update_from_response` applies a **fixed-step proficiency update**: `learning_rate = 0.1`; a correct answer adds
  `+0.1`, a wrong one `−0.05`, then `clamp(0,1)`. `ReciteBackward` uses `update * 1.5`. There is no posterior and no
  forgetting curve.
- `estimate_success_probability` multiplies a proficiency by `letter_strengths[letter]` (default 0.5) and clamps the
  result to `[0.1, 0.9]`.
- `LearnerModel::compute_information_gain` is binary entropy of the success probability times `difficulty_estimate`.
  **Nothing calls it.** `grep -rn compute_information_gain` finds only its definition (`learner.rs:253`).
- `TaskScheduler::select_next_task` is ε-greedy. Exploitation (`generate_adaptive_task`) means: "if
  `forward_proficiency > backward_proficiency + 0.2` → 70% `WhatComesBefore`, else `ReciteBackward`"; otherwise draw
  a random task and, if `|difficulty − target| > 0.3`, draw **once** more. The code comments say so honestly: "For
  now, generate based on recent performance".

So the paper's theory (EIG, Ex-Gaussian, posterior over `z_v`) lives in **abcdeez2**, while the shipping product
(abcdeez) has the metrics *names* and a heuristic loop. Neither has the **forgetting curve `s_v(t)`**, which is the
one ingredient that would make this a spaced-repetition system.

**Server** (`web-backend/src/main.rs`): Axum + sqlx SQLite with migrations; `LearnerState` is serialised as JSON in
the `learner_state` column. Routes: `/health`, `POST /api/users`, `GET /api/users/:user_id`, `POST /api/sessions`,
`GET /api/sessions/:id`, `POST /api/sessions/:id/complete`, `GET /api/sessions/:id/next-task`,
`POST /api/sessions/:id/submit`, `GET /api/users/:id/stats`, `GET /api/users/:id/mastery`.

**App** (`xilem-app/src`, 8,833 lines): `views/{dashboard,settings,welcome,widget_gallery}.rs`,
`viz/{charts,chart_components,widgets}.rs`, `services/{api,timing,websocket}.rs`, `platform/native.rs`;
`xilem-cross-platform/` with `ios-src`, `make_xcframework.sh`, `xilem_abcdeez_mobile.xcodeproj`, `web/`, `desktop/`.

**`OLD_FUNCTIONALITY_NEEDED.md` (648 lines)** lists every abcdeez2 feature that was not carried forward: the
ResearchController with LearningCurve/RetentionTest/InterferenceStudy/AdaptiveScheduling, t-tests/ANOVA/Cohen's d/BF₁₀,
the IRB system, audio recording, EEG/GSR/eye tracking, and a "Federation Network" (GDPR/HIPAA, encryption keys). It
is a backlog of the institution, not the science.

**Working-tree state (observed 2026-11-02, read-only).** `git status` shows `M Cargo.lock`, `M Cargo.toml`, and
deleted `PAPER_IMPLEMENTATION_COMPARISON_REPORT.md`, `PROJECT_SPEC.md`, `REVIEW_NOTES.md` and `analysis/*.R`, which
were never committed after `2909c95`. Three Apple keys (`AuthKey_HWPZ42VS85.p8`, `apns_AuthKey_J48DF9WZD3.p8`,
`apns_prod_AuthKey_3V62J5KPZ8.p8`) sit in the repo root. They are **untracked but not gitignored**
(`git check-ignore` returns nothing; `git log --all -- '*.p8'` is empty, so they were never committed). A single
`git add -A` would publish production APNs keys to `emberian/abcdeez`.

### 2.4 abcdeez-spec (no git; files dated 2025-08-10)

**Maturity: L0/L1.** These are AI-generated *reverse* specifications of abcdeez2: `APP_DESC.md` (390 lines,
"Adaptive Learning System — Complete Application Specification"), `APP_DESC_notes.md` (an agent's progress
checklist: "8 distinct screens … 23+ reusable UI components … Easter egg (Little Crab companion)"),
`app-spec-1/2.md`, `core-spec.txt` (3,777 lines), `web-backend-report.txt` (3,692), `xilem-ui-crate-spec.txt` (3,079),
`xilem-ui-spec.txt` (5,477), and two Xilem references. That is 18,574 lines in total. They look like the input for a
clean-room rewrite (the contraction in §2.3). They describe the monolith in full, including the Apple Sign-In,
federation and PWA paths.

### 2.5 The live environments (no git, 2025-08-11)

**Maturity: L1 Spike, frozen.** Here the goal was to put abcdeez's *own development loop* in the browser.

- `~/dev/-live-dev-env-abcdeez` (README is a "Live Dev Env Build Guide"): `vm/build-tinyemu.sh`,
  `vm/build-alpine-rust-vm.sh` (an Alpine+Rust Docker image that "prebuilds `xilem-cross-platform/web` and installs
  the ABCDEEZ guest agent"), `vm/create-vm-image.sh` → `dist/tinyemu/alpine-rust-rootfs.bin` (ext4).
- `~/dev/-live-dev-env2-abcdeez`: "Real Linux VM: JSLinux/TinyEMU running Alpine Linux in browser … Monaco Editor …
  Offline Capable". The README still contains a `yourusername.github.io` placeholder.
- `abcdeez/live_dev_env/` (in-repo successor): `CHEERPX_MIGRATION.md` describes the move "Browser → TinyEMU.js →
  RISC-V Emulation → Alpine Linux → Rust" ⇒ "Browser → CheerpX (WASM) → x86 Virtualization → Alpine Linux → Rust".
  Its `CLAUDE.md` holds one rule: "never mock cheerpx".
- `~/dev/-live-web-editor-abcdeez`: "Live Rust/WASM Web Editor": Monaco, an Express server that runs `cargo build`,
  `rustfmt`, a hot-reload manager that "Preserves state between reloads". Its compiler service "Falls back to mock
  compilation for demo". It also contains `wasm-compiler/`, `vm-toolchain/`, `sw-coi.js` (a COOP/COEP service worker
  for SharedArrayBuffer) and `real-compiler.html`.

The "never mock cheerpx" rule and the "falls back to mock compilation" line contradict each other, and that
contradiction is where this spike stopped.

### 2.6 Cycles, revival, attention: cognitive-learning half

**Unclosed cycles and missing links**

1. **Theory → product.** The EIG engine (`abcdeez2/core/src/learning/bayesian.rs::monte_carlo_eig`) and the general
   `Topology` were never ported into `abcdeez/core`. *Way through:* port `PosteriorDistribution` and `Topology` into
   the 1.4 k-line core behind a `NodeId` newtype, replace `generate_adaptive_task` with `rank_tasks_by_eig`, and keep
   ε-greedy plus the 70–80% filter. Fix the Ex-Gaussian first, or exclude it.
2. **The forgetting curve is missing everywhere.** `s_v(t)` appears in the paper and in no code. This is the link to
   every "SRS" ambition in the vertical, including BookLevel's "Spaced Repetition: Review prompts at expanding
   intervals". *Way through:* one `MemoryStrength { last_seen, stability }` per (node, op) with a half-life update
   (FSRS-shaped). The scheduler then mixes EIG with retrieval-probability decay.
3. **Domain generality.** The shipped app knows only `Letter(u8)`. The paper's point is DAGs and menus. *Way
   through:* abcdeez2's `Topology::new_dag` / `example_dag` already exist.
4. **Study → data.** `analysis/*.R` (preprocessing, visualizations, DATA_DICTIONARY) was deleted from the working
   tree without being committed. Nothing in either repo records a single participant. H1/H2/H4 are untested.
5. **Live dev env ↔ app.** The VM images were built for the app, but no evidence shows a working end-to-end
   in-browser cargo build.

**Promising and ready for revival**

- PAPER.md as a research programme. Only a small kernel is needed to test **H1 (`λ₁ → 0`)**: the synthetic-glyph
  alphabet, `IsBeforeAfter` items, RT logging (already in `services/timing.rs`), and a regression of RT on distance
  (already the `symbolic_distance_slope` field). Everything else in the research institution can stay composted.
- The cross-platform Xilem shell (`6163e83 builds and runs on ios`, PWA, desktop) is a reusable template for any
  small learning app.
- `abcdeez2/core/src/learning/strategy_mixture.rs` (834 lines), the serial-scan / direct-index mixture. It is the
  paper's most original measurement idea, and it deserves an audit rather than a rewrite.

**Struggling / needs Ember's attention**

- `HOLE[design]`: **is abcdeez a research instrument or a product?** abcdeez2 built a lab (IRB, federation, sensors).
  abcdeez built an "Alphabet mastery tool". `OLD_FUNCTIONALITY_NEEDED.md` pulls the lab back in. Only ember can say
  which one the next commit serves.
- Statistical correctness. `CORE_REVIEW_NOTES.md` flags the Ex-Gaussian PDF, quartiles, Shapiro-Wilk and the mixed
  effects. If any abcdeez2 statistics come back, they need a checker (an R or SciPy reference on fixed vectors), not
  agent confidence.
- Hygiene. The uncommitted deletions and the unignored `.p8` keys in `~/dev/abcdeez` need a human decision. Keys
  cannot be recovered after an accidental push.

---

## 3. BookLevel (`curricularizedbooks`)

### 3.1 curricularizedbooks / BookLevel (`spwplace/curricularizedbooks`, 2026-04-30)

**Maturity: L2 Prototype.** It is a static React site on GitHub Pages
(`spwplace.github.io/curricularizedbooks`). It has gamification but no spaced-repetition scheduler.

- Commits: `acfc6b0 initial commit`, `3d358cf wow a readme`, `8aeb540 dev`, all on 2026-04-30. The ledger records the
  harness as one **kimi** session.
- `plan.md` describes a five-stage agent plan: "Content Extractor (10 parallel sub-agents, one per book)" → Learning
  Architect → `vibecoding-webapp-swarm` design → build → deploy via `deploy_website`.
- **Data**: `book_01_design_for_mind.json` … `book_10_think_like_cto.json`. Each is a dict with `book_metadata,
  chapters, golden_nuggets, skill_tracks, reflection_questions, practice_exercises, prerequisites, next_steps,
  key_cognitive_principles, cognitive_science_references`. There are four paths: Mindset & Mastery (Hermans's *The
  Programmer's Brain*, Yocco's *Design for the Mind*), Leadership & Career, Code Craft, and Rust Mastery.
- **App**: `app/src/data/curriculum.ts` (2,145 lines); `hooks/useGamification.ts` (238 lines). The
  learning-science core is `localStorage['booklevel-progress']`, `calculateLevel(xp) = max(1, ceil(xp/100))`, and
  `XP_VALUES[rating]` per chapter rating.
- **Gap**: plan.md lists "Spaced Repetition: Review prompts at expanding intervals", and nothing implements it (no
  interval, due date or review queue in `useGamification.ts`).

**How it connects to abcdeez:** through ideas only. BookLevel's chapters, prerequisites and skill tracks *are* a DAG
of exactly the kind PAPER.md §4.3 is about, and abcdeez2's `Topology::new_dag` is the engine that could drill it. No
code is shared.

**Unclosed cycle:** BookLevel's prerequisites → abcdeez `Topology::new_dag` → EIG/forgetting scheduler → BookLevel
review queue. **Promising:** the 10 structured JSONs are a ready, real-world domain for the abcdeez study instead of
synthetic glyphs. They are also copyrighted book summaries, so publishing them is a decision for ember (and spwplace).

---

## 4. factshift: the knowledge-ecosystem vision

### 4.1 app.factshift.com (spwashi, 281 commits, 2023-11-02 → 2024-10-30)

**Maturity: L2, spwashi's.** It was deployed as a site (it had a Plausible snippet `fe99d5f` and Netlify, which
`c2567ba` removed).

The app is a Vite SPA (`package.json` `"version": "0.0.2-alpha"`; deps `d3 ^7.8.5`, `ace-builds`, `md5`; dev `sass`,
`typescript`, `vite ^5`). It has 5,412 lines of JS outside `vendor`.

- `src/js/modes/`: `dataindex`, `direct`, `mapfilter`, `querystring`, `reflex`, **`spw`**, `story`.
- `src/js/simulation/`: `forces.js`, `active-forces.js`, `reinit.js`, `nodes/`, `edges/`, `rects/`.
- `src/js/ui/`: `focal-point.js`, `hotkey-buttons.js`, `websocket-container.js`, `enable-sounds-button.js`.
- `src/_spwashi@/`: a special looped page (`scripts/{env,loop,spwashi.js,state}`).
- Late history: `bf68c99 revisiting story mode`, `18e9240 updated boon command`, `48a39d7 honk`, `79240fa [2024-09-B]
  websockets`, `2ba127a [v0.0.2-alpha]: client`.

The Gemini/ChatGPT-style review preserved as `factshift-redux/specs/frontend-review.md` (155 lines) makes the
architectural diagnosis:

> "The primary area for improvement is its **architecture**, which relies heavily on a single, mutable global object
> (`window.spwashi`) for all state management." … "Replace the use of `eval()` …"

The same review praises the "'spw' Command Language: A custom, line-based text language … simple commands (`bonk`,
`group`) and key-value directives (`charge=-100`, `add=50`)".

### 4.2 The vision, in spwashi's words (`factshift-redux/README`)

The README is a raw transcript of a design conversation, and it is the only place the *product* intent is written
down:

> "-'a certain number of nodes allocated to a company and then some sort of mapping scheme to like _____ (billions?)
> such that when people visit factshift.com they can click into an ecosystem/ecology eg something specific to a
> company's ecology or its arc'"
>
> "- wondering how a company might represent hype around their knowledge base / - seasonal orbs, events,
> interactions, flows"
>
> "-i also don't like the architecture of the simulation. i think it's fun bc bugs :) -spwashi"
>
> "- weekly publication rhythm with at least 7 combinations of a CSS, JS, and HTML file available for download as a
> complete webpage by an audience of semi-technical fans of artists"
>
> "- ideally each build target would have an entirely static version of this application with route-specific
> awareness of server connectivity"

`aidev/docs/projects.md:475` summarises the 2025-10-11 session as a backend for "a 'hybrid video editor/course
management system/mmorpg' knowledge-ecosystem site". Read together, these show the vision is **a publishing-first,
local-first content graph with game-like seasons and realms**, and a "company ecology" as a tenant.

### 4.3 factshift-redux (ember, 16 commits, 2025-10-10 → 10-11)

**Maturity: L1 Spike → Frozen-for-Rethink.** It is a typed domain model. The persistence, API and CLI crates are
empty `fn main() {}` stubs.

History: `489e380 initial commit` → `0848c29 import gh:spwashi/app.factshift.com latest` → `b46bce5 llms generate us
some files` → `1744afa cargo workspace` → … `c69068b ontology` → `5a06bd7 clauded it up...` → `7ca1714 a plan` →
`3ed9662 macros...`. The original `~/dev/factshift` directory is gone ("no trace on disk", ledger row 95). It had 51
prompts on 2025-10-11. The aidev history quotes the 2025-10-11 prompt: "We need to interate on crates/rpc/src/lib.rs
… better utilize crates like strum, validator/garde". A 2026-01-04 review session opens with "Sonnet3.5 wrote all
thhis I think? I want you to be very critical" (session 04cf0113).

Crate sizes (lines of `.rs`): `domain` 3,387; `spw_parser` 1,228; `gen-factshift` 286; `rpc` 211; `macros` 166;
`backend` 2; `cli` 2.

**Domain model** (`crates/domain/src/`, flat modules):

| Module | Types (verbatim names) |
|---|---|
| `content.rs` | `enum Realm { Boon, Bane, Bone, Bonk, Honk, Lore, Factshift }`, `ContentStatus`, `ContentType` (incl. `LoreArtifact`, "Boon squares, cards, props"), `AccessibilitySpec`, `UsagePolicy`, `ContentItem`, `ContentRelation`, `RelationKind`, `SearchFilter` |
| `learning.rs` | `enum BloomLevel { Remember, Understand, Apply, Analyze, Evaluate, Create }`, `LearningObjective`, `PadLog { pleasantness, activation, dominance: PadValue }` (PAD affect model), `ReflectionMethod`, `Reflection`, `PathNode`, `LearningPath`, `enum CycleStage { Seed, Grow, Converge, Harvest }`, `SeasonArc { theme, start, end, objectives }` |
| `addressing.rs` | `Cid`, `ContentCodec`, `ContentAddress` (merkle links), `VectorClock`, `PeerId`, `ConflictStrategy`, `SyncMetadata`, `ReplicationState` |
| `crypto.rs` | `KeyType` (Ed25519, secp256k1, RSA), `SignedData`, `Did`, `DidDocument`, `VerificationMethod`, `VerifiableCredential`, `ContentAttestation` |
| `permissions.rs` (642 L) | `Action`, `Scope` (Content … Realm, Author, Global), `Capability`, `CapabilityDelegation` (attenuation), `CapabilityRevocation` (cascading), `AccessRequest` |
| `layout.rs` (619 L) | CSS `Length` units, transforms, cubic-bezier easing, keyframes, `Composition`/`CompositionLayer`, `Timeline` ("TikTok-style video composition") |
| `primitives.rs` | nutype newtypes `Slug`, `LanguageTag`, `ContrastRatio(f32)`, `PadValue(i8)`, `Title`, `Handle`, … |
| `interchange.rs` | `ArchiveFormat`, `ContentArchive` (see `specs/INTERCHANGE_V1.md`, 544 L) |

The realms (`specs/ONTOLOGY_V2.md`, 558 lines) are spwashi's thematic lenses: **Boon** (playful learning), **Bane**
(challenge), **Bone** (foundation), **Bonk** (humor and disruption), **Honk** (attention and social), **Lore**
(narrative), **Factshift** (meta-reflection). The ontology opens: "Factshift is a content management and learning
system built around: Content-addressable, local-first architecture … Learning-centered design with metacognition
and emotional tracking …".

`PLAN.md` (242 lines, "**Status**: Domain model complete, moving to tooling") marks Phases 1/2/3/4/7/9 as ✅ and
leaves pending: Phase 5 `factshift-macros` (`#[derive(Id)]`, `#[entity]`, `#[rpc]`), Phase 6 `gen-factshift`
(SeaORM + Axum + client + OpenAPI from the domain types), and "Macaroons-Inspired Permissions … Chained HMAC for
tamper-proof delegation".

**`spw_parser`** (chumsky): `pub fn parse(input) -> Result<Vec<raw::ast::Expr>, Vec<Simple<char>>>`. The grammar it
targets is spwashi's `specs/seed.spw`: `^seed[Factshift.Spw.Parser.v0_8_LongExample]{ @meta{author:"spwashi+chatgpt",
version:"0.8.3"} … #grammar{ program := stmt (sep stmt)* EOF; pipe := step ("|" step)*; selector:= "@"+ident … } }`.
That grammar is a "Mini language for canvas control. Supports statements; assignments; calls; selectors; pipes."
It is the same line-based command language as app.factshift.com's `spw` mode, now with a formal grammar.

### 4.4 Cycles, revival, attention: factshift

**Unclosed cycles**
- *Domain → anything that runs.* No persistence, server, CLI or codegen output exists. `gen-factshift` is a clap
  skeleton.
- *Old app ↔ new model.* The imported JS app still uses `window.spwashi` and has not been ported onto the domain
  types.
- *Learning objects ↔ abcdeez.* `LearningPath`/`PathNode`/`BloomLevel` and abcdeez's `Topology` describe the same
  thing (a DAG of objectives) and have never met.

**Promising**
- spwashi's actual stated need is small and concrete: a weekly static publication of seven HTML/CSS/JS combinations,
  a stage-and-publish tool, offline-saveable pages. A static-site build from `ContentArchive` would serve it without
  the DID, VC and macaroon apparatus.
- `PadLog` plus `Reflection` (affect plus metacognition per learning event) is a distinctive data model, and it fits
  abcdeez's response log naturally.

**Struggling / needs Ember's attention**
- `HOLE[design]`: **whose project is this?** `projects.md` classes factshift as work for spwashi that "end[s] when
  the engagement ends". The redux domain was AI-generated in one day, and ember's own 2026-01-04 verdict asked for
  harsh critique of it. Before anyone writes more code, ember and spwashi need to decide whether factshift-redux is
  (a) a gift to spwashi, (b) a scaffold to delete, or (c) the seed of the local-first content layer ember wants
  elsewhere (minidregg already owns content addressing, receipts and capabilities. See §7.4).
- The domain is breadth without load. DIDs, VCs, three key types, macaroons-to-be, CSS transforms and vector clocks
  all exist with no caller. This is the abcdeez2 pattern again.

---

## 5. The SPW symbolic notation family

### 5.1 The notation itself (as recorded in ember's repos)

Taken from `spweebo'ard/dev-plan.md` ("13-symbol semantic alphabet") and the prompt at
`crates/spweeboard-core/src/compiler/prompt.txt`:

```
Symbol  Name          Semantic Role                    | Composition
~       potential     latent possibility, becoming      | Order implies flow:
#       vibration     resonance, frequency, rhythm      |   &@  "from the subject's view"
.       ground        foundation, context, base truth   |   @&  "who holds this view"
?       wonder        inquiry, exploration, openness    | Nesting ≈ prepositions:
!       action        execution, assertion, force       |   ?{Worcester#}
*       value         worth, significance, weight       |   wonder{direction[vibration]}
&       subject       agent, entity, the who            |
@       perspective   viewpoint, lens, frame            |
<>      concept       abstraction, idea, category       |
()      scene         situation, context, narrative     |
[]      mode          state, manner, operational frame  |
{}      direction     vector, intent, trajectory        |
^       integration   synthesis, unification, elevation |
```

Few-shot examples from `prompt.txt`: `&@` → "From where I stand, looking out at what unfolds before me."; `?!` →
"A pause of wonder, then decisive movement forward."; `&[work]` → "The self, dressed in the manner of labor."

spwashi's commit messages in spw-workbench are written *in* SPW: `.[caches] — shelve waves …`, `&[lsp] — land
fragments on their anchor line …`, `![audit] — scan packages …`, `&[seed] — read every stream entry head …`.

### 5.2 spweebo'ard (`spwplace/spweeboard`, ember, 13 commits, 2026-01-05 → 01-06)

**Maturity: L1→L2, abandoned.** It did produce a "functioning android app" (`71c60bf`), but the app crashed
repeatedly afterwards, and iOS got only `f65ae14 ios progress`.

AGENTS.md: "an Android keyboard that uses SPW … Users type symbols … and an on-device LLM interprets these into
natural language. **Key concept**: The keyboard doesn't just send symbols - it interprets them through an LLM."

Architecture:

```
Compose KeyboardLayout.kt ──► SpweeboardService (IME + ViewModel)
        │                              │ UniFFI (uniffi.udl, ffi.rs, "auto-uniffi" 1c2720b)
        ▼                              ▼
  InferenceManager.kt ◄──── spweeboard-core (Rust, 6,688 L)
  ModelDownloadManager.kt     spw/{lexer,token,symbol,parser,ast}.rs   SPW → AST
  (GGUF downloads)            compiler/{prompt.rs,prompt.txt}          AST + Ground → prompt
                              ground/{store.rs}                        "Grounds" = context presets
                              inference/{llama.rs,engine.rs}           llama.cpp bindings
                              buffer/history.rs                        expression history
                              ipc/{client,server,protocol}.rs
```

FFI surface (`ffi.rs`): `SpwError`, `SpwParseResult`, `SpwParseState`, `SpwBuffer { push, pop, clear, get_raw,
is_empty, get_parse_state, parse }`, `validate_spw`, `parse_spw`, `SpwGround`, `SpwGroundContentType`,
`SpwGroundStore::open(path)`. Build requirements (AGENTS.md): "JDK 17 (not GraalVM - causes cryptic errors)", NDK
`29.0.13846066`, four Android Rust targets. Supporting files: `android_app_design.md`, `update_model_sizes.py`,
`ios.sh`.

`aidev/docs/projects.md:201-209`: "242 of its 249 prompts, 125 sessions, 13 commits, all on those two days … The
Android build crashed repeatedly ('App keeps stopping', session 7d310d90), and iOS was never started". ember framed
their own role on 2026-01-05 (708ce1cc): "Scaffold the Rust core and platform shell. Someone else is in charge of the
meaning of spw in practice, i'm just codemonk."

### 5.3 spwsft (`~/dev/spwsft`, 1 commit, 2026-01-20)

**Maturity: L0/L1.** There are two files: `spw_finetune_local.py` ("Unsloth LoRA finetune script for GLM-4.7-Flash
with SPW pairs", `--model unsloth/GLM-4.7-Flash`, `--lora-r 16`, `--max-steps 200`, `--lr 2e-4`, `--max-seq-len 2048`,
`train_on_responses_only`, accepting `prompt/response`, `instruction/output` or `text` JSONL) and
`glm_flash_a100(80gb).py`. **No SPW pair dataset exists in the repo.** The point is clear: replace spweebo'ard's
few-shot `prompt.txt` with a small fine-tuned interpreter. **Missing link:** the corpus of (SPW, ground,
interpretation) triples, which only spwashi can author or approve.

### 5.4 spw-workbench (spwashi, 520 commits; ember 2)

**Maturity: L3/L4. It is spwashi's project.** This is the real home of SPW: "the source-first language, runtime, and
tooling organelle for `.spw` workspaces". Packages: `spw-seed` (lexer/parser), `spw-runtime` (interpreter and
"substrate events"), `spw-lsp`, `spw-cli`. Editor extensions: `vscode-spw`, `intellij-spw`, `neovim-spw`. The mount
contract:

> "The consumer owns `.spw/`; the workbench owns `.spw/_workbench`. … This is an organelle rather than a repository
> center: it supplies machinery, preserves a membrane around ownership, and can be upgraded or removed without making
> consumer canon illegible."

**ember's use of it** (memory `breadstuffs-hypersemantic-tree.md`, 2026-07-23): `~/dev/breadstuffs` was mounted as an
spw consumer ("doctor fully green") with "a 25-surface hypersemantic tree grown from the four-line poem `root.spw`":
10 projections in `topography/` (strata, lanes, trust, valence, laws, horizon, praxis, chronicle, shadow,
polymap-router) and 8 region cards in `regions/` (kernel, metatheory, guardians, settlement, deos, mesh, dreggnet,
intellect). The stated purpose: "hypersemantic multitopography; compact surfaces that summon latent regions of the
codebase in LLMs for fluid ideation, vs. the crystallized Rust/Lean/md. Lenses are deliberately mutable; canon stays
in the crystal." There is a hard rule: "**NEVER run `spw init` against breadstuffs**: it appends its Touch ID commit
gate to an existing `.git/hooks/pre-commit`, and breadstuffs' hook is load-bearing". ember's two upstream commits
(`93ff88e &[neovim] — the LSP follows a mounted consumer from any cwd`, `f424cf4 &[cli] — broken path targets are
checked against the disk`) came out of that mounting.

### 5.5 spween (`spwplace/spween`, ember, 6 commits)

**Maturity: L2 Prototype library.** Despite the name, spween is **not SPW notation**. It is a narrative DSL for
branching game scenes (YAML frontmatter `id`/`title`/`tags`/`weight`, passages, choices, conditions, effects). The
README doubles as a tutorial: "Welcome to Parsers and Interpreters — A hands-on guide using `spween`". `src/` is
3,076 lines: `lexer.rs` (`enum Token { FrontmatterDelim, PassageHeader(SmolStr), ChoiceMarker, EffectMarker, Arrow,
… }`), `parser.rs`, `ast.rs`, `runtime.rs`, `value.rs`, plus a `playground/` WASM build and docs `01-getting-started`
… `06-examples`. Commits: `4d38e32 initial commit` (2026-01-05), `febe459 warmer tone`, `afb5b1f conj/disj`
(01-08), `95980f7 runtime: fire passage entry effects once per passage (fix re-entry re-seeding)` (2026-07-13).
That last fix came from a consumer: `projects.md:425` says DelveTalk is a world "where Objective Bend defines
behavior, **Spween defines scenes** and Lean admits changes".

### 5.6 Cycles, revival, attention: SPW

**Unclosed cycles**
- *SPW → meaning.* The interpretation lives in a few-shot prompt (`prompt.txt`) and is not checked against
  spwashi's canon in spw-workbench. Three parsers now exist (`spweeboard-core/src/spw/`, `factshift-redux/
  crates/spw_parser` (chumsky), `spw-workbench/packages/spw-seed` (TS)) and nothing tests them against one shared
  corpus. *Way through:* make spw-seed's grammar the reference and use its test corpus as a conformance panel for
  the Rust parsers. Better still, delete the Rust parsers and call spw-seed via WASM. This follows ember's "no
  mirrors, no twins" rule (§7.3).
- *spwsft ↔ spweebo'ard.* The fine-tune script has no data and the keyboard has no fine-tuned model.

**Promising**
- The spweebo'ard Rust core, with UniFFI, GGUF model management and Grounds, is a working on-device-LLM keyboard
  scaffold. It is worth keeping, whatever the notation.
- spween is small, documented, and already depended on (delvetalk).

**Struggling / needs Ember's attention**
- `HOLE[design]`: SPW semantics belong to spwashi. ember's stated stance is "i'm just codemonk". Any revival of
  spweebo'ard or spwsft first needs spwashi's go-ahead and a corpus.
- The Android crash loop ("App keeps stopping") was never root-caused in a surviving note. The last commit
  (`cf78c7c android: onboarding, history staleness, guardrails`) does not mention a fix.

---

## 6. EKOS (upstream, alexeyban): what VerEKOS was a sibling of

**Maturity: L4 Deployed. It is not ember's.** This section only describes the object that VerEKOS studied.

From `EKOS/README.md`: "EKOS is the open-source knowledge layer for AI agents: a compiler that turns source code,
SQL, documentation and Git history into evidence-backed knowledge that agents query over MCP." Pipeline: Observation
Layer ("collects facts, no interpretation") → Knowledge Compiler ("normalize → analyze → recover → verify") →
Knowledge Recovery + Identity Resolution → Canonical Knowledge Model (CKM) → Semantic Knowledge Ledger ("append-only,
every fact traceable to evidence") → Runtime / Services → agents via the read-only `ekos mcp serve` (RFC 0013). The
four ledger primitives are **Object, Relationship, Event, Evidence**. The CLI pipeline is `ekos init → build →
recover → resolve → compile → commit`.

Scale (counted 2026-11-02): **35 crates** under `ekos/crates/` (`artifact cli clickhouse-query cluster common
compiler-core compiler-sdk dbt-gen demo-server distributed docs-gen ekl evals identity kir ledger marketing migrate
migrate-* pg-live plpgsql recovery runtime scheduler segment-backend semantic session simulation sql-dialect-sdk`),
**176,172 lines** of Rust, **282 devlogs** (latest `devlog_281.md`), **211 RFC files** split between `docs/rfcs/`
(0001–0024) and `ekos/docs/rfcs/` (0025–0207). The latest commits (2026-10-17..19) are RFC 0197–0207: LLM task
routing "Haiku 5.5 default, MiniMax M3 for ask"; Pentaho/Kettle → lakehouse dbt; `fix(localdocs): read DOCX with
roxmltree + zip 9, drop docx-rs (RUSTSEC-2026-0367/0368/0369)` (`8e3c178`). There is also a Solana token
(`TOKENOMICS.md`: mint `CwubepDFJndzSKFmAMAm9u8Xx3PrizAwSq8hcGimpump`, "967,410,000 EKOS (current)") and a
`VISION.md` that is mostly about the token. The headline benchmark claims "67-93% fewer tokens than raw grep-based
search" on plausible/analytics.

ember's verdict on 2026-10-19 (memory `verekos-sibling-project.md`): EKOS is "bad slop", "not worth more days". "Do
not propose more EKOS work unless ember raises it."

---

## 7. VerEKOS: the one-day proof spine (`emberian/verekos`, 198 commits, 2026-10-19)

**Maturity: L3 Proved/Tested Core → Frozen-for-Rethink.** It was paused by
`8972945 closeout: pausing the EKOS half; what VerEKOS leaves behind and what carries over to minidregg`.

### 7.1 Purpose

`README.md`: EKOS "promises a short list of things about that ledger: it only grows; every conclusion points at
evidence; the reader is read-only; a reader allowed to see part of a project cannot learn about the rest; sources
that disagree are kept and flagged; the compiler is deterministic; secrets never enter. Today those promises are kept
by tests, by guard tests that read the source code of other tests, and by review. **VerEKOS states those promises as
theorems about a model, proves them, and runs the proved model against EKOS's own fixtures so that every difference
between the two is explained.**" The precedent it names is veri7vn (`~/dev/o7vn`), the Isabelle sibling of Oracle7.

The design is `docs/design/VEREKOS-DESIGN-2026-10-19.md` (362 lines, revision 3.1, "Written by the root (Fable
5.1)"). Revision 1 came from reading EKOS, veri7vn and minidregg. Revision 2 folded in scout memos A–F. Revision 3
folded in explorations 00–04. Revision 3.1 is the R1 review. §0 summarises it:

> "EKOS keeps its promises by tests, source-scanning guard tests and convention; minidregg can say who changed what
> and whether it was allowed, but not what anything means. VerEKOS puts the compiler inside the world with no kernel
> change (each compiled object is one document cell; evidence is a pinned snapshot transclusion; laws refuse the
> wrong writes; a lens is the read-only Runtime) … The single record under all of it is a **claim** pinned to source
> or to other claims, with a **receipt** per log entry and a status computed from review claims."

### 7.2 EKOS's promises and how each stood (design §1, verified by the root at cited lines)

| # | Promise | Stands? |
|---|---|---|
| P1 | Log only grows; identical content appends nothing | holds; log/state split undocumented |
| P2 | `object_at` is a fold of the prefix; `diff` = union of footprints | holds on linear `TxId` |
| P3 | Every compiled object/relationship cites evidence | **fails**: semantic edges and rollups have empty evidence (**EKOS#12**) |
| P4 | Passes are deterministic | **fails on cache miss**: random v4 evidence ids inside the content signature (**EKOS#10**) |
| P5 | Runtime is read-only | convention: trait carries write methods (**#13**); `ekos_clickhouse_query` writes (**#11**) |
| P6 | Exact-name merge; fuzzy = pending; traversal skips pending | holds for `SameAs`; hypothesis `ExplainedBy` walked as fact (**#17**) |
| P7 | Conflicts kept, normalized, order-independent | holds |
| P8 | Read scope: deny wins, both ends, unattributed hidden | holds ("the leak suite is the strongest empirical check in the repo") |
| P9 | Secrets never enter | **fails** for two readers (**#18**, **#19**); span reader skips exclusions (**#20**) |
| P10 | Human-only decisions unreachable from agents | holds against omission; string scans a rename evades (**#14**) |
| P11 | Domain time ≠ observation time | holds |
| P12 | Freshness manifest detects staleness | holds, as metadata |
| P13 | Branch merge skip-if-present | holds; report printed, not stored |

The issues filed upstream are listed in `notes/upstream-issues.md`, which gives a filed URL for each. The memory
also records ember's authorisation: "we should feel free to open issues on upstream EKOS with our critiques".

| Issue | Finding |
|---|---|
| alexeyban/EKOS#10 | Evidence ids are random, so any pass re-run forks a new version of every object it touches (reproduced empirically in the `ledger.*.versions` control) |
| #11 | `ekos_clickhouse_query` appends to the knowledge ledger |
| #12 | Compiled semantic edges and the rollup object are written with no evidence |
| #13 | Runtime read-only is a convention; split a read trait out of `KnowledgeStore` |
| #14 | Human-only guards are string-containment scans that a rename evades |
| #15 | RFC 0007 no longer describes the shipped identity algorithm |
| #16 | `ekos_identity_review` also confirms `AuthorizedBy`; a decision carries no evidence or actor |
| #17 | Hypothesis `ExplainedBy` edges carry no status, so dependents/impact walk them as facts |
| #18 | `read_crate_doc_comment` sends raw doc comments to the LLM provider unredacted |
| #19 | `git blame` commit summaries persisted to the ledger unredacted |
| #20 | `llm_description`'s span reader skips `is_excluded_path` |

### 7.3 Architecture of what was built

```
  EKOS fixtures / tests ─────► tools/scoreboard + controls/ (11 controls, 279 items)
         │  (EKOS @ 8e3c178 as CONTROL)          │  docs/parity/BOARD.md (rendered, drift-checked)
         ▼                                       ▼
  ekos compile (ecommerce.sql,         check/ (Lean exe verekos-check, run.py)
   + conflicting legacy fixture)          │ the model ANSWERS panels: scope.decision 59/59,
         │                                │ conflicts.unit 16/16, 0 unexplained
         ▼                                ▼
  map/  verekos-map (Lean) ───────► admitted cells on a fresh minidregg Store on hbox
   (byte-identical to the deleted        │ under laws/ L-obj, L-rev, L-run, L-src (Pred values)
    slice1/mapper.py, receipts 95/95)    ▼
                                   slice1/ — seven receipts (pinned birth; law refusals;
                                   sourceNotCovered; a moved pin + reopened conflict; one-room
                                   reader sees no conflict; byte-identical replay w/ attestation)
                                         │
                                   reader/ — a friend's client syncs the slice-1 world with its
                                   own signed reads; find/before/disagree with live-re-checked pins
                                         ▲
  world/  Lean 4 v4.30.0, minidregg @ dcab86da (git dep on local checkout, not path dep)
   ├── WorldCore (Mathlib-free; check-core-imports.sh enforces the boundary)
   └── World (Finset detect, Identity classes, Minidregg instance, Examples)
```

**The Lean model, `world/World/` (5,358 lines, 193 theorem/lemma declarations).** The count was made by grepping
declaration heads. `world/README.md` states "no `sorry`, `admit`, `axiom` or `native_decide`. Each theorem depends
only on Lean's three standard axioms … which we checked with `#print axioms`". The grep for `sorry` and `^axiom`
returned nothing.

| File | # | Representative theorems (verbatim names) | What it says |
|---|---|---|---|
| `Claim.lean` | 0 | — | records: `Carriers`, `ClaimKey` (schema, subject, sources; "no run, no time, no revision"), `ClaimIdDerivation`, `Pin` (target + revision + per-mille weight), `Window`, `Claim`, `Status`, `PrincipalKind`, `Schema`, `Op`, `Receipt` (tx, op, author, run, stage) |
| `Log.lean` | 10 | `write_appendOnly`, `idempotentPut`, `latest_write`, `state_eq_latest`, `diffIsFootprint` | P1/P2: append-only, idempotent put, diff = footprint |
| `TxOrder.lean` | 8 | `txMonotone_write`, `state_eq_replay_takeWhile`, `segment_contiguous`, `diff_eq_segment` | replay on linear tx order |
| `Status.lean` | 9 | **`compilerCannotDecide`**, `decision_has_author`, `reviewSurvives`, `needsReviewOnCoreChange`, `reviewTakesEffect`, `decided_stays_decided` | status = fold over pinned reviews; the compiler cannot decide (P10) |
| `Visible.lean` | 9 | **`deny_wins_id`**, `deny_wins_origin`, `deny_through_premise`, `conflict_hidden_of_alternative_denied`, `unpinned_hidden`, `visible_mono` | P8 read scope; denial flows along pins |
| `Ranked.lean` | 13 | `Ranked.wellFounded`, `Ranked.not_self`, `visible_stable`, `visibleR_rank_irrelevant`, `visible_iff_sourcePins` | pin graph well-founded; bound-independence |
| `Admission.lean` | 13 | `ranked_of_admLog`, `rankInv_of_admLog`, `not_admissible_self_pin`, `maxPinRank_mono` | the admission law keeps the pin graph acyclic |
| `WellFormed.lean` | 7 | `ClaimKey.eq_iff_of_canonical`, `ClaimKey.normalize_eq_iff`, `latest_wellFormed` | sorted, dup-free sources; nonempty pins |
| `Conflicts.lean` / `ConflictsCore.lean` | 8 / 2 | `mem_detect` (exact characterization), `coverage`, `soundness`, `detectList_perm`, `detect_mono` | P7 conflicts are order-independent |
| `Clash.lean` / `ClashCore.lean` | 9 / 4 | `coverageBy`, `soundnessBy`, `detectListBy_perm`, `disjointB_iff` | labelled clashes |
| `Traverse.lean` | 11 | **`pending_edge_never_crossed`**, `unreviewed_hypothesis_edge_not_crossed`, `unreviewed_hypothesis_node_blocks`, `reach_mono_hops` | P6, and the formal answer to EKOS#17 |
| `Identity.lean` | 17 | `same_equivalence`, `same_canonical`, `canonical_eq_iff`, `fuzzy_no_link` | identity as overlay; fuzzy never links |
| `Document.lean` | 16 | `decode_encode`, `encode_decode`, `toDocument_atomPins`, `viewEvidence_noGrant` | claims ↔ minidregg documents round-trip |
| `Shapes.lean` | 24 | `importSource_wellKeyed`, **`reimport_unchanged`**, `reimport_rev_iff`, `not_current_after_unemit`, `history_kept` | import family: re-import of an unchanged file submits nothing |
| `CarryForward.lean` | 13 | `pin_sameBytes_iff`, `pin_moved_iff`, `renderHeaderPin_eq_viewEvidence`, `pin_agrees_with_ekos`, `status_core_rev_agrees` | staleness and carry-forward |
| `Minidregg.lean` | 14 | `claimId_injective`, `staleIn_iff_moved`, `tombstoned_is_stale`, `toEvent_causal_injective`, `visibleR_iff_rendered`, `admit_sourceNotCovered` | **the real instance**: rests on minidregg's `pinHolds`, `transclusion_pinned`, `toCausalPreimage_injective`, `renderTransclusion`, `transclude_uncovered_refused` |
| `Examples.lean` | 6 | `Sch.code_injective`, `keyCode_injective` | `decide` fixtures over `Nat` carriers (prove nothing about minidregg) |

**Two design corrections that only the proofs produced** (closeout, verbatim): "the admission law's second condition
(re-put may not raise a rank), and the review core as the header revision (a signature can return A→B→A; a revision
cannot)." This is the strongest argument in the vertical for proof-first design: each correction is a bug that tests
did not reveal.

**The scoreboard** (`docs/parity/BOARD.md`, generated 2026-10-19T21:31:38Z, EKOS pin `8e3c178fc457…`):

| Panel | Items | EKOS test asserts reproduced | VerEKOS candidate | Assurance |
|---|---|---|---|---|
| `scope.decision` | 59 | 59/59 | **59/59 agree, 0 unexplained** | **executable property** |
| `conflicts.unit` | 16 | 16/16 | **16/16 agree, 0 unexplained** | **executable property** |
| `scope.store` | 8 | 8/8 | — | design target |
| `ledger.ecommerce` / `ledger.northwind` | 1 / 1 | (pipeline through release binary) | — | design target |
| `identity.unit` | 58 | 58/58 | — | design target |
| `branch.unit` | 3 | 3/3 | — | design target |
| `impact.unit` | 26 | 26/26 | — | design target |
| `redact.unit` | 26 | 26/26 | — | design target |
| `ekl.parser` / `ekl.interpreter` | 50 / 33 | 50/50, 33/33 | — | design target |
| `time.ecommerce`, `fusion.unit` | — | no panel | — | design target |

The board is honest about its own limits: "Until one is [scored], the Agree column is the control scored against
itself … it shows the diff code runs, nothing more." Only two of the eleven kernels have a scored candidate.

**Milestones reached on 2026-10-19** (memory and PLAN): M0.5 scoreboard; **M1a** reader-local compile ("a friend's
client syncs the slice-1 world with its own signed reads and answers find/before/disagree with live-re-checked
pins"); W7 transclusion on a current host ("24/24 and 143/143 journey rows"); **M2 slice 1** (EKOS compile landed as
admitted cells on hbox, "tipbin binaries at d94a8817", all seven receipts). After that came the twin deletion (W24:
the Lean mapper reproduces `mapper.py` "byte for byte", receipts 65/65 → 71/71 → 95/95; W25 deleted
`slice1/mapper.py`, `slice1/laws.py`, `reader/vendor/mapper.py` in `bddd85f`) and the re-pin to typeclass carriers
(`79b0445 world: the model over minidregg's own records`).

**The Isabelle layer was dropped.** Design revision 1 put the decision kernels in Isabelle/HOL + AFP, exported to
SML. On the evening of 2026-10-19 ember and the root agreed to drop it: "all kernels are Lean in `world/`".

**Process lessons recorded as memory** (they apply well beyond EKOS):
- `no-mirrors-no-twins.md`: "Never leave a mirror or twin standing … A `rfl` against a twin is evidence only while
  the twin exists; cashing it means deleting the twin. The receipt before deletion is byte-identity of the real
  thing's output with the twin's." ember's words: "ugh we have 'mirrors' and 'twins!' we should never have that".
  The memo ties this to the breadstuffs ATLAS (`~/dev/minidregg/ATLAS.md` §1).
- `checkpoint-commits-over-polish.md`: "it's ok if the commits 'tear' or 'don't work'; checkpointing and sharing
  work frequently is more important rn". It adds that ember "had to push ~41 commits by hand".
- `claude-glm-grok-subprocess-lanes.md`: how to run `claude-glm` (GLM 5.3) and `claude-grok` (grok-4.7 via
  CLIProxyAPI) as detached `-p` lanes with PID files. Grok's "Prompt is too long" deaths were diagnosed as Claude
  Code's own 200 k assumption, not the gateway (236 k probes returned HTTP 200), and fixed with
  `CLAUDE_CODE_MAX_CONTEXT_TOKENS=250000`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW=120000`.
- Traps (design §9): writing passes in Objective Bend; putting the compiled ledger on the agreement mesh; "One SPK
  grain per connector"; "Letting a resident resolve conflicts".
- Non-claims (design §10): "That a parser read the schema correctly. That a model's description is true. … That a
  theorem about the Lean model is a fact about EKOS or about a deployed host, until a panel score or a receipt ties
  the two."

### 7.4 What carries over (closeout, the actual deliverable)

> "**The claim/receipt model** and its minidregg instance: a compiled claim pinned to source atoms at revisions,
> status as a fold over pinned reviews, visibility by pins with deny wins, conflicts as records, admission as a
> ranked pin graph. **This is a document-world schema for *any* compiled knowledge, not for EKOS.**"
>
> "**The import family and the law package**: source files as documents with structural-key atom ids (a re-import
> of an unchanged file submits nothing); four `Pred` laws that refuse evidence-less births and non-human reviews;
> shown to hold on a real Host."
>
> "What does not carry over: The scoreboard panels and controls are EKOS's unit tests as data. … The EKOS findings
> and the upstream issues stay filed; nothing more is sent."

State at closeout: branch `dev`, pushed, "Everything builds. No lane is running. hbox run roots under
`~/verekos-runs/` (about 140 MB) are left as evidence; the two Stores are stopped."

### 7.5 Cycles, revival, attention: VerEKOS

**Unclosed cycles**
1. **Model ↔ minidregg kernel.** The README's "Honest state" says the model is "a model of VerEKOS's own design:
   nothing yet connects it to minidregg's kernel theorems beyond shared carrier types". W26 later rested staleness,
   events, evidence view and pins on minidregg's own theorems. Admission and visibility are still model-only.
   *Way through:* state `admissible` as a minidregg `Pred` and prove the model's `ranked_of_admLog` from the Host's
   admission theorem.
2. **Nine of eleven kernels have no candidate** (identity, branch, impact, redact, EKL ×2, scope.store, ledger ×2).
   The controls exist, so each is a `check/` runner away from a score.
3. **Lean in the loop vs. Lean beside it.** `map/` is Lean that runs (good), but `check/run.py` and
   `tools/scoreboard/*.py` are Python around it. That is acceptable: they are drivers, not twins.

**Promising and ready for revival (high leverage)**
- The **claim/receipt schema** is the most transferable artefact in this whole strand. It is a proved,
  EKOS-independent model of "compiled knowledge with evidence, reviews, scope and conflicts" on minidregg. It is
  exactly the substrate factshift's `ContentAttestation`/`Capability`/`SyncMetadata` was reaching for (§4), and
  exactly what an abcdeez learner model would need to make "this learner knows X, by this evidence" a claim (§8).
- **`reimport_unchanged`** together with structural-key atom ids gives a cheap, proven idempotent-ingest primitive
  for any corpus, including the BookLevel JSONs and lunar-logseq pages.

**Struggling / needs Ember's attention**
- `HOLE[design]`: **where does the claim/receipt model live now?** The closeout says "into minidregg". No minidregg
  commit is cited as having received it, and `world/` still pins minidregg at `dcab86da`. ember must choose: a
  `Theory.Claims` module inside minidregg, or keep `verekos/world` as a library minidregg imports. The
  no-twins rule forbids both existing at once.
- The day ran ~5 parallel lanes across Opus, Sonnet, GLM and Grok, plus hbox Stores. The memory records that ember
  had to step in twice: "quiet upstream now, recenter on our own creation", and mixing in Sonnet/Opus "so we do not
  drift into a lower-intelligence basin". Any revival should re-read `notes/R1-review.md` and the design §11
  corrections ledger before launching lanes.

---

## 8. Personal and collective knowledge substrate (2023), and research retrieval (2026)

### 8.1 lunar-logseq, ticklogseq, lunar.town

**Maturity: Compost (historical, frozen 2023-04).**
- `lunar-logseq` has 236 commits, all `[logseq-plugin-git:commit] <ISO time>`, from 2023-03-14 → 03-31. Remote: the
  local bare repo `~/shitheap/lunar-logseq.git`. It holds 40 org-mode pages and 9 journals for the **lunar.town**
  collective: `'ember.org`, `'grissess.org`, `'thajohns___onboard.org`, `'alif.org`, `Onboarding.org`,
  `Onboarding%3A___%3ABootstrapping.org`, `Infra.org`, `hbox.org`, `VPN.org`, `VM___Agent.org`, `GPT-4.org`,
  `Conferences___seL4 Summit___2023.org`, `Meetings___2023-03-20 alif+ember.org`, `QUERIES.org`,
  `organizational blocks.org`, `Halcyox Scaling Exercise.org`, `ASIC.org`. Onboarding asks: "How should we think
  about evaluating /how well/ our onboarding procedures causes people to: 1. Feel welcomed 2. Get effective
  procedures … acknowledging our energetic limits because we all have jobs 3. Understand where they can contribute
  4. Understand the compensation/profit structure". `organizational blocks.org` is a `#problem #report` template
  ("what seems to be of concern? … when does it arise? … who to respond?").
- `ticklogseq` has 94 autocommits (2023-03-13 → 04-05) and one page (`Hiking Gear.org`).
- `lunar.town/index.html` ("a cozy place … words and bytes.") is a webring of ember, grissess (Graham Northup),
  thajohns (Thomas Johnson) and tom (Thomas Withiam).

This is the earliest knowledge-ecosystem artefact in the vertical: a *collective* graph with onboarding, meetings
and problem reports. `hbox.org` shows hbox was already shared infrastructure in 2023. **Promising:** it is a real,
small, multi-author corpus (human-authored, with org `CLOCK` logbooks) that could test VerEKOS's claim model
(per-author pins, review status, read scope per member) without any EKOS dependency. Publishing anything from it
needs consent from grissess, thajohns and alif.

### 8.2 annas-mcp and semantic-scholar-fastmcp-mcp-server

**Maturity: L4 in use** (as MCP servers in ember's harness; `semantic-scholar` is a configured MCP server in this
very session, though it timed out on connect today).
- `annas-mcp` (Go; upstream iosifache, 23 commits). ember added 3 on 2026-02-09: `f534a18 upd8 & doi & scidb`,
  `419c837 fix: broken downloads & scidb pathway`, `2b91ca9 refactor: address review feedback`. These touched
  `internal/anna/anna.go` (+212/+314 line diffs), `internal/modes/mcpserver.go`, `internal/env/env.go`. The tools are
  `search` and `download`, and it needs an Anna's Archive API key (the global CLAUDE.md's `$ANNAS_SECRET_KEY`). The
  "address review feedback" commit implies an upstream PR.
- `semantic-scholar-fastmcp-mcp-server` (Python; upstream yuzongmin et al.). ember's 3 commits on 2026-02-09:
  `3437a49 Fix bridge recommendations endpoint and modernize FastAPI startup`, `0e99765 Add missing API fields and fix
  User-Agent URL`, `a2ff8ae Add paper_autocomplete and snippet_search tools; remove legacy monolith`.

These are the "reading" end of the learning stack: papers → (curricularized) → structured domains → drills. **Missing
link:** nothing feeds retrieved papers into a BookLevel-style JSON or an abcdeez `Topology`. Today the pipeline is a
human reading in a Claude session.

---

## 9. Cross-strand synthesis: which loops are closed

### 9.1 The idealised learning-and-knowledge loop

```
 (1) retrieve      (2) curricularize        (3) model the domain     (4) drill + measure
 annas-mcp,  ───►  BookLevel JSON /   ───►  abcdeez Topology    ───► abcdeez EIG scheduler,
 semantic-scholar  factshift LearningPath   (DAG of objectives)      RT/accuracy, MasteryMetrics
      ▲                                                                       │
      │                                                                       ▼
 (7) publish /     (6) collective view     (5) record as evidence-backed claims
 static site  ◄─── lunar-logseq / factshift ◄── VerEKOS claim/receipt model on minidregg
 (factshift weekly  realms, seasons             ("learner L can traverse G backwards,
  drops, BookLevel)                              evidence: responses r1..rn, reviewed by …")
```

| Link | State | Evidence |
|---|---|---|
| 1 retrieve | **closed** (works, in use) | annas-mcp / S2 MCP commits 2026-02-09 |
| 1→2 | open (manual) | no ingest code anywhere |
| 2 curricularize | closed as a static artefact | 10 JSONs + `curriculum.ts` |
| 2→3 | **open** | BookLevel prerequisites never become a `Topology` |
| 3 model | closed in abcdeez2, dropped from abcdeez | `topology.rs` (abcdeez2) vs `Letter(u8)` (abcdeez) |
| 4 drill | half: heuristic loop ships, EIG unwired | `compute_information_gain` uncalled |
| 4 measure | half: metric fields exist, no study data | `MasteryMetrics`; `analysis/*.R` deleted |
| 4 forgetting / SRS | **absent everywhere** | no `s_v(t)` in any repo |
| 4→5 | open | nothing records learner state as claims |
| 5 evidence model | **proved** (193 theorems), paused | verekos `world/` |
| 5→6 | open | — |
| 6 collective | historical (2023) | lunar-logseq |
| 7 publish | closed for BookLevel (GH Pages) and old factshift; open for factshift-redux | — |
| SPW as input notation | closed for keyboard → prompt (few-shot); open for conformance | three parsers, no shared corpus |

### 9.2 Recurring failure pattern across the strand

The same thing happened in abcdeez2 (IRB, federation, sensors before a learner existed), factshift-redux (DIDs,
VCs, macaroons and CSS transforms before a page was published), and abcdeez-spec (18 k lines of spec for an app
that would be contracted to 1.4 k). In each case, **agents generated institutional breadth around an unvalidated
core.** ember's corrections are visible in the record: `contract ; reorganize`, "Sonnet3.5 wrote all thhis I think?
I want you to be very critical", "bad slop", "ugh we have 'mirrors' and 'twins!'". VerEKOS is the counterexample.
It had a scoreboard before theorems (design §6, "M0.5, before any theorem"), a stated list of non-claims, and
byte-identity before deletion, and in one day it produced the strand's only proved, measured core.

### 9.3 Ranked revival candidates

| Rank | Candidate | Why now | First concrete step | Blocker |
|---|---|---|---|---|
| 1 | VerEKOS claim/receipt model → minidregg | proved, EKOS-independent, closeout already names it | decide its home (`HOLE[design]` §7.5); import, don't copy | ember's decision |
| 2 | abcdeez H1 pilot (distance-slope study) | the paper's sharpest testable claim; RT timing and slope field exist | port `PosteriorDistribution` + `monte_carlo_eig` into abcdeez core; add `s_v(t)`; run on ember | research-vs-product decision |
| 3 | BookLevel × abcdeez | real DAG domain already structured | convert one book's `prerequisites`/`skill_tracks` into `Topology::new_dag` | copyright on summaries; spwplace ownership |
| 4 | SPW conformance panel | three parsers, one canon | export spw-seed's corpus; score the Rust parsers; delete the losers | spwashi's ownership |
| 5 | spweebo'ard core as a generic on-device-LLM IME | working Rust+UniFFI+GGUF scaffold | root-cause the "App keeps stopping" crash | spwashi go-ahead; time |

### 9.4 Items that need Ember's human attention (consolidated)

1. **`~/dev/abcdeez` working tree:** untracked, *unignored* production APNs `.p8` keys; uncommitted deletions of
   `PAPER_IMPLEMENTATION_COMPARISON_REPORT.md`, `PROJECT_SPEC.md`, `REVIEW_NOTES.md` and `analysis/*.R`. Decide
   whether to commit, restore or ignore them. This dossier did not touch the repo.
2. **abcdeez identity:** research instrument (H1–H4) or alphabet app.
3. **factshift ownership:** gift to spwashi, delete, or fold into minidregg's content layer.
4. **SPW:** any revival requires spwashi; spwsft needs a corpus only spwashi can make.
5. **Claim/receipt model's home:** minidregg module or imported library (no twins).

---

## Appendix A — Commit and file index

| Repo | Key commits (hash, date, subject) |
|---|---|
| abcdeez | `c4cb956` 08-08 first draft · `6163e83` 08-11 builds and runs on ios · `d0ed7af` PWA · `0a74177` runs everywhere!!! · `a9afab5` old functionality ported forward · `ba53d6b` 08-12 0.0.17 · `2909c95` 08-15 save some files before we delete them lol |
| abcdeez2 | `4b7dc1a` gpt-5: please fix errors · `b6e4310` contract ; reorganize · `6ce24be` contraction · `f9e8ce0` tests... pass? · `a28bc0d` claude: create core book · `c235c3f` 08-10 iter web-backend |
| curricularizedbooks | `acfc6b0` / `3d358cf` / `8aeb540` 2026-04-30 |
| app.factshift.com | `48a39d7` honk · `18e9240` updated boon command · `bf68c99` revisiting story mode · `79240fa` websockets · `2ba127a` 2024-10-30 v0.0.2-alpha |
| factshift-redux | `489e380` 10-10 initial · `0848c29` import app.factshift.com · `b46bce5` llms generate us some files · `c69068b` ontology · `7ca1714` a plan · `3ed9662` 10-11 macros... |
| spweebo'ard | `83d6d8e` 01-05 initial · `117920f` scaffold · `71c60bf` 01-06 functioning android app · `1c2720b` auto-uniffi · `cf78c7c` guardrails · `f65ae14` ios progress |
| spween | `4d38e32` 01-05 initial · `afb5b1f` 01-08 conj/disj · `95980f7` 07-13 fire passage entry effects once |
| spw-workbench (ember) | `93ff88e`, `f424cf4` 2026-07-23 |
| verekos | `4c6d99b` 13:14 design · `fd228b7` lane B memo · `9d13683` check imports WorldCore · `9be8a33` verekos-map · `bddd85f` delete the twins · `79b0445` world over minidregg records · `8972945` 17:51 closeout |
| EKOS (upstream) | `8e3c178` 10-19 (VerEKOS control pin) |
| annas-mcp (ember) | `f534a18`, `419c837`, `2b91ca9` 2026-02-09 |
| semantic-scholar (ember) | `3437a49`, `0e99765`, `a2ff8ae` 2026-02-09 |

## Appendix B — Paths worth opening first

- `~/dev/abcdeez/PAPER.md` — the theory.
- `~/dev/abcdeez2/core/src/learning/bayesian.rs`, `core/src/core/topology.rs` — the parts worth porting.
- `~/dev/abcdeez2/CORE_REVIEW_NOTES.md` — the known statistical errors.
- `~/dev/abcdeez/core/src/{learner,task,stats}.rs` — what ships.
- `~/dev/factshift-redux/README`, `specs/ONTOLOGY_V2.md`, `PLAN.md`, `specs/seed.spw`.
- `~/dev/spweebo'ard/dev-plan.md`, `crates/spweeboard-core/src/compiler/prompt.txt`.
- `~/dev/spw-workbench/README.md`; memory `breadstuffs-hypersemantic-tree.md`.
- `~/dev/verekos/project/CLOSEOUT-2026-10-19.md`, `docs/design/VEREKOS-DESIGN-2026-10-19.md`, `world/README.md`,
  `docs/parity/BOARD.md`, `notes/upstream-issues.md`.
- `~/.claude/projects/-Users-ember-dev-EKOS/memory/{verekos-sibling-project,no-mirrors-no-twins,checkpoint-commits-over-polish,claude-glm-grok-subprocess-lanes}.md`.
