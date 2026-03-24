resource "aws_bedrockagent_agent" "platform_agent" {
  agent_name              = "platform-ops-agent"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = "arn:aws:bedrock:us-east-1:282698011778:application-inference-profile/7f0y5vvjhwb4"

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