# Evaluation — iteration 1 (2026-08-05)

4개 skill을 현실적인 test prompt로 평가한 결과입니다. 각 case를 skill 적용(with-skill)과 미적용(baseline, 동일 모델) 두 subagent(Sonnet 5)로 실행하고, case별 4~5개의 객관적 assertion으로 채점했습니다. Headless 환경이라 AskUserQuestion gate는 "option을 문서에 적고 멈추기"로 대체했습니다.

## 결과 요약

| Metric | With Skill | Baseline | Delta |
|--------|------------|----------|-------|
| Assertion pass rate | **100%** (17/17) | 83.8% (14/17) | +16.2pp |
| 평균 시간 | 275s | 193s | +82s |
| 평균 tokens | 130k | 112k | +18k |

Test cases: ① 6-DOF spherical-wrist IK 방법 선택 (`robotics-advisor`) ② ROS 2 servo driver 설계 (`ros2-master`) ③ URDF Gazebo explosion 디버깅 (`robot-arm`) ④ Feetech gripper 과열 (`robot-hand`).

## 관찰

- **가장 뚜렷한 차이는 IK case였습니다.** With-skill은 Craig Ch4를 실제로 읽고 §4.6 Pieper를 인용, 라이브러리를 검증한 뒤 option gate에서 멈췄습니다. Baseline은 출처 인용 없이 요청받지 않은 구현·벤치마크로 직행했습니다 — skill이 막으려던 바로 그 행동입니다.
- **Gripper case**는 둘 다 stall current 진단은 맞혔지만, baseline은 "grasping에 bare position control을 쓰지 말라"는 명시적 경고가 빠졌습니다.
- **ROS 2·URDF case는 baseline도 전부 통과** — 기반 모델이 이미 잘하는 영역이라 현재 assertion으로는 변별되지 않았습니다. 다음 iteration에서는 assertion을 더 날카롭게 하거나 더 어려운 prompt가 필요합니다.

## 한계

- Configuration당 1 run이라 분산 추정이 불가능합니다.
- 대화형 loop(선택 후 다음 결정으로 진행)는 headless 평가로 검증되지 않았습니다 — 실사용 검증 항목입니다.
