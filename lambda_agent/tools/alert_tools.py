import json
import urllib3
import os
import logging

logger = logging.getLogger()
http = urllib3.PoolManager()

def send_teams_message(message, action_result=None):
    """Send message to Microsoft Teams via webhook"""
    # Support both variable names to avoid breaking existing Terraform/env setups.
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL") or os.environ.get("TEAMS_WEBHOOK")
    
    if not webhook_url:
        logger.error("Teams webhook env var not set (expected TEAMS_WEBHOOK_URL or TEAMS_WEBHOOK)")
        return False
    
    # MessageCard format (simpler than AdaptiveCard)
    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "Agent Core Alert",
        "themeColor": "0078D4",
        "sections": [
            {
                "activityTitle": "Agent Core Notification",
                "text": message,
                "facts": [
                    {"name": "Status", "value": "Success"},
                    {"name": "Timestamp", "value": json.dumps(action_result) if action_result else "N/A"}
                ]
            }
        ]
    }
    
    try:
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status in [200, 201]:
            logger.info(f"Teams message sent successfully: {response.status}")
            return True
        else:
            logger.error(f"Teams webhook returned: {response.status}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send Teams message: {str(e)}")
        return False
