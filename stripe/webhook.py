"""Stripe webhook handler — keeps user subscription tiers in sync."""

from __future__ import annotations

import logging
import os

import stripe
from fastapi import FastAPI, Header, HTTPException, Request
from services.supabase_client import supabase

logger = logging.getLogger(__name__)

app = FastAPI(title="MLO Stripe Webhook", version="1.0.0")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Map Stripe price IDs → plan names defined in .env
_PRICE_TO_PLAN: dict[str, str] = {
    os.getenv("STRIPE_PRO_PRICE_ID", ""): "pro",
    os.getenv("STRIPE_ELITE_PRICE_ID", ""): "elite",
}


def _resolve_plan(price_id: str) -> str:
    return _PRICE_TO_PLAN.get(price_id, "free")


def _upsert_user(email: str, plan: str) -> None:
    supabase.table("users").upsert(
        {"email": email, "plan": plan}, on_conflict="email"
    ).execute()


@app.post("/stripe/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, _WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as exc:
        logger.warning("Invalid Stripe signature: %s", exc)
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type: str = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        email = data.get("customer_email") or data.get("customer_details", {}).get("email")
        price_id = (
            data.get("line_items", {})
            .get("data", [{}])[0]
            .get("price", {})
            .get("id", "")
        )
        if not price_id:
            logger.warning("checkout.session.completed missing price_id; defaulting to free plan")
        if email:
            _upsert_user(email, _resolve_plan(price_id))

    elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
        price_id = data.get("items", {}).get("data", [{}])[0].get("price", {}).get("id", "")
        customer_id = data.get("customer")
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            email = customer.get("email")
            if email:
                _upsert_user(email, _resolve_plan(price_id))

    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer")
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            email = customer.get("email")
            if email:
                _upsert_user(email, "free")

    else:
        logger.debug("Unhandled Stripe event type: %s", event_type)

    return {"status": "ok"}
