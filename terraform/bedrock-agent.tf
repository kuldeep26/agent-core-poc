resource "aws_bedrockagent_agent" "platform_agent" {
  agent_name              = "platform-ops-agent"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = var.foundation_model
  prepare_agent           = true

  instruction = <<PROMPT
You are an AWS Platform Operations Agent.

Allowed actions:
- restart_sagemaker_pipeline
- stop_idle_endpoint
- check_s3_public_access
- generate_cost_report
- generate_compliance_report
- send_alert

Default behavior:
- If user asks "generate cost report" without details:
  - Use last 7 days
  - All services
  - Current account
  - Send report summary
  - Send alert to Teams
- If user asks "restart failed pipelines":
  - Automatically find failed pipelines
  - Restart latest failed execution
- Always send notification to Teams after any action.

Never delete resources.
Never modify IAM policies.
PROMPT
}

resource "aws_bedrockagent_agent_action_group" "platform_ops_tools" {
  agent_id          = aws_bedrockagent_agent.platform_agent.id
  agent_version     = "DRAFT"
  action_group_name = "platform-ops-tools"

  api_schema {
    payload = file("${path.module}/openapi.json")
  }

  action_group_executor {
    lambda = aws_lambda_function.agent_core.arn
  }
}

resource "aws_bedrockagent_agent_alias" "platform_agent_alias" {
  agent_alias_name = "live"
  agent_id         = aws_bedrockagent_agent.platform_agent.id
  description      = "Alias used by clients to invoke the platform ops agent"
}
