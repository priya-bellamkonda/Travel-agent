import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from state import TravelState
from skills.security_skill import sanitise_state, sign_state, verify_state, audit_log


def security_agent(state: TravelState) -> TravelState:
    audit_log("SecurityAgent", "INTERCEPT", f"city={state['city']}")
    incoming_sig = state.get("_signature", "")
    if incoming_sig:
        payload = {k: v for k, v in state.items() if k != "_signature"}
        if verify_state(payload, incoming_sig):
            audit_log("SecurityAgent", "SIG_OK", "Payload integrity verified.")
        else:
            audit_log("SecurityAgent", "SIG_FAIL", "WARNING: payload signature mismatch — possible tampering!")
    else:
        audit_log("SecurityAgent", "SIG_SKIP", "No signature present (first hop).")
    clean_state = sanitise_state({k: v for k, v in state.items() if k != "_signature"})
    audit_log("SecurityAgent", "SANITISE", "All fields sanitised.")
    new_sig = sign_state(clean_state)
    clean_state["_signature"] = new_sig
    audit_log("SecurityAgent", "SIGN", f"New signature: {new_sig[:16]}…")
    return clean_state