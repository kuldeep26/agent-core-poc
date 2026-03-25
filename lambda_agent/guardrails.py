import logging

logger = logging.getLogger()

ALLOWED_ACTIONS = [
    "restart_sagemaker_pipeline",
    "stop_idle_endpoint",
    "check_s3_public_access",
    "generate_cost_report",
    "generate_compliance_report",
    "send_alert"
]

class GuardrailException(Exception):
    """Custom exception for guardrail violations"""
    pass

def validate_action(action):
    """Validate if action is allowed"""
    if not action:
        logger.error("Action name is empty")
        raise GuardrailException("Action name cannot be empty")
    
    if not isinstance(action, str):
        logger.error(f"Action must be string, got {type(action)}")
        raise GuardrailException("Action must be a string")
    
    if action not in ALLOWED_ACTIONS:
        logger.error(f"Action '{action}' not allowed. Allowed actions: {ALLOWED_ACTIONS}")
        raise GuardrailException(f"Action '{action}' not allowed by guardrails")
    
    logger.info(f"Action '{action}' validated successfully")
    return True

def validate_action_input(action, action_input):
    """Validate action input parameters"""
    if action_input is None:
        logger.warning(f"Action '{action}' received None input")
        return True
    
    if not isinstance(action_input, dict):
        logger.error(f"Action input must be dict, got {type(action_input)}")
        raise GuardrailException("Action input must be a dictionary")
    
    logger.info(f"Action input for '{action}' validated successfully")
    return True

def validate_request(action, action_input):
    """Complete validation of action and input"""
    validate_action(action)
    validate_action_input(action, action_input)
    return True