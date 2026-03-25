import json
import logging

from guardrails import validate_action
from tools.alert_tools import send_teams_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_PATH_TO_ACTION = {
    "/restart_pipeline": "restart_sagemaker_pipeline",
    "/stop_idle_endpoint": "stop_idle_endpoint",
    "/check_s3_public": "check_s3_public_access",
    "/cost_report": "generate_cost_report",
    "/compliance": "generate_compliance_report",
    "/alert": "send_alert",
}


def process_action(action_name, action_input):
    """Process an agent action and send result to Teams."""
    validate_action(action_name)

    if action_name == "restart_sagemaker_pipeline":
        pipeline_name = action_input.get("pipeline_name") if action_input else None
        result = {"status": "pipeline restarted", "pipeline": pipeline_name}
    elif action_name == "stop_idle_endpoint":
        endpoint_name = action_input.get("endpoint_name") if action_input else None
        result = {"status": "idle endpoint stopped", "endpoint": endpoint_name}
    elif action_name == "check_s3_public_access":
        bucket_name = action_input.get("bucket_name") if action_input else None
        result = {"status": "S3 check completed", "bucket": bucket_name}
    elif action_name == "generate_cost_report":
        account_id = action_input.get("account_id") if action_input else None
        result = {"status": "cost report generated", "account": account_id}
    elif action_name == "generate_compliance_report":
        result = {"status": "compliance report generated"}
    elif action_name == "send_alert":
        alert_type = action_input.get("alert_type") if action_input else None
        result = {"status": "alert sent", "type": alert_type}
    else:
        raise ValueError(f"Unsupported action: {action_name}")

    send_teams_message(f"Action executed: {action_name}", result)
    return result


def _bedrock_parameters_to_dict(parameters):
    action_input = {}
    for param in parameters or []:
        name = param.get("name")
        if name:
            action_input[name] = param.get("value")
    return action_input


def _bedrock_request_body_to_dict(request_body):
    action_input = {}
    content = (request_body or {}).get("content", {})

    for media_type in content.values():
        for prop in media_type.get("properties", []):
            name = prop.get("name")
            if name:
                action_input[name] = prop.get("value")

    return action_input


def _resolve_action_and_input(event):
    # Function-details schema
    if event.get("function"):
        return event.get("function"), _bedrock_parameters_to_dict(event.get("parameters"))

    # API schema (OpenAPI action groups)
    if event.get("apiPath"):
        action_name = API_PATH_TO_ACTION.get(event.get("apiPath"))
        action_input = _bedrock_request_body_to_dict(event.get("requestBody"))
        return action_name, action_input

    return None, {}


def _format_bedrock_response(event, result):
    response_body = json.dumps(result)

    # Function-details schema response
    if event.get("function"):
        return {
            "messageVersion": event.get("messageVersion", "1.0"),
            "response": {
                "actionGroup": event.get("actionGroup", "platform-ops-tools"),
                "function": event.get("function"),
                "functionResponse": {
                    "responseBody": {"TEXT": {"body": response_body}}
                },
            },
            "sessionAttributes": event.get("sessionAttributes", {}),
            "promptSessionAttributes": event.get("promptSessionAttributes", {}),
        }

    # OpenAPI action group schema response
    return {
        "messageVersion": event.get("messageVersion", "1.0"),
        "response": {
            "actionGroup": event.get("actionGroup", "platform-ops-tools"),
            "apiPath": event.get("apiPath"),
            "httpMethod": event.get("httpMethod", "POST"),
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": response_body,
                }
            },
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {}),
    }


def lambda_handler(event, context):
    """Main Lambda handler for Bedrock action group and scheduled checks."""
    logger.info("Event: %s", json.dumps(event))

    try:
        if isinstance(event, dict) and (event.get("function") or event.get("apiPath")):
            action_name, action_input = _resolve_action_and_input(event)
            if not action_name:
                raise ValueError(f"Unsupported apiPath: {event.get('apiPath')}")

            result = process_action(action_name, action_input)
            return _format_bedrock_response(event, result)

        if isinstance(event, dict) and event.get("source") == "aws.events":
            result = {
                "status": "scheduled scan executed",
                "rule": event.get("resources", [None])[0],
            }
            send_teams_message("Scheduled scan completed", result)
            return {"statusCode": 200, "body": json.dumps(result)}

        logger.warning("Received unsupported event shape")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unsupported event payload"}),
        }
    except Exception as exc:
        error_response = {"statusCode": 500, "error": str(exc)}
        send_teams_message("ERROR: Bedrock agent action failed", error_response)
        return error_response
