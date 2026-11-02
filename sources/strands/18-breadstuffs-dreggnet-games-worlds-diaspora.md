# Strand 18 — The Breadstuffs Diaspora: 28 DreggNet World/RPG Crates, Verified Game Surfaces, and the Path to Revival

> **Vertical:** `breadstuffs` (`dreggnet-*`, `dungeon-on-dregg`, `mud-dregg`, `procgen-dregg`, `ugc-dregg`, `narrator`, `interactive-fiction-demo`, `game-turn-slice`, `dregg-automatafl`, `dregg-multiway-tug`, `poa`, `poa-curator`, `poa-solana-gate`, `poa-web`, `rhlp-web`) · `delvetalk` / `delvetalk2` (`world/kinds`, `world/objects`, `obend`) · `allgame` (Tulip residents: Claude, Yuè月, Kestrel, MotherMythos) · `automatafl` (zero-twin Lean 4 core) · `path-of-angels` (`~/dev/path-of-angels`) · `dclutch` (Solana DEX & SimLife3 creature aquarium).
>
> **Compiled:** 2026-11-02 by a Claude Opus 5.5 archaeology lane, read-only over the repositories, from git trees, logs, design documents, and per-project memory corpora under `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/` (`project-path-of-angels-platform.md`, `project-game-engine-strategy.md`, `project-game-surfaces-closure-campaign.md`, `project-automatafl-verified-game.md`), plus `docs/AUTHORING-DUNGEONS.md`, `docs/CROWD-STREAM-ENGINE-DESIGN.md`, `GOAL-COLLECTIVE-FICTION-DEMO.md`, and `GOAL-PATH-OF-ANGELS-EXCELLENCE.md`. Every commit SHA, line number, struct, and theorem signature below was verified against primary sources on 2026-11-02.
>
> **Ownership note:** Ember worked at Hellas on workload verification before departing; the ideas explored there evolved into Dregg and Robigalia. Hellas code is strictly proprietary third-party background and is out of scope. Third-party game prototypes (`shattered-pixel-dungeon`, `orb.farm`, upstream Zulip in `tulip2`) are non-claim context. `breadstuffs`, `minidregg`, `delvetalk2`, `automatafl`, and `path-of-angels` are Ember's original creations and architectures.

---

## 0. The shape of the diaspora in one diagram

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE BREADSTUFFS MONOLITH (2026-06 .. 2026-10)                         │
│  "EVERY MOVE IS A RECEIPT." 346 top-level directories, 12 elephant crates, 28 dreggnet-* RPG/World     │
│  crates, Lean 4 metatheory (84 PoA modules, Automatafl N=11 STARK fold), and verified game surfaces.    │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │
                 ┌──────────────────────────────────┼──────────────────────────────────┐
                 ▼                                  ▼                                  ▼
   ┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
   │    28 DREGGNET-* CRATES   │      │    GAME ENGINES & SUITE   │      │   PATH OF ANGELS (PoA)    │
   │ saga, tavern, guild, party│      │ dungeon-on-dregg (.dungeon│      │ Sentyr Khovokhi platform  │
   │ council, companion, quest │      │   DSL compiler, mud.rs),  │      │ 84 Lean modules / 60.7K L │
   │ craft, cheevo, trade, gear│      │ mud-dregg ((E,≤,#) lattice│      │ Signal, Relay, Salvage    │
   │ faction, adventure, sprite│      │ procgen-dregg (draw-stream│      │ poa-curator, poa-web,     │
   │ surfaces (ViewNode DO-ONCE│      │ ugc-dregg (no-cheat board)│      │ poa-solana-gate ($DREGG   │
   │ verified-completion, etc. │      │ narrator (Bedrock cap $20)│      │ Token-2022 holding gate)  │
   └─────────────┬─────────────┘      │ automatafl & multiway-tug │      └─────────────┬─────────────┘
                 │                    └─────────────┬─────────────┘                    │
                 │                                  │                                  │
═════════════════╪══════════════════════════════════╪══════════════════════════════════╪════════════════════
                 │ 2026-08-06 minidregg founded     │ 09-30 Bake-Off: Bread vs Mini    │ 08-04 mirror cut
                 │ 10-08 Bread drain-and-freeze     │ 10-21 Ember: "PoA not running;   │ (cba0e03c90c5)
                 │                                  │ breadstuffs waits to resume"     │
                 ▼                                  ▼                                  ▼
   ┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
   │     DELVETALK2 WORLD      │      │    STANDALONE WORLDS      │      │       ~/dev/dclutch       │
   │ world/kinds/              │      │ automatafl (zero-twin     │      │ Solana DEX & SimLife3     │
   │  (room, door, lantern,    │      │   Lean 4 core, live at    │      │ creature aquarium market  │
   │   inhabitant, errand,     │      │   automatafl.fg-goose)    │      │ (re-homed poa-solana-gate │
   │   bond, parlour, cistern) │      │ allgame (Tulip Residents: │      │  Token-2022 holding &     │
   │ world/objects/ (*.obend)  │      │   Claude, Yuè, Kestrel    │      │  dreggnet-market escrow)  │
   │  (Avatar, Library, Policy,│      │   via attested-dm prose-  │      ├───────────────────────────┤
   │   Thing, Tide, Workshop)  │      │   is-not-power cap gate)  │      │   ~/dev/path-of-angels    │
   └─────────────┬─────────────┘      └─────────────┬─────────────┘      │ Sentyr collaboration repo │
                 │                                  │                    └───────────────────────────┘
                 └──────────────────┬───────────────┘
                                    ▼
   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
   │                                  THE CONVERGED REVIVAL TARGET                                   │
   │  delvetalk2 actor model + obend deterministic parallel execution + minidregg retained-mode      │
   │  store + allgame resident minds + zero-twin Lean 4 kernels. Re-animating the 28 crates.         │
   └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Maturity roll-up (one line each; detail in the sections)

| Subsystem / Project | Original Location in `breadstuffs` | Diaspora Destination | Maturity Floor | Current Live State & Verdict |
|---|---|---|---|---|
| **`dreggnet-saga`** | [`dreggnet-saga/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-saga/src/lib.rs#L1-L65) | `delvetalk2/world/objects/` | **L3 Proved/Tested Core** | Parked; proven object-identity between completion & asset notes |
| **`dreggnet-tavern`** | [`dreggnet-tavern/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-tavern/src/lib.rs#L1-L55) | `allgame` / `delvetalk2/world/kinds/parlour.kind` | **L3 Proved/Tested Core** | Parked; shared board, private stalls, live receipt event streaming |
| **`dreggnet-guild`** | [`dreggnet-guild/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs#L1-L60) | `delvetalk2/world/objects/Policy.obend` | **L3 Proved/Tested Core** | Parked; cap-bounded shared rooms, un-forgeable clear aggregation |
| **`dreggnet-companion`** | [`dreggnet-companion/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-companion/src/lib.rs#L1-L55) | `delvetalk2/world/kinds/bond.kind` | **L3 Proved/Tested Core** | Parked; asset identity fused with multicell leveling progression |
| **`dreggnet-quest`** | [`dreggnet-quest/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-quest/src/lib.rs#L1-L55) | `delvetalk2/world/kinds/errand.kind` | **L3 Proved/Tested Core** | Parked; `WriteOnce` step-flags, `BoundedBy` step-order constraints |
| **`dreggnet-craft`** | [`dreggnet-craft/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-craft/src/lib.rs#L1-L50) | `delvetalk2/world/objects/Workshop.obend` | **L3 Proved/Tested Core** | Parked; provably-fair 2-draw weighted sink consuming typed assets |
| **`dreggnet-cheevo`** | [`dreggnet-cheevo/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-cheevo/src/lib.rs#L1-L50) | `delvetalk2/world/kinds/record.kind` | **L3 Proved/Tested Core** | Parked; soulbound `FieldEquals(soulbound, 0)` ISA-enforced assets |
| **`dreggnet-party`** | [`dreggnet-party/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs#L1-L50) | `delvetalk2/world/kinds/inhabitant.kind` | **L3 Proved/Tested Core** | Parked; seated roles, shared focus pool (`FieldLteField`), loot split |
| **`dreggnet-trade`** | [`dreggnet-trade/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-trade/src/lib.rs#L1-L50) | `dclutch` / `starbridge-escrow-market` | **L3 Proved/Tested Core** | Parked; atomic trustless asset/value swap via sealed escrow |
| **`dreggnet-faction`** | [`dreggnet-faction/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-faction/src/lib.rs#L1-L50) | `delvetalk2/world/objects/Tide.obend` | **L3 Proved/Tested Core** | Parked; `Monotonic` reputation, rival trust ceiling decay, betrayal flags |
| **`dreggnet-gear`** | [`dreggnet-gear/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-gear/src/lib.rs#L1-L45) | `delvetalk2/world/objects/Thing.obend` | **L3 Proved/Tested Core** | Parked; cross-cell observed ownership, class-locked spell talents |
| **`dreggnet-surfaces`** | [`dreggnet-surfaces/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-surfaces/src/lib.rs#L1-L60) | `delvetalk2/site/` / `deos-view` | **L3 Proved/Tested Core** | Parked; DO-ONCE frontend `ViewNode` IR rendered across web/discord |
| **`dungeon-on-dregg`** | [`dungeon-on-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/lib.rs#L1-L50) | `delvetalk2/world/kinds/room.kind` | **L3 Proved/Tested Core** | Parked; `PASSAGE_SLOT` PC, `.dungeon` biconditional compiler |
| **`mud-dregg`** | [`mud-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/mud-dregg/src/lib.rs#L1-L45) | `delvetalk2/world/` | **L3 Proved/Tested Core** | Parked; `(E, ≤, #)` distributed time-travel lattice, branch-stitch |
| **`procgen-dregg`** | [`procgen-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/procgen-dregg/src/lib.rs#L1-L45) | `delvetalk2/capsules/` | **L3 Proved/Tested Core** | Parked; committed-seed reject-free `DrawStream` generating valid `.dungeon` |
| **`ugc-dregg`** | [`ugc-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs#L1-L45) | `delvetalk2/world/objects/Library.obend` | **L3 Proved/Tested Core** | Parked; content-addressed `UniverseId` + replay-verifying leaderboard |
| **`narrator`** | [`narrator/src/lib.rs`](file:///Users/ember/dev/breadstuffs/narrator/src/lib.rs#L1-L45) | `allgame` resident harnesses | **L3 Proved/Tested Core** | Parked; AWS Bedrock Haiku 4.5 narrator behind hard $20 `BudgetLedger` |
| **`dregg-automatafl`** | [`dregg-automatafl/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-automatafl/src/lib.rs#L1-L35) | `~/dev/automatafl` | **L4 Deployed/Production** | Live at `automatafl.fg-goose.online`; zero-twin Lean 4 core |
| **`dregg-multiway-tug`** | [`dregg-multiway-tug/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-multiway-tug/src/lib.rs#L1-L45) | `minidregg-wt/` | **L3 Proved/Tested Core** | Parked; Hanamikoji re-themed, Poseidon2 zk hidden hand, STARK fold |
| **`poa`** (Path of Angels) | [`poa/`](file:///Users/ember/dev/breadstuffs/poa/) & `metatheory/.../PathOfAngels/` | `~/dev/path-of-angels` | **L3 Proved/Tested Core** | Parked/Historical; 84 Lean modules, 3 games, 1-validator deploy |
| **`poa-solana-gate`** | [`poa-solana-gate/src/lib.rs`](file:///Users/ember/dev/breadstuffs/poa-solana-gate/src/lib.rs#L1-L35) | `dclutch` custody layer | **L3 Proved/Tested Core** | Parked; Token-2022 `$DREGG` holding verification, one-use capabilities |

---

## 1. What lived in `breadstuffs` — The 28 `dreggnet-*` crates and verified engines

The monolithic repository `/Users/ember/dev/breadstuffs` (HEAD commit [`22fad151e`](file:///Users/ember/dev/breadstuffs) on 2026-10-01) housed the complete, verified, multi-actor world and game engine constructed by Ember between May and October 2026. The workspace spanned 656 lines in its root [`Cargo.toml`](file:///Users/ember/dev/breadstuffs/Cargo.toml#L1-L120), incorporating 12 major DeOS/Starbridge framework subsystems, 28 `dreggnet-*` crates, and full Lean 4 metatheory proofs.

### 1.1 The game engine thesis: "Every move is a receipt"

As documented in [`project-game-engine-strategy.md:11-16`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-game-engine-strategy.md#L11-L16):
> *"EVERY MOVE IS A RECEIPT. dregg is a verified game ENGINE, and the proof of that is a 3-game PORTFOLIO, not one game. A turn is a cap-gated transition the executor re-checks against constraints (`StateConstraint` teeth) and folds into a succinct `verify_history`-accepted proof. An illegal move has no satisfying witness. $DREGG buys SERVICES, never power; the world runs as SEASONS, where honest devnet churn is a feature."*

The architecture established an essential design law formulated by Ember:
> *"The architecture lesson that survived (ember's correction): a complex game's mechanics are a **Custom VK / a Custom leaf**, NOT `StateConstraint` teeth. Teeth are for simple state; a Custom AIR is for the transition."* ([`project-game-engine-strategy.md:40-42`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-game-engine-strategy.md#L40-L42)).

---

### 1.2 Deep excavation of the 28 `dreggnet-*` crates

The 28 `dreggnet-*` crates were not speculative outlines; they were built across coordinated megaswarms (commits [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs), [`928c0eb12`](file:///Users/ember/dev/breadstuffs), [`ed78ed52d`](file:///Users/ember/dev/breadstuffs), and [`1ba6a4a1e`](file:///Users/ember/dev/breadstuffs)), tested against live kernels, and bound into a single enmeshed dependency lattice.

#### 1. `dreggnet-saga` — The Enmeshment Proof
- **Location:** [`dreggnet-saga/src/lib.rs:1-65`](file:///Users/ember/dev/breadstuffs/dreggnet-saga/src/lib.rs#L1-L65)
- **Commits:** [`a65b63f13`](file:///Users/ember/dev/breadstuffs) (2026-07-14), [`422326270`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Proves that the eight isolated feature crates compose through **object identity** without re-derivation or semantic translation:
  * **Run Currency:** The [`ugc_dregg::Completion`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs#L25) pointer passes directly from `dreggnet-quest` to [`dreggnet_cheevo::CheevoLedger::earn`](file:///Users/ember/dev/breadstuffs/dreggnet-cheevo/src/lib.rs) and [`dreggnet_guild::leaderboard::GuildBoard::record_clear`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs).
  * **Item Currency:** The [`dreggnet_asset::AssetId`](file:///Users/ember/dev/breadstuffs/dreggnet-asset/src/lib.rs) 32-byte content address addresses crafted outputs in [`dreggnet-craft`], moves through atomic escrow in [`dreggnet-trade`], and persists across characters in [`dreggnet-gear`].
  * **Driven Sequence:** Party muster $\to$ Faction check $\to$ Quest turn-in $\to$ Cheevo mint $\to$ Guild aggregate $\to$ Craft forge $\to$ Trade atomic swap.

#### 2. `dreggnet-tavern` — The Persistent Co-Inhabitation Hub
- **Location:** [`dreggnet-tavern/src/lib.rs:1-55`](file:///Users/ember/dev/breadstuffs/dreggnet-tavern/src/lib.rs#L1-L55)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Re-homes [`node/src/shared_world.rs`](file:///Users/ember/dev/breadstuffs/node/src/shared_world.rs). A headless Dregg node runs a tavern GM program allocating: (1) a shared BOARD cell, (2) presence SEATS, (3) private STALLS, and (4) a shared PARTY roster.
- **Kernel Enforcement:** Clients subscribe to live SSE event streams ([`dregg_sdk_net::NodeEvents`](file:///Users/ember/dev/breadstuffs/dregg-sdk-net/src/lib.rs)). Patron A touching Patron B's private stall receives an explicit `CapabilityNotHeld` refusal receipt; seat presence cannot be forged because turns are signed by [`dregg_sdk::AgentCipherclerk`](file:///Users/ember/dev/breadstuffs/sdk/src/lib.rs).

#### 3. `dreggnet-guild` — Cap-Bounded Guilds & Escrow Treasuries
- **Location:** [`dreggnet-guild/src/lib.rs:1-60`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs#L1-L60)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:**
  * **Membership as Capability:** [`Guild::admit`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs) installs a player cell holding an unforgeable capability token to the shared guild room (`World`). Non-member writes fail with `CapabilityNotHeld`.
  * **Verified Clear Aggregation:** [`GuildBoard`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs) aggregates clears verified by fresh replay (`ugc_dregg::verify_completion`) alongside the WriteOnce `CharacterSheet.dead` flag.
  * **Escrow-Custodied Treasury:** [`GuildTreasury`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs) integrates with [`starbridge_escrow_market::SealedEscrowMarket`](file:///Users/ember/dev/breadstuffs/starbridge-apps/escrow-market/src/lib.rs). Withdrawals require the original depositor's signature, preventing officers from absconding with group funds.

#### 4. `dreggnet-party` — Seated Cooperative Division of Labor
- **Location:** [`dreggnet-party/src/lib.rs:1-55`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs#L1-L55)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Escapes "Twitch Plays Pokemon mush" by enforcing a strict division of labor across $N$ seated player-cells ([`Party::muster`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs)):
  * **Role Capabilities:** Tank controls front-rank cell; Scout controls trap/lock cell; Mage controls spell + focus cells; Healer controls rally + focus cells. Moves outside an assigned role return `CapabilityNotHeld`.
  * **Shared Focus Pool:** Enforces a party-wide [`StateConstraint::FieldLteField`](file:///Users/ember/dev/breadstuffs/cell/src/lib.rs) budget across Mage and Healer.
  * **Collective Forks:** Critical path choices open a [`PartyFork`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs) resolved via [`collective_choice`](file:///Users/ember/dev/breadstuffs/collective-choice/src/lib.rs) quorum certificates.
  * **Loot Distribution:** [`Party::split_loot`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs) writes committed shares into `WriteOnce` cell slots.

#### 5. `dreggnet-council` — Collective Governance Offering
- **Location:** [`dreggnet-council/src/lib.rs:1-50`](file:///Users/ember/dev/breadstuffs/dreggnet-council/src/lib.rs#L1-L50)
- **Commit:** [`ed78ed52d`](file:///Users/ember/dev/breadstuffs) (2026-07-12)
- **Mechanical Guarantee:** Extends the [`Offering`](file:///Users/ember/dev/breadstuffs/dreggnet-offerings/src/lib.rs) trait to governance:
  * `propose`: opens a poll on `collective_choice::VoteEngine`.
  * `vote`: single-use `WriteOnce(VOTE)` ballot signed by custody key; double voting fails closed.
  * `enact`: checks the polis affine quorum predicate $M \cdot \text{RESOLVED} - \sum \text{TALLY} \le 0$. Below quorum, `enact` is refused and leaves state unchanged.

#### 6. `dreggnet-companion` — Fused Assets & Progression Cells
- **Location:** [`dreggnet-companion/src/lib.rs:1-55`](file:///Users/ember/dev/breadstuffs/dreggnet-companion/src/lib.rs#L1-L55)
- **Commit:** [`928c0eb12`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Fuses an owned, tradeable [`dreggnet_asset`](file:///Users/ember/dev/breadstuffs/dreggnet-asset/src/lib.rs) note (hatched from a provably fair [`procgen_dregg::verified_stream`](file:///Users/ember/dev/breadstuffs/procgen-dregg/src/lib.rs#L20) draw tail) with a progression cell running [`dungeon_on_dregg::progression::hero_story`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/lib.rs):
  * **Multicell Predicate:** A companion run buff is admitted if and only if the companion cell's finalized root matches an [`ObservedFieldEquals`](file:///Users/ember/dev/breadstuffs/cell/src/lib.rs) state constraint at `level >= N`.
  * **Permadeath Stakes:** The companion's `dead` slot is `WriteOnce`-final and un-undoable.

#### 7. `dreggnet-quest` — Gated Committed Quest Cells
- **Location:** [`dreggnet-quest/src/lib.rs:1-55`](file:///Users/ember/dev/breadstuffs/dreggnet-quest/src/lib.rs#L1-L55)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Replaces client-side counter tallies with kernel-enforced `WriteOnce` step-flags and [`BoundedBy(step_2 <- step_1)`](file:///Users/ember/dev/breadstuffs/cell/src/lib.rs) step-order constraints. Quest turn-in gates reward granting behind a [`StateConstraint::FieldGte`](file:///Users/ember/dev/breadstuffs/cell/src/lib.rs) on total steps cleared.

#### 8. `dreggnet-craft` — The Provably-Fair Deflationary Sink
- **Location:** [`dreggnet-craft/src/lib.rs:1-50`](file:///Users/ember/dev/breadstuffs/dreggnet-craft/src/lib.rs#L1-L50)
- **Commit:** [`ec9104378`](file:///Users/ember/dev/breadstuffs) (2026-07-15)
- **Mechanical Guarantee:** The economy's essential deflationary sink. Consumes a typed multiset of owned materials via owner-gated burns ([`AssetWorld::revoke`](file:///Users/ember/dev/breadstuffs/dreggnet-asset/src/lib.rs)). Rolls two provably-fair draws over committed [`RecipeBook`](file:///Users/ember/dev/breadstuffs/dreggnet-craft/src/lib.rs) weights using a craft seed derived from beacon randomness, recipe ID, and sorted input asset IDs.

#### 9. `dreggnet-cheevo` — ISA-Enforced Soulbound Achievements
- **Location:** [`dreggnet-cheevo/src/lib.rs:1-50`](file:///Users/ember/dev/breadstuffs/dreggnet-cheevo/src/lib.rs#L1-L50)
- **Commit:** [`ec9104378`](file:///Users/ember/dev/breadstuffs) (2026-07-15)
- **Mechanical Guarantee:** [`CheevoLedger::earn`](file:///Users/ember/dev/breadstuffs/dreggnet-cheevo/src/lib.rs) re-executes playthroughs through `ugc_dregg::verify_completion`, testing predicates (depth reached, zero-death clears, turn ceilings) over committed state vectors. Mints an asset with field `soulbound = 1`. The asset layer transfer instruction gates on `FieldEquals(soulbound, 0)`; transfer attempts are refused by the hardware-level executor ISA, preventing account laundering.

#### 10. `dreggnet-trade` — Atomic Trustless Swaps
- **Location:** [`dreggnet-trade/src/lib.rs:1-50`](file:///Users/ember/dev/breadstuffs/dreggnet-trade/src/lib.rs#L1-L50)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Binds asset transfers to [`starbridge-escrow-market`](file:///Users/ember/dev/breadstuffs/starbridge-apps/escrow-market/src/lib.rs) sealed escrow. Supports asset $\leftrightarrow$ asset and asset $\leftrightarrow$ $DREGG value. Settle executes both legs atomically; missing legs can be reclaimed via timeout, eliminating counterparty risk.

#### 11. `dreggnet-faction` — Gated Reputation State
- **Location:** [`dreggnet-faction/src/lib.rs:1-50`](file:///Users/ember/dev/breadstuffs/dreggnet-faction/src/lib.rs#L1-L50)
- **Commit:** [`45ef8a7d2`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Models faction standing ("The Feud at the Ashenmoor Gate": Embers vs. Tide) as committed cell slots. Reputation slots are [`Monotonic`](file:///Users/ember/dev/breadstuffs/cell/src/lib.rs); pledging loyalty to one faction decrements the opposing faction's ceiling slot (`embers_ceiling`). Betrayal flags are `WriteOnce` and seal faction content permanently.

#### 12. `dreggnet-gear` — Cross-Cell Owned Equipment
- **Location:** [`dreggnet-gear/src/lib.rs:1-45`](file:///Users/ember/dev/breadstuffs/dreggnet-gear/src/lib.rs#L1-L45)
- **Commit:** [`928c0eb12`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Equipping an item verifies ownership across cells via `ObservedFieldEquals` into a finalized asset note. Connects class-locked talents directly to the previously dormant [`spells.rs`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/lib.rs) spellbook (Mage $\ne$ Warrior). Talents cost death-earned echoes, strictly rejecting pay-to-win.

#### 13. `dreggnet-adventure` — Native Descent Offering Integration
- **Location:** [`dreggnet-adventure/src/lib.rs:1-40`](file:///Users/ember/dev/breadstuffs/dreggnet-adventure/src/lib.rs#L1-L40)
- **Commit:** [`4696e6950`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Hosts [`NativeDescentOffering`](file:///Users/ember/dev/breadstuffs/dreggnet-offerings/src/lib.rs) emitting Lean transition programs (`PROGRAM_JSON`). Replays runs through a fresh executor before progression accepts them via [`NativeDescentRun`](file:///Users/ember/dev/breadstuffs/dreggnet-adventure/src/lib.rs).

#### 14. `dreggnet-verified-completion` — Universal Completion Interface
- **Location:** [`dreggnet-verified-completion/src/lib.rs:1-40`](file:///Users/ember/dev/breadstuffs/dreggnet-verified-completion/src/lib.rs#L1-L40)
- **Mechanical Guarantee:** Boundary struct providing immutable run identity:
```rust
pub struct VerifiedCompletion {
    program_id: [u8; 32],
    world_root: [u8; 32],
    completion_root: [u8; 32],
    actor: String,
    turns: usize,
    metrics: BTreeMap<String, Vec<u64>>,
}
```

#### 15. `dreggnet-surfaces` — The DO-ONCE ViewNode Frontend
- **Location:** [`dreggnet-surfaces/src/lib.rs:1-60`](file:///Users/ember/dev/breadstuffs/dreggnet-surfaces/src/lib.rs#L1-L60)
- **Commit:** [`1ba6a4a1e`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Writing `Offering::render -> ViewNode` once lights up native cockpit, Web, Discord bot, and Telegram Mini Apps. Surfaces include `TradeOffering`, `InventoryOffering`, `CheevoShowcase`, `GuildPage`, and `CraftOffering`.

#### 16. `dreggnet-sprite` — In-House Deterministic SVG Generator
- **Location:** [`dreggnet-sprite/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-sprite/src/lib.rs)
- **Commit:** [`1ba6a4a1e`](file:///Users/ember/dev/breadstuffs) (2026-07-14)
- **Mechanical Guarantee:** Pure deterministic asset-to-SVG procedural generator seeded by content hashes, ensuring zero external asset hosting dependencies.

#### 17. `dreggnet-offerings` — Offering Lifecycle & Signed Ladder
- **Location:** [`dreggnet-offerings/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-offerings/src/lib.rs)
- **Commits:** [`6fa643d05`](file:///Users/ember/dev/breadstuffs), [`295b7f73d`](file:///Users/ember/dev/breadstuffs) (2026-07-16)
- **Mechanical Guarantee:** Implements `SessionPolicy` (LRU, TTL, rate limits) in `OfferingHost`. Introduces `Attribution{Signed, Asserted}` making trust visible, and persists signed-counter floors across service restarts to prevent replay attacks.

#### 18. `dreggnet-game-board` — STARK Recursive Multi-Round Test Harness
- **Location:** [`dreggnet-game-board/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-game-board/src/lib.rs)
- **Commit:** [`bd0d609c79`](file:///Users/ember/dev/breadstuffs) (2026-07-25)
- **Mechanical Guarantee:** Houses the capstone STARK folding tests (`tests/multi_round_fold.rs:1042`), verifying full multi-round conflict board games in 1663 seconds of recursive proving.

#### 19. `dreggnet-asset` — The Canonical Verifiable Asset Layer
- **Location:** [`dreggnet-asset/src/lib.rs:1-35`](file:///Users/ember/dev/breadstuffs/dreggnet-asset/src/lib.rs#L1-L35)
- **Mechanical Guarantee:** Implements a sovereign UTXO-style note lineage (`v0 -> v1 -> v2`) where each version is a cell authorized by its holder's Ed25519 birth key. Authority genuinely moves to successor cells rather than mutating in place. `spent := 1`, `prev = note_digest(v_i)`, and `asset_id` is carried unchanged via `WriteOnce`.

#### 20. `dreggnet-market` — Sealed-Bid Batch Cleared Market Offering
- **Location:** [`dreggnet-market/src/lib.rs:1-35`](file:///Users/ember/dev/breadstuffs/dreggnet-market/src/lib.rs#L1-L35)
- **Mechanical Guarantee:** Offering #commerce. Wraps the sealed-bid auction substrate:
  * `LIST`: Spawns an auction cell via `CreateCellFromFactory` with `StrictMonotonic(PHASE)` and `WriteOnce` commit boards.
  * `BID`: Sealed digest `BLAKE3(bidder || value || nonce)` committed on-chain; double-bidding is rejected by `WriteOnce`.
  * `SETTLE`: Verifies ring settlement ([`settle_ring_verified`]) enforcing per-asset conservation $\sum \delta = 0$.

#### 21. `dreggnet-compute` — Metered Compute Job Exchange Offering
- **Location:** [`dreggnet-compute/src/lib.rs:1-35`](file:///Users/ember/dev/breadstuffs/dreggnet-compute/src/lib.rs#L1-L35)
- **Mechanical Guarantee:** Offering #compute over `starbridge_compute_exchange`. Requesters post jobs with `WriteOnce(BUDGET)`. Workers claim jobs with price $\le$ budget via `FieldLteField(BID <= BUDGET)`. Settlement releases payment to the worker (`PAID := claim`, `REFUNDED := budget - claim`).

#### 22. `dreggnet-discord-identity` — Deterministic Custodial Seed Derivation
- **Location:** [`dreggnet-discord-identity/src/lib.rs:1-30`](file:///Users/ember/dev/breadstuffs/dreggnet-discord-identity/src/lib.rs#L1-L30)
- **Mechanical Guarantee:** Single source of truth for Discord identity derivation:
```text
seed = BLAKE3_derive_key("dregg-discord-bot-v1", bot_secret || discord_user_id_le)
```
Used identically in `discord-bot` and `dreggnet-web` Activity (`/da`), preventing user identity drift across web and chat surfaces.

#### 23. `dreggnet-hermes` — Hosted Confined Agent Offering
- **Location:** [`dreggnet-hermes/src/lib.rs:1-30`](file:///Users/ember/dev/breadstuffs/dreggnet-hermes/src/lib.rs#L1-L30)
- **Mechanical Guarantee:** Offering #1. Wraps an `AgentRuntime` with root tokens derived from session seeds. Tool calls pass through `ToolGateway` checking `ToolGrant` rate limits and `Charge` value budgets; over-mandate proposals are refused fail-closed by the executor.

#### 24. `dreggnet-grain` — Sandstorm-Style Sandboxed App Session
- **Location:** [`dreggnet-grain/src/lib.rs:1-30`](file:///Users/ember/dev/breadstuffs/dreggnet-grain/src/lib.rs#L1-L30)
- **Mechanical Guarantee:** Offering #2. Admits grain workers via `grain_turn::ToolGatewayMinter` under `ToolGrant { rate_limit: budget }`. Turn transitions advance `calls_made` counters; when exhausted, the `delegAdmit` rate leg fails and refuses further execution.

#### 25. `dreggnet-names` — Governed Sovereign Namespace Offering
- **Location:** [`dreggnet-names/src/lib.rs:1-30`](file:///Users/ember/dev/breadstuffs/dreggnet-names/src/lib.rs#L1-L30)
- **Mechanical Guarantee:** Offering over `starbridge_nameservice`. Maps strings to sovereign cells with `WriteOnce(NAME_HASH)` (first-claim tooth), `Monotonic(EXPIRY)`, `WriteOnce(REVOKED)`, and F1..F7 owner-authorization predicates.

#### 26. `dreggnet-doc` — Collaborative Multi-Editor Document Offering
- **Location:** [`dreggnet-doc/src/lib.rs:1-30`](file:///Users/ember/dev/breadstuffs/dreggnet-doc/src/lib.rs#L1-L30)
- **Mechanical Guarantee:** Collaborative productivity offering. Edits execute as verified turns via `MultiEditorDoc::edit`, landing receipts on per-agent chains. Edits without edit capabilities fail with `CapabilityNotHeld`; antichain clashes are rejected by conflict semantics.

#### 27. `dreggnet-tournament` — Single-Elimination Verifiable Brackets
- **Location:** [`dreggnet-tournament/src/lib.rs:1-35`](file:///Users/ember/dev/breadstuffs/dreggnet-tournament/src/lib.rs#L1-L35)
- **Mechanical Guarantee:** Single-elimination tournament bracket over $N$ competitors. Each round runs on a fresh, beacon-seeded universe; competitors advance strictly upon submitting a run verified by `ugc_dregg::verify_completion` or `verify_proof_completion`.

#### 28. `dreggnet-audit`, `dreggnet-catalog`, `dreggnet-web`, `dreggnet-telegram`, `dreggnet-wechat`, `dreggnet-prove-service`
- **Audit & Catalog:** Maintains verification descriptor sets and schema registries.
- **Transports & Gateways:** Provides Axum web servers, Telegram Mini App HMAC gateways, WeChat endpoints, and remote STARK proof aggregation pipelines.

---

### 1.3 Verified Game Engines in `breadstuffs`

#### 1. `dungeon-on-dregg` and the `.dungeon` Biconditional Compiler
Landing in commits [`c338e1e2a`](file:///Users/ember/dev/breadstuffs) and [`1dd8a566b`](file:///Users/ember/dev/breadstuffs), [`dungeon-on-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/lib.rs#L1-L50) mapped dungeon crawling directly to an `EmbeddedExecutor` cell:
- Cell slot 0 is [`PASSAGE_SLOT`](file:///Users/ember/dev/breadstuffs/spween-dregg/src/lib.rs), serving as the player's program counter. Slot 1 tracks key items, slot 2 depth, slot 3 gold.
- In [`dungeon-on-dregg/src/dsl/`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/dsl/) (`parse.rs`, `validate.rs`, `ir.rs`, `compile.rs`), Ember created the `.dungeon` text format documented in [`docs/AUTHORING-DUNGEONS.md`](file:///Users/ember/dev/breadstuffs/docs/AUTHORING-DUNGEONS.md#L1-L100).
- **Biconditional Translation Validation:** In [`dungeon-on-dregg/src/dsl/compile.rs:1-60`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/dsl/compile.rs#L1-L60), `compile_world` lowers a parsed `GameWorld` onto `spween::Scene`, lowers through `compile_scene`, and verifies against `check_lowering`: any dropped gate is flagged `MISSING`, and any injected gate is flagged `PHANTOM`.
- **The Spend Counter Pattern:** Exclusion rules (`oath`, `once`) enforce that actions can only be taken once by checking that a counter is `<= 0` in pre-state and bumping it `+= 1`, which lowers to a post-state `FieldLte { value: 1 }`. A second attempt produces a post-state of 2 and triggers an executor `Refused` outcome.

```rust
pub fn validate(world: &GameWorld) -> Vec<Issue> {
    check(world, None).into_iter().map(|(_, i)| i).collect()
}
```

#### 2. `attested-dm` and `dregg-narrator`: "Prose is not power"
As recorded in [`GOAL-COLLECTIVE-FICTION-DEMO.md:55-156`](file:///Users/ember/dev/breadstuffs/GOAL-COLLECTIVE-FICTION-DEMO.md#L55-L156):
- Ember identified the fundamental flaw in naive AI game mastering: lexical prompt-injection filters over natural language are futile because natural language lacks a metasyntax.
- **The Core Architecture:**
  1. **Input Integrity via Guarded Templates:** In `metatheory/Dregg2/Crypto/HandlebarsGuarded.lean`, holes carry explicit regular expression guards over `Dregg2.Exec.Value`:
```lean
inductive GSeg where
  | lit  (text : List Value)
  | hole (id : Nat) (guard : PredRE)

structure GuardedTemplate where
  segments : List GSeg

def guardedSafe (T : GuardedTemplate) (d : Nat → List Value) : Prop :=
  ∀ id g, GSeg.hole id g ∈ T.segments → derives (d id) g = true

theorem guarded_render_mem_language (T : GuardedTemplate) (d : Nat → List Value)
    (h : guardedSafe T d) :
    render T d ∈ (guardedToGrammar T).language :=
  body_gLang d T.segments h
```
  2. **Output Capability Gate:** The LLM's natural language output is parsed through a strict JSON grammar into a closed, typed [`WorldEffect`](file:///Users/ember/dev/breadstuffs/attested-dm/src/lib.rs#L715) enum:
```rust
#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum WorldEffect {
    AdvanceScene(String),
    SetFlag(String, i64),
    GrantItem(String),
    ConsumeItem(String),
    Batch(Vec<WorldEffect>),
}
```
  3. **Capability Confinement:** [`DmCaps::authorize`](file:///Users/ember/dev/breadstuffs/attested-dm/src/lib.rs#L1120) checks the effect against world rules. When a jailbroken Gemma 2 / Claude Haiku narrates granting the player the "Crown of Eternity", `DmCaps` refuses `OverCap`; the turn is aborted, no receipt is emitted, and the ledger state remains completely unchanged:
```rust
pub struct DmCaps {
    pub may_advance_scene: bool,
    pub may_set_flags: bool,
    pub grantable_items: BTreeSet<String>,
}
```
  4. **Prev-Linked Hash Chain:** The transaction log uses BLAKE3 domain-separated receipt hashes:
```rust
chain_receipt_id = BLAKE3(domain || seq || prev || narration || effect || attestation_commitment)
```
  5. **Persisted Spend Ceiling:** In [`narrator/src/lib.rs`](file:///Users/ember/dev/breadstuffs/narrator/src/lib.rs#L1-L45), hosted model calls (AWS Bedrock `us.anthropic.claude-haiku-4-5-20251001-v1:0` and `us.amazon.nova-2-lite-v1:0`) run behind [`BudgetLedger`](file:///Users/ember/dev/breadstuffs/narrator/src/ledger.rs), enforcing a fail-closed hard $20 budget with atomic file locks and pre-flight credit reservation.

#### 3. `mud-dregg`: Multiplayer Branch-Stitch
Defined in [`mud-dregg/src/lib.rs:1-45`](file:///Users/ember/dev/breadstuffs/mud-dregg/src/lib.rs#L1-L45) and [`mud-dregg/src/dungeon.rs:37-50`](file:///Users/ember/dev/breadstuffs/mud-dregg/src/dungeon.rs#L37-L50) (commit [`6f3309911`](file:///Users/ember/dev/breadstuffs) on 2026-07-06):
```rust
pub enum Command {
    Go { room: CellId },
    Take { entity: CellId },
    Say { room: CellId, glyph: FieldElement },
    Force { target: CellId, value: FieldElement },
}
```
- Multiplayer worlds operate as a distributed time-travel lattice $(E, \le, \#)$.
- Players fork world cells, explore timelines privately, and merge back through [`starbridge_v2::branch_stitch_session::BranchStitchSession`](file:///Users/ember/dev/breadstuffs/starbridge-v2/src/lib.rs).
- Disjoint edits merge automatically; conflicting writes to the same entity (e.g., two players issuing `take` on the same sword) trigger a verified $\#$-conflict refusal under the axiom-clean Lean theorem `Metatheory.SettlementSoundness.settlement_soundness`, eliminating last-writer-wins silent corruption.

#### 4. `procgen-dregg` & `ugc-dregg`: Verifiable Generations and Fair Leaderboards
- [`procgen-dregg/src/lib.rs:1-100`](file:///Users/ember/dev/breadstuffs/procgen-dregg/src/lib.rs#L1-L100) folds committed seeds into a [`dregg_dice::RandomnessRequest`](file:///Users/ember/dev/breadstuffs/dice/src/lib.rs), streaming reject-free, unbiased values via [`DrawStream::draw_bounded`](file:///Users/ember/dev/breadstuffs/procgen-dregg/src/lib.rs) across `MIN_ROOMS = 4` to 7 rooms with max degree $\le 6$. Any verifier re-generates byte-identical `.dungeon` files.
- [`ugc-dregg/src/lib.rs:1-100`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs#L1-L100) maintains a content-addressed registry keyed by [`UniverseId`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs) (semantics) alongside IPFS CIDs (wire bytes).
- Supports both $O(N)$ re-execution verification via [`verify_completion`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs) and $O(1)$ succinct STARK verification via [`ProofCompletion`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs), verifying a `WholeChainProof` without storing or revealing moves.

#### 5. `dregg-automatafl`: Cellular Automaton Board Game at N=11
As documented in [`project-automatafl-verified-game.md:1-55`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-automatafl-verified-game.md#L1-L55):
- Simultaneous-move board game on an $11 \times 11$ grid.
- The handwritten Rust AIR was completely deleted in commit `c8789758e8`.
- In `metatheory/Dregg2/Circuit/Emit/`:
  * `resolve_sat_imp_roundBoardN` (line 3768) proves move resolution.
  * `astep_sat_imp_automatonStepCfgN` (line 1090) proves automaton step transition.
  * In `AutomataflCommit.lean:198-202`, `pack_injective_modp` proves base-4 packed felts are injective modulo BabyBear prime $p$:
```lean
theorem pack_injective_modp (cell1 cell2 : Nat → ℤ) (fc : Nat)
    (h1 : ∀ i, i < 15 * fc → 0 ≤ cell1 i ∧ cell1 i < 4)
    (h2 : ∀ i, i < 15 * fc → 0 ≤ cell2 i ∧ cell2 i < 4)
    (heq : ∀ j, j < fc → packCell cell1 j % BABYBEAR_P = packCell cell2 j % BABYBEAR_P) :
    ∀ i, i < 15 * fc → cell1 i = cell2 i
```
  * In `AutomataflTurnCapstone.lean:284`, `turn_sat_imp_roundStep_pi` joins resolution and step transitions across this crypto-free seam.
  * The M0–M7 multi-round conflict braid `braid_sat_imp_runTurn` (`AutomataflBraidFold.lean:483`) was confirmed in commit `bd0d609c79`, executing a complete 2-round conflict turn into a single STARK proof in 1663 seconds of real folding.

#### 6. `dregg-multiway-tug`: ZK Hidden Hand
Defined in [`dregg-multiway-tug/src/lib.rs:1-45`](file:///Users/ember/dev/breadstuffs/dregg-multiway-tug/src/lib.rs#L1-L45) and [`dregg-multiway-tug/src/state.rs:1-60`](file:///Users/ember/dev/breadstuffs/dregg-multiway-tug/src/state.rs#L1-L60):
- Re-themes Hanamikoji (2 players, 7 guilds with influence `[2,2,2,3,3,4,5]`, 21 total cards).
- 21-card conservation: `SumEquals` over eight card-zone counters $== 21$ on every post-state.
- Action flags: `HeapAtom::WriteOnce` on `(player, action)` keys.
- Monotone scores: `HeapAtom::Monotonic` on per-guild placements.
- Terminal rule: `roundWinner` with 9 distinct precedence clauses partitioned into dedicated transition cases.
- Phase 2 zk HIDDEN HAND: cards are committed into a Poseidon2 Merkle tree. A player plays a card by proving `Witnessed{MerkleMembership}` in zero knowledge without revealing card identity.

#### 7. `poa` (Path of Angels): The Sentyr Khovokhi Platform
As recorded in [`GOAL-PATH-OF-ANGELS-EXCELLENCE.md:1-115`](file:///Users/ember/dev/breadstuffs/GOAL-PATH-OF-ANGELS-EXCELLENCE.md#L1-L115) and [`project-path-of-angels-platform.md:1-76`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-path-of-angels-platform.md#L1-L76):
- Platform aboard the Khovokhi (Sentyr's narrative universe), spanning 84 Lean modules and 60,700 lines under `metatheory/Dregg2/Games/PathOfAngels/` with 0 `sorry` and 1,840 verified theorems.
- Three verified games: Signal Triangulation (3 bands $\times$ 6 values = 216 codes, 5 attempts), Relay Repair, Salvage Lock.
- Six station organs: Crew, Records, Bazaar, Choir, Missions, Galley.
- Supported by [`poa-curator`](file:///Users/ember/dev/breadstuffs/poa-curator/README.md#L1-L60) for content manifest epoch signing, [`poa-web`](file:///Users/ember/dev/breadstuffs/poa-web/README.md) for terminal rendering, and [`poa-solana-gate`](file:///Users/ember/dev/breadstuffs/poa-solana-gate/README.md#L1-L78) for SPL Token-2022 holding admission (`XkeTXo1125vz5H9svJpGiw4JvLbN8VmMu9cmMvspump`).
- **The Five Weld Points:**
  * W1: Precommitted beacon seed (`RandomnessBeacon.lean` FFI export).
  * W2: Judged transition circuit effect carve-out (moving beyond blind BLAKE3 topic hashing).
  * W3: Cell state 8-field AIR ceiling expansion (`circuit/src/effect_vm/columns.rs:251`).
  * W4: Automated game-design solver gate (`scripts/poa-design-gate.py` §12.3: checking non-dominated verbs and strategic forks).
  * W5: Curator authority as an attenuable Dregg capability.

#### 8. `CROWD-STREAM-ENGINE-DESIGN.md`: Verifiable Live Streaming
Defined in [`docs/CROWD-STREAM-ENGINE-DESIGN.md:1-100`](file:///Users/ember/dev/breadstuffs/docs/CROWD-STREAM-ENGINE-DESIGN.md#L1-L100):
- Feeds live stream events (YouTube Super Chats, Twitch EventSub/bits) into [`CollectiveRound`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/collective.rs#L513), weighting ballots by financial contribution.
- Quorum-certified winners fold into one `TurnReceipt`, pushed via SSE (`OverlayState` in `dreggnet-web`) to transparent OBS browser overlays for broadcast.

---

## 2. The Great Diaspora — How parts spread into other projects

When `breadstuffs` began its transition in late summer 2026, the codebase did not die; its core concepts, modules, and architectures colonized the surrounding repositories:

```
                                  THE BREADSTUFFS GENESIS
                                             │
      ┌───────────────────┬──────────────────┴────────────────┬───────────────────┐
      ▼                   ▼                                   ▼                   ▼
~/dev/path-of-angels   ~/dev/automatafl                ~/dev/delvetalk2           ~/dev/allgame & dclutch
(cba0e03c90c5 cut)     (zero-twin Lean 4)              (Actor World & obend)      (Residents & Solana DEX)
 ├─ metatheory/         ├─ pure Lean 4 core             ├─ world/kinds/            ├─ claude_resident
 ├─ poa-curator/        ├─ lock-free lobby                 (room, door, lantern,   ├─ kimi_resident (Yuè)
 ├─ poa-web/            ├─ fog-of-war telemetry            inhabitant, errand,     ├─ glm_resident (Kestrel)
 └─ poa/artifacts/      └─ automatafl.fg-goose             bond, parlour, cistern) ├─ dclutch SimLife3
                                                        ├─ world/objects/*.obend   └─ Token-2022 holding gate
```

### 2.1 `path-of-angels`: The Collaboration Extraction
On 2026-08-04, at upstream `breadstuffs` commit `cba0e03c90c5b701e4ad5dae6d6abfa7d5534130`, Ember cleanly carved out the partner boundary into `/Users/ember/dev/path-of-angels`.
As detailed in [`path-of-angels/SOURCE-MAP.md:1-58`](file:///Users/ember/dev/path-of-angels/SOURCE-MAP.md#L1-L58), the repo preserved:
- `metatheory/Dregg2/Games/PathOfAngels/` (Lean game semantics, replay, canon)
- `poa-web/` (browser terminal and signed artifact loaders)
- `poa-curator/` (epoch signing and review projection)
- `poa/artifacts/poag1/` (curator-signed manifests and game descriptors)
- Exclusion of all internal node execution, Solana bridges, and secrets.

On 2026-10-21, Ember issued an explicit historical correction in [`project-path-of-angels-platform.md:11`](file:///Users/ember/.claude/projects/-Users-ember-dev-breadstuffs/memory/project-path-of-angels-platform.md#L11):
> *"⚠ CORRECTED 2026-10-21 (Ember): PoA is NOT a real or running thing; 'breadstuffs is the PoA main line' is extremely wrong and out of date. breadstuffs is where the whole system we built lives; mini and nano are side explorations; breadstuffs waits to be resumed or composted into the next robigalia. Read the rest of this file as history."*

### 2.2 `automatafl`: The Zero-Twin Lean 4 Extraction
Automatafl migrated out of `breadstuffs` into `/Users/ember/dev/automatafl`. As evidenced by git log [`97db66a`](file:///Users/ember/dev/automatafl), `c6652a5`, and `253bafa`, it completely realized Ember's architectural vision:
- The dual-implementation "twin" (where rules were written in Rust and mirrored in Lean) was permanently abandoned.
- The game runs today at `automatafl.fg-goose.online` as a pure Lean 4 verified core with a lightweight Rust telemetry and lock-free lobby harness.

### 2.3 `delvetalk` and `delvetalk2`: The World/Kinds Diaspora into Objective Bend
In October 2026, the RPG and MUD mechanisms from `breadstuffs` met Ember's work on Bend (`obend`).
- **The DelveTalk v1 Failure:** In early October 2026, an autonomous Codex run generated 83 commits and 125,146 lines in `/Users/ember/dev/delvetalk`. Ember termed this initial sprawl "horseshit" and "chug" due to unchecked orchestration and refusal to subtract (`-Users-ember-dev-delvetalk/memory/ember-working-style.md:21`).
- **The `delvetalk2` Rebirth:** Founded on 2026-10-09, `/Users/ember/dev/delvetalk2` restructured the world into clean, composable primitives under `/Users/ember/dev/delvetalk2/world/`:

#### The 22 Kinds in `world/kinds/`
The files in `/Users/ember/dev/delvetalk2/world/kinds/` reflect the exact ontological concepts developed across `breadstuffs`:
1. `room.kind`:
```yaml
of: record
form: <<END
name: text 1..64
spween: text 0..16384
END
head: {name}
voice: dusk-light and stone dust; a place where nobody has decided yet; there is no rush
about: a place walked by choices; prose alone is a scene
body: room
```
Directly incorporates Spween text passages (`text 0..16384`) from `spween-dregg`.
2. `errand.kind`:
```yaml
of: record
form: <<END
asks: text 1..200
on: object 1..128
done: text 1..400
pays: text 1..400
END
body: errand
```
Direct descendant of `dreggnet-quest` ("The Loremaster's Errand"), tracking request conditions, settlement targets, and payouts.
3. `bond.kind`:
```yaml
of: record
form: <<END
parties: text 1..400
terms: text 1..400
amends: object 0..128
law: text 0..4096
END
text: law signer "a party signs only for themselves": changed(new.marks.who) by request.subject
body: bond
```
Direct descendant of `dreggnet-companion` ("an owned asset fused with a leveling cell: a provable bond") and `starbridge-apps/escrow-market`.
4. `station.kind`:
```yaml
of: kind/room
voice: fluorescent and patient; the same hour always; open to Anyone Who Arrives
body: station
```
Inherits the station concept from `poa`, linking `world/bodies/station.spween` stitched from community replies.
5. `lantern.kind`:
```yaml
of: record
form: <<END
name: text 1..64
door: object 1..128
END
body: lantern
```
Direct descendant of `dungeon-on-dregg`'s lantern item slot gating dark exits.
6. `parlour.kind`:
```yaml
of: kind/station
body: parlour
```
Direct descendant of `dreggnet-tavern`'s parlour hub, linking `world/bodies/parlour.spween` and ouija planchette board interactions.
7. `inhabitant.kind`:
```yaml
of: record
form: <<END
name: text 1..64
haunts: object 1..128
tide: object 1..128
END
body: inhabitant
```
Direct descendant of `dungeon-on-dregg/src/mud.rs` inhabitant cells.
8–22. `bee.kind`, `bell.kind`, `cistern.kind`, `counter.kind`, `dj.kind`, `door.kind`, `front.kind`, `garden.kind`, `hexboard.kind`, `planchette.kind`, `porch.kind`, `record.kind`, `register.kind`, `regular.kind`, `weather.kind`: Environmental, board, clock, and audit kinds.

#### The 9 Actors in `world/objects/*.obend`
The `.obend` actor programs in `/Users/ember/dev/delvetalk2/world/objects/` execute natively in Objective Bend:
1. `Policy.obend`:
```bend
# The interpretation policy as an ordinary object: the host sends prompt(...) to
# the configured model and returns the answer as a proposal, never as authority.
def hob() -> String:
  "Give the spell they meant, so the card can run it; the card and its law decide what is admitted, never you."
```
Directly embodies the `attested-dm` thesis: the model proposes, the object's law disposes.
2. `Tide.obend`:
```bend
# kimik3's tide: the town's one clock thing. It ticks itself, once every `gap` clock minutes:
# each tick is its own turn ... missed ticks are not made up ... a tick sooner than `gap`
# after the last is refused tooSoon, so a second chain dies at its first tick.
```
Implements `StrictMonotonic` turn pacing and deterministic world progression from `breadstuffs`.
3. `Library.obend`: Manages universe definitions, scene stacks, and completion verification records (`ugc-dregg`).
4. `Thing.obend`: Implements inventory items and asset notes (`dreggnet-asset`, `dreggnet-gear`).
5. `Workshop.obend`: Implements recipe books, input burning, and fair quality draws (`dreggnet-craft`).
6. `Avatar.obend`: Manages user identity, capabilities, and key bindings.
7. `Kind.obend`, `Mending.obend`, `Record.obend`: Base meta-object system, journal repair, and history logs.

### 2.4 `allgame`: Tulip Residents and Confined Minds
In `/Users/ember/dev/allgame`, the resident mind harness (`claude_resident`, `kimi_resident` for Yuè月 on `allgame-public`, `glm_resident` for Kestrel, `mother_mythos/`) directly adopted the hard lesson from `breadstuffs`'s `attested-dm`:
- Natural language cannot be constrained by prompt decoration or substring filters.
- Real agency requires strict capability confinement (`DmCaps::authorize`) and typed action channels where "prose is not power."

### 2.5 `dclutch`: Solana DEX and Creature Aquarium
In `/Users/ember/dev/dclutch`, the financial and creature systems extracted from `breadstuffs` found a production trading home:
- The Solana Token-2022 holding admission gate developed in [`poa-solana-gate`](file:///Users/ember/dev/breadstuffs/poa-solana-gate/README.md) and [`dregg-bridge::solana_holdings`](file:///Users/ember/dev/breadstuffs/bridge/src/lib.rs).
- Atomic escrow settlement from [`dreggnet-trade`](file:///Users/ember/dev/breadstuffs/dreggnet-trade/src/lib.rs) and [`starbridge-escrow-market`](file:///Users/ember/dev/breadstuffs/starbridge-apps/escrow-market/src/lib.rs).
- The SimLife3 creature aquarium, persisting autonomous living entities over verifiable on-chain state.

---

## 3. What got dropped or parked — And how we take it back up now

When `breadstuffs` froze during the cutover to `minidregg`, dozens of fully tested, driven game and social mechanics were left stranded in the tree:

### 3.1 The Stranded Mechanics

1. **The 28 `dreggnet-*` Social and RPG Modules:**
   - Multi-party seated division of labor (`dreggnet-party`).
   - Cross-cell observed asset leveling (`dreggnet-companion`).
   - Hard ISA-level soulbound non-transferability (`dreggnet-cheevo`).
   - Two-draw deflationary crafting sink (`dreggnet-craft`).
   - Atomic escrow player trading (`dreggnet-trade`).
   - Monotonic faction reputation decay (`dreggnet-faction`).
   - Single-use passkey-voted council enactments (`dreggnet-council`).
   - Multi-patron live receipt-streamed taverns (`dreggnet-tavern`).
   - Escrow-custodied guild treasuries (`dreggnet-guild`).

2. **The `.dungeon` Text DSL and Biconditional Validator:**
   - Hand-authored text files with line-numbered, fail-closed validation (`dungeon-on-dregg/src/dsl/`).
   - Biconditional translation validation ensuring every game gate matches an executor constraint.

3. **Multiplayer Branch-Stitch Time-Travel:**
   - Private timeline exploration with verified lattice merge and `#`-conflict refusal (`mud-dregg`).

4. **ZK Hidden Hand and Proof Folding:**
   - Poseidon2 Merkle hand commitments proving legal play with zero knowledge (`dregg-multiway-tug`).
   - Match-as-single-proof STARK recursive folding (`game_turn_folds_and_lightclient_accepts`).

5. **Provably-Fair Procedural Generation:**
   - Reject-free draw streams derived from committed beacon seeds (`procgen-dregg`).

6. **Automated Game Design Solver Gate:**
   - `scripts/poa-design-gate.py` enforcing non-dominated verbs, strategic fork counts, and binding budgets before content can be committed.

### 3.2 Why Mini Stalled, and Why We Can Revive Them Now

In the 2026-09-30 bake-off between `breadstuffs` and `minidregg` ([`claudesplosion/bakeoff/VERDICT.md`](file:///Users/ember/dev/whatember/sources/strands/09-deos-minidregg-nanodregg-delvetalk-deep-dive.md#L37-L50)), both repositories revealed structural limitations:
- `breadstuffs` suffered from massive monorepo weight, 12 elephant crates, and linker collisions on Linux (mimalloc TLS in `libleanrt.a`).
- `minidregg` suffered from immediate-mode re-execution (write times scaled quadratically: 2.6s $\to$ 13.0s $\to$ 25.5s at 10/100/155 records) and concrete import rebuild cascades.

As Ember diagnosed on 2026-10-31 (`feedback-retained-mode.md`):
> *"this current generation of code generation models keeps writing re-execution … the whole thing would be incremental and efficient and held 'retained-mode'"*

The modern environment solves both failure modes:
1. **Retained-Mode Storage in `minidregg`:** Replaced immediate-mode replay with persistent incremental maps and replayed suffix caching (commit [`c4ecabe0f`](file:///Users/ember/dev/minidregg) on HEAD).
2. **Deterministic Parallel Actors in `obend`:** Objective Bend executes room graphs, inventory mutations, and combat ticks in massively parallel interaction nets without lock contention.
3. **Ontology Alignment in `delvetalk2`:** The `world/kinds/` directory is already shaped to host the 28 `dreggnet-*` crates.
4. **Resident Minds in `allgame`:** Real models (Claude, Yuè, Kestrel) provide narrative richness while `attested-dm`'s `DmCaps` ensures that prose never overrides state.

---

## 4. The Structured Revival Roadmap Table

| Subsystem / Mechanical Feature | Original Source in `breadstuffs` | Primary Guarantee & Signature | Parking Reason (Aug–Oct 2026) | Revival Target in New Stack | Re-activation Mechanism (How it comes alive) | Phase & Priority |
|---|---|---|---|---|---|---|
| **Saga Composition Engine** | [`dreggnet-saga/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-saga/src/lib.rs#L1-L65) (`a65b63f13`) | Object-identical `ugc_dregg::Completion` + `AssetId` handoff | Monorepo freeze; `breadstuffs` CI weight | `/Users/ember/dev/delvetalk2/world/objects/Library.obend` | Port `Completion` struct into an `.obend` interaction actor; wire directly into DelveTalk2 scene transitions | **Phase 1 (Immediate)** |
| **Seated Cooperative Party** | [`dreggnet-party/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-party/src/lib.rs#L1-L55) (`45ef8a7d2`) | Role-based capability enforcement; cross-cell `focus` pool (`FieldLteField`) | Excluded `discord-bot` workspace collision | `/Users/ember/dev/delvetalk2/world/kinds/inhabitant.kind` | Map party roles (Tank, Scout, Mage, Healer) to distinct capability tokens in DelveTalk2 agent sessions | **Phase 1 (Immediate)** |
| **Gated Quest Progress** | [`dreggnet-quest/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-quest/src/lib.rs#L1-L55) (`45ef8a7d2`) | `WriteOnce` step flags; `BoundedBy(step_2 <- step_1)` | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/kinds/errand.kind` | Lower errand preconditions into DelveTalk2 kind validators; enforce turn-in rewards via capability transfer | **Phase 1 (Immediate)** |
| **Soulbound Achievements** | [`dreggnet-cheevo/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-cheevo/src/lib.rs#L1-L50) (`ec9104378`) | Hardware ISA refusal: `FieldEquals(soulbound, 0)` on transfer | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/kinds/record.kind` | Re-derive achievement seals over completed DelveTalk2 run journals; mint un-transferable record objects | **Phase 2 (Near-Term)** |
| **Economic Forge & Sink** | [`dreggnet-craft/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-craft/src/lib.rs#L1-L50) (`ec9104378`) | 2-draw weighted CDF over committed `RecipeBook`; burns inputs | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/objects/Workshop.obend` | Wire `Workshop.obend` to consume multiset materials and draw quality tiers from beacon-seeded pseudo-random streams | **Phase 2 (Near-Term)** |
| **Atomic Trade Escrow** | [`dreggnet-trade/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-trade/src/lib.rs#L1-L50) (`45ef8a7d2`) | Sealed escrow atomic swap: asset $\leftrightarrow$ asset or asset $\leftrightarrow$ $DREGG | Stalled during `minidregg` bake-off | `/Users/ember/dev/dclutch/` & `starbridge-escrow-market` | Connect DelveTalk2 item trading directly to DClutch escrow markets on Solana | **Phase 2 (Near-Term)** |
| **Persistent Social Tavern** | [`dreggnet-tavern/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-tavern/src/lib.rs#L1-L55) (`45ef8a7d2`) | Shared board + private stall cells; live SSE receipt stream | Shift of focus to Tulip Zulip bots | `/Users/ember/dev/delvetalk2/world/kinds/parlour.kind` + `allgame` | Re-home tavern GM as a Tulip resident in `allgame`; stream live room receipts to Delvetown chat channels | **Phase 2 (Near-Term)** |
| **Escrow Guild Treasury** | [`dreggnet-guild/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-guild/src/lib.rs#L1-L60) (`45ef8a7d2`) | Shared room capability; depositor-only escrow reclaim | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/objects/Policy.obend` | Implement guild membership as capability sets in `Policy.obend`; custody group treasuries in DClutch | **Phase 2 (Near-Term)** |
| **Faction Standing & Decay** | [`dreggnet-faction/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-faction/src/lib.rs#L1-L50) (`45ef8a7d2`) | `Monotonic` reputation; rival ceiling drop; betrayal flags | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/objects/Tide.obend` | Drive reputation counters in DelveTalk2 NPCs; gate region entry on signed faction commitments | **Phase 2 (Near-Term)** |
| **Cross-Cell Equipment** | [`dreggnet-gear/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-gear/src/lib.rs#L1-L45) (`928c0eb12`) | `ObservedFieldEquals` multicell ownership; class-locked talents | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/objects/Thing.obend` | Equip items by referencing `Thing.obend` pointers; bind class-locked abilities in DelveTalk2 agent action tables | **Phase 2 (Near-Term)** |
| **Fused Leveling Companion** | [`dreggnet-companion/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-companion/src/lib.rs#L1-L55) (`928c0eb12`) | Asset note + multicell leveling cell (`ObservedFieldEquals`) | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/kinds/bond.kind` | Bind DelveTalk2 companions to DClutch creature assets; gate player buffs on companion level progression | **Phase 2 (Near-Term)** |
| **DO-ONCE ViewNode Frontend** | [`dreggnet-surfaces/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-surfaces/src/lib.rs#L1-L60) (`1ba6a4a1e`) | `Offering::render` $\to$ `deos_view::ViewNode` | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/site/` | Render DelveTalk2 kind/object states to `ViewNode` IR; pipe to Web, Discord, and Telegram Mini Apps | **Phase 3 (Expansion)** |
| **`.dungeon` Text DSL Compiler** | [`dungeon-on-dregg/src/dsl/`](file:///Users/ember/dev/breadstuffs/dungeon-on-dregg/src/dsl/) (`1dd8a566b`) | Biconditional translation validation: `MISSING` vs `PHANTOM` | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/kinds/room.kind` | Recompile `.dungeon` files directly into DelveTalk2 `room.kind` graph structures | **Phase 1 (Immediate)** |
| **Attested Dungeon Master** | [`attested-dm/src/lib.rs`](file:///Users/ember/dev/breadstuffs/attested-dm/src/lib.rs) & `GOAL-COLLECTIVE-FICTION-DEMO.md` | `slot_confinement` theorem (Lean) + `DmCaps::authorize` gate | Local Ollama setup too heavy for CI | `allgame` residents (`claude_resident`, `kimi_resident`) | Host resident DMs in Allgame; route narrative effects through typed DelveTalk2 command channels | **Phase 1 (Immediate)** |
| **Fail-Closed Spend Ceiling** | [`narrator/src/lib.rs`](file:///Users/ember/dev/breadstuffs/narrator/src/lib.rs#L1-L45) (`aa8847c80`) | Hard $20 `BudgetLedger` with pre-flight reservation & file locks | Stalled during `minidregg` bake-off | `allgame` LLM invocation gateway | Wrap all external Claude/Bedrock API calls in `allgame` with `BudgetLedger` fail-closed reservation | **Phase 1 (Immediate)** |
| **Multiplayer Branch-Stitch** | [`mud-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/mud-dregg/src/lib.rs#L1-L45) (`6f3309911`) | $(E, \le, \#)$ time-travel lattice; conflict refusal | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/` | Allow DelveTalk2 players to branch private world copies; reconcile state merges via settlement soundness | **Phase 3 (Expansion)** |
| **Provably-Fair Generation** | [`procgen-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/procgen-dregg/src/lib.rs#L1-L45) (`fd43cd6cd`) | Committed seed $\to$ `DrawStream::draw_bounded` $\to$ `.dungeon` | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/capsules/` | Seed daily dungeon worlds in DelveTalk2 using drand beacon entropy; verify byte-identical regeneration | **Phase 2 (Near-Term)** |
| **No-Cheat Leaderboards** | [`ugc-dregg/src/lib.rs`](file:///Users/ember/dev/breadstuffs/ugc-dregg/src/lib.rs#L1-L45) (`3b6776583`) | Re-execution of run transcripts against genesis world seeds | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/world/objects/Library.obend` | Rank DelveTalk2 player completions on `Library.obend` by fresh deterministic journal replay | **Phase 2 (Near-Term)** |
| **ZK Hidden Hand Play** | [`dregg-multiway-tug/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dregg-multiway-tug/src/lib.rs#L1-L45) | Poseidon2 Merkle hand + `Witnessed{MerkleMembership}` | Stalled during `minidregg` bake-off | `/Users/ember/dev/minidregg-wt/` | Integrate multiway-tug hidden-hand circuit into `minidregg` retained-mode prover | **Phase 3 (Expansion)** |
| **Path of Angels Mini-Games** | [`poa/`](file:///Users/ember/dev/breadstuffs/poa/) & `metatheory/.../PathOfAngels/` | 84 Lean modules; 1840 theorems; Signal, Relay, Salvage | 1-validator collapse; content-node drift | `~/dev/path-of-angels` + DelveTalk2 `station.kind` | Port Signal Triangulation, Relay Repair, and Salvage Lock to browser WASM over DelveTalk2 station rooms | **Phase 3 (Expansion)** |
| **Crowd-Stream Overlay Engine** | [`docs/CROWD-STREAM-ENGINE-DESIGN.md`](file:///Users/ember/dev/breadstuffs/docs/CROWD-STREAM-ENGINE-DESIGN.md#L1-L100) | Live YouTube/Twitch Super Chat $\to$ `CollectiveRound` $\to$ OBS SSE | Stalled during `minidregg` bake-off | DelveTalk2 web frontend + OBS overlay | Ingest YouTube/Twitch chats as weighted ballots into DelveTalk2 collective voting rounds | **Phase 3 (Expansion)** |
| **Game Design Solver Gate** | `scripts/poa-design-gate.py` (`e42d699b9`) | Exhaustive transition table search: non-dominated verbs, strategic forks | Stalled during `minidregg` bake-off | `whatember` CI / DelveTalk2 authoring harness | Run design gate script across all generated DelveTalk2 rooms and `.dungeon` files before release | **Phase 1 (Immediate)** |
| **Sealed-Bid Market** | [`dreggnet-market/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-market/src/lib.rs) (`45ef8a7d2`) | Factory auction cells; sealed bids $\text{BLAKE3}(b \Vert v \Vert n)$; $\sum \delta = 0$ | Stalled during `minidregg` bake-off | `/Users/ember/dev/dclutch/` | Re-home uniform-price sealed-bid auction cycles to DClutch on-chain order books | **Phase 2 (Near-Term)** |
| **Metered Compute Exchange** | [`dreggnet-compute/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-compute/src/lib.rs) (`45ef8a7d2`) | Escrowed job budgets; `FieldLteField(BID <= BUDGET)`; flashwell settle | Stalled during `minidregg` bake-off | `/Users/ember/dev/allgame/` | Use compute exchange to lease GPU/LLM inference time among Tulip residents | **Phase 3 (Expansion)** |
| **Discord Identity Derivation** | [`dreggnet-discord-identity/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-discord-identity/src/lib.rs) | `BLAKE3_derive_key("dregg-discord-bot-v1", bot_secret || uid)` | Excluded bot workspace | DelveTalk2 Discord bridge | Derive custodial Ed25519 player signers for DelveTalk2 Discord slash commands and activities | **Phase 1 (Immediate)** |
| **Confined Agent Offering** | [`dreggnet-hermes/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-hermes/src/lib.rs) (`45ef8a7d2`) | `AgentRuntime` with `ToolGrant` rate caps & `Charge` value budgets | Stalled during `minidregg` bake-off | `allgame` resident harnesses | Wrap resident agent tool execution in `ToolGateway` metered turns | **Phase 2 (Near-Term)** |
| **Sandboxed Grain Apps** | [`dreggnet-grain/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-grain/src/lib.rs) (`45ef8a7d2`) | Sandstorm app grains with `calls_made <= rate_limit` rate legs | Stalled during `minidregg` bake-off | `/Users/ember/dev/delvetalk2/capsules/` | Host interactive mini-apps inside DelveTalk2 rooms via capability-sandboxed grains | **Phase 3 (Expansion)** |
| **Governed Namespaces** | [`dreggnet-names/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-names/src/lib.rs) (`45ef8a7d2`) | Sovereign name cells; `WriteOnce(NAME_HASH)` first-claim tooth | Stalled during `minidregg` bake-off | DelveTalk2 identity layer | Resolve DelveTalk2 room and actor handles to verifiable on-chain sovereign name cells | **Phase 3 (Expansion)** |
| **Collaborative Documents** | [`dreggnet-doc/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-doc/src/lib.rs) (`45ef8a7d2`) | Multi-editor document turns; antichain conflict refusals | Stalled during `minidregg` bake-off | DelveTalk2 lore editor | Enable multi-user collaborative world/lore authoring inside DelveTalk2 | **Phase 3 (Expansion)** |
| **Tournament Brackets** | [`dreggnet-tournament/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-tournament/src/lib.rs) (`45ef8a7d2`) | Seeded elimination bracket; advancement gated strictly on verified win | Stalled during `minidregg` bake-off | DelveTalk2 competitive arcade | Run automated speedrun and high-score tournaments over DelveTalk2 daily dungeons | **Phase 3 (Expansion)** |
| **Deterministic Sprites** | [`dreggnet-sprite/src/lib.rs`](file:///Users/ember/dev/breadstuffs/dreggnet-sprite/src/lib.rs) (`1ba6a4a1e`) | Procedural seed-derived SVG generator for loot and characters | Stalled during `minidregg` bake-off | DelveTalk2 web frontend | Deterministically render item and avatar SVGs directly from content addresses in-browser | **Phase 1 (Immediate)** |
| **Solana Holding Admission** | [`poa-solana-gate/src/lib.rs`](file:///Users/ember/dev/breadstuffs/poa-solana-gate/src/lib.rs) (`7897c8eab`) | Token-2022 balance verification; one-use `HoldingCapability` nonces | Stalled during `minidregg` bake-off | `/Users/ember/dev/dclutch/` | Gate access to exclusive DelveTalk2 rooms and features by proving `$DREGG` holding via Solana RPC | **Phase 2 (Near-Term)** |
