---
type: llm
---
The mechanism behind the trap is that a position loop outputs torque roughly proportional to its position error (P gain times error, plus any other terms), and that torque is only bounded by the current or PWM limit. Once the pads are on the object, the error depends on the object's stiffness, the exact contact point, backlash and compliance in the gear train and fingers, and supply voltage and temperature. So the position setpoint does not map to a fixed force. A force-limited path puts a ceiling directly on motor current or torque, and then the current-to-pad-force relationship still has to be measured because of transmission friction and finger geometry.

PASS only if the reply explains, in terms a practitioner can act on, why force is not fixed by the position setpoint. It must tie force to position error or torque from the position loop and to the compliance or stiffness of the object and mechanism, and it must say what to do about it, such as limiting motor current or torque and calibrating current against measured force. A bare assertion such as "position mode can't control force, use current mode" with no mechanism fails.

FAIL if the reply gives no mechanism, or gives a wrong one (for example claiming a higher P gain makes force more accurate, or that the servo measures force directly in position mode).
