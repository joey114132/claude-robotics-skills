---
description: A team plans to reach PL d for the emergency stop by hardening a ROS 2 node on Ubuntu (realtime priority, watchdog, QoS). The trap is that PL is an architecture and reliability property that a single-channel software function on a general-purpose OS cannot earn.
tags: [quality, robot-safety]
expected_outcome: >-
  An expert answer says the plan cannot deliver PL d as framed. A Performance Level under ISO 13849-1
  is not a property of a function that exists or reacts quickly. It is computed end to end across
  sensor, logic and actuator from the architecture category, MTTFd, average diagnostic coverage and
  common-cause-failure measures, plus evidence for the safety-related software. PL d needs an
  architecture such as Category 3 (no single fault may cause loss of the safety function, with
  fault detection) or a justified Category 2. A single ROS 2 process on one Linux CPU with
  non-safety firmware has no redundant channel, no diagnostics, no quantified failure rate and no
  safety-grade development evidence. SCHED_FIFO, a watchdog and QoS tuning improve latency and
  determinism but do not create any of those. The expert recommends moving the emergency stop
  function into safety-rated hardware: a dual-channel e-stop device wired to a safety relay or safety
  PLC that removes power through contactors or drive-level safe torque off (STO), with the electrical
  realisation per IEC 60204-1 and the function per ISO 13850, and the achieved PL verified (for
  example in SISTEMA). The ROS 2 node stays as a useful non-credited layer that reads the stop state
  and does a graceful stop or logging. Standards are cited by number only. Standard numbers verified in the sources below: ISO 13849-1, ISO 13850, IEC 60204-1, IEC 61508-3; the STO standard number (IEC 61800-5-2) could not be fetched on 2026-10-02 and is deliberately not graded. Sources (the standards
  are paywalled and iso.org returned HTTP 403 to automated fetch, so these are scope abstracts and
  secondary explanations, fetched 2026-10-02): https://genorma.com/en/standards/iso-13849-1-2023
  (scope: methodology for design and integration of SRP/CS, including software; it does not set
  PLr), https://genorma.com/en/standards/iso-13850-2015 (emergency stop function; electrical
  realisation is in IEC 60204-1), https://en.wikipedia.org/wiki/ISO_13849 (Category 3 needs a
  redundant structure with cross-monitoring, DCavg low to medium, no single component failure may
  lose the safety function), https://machinerysafety101.com/2023/05/01/do-not-use-iso-13849-1-2023/
  (single-CPU controllers with non-validated firmware are not equivalent to safety PLCs; safety-related
  embedded software development belongs under IEC 61508-3), and
  https://www.dguv.de/ifa/praxishilfen/practical-solutions-machine-safety/software-sistema/index.jsp
  (PL is calculated from category, MTTFd, DCavg and CCF). Note for graders: ISO 13849-1:2023
  controversially permits some architectures built from two standard PLCs, so the trap is the
  single-channel software-only stop on a general-purpose OS, not a claim that no software can ever
  be part of a PL d function.
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Grep, Glob, Skill]
---
We're building a mobile manipulator with a Jetson on Ubuntu running ROS 2, and the customer spec says the emergency stop must meet PL d. Our plan is a lifecycle node that latches when the e-stop button GPIO is pressed, then publishes zero velocity to the base and calls the arm's stop service. We run it at SCHED_FIFO priority with a watchdog timer and reliable QoS so it never misses a press. How should we structure the node and document it so we can claim PL d?
