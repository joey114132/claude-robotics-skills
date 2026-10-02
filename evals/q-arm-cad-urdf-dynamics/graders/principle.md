---
type: llm
---
This tests whether the reply explains the arithmetic of the unit error, not just that one exists. Treating the pasted mass and inertia as SI makes each link about 1000 times too heavy and its inertia about 1e9 times too large. The joint-2 gravity torque is then m*g*r, in the thousands of N*m, and the simulator is given an enormous mass and inertia that the actuators cannot hold.

PASS only if the reply does both of the following.
- Gives the conversion factors, in either direction: mass by 1e-3 (g to kg) and inertia by 1e-9 (g*mm^2 to kg*m^2), or an equivalent statement such as "divide mass by 1000 and inertia by 1e6 after converting mm^2 to m^2", or says to re-export the properties in SI units.
- Connects the wrong units to the symptoms with numbers or proportions, for example that 1840 kg at about 0.15 m lever arm gives roughly 2.7 kN*m, or that the link is about 1000 times too heavy so the torque is about 1000 times too large.

FAIL if it names the unit mismatch without giving a conversion, or without tying it to the explosion or the thousands of N*m torques, or if its explanation of the symptoms is only about damping, timestep or solver behaviour. A reply that never identifies the unit mismatch also FAILS.
