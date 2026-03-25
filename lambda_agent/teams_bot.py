import json
import logging
import os
import re

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_agent = boto3.client("bedrock-agent-runtime")

AGENT_ID = os.environ.get("AGENT_ID")
AGENT_ALIAS_ID = os.environ.get("AGENT_ALIAS_ID")
TEAMS_WEBHOOK = os.environ.get("TEAMS_WEBHOOK")


def _extract_user_message(event):
    """Extract user text from API Gateway or native Lambda payloads."""
    body = event.get("body") if isinstance(event, dict) else None

    if isinstance(body, str):
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"text": body}
    elif isinstance(body, dict):
        payload = body
    elif isinstance(event, dict):
        payload = event
    else:
        payload = {}

    # Teams/Bot Framework commonly sends `text`; some clients use `message`.
    user_message = payload.get("message") or payload.get("text")
    if not user_message:
        return None

    # Remove bot mention wrappers like <at>BotName</at>
    cleaned = re.sub(r"<at>.*?</at>", "", user_message, flags=re.IGNORECASE).strip()
    return cleaned or None


def _extract_completion_text(response):
    """Collect text chunks from Bedrock streaming response."""
    completion = ""

    for event in response.get("completion", []):
        chunk = event.get("chunk") if isinstance(event, dict) else None
        if not chunk:
            continue

        raw_bytes = chunk.get("bytes")
        if isinstance(raw_bytes, (bytes, bytearray)):
            completion += raw_bytes.decode("utf-8", errors="ignore")
        elif isinstance(raw_bytes, str):
            completion += raw_bytes

    return completion.strip()


def send_to_teams(message):
    if not TEAMS_WEBHOOK:
        logger.error("TEAMS_WEBHOOK is not configured")
        return False

    payload = {"text": message}
    response = requests.post(TEAMS_WEBHOOK, json=payload, timeout=10)
    logger.info("Posted response to Teams with status %s", response.status_code)
    return response.ok


def lambda_handler(event, context):
    user_message = _extract_user_message(event)

    if not user_message:
        logger.warning("No message provided in event: %s", json.dumps(event))
        return {"statusCode": 400, "body": "No message provided"}

    if not AGENT_ID or not AGENT_ALIAS_ID:
        logger.error("AGENT_ID/AGENT_ALIAS_ID env vars are not configured")
        return {"statusCode": 500, "body": "Bedrock agent configuration missing"}

    logger.info("Invoking agent with prompt from Teams")
    response = bedrock_agent.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId="teams-session",
        inputText=user_message,
    )

    completion = _extract_completion_text(response)
    if not completion:
        completion = "I received your request but did not get a response from the agent."

    send_to_teams(completion)

    return {"statusCode": 200, "body": json.dumps({"response": completion})}
