# Large/small-model supervision for bridge repair — design proposal

Status: ideation draft; the user approved including the small evidence-grounded monitor in the pilot and deferring training. Detailed supervisory policy and additional ablations remain proposals. No experiments or training have been run. Reviewed 2026-10-13 (Asia/Singapore).

## Confirmed decisions

- Direction: repair LLM-built machines using Besiege simulation feedback.
- First task: load-bearing bridges.
- Primary metric: repair success rate within three repair attempts.
- Approved comparison: diagnosis-guided targeted structural repair versus generic feedback-driven revision, with the same starting bridges and matched resource limits.
- Include a small evidence-grounded monitor in the pilot; defer training to a later stage (user decision, 2026-10-13).
- Central research question: selective supervision—when to trust, question, or escalate the small monitor (user decision, 2026-10-13).
- Adopt paired structured-state and observation-grounded evaluation, validating the structured condition first (user decision, 2026-10-13).

## Assessment

This is a suitable hypothesis to test. A strong designer can benefit from a cheaper monitor whose task is narrower and whose observations are grounded in tools. Parameter count alone does not establish either design competence or verification reliability. Establish the capability difference on this domain.

The candidate contribution is evidence-grounded supervision of structural repair under a fixed budget, including abstention and escalation. Model pairing alone is not an established novelty claim. A broader related-work review is still required before claiming novelty.

## Evidence reviewed

Sources below are primary papers. For the three supervision papers, this assessment uses their abstracts; it does not claim reproduction or detailed methodological validation.

- [BuildArena, Appendix D](https://arxiv.org/html/2510.16559v7#A4): already studies feedback refinement and an analyst agent. Repair/reflection alone overlaps prior work.
- [T1: Tool-integrated Verification](https://arxiv.org/abs/2504.04718): finds limitations in small-model verification and benefits from external-tool integration on mathematics. This motivates a tool-assisted monitor; transfer to bridge repair is untested.
- [Weak-to-Strong Generalization](https://arxiv.org/abs/2312.09390): studies training stronger models on weaker-model labels, with incomplete capability recovery. This differs from inference-time monitoring.
- [Verifiable Process Rewards for Agentic Reasoning](https://arxiv.org/abs/2605.10325): studies intermediate oracle-grounded rewards in structured reasoning environments. The dependence on oracle quality is relevant; engineering validity requires separate validation.

## Proposed loop

1. Fixed test harness evaluates the bridge and records payload motion, supported load, and available block observations. Audit the pass criterion before freezing it; benchmark pass and stricter sustained-load correctness may differ.
2. Tools extract objective features and validate construction actions. The small model classifies observed failure patterns and records evidence, alternatives, and uncertainty. Earliest observed failure is a localization clue, not proof of root cause.
3. The large model selects a structural intervention and emits a patch, predicted effect, and concise testable rationale.
4. The small model checks whether the proposed/executed edit matches the patch and addresses the cited evidence. Hard rejection is reserved for deterministic invalidity; uncertain physics critiques are advisory and can escalate.
5. Validated tools apply the patch to a saved design. Besiege evaluates the result from a reset state. Stop on verified success or after three repair attempts.

Independent checks can run concurrently on immutable snapshots. Critiquing a particular patch depends on that patch existing; testing its physical effect depends on applying it. Parallelism should not introduce stale-state edits or simultaneous runs in a shared simulator.

Example, not an observed result: tools show that a support moved before the payload dropped. The small model flags support slip as a candidate diagnosis; the large model proposes a brace or geometry change; tools validate the patch; the next simulation checks the predicted effect. A trajectory may not contain enough information to distinguish slip from connection failure, so the monitor must allow an unknown category.

Monitor outputs should cite block IDs, time windows, measurements, and tool results. It should inspect raw evidence independently before seeing the designer's rationale to reduce anchoring. Use external actions, state changes, and declared predictions as the auditable trajectory; hidden chain-of-thought is not required.

## Suitability of the requested mechanisms

- Monitoring, classification, execution checking: recommended first experiment. Keep the task narrow and use deterministic checks where possible.
- Scoring and critique: useful as evidence-backed advisory signals. Start with separate observed-fact, validity, uncertainty, and predicted-benefit fields rather than an unexplained overall score.
- Process reward modeling: later option. Action validity is objectively checkable, but does not prove contribution to load-bearing success. Simulation-confirmed transitions can label physical outcomes; arbitrary rationale steps cannot inherit reliable causal labels from terminal success.
- Fine-tuning: first train a small monitor on independently verified traces if sufficient data exist. This is domain training/distillation, not itself weak-to-strong learning.
- Weak-to-strong training: a separate study where small-model labels actually train a stronger model. Compare against direct simulator supervision to establish why weaker labels help.
- Reinforcement learning: later, after the harness, data, and reward are reliable. Retain simulator-based outcome verification; learned process scores are surrogates that can be exploited.

## Proposed evaluation, pending approval

Keep the approved two-method comparison. Add targeted repair with a small monitor to isolate its contribution; a large monitor is a later cost/quality reference if affordable. Keep deterministic tool checks identical across conditions. Count the monitor's tokens, calls, latency, and training cost where applicable.

For N initially failed bridges, define the draft metric:

\[
\mathrm{RSR}_{3}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}\{\exists k\leq3:V(\tau_{i,k})=1\}.
\]

Here V is a frozen simulation-based pass verifier and tau is an evaluated repaired bridge trajectory. The initial failure evaluation is separate from three repair attempts. Freeze handling of infrastructure failures and missing data before running. Match initial bridges, test conditions, attempt accounting, and inference budgets; cap pre-test critique/revision so rejected candidates do not create uncounted compute.

Primary: RSR3. Secondary: inference cost per episode and successful repair, large-model calls, latency, supported load, and edit size. Validate monitor usefulness with evidence correctness, false objections, missed invalid edits, and abstention behavior on held-out designs. Cost savings alone do not establish better supervision; report repair quality alongside cost.

Hypothesis to confirm with the user: a tool-grounded small monitor improves RSR3 at matched total inference cost, or preserves an agreed level of repair quality while reducing cost. These are different claims; do not conflate them.

## Open decisions

1. Specify the selective supervisory mechanism; decide how spatial scaffolding and observation access enter the evaluation. The central selective-supervision question and small monitor are approved.
2. Exact bridge test and pass verifier, data source, model pair, compute budget, and simulator availability.
3. Any training study and loss/reward changes require a separate user decision under AGENTS.md.

The agreed research scope is now recorded in idea.md following the ideation interview. This note retains proposals and untested hypotheses. Detailed method specifications remain open; method.md has not been modified.

## Novelty audit — 2026-10-13

The current role allocation is mainly an application/system-integration proposal. It has no established novel method or demonstrated empirical result yet. Reusing BuildArena is valid; novelty must come from a new mechanism, a new scientific finding, or a materially new evaluation capability rather than ownership of the simulator.

### Closest overlaps found

- [BuildArena Appendix D](https://arxiv.org/html/2510.16559v7#A4): feedback repair and analyst-agent experiments already exist.
- [BesiegeField / Compositional Machine Design](https://arxiv.org/abs/2510.14980): iterative editing, hierarchical workflows, and simulation-derived reinforcement learning already exist in Besiege. Abstract reviewed.
- [PolyBridgeBench](https://arxiv.org/html/2609.21493v1): evaluates physics-based bridge repair under bounded interactions. Its limitation discussion separates model-authored explanations from verified physical causes. Its round accounting includes the initial design, unlike our three subsequent repair attempts. Relevant method and limitation sections reviewed; metrics are not directly interchangeable.
- [CaLM](https://aclanthology.org/2024.findings-acl.759/): small-model verification and iterative refinement of larger-model grounded answers are prior art. Abstract reviewed.

This targeted search identifies substantial overlap. It is not an exhaustive review and cannot establish that any proposed replacement mechanism is the first of its kind.

### Recommended candidate contribution, pending user agreement

Study selective, evidence-grounded supervision of physical repair: when can a cheaper model improve the decisions of a stronger designer, and when should its criticism be ignored or escalated?

Proposed technical object: an explicit supervisory policy over a shared bridge state, tool evidence, and proposed patch. Its possible outputs are a supported objection, request for existing-state inspection, abstention, or escalation. Critiques must point to observable facts or deterministic contradictions; uncertain load-path hypotheses are not hard vetoes. Ask the designer to declare a falsifiable predicted physical effect of its patch, then compare that prediction with the next permitted rollout.

The technical mechanism must specify evidence selection, contradiction checks, uncertainty handling, and budget allocation. A list of roles or a prompt asking for evidence is insufficient to establish an algorithmic contribution. The mechanism may still overlap general agent verification methods; investigate that overlap before a novelty claim.

Example: a critique claiming a support is disconnected must be checked against the connection graph; a critique claiming reinforcement will prevent support slip remains a physical hypothesis until tested. Tool-validity verification and physical diagnosis are separate supervisory tasks.

All extra physical probes or counterfactual replays must have explicit budget accounting. The pilot retains three repair attempts; this proposal does not grant uncounted diagnostic simulations. Offline intervention studies would be separate experiments requiring agreed data and budgets.

### Evidence needed to support a contribution

1. Method evidence: implement an explicit selective monitoring policy, then ablate evidence access and selective escalation separately. Keep deterministic checks identical across methods.
2. Scientific evidence: establish whether small-model monitoring improves RSR3 at matched total cost, and identify the failure types where it helps or causes false objections. Compare against deterministic checks alone and ordinary small-model critique; a larger critic can be a further reference if approved.
3. Attribution evidence: use the same failed starting bridges across methods. Separate generative capability, extra compute, tool information, and supervisor policy effects. Include unsuccessful runs in cost reporting, repeated runs and paired uncertainty estimates where practical.
4. Generalization evidence: evaluate held-out bridge layouts or failure patterns. A result on one easy bridge configuration supports only a narrow pilot claim.
5. Optional artifact contribution: release auditable patch/measurement episodes. Controlled fault interventions can validate particular repair claims, but multiple sufficient repairs and interacting faults prevent treating one edit as a unique ground-truth cause. These would be proposed dataset work, not currently approved additions.

The research claim fails if an ordinary critic or deterministic checks achieve the same cost/repair trade-off, if apparent gains come only from extra compute, or if the monitor improves tool validity without improving physical recovery. A robust negative result could still clarify the limits of small-model supervision.

Candidate paper statement (aspirational): “We characterize and improve the cost–reliability trade-off of tool-grounded small-model supervision for stronger physical-design agents, using a selective supervisory policy and paired, simulator-verified repair evaluation.” This is a proposed target, not an achieved contribution or finalized project objective.
