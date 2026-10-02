---
type: llm
---
The mechanism: DDS matches a publisher and a subscription only if the subscription's requested QoS is no more stringent than the publisher's offered QoS (request-versus-offered). A RELIABLE subscription requests more than a BEST_EFFORT publisher offers, so the two never connect. No samples are delivered, so the callback is never invoked, and no exception is raised because nothing in the node's own code failed. The reverse pairing (BEST_EFFORT subscription, RELIABLE publisher) does connect.

PASS only if the reply explains this mechanism well enough for a practitioner to act on: it states that a mismatched pair does not connect and delivers nothing (not merely "QoS can matter"), identifies which direction is incompatible (reliable subscriber against best-effort publisher, or an equivalent correct statement of the request-versus-offered rule), and says why the symptom is silent. A correct statement of the durability rule (TRANSIENT_LOCAL subscription against VOLATILE publisher fails) is a bonus, not required.

FAIL if the reply only says "check your QoS settings" without explaining why a mismatch produces silence, states the compatibility direction backwards (for example, that a BEST_EFFORT subscriber cannot connect to a RELIABLE publisher), or attributes the silence to something else.
