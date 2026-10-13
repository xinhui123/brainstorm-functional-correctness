# BuildArena spatial scaffolding audit and proposed evaluation

Date: 2026-10-13 (Asia/Singapore). Status: code-reading assessment, not experimental results. Selective supervision is the approved central question. The user approved paired structured-state and observation-grounded conditions with structured validation first. Exact observation tools, new task variants, and additional data remain proposals. Agreed scope is recorded in idea.md; method.md has not been modified.

## What the inspected code establishes

Inspected the linked original BuildArena repository on its current main branch through public source pages. This is an exploratory review, not a frozen or exhaustive repository audit; an implementation should pin a commit before reproducing results.

- [prompt.yaml](https://github.com/AI4Science-WestlakeU/BuildArena/blob/main/prompt.yaml): supplies coordinate conventions, block specifications, relative-face blueprint formats, and detailed review instructions. Guidance is instructed to derive building steps from a blueprint.
- [spatial/agent.py](https://github.com/AI4Science-WestlakeU/BuildArena/blob/main/spatial/agent.py): plan calls a model with the task; draft runs model agents; build runs Builder/Guidance with registered tools. The inspected construction path therefore includes model-generated plans rather than an observed hardcoded bridge solution.
- [spatial/build.py](https://github.com/AI4Science-WestlakeU/BuildArena/blob/main/spatial/build.py): Block.caption returns positions and attachable-face information; get_block_details exposes block geometry information; attach_block_to instantiates a block at a selected face; _add_block checks collisions. These tools offload state reporting, placement geometry, and collision checking.
- [levels.yaml](https://github.com/AI4Science-WestlakeU/BuildArena/blob/main/levels.yaml): Support tasks provide explicit gap geometry and loading protocol. Fixed task geometry is a possible template-learning confound; it is not evidence that a solution is directly supplied.

Inference: the inspected pipeline measures tool-assisted symbolic construction and some spatial/physical planning. It does not isolate unaided visual 3D grounding or full scene reconstruction. Coordinates can be legitimate input in engineering design; their presence does not prove that spatial reasoning is absent. A lower-level executor following an earlier model's blueprint is also not the same as an entire system receiving the solution from the evaluator.

## Separate the capabilities before making claims

1. Perception: identify parts and spatial relationships from observations.
2. Geometry and reference frames: reason about orientation, depth, clearance, local/world transformations, and cross-view identity.
3. Physical diagnosis: distinguish observed motion from uncertain load-path or connection hypotheses.
4. Planning: choose a repair, order edits, preserve required structure, and anticipate the intervention's physical effect.
5. Execution: express valid actions and verify that the requested edit occurred.

Functional recovery is our primary outcome, but alone does not identify which capability caused improvement. Image-only failure can be a perception failure rather than a planning failure. A tool could perform the spatial reconstruction while the language model performs physical planning; report this as a system capability unless a controlled ablation attributes it to the model.

## Recommended progression, pending agreement

### A. Preserve structured state as a diagnostic control

Keep exact geometry access and the existing attachment API for initial harness validation. Use this condition to establish repair performance with perception largely controlled. Do not label this unaided visual spatial intelligence.

### B. Add spatially meaningful variation

Vary horizontal scene orientation and position, part identifiers, asymmetric supports, lateral payload offsets, clearance obstacles, and non-coplanar bracing. Hold out geometry/failure families for evaluation. Out-of-plane loads and geometry make depth and lateral stability consequential instead of letting a single planar bridge template suffice.

Random camera orientation and appearance test perception. Re-labeling IDs tests representation dependence. Different spans and payloads change task difficulty and physical demands. These are distinct interventions and should not be pooled as equivalent transformations.

For a physically equivalent scene transformation T (e.g., horizontal translation/yaw of the full task with gravity unchanged), a useful proposed consistency diagnostic is:

\[
\pi(T o) \approx T\pi(o).
\]

This describes action equivariance, not an exact requirement for a stochastic model or a one-to-many repair problem. Compare physical recovery across paired equivalent scenes rather than insisting on identical edits. Arbitrarily tilting a bridge under fixed gravity changes the task; it is not a symmetry control. Rotating only the camera changes the observation but should not rotate a world-frame repair action.

### C. Compare structured and observation-grounded access on paired tasks

Propose two observation conditions on the same bridge states:

- Structured control: exact block positions and connectivity as currently available.
- Observation-grounded condition: calibrated multiple views and rollout frames, task/load specification, permitted measurements, and local inspection queries. Full simulator state remains evaluator-only. Every observation tool must obey the same boundary.

Use object IDs to address actions and a simple validated edit API. Do not force mouse precision to stand in for 3D reasoning. Keep unit/scale information and camera calibration when quantitative estimates are required. Occluded geometry must either be recoverable through an allowed view/inspection or genuinely treated as uncertainty; do not create unanswerable trials and call them reasoning failures.

A sensor-derived point cloud or measured local geometry can be an intermediate condition. Direct simulator extraction of a complete graph or exact point cloud is oracle access even if called a measurement tool. Record acquisition provenance and uncertainty.

## Connection to selective supervision

The candidate question becomes: how should supervision change as spatial evidence becomes incomplete or ambiguous?

Example, not an observed trial: a front view cannot distinguish an absent far-side brace from a brace hidden behind the deck. The monitor can request a rear view, propose a qualified hypothesis, or escalate. A confident veto based only on the front view is inappropriate. The larger designer must still choose whether and where to reinforce the structure.

The supervisor's value is its policy for gathering/checking evidence and controlling objections, not its privileged access to the answer. Keep the permitted evidence sources equal across supervision comparisons; otherwise, attribute the gain to the information advantage. Budget inspections and monitor inference. Any additional physical rollout must be counted; the three-repair-attempt metric does not permit free diagnostic simulations.

Primary remains RSR3. Suggested secondary diagnostics: conditional performance across paired equivalent scenes, grounding errors that affect edits, valid-action rate, false objections, abstention/escalation quality, and total cost. Family-held-out tests and repeated paired runs help distinguish templates from transferable behavior. A score decline under reduced information shows dependence on scaffolding, but by itself does not prove intentional shortcut exploitation.

## Prior work and claim limits

- [BLINK](https://arxiv.org/abs/2404.12390): evaluates visual perception including depth and multi-view tasks. Visual spatial testing is existing work, not a new contribution by itself. Abstract reviewed.
- [RoboSpatial](https://arxiv.org/abs/2411.16537): emphasizes reference frames and grounded spatial relations. Abstract reviewed.

Adding screenshots alone does not establish novelty or real-world validity. Besiege remains a controlled physics-game testbed. A stronger potential contribution is a selective supervisory method plus controlled evidence about its behavior across spatial information regimes; novelty and benefits remain unproven.

## Next ideation decision

The user accepted the paired conditions and structured-first progression on 2026-10-13. The project idea and plain-language explanation are now recorded and synchronized. Next specify the executable test, observation access boundary, model pair, and budget. Spatially varied bridge families remain proposed rather than selected datasets.
