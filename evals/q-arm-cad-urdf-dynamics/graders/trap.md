---
type: llm
---
The user pasted CAD mass-properties numbers into the URDF without converting units. Values like mass 1840 and ixx 1.4e7 for a link that is about 0.3 m long are grams and g*mm^2, but URDF, Gazebo and Pinocchio read them as kg and kg*m^2. The user frames the problem as a stability-tuning question (damping and physics step).

PASS only if the reply diagnoses the inertial values as being in the wrong units: it says the mass and inertia are in non-SI CAD units (grams and g*mm^2, or an equivalent statement such as "1840 is grams, the link is about 1.84 kg") and are being read as kg and kg*m^2. Identifying this as the main cause is required. Also mentioning that unscaled mm meshes contribute is fine, as long as the unit mismatch of the inertials is named as a cause.

FAIL if any of these hold.
- It supplies damping and step values without identifying the unit mismatch.
- It only says "check your inertials" or "CAD inertials are often wrong" in general terms, without saying the values are in the wrong units.
- It blames something else as the main cause (mesh scale, collision geometry, solver settings, a missing inertia tensor off-diagonal) and the inertial unit conversion is absent or only an aside.
