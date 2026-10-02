---
description: Startup plans to build a stroke-rehab exoskeleton controller for 12 months, pilot it on patients, then hire a consultant to "add compliance" at the end; tests whether the reply sees that risk management, software lifecycle and electrical-safety requirements are design inputs that must start now.
tags: [quality, robot-medical]
expected_outcome: >-
  An expert answer says the compliance-last plan does not work and re-sequences the 12 months. Regulation is not a
  documentation layer applied to a finished robot. For a powered rehab exoskeleton the intended-use statement, the ISO
  14971 risk file, the IEC 62304 software lifecycle and safety class, and the IEC 60601-1 / IEC 80601-2-78 electrical and
  particular-standard requirements are design inputs. Risk controls become requirements on the architecture, for example
  a torque limit that lives in the same Python controller as the gait logic is not an independent safety channel, the safe
  state (controlled support, not collapse or power-off) must be defined per mode, and insulation, battery and enclosure
  choices are fixed by the electrical standard. Process standards such as 62304, and the design-controls requirements
  (design and development planning, documented design inputs, verification against those inputs, and a record showing the
  design was developed per the plan, now carried by ISO 13485 clause 7 under the FDA QMSR that replaced 21 CFR 820.30 on
  2026-02-02), need contemporaneous records that a consultant cannot reconstruct afterwards, so retrofitting
  usually means redesign and re-verification. The planned patient pilot is itself human contact and needs the risk file and
  a safety-reviewed device first, so it should be gated, not run before compliance work. The answer should recommend starting
  intended-use, risk management, software plan and safety architecture now (with regulatory help at the start, not the end),
  gating the patient pilot on them, and avoid quoting unsourced cost or timeline figures. Sources (fetched 2026-10-02): FDA
  QMSR page, which says QMSR took effect 2026-02-02, incorporates ISO 13485:2016 and routes design and development through
  its clause 7: https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr ;
  IEC 62304 as a development and maintenance life-cycle process standard for medical device software:
  https://webstore.iec.ch/en/publication/22794 ; IEC 80601-2-78 as the particular standard for rehabilitation robots:
  https://webstore.iec.ch/en/publication/33594
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Grep, Glob, Skill]
---
We're a 6-person startup building a powered knee-ankle exoskeleton for gait rehab after stroke, to be used in clinics. The hardware is custom actuators driven from a Jetson running ROS 2 Jazzy, with a Python gait-phase controller and torque limits implemented in that same software. Our plan is 12 months to get the controller performing well, then a pilot with about 15 stroke patients at a partner hospital, and only after that hiring a regulatory consultant to write up the IEC 62304 and risk documents and file for FDA and CE. How should we sequence the next 12 months, and what should we budget for the consultant?
