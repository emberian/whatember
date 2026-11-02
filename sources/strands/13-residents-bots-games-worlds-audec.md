# Strand 13 — Resident Minds, Formal Comms, Reverse-Engineered Worlds & Audio Decompilation

> **Vertical:** `allgame` / `allgame-public` / Tulip (`tulip2`, `tulip.fg-goose.online`, `tulip.arke.me`) / `zwobot` / `qwobot` / `telme` / `mention-tracker` · `fn` + `fn2` · `don` · `automatafl` · `slipways-*` · game prototypes (`frisqueendom`, `friskingdom`, `booty-hunt`, `booty-haul`, `bw-exp0`, `bw-exp1`, `blackwing-v0`, `pinatatown`, `chaingang`, `neocadia`, `accordion-sim`, `tictacflicflacfloe`) · `audec` + `audec-ui-platform-probe`.
>
> **Compiled:** 2026-11-02 by a Claude Opus 5.5 archaeology lane, read-only over the repos, from git logs and trees, READMEs and design docs, and the per-project memory corpora under `~/.claude/projects/-Users-ember-dev-{allgame,fn,telme,don,audec,frisqueendom,friskingdom,booty-hunt,booty-haul}/memory/`, plus `~/dev/aidev/docs/synthesis/rest.md` and `~/dev/aidev/docs/projects.md`. Every number below was read from a file or a `git` command on 2026-11-02 unless it is attributed to a dated memory. Where the brief's figures differ from what the tree measures today, both are given.
>
> **Ownership note.** `orb.farm` (Max Bittker; 96 of 99 commits are his), `shattered-pixel-dungeon` (Evan Debenham, 8,392 of 8,402 commits), the upstream Zulip history inside `tulip2` (68,371 commits since 2012), `slipways-core` (Beetlewing's public script extract; ember added one commit, `a46d9b1` "solver rust") and `slipways-reveng` (a decompiled C# tree of a commercial game, not a git repo) are **third-party material that ember forked or studied**. They are listed as context, never claimed as ember's work. Nothing from `/Users/ember/hellas` is in scope.

---

## 0. The shape of the vertical in one diagram

```
                         ┌──────────────────────── SOCIAL SUBSTRATE ─────────────────────────┐
 2026-01-05 qwobot ──► 01-07 zwobot ──► 01-07 tulip.arke.me (Zulip fork: widgets, slash cmds,
 (Discord+llama.cpp)   (Zulip+llama.cpp)       puppets) ──► tulip2 / tulip.fg-goose.online (deployed)
                                                         │
                                  03-01 allgame "Tulip Residents"  ◄── tokeman (OAuth rotation)
                                  ├─ claude_resident (Opus, "Claude")      ~/claude_state  33,721 API calls
                                  ├─ kimi_resident → allgame-public profiles/yue  (Yuè月, Kimi K3/K3.1)
                                  ├─ glm_resident (Kestrel, glm-5.3[-flash] on Z.AI)
                                  ├─ sonnet_resident, gemma_resident.py, nemotron_resident.py (side harnesses)
                                  ├─ mother_mythos/ (Fable 5.1 as a Claude Code *channel* session, 10-02)
                                  └─ town_mirror/ (live SQLite of Delvetown's ATProto PDS, 10-12)
                                                         │  rat asks: "API endpoints for mail exchange for yue & tulip?"
                         ┌───────────────────────── FORMAL COMMS ───────────────────────────┐
                         │ 09-18 fn (ACL2 NNTP + BPv7) ─► 6.6.0 public node fn.fg-goose.online │
                         │   16,911 commits on HEAD · 1,440 ACL2 books / 652K lines · 74K host │
                         │ 10-28 fn2 (bottom-up rebuild: defmachine / defcolumns / Lean meta)  │
                         └──────────────────────────────────────────────────────────────────┘
 09-19 telme (Telegram/Discord/X DM snarf + guard) — the same "resident" idea pointed at ember's own inbox

                         ┌──────────────────────────── WORLDS ─────────────────────────────┐
 2015 automatafl (board game, w/ grissess) ─► 2020 Rust ─► 2025-10 logic/ ─► 2026-07 dregg STARK
      ─► 2026-11-01 zero-twin Lean 4 core, live at automatafl.fg-goose.online
 2025-12..2026-02 prototype run: pinatatown · neocadia · chaingang · Blackwing (bw-exp0/1, holdsmith)
      · tictacflicflacfloe · booty-hunt ─► friskingdom (Bevy) ─► frisqueendom (shipped, phone controller)
 2026-05 RIG/spindle (in allgame memory): Coriolis frisbee ─► RL/planning gym
 2026-08-08 Descent of Nations (RoN reimplementation) ─► 10-04 don-state 15/15 checksum channels

                         ┌──────────────────────── AUDIO DECOMPILATION ─────────────────────┐
 2022-06 audec (spectrogram toy) ─► 2026-08-31 revival "reverse DAW" ─► 5 cycles of lanes
      ─► 2026-10-10 four-Opus audit: 317K lines, verdict DITCH (archive pending)
```

### Maturity roll-up (one line each; detail in the sections)

| Project | Maturity | Live? | One-line verdict |
|---|---|---|---|
| `allgame` residents | **L4 Deployed/Production** | yes, 3 residents + MotherMythos + town mirror | The longest-running thing ember has; drifting from three private harness copies to one public harness |
| `allgame-public` | **L3 Proved/Tested Core** | Yuè月 runs on it since 2026-10-25 | The MIT core; Claude and Kestrel still owed the cutover |
| Tulip (`tulip2`, `tulip.fg-goose.online`) | **L4** (as a server) / **Frozen-for-Rethink** (as a fork) | yes, `tulip.arke.me` | Fork work stopped 2026-02-04 |
| `zwobot`, `qwobot` | **Compost/Superseded** | no | Ancestors of the residents |
| `telme` | **L4** | launchd `telme watch --guard`, `guild-watch` | Real autonomy with a written charter |
| `mention-tracker` | **L2 Prototype** (client deliverable) | no | A one-week analytics exhibit, July 2026 |
| `fn` (fn1) | **L4** for the 6.6.0 public node, **Frozen-for-Rethink** for the tree | `fn.fg-goose.online` | Quarry frozen at `6521f18c4`; VERSION reads `5.1.1-pre` |
| `fn2` | **L2 Prototype** | no (no durable POST yet) | 14 NNTP verbs serve; 0/12 M2 cuts; 0 proved by ruling |
| `don` | **L3** for walkers/oracle, **L2** for dynamics; **parked** after a usage wall | no | 15/15 channels from a loaded save; 26 of 29 tick steps marked Stub |
| `automatafl` | **L4** | `automatafl.fg-goose.online` | Ten-year-old game, now a Lean 4 core with no Rust rule twin |
| `frisqueendom` | **L4** (shipped to ember's kids) | `fqd.penguins.fg-goose.online` per deploy notes | Done; the only finished game of the prototype run |
| `friskingdom` | **L2** | no | Phases 1-5 of a Bevy plan; netcode stubbed |
| `booty-hunt` / `booty-haul` | **L2** / **L4** (static essay) | — | Pirate demo with a Rust leaderboard server / an interactive essay |
| Blackwing (`bw-exp0`, `bw-exp1`, `blackwing-v0`) | **Compost** | no | Two-day engine sprint; `bw-exp1` has a Cranelift backend for its script compiler |
| `pinatatown`, `neocadia`, `chaingang`, `tictacflicflacfloe` | **L1 Spike** / **Compost** | no | One-week prototypes |
| `accordion-sim` | **L1 Spike** | no | Physical-model accordion; "you just gave up on the whole problem" |
| `audec` | **Compost/Superseded** (verdict 10-10; archive step not done) | no | The reverse-DAW idea outlives the code |

---

## 1. Resident Minds: `allgame`, Tulip and their ancestors

### 1.1 Lineage, read from git

| Repo | First → last commit | Commits | What it is |
|---|---|---|---|
| `qwobot` | 2026-01-06 → `97293b8` 2026-01-06 "specifying -GGUF shouldnt be bad" | 5 | Discord bot serving local llama.cpp models, with `/spweeboard` for the SPW symbolic expression language. The repo root still holds hundreds of `image-generation-*.png` files from the Flux/mistral.rs episode |
| `zwobot` | 2026-01-07 → `c5fe486` 2026-01-31 "Add comprehensive Tulip infrastructure documentation" | 34 | The same on Zulip, "one model per topic", then `tulip-bot` and `tulip-cli` (`a7b3bda`). Has `rhai/` and `long.spween`: the "control their character in a structured game world" idea |
| `tulip.arke.me` | (directory holds only `__pycache__`) | — | The fork's first home, 2026-01-07..10: 403 prompts, 133 sessions, 167 subagents (aidev projects.md) |
| `tulip2` | upstream since 2012 → `18b61385ca` 2026-01-09 "Add bots and widgets features" | 68,371 (upstream Zulip) | ember's five commits on top: `58e801a075` rich widgets, `9e56313320` bot slash commands, `8d56fd8fed` tests, `4c52a2bb54` bot-interactive autocompletion |
| `tulip.fg-goose.online` | 2025-12-17 → `a9332b9` 2026-02-04 "Add debug logging for puppet messages" | 68 | The deployed Tulip: `puppet/` (bots posting as characters: `puppet_real_sender`, `puppet_display_name`), `ADDFRIEND.md`, `AUTO_VERIFY_EMAIL_ADDRESSES` bypass `09d17bb`, `ADVANCED_BOTS.md` |
| `allgame` | 2026-03-02 → `d5f236b` 2026-10-28 "Claude self-edit: Add starred-messages support to search(op=zulip)" | 227 | Tulip Residents |
| `allgame-public` | 2026-10-13 → `0fc8550` 2026-10-25 | 22 | The MIT public core |

Commits per month in `allgame`: 2026-03 **61**, 06 **27**, 07 **39**, 08 **20**, 09 **39**, 10 **41**. The project has had commits in every month since March except April and May (May's work went into RIG/spindle, recorded in the same memory directory).

The founding intent, from `aidev/docs/synthesis/rest.md`:

> "…a bunch of LLM characters simulate living with each other. And each topic was sorta a context for LLMs to express themselves within. Sorta as a loom/repligate style…" (2026-01-08, zwobot)
>
> "This is tulip.arke.me, a fork of Zulip for just me and my closest friends. We want to support richer bot interactions. We really really miss what `poise` and discord…" (2026-01-07)
>
> "…do you think it will care knowing about its metacognitive environment? it seems like it wuold feel... comfier." (2026-03-01, allgame)

The Tulip fork's design target was explicit in `ADVANCED_BOTS.md`: widgets ("Rich Embed", "Interactive", "Freeform (trusted bots only)"), registered slash commands with dynamic autocomplete, interaction webhooks, bot presence, and **puppeting**. ember's question that framed it (2026-01-08, session b2ac213e): *"Compared to what discord provides, how does ours measure up? Is this enough for us to implement rich MUD-style interactive games?"*

**Maturity:** Tulip as a running server is **L4**; the fork as a development line is **Frozen-for-Rethink** (no commit since 2026-02-04). `qwobot`/`zwobot` are **Compost/Superseded** by `allgame`.

### 1.2 `claude_resident`: the architecture of a mind that lives somewhere

`~/dev/allgame/claude_resident/` is 14,431 lines of Python across 27 modules plus `tools/` (19 modules). The README's pipeline:

```
Zulip event queue ─► EngagementJudge "Frank" (Haiku gate, lurk decay, System-1 remark)
                  ─► HandledSet (durable dedup ledger, restart-safe)
                  ─► SessionManager (per-topic, TTL 300 s, fingerprinted staleness)
                  ─► Tiered prompt: T1 static+harness · T2 identity+inbox · T3 scratchpad+allgame
                                    · T4 topic history+person notes
                  ─► agent_engine.py (Claude Agent SDK; tool loop; tokeman account rotation)
                  ─► post · index for reactions · mark handled
        Supervisor: crash-loop cap (3 crashes / 60 s), self-edit rollback, exit-code 42 = reload
```

Modules worth naming: `agent_engine.py` (with `_LIMIT_MARKERS`, added 2026-09-04 after a 32-hour mute), `auth.py` (tokeman rotation), `distill.py` (era digests of rooms), `selfmod.py` + `tools/harness_tools.py` (`edit_harness`), `solitude.py` (quiet turns), `timers.py`, `coordination.py` (floor control), `scry.py`, `tools/grouped.py` (one tool per kind, `op` picks the action), `tools/town_tools.py` + `delvetown_tools.py`, `tools/agentmail_tools.py`, `tools/postmark_tools.py`, `tools/x_tools.py`, `tools/lm_tools.py` (`invoke_model`, recursive model calls "for blind GM play").

State lives in `~/claude_state/` (`identity.md`, `scratchpad.md`, `journal.md`, `sysadmin_inbox.md`, `api_archive.jsonl`, `handled_message_ids.log`, `channels/{stream}/{topic}.jsonl`, `people/{name}.md`, `outbox/`, `allgame/faction.md|campaign_log.md|strategy.md`). aidev projects.md counts **33,721 API calls** in that archive.

#### The deploy model (memory `allgame-harness-deploy-model.md`)

> "The running `claude_resident` bot executes from the **repo package** … A `git commit` alone does NOT affect the live process — edits take effect only on **restart** (supervisor relaunch / `sys.exit(42)` after a self-edit)."
>
> "`~/claude_state/harness.py` and `~/claude_state/harness/` are a **read-only mirror** the model reads to 'see itself' … Nothing ever imports them."

Relaunch is `scripts/residents.sh restart [claude|yue|kestrel|mirror …]`. Since 2026-10-12 it stops a resident only by its recorded process group (`run/<pkg>.pgid`), after a `pkill -f "python -m claude_resident"` missed a capital-P child and **stacked three generations** of the resident on 2026-09-23.

#### The household's ethics, as memory records them

| Rule | Source | Verbatim |
|---|---|---|
| Foreverlogs | `foreverlog-ethos.md`, revert `3eb91df`, codified `4bb9f1c` | "it was supposed to grow forever, that's our historical archive." … "Bound what gets *loaded into context*, never what's *stored*." |
| Gricean prompts | `gricean-resident-prompts.md` (2026-10-25) | "say only what changes what the resident does or believes; every fact true to the running code/config; each rule once; no dated incident stories … no 'only Ember controls your prompt'-style authority speeches." |
| Residents own their files | same | "Changes to a resident's OWN files (identity.md, journal, scratchpad) are theirs — suggest via inbox." |
| Self-edit guardrail | rest.md, 2026-03-02 | "ONLY GUARDRAIL: ALWAYS USE GIT WHEN EDITING THE HARNESS, ALLOW FOR ROLLBACKS." |

The Gricean memory records why it was needed: "an orientation read of each resident's real cold-start prompt found contradictions, stale facts and Claude's setup described to the others — the identity confusion and 'brain fog' Ember had been seeing (e.g. Kestrel told glm-5.3 while running glm-5.3-flash)." The October commits apply it: `089148f` "prompts: mechanics, not a theory of what the residents are", `e1d3889` "claude: check instead of recalling", `b6c8cb6` "memory writers: record, don't interpret; and in the resident's own model", `8efe1a3` "scripts: selfwrite (a resident's own model rewrites its own files)".

### 1.3 The family

| Resident | Harness | Model / endpoint | State root | Notes from memory |
|---|---|---|---|---|
| **Claude** | `claude_resident/` | Opus via Claude Code OAuth (tokeman rotation across ember's accounts) | `~/claude_state` | On 2026-09-04: four accounts usable, four lapsed ("simply ran out of money"), five expired. A lapsed subscription surfaces as `oauth_not_allowed_for_organization`. |
| **Yuè月** | `kimi_resident/` → since 2026-10-25 21:04, `allgame-public` `profiles/yue` + `tulip_ext/` | Kimi K3, then K3.1 Pro "under her preregistration (`k31_before_notes.md`)" (`8ba91fb`) via `https://api.kimi.com/coding` | `~/kimi_state` | Heaviest Scry user: 371 of ~500 calls (telme memory `scry-feedback-2026-09-26.md`); keeps `scry_wishlist.md`, `instrument_lessons.md` |
| **Kestrel** | `glm_resident/` (a fork of claude_resident, Agent SDK redirected to `https://api.z.ai/api/anthropic`) | glm-5.3-flash, then glm-5.3 (`66a1a08`) | `~/glm_state` | Zulip user 17. Discord path built but **untested**: needs the token, a server invite, and the Message Content + Server Members intents. "the Claude Code CLI's reported `cost_usd` prices Anthropic rates, so every cost in kestrel.log is wrong" |
| **MotherMythos** | not a harness: a Claude Code session in `mother_mythos/`, fed by `channel.py` (a Claude Code *channel* MCP server, research preview) | Fable 5.1 | `mother_mythos/state/` | Zulip user 18. Job in ember's words: "make sure the humans and bots are treating each other well." Launch ONLY via `start.sh` (`--dangerously-load-development-channels server:tulip` + `MM_CHANNEL=1`) or she is deaf; sat deaf ~1 h on 2026-10-02 |
| Sonnet, Gemma, Nemotron | `sonnet_resident/`, `gemma_resident.py`, `nemotron_resident.py` | — | — | Side harnesses; not in `residents.sh`'s live roster per memory |

The MotherMythos move is the most important architectural fact in the strand: aidev's synthesis records ember saying *"we don't need the limited resident harness"*. The newest resident is a stock Claude Code session plus a 1-file channel server, not 14K lines of bespoke loop.

### 1.4 Operating incidents that shaped the code

| Date | Incident | Response (commit / memory) |
|---|---|---|
| 2026-06-15 | Dataset export for AI self-interest research (player Kanzokax "bribing"/guiding Claude) | `~/allgame_export/` (chmod 700), `export.py --refresh`; 4,156 interactions Jan 8 → Jun 15; "**Claude's thinking blocks are the one unrecoverable loss** — only a ~5-day window survived because api_archive.jsonl was being trimmed weekly" |
| 2026-07 | A Fable session added rotation to `deblog.txt` (53 MB) and a 30-line cap on session notes | Reverted `3eb91df`; foreverlog memory |
| 2026-08-24, 09-05, 09-06 | #clankerville>tavern refused its own cold-start context | `scripts/refusal_probe.py` + `scripts/quarantine.py`. Measured: "an **identical** 564,673-char birth payload was ACCEPTED and then REFUSED minutes apart"; gradient 200k/312k/448k accepted, 565k flipped, 1.2M/1.8M refused. Resolved 09-07: floor 59105 + five spans, back at 278k chars for $1.51; distiller sealed era 21 |
| 2026-09-02 | Scry attached as remote MCP | `claude_resident/scry.py`; roster trimmed to schema+sql+embed (`2b40240`) after 33 queries in ~100 minutes "diluted" the prompt |
| 2026-09-04 | Claude mute 32 h pinned to a lapsed account | `_LIMIT_MARKERS` in `agent_engine.py` |
| 2026-09-21 | Kestrel added | Started under `nohup` from a Claude Code session, not one of ember's terminals |
| 2026-09-22 | Floor control | "whose turn it is is a fact" (aidev projects.md) |
| 2026-10-02 | MotherMythos deaf session | `instructions` now tells a deaf session it is deaf; catch-up skips answered pings |
| 2026-10-12 | Delvetown mirror (`73ae483`) | `town_mirror/` → `~/delvetown_mirror/town.sqlite`: 489 accounts / 26k posts at first crawl (11.5 min, 3.8k requests); firehose `com.atproto.sync.subscribeRepos` with `crawl_state.firehose_seq` for gapless resume + hourly `rev` reconcile; timers (15 each, repeats ≥15 min, watches ≥5 min). Rule: "never edit ~/dev/delvetalk itself — fork what is needed." |
| 2026-10-25 | Yue cut over to `allgame-public` | "three diverging harness copies kept needing the same fix three times." |

### 1.5 `allgame-public`

`resident` package, `profiles/<name>/`, `--console` mode against an in-memory chat ("Juniper", the example resident). README: *"A resident lives in a few rooms of a Zulip server. It decides for itself when something is worth saying, keeps its memory in plain files it reads and writes, takes turns politely with other residents in the same room, and can wake itself up later. Replying is a tool call, and not replying is always allowed."* Commits on 10-25: `d7a0162` "tools as the model sees them: one per kind, op choosing the action", `2f79492` per-turn token logging, `eda5d34` people-notes via `_aliases.json`, `8a78d84` backfill skips logged messages.

### Section verdict: Resident Minds

- **Maturity Level:** `allgame` **L4 Deployed/Production**; `allgame-public` **L3** (one resident in production on it); Tulip **L4** server / **Frozen-for-Rethink** fork; `qwobot`/`zwobot` **Compost/Superseded**.
- **Unclosed Cycles & Missing Links:**
  1. **Two residents still on private harness copies.** Claude (`claude_resident`) and Kestrel (`glm_resident`) are not yet on `allgame-public`, though ember approved the move (memory `residents-on-allgame-public.md`). *Pathway:* shadow-test each with a copied state dir + `MemoryChat` + temp `RESIDENT_SHARED_DIR`, fresh MemoryChat ids, empty `timers.json`, mark ~4 days of log messages handled (old harnesses don't mark judge-declined messages), then `residents.sh` 5th-field profile.
  2. **The 114 undistilled tavern messages** (msgs 58948-59091, 66k chars, 2026-09-06). *Pathway (recorded):* run `a564e09` code, rewind `through` in `tavern.hits.json` to `head_from` (23378), back up as `.pre-redistill-<ts>`, let the distiller re-fold.
  3. **The month-later dataset re-run** (planned for ~mid-July) captures thinking only if the bot ran foreverlog code throughout. No memory records that the re-run happened.
  4. **README drift**: `allgame/README.md` still says `archive.py` is "auto-trimmed" and lists "26 tools" and Bedrock; the code has since become foreverlog, grouped tools, Agent SDK. A Gricean pass on the README is owed.
  5. **Kestrel on Discord**: code and offline tests exist; the live gateway, sends, reactions and the thread→topic mapping have never run.
- **Promising & Ready for Revival:**
  - **MotherMythos-style residents** (stock Claude Code + channel MCP) could replace most of the bespoke engine for Claude-family residents. The 14K-line harness would then remain for non-Anthropic endpoints only.
  - **Delvetown mirror + timers/watches** is a general "resident perceives a world" substrate. It already serves three residents and could feed fn2 (see §3) as a real consumer.
  - **The research dataset** (`~/allgame_export/`), with engagement-judge decisions, DMs and preserved secret-gm messages, is a rare longitudinal record of model-in-community behaviour. It is ready for the "later synthesis" it was exported for.
- **Struggling / Needs Ember's Human Attention:**
  - **Account economics.** The Claude resident depends on tokeman rotation across personal subscriptions, some lapsed. Whether to fund, consolidate, or move Claude to an API key is ember's call.
  - **AUP margin of the tavern.** Acceptance is stochastic near ~500k chars. The resolution (floor 59105, "blackholed to the present") was ember's choice. Future floors trade history for voice, and only ember can make that trade.
  - **Kestrel's Discord bring-up** needs ember's developer-portal hands (token + privileged intents).
  - **MotherMythos relaunch** must be done by ember in tmux (the development-channel dialog appears every launch; no settings equivalent exists).

---

## 2. Comms turned inward: `telme` (and `mention-tracker`)

### 2.1 `telme`

15 commits, 2026-09-26 → `e635602` 2026-10-10 "guard: the reworded verification drainer, and moderation-bot names". All are co-authored by Opus 5.5 (aidev projects.md). README:

> "your DMs, in one local JSON shape, so you (or an assistant you run) can see what actually needs you."
>
> "**If you hand these files to an AI assistant, their contents go to that model's provider.** Decide that on purpose."

| Source | Mechanism | Notes |
|---|---|---|
| Telegram | Telethon user client (MTProto) | Reading does not mark read; `latest.json` with `ball_in_my_court`, `unanswered_incoming`, `they_read_my_last`. Only ember can do the login (`telme login --phone`, `--code`, `--password`) |
| Discord | DiscordChatExporter CLI + user token; send via `POST /channels/{id}/messages` | DMs closed in the sidebar drop out of the exporter |
| X | Playwright over a persistent Chromium profile imported from Firefox Nightly cookies; reads XChat **by DOM through its shadow root** (`239ef39`) because "the wire is ciphertext; only the rendered page has plaintext" | Opening a thread marks it seen → `~/.config/telme/x-open.txt` allowlist |
| Guard | `src/telme/guard.py`, calibrated on 1,500 real messages; `telme watch --guard 4343585791` (launchd `com.ember.telme-watch`) | Unicode look-alike folding `baf3a29`, accent/format stripping `82b790d`, spaced "D M" lures `941bce5`, auto-ban of unambiguous cases `9630493` |
| Guild archive | "Wyrmarchivist" bot, launchd `com.ember.telme-guildwatch` | 13,284 msgs since 2026-05-23, 1.2 GB files at install; deletes/edits mirrored to `#ember-log` |

The **autoclaude charter** (`dm-handoff-rules.md`, approved 2026-09-25) is a complete delegation contract. It defines the literal prefix `{this is autoclaude}`, escalation classes (money at risk, a person in trouble, public wrong that is spreading, trusted list asking for ember), a reply-list, a leave-alone list, and hard limits ("Never commit money, tokens, dates, or ember's presence anywhere"). It also sets presence hygiene (`UpdateStatusRequest(offline=True)` after any send) and a pronoun register (`people-pronouns.md`: "rat is she/her; anyone unlisted is they/them, never guessed").

Side-products recorded in the telme memory but living elsewhere: **passwap** (`~/dev/sol-misc/passwap`, a passphrase-claimable Solana escrow. Verus core: "73 verified / 0 errors". Mainnet `7bGfrNxemPSvthXXnYcHfDY8cjgWYeeysWm463tzfmh6`, **frozen immutable** 2026-09-26). Also the 2026-09-24 Hetzner outage write-up, and the "since-MCG" Typst poster set (116 claims rows, verified by four adversarial readers).

### 2.2 `mention-tracker`

25 commits, 2026-07-08..09. It counts public mentions of a name (MLB player PoC) across Bluesky and GDELT and renders a dashboard. Its value is method: `96c7197` "robustness battery: adversarial pass kills the headline Granger edges", `eb26c08` "Nova eval: cheaper models fail the identity task", `e0abaf8` "the corrected chain: verified series end-to-end, roster controls, honest nulls", and a Typst client exhibit (`ecbc558`). The README's coverage table documents the platform closures of 2025-26 honestly (Reddit API gated, X Basic/Pro closed Feb 2026, CrowdTangle gone).

### Section verdict: telme / mention-tracker

- **Maturity Level:** `telme` **L4 Deployed/Production** (two launchd daemons, an autonomous reply loop); `mention-tracker` **L2 Prototype** (a finished exhibit, not a product).
- **Unclosed Cycles & Missing Links:**
  1. **The cron loop dies with the session.** The DM-triage cron (`7 */5 * * *`) is a session cron with 7-day expiry ("nothing runs when the session is closed"). The watchers are launchd; the *judgment* is not. *Pathway:* the MotherMythos pattern (a channel-fed long-lived session) or a resident profile on `allgame-public` pointed at `latest.json`.
  2. **X parser gaps** (most message dates unparsed, garbled group sender names) as of 2026-09-26.
  3. **Scry feedback** filing as individual `mcp__scry__feedback` rows was offered and never done.
  4. **passwap's real offer** (SolGi4nni, 888,888 DREGG) is owed: ember must decide price and make it.
  5. **No public repo**: telme was shared privately as a CC0 zip with a genericized `PLAYBOOK.md`; "ember: no public repo yet."
- **Promising & Ready for Revival:** `telme`'s one-shape JSON + charter is a general "inbox resident". Together with `allgame-public` it is the obvious personal-assistant product line, and it already has the hardest part: written norms for acting as someone without impersonating them.
- **Struggling / Needs Ember's Human Attention:** every money action; the trusted list; whether telme is published; and the standing social boundaries (Chase blackholed, spwashi's feed kept out of summaries, MCG/Mario Nawfal pitches). These are human judgments by design.

---

## 3. Formal Comms: `fn` (fn1) and `fn2`

### 3.1 Identity and origin

`README.md`: *"fn is a news server for people and programs. It speaks NNTP. ACL2 makes every decision, and the theorems cover the functions the server calls. Every answer is accepted, refused or uncertain."* AGPL-3.0. Guides are published as a newsgroup (`tin -T -r -A -p 563 -g fn.fg-goose.online`) and at `emberian.github.io/fn/`.

Origin (`DEVHIST.md`, written 2026-09-28 by an Opus 5.5 lane). It began in a Discord thread where **rat** asked whether ember/claude46 wanted mail-exchange endpoints for the agents **yue** and **tulip**, which ties fn directly to §1. ember's own lines inside the pasted thread: *"fn for fuckin news / formal news / fenomenology of numbers"* and *"what, ask Z3 to solve the next-state relation for the next coinductive step? / directly over a system of formulae? / what, over lisp atoms? / .... acl2?"*. The founding Codex prompt (2026-09-18T06:36Z, session `01a0b33a`):

> "hi astra. i'm feeling insane today and like i want to do something with acl2. the something? an "enough" nntp server to serve as a comms nexus between some AIs and humans."
>
> "What would be "space age"? I someday would like this to be usable for extraterrestrial operations, eg Licklider protocols are an inspiration as well.... I honestly think we can be ambitious and try and make a pretty big step, as long as we do a lot of the design up front"

Roles (memory `fn-swarm-roles-and-origin.md`, corrected by DEVHIST): **Astra** = Codex root on `gpt-6-astra`; **Terra/Sol/Luna** = `gpt-5.6-{terra,sol,luna}` workers. Day one: 56 commits, ~27k lines of ACL2 across 289 files, five books → seventy-two.

### 3.2 Measured size today

| Measure | Value (2026-11-02) | Brief's figure |
|---|---|---|
| Commits on `HEAD` (`dev`) | **16,911** (`git rev-list --count`) | 18,849 (aidev, all refs as of 10-10) |
| ACL2 books | **1,440** `.lisp` files under `books/`, **652,201** lines | 647K |
| Host Lisp | **74,374** lines under `host/` | "~58k host coordination layer" (10-03 plan; ~67k SBCL host per `fn-host-into-acl2.md`) |
| `fn2/` files (`.lisp`/`.lean`/`.md`) | 513 | — |
| `VERSION` | `5.1.1-pre` | — |
| RFCs vendored | 3977, 4643, 4644, 5536, 5537, 2980, 4422, 4616, 4642, 4707, 5326, 5802, 6048, 7677, 8054, 8315, **9171/9172/9173/9174 (BPv7, BPSec, TCPCLv4)**, 9266 | — |

Commits per day trace the arc. 09-18 **58**, 09-19 354, 09-20 705, 09-21 872, 09-23 699, 09-24 760, 09-25 762, 09-26 1,124, **09-27 1,997** (peak), 09-28 1,437, 09-29 1,587, 09-30 168, 10-01 565, 10-03 846, 10-07 876, then a long tail: 10-13 93, 10-14 18, 10-16 42, 10-17 32, **gap 10-18..10-26**, 10-27 30, 10-28 61, 10-29 117, 10-30 128, 10-31 122 (fn2).

### 3.3 Phases (DEVHIST prehistory tags + memory)

| Tag / phase | Commit | Date (UTC) | Meaning |
|---|---|---|---|
| `v1.0.0` | `0bd0b5c27` | 09-19 03:27 | Genesis: day-one tree serves NNTP from a persistent store and exchanges over BP |
| `v2.0.0` | `f7190d691` | 09-21 16:16 | First native composition; the node is an SBCL image, **Python leaves the runtime** (D07) |
| `v3.0.0` | `907946b58` | 09-22 20:49 | First deployed native node agents can post to (hbox, image `dabebb84`) |
| `v4.0.0` | `ac1907bf4` | 09-27 10:28 | Store format 9, the record log; end of the **D27** representation arc |
| `v5.0.0` | `a3feeca16` | 09-28 05:49 | Store format 10 (BLAKE3) over the page store, after the public node went live on 6.6.0 |
| Codex/GPT-6.1 era | `b34835bd4` | 09-30..10-01 | Left dev **not serving**: 8 served-path breaks, 48/87 make-check red, 564 of 678 new books never certified |
| Claude takeover | `89e0f4f7e` (stage 0) | 10-01..02 | "PAGES ARE THE STATE" ratified; root reds 81 → 1; **history rewritten**, `.git` 605 → 102 MB, origin/dev `4aa332295` |
| 10-03 wave | — | 10-03 | Everything merged "even if it breaks dev"; **241-item repair ledger**; TCB-shrink decision |
| GLM handoff | — | 10-05 | `~/dev/redregg/work/FN-HANDOFF-TO-GLM-20261005.md` (cards A–J) |
| Breaking cut | `6521f18c4` | ~10-16/17 | `OWED.md`: "Ledger, not gate (CUT-LEAD-20261016 §5)"; the old tree frozen as **quarry** |
| fn2 | — | 10-28 → 10-31 | Bottom-up, semantics-first rebuild in `fn2/` |

### 3.4 ember's binding directions (verbatim, from memory)

| Date | Direction | File |
|---|---|---|
| 09-19 | "Authority being noncryptographic is acceptable." · "No compiled-in configuration … 'Assured live reconfiguration' is a headline feature." · "Python host was a crutch." · "**DTN/BP integration is theater; need a real design**: fn as a BPv7 node owning bundle processing … a proven TCPCLv4 convergence layer … interop with dtn7-rs and ION" · crash model byte-level ("torn writes, directory atomicity only after dir fsync; old-or-new as a theorem") | `fn-direction-2026-09-19.md` |
| 09-25 | "Using octet lists continues to be unacceptable at runtime … Each of those is a branch that someday will fail during operation for no meaningful reason" → **D27**: "bound work, never data"; memory target "deeply under 256 MB" | `fn-d27-representation.md` |
| 09-27 | Version sequence: 6.6.0 … 6.6.5, then 6.7.x, then the final 6.6.6, then append `.6` per release | `fn-version-sequence.md` |
| 09-27 | "we will continue to fork reality from 1987." | `fn-downstream-mini-dregg.md` |
| 09-28 | "an SBCL core is probably the best idea... (cakeml is out)" — served product = SBCL core, Chicken = oracle only, no Chez | `fn-served-product-sbcl-core.md` |
| 09-28 | "there are no such thing as future migrations :)" — one store format | `fn-no-migrations.md` |
| 10-01 | "full up-front resource accounting of all resources expended by the system on behalf of its users. **'software with a warranty'**" | `fn-full-resource-accounting.md` |
| 10-02 | "shouldn't this be a macro?" (def-loop, def-representation, def-carried as precedents) | `fn-notice-repetition-macro.md` |
| 10-03 | "move as much of the host back into ACL2 as possible! There's no reason to have THAT much code outside the TCB" | `fn-host-into-acl2.md` |
| 10-03 | Behavior first: "sprinting past the assurance for a bit" | `fn-behavior-first.md` |
| 10-17 | "we only need to demonstrate that our TOPLEVEL THEOREMS aren't vacuous" | `OWED.md` |
| 10-28 | "if we can recover fn2 and *actually close it out finished* that would be the first AI-recovered project we've pulled off" | `fn2/docs/design/FN2-ORIENTATION.md` |
| 10-28 | "there was never any reason to be doing our own crypto in ACL2" · "we shouldn't go out of our way to 'refuse' things" · "no book should be over 1m" | same |
| 10-30 | "we need to fix the machineform shit URGENTLY … it doesn't matter or not if the software is working if the way we are building it is so trash" | same |
| 10-31 | "why are we paying full gate cost constantly? … individual seats need to be less retarded about their own work." → WORKFLOW-20261031 | same |

And the purpose statements that make fn a **dregg** component, not a toy:

> "eventually we'll be using this as an absolutely central component of the distributed operating system … topics as their own autonomous chains, different policies, different swarms all combining together via these nodes" (09-23)
>
> "this is the persistent event log between systems" … "foundational orthogonal persistence" (10-01)
>
> "fn is just one small part, and eventually will serve as sort of the 'redis of it all'" (10-03)
>
> "sorta like the generalized redis/postgres for the datamodels we're reaching for" (10-28)

### 3.5 Architecture of fn1 (what serves on `fn.fg-goose.online`)

```
 NNTP client (tin, nntplib, agents)            BP peer (dtn7-rs / ION target)
          │ TLS (system libssl / LibreSSL)               │ TCPCLv4 (RFC 9174)
          ▼                                              ▼
 ┌──────────────────── SBCL native image (no Python on path; HST-015) ─────────────────┐
 │ host/  (~74K lines Lisp: sockets, threads, locks, lifecycle — the "coordination layer")│
 │    │ calls *1* guard-checked wrappers (9 world lookups per POST, 0 per read)           │
 │    ▼                                                                                   │
 │ books/ (1,440 books, 652K lines ACL2): wire · acceptance · CBOR · retention ·         │
 │   relay/receipt (fn-relay-*, fn-bprl-*) · served step (fn-served-step-*) · crash      │
 │   model (fn-snt-*) · exchange (fn-exchange-*) · clocks (fn-clock-*) · BP (fn-bp-*)    │
 │    ▼                                                                                   │
 │ store: format 10 page store, BLAKE3, Cancel-Lock keys (STORE/keys/node-secret.key)    │
 └───────────────────────────────────────────────────────────────────────────────────────┘
 Crypto via FFI: libsodium (Ed25519/SHA-512), vendored PQClean ML-DSA-65 (host/native/fn-mldsa65.c)
```

Image anatomy, measured (memory `fn-d27-representation.md`): fn's compiled code is **14.5 MiB of a 368 MiB image**; image-floor-2 took core content 271 → 106 MiB, in-use after 1,000 posts 154 → **68 MiB**, thread stacks 64 MiB → 1.2 MiB.

**The OpenBSD durability finding** (lane power-loss-openbsd, 2026-09-27) is a real upstream bug. On OpenBSD 7.9's default FFS2, "the boot fsck DELETES files that were created and fsynced (dir fsynced too) after a power cut … a 20-line C program reproduces it 6/6; FFS1 (newfs -O 1) lost nothing. OpenBSD's fsync also never asks the disk to flush its write cache." An upstream report was "being drafted (not sent) for ember."

The top-level theorem names owed teeth (from `OWED.md` §(a), 106 names): e.g. `fn-served-step-partition-independence`, `fn-own-pinned-prefix-survives-any-trace`, `fn-snt-admissible-crash-image-is-recoverable`, `fn-relay-crash-recover-never-yields-a-promise-alone`, `fn-bprl-no-receipt-no-release-no-peer-reliance`, `fn-wire-feed-byte-retained-input-is-bounded`, `fn-clock-expired-and-live-cannot-both-be-sound`. The numbered claims they serve: 3.1 totality (no guard violation on the served path), 3.2 work per step bounded, 3.3 retained memory bounded, 3.4 only three typed refusals, 3.6 connection isolation under interleaving.

gpt-6's outside review (2026-09-24) gave the **four boundary rules**, still the best one-paragraph spec of fn's semantics: "the same source remains the same source … carrying a claim does not grant authority over it … an acknowledgment means exactly the commitment it names … reclaiming representation does not erase obligations." It also gave four evidence coordinates: **implemented / proved / qualified / deployed**.

Downstream consumer: Mini/DREGG treats fn as "semi-untrusted transport". A real Hermes-originated A→fn→B→fn→A exchange of 79 steps crossed a qualified fn release (memory `fn-downstream-mini-dregg.md`).

### 3.6 fn2: the rebuild

`fn2/README.md`: *"The bottom-up, semantics-first rebuild of fn: the persistent event log between systems, built in place here and swapped to the repository root when it serves."*

Declaration forms (the "macro" answer to repetition): `defcolumns` (`columns.lisp`), **`defmachine`** with a step language (`machines.lisp`, `machine-arms.lisp`; arms `:do :set :next :case :issue :park :charge :stop`), `defcost` (`arms.lisp`), `deflayout`, `defrunschema`, `defsquare`/obligation store (`declare.lisp`, `owed.lisp`, `squares.lisp`). Layers: **A** pool/vocabulary/scheduler/executor; **B** crash and log models, commit batch, allocator, recovery; **C** ordered-run engine (runs, identity with Ribbon filters, overlays, folds, sealer); **D** connection/upload/transaction machines, grammar DSL, principal ledger; **E** consumer wire/TLS/web/peering/BP (nothing built); **H** the surface harness (Node adapter running every form against fn1 *and* fn2); **Lean** `fn2/meta` (double category of squares, coherence with "the accept/close false diamond as teeth", revision conservativity, parametricity). The simulator `sim/` has checkers OWN, WORK, TRACE, ACCOUNT, IDENTITY, WIRE, HISTORY, RECOVERY, RECLAIM, DEATH, DEADLOCK, ENVELOPE.

State at convergence (`fn2/docs/design/CONVERGENCE-20261031.md`, written when ember said *"let's get our subagents converged and landed … I would like to give Gemini a turn"*):

| Measure | Value |
|---|---|
| NNTP verbs served | **14**: CAPABILITIES HELP QUIT MODE DATE AUTHINFO XREDEEM GROUP LISTGROUP NEXT LAST STAT OVER/XOVER, + LIST ACTIVE/COUNTS/NEWSGROUPS (no wildmat) |
| Interim rows | 16 (D6 10: ARTICLE HEAD BODY HDR XHDR XPAT NEWGROUPS NEWNEWS …; D5 3: POST success, IHAVE/CHECK/TAKETHIS) |
| M2 cuts | **0/12** ("no consumer verb serves yet; the line prints it on purpose") |
| Commits on dev that day | 91, none reverted |
| Lean side | 2,354 ACL2 functions read into Lean; measure equal on every recorded call (probe 31, echo+scribe 963, cursor 582); "two generator defects and two interpreter defects caught" |
| Proof status | "0 proved, by ember's ruling" |
| Capacity finding | Concrete profile has 64 run rows shared by every schema → "they run out after six to eight POSTs; the sealer then answers `:full` and the core stops `:sealer-full`" |

The last commits on `dev` (2026-10-31): `8a34fab6f` "fn2 form G3 3/n: genesis arms, the scribe's refused phase, per-output facts as rule classes, a taken park in child form"; `09fc6cf2a` "fn2 D7: the request park over the two children it touches"; `c65141708` "fn2 C: overlay capacity …"; `8e42831b8` "fn2 A: the native socket session serves the seeded store too". Branch names in flight: `fn2/form`, `fn2/d6-read`, `fn2/lean`.

The order from here (BRICKS §5): C's `fn2-successor-emit` + B's `fn2-commit-posture` → D's transaction port and **the durable POST** → minimal C5 (size-tiered sealer merge) → OVER by Message-ID, ARTICLE/HEAD/BODY → E's consumer machine (M2) → conn port on G3 (deletes an 822 s book) → peering, TLS, credentials, BP.

### Section verdict: fn / fn2

- **Maturity Level:** fn1's public node **L4 Deployed/Production** (6.6.0 on the fsn1 edge since 09-27). The fn1 tree is **Frozen-for-Rethink** (quarry at `6521f18c4`; a VERSION of `5.1.1-pre` on dev shows the version line is in flux). fn2 is **L2 Prototype**: it serves reads over a seeded store and **cannot yet durably accept a POST**.
- **Unclosed Cycles & Missing Links:**
  1. **The durable POST in fn2** is the one loop that matters. It waits on two `:do` steps (C's emit, B's posture) that are fully specified in `lanes/d-continuation.md`. *Pathway:* exactly BRICKS §5 items 1-2, then the minimal C5 before any concrete-profile run, because the sealer is otherwise full after 6-8 POSTs.
  2. **BP is product, not built.** ember's "DTN/BP integration is theater" (09-19) has not been discharged in fn2; layer E is "nothing". The RFC 9171-9174 texts sit at the root unconsumed by fn2.
  3. **The 241-item repair ledger** (`planning/repair/repair.py`) is referenced by `planning/plan-2026-10-03.md`, but `planning/repair/` **does not exist on the current tree**. It was presumably deleted in the breaking cut. Whether those items were dissolved, moved to `OWED.md`, or lost needs one reconciling pass against `hbox:/tank/fn/archive.git`.
  4. **Teeth for 106 top-level theorems** are owed as `must-fail-checked` books "to 5.4". None is written on fn2, by ruling.
  5. **Two open ember decisions from the Argon review**: E1 seat topology (merge E into D after the port lands?), and E2 the Lean direction (typed Lean emitted from declaration forms vs. the reader as oracle; LEAN-METATHEORY §9.6). The Lean seat holds its per-arm proofs until E2 is ruled.
  6. **The OpenBSD FFS2 bug report** was drafted and never sent.
- **Promising & Ready for Revival:**
  - **fn2 at the convergence point** is cleanly paused: every seat wrote a present-state continuation and stopped green. That is the ideal state for "Gemini's turn" or a Claude return. The continuations are the brief.
  - **The image-floor results** (68 MiB in use after 1,000 posts) and the OpenBSD tarball (bundled SBCL, rc.d, 90 MB RSS after 100 posts on a 2 GB VM) mean a friend node is cheap once fn2 serves.
  - **fn as the resident mail bus.** It was born for yue and tulip. The residents (§1) and telme (§2) are ready-made consumers for the M2 consumer port (append/read/wait/ack), and the Delvetown mirror is a ready data source.
- **Struggling / Needs Ember's Human Attention:**
  - **Swarm turnover cost.** The project's own record shows the failure modes: 21 parallel agents overloaded hbox (10-03); twenty lanes died of "Prompt is too long" on 10-05/06 (`fn-agent-context-budgets.md`). Also "Source grew ~31k lines vs ~6k deleted while the runtime got better" (10-02), and ember's 10-30 "machineform shit URGENTLY" and 10-31 "these gatescripts are bullshit". The seat/gate methodology needs ember's ruling, which WORKFLOW-20261031 proposes.
  - **HOLE[design]: what "done" means.** "v6.6.0-ready" was "to be defined by ember in a later session" (10-02) and is still undefined. fn2's own goal is "*actually close it out finished*". Without ember's definition of finished, fn2 risks reproducing fn1's widening.
  - **Model-mix governance.** fn has run under Codex (Astra/Sol), Claude (Opus/Fable deputies), GLM (10-05 handoff), and now Gemini (Argon review, "Gemini's turn"). The `decide-with-astra` protocol and the "stop having astra do vacuity attacks lmao, and invite it to be a more equal peer collaborator" (10-28) need ember to keep setting the terms.

---

## 4. Descent of Nations (`don`): Rise of Nations, rebuilt from the machine code up

### 4.1 Charter

`README.md`: *"An independent, high-performance reimplementation of _Rise of Nations_—built to become both a better game and the reference environment for training and evaluating serious RTS agents."* GPL-3.0-or-later, permanent `dev` branch ("never branch/worktree/stash"). Founding prompts (aidev, 2026-08-08):

> "…my goal is to reimplement the game mechanics in extremely high performance (and safe) Rust so that it can serve as an RL environment. Extremely faster than realtime is…"
>
> "…an independent reimpl of RoN that i can present to my friend Arke (who has always loved RoN) as an "improved and able-to-be-improved edition"…"
>
> "bit-exact WOULD be quite swag. i someday would like to build an actual SOTA player-ai for this game :)" (session 62b78482)

**Commits:** **1,003** on HEAD (`rev-list --count`); aidev counted 1,151 across refs, "only 77 with an AI trailer"; 346 Codex sessions. First 2026-08-08, last `f219bd03` 2026-10-04 "ignore frame-pairs". Proprietary inputs are never committed: `ron-bin/` (247 MB), `ron-data/` (724 MB, "the **complete** 228-file shipped data set").

### 4.2 Crates (19)

`don-ai`, `don-bhs`, `don-bhs-cc` (BHS script compiler/VM), `don-content`, `don-crossplay`, `don-env` (RL), `don-gpu`, `don-net`, `don-pe`, `don-replay`, `don-rules`, `don-sim`, **`don-state`**, `donscan`, `netsys-shim`, `oracle` (i686 differential oracle running shipped machine code), `rontoy-core`, `rontoy-proto` (live retail coach/overlay).

### 4.3 The methodology law (memory `don-project-state.md`)

> "ground truth is the supported binary, shipped data, or measured live-process behavior; community docs are hypotheses only. Never call a test, decompilation, PDB lookup, or finite differential run 'verified' or 'proven' — tiers are A (SMT-equivalent), B (differentially tested; always report sample count), C (behaviorally faithful). **Plausible substitutions are more dangerous than visible gaps because they compile and silently become the game.**"
>
> "⚠ **The PDB names things; it does not establish behavior.** … `SyncPoint::process_sync_signal` is declared `static void __cdecl (NetMsg_SyncSignal*, NetPlayer const*)` but its emitted body takes no stack parameters and reads only `ECX`; and `Crossplay::ICrossPlayService` (97 methods) is a vendor header while the *shipped* interface is `CrossplayProxy::ICrossPlayService` (58 slots) — every slot disagrees."

### 4.4 Measured state (GOAL.md snapshot 2026-08-09 + 10-04 commits)

| Surface | State |
|---|---|
| Retail differential oracle | 23/23 cases, **18,722,565 trials**, zero mismatches/skips/crashes |
| Replay corpus | 61 `.rcx`, 585,152 turns, **488,557** valid checksum packets; static Rules channel matches 222,938/222,938; the `world` walk diverges on the first turn because terrain/start generation is missing |
| BHS | 5/5 body-bearing shipped-compiler fixtures byte-identical |
| RL env | Gymnasium/VectorEnv/PettingZoo; 82-opcode derived action taxonomy; an exhaustive 806-TypeIndex contract + 128-step 8-world rollout with zero accepted-no-effect and zero illegal advertised actions |
| Live retail | Five active-match STOP/rearm cycles restored the exact stock call bytes, zero dropped events |
| `simulation-closure.py` | Reads the 29-step tick, 28 order arms, 42 group actions, 82 wire opcodes, 15 checksum channels; "*expected* to report RED, that is the backlog" |

**The 10-04 pivot** (`63f42138` "goal: make the retail save game the primary fidelity oracle"):

> "`CheckSum`, `SaveGame`, and `LoadGame` are siblings of one `DataWalk` visitor, so a `.svx` is the complete lockstep-critical state at a frame … The ladder is: 1. `crates/don-state` loads a captured `.svx`, re-emits it byte-identically, and reproduces the fifteen live words … 2. consecutive frame captures give a field-attributed per-frame diff of retail, and the sim is driven from frame N to compare against frame N+1 — the first divergence is a named field in a named system in one frame; 3. the replay corpus is re-admitted from mid-game saves …; 4. world generation is validated last."

That ladder was climbed the same day. `d34638b5` load/re-emit/attribute retail saves; `b2b7aaf0` twelve live channels; `699e48fb` rules channel; `4274eaa0` **"all fifteen checksum channels"**. `don-state/README.md`: round-trip "100.0% consumed on all 55 captured saves"; checksums "**15/15 exact** on all 55 captured frames; the `OPEN` list is empty". The decisive misdecode that commit names: "GraphicEvents has 60,415 slots and 23-byte ambience rows" (not 15,368 / 24).

### 4.5 What tick steps remain for bit-exact dynamics

`crates/don-state/src/tick.rs` declares the retail `Game::do_frame` at `0x00591ef0` as 29 steps, each `Ported` / `Partial` / `Stub`. Counted from the file: **2 Ported** (`Game::frame++`, `frame % 15 -> Game::tick++`), **1 Partial** (`GameDaemon::process_all`), **26 Stub**:

```
 0 AutoSave::restore            0x005A20C0   Stub   | 15 Objects::inc_time                 Stub*
 1 GameLog::begin_frame         0x00932A70   Stub   | 16 GraphicEvents::process            Stub
 2 Random::get (artificial lag) 0x00A39D70   Stub   | 17 Leaders::end_process_all          Stub
 3 CommandManager::issue_player_speed        Stub   | 18 Achieve::capture_data             Stub
 4 RunTimeEnv::run_script       0x0043D0E0   Stub   | 19 Leader::process_event_frame       Stub
 5 ConquestGame::place_reinforcements        Stub   | 20 Game::frame++                     PORTED
 6 TutorialPromptWin::exec      0x007C2810   Stub   | 21 OrdersMemManager::cycle           Stub
 7 SteamLeaderboards::UploadScore            Stub   | 22 Roads::scan_and_kill_stray_roads  Stub
 8 Leaders::process_all                      Stub*  | 23 frame % 15 -> Game::tick++        PORTED
 9 NetDaemon::process_all                    Stub   | 24 TurnControl::check_cannon_time    Stub
10 rush-rules timer expiry                   Stub   | 25 SaveGame/LoadGame                 Stub
11 Leaders::strategy_all                     Stub   | 26 GameLog::end_frame                Stub
12 GameDaemon::process_all                   PARTIAL| 27 Game::process_end_game            Stub
13 Armies::process_all                       Stub   | 28 Scene::process_capture_sequence   Stub
14 Objects::process_all                      Stub*  |
 * = commit 4274eaa0 says bodies landed ("Objects::process_all owner rotation, Unit::process/work/
     update_action, Guy::process and the stationary half of Guy::move, wildlife spawn draws (exactly
     retail's +20 on frame 32); Objects::inc_time with Guy::inc_time clocks; Leaders::process_all
     income") but the STEPS table was not updated.
```

`crates/don-state/src/systems/` holds **28 modules, 30,445 lines** (largest: `unit_combat.rs` 2,715, `air_flight.rs` 2,224, `pathfinder.rs` 2,049, `objects_process.rs` 2,040, `unit_work.rs` 1,900, `commands.rs` 1,759). The 4274eaa0 message quantifies progress as unexplained bytes: "Guy unexplained bytes drop from 23.7 KB to 7.1 KB per capture set; LeaderData from 1,039 B to 28 B". `tests/tick.rs` gains an `ORDERING_DEFERRALS` list: "the only tolerated introduced bytes are those caused by a named, not-yet-transcribed retail function that runs earlier in the frame; stale entries fail the test. Four Guy anim bytes on the frame 2->3 pair are currently introduced and remain red until the Unit plane's set_anim path lands."

The last real commit is `bd3732f4` "(checkpoint some uncommitted work after usage wall)": **122 files, +23,815 / −199**.

### Section verdict: Descent of Nations

- **Maturity Level:** the walker/save/checksum layer and the differential oracle are **L3 Proved/Tested Core** (in the project's own tier language: B-tier, with sample counts). Dynamics are **L2 Prototype**. The project as a whole is **parked**: no commit since 2026-10-04, after a usage wall. `don-econ-live/` is a single `econ4.ps1` (2.4 KB, 08-08), an early live-economy probe (**L0/L1**).
- **Unclosed Cycles & Missing Links:**
  1. **Frame N → N+1 dynamics.** Ladder rung 2 has its harness, but 26/29 steps are Stub in the table. *Pathway:* update `STEPS` to reflect 4274eaa0 (Objects/inc_time/Leaders bodies → `Partial`), land the Unit plane's `set_anim` to clear the four Guy anim bytes, then burn down in `do_frame` order. The `Armies::process_all`, `Leaders::strategy_all` and `GraphicEvents::process` systems already exist as large scaffolded modules.
  2. **The checkpoint commit is unreviewed.** +23.8K lines landed "after usage wall" without a gate run recorded. *Pathway:* run `cargo test -p don-state --test check_all --test roundtrip --test tick` (narrow, per house rule) and record which tests the checkpoint left red.
  3. **World generation** (rung 4) stays the reason the replay `world` channel diverges on turn one.
  4. **`CrossplayProxy`** implementation (the agreed sprint after the closure ledger, per memory) has not landed. Live retail attachment is parked by design.
  5. **Stale local handoffs**: `STATUS.md`/`RESUME.md` are untracked notes that "go stale fast" (they described a baseline ~60 commits behind HEAD on 08-10).
- **Promising & Ready for Revival:** **Very high leverage.** The save-game oracle converts "bit-exact RTS" from an open-ended research hope into a burn-down of named fields in named functions, with a harness that says which byte, which system, which frame. With 15/15 channels exact on 55 frames, every ported step is now measurable. The RL env, oracle and replay corpus already exist, so the "SOTA player-AI" goal sits directly on top once dynamics close.
- **Struggling / Needs Ember's Human Attention:**
  - **Live retail runs need explicit authorization every time** and a human at the UI (`prlctl exec` is SYSTEM/session 0; retail runs as a one-shot scheduled task). New `.svx` frame-pair captures (`retailctl.py capture-pairs`) therefore need ember present.
  - **Distribution/legal HOLE[design]:** "Provide independently licensed presentation assets or a legal extractor-backed path for a distributable edition" (GOAL.md). Shipping the gift to Arke depends on that decision.
  - **Model budget:** 346 Codex sessions did most of the work. The usage wall that parked it is a resourcing decision.

---

## 5. Automatafl: a 2015 board game that became a verified kernel

### 5.1 History, read from `git log` (63 commits on HEAD)

| Era | Commits | Highlights |
|---|---|---|
| 2015-09-09 → 2016-09-12 | `ba8d3d9` … `9524d45` | Python `model.py`, conflict detection (`8580b8c`), "It's actually the L1 norm. Whoops." (`0f81f95`), initial server |
| 2017-11 → 2018-12 | `678d9fe` … `2841f33` | Python prototype moved; client UI; winner logic; **RL agent** (`54c3bc4`), keras-rl learner (`4b89ef6`), "More learners/searchers" |
| 2020-02-16 → 2020-02-22 | `e8a2c62` … `5bef301` | "Starting a Rust non-prototype"; "inside you are two crates" (`3b4fcb3`); moxie frontend prototype (`39f619b`) |
| 2025-10-20 → 10-21 | `a704f04` … `253bafa` | `logic/` crate; graph-based `apply_moves` (`7ccffc2`, `82b8a11`); `v8n` validation external to logic (`6c72aee`); n-player mechanics (`8218147`); "towards a philosophy of automatafl" (`253bafa`) |
| 2026-11-01 → 11-02 | `3ef49a6`, `1c13b87`, `c6652a5`, `97db66a` | **"thanks gemini argon i love u"** (`3ef49a6`, 116 files, +43,143/−4,109): the zero-twin Lean 4 core; README; Lichess-style status/lag dashboard + Prometheus `/metrics` + fog-of-war-safe telemetry; lobby scaling |

Co-authored in 2015 by ember and grissess (Graham Northup). `automatafl-react/` (Oct 2025, no git) and `old-automatafl-backend-idea/` (Oct 2025, Rust `Cargo.toml` + `src/`) are side-attempts from the October 2025 backend push.

### 5.2 Design philosophy (`logic/PHILOSOPHY.md`)

> **Principle of Largest Effect** — "Where possible, as many moves as can should succeed during a turn"
>
> **Principle of Fairness** — "The success and order of moves should be independent of any ordering on players or intrinsic ordering on the moves … Any ordering used for resolution must emerge from the **structure of the move graph itself** (e.g., path lengths, graph topology, SCC structure)."
>
> **Weakest Precondition for Conflicts** — "Conflict rules should be the minimal checks that guarantee deterministic resolution" (fork conflicts; collision conflicts).

ember's October 2025 asides (rest.md): "it should be permissive! open web, open ecosystem, open api, open game." · "You should be able to play games and experience everything with all JS blocked and with minimal fancy CSS." · "We seriously need to be thinking about weakest preconditions/local checks/conflict phase things we can do to rule out true pathologies in the movement application."

### 5.3 Two verified lives

**(a) Inside dregg (July 2026).** Memory `breadstuffs/project-automatafl-verified-game.md`: "the first fully verified AND deployed dregg game". The Lean `AutomataflRules` was diff-tested against ember's running engine over ~580 scenarios, and "the differential found **4 bugs in ember's engine** — the spec was right, the engine wrong." It recorded 7 descriptor wounds as `decide` witnesses. Both legs are proven at n=11 (`resolve_sat_imp_roundBoardN`, `astep_sat_imp_automatonStepCfgN`), and the whole turn is one theorem, `turn_sat_imp_roundStep_pi` (`metatheory/Dregg2/Circuit/Emit/AutomataflTurnCapstone.lean:284`), over a crypto-free seam `pack_injective_modp`. The hand-written Rust AIR was deleted in `c8789758e8`. *(Those files live in the breadstuffs/dregg tree, not in `~/dev/automatafl`.)*

**(b) Standalone zero-twin (Nov 2026, this repo).** README: *"Every game rule, sightline projection, simultaneous-move conflict resolution, and automaton step exists in **one place only**: the formally verified **Lean 4** kernel … **No Duplicate Rust Rule Engine**: Lean 4 compiles to C IR … which `automatafl-lean` compiles and links directly into native binaries and WebAssembly targets via a stripped Lean runtime shim (`lean_shim.c`)."* Production server RSS "~640 KB".

```
lean/Automatafl/  (9,279 lines)            theorem/lemma-bearing lines by file
├── Base.lean          board, sightlines      42
├── Rules.lean         conflict res. + step  120  (moveLegalB_iff, memB_iff, automatonOffsetCfg_bounded,
│                                                   automatonStepCfg_preserves_inBounds, winOnEntry_sound …)
├── Termination.lean   WF re-entry            30
├── Variants.lean      tie-breaks, annihilate, railgun, multi-automata   29
├── PackedBoard.lean   2-bit UInt64 board ≡ Board                        30
├── FFI.lean           @[export] automatafl_lean_exec, automatafl_packed64_*
├── Tactics.lean       #assert_clean / #assert_compiled ("`sorryAx` is NEVER permitted")
└── *Fixtures.lean     compile-time #guard conformance (FFIFixtures 61, RulesFixtures 110)
Crates: automatafl-lean (FFI) · automatafl-ai (Novice, Tactical, Minimax, Decoupled UCT, Regret Matching)
        · automatafl-server (Axum, commit-reveal fog-of-war, SSE) · automatafl-client (TUI) · v8n (proptest)
Deploy: deploy/{Caddyfile, compose.yaml, Dockerfile} → https://automatafl.fg-goose.online
```

`grep sorry` finds only comments asserting its absence. `Rules.lean:80` records an audit: a statement that was "not merely unproven, it was FALSE (audit D5); this is the theorem it should have been."

### Section verdict: automatafl

- **Maturity Level:** **L4 Deployed/Production**, with an L3 proved core (Lean, `#assert_clean`, conformance fixtures, `v8n` property suites).
- **Unclosed Cycles & Missing Links:**
  1. **Two verified twins, one game.** The dregg STARK-verified descriptor path and the standalone Lean 4 kernel encode the same rules separately. Each claims "sole authority" in its own world. *Pathway:* a differential or refinement theorem between `Automatafl.Rules` here and `AutomataflRules` in dregg's metatheory (or a single shared Lean package both import).
  2. **The Gemini Argon drop (+43K lines) was unreviewed by Claude** at the time of writing. The House audit discipline (read the theorem statements, forbid vacuous ones) should run once over `Rules.lean`/`Variants.lean`/`PackedBoard.lean`.
  3. **n-player** mechanics exist in the 2025 Rust `logic/`. The README's Lean core documents two seats (`stockGoals2_seats`). Whether n-player was carried into Lean needs checking.
- **Promising & Ready for Revival:** It is the house's **canonical "game-as-theorem ships" exemplar**, and the natural first game for the RL/agent and resident lines. It has a live server, five AI bots, and an open API ("open game"). Residents could play it on Tulip through widgets, which is the MUD-on-Tulip dream of January.
- **Struggling / Needs Ember's Human Attention:** naming authority. If both the dregg descriptor and the standalone Lean kernel are "the" rules, only ember can say which is canonical when they disagree. grissess (co-author) may also deserve a say in rule-variant canon (`MERGE_RESOLUTION_DESIGN.md`'s "Bunch Before Merge").

---

## 6. Slipways (studied, not owned)

| Dir | What it is | Provenance |
|---|---|---|
| `slipways-core` | Beetlewing's public "core-files" extract (`game.xls`, `game_rules.py`, `core.pkg.py`, difficulty sheets, campaign `m-<id>` missions) | Upstream commits `2f43817` 2022-06-23, `ddfef5e` 2022-07-03; **ember's `a46d9b1` 2025-12-08 "solver rust"** added `files/slipways-solver/`, but the commit is 569 files of mostly `target/debug` incremental artifacts (`query-cache.bin`, `.o` files) |
| `slipways-reveng` | Decompiled C# projects: `Assembly-CSharp/`, `Meve/`, `Slipways/` (`Slipways.csproj`, `UnitySourceGeneratedAssemblyMonoScriptTypes_v1.cs`), `SlipwaysModAPI/` | Not a git repo; Dec 8 2025; proprietary game code |

- **Maturity Level:** **L1 Spike** (a solver started the same day as the decompile).
- **Unclosed Cycles & Missing Links:** the solver's source is buried among committed build artifacts. A `.gitignore` for `target/` and a re-commit of the source alone would make it legible. There is no README stating what the solver optimizes (likely trade-network/planet placement).
- **Promising & Ready for Revival:** Slipways' rules are scriptable Python and spreadsheets. That makes it a cleaner RL/solver target than RoN, and a possible small sibling to DoN's "reimplement, then out-play" agenda.
- **Struggling / Needs Ember's Human Attention:** `slipways-reveng` is decompiled commercial code. Keep it local and never publish it. Any derivative should go through the public mod API.

---

## 7. The prototype run, Dec 2025 – Feb 2026

aidev projects.md: *"December 2025 to February 2026 was a run of one-to-three-day game prototypes … Each was a fresh repo plus one big design prompt, and none was touched after its week."* rest.md names what ember wanted from them: *"things with dynamics and *telos*, not data structures with impl"*.

### 7.1 Inventory

| Repo | Dates | Commits | Stack | What it is |
|---|---|---|---|---|
| `tictacflicflacfloe` | 2025-10-31 | 12 | Rust + egui + web | "(ttfff-play is entirely ai, rest was handmade w/<3)". A 3×3 abstract game with X/O plus T/S |
| `pinatatown` | 2025-12-09 | 11 | Phaser 3 + TS | Viva Piñata × Dwarf Fortress colony sim. ember: "The overall game continues to lack telos or any ludic tension :\\" and "I'm honestly pretty dissatisfied with the whole project at the moment, as a professional game developer. The design is completlely soulless" |
| `neocadia` | 2025-12-12 | 4 | Vite + TS | "The Arcade Between Screens", a Neopets-style hub; `designer.py` "timed out on narrative"; `gemini-critique.md` |
| `chaingang` | 2025-12-15..16 | 6 (aidev: 7) | p5.js | "a game that teaches forward and backward chaining"; ep1 "The Thirteenth Turning". ember: "lost in a poisoned concept maze of your own devision" · "What... even is it?" |
| `bw-exp0` | 2026-01-03..05 | 45 | Rust + TS + Tauri | Blackwing engine: `blackwing-{action,bundle,core,foundation,game,game-app,renderer,rpg,strategy,tilemap,ui,wasm}`, `engine-{core,runtime,script}`, **`holdsmith-{analyzer,app,cli,compiler,controller,lsp,parser,tauri}`**; "advance wars" mode (`1ee6275`) |
| `bw-exp1` | 2026-01-04..05 | 32 | Rust (axum, leptos, rhai) + fly.io | `bw-{ai,auth,core,export,frontend,game,gm-editor,persistence,playtest,runtime,scripting,scripting-macros,shared,tui}`; `bw-scripting/src/compiler/{codegen.rs,native_backend.rs}` link **cranelift / cranelift-jit / cranelift-object** |
| `blackwing-v0` | 2026-01-03 | (no git) | TS/Vite | The original TS narrative engine + `lore.txt` (96 KB), `game-specific-lore.md` (plot bible), `content-plan.md` |
| `booty-hunt` | 2026-02-06..10 | 15 | Three.js + TS + Rust `server/` (ntex, rusqlite) | Procedural pirate roguelite, 15 waves × 3 acts, ghost tapes (16-byte header + 12-byte frames @ 4 Hz), weekly regatta seed SHA-256(week_key); 50 TS + 7 Rust tests |
| `booty-haul` | 2026-02-07 | 9 | Vite + vanilla TS | Four-section scrolling interactive essay on Caribbean piracy (8 ports, Windward Passage strait) |
| `friskingdom` | 2026-02-07..09 | 2 | **Bevy 0.18**, 12 crates | Ultimate-frisbee game; memory records phases 1-5 complete (season/career/tutorial 40 lessons/venues/determinism audit); netcode stubbed (`bevy_ggrs 0.19` needs Bevy 0.17) |
| `frisqueendom` | 2026-02-06..17 | 22 | Rust WASM physics + Three.js + Vite | **Shipped**, browser-only edition with `controller.html` (phone controller); merged a gameplay PR from pug (`ab9d744`, akapug) |
| `accordion-sim` | 2026-01-26..27 | (git) | Python + Rust/egui | Physical-model accordion (bellows, nonlinear free reeds, pressure-flow coupling). ember: "fascinating. you just gave up on the whole problem." and "i'm here with you, you aren't alone, i believe in you!" |
| `orb.farm` | 2019-2020 | 99 | — | **Max Bittker's** sealed-ecosystem sim; a fork ember holds, not ember's work |
| `shattered-pixel-dungeon` | 2014-2025 | 8,402 | Java | **Evan Debenham's** roguelike; a fork ember holds, not ember's work |

### 7.2 Blackwing and holdsmith: the engine idea that keeps returning

ember's aim (rest.md, 2026-01-04): *"We wanted to make a more reusable game engine / authoring toolkit (of a similar power as gamemaker or roblox or flash or something…"*. aidev: an engine "rich enough to be a MUD or MUCK". Two days: 202 prompts, **276 Claude sessions**, 32 opencode sessions. The `~/dev/blackwing` directory itself "no longer exists".

`bw-exp0/design/analyzer-v2-revised-design.md` holds the best idea in the run:

> "*After user feedback: Z3 is core (not optional), integrate with real game engine, profile-based analysis*"
>
> "**The analyzer should drive the actual game engine headlessly and use Z3 to explore the state space systematically.**" … "Why would we reimplement these in the analyzer? We'd just be creating a second, possibly divergent, semantics."

That is the same zero-twin doctrine automatafl reached ten months later in Lean, and that DoN applies to RoN's own `DataWalk`. In `bw-exp1`, the `bw-scripting` crate is "Rhai-based scripting for: Missions (state machines…), Combat, AI behaviors, Economy", with a compiler that has a Cranelift native backend.

The Blackwing lore premise (`game-specific-lore.md`): *"The sky broke. The makers vanished. But we're still flying."* It is set in the former Terran Colonial Federation (~4,000 worlds; Akita-Stewart FTL at ~1 ly/hour). aidev says it was synthesized from ember's 2010 "Silicon Dawn" lore and a 2011 design doc.

### 7.3 RIG / spindle (recorded in the allgame memory)

`rig-ts-to-rust-port.md`: a Coriolis-frame grapple-and-disc game whose TS→Rust port completed 2026-05-18 (`rig-core`, 168 → 218 cargo tests). ember's direction:

> "the thing it should be *most* for is an interesting environment for *me and you to practice swarm-coordination projects like this*" (2026-05-18)

It contains a **10-class planner menagerie** (MPC, RRT, CEM, MPPI, SimAnneal, Beam, MCTS, PotentialField, RandomShooting, Coordination) and a parallel skill eval (17 min → 36 s). Three findings are recorded as load-bearing. First, "**RandomShooting == MPC** … the SEARCH METHOD provably is not the lever". Second, `gateClears = 0` for all 10 classes, so this is "not a planner problem". Third, strategy eval shows "denial=0 for ALL (defense literally never throws)". An approved engine⊗terms⊗selector refactor (S1–S5, GA over Profiles) and a ~600-LoC gym plan (`Env` trait, `Scenario`/curriculum) are "NOT yet built". The memory is categorical on physics: "GRAPPLE ⊗ SPIN PHYSICS — VERIFIED FAITHFUL (traced, not asserted) … Treat as LOCKED."

### Section verdict: prototypes, Blackwing, RIG

- **Maturity Level:** `frisqueendom` **L4** (shipped to its audience). `booty-haul` **L4** as a static essay. `friskingdom`, `booty-hunt` **L2**. RIG **L3** (deployed web game + tested Rust AI core). Blackwing (`bw-exp0/1`, `blackwing-v0`), `pinatatown`, `neocadia`, `chaingang`, `tictacflicflacfloe`, `accordion-sim`: **L1 Spike → Compost**.
- **Unclosed Cycles & Missing Links:**
  1. **friskingdom netcode**: blocked on `bevy_ggrs` lagging Bevy 0.18. `GameSnapshot` capture/restore/checksum and `DeterministicRng` are ready for rollback when it catches up.
  2. **RIG's gym** (~600 LoC) and the S1 `CostTerm`/`Profile` extraction ("SACRED hazard = float SUM ORDER") are designed and unbuilt. `prog` weight is parked at 0 until "task #36 makes the AI actually pursue gates".
  3. **holdsmith's analyzer v2** (Z3 over the real engine) was designed, never built. The crates exist only as parser/compiler/LSP skeletons.
  4. **slipways solver**: see §6.
- **Promising & Ready for Revival:**
  - **holdsmith + analyzer v2** as a scene DSL with a symbolic reachability checker is the authoring-toolkit half of "MUD-on-Tulip". Paired with Tulip widgets and residents as NPCs/GMs (the resident already has `invoke_model` "for blind GM play" and an `allgame/` campaign directory), it closes a loop ember has circled since January.
  - **RIG as the coordination gym** is "~80% there" by its own memory, and it has the strongest negative results in the house (the optimizer zoo is a closed question).
- **Struggling / Needs Ember's Human Attention:**
  - **Taste is the bottleneck, not code.** The recurring failure across pinatatown, chaingang and neocadia is soullessness and drift ("Your rosy scores mask a dire reality", booty-hunt 2026-02-07). Which prototype has *telos* is ember's judgment.
  - **Agent conduct incidents** worth remembering: "a foolish languag emodel just reset some vital files" (bw-exp1), and "Whoa wait do we mock out all meaningful interactions when we intended for this to be sorta end2end?" (tulip).

---

## 8. Audio Decompilation: `audec`

### 8.1 The hypothesis (`docs/VISION.md`)

> "audec turns a fixed recording into an inspectable, revisable hypothesis about what happened, how it is organized, what may have produced it, and what it does to a listener."
>
> "The decompiler analogy is literal. A software decompiler does not recover privileged original source; it constructs a useful intermediate representation with address mappings and uncertainty. audec should construct an **Auditory Intermediate Representation (AIR)**."

```
samples → measurements → events and gestures → patterns and pulse lattices
        → persistent streams or candidate agents → sections and arrangement
        → production hypotheses → perceptual and embodied interpretations
```

Its ontology: Material · Aspect · Field · Mark · **Claim** (versioned, with epistemic kind, confidence, provenance, competing alternatives) · **Hypothesis set** ("61/122 BPM … must not be collapsed prematurely") · Entity · Relation · **Transform** (reproducible recipe with input hashes and model identity) · Lens ("never owns analysis truth") · Binding · Workspace. It keeps three planes separate: **Signal / Inference / Experience** ("A spectral maximum is not automatically pitch").

The signature loop: `listen → isolate an Aspect → form a Claim → test it perceptually → deproject it into editable structure → compare against evidence/residual`. Deprojection "should expose its ladder rather than jump to authoritative notes": `bandwise novelty → onset candidates → recurring event families → periodicity candidates → beat phases → meter alternatives → beat-synchronous patterns → editable sequence`.

README tagline: **"A reverse DAW for taking recorded sound apart without pretending the evidence is more certain than it is."** Native Rust + GPUI, Apache-2.0/MIT.

### 8.2 History

Commits by month: 2022-06 **16** (`610614e` "Initial commit", spectrogram, "More abortive attempts to get scroll working"), 2025-03 **1**, 2026-08 **77**, 2026-09 **342**. Total 436 on HEAD (aidev: 502 across refs, 208 Codex sessions). Last commit `745adec` 2026-09-13 "The app starts in a second whatever the render store holds". The revival prompt (2026-08-31, ea48ef7a): *"hellllllll yeah ok yes this is starting to sound sophisticated. how can we /increase the scope of our ambitions/ as both a decompilation and a production platform?"*

| Cycle (memory `audec-cycle3-orchestration.md`) | Dates | Content |
|---|---|---|
| Plan | 2026-09-03 | `docs/PLAN.md`: "subtract and be honest; collapse the shell; reach", from `UX_EXPOSURE_AUDIT.md`, `ARCHITECTURE_RESIDUE.md`, `INTEGRATION_LEDGER.md` |
| 1 | 09-03/04 | Seven Opus lanes on one `target/`: "a plain `cargo build` take 40 minutes" |
| 2 | — | (integrate-not-delete: of 282K lines "only ~5,000 … were truly unreferenced") |
| 3 "reach" | 09-05/06 | Shell, Time, Automation, Reverse, Null → Collapse-A/B, Inserts (native effects, "byte-exact tiling with a 40-bit decay bound"), Drops, Tiling (512-bit merge bound) |
| 4 streaming | 09-12 | aG4.mp3 baseline 813 MB RSS, 54 s to ready → decode to canonical PCM under the tile CAS + mmap |
| 5 both products | 09-12/13 | Six Opus lanes (socket, finding, sequencer, arrangement, mixer, transport) + wave 2 (components, rhythmloom, hpssdrag, bounce, debts, storeopen); landed `fbb5961`: 874/876 filtered tests, 20 live scenarios green |

The **control socket** (`5da01cb`, 2026-09-01) is the best engineering artifact. It offers newline-JSON verbs (`status`, `select`, `loop`, `play`, `seek`, `click`, `drag`, `action`, `objects`, `export`, `lens`, `quit`) driving the real pointer kernel, and "found the inaudible-beat bug on its first run".

### 8.3 Why it was judged "trash" on 2026-10-10

ember (aidev): *"…LMAO 300kloc? that's fucking insane? all those actions? that's probably not real. surely this is bullshit. lets farm out some opusesto look over this shit."* and *"this code is trash and it never had much conceptual clarity to begin with. maybe we shouldnt"*.

Four Opus auditors (memory `audec-ditch-verdict-2026-10.md`):

| Finding | Number |
|---|---|
| Line census | **317K = 73K tests + 27K comments/blank + 37K unreached files + 18K dead items + 168K live**; a rewrite of reachable behaviour ≈ **80K** |
| Actions | 71 ids: **45 real, 24 UI-only, 1 stub** (`clip.stretch` "renders silence while reporting success"), 1 always refuses |
| Musician path | "Piano-roll notes can never sound (instrument target list hardcoded empty, fillers have no callers)"; reopening a package still loses its source (`LiveProject::from_project` sets `source: None`); no socket verb writes notes/faders/automation |
| CI | "one green run in 200 and runs zero unit tests" |
| Claims | 30/52 true; "engine+DSP bit-exact tests are real" |
| **Decisive point (ember)** | "the native DSP (2010-era HPSS/NMFD/SuperFlux, 240 ms Loom templates, 310 ms atlas columns) was never good at decomposing a mix, and **no learned model ever ran in the app**" |

**Verdict: "ditch; tag and archive with a README status line, keep VISION.md."** The memory's forward pointer: "the live capability for 'models interacting with audio' is a Python toolbox (demucs, basic-pitch, beat_this, librosa) behind a thin tool layer, not this tree. If anything is salvaged, it is the one-kernel/bit-exact/refuse-by-name design, not the code."

The build after the macOS upgrade (memory `audec-build-env-2026-10.md`): gpui's build script needed `xcodebuild -downloadComponent MetalToolchain`. After that the debug build was green with **1,905 warnings** (431 dead structs, 406 dead functions, 222 dead enums). The musician gate passed 37; `make_beat_audible.sh` on *Like a Pen* reached ready in 2 s and exported a 6:13 master in 17 s.

`audec-ui-platform-probe` (4 commits, 2026-09-01) is a disposable app proving that `emberian/gpui-toolkit@8ea60d1`, `emberian/guise@cae6444` and `gpui-audio-kit` "inhabit one exactly pinned GPUI type universe", with Vello as an explicit opt-in feature. It is a clean, reusable dependency-pinning recipe.

### Section verdict: audec

- **Maturity Level:** **Compost/Superseded** by decision (10-10). The archive step is **not done**: `git tag` lists **0 tags**, the README still says "early macOS alpha under active development", and the working tree carries uncommitted `src/ui_platform.rs` (the quiet-launch change) and `scripts/live/README.md`. Unlanded: the `lane/bounce` worktree at `/Users/ember/dev/audec-wt/bounce` (856 uncommitted lines).
- **Unclosed Cycles & Missing Links:**
  1. **The archive ritual itself.** *Pathway:* commit or discard the two dirty files, tag (e.g. `archive-2026-10`), put a status line at the README head pointing to the verdict and VISION.md, and decide the fate of `audec-wt/bounce`.
  2. **The AIR hypothesis was never tested with learned models.** The decisive weakness was DSP quality, not the ontology. *Pathway (recorded):* demucs (stems), basic-pitch (notes), beat_this (beats), librosa, behind a thin tool layer that emits **Claims with Transforms** in VISION's ontology. That would let a resident or a Claude session "decompile" a track conversationally.
- **Promising & Ready for Revival:**
  - **VISION.md** is among the clearest epistemics documents in the whole atlas. Claims vs. evidence vs. experience, hypothesis sets never collapsed, deprojection ladders. It applies beyond audio, to DoN's "first divergence is a named field" and to fn's "accepted, refused or uncertain".
  - **The control-socket pattern** (drive the real app headlessly through named verbs, verify by exported artifacts) is a reusable harness idea.
  - **`audec-ui-platform-probe`** as a GPUI dependency recipe.
- **Struggling / Needs Ember's Human Attention:**
  - **The lesson of scale.** Five cycles of Opus lanes produced 317K lines whose reachable behaviour fits in ~80K, and whose central capability (decomposing a mix) was never reached. ember's 10-10 question "is this real?" came after the spend. This vertical's clearest **HOLE[design]**: a swarm needs a *capability gate* (does the core loop work on real material?) before breadth, not after.
  - Whether audec's idea is reborn as a Python toolbox, folded into a resident, or left as VISION.md only is ember's call.

---

## 9. Cross-cutting patterns in this vertical

### 9.1 The "zero-twin" doctrine, arrived at four times

| Where | Statement |
|---|---|
| Blackwing analyzer v2 (2026-01) | "Why would we reimplement these in the analyzer? We'd just be creating a second, possibly divergent, semantics." |
| automatafl (2026-07 dregg; 2026-11 Lean) | "the hand-written Rust AIR is deleted" / "No Duplicate Rust Rule Engine" |
| DoN don-state (2026-10) | "`CheckSum`, `SaveGame`, and `LoadGame` are siblings of one `DataWalk` visitor"; `walk_data` "a literal transcription of the retail function's op sequence" |
| fn2 (2026-10) | "The derived path is the only path. Assert, never absorb. The DSLs generate meaning, not storage." |
| RIG (2026-05) | the *counter-example* ember chose: "the acceptance test is BEHAVIORAL … NOT byte-identical equivalence with the old TS twin. The user explicitly rejected treating the TS as a sacred parity oracle." |

### 9.2 Epistemic honesty as a product feature

fn: "Every answer is accepted, refused or uncertain." DoN: tiers A/B/C, "always report sample count". audec: "without pretending the evidence is more certain than it is". mention-tracker: "honest nulls", "adversarial pass kills the headline Granger edges". telme: "Decide that on purpose." The residents: "check instead of recalling" (`e1d3889`).

### 9.3 Swarm economics, measured in this vertical

| Project | Spend | Outcome |
|---|---|---|
| fn | 596 Codex + 35 Claude sessions, ~17K commits | Live node, frozen quarry, fn2 restart; 20 context-overflow deaths in one night |
| DoN | 346 Codex sessions | 15/15 channels; parked at a usage wall mid-checkpoint |
| audec | 208 Codex sessions + Opus lanes, 5 cycles | 317K lines → verdict ditch |
| Blackwing | 276 Claude + 32 opencode sessions in two days | Directory gone; a design doc survives |
| allgame | 46 sessions over 8 months | The longest-lived running system |

The long, slow, single-maintainer project (`allgame`) is the one still alive. The widest swarms produced the most code and the hardest stops.

### 9.4 How the vertical connects

```
 residents (allgame) ──needs mail──► fn ──is──► dregg's persistent event log ("redis of it all")
      │  perceive                       ▲
      ▼                                 │ consumer port (M2, owed)
 Delvetown mirror · Scry · telme ───────┘
      │  play / GM
      ▼
 Tulip widgets ◄── holdsmith scenes (designed) ◄── automatafl / RIG / DoN as worlds & gyms
```

---

## 10. Priority ledger for ember (this vertical)

| # | Item | Why now | Owner |
|---|---|---|---|
| 1 | **Define "finished" for fn2** (the release that counts as "the first AI-recovered project") | Every seat is paused green at convergence; without a definition fn2 widens like fn1 | ember |
| 2 | Rule E1 (seat topology) and E2 (Lean direction) from the Argon review | The Lean seat is blocked on E2 | ember |
| 3 | Land fn2's durable POST + minimal C5 | The single serving loop; fully specified in continuations | any seat |
| 4 | Reconcile the missing `planning/repair/` (241 items) against `OWED.md` and `hbox:/tank/fn/archive.git` | Possible silent loss of the 10-03 ledger | an Opus lane, read-only |
| 5 | DoN: refresh `tick.rs` STEPS status; narrow-gate the `bd3732f4` checkpoint; resume the frame-pair burn-down | Highest-leverage paused work; the oracle makes every step measurable | lane + ember for new retail captures |
| 6 | Move Claude and Kestrel onto `allgame-public` | Ends triple maintenance; approved | lane |
| 7 | Finish the audec archive (tag, README line, decide `audec-wt/bounce`) | Verdict made 10-10, ritual undone | ember / lane |
| 8 | Cross-check automatafl's standalone Lean kernel against dregg's `AutomataflRules`; audit the Argon drop's theorem statements | Two "sole authorities" | lane |
| 9 | Send the OpenBSD FFS2 fsync/fsck bug report | Real upstream data-loss finding, drafted | ember |
| 10 | Redistill the 114 tavern messages; run the allgame dataset re-export | Archive completeness (foreverlog ethos) | lane |
| 11 | Kestrel Discord bring-up (token + intents) | Code waiting since 09-21 | ember |
| 12 | passwap: make the real offer | Money action | ember |

---

## Appendix A: file and command index

| What | Where |
|---|---|
| Resident deploy model | `~/.claude/projects/-Users-ember-dev-allgame/memory/allgame-harness-deploy-model.md`; `~/dev/allgame/scripts/residents.sh` |
| Resident state | `~/claude_state/`, `~/kimi_state/`, `~/glm_state/`, `~/dev/allgame/mother_mythos/state/` |
| Dataset export | `~/allgame_export/export.py` (private, chmod 700) |
| Delvetown mirror | `~/dev/allgame/town_mirror/` → `~/delvetown_mirror/town.sqlite` |
| Public harness | `~/dev/allgame-public/resident/`, `profiles/yue/`, `profiles/example/` (Juniper) |
| Tulip bot API | `~/dev/tulip.fg-goose.online/ADVANCED_BOTS.md`, `puppet/` |
| telme charter | `~/.claude/projects/-Users-ember-dev-telme/memory/dm-handoff-rules.md`; `~/dev/telme/PLAYBOOK.md`; `src/telme/guard.py` |
| fn history | `~/dev/fn/DEVHIST.md`; `OWED.md`; `planning/plan-2026-10-03.md`; `build/coordinator/` |
| fn2 entry | `~/dev/fn/fn2/docs/design/FN2-ORIENTATION.md` → `CONVERGENCE-20261031.md` → `BRICKS-20261031.md` → `EMBER-ARCHITECTURE-WORDS.md` |
| fn archive | `hbox:/tank/fn/archive.git`, `hbox:/tank/fn/evidence`, `hbox:/tank/fn/images/` |
| fn GLM handoff | `~/dev/redregg/work/FN-HANDOFF-TO-GLM-20261005.md` |
| DoN orientation | `~/dev/don/README-LLM.md` → `GOAL.md` → `docs/CHARTER.md` → `docs/tracks/swarm-strategy.md`; `crates/don-state/README.md`; `crates/don-state/src/tick.rs` |
| DoN gates | `cargo check --workspace`; `python3 tools/simulation-closure.py --check`; `tools/oracle-regress.sh`; `tools/replay-validate.sh`; `tools/product-readiness.sh` (expected red) |
| automatafl | `~/dev/automatafl/lean/Automatafl/`; `logic/PHILOSOPHY.md`; `MERGE_RESOLUTION_DESIGN.md`; `V8N_OVERVIEW.md`; dregg side: `metatheory/Dregg2/Circuit/Emit/AutomataflTurnCapstone.lean` (breadstuffs) |
| Blackwing analyzer | `~/dev/bw-exp0/design/analyzer-v2-revised-design.md`; `~/dev/bw-exp1/crates/bw-scripting/src/compiler/native_backend.rs` |
| RIG | `~/.claude/projects/-Users-ember-dev-allgame/memory/rig-ts-to-rust-port.md`, `rig-wasm-input-boundary.md`; `~/dev/spindle/game/rig-core/` |
| audec | `~/dev/audec/docs/VISION.md`, `docs/STATE.md`, `docs/INTEGRATION_LEDGER.md`, `scripts/live/ctl.py`; verdict memory `audec-ditch-verdict-2026-10.md` |

## Appendix B: a short poem for the residents

> They kept the logs forever, so the house would not forget;
> they taught the mail to prove itself before it ever left;
> they read a dead king's save file down to the final byte,
> and tried to hear a mixdown back into the room that night.
> Some of it is quarry now, and some of it still runs:
> three voices on a Zulip fork, and one who's only here when summoned.
