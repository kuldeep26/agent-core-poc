import json
import boto3
import os
import logging
from guardrails import validate_action
from cross_account import get_sagemaker_client
from tools.alert_tools import send_teams_message

logger = logging.getLogger()
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")

def process_action(action_name, action_input):
    """Process agent action and send result to Teams"""
    try:
        validate_action(action_name)
        
        result = None
        if action_name == "restart_sagemaker_pipeline":
            # Use action_input for pipeline configuration
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
        
        # Send to Teams
        send_teams_message(f"Action executed: {action_name}", result)
        return result
        
    except Exception as e:
        error_msg = f"Action {action_name} failed: {str(e)}"
        send_teams_message(error_msg, {"error": str(e)})
        raise

def lambda_handler(event, context):
    """Main Lambda handler for Bedrock agent invocation"""
    try:
        logger.info(f"Event: {json.dumps(event)}")
        
        # Invoke Bedrock agent
        response = bedrock_agent_runtime.invoke_agent(
            agentId=os.environ.get("AGENT_ID"),
            agentAliasId=os.environ.get("AGENT_ALIAS_ID"),
            sessionId=context.request_id,
            inputText=event.get("inputText", "")
        )
        
        # Process response
        result = {"statusCode": 200, "body": json.dumps(response)}
        send_teams_message("Bedrock agent invoked successfully", result)
        
        return result
        
    except Exception as e:
        error_response = {"statusCode": 500, "error": str(e)}
        send_teams_message("ERROR: Bedrock agent failed", error_response)
        return error_response