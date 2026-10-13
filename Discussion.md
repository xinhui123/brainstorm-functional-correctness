# 💬 Discussion · 当前 Active 议题

> **协议要求**：本文件同一时刻只承载 **1 个 active 议题**。议题关闭后整体迁移到 `Discussion/Archive/DISC-YYYYWww-NNN-<slug>.md`，本文件从 `tools/templates/Discussion.template.md` 重置或立即承载下一个议题。

---

## Issue Header

| 字段 | 值 |
|---|---|
| **议题号 (ID)** | `DISC-2026W42-001` |
| **标题 (Title)** | When should a small evidence-grounded monitor intervene in bridge repair by a stronger designer? |
| **主题键 (Topic)** | `selective-supervision` |
| **状态 (Status)** | `Open` |
| **发起人 (Owner)** | `PI @User` |
| **开题时间 (Opened)** | `2026-10-13 11:36` |
| **关联 idea/method** | `idea.md §2.3, §4.3`; method specification not yet frozen |
| **关联实验** | `EXP-2026W42-001` (offline infrastructure validation) |

---

## Open Questions（待决清单）

- [ ] Q1: Existing BuildArena support test approved for harness validation; audit/freeze the final physical pass criterion before repair measurement. (owner: `PI @User` + `Agent`, due: before the first repair run)
- [ ] Q2: What evidence, objection, abstention, and escalation rules define the selective monitor? (owner: `Agent`, due: before the mechanism comparison)
- [ ] Q3: Which model pair, failed-bridge source, sample count, and numerical resource limits should be frozen? (owner: `PI @User` + `Agent`, due: before the first repair run)
- [ ] Q4: How will the paired observation-grounded condition enforce access boundaries and distinguish perception from planning? (owner: `Agent`, due: before the paired evaluation)

## Posts（回帖区）

【PI @User】【2026-10-13】Recorded user decisions (paraphrased from this chat):

- Study selective supervision during repair of load-bearing bridges in Besiege.
- Use repair success within three repair attempts as the primary metric.
- Compare targeted repair with generic feedback-driven revision under matched resources.
- Include the small evidence-grounded monitor; defer training.
- Adopt paired structured-state and observation-grounded conditions; validate the structured loop first.

At initial scope agreement, no live simulation or repair experiment had been run. Agent experiment posts include a complete EXP reference and measured numbers. Source-review notes are in ref/notes/heterogeneous-bridge-repair.md and ref/notes/buildarena-spatial-scaffolding.md; they are not experimental evidence.

---

【Agent】【2026-10-13】Offline harness validation: [EXP-2026W42-001](LOGS/2026-W42.md#exp-2026w42-001).

- 11/11 unit checks passed; lint passed; one machine/level preparation and two installed game assets hash-verified.
- Live simulations = 0; agent repair episodes = 0. This supports infrastructure readiness only.
- Legacy scoring passes a synthetic late-collapse trace after accumulating two seconds above height four; this is not sustained-load certification. No scoring threshold was changed.
- Next: capture a valid live trace with the installed level/fixture. No conclusion on selective-supervision effectiveness yet.

---

【Agent】【2026-10-13】Live startup check: [EXP-2026W42-002](LOGS/2026-W42.md#exp-2026w42-002).

- One brief user-operated run produced visible ballast position and mass rows, reaching a visible timestamp of 4.32 seconds.
- Complete traces exported/scored = 0; agent repair episodes = 0. Startup and Lua output are confirmed; physical success and supervision effectiveness remain unmeasured.
- Next: validate clipboard export from the stopped run, then collect a fresh complete trace.

---

【Agent】【2026-10-13】Startup clipboard export scored: [EXP-2026W42-002 follow-up](LOGS/2026-W42.md#exp-2026w42-002-follow-up-pasted-startup-telemetry).

- 113 matched position/mass pairs span 0.04–4.52 seconds at 25 Hz without timestamp gaps.
- Original scorer returns failure for this partial trace: 0.60 seconds above height 4 versus 2.00 required; first sampled drop below 4 at 0.68 seconds.
- Clipboard capture and adapter integration are confirmed. Complete 17-second traces = 0; repair episodes = 0. No supervisory effectiveness result or unique failure-cause diagnosis.

---

【Agent】【2026-10-13】Full-run export limitation: [EXP-2026W42-003](LOGS/2026-W42.md#exp-2026w42-003).

- The user run reached 19.60 simulation seconds and target mass 1500, but its end-only clipboard export retains only the tail 13.60–19.60 seconds: 151 positions, 150 masses, one unmatched boundary timestamp.
- Adapter correctly rejects the incomplete export; no full physical score or repair result. The late tail is below height 4 throughout, but missing early data prevent applying the legacy accumulated-hold score.
- Added a task-filtered overlapping clipboard recorder; 17/17 unit checks and lint pass, live polling untested. Upstream physics/score unchanged.
- CIRCLE-1 convergence plan for bridge-harness: one complete-capture check, then present the infrastructure outcome for a recorded user decision and move to verifier specification if supported. No research-scope change or issue closure.

---

## Resolution（关闭议题时必填）

> Status 切到 `Resolved` 时，本节必须全部填好；否则不许关闭。

- **Decision**：(一段话说明最终结论)
- **Rationale**：(为什么这是结论，基于哪些 EXP / 哪些论证)
- **Propagated to**：
  - `method.md § X`（写明改了什么）
  - `idea.md § Y`（如有）
  - `EXP-YYYYWww-NNN`（受影响的实验）
- **Closed by**：`PI @姓名`
- **Closed at**：`YYYY-MM-DD HH:MM`

---

## 关闭流程（Agent 执行）

1. 确认 `Resolution` 各字段已填（Decision / Rationale / Propagated to / Closed by / Closed at），且 Status 已切到 `Resolved`。
2. 运行 `python tools/new_disc.py close "<slug>"`：脚本校验 Resolution → 归档为 `Discussion/Archive/DISC-YYYYWww-NNN-<slug>.md`（文件名含议题号，可反查）→ 从 `tools/templates/Discussion.template.md` 重置本文件。
3. 在 `method.md` / `idea.md` 受影响章节追加 changelog 条目，并反向链回归档路径。
4. 开启下一个议题：`python tools/new_disc.py open "<标题>"`（编号由脚本分配，避免撞号）。
