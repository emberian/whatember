# Strand 17 — DeOS Surfaces, Starbridge App Ecosystem, Moldable Inspector, and the Diaspora

Primary-source technical dossier, compiled 2026-11-02 from the repositories, git commits,
architecture docs, agent transcripts, and memory corpora across `/Users/ember/dev/breadstuffs`,
`/Users/ember/dev/delvetalk`, `/Users/ember/dev/delvetalk2`, `/Users/ember/dev/spween`,
`/Users/ember/dev/spw-workbench`, `/Users/ember/dev/minidregg`, `/Users/ember/dev/obend`,
and `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/`.

---

## 0. Executive Ledger & The Guiding Vision

### 0.1 Primary Source Ledger

| System / Surface | Breadstuffs Path & Git Commit | Modern Crate / Diaspora Location | Primary Invariants & Verification Seams |
|---|---|---|---|
| **Starbridge v2 Cockpit** | `starbridge-v2/` (`a7de1c5a4`, `d5ad5a6e4`) (194,109 LOC) | `obend/crates/obend-gui` (2,088 LOC) | GPUI ocap master shell, 32 mode tabs, docked dev loop, spotter palette, living card panes |
| **Starbridge App Ecosystem** | `starbridge-apps/` (`1e25f8fc8`, `4b80c7095`) (114,679 LOC) | `minidregg/tests/objective-bend-source/` | 32 domain apps; rule: *"The answer is never `Effect::FooApp`"*; slot caveats (`WriteOnce`, `Monotonic`, `AffineLe`) |
| **Moldable Inspector & Gadgets** | `starbridge-v2/src/presentable.rs` (`800945db6`, `ce4aca034`) | `obend-gui/src/viewport.rs` | 7 presentation kinds (`RawFields`..`Source`), L1–L10 ladder, `IntentDraft -> simulate() -> commit()` |
| **Cap-Bounded Reflection** | `deos-reflect/` (`21ebc84cf`, `b3ef43204`) (1,420 LOC) | `minidregg` DeOS Crown | Cap-bounded attested read (`Inspectable`, `OcapGraph`, `Frustum`, `AffordanceSurface`); no omniscient leaks |
| **Renderer-Agnostic View-Tree** | `deos-view/` (`ecbbe2252`, `c5ab6469e`) (19,963 LOC) | `obend-gui/src/server.rs` | Dual-renderer (`native` GPUI vs `web` HTML) over serializable `ViewNode` tree; progressive disclosure |
| **Zed Full Workspace Embed** | `deos-zed-full/` (`3190aa849`, `302aea28c`) (4,774 LOC) | Parked / Target for `spw-workbench` | Real Zed `Workspace` over `FirmamentZedFs`; files = cells, file save = verified turn |
| **Matrix Rehydratable Membrane**| `deos-matrix/` (`c330befc5`, `afcac822e`) (7,706 LOC) | `delvetalk2` AT Proto Journal | Chat rooms = cells, messages = turns; messages carry rehydratable world-fork membranes (`shared_fork.rs`) |
| **DeOS Homeserver Grain** | `deos-homeserver/` (`07942f63c`, `f1c2a5ffe`) (13,484 LOC) | Sandstorm-style sovereign grain | Matrix homeserver as an isolated Sandstorm grain hosted on sovereign cell storage |
| **Software-Rasterized Webview** | `servo-render/` (`83179110f`, `5ae26d4ee`) (24,749 LOC) | Parked | SWGL (`swgl 0.68.0`) CPU rasterizer; renders RGBA8 frames into `CompositorPd` digest; no GPU/EGL |
| **Android Cell (Graphideos)** | `android-cell/` (`6fae061d0`, `8cd45ddee`) (11,066 LOC) | Parked | Android APKs as cap-confined cells; `AppFactory`, `PermGate` cap badges, SystemUI cap-chrome |
| **Sandstorm Grain Integration** | `sandstorm-bridge/`, `sandstorm-package/` (`028bc0271`) | Extracted for Mini hosting (Ember 09-26) | Real `.spk` parser (xz, Ed25519, Cap'n Proto); grain `/var` = cell umem heap; Powerbox = attenuating caps |
| **Verifiable Narrative DSL** | `spween-dregg/` (`4ddb4f1f6`, `dad9fd8db`) (8,183 LOC) | `~/dev/spween`, `delvetalk2` scenes | Interactive fiction DSL on world-cells; choices = verified turns; un-retconnable receipt chains |
| **DrEX Terminal v2** | `drex-web-v2/` (`da95a0fa7`, `6f04af76f`) (1,790 LOC) | Parked / Target for `obend-gui` | Preact + Signals DEX terminal; Open/Shielded/Dark tier-dial; `window.dregg` extension handshake |
| **Fair Launch Engine Portal** | `launchpad-web/` (`e1247989b`, `8e1850596`) (2,245 LOC) | Parked | Uniform-price fair-launch indexer driven by live node turn streams (`POST /turn/submit`) |
| **Light Client Portal** | `portal/` (`1f39d35f2`, `df7118b88`) (12,006 LOC) | Parked | In-tab recursive-STARK light client (`portal.dregg.studio`) evaluating cryptographic receipts |
| **Browser Wallet & Broker** | `extension/` (`06b366e54`, `7593b4c1d`) (74,905 LOC) | Parked | WebExtension (`window.dregg`); BIP-39 mnemonic identity, signing, and capability brokerage |
| **Town of Inhabited Objects** | N/A (Modern Synthesis) | `delvetalk2` (branch `foundation`) | Post-cockpit subtraction: text & cards, spells, receipts, Hob the reader, AT Protocol repository |

---

### 0.2 The Founding Philosophy: 1999 AOL Wonder × Pharo Smalltalk Liveness

In `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-deos-ux-vision.md` (origin session
`3b829648-9d41-4dad-bd2e-1a3eb7f618ab`, recorded 2026-06-19), Ember articulated the existential
purpose and user experience of DeOS:

> *"i am the person who needs this substrate. i'll be using this os for a while."*
> 
> *The "who needs this / killer app" question is ANSWERED and it dissolves the biggest strategic lack:
> **ember IS the user. deos is her daily-driver sovereign OS — she will live in it.** Not a fallback,
> the Engelbart/Pharo/Houyhnhnm THESIS: you build the tools you live in; sovereign computing is for
> the sovereign, and the sovereign is here.*
>
> *The feeling — 1999 AOL as a 4-5-year-old. "WOW!! THIS IS AMAZING!! i had no comprehension.
> just clicking around. absorbing. not understanding why sometimes the back button stopped working
> (a new window was opening over it!)." Running RedHat off his dad's machine. Browser, website,
> flash. The deos UX is supposed to feel like THAT — the user "has no idea wtf is going on" and
> it's wonderful. Wonder precedes comprehension; you click, you absorb, the system rewards
> exploration. The deos objects you click around: **badges, powerboxes, living screenshots**
> (the rehydratable frustum-snapshots), cells, affordances.*
>
> *The substrate — Pharo/Smalltalk LIVENESS. "the smalltalk experience. it's supposed to be
> pharo-ish." Pharo = a live, image-based, self-describing environment: every object is a live,
> inspectable, modifiable thing; you can halt anywhere, inspect, change, continue; the whole system
> is malleable from within itself. **deos is ALSO an IDE, debugger, etc.** — exactly as Pharo's
> environment IS its own live IDE/inspector/debugger.*

This dual thesis governed every line of DeOS UI code written between May and August 2026:
a user experience combining the uninhibited, tactile magic of 1990s desktop computing with the
mathematical rigor of an object-capability operating system where **every button press is a
verified state transition (a turn), every UI panel is an inspectable cell, and every window can be
serialized into a cryptographic snapshot and sent over chat to be rehydrated and executed on another
machine.**

---

## 1. What Lived in Breadstuffs: The 31 Environments, Crates & Surfaces

Breadstuffs was not merely a cryptographic kernel; it was a complete, sovereign operating system
environment comprising over **550,000 lines of UI, environment, application, and tooling code**.
This ecosystem spanned six distinct functional quadrants.

```
+---------------------------------------------------------------------------------------------------+
|                                  THE BREADSTUFFS DeOS CONTINUUM                                   |
+---------------------------------------------------------------------------------------------------+
|  [Desktop & Execution Cockpit]          |  [Cap-Bounded Reflection & View]                        |
|  - starbridge-v2 (194k LOC, GPUI shell) |  - deos-reflect (1.4k LOC, pure AST/Ocap projection)    |
|  - servo-render (24k LOC, SWGL frame)   |  - deos-view (19.9k LOC, native GPUI + web HTML)        |
|  - android-cell (11k LOC, Graphideos)   |  - deos-js / runtime (21.5k LOC, SpiderMonkey applets)  |
|  - dregg-tui (1.1k LOC, Ratatui CLI)    |  - deos-web-cells (4.6k LOC, live DOM cells)            |
+-----------------------------------------+---------------------------------------------------------+
|  [Developer Panes & Inhabitation]       |  [Multiplayer Communications & Grains]                  |
|  - deos-zed & zed-full (11.4k LOC, FS)  |  - deos-matrix (7.7k LOC, rehydratable membranes)       |
|  - deos-terminal (3.3k LOC, Alacritty)  |  - deos-homeserver (13.4k LOC, grain-hosted Matrix)     |
|  - deos-hermes (24k LOC, agent harness) |  - sandstorm-bridge/package/serve (10.3k LOC, SPKs)     |
+-----------------------------------------+---------------------------------------------------------+
|  [Starbridge 32-App Ecosystem]          |  [Web Portals, Wallets & Financial Frontends]           |
|  - starbridge-apps (114.6k LOC)         |  - extension (74.9k LOC, browser wallet & broker)       |
|  - app-framework (21.8k LOC, DSI)       |  - portal (12k LOC, in-tab STARK light client)          |
|  - starbridge-web-surface (17k LOC)     |  - drex-web & drex-web-v2 (5k LOC, DEX terminals)       |
|  - spween-dregg (8.1k LOC, CYOA engine) |  - launchpad-web (2.2k LOC, fair-launch turn stream)    |
+---------------------------------------------------------------------------------------------------+
```

### 1.1 The Native Desktop Cockpit & Rendering Engine

#### 1. `starbridge-v2` (`/Users/ember/dev/breadstuffs/starbridge-v2`, 194,109 LOC)
- **Scaffold Commit**: `a7de1c5a4` (2026-06-13); **Last Touches**: `d5ad5a6e4` (2026-09-30).
- **Core Architecture**: The flagship native desktop application built using Zed's **GPUI** framework.
  It housed 115 source files including the master cockpit (`src/cockpit/`), containing 21 modules
  (`panels_workspace.rs`, `panels_main.rs`, `panels_moldable.rs`, `panels_web.rs`, `panels_devtools.rs`,
  `panels_app_launcher.rs`, `live.rs`, `construct.rs`, `render.rs`, `shell_ops.rs`).
- **DeOS Desktop Subsystem** (`src/deos_desktop/`, 29 modules): Implemented the full Pharo/Smalltalk-style
  desktop:
  - `world_explorer.rs`: Visual hierarchy walker over sovereign cells, authority delegations, and receipts.
  - `spotter.rs`: Universal command palette and search indexing every `Presentable` object.
  - `halo.rs`: Direct-manipulation ring surrounding on-screen cells (tear off, inspect, fork, actuate).
  - `systemui_chrome_render.rs` & `android_window.rs`: Cap-badge status bars and quick-setting pull-downs.
  - `matrix_room.rs`, `agent_room.rs`, `exchange_floor.rs`, `docgraph_view.rs`, `face_scroll.rs`, `toasts.rs`.
- **Inhabitation & Rehydration**: `src/shared_fork.rs` and `src/distributed_card.rs` enabled live cockpit
  tabs to be detached into independent OS windows (`tear_off_tab_unleased`), snapshotted to disk, or
  transmitted across machines.
- **The seL4 Framebuffer Keystone**: Commit `d92d0526c` (2026-06-19) closed the #1 precious milestone:
  wiring GPUI's offscreen software render directly into the seL4 QEMU ramfb framebuffer (`deos-live.system`),
  allowing the full Starbridge v2 cockpit to boot on a formally verified microkernel without an X11 or Wayland host.

#### 2. `servo-render` (`/Users/ember/dev/breadstuffs/servo-render`, 24,749 LOC)
- **Origin Commit**: `83179110f` (2026-06-14); **Key Hardening**: `5ae26d4ee` (2026-07-27).
- **Architecture**: A hardware-independent web rendering pipeline designed to run inside an unprivileged
  seL4 Protection Domain (PD).
- **The SWGL Core**: Used Mozilla WebRender's C++17 software rasterizer (`swgl 0.68.0`) in
  `swgl_context.rs`. It implemented `gleam::gl::Gl`, compiling pure C++ into a CPU-only rasterizer that
  rendered HTML/CSS directly into a caller-owned RGBA8 buffer (`Vec<u8>`).
- **Attested Output**: In `compositor_seam.rs`:
  ```rust
  pub fn present_frame(frame: &RgbaFrame, region: Rect) -> FrameReceipt {
      let digest = blake3::hash(&frame.pixels);
      // Digest committed to seL4 CompositorPd gate (T1 non-overlap, T2 label, T3 focus)
      FrameReceipt { digest, bounds: region, timestamp: now() }
  }
  ```
- **Libservo Elephant**: Contained an opt-in feature `--features libservo` in `webview.rs` wiring into
  SpiderMonkey (`mozjs`) and Servo's layout engine. Because of `mozjs` compilation overhead (multi-GB
  C++ build), SWGL was cleanly decoupled into `swgl-standalone` so pixel rendering could be tested
  instantly without building SpiderMonkey.

#### 3. `android-cell` (Graphideos) (`/Users/ember/dev/breadstuffs/android-cell`, 11,066 LOC)
- **Origin Commit**: `6fae061d0` (2026-06-24); **Memory**: `project-graphideos-android-epoch.md`.
- **The Graphideos Concept**: Running unmodified Android applications within cap-confined cell sandboxes.
  `servo : web :: android-runtime : android`.
- **Key Modules**:
  - `appfactory.rs`: Minted an `android-cell` from an APK's manifest descriptor; declared permissions
    defined the exact initial capability set (`CapBadgeSet`), eliminating ambient Android authority.
  - `permgate.rs`: Interposed over Android's `Context.checkSelfPermission`. If a cap badge was dim, the
    runtime returned `PERMISSION_DENIED` in-process. Handing over a permission minted a genuine
    `Effect::GrantCapability` through the kernel `TurnExecutor`.
  - `intentgate.rs` & `broadcastgate.rs`: Intercepted Android Intents and Binder RPCs, routing them
    through verified capability checks.
  - `runtime/`: Shipped `MacOsEmulatorRuntime` (driving Google Android Emulator over Hypervisor.framework)
    and `CapturedFrameRuntime` (headless PNG/RGBA8 tile pipe).

#### 4. `dregg-tui` (`/Users/ember/dev/breadstuffs/dregg-tui`, 1,132 LOC)
- Ratatui-based terminal cockpit displaying the active cell graph, ledger height, witness cursor, and
  recent receipts for headless server environments and remote SSH sessions.

---

### 1.2 Cap-Bounded Reflection & The View-Tree Substrate

#### 5. `deos-reflect` (`/Users/ember/dev/breadstuffs/deos-reflect`, 1,420 LOC)
- **Origin Commit**: `21ebc84cf` (2026-06-23); **Fix**: `b3ef43204` (2026-08-01).
- **Purpose**: Cap-bounded, attested reflection over cell substance, completely independent of GPUI.
  Crawling was strictly per-viewer: *a principal can only observe what their authority reaches.*
- **Core Types (`src/lib.rs`)**:
  ```rust
  pub use substance::{Field, FieldValue, Inspectable, ObjectKind, reflect_cell};
  pub use graph::{GraphEdge, GraphLayer, GraphNode, OcapGraph};
  pub use frustum::Frustum;
  pub use affordances::{Affordance, AffordanceSurface, EffectSummary};
  pub use present::{Presentation, PresentationBody, PresentationKind, ReflectedCell};
  ```
- **The Attested Redaction Principle**: When inspecting private or committed fields, `deos-reflect`
  emits the cryptographic commitment (`Poseidon2` / `Blake3`), never the cleartext value.

#### 6. `deos-view` (`/Users/ember/dev/breadstuffs/deos-view`, 19,963 LOC)
- **Origin Commit**: `ecbbe2252` (2026-06-23); **Last Touches**: `c5ab6469e` (2026-08-06).
- **Core Thesis**: The card is **renderer-independent**. `deos-js` produces declarative UI trees
  (`tree::ViewNode`), and `deos-view` renders that data into pixels or markup.
- **Dual Renders**:
  - `native` (GPUI): `bridge::build_live_view` executes SpiderMonkey JS applets, extracts `ViewNode`,
    and `render::AppletView` translates nodes (`vstack`, `button`, `text`, `bind`) into GPUI widgets.
    Buttons bind directly to `World::commit_turn`.
  - `web` (HTML/DOM): `web::render_card_document` translates the exact same `ViewNode` tree into a
    standalone `.html` string with embedded styling and SVG badges.
- **Progressive Disclosure**: `ViewNode::Adept`, `Disclosure::Simple | Disclosure::Adept`, and the
  `disclose()` AST transform allowed UI elements to hide developer/cryptographic details from casual
  users while allowing power users to expand raw state constraints and Lean invariants.

#### 7. `deos-js`, `deos-js-core`, `deos-js-runtime` (21,526 LOC combined)
- Embedded SpiderMonkey runtime executing unprivileged userspace applets.
- Exposed the `deos.ui.*` DOM building API, `deos.turn.*` intent builder, and `deos.cell.*` query layer.
- `src/attach.rs`: Enabled an autonomous agent (Claude Sonnet 4.5 via ACP/MCP) to attach to a live
  `Rc<RefCell<World>>`, inspect cells through `deos-reflect`, synthesize a JavaScript applet, execute it,
  and commit verified state transitions (`0d03f6ee...`).

---

### 1.3 Developer Panes, Confined Inhabitation & Editors

#### 8. `deos-zed` (6,672 LOC) & `deos-zed-full` (4,774 LOC)
- **Origin Commit**: `3190aa849` (2026-06-23); **Test Harness**: `302aea28c` (2026-09-30).
- **The Vision**: Embedding the full, real Zed editor stack directly into the DeOS cockpit.
- **`FirmamentZedFs`** (`src/firmament_zed_fs.rs`): Implemented Zed's asynchronous `fs::Fs` trait over
  sovereign cells:
  - Files and directories mapped to cells in the sovereign graph.
  - Buffer saves invoked verified kernel turns:
    ```rust
    impl fs::Fs for FirmamentZedFs {
        async fn save(&self, path: &Path, content: &Rope, ...) -> Result<()> {
            let patch = dregg_doc::diff(&self.read(path).await?, content);
            let turn = TurnBuilder::new().apply_patch(self.cell_for_path(path)?, patch).build();
            self.executor.commit_turn(turn).await?;
            Ok(())
        }
    }
    ```
  - Validated by three headless integration tests (`cargo test --features full-zed`):
    `tests/firmament_zed_fs.rs`, `tests/project_over_cells.rs`, and `tests/full_workspace_over_cells.rs`.
    The full Zed `Workspace`, `project_panel`, `outline_panel`, and `terminal_view` mounted cleanly over
    cells-as-files.

#### 9. `deos-terminal` (`/Users/ember/dev/breadstuffs/deos-terminal`, 3,309 LOC)
- Integrated Alacritty PTY terminal dock pane. Allowed the developer to pop open a shell with ⌘K,
  executing local commands inside a cap-bounded sub-environment.

#### 10. `deos-hermes` (`/Users/ember/dev/breadstuffs/deos-hermes`, 24,012 LOC)
- The confined agent host. Hermes ran autonomous LLM reasoning loops inside an isolated Protection
  Domain. All external actuation (filesystem, network, editor) was mediated via capability handles,
  with ambient authority denied (verdict `0xf`). Every agent action emitted an irrevocable, verifiable
  turn receipt.

---

### 1.4 Multiplayer Communications & Sovereign Grains

#### 11. `deos-matrix` (7,706 LOC) & `deos-homeserver` (13,484 LOC)
- **Origin Commit**: `c330befc5` (2026-06-22); **Memory**: `project-deos-self-hosting-epoch.md`.
- **The Concept**: Native Matrix chat (`matrix-rust-sdk`) re-pilled around sovereign cells:
  - Matrix Rooms = Sovereign Cells; Matrix Identities = Cell Cap Badges; Messages = Verified Turns.
- **The Rehydratable Membrane (`src/membrane.rs`)**: The crowning multiplayer primitive. A chat message
  could encapsulate a *membrane*: a frustum-culled, cap-bounded snapshot of a live world-fork. The
  recipient received the message, clicked the membrane, and the cockpit rehydrated the world-fork
  in-memory. The recipient executed turns within the fork, and a subsequent *stitch* operation merged
  the divergent branches back into the sender's ledger using categorical pushouts.
- **`deos-homeserver`**: A Matrix homeserver designed to run as an unprivileged, persistent Sandstorm-style
  grain on top of the cell store (`docs/deos/GRAIN-HOMESERVER.md`), making communications self-hosted
  without relying on third-party Matrix homeservers.

#### 12. Sandstorm Integration: `sandstorm-bridge`, `sandstorm-package`, `sandstorm-serve` (10,393 LOC combined)
- **Origin**: Began in May 2026; standalone package parser extracted by Ember in commit `028bc0271`
  (2026-09-26: *"Extract reusable signed Sandstorm package parser for Mini hosting"*).
- **Mechanism**:
  - `sandstorm-package`: Decompressed real `.spk` packages (8-byte magic `Spk1`, xz decompression,
    Ed25519 signature verification where App ID = public key, and Cap'n Proto archive decoding).
  - `sandstorm-bridge`: Mapped Sandstorm grain concepts directly to DeOS cells:
    - Grain `/var` directory = Sovereign cell `umem` heap.
    - Grain lifecycle (`create`, `wake`, `sleep`, `delete`) = Cell lease and persistence management.
    - Sandstorm Powerbox = Attenuable credentials (`dga1_...`, ed25519 caveat chains).
    - HTTP Bridge: Interposed `X-Sandstorm-*` identity and permission headers derived from the holder's
      cell capability.

---

### 1.5 The Starbridge App Ecosystem & Web Surfaces

#### 13. `app-framework` (21,851 LOC) & `starbridge-apps` (114,679 LOC)
- **Origin Commit**: `1e25f8fc8` (2026-05-24); **Census**: `docs/deos/STARBRIDGE-APPS-CENSUS.md`.
- **The Immutable Law**:
  > *"The answer is never `Effect::FooApp`."*
  > *When an app wants a domain Effect, the missing primitive is the generic one (`Caveat`,
  > `StateConstraint`, `Authorization`, `Factory`) it would compose from. Every starbridge-app
  > must be buildable from dregg-native primitives only.*
- **The 32 Apps**:
  1. `nameservice`: Hierarchical domain registration with `WriteOnce` and `Monotonic` slot caveats.
  2. `identity`: Selective credential disclosure, verifiable presentation, and revocation.
  3. `subscription`: Cap-metered bounded ring buffer for pub/sub message consumption.
  4. `governed-namespace`: Threshold multisig voting on namespace registration.
  5. `compartment-workflow-mandate`: Clearance-graph workflow progression and spend policies.
  6. `storage-gateway-mandate`: Bounded volume read/write gateway for blob storage.
  7. `privacy-voting`: Monotonic poll counters with per-voter one-vote-per-cell caveats.
  8. `bounty-board`: First-claimer-wins bounty lifecycle (`POSTED -> CLAIMED -> SUBMITTED -> PAID`).
  9. `compute-exchange`: Escrow budget state machine (`AffineEq(PAID + REFUNDED == BUDGET)`).
  10. `gallery`: Commit-reveal art curation using sealed submission boards.
  11. `sealed-auction`: Sealed-bid uniform price auction clearing.
  12. `domains`: Distributed DNS-style authoritative zone cells.
  13. `edge-mandate`: Attenuated execution mandates at network edge nodes.
  14. `escrow-market`: Multi-party conditional asset escrow.
  15. `first-room`: Smalltalk-style beginner world and cell tutorial.
  16. `guard`: Capability revocation gates and watchdog contracts.
  17. `kvstore`: Verified content-addressed key-value store.
  18. `org`: DAO structure with role hierarchies and treasury allocations.
  19. `polis`: Quadratic voting and Deliberative polling.
  20. `site-host`: Static website hosting served directly from cell heaps.
  21. `supply-chain-provenance`: Multi-hop physical asset custody tracking.
  22. `swarm-orchestration`: Multi-agent work distribution and receipt settlement.
  23. `tool-access-delegation`: Fine-grained attenuation of CLI/API tool execution.
  24. `tussle`: Competitive multi-agent game state machine.
  25. `execution-lease`: Computron resource metering and lease renewals.
  26. `vat`: E-style isolated event-loop containers with CapTP messaging.
  27. `agent-orchestration`: Hierarchical subagent scheduling.
  28. `agent-provenance`: Verification of LLM model signatures and prompts.
  29. `billing`: Usage-based micro-invoicing.
  30. `branch-stitch-multiplayer`: Multi-user document branch merge demonstrator.
  31. `shared`: Common Preact inspectors and JSON factory descriptors.
  32. `starbridge-web-surface` (17,030 LOC): Browser-based `dregg://` cell URI resolver and transclusion.

#### 14. `deos-leptos` (4,108 LOC) & `deos-web-cells` (4,667 LOC)
- `deos-leptos`: Explored Rust web frontend reactivity: Cell state = Leptos `RwSignal`; Affordances =
  reactive UI components; Rehydration = per-viewer SSR hydration.
- `deos-web-cells`: Implemented live DOM snapshot cells (`BundleKind::LiveDomSnapshot`), enabling
  declarative HTML/DOM subtrees to be content-addressed, transcluded across documents, and stored
  directly on the cell ledger.

#### 15. Frontends & Portals: `drex-web-v2`, `launchpad-web`, `portal`, `extension`
- `drex-web-v2` (1,790 LOC, `da95a0fa7`): Clean Preact + `@preact/signals` trading interface. Implemented
  a 3-tier view dial (**Open** = public order book, **Shielded** = blurred liquidity amounts,
  **Dark** = sealed-bid commit-reveal). Handshook with `window.dregg`.
- `launchpad-web` (2,245 LOC, `e1247989b`): Fair-launch token interface driven directly by live node
  turn streams (`POST /turn/submit`). Bypassed traditional EVM bonding curves in favor of batch-cleared
  uniform-price auctions.
- `portal` (12,006 LOC, `1f39d35f2`): Trustless network explorer (`portal.dregg.studio`) embedding the
  `dregg-wasm` recursive STARK light client. Verified block headers and turn receipts locally in the tab.
- `extension` (74,905 LOC, `06b366e54`): Firefox/Chrome browser extension exposing `window.dregg`. Managed
  BIP-39 mnemonic phrases, signed transactions, and brokered capability delegations.
- `spween-dregg` (8,183 LOC, `4ddb4f1f6`): Bound the Spween narrative-choice DSL to sovereign world-cells.
  Every player dialogue choice was executed as a verified turn, producing an unforgeable, un-retconnable
  receipt chain. Included `VoteEngine` for collective Twitch-plays-style storytelling.

---

## 2. The Moldable Inspector & Gadget Framework

In `starbridge-v2/src/presentable.rs` (commit `800945db6`) and `docs/deos/INSPECTOR-FRAMEWORK.md`,
Ember adapted Tudor Gîrba's Glamorous Toolkit (GT) and Pharo moldable inspector philosophy to
the cryptographic ledger.

```
+---------------------------------------------------------------------------------------------------+
|                                  THE MOLDABLE INSPECTOR PIPELINE                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-------------------------------------------------------------------------------------------+   |
|   |                      The 7 Presentation Kinds (enum PresentationKind)                     |   |
|   |  1. RawFields: Mandatory structural floor (field-tree with attested redactions)           |   |
|   |  2. Graph: Ocap delegations, cell reachability closure, state machine transitions         |   |
|   |  3. DomainVisual: High-level domain visualizer (ballot box, token ring, clearance tape)   |   |
|   |  4. Affordances: Cap-gated message roster; illuminated = allowed, dimmed = refused       |   |
|   |  5. Provenance: Irrevocable receipt chain, turn author signatures, blame graph            |   |
|   |  6. Invariant: Active state constraints, Lean theorem checks, conservation proofs        |   |
|   |  7. Source: Underlying Lean / Objective Bend / AST source definition                      |   |
|   +-------------------------------------------------------------------------------------------+   |
|                                                |                                                  |
|                                                v                                                  |
|   +-------------------------------------------------------------------------------------------+   |
|   |                         Interactive Gadgets (trait CommittingGadget)                      |   |
|   |                                                                                           |   |
|   |    [User Input / Dial]  --->  IntentDraft  --->  simulate()  --->  commit_turn()          |   |
|   |                                                      |                    |               |   |
|   |                                             (Predict Turn)         (Verified Turn)        |   |
|   +-------------------------------------------------------------------------------------------+   |
|                                                |                                                  |
|                                                v                                                  |
|   +-------------------------------------------------------------------------------------------+   |
|   |                         The L1--L10 Shipped Inspector Ladder                              |   |
|   |   L1: presentable.rs         L2: predicate_composer.rs      L3: turn_builder.rs           |   |
|   |   L4: cap_inspector.rs       L5: cell_inspector.rs          L6: receipts_inspector.rs     |   |
|   |   L7: token_inspector.rs     L8: federation_inspector.rs    L9: circuit_inspector.rs      |   |
|   |                              L10: settlement_inspector.rs                                 |   |
|   +-------------------------------------------------------------------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### 2.1 The Core Traits: `Presentable`, `Gadget`, `CommittingGadget`

Unlike standard debuggers that provide a static, one-size-fits-all JSON or property-grid tree,
every DeOS protocol object implemented `Presentable`:

```rust
// starbridge-v2/src/presentable.rs
pub trait Presentable {
    /// Returns the set of named presentation faces this object supports.
    fn presentations(&self, ctx: &PresentationContext) -> Vec<Presentation>;

    /// Render a specific presentation face.
    fn render_presentation(&self, kind: PresentationKind, ctx: &PresentationContext) -> PresentationBody;
}

pub trait Gadget {
    type Output;
    fn render_editor(&mut self, ui: &mut GadgetUi) -> Option<Self::Output>;
}

pub trait CommittingGadget: Gadget {
    /// Predict-then-commit: every UI mutation stages an IntentDraft,
    /// verifies the turn against local invariants, and commits to the ledger.
    fn stage_intent(&self) -> Result<IntentDraft, GadgetError>;
    fn commit(&mut self, executor: &mut TurnExecutor) -> Result<Receipt, GadgetError>;
}
```

### 2.2 The Shipped L1–L10 Ladder

The framework successfully replaced monolithic UI views with modular inspector modules:
- **L1 — Presentation Spine (`presentable.rs`)**: Base registry, presentation kinds, and `Spotter` palette.
- **L2 — Predicate Composer (`predicate_composer.rs`)**: Visual builder for `StateConstraint` predicates
  (`WriteOnce`, `Monotonic`, `AffineLe`).
- **L3 — Turn Builder (`turn_builder.rs`)**: Effect stage and intent drafter.
- **L4 — Cap Inspector (`cap_inspector.rs`)**: Visualized capability attenuation chains and caveats.
- **L5 — Cell Inspector (`cell_inspector.rs`)**: Live cell slot viewer and value inspector.
- **L6 — Receipts Inspector (`receipts_inspector.rs`)**: Turn receipt auditor and execution trace walker.
- **L7 — Token Inspector (`token_inspector.rs`)**: Balance rings and conservation law verifier.
- **L8 — Federation Inspector (`federation_inspector.rs`)**: Blocklace DAG consensus viewer.
- **L9 — Circuit Inspector (`circuit_inspector.rs`)**: AIR constraint polynomial viewer.
- **L10 — Settlement Inspector (`settlement_inspector.rs`)**: Cross-chain bridge escrow and settlement status.

---

## 3. The Diaspora: How Ideas & Surfaces Spread Into Modern Projects

When the monolithic Breadstuffs repository froze in August–October 2026, its ideas did not die;
they dispersed into specialized downstream projects.

```
                                    /Users/ember/dev/breadstuffs
                                                 |
         +--------------------+------------------+-------------------+--------------------+
         |                    |                                      |                    |
         v                    v                                      v                    v
  ~/dev/delvetalk2      ~/dev/spween & spw-workbench           ~/dev/minidregg     ~/dev/obend/obend-gui
  ----------------      ----------------------------           ---------------     ---------------------
  - Inhabited Town      - Standalone DSL crate                 - "DeOS Crown"      - Lightweight runner
  - Plain-words Law     - VS Code extension & LSP                Lean theorems     - 10 ProjectionKinds
  - Cards & Spells      - Semantic brace operators             - Compressed core   - LawDial controls
  - AT Protocol repo    - Narrative state trees                  (<150k lines)     - SVG / HTML views
  - "No coins" rule     - Collective branch choice             - Zero twins        - Picard-Lindelof ODE
```

### 3.1 Diaspora Destinations

#### 1. `delvetalk` & `delvetalk2` (`/Users/ember/dev/delvetalk2`, branch `foundation`)
- **The Inhabited World Reborn**: DelveTalk inherited the soul of DeOS—the world of durable, programmable,
  inhabited objects. But it radically subtracted the heavy GUI scaffolding:
  - *Monolithic GPUI replaced by Plain Text & Cards*: Objects are described by cards; interactions take
    the form of natural-language replies or concise "spells" (`delvetalk garden-1 plant`).
  - *Hob the Reader*: Ingestion layer translating natural language into admitted action spells.
  - *AT Protocol Repository*: Town state federated as signed AT Protocol records (`did:web:gsb.fg-goose.online`).
  - *"No coins" Rule*: Strict policy against exposing raw hashes, DIDs, or blockchain jargon on
    user-facing surfaces.

#### 2. `spween` & `spw-workbench` (`/Users/ember/dev/spween`, `/Users/ember/dev/spw-workbench`)
- `spween`: Decoupled into an elegant, educational DSL parser and interpreter for interactive fiction,
  maintaining the trait-based `EffectHandler` abstraction.
- `spw-workbench`: Evolved into a dedicated organelle for `.spw` workspaces, featuring a complete
  Language Server Protocol (LSP) server, CLI, runtime, and VS Code extension (`extensions/vscode-spw`).

#### 3. `minidregg` (`/Users/ember/dev/minidregg`)
- **The DeOS Crown Preserved in Lean**: In `minidregg/ATLAS.md` (§3, item 14), Ember codified what
  survived Breadstuffs:
  > *"The deos crown: surface-as-cap, membrane non-amplification, `replayedDeterministic_iff_confined`
  > (confinement IS the deterministic-replay fragment), affordance-soundness; DocMerge as LUB / pushout
  > products; fog-of-war non-interference. Identity: affordance = cap-gated effect-template;
  > firing = turn; turn = receipt — one machinery, three faces (human/authored/agentic)."*
- `tests/objective-bend-source/DeosCounter.obend`: Directly ported Breadstuffs' `deos-js` counter
  applet into formal Objective Bend syntax, modeling turns as `Activity<Plan, Response, Nat>`.

#### 4. `obend-gui` (`/Users/ember/dev/obend/crates/obend-gui`, 2,088 LOC)
- **The Modern Viewport Successor**: Replaced `starbridge-v2`'s massive 194k-line GPUI monolith with
  a tight, modular notebook runner and hardware CAD projection previewer.
- Supports 10 distinct `ProjectionKind`s:
  `Circuit`, `Netlist`, `Timing`, `Gdsii`, `Waveform`, `CellQuote`, `NotebookCell`, `ProofTree`,
  `ContractBadge`, `ClearingLedger`.
- Implements interactive SVG/HTML rendering for Picard–Lindelöf ODE flowpipe slices, 5-axis CNC
  waypoints, eFPGA heatmaps, and live `.free` / `.press` / `.locked` `LawDial` controls.

---

### 3.2 Lessons Learned in the Transition

#### 1. Why Rigid Monolithic Shells Failed
- **The Build Lock Nightmare**: In July 2026, local developer iteration ground to a halt because
  compiling `starbridge-v2` locked the entire target directory. Building the desktop cockpit pulled
  GPUI, Alacritty, Servo, SpiderMonkey, Matrix SDK, and the Lean kernel archive (`libdregg_lean.a`),
  resulting in a 292MB binary that took minutes to link and frequently jammed (`reference-persvati-remote-build`).
- **Duplicate Dependency Crises**: Direct dependencies collided with nested dependencies (e.g. workspace
  GPUI `adb902652` vs `gpui-component`'s internal `54fbcb6943`), requiring complex workspace overrides.
- **Immediate-Mode UI Re-execution Overhead**: Commit `f27fd4169` documented that the cockpit repainted
  carded surfaces as frozen snapshots every frame, BLAKE3-hashing the entire state root on every render
  tick because projection memoization had not been integrated.
- **The Autonomous Swarm Failure**: In `~/.claude/projects/-Users-ember-dev-delvetalk/memory/ember-working-style.md:21`:
  > *"Three hours of autonomous codex produced 45 commits and a 124K-line repo ember called
  > 'horseshit' and 'chug'; the failure was orchestration and refusal to subtract, not effort."*
  The remedy was radical subtraction: separate the data models, drop monolithic GUI frameworks, and
  deliver user agency through lightweight, composable surfaces.

#### 2. Why GPUI Cockpit Builds Needed Discipline
- Monolithic cockpits must not bundle full editor workspaces, full web browsers, and full chat servers
  into the primary binary. The split pioneered by `deos-view` (declarative `ViewNode` tree) and
  `obend-gui` (HTTP/WebSocket server streaming interactive SVG/HTML viewports) demonstrated that
  **rendering belongs at the edge, while state remains pure, verifiable data.**

#### 3. How Sandstorm `.spk` Grains Evolved
- Sandstorm proved the elegance of capability-secured application grains with private `/var` heaps.
  However, Sandstorm grains lacked decentralized, light-client witnessability—users had to trust the
  central Sandstorm supervisor.
- In DeOS, grains became **content-addressed sovereign cells** with verifiable `umem` heaps.
  In `minidregg` and `delvetalk2`, this evolved into sovereign objects where state transitions are
  mathematically checked against a plain-words law and recorded on an AT Protocol or blocklace journal.

---

## 4. What Got Dropped, Parked, or Underelaborated

During the late-summer 2026 pivot to kernel verification and Mini/Nano rebuilds, several advanced
surfaces were parked. These assets represent hundreds of thousands of lines of high-value work:

1. **`deos-zed` & `deos-zed-full` (11,446 LOC)**: The proven integration of Zed's `Workspace` over
   `FirmamentZedFs`. Parked due to GPUI/Zed upstream churn. Left behind: a working editor where saving
   a file emits a verified Pijul/DocCore patch turn.
2. **`deos-matrix` & `deos-homeserver` (21,190 LOC)**: The rehydratable membrane chat client and
   grain-hosted Matrix homeserver. Parked when the consensus layer detached from the legacy node.
   Left behind: the UI mechanism for sending live, forkable world branches inside chat messages.
3. **`deos-reflect` (1,420 LOC)**: The pure, cap-bounded reflection engine. Parked during the
   crate-split campaign. Left behind: the only audit-proven inspector that redacts secrets and graphs
   capability blast radiuses without pulling GPUI.
4. **`servo-render` (24,749 LOC)**: Software-rasterized web browsing using WebRender SWGL. Parked due
   to SpiderMonkey build complexity. Left behind: working C++17 software rasterization emitting RGBA8
   tiles verified by cryptographic digests.
5. **`android-cell` (Graphideos, 11,066 LOC)**: Android container/emulator isolation with capability
   badging. Parked as out-of-scope for the kernel bakeoff. Left behind: real `Context.checkSelfPermission`
   interposition and SystemUI capability status bars.
6. **The 34 Apps in `starbridge-apps` (114,679 LOC)**: 32 complete domain applications (voting, auctions,
   escrow, identity, bounty boards, compute markets) adhering to *"The answer is never Effect::FooApp"*.
   Left behind: complete factory descriptors and slot caveats (`WriteOnce`, `Monotonic`, `AffineLe`).
7. **`drex-web-v2` & `launchpad-web` (4,035 LOC)**: Modern Preact + Signals trading terminals with
   3-tier dials (Open/Shielded/Dark) and live turn-stream fair launches.
8. **`extension` & `portal` (86,911 LOC)**: Browser extension capability broker and in-browser
   recursive STARK light client verifier.
9. **`moldable-inspector` (L1–L10 ladder)**: The 7 presentation faces and gadget composition spine,
   currently locked inside the legacy `starbridge-v2` crate.

---

## 5. Concrete Revival Roadmap: Re-Attaching Surfaces to Obend, Mini & DelveTalk2

The diaspora surfaces can be systematically revived by mounting them onto modern hosts:
`obend-gui`, `delvetalk2`, `minidregg`, and `spw-workbench`.

### 5.1 The Master Revival Matrix

| Parked Crate / Asset | Breadstuffs LOC & Key Entry | Modern Target Host | New Adapter Seam / Mechanism | Revival Tier & Milestone |
|---|---|---|---|---|
| **`deos-reflect`** | 1,420 LOC<br>`deos-reflect/src/lib.rs` | `minidregg` & `delvetalk2` | Bind `Inspectable` & `Frustum` over DelveTalk `WorldObject`s and Lean ASTs | **Tier 1 (Immediate)**<br>Milestone: Cap-bounded reflection over DelveTalk cards |
| **`starbridge-apps` (8 Core Seed Apps)** | ~35,000 LOC<br>`starbridge-apps/{nameservice, identity, bounty-board, privacy-voting}` | `delvetalk2` & `minidregg` | Compile FactoryDescriptors into Objective Bend `.obend` record/law definitions | **Tier 1 (Immediate)**<br>Milestone: Bounty board & voting running as DelveTalk objects |
| **`moldable-inspector` (Spine & Presentable)** | ~8,000 LOC<br>`starbridge-v2/src/presentable.rs` | `obend/crates/obend-gui` | Map the 7 `PresentationKind`s to `obend_gui::ProjectionKind` and SVG/HTML views | **Tier 1 (Immediate)**<br>Milestone: Multi-face inspection of Obend notebooks & Lean proofs |
| **`spween-dregg`** | 8,183 LOC<br>`spween-dregg/src/lib.rs` | `delvetalk2` & `~/dev/spween` | Re-wire `spween::EffectHandler` to DelveTalk `Activity<Plan, Response>` | **Tier 1 (Immediate)**<br>Milestone: Verifiable CYOA scenes embedded in Delve.town cards |
| **`deos-view` (Web/HTML Render Path)** | ~9,000 LOC<br>`deos-view/src/web.rs` | `obend-gui/src/server.rs` | Translate `ViewNode` trees into `obend-gui` interactive HTML/SVG viewports | **Tier 2 (Near-Term)**<br>Milestone: Declarative card rendering in Obend browser interface |
| **`sandstorm-package`** | 2,248 LOC<br>`sandstorm-package/src/lib.rs` | `minidregg` hosting | Reuse Ember's clean Sep 26 standalone parser (`028bc0271`) to unpack `.spk` bundles | **Tier 2 (Near-Term)**<br>Milestone: Loading signed legacy Sandstorm tools into cell heaps |
| **`drex-web-v2` & `launchpad-web`** | 4,035 LOC<br>`drex-web-v2/src/app.js` | `obend-gui` web client | Replace legacy RPC with `obend-gui` WebSocket `/ws/eval` and DelveTalk feeds | **Tier 2 (Near-Term)**<br>Milestone: 3-tier dial (Open/Shielded/Dark) trading terminal |
| **`deos-matrix` Rehydratable Membrane** | 7,706 LOC<br>`deos-matrix/src/membrane.rs` | `delvetalk2` AT Proto Journal | Serialize DelveTalk object frustums into AT Proto records; stitch via pushout | **Tier 2 (Near-Term)**<br>Milestone: Sharing live forkable town rooms via feed messages |
| **`deos-zed` / `FirmamentZedFs`** | 11,446 LOC<br>`deos-zed-full/src/firmament_zed_fs.rs` | `spw-workbench` & Zed | Mount `FirmamentZedFs` as an LSP Virtual Document provider or VS Code FS provider | **Tier 3 (Frontier)**<br>Milestone: Cell-backed editor where saving commits verified turns |
| **`servo-render` (SWGL Standalone)** | 24,749 LOC<br>`servo-render/src/swgl_context.rs` | `obend-gui` offline CAD render | CPU software rasterizer for generating certified headless HTML/SVG screenshots | **Tier 3 (Frontier)**<br>Milestone: Headless, GPU-free render pipe for contract badges |
| **`android-cell` (Graphideos)** | 11,066 LOC<br>`android-cell/src/appfactory.rs` | Sandboxed MicroVM / Container | Run APKs under Hypervisor.framework with cap-badges wired to DelveTalk laws | **Tier 3 (Frontier)**<br>Milestone: Mobile application containment on sovereign OS |

---

### 5.2 Phased Execution Plan

#### Phase 1: Semantic Re-Attachment (Immediate — T1)
1. **DelveTalk2 App Ingestion**:
   - Extract the 8 core factory descriptors from `starbridge-apps/` (`bounty-board`, `privacy-voting`,
     `nameservice`, `identity`, `compute-exchange`, `gallery`, `subscription`, `governed-namespace`).
   - Re-express their state constraints (`WriteOnce`, `Monotonic`, `AffineLe`) as plain-language laws
     and Objective Bend activities in `delvetalk2/capsules/`.
2. **Moldable Inspector in Obend-GUI**:
   - Lift `PresentationKind` and the `Presentable` trait from `starbridge-v2/src/presentable.rs` into
     `obend-gui/src/viewport.rs`.
   - Wire `RawFields`, `Graph`, `DomainVisual`, `Invariant`, and `Source` into `obend-gui`'s existing
     10 `ProjectionKind`s, enabling rich visual inspection of Lean goals, Picard–Lindelöf ODE flowpipes,
     and hardware layouts.
3. **Spween Narrative Choice in DelveTalk**:
   - Reconnect `spween` to `delvetalk2`, allowing cards to present interactive narrative scenes where
     replying with a spell advances the passage and records an immutable receipt.

#### Phase 2: Web & Communications Decoupling (Near-Term — T2)
1. **Lightweight Card Web View**:
   - Port `deos-view/src/tree.rs` and `web.rs` into `obend-gui/src/server.rs`.
   - Provide an HTTP/WebSocket endpoint rendering declarative `ViewNode` cards directly in browsers
     without requiring GPUI or native desktop builds.
2. **AT Protocol Rehydratable Membranes**:
   - Adapt `deos-matrix/src/membrane.rs` to DelveTalk's AT Protocol sync layer.
   - When a user shares a room or object state, emit an AT Protocol record holding the cap-bounded
     frustum snapshot. Any follower can rehydrate the object, experiment locally, and propose an
     admitted patch.
3. **Sandstorm Package Hosting**:
   - Connect `sandstorm-package` (`028bc0271`) to `minidregg`, allowing standalone `.spk` archives
     to be uploaded and executed in confined WebAssembly environments.

#### Phase 3: The Sovereign Workbench (Frontier — T3)
1. **Virtual Cell Filesystem for Editors**:
   - Extract the async FS abstractions from `deos-zed-full/src/firmament_zed_fs.rs`.
   - Implement a VS Code / Zed Language Server extension in `spw-workbench` that mounts `cell://` URIs,
     enabling developers to edit live on-ledger objects with automatic turn-receipt emission on save.
2. **Deterministic SWGL Document Bakes**:
   - Recommission `servo-render`'s standalone SWGL rasterizer to produce cryptographic PNG snapshots
     of rendered cards and hardware viewports, guaranteeing identical pixel output across macOS, Linux,
     and seL4 without depending on host GPU drivers.

---

## 6. Conclusion: The Return of the Living Image

The tragedy of the original DeOS effort in `breadstuffs` was not an error of vision; it was an error
of **packaging and mass**. By attempting to construct the compiler, the proof system, the microkernel,
the GPUI desktop, the browser engine, the editor, the chat system, and 34 applications in a single,
interlocked monorepo, build friction and dependency cascades eventually choked developer iteration.

The diaspora to `delvetalk2`, `minidregg`, `spween`, and `obend-gui` was a necessary retreat to
sanity—a subtraction campaign that restored fast cycles, modular boundaries, and clean formal methods.
Now that `minidregg` has settled the verified kernel core, `obend` has established the projection
viewports, and `delvetalk2` has proven the power of an inhabited town of objects, **the rich surfaces
of DeOS and Starbridge can be reclaimed.**

By re-attaching the moldable inspector, the rehydratable membrane, the 32 starbridge apps, and the
card-based view-tree to these lean modern substrates, Ember's original 1999 AOL wonder—the live,
malleable, self-describing computing image where a child can click with delight and an adept can
inspect every mathematical invariant—is finally ready to live.
