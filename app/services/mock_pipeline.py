"""
Mock pipeline adapted to your dataset:
- classify_post(text) -> {"organic_score", "label", "confidence"}
- bot_score_for_post(account_id, text) -> float
- cluster_posts(list_of_posts) -> mapping {post_id: cluster_id}
"""

from typing import Dict, Any, List
import random
import hashlib

def simple_hash_to_float(s: str) -> float:
    h = int(hashlib.sha1(s.encode()).hexdigest()[:8], 16)
    return (h % 1000) / 1000.0

def classify_post(text: str) -> Dict[str, Any]:
    text_l = text.lower()
    suspicious_tokens = ["moon", "pump", "to the moon", "shill", "buy now", "rekt", "moonshot", "partnership", "confirmed"]
    score = 0.85
    for t in suspicious_tokens:
        if t in text_l:
            score -= 0.28
    score -= (simple_hash_to_float(text) - 0.5) * 0.2
    score = max(0.0, min(1.0, score))
    label = "Organic" if score >= 0.55 else "Suspicious"
    return {"organic_score": round(score, 3), "label": label, "confidence": round(abs(score - 0.5) + 0.5, 3)}

def bot_score_for_post(account_id: str, text: str) -> float:
    base = simple_hash_to_float(account_id + text)
    if "bot" in account_id.lower() or "farm" in account_id.lower():
        base = max(base, 0.8)
    # accounts with extremely high posting rate (simulated) should be high; caller may detect via external metadata
    return round(base, 3)

def cluster_posts(posts: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Posts: list of dicts with 'post_id' and 'text'.
    Naive clustering: identical or near-identical texts -> same cluster_id.
    """
    clusters = {}
    mapping = {}
    next_cluster = 1
    for p in posts:
        text = " ".join(p.get("text", "").lower().split())
        # exact text grouping (fast hack for coordinated messages)
        key = text
        if key not in clusters:
            clusters[key] = next_cluster
            next_cluster += 1
        mapping[p["post_id"]] = clusters[key]
    return mapping
