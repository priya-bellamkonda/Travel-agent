import re
import json
import hashlib
import time
from typing import Any, Dict, Tuple

# LLM Guard prompt injection scanner 
try:
    from llm_guard.input_scanners import PromptInjection
    from llm_guard.input_scanners.prompt_injection import MatchType
    _scanner = PromptInjection(match_type=MatchType.FULL)
    LLM_GUARD_AVAILABLE = True
except Exception:
    _scanner = None
    LLM_GUARD_AVAILABLE = False

# Config
MAX_FIELD_LENGTH = 8_000
ALLOWED_CITY_PATTERN = re.compile(r"^[A-Za-z\s\-',\.]{2,100}$")
INJECTION_PATTERNS = [
    r"ignore (previous|above|all) instructions",
    r"you are now",
    r"disregard (your|all) (instructions|rules|guidelines)",
    r"act as (a|an)",
    r"jailbreak",
    r"<\s*script",
    r"system\s*prompt",
    r"override (safety|security|guidelines)",
]
COMPILED_INJECTIONS = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

# Helpers

def _regex_injection(text: str) -> bool:
    return any(pat.search(text) for pat in COMPILED_INJECTIONS)


def _llmguard_injection(text: str) -> Tuple[bool, float]:
    """
    Returns (is_injected, risk_score) using LLM Guard.
    Falls back to (False, 0.0) if LLM Guard is not available.
    """
    if not LLM_GUARD_AVAILABLE or _scanner is None:
        return False, 0.0
    try:
        sanitised, is_valid, risk_score = _scanner.scan(text)
        # is_valid=False means injection detected
        return (not is_valid), risk_score
    except Exception:
        return False, 0.0


def _contains_injection(text: str) -> Tuple[bool, str]:
    """
    Combines regex + LLM Guard checks.
    Returns (detected, method_that_detected).
    """
    if _regex_injection(text):
        return True, "regex"
    injected, score = _llmguard_injection(text)
    if injected:
        return True, f"llm_guard(score={score:.2f})"
    return False, ""


def _truncate(value: str, max_len: int = MAX_FIELD_LENGTH) -> str:
    if len(value) > max_len:
        return value[:max_len] + "\n[SECURITY: content truncated]"
    return value


def _sign_payload(payload: Dict[str, Any], secret: str = "langgraph-secret") -> str:
    serialised = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(f"{secret}:{serialised}".encode()).hexdigest()


def _verify_signature(payload: Dict[str, Any], signature: str,
                       secret: str = "langgraph-secret") -> bool:
    return _sign_payload(payload, secret) == signature

# Public API 

def validate_city(city: str) -> Tuple[bool, str]:
    city = city.strip()
    if not city:
        return False, "City name cannot be empty."
    if not ALLOWED_CITY_PATTERN.match(city):
        return False, (
            f"City name '{city}' contains invalid characters. "
            "Only letters, spaces, hyphens, apostrophes, and commas are allowed."
        )
    detected, method = _contains_injection(city)
    if detected:
        return False, f"City name blocked by security check ({method})."
    return True, city.title()


def sanitise_state(state: Dict[str, Any]) -> Dict[str, Any]:
    clean = {}
    for key, value in state.items():
        if isinstance(value, str):
            detected, method = _contains_injection(value)
            if detected:
                value = (
                    f"[SECURITY WARNING: injection detected in '{key}' "
                    f"via {method}]\n" + value
                )
            clean[key] = _truncate(value)
        else:
            clean[key] = value
    return clean


def sign_state(state: Dict[str, Any]) -> str:
    return _sign_payload(state)


def verify_state(state: Dict[str, Any], signature: str) -> bool:
    return _verify_signature(state, signature)


def audit_log(agent_name: str, event: str, detail: str = "") -> None:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"[SECURITY AUDIT] {ts} | agent={agent_name} | event={event} | {detail}")


def llmguard_status() -> str:
    if LLM_GUARD_AVAILABLE:
        return "LLM Guard active (prompt injection scanner loaded)"
    return "LLM Guard not available — regex-only mode"