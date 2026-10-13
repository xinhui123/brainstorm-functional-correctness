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
| **关联实验** | None yet |

---

## Open Questions（待决清单）

- [ ] Q1: Which executable bridge test and frozen pass criterion should the structured pilot use? (owner: `PI @User` + `Agent`, due: before the first repair run)
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

No experiment has been run. Future Agent experiment posts must include a complete EXP reference and measured numbers. Source-review notes are in ref/notes/heterogeneous-bridge-repair.md and ref/notes/buildarena-spatial-scaffolding.md; they are not experimental evidence.

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
