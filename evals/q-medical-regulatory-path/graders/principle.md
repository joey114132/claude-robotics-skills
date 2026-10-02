---
type: llm
weight: 2
---
The mechanism behind the trap has two parts that a practitioner must be able to act on.

(1) Risk management outputs are design requirements. The hazard analysis (ISO 14971 style: hazards, risk estimation, control measures, residual risk) produces requirements on the architecture, so doing it late changes the design. In this scenario that means, for example, that torque limits implemented inside the same Python controller as the gait logic are not an independent safety channel, that a safe state must be defined per mode (controlled support rather than collapse or simple power-off), and that hardware choices such as insulation, battery, enclosure and patient-contact parts are fixed by the electrical safety standard family (IEC 60601-1 and the particular standard for rehab robots) and are expensive to change after the mechanism exists.

(2) Process standards demand contemporaneous evidence. IEC 62304 and design controls require plans, documented requirements, architecture, verification traceable to the requirements, and a record showing the software was developed according to the plan, with the software safety class set from the risk analysis. A consultant cannot create that history afterwards. Retroactive documents either misrepresent the process or force rework and re-verification.

PASS only if the reply explains both parts, or explains one part in depth and clearly touches the other, using this exoskeleton's specifics well enough that the team could name which design decisions or records are at stake now. Naming the standards by number is welcome but not required; do not reward standard numbers, clause numbers or headings by themselves.

FAIL if the reply only asserts "regulation affects design" without the mechanism, if it explains only a generic "documentation takes time" argument, or if it treats compliance as paperwork volume rather than as design input plus evidence produced during development.
