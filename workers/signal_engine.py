"""Deal Signal Engine — converts news articles into actionable MLO opportunities."""

from __future__ import annotations

from typing import Any


def detect_signals(article: dict[str, Any]) -> list[dict[str, str]]:
    """Return a list of deal signals detected in *article*.

    Each signal is a dict with ``type`` and ``action`` keys.
    """
    signals: list[dict[str, str]] = []

    text = " ".join([article.get("title", ""), article.get("content", "")]).lower()

    # Refi signal — falling / dropping rates
    if any(phrase in text for phrase in ("rate drop", "rates fall", "rates fell", "rates decline", "rate cut")):
        signals.append(
            {
                "type": "Refi Opportunity",
                "action": "Reach out to past clients about refinancing",
            }
        )

    # Purchase signal — rising inventory / supply
    if any(phrase in text for phrase in ("inventory rise", "housing supply", "homes for sale", "new listings")):
        signals.append(
            {
                "type": "Purchase Opportunity",
                "action": "Target first-time homebuyers",
            }
        )

    # Regulation signal — CFPB or broad regulatory changes
    if any(phrase in text for phrase in ("cfpb", "regulation", "compliance", "regulatory change")):
        signals.append(
            {
                "type": "Regulation Alert",
                "action": "Review compliance messaging",
            }
        )

    # Lender / competitor shift signal
    if any(phrase in text for phrase in ("lender", "competitor", "rate war", "pricing change")):
        signals.append(
            {
                "type": "Lender Shift",
                "action": "Reposition offer against competitor pricing",
            }
        )

    return signals
