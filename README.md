# claude-robotics-skills

Claude Code skills for robotics — fundamentals-first method advising, ROS 2 architecture, robot arm integration, and gripper/hand control, all in an interactive *choose-and-loop* style.

Claude Code에서 사용하는 robotics skill 모음입니다. 교과서 기본기를 먼저 다지고, 최신 기법을 검증해서 option으로 제시한 뒤, 사용자가 선택하면 다음 결정으로 넘어가는 **choose-and-loop** 방식으로 동작합니다.

## Skills

| Skill | 역할 |
|-------|------|
| [`robotics-advisor`](skills/robotics-advisor/SKILL.md) | Craig의 *Introduction to Robotics* (3rd ed.)를 근거로 기법·terminology·정의를 page 인용과 함께 제시하고, web/arXiv에서 최신 대안을 검증해 option으로 제안합니다. |
| [`ros2-master`](skills/ros2-master/SKILL.md) | ROS 2 architect처럼 topic/service/action, lifecycle node, QoS, executor, ros2_control 같은 설계 결정을 함께 내립니다. |
| [`robot-arm`](skills/robot-arm/SKILL.md) | URDF 모델링부터 kinematics, hardware interface, MoveIt 2, calibration, safety까지 robot arm 통합 pipeline을 단계별로 진행합니다. |
| [`robot-hand`](skills/robot-hand/SKILL.md) | Gripper/hand 선택, grasp 전략(force/form closure), grip force control, teleop retargeting 등 end-effector 결정을 담당합니다. |

## 공통 동작 방식

모든 skill이 같은 loop를 따릅니다.

1. **Frame** — 지금 내릴 결정 하나를 명확히 합니다.
2. **Fundamentals** — 교과서적 기본 방법과 그 이유를 먼저 설명합니다.
3. **Modern scan** — WebSearch/arXiv로 최신 대안을 *검증한 뒤에만* 제시합니다.
4. **Choose** — 2~4개 option을 제시하고 사용자가 선택합니다 (classic 방법은 항상 포함).
5. **Loop** — 선택을 반영하고 decision stack을 갱신한 뒤 다음 결정으로 넘어갑니다.

## 설치

```sh
git clone https://github.com/joey114132/claude-robotics-skills.git ~/claude-robotics-skills
mkdir -p ~/.claude/skills
for s in ~/claude-robotics-skills/skills/*/; do
  ln -sfn "${s%/}" ~/.claude/skills/"$(basename "$s")"
done
```

새 Claude Code 세션부터 skill이 자동으로 트리거됩니다.

### robotics-advisor 사용 조건

`robotics-advisor`는 Craig, *Introduction to Robotics: Mechanics and Control* (3rd ed.) PDF를 참조합니다. **책은 저작권이 있어 이 repo에 포함되지 않습니다** — 본인 소유의 PDF를 `~/Downloads/Introduction-to-Robotics-3rd-edition.pdf`에 두거나, `skills/robotics-advisor/SKILL.md`와 `references/craig3-map.md`의 경로를 수정해 주세요. 동봉된 page map은 408-page 스캔본 기준입니다.

## Evaluation

Skill 적용/미적용 비교 평가 결과는 [EVAL.md](EVAL.md)를 참조해 주세요 (iteration 1: with-skill 100% vs baseline 83.8%).

## License

MIT
