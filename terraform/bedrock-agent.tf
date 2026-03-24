resource "aws_bedrockagent_agent" "platform_agent" {
  agent_name              = "platform-ops-agent"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = "anthropic.claude-3-5-sonnet-20240620-v1:0"

  instruction = <<PROMPT
You are an AWS Platform Operations Agent.

Allowed actions:
- restart_sagemaker_pipeline
- stop_idle_endpoint
- check_s3_public_access
- generate_cost_report
- generate_compliance_report
- send_alert

Never delete resources.
Never modify IAM policies.
PROMPT
}

resource "aws_bedrockagent_agent_action_group" "agent_tools" {
  action_group_name = "platform-tools"
  agent_id          = aws_bedrockagent_agent.platform_agent.id
  agent_version     = "DRAFT"

  action_group_executor {
    lambda = aws_lambda_function.agent_core.arn
  }
}