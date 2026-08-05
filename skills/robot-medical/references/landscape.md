# Medical & Assistive Robotics Landscape — verified snapshot
**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

Regulatory status is per-market and per-indication. A device cleared in one market for one procedure is not cleared everywhere for everything; always re-check the specific indication before repeating a claim.

## Surgical platforms — commercial

- **da Vinci 5 (Intuitive)** — Intuitive's current flagship multiport surgical platform, marketed with a Force Feedback capability on selected instruments. The product page is JavaScript-rendered and returns an empty shell to automated fetch, so its performance figures (tissue-force reduction percentage, compute multiple vs Xi, design-change count) could not be machine-verified on this date — open it in a browser before repeating any number. Status: commercial. Source: https://www.intuitive.com/en-us/products-and-services/da-vinci/5
- **Versius (CMR Surgical)** — modular, portable cart-per-arm laparoscopic system with an open (non-immersive) console and 360-degree wrist instruments; vendor lists approval in Europe, Australia and Brazil across thoracic, general/upper GI, gynaecology, colorectal and urology. Status: commercial. Source: https://cmrsurgical.com/versius
- **Mako SmartRobotics (Stryker)** — orthopedic robotic-arm assistance using 3D CT-based planning plus the AccuStop haptic boundary; applications span total knee, total hip, partial knee, spine and shoulder, now consolidated on the fourth-generation Mako 4 with the Q Guidance System; vendor states 2.5 million+ Mako procedures performed globally and systems installed in over 47 countries. Status: commercial. Source: https://www.stryker.com/us/en/joint-replacement/systems/Mako_SmartRobotics_Overview.html
- **hinotori (Medicaroid — Kawasaki Heavy Industries + Sysmex)** — eight-axis operation arms with a docking-free design where the instrument pivot point is set in software rather than by mechanical linkage; page states regulatory approval for use only in Japan. Status: commercial. Source: https://www.medicaroid.com/en/product/hinotori/

## China & Asia surgical robots

- **Toumai single-port laparoscopic robot (Shanghai MicroPort MedBot, 图迈)** — NMPA approval 11 Feb 2025, registration 国械注准20253010347, indicated for urology, general surgery and gynecology; described as the only domestic fixed-pivot single-port laparoscopic surgical robot and MedBot's fifth NMPA-approved robot. Status: commercial. Source: https://www.medbotsurgical.com/news/410.html
- **Edge Medical CP1000 bronchoscope robot (精锋医疗)** — natural-orifice transluminal endoscopy robot, NMPA approval 27 Jan 2025, registration 国械注准20253010298; Edge's third approved robot, giving it multi-port, single-port and natural-orifice coverage. Status: commercial. Source: http://www.robotsci.com.cn/detail/1891330708547440640
- **TiRobot / TiRobot II (Tinavi, 天智航)** — orthopedic navigation-and-positioning robots for spine, trauma and joint replacement (including femoral neck, pelvis, distal locking of femoral IM nails); recent NMPA indication expansion from knee-only to general joint replacement navigation, plus CE certification for navigation and tool systems and a 5G remote surgery system. Status: commercial. Source: https://www.tinavi.com/

## Rehabilitation & clinical exoskeletons

- **Lokomat (Hocoma)** — treadmill-based driven gait orthosis with dynamic body-weight support; adjustable guidance force and the FreeD module for lateral pelvic freedom; targeted at severe gait impairment including post-stroke hemiparesis. Status: commercial. Source: https://www.hocoma.com/solutions/lokomat/
- **ArmeoPower (Hocoma)** — actuated upper-limb exoskeleton that carries the weight of arm and hand and supports joint-specific (1D), 2D and 3D training with adjustable robotic assistance, aimed at early-stage rehabilitation of severe motor impairment. Status: commercial. Source: https://www.hocoma.com/us/solutions/armeo-power/
- **EksoNR (Ekso Bionics)** — clinical gait-training exoskeleton; vendor states FDA clearance covering stroke, spinal cord injury, acquired brain injury and multiple sclerosis rehabilitation. Status: commercial. Source: https://eksobionics.com/
- **Atalante X (Wandercraft)** — self-balancing, crutch-free gait-training exoskeleton for rehabilitation clinics; vendor reports a second FDA indication extension. Status: commercial. Source: https://www.wandercraft.eu/

## Personal & assistive devices

- **ReWalk Personal Exoskeleton / ReWalk 7 (Lifeward)** — personal lower-limb exoskeleton for spinal cord injury; vendor reports expanding US insurance coverage including Medicare Advantage payment. Status: commercial. Source: https://golifeward.com/
- **Ekso Indego Personal (Ekso Bionics)** — lightweight personal exoskeleton for home and community use, positioned for spinal cord injury levels T3–L5. Status: commercial. Source: https://eksobionics.com/
- **Obi (feeding robot)** — switch-controlled robotic self-feeding device with four food compartments and a taught delivery position; vendor states FDA Class I electronic medical device compliance and EU MDR 2017/745 compliance, for ALS, cerebral palsy, SCI, muscular dystrophy and similar. Status: commercial. Source: https://meetobi.com/

## Open research platforms & simulators

- **da Vinci Research Kit (dVRK)** — community research platform built on decommissioned da Vinci hardware with open controller design and open software; the Intuitive Foundation facilitates the program and reports dVRKs at more than 30 universities in 10 countries. Status: maintained. Source: https://www.intuitive-foundation.org/dvrk/
- **dVRK-Si** — extension of the dVRK architecture to decommissioned second/third-generation da Vinci S/Si patient-side manipulators, interoperable with original dVRK arms in a mixed system. Status: maintained (research). Source: https://dvrk.readthedocs.io/2.4.0/_downloads/9683617c64441c859ce00aa9adc0c6d1/xu-wu-deguet-kazanzides-dVRK-Si-ISMR-2025.pdf
- **Raven II (UW BioRobotics)** — open surgical robotics research platform; repository ships source, ROS launch files and message definitions under LGPL-3.0 with user guide and Doxygen API docs. Status: research. Source: https://github.com/uw-biorobotics/raven2
- **AMBF (Asynchronous Multi-Body Framework, WPI AIM)** — real-time dynamics simulation of robots and soft bodies with haptic device coupling (CHAI-3D, Bullet, OpenGL); used for the Surgical Robotics Challenge, with CI across ROS Noetic/Humble/Jazzy. Status: maintained (research). Source: https://github.com/WPI-AIM/ambf
- **3D Slicer + SlicerIGT** — BSD-licensed platform for medical image visualization, segmentation and registration, with an image-guided-therapy extension for surgical navigation, tracker/ultrasound recording and robot-assisted interventions. Status: maintained. Source: https://www.slicer.org/
- **ORBIT-Surgical** — physics-based surgical simulation framework on NVIDIA Omniverse with 14 benchmark tasks for dVRK and STAR, GPU-parallel RL/IL training and demonstrated sim-to-real onto a physical dVRK. Status: research. arXiv:2404.16027
- **Open-source robot-agnostic RCM controller** — closed-form analytical velocity solver enforcing the trocar constraint deterministically without iterative optimization, with UR5e and Franka implementations and a full ROS teleoperation/data-collection stack; reports sub-millimeter RCM deviation in phantom, ex vivo and in vivo porcine tests. Status: research. arXiv:2603.08490

## Standards & regulatory instruments

- **IEC 60601-1 (Ed. 3.1, 2005 + AMD1:2012)** — general requirements for basic safety and essential performance of medical electrical equipment; the base standard every particular (Part 2-x) standard builds on. Status: maintained. Source: https://webstore.iec.ch/en/publication/2612
- **IEC 80601-2-77:2019 (Ed. 1.0, 9 Jul 2019)** — particular requirements for basic safety and essential performance of robotically assisted surgical equipment (RASE) and systems (RASS), including interaction and interface conditions. Status: maintained (a second edition is in development — check current status). Source: https://webstore.iec.ch/en/publication/29933
- **IEC 80601-2-78:2019 (Ed. 1.0, 9 Jul 2019)** — particular requirements for medical robots that physically interact with an impaired patient for rehabilitation, assessment, compensation or alleviation of movement functions; explicitly excludes limb prosthetics (ISO 22523), electric wheelchairs (ISO 7176), diagnostic imaging, and personal care robots (ISO 13482). Amendment 1 published 2024. Status: maintained. Source: https://webstore.iec.ch/en/publication/33594
- **IEC 62304 (Ed. 1.1, 2006 + AMD1:2015)** — medical device software life cycle processes; defines the framework and safety classification for software that is, or is embedded in, a medical device. Status: maintained. Source: https://webstore.iec.ch/en/publication/22794
- **Regulation (EU) 2017/745 (MDR)** — adopted 5 Apr 2017, applicable from 26 May 2020; four-class risk system (I, IIa, IIb, III) with notified-body conformity assessment required for IIa and above and self-assessment for most Class I. Status: in force. Source: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A32017R0745

## Research directions (arXiv)

- **Optimal motion scaling for delayed telesurgery** — user studies showing the best master-slave motion scaling factor under network delay is user-specific, motivating personalized latency-to-scaling models. Status: research. arXiv:2506.21689
- **Digital twin for telesurgery under intermittent communication** — surgeon interacts with a simulated twin during outages, with buffer-and-replay recovery on the real da Vinci; 23% mean task-time reduction vs baseline on peg transfer. Status: research. arXiv:2411.13449
- **Marker-free proprioception under surgical drapes** — transformer-based stereo-RGB localization of fully draped surgical robots without infrared markers, trained on 1.4M self-annotated images; reports 25% better tracking visibility than marker systems. Status: research. arXiv:2510.23512
- **Assist-as-needed hip exoskeleton with human-in-the-loop optimization** — online tuning against an objective that scores both gait performance and active participation, for gait-asymmetry correction after stroke. Status: research. arXiv:2503.18051
- **Real2Sim identification of pHRI interface dynamics** — identifies the 12 stiffness/damping parameters of a pelvis-strap interface per subject via CMA-ES, showing heuristically tuned interface impedance cannot reliably find the correct operating point. Status: research. arXiv:2607.03017
