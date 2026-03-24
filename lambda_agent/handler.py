from guardrails import validate_action
from tools import sagemaker_tools, s3_tools, cost_tools, compliance_tools, alert_tools

def lambda_handler(event, context):

    action = event.get("action")

    validate_action(action)

    if action == "restart_sagemaker_pipeline":
        return sagemaker_tools.restart_failed_pipelines()

    elif action == "stop_idle_endpoint":
        return sagemaker_tools.stop_idle_endpoints()

    elif action == "check_s3_public_access":
        return s3_tools.check_public_buckets()

    elif action == "generate_cost_report":
        return cost_tools.monthly_cost()

    elif action == "generate_compliance_report":
        return compliance_tools.compliance_report()

    elif action == "send_alert":
        return alert_tools.send_alert(event.get("message"))

    return {"status": "no action"}