ALLOWED_ACTIONS = [
    "restart_sagemaker_pipeline",
    "stop_idle_endpoint",
    "check_s3_public_access",
    "generate_cost_report",
    "generate_compliance_report",
    "send_alert"
]

def validate_action(action):
    if action not in ALLOWED_ACTIONS:
        raise Exception(f"Action {action} not allowed by guardrails")