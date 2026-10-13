# Research Idea: Selective supervision for physics-grounded bridge repair

> Agreed research scope after the one-question-at-a-time ideation interview, 2026-10-12–2026-10-13. Implementation details remain open where explicitly stated. No performance result or novelty claim has been established.

## 1. 核心概述 (The Essence)

- **一句话总结 (One-Sentence Summary):**
  > Study when a small evidence-grounded monitor should intervene, request evidence, abstain, or escalate while a stronger model repairs load-bearing bridges in Besiege, evaluating repair success within three attempts under paired structured-state and observation-grounded conditions.

- **一段话摘要 (One-Paragraph Abstract):**
  LLM-built structures can satisfy construction rules and still fail their intended physical function. We will study selective supervision of bridge repair: a larger model chooses structural changes, a smaller monitor audits available evidence and execution, and a fixed simulator test determines success. The first pilot validates the loop with structured state; a subsequent paired condition restricts access to observations and permitted measurements. We will compare diagnosis-guided targeted repair against generic feedback-driven revision on the same initially failed bridges with matched resource limits. The scientific target is to determine when small-model supervision helps, when it produces harmful objections, and how evidence availability changes the appropriate intervention. Training is deferred. The specific supervision policy, model pair, test verifier, and numerical budgets must be frozen before experiments.

## 2. 深度阐述 (Deep Dive)

### 2.1 背景与动机 (Background & Motivation)

- **Background:** Executable physical-design agents need to produce structures that perform their specified function under simulation.
- **Core problem:** A failed rollout can reveal symptoms without establishing a unique physical cause. A cheap critic may detect checkable contradictions but misjudge difficult structural effects.
- **Motivation:** Determine whether selective, tool-grounded supervision improves functional repair within limited inference and simulation resources, including when spatial evidence is incomplete.
- **Scope:** Load-bearing bridge repair in the Besiege game simulator. Results will not establish real-world structural safety or manufacturing capability.

### 2.2 相关工作现状 (State of the Art - SOTA)

- [BuildArena](https://arxiv.org/html/2510.16559v7#A4) already evaluates functional construction and studies feedback refinement/analyst agents. Its [source](https://github.com/AI4Science-WestlakeU/BuildArena) is the starting reference.
- [BesiegeField](https://arxiv.org/abs/2510.14980) studies iterative editing, hierarchical workflows, and simulation-reward reinforcement learning.
- [PolyBridgeBench](https://arxiv.org/abs/2609.21493) studies bounded bridge recovery after native simulation failures. Its round accounting differs from our three subsequent repairs.
- [CaLM](https://aclanthology.org/2024.findings-acl.759/) demonstrates small-model verification of larger-model grounded generation outside physical design.
- **Candidate research gap:** Characterize and improve selective supervisory decisions for physical repair as evidence becomes incomplete, while controlling for extra compute and information. This is a research question, not a verified claim of first-of-its-kind novelty.
- Detailed evidence and qualifications: ref/notes/heterogeneous-bridge-repair.md and ref/notes/buildarena-spatial-scaffolding.md.

### 2.3 研究目标 (Research Objectives)

1. Study when the small monitor should trust, question, abstain, or escalate during repair by a stronger designer.
2. Validate a bridge repair loop in the structured-state condition, using simulator-confirmed outcomes rather than appearance or model self-report.
3. Compare targeted repair and generic feedback-driven revision under matched resources, then study selective supervision on paired structured-state and observation-grounded tasks.
4. Separate functional recovery from tool validity, spatial grounding errors, false objections, and additional information/compute effects.

These objectives and the paired evaluation scope were approved by the user during the ideation interview. Additional datasets, task families, baselines, training objectives, or changes to the primary metric require a new user decision.

## 3. 技术实现 (Methodology)

### 3.1 理论基础 (Theoretical Foundation)

The initial study is an inference-time empirical investigation, with no training loss or theorem claimed. The primary measurable quantity is defined in § 4.3. No new loss, formal assumption, or theorem has been written into method.md.

Working hypothesis: evidence checks and selective intervention can make small-model supervision useful at a matched total inference cost. This is falsifiable if supervision fails to improve physical repair or if the apparent benefit is fully explained by extra information or computation.

### 3.2 核心方法 (Proposed Method)

- **Larger designer:** chooses a structural repair and states its predicted physical effect.
- **Small monitor:** audits evidence and execution, with selective intervention rather than unconditional acceptance/rejection.
- **Tools:** report permitted observations, validate action execution, and preserve machine snapshots.
- **Verifier:** a frozen Besiege test determines physical pass/fail independently of the agents.
- **Loop:** observe failure → inspect/check evidence → propose targeted patch → audit and execute → simulate → stop on verified success or after three repair attempts.
- **Concurrency:** independent inspections may run on immutable snapshots; execution and simulation depend on a selected patch and consistent simulator state.
- **Not yet frozen:** evidence-selection algorithm, abstention/escalation rules, action schema, and retry accounting. Their concrete specification belongs in method.md only after the necessary decisions.

### 3.3 基准对比 (Baselines)

- **Approved comparator:** generic feedback-driven revision using the same starting bridges, available evidence, three-repair limit, and matched resource constraints.
- **Approved pilot system:** diagnosis-guided targeted repair with a small evidence-grounded monitor.
- **Proposed additional ablations:** targeted repair without the monitor, ordinary small-model critique, and selective monitoring components. These are needed to isolate the mechanism but their exact run matrix is not yet approved.
- Keep deterministic validity checks identical within each observation condition. Report all inference calls and costs, including rejected patches and monitor work. Equal tokens across different models do not establish equal compute or monetary cost.

## 4. 实验设计 (Experimental Design)

### 4.1 数据集 (Datasets)

Use initially failed load-bearing bridge designs evaluated in Besiege. Exact source, sample count, task version, and split are not yet selected. BuildArena Support Lv.1 is the proposed smallest starting task, not a frozen dataset decision. Training data generation and new task-family construction are deferred pending separate decisions.

### 4.2 实验流程 (Execution Pipeline)

1. **Structured pilot first:** validate loading/resetting, reproducible failure, observation capture, patch execution, and independently verified pass/fail before measuring agent improvements.
2. **Repair comparison:** use the same failed starting designs across approved methods. Freeze verifier, attempt accounting, model versions, and resource limits first.
3. **Paired observation-grounded condition:** reuse the task states while changing observation access. Full state is evaluator-only in the restricted condition; every agent tool must respect the access boundary.
4. **Mechanism evaluation:** proposed ablations and repeated paired runs will separate monitor policy effects from extra evidence and compute.
5. **Spatial controls:** viewpoint changes, physically equivalent scene transformations, and more demanding 3D task variants are proposals to specify after harness validation. Appearance changes and physical difficulty changes must be analyzed separately.
6. **Training:** fine-tuning, process reward modeling, weak-to-strong training, and RL are later-stage options, not part of the first pilot.

### 4.3 评价指标 (Metrics)

- **Primary:** repair success rate within at most three repair attempts (RSR3), among initially failed bridges.

\[
\mathrm{RSR}_{3}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}\{\exists k\leq3:V(\tau_{i,k})=1\}.
\]

N is the number of eligible initially failed bridges; V is the frozen simulation-based pass verifier; tau is the evaluated repaired bridge trajectory. The initial failure evaluation is separate from the three repair attempts. A bridge is counted once if any permitted repair passes. This quantity evaluates recovery; it is not an overall generation success rate.

- **Proposed secondary diagnostics:** all-episode inference cost and latency, supported load, edit size, valid-action rate, grounding errors, false objections, and abstention/escalation behavior.
- **Pre-run choices:** exact load/holding criterion, missing-data and infrastructure-failure policy, accounting for rejected/invalid candidates, repeat count, and numerical budgets remain open.
- **Budget boundary:** no numerical budget has been provided. Follow AGENTS.md escalation limits: no unapproved single run estimated above two GPU hours or five GB of writes. Extra diagnostic rollouts are not free.
- **SOTA comparison:** no target model/score/threshold has been selected; do not compare unlike tasks or declare SOTA improvement. Apply protocol escalation once a comparable target is established.

## 5. 预期效果与影响 (Expected Outcomes)

- **Expected output:** a reproducible repair harness, explicit selective-supervision policy, and measured repair/cost/error trade-offs across observation conditions.
- **Potential contribution:** evidence about when a cheaper supervisor helps or harms a stronger physical-design agent, plus a mechanism whose benefits survive appropriate ablations. These contributions are aspirational until supported by experiments.
- **Negative-result criterion:** if ordinary critique or deterministic checks match the same trade-off, or improvements disappear when compute/evidence is controlled, the proposed mechanism has not established added value.
- **Limits:** game-simulator results and bridge pilot findings do not establish general 3D intelligence or real-world engineering competence.

## 6. Agent 追踪专区 (Agent Traceability)

- **2026-10-12:** User chose beginner mode, repair-agent direction, and load-bearing bridges; primary metric subsequently confirmed as RSR3.
- **2026-10-13:** User approved the generic-revision comparison, small evidence-grounded monitor, deferred training, selective supervision as the central question, and paired observation conditions with the structured condition first.
- **2026-10-13:** 本次立项已过 grill-me 闸门 + 人话闸门. The grill-me interview resolved direction, task category, primary metric, comparator, monitor/training scope, central question, and observation scope. Section 7 was rewritten using .claude/skills/eli5-idea/SKILL.md and stamped in this session.
- **Current bottleneck:** simulator integration and experiment code are not ready; the pass verifier, model pair, failed-bridge source, and numerical budget remain to be selected.
- **Active issue:** DISC-2026W42-001 in Discussion.md. No repair experiment has run.
- **Supporting notes:** ref/notes/heterogeneous-bridge-repair.md; ref/notes/buildarena-spatial-scaffolding.md.

## 7. 人话版 (ELI5)

- **同步戳 (Sync stamp):** `source-hash: 1e09efc4774b` · 更新于 `2026-10-13`

### 7.1 承重的那一句

We are testing whether a cheaper AI inspector can help a stronger AI fix a bridge, while knowing when its own advice is too uncertain to trust.

### 7.2 这个麻烦在现实里长什么样

An AI builds a bridge that looks convincing, but a load placed on it falls. The bridge needs a repair. A second AI says to add a brace, yet it may have confused a hidden connection with a missing one. Following that advice could waste one of the few chances to test a repair.

### 7.3 现在大家怎么办、为什么不够

Existing research already lets AI builders test designs and try again after failure. It also uses AI critics. The open question for this project is when a cheaper inspector's advice actually helps, and when it should ask for better evidence or leave the difficult decision to the stronger builder.

### 7.4 我们的招（一个具体类比）

Think of repairing a shelf with an experienced carpenter and an assistant. The assistant checks measurements, confirms which screw was changed, and notices contradictions. If the back of the shelf is hidden, the assistant asks to inspect it instead of confidently declaring that a screw is missing. The carpenter chooses the repair. We put weight on the shelf to see whether it works.

Our first bridge tests give both AIs clear measurements. Later we use the same tasks with views and permitted inspections, so they must handle incomplete spatial evidence. Both conditions have limited repair chances and resource budgets.

### 7.5 这个类比在哪断

The AIs do not have a carpenter's physical experience. An inspector can misunderstand a measurement, and even a valid edit may not strengthen a bridge. Besiege tests behavior inside a game simulator; passing there does not certify a real bridge. The final judgment therefore comes from a specified simulation test, not either AI's confidence.

### 7.6 真名对照（把正式叫法交回去）

- A repair that actually holds the load: functional correctness.
- A cheaper inspector that checks evidence: small evidence-grounded monitor.
- Knowing when to object, ask, stay uncertain, or call for help: selective supervision.
- Clear machine measurements versus views and permitted inspections: structured-state versus observation-grounded conditions.
- The independent load test: simulation-based verifier.
- Fixing failed bridges within three chances: RSR3.

### 7.7 怎么算赢 & 现在卡在哪

- **Winning:** among the same initially failed bridges, fix more within three repairs at the same total resource budget. For illustration only, fixing 12 of 20 is 60%; fixing 16 is 80%. We must check whether the inspector's decisions caused any improvement.
- **Current obstacle:** simulator integration and experiment code are not ready; we still need to select the load-test rule, models, starting bridges, and spending limit. No repair results exist yet.
