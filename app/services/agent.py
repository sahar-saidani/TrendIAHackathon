from typing import Dict

def simple_watchdog_answer(token_id: str, risk_obj: Dict):
    score = risk_obj.get("score", 0)
    label = risk_obj.get("label", "Safe")
    reason = risk_obj.get("reason", "")
    answer = f"Token {token_id} risk: {label} ({score}). Reason: {reason}."
    return {"answer": answer, "score": score, "label": label, "reason": reason}
