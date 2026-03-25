import json
import urllib3
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
http = urllib3.PoolManager()


def _build_facts(action_result):
    facts = [
        {"name": "Timestamp", "value": datetime.now(timezone.utc).isoformat()}
    ]

    if not isinstance(action_result, dict):
        return facts

    status_value = action_result.get("status")
    if status_value:
        facts.insert(0, {"name": "Status", "value": str(status_value)})

    for key, value in action_result.items():
        if key == "status" or value is None:
            continue
        facts.append({"name": key.replace("_", " ").title(), "value": str(value)})

    return facts


def send_teams_message(message, action_result=None):
    """Send message to Microsoft Teams via webhook"""
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL") or os.environ.get("TEAMS_WEBHOOK")

    if not webhook_url:
        logger.error("Teams webhook env var not set (expected TEAMS_WEBHOOK_URL or TEAMS_WEBHOOK)")
        return False

    facts = _build_facts(action_result)

    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "Agent Core Notification",
        "themeColor": "0078D4",
        "sections": [
            {
                "activityTitle": "Agent Core Notification",
                "text": message,
                "facts": facts,
            }
        ],
    }

    try:
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

        if response.status in [200, 201]:
            logger.info("Teams message sent successfully: %s", response.status)
            return True

        logger.error("Teams webhook returned: %s", response.status)
        return False

    except Exception as e:
        logger.error("Failed to send Teams message: %s", str(e))
        return False
